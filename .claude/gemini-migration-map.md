# Gemini → Claude Code migration map

Written 2026-10-24 by following `~/.claude/playbooks/claude-md-setup.md`,
section "Migrating a project from Antigravity/Gemini". This file is the proof
that no rule was lost. Delete it only after the owner confirms it and the
`.agents/rules/` files are retired (playbook step 9).

## Step 1 — sources found

| Source | Rules | Tracked by git |
|---|---|---|
| `.agents/rules/eval-driven-development.md` | 7 (E1–E7) | no (`.gitignore:58`) |
| `.agents/rules/immutable-knowledge-base.md` | 4 (K1–K4) | no |
| `.agents/rules/logic-constraints.md` | 16 (L1–L16) | no |
| `.agents/rules/ui-ux-constraints.md` | 4 (U1–U4) | no |
| `CLAUDE.md` (root, before this migration) | 20 sections (C1–C20), 417 lines | yes |
| `frontend/CLAUDE.md` | 5 rules, already Claude-shaped | yes |
| `frontend/AGENTS.md` | 1 (Next.js docs warning), imported by `frontend/CLAUDE.md` | yes |
| `~/.gemini/config/projects/7de037a9-….json` | 0 rules; permission grants only | n/a |

No `GEMINI.md`, `.gemini/`, root `AGENTS.md` or `~/.gemini/settings.json` exists.

## Step 3 — one home per rule

Homes: **CM** = root `CLAUDE.md` · **KB** = `.claude/rules/knowledge-base.md` ·
**EV** = `.claude/rules/evals.md` · **BE** = `.claude/rules/backend.md` ·
**FE** = `frontend/CLAUDE.md` · **ST** = `.claude/settings.json` ·
**BL** = `.claude/check-baseline.md` · **Drop**.

| # | Rule | Home | Note |
|---|---|---|---|
| E1 | Run the eval before calling AI-logic work done | EV | Command corrected: no `MODEL_NAME`, `--concurrency 1` |
| E2 | Run the eval as a background task (`WaitMsBeforeAsync`) | Drop | Antigravity-only setting; Claude Code has `run_in_background` |
| E3 | Both scores must stay at 100% | EV | Outdated. Replaced by "not below `latest_run_metrics.json` at `HEAD`" (95.74 / 100) |
| E4 | Be surgical with the system prompt | EV | |
| E5 | Change the test when the behaviour should change | EV | |
| E6 | The 5-step EDD loop | EV | |
| E7 | Why ad-hoc prompting is dangerous | Drop | Rationale only; E6 carries the rule |
| K1 | Never edit `data/` | CM + KB + ST | One line in CM; approval-per-file detail in KB; `ask` rule on `Edit(/data/**)` |
| K2 | No parser hacks | KB | |
| K3 | Fix the pipeline, not the data | KB | |
| K4 | Only `data/.manifest.json` may change, only when re-ingesting | KB | |
| L1 | Do not change app logic unless asked | CM | Merged with L4, L14 |
| L2 | Backward compatibility: optional props, default values | FE | Props and hooks are frontend terms |
| L3 | Do not guess; reason only from files read | CM | Merged with L5 |
| L4 | Follow existing structure; no unrelated refactors | CM | |
| L5 | Say so when files cannot confirm an issue | CM | |
| L6 | Debug logs use `__DEV__` | BE | Live convention: 8 prints use `🔧 [__DEV__]` in `chat.py` and `search.py` |
| L7 | Name the exact file and line | CM | |
| L8 | Ask before adding a dependency; check manifests first | CM + ST | `ask` rules for `uv add`, `uv pip install`, `pip install`, `npm install` |
| L9 | Grep every reference before rename or delete | CM | |
| L10 | Never hardcode secrets | CM | Global hook `block_secrets.py` misses OpenRouter keys (see step 8) |
| L11 | Never read `.env`; use `.env.example` | CM + ST | `Read`/`Edit` deny + sandbox |
| L12 | Never leave a catch block empty | CM | No Python linter is installed to enforce it |
| L13 | Components under ~450 lines; logic in hooks | FE | |
| L14 | Non-destructive editing | CM | |
| L15 | Compile/lint before calling work done | CM + BL | Lint is red today; BL holds the counts |
| L16 | Git hygiene: no `git add .`; review the diff | CM + ST | Deny rules, reordered forms included |
| U1 | Do not change styles or layout unless asked | FE | Already there |
| U2 | UI debug logs use `__DEV__` | Drop | No frontend file uses it; L6 covers the backend use |
| U3 | Responsive on mobile, tablet, desktop | FE | Already there |
| U4 | Hooks at the top level of the consuming component | FE | Already there |
| C1 | Fast-path table answers 53 of 94 cases; report 41-case and 8-case figures | EV | |
| C2 | EDD rules 1–5 | EV | Same as E1–E6 |
| C3 | `MODEL_NAME` swaps the judge; migrate in source; `fast_llm` ≠ `gemini-3.5-flash-lite` | EV | |
| C4 | `--concurrency 10` segfaults on this Mac | CM + EV | Moved into the command itself |
| C5 | Back up `latest_run_metrics.json` before a partial run | EV | |
| C6 | Fast run = warm cache; cache is never invalidated | EV | Runtime history (27 s vs 230 s) dropped; it is in git history |
| C7 | Judge noise; rate limits present as fails | EV | |
| C8 | `data/` correction exception, approved per file | KB | |
| C9 | Check the fast-path table before proposing a `data/` edit | KB | |
| C10 | Any push restarts the Space and re-ingests (~8 min) | CM | |
| C11 | `data/` is Git LFS; `allowincompletepush` | KB | |
| C12 | Never commit `data/.manifest.json` | KB | `.gitignore` enforces; one line kept for the reason |
| C13 | Ingestion is destructive and keys on filename | KB | |
| C14 | Core logic rules | CM | Same as L1–L16 |
| C15 | A line-count change invalidates citations; run `/citation-sweep` | CM | |
| C16 | Evidence must sit at the same level as its claim | CM | |
| C17 | Never run `git filter-repo` here | CM + ST | Deny rule |
| C18 | Secrets | CM + ST | Same as L10, L11 |
| C19 | Commands (port 7860, compose, eval) | CM | |
| C20 | Tracing: instrument only in `config.py`; keep `batch=True` | BE | |

