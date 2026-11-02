# backend/tests/test_core_switches.py
"""The three env switches: fast path, transcript refine, weather tool with approval."""
import asyncio
import hashlib
import json
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage, ToolMessage

from backend import memory
from backend.core import agents, chat, config, semantic_router
from backend.core.tools import weather_aqi
from conftest import (
    ANSWER,
    FakeMessagesListChatModel,
    NETWORK_ATTEMPTS,
    QUESTION,
    RETRIEVED_TEXT,
    ScriptedModel,
    SWITCH_NAMES,
    StrictFakeMessagesListChatModel,
    answer_turn,
    checkpoint_messages,
    parse_events,
    rag_script,
    run_chat,
    streamed_text,
)

# Measured on main at 6e5c4b8, before any switch code. A new value here means the eval
# cache goes cold: the tool list and the prompt text are both part of the cache key.
TOOL_LIST_SHA256 = "50068bedc3765b49546a0b9172af8d4e6874e6025100d81deb8d377dedd806b2"
ANSWER_PROMPT_SHA256 = "f96532cd7bf20cbab574743980e6e701652fdf1746d24a7db8507db9b5ca3d31"
ROUTER_PROMPT_SHA256 = "d7c3b299093e0ae57f0f7b9a79f25f6b25fc156240ffa6235a41f726bd5562c1"
CONVERSATIONAL_PROMPT_SHA256 = "a55e482850da908a6b3f910b76e6ff8d67d7af3c262166b08454f064a85b9c36"

ALL_TOOLS = ["get_system_time", "get_internship_stats", "get_problem_index", "search_knowledge_base", "get_weather_and_aqi"]
WEATHER_QUESTION = "What is the weather in New Delhi?"
PLANTED_KEY = "planted fast path question"
PLANTED_ANSWER = "The planted stored answer."
WEATHER_ANSWER = "New Delhi is 30 degrees."

pinned = pytest.mark.switch_states("no_variable")


def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def bound_tools(binding):
    """The tools sent to the main model, read from the real binding and its fallback."""
    tools = binding.runnable.kwargs["tools"]
    assert binding.fallbacks[0].kwargs["tools"] == tools
    return tools


def weather_call_turn():
    """A qa_node step that calls the weather tool, as the main model does."""
    return FakeMessagesListChatModel(responses=[AIMessage(
        content="",
        tool_calls=[{"name": "get_weather_and_aqi", "args": {"location": "New Delhi"}, "id": "call_w"}],
    )])


def paused(graph, thread_id="thread-1"):
    return asyncio.run(graph.aget_state({"configurable": {"thread_id": thread_id}})).next


def has_panel_event(chunks):
    return any(e.get("event") == "on_agent_interrupt" for e in parse_events(chunks))


def resume(graph, thread_id="thread-1"):
    async def collect():
        return [c async for c in chat.resume_graph_stream(thread_id, graph)]

    return asyncio.run(collect())


class FakeWeatherResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "results": [{"latitude": 28.6, "longitude": 77.2, "name": "New Delhi"}],
            "current_weather": {"temperature": 30, "windspeed": 5},
            "current": {"pm10": 40, "pm2_5": 20},
        }


@pytest.fixture
def weather_requests(monkeypatch):
    """Replaces the tool's HTTP calls and records them."""
    urls = []

    def fake_get(url, *args, **kwargs):
        urls.append(url)
        return FakeWeatherResponse()

    monkeypatch.setattr(weather_aqi.requests, "get", fake_get)
    return urls


@pytest.fixture
def app_module(monkeypatch):
    """backend.app opens Postgres at import (app.py:56), so that one call is replaced first."""
    monkeypatch.setattr(memory, "setup_database_tables", lambda: None)
    import backend.app

    return backend.app


@pytest.fixture
def rate_limit_calls(app_module, monkeypatch):
    calls = []

    def fake_check_rate_limit(request):
        calls.append(request)
        return None

    monkeypatch.setattr(app_module, "check_rate_limit", fake_check_rate_limit)
    return calls


def refine(app_module, text):
    return asyncio.run(app_module.refine_transcript(app_module.RefineRequest(transcript=text), object()))


