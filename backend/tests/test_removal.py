# backend/tests/test_removal.py
"""A removal test per optional feature: delete it from a copy, then run the core tests there.

The env switches leave the code in place, so a switched-off run cannot show that the
code can go. So each test copies backend/ to a temporary folder, applies a recipe (the
real deletions, as the plan's removal method does them), and runs the core tests on the
copy in a new process, where conftest.py applies its import-time fakes as usual.

Nothing here edits the working tree. Each recipe edit must find its text exactly once,
so a recipe goes stale loudly. A recipe proves the removal it writes down, and no other.
See DECISIONS.md, "What a removal test proves".

Four checks stop a test from passing with the feature still present:
1. The probe reports each sign of the feature; all gone is "absent", all there is
   "present", and any other mix fails.
2. The same probes on an unedited copy must report "present".
3. Each run must hold exactly the unedited run's cases, less the ones the recipe names.
   A stale name is silent in pytest, so the names are checked against that run.
4. The probe holds what the recipe's named tests would have shown about core: the
   answer through the route, and for title generation, the row and a second turn.
"""
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pytest

REPO = Path(__file__).parents[2]

# test_core_switches.py pins the features themselves: their tool list, prompts and hashes.
CORE_FILES = (
    "test_core_chat.py",
    "test_core_graph.py",
    "test_core_pre_steps.py",
    "test_core_registry.py",
    "test_core_routes.py",
)
OUTCOME_FILE = "removal_outcome.txt"
PROBE_ID = "backend.tests.test_removal_probe_{feature}::test_probe[no_variable]"

PROBE_HEADER = '''
import asyncio
import importlib.util
import inspect
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage

import backend.core.tools
from backend import memory
from backend.core import agents, chat, config, semantic_router
from backend.core.tools import search
from conftest import ANSWER, DONE, QUESTION, ScriptedModel, checkpoint_messages, rag_script, run_chat, streamed_text
from test_core_routes import call_chat_approve, call_chat_stream, routes

pytestmark = pytest.mark.switch_states("no_variable")


def report(feature, signs, core_works):
    """Writes one line. A sign is True while the feature is there."""
    in_copy = Path(memory.__file__).resolve().is_relative_to(Path.cwd().resolve())
    if all(signs.values()):
        label = "present"
    elif not any(signs.values()):
        label = "absent"
    else:
        label = "mixed " + ",".join(name for name, there in signs.items() if there)
    core = "works" if core_works and in_copy else "broken"
    with open("removal_outcome.txt", "a", encoding="utf-8") as outcome:
        outcome.write(f"{feature}={label} core={core}\\n")


def bound_tool_names():
    """Read before set_qa, which replaces the binding with a fake."""
    return [t["function"]["name"] for t in agents.llm_with_tools.runnable.kwargs["tools"]]


def module_exists(name):
    return importlib.util.find_spec(name) is not None


def paths(app_module):
    return [route.path for route in app_module.app.routes]


def core_routes_work(app_module, chunks):
    return ANSWER in streamed_text(chunks) and chunks[-1] == DONE and "/chat_stream" in paths(app_module)
'''


# ------------------------------------------------------------------
# The edits a recipe is made of
# ------------------------------------------------------------------
class StaleRecipe(AssertionError):
    pass


def _found_once(root, relative, text):
    path = root / relative
    count = path.read_text(encoding="utf-8").count(text)
    if count != 1:
        raise StaleRecipe(f"expected this text once in {relative}, found {count}; update the recipe:\n{text}")
    return path


def replace(root, relative, old, new=""):
    path = _found_once(root, relative, old)
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


def cut(root, relative, start, stop=None, new=""):
    """Replaces from `start` up to the first `stop` after it, or to the end of the file."""
    path = _found_once(root, relative, start)
    text = path.read_text(encoding="utf-8")
    begin = text.index(start)
    if stop is None:
        end = len(text)
    elif stop in text[begin:]:
        end = text.index(stop, begin)
    else:
        raise StaleRecipe(f"no end marker after the start in {relative}; update the recipe:\n{stop}")
    path.write_text(text[:begin] + new + text[end:], encoding="utf-8")


def delete(root, relative):
    path = root / relative
    if not path.exists():
        raise StaleRecipe(f"{relative} does not exist; update the recipe")
    path.unlink()


