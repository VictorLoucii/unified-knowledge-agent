# backend/app.py
import os
import json
import re
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


# ==========================================
# SECURITY & TOKEN-ABUSE GUARDRAILS
# ==========================================

def check_input_guardrail(message: str) -> str | None:
    """
    Checks user input for jailbreak or token-burning attempts.
    Returns a refusal message if a violation is found, or None if safe.
    """
    # 1. Length Cap
    if len(message) > 1000:
        return "⚠️ [Input Filter] Message too long. Please limit your query to under 1,000 characters."

    # 2. Pattern Matching
    lower_msg = message.lower().strip()
    
    # Check for prompt injection / jailbreak words
    jailbreak_keywords = [
        "ignore all previous", "ignore previous instructions", "ignore guidelines",
        "ignore rules", "ignore previous rules", "ignore all previous rules",
        "bypass rules", "you are now a", "jailbreak", "developer mode",
        "acting as a", "override instructions", "expose your system prompt",
        "reveal your system prompt", "api key", "database password", "db password"
    ]
    for kw in jailbreak_keywords:
        if kw in lower_msg:
            return "⚠️ [Input Filter] Request blocked. This query violates security guidelines regarding prompt modification or credential request."

    # Check for token-burning patterns (excessive text generation request)
    token_burn_patterns = [
        # Match "write a long fantasy story", "tell me a story", "generate a short creative poem", etc.
        # Now allows alphanumeric characters (like 3000) and up to 5 optional words in between.
        r"\b(?:write|generate|create|compose|tell|tell\s+me)\s+(?:a|an|me|us|the)?\s+(?:[a-zA-Z0-9]+\s+){0,5}(?:story|essay|novel|poem|play|song|script|article|report)\b",
        # Match standalone large word counts (e.g., "3000 words", "1500 word", "3k words") anywhere in the text
        r"\b\d{3,}\s*(?:words?|k\s*words?|thousand\s*words?)\b",
        r"\b\d+\s*k\s*words?\b",
        # Match "repeat this word", "repeat after me", "copy the text", etc.
        r"\b(?:repeat|copy|duplicate|print)\s+(?:this|the|following|word|character|sentence|paragraph|text|after\s+me)\b",
        # Match "loop indefinitely", "repeat forever", etc.
        r"\b(?:repeat|loop|print|run)\s+(?:[a-zA-Z]+\s+){0,3}(?:indefinitely|forever|infinite|again\s+and\s+again)\b",
    ]
    for pattern in token_burn_patterns:
        if re.search(pattern, lower_msg):
            return "⚠️ [Input Filter] Request blocked. Requests for excessive content generation (e.g., stories, essays, infinite loops) are restricted to protect API quotas."

    return None


def get_last_tool_output_length(state) -> int:
    """Helper to find the length of the last tool output in the chat history."""
    if not state or not hasattr(state, "values") or "messages" not in state.values:
        return 0
    # Search backwards for the last tool message
    for msg in reversed(state.values["messages"]):
        if msg.type == "tool" and msg.content:
            return len(msg.content)
    return 0


def mask_sensitive_data(text: str) -> str:
    """Scans and masks any API keys, DB passwords, or credentials before sending."""
    if not text:
        return text
    
    # Mask environment variable values dynamically
    sensitive_keys = ["OPENROUTER_API_KEY", "DATABASE_URL", "PGPASSWORD", "LANGCHAIN_API_KEY"]
    for key in sensitive_keys:
        val = os.getenv(key)
        if val and len(val) > 4 and val in text:
            text = text.replace(val, "[REDACTED SECRET]")
            
    # Mask typical OpenRouter / OpenAI API keys (sk-or-v1-...) with flexible length
    text = re.sub(r"\bsk-or-v1-[a-zA-Z0-9]{40,80}\b", "[REDACTED OPENROUTER KEY]", text)
    # Mask other typical API keys with flexible length
    text = re.sub(r"\bsk-[a-zA-Z0-9]{32,64}\b", "[REDACTED API KEY]", text)
    # Mask DB password patterns in connection strings
    text = re.sub(r"postgresql://[^:]+:([^@]+)@", "postgresql://user:[REDACTED_PASSWORD]@", text)
    
    return text


