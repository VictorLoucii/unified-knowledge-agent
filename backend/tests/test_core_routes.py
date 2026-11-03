# backend/tests/test_core_routes.py
"""The chat routes in app.py, called in-process with the core fixture.

The other core tests stop at chat.py, so nothing else runs what app.py adds around
a turn. The removal tests run this file too: they import these helpers into their
probes, and a removal that breaks app.py fails here.
"""
import asyncio

import pytest

from backend import memory
from conftest import ANSWER, DONE, QUESTION, ScriptedModel, parse_events, rag_script, streamed_text

BROWSER_ID = "browser-1"


@pytest.fixture
def routes(core, monkeypatch):
    """backend.app with its Postgres and ingestion checks replaced, and the test's graph in place."""
    # app.py opens Postgres at import, so that one call is replaced first.
    monkeypatch.setattr(memory, "setup_database_tables", lambda: None)
    import backend.app as app_module

    async def owned(*args, **kwargs):
        return True

    monkeypatch.setattr(app_module, "owns_thread", owned)
    monkeypatch.setattr(app_module, "get_ingestion_state", lambda: "done")
    monkeypatch.setattr(app_module, "check_rate_limit", lambda request: None)
    monkeypatch.setattr(app_module, "graph", core.graph)
    return app_module


def call_chat_stream(app_module, message=QUESTION, thread_id="thread-1"):
    async def collect():
        request = app_module.ChatRequest(message=message, thread_id=thread_id)
        response = await app_module.chat_stream(request, object(), BROWSER_ID)
        return [chunk async for chunk in response.body_iterator]

    return asyncio.run(collect())


def call_chat_approve(app_module, thread_id="thread-with-nothing-to-resume"):
    async def collect():
        request = app_module.ActionRequest(thread_id=thread_id, approve=True)
        response = await app_module.chat_approve(request, object(), BROWSER_ID)
        return [chunk async for chunk in response.body_iterator]

    return asyncio.run(collect())


def test_chat_stream_route_streams_the_answer(core, routes):
    """Steps: route, registry, graph, stream."""
    core.set_qa(rag_script(QUESTION, ANSWER))

    chunks = call_chat_stream(routes)

    assert ANSWER in streamed_text(chunks)
    assert chunks[-1] == DONE
    assert core.registry_calls == [("thread-1", QUESTION, BROWSER_ID)]


def test_chat_approve_route_ends_a_thread_with_nothing_to_resume(core, routes):
    """Steps: route, resume fails inside the graph, the stream still ends. No model call."""
    core.set_fast_replies()
    core.set_qa(ScriptedModel())

    chunks = call_chat_approve(routes)

    assert any(event.get("event") == "on_error" for event in parse_events(chunks))
    assert chunks[-1] == DONE
    assert core.qa.calls == []
