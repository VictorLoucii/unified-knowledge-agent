---
name: close-out
description: Reconcile CLAUDE.md, DECISIONS.md, OPEN.md and README.md against what actually happened this session, before the user clears the context. Use when the user types /close-out, or says they are about to clear, wrap up, or end the session. It does not write a handover summary — those files carry the state.
---

# Close out

Do not write a summary to paste into a new chat. `CLAUDE.md`, `DECISIONS.md` and
`OPEN.md` already carry the state. Make those files match reality instead.

Run all five checks. Ask the questions in one batch, not one at a time.

## 1. Does README.md still match the measured numbers? (most important)

Read `backend/evals/latest_run_metrics.json`, then the status line in
`README.md`. Print both figures side by side and say plainly whether they agree.
A README claiming a score the metrics file does not support is what started the
session this skill came from. Two traps:

- Every eval run overwrites that file, including a partial `--indices` run. If
  this session ran one, the file may hold a single-case result. Say so instead
  of comparing it.
- Report the three-part breakdown, not the headline. `CLAUDE.md` records that
  the fast-path table answers 53 of the 94 cases and 26 of the 34 recall
  targets. A README quoting only the headline is incomplete — flag it.

## 2. What is uncommitted that should not be?

Run `git status --short`. Name the files that implement this session's work and
are still unstaged. Never run `git add .`. Commit nothing unapproved. Flag
anything large or tracked-but-disposable — a cache, a database, a `.bak`
directory — with its size. `.gitignore` matches `**/chroma_db/`, which does
**not** match `chroma_db.bak/`.

## 3. Are the OPEN.md items still open?

For each numbered item, ask whether this session closed it, advanced it, or left
it alone. Then edit `OPEN.md`: delete what is done, and rewrite the *Already
established* and *Not checked* lines for whatever advanced.

## 4. Was anything decided that DECISIONS.md should record?

Ask. A decision has a rejected alternative. "We rebuilt the index" is not one;
"we kept the backups because recall regressed" is. Record the reason.

## 5. Did any rule change?

Ask whether anything learned belongs in `CLAUDE.md` as a standing rule. Add one
only if it would have changed what you did. Never restate a score in a rule.
