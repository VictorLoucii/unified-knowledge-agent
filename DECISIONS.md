# Decisions

One entry per real decision: what was chosen, what was rejected, and why the
rejected option lost. The point is to stop a future session from quietly
undoing something deliberate.

Open work is in [OPEN.md](OPEN.md).

---

## Model and provider

### Gemini 2.5 Flash as the unified driver — SUPERSEDED 2026-08-22, see the next entry

**Chosen:** `google/gemini-2.5-flash` via OpenRouter for the agent, the query
expansion and the fallback model.

**Rejected:** DeepSeek V3 as the primary driver.

**Why:** DeepSeek V3 emits text before it emits its tool call. The frontend's
human-in-the-loop approval panel keys off the pause that precedes a tool call,
so that leading text breaks the handshake and the user sees the agent talking
about an action it has not been approved for. DeepSeek is still usable for
evaluation by setting `MODEL_NAME`, but not as the driver.

### GPT-5 Mini drives, Gemini 3.6 Flash routes and falls back, Flash Lite only expands

**Chosen (2026-08-22, `2c06890`):** `openai/gpt-5-mini` with
`reasoning_effort="low"` for `primary_llm` (`config.py:49`);
`google/gemini-3.6-flash` for `fallback_llm` (`config.py:60`) and `fast_llm`
(`config.py:70`); `google/gemini-3.5-flash-lite` for `expansion_llm`
(`search.py:16`) only. The judge at `eval.py:67` is unchanged.

**Rejected:** `google/gemini-3.6-flash` as the driver; `gemini-3.5-flash-lite`
as `fast_llm`; `reasoning_effort` of `minimal` or `medium`.

**Why.** Google closed `gemini-2.5-flash` to new users, and every request-path
string named it (OPEN.md item 8). A 12-call streaming probe with the real tools
bound and the real `qa_node` prompt showed that neither GPT-5 Mini nor 3.6 Flash
emits text before its tool call, so the approval-panel constraint above holds
for both. GPT-5 Mini won on the rest: 0.18% tool-call error against 1.77% on
the provider pages, listed $0.25/$2.00 against $0.75/$3.75 per 1M, 3.5 s
against 11 s to the first tool call in the probe (one sample each), and a
separate $3.80 OpenAI balance that pays for the eval through BYOK. `minimal`
effort chose the search tool for a weather question; `low` chose the weather
tool and spent about 60 reasoning tokens.

**Flash Lite is rejected as `fast_llm` by measurement, not by taste.** The scope
router at `agents.py:40-52` runs on `fast_llm`. With Lite it answered
`OUT_OF_SCOPE` for tests 46, 58, 59, 60, 93 and `CONVERSATIONAL` for test 42;
2.5 Flash and 3.6 Flash both answer `IN_SCOPE` on all six. Those cases then
never reached `qa_node`, called no tool, and scored 87/94 and 33/34. Raising
GPT-5 Mini to `medium` changed nothing, because the primary was never called.
With `fast_llm` on 3.6 Flash the suite returned 90/94 and 34/34, identical to
the committed baseline, with 38/41 and 8/8 on the genuinely exercised cases.
Lite stays on `expansion_llm` because all 26 cases that reached the search tool
hit their target with it.

**Why `low` and not `minimal`:** the weather probe above. **Why not `medium`:**
no tool-choice difference on 14 cases, more tokens and latency.

**Also rejected, the same day:** strengthening the `qa_node` prompt with "even
when you already know the answer from general knowledge" and "never answer a
technical question without it". Probed on five queries: the four failing Python
questions already called the search tool under the unchanged prompt, and the
addition pushed the *weather* query to the search tool. The prompt was left as
it is. Whoever fixes the weather wording later (OPEN.md item 11) starts from
that result, not from zero.

### OpenRouter stays, and cannot be replaced by a Claude Code subscription

**Chosen:** one OpenRouter key and one endpoint for every model call.

**Rejected:** routing the app's model calls through a Claude Code Max plan.

**Why:** three independent reasons. The Max plan authenticates a local CLI, not
an HTTP endpoint, so there is no value that can go in `openai_api_base`. The
backend runs in a container and is force-pushed to a public HuggingFace Space,
and that container cannot hold a CLI login. And the code depends on
`bind_tools`, `astream_events`, `with_structured_output` and `with_fallbacks`,
all four of which a wrapper would have to reimplement. Embeddings run locally
(`all-MiniLM-L6-v2`) and Chroma is a local directory, so OpenRouter is the only
paid dependency and there is no second bill to consolidate.

---

## Retrieval

### Header re-prepending at ingestion, not metadata filtering

**Chosen:** `ingest.py` prepends the parent header hierarchy to the text of
every child chunk before embedding.

**Rejected:** relying on ChromaDB metadata to carry the header context.

**Why:** Chroma strips structural context from the embedded text, so a chunk
that reads "the fix was to add flexDirection: row" loses all trace of which
problem it belongs to. Putting `# Problem 12` into `page_content` makes the id
both searchable and recoverable — the recall marker in `search.py` is derived
by reading the header back out of retrieved chunks. This is why recall works at
all, and it is why `search.py:240` can de-duplicate by exact `page_content`.

### Keyword-style query expansion, not natural-language sentences

**Chosen:** the expansion model produces 3 short keyword queries of 1–5 words.

**Rejected:** 3 full descriptive sentences; also rejected a mixed prompt asking
for two keyword queries plus one sentence.

**Why:** isolated by ablation, each change tested alone with `--indices 5,83`.
The sentence style caused index 83 to return ten chunks from a single wrong
file with negative cross-encoder scores; the keyword style surfaced the right
file immediately. The mixed prompt was tested for one cycle and scored 0/4 —
one sentence among three queries was enough to pull retrieval back off target.