# ------------------------------------------------------------------
# The recipes
# ------------------------------------------------------------------
def remove_weather(root):
    """The tool and its approval: nothing is left to approve, so the route and the resume go too."""
    delete(root, "backend/core/tools/weather_aqi.py")
    tools = "backend/core/tools/__init__.py"
    replace(root, tools, "from .weather_aqi import get_weather_and_aqi\n")
    replace(root, tools, "    get_weather_and_aqi,\n")

    agents = "backend/core/agents.py"
    replace(root, agents, ", weather_tool_enabled\n", "\n")
    cut(root, agents, "safe_tools = [t for t", "WEATHER_OFF_LINE = ", "safe_tools = list(tools)\n\n")
    replace(root, agents, "    weather_on = weather_tool_enabled()\n")
    # The off line stays: router RULE 2 still lets a weather question through, and this line stops an invented figure.
    replace(root, agents, '            f"{WEATHER_TOOL_LINE if weather_on else WEATHER_OFF_LINE}"\n', '            f"{WEATHER_OFF_LINE}"\n')
    replace(
        root, agents,
        "    model = llm_with_tools if weather_on else llm_without_weather\n    response = await model.ainvoke(messages)",
        "    response = await llm_with_tools.ainvoke(messages)",
    )
    cut(root, agents, '    for tc in last_message.tool_calls:\n        if tc["name"] == "get_weather_and_aqi"', '    return "safe_tools"\n')
    replace(root, agents, 'workflow.add_node("sensitive_tools", ToolNode(tools=sensitive_tools))\n')
    replace(root, agents, '        "sensitive_tools": "sensitive_tools",\n')
    replace(root, agents, 'workflow.add_edge("sensitive_tools", "qa_node")\n')
    replace(root, agents, 'checkpointer=checkpointer, interrupt_before=["sensitive_tools"])', "checkpointer=checkpointer)")

    app = "backend/app.py"
    replace(root, app, 'checkpointer=memory, interrupt_before=["sensitive_tools"])', "checkpointer=memory)")
    replace(root, app, "generate_chat_responses, resume_graph_stream\n", "generate_chat_responses\n")
    cut(root, app, "class ActionRequest(BaseModel):", "# ==========================================\n# 6. MEMORY")
    replace(root, app, "        is_interrupted = False\n")
    replace(root, app, '            if "on_agent_interrupt" in chunk:\n                is_interrupted = True\n')
    replace(
        root, app,
        '                if not is_interrupted:\n                    latency = time.time() - start\n'
        '                    timing_msg = f"\\n\\n*⚡ Query processed in {latency:.2f}s*"\n'
        "                    yield f\"data: {json.dumps({'event': 'on_chat_model_stream', 'name': 'latency', 'data': {'chunk': {'content': timing_msg}}})}\\n\\n\"\n",
        '                latency = time.time() - start\n'
        '                timing_msg = f"\\n\\n*⚡ Query processed in {latency:.2f}s*"\n'
        "                yield f\"data: {json.dumps({'event': 'on_chat_model_stream', 'name': 'latency', 'data': {'chunk': {'content': timing_msg}}})}\\n\\n\"\n",
    )

    chat = "backend/core/chat.py"
    cut(root, chat, "async def resume_graph_stream(")
    cut(root, chat, "        # Check if the graph is currently interrupted\n", '        print(f"🔧 [__DEV__] Query: \'{user_message}\' | Latency: {time.time() - start_time:.2f}s | Response: \'{full_response')

    config = "backend/core/config.py"
    replace(root, config, 'def weather_tool_enabled() -> bool:\n    return _switch_on("WEATHER_TOOL_ENABLED")\n\n\n')
    replace(root, config, ", weather tool {weather_tool_enabled()}")

    conftest = "backend/tests/conftest.py"
    replace(root, conftest, '        monkeypatch.setattr(agents, "llm_without_weather", model)\n')
    replace(root, conftest, 'checkpointer=FkMemorySaver(registry), interrupt_before=["sensitive_tools"])', "checkpointer=FkMemorySaver(registry))")


