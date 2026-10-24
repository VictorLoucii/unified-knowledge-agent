---
paths:
  - "backend/core/**"
  - "backend/evals/**"
---

# Eval-driven development

These rules apply to any change to the system prompt, the semantic router, the
tools or the retrieval pipeline. Carried over from
`.agents/rules/eval-driven-development.md` and the pre-migration `CLAUDE.md`.

## The command

```bash
uv run python -m backend.evals.eval --concurrency 1
```

- **Never set `MODEL_NAME`.** Three places read it: `config.py:49` (agent,
  default `openai/gpt-5-mini`), `search.py:16` (query expansion,
  `google/gemini-3.5-flash-lite`) and `eval.py:67` (judge,
  `deepseek/deepseek-chat`). Setting it also swaps the judge. A model migration
  changes the default strings in source (`OPEN.md` item 8).
- **`fast_llm` must not be `gemini-3.5-flash-lite`.** As the scope router it
  marked six plain Python questions out of scope (`OPEN.md` item 8).
- **`--concurrency 1`.** The default of 10 segfaults on this Mac in PyTorch's
  Apple-GPU backend.
- **Every run overwrites `backend/evals/latest_run_metrics.json`**, a partial
  `--indices` run too. Back it up before a partial run; restore it after.
- `--indices` is 1-based (`eval.py:124`). `eval.py:130` sizes the totals from the
  sliced dataset.
- The run needs `.env`, which the sandbox blocks. The owner starts it.

## The rules

1. **Run the suite before calling the work done.**
2. **Do not drop below the committed baseline**: `latest_run_metrics.json` at
   `HEAD`. On a regression, find the cause, fix or revert, and re-run. Read the
   pass threshold from `eval.py`; never restate it.
3. **Be surgical with the system prompt.** The directives in
   `backend/core/agents.py` for problem extraction, rigid formatting and the
   zero-knowledge guardrail are load-bearing.
4. **Change the test when the behaviour should change.** Update the expected
   output in `backend/evals/qa_dataset.json`; do not bend the prompt to an
   outdated test. Update `check_fast_path.py` in the same change when a change
   alters what it guards.
5. **For any bug, follow the EDD loop:**
   1. Document the query, the wrong output and the desired output. Touch nothing.
   2. Add the failing case to `qa_dataset.json`.
   3. Run the suite; watch the case fail.
   4. Fix the prompt or the retrieval logic.
   5. Re-run: the new case passes, old cases pass, scores at or above baseline.

## Read this before you trust the score

The fast-path table (`backend/core/fast_path_routes.py`, 53 entries) answers 53
of the 94 cases with no retriever or model call. `semantic_router.py` matches a
key as a substring of the query; `agents.py:fast_path_node` returns the stored
answer and a synthetic `ToolMessage` with the problem id, which `eval.py`
scrapes for Recall@k.

**When you change retrieval, report the 41-case and 8-case figures beside the
headline.** Run only the exercised cases:

```
--indices 1,3,4,5,6,27,28,29,30,31,36,37,42,44,45,46,51,57,58,59,60,62,63,64,65,66,67,68,71,72,73,74,77,78,79,80,81,83,92,93,94
```

That run prints the 41-case logic figure; its recall figure is the 8 genuine
retrievals (indices 6, 46, 77, 78, 79, 80, 81, 83). Derive the list again by
substring-matching each query against `FAST_PATH_INTERCEPTS` if the table or
dataset changes.

## Runtime proves nothing

- `eval.py:31` caches every model call in `.langchain.db` (gitignored, ~100 MB).
  A warm run makes no network calls. Any prompt, retrieval or model-string edit
  turns hits into misses. Do not read a slow run as a regression or a fast one
  as a pass.
- The cache is never invalidated: lookups key on the exact prompt text, and
  nothing in `backend/` calls `clear`. Reverting a file makes old rows match
  again, so a pre-change figure can always be re-measured.
- Recorded runtimes in this repo are not comparable to each other.

## Judge noise is real

The judge is an LLM; index 42 has flipped verdict on unchanged code. Before
chasing a one-case difference, check whether the agent's output changed. A
fast-path case with an unchanged table is byte-identical, so the judge moved.
`eval.py` retries a failed judge call five times, then records `passed=False`.
Grep the output for `LLM Judge evaluation failed` before editing a prompt.
