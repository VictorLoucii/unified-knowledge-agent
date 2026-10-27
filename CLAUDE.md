# Unified Knowledge Agent

A RAG agent over a personal knowledge base of markdown files in `data/`.
FastAPI + LangGraph backend, Next.js frontend, ChromaDB for vectors, OpenRouter
for model calls, Arize Phoenix for tracing. The repo is public; a push to `main`
mirrors to a HuggingFace Space (`.github/workflows/sync_to_hub.yml`).

## Map

| Path | What it holds |
|---|---|
| `backend/app.py` | FastAPI app, `/health`, background ingestion at startup |
| `backend/core/agents.py` | LangGraph graph, system prompt, `fast_path_node` |
| `backend/core/semantic_router.py`, `fast_path_routes.py` | Fast-path table: 53 stored answers, matched by substring |
| `backend/core/ingest.py` | Chunking and ingestion into `backend/chroma_db`, `backend/docstore` |
| `backend/core/tools/search.py` | Query expansion, retrieval, reranking |
| `backend/core/config.py` | Models, tracing setup, environment loading |
| `backend/evals/` | Eval suite (`eval.py`), dataset (`qa_dataset.json`), committed scores |
| `frontend/` | Next.js app; its own rules in `frontend/CLAUDE.md` |
| `data/` | The knowledge base. Source of truth. Git LFS |

## Commands

| Task | Command | Who runs it |
|---|---|---|
| Install | `uv sync`; `cd frontend && npm ci` | owner |
| Backend | `uv run uvicorn backend.app:app --reload --port 7860` | owner |
| Frontend | `cd frontend && npm run dev` | owner |
| Lint | `cd frontend && npm run lint` | Claude |
| Types | `cd frontend && npx tsc --noEmit` | Claude |
| Python syntax | `.venv/bin/python -m compileall -q backend` | Claude |
| Fast-path drift | `.venv/bin/python -m backend.evals.check_fast_path` | owner |
| Eval | `uv run python -m backend.evals.eval --concurrency 1` | owner |

- `--port 7860` is required. The frontend's three call sites fall back to
  `localhost:7860`, and `Dockerfile:33` binds 7860.
- Inside the sandbox, `uv` cannot write its cache and Python cannot read `.env`.
  So Claude uses `.venv/bin/python` and hands the owner any command that loads
  `backend/core/config.py`. The owner runs such a command with `!`, which runs
  outside the sandbox.
- `docker compose up --build` has never been run end to end (`OPEN.md` item 6).

Current check results: `.claude/check-baseline.md`.

## Working rules

- **`data/` is not edited.** The one exception is a correction the owner
  approves per file. Rules: `.claude/rules/knowledge-base.md`.
- **Changes to the prompt, router, tools or retrieval are eval-driven.** Never
  set `MODEL_NAME`. Rules: `.claude/rules/evals.md`.
- State assumptions. When a request reads two ways, ask. Reason only from files
  you have read; when the files cannot confirm something, say so.
- Touch only what the request needs. Do not change application logic unless
  asked. Keep existing comments, docstrings and unrelated functions. Mention
  dead code; do not remove it. Do not refactor unrelated code.
- Name the file and line of every change you propose or make.
- Grep every reference before renaming or deleting a function, hook, column or
  variable.
- Check `pyproject.toml`, `uv.lock` and `frontend/package.json` before writing a
  utility. Ask before adding a dependency.
- Never leave a catch or `except` block empty. Log the error or return a
  descriptive message.
- Done means the Claude-run checks above were run, no count is above
  `.claude/check-baseline.md`, and the owner has the eval command when the eval
  rules apply. Report the results.
- Keep every check current. When code changes what a check guards, update the
  check in the same change. Never loosen a check to make it pass.
- Stage named files only. Show `git diff --staged` before any commit.
- A record's evidence must sit at the same level as its claim. Before writing a
  mechanism into a record, name what you would measure to be wrong, and measure
  it; otherwise label it a hypothesis.
- A commit that changes a file's line count breaks `file:line` citations in
  `CLAUDE.md`, `DECISIONS.md`, `OPEN.md`, `README.md` and every other tracked
  file outside `data/`. Run `/citation-sweep`.
  A filename grep is not enough, for two reasons. Some citations are bare
  (`| :102 |`, `at :210`): on 2026-08-21, 12 bare refs into `app.py` against 44
  the grep found. And a range must be checked at both ends: that day the
  `/health` range in `OPEN.md` moved its end by one, and one of two sessions
  filed it safe. `247dd15` replaced a 10-line `app.py` block with a 17-line
  comment; eight citations across two records broke by exactly 7, found by
  accident weeks later.
  Leave past-tense citations to deleted code alone.

## Secrets

Variable names live in `.env.example`; read that. It names OpenRouter, OpenAI,
LangChain and WAQI keys and a database URL. `.claude/settings.json`
denies it to Claude's tools and, through the sandbox, to shell commands. Never
hardcode a key; code reads keys from the environment.

## Gotchas

- **Any push restarts the Space**, which re-ingests every `data/` file. On
  2026-08-21 it answered from a partly loaded index for 7 m 57 s while `/health`
  reported ready (`OPEN.md` item 4). Pushes are the owner's call.
- **Never run `git filter-repo` in this repo.** With `--force` it ends in
  `git reset --hard` and can destroy uncommitted `data/` notes. Clone with
  `GIT_LFS_SKIP_SMUDGE=1` to a scratch directory and work there. A deny rule
  blocks it here.
- `.langchain.db` (~100 MB, gitignored) caches every eval model call. A fresh
  clone starts cold. See `DECISIONS.md` for why it stays out of Git.
- Shell traps on this Mac (`grep` shadowed, zsh globs, `===`):
  `~/.claude/playbooks/tool-traps-mac.md`.

## Records and skills

- `DECISIONS.md`: why things are the way they are. `OPEN.md`: open problems, by
  item number. Read the named section, not the whole file.
- `.claude/advisor-executor-hitl.md`: the two-session relay
  (`/relay-advisor`, `/relay-executor`).
- `/citation-sweep` re-checks citations; `/close-out` reconciles the records
  before the context is cleared.
