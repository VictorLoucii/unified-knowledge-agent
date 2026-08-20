# Open work

Known, diagnosed, and deliberately not started. Each entry records what is
wrong, what has already been established, and what has *not* been checked, so
none of it has to be rediscovered.

Decisions already taken are in [DECISIONS.md](DECISIONS.md).

---

## 1. Index 83 — 'Community Type' — FIXED 2026-08-20

**Status: fixed and measured.** The fix is the generalised verbatim directive at
`search.py:38-44`. Recall went from 33/34 to **34/34** and the AI Logic score
held at 90/94, so the change gained a point without costing one.

This item is kept at length, and not deleted, because **the diagnosis was wrong
twice before the fix worked.** That sequence is the useful part, not the result.

### The case-level timeline — read, not inferred

The same query, byte-identical, with the same `target_problem_id` of 12:

| When | Dataset | Recall | This case |
|---|---|---|---|
| 2026-07-26 (`f30ff63`) | 90 cases, index **82** | 34/34 | passed |
| after the 2026-08-17 index rebuild | 94 cases, index **83** | 33/34 | failed |
| 2026-08-20, after this fix | 94 cases, index **83** | 34/34 | passed |

Read from `git show f30ff63:backend/evals/qa_dataset.json` and the copy at
`HEAD`. So this is not a figure that happens to match twice — **the fix restores
the same case that the rebuild broke.**

### Three measurements, in order. Two of them refuted a recorded cause.

**1. The recorded mechanism was refuted by measuring the candidate pool.**

This item previously stated, as established fact:

> **The mechanism is the order of two steps.** `search.py:379` truncates the
> merged candidate pool to 50. `search.py:399` reranks to 10. The truncation
> happens *before* the rerank, so a document the reranker would have scored
> highly can be discarded before it is ever scored.

*(That quotation is left exactly as it was written. Its line numbers were
correct when it was written and are now `:390` and `:410`; correcting numbers
inside a quotation would make the quotation false.)*

**Refuted twice over.** In the failing case the document is not in the pool to
be discarded. In the succeeding case it sat at pool position 37 — inside the cap
of 50 — so the cap was not excluding it there either.

| | shortened query (failed) | full question (succeeded) |
|---|---|---|
| candidate pool, deduped | 97 | 108 |
| docs containing "community type" | **0** | 2, at positions 37 and 43 |
| docs from `NEXTIER_Internship_Bugs.md` | **0** | 18 |

**How that error survived.** Every piece of evidence offered for it was
output-level — what the tool returned. The mechanism it asserted was pool-level.
Nobody inspected the pool for weeks. `CLAUDE.md` now carries the standing rule
this produced: a record's evidence must sit at the same level as its claim.

**2. The replacement theory was weakened by measuring the tool argument.**

The replacement theory was that the tool's docstring is keyword-shaped —
`search.py:32-34` describes it as being for "specific topics, keywords, errors,
code logic, or existence checks" — and that the model fills the gap by
shortening. It was labelled `inferred`.

**It is weaker than inferred.** Three cases were probed at HEAD with the
docstring untouched, each by one graph invocation with no response cache
installed, so the argument was chosen live:

| Index | What the model sent | Verbatim? |
|---|---|---|
| 42 | `What is the primary purpose of \`pip\` in Python?` (47 chars) | **yes** |
| 93 | the full 87-character question | **yes** |
| 83 | `Community Type metric` (21 chars, from 76) | no |

**The model does not systematically shorten.** With the same docstring and the
same model, two of three sampled queries arrived whole. Keyword-shaped guidance
cannot be what causes shortening if most queries are not shortened. **Nothing
measured explains why 83 was the exception.** Three cases is a small sample and
nothing here generalises past it.

*A hypothesis, labelled as one:* 83 is the only one of the three whose question
wraps a quoted term in conversational framing. The one piece of evidence is that
the full question's expansion **keeps** the quotes — `'"Community Type" metric'`
— while the fragment's expansion loses them and drifts to `'Graph community
detection metric'` and `'Social network community measure'`. The framing is
unchanged between the failing and succeeding runs, so it cannot be sufficient on
its own; a directive overrides it.

**3. The fix works, and its mechanism is still a hypothesis.**

  before  argument 21 chars, `RETRIEVED_PROBLEM_IDS: []`, answered from general
          knowledge via the disclaimer at `agents.py:119`
  after   argument 76 chars and verbatim, `RETRIEVED_PROBLEM_IDS: ['12', '4',
          'Statement']`, answer built from retrieval

**Why the model complied where it previously did not is not established.** An
explicit directive raised compliance in the one case that needed it. That is
what was measured. It is not a mechanism, and it must not be written up as one —
which is the mistake this item already made once.

### The measured result, with its headroom stated

| | floor, at HEAD | after |
|---|---|---|
| headline recall | 33/34 | **34/34** |
| headline AI Logic | 90/94 | 90/94 |
| 8-case recall | 7/8 | **8/8** |
| 41-case AI Logic | 38/41 | **38/41** |

**The 41-case figure held with zero headroom, and that matters more than the
pass.** The failing set inside the 41 moved from `{42, 83, 93}` to
`{37, 42, 93}` — one case gained, one lost, cancelling. Had 37 not flipped the
figure would read 39/41; had 37 flipped the other way at the floor, the floor
would have been 39/41 and the change would now read as a regression. The same
change and the same measurements, with the verdict decided by a case that is
documented as unstable.

**Index 37 is judge variance, and the captured reasons are the evidence.** Same
case, same named content, opposite verdicts:

- floor, PASS: "...the 'Yellow Card' Protocol and recommendations for handling
  the error are **extra context that does not contradict** the expected output."
- after, FAIL: "The agent's output **included additional information** about the
  'Yellow Card' Protocol ... which were not part of the Expected Output."

**The limit on that claim.** 37 is inside the 41, so its agent call was a cache
miss and its output is **not** guaranteed byte-identical between the two runs.
This is evidence of judge variance on the same substance. It is not proof of a
flip on identical text.