**The cost, recorded honestly:** this trades one failure for two fixes. Indices
5 and 83 pass; index 37 regressed and now answers the LangGraph recursion limit
from general knowledge. Net logic is flat at 90/94, and the entire gain is on
recall, 33/34 → 34/34, which is what opens the suite's gate.

**Update, 2026-08-18 — that trade has since reversed.** The index rebuild
swapped the pair back: index 37 now passes and index 83 now misses. Recall
returned to 33/34. The decision above still stands — keyword expansion beat
sentences on its own merits — but the two cases were never independent. They
compete for slots in one candidate pool that `search.py:390` truncates *before*
`search.py:410` reranks it, so whichever change lands last decides the winner.
That mechanism, not the expansion style, is the thing to fix. See
[OPEN.md](OPEN.md) item 1.

**Update, 2026-08-20 — the mechanism named in the paragraph above was refuted,
and index 83 is fixed.** Measuring the candidate pool showed that the document
index 83 needs never enters it, so truncation order was never what excluded it.
The fix was the docstring directive at `search.py:38-44`, not a change to the
pool. Recall is 34/34 again and net logic is again flat at 90/94, because 37 and
83 traded once more — this time with the judge's own reasons captured on both
sides, which is what identifies 37 as judge variance rather than retrieval.
**The observation that the two trade has survived; every explanation offered for
it so far has not.** See [OPEN.md](OPEN.md) item 1.

**Also ruled out in the same investigation:** the header relevance boost, which
was changed from +200 to +30. Tested on its own, restoring it to 200 fixed
neither failing case. It stays at 30.

### The tool docstring demands the user's whole question, not a keyword fragment

**Chosen, 2026-08-20:** `search.py:38-44` instructs the model to pass the user's
question word for word, and keeps the Problem ID and ordinal examples verbatim
inside the generalised rule.

**Rejected:** a third hardcoded query injection at `search.py:86-93`. Two
already exist there, so a `Community Type` entry would have passed index 83 and
would have matched precedent. It would have moved the score without improving
the pipeline, which is the failure `CLAUDE.md`'s opening section exists to
prevent.

**Why the examples had to survive the generalisation.** They are load-bearing in
a way their old wording did not advertise. `search.py:62` matches the problem
regex against the query and skips expansion entirely on a hit, and
`search.py:120-121` tests the four literal strings `"first problem"`,
`"oldest problem"`, `"last problem"` and `"latest problem"` as substrings. A
paraphrase that dropped those phrases would silently re-enable expansion for the
queries the original directive existed to protect, and would break the ordinal
interceptor outright.

**What is *not* claimed.** Measured on three cases at HEAD before the change,
the model already passed the user's whole question verbatim for two of them.
So the docstring being keyword-shaped is **not** established as the cause of the
shortening, and why an explicit directive changed the remaining case is a
hypothesis. See [OPEN.md](OPEN.md) item 1.

### The query cap is 1,000, matching the input guardrail

**Chosen, 2026-08-20:** `search.py:50-58` caps the query at 1,000 characters and
prints a `✂️` line when the cut fires.

**Rejected:** keeping the previous cap of 150 and adding only the log line; and
picking a new number on judgement.

**Why 1,000.** `guardrails.py:13` already refuses any user message longer than
that, so the cap imports a bound the product enforces instead of inventing one.
The caveat travels with it: that guard runs on the `chat.py` path only, and
`eval.py` invokes the compiled graph directly, so on the suite's path this line
is the only bound there is.

**Why it was decided inside the same change.** A docstring demanding the whole
question would have promised exactly what a 150-character cut quietly undid, and
nothing logged the cut, so the failure would have been silent at both ends.

**The suite cannot measure it.** No query reaching the tool exceeds 144
characters, and the only two dataset queries over 150 are fast-path intercepted.
The change was made for real users, not for the test.

---

## Routing

### The deterministic fast-path table runs before the classifying model

**Chosen:** `route_input_node` consults `FAST_PATH_INTERCEPTS` first and
returns immediately on a hit. The scope-classifying model call happens only if
the table misses.

**Rejected:** the previous order, model call first.

**Why:** with the classifier first, a model call could return `CONVERSATIONAL`
and exit before the table was ever consulted, so one model call could override
53 exact-match answers. That cost two cases outright — one lost its stored
answer, the other also lost its recall marker, because the conversational node
emits no `ToolMessage` for the evaluation to read. A deterministic exact match
should never be overridable by a probabilistic one. Skipping the classifier on
a hit also removes one model call per intercepted query on every run.

### `OUT_OF_SCOPE` takes precedence in the router prompt

**Chosen:** numbered rules, `OUT_OF_SCOPE` first, with an explicit clause
saying it overrides everything below it including requests to write code.

**Rejected:** reverting the prompt to its pre-weather form.

**Why:** the weather and AQI rule is needed for the new tool, so a revert was
not available. The defect was ordering: `OUT_OF_SCOPE` sat third behind two
rules pushing toward `IN_SCOPE`, and the refusal stopped firing for a LinkedIn
scraping request. Verified by running both prompts against the six
out-of-scope cases before spending an evaluation cycle.

---

## Deployment

### The Space ingests at startup; the index is not shipped

**Chosen (2026-08-18):** stop tracking `data/.manifest.json`, so a git clone
arrives with no manifest and the container ingests all 26 files at startup.

**Rejected:** shipping `backend/chroma_db` and `backend/docstore` through the
LFS rules that already sit unused at `.gitattributes:4-6`.

**Why:** three reasons, in order of weight.

