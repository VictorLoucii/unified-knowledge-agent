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

## 2. Content-hash tracking, so re-ingestion stops being manual

**Status:** not started. Split out of the completed rebuild item.

Ingestion keys on filename only, so an edited file is never re-read. The
2026-08-17 rebuild was the manual workaround.

**Already established:**

- A hash alone is not enough. It detects the change but does not remove the old
  chunks. A working version needs the manifest to store
  `{basename: {sha256, doc_ids}}`, a delete path for both Chroma and the
  docstore, and `add_documents` called with explicit `ids=`.
- Clearing manifest entries without rebuilding is *not* safe — it appends a
  second copy rather than replacing the first. Measured on the pre-rebuild
  index: 8,404 distinct chunks were each stored 5 times, a few 10, 15 and 20
  times.

**Measured during the rebuild, useful here:** a full ingest of 26 files —
17,954 child chunks, 8,909 parents — took **97 seconds** on a MacBook Air with
the embedding weights already on disk. Treat that as a floor, not a forecast,
on other hardware or a cold model download.

That 97 seconds decided item 4. The deployed Space now ingests at startup, so
it pays this cost on every restart — in a background thread, so it never blocks
the port bind. Content-hash tracking would not remove that cost, because Space
storage is ephemeral and there is never a prior index to compare against. This
item is now purely about the local workflow.

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

## 5. Two documents now describe tracing code that no longer exists

**Status:** found 2026-08-18 while removing the duplicate tracing setup. Not
fixed, and one of them must not be fixed here.

- **`data/Unified_Knowledge_Project_Details.md:1342-1364`** presents the
  deleted `app.py` block — `SimpleSpanProcessor`, `OTLPSpanExporter`,
  `http://localhost:6006/v1/traces` — as the way to instrument the backend.
  **Do not edit this.** `data/` is the curated source of truth and this
  project's rules forbid touching it. The consequence is real: ask the deployed
  agent how tracing is set up and it will answer with code that was removed for
  being a production defect. Editing that note is the user's call, in their own
  editor, followed by a rebuild — and ingestion keys on filename, so an edit
  alone will not be picked up (see item 2).
- **`CLAUDE.md`** states that Phoenix is self-hosted via docker compose.
  `docker-compose.yml` defines two services, `backend` and `frontend`, plus a
  commented-out postgres. There is no Phoenix service — read, whole file. So
  there is also no compose service in which to open the gRPC port that
  `config.py:31` now depends on.

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

## 7. Smaller items

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