WEATHER_PROBE = '''
def test_probe(core, routes):
    names = bound_tool_names()
    core.set_qa(rag_script(QUESTION, ANSWER))
    chunks = call_chat_stream(routes)
    report("weather", {
        "tool_bound": "get_weather_and_aqi" in names,
        "module": module_exists("backend.core.tools.weather_aqi"),
        "node": "sensitive_tools" in agents.workflow.nodes,
        "approve_route": "/chat_approve" in paths(routes),
        "resume_function": hasattr(chat, "resume_graph_stream"),
        "prompt_line": "get_weather_and_aqi" in core.qa.calls[0][0].content,
        "no_off_line": agents.WEATHER_OFF_LINE not in core.qa.calls[0][0].content,
        "switch_reader": hasattr(config, "weather_tool_enabled"),
        "startup_line": "weather tool" in Path(config.__file__).read_text(encoding="utf-8"),
        "app_interrupt_branch": "on_agent_interrupt" in inspect.getsource(routes.chat_stream),
        "chat_interrupt_branch": "on_agent_interrupt" in inspect.getsource(chat.generate_chat_responses),
    }, core_routes_work(routes, chunks))
'''


def remove_system_time(root):
    delete(root, "backend/core/tools/system.py")
    tools = "backend/core/tools/__init__.py"
    replace(root, tools, "from .system import get_system_time\n")
    replace(root, tools, "    get_system_time,\n")


SYSTEM_TIME_PROBE = '''
def test_probe(core, routes):
    names = bound_tool_names()
    core.set_qa(rag_script(QUESTION, ANSWER))
    chunks = call_chat_stream(routes)
    report("system_time", {
        "tool_bound": "get_system_time" in names,
        "module": module_exists("backend.core.tools.system"),
        "exported": hasattr(backend.core.tools, "get_system_time"),
    }, core_routes_work(routes, chunks))
'''


PROBLEM_ID_PAYLOAD_TEST = '''def test_fast_path_payload_carries_only_the_last_message(monkeypatch):
    monkeypatch.setattr(backend_config, "extract_problem_block", lambda problem_id: PROBLEM_BLOCK)
    query = "Tell me about Problem 7"
    state = {"messages": [HumanMessage(content="first"), AIMessage(content="reply"), HumanMessage(content=query)]}

    send = asyncio.run(agents.route_input_node(state))

    assert [m.content for m in send.arg["messages"]] == [query]


'''


def remove_fast_path_table(root):
    """The table only. The switch, route_query and fast_path_node stay, because Problem-N shares them until item 12.

    The two Problem-N tests stay in the run, to prove that. They name the table fixture
    only to keep the table out of their way, so they lose that one name here.
    """
    delete(root, "backend/core/fast_path_routes.py")
    delete(root, "backend/evals/check_fast_path.py")
    router = "backend/core/semantic_router.py"
    replace(root, router, "from backend.core.fast_path_routes import FAST_PATH_INTERCEPTS\n")
    cut(root, router, "    # 1. Exact Match Intercepts", "    # Also handle problem ID fast path")
    graph_tests = "backend/tests/test_core_graph.py"
    replace(root, graph_tests, "def test_problem_id_hit_routes_once(core, route_calls, planted_table, monkeypatch):", "def test_problem_id_hit_routes_once(core, route_calls, monkeypatch):")
    replace(root, graph_tests, "def test_rag_question_after_a_problem_id_hit_sends_a_valid_list(core, planted_table, monkeypatch):", "def test_rag_question_after_a_problem_id_hit_sends_a_valid_list(core, monkeypatch):")
    # The Send payload stays too, so its test keeps running, through the route that stays.
    cut(root, graph_tests, "def test_fast_path_payload_carries_only_the_last_message(planted_table):", "def test_rag_prompt_hint_text_stays_the_same(core):", PROBLEM_ID_PAYLOAD_TEST)


FAST_PATH_TABLE_PROBE = '''
# A real key of the table, with no problem id, so only the table can answer it.
TABLE_KEY = "file upload bug"


def test_probe(core, routes):
    route = asyncio.run(semantic_router.route_query(TABLE_KEY))
    core.set_qa(rag_script(QUESTION, ANSWER))
    chunks = call_chat_stream(routes)
    report("fast_path_table", {
        "module": module_exists("backend.core.fast_path_routes"),
        "table": hasattr(semantic_router, "FAST_PATH_INTERCEPTS"),
        "stored_answer": route["route_category"] == "FAST_PATH",
    }, core_routes_work(routes, chunks))
'''