This item previously said 37 and 83 "keep trading against each other" and
attributed it to the refuted pool mechanism. **They traded again here.** The
observation stands; the old explanation remains refuted and the new one is the
judge, for 37 specifically, on the evidence above.

### Rejected, and recorded so it is not reached for again

`search.py:86-93` already hardcodes two query injections for queries that expand
badly. A third for Community Type would have passed index 83 and would have
matched precedent. It would have moved the score without improving the pipeline,
which is the failure `CLAUDE.md`'s opening section exists to prevent.

### Still not established

- Why the model shortened index 83 and not 42 or 93.
- Why an explicit directive changed that.
- Whether the docstring change altered the argument for any case other than 83.
  **The seven passing recall targets were never probed.** They were not needed —
  recall rose, so there was no lost point to attribute — but if a future change
  drops one, their pre-change arguments are still measurable at any commit.
- The pool-ordering defect at `search.py:390` is untouched and still real: the
  pool is 97 and the cap is 50, so roughly half the candidates are discarded by
  `calculate_relevance_score`, a hand-written keyword scorer, before the
  cross-encoder scores anything. Whether widening it helps is **unknown**. A
  change raising the cap to 240 was written and reverted unevaluated on
  2026-08-20.

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
weights already on disk. Treat that as a floor, not a forecast.

**The deployed Space pays roughly twelve times that. Measured 2026-08-19:**
17,958 children in **about twenty minutes**, against 97 seconds locally — about
**15 chunks per second in the container, against about 185 on the Mac.** The
Space pays it on every container start, in the background thread at `app.py:76`,
so it never blocks the port bind. **It is not brief.** See item 4.

**The likely cause, read:** `config.py:88` is
`HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")` with **no device pinned**,
so the library selects the device. The Mac has one to select and the container
does not. *That the library picks the Mac GPU is general knowledge and is
unverified; what is read from source is that the code names no device.*

**Corroboration that the log describes this code.** `ingest.py:106` loops per
file and `ingest.py:165-169` batches within each file at `BATCH_SIZE = 100`.
17,958 children over 26 files, each file rounding up, gives between 180 and 205
batches. The log's 194 sits inside that range.

**Provenance:** the twenty-minute figure and the batch count come from the
Space's startup log, pasted by the user and read by the advisory session. I did
not read that log. The 97-second local figure is a record of a past run.

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
files in the background thread at `app.py:76`.

**How it was confirmed, at zero OpenRouter cost.** `app.py:102-119` exposes
`/health`, which reports `rag_hydrated` by testing whether the docstore holds
any key (`app.py:110`). An empty docstore was the entire bug, so this flag was
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
`online` while ingestion ran, which is what `app.py:74-76` was built for.

### Residue

**Closed 2026-08-19 — full 26-file coverage is now demonstrated.** The previous
entry read: "`rag_hydrated` proves 'at least one document', not 'all 26 files'.
`app.py:110` calls `next(store.yield_keys(), None)`. Nothing exposes a count."
The Space's startup log for the `5103325` rebuild printed
`Vector Database missing 26 files. Initiating Incremental Auto-Ingestion...`,
then one `Loading and splitting markdown data for` line per file — **26 of
them** — then `Auto-Ingestion complete. The Agent's memory is hydrated.`
Counting those log lines is what closes this; `/health` still cannot.
**Provenance: this is the advisory session's count over a container log pasted
by the user. I did not read that log and cannot re-derive it.**

**The same log settles three claims that were reasoned from the installed
package rather than seen.** The container printed `Span Processor:
BatchSpanProcessor`, `Collector Endpoint: localhost:4317`, `Transport: gRPC`,
and **no** `Attempting to instrument while already instrumented` line. That is
[DECISIONS.md](DECISIONS.md), "One tracing setup only", confirmed in
production. Same provenance caveat: reported, not read by me.

**Chunk counts moved, and the delta is not isolated.** The Space reported 8,911
parents and 17,958 children, against the 8,909 / 17,954 recorded for the local
rebuild at item 2. Commit `5103325` is the only `data/` change between them, so
`+2 / +4` is *plausibly* the two added bullets — **inferred, not proven per
file.** Do not treat item 2's local figures as a baseline for the Space.

### The Space reports healthy while its knowledge base is still loading

**Found 2026-08-19. Diagnosed from source. Nothing changed.** This is a
*different fact* from the residue closed above, which was about proving all 26
files eventually load. This one is about the window before they do.

Read, three lines:

1. `app.py:76` fires ingestion with
   `asyncio.create_task(asyncio.to_thread(initialize_rag))`. **Nothing awaits
   it.**
2. `app.py:110` computes `rag_hydrated` as `next(store.yield_keys(), None)`,
   which is true once **any** key exists — that is, after the **first** of 26
   files.
3. Item 2 records the Space's ingest at roughly **twenty minutes**.

**So for about twenty minutes after every container start, the Space reports
`rag_hydrated: true` while answering from a partially loaded knowledge base.**
It does not error. It answers, from less than it has. A question whose evidence
lives in a file not yet ingested gets a confident answer built on whatever did
load.

**Why this may recur rather than being a one-off after a push.** Free
HuggingFace Spaces sleep when idle and cold-start on the next visit, which would
put a visitor inside this window regularly. *General knowledge, *not* verified
for this Space.* If true, it matters most for the case the project exists to
serve: a recruiter opening the demo cold.

**Not fixed, and not obviously a one-liner.** Making `/health` report true coverage
needs a count the docstore does not expose, and gating answers on completion
would trade a wrong answer for a twenty-minute outage. Both are product calls.

**Cheapest honest option, not applied:** have `initialize_rag` set a module-level
flag when it finishes and report that alongside `rag_hydrated`, so the two
questions — "is anything loaded" and "is loading finished" — stop sharing one
answer. Purely additive. `CLAUDE.md` forbids changing application logic unless
asked.

### Still genuinely open

