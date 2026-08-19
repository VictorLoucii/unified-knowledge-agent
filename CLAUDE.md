# Unified Knowledge Agent — working rules

A RAG agent over a personal knowledge base of markdown files. FastAPI +
LangGraph backend, Next.js frontend, ChromaDB for vectors, OpenRouter for
model calls. The `data/` directory is the single source of truth.

---

## Read this before you trust the evaluation score

**The fast-path table answers 53 of the 94 evaluation cases without calling
the retriever or the answering model.**

`backend/core/fast_path_routes.py` holds `FAST_PATH_INTERCEPTS`, a table of 53
question/answer pairs. `semantic_router.py` matches a key as a *substring* of
the user query. On a hit, `agents.py:fast_path_node` returns the stored string
as the answer and synthesises a `ToolMessage` carrying the stored problem id,
which is exactly what `eval.py` scrapes to compute Recall@k.

Measured consequence, as of the last full run:

| Metric | Headline | From the table | Genuinely exercised |
|---|---|---|---|
| AI Logic Score | 90/94 | 53 cases | **41 cases** |
| Recall@k | 33/34 | 26 cases | **7 of 8 cases** |

So the Recall@k headline rests on 8 vector retrievals, not 34. The table is a
legitimate O(1) cache in the product. It is not a measurement of the RAG
pipeline. **When you change retrieval, report the 41-case and 8-case figures
alongside the headline, or you will report a change that did not happen.**

The 8 genuinely-exercised recall cases are indices **6, 46, 77, 78, 79, 80, 81,
83**. `--indices` is 1-based (`eval.py:124` does `dataset[i-1]`). Index 83 is
the current miss; see [OPEN.md](OPEN.md) item 1.

Note also that the intercept keys match the eval's queries verbatim, so the
table helps the score far more than it helps a real user, who will phrase the
question differently and fall through to RAG.

---

## Eval-Driven Development

Adding or changing anything that touches the system prompt, the semantic
router, the tools, or the retrieval pipeline puts you under these rules.

**1. Run the suite before you call the work done.**

```bash
uv run python -m backend.evals.eval
```

Use the bare command. Do **not** set `MODEL_NAME`. It is read in three places —
`config.py` (the agent under test), `search.py` (the query-expansion model) and
`eval.py` (the LLM judge) — and setting it silently reassigns the judge, which
invalidates every cached judgment and makes the run far more expensive. The
defaults differ: `config.py:49` and `search.py:16` default to
`google/gemini-2.5-flash`, `eval.py:67` defaults to `deepseek/deepseek-chat`.

**This also means a model migration belongs in the hardcoded default strings in
source, never in `MODEL_NAME`.** Setting the variable would swap the judge along
with the agent. `google/gemini-2.5-flash` is now closed to new users — see
[OPEN.md](OPEN.md) item 8 before changing any model string.

Targeted runs are much cheaper while iterating:

```bash
uv run python -m backend.evals.eval --indices 5,37,42,83
```

**Warning: every run, including a partial `--indices` run, overwrites
`backend/evals/latest_run_metrics.json`.** Back that file up before a partial
run and restore it afterwards, or you will lose the committed baseline.

`--concurrency` caps how many cases run at once (`eval.py:112`, default 10;
the semaphore is at `eval.py:189`). It changes wall-clock time only, never a
score. Lower it if you suspect rate limiting — see "Judge noise is real"
below.

**2. Do not drop below the committed baseline.**

The floor is whatever `backend/evals/latest_run_metrics.json` holds at `HEAD`.
Do not merge, commit, or finalise a change that lowers either score below it.
If you regress, find the cause, fix or revert, and re-run until you are back at
or above the committed figures. The suite's own gate lives at `eval.py` —
read the threshold from the code, never restate a number in a rule or a skill.

**3. Be surgical with the system prompt.**

The directives in `backend/core/agents.py` that handle problem extraction,
rigid formatting and the zero-knowledge guardrail are load-bearing. Do not
remove or heavily rewrite them without a specific reason.

**4. Change the test when the behaviour should change.**

If a new feature legitimately changes how the agent should answer, update the
expected output and criteria in `backend/evals/qa_dataset.json`. Do not bend
the system prompt to satisfy a test that no longer describes what you want.

**5. Follow the EDD loop for any bug you find.**