def remove_refine(root):
    app = "backend/app.py"
    cut(root, app, "class RefineRequest(BaseModel):", '@app.get("/")')
    config = "backend/core/config.py"
    replace(root, config, 'def transcript_refine_enabled() -> bool:\n    return _switch_on("TRANSCRIPT_REFINE_ENABLED")\n\n\n')
    replace(root, config, "transcript refine {transcript_refine_enabled()}, ")


REFINE_PROBE = '''
def test_probe(core, routes):
    core.set_qa(rag_script(QUESTION, ANSWER))
    chunks = call_chat_stream(routes)
    report("refine", {
        "route": "/refine_transcript" in paths(routes),
        "request_model": hasattr(routes, "RefineRequest"),
        "switch_reader": hasattr(config, "transcript_refine_enabled"),
        "startup_line": "transcript refine" in Path(config.__file__).read_text(encoding="utf-8"),
    }, core_routes_work(routes, chunks) and "/history" in paths(routes))
'''


def remove_query_expansion(root):
    search = "backend/core/tools/search.py"
    cut(root, search, "expansion_llm = ChatOpenAI(", "@tool\nasync def search_knowledge_base")
    cut(root, search, "    direct_match = re.search(", "    all_queries = [", "    search_variants = []\n\n")
    replace(root, "backend/tests/conftest.py", '    monkeypatch.setattr(search, "expansion_llm", expansion_llm)\n')


QUERY_EXPANSION_PROBE = '''
def test_probe(core, routes):
    core.set_qa(rag_script(QUESTION, ANSWER))
    chunks = call_chat_stream(routes)
    report("query_expansion", {
        "client": hasattr(search, "expansion_llm"),
        "expanded_search": any("EXPANSIONMARKER" in query for query in core.retriever.queries),
    }, core_routes_work(routes, chunks) and QUESTION in core.retriever.queries)
'''


def remove_title_generation(root):
    """The model-made title. The registry INSERT is core and stays, with its fallback title."""
    memory = "backend/memory.py"
    cut(root, memory, "async def generate_title_from_llm(", "async def register_thread(")
    cut(root, memory, "# The event loop keeps only a weak reference", "async def get_thread_owner(")
    chat = "backend/core/chat.py"
    replace(root, chat, "from backend.memory import register_thread, start_title_generation", "from backend.memory import register_thread")
    replace(root, chat, "    if created:\n        start_title_generation(turn.async_pool, turn.thread_id, turn.user_message)\n")
    conftest = "backend/tests/conftest.py"
    replace(root, conftest, '    monkeypatch.setattr(chat, "start_title_generation", fake_start_title_generation)\n')
    replace(root, conftest, '        monkeypatch.setattr(chat, "start_title_generation", memory.start_title_generation)\n')
    replace(root, conftest, "    # A test that failed before run_chat drained its title task leaves it here; never carry it over\n    memory._title_tasks.clear()\n")
    replace(root, conftest, "        while memory._title_tasks:\n            await asyncio.gather(*memory._title_tasks)\n")


TITLE_GENERATION_PROBE = '''
class TitleModel:
    def __init__(self):
        self.calls = []

    async def ainvoke(self, messages, config=None, **kwargs):
        self.calls.append(messages)
        return AIMessage(content="Probe Title")


SECOND_QUESTION = "Which model does the reranker use?"
SECOND_ANSWER = "It uses a cross-encoder."
FALLBACK_TITLE = QUESTION[:40] + "..."


def test_probe(core, routes):
    """Through the real registry: the core fixture replaces the title function otherwise. Two turns on one thread."""
    title_model = TitleModel()
    core.use_real_registry(title_model)
    core.set_fast_replies("IN_SCOPE", "IN_SCOPE")
    core.set_qa(ScriptedModel(*rag_script(QUESTION, ANSWER).models, *rag_script(SECOND_QUESTION, SECOND_ANSWER).models))
    first = run_chat(core.graph, QUESTION, pool=core.registry)
    second = run_chat(core.graph, SECOND_QUESTION, pool=core.registry)
    row = core.registry.rows.get("thread-1", {})
    saved = [m.type for m in checkpoint_messages(core.graph)]
    title_is_right = row.get("title") == ("Probe Title" if title_model.calls else FALLBACK_TITLE)
    answers_are_right = streamed_text(first) == ANSWER and streamed_text(second) == SECOND_ANSWER
    report("title_generation", {
        "start_function": hasattr(memory, "start_title_generation"),
        "model_function": hasattr(memory, "generate_title_from_llm"),
        "chat_call": hasattr(chat, "start_title_generation"),
        "model_called": bool(title_model.calls),
        "model_title_saved": row.get("title") == "Probe Title",
    }, row.get("owner_id") == "owner-1" and title_is_right and answers_are_right and saved == ["human", "ai", "tool", "ai"] * 2)
'''


