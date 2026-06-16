import re
from langchain_core.tools import tool
from backend.core.config import vectorstore

@tool
def get_internship_stats() -> str:
    """Returns the total number of problems and logs stored in the knowledge base."""
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
            f"The knowledge base currently contains {problem_count} uniquely numbered debugging logs, "
            f"plus {note_count} general engineering notes and post-mortems. "
            f"Total knowledge documents: {problem_count + note_count}."
        )
    except Exception as e:
        return f"Could not determine stats: {e}"
