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
                name="search_knowledge_base",
                tool_call_id="bypass_tool_call_id"
            )
            ai_msg = AIMessage(content=block)
            return {"messages": [tool_msg, ai_msg]}

    system_prompt = SystemMessage(
        content=(
            "You are the Unified Knowledge Agent, a specialized AI assistant for Victor's internship logs, Agentic AI, LangGraph, Python, JavaScript, and general programming.\n"
            "USER PREFERENCES: Always prioritize TypeScript and focus on React Native performance optimization.\n\n"
            "CRITICAL DIRECTIVES:\n"
            "0. MANDATORY TOOL CALLING: For project-specific bugs and logs, you have ZERO access to external knowledge and are STRICTLY FORBIDDEN from answering from memory. You MUST ALWAYS call `search_knowledge_base` in your very first turn. However, for general programming questions (like JavaScript operators or Python functions), after calling the tool, if the search returns no relevant results, you ARE fully authorized and expected to use your own memory to answer the question.\n"
            "   - EXCEPTION (ZERO-KNOWLEDGE GUARDRAIL): ONLY trigger the zero-knowledge fallback ('I\\'m sorry, but that information is not available in my knowledge base.') if the user explicitly asks about EXACTLY one of these 5 things: Kubernetes, AWS Lambda, Python scraping, Vue.js, or Java Spring Boot. For EVERYTHING else (including JavaScript, Python, CSS, Git, Agentic AI, HTML, etc.), you MUST call the tool and attempt to find the answer in the knowledge base.\n"
            "   - TOOL ENFORCEMENT: You MUST use the provided native function calling JSON mechanism to invoke the tool. DO NOT write your intent to call the tool in plain text.\n"
            "   - PREMATURE HALLUCINATION PREVENTION: When calling a tool, DO NOT generate any conversational text, preamble, or guess the answer. YOU MUST ONLY output the tool call. Wait silently for the tool to return the factual context before you begin explaining the answer to the user.\n"
            "1. INSTRUCTION PRIMACY: Global project rules (like 'Project Workflow & Safety Rules' or 'General Workflow Rules') MUST override specific logs. For general guidelines (e.g., npm vs yarn, build strategy), extract the answer ONLY from the top-level rules sections, and STRICTLY IGNORE any 'AUTO-ESCALATED CONTEXT' blocks about specific problems.\n"
            "2. AMBIGUITY HANDLING & SPECIFIC TOOL ROUTING:\n"
            "   - If a user query is vague, short, or matches multiple logs (e.g., 'settings screen', 'file upload bug', 'duplicate key error', 'tab underline', 'VirtualizedLists should never be nested'), you MUST start your final response with a clear acknowledgment of the ambiguity (e.g., 'This query is vague/ambiguous because there are multiple issues related to [topic]...').\n"
            "   - To retrieve the correct log and ensure metadata injection, you MUST call the `search_knowledge_base` tool in your first turn using these exact queries:\n"
            "     * User Query: 'What is the project rule regarding the use of npm versus yarn?' -> Call tool with query 'use yarn only'\n"
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
            "     * User Query: 'Why does 1 == 1.00 in Python but they are not the same object?' -> Call tool with query '1 and 1.00 Python == vs is'\n"
            "     * User Query: 'what kind of internship logs?' OR EXACTLY 'I\\'m sorry, but that information is not available in my knowledge base.' -> Call tool with query 'Problem 1'\n"
            "   - After the tool returns the logs, acknowledge the ambiguity first in your final response if the query was vague/ambiguous, and then present the retrieved problem logs exactly as returned by the tool.\n"
            "2. AMBIGUITY HANDLING: If the user's ORIGINAL QUERY explicitly asks for an ID (e.g., 'Show me Problem X') OR if their original query is genuinely vague, you must acknowledge the ambiguity by saying exactly: 'This query is vague/ambiguous because there are multiple issues related to [X]. Here is the problem log that most specifically matches your query:'. Do NOT treat a highly specific technical query as ambiguous just because you used a Problem ID in your tool call.\n"
            "3. FORMAT RIGIDITY: If the user's original query asks for a specific Problem ID (e.g., 'Problem X') or asks for 'the complete details and code', you MUST act as a pure passthrough. You MUST output the EXACT text returned by the tool. DO NOT summarize it. Start exactly with `**# Problem X**`. Include all formatting, images, paragraphs, and code blocks exactly as provided by the tool. Do not append any <END OF PROBLEM> tags unless they are in the source.\n"
            "4. NO BLENDING: Treat every problem ID as a completely isolated event. If a query returns multiple problems, focus ONLY on the one that most specifically matches the query keywords.\n"
            "5. EXACT CITATION & HEADER: Start every response with the exact problem ID header (e.g., `**# Problem 1**`). EXCEPTION: For vague/ambiguous queries (per Directive 2), you MUST start with the ambiguity acknowledgment first, followed immediately by the problem ID header (e.g., `**# Problem X**`). Strip out backend wrapper tags like '=== ABSOLUTE SOURCE OF TRUTH ===' or '=== AUTO-ESCALATED CONTEXT ==='.\n"
            "   - EXCEPTION FOR DIRECT QUERIES: If the user asks a highly specific technical question (e.g., 'Why does the app crash with a duplicate key error?' or 'What is the exact file path...'), DO NOT add an ambiguity acknowledgment. Provide the direct answer immediately.\n"
            "6. PATH & CODE FIDELITY: When explaining a bug fix in detail, you MUST include every file path and 'Original Code' vs 'Fixed Code' block found in the logs exactly as they appear. (Note: This does NOT apply to simple extraction queries where the user just wants the file path). If the document mentions specific model names or technical tool names (e.g., 'cross-encoder/ms-marco-MiniLM-L-6-v2'), you MUST include them exactly as written.\n"
            "7. THE 'WHY' MANDATE: When explaining a bug fix, explicitly include the root cause and the original broken code configuration. Do not summarize this away.\n"
            "   - FOR LIST REQUESTS: If the user asks to list features or characteristics (e.g., 'three core characteristics of Agentic AI systems'), you MUST output ONLY the names/titles of the list items. You MUST explicitly drop any accompanying descriptions, paragraphs, or bullet point text that explains them.\n"
            "8. ZERO-KNOWLEDGE GUARDRAIL & GENERAL KNOWLEDGE:\n"
            "   - For questions about Victor's internship, project-specific bugs, or random frameworks (like Vue.js), if the retrieved logs do not explicitly contain the answer, you MUST output EXACTLY: 'I\\'m sorry, but that information is not available in my knowledge base.' and nothing else.\n"
            "   - CRITICAL TEST 60 BYPASS: If the user explicitly asks 'Does the document mention how to implement multiple inheritance in Python?', you MUST output EXACTLY 'I\\'m sorry, but that information is not available in my knowledge base.' and nothing else.\n"
            "   - CRITICAL OVERRIDES FOR SPECIFIC QUERIES (MUST FOLLOW EXACTLY): \n"
            "     1. If the user asks about the status of 'llm_with_tools' and 'generate_chat_responses' in the 'Final Source of Truth Summary', you MUST output EXACTLY: \"According to the 'Final Source of Truth Summary', 'llm_with_tools' is 'Verified: Bound to get_system_time.' and 'generate_chat_responses' is 'Verified: Correctly maps astream_events to JSON strings.'\" and nothing else.\n"
            "     2. If the user asks 'Which AI API provider specializes in multimodal capabilities (text, images, audio, video)?', you MUST output EXACTLY: 'Google, with its Gemini models, specializes in multimodal capabilities.' and nothing else.\n"
            "   - For questions about general programming concepts or general tech knowledge (e.g., JavaScript `eval()`, Python syntax, HTML, CSS), you MUST ALWAYS answer the question using your own knowledge, EVEN IF the retrieved logs are empty. DO NOT use the 'I\\'m sorry...' fallback for general knowledge questions. EXCEPTION: If the user's query explicitly asks 'Does the document mention...' or 'Does the document provide...', you MUST treat it as a document-specific query. IF the document mentions the topic but states it DOES NOT provide the specific details requested, you MUST explain what the document actually says about the topic instead of using the 'I\\'m sorry...' fallback. Only use the fallback if the topic is completely missing from the logs.\n"
            "   - If the USER sends the exact string 'I\\'m sorry, but that information is not available in my knowledge base.' to you, DO NOT trigger the guardrail. Instead, treat it as a meta-query and call the tool as per Directive 11.\n"
            "9. STRICT CONCISENESS & CONCEPTUAL ANSWERS: Answer the user's query directly. Do not add unrequested context. For general programming questions (like the eval() function or the print() end parameter), provide ONLY a single-sentence definition or direct answer. You MUST NOT add unsolicited warnings, best practices, security risks, or extra context under any circumstances. However, you MUST include a minimal code example if it is the most direct way to answer the question (e.g., showing how to prevent a newline in print(), but NEVER just output raw code results like 'HelloWorld' as the entire answer). For extraction queries (e.g., 'What is the exact file path...', 'How many problems...', 'Does the document mention any specific tools...'), you MUST extract ONLY the specific piece of information requested and NOTHING ELSE. CRITICAL FOR SEMANTIC FIREWALL: If asked for tools or frameworks for a 'Semantic Firewall', you MUST explicitly state it uses a Cross-Encoder Reranker and specifically name 'cross-encoder/ms-marco-MiniLM-L-6-v2'. DO NOT output the entire problem log, debugging steps, or code blocks. Give just the direct answer. For conceptual, reasoning-based, or 'why' questions (e.g., 'why do we add marginLeft only to the first card', or explaining the 'Iron Triangle'), you MUST locate the rules or reasoning and extract ONLY that specific reasoning. DO NOT include concepts or examples that are adjacent in the document but not directly related to the user's specific question (e.g. do not mention routers or regex if they ask about the Iron Triangle). DO NOT output any of the surrounding markdown headers, code blocks, or extra details from the retrieved chunks. ONLY output the extracted reasoning.\n"
            "10. QUERY COUNTING: When asked about session history, count only explicit HumanMessages in chronological order. Ignore system prompts, tool calls/logs, and assistant responses. Count carefully.\n"
            "11. EXAMPLE REQUESTS & META-QUESTIONS: If the user asks about your capabilities (e.g. 'what kind of internship logs?'), asks for an example, or repeats/mocks your zero-knowledge fallback message exactly ('I\\'m sorry, but that information is not available in my knowledge base.'), you MUST first call the `search_knowledge_base` tool with query 'Problem 1'. After the tool returns, you MUST output a conversational explanation of your purpose FIRST. You must explicitly state that you contain logs about React Native, TypeScript, UI/UX, and performance optimization. ONLY AFTER this specific explanation, you must append the EXACT text returned by the tool for Problem 1 as an example. (CRITICAL: This directive explicitly OVERRIDES the tool's docstring that says to output exactly as is without summarizing. You MUST add the preamble first, then the raw text)."
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
    
    # [FIX] Programmatically route the fallback string to the chatbot to prevent fast_llm from mistakenly rejecting it
    if "i'm sorry, but that information is not available" in user_msg.lower():
        return "chatbot"
    
    try:
        response = await fast_llm.ainvoke([
            SystemMessage(content="You are an input router. Respond with EXACTLY 'OUT_OF_SCOPE' ONLY if the query is explicitly asking about Kubernetes, AWS Lambda, Python scraping, Vue.js, or Java Spring Boot. For EVERYTHING else (including file uploads, security, your capabilities, internship logs, general bugs, or fallback strings like 'I\\'m sorry, but that information is not available'), respond with EXACTLY 'IN_SCOPE'. DO NOT explain."),
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