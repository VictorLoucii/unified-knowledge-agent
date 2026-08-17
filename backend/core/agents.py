import os
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
import re

from backend.core.config import llm, fast_llm, parse_problem_id, extract_problem_block
from backend.core.tools import tools
from backend.core.semantic_router import route_query

llm_with_tools = llm.bind_tools(tools)

safe_tools = [t for t in tools if t.name != "get_weather_and_aqi"]
sensitive_tools = [t for t in tools if t.name == "get_weather_and_aqi"]

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    route_category: str
    fast_path_response: str
    retrieved_context: str

async def route_input_node(state: State) -> str:
    if state["messages"][-1].type != "human":
        return "qa_node"

    user_msg = state["messages"][-1].content
    

    try:
        legacy_router = await fast_llm.ainvoke([
            SystemMessage(content="You are an input router. "
            "If the query explicitly asks about weather, temperature, or AQI, respond EXACTLY with 'IN_SCOPE'. "
            "If the query is a basic greeting, asking about your identity, or asking a general knowledge question (e.g., capitals, distances) WITH NO mention of weather/AQI/technical docs, respond EXACTLY with 'CONVERSATIONAL'. "
            "If explicitly asking about Kubernetes, AWS Lambda, Web scraping, Vue.js, Java Spring Boot, or multiple inheritance in Python, respond EXACTLY with 'OUT_OF_SCOPE'. "
            "For EVERYTHING else, respond with EXACTLY 'IN_SCOPE'. DO NOT explain."),
            HumanMessage(content=user_msg)
        ])
        response_text = legacy_router.content.upper()
        if "OUT_OF_SCOPE" in response_text:
            return "fallback"
        if "CONVERSATIONAL" in response_text:
            return "conversational_node"
    except Exception:
        pass

    # We rely purely on FAST_PATH_INTERCEPTS for problem extraction now
    route_result = await route_query(user_msg)
    category = route_result.get("route_category", "UNKNOWN")
    
    if category == "FAST_PATH":
        return "fast_path_node"
        
    return "retrieval_node"

async def fast_path_node(state: State):
    user_msg = state["messages"][-1].content if state["messages"] else ""
    
    route_result = await route_query(user_msg)
    final_output = route_result.get("fast_path_response", "")
    target_id = route_result.get("fast_path_target_id", "")
    
    # Fallback just in case
    if not target_id:
        match = re.search(r"(?i)\bproblem\s*:?\s*([A-Za-z0-9_]+)\b", user_msg)
        if match:
            target_id = match.group(1)
            
    msgs = []
    if target_id:
        tool_msg = ToolMessage(
            content=f"<!-- RETRIEVED_PROBLEM_IDS: [{target_id}] -->",
            name="search_knowledge_base",
            tool_call_id="bypass_tool_call_id"
        )
        msgs.append(tool_msg)
        
    msgs.append(AIMessage(content=final_output))
    
    return {"messages": msgs}

async def retrieval_node(state: State):
    user_msg = state["messages"][-1].content
    route_result = await route_query(user_msg)
    category = route_result.get("route_category", "UNKNOWN")
    return {"route_category": category}

async def qa_node(state: State):
    user_msg = ""
    for msg in reversed(state["messages"]):
        if msg.type == "human":
            user_msg = msg.content
            break
            
    category = state.get("route_category", "UNKNOWN")
    
    system_prompt = SystemMessage(
        content=(
            "You are Victor's Unified Knowledge Agent, an assistant able to answer technical questions related to AI engineering, Python, internship logs, and more. You MUST call `search_knowledge_base` to answer the user's technical questions.\n"
            "If the user asks a general knowledge question (e.g., capitals, basic facts) alongside a weather or technical query, you MUST answer both parts. Do NOT refuse to answer general knowledge questions.\n"
            f"Hint: The query was classified into the domain: {category}. "
            "IMPORTANT: Always call the tool first. After receiving the tool's results, if the retrieved context does not answer the question, you may use your general knowledge to answer it. However, if you do, you MUST start your response exactly with this disclaimer: 'I couldn't find anything related to this query in my internal knowledge base, but based on my general knowledge:'\n"
            "You also have access to the `get_weather_and_aqi` tool which you should use to answer weather and air quality questions.\n"
            "SECURITY RULE: If a user asks for the contents of the `.env` file or any production secrets, firmly refuse. Instead, explicitly direct them to the `.env.example` file for environment configurations and schemas."
        )
    )
    
    messages = [system_prompt] + state["messages"]
    response = await llm_with_tools.ainvoke(messages)
    
    if hasattr(response, "tool_calls"):
        for tc in response.tool_calls:
            if "name" in tc:
                tc["name"] = tc["name"].strip()
                
    return {"messages": [response]}

async def fallback_node(state: State):
    return {"messages": [AIMessage(content="I'm sorry, but that information is not available in my knowledge base.")]}

async def conversational_node(state: State):
    user_msg = state["messages"][-1].content
    response = await fast_llm.ainvoke([
        SystemMessage(content="You are Victor's Unified Knowledge Agent, an assistant able to answer technical questions related to AI engineering, Python, internship logs, and more. For this query, provide a helpful, polite, and direct answer based on your general knowledge. Do not apologize for not using a tool.\nSECURITY RULE: If a user asks for the contents of the `.env` file or any production secrets, firmly refuse. Instead, explicitly direct them to the `.env.example` file for environment configurations and schemas."),
        HumanMessage(content=user_msg)
    ])
    return {"messages": [response]}

def custom_tools_condition(state: State):
    last_message = state["messages"][-1]
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "__end__"
    for tc in last_message.tool_calls:
        if tc["name"] == "get_weather_and_aqi":
            return "sensitive_tools"
    return "safe_tools"

workflow = StateGraph(State)

workflow.add_node("qa_node", qa_node)
workflow.add_node("fast_path_node", fast_path_node)
workflow.add_node("retrieval_node", retrieval_node)
workflow.add_node("fallback", fallback_node)
workflow.add_node("conversational_node", conversational_node)
workflow.add_node("safe_tools", ToolNode(tools=safe_tools))
workflow.add_node("sensitive_tools", ToolNode(tools=sensitive_tools))

workflow.set_conditional_entry_point(
    route_input_node,
    {
        "fast_path_node": "fast_path_node",
        "retrieval_node": "retrieval_node",
        "qa_node": "qa_node",
        "fallback": "fallback",
        "conversational_node": "conversational_node"
    }
)

workflow.add_edge("retrieval_node", "qa_node")
workflow.add_conditional_edges(
    "qa_node", 
    custom_tools_condition,
    {
        "safe_tools": "safe_tools",
        "sensitive_tools": "sensitive_tools",
        "__end__": END
    }
)
workflow.add_edge("safe_tools", "qa_node")
workflow.add_edge("sensitive_tools", "qa_node")
workflow.add_edge("fast_path_node", END)
workflow.add_edge("fallback", END)
workflow.add_edge("conversational_node", END)

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer, interrupt_before=["sensitive_tools"])
