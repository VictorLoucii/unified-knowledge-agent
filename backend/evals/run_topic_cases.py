# backend/evals/run_topic_cases.py
"""Runs the topic dev cases through the eval's graph and prints what came back.

Run (owner; needs .env): uv run python -m backend.evals.run_topic_cases

The cases come from the owner's problem log (miscellaneous/REVAMP.md, section 13). They are
dev cases, not test cases: nothing is graded. Their use is a before-and-after record for
the Problem-N removal, which deletes auto-escalation. Escalation turns a matching chunk
into the whole problem block, so these cases show whether a topic question still gets a
whole fix without it. Run this file on both sides and compare the printed sections and answers.

It sets up the graph the way eval.py does: the same switches, the same compile, and the
same model cache in .langchain.db, so a second run on unchanged code makes no model call.
"""
import asyncio
import json
import os
import sys
import uuid
from pathlib import Path

project_root = str(Path(__file__).parent.parent.parent.resolve())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# The same environment as eval.py:14-18.
os.environ["EVAL_MODE"] = "true"
for _switch in ("FAST_PATH_ENABLED", "TRANSCRIPT_REFINE_ENABLED", "WEATHER_TOOL_ENABLED"):
    os.environ.setdefault(_switch, "true")

from langchain_community.cache import SQLiteCache  # noqa: E402
from langchain_core.globals import set_llm_cache  # noqa: E402
from langchain_core.messages import HumanMessage  # noqa: E402
from langgraph.checkpoint.memory import MemorySaver  # noqa: E402

from backend.core.agents import workflow  # noqa: E402

TOPIC_CASES = ("keyboard hiding", "the screen")


async def run_case(graph, query):
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    state = await graph.ainvoke({"messages": [HumanMessage(content=query)]}, config=config)
    tool_messages = [m for m in state["messages"] if m.type == "tool"]
    print("=" * 70)
    print(f"QUERY: {query}")
    print(f"ROUTE: {'fast path' if any(m.tool_call_id == 'bypass_tool_call_id' for m in tool_messages) else 'graph'}"
          f"; tool messages: {len(tool_messages)}")
    for n, msg in enumerate(tool_messages, 1):
        sections = msg.artifact.get("retrieved_sections", []) if isinstance(msg.artifact, dict) else []
        escalated = msg.content.count("=== AUTO-ESCALATED CONTEXT:")
        print(f"TOOL MESSAGE {n}: {len(msg.content)} chars; auto-escalated blocks: {escalated}; "
              f"retrieved sections: {len(sections)}")
        for section in sections:
            print(f"  - {section['source_file']} :: {json.dumps(section['headers'], ensure_ascii=False)}")
    print("ANSWER:")
    print(state["messages"][-1].content)


async def main():
    set_llm_cache(SQLiteCache(database_path=os.path.join(project_root, ".langchain.db")))
    graph = workflow.compile(checkpointer=MemorySaver())
    for query in TOPIC_CASES:
        await run_case(graph, query)


if __name__ == "__main__":
    asyncio.run(main())