- **The model download time is still unmeasured.** The Dockerfile has no
  pre-download step, so `all-MiniLM-L6-v2` and
  `cross-encoder/ms-marco-MiniLM-L-6-v2` are fetched at first use. That time is
  not inside the 97 seconds in item 2. The three-minute figure above covers
  build plus app start, not ingestion alone, so it does not isolate it either.
  **The `5103325` log does not help.** Its `Loading weights: 100%|...| 103/103
  [00:00<00:00, ...]` line is a load from disk, no download progress appears,
  and the log carries no per-line timestamps, so neither duration can be read
  off it.
- **No question has been put to the Space.** Doing so spends OpenRouter credit,
  so it was deliberately skipped.

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

**Status: the two stale documents are FIXED. The propagation analysis below
stands and is the reason to keep this item.**

### The two stale documents — both corrected

- **`data/Unified_Knowledge_Project_Details.md`**, section
  `### C. Backend Instrumentation`. **Corrected 2026-08-19, commit `5103325`,
  approved per file under the `data/` exception.** Lines **1344-1368** were
  replaced; 13 out, 13 in, file length unchanged at 1952.
  **Two things this item got wrong before the fix, both corrected here.** The
  fence closes at **:1368**, not :1364 — :1364 was the `add_span_processor`
  line. And "only the fence is stale" was one line too narrow: :1344 said the
  provider went into "the application server's entry point" and :1346 named
  `app.py` as the file modified, and both were false once `247dd15` moved the
  setup to `config.py`.
  The surrounding reasoning about Arize Phoenix and running it in Docker to
  control cost was accurate and is untouched.
- **`CLAUDE.md`** claimed Phoenix is self-hosted via docker compose. Corrected
  2026-08-18. `docker-compose.yml` defines only `backend` and `frontend` plus a
  commented-out postgres — read, whole file. **`DECISIONS.md` carried the same
  claim and was not corrected at the same time; fixed 2026-08-19.**

### `data/` is Git LFS, which hides the diff

Found while applying `5103325`, and in no record before it. `.gitattributes:8`
is `data/*.md filter=lfs diff=lfs merge=lfs -text` — read. Two consequences.

- **`git diff` on a `data/` file shows a three-line pointer, not the text.**
  `5103325` reports "2 insertions, 2 deletions" for a 13-line change. To read a
  real diff, smudge the committed side first:
  `git cat-file -p HEAD:data/<f>.md | git lfs smudge > /tmp/before.md`
- **`.github/workflows/sync_to_hub.yml:16` sets
  `git config lfs.allowincompletepush true`** before the force-push to
  HuggingFace at :20 — read, whole file. That lets the mirror report success
  while shipping a pointer instead of the file. It did not fire for `5103325`,
  confirmed by the user fetching the Space's copy and matching
  `register(batch=True)`. **Treat that fetch as a standing check after every
  `data/` push**, because nothing in the workflow fails when the object is
  missing.

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

## 6. `docker compose up` has never been run

**Status 2026-08-19: four defects found, all four fixed in source. The local
path is CONFIRMED WORKING by execution. The compose path has still never been
run.** Fixed in `a147950` (published port, two dead volume mounts), `1163357`
(the frontend's frozen API URL), and `ff45f62` (local development documented on
the wrong port). Never affected the deployed Space, which uses neither
`docker-compose.yml` nor `frontend/frontend.Dockerfile`.

### The local path works — observed 2026-08-19, after `ff45f62`

The user started `uv run uvicorn backend.app:app --reload --port 7860` and
`cd frontend && npm run dev`, then put one query through the browser at
`localhost:3000`. From the server output:

```
INFO:  Uvicorn running on http://127.0.0.1:7860
INFO:  127.0.0.1:59286 - "GET /history?limit=20&offset=0 HTTP/1.1" 200 OK
INFO:  127.0.0.1:59296 - "OPTIONS /chat_stream HTTP/1.1" 200 OK
INFO:  127.0.0.1:59296 - "POST /chat_stream HTTP/1.1" 200 OK
⚡ [ROUTER] Fast-Path Intercept triggered for: What is the project rule
   regarding the use of npm versus yarn?
```

The answer rendered in the UI and the thread appeared in the Chat History
sidebar. **So this confirms more than the port number.** The streaming endpoint,
the request shape and session persistence all worked, which is exactly what a
matching port was never sufficient to prove.

**The `OPTIONS ... 200` is the browser's cross-origin preflight passing**, which
confirms live what was previously only read from `app.py:92` — that CORS is not
a blocker here.

**Provenance: the terminal output and a screenshot were pasted by the user and
read; nobody re-ran it inside a session.** It is one query through one endpoint,
not a suite. It establishes that the two halves talk on 7860; it does not
establish that every route behaves.

### What is actually still open

**`docker compose up --build` has never been executed in this repository, before
or after any of the fixes.** Three things follow, in increasing order of doubt:

1. **Whether the stack comes up at all.** Nothing about the compose path has
   ever been observed working.
2. **Whether the `args:` block delivers the value into the image.** The
   *freezing* is measured — two local `next build` runs, no Docker, showed
   `localhost:7860` three times with no variable set and `localhost:8000` three
   times with it set, one occurrence per call site. That the Docker `args:`
   plumbing reaches `next build` the same way is read-correct and unconfirmed.
   **Cheap settling test, no backend needed:** `docker compose build frontend`,
   then search that image's `.next/static` for `7860`.
3. **Whether the two halves talk *through compose*.** They do talk locally —
   see the observed run above — but that ran two processes on the host, not two
   containers with a published port between them. **CORS is ruled out on both
   paths:** `app.py:92` sets `allow_origin_regex=".*"` with `allow_methods` and
   `allow_headers` both `["*"]`, and the local run's `OPTIONS ... 200` shows a
   real browser preflight passing against it.

**Verification is not free but is not expensive either.** The Docker daemon was
down throughout, and `docker builder prune -a -f` on 2026-08-19 emptied the
build cache, so a first build re-downloads everything `Dockerfile:18`'s
`uv sync --frozen` pulls, including CPU-only PyTorch. A long build is expected
and is **not** evidence about any of the fixes. Disk is not a constraint.
Test 2 above avoids all of this by building only the frontend service.

