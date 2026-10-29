# Check baseline

Measured 2026-10-24 at `0087b43`, sandbox on. Update this file only in the change
that moves a number, and say why.

| Check | Command | Result |
|---|---|---|
| Frontend lint | `cd frontend && npm run lint` | 27 problems: 26 errors, 1 warning |
| Frontend types | `cd frontend && npx tsc --noEmit` | 0 errors |
| Python syntax | `.venv/bin/python -m compileall -q backend` | exit 0 |
| Core tests | `.venv/bin/python -m pytest --confcutdir=backend/tests backend/tests` (sandbox); `uv run pytest` (owner, CI) | 10 passed, 1 xfailed (the masking bug, kept as a strict expected failure). Added 2026-10-29 |
| Fast-path drift | `.venv/bin/python -m backend.evals.check_fast_path` | exit 1, `JOB_HUNT` row only (owner runs it; needs `.env`) |
| CI | `.github/workflows/ci.yml` (GitHub, every push and PR) | Run `40894313618` on `p2-ci` at `77ff34b`: both jobs green. Lint limit `LINT_MAX: 27`; lower it with the lint row. Added 2026-10-29 |
| Eval suite | `uv run python -m backend.evals.eval --concurrency 1` | `latest_run_metrics.json` at `HEAD`: logic 95.74 (90/94), recall 100. Last written 2026-08-20, `0804bc6`; not re-run today |

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
