# backend/tests/test_core_registry.py
"""Core contract tests for the thread registry (memory.py), end to end and offline.

The registry INSERT is core: the checkpoint tables have foreign keys to
thread_metadata, so a turn without the row cannot save its history. The
model-made title is optional: when it fails, raises or is skipped, the turn
still registers its thread and streams its answer.
"""
import asyncio

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from psycopg.errors import ForeignKeyViolation

from backend import memory
from conftest import (
    ANSWER,
    DONE,
    QUESTION,
    FailingModel,
    ScriptedModel,
    checkpoint_messages,
    rag_script,
    run_chat,
    streamed_text,
)

FALLBACK_TITLE = QUESTION[:40] + "..."


class TitleModel:
    """Stands in for config.llm in generate_title_from_llm; records each call."""

    def __init__(self, title):
        self.title = title
        self.calls = []

    async def ainvoke(self, messages, config=None, **kwargs):
        self.calls.append(list(messages))
        return AIMessage(content=self.title)


def test_new_thread_is_registered_and_gets_the_model_title(core):
    """Steps: registry (real INSERT), title (background), answer, stream, checkpoint."""
    title_model = TitleModel("Reranker Context")
    core.use_real_registry(title_model)
    core.set_qa(rag_script(QUESTION, ANSWER))

    chunks = run_chat(core.graph, QUESTION, pool=core.registry)

    assert core.registry.rows["thread-1"] == {"title": "Reranker Context", "owner_id": "owner-1"}
    assert len(title_model.calls) == 1
    assert streamed_text(chunks) == ANSWER
    assert chunks[-1] == DONE
    assert [m.type for m in checkpoint_messages(core.graph)] == ["human", "ai", "tool", "ai"]


def test_failing_title_model_keeps_the_fallback_title_and_the_answer(core, capsys):
    """Steps: registry, title fails inside generate_title_from_llm, answer, stream."""
    core.use_real_registry(FailingModel())
    core.set_qa(rag_script(QUESTION, ANSWER))

    chunks = run_chat(core.graph, QUESTION, pool=core.registry)

    # The fallback equals the INSERT's title, so the log line shows the task ran
    assert "Failed to generate title from LLM: fake provider outage" in capsys.readouterr().out
    assert core.registry.rows["thread-1"] == {"title": FALLBACK_TITLE, "owner_id": "owner-1"}
    assert streamed_text(chunks) == ANSWER
    assert chunks[-1] == DONE
    assert [m.type for m in checkpoint_messages(core.graph)] == ["human", "ai", "tool", "ai"]


def test_raising_title_function_does_not_fail_the_turn(core, monkeypatch, capsys):
    """Steps: registry, title raises past generate_title_from_llm, answer, stream."""
    core.use_real_registry(FailingModel())

    async def raising_title(user_message):
        raise RuntimeError("fake title failure")

    monkeypatch.setattr(memory, "generate_title_from_llm", raising_title)
    core.set_qa(rag_script(QUESTION, ANSWER))

    chunks = run_chat(core.graph, QUESTION, pool=core.registry)

    assert "Background title update failed: fake title failure" in capsys.readouterr().out
    assert core.registry.rows["thread-1"] == {"title": FALLBACK_TITLE, "owner_id": "owner-1"}
    assert streamed_text(chunks) == ANSWER
    assert chunks[-1] == DONE
    assert [m.type for m in checkpoint_messages(core.graph)] == ["human", "ai", "tool", "ai"]


def test_title_task_that_cannot_start_does_not_fail_the_turn(core, monkeypatch, capsys):
    """Steps: registry, scheduling the title task raises, answer, stream."""
    title_model = TitleModel("Reranker Context")
    core.use_real_registry(title_model)
    real_create_task = asyncio.create_task

    def create_task_refusing_titles(coro, *args, **kwargs):
        # Only the title task is refused; the graph's own tasks still start
        if getattr(coro, "__name__", "") == "update_title_bg":
            raise RuntimeError("fake scheduling failure")
        return real_create_task(coro, *args, **kwargs)

    monkeypatch.setattr(memory.asyncio, "create_task", create_task_refusing_titles)
    core.set_qa(rag_script(QUESTION, ANSWER))

    chunks = run_chat(core.graph, QUESTION, pool=core.registry)

    assert "Background title update could not start: fake scheduling failure" in capsys.readouterr().out
    assert title_model.calls == []
    assert core.registry.rows["thread-1"] == {"title": FALLBACK_TITLE, "owner_id": "owner-1"}
    assert streamed_text(chunks) == ANSWER
    assert chunks[-1] == DONE
    assert [m.type for m in checkpoint_messages(core.graph)] == ["human", "ai", "tool", "ai"]


