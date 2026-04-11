
---

# 📊 Unified Knowledge Agent

**The mission:** To build a production-grade, full-stack Agentic RAG system that transforms static technical logs and documents into an interactive, reasoning intelligence layer.

Current Status: **Phase 5 Complete (Persistence, Pagination & Professional UX)**

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
* **Scalable Pagination:** Implemented `LIMIT` and `OFFSET` logic in the history retrieval layer, allowing the system to handle thousands of chat sessions with minimal initial load times.
* **URL Routing & Hydration:** Deep-linking support via URL query parameters (`?thread=[id]`), enabling users to bookmark, share, or refresh specific chat sessions.
* **Optimistic UI Sync:** The sidebar updates instantly upon sending a new message, providing zero-latency feedback before the backend processing even begins.
* **Intelligent Session Naming:** Automatically generates chat titles from the initial user prompt, stored in a dedicated metadata table for fast retrieval.
* **Safe Session Deletion:** A cascading delete protocol cleans up internal LangGraph checkpoints (`checkpoint_writes`, `blobs`, `checkpoints`) and custom metadata synchronously.
* **Pro Empty State:** A custom welcome dashboard featuring interactive "Suggested Queries" to guide the user through the knowledge base.

---

## 📂 Project Structure

```text
Unified-Knowledge-Agent/
├── backend/          
│   ├── app.py          # FastAPI routes, LangGraph workflow & SSE Logic
│   ├── memory.py       # Database schema setup, Paginated SQL queries & Deletion
│   └── chroma_db/      # Persistent Vector Store
├── frontend/         
│   ├── src/app/        # Next.js Chat UI with Paginated Sidebar & Welcome Dashboard
│   └── hooks/          # useChatStream hook for SSE handling & auto-hydration
├── data/               # Knowledge library (Internship logs/PDFs)
├── pyproject.toml      # Global dependencies managed by uv
└── uv.lock             # Deterministic lockfile
```

---

## 🛡️ Architecture Highlights

### **1. The Metadata Layer**
To avoid the overhead of parsing binary LangGraph blobs, we implemented a `thread_metadata` table. When a new session starts, the backend captures the user prompt to store a relational title and a `created_at` timestamp for chronological sorting.

### **2. Efficient Pagination & Scaling**
To prevent the "Large History Slowdown," the `/history` endpoint supports chunked fetching. The frontend manages an `offset` state and appends new threads to the sidebar only when the user explicitly requests "Older Chats," maintaining a lightweight DOM.

### **3. Optimistic Synchronization & Hydration**
When a new chat starts, the frontend "optimistically" creates a sidebar entry. Upon stream completion, a callback triggers a background re-sync with the database to ensure the local UI perfectly matches the server-side state.

---

## ⚡ Getting Started

### Prerequisites
* Python 3.12+ | Node.js 18+ | PostgreSQL | [uv](https://astral.sh/uv/install.sh)

### Installation & Setup

1.  **Clone & Sync:**
    ```bash
    git clone https://github.com/victorloucii/unified-knowledge-agent.git
    cd unified-knowledge-agent
    uv sync
    ```

2.  **Run the System:**
    ```bash
    # Start Backend
    uv run uvicorn backend.app:app --reload
    # Start Frontend (In separate terminal)
    npm run dev
    ```

---

## 🗺️ Roadmap: The Path to Production

- [x] **Phase 1-3:** Prototype development & RAG integration.
- [x] **Phase 4:** Standardization (FastAPI, Next.js, Mono-repo setup).
- [x] **Phase 5: Persistence & UX (Complete):**
    * **PostgreSQL** checkpointing & **Thread Metadata** tracking.
    * **Pagination Layer** for scalable history retrieval.
    * **URL Routing** for session persistence across refreshes.
    * **Optimistic UI** & **Cascading Deletion** logic.
- [ ] **Phase 6: Deployment & Refinement:**
    * Dockerization & Cloud Deployment (Railway/AWS/Vercel).
    * Dynamic PDF ingestion API.
    * Multi-user authentication and secure session isolation.