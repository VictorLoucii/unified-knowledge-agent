# Open work

Known, diagnosed, and deliberately not started. Each entry records what is
wrong, what has already been established, and what has *not* been checked, so
none of it has to be rediscovered.

Decisions already taken are in [DECISIONS.md](DECISIONS.md).

---

## 1. Rebuild the vector index to pick up edited markdown

**Status:** diagnosed, planned, not run.

Ingestion keys on filename only, so edited files are never re-read. Three files
in `data/` have been edited since their last ingestion — roughly 33 KB added
across `AgenticAI_Interview_Questions_Theory.md`, `JobHunt_Project_Details.md`
and `Unified_Knowledge_Project_Details.md` — and none of that text is in
ChromaDB. `Pragmatic_Programmer_for_Agentic_AI.md` is on disk and absent from
the manifest, so it would be picked up by any ingestion run.

**Already established:**

- The edits are almost purely additive: 3 removed lines against 496 added.
- **No existing test breaks after a rebuild.** Every `expected_output` was
  matched as 8-word verbatim spans against the pre-edit and post-edit contents.
- **Exactly one case gains:** the docker-compose build case can only pass after
  a rebuild, because its answer has never been ingested.
- Clearing manifest entries without rebuilding is *not* safe — it appends a
  second copy rather than replacing the first, and changed chunks do not
  de-duplicate, so the stale and fresh versions compete in retrieval.

**The plan:**

1. Copy any new `.docx` outside `data/` first — ingestion deletes the original.
2. `mv backend/chroma_db backend/chroma_db.bak` and the same for
   `backend/docstore`. Rename, do not delete; both are gitignored and git holds
   no backup.
3. Reset `data/.manifest.json` to `{"ingested_files": []}`.
4. There is no ingestion CLI — `initialize_rag` only fires on FastAPI startup.
   Call it directly:
   `uv run python -c "from backend.core.ingest import initialize_rag; initialize_rag()"`
   It needs `OPENROUTER_API_KEY` present, because importing `config` raises
   without it.
5. Confirm the manifest lists every file and both directories repopulated.
6. Re-run the evaluation and compare against the committed baseline.
7. Delete the two `.bak` directories only once step 6 looks right.

**Not checked:** how long a full ingest takes, and whether the weather case's
criteria need a live `WAQI_API_KEY`.

**Also worth deciding separately:** whether to add content-hash tracking so
this stops being manual. A hash alone is not enough — it detects the change but
does not remove the old chunks. A working version needs the manifest to store
`{basename: {sha256, doc_ids}}`, a delete path for both Chroma and the
docstore, and `add_documents` called with explicit `ids=`.

---

## 2. Index 37 — LangGraph recursion limit answered from general knowledge

**Status:** diagnosed, cause known, not fixed.

The agent answers "100 or 1000" instead of "25 steps", and says
`RecursionError` instead of `GraphRecursionError`.

**Already established:**

- This is a **retrieval** failure, not a fallback failure. The cached answer
  begins with the exact required disclaimer, so the general-knowledge fallback
  behaved as designed. See the fallback entry in [DECISIONS.md](DECISIONS.md).
- The content is in the index and reachable — the same case passed before the
  query-expansion change.
- It is the price paid for fixing indices 5 and 83. Net logic was flat; the
  gain was on recall.
- The evaluation is right to fail it: the answer is wrong on the facts and the
  correct answer was available.

**Not tried:** anything targeted at this case. The obvious next step is to find
why the keyword expansion misses this content specifically, rather than
reopening the expansion prompt — a mixed keyword-plus-sentence prompt was
already tested for one cycle and scored 0/4.

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

- Across `data/` this manufactures **37 fake ids**: `Summary` ×12,
  `Description` ×9, `The` ×5, `Statement` ×2, and others.
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

## 4. Smaller items

- **Index 22 is judge noise, not a regression.** It is served by the unchanged
  fast-path table, so its output is byte-identical between runs, and its
  verdict has still flipped. The judge's `request_timeout` changed its cache
  key at one point, which re-judged everything. Do not chase it.
- **`.langchain.db` is tracked in git**, about 12 MB packed, and only one
  commit deep. It holds prompts and completions from the knowledge base — no
  credentials, verified by scanning all 47.8 MB of decompressed text — and it
  is public on both GitHub and the HuggingFace Space. Worth a deliberate
  decision about whether it should stay tracked.
- **The README's `k=40` claim is partial.** `config.py` does set
  `search_kwargs={"k": 40}`, but `search.py` then truncates the candidate pool
  to 50 and reranks to 10. The sentence is true about the retriever and silent
  about the later cuts.
- **The evaluation never exercises `chat.py`.** `eval.py` invokes the compiled
  graph directly, so the input guardrail, the output masking and the semantic
  cache are all untested by the suite.