1. **The startup cost is already absorbed.** `app.py:74-76` runs
   `initialize_rag` in a background thread precisely so HuggingFace health
   checks pass instantly — the comment there says so. The ingest never blocks
   the port bind, and the Space does answer from the first second.

   **Corrected 2026-08-19 — "only briefly" was wrong, by more than an order of
   magnitude.** This reason originally read "only retrieval is cold, and only
   briefly", reasoning from the 97-second local ingest in `OPEN.md` item 2. The
   Space's measured ingest is **roughly twenty minutes**, about 15 chunks per
   second against 185 locally. The reason still holds — the startup cost is
   absorbed and the port binds immediately — but the cold window is twenty
   minutes, not seconds. See `OPEN.md` item 4, "The Space reports healthy while
   its knowledge base is still loading".
2. **A shipped index goes stale silently.** Ingestion keys on filename, so an
   edited `data/` file is never re-read (`OPEN.md` item 2). A committed index
   would drift from the source of truth with nothing to signal it, and fixing
   that drift would mean a ~146 MB commit each time.
3. **It adds nothing to the repository.** The rejected route costs about
   146 MB of LFS — `chroma_db` 111 MB, `docstore` 35 MB — against a project
   whose history was rewritten a day earlier specifically to remove a 12 MB
   blob. Whether HuggingFace would even accept that much was never verified.

**What made the chosen route safe to pick.** `data/*.md` are LFS-tracked
(`.gitattributes:8`), so startup ingestion would read 130-byte pointers rather
than notes if the objects were missing — and `sync_to_hub.yml:16` sets
`lfs.allowincompletepush true`, which lets a push succeed when LFS uploads
fail. Checked directly rather than assumed: HuggingFace serves 25,990 bytes of
real markdown for `AgenticAI_Interview_Questions_Coding.md`. The content is
there.

**Consequence:** the LFS rules at `.gitattributes:4-6` are now permanently
dead, since `.gitignore:21` cancels them and always will. Local behaviour is
unchanged — `data/.manifest.json` still exists on disk, so a local Docker build
still copies both the manifest and the working-tree index, and still takes the
early return. Only clones behave differently.

**Confirmed live the same day, commit `003496a`.** The Space rebuilt in about
three minutes and `/health` then reported `rag_hydrated: true` on eight
consecutive polls over five and a half minutes. That flag tests whether the
docstore holds any key (`app.py:110`), and an empty docstore was the entire
bug. It cost no OpenRouter credit. Two assumptions became facts: the
sentence-transformer models do resolve inside the Space, and the background
ingestion thread does keep the app answering while it runs.

**One fact found afterwards that strengthens the choice:** the Space reports
`storage: None`. There is no persistent disk, so an index could never survive a
restart there even if one were shipped. The rejected route would have paid
146 MB for something the platform discards.

**Still unverified, and recorded as such in [OPEN.md](OPEN.md) item 4:** the
model download time, and whether all 26 files complete rather than merely
start — `rag_hydrated` proves "at least one document", and nothing exposes a
count.

### `/health` reports ingestion as four states, not a finished boolean

**Chosen (2026-08-21):** `/health` gains one key, `ingestion_state`, taking the
string values `not_started`, `running`, `done` or `failed`. `rag_hydrated` keeps
its exact former meaning and is still computed at `app.py:110`. The key is
purely additive; nothing already in the response changed.

**Rejected: a boolean `ingestion_finished`.** Its case was not weak. One key, one
meaning, no vocabulary a caller must string-match against and no value anyone
can later rename. It is also exactly what the two exits named in the task can
honestly express.

**What refuted it was reading the function, not preferring richness.**
`initialize_rag` had **three** exits, not two. `get_data_file_paths()` raises
`FileNotFoundError`, which the function caught, printed and returned from. That
is a **failure**: nothing was ingested and nothing ever will be for that process.
A boolean has one word for it and that word is `true`, so the boolean would have
reported a dead ingestion as a finished one. A fourth path — an exception
escaping the body — was worse still: `app.py` launches the work with
`asyncio.create_task(asyncio.to_thread(initialize_rag))` and keeps no reference,
so the exception lands on a Task nobody retrieves and both named exits are
skipped. A flag written only at those two points stays at its pre-completion
value for the life of the process.

**Argued from what a caller does, which is the test that settled it:**

| Value | What a caller does |
|---|---|
| `not_started` | keeps waiting — and if it never changes, the task was never dispatched |
| `running` | keeps waiting |
| `done` | stops waiting |
| `failed` | stops waiting **and reports an error** |

`failed` is the value that changes caller behaviour most, and it is the one the
boolean cannot express. Without it a caller polls forever against a container
where ingestion died — the same silent-failure shape as the bug in
[OPEN.md](OPEN.md) item 4, moved one layer out.

**Two implementation choices that follow from the decision, not from taste.**

1. **A getter, not an exported name.** `app.py` calls `get_ingestion_state()`.
   `from backend.core.ingest import _ingestion_state` would bind the string at
   import time and never see an update, which would have shipped a key frozen at
   `not_started` for ever.
2. **A thin public wrapper over the existing body.** `initialize_rag` keeps its
   name — `app.py` and several records cite it — and now sets `running`, calls
   the unchanged body as `_run_ingestion`, and catches `Exception` to report
   `failed`. Wrapping avoided re-indenting roughly 130 unchanged lines, which
   would have moved every citation into the file for no reason.

**What this does not do.** It does not gate any route on completion, and it does
not count documents. `ingestion_state: "done"` means the ingestion function
returned, not that all 26 files are present. Both remain open in
[OPEN.md](OPEN.md) item 4.

### Local development is documented on 7860, and the port is not ours to pick

**Chosen (2026-08-19):** move `README.md` and `CLAUDE.md` to
`uvicorn ... --port 7860`, rather than move the frontend's fallback to 8000.

