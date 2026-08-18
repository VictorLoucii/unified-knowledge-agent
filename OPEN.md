# Open work

Known, diagnosed, and deliberately not started. Each entry records what is
wrong, what has already been established, and what has *not* been checked, so
none of it has to be rediscovered.

Decisions already taken are in [DECISIONS.md](DECISIONS.md).

---

## 1. Index 83 — 'Community Type' no longer retrieves Problem 12

**Status:** diagnosed, cause known, not fixed. Costs one recall point.

This is the single miss behind the 33/34 recall recorded in
`latest_run_metrics.json`. It appeared with the 2026-08-17 index rebuild.

**Already established:**

- **It is not judge noise and not flaky.** With the cached query expansion
  dropped before each trial, target 12 was missed in 0 of 5 trials.
- The chain is: the agent calls the tool with a shortened query,
  `'Community Type metric'`; the expansion model turns that into
  `'Social network community measure'` and `'Graph community detection
  metric'`, which are the wrong domain; eight of the top ten hits then come
  from `AgenticAI_Interview_Questions_Theory.md`, the file that gained the most
  new text in the rebuild.
- **The content is present and reachable.** Called directly with the user's
  full question, the search tool returns Problem 12 at rank 1.
- **The mechanism is the order of two steps.** `search.py:379` truncates the
  merged candidate pool to 50. `search.py:399` reranks to 10. The truncation
  happens *before* the rerank, so a document the reranker would have scored
  highly can be discarded before it is ever scored.
- This is why indices 37 and 83 keep trading against each other. Both are RAG
  cases competing for slots in one truncated pool. The keyword-expansion change
  swapped them one way; the rebuild swapped them back.
- One earlier one-off run of the same short query *did* retrieve Problem 12, so
  the expansion output has changed at least once across a session. Stability
  over time is **not** established.

**Not tried:** any fix. Giving each expanded query a quota, or reranking before
truncating, would both address the mechanism. Both are application-logic changes
to `search.py` and need their own evaluation cycle.

---

## 2. The local index never updates, which silently ages the evaluation baseline

**Status:** not started. Reframed 2026-08-18 — this is a correctness problem for
measurement, not only a workflow convenience.

Ingestion keys on filename only, so an edited file is never re-read. The
2026-08-17 rebuild was the manual workaround.

### Why this is now a correctness problem

The deployed Space no longer has this defect. Since `003496a` it ships no
manifest and re-ingests all 26 files on every container start, so its index
always matches `data/`. **The staleness that survives is local — and local is
where measurement happens.** `eval.py` drives the compiled graph against the
local index, so an edited `data/` file leaves the committed baseline in
`latest_run_metrics.json` measured against content that no longer exists, with
nothing reporting it.

**The scope limit, which decides how much a fix buys.** **Taken from CLAUDE.md,
not source:** 53 of the 94 cases are answered by the fast-path table without
touching the retriever, and 26 of the 34 recall cases likewise. For those, the
stale copy lives in `backend/core/fast_path_routes.py` as hardcoded Python — see
item 5. **Content-hash tracking would report a difference and change nothing
about what those 53 cases return.** It addresses the 41 genuinely-exercised
cases only.

### Already established

- A hash alone is not enough. It detects the change but does not remove the old
  chunks. A working version needs the manifest to store
  `{basename: {sha256, doc_ids}}`, a delete path for both Chroma and the
  docstore, and `add_documents` called with explicit `ids=`.
- Clearing manifest entries without rebuilding is *not* safe — it appends a
  second copy rather than replacing the first. Measured on the pre-rebuild
  index: 8,404 distinct chunks were each stored 5 times, a few 10, 15 and 20
  times.

**Measured during the rebuild:** a full ingest of 26 files — 17,954 child
chunks, 8,909 parents — took **97 seconds** on a MacBook Air with the embedding
weights already on disk. Treat that as a floor, not a forecast. The deployed
Space pays this on every restart, in the background thread at `app.py:69`, so it
never blocks the port bind.

### Three options, none started

- **Detector only.** Hash each `data/` file at startup, compare against hashes
  stored in the manifest, print a warning naming any that differ. **Buys:** the
  silent failure becomes visible, which is the shape of all three defects fixed
  on 2026-08-18. **Costs:** purely additive — no delete path, nothing
  destructive, cannot lose data. The Space ignores it, having no manifest.
  **Recommended first.**
- **Hash change triggers a full rebuild.** **Buys:** one moving part that cannot
  half-succeed. **Costs:** ~97 s locally, and it must rename the index
  directories aside rather than delete them — **taken from CLAUDE.md:** both are
  gitignored, so git holds no backup.
