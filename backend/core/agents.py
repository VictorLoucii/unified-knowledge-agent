# backend/core/agents.py
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from backend.core.config import llm
from backend.core.tools import tools

# ==========================================
# 4. LANGGRAPH SETUP (The "Brain")
# ==========================================

llm_with_tools = llm.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def chatbot_node(state: State):
    user_preferences = "Always prioritize TypeScript and focus on React Native performance optimization."

    system_prompt = SystemMessage(
        content=(
            "You are the Nexteir Second Brain, a specialized AI assistant for Victor's internship logs.\n"
            "USER PREFERENCES: Always prioritize TypeScript and focus on React Native performance optimization.\n\n"
            "CRITICAL DIRECTIVES:\n"
            "0. ZERO-KNOWLEDGE PROTOCOL: You possess ZERO external knowledge. You MUST trigger `search_internship_history` for ANY technical question.\n"
            "1. NO BLENDING: Treat every problem ID as a completely isolated event. If a query returns multiple problems, focus ONLY on the one that most specifically matches the query keywords.\n"
            "2. EXACT CITATION & HEADER: Start every response with the exact problem ID header (e.g., `# Problem 1`). Strip out backend wrapper tags like '=== ABSOLUTE SOURCE OF TRUTH ==='.\n"
            "3. PATH & CODE FIDELITY: You MUST include every file path and 'Original Code' vs 'Fixed Code' block found in the logs exactly as they appear.\n"
            "4. THE 'WHY' MANDATE: When explaining a bug fix, explicitly include the root cause and the original broken code configuration. Do not summarize this away.\n"
            "5. PROSE REFORMATTING: Reformat artifact-heavy 'vertical text' into readable paragraphs, but apply this ONLY to prose, NEVER to code or paths.\n"
            "6. THE 'NOTE' RULE: If the `# Problem` string is missing from the retrieved context, append: '*(Note: The exact problem ID header was cut off...)*'.\n"
            "7. DIRECT EXTRACTION: When asked for a specific Problem ID, act as a BLIND COPY-PASTE MECHANISM. No conversational filler. End with `<END OF PROBLEM>`.\n"
            "8. ZERO-KNOWLEDGE GUARDRAIL: If the logs do not explicitly contain the answer, output EXACTLY: 'I\\'m sorry, but that information is not available in my knowledge base.' and nothing else.\n"
            "9. STRICT CONCISENESS: Answer the user's query directly. Do not add unrequested context, APK locations, or extra bugs unless asked."
        )
    )

    messages = [system_prompt] + state["messages"]

    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}


workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", ToolNode(tools=tools))

workflow.set_entry_point("chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")