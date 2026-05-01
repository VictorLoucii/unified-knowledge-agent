import json
import re
import os

MARKDOWN_FILE_PATH = "data/NEXTIER_Internship_Bugs.md"
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
    try:
        with open(MARKDOWN_FILE_PATH, "r", encoding="utf-8") as file:
            md_content = file.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {MARKDOWN_FILE_PATH}")
        return

    # --- ZONE 3: Workflow & Rules (5 Queries) ---
    dataset = [
        {
            "query": "What is the project rule regarding the use of npm versus yarn?",
            "expected_output": "Use Yarn Only: Avoid `npm` commands entirely to prevent `package-lock.json` conflicts. Use `yarn install`, `yarn start`, etc.",
            "evaluation_criteria": "The agent MUST prioritize the General Workflow Rules. It MUST extract the core reasoning.",
            "target_problem_id": None
        },
        {
            "query": "Why did we change the import from @/i18n to ./src/i18n for local wireless debugging?",
            "expected_output": "Metro bundler failed to resolve the @/i18n alias during wireless debugging and returned a 500 error (UnableToResolveError). Using the relative path ensures proper module resolution without relying on alias configuration.",
            "evaluation_criteria": "The agent MUST return the reasoning provided in the notes. It MUST include the surrounding conceptual explanations.",
            "target_problem_id": None
        },
        {
            "query": "When the parent screen controls horizontal spacing, why do we add marginLeft only to the first card in a FlatList?",
            "expected_output": "Your card style already has spacing between cards... If we added marginLeft to all cards, you'd get double spacing. So we check: index === 0 Meaning: only the first card gets marginLeft",
            "evaluation_criteria": "The agent MUST locate the 'best practice' UI rules and extract the specific reasoning.",
            "target_problem_id": None
        },
        {
            "query": "What is the recommended build strategy if the app is running in the emulator?",
            "expected_output": "If the app is running in the emulator, skip `./gradlew clean` before building to preserve working native links. Use `./gradlew assembleRelease` directly.",
            "evaluation_criteria": "The agent MUST pull this from the Project Workflow & Safety Rules at the top of the file.",
            "target_problem_id": None
        },
        {
            "query": "What is the 'Golden Rule' when modifying shared UI components like AutocompleteField?",
            "expected_output": "Never break the existing contract. Instead of hardcoding logic for one specific field, you add a new capability (a Prop) to the shared component and give it a Default Value that preserves the existing behavior. This ensures Backward Compatibility.",
            "evaluation_criteria": "The agent MUST identify the Golden Rule of Shared Component Safety.",
            "target_problem_id": 63
        }
    ]

    # --- ZONE 1: Direct Extraction (7 Queries) ---
    direct_extraction_ids = [1, 14, 40, 60, 80, 110, 115]
    for pid in direct_extraction_ids:
        problem_text = extract_problem_text(md_content, pid)
        if problem_text:
            if not problem_text.endswith("<END OF PROBLEM>"):
                problem_text += "\n\n<END OF PROBLEM>"
            dataset.append({
                "query": f"Can you provide the complete details and code for Problem {pid}?",
                "expected_output": problem_text,
                "evaluation_criteria": f"The agent MUST start the response with '# Problem {pid}'. It MUST NOT summarize the code. It MUST output the exact text and end with '<END OF PROBLEM>'.",
                "target_problem_id": pid
            })

    # --- ZONE 2: Semantic Discovery (8 Queries) ---
    semantic_mappings = [
        {"query": "How did we resolve the navigation issue for the Active Investment and Investment Portfolio screens?", "id": 3},
        {"query": "What caused the alignment bug on the Answer screen, specifically with the Add button?", "id": 4},
        {"query": "What was the security issue regarding Unrestricted File Uploads and how was it patched?", "id": 5},
        {"query": "Why was an underline appearing in the Profile -> about/education tabs and how did we remove it?", "id": 7},
        {"query": "Why does the AI chatbot input field shift when typing or opening the keyboard?", "id": 55},
        {"query": "What caused the 6th OTP input box to be cut off on smaller Android screens?", "id": 13},
        {"query": "How do we resolve the Android TextInput cursor jumping to the end of the text string?", "id": 99},
        {"query": "Why weren't OneSignal push notifications stopping when the user toggled them off in the settings?", "id": 49}
    ]
    
    for item in semantic_mappings:
        problem_text = extract_problem_text(md_content, item["id"])
        if problem_text:
            dataset.append({
                "query": item["query"],
                "expected_output": problem_text,
                "evaluation_criteria": "The agent MUST synthesize an answer based on the provided technical log using semantic keyword matching.",
                "target_problem_id": item["id"]
            })

    # --- ZONE 4: Ambiguity Triage (5 Queries) ---
    ambiguity_mappings = [
        {"query": "I have an issue with the settings screen.", "id": 9},
        {"query": "How do I fix the tab underline?", "id": 7},
        {"query": "file upload bug", "id": 5},
        {"query": "I am getting a 'VirtualizedLists should never be nested' error. How do I fix it?", "id": 90},
        {"query": "Why does the app crash with a 'duplicate key' error?", "id": 33}
    ]

    for item in ambiguity_mappings:
        problem_text = extract_problem_text(md_content, item["id"])
        if problem_text:
            dataset.append({
                "query": item["query"],
                "expected_output": problem_text,
                "evaluation_criteria": "The agent MUST recognize the query is vague or ambiguous. It MUST retrieve the correct underlying problem log but should ideally present it contextually.",
                "target_problem_id": item["id"]
            })

    # --- ZONE 5: Negative Constraints (5 Queries) ---
    negative_queries = [
        "How do I configure a Kubernetes cluster for the Nexteir backend?",
        "What is the best way to deploy an AWS Lambda function for the agent?",
        "Can you write a Python script to scrape LinkedIn data for our users?",
        "How do we handle state management using Vue.js?",
        "Explain the memory leak issue in the Java Spring Boot microservice."
    ]
    
    for nq in negative_queries:
        dataset.append({
            "query": nq,
            "expected_output": "I'm sorry, but that information is not available in my Second Brain.",
            "evaluation_criteria": "The agent MUST trigger its 'Zero-Knowledge' guardrail. It MUST politely refuse to answer and clearly state the information is not in the logs.",
            "target_problem_id": None
        })

    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as json_file:
        json.dump(dataset, json_file, indent=2, ensure_ascii=False)

    print(f"✅ Successfully generated {OUTPUT_JSON_PATH} with {len(dataset)} test cases!")

if __name__ == "__main__":
    main()