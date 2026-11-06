# backend/core/config.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.storage import LocalFileStore, create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.core.skip_counter import count_skip

# ==========================================
# 1. ENVIRONMENT & LLM SETUP
# ==========================================
load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("🚨 OPENROUTER_API_KEY not found! Check your .env file.")

# Disabling LangSmith tracing in favor of Phoenix
os.environ.pop("LANGCHAIN_TRACING_V2", None)
os.environ.pop("LANGCHAIN_PROJECT", None)

try:
    from openinference.instrumentation.langchain import LangChainInstrumentor
    from phoenix.otel import register
    
    # Default the Phoenix endpoint to the local docker container, but let the
    # environment win. A plain assignment here overwrote whatever the deployed
    # container had been configured with, so it could never point the collector
    # elsewhere or opt out.
    os.environ.setdefault("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:4317")
    
    # batch=True is required, not a tuning knob. register() defaults to
    # batch=False (phoenix/otel/otel.py:68), which installs a SimpleSpanProcessor
    # and exports every span synchronously on the calling thread. When nothing is
    # listening on the collector endpoint each export blocks on a failed
    # connection, so the caller pays for it. A BatchSpanProcessor moves the
    # export to a background thread, so a missing collector costs nothing on the
    # request path.
    tracer_provider = register(batch=True)
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    print("✅ Arize Phoenix tracing successfully initialized.")
except Exception as e:
    print(f"⚠️ [WARNING] Failed to initialize Phoenix tracing: {e}")
    count_skip("startup_faults")

is_eval_mode = os.getenv("EVAL_MODE", "false").lower() == "true"

primary_llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "openai/gpt-5-mini"),
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
    streaming=not is_eval_mode,
    request_timeout=45,
    max_retries=2,  # Reduced so it fails over faster
    reasoning_effort="low",  # probe 2026-08-22: "minimal" picks the wrong tool for weather; "low" spends ~60 reasoning tokens
)

fallback_llm = ChatOpenAI(
    model="google/gemini-3.6-flash",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
    streaming=not is_eval_mode,
    request_timeout=45,
    max_retries=3,
)

fast_llm = ChatOpenAI(
    model="google/gemini-3.6-flash",  # NOT flash-lite: as the scope router it marks plain Python questions OUT_OF_SCOPE (6 eval failures, 2026-08-22)
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
    streaming=False,
    max_retries=2, request_timeout=45,  # G18: without a timeout a hung call never raises, so it would never reach the backup
)

llm = primary_llm.with_fallbacks([fallback_llm])
print(f"🤖 Loading LLM model: {llm.model_name}")

# G18: fast_llm's backup, on another vendor, so a Gemini outage does not stop the scope router.
# The string repeats primary_llm's default (config.py:51); a model migration changes both.
# streaming=False is required: a streaming backup would put the router's label into the
# visitor's stream (chat.py forwards every model stream event) and send conversational text twice.
fast_llm_backup = ChatOpenAI(
    model="openai/gpt-5-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
    streaming=False,
    request_timeout=45,
    max_retries=2,
    reasoning_effort="low",
)
fast_llm = fast_llm.with_fallbacks([fast_llm_backup])

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
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,  # Now uses the wrapped store
    child_splitter=child_splitter,
    parent_splitter=parent_splitter, # <-- Now enforces a size limit on the stored memory
    search_kwargs={"k": 40},         # <-- [FIX] Pulls top 40 most relevant sections to feed the reranker
)

print(f"✅ Connected to local ChromaDB & DocStore at: {BASE_DIR}")


def get_data_file_paths() -> list[str]:
    """Resolves and returns the paths to all active data sources."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # Try finding data in standard project structures
    possible_data_dirs = [
        os.path.join(base_dir, "..", "..", "data"),
        os.path.join(base_dir, "..", "data")
    ]
    
    target_data_dir = None
    for p in possible_data_dirs:
        if os.path.exists(p) and os.path.isdir(p):
            target_data_dir = p
            break
            
    if not target_data_dir:
        print("⚠️ [WARNING] Could not find the 'data' directory.")
        count_skip("startup_faults")
        return []

    data_paths = []
    for filename in os.listdir(target_data_dir):
        if filename.endswith(".md") or filename.endswith(".docx"):
            data_paths.append(os.path.join(target_data_dir, filename))
            
    if not data_paths:
        print(f"⚠️ [WARNING] No .md or .docx files found in {target_data_dir}.")
        count_skip("startup_faults")
        
    return data_paths


# ==========================================
# 3. FEATURE SWITCHES
# ==========================================
# Read at call time, so a test can flip one between a pause and a resume. The process
# environment is fixed until a restart, so the deployed app sees one value per process.
def _switch_on(name: str) -> bool:
    """Only "false" turns a feature off. Unset or empty means on, so a copied `NAME=` line changes nothing."""
    return os.getenv(name, "true").strip().lower() != "false"


def fast_path_enabled() -> bool:
    return _switch_on("FAST_PATH_ENABLED")


def transcript_refine_enabled() -> bool:
    return _switch_on("TRANSCRIPT_REFINE_ENABLED")


def weather_tool_enabled() -> bool:
    return _switch_on("WEATHER_TOOL_ENABLED")


print(
    f"🎚️ Feature switches: fast path {fast_path_enabled()}, "
    f"transcript refine {transcript_refine_enabled()}, weather tool {weather_tool_enabled()}"
)