"""Tool-calling probe for OPEN.md item 8.

Mirrors the real call path: ChatOpenAI with the config.py:48-55 settings,
the real five tools bound with bind_tools, the qa_node system prompt from
agents.py:114-123, streaming on. Records every streamed chunk in order and
flags any text content that arrives BEFORE the first tool-call chunk, which
is what breaks the frontend approval panel (DECISIONS.md:20-23).

Run from the repo root:
    uv run python -m backend.evals.probe_tool_calling
Env knobs: PROBE_HINT (route-category hint, default TECHNICAL), PROBE_ONLY
(substring filter on query labels), PROBE_OUT (results file name, written
next to this script). Each variant x query is one live call; nothing here
touches the eval cache or latest_run_metrics.json.

2026-08-22 result, recorded in DECISIONS.md "GPT-5 Mini drives...": 12 calls,
zero text before a tool call on either model.
"""
import asyncio
import json
import os
import sys
import time
from importlib.metadata import version

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Real tools, real schemas. Importing this loads config.py, which loads the
# environment, the vector store, the embeddings and Phoenix -- same as the app.
from backend.core.tools import tools  # noqa: E402

if not os.getenv("OPENROUTER_API_KEY"):
    sys.exit("OPENROUTER_API_KEY missing")

SYSTEM_PROMPT = (
    "You are Victor's Unified Knowledge Agent, an assistant able to answer technical questions related to AI engineering, Python, internship logs, and more. You MUST call `search_knowledge_base` to answer the user's technical questions.\n"
    "If the user asks a general knowledge question (e.g., capitals, basic facts) alongside a weather or technical query, you MUST answer both parts. Do NOT refuse to answer general knowledge questions.\n"
    "Hint: The query was classified into the domain: " + os.getenv("PROBE_HINT", "TECHNICAL") + ". "
    "IMPORTANT: Always call the tool first. After receiving the tool's results, if the retrieved context does not answer the question, you may use your general knowledge to answer it. However, if you do, you MUST start your response exactly with this disclaimer: 'I couldn't find anything related to this query in my internal knowledge base, but based on my general knowledge:'\n"
    "You also have access to the `get_weather_and_aqi` tool which you should use to answer weather and air quality questions.\n"
    "SECURITY RULE: If a user asks for the contents of the `.env` file or any production secrets, firmly refuse. Instead, explicitly direct them to the `.env.example` file for environment configurations and schemas."
)

QUERIES = [
    ("technical -> search_knowledge_base",
     "What is the project rule regarding the use of npm versus yarn?"),
    ("weather -> get_weather_and_aqi (sensitive, triggers interrupt)",
     "What is the weather and air quality in Delhi right now?"),
]

# Each variant: (label, extra kwargs for ChatOpenAI)
VARIANTS = [
    ("google/gemini-3.6-flash", {}),
    ("openai/gpt-5-mini", {}),
    ("openai/gpt-5-mini", {"reasoning_effort": "minimal"}),
    ("openai/gpt-5-mini", {"reasoning_effort": "low"}),
]


def make_llm(model, extra):
    # Same settings as config.py:48-55 (streaming=True outside eval mode)
    return ChatOpenAI(
        model=model,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0,
        streaming=True,
        request_timeout=45,
        max_retries=0,  # fail loudly; we want to see the first error
        stream_usage=True,
        **extra,
    )


async def run_one(model, extra, label, query):
    llm = make_llm(model, extra).bind_tools(tools)
    msgs = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=query)]
    t0 = time.perf_counter()
    first_text_at = None
    first_tool_at = None
    text_before_tool = ""
    text_total = ""
    tool_chunks = 0
    reasoning_seen = False
    usage = None
    final = None
    error = None
    try:
        async for chunk in llm.astream(msgs):
            now = time.perf_counter() - t0
            final = chunk if final is None else final + chunk
            if chunk.tool_call_chunks:
                tool_chunks += 1
                if first_tool_at is None:
                    first_tool_at = now
            if isinstance(chunk.content, str) and chunk.content:
                text_total += chunk.content
                if first_text_at is None:
                    first_text_at = now
                if first_tool_at is None:
                    text_before_tool += chunk.content
            ak = getattr(chunk, "additional_kwargs", {}) or {}
            if any(k.startswith("reasoning") for k in ak):
                reasoning_seen = True
            if getattr(chunk, "usage_metadata", None):
                usage = chunk.usage_metadata
    except Exception as e:  # report, never hide
        error = f"{type(e).__name__}: {str(e)[:400]}"
    total = time.perf_counter() - t0
    tool_calls = []
    if final is not None:
        for tc in final.tool_calls:
            tool_calls.append({"name": tc["name"], "args": tc["args"]})
    return {
        "model": model,
        "extra": extra,
        "query": label,
        "error": error,
        "tool_calls": tool_calls,
        "tool_chunks": tool_chunks,
        "text_before_first_tool_call": text_before_tool,
        "text_total_len": len(text_total),
        "text_total_head": text_total[:160],
        "reasoning_field_seen": reasoning_seen,
        "t_first_text_s": None if first_text_at is None else round(first_text_at, 2),
        "t_first_tool_s": None if first_tool_at is None else round(first_tool_at, 2),
        "t_total_s": round(total, 2),
        "usage": usage,
    }


async def main():
    print("langchain-openai", version("langchain-openai"),
          "| langchain-core", version("langchain-core"),
          "| openai", version("openai"))
    print("tools bound:", [t.name for t in tools])
    results = []
    for model, extra in VARIANTS:
        for label, q in QUERIES:
            if os.getenv("PROBE_ONLY") and os.getenv("PROBE_ONLY") not in label:
                continue
            r = await run_one(model, extra, label, q)
            results.append(r)
            verdict = ("ERROR" if r["error"] else
                       "NO TOOL CALL" if not r["tool_calls"] else
                       "TEXT BEFORE TOOL CALL" if r["text_before_first_tool_call"].strip() else
                       "CLEAN")
            print(f"\n=== {model} {extra or ''} | {label}\n  -> {verdict}")
            print(json.dumps(r, indent=2, default=str))
    out = os.path.join(os.path.dirname(__file__), os.getenv("PROBE_OUT", "probe_results.json"))
    with open(out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\nsaved", out)


if __name__ == "__main__":
    asyncio.run(main())