- **Incremental update**, as described under "Already established" above.
  **Buys:** no full reprocessing. **Costs:** three parts that can each fail
  silently. The measured 5x duplication came from exactly this class of partial
  update, which is evidence against it in this codebase.

---

## 3. The `Problem Statement` regex reads sub-headings as problem ids

**Status:** diagnosed, latent, not fixed. Has not cost a test.

`search.py` extracts problem ids with

```
(?im)^[^a-zA-Z]*\b(problem|question)s?\b\s*(?::\s*|\s+)([A-Za-z0-9_]+)
```

at 10 sites. The leading `[^a-zA-Z]*` skips markdown decoration and then treats
the next word as the id, so `### **Problem Statement**` yields the id
`Statement`.

**Already established:**

- Across `data/` this manufactures **30 distinct fake ids over 57
  occurrences**: `Summary` ×12, `Description` ×9, `The` ×5, `str` ×2,
  `Statement` ×2, and others. (An earlier note said 37; that was an occurrence
  count taken before the 2026-08-17 content additions. Recounted 2026-08-18.)
- Fake ids leak into the `RETRIEVED_PROBLEM_IDS` marker — real logs show
  `['67', '12', 'Statement']`. Harmless for scoring, which only tests
  membership of the target, but the signal is dirty.
- **It truncates blocks.** A block runs from one match to the next, so a
  sub-heading inside a problem ends it early. Problem 12 is cut from 2,806
  characters to 123 — a 96% loss — through the search tool.
- **The scope is narrower than it first appears.** `config.py` uses a stricter
  regex that does not misfire, so the `Problem N` fast path returns the full
  block correctly. Only the search tool truncates. The user-visible symptom is
  that the same question can return a complete answer one way and a stub the
  other.

**Not tried:** any fix. Requiring the captured group to be numeric, or
requiring `problem` to be followed by a digit, would both work, but every one
of the 10 sites would need to change together and the change touches the recall
marker, so it needs its own evaluation cycle.

---

## 4. The deployed Space ran with an empty vector database — FIXED and VERIFIED

**Status: fixed and confirmed live 2026-08-18, commit `003496a`.** Kept here
only for the small residue below. The decision and the full mechanism are in
[DECISIONS.md](DECISIONS.md), "The Space ingests at startup".

`data/.manifest.json` is no longer tracked, so the Space's clone arrives without
one, `ingest.py:32` returns an empty manifest, and the container ingests all 26
files in the background thread at `app.py:69`.

**How it was confirmed, at zero OpenRouter cost.** `app.py:95-112` exposes
`/health`, which reports `rag_hydrated` by testing whether the docstore holds
any key (`app.py:103`). An empty docstore was the entire bug, so this flag was
`false` before.

1. `13:28:04` Space stage `RUNNING_BUILDING`.
2. `13:28:24` `RUNNING_APP_STARTING`.
3. `13:31:07` `RUNNING`. About three minutes end to end.
4. `13:31:46` through `13:37:09`, polled every 45 s: `{"status":"online",
   "rag_hydrated":true}` on all eight polls. The container did not die during
   ingestion.

The docstore cannot be populated by anything else. `backend/docstore` is
gitignored so it is not in the clone, and the Space reports `storage: None`, so
there is no persistent disk carrying one over. Only ingestion can have written
those keys.

**Two of the three unknowns are now answered.** The models *do* resolve inside
the Space — ingestion cannot embed without `all-MiniLM-L6-v2`, and the store is
populated. The startup penalty *does not* break anything — the app reported
`online` while ingestion ran, which is what `app.py:67-69` was built for.

### Residue, genuinely still open

- **The model download time is still unmeasured.** The Dockerfile has no
  pre-download step, so `all-MiniLM-L6-v2` and
  `cross-encoder/ms-marco-MiniLM-L-6-v2` are fetched at first use. That time is
  not inside the 97 seconds in item 2. The three-minute figure above covers
  build plus app start, not ingestion alone, so it does not isolate it either.
- **`rag_hydrated` proves "at least one document", not "all 26 files".**
  `app.py:103` calls `next(store.yield_keys(), None)`. Nothing exposes a count.
  Full coverage has not been demonstrated, only started and sustained.
- **No question has been put to the Space.** Doing so spends OpenRouter credit,
  so it was deliberately skipped. The remaining user-side check is the Space
  build log: look for `Vector Database missing 26 files` rather than
  `up to date`.

