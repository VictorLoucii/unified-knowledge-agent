
---

# 📊 Unified Knowledge Agent

**The mission:** To build a production-grade, full-stack Agentic RAG system that transforms static technical logs and documents into an interactive, reasoning intelligence layer.

Current Status: **Phase 5 Complete (Persistence, Professional UX & Power User Tools)**

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
* **Sticky Pinning:** Save important conversations to the top of the sidebar. Uses `localStorage` for UI persistence so your priority chats stay where they belong.
* **Bulk Management:** Efficient multi-select checkboxes with "Select All" logic. Perform concurrent deletions across multiple threads to keep the workspace clean.
* **Universal Copy System:** One-tap copying for both Human and AI messages. Includes a **Recursive Fallback Mechanism** to ensure functionality even on non-secure (HTTP/IP-based) local network testing.
* **Scalable Pagination:** Implemented `LIMIT` and `OFFSET` logic in the history retrieval layer, allowing the system to handle thousands of chat sessions with minimal initial load times.
* **URL Routing & Hydration:** Deep-linking support via URL query parameters (`?thread=[id]`), enabling users to bookmark or refresh specific chat sessions.
* **Optimistic UI Sync:** The sidebar updates instantly upon sending a new message, providing zero-latency feedback before the backend processing begins.

---

## 📂 Project Structure

```text
Unified-Knowledge-Agent/
├── backend/          
│   ├── app.py          # FastAPI routes, LangGraph workflow & SSE Logic
│   ├── memory.py       # Database schema setup, Paginated SQL queries & Deletion
│   └── chroma_db/      # Persistent Vector Store
├── frontend/         
│   ├── src/app/        # Next.js Chat UI with Pinning, Multi-select & Copy Logic
│   └── hooks/          # useChatStream hook for SSE handling & auto-hydration
├── data/               # Knowledge library (Internship logs/PDFs)
├── pyproject.toml      # Global dependencies managed by uv
└── uv.lock             # Deterministic lockfile
```

---

## 🛡️ Architecture Highlights

### **1. The Hybrid Persistence Model**
We utilize a dual-layer persistence strategy. **PostgreSQL** handles the heavy lifting of agent states and thread metadata, while **Browser LocalStorage** manages UI-specific states like pinned threads. This ensures a "snappy" interface that remembers your preferences without unnecessary database round-trips.

### **2. Resilient Clipboard Integration**
To support the "Always-Available" developer workflow, the clipboard logic detects `isSecureContext`. If testing over a local IP (standard in React Native development), the system automatically falls back to an invisible `textarea` injection method to bypass browser security blocks.

### **3. Cascading Deletion Protocol**
Deleting a thread triggers a clean-up across all relational tables. PostgreSQL `ON DELETE CASCADE` rules ensure that when a thread metadata record is removed, all associated LangGraph checkpoints, blobs, and writes are purged, preventing database bloat.

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
    cd frontend && npm run dev
    ```

---

## 🗺️ Roadmap: The Path to Production

- [x] **Phase 1-3:** Prototype development & RAG integration.
- [x] **Phase 4:** Standardization (FastAPI, Next.js, Mono-repo setup).
- [x] **Phase 5: Persistence & UX (Complete):**
    * **PostgreSQL** checkpointing & **Thread Metadata** tracking.
    * **Pagination Layer** for scalable history retrieval.
    * **Power User UX:** Pinning, Bulk Delete, and Universal Copy.
    * **Clipboard Fallback** for cross-network testing.
- [ ] **Phase 6: Deployment & Refinement:**
    * Dockerization & Cloud Deployment (Railway/AWS/Vercel).
    * Dynamic PDF ingestion API.
    * Multi-user authentication and secure session isolation.