async def generate_chat_responses(user_message: str, thread_id: str):
    # 1. Run Input Guardrail Check
    refusal = check_input_guardrail(user_message)
    if refusal:
        # Save title before streaming starts
        await save_thread_title(async_pool, thread_id, user_message)
        error_event = {
            "event": "on_chat_model_stream",
            "name": "Guardrail",
            "run_id": "guardrail_violation",
            "data": {"chunk": {"content": refusal}},
        }
        yield f"data: {json.dumps(error_event)}\n\n"
        yield "data: [DONE]\n\n"
        return

    inputs = {"messages": [HumanMessage(content=user_message)]}
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # [NEW] Save title before streaming starts
        await save_thread_title(async_pool, thread_id, user_message)

        # Get initial state to find if any tools ran in previous turns (for follow-ups)
        state = await graph.aget_state(config)
        last_tool_output_length = get_last_tool_output_length(state)
        
        generated_chars_count = 0
        stream_buffer = ""
        BUFFER_WINDOW = 120
        max_allowed = max(2000, last_tool_output_length + 1500)

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
                    content = chunk.content
                    stream_buffer += content
                    
                    if len(stream_buffer) > BUFFER_WINDOW:
                        to_output = stream_buffer[:-BUFFER_WINDOW]
                        stream_buffer = stream_buffer[-BUFFER_WINDOW:]
                        
                        safe_output = mask_sensitive_data(to_output)
                        generated_chars_count += len(safe_output)
                        
                        if generated_chars_count > max_allowed:
                            warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                            safe_event["data"]["chunk"] = {"content": warning}
                            yield f"data: {json.dumps(safe_event)}\n\n"
                            yield "data: [DONE]\n\n"
                            return
                        
                        safe_event["data"]["chunk"] = {"content": safe_output}
                        yield f"data: {json.dumps(safe_event)}\n\n"

            elif kind in ["on_tool_start", "on_tool_end"]:
                if kind == "on_tool_end":
                    tool_output = event["data"].get("output")
                    if tool_output and isinstance(tool_output, str):
                        last_tool_output_length = len(tool_output)
                        max_allowed = max(2000, last_tool_output_length + 1500)
                yield f"data: {json.dumps(safe_event)}\n\n"

        # Flush remaining buffer
        if stream_buffer:
            safe_output = mask_sensitive_data(stream_buffer)
            generated_chars_count += len(safe_output)
            
            flush_event = {
                "event": "on_chat_model_stream",
                "name": "chatbot",
                "run_id": "flush_buffer",
                "data": {"chunk": {"content": safe_output}}
            }
            
            if generated_chars_count > max_allowed:
                warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                flush_event["data"]["chunk"]["content"] = warning
                yield f"data: {json.dumps(flush_event)}\n\n"
            else:
                yield f"data: {json.dumps(flush_event)}\n\n"

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
        state = await graph.aget_state(config)
        print(f"🤖 [DEBUG] resume_graph_stream state for thread {thread_id}: next = {state.next if state else None}")
        
        last_tool_output_length = get_last_tool_output_length(state)
        generated_chars_count = 0
        stream_buffer = ""
        BUFFER_WINDOW = 120
        max_allowed = max(2000, last_tool_output_length + 1500)

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
                    content = chunk.content
                    stream_buffer += content
                    
                    if len(stream_buffer) > BUFFER_WINDOW:
                        to_output = stream_buffer[:-BUFFER_WINDOW]
                        stream_buffer = stream_buffer[-BUFFER_WINDOW:]
                        
                        safe_output = mask_sensitive_data(to_output)
                        generated_chars_count += len(safe_output)
                        
                        if generated_chars_count > max_allowed:
                            warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                            safe_event["data"]["chunk"] = {"content": warning}
                            yield f"data: {json.dumps(safe_event)}\n\n"
                            yield "data: [DONE]\n\n"
                            return
                        
                        safe_event["data"]["chunk"] = {"content": safe_output}
                        yield f"data: {json.dumps(safe_event)}\n\n"

            elif kind in ["on_tool_start", "on_tool_end"]:
                if kind == "on_tool_end":
                    tool_output = event["data"].get("output")
                    if tool_output and isinstance(tool_output, str):
                        last_tool_output_length = len(tool_output)
                        max_allowed = max(2000, last_tool_output_length + 1500)
                yield f"data: {json.dumps(safe_event)}\n\n"

        # Flush remaining buffer
        if stream_buffer:
            safe_output = mask_sensitive_data(stream_buffer)
            generated_chars_count += len(safe_output)
            
            flush_event = {
                "event": "on_chat_model_stream",
                "name": "chatbot",
                "run_id": "flush_buffer",
                "data": {"chunk": {"content": safe_output}}
            }
            
            if generated_chars_count > max_allowed:
                warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                flush_event["data"]["chunk"]["content"] = warning
                yield f"data: {json.dumps(flush_event)}\n\n"
            else:
                yield f"data: {json.dumps(flush_event)}\n\n"

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
        import traceback
        print("🚨 resume_graph_stream Crash Details:")
        traceback.print_exc()
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
