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

# [THE FIX] Wrap the raw store so it decodes bytes into Document objects
raw_store = LocalFileStore(store_directory)
store = create_kv_docstore(raw_store)

# The "Micro-Insight" scout: Finds the exact sentence that matches the query
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

#The "Context Diet": Prevents massive log files from becoming Mega-Chunks
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,  # Now uses the wrapped store
    child_splitter=child_splitter,
    parent_splitter=parent_splitter, # <-- Now enforces a size limit on the stored memory
    search_kwargs={"k": 25},         # <-- [FIX] Pulls top 25 most relevant sections to feed the reranker
)

print(f"✅ Connected to local ChromaDB & DocStore at: {BASE_DIR}")