"""Compare every FAST_PATH_INTERCEPTS entry against the live data/ problem block.

Run from the repo root:
    uv run python -m backend.evals.check_fast_path
Imports backend.core.config so the environment is loaded the way the app loads
it. That import is not free — config.py:14-124 runs load_dotenv, registers
Phoenix tracing, builds three ChatOpenAI clients and loads the all-MiniLM-L6-v2
embedding model — but no model call is made. This script only reads files.

Why the drift matters. semantic_router.py:7-15 serves the stored string when a
table key is a substring of the query, and it runs first. semantic_router.py:18-29
serves extract_problem_block() live when no key matched but the query names a
problem. So one problem can reach a user by two paths, and every difference this
script prints is a difference between what those two paths return.

target_id carries two meanings and only one of them is a copy claim. When it is
truthy, agents.py:87-93 synthesises the ToolMessage that eval.py:47-55 scrapes
and eval.py:143-147 scores for Recall@k, so target_id is a recall label first.
For 20 entries the stored output is also a copy of that problem's block. For 5 it
is a short answer *about* the problem and was never a copy, and the 26th
("JOB_HUNT") has no live block, so nothing establishes it either way. NOT_A_COPY
names that second population; it is not a lenient verdict on the first.

Measured 2026-08-22 at 55fb8e9, one run: 26 of the 53 entries carry a target_id
(25 ints and the string "JOB_HUNT"), pointing at 20 distinct ids. 3 identical,
17 differing only in the header and/or the end marker, 5 not a copy, 1 with no
live block. Exit code 1, caused by "JOB_HUNT" alone.
"""
import re
import sys

from backend.core.fast_path_routes import FAST_PATH_INTERCEPTS
from backend.core.config import extract_problem_block

END_MARKER = "<END OF PROBLEM>"

# Tolerant of the mangled headers the table already stores — '**# Problem 1**4',
# '****# Problem 4**0**', '# Problem 9'. A test that demanded the exact
# '**# Problem N**' form would class three real copies as short answers.
PROBLEM_HEADING = re.compile(r"^[*#\s]*#\s*Problem\b", re.IGNORECASE)

# Only these two mean the repository is wrong. A header or marker difference is
# real drift and is printed, but it can only be repaired inside
# fast_path_routes.py, whose strings 53 evaluation cases return; failing on it
# would make the exit code permanently red and therefore meaningless.
FAILING_VERDICTS = ("BODY_DIFFERS", "NO_LIVE_BLOCK")


def _short_key(key: str, width: int = 56) -> str:
    """Elides the middle, not the tail.

    Seven table keys begin 'Can you provide the complete details and code for
    Problem N?'. A plain key[:52] renders all seven identically, which defeats
    the column.
    """
    if len(key) <= width:
        return key
    head = (width - 3) // 2
    tail = width - 3 - head
    return key[:head] + "..." + key[-tail:]


def _first_line(text: str) -> str:
    return text.split("\n", 1)[0]


def _body(text: str) -> str:
    """The block with its first line and its trailing end marker removed."""
    trimmed = text.rstrip()
    if trimmed.endswith(END_MARKER):
        trimmed = trimmed[: -len(END_MARKER)]
    newline = trimmed.find("\n")
    return trimmed[newline + 1:].strip() if newline != -1 else ""


def classify(stored: str, live: str | None) -> tuple[str, str]:
    """Returns (verdict, action). The action names the file a reader must open."""
    if live is None:
        return "NO_LIVE_BLOCK", "data/: no '# Problem <id>' header exists"
    if stored == live:
        return "IDENTICAL", "nothing"
    # `_body(live)` guards a vacuous equality. config.py:198-200 emits a bare
    # header for a block with no newline, whose body is "" — and every one-line
    # short answer also has a body of "". Without the guard those two collide
    # here and a short answer is reported as a header difference. No such block
    # exists in data/ today (118 headers scanned, 0 header-only), so this cannot
    # fire; it becomes reachable the moment someone commits an empty problem.
    if _body(stored) == _body(live) and (
        _body(live) or PROBLEM_HEADING.match(stored.lstrip())
    ):
        parts = []
        if _first_line(stored) != _first_line(live):
            parts.append("header")
        if not stored.rstrip().endswith(END_MARKER):
            parts.append("marker")
        # The branch is only reached when stored != live, so a difference that is
        # neither the first line nor the marker is whitespace `_body` stripped at
        # :72. Without this fallback the action reads "fast_path_routes.py: " and
        # names a file without naming a repair.
        if not parts:
            parts.append("whitespace")
        return "HEADER_OR_MARKER", "fast_path_routes.py: " + "+".join(parts)
    if not PROBLEM_HEADING.match(stored.lstrip()):
        return "NOT_A_COPY", "nothing - a short answer, never a copy claim"
    return "BODY_DIFFERS", "fast_path_routes.py or data/: bodies disagree"


def main() -> int:
    counts: dict[str, int] = {}
    failing: list[str] = []
    checked = 0

    print(f"Table holds {len(FAST_PATH_INTERCEPTS)} entries. "
          f"Comparing every entry that carries a target_id.\n")
    print(f"{'VERDICT':<16} {'ID':<9} {'STORED':>6} {'LIVE':>6}  "
          f"{'ACTION':<44} KEY")
    print("-" * 132)

    for key, entry in FAST_PATH_INTERCEPTS.items():
        target_id = entry.get("target_id")
        if target_id is None:
            continue
        checked += 1
        stored = entry["output"]
        live = extract_problem_block(str(target_id))
        verdict, action = classify(stored, live)
        counts[verdict] = counts.get(verdict, 0) + 1
        if verdict in FAILING_VERDICTS:
            failing.append(f"{verdict} target_id={target_id!r} key={_short_key(key, 60)!r}")
        print(f"{verdict:<16} {str(target_id):<9} {len(stored):>6} "
              f"{len(live or ''):>6}  {action:<44} {_short_key(key)!r}")

    distinct = len({e["target_id"] for e in FAST_PATH_INTERCEPTS.values()
                    if e.get("target_id") is not None})
    print("-" * 132)
    print(f"\n{checked} entries carry a target_id, pointing at {distinct} "
          f"distinct ids.")
    for verdict in sorted(counts):
        print(f"  {verdict:<16} {counts[verdict]}")
    print(f"  {'TOTAL':<16} {sum(counts.values())}")

    if failing:
        print(f"\nNeeds action ({len(failing)}):")
        for line in failing:
            print(f"  {line}")
        return 1

    print("\nNothing needs action.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
