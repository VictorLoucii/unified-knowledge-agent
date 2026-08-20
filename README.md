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

**The Mission:** To transform a growing directory of 20+ multi-disciplinary knowledge bases (including technical internship logs, Python guidelines, Agentic AI concepts, and more) into a deterministic, production-grade Agentic Intelligence layer. This system moves beyond "vibe-based" RAG by implementing strict logic guardrails, Human-in-the-loop (HITL) safety, and automated evaluation pipelines.

**Current Status:** Evaluated — 100% Search Recall@k (34/34) and 95.7% AI Logic Score (90/94) on a 94-case golden dataset. Of those, 53 cases are served by a deterministic fast-path lookup and 41 exercise the full RAG pipeline; measured on its own, that pipeline scores 8/8 on recall and 38/41 on AI Logic. The recall regression introduced by the 2026-08-17 index rebuild was fixed on 2026-08-20 — see [OPEN.md](OPEN.md) item 1.

---

## 👁️ System Demo & UX

![Agent Demo](./assets/demo.gif)

### The "Yellow Card" Protocol (HITL)
The agent utilizes `on_agent_interrupt` to pause before executing heavy tools, requiring explicit human approval via the UI. The Phase 8 update ensures a seamless handshake between the LangGraph state and the Next.js frontend.

### LLM-Powered Voice Autocorrect
The frontend features a Web Speech API integration that passes raw voice transcripts through a lightweight `/refine_transcript` FastAPI endpoint. This corrects technical jargon spelling (e.g., "seementally" -> "semantically") and intelligently appends punctuation without altering user intent, ensuring accurate inputs for downstream semantic routing.

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

### 1. Automated Data Ingestion Pipeline
* **Drop-in Multi-File Support:** Simply drop `.md` or `.docx` files directly into the `data/` directory. The ingestion pipeline (`backend/core/ingest.py`) will automatically discover and process them upon startup.
* **Auto-Conversion & Destructive `.docx` Handling:** Any `.docx` files are automatically converted into `.md` format via Pandoc, scrubbed of formatting artifacts, and then **permanently deleted**. Do not expect to find original `.docx` files after a successful ingestion.
* **Manifest Tracking:** Successfully ingested documents are tracked in `.manifest.json` to prevent duplicate processing.
* **Continuous Content Refinement:** Existing `.md` files are regularly updated with targeted keywords and contextual enhancements to continuously improve retrieval accuracy and AI Logic synthesis.

### 2. High-Performance Retrieval Engine
* **Robust Header-Injection Chunking:** Preserves Markdown structure by dynamically prepending parent header contexts (e.g. `## Project Tech Stack`) to **every individual chunk** *after* recursive text splitting. This resolves ChromaDB's native metadata-stripping blind spot and eliminates orphaned context.
* **Corpus Growth Stress-Testing:** Includes a validation suite (`eval_corpus_growth.py`) that slices the document base to evaluate recall stability against growing datasets, verifying retrieval resilience.
* **Optimized Search Width:** The retriever is configured with $k=40$ child documents per query. `search.py` then merges the results of every expanded query, truncates the combined candidate pool to 50, and reranks that pool down to the 10 documents passed to the model.

