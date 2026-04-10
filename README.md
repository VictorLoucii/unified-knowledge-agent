
---

# 📊 Unified Knowledge Agent

**The mission:** To build a production-grade, full-stack Agentic RAG system that transforms static technical logs and documents into an interactive, reasoning intelligence layer.

Current Status: **Phase 5 Complete (PostgreSQL Persistence & Long-Term Memory)**

---

## 🛠️ The Technical Stack

| Layer | Technology | Key Function |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Stateful, multi-turn agent logic & tool-calling |
| **Persistence** | **PostgreSQL** | Long-term memory & session checkpointing via `psycopg` |
| **Backend** | **FastAPI** | High-performance Python bridge with async streaming |
| **Frontend** | **Next.js 14** | Responsive UI with real-time token streaming & history sidebar |
| **Environment** | **uv** | Blazing-fast Python package & project management |
| **Vector DB** | **ChromaDB** | Vector storage for local technical internship logs |

---

## 🚀 Key Features

* **Long-Term Memory:** Integrated PostgreSQL checkpointer allows the agent to remember conversation context across browser refreshes and system restarts.
* **Persistent Sessions:** A dedicated sidebar enables users to toggle between multiple historical chat sessions, reconstructing the agent's state instantly.
* **Agentic Reasoning:** An autonomous agent that intelligently decides when to retrieve data and how to synthesize technical solutions.
* **Asynchronous Streaming:** Fully non-blocking SSE (Server-Sent Events) architecture for token-by-token response delivery.
* **Async Database Pooling:** High-concurrency management using `psycopg_pool` to ensure the database remains responsive under load.

---

## 📂 Project Structure

```text
Unified-Knowledge-Agent/
├── backend/          # LangGraph engine + FastAPI + PostgreSQL checkpointer
├── frontend/         # Next.js React application + Chat History Sidebar
├── data/             # Knowledge library (Internship logs/PDFs)
├── pyproject.toml    # Global dependencies managed by uv
└── uv.lock           # Deterministic lockfile for production parity
```

---

## ⚡ Getting Started

### Prerequisites
* Python 3.12+
* Node.js 18+
* [PostgreSQL](https://www.postgresql.org/) (Ensure the service is running)
* [uv](https://github.com/astral-sh/uv) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/victorloucii/unified-knowledge-agent.git
   cd unified-knowledge-agent
   ```

2. **Initialize Dependencies:**
   ```bash
   # uv automatically handles the virtual environment and syncs dependencies
   uv sync
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=postgresql://localhost/postgres
   ```

4. **Run the System:**
   Start the backend:
   ```bash
   uv run uvicorn backend.app:app --reload
   ```

---

## 🗺️ Roadmap: The Path to Production

- [x] **Phase 1-3:** Prototype development & RAG integration.
- [x] **Phase 4:** Standardization (FastAPI, Next.js, Mono-repo setup).
- [x] **Phase 5: Persistence Layer:**
    * Integrated **PostgreSQL** for checkpointing.
    * Developed persistent sidebar UI for session management.
    * Implemented async connection pooling for high-performance memory retrieval.
- [ ] **Phase 6: Deployment & Refinement:**
    * Dockerization for cloud deployment (Railway/AWS).
    * Dynamic PDF ingestion API for real-time document updates.
    * Multi-user authentication and secure session isolation.

---

