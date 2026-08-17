from backend.core.config import fast_llm
from backend.core.fast_path_routes import FAST_PATH_INTERCEPTS
import re

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
            return {"route_category": "RAG"}

    # 2. Default to RAG for Vector Database Retrieval
    print("🔀 [ROUTER] Classified as RAG (Delegating to ChromaDB)")
    return {"route_category": "RAG"}
