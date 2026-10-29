# backend/core/rate_limit.py
# Rate limit for the routes that spend model credit (REVAMP.md decision 13).
#
# Counters live in memory. That is correct only while the Space runs one
# process: Dockerfile CMD starts uvicorn with no --workers. Every restart
# resets them.
import time
from collections import deque
from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

PER_IP_LIMIT = 10           # requests per client IP
PER_IP_WINDOW_SECONDS = 60  # sliding window
DAILY_LIMIT = 300           # requests per UTC calendar day, all clients together
SWEEP_ABOVE_KEYS = 1000     # drop idle IPs once the table grows past this

RATE_LIMITED_LINE = "This app is getting a lot of requests right now. Please try again in a few minutes."

_per_ip: dict[str, deque] = {}
_daily_date = None
_daily_count = 0


def client_ip(request: Request) -> str:
    """The rightmost X-Forwarded-For entry, else the socket peer.

    HF's proxy appends the caller's IP, so the rightmost entry is the real one;
    the leftmost is whatever the caller sent (REVAMP.md M4). An empty last entry
    falls back to the socket peer, never to an entry further left.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        last = forwarded.split(",")[-1].strip()
        if last:
            return last
    return request.client.host if request.client else "unknown"


def _sweep(now: float) -> None:
    for key in [k for k, q in _per_ip.items() if not q or now - q[-1] >= PER_IP_WINDOW_SECONDS]:
        del _per_ip[key]


def check_rate_limit(request: Request) -> JSONResponse | None:
    """Counts this request. Returns a 429 response when a limit is reached, else None.

    No await between the check and the count, so one event loop needs no lock.
    A request refused per IP does not use up a daily slot.
    """
    global _daily_date, _daily_count
    now = time.monotonic()
    ip = client_ip(request)

    stamps = _per_ip.setdefault(ip, deque())
    while stamps and now - stamps[0] >= PER_IP_WINDOW_SECONDS:
        stamps.popleft()
    if len(stamps) >= PER_IP_LIMIT:
        print(f"🔧 [__DEV__] rate limit | per-IP limit hit for {ip}")
        return JSONResponse(status_code=429, content={"error": RATE_LIMITED_LINE})

    today = datetime.now(timezone.utc).date()
    if today != _daily_date:
        _daily_date, _daily_count = today, 0
    if _daily_count >= DAILY_LIMIT:
        print(f"🔧 [__DEV__] rate limit | daily limit hit ({DAILY_LIMIT})")
        return JSONResponse(status_code=429, content={"error": RATE_LIMITED_LINE})

    stamps.append(now)
    _daily_count += 1
    if len(_per_ip) > SWEEP_ABOVE_KEYS:
        _sweep(now)
    return None