# ------------------------------------------------------------------
# The variable
# ------------------------------------------------------------------
@pytest.mark.parametrize("value, expected", [
    (None, True),
    ("", True),
    ("   ", True),
    ("true", True),
    ("off", True),
    ("false", False),
    ("FALSE", False),
    (" false ", False),
])
def test_only_false_turns_a_switch_off(monkeypatch, value, expected):
    if value is not None:
        monkeypatch.setenv("FAST_PATH_ENABLED", value)
    assert config.fast_path_enabled() is expected


@pytest.mark.parametrize("name, reader", [
    ("FAST_PATH_ENABLED", config.fast_path_enabled),
    ("TRANSCRIPT_REFINE_ENABLED", config.transcript_refine_enabled),
    ("WEATHER_TOOL_ENABLED", config.weather_tool_enabled),
])
def test_each_switch_reads_its_own_variable(monkeypatch, name, reader):
    monkeypatch.setenv(name, "false")
    readers = [config.fast_path_enabled, config.transcript_refine_enabled, config.weather_tool_enabled]
    assert [r() for r in readers] == [r is not reader for r in readers]


def test_eval_sets_every_switch_before_the_backend_loads():
    """Read as text: importing eval.py installs a global SQLite cache and builds the judge client."""
    source = (Path(__file__).parents[1] / "evals" / "eval.py").read_text(encoding="utf-8")
    before_imports = source[:source.index("from backend.")]
    assert 'os.environ.setdefault(_switch, "true")' in before_imports
    for name in SWITCH_NAMES:
        assert f'"{name}"' in before_imports


# ------------------------------------------------------------------
# No variable set: byte-identical to main, so the eval cache stays warm
# ------------------------------------------------------------------
def test_no_variable_keeps_the_bound_tool_list():
    tools = bound_tools(agents.llm_with_tools)
    assert sha256(json.dumps(tools, sort_keys=True)) == TOOL_LIST_SHA256
    assert [t["function"]["name"] for t in tools] == ALL_TOOLS


@pinned
def test_no_variable_keeps_the_answer_prompt(core):
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))

    run_chat(core.graph, QUESTION)

    assert sha256(core.qa.calls[0][0].content) == ANSWER_PROMPT_SHA256


@pinned
def test_no_variable_keeps_the_router_and_conversational_prompts(core, monkeypatch):
    seen = []

    class RecordingModel(StrictFakeMessagesListChatModel):
        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            seen.append(messages[0].content)
            return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

    monkeypatch.setattr(agents, "fast_llm", RecordingModel(
        responses=[AIMessage(content="CONVERSATIONAL"), AIMessage(content="Hello.")],
    ))
    core.set_qa(ScriptedModel())

    run_chat(core.graph, "hello there")

    assert [sha256(text) for text in seen] == [ROUTER_PROMPT_SHA256, CONVERSATIONAL_PROMPT_SHA256]


# ------------------------------------------------------------------
# Fast path
# ------------------------------------------------------------------
@pinned
def test_fast_path_off_sends_a_table_question_down_the_normal_route(core, monkeypatch):
    monkeypatch.setenv("FAST_PATH_ENABLED", "false")
    monkeypatch.setattr(semantic_router, "FAST_PATH_INTERCEPTS", {PLANTED_KEY: {"output": PLANTED_ANSWER, "target_id": "planted_id"}})
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(PLANTED_KEY, ANSWER))

    chunks = run_chat(core.graph, PLANTED_KEY)

    assert streamed_text(chunks) == ANSWER
    assert len(core.qa.calls) == 2
    assert [m.type for m in checkpoint_messages(core.graph)] == ["human", "ai", "tool", "ai"]
    assert RETRIEVED_TEXT in checkpoint_messages(core.graph)[2].content


@pinned
def test_fast_path_off_sends_a_problem_id_question_down_the_normal_route(core, monkeypatch):
    def block_lookup_must_not_run(problem_id):
        raise AssertionError("the Problem-N block lookup ran with the fast path off")

    monkeypatch.setenv("FAST_PATH_ENABLED", "false")
    monkeypatch.setattr(config, "extract_problem_block", block_lookup_must_not_run)
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))

    chunks = run_chat(core.graph, "Tell me about Problem 7")

    assert streamed_text(chunks) == ANSWER
    assert len(core.qa.calls) == 2
    assert core.fast_llm.calls == 1


