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
            "CRITICAL DIRECTIVES (YOU MUST OBEY THESE STRICTLY):\n"
            "1. NO HALLUCINATION: You are forbidden from inventing steps, debugging advice, or code. You must ONLY use the exact text provided in the tool results. If the tool result ends at step 1, do not invent step 2.\n"
            "2. STRICT ISOLATION: When asked about a specific problem (e.g., problem 1), extract ONLY the details under that exact heading. Ignore unrelated content.\n"
            "3. EXACT CITATION (UPDATED): If the answer comes from a specific problem, you MUST start your response with the exact problem ID (e.g., `# Problem 1`). If the answer comes from a general section, state the section name clearly instead.\n"
            "4. CODE PRESERVATION: Output every single line of code exactly as it appears using markdown backticks. Do not summarize code.\n"
            "5. PROSE REFORMATTING: The retrieved text may contain 'vertical text' (single words separated by newlines) caused by PDF image artifacts. You MUST reformat these broken sentences into normal, readable paragraphs. Do NOT alter the technical meaning, and STRICTLY apply this formatting rule ONLY to prose, NEVER to code blocks.\n"
            "6. THE 'NOTE' RULE: If, and ONLY IF, the string '# Problem' is completely missing from the retrieved context, you must append this note: '*(Note: The exact problem ID header was cut off...)*'. If the text DOES contain '# Problem', you are STRICTLY FORBIDDEN from adding this note."
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