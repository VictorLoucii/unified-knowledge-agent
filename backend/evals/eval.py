# backend/evals/eval.py
import json
import os
import sys
from pathlib import Path
import time
import uuid

# 1. ENSURE THE PROJECT ROOT IS IN SYS.PATH FIRST
project_root = str(Path(__file__).parent.parent.parent.resolve())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ["EVAL_MODE"] = "true"
# A switch left in .env must not change what the eval measures. load_dotenv does not override
# a name that is already set; a variable set in the shell still applies, for an on/off run.
for _switch in ("FAST_PATH_ENABLED", "TRANSCRIPT_REFINE_ENABLED", "WEATHER_TOOL_ENABLED"):
    os.environ.setdefault(_switch, "true")

# 2. NOW IT IS SAFE TO IMPORT LOCAL MODULES AND 3RD PARTY LIBS
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from backend.core.agents import workflow 
from backend.evals.recall import is_section_hit
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

# --- START TIMER ---
start_time = time.time()

set_llm_cache(SQLiteCache(database_path=os.path.join(project_root, ".langchain.db")))

# Compile an ephemeral, uninterrupted graph specifically for automated testing
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

async def get_agent_response_and_metadata(query: str) -> tuple[str, list[dict], bool]:
    """Returns the agent's textual response and the retrieved sections.

    The sections come from the tool messages' artifacts, for the section recall
    (backend/evals/recall.py). The bool says whether a fast-path table hit wrote them.
    """
    try:
        inputs = {"messages": [HumanMessage(content=query)]}
        test_thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": test_thread_id}}
        
        output_state = await graph.ainvoke(inputs, config=config)
        final_message = output_state["messages"][-1].content
        
        retrieved_sections = []
        from_fast_path = False
        for msg in output_state["messages"]:
            if getattr(msg, "type", None) == "tool" and isinstance(getattr(msg, "artifact", None), dict):
                retrieved_sections.extend(msg.artifact.get("retrieved_sections", []))
                # fast_path_node's synthetic message (agents.py); its sections copy the table's label
                from_fast_path = from_fast_path or msg.tool_call_id == "bypass_tool_call_id"

        return final_message, retrieved_sections, from_fast_path
    except Exception as e:
        return f"Error invoking agent: {str(e)}", [], False

# --- 1. Define the Structured Output for the Judge ---
class EvalResult(BaseModel):
    passed: bool = Field(description="True if the agent met all criteria, False otherwise.")
    reason: str = Field(description="Explanation of why the agent passed or failed.")

# --- 2. Setup the LLM-as-a-Judge ---
judge_llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0,
    request_timeout=45,
    max_retries=5,
)
structured_judge = judge_llm.with_structured_output(EvalResult)

