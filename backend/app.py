#FastAPI-LangChain-Streaming/app.py
import os
import json
from datetime import datetime
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from pydantic import BaseModel

# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse

# Langchain / LangGraph Imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings # [NEW] Added Embeddings
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver # [NEW] Added Memory Checkpointer
from langchain_chroma import Chroma # [NEW] Added Chroma

# ==========================================
# 1. ENVIRONMENT & LLM SETUP
# ==========================================
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("🚨 OPENAI_API_KEY not found! Check your .env file.")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Nexteir_Second_Brain_Prod"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

# ==========================================
# 2. VECTOR DB INITIALIZATION [NEW]
# ==========================================
# Connect to the persistent DB created in basics.ipynb
persist_directory = "./chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(
    persist_directory=persist_directory, 
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
print("✅ Connected to local ChromaDB.")

# ==========================================
# 3. TOOL DEFINITIONS
# ==========================================
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time. Use this when the user asks for the time."""
    return datetime.now().strftime(format)

#  The Agentic RAG Tool ported from notebook
@tool
def search_internship_history(query: str) -> str:
    """
    Use this tool to search the Nexteir Internship logs for debugging solutions, 
    React Native issues, architectural decisions (like Yarn vs NPM), and UI fixes.
    Input should be a clear, concise search query.
    """
    docs = retriever.invoke(query)
    formatted_context = "\n\n---\n\n".join(
        [f"Page {doc.metadata.get('page', 'Unknown')}:\n{doc.page_content}" for doc in docs]
    )
    return formatted_context

# [NEW] Registered the new tool
tools = [get_system_time, search_internship_history]
llm_with_tools = llm.bind_tools(tools)

# ==========================================
# 4. LANGGRAPH SETUP (The "Brain")
# ==========================================
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chatbot_node(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

workflow = StateGraph(State)

# Add Nodes
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", ToolNode(tools=tools))

# Set Routing logic
workflow.set_entry_point("chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

# [NEW] Compile Graph with Memory Checkpointer
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# ==========================================
# 5. FASTAPI SETUP (The "Bridge")
# ==========================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_session" # [NEW] Added thread tracking

async def generate_chat_responses(user_message: str, thread_id: str):
    inputs = {"messages": [HumanMessage(content=user_message)]}
    config = {"configurable": {"thread_id": thread_id}} # [NEW] Pass thread to config
    
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
        print(f"🚨 Backend Crash: {e}")
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
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)