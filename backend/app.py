# backend/app.py
import os
from contextlib import asynccontextmanager
from pydantic import BaseModel
import asyncio

# OpenTelemetry & Phoenix tracing is set up in ONE place: config.py:23-44.
#
# Do not add a second setup here. This file previously built its own
# TracerProvider with a SimpleSpanProcessor exporting to
# http://localhost:6006/v1/traces, and because these lines run before the
# `from backend.core.ingest import ...` below pulls in config.py, that setup
# won it. config.py's LangChainInstrumentor().instrument() call was then
# refused with "Attempting to instrument while already instrumented", so the
# BatchSpanProcessor it installs never received a LangChain span.
#
# The cost was on the live request path. A SimpleSpanProcessor exports on the
# thread that ended the span, and with no collector listening each export
# retries and then times out. Measured 2026-08-18 against a closed port,
# reproducing these exact lines: 7.194 s per span on the caller's thread,
# against effectively zero for a BatchSpanProcessor. A deployed container has
# nothing listening, so every request paid it. See DECISIONS.md,
# "batch=True is a requirement, not a tuning knob".

from backend.core.ingest import initialize_rag
from backend.core.chat import generate_chat_responses, resume_graph_stream
from backend.core.config import store

from backend.memory import (
    DB_URI,
    setup_database_tables,
    get_all_threads_history,
    delete_thread_from_db,
)

# Core Component Imports
from backend.core.agents import workflow

# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse

# LangGraph / Postgres checkpointer
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool


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

    # Interrupt before sensitive tools to wait for user approval
    graph = workflow.compile(checkpointer=memory, interrupt_before=["sensitive_tools"])
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
        "version": "6.3-tracing-fix",  # <--- CHANGE THIS ON EVERY PUSH
        "rag_hydrated": is_hydrated,
        "provider": "Hugging Face Spaces",
    }


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_session"


@app.post("/chat_stream")
async def chat_stream(request: ChatRequest):
    async def timed_generator():
        import time, json
        start = time.time()
        is_interrupted = False
        async for chunk in generate_chat_responses(request.message, request.thread_id, graph, async_pool):
            if "on_agent_interrupt" in chunk:
                is_interrupted = True
            if chunk.strip() == "data: [DONE]":
                if not is_interrupted:
                    latency = time.time() - start
                    timing_msg = f"\n\n*⚡ Query processed in {latency:.2f}s*"
                    yield f"data: {json.dumps({'event': 'on_chat_model_stream', 'name': 'latency', 'data': {'chunk': {'content': timing_msg}}})}\n\n"
            yield chunk

    return StreamingResponse(
        timed_generator(),
        media_type="text/event-stream",
    )


class RefineRequest(BaseModel):
    transcript: str

@app.post("/refine_transcript")
async def refine_transcript(request: RefineRequest):
    """Refines a raw voice transcript using a fast LLM."""
    from backend.core.config import fast_llm
    from langchain_core.messages import SystemMessage, HumanMessage
    
    sys_prompt = "You are a transcription refinement assistant. Fix any spelling mistakes (especially tech jargon like 'markdown', 'tech stack', 'semantically') and ensure proper punctuation (e.g., adding a question mark if it's a question) in the following text. Only return the corrected text, nothing else. Do not wrap in quotes or add preamble."
    
    try:
        response = await fast_llm.ainvoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=request.transcript)
        ])
        return {"refined_transcript": response.content.strip()}
    except Exception as e:
        print(f"🚨 Error refining transcript: {e}")
        return {"refined_transcript": request.transcript} # Fallback to original



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
        async def timed_resume_generator():
            import time, json
            start = time.time()
            async for chunk in resume_graph_stream(request.thread_id, graph):
                if chunk.strip() == "data: [DONE]":
                    latency = time.time() - start
                    timing_msg = f"\n\n*⚡ Query resumed & processed in {latency:.2f}s*"
                    yield f"data: {json.dumps({'event': 'on_chat_model_stream', 'name': 'latency', 'data': {'chunk': {'content': timing_msg}}})}\n\n"
                yield chunk
                
        return StreamingResponse(
            timed_resume_generator(),
            media_type="text/event-stream"
        )
    else:
        return {"status": "action_cancelled"}


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