### Where the reasoning lives, now that the defects are closed

Each fix took a specific shape over a rejected alternative. None of that is
repeated here; it is recorded where someone changing the file will actually see
it.

| Decision | Recorded in |
|---|---|
| Local development on 7860, not the code on 8000 | [DECISIONS.md](DECISIONS.md), "Local development is documented on 7860" |
| `NEXT_PUBLIC_*` must be a build argument, never `environment:` | `CLAUDE.md` "Frontend rules"; `frontend/frontend.Dockerfile:15-27`; `docker-compose.yml:48-62`, plus `:66-67` |
| Host 8000 mapping to container 7860, rather than 7860 both sides | `README.md`'s `[!IMPORTANT]` block; `docker-compose.yml:29-31` |
| Volume mounts deleted rather than repointed | `docker-compose.yml:35-39` |

**Do not re-add an `environment:` entry for `NEXT_PUBLIC_API_URL`, and do not
unify the two host ports.** Both look like tidying and both reintroduce a fixed
defect. The comments in `docker-compose.yml` say so at the point of edit.

---

## 7. `fast_llm` has no fallback, and every model in the system is the same model

**Status:** diagnosed from source 2026-08-18 after a live rate-limit incident.
The silent part is fixed; the exposure itself is not.

### What happened

On 2026-08-18 a question through the deployed frontend hit
`openai.APIError: google/gemini-2.5-flash is temporarily rate-limited upstream`
at `search.py:74`. `search.py:76-80` caught it, logged it, and set
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
count of the four, `max_retries=2` at `config.py:74`. **Four call sites** — an
earlier version of this item said three, having grepped only `backend/core/` and
missed the one in `app.py`:

| Site | Behaviour on failure |
|---|---|
| `chat.py:119` triage | `chat.py:154-155` logs and falls through to the core pipeline. Graceful. |
| `agents.py:41` scope router | Falls through to `retrieval_node`. **See below.** |
| `agents.py:140` conversational | No local handler. Propagates to `chat.py:289-296`, which sends `{'error': ...}` to the browser. Hard failure, but visible. |
| `app.py:161` `/refine_transcript` | `app.py:166-168` logs and returns the raw transcript unchanged. Graceful. |

**Line numbers drift.** `agents.py:140` was `:126` before commit `a8c9af9`
added the router log. Re-grep rather than trusting a line number in this file.

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

**0. Add a BYOK provider key. DONE 2026-08-18, AND CURRENTLY INERT.** The key
was added and its connection test for `google/gemini-2.5-flash` **failed** — the
model is closed to new users. Every request therefore still falls through to
OpenRouter's shared endpoints, which is the pre-existing behaviour including the
rate limit that failed. **This option cannot help until the model strings
change. See item 8**, which also records why nothing broke when the key was
added.

- **Give `expansion_llm` its own fallback** (`search.py:15-23`) on a different
  provider. The constraint below does not apply to it: `search.py:74` calls
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
  edit. Gated on finding a model. **Item 8 changes this calculation:** the
  question is no longer only which fallback to add, but which model the whole
  system should name at all.
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

## 8. The whole system names one model, and that model is closing to new users

**Status:** documented 2026-08-18. **No model choice has been made. No model
string has been changed. No migration has been started.** This item exists so
the next session does not rediscover any of it.

### Provenance — read this before acting on anything here

**Sections marked *dashboard* below come from the OpenRouter and Google AI
Studio web dashboards, read from screenshots by the user's advisor.** They are
not from this repository, not from its documentation, and have not been
re-verified. Re-check them on the dashboard before acting. The source-read
sections are marked separately and were verified against the files.

### The blocker — *dashboard*

A Google AI Studio provider key was added under OpenRouter BYOK. **Its
connection test for `google/gemini-2.5-flash` FAILED**, with:

> This model models/gemini-2.5-flash is no longer available to new users. Please
> update your code to use models/gemini-3.6-flash for the latest features and
> improvements. (Tested with: Google AI Studio | google/gemini-2.5-flash)

**Two consequences, and the second is the one that matters.**

1. **The BYOK key currently changes nothing.** Every request names
   `gemini-2.5-flash`, the key cannot serve it, and the request falls through to
   OpenRouter's shared endpoints — the pre-existing behaviour, including the
   shared rate limit that failed on 2026-08-18. This supersedes item 7's
   option 0, which is now done but inert.
2. **Nothing broke, and that was not luck.** The key sits in the *Prioritized*
   section with "Always use for this provider — Never fall back to OpenRouter
   endpoints" **OFF**. Had it been ON, every request to the deployed Space would
   now fail outright. **Do not turn that setting on while the code still names
   2.5.**

Key configuration, for the record: the user's existing free-tier key on Google
Cloud project "Gemini Project" (`gen-lang-client-0161969403`), created
1 Jul 2026, billing tier "Free tier". **Deliberately not** the key on project
"vision-flow-analtyics", which sits on a paid billing account for different
work — keeping those separate was an explicit requirement. Filters are Models =
All, API Keys = All, row enabled.

**Connection tests PASSED for `gemini-3.6-flash` and `gemini-3.5-flash`.**

**The limit of those passes, and it is the important one.** A connection test
proves the key can reach the model. **It does not exercise tool calling.** So no
candidate is validated against the constraint that decides this project.
**Taken from DECISIONS.md, not source:** a model that emits text before its tool
call breaks the frontend's human-in-the-loop approval panel, which is why
DeepSeek V3 was rejected as the driver.

### The exposure — *read from source*

Every model string in the repository names `gemini-2.5-flash`. Five
occurrences, and there are no others — checked across `backend/`,
`frontend/src`, the `Dockerfile`, `docker-compose.yml` and `.env.example`:

