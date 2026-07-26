from backend.core.config import fast_llm
from backend.core.fast_path_routes import FAST_PATH_INTERCEPTS
from langchain_core.messages import SystemMessage, HumanMessage
import re

# The first batch of specific semantic domains mapped to files
DOMAIN_FILE_MAPPING = {
    "INTERNSHIP_BUGS": "NEXTIER_Internship_Bugs.md",
    "AGENTIC_AI_THEORY": "AgenticAI_Interview_Questions_Theory.md",
    "API_RELATED": "API RELATED.md",
    "REACT_NATIVE_DOCS": "RNjs.docx.md",
    "UNIFIED_KNOWLEDGE": "Unified_Knowledge_Project_Details.md"
}

ROUTER_SYSTEM_PROMPT = """You are an intent classifier. Your job is to classify the user's query into exactly ONE of the following domains:

- INTERNSHIP_BUGS: Queries about specific bug fixes, UI issues, React Native app bugs (like tab underlines, keyboard issues, padding, API errors like invalid_grant).
- AGENTIC_AI_THEORY: Queries about LangGraph, agent memory, semantic firewall, Iron Triangle, AI concepts, etc.
- API_RELATED: Queries about HTTP methods, REST, APIs, web requests.
- REACT_NATIVE_DOCS: Queries about general React Native or JavaScript rules, styling, flatlists, building for emulator, etc.
- UNIFIED_KNOWLEDGE: Queries about the architecture of this knowledge agent, docker setup, or specific agentic AI project issues (like 'Ghost Streaming State' or 'Serialization Crash').
- OUT_OF_SCOPE: Explicitly asking about Kubernetes, AWS Lambda, Web scraping, Vue.js, Java Spring Boot, or multiple inheritance in Python.
- UNKNOWN: If it doesn't clearly fit into any of the above.

You MUST respond with exactly the category name and NOTHING else.
"""

async def route_query(user_query: str) -> dict:
    # 1. Exact Match Intercepts (O(1) lookup)
    for exact_q, fast_data in FAST_PATH_INTERCEPTS.items():
        # Case insensitive exact match or contains logic based on the original override logic
        if exact_q.lower() in user_query.lower():
            print(f"⚡ [ROUTER] Fast-Path Intercept triggered for: {exact_q}")
            return {
                "route_category": "FAST_PATH",
                "fast_path_response": fast_data["output"],
                "fast_path_target_id": fast_data.get("target_id", "")
            }
            
    # Also handle problem ID fast path
    problem_match = re.search(r"(?i)\bproblem\s*:?\s*([A-Za-z0-9_]+)\b", user_query)
    if problem_match:
        from backend.core.config import extract_problem_block
        problem_id = problem_match.group(1)
        block = extract_problem_block(problem_id)
        if block:
            print(f"⚡ [ROUTER] Dynamic Fast-Path triggered for Problem ID: {problem_id}")
            return {
                "route_category": "FAST_PATH",
                "fast_path_response": block,
                "fast_path_target_id": problem_id
            }
        else:
            return {"route_category": "INTERNSHIP_BUGS"}

    # 2. LLM Intent Classification
    try:
        response = await fast_llm.ainvoke([
            SystemMessage(content=ROUTER_SYSTEM_PROMPT),
            HumanMessage(content=user_query)
        ])
        category = response.content.strip().upper()
        
        # Validation
        if category in DOMAIN_FILE_MAPPING or category in ["OUT_OF_SCOPE", "UNKNOWN"]:
            print(f"🔀 [ROUTER] Classified as {category}")
            return {"route_category": category}
        else:
            print(f"⚠️ [ROUTER] Invalid classification: {category}. Defaulting to UNKNOWN.")
            return {"route_category": "UNKNOWN"}
            
    except Exception as e:
        print(f"🚨 [ROUTER] LLM Classification failed: {e}")
        return {"route_category": "UNKNOWN"}
