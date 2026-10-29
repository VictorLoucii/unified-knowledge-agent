# backend/tests/test_core_graph.py
"""Core contract tests for the compiled LangGraph graph (agents.py), offline."""
import asyncio

from langchain_core.messages import HumanMessage

from conftest import ANSWER, QUESTION, RETRIEVED_TEXT, checkpoint_messages, rag_script


def test_graph_answers_a_rag_question_and_checkpoints_it(core):
    """Steps: route, retrieval, answer, checkpoint."""
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))
    config = {"configurable": {"thread_id": "graph-thread"}}

    result = asyncio.run(core.graph.ainvoke({"messages": [HumanMessage(content=QUESTION)]}, config))

    assert result["route_category"] == "RAG"
    assert [m.type for m in result["messages"]] == ["human", "ai", "tool", "ai"]
    assert RETRIEVED_TEXT in result["messages"][2].content
    assert result["messages"][-1].content == ANSWER
    assert [m.type for m in checkpoint_messages(core.graph, "graph-thread")] == ["human", "ai", "tool", "ai"]