| Site | Form |
|---|---|
| `config.py:49` `primary_llm` | `MODEL_NAME` env var, default `google/gemini-2.5-flash` |
| `config.py:59` `fallback_llm` | hardcoded |
| `config.py:69` `fast_llm` | hardcoded |
| `search.py:16` `expansion_llm` | `MODEL_NAME` env var, same default |
| `generate_eval_dataset.py:41` | hardcoded. Offline script, not on the request path. |

**OpenRouter still serves the model** — two questions were answered correctly
through the deployed Space on 2026-08-18. "No longer available to new users" is
not "switched off", and existing access usually continues. That last sentence is
**inferred** from the wording, not established. The point stands regardless: the
whole application rests on one model that has begun closing doors.

### The trap that will bite a migration — *read from source*

`eval.py:67` is `model=os.getenv("MODEL_NAME", "deepseek/deepseek-chat")`.
`config.py:49` and `search.py:16` read the **same variable** with a different
default. So setting `MODEL_NAME` does not only change the agent — **it swaps the
evaluation judge from DeepSeek to whatever is set.** That is exactly what
CLAUDE.md warns about under Eval-Driven Development.

**Therefore: any migration belongs in the hardcoded default strings in source,
never in an environment variable.**

**And `config.py:49` is the one change that does oblige an evaluation run**,
because it is the model under test. **Taken from CLAUDE.md:** roughly $0.11 of a
$1.12 balance, and any run — including a partial `--indices` one — overwrites
`backend/evals/latest_run_metrics.json`, so back that file up first.

### Pricing — *dashboard*, per 1M tokens

| Model | List in / out | Weighted average actually paid |
|---|---|---|
| `google/gemini-2.5-flash` (current) | $0.30 / $2.50 | — |
| `google/gemini-3.5-flash-lite` | $0.30 / $2.50 — **cost parity** | $0.2125 / $2.351 |
| `google/gemini-3.5-flash` | $1.50 / $9.00 — 5x in, 3.6x out | $0.9848 / $8.999 |

- **`gemini-3.5-flash-lite`:** released 21 Jul 2026, 1M context. Providers:
  Google AI Studio, Google Vertex, Google Vertex (US). Latency 0.53 s / 0.67 s,
  throughput 72 / 64 tps, uptime 99.92%. Its own description says it is "suited
  for subagents that execute focused tasks within complex, multi-agent
  workflows."
- **`gemini-3.5-flash`:** released 19 May 2026, 1M context. Same three
  providers. Latency 1.53 s / 2.06 s, throughput 144 / 177 tps, uptime
  99.63% / 99.66%.

**Do not read Lite as simply faster.** It has the lower latency and the *lower*
throughput. For long answers throughput probably dominates. Not established.

**Three providers per model** extends the two-provider finding in item 7, which
was measured on the 2.5 family.

**The gap: `gemini-3.6-flash` and `gemini-3.7-flash` have not been priced.**
3.6 is the model Google's own error names as the replacement, which is the only
compatibility signal anyone has, and its cost is unknown.

### Two things nobody has looked at

1. **OpenRouter routing modes.** Every model page states that requests are
   routed "based on the routing mode you pick — Balanced (price + speed), Nitro
   (fastest), or **Exacto (highest tool-calling accuracy)**". *Dashboard.*
   Tool-calling accuracy is this project's binding constraint and Exacto has
   never been considered. It may matter more than the price difference.
2. **A per-site model split.** `fast_llm` does short classification and cleanup
   work at four sites — `agents.py:41`, `agents.py:140`, `chat.py:119` and
   `app.py:161` — **read from source**. None of them calls a tool, so none is
   bound by the approval-panel constraint. `fast_llm` does not have to share a
   model with the agent that does tool calls and formatted answers. All four
   currently use one model, which is why this reads as a single decision.
   **It is not one decision.**

### Unread, and the user's to check

- **The Google AI Studio Rate Limit page.** Decides whether an evaluation run,
  which fires roughly 188 model calls in a burst, would throttle against the
  user's own free-tier key.
- **Google's free-tier data-use terms.** The agent sends chunks of personal
  notes — internship logs, project details — on every request, and free and paid
  tiers have historically differed here. That last clause is the advisor's own
  knowledge, unverified. **The free tier was taken by default, not by decision.**
- **Whether OpenRouter charges a fee for BYOK requests, and how much.** Stated
  on the BYOK page.
- **Prices for `gemini-3.6-flash` and `gemini-3.7-flash`.**

---

## 9. The deployed API is public, unauthenticated, and three of its routes spend credit

**Status:** found 2026-08-19 from the Space's access log. Diagnosed from source.
**Options (b) and (d) were applied 2026-08-20 — see "What was done, 2026-08-20"
below. Options (c) and (e) stay blocked**, on a server-side component the
frontend does not have. What is left open is a product call, not a defect.

**What the log showed.** Automated scanners probed the Space repeatedly during
startup: the four common secrets paths (dotenv, its `.local` and `.production`
variants, and `.streamlit/secrets.toml`) plus two path-traversal attempts using
`file%3D../` prefixes. **Every secrets path returned 404. Nothing leaked.** One
endpoint answered: `GET /openapi.json` returned 200. *Reported by the advisory
session from a container log pasted by the user; I did not read that log.*

### Read from source, not from the log

- `app.py:84` **was** `app = FastAPI(lifespan=lifespan)` with no `docs_url`,
  `redoc_url` or `openapi_url` argument, so FastAPI's defaults applied and
  `/docs`, `/redoc` and `/openapi.json` were all public. **Closed 2026-08-20 by
  option (d)** — the same line now passes all three as `None`.
- **There is no authentication and no rate limiting anywhere in `backend/`.** A
  recursive grep over `backend/` for `Depends(`, `APIKeyHeader`, `HTTPBearer`,
  `set_cookie`, `slowapi`, `RateLimit` and `Authorization` returns **zero
  matches**.
- **Three public routes reach a paid model** — `/chat_stream`,
  `/refine_transcript` and `/chat_approve`. None checks anything about the
  caller. The full route table is below.