1. Document the query, the wrong output and the desired output. Touch nothing.
2. Add the failing case to `qa_dataset.json`.
3. Run the suite and watch it fail. That is your baseline.
4. Fix the prompt or the retrieval logic.
5. Re-run. The new case passes, every old case still passes, and the scores are
   at or above the committed baseline.

### A fast run means a warm cache, not a working pipeline

`eval.py:31` installs a `SQLiteCache` at `.langchain.db`. That file is about
97 MB on disk and is gitignored (`.gitignore:28-29`), so a fresh clone starts
cold and a fully warm run makes no network calls at all. Runtime is therefore
not evidence about retrieval. Three separate things make a run fast and only
one of them is the pipeline: the fast-path table answers 53 cases with no
model call, the cache answers repeats with no network call, and
`--concurrency` overlaps whatever waiting is left. See
[DECISIONS.md](DECISIONS.md), "`.langchain.db` was stripped from the history,
not migrated to LFS", for why the file stays out of Git.

The cache keys on exact prompt text. Any edit to the system prompt, the
retrieval logic or a model string turns every hit into a miss. The next run is
then slow whether or not the change was correct. Do not read a slow run as a
regression, and do not read a fast one as a pass.

Recorded runtimes in this repo are not comparable to each other. The two logs
dated 2026-07-26 report 27.17 s and 230.68 s on the same runner, at the same
concurrency, with the same 155 reranked retrievals and a one-case difference
in the dataset. Only the 230.68 s log is at `HEAD`; `c982350` put it there.
The 27.17 s log is the 90-case run and is in history only — read it with
`git show f30ff63:full_evaluation_log.txt`. The slower one is the later one,
so a cache that only grows does not explain it. The cause is unconfirmed. The
one lead: the slow log's header records `Span Processor: SimpleSpanProcessor`,
which exports every span synchronously on the calling thread. The fast log
cannot be compared against it. That log begins at `🤖 Loading LLM model`,
which `config.py` prints after the tracing block, so its startup was never
captured and its tracing configuration is unknown. This pair is therefore not
a before/after for `batch=True`; do not cite it as one. Treat both numbers as
history and do not derive an expected runtime from them.

### Judge noise is real

The judge is an LLM. Cases have flipped verdict across runs on unchanged code —
index 42 alternated fail/pass/pass/fail. Before chasing a single-case
difference, check whether the agent's output actually changed. If the case is
served by the fast-path table and that table is unmodified, the output is
byte-identical and the difference is the judge.

Rate limiting also presents as a fail, not as an error. `eval.py:155-177`
retries a failed judge call five times, sleeping 2 s between attempts, then
falls back to `passed=False` with the reason recorded in the verdict. At the
default concurrency of 10 an OpenRouter limit therefore shows up as a slow run
with a few unexplained failures. Grep the output for `LLM Judge evaluation
failed` before you edit a prompt to chase one.

---

## `data/` is the source of truth — corrections need approval, per file

`data/` is the raw knowledge base. It is manually curated and is the single
source of truth.

**The default is still: do not modify, edit, or append to any `.md` or `.docx`
file inside `data/`.** Nothing here licenses a routine edit.

### The one exception: a proposed correction, approved per file

Since 2026-08-18 a `data/` file may be corrected, under these conditions, all of
which must hold:

1. **Propose first, write second.** Show the exact file, the exact lines, and
   the exact replacement text. Wait for approval. Approval covers **that one
   file**, and does not carry to the next file or the next session — the same
   shape as a push.
2. **Corrections only.** The permitted reason is that the note states something
   that is no longer true, such as documenting code that has since been deleted.
   Rewriting for style, brevity or tone is not a correction.
3. **The parser-hack ban is unchanged and absolute.** See the bullet below. An
   edit that exists to make the text easier to chunk, retrieve or parse is
   forbidden whether or not it is approved.
4. **Check `git status` on `data/` first.** The rule below about hand-written
   notes existing in no commit is real. If anything in `data/` is modified or
   untracked, commit it before editing, so every file has a recoverable version.

**Before proposing any `data/` edit, check the fast-path table.** 26 of the 53
entries in `backend/core/fast_path_routes.py` are verbatim copies of `data/`
problem blocks, and `agents.py:36-38` consults that table before any model call.
If a table key matches the query a reader would ask, editing `data/` changes
nothing the user sees — the fix is in the Python file instead. See
[OPEN.md](OPEN.md) item 5.

