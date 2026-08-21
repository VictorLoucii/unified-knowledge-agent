## Frontend rules

- Do not change styles, layout or design unless asked.
- All UI changes must work on mobile, tablet and desktop.
- **Golden rule of hooks.** Declare hooks at the top level of the component
  that consumes their values. Never declare a hook inside a child when the
  parent needs the data.
- This is Next.js, not React Native. `frontend/AGENTS.md` warns that this
  Next.js version has breaking changes against common knowledge — read the
  relevant guide under `node_modules/next/dist/docs/` before writing frontend
  code.
- **`NEXT_PUBLIC_*` is frozen at build time.** `next build` inlines every
  `NEXT_PUBLIC_*` value into the browser bundle, so supplying one at container
  start does nothing at all. Pass it as a Docker build argument instead — see
  `frontend/frontend.Dockerfile` and the `args:` block in `docker-compose.yml`.
  **Confirm it by searching `.next/static` for the value; do not reason about
  it.** Building once with the variable set and once without, then grepping, is
  a few seconds' work and settles the question outright.
  Local development needs none of this: start the backend on port 7860 and the
  fallback the three call sites already hardcode is correct.


@AGENTS.md
