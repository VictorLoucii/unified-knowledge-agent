---
paths:
  - "data/**"
  - "backend/core/ingest.py"
  - "backend/core/fast_path_routes.py"
---

# Knowledge base rules (`data/`)

`data/` is the manually curated knowledge base and the single source of truth.
Carried over from `.agents/rules/immutable-knowledge-base.md` and the pre-migration
`CLAUDE.md`; see `.claude/gemini-migration-map.md`.

## Do not edit `data/`, except an approved correction

The default: do not modify, edit or append to any `.md` or `.docx` in `data/`.
Since 2026-08-18 one exception exists. All four conditions must hold:

1. **Propose first, write second.** Show the file, the lines and the replacement
   text. Approval covers that one file, in that session only.
2. **Corrections only.** The note states something no longer true. Style,
   brevity or tone rewrites are not corrections.
3. **No parser hacks, approved or not.** Never inject formatting tags, HTML or
   structural markers (e.g. `**# Problem XYZ**`) to ease chunking or parsing.
4. **Commit `data/` first.** Run `git status data/`. Hand-written notes have
   existed in no commit; commit them before editing.

`.claude/settings.json` puts an `ask` rule on `Edit(/data/**)`, which covers every
file-editing tool.

**Before proposing a `data/` edit, check the fast-path table.** 26 of the 53
entries in `backend/core/fast_path_routes.py` carry a `target_id`; 20 hold a copy
of a `data/` problem block. Run `.venv/bin/python -m backend.evals.check_fast_path`
(it needs `.env`, so the owner runs it). If a table key matches the reader's
query, the user sees the table, not `data/`; fix the Python file. See `OPEN.md`
item 5.

## Fix the pipeline, not the data

If retrieval misses a section, change `backend/core/ingest.py` (chunking),
`backend/core/tools/search.py` (query expansion, reranking, score boosting) or
the expansion prompt. The only `data/` file Claude may change or delete is
`data/.manifest.json`, and only when deliberately re-ingesting. Never commit it:
a tracked manifest once made the Space skip ingestion and serve an empty
database (`DECISIONS.md`, "The Space ingests at startup").

## `data/` is Git LFS

`.gitattributes:8` routes `data/*.md` through LFS, so `git diff` shows a pointer,
not the text. Smudge the committed side first:

```bash
git cat-file -p HEAD:data/<file>.md | git lfs smudge > "$TMPDIR/before.md"
diff -u "$TMPDIR/before.md" data/<file>.md
```

`.github/workflows/sync_to_hub.yml:16` sets `lfs.allowincompletepush true`, so
the HuggingFace mirror can report success while shipping a pointer. After every
`data/` push, fetch the Space's copy and grep it for the new text.

## Ingestion is destructive and does not update

- A `.docx` in `data/` is converted to markdown and the original is deleted.
  Copy it outside `data/` first.
- Ingestion keys on filename only, against `data/.manifest.json`. An edited file
  already in the manifest is never re-read; clearing its entry adds a second
  copy. To pick up edits, rebuild: rename `backend/chroma_db` and
  `backend/docstore` aside (never delete; git holds no backup), empty the
  manifest, then ingest. See `OPEN.md` item 2.
- The deployed Space ships no manifest, so it re-ingests all files on every
  container start (`OPEN.md` item 4).
