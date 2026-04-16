# backend/app.py
import os
import json
from contextlib import asynccontextmanager
from pydantic import BaseModel

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
# PHASE 5. FASTAPI & DB POOL LIFECYCLE
# ==========================================

# [FIX] Replaced the synchronous block with the new helper function
setup_database_tables()

async_pool = None
graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global async_pool, graph

    async_pool = AsyncConnectionPool(conninfo=DB_URI, max_size=10, open=False)
    await async_pool.open()

    memory = AsyncPostgresSaver(async_pool)
    
    # Compile the graph imported from backend.core.agents
    graph = workflow.compile(checkpointer=memory)
    print("🚀 Async Database Pool & LangGraph Engine Started")

    yield

    await async_pool.close()
    print("🛑 Async Database Pool Closed")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)