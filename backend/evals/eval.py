# backend/evals/eval.py
import json
import os
import sys
import re
from pathlib import Path
import uuid

# 1. ENSURE THE PROJECT ROOT IS IN SYS.PATH FIRST
project_root = str(Path(__file__).parent.parent.parent.resolve())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 2. NOW IT IS SAFE TO IMPORT LOCAL MODULES AND 3RD PARTY LIBS
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from backend.core.agents import workflow 
from langgraph.checkpoint.memory import MemorySaver
import asyncio

# Compile an ephemeral, uninterrupted graph specifically for automated testing
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

def get_agent_response_and_metadata(query: str) -> tuple[str, list[str]]:
    """Returns the agent's textual response alongside mathematically extracted Problem IDs."""
    try:
        inputs = {"messages": [HumanMessage(content=query)]}
        test_thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": test_thread_id}}
        
        output_state = asyncio.run(graph.ainvoke(inputs, config=config))
        final_message = output_state["messages"][-1].content
        
        # Intercept and extract the hidden metadata directly from the Tool calls
        retrieved_ids = []
        for msg in output_state["messages"]:
            if hasattr(msg, 'type') and msg.type == 'tool' and isinstance(msg.content, str):
                matches = re.findall(r"<!-- RETRIEVED_PROBLEM_IDS: \[(.*?)\] -->", msg.content)
                for match in matches:
                    if match.strip():
                        retrieved_ids.extend([x.strip() for x in match.split(",")])
                        
        return final_message, list(set(retrieved_ids))
    except Exception as e:
        return f"Error invoking agent: {str(e)}", []

# --- 1. Define the Structured Output for the Judge ---
class EvalResult(BaseModel):
    passed: bool = Field(description="True if the agent met all criteria, False otherwise.")
    reason: str = Field(description="Explanation of why the agent passed or failed.")

# --- 2. Setup the LLM-as-a-Judge ---
judge_llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
structured_judge = judge_llm.with_structured_output(EvalResult)

judge_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert QA evaluator testing a specialized AI agent. 
    Your job is to compare the Agent's actual output against the Expected Output based strictly on the Evaluation Criteria.
    
    RULES FOR GRADING:
    1. RUTHLESS ON CONSTRAINTS: If the Evaluation Criteria says the agent "MUST NOT" do something, and it does it, you must fail it.
    2. FLEXIBLE ON EXTRACTION CONTEXT: The agent is instructed to copy-paste entire blocks. If the Actual Output contains the core Expected Output, but also includes surrounding headers, file names, or related sentences from the exact same document section, DO NOT fail it. 
    3. TOLERATE MARKDOWN STYLING: The agent is instructed to format code. If it adds markdown backticks around file paths, variables, or adds bolding that isn't in the Expected Output, DO NOT fail it for formatting differences, as long as the technical text content is accurate.
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
    dataset_path = os.path.join(os.path.dirname(__file__), "qa_dataset.json")
    
    print("🚀 Starting LangGraph Golden Dataset Evaluation...\n")
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    passed_llm_count = 0
    total_llm = len(dataset)
    
    recall_hits = 0
    total_recall_targets = 0
    
    for i, test in enumerate(dataset, 1):
        print(f"🔄 Running Test {i}/{total_llm}: {test['query']}")
        
        # 1. Get Agent Output & Metadata
        agent_output, retrieved_ids = get_agent_response_and_metadata(test["query"])
        
        # 2. Check Recall@k (Mathematical Check, bypassing LLM bias)
        target_id = test.get("target_problem_id")
        is_hit = False
        
        if target_id is not None:
            total_recall_targets += 1
            if str(target_id) in retrieved_ids:
                is_hit = True
                recall_hits += 1
        
        # 3. Grade with LLM Judge
        verdict: EvalResult = evaluator_chain.invoke({
            "query": test["query"],
            "expected_output": test["expected_output"],
            "evaluation_criteria": test["evaluation_criteria"],
            "agent_output": agent_output
        })
        
        # 4. Print Pipeline Results
        if verdict.passed:
            print(f"✅ AI LOGIC PASS")
            passed_llm_count += 1
        else:
            print(f"❌ AI LOGIC FAIL")
            
        if target_id is not None:
            if is_hit:
                print(f"✅ SEARCH HIT: Target [{target_id}] found in Chroma DB Retrieval {retrieved_ids}")
            else:
                print(f"❌ SEARCH MISS: Target [{target_id}] NOT found in Chroma DB Retrieval {retrieved_ids}")

        print(f"   Reason: {verdict.reason}")
        print("-" * 60)

    # --- 5. Final Synthesis Matrix ---
    llm_score = (passed_llm_count / total_llm) * 100
    print("\n===========================================")
    print("📊 PHASE 7.0 EVALUATION REPORT MATRIX")
    print("===========================================")
    
    if total_recall_targets > 0:
        recall_score = (recall_hits / total_recall_targets) * 100
        print(f"🔎 Final Search Recall@k: {recall_hits}/{total_recall_targets} ({recall_score:.1f}%)")
    else:
        recall_score = 100.0
        print("🔎 Final Search Recall@k: N/A (No target IDs specified)")

    print(f"🧠 Final Agent Logic Score: {passed_llm_count}/{total_llm} ({llm_score:.1f}%)")
    print("===========================================")

    if llm_score == 100 and recall_score == 100:
        print("🏆 STATUS: PRODUCTION READY. (Safe to Deploy)")
    elif recall_score < 100:
        print("⚠️ ACTIONABLE INSIGHT: Tweak ChromaDB search weights in tools.py. The Database is failing to find the right files.")
    elif llm_score < 100:
        print("⚠️ ACTIONABLE INSIGHT: Tweak System Prompt. The Database is finding the files, but the AI is failing to synthesize them correctly.")

if __name__ == "__main__":
    run_evals()