def remove_latency_footer(root):
    app = "backend/app.py"
    cut(
        root, app, "    async def timed_generator():\n", "    return StreamingResponse(\n        timed_generator(),",
        "    async def timed_generator():\n"
        "        async for chunk in generate_chat_responses(request.message, request.thread_id, graph, async_pool, owner_id):\n"
        "            yield chunk\n\n",
    )
    cut(
        root, app, "            import time, json\n            start = time.time()\n            async for chunk in resume_graph_stream",
        "                yield chunk\n",
        "            async for chunk in resume_graph_stream(request.thread_id, graph):\n",
    )


LATENCY_FOOTER_PROBE = '''
@pytest.mark.expected_skips(lines=["🚨 resume_graph_stream Crash Details:"], failed_requests=1)
def test_probe(core, routes):
    core.set_qa(rag_script(QUESTION, ANSWER))
    chunks = call_chat_stream(routes)
    approve_chunks = call_chat_approve(routes)
    report("latency_footer", {
        "chat_stream_footer": "Query processed in" in streamed_text(chunks),
        "chat_approve_footer": "Query resumed" in streamed_text(approve_chunks),
    }, core_routes_work(routes, chunks) and approve_chunks[-1] == DONE)
'''


@dataclass(frozen=True)
class Recipe:
    feature: str
    remove: Callable[[Path], None]
    probe: str
    # (core file, test function): the tests of the feature itself, which go with it.
    goes_with_feature: tuple = ()


RECIPES = (
    Recipe("weather", remove_weather, WEATHER_PROBE, (
        ("test_core_routes", "test_chat_approve_route_ends_a_thread_with_nothing_to_resume"),
    )),
    Recipe("system_time", remove_system_time, SYSTEM_TIME_PROBE),
    Recipe("fast_path_table", remove_fast_path_table, FAST_PATH_TABLE_PROBE, (
        ("test_core_graph", "test_fast_path_hit_keeps_the_target_id_marker"),
        ("test_core_graph", "test_fast_path_table_hit_routes_once"),
        ("test_core_graph", "test_rag_question_after_a_table_hit_sends_a_valid_list"),
    )),
    Recipe("refine", remove_refine, REFINE_PROBE),
    Recipe("query_expansion", remove_query_expansion, QUERY_EXPANSION_PROBE, (
        ("test_core_chat", "test_query_expansion_text_stays_out_of_the_stream"),
    )),
    # The probe holds the core half of these: the row, the checkpoint and the answer.
    Recipe("title_generation", remove_title_generation, TITLE_GENERATION_PROBE, (
        ("test_core_pre_steps", "test_save_step_passes_on_and_starts_the_title_for_a_new_thread"),
        ("test_core_pre_steps", "test_save_step_passes_on_without_a_title_for_an_existing_thread"),
        ("test_core_registry", "test_core_path_starts_the_title_once"),
        ("test_core_registry", "test_failing_title_model_keeps_the_fallback_title_and_the_answer"),
        ("test_core_registry", "test_new_thread_is_registered_and_gets_the_model_title"),
        ("test_core_registry", "test_raising_title_function_does_not_fail_the_turn"),
        ("test_core_registry", "test_second_turn_skips_the_title_and_keeps_the_thread"),
        ("test_core_registry", "test_title_task_that_cannot_start_does_not_fail_the_turn"),
    )),
    Recipe("latency_footer", remove_latency_footer, LATENCY_FOOTER_PROBE),
)


# ------------------------------------------------------------------
# Running a copy
# ------------------------------------------------------------------
@dataclass(frozen=True)
class CopyRun:
    cases: dict  # case id -> "passed", "xfailed", "skipped" or "failed"
    outcomes: tuple  # the lines the probes wrote
    log: str


def _skip_copy(directory, names):
    """Python source only: backend/ also holds the vector store, which is large and unused here."""
    return [
        name for name in names
        if name in ("chroma_db", "docstore", "__pycache__")
        or ((Path(directory) / name).is_file() and not name.endswith(".py"))
    ]


