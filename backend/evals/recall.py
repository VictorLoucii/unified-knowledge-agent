# backend/evals/recall.py
"""What counts as a section recall hit. DECISIONS.md, "Recall counts sections, not problem numbers".

A section is {"source_file": <basename>, "headers": {"Header 1": ..., "Header 2": ..., "Header 3": ...}},
with the header strings exactly as ingest.py's splitter writes them into chunk metadata.
A case is a hit when one retrieved section equals one of its target sections: the same
file and the same headers at the same levels. A parent or child section does not count.

No imports from backend.core: eval.py builds the graph and the judge at import, and this
rule is tested without .env.
"""


def section_key(section: dict) -> tuple:
    return (section["source_file"], tuple(sorted(section["headers"].items())))


def is_section_hit(target_sections: list, retrieved_sections: list) -> bool:
    wanted = {section_key(s) for s in target_sections}
    return any(section_key(s) in wanted for s in retrieved_sections)
