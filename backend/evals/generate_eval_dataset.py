import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Ensure the project root is in sys.path
project_root = str(Path(__file__).parent.parent.parent.resolve())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables
load_dotenv(os.path.join(project_root, ".env"))

from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# 1. Define the Schema for Test Cases
class TestCase(BaseModel):
    query: str = Field(description="The question to ask the agent. Include Direct Retrieval, Cross-Document Reasoning, Ambiguous Queries, and Negative Constraints.")
    expected_output: str = Field(description="The exact expected answer or critical reasoning the agent must output.")
    evaluation_criteria: str = Field(description="Strict rules for the LLM judge to grade this response.")
    target_problem_id: Optional[int] = Field(description="The integer Problem ID if this question refers to a specific known problem, otherwise null.")

class TestCaseList(BaseModel):
    test_cases: List[TestCase] = Field(description="List of generated test cases.")

# 2. Setup the LLM Client pointing to OpenRouter
# Using ChatOpenAI as an interface to OpenRouter
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Error: OPENROUTER_API_KEY is not set in the .env file.")
    sys.exit(1)

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="google/gemini-2.5-flash",
    temperature=0.2
)

parser = PydanticOutputParser(pydantic_object=TestCaseList)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an expert QA engineer building an evaluation dataset for an AI assistant.
Your goal is to generate high-variance test cases based on the provided document text.

The test cases MUST cover the following types of queries:
1. Direct Retrieval: Finding specific facts/numbers hidden deep in the text.
2. Cross-Document Reasoning (if applicable): Synthesizing context from the document.
3. Ambiguous/Synonym Queries: Testing vector embedding quality using synonyms.
4. Negative Constraints: Questions about things *not* in the text to test hallucination resistance (the expected output should state the information is not available).

Generate between 6 to 8 test cases.
Format your output strictly according to the requested JSON schema.
"""),
    ("human", "Here is the document content (from {file_name}):\n\n{document_text}\n\n{format_instructions}")
])

chain = prompt_template | llm | parser

def main():
    data_dir = os.path.join(project_root, "data")
    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found at {data_dir}")
        sys.exit(1)

    # 3. Find and sort .md files by size (descending)
    md_files = []
    for f in os.listdir(data_dir):
        if f.endswith(".md"):
            file_path = os.path.join(data_dir, f)
            size = os.path.getsize(file_path)
            md_files.append((file_path, size, f))
    
    md_files.sort(key=lambda x: x[1], reverse=True)
    
    # 4. Strict Constraint: Process the first 3 largest files to recover lost tests
    target_files = md_files[:3]
    print(f"Found {len(md_files)} Markdown files. Processing first 3 largest files:")
    for path, size, name in target_files:
        print(f" - {name} ({size / 1024:.2f} KB)")
        
    all_test_cases = []
    
    for file_path, size, file_name in target_files:
        print(f"\nProcessing {file_name}...")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Truncate content if it's excessively large to avoid context limit blowouts.
        max_chars = 100000
        if len(content) > max_chars:
            print(f"  Warning: File is very large ({len(content)} chars). Truncating to first {max_chars} chars for test generation.")
            content = content[:max_chars]
            
        try:
            print("  Invoking LLM to generate test cases...")
            result = chain.invoke({
                "file_name": file_name,
                "document_text": content,
                "format_instructions": parser.get_format_instructions()
            })
            
            # Append generated test cases to our main list
            if result and result.test_cases:
                all_test_cases.extend([tc.model_dump() for tc in result.test_cases])
                print(f"  Successfully generated {len(result.test_cases)} test cases.")
            else:
                print("  LLM returned an empty list of test cases.")
                
        except Exception as e:
            print(f"  Error generating test cases for {file_name}: {e}")

    # 5. Output to draft_qa_dataset.json
    output_path = os.path.join(project_root, "backend", "evals", "draft_qa_dataset.json")
    print(f"\nWriting {len(all_test_cases)} total test cases to {output_path}...")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_test_cases, f, indent=2)
        
    print("Done! Please review draft_qa_dataset.json manually before appending to the main qa_dataset.json.")

if __name__ == "__main__":
    main()
