import os
import re
from langchain_core.tools import tool

@tool
def get_problem_index(start: int = 1, end: int = 25) -> str:
    """
    Use this tool ONLY for top-level navigation, such as 'what are the problems?',
    'show me the index', or 'list all problems'.

    CRITICAL ROUTING RULE: DO NOT use this tool to look for specific topics,
    errors, bugs, or existence checks (e.g., 'are there problems about X' or
    'is there a fix for Y').

    DO NOT USE THIS TOOL FOR ORDINAL REQUESTS. If the user asks for the 'first problem',
    'last problem', 'oldest', or 'latest', you MUST REJECT this tool and use
    search_knowledge_base instead.
    """
    print(f"\n📥 [TOOL CALL] get_problem_index triggered for range {start} to {end}")

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))
        DATA_FILE = os.path.join(ROOT_DIR, "data", "NEXTIER_Internship_Bugs.md")

        if not os.path.exists(DATA_FILE):
            return "Error: Internship database file not found."

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            full_text = f.read()

        # Capture ALL Problem IDs using the Phase 6.3 anchor strategy
        header_pattern = r"(?im)^\s*(?:#|//)\s*problem\s*:?\s*(\d+)"
        matches = list(re.finditer(header_pattern, full_text))

        if not matches:
            return "No problems found in the database."

        problem_titles = []

        # The "Look-Ahead Block" Strategy
        for i, match in enumerate(matches):
            prob_num = int(match.group(1))

            start_idx = match.end()
            end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
            block = full_text[start_idx:end_idx]

            # LAYER 1: Code Blocks
            block = re.sub(r"```.*?```", "", block, flags=re.DOTALL)
            # LAYER 2: Base64
            block = re.sub(r"data:image\S+", "", block)
            # LAYER 2.1: Pandoc & Markdown Media Paths (Handles multi-line attributes)
            block = re.sub(r"!\[.*?\]\(.*?\)(?:\{[^}]*?\})?", "", block)
            # LAYER 3: URLs
            block = re.sub(r"http\S+", "", block)

            lines = block.split("\n")
            clean_title = "Could not extract clear title"

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # LAYER 4: MD Symbols
                line_clean = re.sub(r"[#\*_>\-\[\]\(\)]+", "", line).strip()

                # LAYER 6: The TSX Filter
                if ".tsx" in line_clean.lower() or "src/" in line_clean.lower():
                    continue

                # LAYER 5: The Gauntlet (must be > 15 chars)
                if len(line_clean) >= 15:
                    clean_title = line_clean
                    break

            problem_titles.append((prob_num, clean_title))

        # Sort and apply Start/End Range logic
        problem_titles.sort(key=lambda x: x[0])

        start_idx = max(0, start - 1)

        # [PHASE 7.3 FIX] The Hard Token Ceiling
        MAX_PAGINATION_SIZE = 25
        requested_end = min(end, start + MAX_PAGINATION_SIZE - 1)
        end_idx = min(len(problem_titles), requested_end)

        paginated = problem_titles[start_idx:end_idx]

        output = [f"=== PROBLEM INDEX ({start} to {requested_end}) ==="]
        for num, title in paginated:
            output.append(f"Problem {num}: {title}")

        # === THE TOKEN SAVER PROTOCOL ===
        if len(problem_titles) > end_idx:
            output.append(
                f"\n*(Note: Hard-capped at {len(paginated)} items out of {len(problem_titles)} total problems to save tokens. "
                "Please be more specific by asking for a specific Problem ID, searching by keyword, or requesting the next page [e.g., 'show problems 26 to 50'].)*"
            )

        return "\n".join(output)

    except Exception as e:
        print(f"🚨 [ERROR] get_problem_index crashed: {e}")
        return f"Error extracting titles: {e}"