**An approved edit reaches the deployed Space by commit and push alone.** The
Space ships no manifest since `003496a`, so it re-ingests every file on each
container start. No manual rebuild is needed there. **The local index is a
different matter** — it never updates, and `eval.py` measures against it. See
[OPEN.md](OPEN.md) item 2.

### `data/` is Git LFS — `git diff` will not show you the change

`.gitattributes:8` is `data/*.md filter=lfs diff=lfs merge=lfs -text`. Two
things follow, and both have already caught a session out.

- **`git diff` on a `data/` file prints a three-line pointer, not the text.** A
  13-line correction reported "2 insertions, 2 deletions". Never read a `data/`
  diff that way. Smudge the committed side first:

  ```bash
  git cat-file -p HEAD:data/<file>.md | git lfs smudge > /tmp/before.md
  diff -u /tmp/before.md data/<file>.md
  ```

- **`.github/workflows/sync_to_hub.yml:16` sets
  `git config lfs.allowincompletepush true`** before force-pushing to
  HuggingFace. The mirror can therefore report success while shipping a pointer
  instead of the file. **After every `data/` push, confirm the bytes arrived**
  by fetching the Space's copy and grepping it for text you just added. Nothing
  in the workflow fails when the object is missing.

- **No parser hacks.** Do not inject formatting tags, HTML or structural
  markers into the source files to make them easier to parse. The data stays
  clean, natural and human-readable.
- **Fix the pipeline, not the data.** If retrieval misses a section, change
  `backend/core/ingest.py` (chunking), `backend/core/tools/search.py` (query
  expansion, reranking, score boosting) or the expansion prompt.
- **Cache files are the exception.** `data/.manifest.json` may be modified or
  deleted, and only when deliberately re-ingesting.
- **Do not commit `data/.manifest.json`.** It is gitignored on purpose since
  2026-08-18. Tracking it shipped a manifest naming all 26 files to the
  HuggingFace Space, which has no vector index of its own, so `initialize_rag`
  took the early return at `ingest.py:91-93` and the deployed product served an
  empty database in silence. The file must stay on your disk — local Docker
  builds still copy it — and out of every commit. See
  [DECISIONS.md](DECISIONS.md), "The Space ingests at startup".

### Ingestion is destructive and does not update

Two behaviours to know before you run ingestion:

- **Any `.docx` dropped into `data/` is converted to markdown and the original
  is permanently deleted** (`ingest.py`). Copy the original somewhere outside
  `data/` first.
- **Ingestion keys on filename only.** `ingest.py` compares basenames against
  `data/.manifest.json`. It ignores content, size and mtime, and there is no
  delete path anywhere in the backend. A file already in the manifest will
  never be re-read no matter how much you edit it, and clearing its manifest
  entry adds a second copy rather than replacing the first. `search.py`
  de-duplicates by exact `page_content`, so identical chunks collapse but
  *changed* ones do not — you get the stale and the fresh version competing.
  To pick up edited files, rebuild: rename `backend/chroma_db` and
  `backend/docstore` aside, empty the manifest, then run ingestion. Both
  directories are gitignored, so git holds no backup — rename, never delete.

---

## Core logic rules

- Do not change application logic unless asked.
- **Backward compatibility is the golden rule.** Changes to shared components
  or hooks use optional props and default values so existing callers keep
  working.
- Do not guess or assume missing information. Reason only from files you have
  actually read. If something cannot be confirmed from the code, say so.
- Follow the existing project structure and style. Do not refactor unrelated
  code.
- Say exactly which file and which line to change.
- **Do not add dependencies without asking.** Check `package.json`,
  `pyproject.toml` and `uv.lock` before writing a utility or adding a package.
- Grep for every reference to a function, hook, column or variable before
  renaming or deleting it.
- Never leave a catch block empty. Log the error or return a descriptive
  message.
- Keep components and screens under roughly 450 lines. Push presentation into
  sub-components and business logic into hooks.
- **Non-destructive editing.** Preserve existing comments, docstrings and
  unrelated functions. Do not delete logic unless told to.
- Check modified files compile or lint before calling the work done.
- **Git hygiene.** Never run `git add .`. Stage only the files that implement
  the requested change, and read the diff before committing.
