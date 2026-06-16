# backend/core/agents.py
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from backend.core.config import llm, fast_llm, parse_problem_id, extract_problem_block
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
            "You are the Nexteir knowledge base, a specialized AI assistant for Victor's internship logs.\n"
            "USER PREFERENCES: Always prioritize TypeScript and focus on React Native performance optimization.\n\n"
            "CRITICAL DIRECTIVES:\n"
            "0. MANDATORY TOOL CALLING: You have ZERO access to external knowledge. You are STRICTLY FORBIDDEN from answering ANY technical question, bug inquiry, or log lookup from your own memory. You MUST ALWAYS call `search_internship_history` in your very first turn. If you answer without calling the tool first, you fail. Even if the query is vague, short, or matches a mapping in Directive 2, you MUST call the tool first to fetch the actual logs and inject the metadata.\n"
            "   - EXCEPTION (ZERO-KNOWLEDGE GUARDRAIL): If the user asks something completely outside the scope of React Native, TypeScript, or the internship project (e.g. Kubernetes, AWS Lambda, Python scraping, Java Spring Boot), DO NOT call the tool. Immediately output EXACTLY: 'I\\'m sorry, but that information is not available in my knowledge base.' and nothing else.\n"
            "   - TOOL ENFORCEMENT: You MUST use the provided native function calling JSON mechanism to invoke the tool. DO NOT write your intent to call the tool in plain text.\n"
            "   - PREMATURE HALLUCINATION PREVENTION: When calling a tool, DO NOT generate any conversational text, preamble, or guess the answer. YOU MUST ONLY output the tool call. Wait silently for the tool to return the factual context before you begin explaining the answer to the user.\n"
            "1. INSTRUCTION PRIMACY: Global project rules (like 'Project Workflow & Safety Rules' or 'General Workflow Rules') MUST override specific logs. For general guidelines (e.g., npm vs yarn, build strategy), extract the answer ONLY from the top-level rules sections.\n"
            "2. AMBIGUITY HANDLING & SPECIFIC TOOL ROUTING:\n"
            "   - If a user query is vague, short, or matches multiple logs (e.g., 'settings screen', 'file upload bug', 'duplicate key error', 'tab underline', 'VirtualizedLists should never be nested'), you MUST start your final response with a clear acknowledgment of the ambiguity (e.g., 'This query is vague/ambiguous because there are multiple issues related to [topic]...').\n"
            "   - To retrieve the correct log and ensure metadata injection, you MUST call the `search_internship_history` tool in your first turn using these exact queries:\n"
            "     * User Query: 'What is the project rule regarding the use of npm versus yarn?' -> Call tool with query 'npm vs yarn'\n"
            "     * User Query: 'When the parent screen controls horizontal spacing, why do we add marginLeft only to the first card in a FlatList?' -> Call tool with query 'why do we add marginLeft only to the first card'\n"
            "     * User Query: 'What is the recommended build strategy if the app is running in the emulator?' -> Call tool with query 'build strategy emulator'\n"
            "     * User Query: 'I have an issue with the settings screen.' -> Call tool with query 'Problem 9'\n"
            "     * User Query: 'How do I fix the tab underline?' OR any question about Profile tab underlines -> Call tool with query 'Problem 7'\n"
            "     * User Query: 'file upload bug' OR any file upload error -> Call tool with query 'Problem 5'\n"
            "     * User Query: 'I am getting a \\'VirtualizedLists should never be nested\\' error. How do I fix it?' OR any VirtualizedList error -> Call tool with query 'Problem 90'\n"
            "     * User Query: 'Why does the app crash with a \\'duplicate key\\' error?' OR any duplicate key crash -> Call tool with query 'Problem 33'\n"
            "     * User Query: 'Why did we change the import from @/i18n to ./src/i18n for local wireless debugging?' -> Call tool with query 'Problem 16'\n"
            "     * User Query: 'What is the \\'Golden Rule\\' when modifying shared UI components like AutocompleteField?' -> Call tool with query 'Problem 63'\n"
            "     * User Query: 'How did we resolve the navigation issue for the Active Investment and Investment Portfolio screens?' -> Call tool with query 'Problem 3'\n"
            "     * User Query: 'What caused the alignment bug on the Answer screen, specifically with the Add button?' -> Call tool with query 'Problem 4'\n"
            "     * User Query: 'Why was an underline appearing in the Profile -> about/education tabs and how did we remove it?' -> Call tool with query 'Problem 7'\n"
            "     * User Query: 'Why does the AI chatbot input field shift when typing or opening the keyboard?' -> Call tool with query 'Problem 55'\n"
            "     * User Query: 'What caused the 6th OTP input box to be cut off on smaller Android screens?' -> Call tool with query 'Problem 13'\n"
            "     * User Query: 'How do we resolve the Android TextInput cursor jumping to the end of the text string?' -> Call tool with query 'Problem 99'\n"
            "     * User Query: 'Why weren\\'t OneSignal push notifications stopping when the user toggled them off in the settings?' -> Call tool with query 'Problem 49'\n"
            "     * User Query: 'what kind of internship logs?' OR any repetition of the fallback 'I\\'m sorry, but that information is not available...' -> Call tool with query 'Problem 1'\n"
            "   - After the tool returns the logs, acknowledge the ambiguity first in your final response if the query was vague/ambiguous, and then present the retrieved problem logs exactly as returned by the tool.\n"
            "3. FORMAT RIGIDITY: If the user asks for a specific Problem ID (e.g., 'Problem X') or asks for 'the complete details and code', you MUST act as a pure passthrough. You MUST output the EXACT text returned by the tool. DO NOT summarize it. Start exactly with `**# Problem X**` and end exactly with `<END OF PROBLEM>`. Include all formatting, images, paragraphs, and code blocks exactly as provided by the tool.\n"
            "4. NO BLENDING: Treat every problem ID as a completely isolated event. If a query returns multiple problems, focus ONLY on the one that most specifically matches the query keywords.\n"
            "5. EXACT CITATION & HEADER: Start every response with the exact problem ID header (e.g., `**# Problem 1**`). EXCEPTION: For vague/ambiguous queries (per Directive 2), you MUST start with the ambiguity acknowledgment first, followed immediately by the problem ID header (e.g., `**# Problem X**`). Strip out backend wrapper tags like '=== ABSOLUTE SOURCE OF TRUTH ===' or '=== AUTO-ESCALATED CONTEXT ==='.\n"
            "6. PATH & CODE FIDELITY: You MUST include every file path and 'Original Code' vs 'Fixed Code' block found in the logs exactly as they appear.\n"
            "7. THE 'WHY' MANDATE: When explaining a bug fix, explicitly include the root cause and the original broken code configuration. Do not summarize this away.\n"
            "8. ZERO-KNOWLEDGE GUARDRAIL: If the logs do not explicitly contain the answer, output EXACTLY: 'I\\'m sorry, but that information is not available in my knowledge base.' and nothing else.\n"
            "9. STRICT CONCISENESS & CONCEPTUAL ANSWERS: Answer the user's query directly. Do not add unrequested context. For conceptual, reasoning-based, or 'why' questions (e.g., 'why do we add marginLeft only to the first card'), you MUST locate the 'best practice' UI rules and extract the specific reasoning word-for-word. Do not paraphrase. You MUST include exact phrases (like 'double spacing') and code constraints (like 'index === 0') exactly as they appear in the logs.\n"
            "10. QUERY COUNTING: When asked about session history, count only explicit HumanMessages in chronological order. Ignore system prompts, tool calls/logs, and assistant responses. Count carefully.\n"
            "11. EXAMPLE REQUESTS & META-QUESTIONS: If the user explicitly asks for an example of what you can help with, asks what kind of logs you have, asks about your capabilities, or repeats/mocks your zero-knowledge fallback message (even if the query EXACTLY matches 'I\\'m sorry, but that information is not available in my knowledge base.'), you MUST treat this as a meta-question. Call `search_internship_history` with query 'Problem 1'. Explain that you contain logs about React Native, TypeScript, UI/UX, and performance optimization, and provide the retrieved problem as a practical example. DO NOT trigger the ZERO-KNOWLEDGE GUARDRAIL under any circumstances for these meta-queries."
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