- `app.py:90-96` sets `allow_origin_regex=".*"` with `allow_credentials=True`.
  The comment at `app.py:86` calls this "Secure CORS" and `app.py:92` says it
  "Allows any local origin format"; `.*` matches **every** origin, not local
  ones.

### The assessment, and where it differs from the first reading

`/openapi.json` on its own is **low**. It publishes API shape, not secrets and
not data, and for a portfolio project a browsable schema may be exactly what is
wanted.

**The exposure that matters is not the schema.** It is that the spend routes
are open to anyone with the URL, and that the three `/history` routes hand out
stored conversations. Closing `/openapi.json` does **not** address either — the
routes answer a plain `curl` whether or not their schema is published.

**CORS is not the control here.** `allow_origin_regex=".*"` is wrong as written,
but CORS only governs what browser JavaScript may *read*. It does not gate
`curl`, a script, or a server-to-server call. Tightening it would not protect
the balance. Worth fixing so the comment stops claiming something untrue; do not
expect it to buy security.

### The full public surface — every route, read from source 2026-08-19

`app.py` declares eight routes. **None of them checks anything about the
caller.**

| Route | Line | Reaches a model | Notes |
|---|---|---|---|
| `GET /health` | :102 | no | Reports `rag_hydrated`. Harmless. |
| `POST /chat_stream` | :127 | **yes** | Runs the full graph. **Guarded — see below.** |
| `POST /refine_transcript` | :152 | **yes** | `fast_llm.ainvoke` at :161. **Length cap only**, `app.py:150`, 8,000 characters. No guardrail, no cache. |
| `GET /` | :172 | no | Serves `static/index.html` if present. |
| `POST /chat_approve` | :184 | **yes** | Resumes an interrupted graph run for any `thread_id`. |
| `GET /history` | :209 | no | Lists **every** thread id and title, with `limit`/`offset`. |
| `GET /history/{thread_id}` | :222 | no | Full message content of any conversation. |
| `DELETE /history/{thread_id}` | :252 | no | Deletes all data for that thread. |

**The three `/history` routes chain, and that is the data exposure.** `/history`
at :209 hands out the thread ids, so nothing has to be guessed; `/history/{id}`
at :222 returns the messages; `DELETE /history/{id}` at :252 removes them. The
stored conversations contain retrieved fragments of the personal knowledge base,
because that is what the agent answers with.

**`/chat_approve` extends the chain to a fourth spend route.** It takes a
`thread_id` and calls `resume_graph_stream`, so a thread id obtained from
`/history` can be used to resume someone else's interrupted run — which spends
credit. **An earlier version of this item counted two spend routes. There are
three: `/chat_stream`, `/refine_transcript` and `/chat_approve`.**

### The guardrails are asymmetric, and `/refine_transcript` is the soft target

**Read.** `/chat_stream` is genuinely defended, but none of the defence lives in
`app.py` — it is all in `chat.py`, which only `/chat_stream` routes through.

- `chat.py:49` calls `check_input_guardrail`. `guardrails.py:13` refuses any
  message over 1,000 characters, and `guardrails.py:20-25` blocks jailbreak and
  key-extraction phrases.
- `chat.py:66-99` checks the semantic cache first. A repeated or near-identical
  question is answered with **no model call**.
- The fast-path table intercepts 53 known questions before any model call.
  *(Taken from CLAUDE.md as a record; the count is not re-derived here.)*

`/refine_transcript` at `app.py:152-168` had **none** of them. No guardrail, no
length check, no cache. `app.py:149-150` was
`class RefineRequest(BaseModel): transcript: str` — **no maximum length**. Every
call reached the model. It was simultaneously the cheapest route to abuse and the
only one with no brakes.

**A length cap was added 2026-08-20.** `app.py:150` is now
`transcript: str = Field(..., max_length=8000)`. It bounds the cost of one model
call and nothing else. There is still no guardrail and no cache on this route, so
the asymmetry with `/chat_stream` stands.

**This is the same seam as item 11's note that "the evaluation never exercises
`chat.py`", seen from the other side.** Protections that live in `chat.py` cover
only what routes through `chat.py`.

### The key itself is not exposed

**Read.** `config.py:50`, `:60` and `:70` each pass
`openai_api_key=os.getenv("OPENROUTER_API_KEY")`. The key stays in the container
and never reaches a browser. The exposure is not key theft — it is that public
routes make model calls on behalf of whoever asks.

### Two pieces of dead configuration

- **`app.py:88` reads `VERCEL_FRONTEND_URL` into `frontend_url`, and nothing
  ever uses it.** A grep across `backend/` returns that single line and no other
  hit — read. The CORS middleware at `app.py:90-96` uses
  `allow_origin_regex=".*"` with `allow_credentials=True` instead. **So the
  allowlist the comment at `app.py:86` calls "Secure CORS" was written and never
  wired in.**
- CORS is not the control here regardless. It governs what browser JavaScript
  may *read*, not what `curl` or a server may call.

### Withholding the frontend link is not a mitigation

**Read.** The Space's own hostname is in the public repository three times:

- `data/Agentic_AI_Engineer.md:13824` — the full `/health` URL.
- `data/Errors_in_AgenticAI_Projects.md:1706` — the Space URL.
- `.github/workflows/sync_to_hub.yml:20` — the Space URL.

Vercel serves the frontend and holds no key, so withholding that link protects
nothing. HuggingFace Spaces are also publicly listed — *general knowledge, not
verified for this Space* — so the Space is discoverable without the repository
at all. **Recorded so a future session does not treat the withheld link as
protection.** The two `data/` occurrences are accurate notes, merely revealing;
correcting them is **not** a correction in the sense the per-file rule means, so
no `data/` edit is proposed.

### Scope of the loss

**Stated by the user, not read — an OpenRouter dashboard setting.** Auto-topup
is **off**, so the financial loss is capped at the balance, about **$1.12**.

The consequence that matters for a portfolio project is not the money. **A
drained balance means the Space stops answering, and the demo is dead at the
moment a recruiter opens it.**

### No evidence of abuse