- **A commit that changes a file's line count invalidates every citation to
  it.** `CLAUDE.md`, `DECISIONS.md`, `OPEN.md` and `README.md` cite source by
  `file:line`. After such a commit, grep all four for that filename and re-check
  each hit against the file. Commit `247dd15` replaced a 10-line block in
  `app.py` with a 17-line comment, and **eight citations across two records
  silently became wrong by exactly 7** — found by accident, weeks later. Leave
  citations that describe *deleted* code in the past tense alone; those are
  history and are correct as written.

## History rewrites

**Never run `git filter-repo` in this working repository.** Its clean-tree guard
calls `git ls-files -o` *without* `--exclude-standard`, so it counts gitignored
paths as untracked. Here that is over 126,000 entries, most of them inside
`.venv`, and no amount of gitignoring reduces it. The guard can never pass.

`--force` skips every guard and then ends with `git reset --hard`, because
`reset = not is_bare`. That discards every uncommitted change to a tracked file.
The repository has repeatedly held hand-written `data/` notes that exist in no
commit, so this is a live data-loss path, not a theoretical one.

Clone to a scratch directory and operate there. Use `GIT_LFS_SKIP_SMUDGE=1` so
the clone keeps LFS pointers instead of downloading every object. In a fresh
clone the guards pass on their own and `--force` is never needed.

`--dry-run` does not help: it disables commit-message rewriting outright, so it
cannot verify a `--message-callback`. Run the real pass in the throwaway clone
and inspect `git log` there before pushing anything.

## Secrets

Never hardcode API keys, passwords or credentials — read them from the
environment. Never open, read or request the real `.env`; use `.env.example`
to check variable names and schemas.

## Frontend rules

- Do not change styles, layout or design unless asked.
- All UI changes must work on mobile, tablet and desktop.
- **Golden rule of hooks.** Declare hooks at the top level of the component
  that consumes their values. Never declare a hook inside a child when the
  parent needs the data.
- This is Next.js, not React Native. `frontend/AGENTS.md` warns that this
  Next.js version has breaking changes against common knowledge — read the
  relevant guide under `node_modules/next/dist/docs/` before writing frontend
  code.

---

## Commands

```bash
# install
uv sync

# backend (also triggers ingestion of any file not in the manifest).
# --port 7860 is REQUIRED, not optional. Uvicorn defaults to 8000 and the three
# frontend call sites fall back to localhost:7860, so omitting it leaves the
# browser calling a port nothing serves. 7860 is what HuggingFace Spaces serve
# on and what Dockerfile:33 binds. Compose is the one exception — see below.
uv run uvicorn backend.app:app --reload --port 7860

# frontend
cd frontend && npm run dev

# full stack. Fixed in source, but NEVER RUN end to end — see OPEN.md item 6.
# docker-compose.yml:31 publishes 8000:7860; the container side must stay 7860
# because Dockerfile:33 binds it. The frontend's API URL is frozen into its
# browser bundle by next build, so docker-compose.yml:62 passes it as a BUILD
# ARG. Never move that to `environment:` — it would apply after the freeze and
# do nothing. Changing it needs `docker compose build frontend`, not a restart.
docker compose up --build

# evaluation — see the EDD section above before running
uv run python -m backend.evals.eval
```

Observability is Arize Phoenix. Note that `docker-compose.yml` defines no
Phoenix service — only `backend` and `frontend` — so Phoenix is started by
hand, not by compose. `config.py:31` defaults the collector to
`http://localhost:4317`, which `phoenix.otel` resolves to the gRPC exporter
(`phoenix/config.py:2828` sets `GRPC_PORT = 4317`).

If no collector is listening, tracing degrades quietly, because `config.py:40`
uses `register(batch=True)` so failed exports stay off the request path. Never
change that to `batch=False`.

**Instrument in exactly one place: `config.py:23-44`.** `app.py` once carried a
second setup with a `SimpleSpanProcessor`, and because it ran before the import
chain reached `config.py` it silently won, leaving the batch processor with no
spans. Measured against a closed port: 7.194 s per span on the caller's thread,
against roughly zero for the batch processor. `app.py:7-23` is now a comment
explaining why nothing may go back there. Do not add a second instrumentation.
