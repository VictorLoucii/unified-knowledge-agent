# backend/tests/test_core_graph.py
"""Core contract tests for the compiled LangGraph graph (agents.py), offline."""
import asyncio

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from backend.core import agents, semantic_router
from backend.core import config as backend_config
from conftest import (
    ANSWER,
    FALLBACK_TEXT,
    QUESTION,
    RETRIEVED_TEXT,
    ScriptedModel,
    checkpoint_messages,
    rag_script,
    run_chat,
    streamed_text,
)

GREETING_REPLY = "Hello. Ask me about the knowledge base."
# No "problem X" in the key, so the regex fallback in fast_path_node cannot supply the id.
PLANTED_KEY = "planted fast path question"
PLANTED_ANSWER = "The planted stored answer."
PLANTED_TARGET_ID = "planted_id"
PROBLEM_BLOCK = "**# Problem 7**\nThe stored block."


@pytest.fixture
def route_calls(monkeypatch):
    """Records every route_query call the graph makes, and still runs the real function."""
    calls = []
    real_route_query = agents.route_query

    async def counting_route_query(user_query):
        calls.append(user_query)
        return await real_route_query(user_query)

    monkeypatch.setattr(agents, "route_query", counting_route_query)
    return calls


@pytest.fixture
def planted_table(monkeypatch):
    """Replaces the fast-path table, so these tests do not depend on its contents."""
    monkeypatch.setattr(
        semantic_router,
        "FAST_PATH_INTERCEPTS",
        {PLANTED_KEY: {"output": PLANTED_ANSWER, "target_id": PLANTED_TARGET_ID}},
    )


def test_graph_answers_a_rag_question_and_checkpoints_it(core):
    """Steps: route, retrieval, answer, checkpoint."""
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))
    config = {"configurable": {"thread_id": "graph-thread"}}
    # chat.py registers the thread before the graph runs; the checkpointer requires the row
    core.registry.rows["graph-thread"] = {"title": QUESTION[:40], "owner_id": "owner-1"}

    result = asyncio.run(core.graph.ainvoke({"messages": [HumanMessage(content=QUESTION)]}, config))

    assert result["route_category"] == "RAG"
    assert [m.type for m in result["messages"]] == ["human", "ai", "tool", "ai"]
    assert RETRIEVED_TEXT in result["messages"][2].content
    assert result["messages"][-1].content == ANSWER
    assert [m.type for m in checkpoint_messages(core.graph, "graph-thread")] == ["human", "ai", "tool", "ai"]


def test_fast_path_table_hit_routes_once(core, route_calls, planted_table):
    """Steps: route (table hit), fast_path_node, stream; no model call."""
    core.set_fast_replies()
    core.set_qa(ScriptedModel())

    chunks = run_chat(core.graph, PLANTED_KEY)

    assert route_calls == [PLANTED_KEY]
    assert streamed_text(chunks) == PLANTED_ANSWER
    assert core.fast_llm.calls == 0 and core.qa.calls == []


def test_problem_id_hit_routes_once(core, route_calls, planted_table, monkeypatch):
    """Steps: route (Problem-N block found), fast_path_node, stream; no model call."""
    monkeypatch.setattr(backend_config, "extract_problem_block", lambda problem_id: PROBLEM_BLOCK)
    core.set_fast_replies()
    core.set_qa(ScriptedModel())
    query = "Tell me about Problem 7"

    chunks = run_chat(core.graph, query)

    assert route_calls == [query]
    assert streamed_text(chunks) == PROBLEM_BLOCK
    assert core.fast_llm.calls == 0 and core.qa.calls == []


def test_rag_question_routes_once(core, route_calls):
    """Steps: route (RAG), scope router, retrieval_node, answer, stream."""
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))

    chunks = run_chat(core.graph, QUESTION)

    assert route_calls == [QUESTION]
    assert streamed_text(chunks) == ANSWER


def test_conversational_message_routes_once(core, route_calls):
    """Steps: route (RAG), scope router (CONVERSATIONAL), conversational_node, stream."""
    core.set_fast_replies("CONVERSATIONAL", GREETING_REPLY)
    core.set_qa(ScriptedModel())
    query = "hello there"

    chunks = run_chat(core.graph, query)

    assert route_calls == [query]
    assert streamed_text(chunks) == GREETING_REPLY