*Container log, pasted by the user; I did not read it.* The scanner traffic
probed secrets paths, `/api/config` and `POST /api/predict`. `/api/predict` is
**Gradio's** endpoint, not this app's, so the scanner did not have the real
route names. No POST to `/chat_stream`, `/refine_transcript` or `/chat_approve`
appears.

**The link to `/openapi.json` was real, though.** It returned 200 and published
exactly the route names the scanner was missing. **Closed 2026-08-20 by option
(d).** It now returns 404 — measured against the real `app` object, not assumed.

### Options — (b) and (d) applied 2026-08-20; (c) and (e) still blocked

**(a) Record only, fix nothing.** Costs nothing. Buys a written record so the
next session does not rediscover this. **This is what was done on 2026-08-19.**

**(b) A length cap on `RefineRequest.transcript`, `app.py:149-150`. — APPLIED
2026-08-20.** One line, purely additive, breaks no caller. Bounds the cost of one
model call; does not stop abuse. The value is **8,000** characters. It is not the
`1000` this option used to recommend for symmetry with `guardrails.py:13` — that
recommendation was refuted from the frontend source, and the refutation is under
"Why 8,000 and not 1,000" below.

**(c) A shared secret required by the spend routes.** **This does not work as
stated, and the frontend is why.** Read: every call site is client-side —
`page.tsx:71`, `ChatInput.tsx:84`, and `useChatStream.ts:48`, `:173`, `:218`,
`:261`, `:293`. All three files resolve
`process.env.NEXT_PUBLIC_API_URL`, and `ChatInput.tsx` and `page.tsx` are
`"use client"`. **A `NEXT_PUBLIC_*` variable is inlined into the JavaScript
bundle at build time and served to every visitor**, so a secret the frontend
holds is readable in devtools by anyone. The only version of (c) that works puts
a server-side proxy in front — a Next.js route handler that holds the secret
server-side and forwards. That is a real feature, not a one-line change.

**(d) `openapi_url=None, docs_url=None, redoc_url=None` at `app.py:84`. —
APPLIED 2026-08-20.** One line. Obscurity only — `/chat_stream` is not an exotic
name. Slightly better than it first appears, because the scanner in the log
demonstrably did **not** have the route names, and `/openapi.json` handed them
over. Fixes nothing on its own.

**(e) Authentication on the three `/history` routes.** **Blocked by the same
thing as (c).** The frontend calls `/history` from the browser at
`page.tsx:71` and `useChatStream.ts:48`, so any credential it carries is equally
public. Narrowing the scope does not escape the problem: this frontend has no
server-side session to hold anything.

**The real dependency, stated plainly.** (c) and (e) are not backend tasks. They
need a server-side component the frontend does not currently have. Doing either
badly breaks the demo, which is worse than the exposure it fixes. **Give them
their own session with the frontend in scope.**

### What was done, 2026-08-20 — options (b) and (d)

Both edits sit on lines that already existed, and `backend/app.py` has the same
number of lines before and after. **Every `file:line` citation into that file
still points where it did.** The 33 `app.py:NNN` references that stood across the
records before the edit, and the 12 bare `:NNN` references inside this item, were
re-checked line by line afterwards. One was already wrong and is corrected in the
same commit: this item cited `app.py:87` for the "Secure CORS" comment, which
sits at `app.py:86`.

**A grep for that filename now returns 41, not 33, and the eight are additions
rather than omissions.** They are citations written for the first time by this
section, by the corrected line above it, and by the `DECISIONS.md` entry in the
same commit: one to the `pydantic` import, two more to the `FastAPI` line, two
more to the CORS comment, and four to the capped field — three here and one in
`DECISIONS.md` — less the single citation lost with the "Not checked" bullet that
this section answers.

1. **`app.py:84`** now reads
   `app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)`.
   **Measured:** `/openapi.json`, `/docs` and `/redoc` each return **404**,
   requested against the real `app` object.
2. **`app.py:150`** now reads `transcript: str = Field(..., max_length=8000)`,
   with `Field` added to the `pydantic` import already on `app.py:4`.
   **Measured:** a POST of 8,001 characters returns **422** with
   `string_too_long` and carries no `refined_transcript` key; 8,000 characters
   validates.

**How those two were measured, and by whom.** Both come from one in-process run
against the real `app` object, with `TestClient` used *without* its context
manager so the lifespan never starts — no pool, no ingestion, and no request that
reaches `fast_llm`. One session ran it; nobody reproduced it independently. The
run is cheap to repeat if a later session wants its own figure.

**The 422 is invisible to the user, and nothing breaks.** `ChatInput.tsx:89-91`
reads `data.refined_transcript || currentTranscript` with no `response.ok` check,
so a rejected transcript falls back to the raw one and the input box still fills.
The text is merely unrefined.

**What the cap does not do.** `fastapi/routing.py:425` reads the whole body
before anything validates it, so a large POST is still received and parsed, then
rejected. The cap bounds the cost of one **model call**, not the bytes the server
ingests. And it bounds one call only — there is still no rate limit anywhere in
`backend/`, so total spend scales with request count, which nothing here limits.

**Option (d) costs the local `/docs` page too.** The interactive schema is gone
in development as well as in the Space. Getting it back is an edit to
`app.py:84`, not a setting.

**One consequence left alone.** `data/Agentic_AI_Engineer.md:14254` gives
`http://127.0.0.1:8000/docs` as a local URL, which option (d) turns into a 404.
`data/` is out of scope here — read as a grep hit, not in context — and this is
recorded so the next reader knows why that URL stops working.

#### Why 8,000 and not 1,000

`1000` was what this item recommended, for symmetry with `guardrails.py:13`.
**That recommendation was wrong, and the frontend is why.** There are two ways to
stop recording and they do not behave alike.

1. `ChatInput.tsx:117-127` — pressing Send while the microphone is live stops,
   refines, and submits at `:124` with no chance to edit. On this path a
   transcript over 1,000 characters does produce a message `guardrails.py:13`
   refuses, so the symmetry argument holds.
