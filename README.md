
---

# 📊 Unified Knowledge Agent

**The mission:** To build a production-grade, full-stack Agentic RAG system that transforms static technical logs and documents into an interactive, reasoning intelligence layer.

Current Status: **Phase 5 Refined (Persistence, Metadata & UI Optimization)**

---

## 🛠️ The Technical Stack

| Layer | Technology | Key Function |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Stateful, multi-turn agent logic & tool-calling |
| **Persistence** | **PostgreSQL** | Long-term memory & session checkpointing via `psycopg` |
| **Metadata** | **Relational SQL** | Custom `thread_metadata` table for intelligent session naming |
| **Backend** | **FastAPI** | High-performance Python bridge with async streaming |
| **Frontend** | **Next.js 14** | Responsive UI with real-time token streaming & history sidebar |
| **Environment** | **uv** | Blazing-fast Python package & project management |
| **Vector DB** | **ChromaDB** | Vector storage for local technical internship logs |

---

## 🚀 Key Features

* **Long-Term Memory:** Integrated PostgreSQL checkpointer allows the agent to remember conversation context across browser refreshes and system restarts.
* **Intelligent Session Naming:** Automatically generates chat titles from the initial user prompt, stored in a dedicated metadata table for fast retrieval.
* **Safe Session Deletion:** Implemented a cascading delete protocol that cleans up LangGraph checkpoints (`checkpoint_writes`, `blobs`, and `checkpoints`) alongside session metadata without leaving orphaned data.
* **Clean History Reconstruction:** Advanced server-side filtering removes intermediate "AI Thinking" states and raw tool outputs, ensuring historical sessions are as readable as live chats.
* **Asynchronous Streaming:** Fully non-blocking SSE (Server-Sent Events) architecture for token-by-token response delivery.
* **Async Database Pooling:** High-concurrency management using `psycopg_pool` to ensure the database remains responsive under load.

---

## 📂 Project Structure

```text
Unified-Knowledge-Agent/
├── backend/          
│   ├── app.py          # FastAPI routes, LangGraph workflow & SSE Logic
│   ├── memory.py       # Database schema setup, Metadata handling & Deletion logic
│   └── chroma_db/      # Persistent Vector Store
├── frontend/         
│   ├── src/app/        # Next.js Chat UI with Sidebar state management
│   └── hooks/          # useChatStream for SSE processing & history hydration
├── data/               # Knowledge library (Internship logs/PDFs)
├── pyproject.toml      # Global dependencies managed by uv
└── uv.lock             # Deterministic lockfile
```

---

## 🛡️ Architecture Highlights

### **1. The Metadata Layer (Option A Implementation)**
To avoid the overhead of parsing binary LangGraph blobs, we implemented a `thread_metadata` table. When a new session starts, the backend captures the first 40 characters of the user's prompt and stores it as a relational title, which is then `LEFT JOIN`ed during history fetches.

### **2. Cascading Deletion**
To maintain database integrity, the deletion endpoint targets the LangGraph internal tables in a specific order to respect foreign key constraints:
1. `checkpoint_writes`
2. `checkpoint_blobs`
3. `checkpoints`
4. `thread_metadata`

### **3. UI Logic: Message Filtering**
We solved the "Double Bubble" and "Vertical Text" glitch by filtering the message stream. The backend now skips `system` messages, `tool` outputs, and empty AI "thought" messages, ensuring the user only sees polished content.

---

## ⚡ Getting Started

### Prerequisites
* Python 3.12+
* Node.js 18+
* [PostgreSQL](https://www.postgresql.org/) (Ensure the service is running)
* [uv](https://github.com/astral-sh/uv) installed

### Installation & Setup

1. **Clone & Sync:**
   ```bash
   git clone https://github.com/victorloucii/unified-knowledge-agent.git
   cd unified-knowledge-agent
   uv sync
   ```

2. **Configure Environment:**
   ```env
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=postgresql://localhost/postgres
   ```

3. **Run the System:**
   ```bash
   uv run uvicorn backend.app:app --reload
   ```

---

## 🗺️ Roadmap: The Path to Production

- [x] **Phase 1-3:** Prototype development & RAG integration.
- [x] **Phase 4:** Standardization (FastAPI, Next.js, Mono-repo setup).
- [x] **Phase 5: Persistence Layer (Complete):**
    * Integrated **PostgreSQL** for checkpointing.
    * Implemented **Thread Metadata** for session naming.
    * Built **Safe Delete** functionality for session management.
    * Optimized **History Filtering** for clean UI rendering.
- [ ] **Phase 6: Deployment & Refinement:**
    * Dockerization for cloud deployment (Railway/AWS).
    * Dynamic PDF ingestion API for real-time document updates.
    * Multi-user authentication and secure session isolation.

---