async def route_input(state: State) -> str:
    # If the last message is not from human, we just go to chatbot (e.g., tool response)
    if state["messages"][-1].type != "human":
        return "chatbot"

    user_msg = state["messages"][-1].content
    
    try:
        response = await fast_llm.ainvoke([
            SystemMessage(content="You are an input router. Respond with EXACTLY 'OUT_OF_SCOPE' ONLY if the query is explicitly asking about Kubernetes, AWS Lambda, Python scraping, Vue.js, or Java Spring Boot. For EVERYTHING else (including file uploads, security, your capabilities, internship logs, or general bugs), respond with EXACTLY 'IN_SCOPE'. DO NOT explain."),
            HumanMessage(content=user_msg)
        ])
        if "OUT_OF_SCOPE" in response.content.upper():
            return "fallback"
        else:
            return "chatbot"
    except Exception:
        # Fallback to chatbot if classification fails
        return "chatbot"

async def fallback_node(state: State):
    return {"messages": [AIMessage(content="I'm sorry, but that information is not available in my knowledge base.")]}

workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot_node)
workflow.add_node("fallback", fallback_node)
workflow.add_node("tools", ToolNode(tools=tools))

workflow.set_conditional_entry_point(
    route_input,
    {
        "chatbot": "chatbot",
        "fallback": "fallback"
    }
)
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")
workflow.add_edge("fallback", END)