# backend/core/tools.py
import re
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from backend.core.config import store, retriever, vectorstore

# ==========================================
# 3. TOOL DEFINITIONS
# ==========================================


@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time. Use this when the user asks for the time."""
    from datetime import datetime

    return datetime.now().strftime(format)


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
    search_internship_history instead.
    """
    import os
    import re

    print(f"\n📥 [TOOL CALL] get_problem_index triggered for range {start} to {end}")

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
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


@tool
def get_internship_stats() -> str:
    """Returns the total number of problems and logs stored in the Second Brain."""
    unique_problems = set()
    unique_notes = set()
    try:
        # [THE FIX: Scan the in-memory Chroma database instead]
        data = vectorstore.get()

        if data and "documents" in data:
            for content, metadata in zip(data["documents"], data["metadatas"]):
                if not content or not metadata:
                    continue

                headers_text = " ".join(
                    [str(val) for k, val in metadata.items() if "Header" in k]
                )
                full_text = headers_text + "\n" + str(content)

                matches = re.findall(r"(?i)problem\s*:?\s*(\d+)", full_text)

                if matches:
                    for num in matches:
                        unique_problems.add(num)
                elif headers_text.strip():
                    unique_notes.add(headers_text.strip())

        problem_count = len(unique_problems)
        note_count = len(unique_notes)

        return (
            f"The Second Brain currently contains {problem_count} uniquely numbered debugging logs, "
            f"plus {note_count} general engineering notes and post-mortems. "
            f"Total knowledge documents: {problem_count + note_count}."
        )
    except Exception as e:
        return f"Could not determine stats: {e}"


