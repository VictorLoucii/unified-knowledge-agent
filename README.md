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

**Current Status:** Phase 8.2 - Input/Output Guardrails, DLP Masking & Production Security

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

## 🚀 Phase 8.1: Modular Refactoring & 100% Logic Scores

Phase 8.1 focuses on **modular tooling, production performance optimization, and 100% recall/logic scores**:

* **Verified Retrieval Accuracy:** Achieved **100% Search Recall@k** across the entire internal dataset, ensuring the "Librarian" never misses a relevant log.
* **Perfect Agent Logic Scoring:** Achieved a **100% Agent Logic Score** across all 30 complex test cases in the `backend/evals/qa_dataset.json` Golden Dataset.
* **Modular Backend Architecture:** Split the bloated `tools.py` into a highly clean, specialized `backend/core/tools/` sub-package.
* **Configurable LLM Backends:** Integrated support for running evaluations and agent logic against multiple model backends using the `MODEL_NAME` environment variable (e.g., iterating cost-effectively with `google/gemini-2.0-flash-001` before performing a production "Golden Run" on `deepseek/deepseek-chat`).
* **Advanced Markdown Rendering:** The frontend now utilizes `react-markdown` and `remark-gfm` to render technical logs, code blocks, and tables with full fidelity.
* **Regex Sanitization Firewall:** Implemented frontend-side regex sanitization to strip hidden metadata, system anchors, and `<END OF PROBLEM>` tags.
* **Internal Knowledge Base Branding:** Fully transitioned terminology from "Second Brain" to "Internal Knowledge Base" to align with enterprise standards.

---

## 🚀 Phase 8.2: Input/Output Guardrails, DLP Masking & Production Security

Phase 8.2 introduces robust runtime security layers, token-protection guardrails, and Data Loss Prevention (DLP) to secure the agent against malicious inputs and cost abuse:

* **Fast Input Gatekeeper:** Added an instant regex-based validator at the API gateway level to enforce a **1,000-character input limit** and immediately block jailbreaks, system prompt exposures, and credentials requests.
* **Token-Abuse Prevention:** Intercepts requests for excessive content generation (e.g., writing stories, essays, novels, or infinite loops) at 0 token cost, protecting your API budget.
* **DLP Secret Masking:** Implemented a real-time sliding 120-character buffer window that automatically scans and redacts sensitive environment variables (such as OpenRouter keys, OpenAI keys, and database passwords) before they are streamed to the user's screen.
* **Dynamic Response Cap:** Replaces static text ceilings with a context-aware threshold: $\text{Max Allowed Chars} = \max(2000, \text{Last Tool Output Length} + 1500)$. General chat responses are capped at 2,000 characters, while legitimate debugging logs scale dynamically to avoid truncation.
* **Tool Sanitization (Least Privilege):** Truncates tool query arguments to a maximum of 150 characters and applies defensive XML tagging around untrusted user inputs fed to the query expansion LLM to prevent prompt injection.
* **Contextual UI Triggers:** The frontend "Generate Post-Mortem" button is now rendered conditionally, showing only when technical debugging logs (`# Problem`) have been active in the chat thread.

---

## 🚀 Phase 9: Token Optimization, Output Guardrail Truncation Fix & Server Modularization

Phase 9 introduces major architectural cleanups and cost optimization strategies, dramatically lowering LLM token consumption while fixing crucial output guardrail bugs:

* **Token Optimization & Cost Control**:
  * **Programmatic LLM Bypass**: Intercepts direct Problem requests (e.g. `Problem 33`, `details of problem 5`) at the API and Graph levels, fetching raw markdown blocks directly from the source logs. Streams the response in chunks simulating real-time LLM output, reducing both input and output token consumption to **0** for log-retrieval queries.
  * **System Prompt Compression**: Compressed rules, instructions, and query-mapping lists in the base system prompt by ~50%, saving 500-600 input tokens per turn.
  * **Context Diet**: Optimized vector store retrieval limits (`parent_splitter` chunk size from 1500 to 1000 characters, top matches limited to 5) and capped search block truncation limits to 5000 characters, minimizing input token leakage.
