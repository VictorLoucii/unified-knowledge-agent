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

That 97 seconds is also the number that decides item 4, where the question is
whether the deployed container can afford to ingest at startup.

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

## 4. The deployed Space runs with an empty vector database

**Status:** diagnosed from source and confirmed by observation. Never recorded
until 2026-08-18. Not fixed. This is the most consequential item here: the
deployed product cannot answer from the knowledge base at all.

**Do not confuse this with the HuggingFace sync failure. That is settled.** The
sync works — run #78, commit `8142e49`, six green steps in 8 seconds. Fixing the
push did not touch this, and this predates it: runs #66 through #73 all
succeeded and the Space still had no index.

**The mechanism, every line verified 2026-08-18:**

1. `.gitignore:21` excludes `**/chroma_db/` and `.gitignore:23` excludes
   `**/docstore/`, so neither directory is in the repository.
2. `Dockerfile:21` is `COPY backend/ ./backend/`, which therefore copies no
   index — there is nothing to copy.
3. `Dockerfile:24` is `COPY data/ ./data/`, which *does* ship
   `data/.manifest.json`, because that file is tracked.
4. The shipped manifest names all 26 files, so at startup `initialize_rag`
   finds nothing to ingest and takes the early return at `ingest.py:91-93`,
   printing "Vector Database & DocStore up to date" over an empty store.
5. Chroma then creates an empty persistent directory, so nothing errors. The
   failure is silent.

**Confirmed by observation:** the Space's `backend/` folder is 255 kB and holds
only `core/`, `evals/`, `app.py`, `basics.ipynb` and `memory.py`. No
`chroma_db`, no `docstore`.

**Someone already intended to ship the index and was silently overruled.**
`.gitattributes:4-6` carry LFS rules for `backend/chroma_db/**/*.bin`,
`**/*.pickle` and `*.sqlite3`. `.gitignore:21` cancels all three, so those rules
match nothing and have never done anything.

**Two routes, neither obviously right:**

- **Ship the index** through the LFS rules that already exist. Costs about
  146 MB of LFS (`chroma_db` 111 MB, `docstore` 35 MB), and the shipped index
  goes stale the moment any `data/` file is edited, because ingestion keys on
  filename — see item 2. Every rebuild becomes a large commit. Buys instant
  startup and deterministic content.
- **Stop tracking `data/.manifest.json`** so the container ingests at startup.
  Buys nothing large in git and content that is always current. Costs a startup
  penalty on every restart, because Space storage is ephemeral.

**The number that decides it is already in item 2:** a full ingest of 26 files
took **97 seconds** locally, with the embedding weights already on disk. That is
a floor, not a forecast — see below.

**Not checked, and load-bearing for the second route:**

- Whether `all-MiniLM-L6-v2` and `cross-encoder/ms-marco-MiniLM-L-6-v2` resolve
  inside the Space's network sandbox. If they do not, startup ingestion cannot
  work and only the first route is available.
- The Dockerfile has **no model pre-download step**, so both models are fetched
  at first use inside the container. Their download time is not in the 97
  seconds and is not measured.
- What the deployed Space actually answers today. Nobody has asked it a
  question. The expected behaviour, given an empty index, is that it answers
  only from the 53-entry fast-path table and from general knowledge behind the
  disclaimer.

---

## 5. Smaller items

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