**One latent trap this route introduces.** If a `.docx` is ever added to
`data/`, the container will try to convert it with pandoc (`ingest.py:66`),
which is **not installed in the image**. `ingest.py:80-81` catches the error and
skips the file, so it degrades rather than crashes, but that document would
silently never be ingested in the Space. There are no `.docx` files in `data/`
today — checked 2026-08-18, count zero, none tracked.

**Also settled by this choice:** the LFS rules at `.gitattributes:4-6` for
`backend/chroma_db/**` stay permanently dead. `.gitignore:21` cancels them and
now always will. They are harmless; removing them is optional tidying.

---

## 5. Stale content: three paths carry `data/` to the user, and they age differently

**Status:** two stale documents found 2026-08-18; the propagation analysis added
after them. Nothing fixed.

### The two stale documents

- **`data/Unified_Knowledge_Project_Details.md`**, section
  `### C. Backend Instrumentation`. Precise anchors: the heading is at
  **:1342**, "Code snippet added at the top" at **:1348**, and the python fence
  opens at **:1350** and closes at **:1364**. The fenced block presents the
  deleted `app.py` code — `OTLPSpanExporter`, `SimpleSpanProcessor`,
  `http://localhost:6006/v1/traces` — as current. **Only the fence is stale.**
  The prose at :1344 and the surrounding reasoning about Arize Phoenix and
  running it in Docker to control cost are still accurate.
- **`CLAUDE.md`** claimed Phoenix is self-hosted via docker compose. Corrected
  2026-08-18. `docker-compose.yml` defines only `backend` and `frontend` plus a
  commented-out postgres — read, whole file.

### The three paths, and why this matters more than "a note is out of date"

Read from source:

| Path | Reads what | After a `data/` edit |
|---|---|---|
| `config.py:171-174` `extract_problem_block` | Opens the `.md` files **from disk at request time** | **Never stale.** No ingestion involved. |
| The vector index | Chroma and the docstore | Stale locally until a rebuild. **Fresh in the Space on every container start**, because since `003496a` there is no manifest and `ingest.py:32` returns an empty one. Observed twice on 2026-08-18 with identical chunk counts. |
| `fast_path_routes.py` `FAST_PATH_INTERCEPTS` | **Hardcoded Python strings** | **Permanently stale.** Nothing updates it, ever. |

**The permanently stale path wins.** `agents.py:36-38` calls `route_query`
first and returns `fast_path_node` on a hit, before any model call, and
`semantic_router.py:9` matches the key as a *substring* of the user's query.
**Taken from DECISIONS.md, not source:** that ordering is deliberate, recorded
under "The deterministic fast-path table runs before the classifying model", so
a probabilistic call cannot override a deterministic match.

**Measured 2026-08-18:** the table holds 53 entries. **26 carry a `target_id`
and are verbatim copies of `data/` problem blocks**, ending with the same
`<END OF PROBLEM>` marker that appears in the markdown. 27 are short answers
with `target_id: None`.

### Consequences to act on

1. **An edit to `data/` that is committed and pushed reaches the deployed
   Space with no manual rebuild.** That makes fixing the stale document far
   smaller than it first appears. Confidence HIGH — `ingest.py:32` read, plus
   two observed startups.
2. **But check the fast-path table first.** If a table key matches the query a
   reader would ask, the edit never surfaces, on any host, ever. Nothing in the
   ingestion pipeline can fix that; the fix is editing
   `backend/core/fast_path_routes.py`.
3. **A consistency check is cheap and nothing does it today.** For each of the
   26 entries with a `target_id`, compare the stored `output` against
   `extract_problem_block(target_id)`. That needs no hashing, no manifest and no
   ingestion, because `extract_problem_block` already reads the files live. Not
   started.

`data/` is currently clean — `git status --porcelain --untracked-files=all
data/` is empty, 39 files tracked, checked 2026-08-18. See item 2 for what this
does to the evaluation baseline.

---

## 6. `docker compose up` cannot reach the backend

**Status:** diagnosed from source 2026-08-18, not fixed, never observed
failing because nobody reported running it. Does not affect the deployed Space.

`CLAUDE.md` documents `docker compose up --build` as the full-stack command.

- `docker-compose.yml:29` publishes `"8000:8000"`.
- `Dockerfile:30` is `EXPOSE 7860` and `Dockerfile:33` binds `--port 7860`.

Nothing listens on container port 8000, so the published port reaches nothing.
`docker-compose.yml:49` then points the frontend at `http://localhost:8000`.

