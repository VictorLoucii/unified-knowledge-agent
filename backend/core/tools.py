# backend/core/tools.py
import re
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from backend.core.config import store, retriever

# ==========================================
# 3. TOOL DEFINITIONS
# ==========================================

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time. Use this when the user asks for the time."""
    from datetime import datetime

    return datetime.now().strftime(format)


@tool
def get_problem_index() -> str:
    """
    Use this tool ONLY when the user explicitly asks for a list, index, 
    titles, or summary of ALL problems in the database.
    """
    index_list = []
    try:
        # Scan all documents in the local store (Cost: $0)
        for key in store.yield_keys():
            doc = store.mget([key])[0]
            if doc:
                header = str(doc.metadata.get("Header 1", ""))
                
                # Only grab actual Problem logs
                if re.search(r"Problem\s*:?\s*\d+", header, re.IGNORECASE):
                    # Extract clean text for the title preview
                    lines = [line.strip() for line in doc.page_content.split('\n') 
                             if line.strip() and not line.startswith('[SCREENSHOT')]
                    
                    title_preview = ""
                    for line in lines:
                        # Strip out markdown symbols for a cleaner title
                        clean_line = re.sub(r'^[#\*\->\s]+', '', line).replace("**", "").replace("_", "").strip()
                        if clean_line:
                            title_preview = clean_line[:80] + "..."
                            break
                            
                    if not title_preview:
                        title_preview = "No description available"
                    
                    # Normalize header to just "Problem X"
                    match = re.search(r'(Problem\s*:?\s*\d+)', header, re.IGNORECASE)
                    clean_header = match.group(1).title() if match else header
                    
                    index_list.append((clean_header, title_preview))
        
        # Sort the list numerically based on the problem number
        def extract_num(item):
            match = re.search(r'\d+', item[0])
            return int(match.group()) if match else 9999
            
        index_list.sort(key=extract_num)
        
        # Format items neatly
        formatted_items = [f"{item[0]} - {item[1]}" for item in index_list]
        total_items = len(formatted_items)
        
        # SAFEGUARD: Slice the LIST, not the string characters
        if total_items > 40:
            first_batch = formatted_items[:39]
            last_item = formatted_items[-1] # Grab the absolute last item (e.g., Problem 85)
            
            formatted_list = "Here is the index of problems:\n" + "\n".join(first_batch)
            formatted_list += f"\n\n... [ {total_items - 40} items omitted for memory limits ] ...\n\n"
            formatted_list += f"--- LAST PROBLEM IN DATABASE ---\n{last_item}"
            formatted_list += "\n\n[SYSTEM NOTE: If the user asks for a problem in the omitted range, use the 'search_internship_history' tool to fetch it.]"
        else:
            formatted_list = "Here is the index of all problems:\n" + "\n".join(formatted_items)
        
        return formatted_list

    except Exception as e:
        return f"Could not generate index: {e}"



@tool
def get_internship_stats() -> str:
    """Returns the total number of problems and logs stored in the Second Brain."""
    problem_count = 0
    note_count = 0
    try:
        # Scan all documents in the local store
        for key in store.yield_keys():
            doc = store.mget([key])[0]
            if doc:
                header = str(doc.metadata.get("Header 1", ""))

                # STRICT REGEX: Looks for "Problem" followed by optional spaces/colons, then a NUMBER
                if re.search(r"Problem\s*:?\s*\d+", header, re.IGNORECASE):
                    problem_count += 1
                # Otherwise, if the header isn't empty, it's a general note
                elif header.strip():
                    note_count += 1

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
    Use this tool to search the Nexteir Internship logs for debugging solutions,
    React Native issues, architectural decisions (like Yarn vs NPM), and UI fixes.
    Input should be a clear, concise search query.
    """
    expansion_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, name="Expansion_LLM")

    search_variants = expansion_llm.invoke(
        f"Based on the user's query: '{query}', generate 3 search variations. "
        "RULE 1: If the user explicitly mentions a problem number (like 'problem 5'), "
        "one variation MUST be the exact header format: '# Problem [number]'. "
        "RULE 2: Extract technical keywords and proper nouns. "
        "Respond with ONLY the raw queries, one per line. No numbers, no bullets."
    ).content.split("\n")

    # Force strip any accidental numbers/bullets if the LLM disobeys
    all_queries = [
        q.strip().lstrip("0123456789.- ") for q in search_variants if q.strip()
    ] + [query]

    # Aggressively format any query containing "problem X" to match the database
    all_queries = [
        (
            re.sub(r"(?i).*problem\s*(\d+).*", r"# Problem \1", q)
            if "problem" in q.lower() and re.search(r"\d+", q)
            else q
        )
        for q in all_queries
    ]

    # [THE FIX 2: Deduplicate queries so we don't multiply scores 4x]
    all_queries = list(set(all_queries))
    print(f"🤖 [DEBUG] Queries actually being searched: {all_queries}")

    all_docs = []

    # --- STEP 1: Vector Search (Handles semantic concepts) ---
    for q in all_queries:
        all_docs.extend(retriever.invoke(q))

    # --- STEP 2: EXACT MATCH BYPASS (Handles Vector Blindspots) ---
    # Vector DBs strip headers for embeddings, making ID lookups fail.
    # We manually scan the local docstore metadata for exact Problem IDs to guarantee they are found.
    try:
        for key in store.yield_keys():
            doc = store.mget([key])[0]
            if doc:
                headers_text = " ".join(
                    [str(val) for k, val in doc.metadata.items() if "Header" in k]
                ).lower()
                for q in all_queries:
                    clean_q = q.replace("#", "").strip().lower()
                    # Only trigger bypass for exact problem queries
                    if "problem" in clean_q:
                        # [THE FIX] Use regex word boundary (\b) to stop "1" from matching "10"
                        pattern = r"\b" + re.escape(clean_q) + r"\b"
                        if re.search(pattern, headers_text):
                            all_docs.append(doc)
                            break  # Found it, skip checking other queries for this doc

    except Exception as e:
        print(f"⚠️ [WARNING] Direct store scan failed: {e}")

    # Deduplicate documents based on content
    unique_docs = list({doc.page_content: doc for doc in all_docs}.values())

    # --- HYBRID RE-RANKING LOGIC ---
    STOP_WORDS = {
        "the", "and", "how", "fix", "for", "with", "that", "this", 
        "from", "are", "you", "not", "but", "what", "did", "use", 
        "when", "can", "is",
    }

    core_keywords = set(
        [
            word.lower()
            for word in re.findall(r"\b\w+\b", query)
            if (len(word) >= 3 or word.isdigit()) and word.lower() not in STOP_WORDS
        ]
    )

    print(f"🔍 [DEBUG] Extracted Core Keywords for Scoring: {core_keywords}")

    def calculate_relevance_score(doc):
        headers_text = " ".join(
            [str(val) for key, val in doc.metadata.items() if "Header" in key]
        )
        text_lower = (headers_text + " " + doc.page_content).lower()
        score = 0

        # 1. Exact Phrase/ID Matches (Heavy Weight: +10)
        for q in all_queries:
            clean_q = q.replace("#", "").strip().lower()

            # Prevent empty string matching
            if clean_q:
                # [THE FIX] Use regex word boundary here too
                pattern = r"\b" + re.escape(clean_q) + r"\b"
                if re.search(pattern, text_lower):
                    score += 10
                    # Added a little extra debug info so you can see WHICH problem got the score
                    print(
                        f"🎯 [DEBUG] Exact Match Found for '{q}' in: {doc.metadata.get('Header 1', 'Unknown')}"
                    )

        # 2. Granular Keyword Matches (Lighter Weight: +1 per word)
        for kw in core_keywords:
            # [THE FIX] Handle basic singular/plural forms (e.g., 'issues' <-> 'issue')
            base_word = kw[:-1] if kw.endswith("s") else kw
            plural_word = base_word + "s"

            # Match the exact keyword, its base (singular), or its plural using word boundaries
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
                score += 1

        return score

    # Apply the new scoring function
    unique_docs.sort(key=calculate_relevance_score, reverse=True)

    if unique_docs:
        print(
            f"🔍 [DEBUG] Top Doc Score for '{query}': {calculate_relevance_score(unique_docs[0])}"
        )

    unique_docs = unique_docs[:3]

    def format_doc_for_llm(doc):
        headers = []
        if "Header 1" in doc.metadata:
            headers.append(f"# {doc.metadata['Header 1']}")
        if "Header 2" in doc.metadata:
            headers.append(f"## {doc.metadata['Header 2']}")
        if "Header 3" in doc.metadata:
            headers.append(f"### {doc.metadata['Header 3']}")

        header_str = " > ".join(headers) if headers else "Unknown Section"

        return f"Section Hierarchy: {header_str}\nPage {doc.metadata.get('page', 'Unknown')}:\n{doc.page_content}"

    formatted_context = "\n\n---\n\n".join(
        [format_doc_for_llm(doc) for doc in unique_docs]
    )

    MAX_CHAR_LIMIT = 150000

    if len(formatted_context) > MAX_CHAR_LIMIT:
        print(
            f"⚠️ [WARNING] Context too large ({len(formatted_context)} chars). Truncating."
        )
        formatted_context = (
            formatted_context[:MAX_CHAR_LIMIT]
            + "\n\n...[CONTENT TRUNCATED DUE TO SIZE]..."
        )
    print("\n====== RAW TOOL OUTPUT FED TO AI ======")
    print(formatted_context)
    print("=======================================\n")

    return formatted_context


tools = [get_system_time, get_internship_stats, get_problem_index, search_internship_history]