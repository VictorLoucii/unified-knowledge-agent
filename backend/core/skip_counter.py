# backend/core/skip_counter.py
"""Counts the times the app hit a fault and carried on, for /health to report.

See DECISIONS.md, "What counts as a skip, and what the count does not show".

Imports nothing from backend: config.py counts while it is still being imported.
A count lives in this process and restarts with it. Ingestion runs on a thread
while requests run on the event loop, so a lock guards each change.
"""
import threading
import time

KINDS = ("request_skips", "startup_faults", "failed_requests")

_lock = threading.Lock()
_counts = dict.fromkeys(KINDS, 0)
_started_at = time.monotonic()


def count_skip(kind: str) -> None:
    """Adds one to a kind. Never raises: every caller is already handling a fault and must carry on."""
    try:
        with _lock:
            _counts[kind] += 1
    except Exception as e:
        print(f"🚨 count_skip failed: {type(e).__name__}: {e}")


def skip_report() -> dict[str, int]:
    """Numbers only, because /health is public: each kind's count and the seconds this process has run."""
    with _lock:
        report = dict(_counts)
    report["seconds_since_start"] = int(time.monotonic() - _started_at)
    return report
