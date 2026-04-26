# backend/evals/eval.py
import json
import os
import sys
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

def get_agent_response(query: str) -> str:
    try:
        inputs = {"messages": [HumanMessage(content=query)]}
        
        # Generate a truly unique ID for this specific test
        test_thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": test_thread_id}}
        
        # Use asyncio.run to execute the async graph in our synchronous eval loop
        output_state = asyncio.run(graph.ainvoke(inputs, config=config))
        
        return output_state["messages"][-1].content
    except Exception as e:
        return f"Error invoking agent: {str(e)}"

# --- 1. Define the Structured Output for the Judge ---
class EvalResult(BaseModel):
    passed: bool = Field(description="True if the agent met all criteria, False otherwise.")
    reason: str = Field(description="Explanation of why the agent passed or failed.")

# --- 2. Setup the LLM-as-a-Judge ---
# Using gpt-4o as the judge because it is excellent at following strict instructions
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
        
    passed_count = 0
    total = len(dataset)
    
    for i, test in enumerate(dataset, 1):
        print(f"🔄 Running Test {i}/{total}: {test['query']}")
        
        # 1. Get Agent Output
        agent_output = get_agent_response(test["query"])
        
        # 2. Grade with Judge
        verdict: EvalResult = evaluator_chain.invoke({
            "query": test["query"],
            "expected_output": test["expected_output"],
            "evaluation_criteria": test["evaluation_criteria"],
            "agent_output": agent_output
        })
        
        # 3. Print Results
        if verdict.passed:
            print(f"✅ PASS")
            passed_count += 1
        else:
            print(f"❌ FAIL")
            
        print(f"   Reason: {verdict.reason}")
        print("-" * 60)

    # --- 5. Final Score ---
    score = (passed_count / total) * 100
    print(f"\n🎯 Final Evaluation Score: {passed_count}/{total} ({score:.1f}%)")
    if score == 100:
        print("🏆 Congratulations! Your LangGraph Agent is Production-Ready.")
    else:
        print("⚠️ Your agent failed some strict constraints. Review the reasons above and tweak your system prompt or tools.")

if __name__ == "__main__":
    run_evals()