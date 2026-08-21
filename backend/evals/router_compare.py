"""Compare the scope router's verdict (agents.py:40-52 prompt) across models.

Run from the repo root:
    uv run python -m backend.evals.router_compare
Imports backend.core.config so the environment is loaded the way the app
loads it. 13 short live calls per model.

2026-08-22 result: gemini-3.5-flash-lite answered OUT_OF_SCOPE for 46, 58, 59,
60, 93 and CONVERSATIONAL for 42; 2.5 Flash and 3.6 Flash answered IN_SCOPE on
all six. That is why fast_llm is not Lite (config.py:70).
"""
import asyncio
import json
import os

from backend.core import config  # loads env, builds fast_llm (Flash Lite)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

SYS = (
    "You are an input router. Apply these rules in order and stop at the first one that matches. "
    "RULE 1 (highest priority): If the query explicitly asks about Kubernetes, AWS Lambda, Web scraping, Vue.js, Java Spring Boot, or multiple inheritance in Python, respond EXACTLY with 'OUT_OF_SCOPE'. This rule overrides every rule below it, including any request to write code or a script about those topics. "
    "RULE 2: If the query explicitly asks about weather, temperature, or AQI, respond EXACTLY with 'IN_SCOPE'. "
    "RULE 3: If the query is a basic greeting, asking about your identity, or asking a general knowledge question (e.g., capitals, distances) WITH NO mention of weather/AQI/technical docs, respond EXACTLY with 'CONVERSATIONAL'. "
    "RULE 4: For EVERYTHING else, respond with EXACTLY 'IN_SCOPE'. DO NOT explain."
)

d = json.load(open(os.path.join(os.path.dirname(__file__), "qa_dataset.json")))
IDX = [27, 28, 29, 30, 31, 42, 46, 58, 59, 60, 62, 63, 93]


def mk(model):
    return ChatOpenAI(
        model=model,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0, streaming=False, max_retries=1, request_timeout=45,
    )


MODELS = {
    "google/gemini-3.5-flash-lite (config.fast_llm)": config.fast_llm,
    "google/gemini-3.6-flash": mk("google/gemini-3.6-flash"),
    "google/gemini-2.5-flash": mk("google/gemini-2.5-flash"),
}


async def main():
    for name, llm in MODELS.items():
        out = []
        for i in IDX:
            try:
                r = await llm.ainvoke([SystemMessage(content=SYS), HumanMessage(content=d[i - 1]["query"])])
                out.append((i, r.content.strip()[:14]))
            except Exception as e:  # show it, never hide it
                out.append((i, "ERR " + type(e).__name__ + ":" + str(e)[:60]))
        print(name, out, flush=True)


if __name__ == "__main__":
    asyncio.run(main())
