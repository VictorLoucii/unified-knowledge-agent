---
name: citation-sweep
description: Re-check every file:line citation in CLAUDE.md, DECISIONS.md, OPEN.md and README.md after a commit changes a tracked file's line count. Use when the user types /citation-sweep, or right after such a commit, before the handback. Read-only: it reports moved citations; it does not edit the records.
---

# Citation sweep

`CLAUDE.md`, `DECISIONS.md`, `OPEN.md` and `README.md` cite source by
`file:line`. A commit that changes a file's line count moves every citation
into that file. The rule, and the evidence for why a plain grep is not enough,
are in the root `CLAUDE.md` under "Core logic rules". This skill is the
procedure only.

**Warning, before step 1: in zsh an unquoted variable does not word-split.**
`R="CLAUDE.md DECISIONS.md OPEN.md README.md"; grep -n 'pat' $R` passes grep one
filename — the whole string — and prints a `No such file or directory` warning
followed by **zeroes**. Read quickly, four zeroes is indistinguishable from a
clean sweep, and zero is the *expected* answer for most forms, so this trap
manufactures the result you are hoping for. Two sessions hit it in the same turn
on 2026-08-22. Always spell the four filenames out in the command.

For every file whose line count the commit changed:

1. **Grep the four records for the filename.** `grep -n "<file>:[0-9]" CLAUDE.md
   DECISIONS.md OPEN.md README.md`. Open each hit and re-check the cited line
   against the file as it is now.
   **Read the path on every hit — a basename is not a file.** That grep for
   `CLAUDE.md` also returns `frontend/CLAUDE.md:1-21`, a 23-line file, twice.
   The prefix is invisible to the pattern, and the instruction above says to
   check the hit against "the file as it is now", which is exactly the question
   the prefix answers. A sweeper who misses it opens root `CLAUDE.md` at 1-21,
   finds the title instead of "## Frontend rules", and **corrects a citation
   that was already right** — a wrong fix, not a missed one. Neither step 4 nor
   step 5 catches this: the citation is not past-tense, and a sweeper who has
   already mis-identified the file has no reason to read the frame. Do not
   anchor the pattern to a path to fix this; that would miss a legitimate bare
   citation written with different spacing. Read the path instead.
2. **Search the bare form separately.** Some citations carry no filename — a
   table cell such as `| :102 |` or prose such as `at :210` (OPEN.md item 9's
   route table and the prose below it are where these hide). Grep for `:[0-9]`
   near the file's name or inside any table whose header names the file. The
   filename grep never finds these.
3. **Check both ends of every range.** A citation such as `file.py:110-130` is
   found by the grep at its start. Re-check the end line as well; an end that
   moved while the start did not slips past otherwise.
4. **Leave past-tense citations to deleted code alone.** A citation that
   describes code as it *was* before a commit is history and is correct as
   written. Do not "fix" it to a line that no longer holds that code.
5. **A block that declares its own commit is also history, even when the code
   still exists.** Read the prose around a table before correcting its numbers.
   `DECISIONS.md` holds two tables written in the same commit, one headed "at
   the commit that records this entry" and one headed "its single home now".
   Only the second could drift, and correcting the first would make its own
   header false. The difference is one word, and step 4 does not cover it —
   step 4 is written as *to deleted code*, and these point at content that
   still exists and has moved.

Report each form searched and the count of hits re-checked, so the handback's
`sweep:` line can name them. Fix a moved citation in the record that holds it;
a correction to a record is an edit with its own reasoning, not part of this
sweep.