## Step 4 — reuse from other projects

Source: the JobHunt migration of 2026-10-24, which scouted 5 projects. Checks:
earned · needed here · current · not covered globally.

| Candidate | E | N | C | G | Result |
|---|---|---|---|---|---|
| Dated check baseline file | ✓ JobHunt red checks | ✓ lint red, 27 problems | ✓ | ✓ | Taken → BL |
| "Keep every check current" | ✓ Shepherd-Care | ✓ `check_fast_path.py`, `qa_dataset.json` | ✓ | ✓ | Adapted into E5 wording in CM |
| Reordered `git add` / `git commit -a` deny forms | ✓ JobHunt probes | ✓ local list lacks them | ✓ | partly (autoMode hard_deny is a classifier, not a rule) | Taken → ST |
| `ask` on package installs | ✓ L8 | ✓ | ✓ | ✓ | Taken → ST |
| Sandbox, strict mode | ✓ JobHunt pytest read `.env` | ✓ eval and app read `.env` | ✓ | ✓ | Taken → ST |
| Machine traps pointer | ✓ | ✓ zsh `===` hit this session | ✓ | ✓ | Taken → CM, pointer only |
| `HANDOFF.md` for current state | ✓ | ✗ `OPEN.md` already holds open work | ✓ | ✓ | Rejected |
| `attribution` setting | ✓ | ✓ | ✓ | ✗ set in `~/.claude/settings.json` | Rejected |
| Notification rule | ✓ | ✓ | ✓ | ✗ global `CLAUDE.md` | Rejected |

## Step 8 — probes, 2026-10-24

| Probe | Result |
|---|---|
| `wc -c < .env` in the shell | Blocked: `operation not permitted` (sandbox) |
| `.env.example` read | Through, as intended |
| Sandbox read-deny list at session start | Lists the repo's `.env` |
| App code loading `.env` (`check_fast_path`) | Blocked: `PermissionError` — so the owner runs it |
| Git history, names only | Only `.env.example`; no secret file was ever committed |
| `git add --dry-run -A` | Blocked (deny rule) |
| `git -C . add --dry-run .` | Blocked (deny rule) |
| `git commit --dry-run -a` | Blocked (deny rule) |
| `git push --dry-run origin main --force` | Blocked (global guard) |
| `allowUnsandboxedCommands` | `false` in the file |
| Python `open()`, symlink, `cp` on the real `.env` | Not run: the auto-mode classifier refused the probe |
| Read/Grep tools and shell routes in a decoy repo with a canary | Not run: the fresh `claude -p` session refused the probe |
| Global hook `block_secrets.py:16` vs OpenRouter keys | **Gap, reported to owner.** `sk-[A-Za-z0-9]{32,}` cannot match `sk-or-v1-…` |
| `Write(...)` permission rules | Removed: Claude Code warned they match nothing; `Edit(...)` covers all edit tools |
