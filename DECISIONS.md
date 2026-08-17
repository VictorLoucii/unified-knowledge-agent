# Decisions

One entry per real decision: what was chosen, what was rejected, and why the
rejected option lost. The point is to stop a future session from quietly
undoing something deliberate.

Open work is in [OPEN.md](OPEN.md).

---

## Model and provider

### Gemini 2.5 Flash as the unified driver

**Chosen:** `google/gemini-2.5-flash` via OpenRouter for the agent, the query
expansion and the fallback model.

**Rejected:** DeepSeek V3 as the primary driver.

**Why:** DeepSeek V3 emits text before it emits its tool call. The frontend's
human-in-the-loop approval panel keys off the pause that precedes a tool call,
so that leading text breaks the handshake and the user sees the agent talking
about an action it has not been approved for. DeepSeek is still usable for
evaluation by setting `MODEL_NAME`, but not as the driver.

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
all, and it is why `search.py:229` can de-duplicate by exact `page_content`.

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
recall, 33/34 → 34/34, which is what opens the suite's gate. Index 37 is open
work, not an accepted loss — see [OPEN.md](OPEN.md).

**Also ruled out in the same investigation:** the header relevance boost, which
was changed from +200 to +30. Tested on its own, restoring it to 200 fixed
neither failing case. It stays at 30.

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

### Arize Phoenix over LangSmith

**Chosen:** self-hosted Phoenix via docker compose, with LangSmith environment
variables actively popped at import.

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

### The Phoenix endpoint is defaulted, not assigned

**Chosen:** `os.environ.setdefault("PHOENIX_COLLECTOR_ENDPOINT", ...)`.

**Rejected:** plain assignment.

**Why:** assignment overwrote whatever the environment held, so a deployed
container could never point the collector somewhere reachable or set it empty
to opt out. `setdefault` keeps local development working with no configuration
while letting the environment win.

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
