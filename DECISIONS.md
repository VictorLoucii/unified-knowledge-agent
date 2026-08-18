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
recall, 33/34 → 34/34, which is what opens the suite's gate.

**Update, 2026-08-18 — that trade has since reversed.** The index rebuild
swapped the pair back: index 37 now passes and index 83 now misses. Recall
returned to 33/34. The decision above still stands — keyword expansion beat
sentences on its own merits — but the two cases were never independent. They
compete for slots in one candidate pool that `search.py:379` truncates *before*
`search.py:399` reranks it, so whichever change lands last decides the winner.
That mechanism, not the expansion style, is the thing to fix. See
[OPEN.md](OPEN.md) item 1.

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

## Deployment

### The Space ingests at startup; the index is not shipped

**Chosen (2026-08-18):** stop tracking `data/.manifest.json`, so a git clone
arrives with no manifest and the container ingests all 26 files at startup.

**Rejected:** shipping `backend/chroma_db` and `backend/docstore` through the
LFS rules that already sit unused at `.gitattributes:4-6`.

**Why:** three reasons, in order of weight.

1. **The startup cost is already absorbed.** `app.py:67-69` runs
   `initialize_rag` in a background thread precisely so HuggingFace health
   checks pass instantly — the comment there says so. The 97-second ingest
   measured in `OPEN.md` item 2 never blocks the port bind. The Space answers
   from the first second; only retrieval is cold, and only briefly.
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
docstore holds any key (`app.py:103`), and an empty docstore was the entire
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

**A knowledge-base document now contradicts the code.**
`data/Unified_Knowledge_Project_Details.md:1342-1364` presents the deleted
block as the way to instrument the backend. `data/` is never edited by this
project's rules, so it is left alone and recorded in [OPEN.md](OPEN.md)
item 5 instead. Ask the agent how tracing works and it will describe the removed code.

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

### The recall baseline was lowered to 33/34 on purpose

**Chosen:** rebuild the vector index, accept that Recall@k falls from 34/34 to
33/34, and record the new figure as the baseline.

**Rejected:** reverting the rebuild to keep 34/34. Also rejected: changing
`search.py` to win index 83 back inside the same change.

**Why:** the pre-rebuild index held roughly five copies of everything — 8,404
distinct chunks stored 5 times each, 85,008 child chunks against 17,954 after.
`search.py:379` truncates the candidate pool to 50 before reranking, so a pool
of 50 held about 10 distinct documents. That is a worse defect than one recall
point, and it was invisible in the score.

The rebuild also fixed index 37, which `OPEN.md` had carried as a known failure.
Net on AI Logic was flat at 90/94; the movement was one genuinely-exercised RAG
case gained and one lost.

Fixing index 83 properly means changing the order of truncation and reranking,
which is application logic and needs its own evaluation cycle. Bending
`search.py` to recover one case inside a rebuild commit would have hidden the
mechanism. It is written up as `OPEN.md` item 1 instead.

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
