# backend/app.py
import os
import json
from datetime import datetime
from typing import TypedDict, Annotated

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from pydantic import BaseModel

from backend.memory import (
    DB_URI,
    setup_database_tables,
    save_thread_title,
    get_all_threads_history,
    delete_thread_from_db,
)

# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

# Langchain / LangGraph Imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import ConnectionPool, AsyncConnectionPool
from langchain_chroma import Chroma


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
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
persist_directory = os.path.join(BASE_DIR, "chroma_db")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

print(f"✅ Connected to local ChromaDB at: {persist_directory}")

# ==========================================
# 3. TOOL DEFINITIONS
# ==========================================


@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time. Use this when the user asks for the time."""
    from datetime import datetime

    return datetime.now().strftime(format)


@tool
def search_internship_history(query: str) -> str:
    """
    Use this tool to search the Nexteir Internship logs for debugging solutions,
    React Native issues, architectural decisions (like Yarn vs NPM), and UI fixes.
    Input should be a clear, concise search query.
    """
    expansion_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    search_variants = expansion_llm.invoke(
        f"Generate 3 diverse search queries to find information about '{query}' "
        "in technical internship logs. "
        "CRITICAL INSTRUCTION: If the user is looking for a specific problem number, "
        "always include a variant formatted EXACTLY like '//problemX:' (no spaces, with colon). "
        "Also include variants focusing on the core concepts (e.g., 'MultiSelectAutocompleteField', 'skills modal'). "
        "Respond with only the queries, one per line."
    ).content.split("\n")

    all_queries = [query] + [q.strip() for q in search_variants if q.strip()]

    all_docs = []
    for q in all_queries:
        all_docs.extend(retriever.invoke(q))

    unique_docs = {doc.page_content: doc for doc in all_docs}.values()

    formatted_context = "\n\n---\n\n".join(
        [
            f"Page {doc.metadata.get('page', 'Unknown')}:\n{doc.page_content}"
            for doc in unique_docs
        ]
    )

    return formatted_context


tools = [get_system_time, search_internship_history]
llm_with_tools = llm.bind_tools(tools)


# ==========================================
# 4. LANGGRAPH SETUP (The "Brain")
# ==========================================
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def chatbot_node(state: State):
    user_preferences = "Always prioritize TypeScript and focus on React Native performance optimization."

    system_prompt = SystemMessage(
        content=(
            f"You are the Nexteir Second Brain, a specialized AI assistant for Victor's internship logs. "
            f"USER PREFERENCES: {user_preferences} "
            "Your goal is to provide technical solutions based strictly on the provided documentation. "
            "CRITICAL RULE: If you find information labeled with '//problemX:', treat it as the "
            "definitive and primary answer for any questions about 'problem X'. "
            "Do not tell the user you 'cannot find' a problem if a result starting with '//problem' exists. "
            "FORMATTING RULE: The retrieved context contains arbitrary line breaks from PDF extraction. You MUST remove unnecessary newlines, fix broken sentences, and format your output into natural, highly readable paragraphs and lists."
        )
    )

    messages = [system_prompt] + state["messages"]

    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}


workflow = StateGraph(State)

workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", ToolNode(tools=tools))

workflow.set_entry_point("chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

# [PHASE 5] Compile Graph with Postgres Checkpointer
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
    graph = workflow.compile(checkpointer=memory)
    print("🚀 Async Database Pool & LangGraph Engine Started")

    yield

    await async_pool.close()
    print("🛑 Async Database Pool Closed")


# ==========================================
# 5. FASTAPI SETUP (The "Bridge")
# ==========================================
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
# 6. MEMORY & HISTORY ENDPOINTS [PHASE 5]
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


# [NEW] Added Delete Endpoint
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