### 3. Unified LLM Architecture & Cost Control
* **Unified Model Driver (Gemini 2.5 Flash):** Uses `google/gemini-2.5-flash` as the primary, fallback, and triage classifier model. This provides strict tool-calling hygiene (preventing pre-execution text leakage that breaks the HITL UI), ultra-low latency, and maximum token efficiency.
* **High-Speed Input Classifier:** Triage routing runs on a non-streaming, fast setup of Gemini 2.5 Flash to direct out-of-scope queries instantly, saving tokens and reducing overall latency.
* **Zero-Token Programmatic Bypass:** Intercepts direct log-retrieval queries (e.g., "Problem 12") at the API and Graph levels, fetching raw logs directly from the source files and bypassing LLM inference entirely.
* **Direct Query Bypass for Search Expansion:** Intercepts searches referencing specific problem IDs to bypass the query expansion LLM entirely, conserving OpenRouter API credits.
* **Semantic Caching:** Employs a dedicated local Chroma collection (`semantic_cache`) using Cosine similarity to intercept repeating queries, serving cached hits instantly and bypassing LLM calls.
* **Prompt Compression:** Features a compressed system prompt (~50% smaller) and a tuned "Context Diet" limiting `parent_splitter` chunks to 1,000 characters to prevent input token leakage.
* **Asynchronous & Lazy-Loaded Optimizations:** Executes search tool expansion tasks asynchronously (`ainvoke`) to avoid blocking the event loop, and lazy-loads the 80MB `CrossEncoder` model only when vector search is requested to improve application startup latency.
* **Hyper-Local Weather & AQI Integration (HITL Protected):** Seamlessly answers dynamic environmental queries using Open-Meteo's APIs. Features a custom-built algorithm to calculate the **Indian National AQI (CPCB)** from raw pollutant data, entirely protected by LangGraph's Human-in-the-Loop pause/resume functionality to prevent unwarranted API requests.

### 4. Production Security & Guardrails
* **Zero-Cost Trace Observability (Arize Phoenix):** Integrated Arize Phoenix as a locally-run collector, completely replacing LangChain/LangSmith to provide powerful local tracing and debugging without external API dependencies or costs. Instrumentation lives in one place, `backend/core/config.py`, and uses a batching span processor so a missing collector costs nothing on the request path. Phoenix is started by hand — `docker-compose.yml` does not define a Phoenix service.
* **General Knowledge Fallback with Strict Disclaimers:** Enforces strict RAG adherence but allows a clean fallback to general LLM knowledge for basic, out-of-scope conversational queries. When doing so, it prepends a prominent disclaimer to prevent users from mistaking generalized advice for internal company policy.
* **Fast Input Firewall:** An instant API gateway guardrail enforcing a **1,000-character input ceiling** and blocking jailbreaks, system prompt exposure attempts, and credential leaks.
* **Data Loss Prevention (DLP) Masking:** A sliding 120-character regex buffer window that automatically redacts API keys and database secrets before they stream to the client interface.
* **Dynamic Response Capping:** Prevents response truncations by scaling content length restrictions dynamically: $\text{Max Allowed Chars} = \max(2000, \text{Last Tool Output Length} + 1500)$.

### 5. Robust Automated Testing
* **LLM-as-a-Judge Evaluation Suite:** Automatically grades generated answers against an 80+ case Golden Dataset (`qa_dataset.json`) assessing correctness and alignment.
* **Resilient Parsing Retries:** Features automatic retry loops with backoff delays to safeguard against transient OpenRouter/LLM JSON parsing errors.

---

## 🛠️ The Technical Stack

