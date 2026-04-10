# backend/app.py
import os
import json
from datetime import datetime
from typing import TypedDict, Annotated

from contextlib import asynccontextmanager  # [FIX] Added for FastAPI lifespan
from dotenv import load_dotenv
from pydantic import BaseModel

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
import psycopg  # [PHASE 5] Added for autocommit setup
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver  # [FIX] Async Saver
from psycopg_pool import ConnectionPool, AsyncConnectionPool  # [FIX] Async Pool
from langchain_chroma import Chroma


# ==========================================
# 1. ENVIRONMENT & LLM SETUP
# ==========================================
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("🚨 OPENAI_API_KEY not found! Check your .env file.")

# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "Nexteir_Second_Brain_Prod"

# Disable tracing temporarily since no LANGCHAIN_API_KEY is present
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_PROJECT"] = "Nexteir_Second_Brain_Prod"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

# ==========================================
# 2. VECTOR DB INITIALIZATION [NEW]
# ==========================================
import os

# This gets the absolute path to the directory where app.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# This explicitly points to backend/chroma_db
persist_directory = os.path.join(BASE_DIR, "chroma_db")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

print(f"✅ Connected to local ChromaDB at: {persist_directory}")

# ==========================================
# 3. TOOL DEFINITIONS
# ==========================================


@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time. Use this when the user asks for the time."""
    from datetime import datetime  # Just in case this import also got lost

    return datetime.now().strftime(format)


@tool
def search_internship_history(query: str) -> str:
    """
    Use this tool to search the Nexteir Internship logs for debugging solutions,
    React Native issues, architectural decisions (like Yarn vs NPM), and UI fixes.
    Input should be a clear, concise search query.
    """
    # 1. Multi-Query Expansion (Updated Prompt)
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

    # ... (The rest of the tool remains exactly the same: Execute search, deduplicate, format)
    # 2. Execute broad search
    all_docs = []
    for q in all_queries:
        all_docs.extend(retriever.invoke(q))

    # 3. Deduplicate
    unique_docs = {doc.page_content: doc for doc in all_docs}.values()

    # 4. Format
    formatted_context = "\n\n---\n\n".join(
        [
            f"Page {doc.metadata.get('page', 'Unknown')}:\n{doc.page_content}"
            for doc in unique_docs
        ]
    )

    return formatted_context


# Now both tools are defined before you bind them!
tools = [get_system_time, search_internship_history]
llm_with_tools = llm.bind_tools(tools)


# ==========================================
# 4. LANGGRAPH SETUP (The "Brain")
# ==========================================
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def chatbot_node(state: State):
    # [PHASE 5] User Persona - This could eventually be fetched from the DB based on user_id
    user_preferences = "Always prioritize TypeScript and focus on React Native performance optimization."

    # Define the "Identity" and "Rules" for your Agent
    system_prompt = SystemMessage(
        content=(
            f"You are the Nexteir Second Brain, a specialized AI assistant for Victor's internship logs. "
            f"USER PREFERENCES: {user_preferences} "
            "Your goal is to provide technical solutions based strictly on the provided documentation. "
            "CRITICAL RULE: If you find information labeled with '//problemX:', treat it as the "
            "definitive and primary answer for any questions about 'problem X'. "
            "Do not tell the user you 'cannot find' a problem if a result starting with '//problem' exists."
        )
    )

    # Prepend the system prompt to the existing conversation
    messages = [system_prompt] + state["messages"]

    # [CRITICAL FIX] Await the async invocation to prevent thread blocking during streaming
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}


workflow = StateGraph(State)

# Add Nodes
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", ToolNode(tools=tools))

# Set Routing logic
workflow.set_entry_point("chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

# [PHASE 5] Compile Graph with Postgres Checkpointer
DB_URI = os.getenv("DATABASE_URL", "postgresql://localhost/postgres")

# 1. Keep the synchronous setup block (it works perfectly for creating tables)
try:
    with psycopg.connect(DB_URI, autocommit=True) as conn:
        setup_memory = PostgresSaver(conn)
        setup_memory.setup()
    print("✅ PostgresSaver tables verified/created.")
except Exception as e:
    print(f"❌ Postgres Connection Error: {e}")
    print("👉 Ensure Postgres is running and DATABASE_URL in .env is correct.")


# 2. [CRITICAL FIX] Use Lifespan to start the async pool AFTER the server boots
async_pool = None
graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global async_pool, graph
    
    # [FIX] Initialize pool without opening it in constructor
    async_pool = AsyncConnectionPool(conninfo=DB_URI, max_size=10, open=False) 
    await async_pool.open() # Explicitly open it here
    
    memory = AsyncPostgresSaver(async_pool)
    graph = workflow.compile(checkpointer=memory)
    print("🚀 Async Database Pool & LangGraph Engine Started")
    
    yield
    
    await async_pool.close()
    print("🛑 Async Database Pool Closed")


# ==========================================
# 5. FASTAPI SETUP (The "Bridge")
# ==========================================
# Attach the lifespan to the app
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
    thread_id: str = "default_session"  # [NEW] Added thread tracking


async def generate_chat_responses(user_message: str, thread_id: str):
    inputs = {"messages": [HumanMessage(content=user_message)]}
    config = {"configurable": {"thread_id": thread_id}}  # [NEW] Pass thread to config

    try:
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
        traceback.print_exc()  # This prints the exact file and line number of the crash

        # Fallback to repr() to catch empty string errors
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
async def get_all_threads():
    """Fetches a list of all unique thread IDs from PostgreSQL."""
    try:
        # [FIX] Use async_pool and await the database commands
        async with async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id DESC;"
                )
                rows = await cur.fetchall()
                threads = [row[0] for row in rows]
        return {"threads": threads}
    except Exception as e:
        print(f"🚨 Error fetching threads: {e}")
        return {"error": str(e), "threads": []}


@app.get("/history/{thread_id}")
async def get_thread_history(thread_id: str):
    """Fetches the message history for a specific thread_id."""
    try:
        config = {"configurable": {"thread_id": thread_id}}
        # [FIX] Use aget_state instead of get_state for the async checkpointer
        state = await graph.aget_state(config)

        # If the thread hasn't been created yet, return empty
        if not state or not hasattr(state, "values") or "messages" not in state.values:
            return {"messages": []}

        formatted_messages = []
        for msg in state.values["messages"]:
            # Ignore SystemMessages for the frontend display
            if msg.type == "system":
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