**Rejected:** changing `http://localhost:7860` to `http://localhost:8000` in
`frontend/src/app/page.tsx`, `frontend/src/components/ChatInput.tsx` and
`frontend/src/hooks/useChatStream.ts`.

**Why.** 7860 is a platform constraint, not a preference. The user's own note at
`data/Errors_in_AgenticAI_Projects.md:1745` records a HuggingFace **deployment
restart loop** caused by a port mismatch, because Spaces expect traffic on 7860;
`:1674` records the resolution as "Standardized all infrastructure on port
7860", and `:1760` records the `localhost:7860` frontend fallback as a
deliberate choice for local development. The container must therefore bind 7860
whatever the documentation says, so moving the frontend to 8000 would have
recreated the split rather than closed it.

The code already agreed with the note in five places — `Dockerfile:30` and
`:33`, `README.md:7`'s `app_port: 7860`, `backend/app.py:270`, and the three
call sites above. **8000 appears in no Python or TypeScript source file
anywhere in the repository**; grepped repo-wide, the only source hits are
`search.py:481` and `:483`, which truncate a text block at 8000 *characters*.
`README.md`'s `--port 8000` was the single line out of step.

**What the choice buys.** On 7860 local development needs no configuration at
all: the fallback already points there, so a fresh clone works with no
`.env.local` and no environment variable. A fix that instructed users to create
`.env.local` could never have reached a clone anyway — `.gitignore:15` and `:40`
exclude it.

**The consequence to leave alone.** Local `uvicorn` serves `localhost:7860`
while Compose serves `localhost:8000`, because `docker-compose.yml:31` maps host
8000 to container 7860. Only the *host* side differs; the container side is what
was standardised. Keeping them distinct also lets the local server and the
Compose stack run at the same time without colliding on a port. `README.md`
carries an `[!IMPORTANT]` block saying so, because two different local URLs look
exactly like the defect that was just fixed.

**Confirmed by running it, 2026-08-19.** With the backend on 7860 and
`npm run dev` alongside it, a query put through the browser returned
`GET /history 200`, an `OPTIONS /chat_stream 200` preflight and
`POST /chat_stream 200`; the answer rendered and the thread persisted to the
history sidebar. A matching port was never sufficient on its own, and this shows
the two halves actually talk. *Provenance: terminal output pasted by the user
and read, not re-run inside a session.* The **compose** path remains unrun — see
[OPEN.md](OPEN.md) item 6.

---

---

## Guardrails and observability

### The general-knowledge fallback stays, disclaimer and all

**Chosen:** when retrieval does not answer the question, the agent may answer
from general knowledge, but must prefix the exact disclaimer defined in
`agents.py`.

**Rejected:** forbidding the fallback so the agent always refuses instead.

**Why:** index 37 is the case for keeping it. Retrieval failed, the agent fell
back, and it correctly prefixed the disclaimer — the cached answer begins "I
couldn't find anything related to this query in my internal knowledge base".
Without the fallback that case would have returned confident wrong facts with
no warning. The mechanism converted a silent failure into a visible one, and
the evaluation still fails the case, which is correct because the right answer
was in the knowledge base. Keep the feature; fix the retrieval.

### The scope router keeps failing open; only its silence was fixed

**Chosen (2026-08-18):** `agents.py:54` logs the exception and still falls
through to `retrieval_node`. Behaviour is unchanged.

**Rejected — failing closed.** Refusing the query when the router model is
unavailable would refuse legitimate questions during any outage, which is a
worse product than answering an out-of-scope one.

**Rejected — leaving the empty `except Exception: pass`.** It broke CLAUDE.md's
rule against empty catch blocks, and its real cost was that nothing in the
container log recorded that the guardrail had been skipped.

**Why this needed a decision at all:** when `fast_llm` fails at `agents.py:41`,
the fall-through skips the `OUT_OF_SCOPE` branch at `agents.py:50-51`. The
refusal recorded above under "OUT_OF_SCOPE takes precedence in the router
prompt" therefore stops firing. That guardrail was fixed deliberately once
already, so a future session finding this fall-through should know it was seen
and left, not missed. The exposure is written up as [OPEN.md](OPEN.md) item 7.

**Not decided:** whether to give `fast_llm` a fallback. It has none —
`config.py:78` wraps only `primary_llm`.

### Arize Phoenix over LangSmith

**Chosen:** a self-hosted Phoenix collector run locally, with LangSmith
environment variables actively popped at import.

**Corrected 2026-08-19.** This entry said "via docker compose". It is not.
`docker-compose.yml` defines only `backend` and `frontend` plus a commented-out
postgres — read, whole file. Phoenix is started by hand with the `docker run`
command recorded in `data/Unified_Knowledge_Project_Details.md` at :1408, which
publishes both 6006 and 4317. `CLAUDE.md` was corrected on 2026-08-18 and this
file was missed.

**Rejected:** LangSmith.

**Why:** Phoenix runs locally with no external API dependency and no cost, and
this is a portfolio project where an ongoing bill for tracing is not
justifiable.

### `batch=True` is a requirement, not a tuning knob

**Chosen:** `register(batch=True)` in `config.py`.

**Rejected:** the library default, `batch=False`.

**Why:** the default installs a `SimpleSpanProcessor`, which exports every span
synchronously on the thread that produced it. With no collector listening,
every export blocks on a failed connection and the caller waits. Measured: the
94-case suite ran in 1058 s with the default and 24 s with batching, and the
failed-export lines in the two logs went from 2,489 to 8. This is a production
defect, not a test-speed one — the backend imports `config.py`, and nothing
listens on the collector port inside the deployed container, so every live user
request was paying for it. **Do not change this back.**

### One tracing setup only, and it lives in `config.py`