**Two dead volume mounts in the same file, lower stakes.**
`docker-compose.yml:35-36` mount `./chroma_db:/app/chroma_db` and
`./docstore:/app/docstore`. `config.py:84` sets `BASE_DIR` to the parent of
`core/`, so the real paths are `/app/backend/chroma_db` and
`/app/backend/docstore`. The host sources are wrong too — the repository has
`backend/chroma_db`, not `./chroma_db`. Local RAG still works, because
`COPY backend/ ./backend/` puts the index in the image, so these mounts are
dead rather than harmful. They do mean a local compose run persists nothing.

**Not tried:** any fix. Changing the published port is a one-line change but it
is application configuration, and the frontend URL at `docker-compose.yml:49`
has to move with it.

---

## 7. `fast_llm` has no fallback, and every model in the system is the same model

**Status:** diagnosed from source 2026-08-18 after a live rate-limit incident.
The silent part is fixed; the exposure itself is not.

### What happened

On 2026-08-18 a question through the deployed frontend hit
`openai.APIError: google/gemini-2.5-flash is temporarily rate-limited upstream`
at `search.py:63`. `search.py:65-69` caught it, logged it, and set
`search_variants = []`, so the tool searched with the user's original phrase and
the answer was still correct. That path degraded gracefully and worked as
designed.

**It is not a one-off blip.** `search.py:22` sets `max_retries=5` on the
expansion model, and the error was raised only after those five retries were
exhausted.

### Every model call is the same model

Read from source:

| Site | Model |
|---|---|
| `config.py:49` `primary_llm` | `MODEL_NAME`, defaulting to `google/gemini-2.5-flash` |
| `config.py:59` `fallback_llm` | `google/gemini-2.5-flash`, hardcoded |
| `config.py:69` `fast_llm` | `google/gemini-2.5-flash`, hardcoded |
| `search.py:16` `expansion_llm` | `MODEL_NAME`, same default |

`config.py:77` is `llm = primary_llm.with_fallbacks([fallback_llm])`. With
`MODEL_NAME` unset — which CLAUDE.md instructs — the fallback asks the same
provider for the same model that just refused. It protects against a
per-request error, not a model-level or provider-level outage.

**Unverified, and it would soften this:** OpenRouter routes one model across
several upstream providers, and the error said "rate-limited *upstream*". The
retry may therefore land on a different upstream. That is inferred from the
wording of the error message, not from OpenRouter's documented routing.

### `fast_llm` is the sharper exposure

`config.py:77` wraps only `primary_llm`. **`fast_llm` is wrapped by nothing.**
It makes the first model call on every request and carries the lowest retry
count of the four, `max_retries=2` at `config.py:74`. Three call sites:

| Site | Behaviour on failure |
|---|---|
| `chat.py:119` triage | `chat.py:154-155` logs and falls through to the core pipeline. Graceful. |
| `agents.py:41` scope router | Falls through to `retrieval_node`. **See below.** |
| `agents.py:126` conversational | No local handler. Propagates to `chat.py:289-296`, which sends `{'error': ...}` to the browser. Hard failure, but visible. |

`semantic_router.py:1` imports `fast_llm` and never uses it — `route_query` is
pure string matching and regex (`semantic_router.py:7-35`), so the router itself
is not exposed. That import is dead.

### The scope router fails open, and it used to fail silently

**Fixed 2026-08-18:** `agents.py:54` was `except Exception: pass`, which broke
CLAUDE.md's rule against empty catch blocks. It now logs.

**Not fixed, and deliberately so:** the behaviour is unchanged. When
`fast_llm` fails at `agents.py:41`, control reaches `agents.py:71` and returns
`"retrieval_node"`, skipping the `OUT_OF_SCOPE` branch at `agents.py:50-51` and
the `CONVERSATIONAL` branch at `agents.py:52-53`. So a query that should be
refused is answered instead, for as long as the model is unavailable.

**Taken from DECISIONS.md, not source:** that refusal is deliberate and
load-bearing. The entry "OUT_OF_SCOPE takes precedence in the router prompt"
records that it stopped firing for a LinkedIn scraping request and that the rule
ordering was changed to restore it. A rate limit now reproduces that same
failure by a different route.

**Whether it should fail closed instead is a product decision and has not been
taken.** Failing closed would refuse legitimate queries during any outage.

### OpenRouter findings, 2026-08-18 — provenance: a third-party dashboard

**Read these with their provenance attached.** The two findings below come from
the OpenRouter web dashboard, read from screenshots by the user's advisor. They
are **not** from this repository, not from its documentation, and have not been
re-verified from source. Anything acted on from here should be re-checked on the
dashboard first. Both are the user's to act on — the OpenRouter dashboard is
outside the repository.

