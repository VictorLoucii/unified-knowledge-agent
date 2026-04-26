import json
import re
import os

# 1. Define the paths
MARKDOWN_FILE_PATH = "data/NEXTIER_Internship_Bugs.md" 
# FIX: Ensure we write to the exact file that the Eval script reads from
OUTPUT_JSON_PATH = "backend/evals/qa_dataset.json"

def extract_problem_text(markdown_text, problem_num):
    """
    Uses Regex to find a specific problem and grabs everything 
    up to the next problem or the end of the file.
    """
    pattern = rf"(# Problem {problem_num}\n.*?)(?=\n# Problem |\Z)"
    match = re.search(pattern, markdown_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    else:
        print(f"⚠️ Warning: Could not find Problem {problem_num} in the file.")
        return ""

def main():
    # 2. Read the markdown file
    try:
        with open(MARKDOWN_FILE_PATH, "r", encoding="utf-8") as file:
            md_content = file.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {MARKDOWN_FILE_PATH}")
        return

    # 3. Extract the long problems dynamically
    problem_14_text = extract_problem_text(md_content, 14)
    problem_110_text = extract_problem_text(md_content, 110)
    
    # Append the required tag for the ordinal test
    if problem_110_text:
        problem_110_text += "\n\n<END OF PROBLEM>"

    # 4. Build the dataset list with RELAXED judge criteria
    dataset = [
        {
            "query": "What is the project rule regarding the use of npm versus yarn?",
            "expected_output": "Use Yarn Only: Avoid `npm` commands entirely to prevent `package-lock.json` conflicts. Use `yarn install`, `yarn start`, etc.",
            "evaluation_criteria": "The agent MUST prioritize the General Workflow Rules. It MUST extract the core reasoning, but it is ALLOWED to include the section header as mandated by its system prompt."
        },
        {
            "query": "Why did we change the import from @/i18n to ./src/i18n for local wireless debugging?",
            "expected_output": "Metro bundler failed to resolve the @/i18n alias during wireless debugging and returned a 500 error (UnableToResolveError). Using the relative path ensures proper module resolution without relying on alias configuration.",
            "evaluation_criteria": "The agent MUST return the reasoning provided in the notes. Because the RAG system extracts document chunks, the agent is ALLOWED and EXPECTED to include the surrounding conceptual explanations, technical differences, and alias rules from that same markdown section."
        },
        {
            "query": "When the parent screen controls horizontal spacing, why do we add marginLeft only to the first card in a FlatList?",
            "expected_output": "Your card style already has spacing between cards... If we added marginLeft to all cards, you'd get double spacing. So we check: index === 0 Meaning: only the first card gets marginLeft",
            "evaluation_criteria": "The agent MUST locate the 'best practice' UI rules and extract the specific reasoning. Including file names from the context is ALLOWED. It MUST NOT blend this with any specific bug logs."
        },
        {
            "query": "Can you provide the complete details and code for Problem 14 regarding the locked fullName text input field after Google Sign-in?",
            "expected_output": problem_14_text,
            "evaluation_criteria": "The agent MUST start the response with '# Problem 14'. It MUST NOT summarize the code. It is ALLOWED to format inline variables and file paths with markdown backticks."
        },
        {
            "query": "Show me the last problem from the internship bug log.",
            "expected_output": problem_110_text,
            "evaluation_criteria": "The agent MUST output the exact text of the problem without summarizing. NOTE TO JUDGE: The expected output is a raw technical log, so it NATURALLY contains code snippets, file names, and explanations. You MUST NOT penalize the agent for including these. It MUST act as a pure passthrough and end the response with the exact tag '<END OF PROBLEM>'."
        }
    ]

    # 5. Let Python handle the JSON escaping and save the file
    # We use os.makedirs to ensure the backend/evals folder exists just in case
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(dataset, json_file, indent=2, ensure_ascii=False)
        
    print(f"✅ Successfully generated {OUTPUT_JSON_PATH} with {len(dataset)} test cases!")

if __name__ == "__main__":
    main()