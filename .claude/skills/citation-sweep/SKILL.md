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

For every file whose line count the commit changed:

1. **Grep the four records for the filename.** `grep -n "<file>:[0-9]" CLAUDE.md
   DECISIONS.md OPEN.md README.md`. Open each hit and re-check the cited line
   against the file as it is now.
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

Report each form searched and the count of hits re-checked, so the handback's
`sweep:` line can name them. Fix a moved citation in the record that holds it;
a correction to a record is an edit with its own reasoning, not part of this
sweep.
