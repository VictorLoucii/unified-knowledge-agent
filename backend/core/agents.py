import os
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
import re

from backend.core.config import llm, fast_llm, parse_problem_id, extract_problem_block
from backend.core.tools import tools
from backend.core.semantic_router import route_query, DOMAIN_FILE_MAPPING

llm_with_tools = llm.bind_tools(tools)

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
            SystemMessage(content="You are an input router. Respond with EXACTLY 'OUT_OF_SCOPE' ONLY if the query is explicitly asking about Kubernetes, AWS Lambda, Web scraping, Vue.js, Java Spring Boot, or multiple inheritance in Python. For EVERYTHING else, respond with EXACTLY 'IN_SCOPE'. DO NOT explain."),
            HumanMessage(content=user_msg)
        ])
        if "OUT_OF_SCOPE" in legacy_router.content.upper():
            return "fallback"
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
            "You are the Unified Knowledge Agent. You MUST call `search_knowledge_base` to answer the user's technical questions.\n"
            f"Hint: The query was classified into the domain: {category}. "
            "If the tool returns no results, you may answer from memory, but prioritize the tool results."
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

workflow = StateGraph(State)

workflow.add_node("qa_node", qa_node)
workflow.add_node("fast_path_node", fast_path_node)
workflow.add_node("retrieval_node", retrieval_node)
workflow.add_node("fallback", fallback_node)
workflow.add_node("tools", ToolNode(tools=tools))

workflow.set_conditional_entry_point(
    route_input_node,
    {
        "fast_path_node": "fast_path_node",
        "retrieval_node": "retrieval_node",
        "qa_node": "qa_node",
        "fallback": "fallback"
    }
)

workflow.add_edge("retrieval_node", "qa_node")
workflow.add_conditional_edges("qa_node", tools_condition)
workflow.add_edge("tools", "qa_node")
workflow.add_edge("fast_path_node", END)
workflow.add_edge("fallback", END)
