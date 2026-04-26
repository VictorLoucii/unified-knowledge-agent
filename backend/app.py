# backend/app.py
import os
import json
from contextlib import asynccontextmanager
from pydantic import BaseModel
from langchain_text_splitters import MarkdownHeaderTextSplitter
from backend.core.config import retriever, store, parent_splitter
import asyncio

from backend.memory import (
    DB_URI,
    setup_database_tables,
    save_thread_title,
    get_all_threads_history,
    delete_thread_from_db,
)

# Core Component Imports
from backend.core.agents import workflow

# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from langchain_core.messages import HumanMessage

# LangGraph / Postgres checkpointer
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool


# ==========================================
# PHASE 4.5. COLD-START AUTO-INGESTION
# ==========================================
def initialize_rag():
    print("🧠 Checking Vector Database state...")

    # 1. Check if the docstore already has data (using yield_keys to avoid loading everything)
    try:
        # yield_keys returns a generator, so we check if it has at least one item
        first_key = next(store.yield_keys(), None)
        if first_key is not None:
            print(
                "✅ Vector Database & DocStore populated. Proceeding with existing index."
            )
            return
    except Exception as e:
        print(f"⚠️ Error checking docstore: {e}")

    print("⚠️ Vector Database empty. Initiating Cold-Start Auto-Ingestion...")

    # 2. Resolve exact paths (app.py is in backend/, data/ is one level up)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
    DATA_FILE = os.path.join(ROOT_DIR, "data", "NEXTIER_Internship_Bugs.md")

    if not os.path.exists(DATA_FILE):
        print(f"🚨 ERROR: Source data not found at {DATA_FILE}")
        return

    # 3. Read and split the markdown specifically by headers
    print("📄 Loading and splitting markdown data by headers...")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        markdown_document = f.read()

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    md_header_splits = markdown_splitter.split_text(markdown_document)

    # ==========================================
    # [THE MONSTER DOC FIX]
    # Document 330 is so massive that it generates 6,611 child chunks.
    # We MUST pre-split these header sections so no single document
    # overflows the Langchain -> ChromaDB transaction limit.
    # ==========================================
    safe_splits = parent_splitter.split_documents(md_header_splits)

    print(
        f"⚙️ Adding {len(safe_splits)} safe parent documents to the Retriever in batches..."
    )

    # Because we pre-split them, we can safely raise the batch size back up
    # for a faster ingestion process!
    BATCH_SIZE = 100
    for i in range(0, len(safe_splits), BATCH_SIZE):
        batch = safe_splits[i : i + BATCH_SIZE]
        print(
            f"📦 Processing batch {i//BATCH_SIZE + 1} (Documents {i} to {i + len(batch)})..."
        )
        retriever.add_documents(batch)

    print("✅ Auto-Ingestion complete. The Agent's memory is hydrated.")


# ==========================================
# PHASE 5. FASTAPI & DB POOL LIFECYCLE
# ==========================================

# [FIX] Replaced the synchronous block with the new helper function
setup_database_tables()

async_pool = None
graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global async_pool, graph

    # 1. Start the DB Pool first so the app is ready
    async_pool = AsyncConnectionPool(conninfo=DB_URI, max_size=10, open=False)
    await async_pool.open()

    memory = AsyncPostgresSaver(async_pool)

    #  We add the interrupt. This freezes the state right before 'tools' executes.
    graph = workflow.compile(checkpointer=memory, interrupt_before=["tools"])
    print("🚀 Async Database Pool & LangGraph Engine Started")

    # 2. Run the heavy auto-ingestion in a background thread!
    # This lets FastAPI finish starting up and pass Hugging Face health checks instantly.
    asyncio.create_task(asyncio.to_thread(initialize_rag))

    yield

    await async_pool.close()
    print("🛑 Async Database Pool Closed")


app = FastAPI(lifespan=lifespan)