def test_out_of_scope_message_routes_once(core, route_calls):
    """Steps: route (RAG), scope router (OUT_OF_SCOPE), fallback, stream."""
    core.set_fast_replies("OUT_OF_SCOPE")
    core.set_qa(ScriptedModel())
    query = "How do I deploy a pod to Kubernetes?"

    chunks = run_chat(core.graph, query)

    assert route_calls == [query]
    assert streamed_text(chunks) == FALLBACK_TEXT


def test_fast_path_hit_keeps_the_target_id_marker(core, planted_table):
    """eval.py reads recall from this marker. The key has no "problem X" text, so the id comes from the router."""
    core.set_fast_replies()
    core.set_qa(ScriptedModel())

    run_chat(core.graph, PLANTED_KEY)

    tool_messages = [m for m in checkpoint_messages(core.graph) if isinstance(m, ToolMessage)]
    assert [m.content for m in tool_messages] == [f"<!-- RETRIEVED_PROBLEM_IDS: [{PLANTED_TARGET_ID}] -->"]


def assert_follow_up_sent_a_valid_list(core, marker_id):
    """Every model call of the follow-up has no unmatched tool message, and the marker stays stored."""
    assert len(core.qa.calls) == 2
    for call in core.qa.calls:
        called_ids = set()
        for message in call:
            if isinstance(message, ToolMessage):
                assert message.tool_call_id in called_ids
            called_ids.update(tc["id"] for tc in getattr(message, "tool_calls", None) or [])
    assert [m.type for m in core.qa.calls[0]] == ["system", "human", "ai", "human"]
    assert RETRIEVED_TEXT in core.qa.calls[1][-1].content
    stored = [m.content for m in checkpoint_messages(core.graph) if isinstance(m, ToolMessage)]
    assert f"<!-- RETRIEVED_PROBLEM_IDS: [{marker_id}] -->" in stored


def test_rag_question_after_a_table_hit_sends_a_valid_list(core, planted_table):
    """OPEN.md item 15: the main model rejects a tool message with no matching tool call."""
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))

    run_chat(core.graph, PLANTED_KEY)
    chunks = run_chat(core.graph, QUESTION)

    assert streamed_text(chunks) == ANSWER
    assert_follow_up_sent_a_valid_list(core, PLANTED_TARGET_ID)


def test_rag_question_after_a_problem_id_hit_sends_a_valid_list(core, planted_table, monkeypatch):
    """OPEN.md item 15, the same fault through the Problem-N route."""
    monkeypatch.setattr(backend_config, "extract_problem_block", lambda problem_id: PROBLEM_BLOCK)
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))

    run_chat(core.graph, "Tell me about Problem 7")
    chunks = run_chat(core.graph, QUESTION)

    assert streamed_text(chunks) == ANSWER
    assert_follow_up_sent_a_valid_list(core, "7")


def test_only_the_unmatched_tool_message_is_dropped():
    """A real result from an earlier turn stays: without it, its tool call has no output, which is also a 400."""
    def call(call_id):
        return AIMessage(content="", tool_calls=[{"name": "search_knowledge_base", "args": {}, "id": call_id}])

    real_result = ToolMessage(content="real", tool_call_id="call_a")
    unmatched = ToolMessage(content="marker", tool_call_id="other_id")
    messages = [
        HumanMessage(content="q1"), call("call_a"), real_result, AIMessage(content="a1"),
        HumanMessage(content="q2"), unmatched, AIMessage(content="a2"),
        HumanMessage(content="q3"),
    ]

    kept = agents.drop_unmatched_tool_messages(messages)

    assert kept == [m for m in messages if m is not unmatched]
    # One way only: a tool call with no result is not this filter's case (OPEN.md item 15).
    unanswered = [HumanMessage(content="q1"), call("call_w"), HumanMessage(content="q2")]
    assert agents.drop_unmatched_tool_messages(unanswered) == unanswered


def test_fast_path_payload_carries_only_the_last_message(planted_table):
    """The payload is stored in the checkpoint, so the whole history would be stored again on every hit."""
    state = {"messages": [HumanMessage(content="first"), AIMessage(content="reply"), HumanMessage(content=PLANTED_KEY)]}

    send = asyncio.run(agents.route_input_node(state))

    assert [m.content for m in send.arg["messages"]] == [PLANTED_KEY]


def test_rag_prompt_hint_text_stays_the_same(core):
    """Any change to this text is a prompt change and turns the eval's cached model calls into misses."""
    core.set_fast_replies("IN_SCOPE")
    model = rag_script(QUESTION, ANSWER)
    core.set_qa(model)

    run_chat(core.graph, QUESTION)

    assert "Hint: The query was classified into the domain: RAG. IMPORTANT:" in model.calls[0][0].content
