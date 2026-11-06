# backend/evals/check_section_labels.py
"""Checks the section recall labels against data/. Run: .venv/bin/python -m backend.evals.check_section_labels

Each label (target_sections in qa_dataset.json and in FAST_PATH_INTERCEPTS) must name a
section that ingest.py's splitter produces from data/ today. A label that names no section
can never be a hit, so the section recall would fall with no change in retrieval. Edit
data/ and this check shows which labels to rebuild. DECISIONS.md, "Recall counts sections,
not problem numbers", says how the labels were built.

It also checks that every case with a target_problem_id, and every table entry with a
target_id, carries a label, and it names each label path that occurs more than once in its
file: a chunk from the other place would count as a hit too.

Needs data/ with its Git LFS content; it needs no .env and makes no network call.
Exit 0: every label resolves. Exit 1: a label is missing or names no section.
Exit 2: data/ holds LFS pointer files, not the notes.
"""
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

from langchain_text_splitters import MarkdownHeaderTextSplitter

from backend.core.fast_path_routes import FAST_PATH_INTERCEPTS
from backend.evals.recall import section_key

REPO = Path(__file__).parents[2]
DATA = REPO / "data"
LEVELS = ("Header 1", "Header 2", "Header 3")

# A copy of the preprocessing in ingest.py, in order. test_recall_labels.py checks that it
# still matches ingest.py's source, so a change there fails a test instead of this check.
INGEST_SUBS = (
    (r'!\[.*?\]\(.*?\)(\{.*?\})?', ''),
    (r'(?m)^\s*\\#\\#\\#\s', '### '),
    (r'(?m)^\s*\\#\\#\s', '## '),
    (r'(?m)^\s*\\#\s', '# '),
)
HEADERS_TO_SPLIT_ON = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]


def preprocess(text: str) -> str:
    for pattern, replacement in INGEST_SUBS:
        text = re.sub(pattern, replacement, text)
    return text


def section_keys(name: str, text: str) -> list:
    """The recall key (recall.section_key) of every section the splitter makes from one file."""
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
    return [section_key({"source_file": name, "headers": {k: d.metadata[k] for k in LEVELS if k in d.metadata}})
            for d in splitter.split_text(preprocess(text))]


def labelled_rows() -> list:
    """(row name, old id, label or None) for every row that carries an old id."""
    with open(REPO / "backend/evals/qa_dataset.json", encoding="utf-8") as f:
        dataset = json.load(f)
    rows = [(f"case {n}", c["target_problem_id"], c.get("target_sections"))
            for n, c in enumerate(dataset, 1) if c.get("target_problem_id") is not None]
    rows += [(f"entry {key[:50]!r}", e["target_id"], e.get("target_sections"))
             for key, e in FAST_PATH_INTERCEPTS.items() if e.get("target_id") is not None]
    return rows


def main() -> int:
    paths = {}
    for name in sorted(os.listdir(DATA)):
        if name.endswith(".md"):
            text = (DATA / name).read_text(encoding="utf-8")
            if text.startswith("version https://git-lfs"):
                print(f"data/{name} is a Git LFS pointer. Fetch the notes (git lfs pull) and run again.")
                return 2
            paths[name] = Counter(section_keys(name, text))

    rows = labelled_rows()
    failing, repeated, checked = [], set(), 0
    for row, old_id, label in rows:
        if not label:
            failing.append(f"{row} (old id {old_id!r}): no target_sections")
            continue
        for section in label:
            checked += 1
            # The same key as the hit rule, so a header name outside LEVELS cannot pass here and miss there.
            unknown = set(section["headers"]) - set(LEVELS)
            count = paths.get(section["source_file"], Counter())[section_key(section)]
            if unknown:
                failing.append(f"{row}: header names not written by ingest: {sorted(unknown)}")
            elif count == 0:
                failing.append(f"{row}: no such section: {section['source_file']} :: {section['headers']}")
            elif count > 1:
                repeated.add(f"{section['source_file']} :: {section['headers']} occurs {count} times")

    print(f"{len(rows)} labelled rows, {checked} section paths checked against "
          f"{sum(sum(c.values()) for c in paths.values())} sections in {len(paths)} files.")
    for line in sorted(repeated):
        print(f"REPEATED  {line}")
    for line in failing:
        print(f"FAIL      {line}")
    print("PASS" if not failing else f"{len(failing)} failing")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