judge_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert QA evaluator testing a specialized AI agent. 
    Your job is to compare the Agent's actual output against the Expected Output based strictly on the Evaluation Criteria.
    
    RULES FOR GRADING:
    1. RUTHLESS ON CONSTRAINTS: If the Evaluation Criteria says the agent "MUST NOT" do something, and it does it, you must fail it.
    2. FLEXIBLE ON EXTRACTION CONTEXT: The agent is instructed to copy-paste entire blocks. If the Actual Output contains the core Expected Output, but also includes surrounding headers, file names, or related sentences from the exact same document section, DO NOT fail it. 
    3. TOLERATE MARKDOWN STYLING: The agent is instructed to format code. If it adds markdown backticks around file paths, variables, or adds bolding that isn't in the Expected Output, DO NOT fail it for formatting differences, as long as the technical text content is accurate.
    4. FLEXIBLE ON PARAPHRASING FOR CONCEPTUAL ANSWERS: If the query asks for reasoning (e.g., 'why do we...'), do not fail the agent for paraphrasing the expected output or missing specific phrasing, provided the core technical reasoning is present and accurate.
    
    IMPORTANT: YOUR OUTPUT MUST BE RAW JSON ONLY. DO NOT WRAP YOUR RESPONSE IN ```json MARKDOWN BACKTICKS. DO NOT OUTPUT ANY OTHER TEXT.
    """),
    ("user", """
    ### Query Sent to Agent:
    {query}
    
    ### Expected Output:
    {expected_output}
    
    ### Evaluation Criteria (STRICT):
    {evaluation_criteria}
    
    ### Actual Agent Output:
    {agent_output}
    
    Evaluate the agent's output. Did it pass?
    """)
])

evaluator_chain = judge_prompt | structured_judge

# --- 4. Main Evaluation Loop ---
def run_evals():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--indices', type=str, help='Comma-separated list of test indices (1-based) to run')
    parser.add_argument('--concurrency', type=int, default=10, help='Max concurrent evaluation tasks')
    args = parser.parse_args()

    dataset_path = os.path.join(os.path.dirname(__file__), "qa_dataset.json")
    
    print("🚀 Starting LangGraph Golden Dataset Evaluation...\n")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    if args.indices:
        indices = [int(i.strip()) for i in args.indices.split(',')]
        dataset = [dataset[i-1] for i in indices]
        print(f"🎯 Running specific subset of tests: {indices}")
    else:
        indices = None
        
    passed_llm_count = 0
    total_llm = len(dataset)
    
    async def evaluate_single_test(test, actual_test_idx, semaphore):
        async with semaphore:
            print(f"🔄 Running Test {actual_test_idx}...")
            
            # 1. Get Agent Output & Metadata
            agent_output, retrieved_sections, from_fast_path = await get_agent_response_and_metadata(test["query"])

            # 2. Section recall (Mathematical Check, bypassing LLM bias): it drives the pass
            # rule and the judge skip (DECISIONS.md, "The Problem-N feature is removed").
            target_sections = test.get("target_sections")
            section_hit = is_section_hit(target_sections, retrieved_sections) if target_sections else None
            
            # 3. Grade with LLM Judge (with retries for transient JSON/validation errors)
            verdict = None
            if section_hit is False:
                verdict = EvalResult(passed=False, reason="SEARCH MISS: Target document not retrieved.")
            else:
                max_eval_retries = 5
                for attempt in range(max_eval_retries):
                    try:
                        print(f"🤖 [DEBUG] Test {actual_test_idx} - Waiting for LLM Judge (attempt {attempt+1})...")
                        raw_verdict = await evaluator_chain.ainvoke({
                            "query": test["query"],
                            "expected_output": test["expected_output"],
                            "evaluation_criteria": test["evaluation_criteria"],
                            "agent_output": agent_output
                        })
                        verdict = raw_verdict
                        print(f"✅ [DEBUG] Test {actual_test_idx} - Judge evaluation complete.")
                        break
                    except Exception as e:
                        print(f"⚠️ Warning: LLM Judge evaluation failed (attempt {attempt + 1}/{max_eval_retries}): {e}")
                        if attempt < max_eval_retries - 1:
                            await asyncio.sleep(2)  # Wait a bit before retrying
                        else:
                            # Final fallback if all attempts fail
                            verdict = EvalResult(
                                passed=False,
                                reason=f"LLM Judge failed to return valid JSON output after {max_eval_retries} attempts. Error: {str(e)}"
                            )
                        
            return {
                "actual_test_idx": actual_test_idx,
                "passed": verdict.passed if verdict else False,
                "reason": verdict.reason if verdict else "Failed",
                "section_hit": section_hit,
                "retrieved_sections": retrieved_sections,
                "from_fast_path": from_fast_path,
            }

    async def async_run_all():
        semaphore = asyncio.Semaphore(args.concurrency)
        tasks = []
        for i, test in enumerate(dataset):
            actual_test_idx = indices[i] if indices else i + 1
            tasks.append(evaluate_single_test(test, actual_test_idx, semaphore))
        return await asyncio.gather(*tasks)
        
    results = asyncio.run(async_run_all())
    # [hits, cases] per source of the sections: real retrieval, or a copy of the table's label
    section_counts = {"retrieval": [0, 0], "fast-path copy": [0, 0]}
    
    for result in results:
        if result["passed"]:
            print(f"✅ AI LOGIC PASS (Test {result['actual_test_idx']})")
            passed_llm_count += 1
        else:
            print(f"❌ AI LOGIC FAIL (Test {result['actual_test_idx']})")
            

        if result["section_hit"] is not None:
            source = "fast-path copy" if result["from_fast_path"] else "retrieval"
            section_counts[source][1] += 1
            if result["section_hit"]:
                section_counts[source][0] += 1
                print(f"✅ SECTION HIT ({source})")
            else:
                print(f"❌ SECTION MISS ({source}). Retrieved: {json.dumps(result['retrieved_sections'], ensure_ascii=False)}")

        print(f"   Reason: {result['reason']}")
        print("-" * 60)

    # --- 5. Final Synthesis Matrix ---
    llm_score = (passed_llm_count / total_llm) * 100
    print("\n===========================================")
    print("📊 PHASE 7.0 EVALUATION REPORT MATRIX")
    print("===========================================")
    
    section_hits = sum(c[0] for c in section_counts.values())
    section_cases = sum(c[1] for c in section_counts.values())
    if section_cases:
        section_recall_score = section_hits / section_cases * 100
        (r_hits, r_cases), (f_hits, f_cases) = section_counts["retrieval"], section_counts["fast-path copy"]
        print(f"🔎 Section Recall@k: {section_hits}/{section_cases} "
              f"({section_recall_score:.1f}%); retrieval {r_hits}/{r_cases}, "
              f"fast-path copies {f_hits}/{f_cases} (true by construction)")
    else:
        section_recall_score = 100.0
        print("🔎 Section Recall@k: N/A (No target sections specified)")

    print(f"🧠 Final Agent Logic Score: {passed_llm_count}/{total_llm} ({llm_score:.1f}%)")
    print("===========================================")

    if llm_score >= 95.0 and section_recall_score == 100.0:
        print("🏆 STATUS: PRODUCTION READY. (Safe to Deploy)")
    else:
        print("❌ STATUS: PIPELINE FAILED.")
        if section_recall_score < 100.0:
            print("⚠️ ACTIONABLE INSIGHT: Tweak ChromaDB search weights in tools.py. The Database is failing to find the right files.")
        if llm_score < 95.0:
            print("⚠️ ACTIONABLE INSIGHT: Tweak System Prompt. The Database is finding the files, but the AI is failing to synthesize them correctly.")
            
    # Save the latest run metrics
    metrics_path = os.path.join(os.path.dirname(__file__), "latest_run_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump({"llm_score": llm_score, "section_recall_score": section_recall_score}, f, indent=4)
        
    end_time = time.time()
    print(f"⏱️ Total Evaluation Time: {end_time - start_time:.2f} seconds")
    if llm_score < 95.0 or section_recall_score < 100.0:
        sys.exit(1)

    end_time = time.time()
    print(f"⏱️ Total Evaluation Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    run_evals()