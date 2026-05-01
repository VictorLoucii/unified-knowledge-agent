---
title: Unified Knowledge Agent (Internal Knowledge Base)
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: true
---

# 🧠 Unified Knowledge Agent: Internal Knowledge Base

**The Mission:** To transform 600+ fragmented technical internship logs into a deterministic, production-grade Agentic Intelligence layer. This system moves beyond "vibe-based" RAG by implementing strict logic guardrails, Human-in-the-loop (HITL) safety, and automated evaluation pipelines.

**Current Status:** Phase 8.0 - Hardened Production Logic & Frontend Sync

---

## 👁️ System Demo & UX

![Agent Demo](./assets/demo.gif)

### The "Yellow Card" Protocol (HITL)
The agent utilizes `on_agent_interrupt` to pause before executing heavy tools, requiring explicit human approval via the UI. The Phase 8 update ensures a seamless handshake between the LangGraph state and the Next.js frontend.

<div align="center">
  <img src="./assets/ss1.png" alt="Interface Snapshot 1" width="48%">
  <img src="./assets/ss2.png" alt="Interface Snapshot 2" width="48%">
</div>

---

## 🚀 Phase 8.0: The Hardening & Sync Layer

Phase 8 shifts from architectural setup to **production-grade reliability and UI polish**:

* **Verified Retrieval Accuracy:** Achieved **100% Search Recall@k** across the entire internal dataset, ensuring the "Librarian" never misses a relevant log.
* **Agent Logic Scoring:** Validated an **83% Agent Logic Score** across 30 complex test cases in the `backend/evals/qa_dataset.json` Golden Dataset.
* **Advanced Markdown Rendering:** The frontend now utilizes `react-markdown` and `remark-gfm` to render technical logs, code blocks, and tables with full fidelity.
* **Regex Sanitization Firewall:** Implemented frontend-side regex sanitization to strip hidden metadata, system anchors, and `<END OF PROBLEM>` tags.
* **Internal Knowledge Base Branding:** Fully transitioned terminology from "Second Brain" to "Internal Knowledge Base" to align with enterprise standards.

---

## 🛠️ The Technical Stack

| Layer | Technology | Key Function |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Stateful state machine with HITL interrupts & persistence |
| **Cloud State** | **Supabase (PostgreSQL)** | State survives container prunes; enables multi-device sync |
| **Logic Layer** | **Python (FastAPI)** | Hardened "Raw Interceptors" & Regex Anchors |
| **Observability** | **LangSmith** | Real-time X-ray of tool-routing, latency, and cost |
| **Data Ingestion** | **ChromaDB** | Vector storage using `all-MiniLM-L6-v2` local embeddings |
| **Frontend** | **Next.js 14 / Tailwind** | Markdown-rendered UI with HITL "Action Required" status |

---

## 📂 Project Structure
```text
.
├── assets/                # UI snapshots and demo media
├── backend/          
│   ├── app.py             # FastAPI Entry & Lifecycle
│   ├── basics.ipynb       # RAG experimentation & embedding logic
│   ├── chroma_db/         # Local vector database storage
│   ├── core/              
│   │   ├── agents.py      # LangGraph node logic & system rules
│   │   ├── config.py      # VectorStore & Supabase PostgresSaver setup
│   │   └── tools.py       # Librarian Triage & Search tools
│   ├── evals/             
│   │   ├── eval.py        # Automated LLM-as-a-Judge evaluation
│   │   └── qa_dataset.json # Phase 8.0 Golden Dataset (30 cases)
│   ├── memory.py          # Persistence logic
│   └── static/            # Static assets for the backend
├── data/                  
│   └── NEXTIER_Internship_Bugs.md   # Standardized source of truth
├── frontend/         
│   ├── src/               
│   │   ├── app/           # Next.js App Router (layout/page)
│   │   ├── components/    # Chat UI (Header, Input, MessageList, Sidebar)
│   │   ├── hooks/         # useChatStream for HITL approval flow
│   │   └── types/         # TypeScript definitions for agents
│   ├── next.config.ts     # Frontend configuration
│   └── frontend.Dockerfile # Containerization for Next.js
├── docker-compose.yml     # Multi-container orchestration (Backend + Frontend)
├── Dockerfile             # Backend containerization
├── generate_dataset.py    # Synthetic dataset generation script
├── pyproject.toml         # Python dependencies (uv)
└── uv.lock                # Deterministic lockfile