* **Output Guardrail Truncation Fix**:
  * **Robust Length Parser**: Replaced simple type checks in length validation with a comprehensive `get_content_length` parser that extracts sizes from `ToolMessage`, `BaseMessage`, list, and dict types, fixing premature connection cancellations and response truncations on large log retrievals.
* **Backend Server Modularization**:
  * **Clean Architecture**: Split the main `backend/app.py` file to move heavy streaming handlers and bypass workflows to a dedicated `backend/core/chat.py` module, guardrail helpers to `backend/core/guardrails.py`, and automatic database ingestion to `backend/core/ingest.py`.
  * **Lightweight Files**: Brought the main server code length down by 55% to just 206 lines, satisfying the project's under-450-line modularity rule (`.agents/rules/logic-constraints.md`).

---

## 🚀 Phase 10: Semantic Caching for Cost Optimization

Phase 10 implements **Semantic Caching** to bypass LLM execution for previously answered queries, reducing input and output token costs to **0** on repeating or semantically similar user intents:

* **Configurable Semantic Similarity**: Utilizes a configurable similarity threshold `SEMANTIC_CACHE_THRESHOLD` (defaulting to `0.92` Cosine Similarity) to match queries against the cache.
* **Dedicated Local Vector Cache**: Configures a dedicated local Chroma collection (`semantic_cache`) using Cosine distance space (`hnsw:space = cosine`) to evaluate queries with precision.
* **Exclusion Guardrails**: Excludes empty queries, exact problem-log requests (handled by the Programmatic Bypass), and short general phrases (e.g., "hi", "ok", "yes") from entering or hitting the cache.
* **Stream & Ingestion Integration**: Automatically intercepts incoming queries in the streaming pipeline (`generate_chat_responses` and `resume_graph_stream`), serving cache hits instantly, or caching new LLM responses upon completion.
* **Verification Suite**: Includes the integration test script `backend/scratch/test_semantic_cache.py` to evaluate cache hit/miss behavior, threshold bounds, and exclusion guardrails.

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
│   ├── app.py             # FastAPI Entry & Lifecycle (Streamlined to ~200 lines)
│   ├── basics.ipynb       # RAG experimentation & embedding logic
│   ├── chroma_db/         # Local vector database storage
│   ├── core/              
│   │   ├── agents.py      # LangGraph node logic & system rules
│   │   ├── chat.py        # Core agent execution & streaming handlers
│   │   ├── config.py      # VectorStore & Supabase PostgresSaver setup
│   │   ├── guardrails.py  # Runtime input/output guardrail checks
│   │   ├── ingest.py      # RAG auto-ingestion & schema setup
│   │   └── tools/         # Modular Librarian Triage & Search sub-package
│   │       ├── __init__.py
│   │       ├── problem_index.py
│   │       ├── search.py
│   │       ├── stats.py
│   │       └── system.py
│   ├── evals/             
│   │   ├── eval.py        # Automated LLM-as-a-Judge evaluation
│   │   └── qa_dataset.json # Phase 8.0 Golden Dataset (30 cases)
│   ├── memory.py          # Persistence logic
│   ├── scratch/           # Experimental & testing scripts
│   │   └── test_semantic_cache.py # Semantic cache integration test
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
```

---

## 🚦 Developer Commands & Evaluation Workflow

### Running the Evaluation Suite
You can customize the model used for testing by setting the `MODEL_NAME` environment variable. By default, it uses `deepseek/deepseek-chat`.

**1. Iterating on a Cheap Model (Gemini 2.0 Flash):**
```bash
MODEL_NAME="google/gemini-2.0-flash-001" uv run python -m backend.evals.eval
```

**2. Final Production "Golden Run" (DeepSeek V3):**
```bash
MODEL_NAME="deepseek/deepseek-chat" uv run python -m backend.evals.eval
```

### Running the Semantic Cache Integration Test
Verify the hit, miss, and exclusion behavior of the semantic cache locally:
```bash
uv run python -m backend.scratch.test_semantic_cache
```


### Running the Application Locally
You can run the full system using Docker Compose:
```bash
docker-compose up --build
```
Or start the backend locally:
```bash
cd backend
uv run uvicorn app:app --reload --port 8000
```