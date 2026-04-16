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

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("🚨 OPENAI_API_KEY not found! Check your .env file.")

# Disable tracing temporarily since no LANGCHAIN_API_KEY is present
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_PROJECT"] = "Nexteir_Second_Brain_Prod"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

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

child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,  # Now uses the wrapped store
    child_splitter=child_splitter,
    search_kwargs={"k": 15},
)

print(f"✅ Connected to local ChromaDB & DocStore at: {BASE_DIR}")