2. `ChatInput.tsx:180` — the microphone button stops and refines **without
   submitting**. `ChatInput.tsx:92-93` puts the refined text in the input box and
   the user edits it there. A 1,400-character dictation trimmed by hand to 600
   sends successfully today. A cap of 1,000 would have rejected it before it
   could be trimmed, and `ChatInput.tsx:89-91` would have said nothing.

The two limits also measure different strings. `ChatInput.tsx:92-93` prepends
whatever was already in the box, so even a 900-character transcript can produce a
message the filter refuses.

**Where 8,000 comes from.** The frontend bounds the transcript nowhere:
`useVoiceRecording.ts:20` sets `continuous: true`, and the textarea at
`ChatInput.tsx:156-173` carries no `maxLength`. So the bound cannot be read off
what the frontend sends. It comes from what a person can dictate and what one
request may cost. At roughly 700-900 characters a minute of speech — general
knowledge, not measured here — 8,000 is about ten minutes of unbroken dictation.
For scale, the longest question in `qa_dataset.json` is 163 characters and the
median 75, across 94 cases. The worst single request the cap allows is about
2,000 input tokens.

**No evaluation run was owed for either edit.** `eval.py:22` imports only
`workflow` from `agents.py`, `eval.py:35` compiles it against `MemorySaver`, and
`eval.py:44` calls `graph.ainvoke` directly. The suite never imports
`backend/app.py`, never issues an HTTP request, and never routes through
`chat.py`, so it exercises neither `/refine_transcript` nor `/chat_stream`.

#### The resume path, settled by probe

The open question was whether `resume_graph_stream` fails safely for a
`thread_id` with no pending interrupt. It does, in both senses — it does not
crash, and it does not spend.

**Mechanism, read.** `langgraph` 1.1.3,
`.venv/lib/python3.12/site-packages/langgraph/pregel/_loop.py`: `:633-644` sets
`is_resuming` from `bool(checkpoint["channel_versions"])` together with
`self.input is None`; `:717` takes the resuming branch and bumps `versions_seen`;
`:759-760` raises `EmptyInputError` when neither a resume nor an input write
applies.

**Observation, run.** The real `workflow` from `agents.py`, compiled against
`MemorySaver` — which is what `eval.py:35` does. No server, no database, no HTTP.

- An unknown `thread_id` raises `langgraph.errors.EmptyInputError: Received no
  input for __start__` and produces zero events. `chat.py:431-436` catches it and
  yields `{"error": ...}` then `[DONE]`, so the stream terminates cleanly.
- A thread with `state.next == ()` raises nothing and yields two events,
  `on_chain_start` and `on_chain_end`. No `on_chat_model_*` event appears, so no
  model call is made.

The settled-thread probe wrote its state with `as_node="fast_path_node"`, because
`agents.py:188` edges that node straight to `END` and the write therefore leaves
nothing to run. **A first attempt wrote the `messages` channel with no `as_node`,
which re-triggered the entry node and spent one real model call.** Recorded
because the fault was in the probe's design, not in the code under test, and the
same trap will catch the next session that fabricates a state this way.

**`/chat_approve` is still a spend route.** A thread that *is* interrupted
resumes and calls the model for any caller holding its id. Nothing here changed
that.

### Not checked

- Whether the HuggingFace Space sits behind any gateway that rate-limits or
  filters before the container sees a request. That could change the whole
  assessment; there is no evidence either way.

*The second bullet that stood here — whether `resume_graph_stream` fails safely
for a `thread_id` with no pending interrupt — was answered 2026-08-20. See "The
resume path, settled by probe" above.*

---

## 10. Every query was silently truncated to 150 characters — FIXED 2026-08-20

**Status: fixed**, in the same change as item 1, because item 1's fix would have
promised exactly what this line quietly undid.

`search.py:47` was `query = str(query)[:150].strip()`, the first statement in
`search_knowledge_base`. It ran before expansion, before retrieval, and before
the debug line that prints the query — so the log showed the truncated string as
if it were what arrived, and a reader could not tell a long query had been cut.

**What replaced it**, at `search.py:50-58`: the cap is now 1,000 and a `✂️` line
prints when the cut fires, immediately before the existing query print.

**Why 1,000, and the caveat that belongs with it.** `guardrails.py:13` already
refuses any user message over 1,000 characters, so this imports a bound the
product enforces rather than inventing a number. **That guard runs on the
`chat.py` path only.** `eval.py` invokes the compiled graph directly and never
reaches it — see item 11 — so on the suite's path this line is the only bound
there is. It is a bound the product enforces on one of its two paths, not a
bound the suite enforces.

**The suite could not have detected either half of this fix, and that is worth
stating plainly.** The longest query that reaches the tool in the whole dataset
is 144 characters, at index 60. The only two queries over 150 — index 48 at 163
and index 50 at 152 — are both fast-path intercepted, so neither ever reaches
`search_knowledge_base`. Measured 2026-08-20. **The cap change cannot move
either score.** It was made for real users, not for the test, and a later reader
should not mistake an unmeasurable change for an unmeasured one.

**Still not established:** whether 150 was chosen for a reason. No record names
it, and the original comment gave a purpose but not a number. That comment is
preserved and extended rather than replaced. Whether any real user query was
ever truncated in production is also unknown — nothing logged it, which was the
defect.

---

## 11. Smaller items

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
- **The runtime line is printed twice on a pass and once on a fail, and that is
  a useful accident.** `eval.py:246-247` and `eval.py:251-252` are the same
  `end_time` / `⏱️ Total Evaluation Time` pair, with `sys.exit(1)` at
  `eval.py:249` between them. A failing run exits before the second. So the
  count of that line is a gate signature that survives in any archived log,
  independent of whether the status line was captured. Confirmed on two logs on
  2026-08-20: `f30ff63:full_evaluation_log.txt` and the copy at `HEAD` both
  print it twice and both carry `🏆 STATUS: PRODUCTION READY`. **Anyone tidying
  the duplicate away is removing a diagnostic**; say so in the commit.
