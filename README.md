
---
title: Unified Knowledge Agent (Nexteir Second Brain)
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: true
---

# 🧠 Unified Knowledge Agent: Nexteir Second Brain

**The Mission:** To transform 600+ fragmented technical internship logs into a deterministic, production-grade Agentic Intelligence layer. This system moves beyond "vibe-based" RAG by implementing strict logic guardrails, Human-in-the-Loop (HITL) safety, and automated evaluation pipelines.

**Current Status:** Phase 7.0 - Production-Ready (Safe-to-Fail Orchestration)

---

## 👁️ System Demo & UX

![Agent Demo](./assets/demo.gif)

### The "Yellow Card" Protocol (HITL)
The agent utilizes `on_agent_interrupt` to pause before executing heavy tools, requiring explicit human approval via the UI before accessing the deep knowledge layer.

<div align="center">
  <img src="./assets/ss1.png" alt="Interface Snapshot 1" width="48%">
  <img src="./assets/ss2.png" alt="Interface Snapshot 2" width="48%">
</div>

---

## 🚀 Phase 7.0: The Reliability Layer

Unlike standard RAG, Phase 7 focus on **Control, Evaluation, and Synthesis**:

* **Human-in-the-Loop (HITL) Trigger:** Implemented a state-persistent "Yellow Card" approval system. The agent pauses execution for high-token or critical tool calls, demonstrating a "Safety-First" autonomous workflow.
* **The "Golden Dataset" Eval Suite:** A deterministic evaluation pipeline (`evals/eval.py`) that tests the agent against 20+ "Hard" technical queries. **Current Success Rate: 100%** for technical bug extraction and 95% for intent triage.
* **Intent-Aware Triage (Librarian Mode):** For vague queries (e.g., "the screen"), the agent acts as a **Librarian**, providing a bulleted menu of matches rather than a "code dump." This ensures 100% precision and token efficiency.
* **Automated Post-Mortem Generation:** A specialized mode where the agent synthesizes a chat session into a structured technical report (Root Cause, Fix, Lessons Learned) for documentation.

---

## 🛠️ The Technical Stack

| Layer | Technology | Key Function |
| :--- | :--- | :--- |
| **Orchestration** | **LangGraph** | Stateful state machine with HITL interrupts & persistence |
| **Cloud State** | **Supabase (PostgreSQL)** | State survives `docker prune`; enables multi-device sync |
| **Logic Layer** | **Python (FastAPI)** | Hardened "Raw Interceptors" & Regex Anchors |
| **Observability** | **LangSmith** | Real-time X-ray of tool-routing, latency, and cost |
| **Data Ingestion** | **Pandoc** | Media-extraction scrubbing (Scrubbed 100k+ char Base64 noise) |
| **Frontend** | **Next.js 14** | Responsive UI with HITL "Action Required" status |

---

## 📂 Project Structure

```text
Unified-Knowledge-Agent/
├── backend/          
│   ├── app.py             # FastAPI Entry (Async DB Pool & Lifecycle)
│   ├── core/              # The Agentic Brain
│   │   ├── agents.py      # System Prompt Rules & LangGraph Node Logic
│   │   ├── config.py      # VectorStore & Supabase PostgresSaver setup
│   │   └── tools.py       # Librarian Triage & Raw Extraction tools
│   ├── evals/             # The "Truth" Layer
│   │   ├── eval.py        # Automated LLM-as-a-Judge grading
│   │   └── qa_dataset.json # The Golden Dataset
│   └── memory.py          # Supabase-backed persistence logic
├── frontend/         
│   ├── src/               
│   │   ├── components/    # HITL-aware UI components
│   │   └── hooks/         # useChatStream for HITL approval handling
├── data/                  
│   ├── media_dump/        # Extracted media from Pandoc (Scrubbed from .md)
│   ├── NEXTIER_Internship_Bugs.docx # Raw Source
│   └── NEXTIER_Internship_Bugs.md   # Standardized Markdown with # Anchors
├── docker-compose.yml     # Multi-container orchestration
└── generate_dataset.py    # Script to build the Golden Dataset from logs
```

---

## 🛡️ Architectural Guardrails (The "Frozen" Logic)

To achieve 100% fidelity, we "froze" the following deterministic patterns:

1.  **The Indexer Ban:** The agent is strictly forbidden from using the indexer for keyword searches, forcing deep semantic retrieval to prevent hallucinations.
2.  **The "Hard Token Ceiling":** Python-enforced pagination (Max 25 items) that overrides LLM "People-Pleaser" behavior, protecting the API budget.
3.  **The Metadata Firewall:** Prevents "General Workflow" chunks from triggering the "Blind Copy-Paste" extractor mode.
4.  **The Ordinal Interceptor:** Hardcoded Python math to handle "first/last" queries, bypassing LLM reasoning errors.

---

## ⚡ Deployment & Workflow

### 1. The "Clean Slate" Sync
Whenever new logs are added to the `.docx` source:
```bash
# 1. Extract Media & Convert
pandoc data/NEXTIER_Internship_Bugs.docx -t markdown --extract-media=data/media_dump -o data/NEXTIER_Internship_Bugs.md

# 2. Reset Memory (Nuke & Hydrate)
rm -rf backend/chroma_db backend/docstore
uv run python -m backend.app
```

### 2. Multi-Cloud Sync
* **Frontend:** Deployed on **Vercel** for global CDN delivery.
* **Backend:** Deployed on **Hugging Face Spaces** (Docker) for dedicated RAG compute.
* **Database:** **Supabase** handles the persistent LangGraph state machine.
```

---