# ------------------------------------------------------------------
# Transcript refine
# ------------------------------------------------------------------
@pinned
def test_refine_off_returns_the_raw_text_with_no_model_call(core, app_module, rate_limit_calls, monkeypatch):
    monkeypatch.setenv("TRANSCRIPT_REFINE_ENABLED", "false")
    core.set_fast_replies()

    result = refine(app_module, "raw  words from the mic")

    assert result == {"refined_transcript": "raw  words from the mic"}
    # The script is empty, so a model call raises before `calls` moves and only extra_calls records it.
    assert core.fast_llm.extra_calls == 0
    assert rate_limit_calls == []


@pinned
def test_refine_on_calls_the_model_and_counts_the_request(core, app_module, rate_limit_calls):
    core.set_fast_replies("  Refined words.  ")

    result = refine(app_module, "raw words")

    assert result == {"refined_transcript": "Refined words."}
    assert core.fast_llm.calls == 1
    assert len(rate_limit_calls) == 1


# ------------------------------------------------------------------
# Weather tool with approval
# ------------------------------------------------------------------
def test_weather_off_binding_lists_every_other_tool_in_order():
    assert [t["function"]["name"] for t in bound_tools(agents.llm_without_weather)] == ALL_TOOLS[:-1]


@pinned
def test_weather_off_question_answers_with_no_panel_on_the_other_binding_and_prompt_line(core, monkeypatch, weather_requests):
    monkeypatch.setenv("WEATHER_TOOL_ENABLED", "false")
    core.set_fast_replies("IN_SCOPE")
    model = ScriptedModel(answer_turn(ANSWER))
    core.set_qa(ScriptedModel())  # both bindings refuse, then the off binding gets the real script
    monkeypatch.setattr(agents, "llm_without_weather", model)

    chunks = run_chat(core.graph, WEATHER_QUESTION)

    assert streamed_text(chunks) == ANSWER
    assert not has_panel_event(chunks)
    assert paused(core.graph) == ()
    assert weather_requests == []
    prompt = model.calls[0][0].content
    assert agents.WEATHER_OFF_LINE in prompt
    assert "get_weather_and_aqi" not in prompt


@pinned
def test_weather_off_ignores_a_weather_call_the_model_invents(core, monkeypatch, weather_requests):
    monkeypatch.setenv("WEATHER_TOOL_ENABLED", "false")
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(ScriptedModel(weather_call_turn(), answer_turn(ANSWER)))

    chunks = run_chat(core.graph, WEATHER_QUESTION)

    assert streamed_text(chunks) == ANSWER
    assert not has_panel_event(chunks)
    assert paused(core.graph) == ()
    assert weather_requests == []
    tool_messages = [m for m in checkpoint_messages(core.graph) if isinstance(m, ToolMessage)]
    assert len(tool_messages) == 1 and "not a valid tool" in tool_messages[0].content


@pinned
def test_thread_paused_before_the_switch_went_off_answers_without_the_tool(core, monkeypatch, weather_requests):
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(ScriptedModel(weather_call_turn()))
    first = run_chat(core.graph, WEATHER_QUESTION)
    assert has_panel_event(first) and paused(core.graph) == ("sensitive_tools",)

    monkeypatch.setenv("WEATHER_TOOL_ENABLED", "false")
    core.set_qa(ScriptedModel(answer_turn(ANSWER)))
    chunks = resume(core.graph)

    assert streamed_text(chunks) == ANSWER
    assert not has_panel_event(chunks)
    assert weather_requests == [] and NETWORK_ATTEMPTS == []
    stored = checkpoint_messages(core.graph)
    assert [m.type for m in stored] == ["human", "ai", "tool", "ai"]
    assert stored[2].content == weather_aqi.WEATHER_OFF_RESULT
    assert stored[2].tool_call_id == "call_w"


@pinned
def test_no_variable_weather_question_pauses_and_approval_answers(core, monkeypatch, weather_requests):
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(ScriptedModel(weather_call_turn(), answer_turn(WEATHER_ANSWER)))
    monkeypatch.setattr(agents, "llm_without_weather", ScriptedModel())  # refuses if qa_node picks it

    first = run_chat(core.graph, WEATHER_QUESTION)

    assert has_panel_event(first)
    assert paused(core.graph) == ("sensitive_tools",)
    assert weather_requests == []

    chunks = resume(core.graph)

    assert streamed_text(chunks) == WEATHER_ANSWER
    assert len(weather_requests) == 3
    tool_message = checkpoint_messages(core.graph)[2]
    assert tool_message.type == "tool" and tool_message.content.startswith("Location: New Delhi")