def test_second_turn_skips_the_title_and_keeps_the_thread(core):
    """Steps: registry finds the row (owner re-read), no second title call, answer, checkpoint."""
    second_question = "Which model does the reranker use?"
    second_answer = "It uses a cross-encoder."
    title_model = TitleModel("Reranker Context")
    core.use_real_registry(title_model)
    core.set_fast_replies("ROUTE_TO_CORE", "IN_SCOPE", "ROUTE_TO_CORE", "IN_SCOPE")
    core.set_qa(ScriptedModel(
        *rag_script(QUESTION, ANSWER).models,
        *rag_script(second_question, second_answer).models,
    ))

    run_chat(core.graph, QUESTION, pool=core.registry)
    chunks = run_chat(core.graph, second_question, pool=core.registry)

    assert len(title_model.calls) == 1
    assert core.registry.rows["thread-1"] == {"title": "Reranker Context", "owner_id": "owner-1"}
    assert streamed_text(chunks) == second_answer
    assert [m.type for m in checkpoint_messages(core.graph)] == ["human", "ai", "tool", "ai"] * 2


def test_real_registry_refuses_a_thread_owned_by_another_browser(core):
    """Steps: registry (INSERT conflicts, owner re-read differs), refusal, no title, no checkpoint."""
    title_model = TitleModel("Reranker Context")
    core.use_real_registry(title_model)
    core.registry.rows["thread-1"] = {"title": "Someone else's chat", "owner_id": "owner-2"}
    core.set_qa(ScriptedModel())

    chunks = run_chat(core.graph, QUESTION, pool=core.registry)

    assert streamed_text(chunks) == "This chat is not available."
    assert chunks[-1] == DONE
    assert title_model.calls == []
    assert core.registry.rows["thread-1"] == {"title": "Someone else's chat", "owner_id": "owner-2"}
    assert checkpoint_messages(core.graph) == []


def test_cache_hit_path_starts_the_title_once(core, monkeypatch):
    """Steps: registry (the shared save step), then a cache hit; the title starts once."""
    hit = (Document(page_content=QUESTION, metadata={"response": ANSWER}), 0.0)
    monkeypatch.setattr(core.cache, "similarity_search_with_score", lambda query, k=1: [hit])
    core.set_qa(rag_script(QUESTION, ANSWER))

    run_chat(core.graph, QUESTION)

    # Whether the cached turn then falls through (M1) does not change this count
    assert core.title_calls == [("thread-1", QUESTION)]


def test_triage_reply_path_starts_the_title_once(core):
    """Steps: registry (the shared save step), then a triage reply; the title starts once."""
    core.set_fast_replies("Hello! Ask me about the knowledge base.", "IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))

    run_chat(core.graph, QUESTION)

    # Whether the triage turn then falls through (M1) does not change this count
    assert core.title_calls == [("thread-1", QUESTION)]


def test_core_path_starts_the_title_once(core):
    """Steps: registry (the shared save step), then the graph path; the title starts once."""
    core.set_qa(rag_script(QUESTION, ANSWER))

    run_chat(core.graph, QUESTION)

    assert core.title_calls == [("thread-1", QUESTION)]


def test_checkpoint_write_without_a_registry_row_is_refused(core):
    """The fake checkpointer mirrors coupling 1, so the tests above can catch a missing INSERT."""
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))
    config = {"configurable": {"thread_id": "unregistered"}}

    with pytest.raises(ForeignKeyViolation, match="fk_cascade_metadata_checkpoints"):
        asyncio.run(core.graph.ainvoke({"messages": [HumanMessage(content=QUESTION)]}, config))
    assert "unregistered" not in core.registry.rows
