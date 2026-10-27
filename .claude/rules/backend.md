---
paths:
  - "backend/**/*.py"
---

# Backend rules

- Prefix debug prints with `🔧 [__DEV__]`, as `backend/core/chat.py` and
  `backend/core/tools/search.py` do.
- **Tracing is set up in one place: `backend/core/config.py:23-44`.** Never add
  a second setup. `app.py` once had one with a `SimpleSpanProcessor`; it ran
  first and won, and each span cost 7.194 s on the caller's thread against a
  closed port. `app.py:8-24` is a comment explaining why.
- Keep `register(batch=True)` (`config.py:40`). With no Phoenix collector
  listening, batch mode keeps failed exports off the request path.
- Phoenix is started by hand; `docker-compose.yml` defines no Phoenix service.
  The collector defaults to `http://localhost:4317` (gRPC).