@tool
def search_internship_history(query: str) -> str:
    """
    CRITICAL DIRECTIVE: You MUST call this tool for EVERY technical question, bug inquiry,
    UI styling rule, or project workflow question. Do NOT rely on your internal programming knowledge.

    Use this tool for ANY query regarding specific topics, keywords, errors,
    code logic, or existence checks (e.g., 'is there a fix for...', 'are there problems about X',
    'why do we add marginLeft', or 'how do I handle Y').

    This is the ONLY tool that can see the full content of the logs.

    CRITICAL: If the user asks for a specific Problem ID (e.g., 'Problem 26'),
    OR asks for ordinal positions like 'the first problem' or 'the last problem',
    you MUST use this tool and pass that exact phrase as the query.
    """
    import os
    import re
    from langchain_openai import ChatOpenAI
    from backend.core.config import retriever

    print(f"\n📥 [TOOL CALL] search_internship_history triggered with query: '{query}'")

    expansion_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, name="Expansion_LLM")

    search_variants = expansion_llm.invoke(
        f"Based on the user's query: '{query}', generate 3 search variations. "
        "RULE 1: Extract technical keywords and proper nouns. "
        "RULE 2: DO NOT invent or add problem numbers. ONLY include a problem number if the user explicitly typed one in their query. "
        "Respond with ONLY the raw queries, one per line. No numbers, no bullets."
    ).content.split("\n")

    all_queries = [
        q.strip().lstrip("0123456789.- ") for q in search_variants if q.strip()
    ] + [query]

    all_queries = [
        (
            re.sub(r"(?i).*problem\s*(\d+).*", r"# Problem \1", q)
            if "problem" in q.lower() and re.search(r"\d+", q)
            else q
        )
        for q in all_queries
    ]

    all_queries = list(set(all_queries))
    print(f"🤖 [DEBUG] Queries actually being searched: {all_queries}")

    direct_problem_blocks = []
    target_problems = set()

    for q in all_queries:
        match = re.search(r"(?i)problem\s*(\d+)", q)
        if match:
            target_problems.add(match.group(1))

    # ==========================================
    # 1. ORDINAL INTERCEPTOR (First / Last)
    # ==========================================
    query_lower = query.lower()
    needs_first = any(x in query_lower for x in ["first problem", "oldest problem"])
    needs_last = any(x in query_lower for x in ["last problem", "latest problem"])

    if needs_first or needs_last:
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
            DATA_FILE = os.path.join(ROOT_DIR, "data", "NEXTIER_Internship_Bugs.md")

            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    temp_text = f.read()

                all_ids = [
                    int(m)
                    for m in re.findall(
                        r"(?im)^\s*(?:#|//)\s*problem\s*:?\s*(\d+)", temp_text
                    )
                ]

                if all_ids:
                    if needs_first:
                        min_id = str(min(all_ids))
                        target_problems.add(min_id)
                        print(
                            f"🎯 [DEBUG] Ordinal 'First' detected. Lowest ID is {min_id}"
                        )
                    if needs_last:
                        max_id = str(max(all_ids))
                        target_problems.add(max_id)
                        print(
                            f"🎯 [DEBUG] Ordinal 'Last' detected. Highest ID is {max_id}"
                        )
        except Exception as e:
            print(f"⚠️ [WARNING] Ordinal interceptor failed: {e}")

    # ==========================================
    # 2. RAW EXTRACTION EXECUTION
    # ==========================================
    if target_problems:
        print(f"🚀 [DEBUG] Engaging Raw Interceptor for IDs: {target_problems}")
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
            DATA_FILE = os.path.join(ROOT_DIR, "data", "NEXTIER_Internship_Bugs.md")

            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    full_file_text = f.read()

                all_header_matches = list(
                    re.finditer(
                        r"(?im)^\s*(?:#|//)\s*problem\s*:?\s*(\d+)", full_file_text
                    )
                )

                for i, match in enumerate(all_header_matches):
                    prob_num = match.group(1)
                    if prob_num in target_problems:
                        start_idx = match.start()
                        end_idx = (
                            all_header_matches[i + 1].start()
                            if i + 1 < len(all_header_matches)
                            else len(full_file_text)
                        )
                        block = full_file_text[start_idx:end_idx].strip()

                        direct_problem_blocks.append(
                            f"=== ABSOLUTE SOURCE OF TRUTH: PROBLEM {prob_num} ===\n{block}\n==============================================\n"
                        )
        except Exception as e:
            print(f"🚨 [ERROR] Raw Interceptor execution failed: {e}")

    # ==========================================
    # 3. SHORT-CIRCUIT THE VECTOR SEARCH
    # ==========================================
    if direct_problem_blocks:
        final_output = "\n\n".join(direct_problem_blocks)
        print(
            f"✅ [DEBUG] Short-circuiting vector search. Fed {len(direct_problem_blocks)} raw blocks."
        )

        # [PHASE 7.0 FIX]: Inject metadata even during an early return!
        retrieved_ids_str = ",".join(list(target_problems))
        final_output += f"\n\n<!-- RETRIEVED_PROBLEM_IDS: [{retrieved_ids_str}] -->"

        return final_output

    # ==========================================
    # 4. RESUME STANDARD VECTOR SEARCH
    # ==========================================
    all_docs = []

    for q in all_queries:
        all_docs.extend(retriever.invoke(q))

    unique_docs = list({doc.page_content: doc for doc in all_docs}.values())

    STOP_WORDS = {
        "the",
        "and",
        "how",
        "fix",
        "for",
        "with",
        "that",
        "this",
        "from",
        "are",
        "you",
        "not",
        "but",
        "what",
        "did",
        "use",
        "when",
        "can",
        "is",
    }

    core_keywords = set(
        [
            word.lower()
            for word in re.findall(r"\b\w+\b", query)
            if (len(word) >= 3 or word.isdigit()) and word.lower() not in STOP_WORDS
        ]
    )

    def calculate_relevance_score(doc):
        headers_text = " ".join(
            [str(val) for key, val in doc.metadata.items() if "Header" in key]
        )
        text_lower = (headers_text + " " + doc.page_content).lower()
        score = 0

        for q in all_queries:
            clean_q = q.replace("#", "").strip().lower()
            if clean_q:
                match_num = re.search(r"\d+", clean_q)
                if "problem" in clean_q and match_num:
                    pattern = r"problem\s*:?\s*" + match_num.group(0) + r"\b"
                else:
                    pattern = r"\b" + re.escape(clean_q) + r"\b"

                if re.search(pattern, text_lower):
                    score += 10

        exact_query_lower = query.lower().strip()
        # [THE FIX: Heavily weight header matches to prevent hijacking]
        if len(exact_query_lower) >= 2:
            headers_text_lower = headers_text.lower()
            if exact_query_lower in headers_text_lower:
                score += 500  # Massive boost for exact match in header
            elif exact_query_lower in text_lower:
                score += 100

        for kw in core_keywords:
            base_word = kw[:-1] if kw.endswith("s") else kw
            plural_word = base_word + "s"
            pattern = (
                r"\b("
                + re.escape(kw)
                + r"|"
                + re.escape(base_word)
                + r"|"
                + re.escape(plural_word)
                + r")\b"
            )

            if re.search(pattern, text_lower):
                # [THE FIX: Heavily boost the weight if the user only typed 1-3 words]
                score += 15 if len(core_keywords) <= 3 else 5

        return score

    # [PHASE 6.8 FIX] SORT AND TRUNCATE FIRST!
    unique_docs.sort(key=calculate_relevance_score, reverse=True)
    
    # [THE FIX: Increase K value to 8 to ensure deep retrieval for short-tail queries]
    unique_docs = unique_docs[:10] 
    print(f"🔧 [__DEV__] Increased K-value to 8. Sorting for broad short-tail queries completed.")

    print(f"\n📊 [DEBUG] Top 8 Vector Matches for General Search:")
    for i, doc in enumerate(unique_docs):
        score = calculate_relevance_score(doc)
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"  {i+1}. Score: {score} | Preview: {preview}...")

    # [PHASE 6.8 FIX ONLY ESCALATE PROBLEMS FOUND IN THE TOP 3 DOCS
    discovered_problems = set()
    for doc in unique_docs:
        headers_text = " ".join(
            [str(val) for k, val in doc.metadata.items() if "Header" in k]
        )

        # 🚀 THE FIX: Prevent Extractor Trap by checking metadata headers
        # If the chunk comes from a Workflow or General section, do NOT scrape it for bug IDs.
        if any(
            keyword in headers_text.lower()
            for keyword in ["workflow", "rule", "general", "role"]
        ):
            print(
                f"🔧 [__DEV__] Skipping auto-escalation for general document: {headers_text[:50]}..."
            )
            continue

        full_text = headers_text + " " + doc.page_content
        matches = re.findall(r"(?i)problem\s*(\d+)", full_text)
        for m in matches:
            discovered_problems.add(m)

    escalated_text = ""
    if discovered_problems:
        print(
            f"🔍 [DEBUG] Top 3 Docs contained Problems {discovered_problems}. Auto-Escalating..."
        )
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
            DATA_FILE = os.path.join(ROOT_DIR, "data", "NEXTIER_Internship_Bugs.md")

            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    full_file_text = f.read()

                matches = list(
                    re.finditer(
                        r"(?im)^\s*(?:#|//)\s*problem\s*:?\s*(\d+)", full_file_text
                    )
                )
                escalated_blocks = []

                for i, match in enumerate(matches):
                    prob_num = match.group(1)
                    if prob_num in discovered_problems:
                        start_idx = match.start()
                        end_idx = (
                            matches[i + 1].start()
                            if i + 1 < len(matches)
                            else len(full_file_text)
                        )
                        block = full_file_text[start_idx:end_idx].strip()

                        if len(block) > 15000:
                            block = (
                                block[:15000] + "\n\n...[BLOCK TRUNCATED FOR LENGTH]..."
                            )

                        # [PHASE 7.2 FIX] The Strict Librarian Directive - Modified for Feature Bugs
                        escalated_blocks.append(
                            f"=== AUTO-ESCALATED CONTEXT: PROBLEM {prob_num} ===\n"
                            f"(AGENT INSTRUCTION: CONDITIONAL EXTRACTION - If the user explicitly requested this exact bug ID, or a highly specific technical error, you MUST synthesize the entire text below this line including code and paths. "
                            f"Act as a Librarian (listing ONLY IDs) if the query is vague/ambiguous and matches 2 or more completely unrelated problems (e.g., 'file upload bug' matching 3 different IDs). You are STRICTLY FORBIDDEN from summarizing code blocks—output them exactly.)\n\n"
                            f"{block}\n==============================================\n"
                        )

                if escalated_blocks:
                    escalated_text = "\n\n".join(escalated_blocks)
        except Exception as e:
            print(f"⚠️ [WARNING] Auto-Escalation failed: {e}")

    def format_doc_for_llm(doc):
        headers = []
        if "Header 1" in doc.metadata:
            headers.append(f"# {doc.metadata['Header 1']}")
        if "Header 2" in doc.metadata:
            headers.append(f"## {doc.metadata['Header 2']}")
        if "Header 3" in doc.metadata:
            headers.append(f"### {doc.metadata['Header 3']}")

        header_str = " > ".join(headers) if headers else "Unknown Section"
        content = doc.page_content
        DOC_MAX_CHARS = 10000
        if len(content) > DOC_MAX_CHARS:
            content = (
                content[:DOC_MAX_CHARS]
                + "\n\n...[SPECIFIC DOC TRUNCATED FOR LENGTH]..."
            )

        return f"Section Hierarchy: {header_str}\nPage {doc.metadata.get('page', 'Unknown')}:\n{content}"

    formatted_context = "\n\n---\n\n".join(
        [format_doc_for_llm(doc) for doc in unique_docs]
    )

    # FIX: Prioritize Top Vector Matches (General Knowledge) BEFORE bulky Escalated Problems
    if escalated_text:
        final_output = (
            "=== TOP VECTOR MATCHES (GENERAL KNOWLEDGE / WORKFLOW RULES) ===\n\n"
            + formatted_context
            + "\n\n"
            + escalated_text
        )
    else:
        final_output = formatted_context

    MAX_CHAR_LIMIT = 30000
    if len(final_output) > MAX_CHAR_LIMIT:
        final_output = (
            final_output[:MAX_CHAR_LIMIT]
            + "\n\n...[TOTAL CONTENT TRUNCATED DUE TO SIZE]..."
        )

    # [RECALL@K METADATA INJECTION]
    # Inject retrieved IDs as an invisible comment for the evaluation parser.
    # The LLM ignores this, ensuring UI/Persona backward compatibility.
    retrieved_ids_str = ",".join(list(discovered_problems))
    final_output += f"\n\n<!-- RETRIEVED_PROBLEM_IDS: [{retrieved_ids_str}] -->"

    return final_output


tools = [
    get_system_time,
    get_internship_stats,
    get_problem_index,
    search_internship_history,
]