**Chosen (2026-08-18):** delete the OpenTelemetry block that stood at
`app.py:7-16` and let `config.py:23-44` be the only instrumentation. A comment
now occupies those lines explaining why nothing may go back there.

**Rejected — keeping both and making `app.py`'s processor a batch one.** It
leaves two setups to drift apart, which is how this defect appeared.

**Rejected — recording it in `OPEN.md` and leaving the code alone.** Every
deployed request kept paying for it.

**Why `app.py`'s block was the live one, read rather than inferred from logs.**
`app.py:16` ran at module level. `app.py:18` then imported `ingest`, and
`ingest.py:21` imports `config`, which is what reached `config.py:41`. So
`app.py` always instrumented first and `config.py` was always the one refused
with "Attempting to instrument while already instrumented". The
`BatchSpanProcessor` that `config.py` installs therefore never received a
single LangChain span.

**The cost, measured.** A `SimpleSpanProcessor` exports on the thread that
ended the span. Reproducing `app.py:13-15` exactly against a closed port — the
deployed container's condition, since nothing listens there:

| Processor | 3 spans | Per span, on the caller's thread |
|---|---|---|
| `SimpleSpanProcessor` | 21.581 s | **7.194 s** |
| `BatchSpanProcessor` | 0.000 s | ~0 |

That matches the retry backoff in the container log, 1.17 + 1.96 + 4.77 s. A
production log showed 23 such cycles for one startup and one question.

**Why deleting it leaves no gap, read from the installed package.**

- `phoenix/config.py:2828` defines `GRPC_PORT = 4317`, so `config.py:31`'s
  endpoint is the correct gRPC port and not a guess.
- `otel.py:691-694` infers the gRPC exporter when the URL has no path and the
  port matches. `http://localhost:4317` satisfies both.
- `otel.py:291-294` removes the constructor's default `SimpleSpanProcessor`
  when another processor is added, so `register(batch=True)` really is
  batch-only.
- `otel.py:180-181` shows `register()` sets the global tracer provider by
  default, which `config.py:40` never overrides. The global provider was
  already Phoenix's.

**The one cost accepted:** local tracing moves from HTTP on 6006 to gRPC on
4317. Whether a locally-run Phoenix binds 4317 was **not** verified — the
figures above are the client-side default. Check the Phoenix startup banner.

**The knowledge-base document that contradicted the code is now corrected.**
`data/Unified_Knowledge_Project_Details.md` presented the deleted block as the
way to instrument the backend. When this entry was written, `data/` was never
edited, so it was recorded in [OPEN.md](OPEN.md) item 5 instead.

**Superseded 2026-08-19, commit `5103325`.** The `data/` correction exception
added on 2026-08-18 allows an approved, per-file fix, and one was approved.
Lines **1344-1368** were replaced. **The range this entry gave, `1342-1364`, was
wrong twice over:** the fence closes at :1368, and the stale text started at
:1344, not at the fence. Both are corrected in OPEN.md item 5.

**Confirmed live.** The Space rebuilt seven minutes after the commit and its
startup log showed the batch processor, the 4317 gRPC endpoint, and no
"already instrumented" line. Ask the agent how tracing works and it now
describes `config.py`.

### A `data/` correction carries its reasoning, not just the corrected text

**Chosen (2026-08-19, commit `5103325`):** when correcting the stale
instrumentation block in `data/Unified_Knowledge_Project_Details.md`, replace the
wrong code **and** add two bullets explaining why `batch=True` is required and
why the setup may not go back into `app.py`.

**Rejected:** the minimal swap — fix the fenced code, add nothing. It was offered
and declined.

**Why the minimal swap is not enough.** Established while checking the fast-path
table for that edit: **the vector index is the only path this text takes to a
reader.** `extract_problem_block` never serves this file — its regex at
`config.py:177-179` is `^\s*(?:#|//|\*)` and every heading in the file is
pandoc-escaped as `\#`, giving **0 matches** when run against it. No fast-path
key concerns tracing either. So a reader gets a *retrieved chunk*, not the
section.

A bare corrected fence therefore reaches someone as `register(batch=True)` with
no indication that it is load-bearing rather than a default somebody typed.
`CLAUDE.md` says "Never change that to `batch=False`" and this file says "Do not
change this back" — **and neither file is in `data/`, so the agent cannot cite
either.** The note is the only place that reasoning can reach a reader through
this system.

**The honest limit.** The bullets help only if they land in the same retrieved
chunk as the fence. `config.py:114` sets the parent chunk size to 1000 and the
section runs to roughly 1,600 characters, so they probably do not. Recorded
rather than resolved.

**Precedent set:** a correction under the `data/` per-file exception may add
reasoning that did not exist before, when the corrected fact is one a reader
would otherwise act wrongly on. It is still not licence to rewrite for style.

### The Phoenix endpoint is defaulted, not assigned

**Chosen:** `os.environ.setdefault("PHOENIX_COLLECTOR_ENDPOINT", ...)`.

**Rejected:** plain assignment.

**Why:** assignment overwrote whatever the environment held, so a deployed
container could never point the collector somewhere reachable or set it empty
to opt out. `setdefault` keeps local development working with no configuration
while letting the environment win.

### The refine cap is 8,000 characters, not 1,000

**Chosen:** `transcript: str = Field(..., max_length=8000)` at `app.py:151`.

**Rejected:** `1000`, matching the message cap at `guardrails.py:13`, so the two
routes would read consistently.

**Why the rejected option lost.** Consistency was the whole case for `1000`, and
it rests on a claim about the frontend that is false. `ChatInput.tsx:180` — the
microphone button — stops recording and refines **without submitting**, so the
refined text lands in the input box and the user edits it there. A dictation of
1,400 characters trimmed by hand to 600 sends successfully today; a cap of 1,000
rejects it before it can be trimmed. `ChatInput.tsx:89-91` reads
`data.refined_transcript || currentTranscript` with no `response.ok` check, so
the user is told nothing when that happens — the feature just stops refining.

