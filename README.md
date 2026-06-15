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

**Current Status:** Production-Ready & Evaluated (100% Search Recall & Agent Logic Scores)

---

## 👁️ System Demo & UX

![Agent Demo](./assets/demo.gif)

### The "Yellow Card" Protocol (HITL)
The agent utilizes `on_agent_interrupt` to pause before executing heavy tools, requiring explicit human approval via the UI. The Phase 8 update ensures a seamless handshake between the LangGraph state and the Next.js frontend.

<div align="center">
  <img src="./assets/ss1.png" alt="Interface Snapshot 1" width="48%">
  <img src="./assets/ss2.png" alt="Interface Snapshot 2" width="48%">
</div>

<div align="center" style="margin-top: 10px;">
  <img src="./assets/ss3.png" alt="Interface Snapshot 3" width="48%">
  <img src="./assets/ss4.png" alt="Interface Snapshot 4" width="48%">
</div>

---

## 🚀 Key Features & Capabilities

This system is built for deterministic reliability, performance optimization, and rigorous security:

### 1. High-Performance Retrieval Engine (100% Recall)
* **Metadata Header Preservation:** Pre-splits markdown documents and prepends header contexts (e.g. `# Problem ID`) back to the chunk `page_content` prior to ingestion. This resolves ChromaDB's native metadata-stripping blind spot.
* **Corpus Growth Stress-Testing:** Includes a validation suite (`eval_corpus_growth.py`) that slices the document base to evaluate recall stability against growing datasets, verifying retrieval resilience.
* **Optimized Search Width:** Configured with optimized $k=40$ child document retrieval bounds feeding the reranker for maximum coverage.

### 2. Unified LLM Architecture & Cost Control
* **Unified Model Driver (Gemini 2.5 Flash):** Uses `google/gemini-2.5-flash` as the primary, fallback, and triage classifier model. This provides strict tool-calling hygiene (preventing pre-execution text leakage that breaks the HITL UI), ultra-low latency, and maximum token efficiency.
* **High-Speed Input Classifier:** Triage routing runs on a non-streaming, fast setup of Gemini 2.5 Flash to direct out-of-scope queries instantly, saving tokens and reducing overall latency.
* **Zero-Token Programmatic Bypass:** Intercepts direct log-retrieval queries (e.g., "Problem 12") at the API and Graph levels, fetching raw logs directly from the source files and bypassing LLM inference entirely.
* **Semantic Caching:** Employs a dedicated local Chroma collection (`semantic_cache`) using Cosine similarity to intercept repeating queries, serving cached hits instantly and bypassing LLM calls.
* **Prompt Compression:** Features a compressed system prompt (~50% smaller) and a tuned "Context Diet" limiting `parent_splitter` chunks to 1,000 characters to prevent input token leakage.

### 3. Production Security & Guardrails
* **Fast Input Firewall:** An instant API gateway guardrail enforcing a **1,000-character input ceiling** and blocking jailbreaks, system prompt exposure attempts, and credential leaks.
* **Data Loss Prevention (DLP) Masking:** A sliding 120-character regex buffer window that automatically redacts API keys and database secrets before they stream to the client interface.
* **Dynamic Response Capping:** Prevents response truncations by scaling content length restrictions dynamically: $\text{Max Allowed Chars} = \max(2000, \text{Last Tool Output Length} + 1500)$.

### 4. Robust Automated Testing
* **LLM-as-a-Judge Evaluation Suite:** Automatically grades generated answers against a 30+ case Golden Dataset (`qa_dataset.json`) assessing correctness and alignment.
* **Resilient Parsing Retries:** Features automatic retry loops with backoff delays to safeguard against transient OpenRouter/LLM JSON parsing errors.

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
│   │   ├── eval.py        # Automated LLM-as-a-Judge evaluation (with retry support)
│   │   ├── eval_corpus_growth.py # Recall vs. Corpus Growth evaluation tool
│   │   └── qa_dataset.json # Golden Dataset (30+ cases)
│   ├── memory.py          # Persistence logic
│   ├── scratch/           # Experimental & testing scripts
│   │   └── test_semantic_cache.py # Semantic cache integration test
│   └── static/            # Static assets for the backend
├── data/                  
│   ├── NEXTIER_Internship_Bugs.md   # Standardized source of truth
│   └── media_dump/        # Parsed document assets and diagrams
├── frontend/         
│   ├── src/               
│   │   ├── app/           # Next.js App Router (layout/page)
│   │   ├── components/    # Chat UI (ChatHeader, ChatInput, MessageList, Sidebar, CodeBlock)
│   │   ├── hooks/         # useChatStream for HITL approval flow
│   │   └── types/         # TypeScript definitions for agents
│   ├── next.config.ts     # Frontend configuration
│   └── frontend.Dockerfile # Containerization for Next.js
├── docker-compose.yml     # Multi-container orchestration (Backend + Frontend)
├── Dockerfile             # Backend containerization
├── generate_dataset.py    # Synthetic dataset generation script
├── pyproject.toml         # Python dependencies (uv)
├── scratch/               # Experimental root-level tests (test_agent.py, test_guardrails.py, test_params.py)
├── test_conn.py           # Database connectivity test script
└── uv.lock                # Deterministic lockfile
```

---

## 🚦 Developer Commands & Evaluation Workflow

### Running the Evaluation Suite
By default, the evaluation suite now runs on the primary model, `google/gemini-2.5-flash`.

**1. Running the Standard Evaluation (Gemini 2.5 Flash):**
```bash
uv run python -m backend.evals.eval
```

**2. Running with alternative models (e.g., DeepSeek V3):**
> [!WARNING]
> While DeepSeek V3 can be evaluated by setting `MODEL_NAME`, it exhibits pre-execution hallucinations during tool calls that break the frontend's HITL approval panel.
```bash
MODEL_NAME="deepseek/deepseek-chat" uv run python -m backend.evals.eval
```

### Running the Corpus Growth Evaluation Stress-Test
Verify retrieval recall against expanding database sizes:
```bash
MODEL_NAME="google/gemini-2.5-flash" uv run python -m backend.evals.eval_corpus_growth
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