**1. `google/gemini-2.5-flash` has more than one upstream provider.** The model
page's Providers table lists Google Vertex and Google AI Studio, both at
$0.30 / $2.50 per million tokens, and the performance charts plot three series:
Google AI Studio, Google Vertex (Global) and Google Vertex (EU).

*Consequence:* a retry of the same model can land on a different provider, so
`config.py:77`'s same-model fallback is **not pure decoration**. This lowers the
priority of the "point `config.py:59` at a different provider" option below —
that option was recorded without knowing the provider count.

*Not settled:* whether OpenRouter fails over between providers **inside** a
single request or only between requests. The aggregate availability figure on
the model page is higher than any individual provider's, which hints at the
former, but the figures were not legible at the zoom level used. This does not
change the ranking, so it was left open.

**2. No BYOK provider key is configured, and this is the root cause.** Every
entry on the OpenRouter BYOK page reads "Not configured", including Google AI
Studio and Google Vertex. So every request goes through OpenRouter's shared
arrangement with Google, and **the shared rate limit is what the 2026-08-18
failure hit.** The error's own remedy — "add your own key to accumulate your
rate limits" — is therefore the actual fix.

That page also states that OpenRouter prioritises your own key when present and
falls back to its own endpoints if your key is rate-limited, when that option is
enabled.

**This is the largest item here.** It removes the failure rather than routing
around it, and **no code change in this repository can achieve it.** It is an
account action on the OpenRouter dashboard, and the key is the user's to create
and enter. Never request a key in chat.

*Stated on the BYOK page and NOT read:* that Google AI Studio's free tier might
make these calls materially cheaper, and that OpenRouter charges some fee for
using your own key. Both need checking before relying on either.

### Options, in priority order after the OpenRouter findings

**0. Add a BYOK provider key.** Not a code change, not in this repository, and
above everything below it. See the finding above.

- **Give `expansion_llm` its own fallback** (`search.py:15-23`) on a different
  provider. The constraint below does not apply to it: `search.py:63` calls
  `ainvoke` on a plain prompt and parses `.content` as text, so it never calls a
  tool and never touches the approval panel. But this feeds retrieval, so it is
  under the EDD rules. Low value — the current path already produced a correct
  answer.
- **Point `config.py:59` at a different provider.** **Downgraded 2026-08-18.**
  It protects the failure that would break the product, but the multi-provider
  finding above means the existing same-model fallback may already retry against
  a different upstream, and a BYOK key addresses the cause directly. **Taken
  from DECISIONS.md:** the replacement must not emit text before its tool call,
  or the frontend's human-in-the-loop approval panel breaks, and it must support
  `bind_tools`, `astream_events`, `with_structured_output` and
  `with_fallbacks`. That is a candidate search plus testing, not a one-line
  edit. Gated on finding a model, and now lower priority than option 0.
- **Give `fast_llm` a fallback.** Not previously considered. It never calls
  tools at any of its three sites, so the approval-panel constraint does not
  apply to it either — the same reasoning as `expansion_llm`.

**This does not oblige an evaluation run, established from source.**
`langchain_core/runnables/fallbacks.py:187-188` iterates the runnables and
returns on the first success, and `fallbacks.py:156-161` documents that iterator
as yielding the runnable and then its fallbacks. A fallback is never reached
while the primary succeeds, so a passing 94-case run cannot exercise a changed
fallback and the score cannot move. This holds only for `config.py:59` and the
fallbacks above. Changing `config.py:49` changes the model under test and does
require a run.

---

## 8. Smaller items

- **Index 22 is judge noise, not a regression.** It is served by the unchanged
  fast-path table, so its output is byte-identical between runs, and its
  verdict has still flipped. The judge's `request_timeout` changed its cache
  key at one point, which re-judged everything. Do not chase it.
- **`git filter-repo` cannot run in this working repo without `--force`.** Its
  clean-tree guard calls `git ls-files -o` *without* `--exclude-standard`, so it
  counts gitignored paths too — 126,974 entries here, 51,050 of them inside
  `.venv`. Gitignoring does not help. And `--force` skips every guard and then
  ends with `git reset --hard` (`reset = not is_bare`), which would discard all
  uncommitted tracked changes. Operate on a fresh clone instead.
- **The evaluation never exercises `chat.py`.** `eval.py` invokes the compiled
  graph directly, so the input guardrail, the output masking and the semantic
  cache are all untested by the suite.