| Layer | Technology | Key Function |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Stateful state machine with HITL interrupts & persistence |
| **Cloud State** | **Supabase (PostgreSQL)** | State survives container prunes; enables multi-device sync |
| **Logic Layer** | **Python (FastAPI)** | Hardened "Raw Interceptors" & Regex Anchors |
| **Observability** | **Arize Phoenix (local collector)** | Zero-cost, local real-time X-ray of trace observability (replaced LangChain/LangSmith) |
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
│   │   ├── ingest.py      # RAG auto-ingestion & robust markdown chunking
│   │   ├── semantic_router.py # Semantic query classifier (Fast Path & Triage)
│   │   └── tools/         # Modular Librarian Triage & Search sub-package
│   │       ├── __init__.py
│   │       ├── problem_index.py
│   │       ├── search.py
│   │       ├── stats.py
│   │       └── system.py
│   ├── evals/             
│   │   ├── eval.py        # Automated LLM-as-a-Judge evaluation (with retry support)
│   │   ├── eval_corpus_growth.py # Recall vs. Corpus Growth evaluation tool
│   │   ├── generate_eval_dataset.py # Auto-generates test cases from markdown files via OpenRouter
│   │   └── qa_dataset.json # Golden Dataset (80+ cases)
│   ├── memory.py          # Persistence logic
│   ├── scratch/           # Experimental & testing scripts
│   │   └── test_semantic_cache.py # Semantic cache integration test (gitignored, not in a clone)
│   └── static/            # Static assets for the backend
├── data/                  
│   ├── *.md / *.docx      # Dynamic multi-file knowledge bases ingested on startup
│   ├── .manifest.json     # Tracks ingested files. Gitignored on purpose, so the
│   │                      # deployed Space arrives without one and re-ingests.
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
├── phoenix_trace_log.txt  # Generated local tracing log for Arize Phoenix
├── scratch/               # Experimental root-level tests (test_agent.py, test_guardrails.py, test_params.py)
├── test_conn.py           # Database connectivity test script
└── uv.lock                # Deterministic lockfile
```

---

## 🚦 Developer Commands & Evaluation Workflow

### Running the Evaluation Suite

Two different models are involved, and they have different defaults. The **agent
under test** is `google/gemini-2.5-flash` (`backend/core/config.py`). The
**LLM judge that scores the answers** is `deepseek/deepseek-chat`
(`backend/evals/eval.py`). Run the bare command and you get that pairing:

```bash
uv run python -m backend.evals.eval
```

> [!WARNING]
> **Do not set `MODEL_NAME`.** It is read in three places — the agent, the
> query-expansion model, and the LLM judge — so setting it silently reassigns
> the judge as well as the agent. That invalidates every cached judgment and
> makes the run far more expensive. It is also why a model change belongs in the
> source defaults rather than the environment.

Targeted runs are much cheaper while iterating. Note that **any** run, including
a partial one, overwrites `backend/evals/latest_run_metrics.json`, so back that
file up first:

```bash
uv run python -m backend.evals.eval --indices 5,37,42,83
```

DeepSeek V3 remains usable for evaluation but not as the driver: it emits text
before it emits its tool call, which breaks the frontend's HITL approval panel.
See [DECISIONS.md](DECISIONS.md).

### Running the Corpus Growth Evaluation Stress-Test
Verify retrieval recall against expanding database sizes:
```bash
uv run python -m backend.evals.eval_corpus_growth
```

### Running the Semantic Cache Integration Test

Verifies the hit, miss, and exclusion behaviour of the semantic cache locally:
```bash
uv run python -m backend.scratch.test_semantic_cache
```

> [!NOTE]
> `backend/scratch/` is gitignored, so this script is **not** part of a fresh
> clone. The command works only in a working copy that already has it.

### Running the Application Locally

Start the backend from the **repository root** — `backend/app.py` uses absolute
`backend.*` imports, so running it from inside `backend/` fails with
`ModuleNotFoundError`:
```bash
uv run uvicorn backend.app:app --reload --port 7860
```

**Pass `--port 7860`.** Uvicorn defaults to 8000, and the frontend calls 7860 —
`src/app/page.tsx`, `src/components/ChatInput.tsx` and `src/hooks/useChatStream.ts`
all fall back to `http://localhost:7860`. On 7860 the two halves meet with no
configuration: you need no `.env.local` and no environment variable. 7860 is not
a free choice — Hugging Face Spaces serve on it, which is why `app_port: 7860`
sits at the top of this file and `Dockerfile:33` binds it.

Then start the frontend:
```bash
cd frontend && npm run dev
```

### Running the Application with Docker Compose

```bash
docker compose up --build
```

> [!IMPORTANT]
> **Compose uses a different host port from the local command above, and that is
> deliberate — do not "fix" it.** Locally the backend is on
> **`http://localhost:7860`**. Under Compose it is on
> **`http://localhost:8000`**, because `docker-compose.yml:31` maps host `8000`
> to container `7860`. The container side must stay 7860; only the host side
> differs, so the two can run at once without colliding.

The frontend's API URL is baked into its browser bundle at build time, so
`docker-compose.yml:62` passes it as a **build argument**, not an environment
variable. Changing it requires `docker compose build frontend`, not a restart.

> [!NOTE]
> **Compose is fixed in source but has never been run end to end.** All three
> known defects — the published port, two dead volume mounts, and the frozen API
> URL — are corrected, and the freezing was confirmed by building the frontend
> and searching the bundle. Nobody has yet executed `docker compose up --build`
> to confirm the whole stack comes up. See [OPEN.md](OPEN.md) item 6.