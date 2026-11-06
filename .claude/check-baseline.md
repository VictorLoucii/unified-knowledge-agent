# Check baseline

Measured 2026-10-24 at `0087b43`, sandbox on. Update this file only in the change
that moves a number, and say why.

| Check | Command | Result |
|---|---|---|
| Frontend lint | `cd frontend && npm run lint` | 27 problems: 26 errors, 1 warning |
| Frontend types | `cd frontend && npx tsc --noEmit` | 0 errors |
| Python syntax | `.venv/bin/python -m compileall -q backend` | exit 0 |
| Core tests | `.venv/bin/python -m pytest --confcutdir=backend/tests backend/tests` (sandbox); `uv run pytest` (owner, CI) | 307 passed, 5 xfailed, 65.01 s by `time` (the masking bug, kept as a strict expected failure, now run in five switch states). Added 2026-10-29; 10 registry tests added the same day (`test_core_registry.py`, P2 item 3); 19 pre-step tests added the same day (`test_core_pre_steps.py`, P2 item 4). 2026-10-30, P2 item 5: 7 semantic-cache tests removed with the cache, 3 added (39 - 7 + 3 = 35). 2026-10-30, P2 item 6: 6 triage tests removed with triage, 2 added (35 - 6 + 2 = 31). 2026-11-01, P2 item 7: 8 route tests added (31 + 8 = 39). 2026-11-02, `OPEN.md` item 15: 3 follow-up tests added, 0 removed (39 + 3 = 42, 43 with the xfail). 2026-11-02, P2 item 8: the tests that use `core` now run in switch states, 32 in five and 5 in two, with 6 unchanged (160 + 10 + 6 = 176 cases); `test_core_switches.py` adds 24 cases from 15 functions (176 + 24 = 200). 2026-11-03, P2 item 9: 8 removal, 23 import-check and 10 route cases added, 0 removed (200 + 41 = 241); without `test_removal.py` the suite takes 7.20 s. 2026-11-04, P2 item 10: 60 cases added, 0 removed, in `test_no_silent_skips.py` (241 + 60 = 301); the tree before it took 62.18 s by the same clock. 2026-11-06, P2 item 11, G18: 11 cases added from 3 functions in `test_core_graph.py`, 0 removed (301 + 11 = 312); the tree before it, `db0cbd9`, took 69.68 s by the same clock |
| Fast-path drift | `.venv/bin/python -m backend.evals.check_fast_path` | exit 1, `JOB_HUNT` row only (owner runs it; needs `.env`) |
| CI | `.github/workflows/ci.yml` (GitHub, every push and PR) | Run `41816624891` on `p2-no-silent-skips` at `c393e97`: completed with success (owner's `gh run watch`; backend 2 m 54 s, frontend 1 m 13 s; core tests 296 passed, 5 xfailed, 98.72 s by pytest's timer). Lint limit `LINT_MAX: 27`; lower it with the lint row. Added 2026-10-29 |
| Eval suite | `uv run python -m backend.evals.eval --concurrency 1` | `latest_run_metrics.json` at `HEAD`: logic 95.74 (90/94), recall 100. Last written 2026-08-20, `0804bc6`. Re-run 2026-11-01 before and after P2 item 7: 91/94, 34/34, the same 94 verdicts; the file stays at 95.74 (`DECISIONS.md`). Re-run 2026-11-02, two before and one after `OPEN.md` item 15: 91/94, 34/34, the same 94 verdicts; the file stays at 95.74. Re-run 2026-11-02 before and after P2 item 8: 91/94, 34/34, the same 94 verdicts; the file stays at 95.74. Re-run 2026-11-04 before and after P2 item 10: 91/94, 34/34, the same 94 verdicts; the file stays at 95.74. Re-run 2026-11-06 before and after P2 item 11 (G18): 91/94, 34/34, the same 94 verdicts; the after-run was cold for router calls; the file stays at 95.74 |

pytest runs the core tests in `backend/tests/`; no Python linter or type checker
is installed. The root `test_*.py` and `scratch/test_*.py` files are one-off
scripts, not a suite; `testpaths` in `pyproject.toml` keeps pytest out of them.
In the sandbox, pytest needs `--confcutdir=backend/tests`: without it, collection
stats the repo-root `.env` and the sandbox refuses (`PermissionError`).

Lint problems by file and rule (compare the set, not only the count):

| File | Rule | Count |
|---|---|---|
| `next.config.ts` | `@typescript-eslint/no-explicit-any` | 1 |
| `src/app/page.tsx` | `@typescript-eslint/no-explicit-any` | 7 |
| `src/app/page.tsx` | `react-hooks/set-state-in-effect` | 2 |
| `src/app/page.tsx` | `react-hooks/exhaustive-deps` (warning) | 1 |
| `src/components/MessageList.tsx` | `@typescript-eslint/no-explicit-any` | 7 |
| `src/components/Sidebar.tsx` | `@typescript-eslint/no-explicit-any` | 4 |
| `src/hooks/useAudioVisualizer.ts` | `@typescript-eslint/no-explicit-any` | 1 |
| `src/hooks/useAudioVisualizer.ts` | `react-hooks/set-state-in-effect` | 1 |
| `src/hooks/useChatStream.ts` | `@typescript-eslint/no-explicit-any` | 1 |
| `src/types/agent.ts` | `@typescript-eslint/no-explicit-any` | 2 |