def make_copy(root):
    shutil.copytree(REPO / "backend", root / "backend", ignore=_skip_copy)
    shutil.copy(REPO / "pyproject.toml", root / "pyproject.toml")


def _case_status(case):
    if case.find("failure") is not None or case.find("error") is not None:
        return "failed"
    skipped = case.find("skipped")
    if skipped is not None:
        return "xfailed" if skipped.get("type") == "pytest.xfail" else "skipped"
    return "passed"


def run_copy(root, recipes, leave_out=()):
    """Runs the core files and each recipe's probe in a new process, with the copy as its working folder."""
    for recipe in recipes:
        (root / f"backend/tests/test_removal_probe_{recipe.feature}.py").write_text(PROBE_HEADER + recipe.probe, encoding="utf-8")
    selected = [f"backend/tests/{name}" for name in CORE_FILES]
    selected += [f"backend/tests/test_removal_probe_{recipe.feature}.py" for recipe in recipes]
    for module, function in leave_out:
        selected += ["--deselect", f"backend/tests/{module}.py::{function}"]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    report = root / "report.xml"
    done = subprocess.run(
        [sys.executable, "-m", "pytest", "--confcutdir=backend/tests", "-q", "--tb=short", f"--junitxml={report}", *selected],
        cwd=root, env=env, capture_output=True, text=True, timeout=300,
    )
    log = (done.stdout + done.stderr)[-3000:]
    assert report.exists(), f"pytest wrote no report (exit {done.returncode}):\n{log}"
    cases = {
        f"{case.get('classname')}::{case.get('name')}": _case_status(case)
        for case in ET.parse(report).getroot().iter("testcase")
    }
    outcome_file = root / OUTCOME_FILE
    outcomes = tuple(outcome_file.read_text(encoding="utf-8").splitlines()) if outcome_file.exists() else ()
    return CopyRun(cases, outcomes, log)


@pytest.fixture(scope="module")
def unedited(tmp_path_factory):
    """The same core files and every probe, with nothing removed. The baseline for each recipe."""
    root = tmp_path_factory.mktemp("removal_unedited")
    make_copy(root)
    return run_copy(root, RECIPES)


def _function_of(case_id):
    return case_id.split("::")[1].split("[")[0]


def _module_of(case_id):
    return case_id.split("::")[0].rpartition(".")[2]


def _is_probe(case_id):
    return _module_of(case_id).startswith("test_removal_probe_")


def test_unedited_copy_reports_every_feature_present(unedited):
    bad = {case: status for case, status in unedited.cases.items() if status not in ("passed", "xfailed")}
    assert not bad, f"{bad}\n{unedited.log}"
    assert sorted(unedited.outcomes) == sorted(f"{r.feature}=present core=works" for r in RECIPES), unedited.log
    assert sum(not _is_probe(case) for case in unedited.cases) > 100, "the core files lost most of their cases"


@pytest.mark.parametrize("recipe", RECIPES, ids=lambda r: r.feature)
def test_core_works_with_the_feature_deleted(recipe, unedited, tmp_path):
    make_copy(tmp_path)
    recipe.remove(tmp_path)
    run = run_copy(tmp_path, [recipe], recipe.goes_with_feature)

    # A name in the list that matches no test is silent in pytest, so it is checked here.
    core_cases = {case: status for case, status in unedited.cases.items() if not _is_probe(case)}
    known = {(_module_of(case), _function_of(case)) for case in core_cases}
    stale = set(recipe.goes_with_feature) - known
    assert not stale, f"goes_with_feature names no test: {sorted(stale)}"

    expected = {
        case: status for case, status in core_cases.items()
        if (_module_of(case), _function_of(case)) not in recipe.goes_with_feature
    }
    expected[PROBE_ID.format(feature=recipe.feature)] = "passed"
    wrong = {
        case: (expected.get(case, "not expected"), run.cases.get(case, "did not run"))
        for case in expected.keys() | run.cases.keys()
        if expected.get(case) != run.cases.get(case)
    }
    assert not wrong, f"case: (expected, got): {wrong}\n{run.log}"
    # A case that fails on both sides matches above, so a failure is checked on its own.
    bad = {case: status for case, status in run.cases.items() if status not in ("passed", "xfailed")}
    assert not bad, f"{bad}\n{run.log}"
    assert run.outcomes == (f"{recipe.feature}=absent core=works",), f"{run.outcomes}\n{run.log}"
