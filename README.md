

---

# 📊 Unified Knowledge Agent

**The mission:** To build a production-grade, full-stack Agentic RAG system that transforms static technical logs and documents into an interactive, reasoning intelligence layer.

Current Status: **Phase 4 Complete (Standardized Full-Stack Architecture)**

---

## 🛠️ The Technical Stack

| Layer | Technology | Key Function |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Stateful, multi-turn agent logic & tool-calling |
| **Backend** | **FastAPI** | High-performance Python bridge with streaming support |
| **Frontend** | **Next.js 14** | Responsive UI with real-time token streaming |
| **Environment** | **uv** | Blazing-fast Python package & project management |
| **Database** | **ChromaDB** | Vector storage for local technical logs (Phase 4) |

---

## 🚀 Key Features

* **Agentic Reasoning:** Unlike traditional RAG, this system uses an autonomous agent that decides *when* to retrieve data and *how* to synthesize complex answers.
* **Real-time Streaming:** Token-by-token response delivery for a seamless, ChatGPT-like user experience.
* **Professional Mono-repo:** A unified structure managed by `uv`, ensuring environment consistency across the backend and frontend.
* **Standardized Architecture:** Built with scalability in mind, separating the intelligence layer (LangGraph) from the delivery layer (FastAPI).

---

## 📂 Project Structure

```text
Unified-Knowledge-Agent/
├── backend/          # LangGraph engine + FastAPI streaming bridge
├── frontend/         # Next.js React application
├── data/             # Knowledge library (Internship logs/PDFs)
├── pyproject.toml    # Global dependencies managed by uv
└── uv.lock           # Deterministic lockfile for production parity
```

---

## ⚡ Getting Started

### Prerequisites
* Python 3.12+
* Node.js 18+
* [uv](https://github.com/astral-sh/uv) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/victorloucii/unified-knowledge-agent.git
   cd unified-knowledge-agent
   ```

2. **Set up the Backend:**
   ```bash
   # uv automatically handles the virtual environment and syncs dependencies
   uv sync
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the `backend/` directory:
   ```env
   OPENAI_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   ```

4. **Run the System:**
   From the root directory:
   ```bash
   uv run backend/app.py
   ```

---

## 🗺️ Roadmap: The Path to Production

- [x] **Phase 1-3:** Prototype development & RAG integration.
- [x] **Phase 4:** Standardization (FastAPI, Next.js, Mono-repo setup).
- [ ] **Phase 5: Cloud Migration (Current Target):** * Replace local storage with **Supabase (Postgres + pgvector)**.
    * Implement persistent conversation memory.
    * Integrate **LangSmith** for observability.
- [ ] **Phase 6: Production Scaling:**
    * Dockerization for cloud deployment (Railway/AWS).
    * Dynamic PDF ingestion API.


---