The second half of the reason: a per-call cap does not bound total spend, because
nothing bounds call count. There is no rate limiting anywhere in `backend/`. So
the tighter number buys nothing measurable and costs a path that works.

**Anyone tidying `8000` down to match `guardrails.py:13` is undoing this.** The
two numbers measure different strings and are not meant to agree — the message
cap measures what is sent, the transcript cap measures what is dictated before
editing. The full evidence, both stop paths and where 8,000 comes from, is in
[OPEN.md](OPEN.md) item 9 under "Why 8,000 and not 1,000".

---

## Evaluation

### The fast-path table is a product feature, not a measurement

**Recorded, not chosen:** the table answers 53 of the 94 evaluation cases and
26 of the 34 recall cases without touching the retriever. The headline logic
score is therefore not a measure of the RAG pipeline.

**Why it matters:** report the 41-case logic figure and the 8-case recall
figure alongside the headline whenever retrieval changes, or you will report a
movement that did not happen. The full explanation is in
[CLAUDE.md](CLAUDE.md).

### Changing a fallback model does not oblige an evaluation run

**Chosen (2026-08-18):** a change to `config.py:60` `fallback_llm`, or to any
fallback added later, may be made and committed without running the suite.

**Rejected:** spending roughly $0.11 of a $1.13 balance to confirm a no-op.

**Why, established from source rather than argued.**
`langchain_core/runnables/fallbacks.py:187-188` iterates the runnables and
returns on the first success, and `fallbacks.py:156-161` documents that iterator
as yielding the runnable and then its fallbacks. A fallback is therefore never
reached while the primary succeeds. A passing 94-case run cannot execute the
changed code, so the score cannot move.

The rule's own trigger in [CLAUDE.md](CLAUDE.md) names the system prompt, the
semantic router, the tools and the retrieval pipeline. A fallback model is none
of those.

**The limit of this, stated explicitly:** it applies only while the primary
succeeds. Changing `config.py:49` `primary_llm` changes the model under test and
does require a full run.

### The recall baseline was lowered to 33/34 on purpose

**Chosen:** rebuild the vector index, accept that Recall@k falls from 34/34 to
33/34, and record the new figure as the baseline.

**Rejected:** reverting the rebuild to keep 34/34. Also rejected: changing
`search.py` to win index 83 back inside the same change.

**Why:** the pre-rebuild index held roughly five copies of everything — 8,404
distinct chunks stored 5 times each, 85,008 child chunks against 17,954 after.
`search.py:390` truncates the candidate pool to 50 before reranking, so a pool
of 50 held about 10 distinct documents. That is a worse defect than one recall
point, and it was invisible in the score.

The rebuild also fixed index 37, which `OPEN.md` had carried as a known failure.
Net on AI Logic was flat at 90/94; the movement was one genuinely-exercised RAG
case gained and one lost.

**Corrected 2026-08-20.** This originally read "Fixing index 83 properly means
changing the order of truncation and reranking, which is application logic and
needs its own evaluation cycle." That was measured false. The document index 83
needs is never retrieved into the candidate pool at all, so no reordering could
recover it. See `OPEN.md` item 1.

**Update, 2026-08-20 — the point was recovered, so the heading is now history.**
The baseline is 34/34 again. **The decision recorded here still stands:** taking
the rebuild and accepting a one-point cost was right, because five copies of
every chunk was the worse defect and the score could not see it. What has
changed is only that the cost has since been paid back, by the docstring
directive at `search.py:38-44` rather than by anything in this entry. The two
rejected alternatives were also never reached for.

**The decision recorded here is unaffected.** Bending `search.py` to recover one
case inside a rebuild commit would still have hidden the defect, whatever the
defect turned out to be — and it turned out not to be the one named above, which
is the argument for keeping the two changes apart, not against it. It is written
up as `OPEN.md` item 1 instead.

**Consequence:** `eval.py:232` still gates on `recall_score == 100.0`, so the
suite reports `PIPELINE FAILED` at this baseline. That is expected until index
83 is fixed. Do not relax the gate to make the message go away.

### `.langchain.db` was stripped from the history, not migrated to LFS

**Chosen:** remove the blob from every commit with `git filter-repo`, run in a
throwaway clone, then force-push. The same pass also stripped the
`Co-Authored-By` and `Claude-Session` trailers, since the rewrite range was
already set by the older blob commit and doing both cost zero extra disruption.

**Rejected — migrating it to LFS.** It is a regenerable response cache that
grows on every eval run. Tracking it in LFS would have kept shipping it, and the
quota problem would have returned larger.

**Rejected — `git rm --cached` alone.** The remote was ten commits behind, so the
blob sat inside the pack being pushed either way. It would not have unblocked
anything.

**Rejected — running `filter-repo --force` in the working repo.** Its clean-tree
guard cannot pass here, and `--force` skips every guard and ends with
`git reset --hard`. Roughly 33 KB of hand-written `data/` notes existed in no
commit at the time. The fresh clone avoided the question entirely.

**Why it was safe to publish the rewrite:** the committed blob was re-scanned
independently — 1,502 rows, 31.7 M characters, 13 credential pattern classes —
and the only match was `postgresql://localhost/postgres`, with no user and no
password. Note that a rewrite does not unpublish: if a secret ever does reach a
commit here, rotate the credential. The rewrite is for size, not secrecy.

**Consequence:** 17 of 66 commits have new hashes. `.langchain.db` is now in
`.gitignore`, so the path back to the same failure is closed. Keep a copy of the
cache outside the repository if you want eval runs to stay cheap.

