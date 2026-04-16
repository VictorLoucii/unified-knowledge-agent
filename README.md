
---

# 📊 Unified Knowledge Agent

**The mission:** To build a production-grade, modular Agentic RAG system that transforms static technical logs into an interactive, reasoning intelligence layer—optimized for performance and zero-cost local indexing.

Current Status: **Phase 5.5 Complete (Modular Refactor & Zero-Waste RAG)**

---

## 🛠️ The Technical Stack

| Layer | Technology | Key Function |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Stateful, multi-turn agent logic & tool-calling |
| **Persistence** | **PostgreSQL** | Long-term memory & session checkpointing via `psycopg` |
| **Embeddings** | **HuggingFace (Local)** | `all-MiniLM-L6-v2` for **$0 cost** vector indexing |
| **LLM** | **GPT-4o-Mini** | High-reasoning, low-cost intelligence for the final answer |
| **Backend** | **FastAPI** | Modularized Python bridge (Pruned `app.py` + `core/` logic) |
| **Frontend** | **Next.js 14** | Responsive UI with real-time token streaming & history sidebar |
| **Vector DB** | **ChromaDB** | Local vector storage with Markdown-optimized parsing |

---

## 🚀 Key Features

* **Zero-Waste RAG Architecture:** Switched from OpenAI embeddings to local HuggingFace models. Indexing 5.4MB of data now costs **$0.00**, allowing for infinite database rebuilds during development.
* **Modular Backend Logic:** Refactored a 600-line monolith into a clean `core/` directory. Separation of concerns between `agents.py` (logic), `config.py` (infrastructure), and `tools.py` (capabilities).
* **Markdown-First Ingestion:** Migrated from `pypdf` to `.md` source files. This ensures high-fidelity parsing of code blocks and technical headers, significantly improving retrieval accuracy.
* **Long-Term Memory:** Integrated PostgreSQL checkpointer allows the agent to remember conversation context across browser refreshes and system restarts.
* **Universal Copy & Fallback:** Includes a **Recursive Fallback Mechanism** for clipboards, ensuring copy-paste works even when testing over local IP/HTTP environments.
* **Optimistic UI Sync:** The sidebar updates instantly upon sending a new message, providing zero-latency feedback.

---

## 📂 Project Structure

```text
Unified-Knowledge-Agent/
├── backend/          
│   ├── app.py             # Lean FastAPI entry point (Routes & Lifecycle)
│   ├── core/              # The "Brain" of the operation
│   │   ├── agents.py      # LangGraph state machine & workflow
│   │   ├── config.py      # LLM, Local Embeddings & VectorStore setup
│   │   └── tools.py       # Custom tools (Time, Stats, RAG Search)
│   ├── memory.py          # PostgreSQL schema & paginated history logic
│   ├── chroma_db/         # Local Vector Store (Persisted)
│   └── docstore/          # Local Parent-Document storage
├── frontend/         
│   ├── src/app/           # Next.js Chat UI (Pinning, Multi-select)
│   └── hooks/             # useChatStream hook for SSE handling
├── data/                  # Source Knowledge (.md / .pdf)
├── pyproject.toml         # Dependencies managed by uv
└── uv.lock                # Deterministic lockfile
```

---

## 🛡️ Architecture Highlights

### **1. Modular Logic Dispersal**
We follow a strict "Pruned Entry-Point" pattern. `app.py` is restricted to handling the FastAPI bridge and database pooling, while the Agentic logic is isolated in `backend/core/`. This prevents "Spaghetti Code" and makes the system 10x easier to debug or scale.

### **2. Local Embedding Efficiency**
By utilizing `sentence-transformers/all-MiniLM-L6-v2` locally, we've eliminated network latency and API credit "burn" during the RAG retrieval phase. The system performs hybrid re-ranking based on core keywords to ensure the most relevant internship logs are prioritized.

### **3. Scalable Persistence Layer**
A dual-layer strategy: **PostgreSQL** for heavy-lifting agent states/thread metadata and **Browser LocalStorage** for UI-specific states like pinned threads. 

---

## ⚡ Getting Started

### Prerequisites
* Python 3.12+ | Node.js 18+ | PostgreSQL | [uv](https://astral.sh/uv/install.sh)

### Installation & Setup

1.  **Clone & Sync:**
    ```bash
    git clone https://github.com/VictorLoucii/unified-knowledge-agent.git
    cd unified-knowledge-agent
    uv sync
    ```

2.  **Run the System:**
    ```bash
    # Start Backend
    uv run python backend/app.py
    
    # Start Frontend (In separate terminal)
    cd frontend && npm run dev
    ```

---

## 🗺️ Roadmap: The Path to Production

- [x] **Phase 1-3:** Prototype development & RAG integration.
- [x] **Phase 4:** Standardization (FastAPI, Next.js, Mono-repo setup).
- [x] **Phase 5: Persistence & UX:**
    * PostgreSQL checkpointing & Pagination.
    * Power User UX (Pinning, Bulk Delete, Universal Copy).
- [x] **Phase 5.5: Refinement (Current):**
    * **Modular Refactor:** Split `app.py` into `core/` modules.
    * **Zero-Waste RAG:** Local embeddings & `.md` data ingestion.
- [ ] **Phase 6: Deployment:**
    * Dockerization & Cloud Deployment (Railway/AWS).
    * Dynamic PDF/MD ingestion API.
    * Multi-user authentication.

---