# [PHASE 6 UPDATE] Secure CORS for Vercel Handshake
# Reads the frontend URL from environment, defaults to localhost to prevent breaking local dev
frontend_url = os.environ.get("VERCEL_FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # <Allows any local origin format
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# DEPLOYMENT HEALTH CHECK
# ==========================================
@app.get("/health")
async def health_check():
    """
    Fastest way to verify if the latest Git Push is live
    and if the RAG brain has finished hydrating.
    """
    try:
        # Check if at least one document exists in the store
        is_hydrated = next(store.yield_keys(), None) is not None
    except Exception:
        is_hydrated = False

    return {
        "status": "online",
        "version": "6.2-stable",  # <--- CHANGE THIS ON EVERY PUSH
        "rag_hydrated": is_hydrated,
        "provider": "Hugging Face Spaces",
    }


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_session"


async def generate_chat_responses(user_message: str, thread_id: str):
    inputs = {"messages": [HumanMessage(content=user_message)]}
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # [NEW] Save title before streaming starts
        await save_thread_title(async_pool, thread_id, user_message)

        async for event in graph.astream_events(inputs, config, version="v2"):
            kind = event["event"]

            safe_event = {
                "event": kind,
                "name": event.get("name", ""),
                "run_id": event.get("run_id", ""),
                "data": {},
            }

            if kind == "on_chat_model_stream":
                # [FIX] Block the expansion LLM from leaking into the UI stream
                if event.get("name") == "Expansion_LLM":
                    continue

                chunk = event["data"].get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    safe_event["data"]["chunk"] = {"content": chunk.content}
                    yield f"data: {json.dumps(safe_event)}\n\n"

            elif kind in ["on_tool_start", "on_tool_end"]:
                yield f"data: {json.dumps(safe_event)}\n\n"
            # [NEW] Check if the graph is currently interrupted
        state = await graph.aget_state(config)
        if state.next and "tools" in state.next:
            # Send a special signal to the frontend
            interrupt_event = {
                "event": "on_agent_interrupt",
                "data": {"waiting_for": "tool_approval"}
            }
            yield f"data: {json.dumps(interrupt_event)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        import traceback

        print("🚨 Backend Crash Details:")
        traceback.print_exc()

        print(f"🚨 Raw Error: {repr(e)}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"


@app.get("/")
async def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "FastAPI LangGraph Streaming Backend is running!"}

class ActionRequest(BaseModel):
    thread_id: str
    approve: bool  # True to proceed, False to cancel

@app.post("/chat_approve")
async def chat_approve(request: ActionRequest):
    """Endpoint for the frontend to approve or reject a pending tool call."""
    if request.approve:
        return StreamingResponse(
            resume_graph_stream(request.thread_id),
            media_type="text/event-stream"
        )
    else:
        return {"status": "action_cancelled"}

async def resume_graph_stream(thread_id: str):
    """Resumes the graph from the exact point it was paused."""
    config = {"configurable": {"thread_id": thread_id}}
    try:
        # Passing 'None' tells LangGraph to pick up exactly where it left off
        async for event in graph.astream_events(None, config, version="v2"):
            kind = event["event"]
            safe_event = {
                "event": kind,
                "name": event.get("name", ""),
                "run_id": event.get("run_id", ""),
                "data": {},
            }

            if kind == "on_chat_model_stream":
                if event.get("name") == "Expansion_LLM":
                    continue
                chunk = event["data"].get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    safe_event["data"]["chunk"] = {"content": chunk.content}
                    yield f"data: {json.dumps(safe_event)}\n\n"

            elif kind in ["on_tool_start", "on_tool_end"]:
                yield f"data: {json.dumps(safe_event)}\n\n"

        # Check if it hit ANOTHER interrupt (unlikely, but good practice)
        state = await graph.aget_state(config)
        if state.next and "tools" in state.next:
            interrupt_event = {
                "event": "on_agent_interrupt",
                "data": {"waiting_for": "tool_approval"}
            }
            yield f"data: {json.dumps(interrupt_event)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"


@app.post("/chat_stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        generate_chat_responses(request.message, request.thread_id),
        media_type="text/event-stream",
    )


# ==========================================
# 6. MEMORY & HISTORY ENDPOINTS
# ==========================================
@app.get("/history")
async def get_all_threads(limit: int = 20, offset: int = 0):
    """Fetches a list of all unique thread IDs and their titles from PostgreSQL."""
    try:
        threads = await get_all_threads_history(async_pool, limit, offset)
        # If we get exactly the limit amount, there are likely more rows to fetch
        has_more = len(threads) == limit
        return {"threads": threads, "has_more": has_more}
    except Exception as e:
        print(f"🚨 Error fetching threads: {e}")
        return {"error": str(e), "threads": [], "has_more": False}


@app.get("/history/{thread_id}")
async def get_thread_history(thread_id: str):
    """Fetches the message history for a specific thread_id."""
    try:
        config = {"configurable": {"thread_id": thread_id}}
        state = await graph.aget_state(config)

        if not state or not hasattr(state, "values") or "messages" not in state.values:
            return {"messages": []}

        formatted_messages = []
        for msg in state.values["messages"]:
            # Skip system messages, raw tool output, and empty AI tool-call messages
            if msg.type in ["system", "tool"] or not msg.content:
                continue

            formatted_messages.append(
                {
                    "role": "user" if msg.type == "human" else "assistant",
                    "content": msg.content,
                }
            )

        return {"messages": formatted_messages}
    except Exception as e:
        print(f"🚨 Error fetching thread state: {e}")
        return {"error": str(e), "messages": []}


# Added Delete Endpoint
@app.delete("/history/{thread_id}")
async def delete_thread(thread_id: str):
    """Deletes all data for a specific thread_id."""
    try:
        await delete_thread_from_db(async_pool, thread_id)
        return {"status": "success"}
    except Exception as e:
        print(f"🚨 Delete Error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    import os

    # Hugging Face uses port 7860 by default.
    # This also falls back to 7860 locally if PORT isn't set.
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
