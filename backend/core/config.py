# backend/core/config.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.storage import LocalFileStore, create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# 1. ENVIRONMENT & LLM SETUP
# ==========================================
load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("🚨 OPENROUTER_API_KEY not found! Check your .env file.")

# Disable tracing temporarily since no LANGCHAIN_API_KEY is present
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Nexteir_Second_Brain_Prod"

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
    streaming=True,
    request_timeout=45,
    max_retries=5,
)
print(f"🤖 Loading LLM model: {llm.model_name}")

# ==========================================
# 2. VECTOR DB INITIALIZATION
# ==========================================
# Adjust BASE_DIR since this file is now nested inside the core/ directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
persist_directory = os.path.join(BASE_DIR, "chroma_db")
store_directory = os.path.join(BASE_DIR, "docstore")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    collection_name="nexteir_internship",
    persist_directory=persist_directory,
    embedding_function=embeddings,
)

cache_vectorstore = Chroma(
    collection_name="semantic_cache",
    persist_directory=persist_directory,
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"}
)

SEMANTIC_CACHE_THRESHOLD = float(os.getenv("SEMANTIC_CACHE_THRESHOLD", "0.92"))

# [THE FIX] Wrap the raw store so it decodes bytes into Document objects
raw_store = LocalFileStore(store_directory)
store = create_kv_docstore(raw_store)

# The "Micro-Insight" scout: Finds the exact sentence that matches the query
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

#The "Context Diet": Prevents massive log files from becoming Mega-Chunks
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,  # Now uses the wrapped store
    child_splitter=child_splitter,
    parent_splitter=parent_splitter, # <-- Now enforces a size limit on the stored memory
    search_kwargs={"k": 25},         # <-- [FIX] Pulls top 25 most relevant sections to feed the reranker
)

print(f"✅ Connected to local ChromaDB & DocStore at: {BASE_DIR}")


import re

def get_data_file_path() -> str:
    """Resolves and returns the path to NEXTIER_Internship_Bugs.md."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    possible_paths = [
        os.path.join(base_dir, "..", "..", "data", "NEXTIER_Internship_Bugs.md"),
        os.path.join(base_dir, "..", "data", "NEXTIER_Internship_Bugs.md"),
        "/Users/victorloucii/agentic_ai_engineer/Unified-Knowledge-Agent/data/NEXTIER_Internship_Bugs.md"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("Could not find NEXTIER_Internship_Bugs.md file.")


def parse_problem_id(message: str) -> str | None:
    """Parses problem ID from user query if they are requesting a log passthrough."""
    if not message:
        return None
    match = re.search(r"(?i)\bproblem\s*:?\s*(\d+)\b", message)
    if match:
        return match.group(1)
    return None


def extract_problem_block(problem_id: str) -> str | None:
    """Extracts a problem block from the bugs markdown file directly."""
    try:
        data_file = get_data_file_path()
        with open(data_file, "r", encoding="utf-8") as f:
            full_file_text = f.read()

        all_header_matches = list(
            re.finditer(
                r"(?im)^\s*(?:#|//)\s*problem\s*:?\s*(\d+)", full_file_text
            )
        )

        for i, match in enumerate(all_header_matches):
            prob_num = match.group(1)
            if prob_num == problem_id:
                start_idx = match.start()
                end_idx = (
                    all_header_matches[i + 1].start()
                    if i + 1 < len(all_header_matches)
                    else len(full_file_text)
                )
                block = full_file_text[start_idx:end_idx].strip()
                
                # Normalize header to '# Problem X'
                if not block.startswith(f"# Problem {problem_id}"):
                    first_line_end = block.find("\n")
                    if first_line_end != -1:
                        block = f"# Problem {problem_id}" + block[first_line_end:]
                    else:
                        block = f"# Problem {problem_id}"
                
                return f"{block}\n\n<END OF PROBLEM>"
    except Exception as e:
        print(f"🚨 [ERROR] extract_problem_block failed: {e}")
    return None