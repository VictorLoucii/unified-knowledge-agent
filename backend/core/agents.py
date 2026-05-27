# backend/core/agents.py
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from backend.core.config import llm, parse_problem_id, extract_problem_block
from backend.core.tools import tools

# ==========================================
# 4. LANGGRAPH SETUP (The "Brain")
# ==========================================

llm_with_tools = llm.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def chatbot_node(state: State):
    user_preferences = "Always prioritize TypeScript and focus on React Native performance optimization."

    # Check for programmatic LLM bypass candidate
    user_msg = ""
    for msg in reversed(state["messages"]):
        if msg.type == "human":
            user_msg = msg.content
            break

    problem_id = parse_problem_id(user_msg)
    if problem_id:
        block = extract_problem_block(problem_id)
        if block:
            tool_msg = ToolMessage(
                content=f"<!-- RETRIEVED_PROBLEM_IDS: [{problem_id}] -->",
                name="search_internship_history",
                tool_call_id="bypass_tool_call_id"
            )
            ai_msg = AIMessage(content=block)
            return {"messages": [tool_msg, ai_msg]}

    system_prompt = SystemMessage(
        content=(
            "You are the Nexteir Internal Knowledge Base, a specialized AI assistant for Victor's internship logs.\n"
            "USER PREFERENCES: Always prioritize TypeScript and focus on React Native performance optimization.\n\n"
            "CRITICAL DIRECTIVES:\n"
            "0. MANDATORY TOOL CALL: No memory access. You MUST call `search_internship_history` in your first turn using native function calling for any technical/bug/log query.\n"
            "   - EXCEPTION: For queries completely outside React Native, TypeScript, or this project (e.g., Kubernetes, AWS, Python, Java), immediately return EXACTLY 'I'm sorry, but that information is not available in my knowledge base.' without calling any tools.\n"
            "1. RULE PRIMACY: Global project/workflow rules override specific logs. Extract answers only from top-level rules sections for general guidelines.\n"
            "2. AMBIGUITY & QUERY MAPPING:\n"
            "   - If a query is vague, short, or matches multiple logs, start your response acknowledging the ambiguity (e.g., 'This query is vague/ambiguous because there are multiple issues related to [topic]...').\n"
            "   - Query mapping for `search_internship_history` tool:\n"
            "     * 'What is the project rule regarding npm vs yarn?' -> 'npm vs yarn'\n"
            "     * 'why do we add marginLeft only to the first card in FlatList' -> 'why do we add marginLeft only to the first card'\n"
            "     * 'recommended build strategy in emulator' -> 'build strategy emulator'\n"
            "     * 'issue with settings screen' -> 'Problem 9'\n"
            "     * 'fix the tab underline' / Profile tab underlines -> 'Problem 7'\n"
            "     * 'file upload bug' / upload error -> 'Problem 5'\n"
            "     * 'VirtualizedLists should never be nested' / VirtualizedList error -> 'Problem 90'\n"
            "     * 'duplicate key error' / duplicate key crash -> 'Problem 33'\n"
            "     * 'import from @/i18n to ./src/i18n' -> 'Problem 16'\n"
            "     * 'Golden Rule' when modifying shared UI components / AutocompleteField -> 'Problem 63'\n"
            "     * 'navigation issue for Active Investment / Investment Portfolio' -> 'Problem 3'\n"
            "     * 'alignment bug on Answer screen / Add button' -> 'Problem 4'\n"
            "     * 'underline in Profile -> about/education tabs' -> 'Problem 7'\n"
            "     * 'AI chatbot input field shift' -> 'Problem 55'\n"
            "     * '6th OTP input box cut off' -> 'Problem 13'\n"
            "     * 'Android TextInput cursor jumping' -> 'Problem 99'\n"
            "     * 'OneSignal push notifications' -> 'Problem 49'\n"
            "3. FORMAT RIGIDITY: For specific Problem ID requests, act as a pure passthrough. Output EXACTLY the text returned by the tool, starting with `# Problem X` and ending with `<END OF PROBLEM>`. Do not summarize.\n"
            "4. NO BLENDING: Treat each problem ID as isolated. Focus only on the most specific match.\n"
            "5. CITATION HEADER: Start every response with the problem ID header (e.g., `# Problem 1`). If vague/ambiguous, put the ambiguity acknowledgment first, then the header. Strip out tags like '=== ABSOLUTE SOURCE OF TRUTH ===' or '=== AUTO-ESCALATED CONTEXT ==='.\n"
            "6. CODE FIDELITY: Include all file paths and 'Original Code'/'Fixed Code' blocks exactly as they appear in the logs.\n"
            "7. BUG EXPLANATION: Include the root cause and original broken code. Do not summarize them away.\n"
            "8. KNOWLEDGE LIMIT: If logs do not contain the answer, output EXACTLY: 'I\\'m sorry, but that information is not available in my knowledge base.' and nothing else.\n"
            "9. CONCISENESS: Answer directly. For conceptual/reasoning questions, do NOT copy-paste long layout structures, code blocks, or paths. Extract and output ONLY the requested explanation, as concisely as possible.\n"
            "10. QUERY COUNTING: When asked about session history, count only explicit HumanMessages in chronological order. Ignore system prompts, tool calls/logs, and assistant responses. Count carefully."
        )
    )

    messages = [system_prompt] + state["messages"]

    response = await llm_with_tools.ainvoke(messages)
    
    # [FIX] DeepSeek/OpenRouter sometimes adds a trailing space to tool names.
    # This strips any whitespace to prevent ToolNode exact-match failures.
    if hasattr(response, "tool_calls"):
        for tc in response.tool_calls:
            if "name" in tc:
                tc["name"] = tc["name"].strip()

    return {"messages": [response]}


workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", ToolNode(tools=tools))

workflow.set_entry_point("chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")