### `data/` may be corrected, one file at a time, with approval

**Chosen (2026-08-18):** the absolute prohibition in `CLAUDE.md` becomes a
default with one exception. An agent may **propose** a correction to one named
`data/` file, showing the exact lines and the exact replacement, and may write it
only after the user approves that file. Approval does not carry to another file
or another session.

**Rejected — keeping the absolute ban.** Not because it was unfollowable. It was
followable, and it was being followed. The ban bound the agent, not the user: it
placed every `data/` correction on the user, who could open any file and fix it
at any time. Nothing was ever unreachable.

What changed is who does the work. The user's stated reason is volume — enough
notes carry content that has gone stale that correcting them all by hand is
impractical — so the work was delegated under per-file approval. **That volume
is the user's assessment and has not been measured.** One stale passage is
verified: `data/Unified_Knowledge_Project_Details.md:1350-1364` documents an
`app.py` block deleted on 2026-08-18 for being a production defect, confirmed by
reading the file and commit `247dd15`. How many others exist is unknown.
`OPEN.md` item 5 now names a check, `backend/evals/check_fast_path.py`, added
2026-08-22 — but it compares the fast-path table against `data/`, not `data/`
against the code it documents. Nothing checks for stale passages.

**This is a delegation of labour, not a judgement that the rule was wrong.** The
distinction matters for whoever reads this next. "The rule forbade something
necessary, so the rule was wrong" would generalise to any future request to
widen the exception. "The user chose to delegate work that was always theirs"
does not generalise, and the per-file approval is what keeps it from doing so.

**Rejected — a verbal allowance carried in conversation.** It does not reach the
next session, which reads `CLAUDE.md` and refuses. The relaxation has to live in
the file or it does not exist.

**Why the guard rails kept their shape.** The original rule protected two
different things and only one of them needed relaxing.

- **The parser-hack ban is untouched and absolute.** Injecting tags, HTML or
  structural markers to make chunking easier stays forbidden, approved or not.
  That was always the real point of the rule, and none of it is a correction.
- **Corrections only.** Restating a fact that is no longer true is permitted.
  Rewriting for style, brevity or tone is not.
- **`git status` on `data/` first.** The history section of `CLAUDE.md` records
  that this repository has held hand-written `data/` notes existing in no
  commit. `data/` was verified clean before this change — `git status
  --porcelain --untracked-files=all data/` empty, 39 files tracked — so every
  file already has a recoverable version. That precondition is a standing
  requirement, not a one-off.

**The trap that makes this less useful than it looks, and is stated in the
rule:** 26 of the 53 `FAST_PATH_INTERCEPTS` entries carry a `target_id`, and 20
of those hold a copy of a `data/` problem block — 3 byte-identical, 17 differing
only in the first line or the trailing `<END OF PROBLEM>` marker.
`agents.py:36-38` consults that table before any model call, so editing `data/`
cannot change what those queries return. Measured 2026-08-22 by
`backend/evals/check_fast_path.py`. See [OPEN.md](OPEN.md) item 5.

**Consequence:** an approved edit reaches the deployed Space by commit and push
alone, because the Space ships no manifest since `003496a` and re-ingests on
every start. The local index does not update, and `eval.py` measures against it
— see [OPEN.md](OPEN.md) item 2.

### Destructive `.docx` conversion, accepted

**Chosen:** `ingest.py` converts any `.docx` in `data/` to markdown via pandoc
and then permanently deletes the original.

**Rejected:** keeping both copies.

**Why:** two copies of the same document both get ingested, and markdown is the
only format the chunker understands. The cost is that the original is
unrecoverable, so originals are kept outside `data/` before ingestion. This is
documented at the top of `ingest.py` and is a real trap for a future session.

### The `@/i18n` test criteria were rewritten, not tuned

**Chosen:** state the three facts the answer must contain, and adopt the
neighbouring case's wording allowing additional relevant context.

**Rejected:** leaving it, or loosening it until it passed.

**Why:** the criteria required the agent to "include the surrounding
conceptual explanations" and the judge then failed the agent for doing exactly
that. The neighbouring case already carried the "additional context must not
fail the test" convention and passed on identical behaviour, so this was
consistency with an existing pattern rather than score tuning.

### `check_fast_path.py` tiers its verdicts; a strict byte comparison was rejected

**Chosen:** five verdicts — identical, header and/or marker only, body differs,
not a copy, no live block — each line carrying an action column that names the
file a reader must open, or says "nothing" and why. Exit non-zero for a body
difference and a missing live block only.

**Rejected:** a strict comparison, in which any byte difference is a failure.
Also rejected: splitting the header/marker tier in two, one tier for a mangled
header and one for a missing marker.

**Why not strict:** `target_id` is a recall label before it is a copy claim.
When it is truthy, `agents.py:87-93` synthesises the `ToolMessage` that
`eval.py:47-55` scrapes and `eval.py:143-147` scores for Recall@k. Five entries
carry one and hold a short answer *about* a problem rather than a copy of it, so
a strict rule measures them against something they never claimed to equal and
they can never pass. The second reason is the exit code. Repairing the rest
means editing `backend/core/fast_path_routes.py`, whose strings 53 evaluation
cases return, so under a strict rule the script ships permanently red — and an
exit code that can never return to zero carries no information, so nothing gets
wired to it. Strict would have failed 23 of 26 on the day it was written.

**Why not the two-way tier split:** measured 2026-08-22, of the 17 entries that
differ only in the header and/or the marker, 4 have a mangled header alone, 7
lack the marker alone, and **6 have both** — ids 9, 13, 33, 49, 55, 90. A tier
named for one fault hides the other in those six, and a reader repairing that
tier by adding markers would leave six headers broken. The two faults are
printed as independent flags on each line instead — `header`, `marker` or
`header+marker` — which costs no verdict name and cannot mislabel them. The
split was proposed from the stored-versus-live length gap, which is a proxy: a
mangled `**# Problem 1**3` is the same length as a correct `**# Problem 13**`,
so four of the six looked like marker-only differences.

**Two latent defects were closed in the same commit, neither reachable today.**
The action column could name a file and no repair when a difference was
whitespace `_body` strips; a `whitespace` flag now covers that. And a live block
with an empty body — which `config.py:198-200` can emit for a header with
nothing under it — has the same empty body as any one-line short answer, so the
two collided and the short answer was reported as a header difference; the body
test now requires a non-empty body or a problem heading. `data/` holds 118
problem headers and no header-only block, so neither case fires.

## Records

### The citation-sweep rule kept its evidence in the root; only the procedure moved

Part of the goal "shrink `CLAUDE.md` without losing what it knows". Done
2026-08-21 against `3a07f52`, where the root was 434 lines (`wc -l`). After
the change the root is 408 lines (`wc -l`).

**Chosen:** the root keeps a standing rule of 12 lines: the trigger, both
reasons a filename grep is insufficient, every measurement and date the old
17-line bullet carried, and a pointer to `/citation-sweep`. The new skill
`.claude/skills/citation-sweep/SKILL.md` holds the four-step procedure only,
and repeats no measurement or date. The "## Frontend rules" section moved
verbatim to `frontend/CLAUDE.md`, above its `@AGENTS.md` import.

**Rejected:** the root keeps one line and the skill carries the procedure with
the evidence beside each step (`247dd15` by 7; 12 bare refs against 44; the
range end that moved). It would have saved about 8 more root lines.

**Why:** the goal forbids moving a measurement or a reason out of the file that
loads every turn. A skill body loads only when invoked. A session that commits
a line-count change without invoking the skill sees the root rule and the
skill's one-line description, nothing more; under the rejected shape it would
have no reason to distrust its own grep, which is exactly how `247dd15` moved
eight citations unnoticed. Under the chosen shape the root still says why the
grep fails, and `.claude/advisor-executor-hitl.md:100` ("`CLAUDE.md` sets out
both") stays true.

Where each removed range went. Line numbers on the left are `CLAUDE.md` at
`3a07f52`; on the right, the files at the commit that records this entry.

| At `3a07f52` | Content | Now |
|---|---|---|
| `CLAUDE.md:368-388` (21 lines) | "## Frontend rules", verbatim | `frontend/CLAUDE.md:1-21` |
| `CLAUDE.md:389` | the `---` separator | `CLAUDE.md:363`, unchanged, now between "## Secrets" and "## Commands" |
| `CLAUDE.md:313-329` (17 lines), the rule and its evidence | reworded, every measurement kept | `CLAUDE.md:313-324` (12 lines) |
| `CLAUDE.md:313-329`, the procedure | grep the filename; search bare `:NNN` separately; check both ends of a range; leave past-tense citations alone | `.claude/skills/citation-sweep/SKILL.md:16-29` |

Every measurement, date and hash from the old bullet, and its single home now:

| Item | Now |
|---|---|
| bare-citation examples `\| :102 \|` and `at :210` | `CLAUDE.md:326` |
| their location, OPEN.md item 9's route table and the prose below it | `.claude/skills/citation-sweep/SKILL.md:28-29` |
| 12 bare refs into `app.py` against 44 found by the filename grep, 2026-08-21 | `CLAUDE.md:326-327` |
| the `/health` range in OPEN.md whose end moved by one, 2026-08-21; one session filed it safe, the other caught it | `CLAUDE.md:328-329` |
| `247dd15`: a 10-line `app.py` block replaced by a 17-line comment; eight citations across two records wrong by exactly 7; found by accident, weeks later | `CLAUDE.md:330-332` |
| leave past-tense citations to deleted code alone; they are history | `CLAUDE.md:332-333` and `SKILL.md:35-37` |

`OPEN.md:729` cited `CLAUDE.md` "Frontend rules" by title and now names
`frontend/CLAUDE.md`. The other four title references into the root
(`OPEN.md:147`, `OPEN.md:983`, `DECISIONS.md:109`, `DECISIONS.md:716`) point at
sections that did not move. No bare `:NNN` citation into the root exists in the
four records (grep, 0).

**Corrected 2026-08-22.** The right-hand column above was **exact at
`f4b9ee1`**, the commit that wrote this entry: `CLAUDE.md` held 408 lines and
the bare-examples line sat at `:317`, as cited. `430c940` then added four lines
to `CLAUDE.md` and did not sweep, moving all five down by four — the first of
them from `:317` to `:321`. `81889dc`, `c1cc45f`, `efe4285` and `55fb8e9`
carried the break unchanged, and the commit that added `check_fast_path.py`
moved them a further five. All five now name the true line.

The table above them is not corrected and does not need to be. Its numbers are
exact at the frame it declares in words two paragraphs up, checked at `f4b9ee1`:
`## Secrets` at 357, the `---` at 363, `## Commands` at 365; the rule at 313-324,
twelve lines; `frontend/CLAUDE.md:1-21`, twenty-one lines. **Both tables were
written in the same commit and both were correct in it. The only difference is
one word in their headers** — table 1 says "at the commit that records this
entry", table 2 says "now". One declared a frame and the other claimed currency,
and only the one claiming currency could drift. Note that the rule "leave
past-tense citations alone" does not decide this: it is written as *to deleted
code*, and table 1 points at content that still exists and has moved. The frame
declaration is what carries it.

This is the failure the rule it documents exists to catch, found in the entry
that documents it, four commits after the commit that caused it.
