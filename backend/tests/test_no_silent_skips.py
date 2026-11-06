# backend/tests/test_no_silent_skips.py
"""No silent skips: the check on every test, the count at every site, and /health.

The autouse fixture no_silent_skips (conftest.py) fails any test that prints a skip line
or raises a skip count it did not name. So each site test below only forces its fault and
names the line and the rise; the fixture does the counting check. Sites the tests of
other files cover: memory.py's three title sites (test_core_registry.py), the failed turn
in chat.py (test_core_chat.py, test_core_pre_steps.py) and the failed resume
(test_core_routes.py).

Everything runs on fakes, so a clean run proves only the faked paths. This file is outside
test_removal.py's CORE_FILES: it tests the features the removal tests delete.
See DECISIONS.md, "What counts as a skip, and what the count does not show".
"""
import ast
import asyncio
import json
import subprocess
import sys
import threading
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import httpx
import openai
import pytest
from langchain_core.documents import Document

from backend import memory
from backend.core import agents, chat, config, ingest, skip_counter
from backend.core.skip_counter import KINDS, count_skip, skip_report
from backend.core.tools import search, weather_aqi
from conftest import (
    ANSWER,
    COUNTS_AFTER_IMPORT,
    IMPORT_SKIP_LINES,
    QUESTION,
    SKIP_LINES,
    SKIP_MARKERS,
    FailingModel,
    ScriptedModel,
    rag_script,
    run_chat,
    silent_skip_problems,
    streamed_text,
)
from test_core_routes import BROWSER_ID, call_chat_stream, routes  # noqa: F401
from test_removal import _case_status, make_copy

REPO = Path(__file__).parents[2]
one_state = pytest.mark.switch_states("no_variable")
PHOENIX_LINE = "⚠️ [WARNING] Failed to initialize Phoenix tracing: "


def raises(*args, **kwargs):
    raise RuntimeError("fake fault")


def run_search(query):
    return asyncio.run(search.search_knowledge_base.ainvoke({"query": query}))


# ------------------------------------------------------------------
# The check itself
# ------------------------------------------------------------------
def test_the_check_reports_each_kind_of_problem():
    line = "⚠️ [WARNING] something"
    assert silent_skip_problems([], {"request_skips": 0}) == []
    assert silent_skip_problems([line], {}, [line]) == []
    assert silent_skip_problems([line], {}) == [f"unexpected skip line: {line!r}"]
    assert silent_skip_problems([], {}, [line]) == [f"expected skip line never printed: {line!r}"]
    assert silent_skip_problems([], {"request_skips": 1}) == ["request_skips rose by 1, expected 0"]
    assert silent_skip_problems([], {"request_skips": 0}, (), {"request_skips": 1}) == ["request_skips rose by 0, expected 1"]


@pytest.mark.parametrize("text", ["[WARNING] a", "[ERROR] b", "🚨 c", "⚠️ d", "❌ e"])
def test_each_marker_counts_as_a_skip_line(text):
    assert SKIP_MARKERS.search(text)


@pytest.mark.parametrize("text", ["🔧 [__DEV__] Query", "✅ Connected", "🤖 Loading LLM model", "🎚️ Feature switches"])
def test_ordinary_log_lines_are_not_skip_lines(text):
    assert not SKIP_MARKERS.search(text)


def test_the_recorder_sees_a_print_from_a_thread_and_from_a_task():
    async def task():
        print("🚨 from a task")

    worker = threading.Thread(target=print, args=("🚨 from a thread",))
    worker.start()
    worker.join()
    asyncio.run(task())
    seen = list(SKIP_LINES)
    SKIP_LINES.clear()
    assert seen == ["🚨 from a thread", "🚨 from a task"]


PLANTED_TESTS = '''
import threading

import pytest

from backend.core.skip_counter import count_skip


def test_clean():
    print("an ordinary line")


def test_prints_a_skip_line():
    print("⚠️ [WARNING] planted")


def test_prints_a_skip_line_on_a_thread():
    worker = threading.Thread(target=print, args=("🚨 planted on a thread",))
    worker.start()
    worker.join()


def test_prints_a_skip_line_under_capsys(capsys):
    print("⚠️ [WARNING] planted")
    capsys.readouterr()


def test_raises_the_count():
    count_skip("request_skips")


@pytest.mark.expected_skips(lines=["⚠️ [WARNING] planted"], request_skips=1)
def test_names_what_it_does():
    print("⚠️ [WARNING] planted")
    count_skip("request_skips")


@pytest.mark.expected_skips(lines=["⚠️ [WARNING] planted"])
def test_names_a_line_that_never_prints():
    pass
'''


def test_a_real_pytest_run_fails_on_a_skip_line_and_passes_without_one(tmp_path):
    """The fixture itself, in a new process, on planted tests in a copy of backend/."""
    make_copy(tmp_path)
    (tmp_path / "backend/tests/test_planted.py").write_text(PLANTED_TESTS, encoding="utf-8")
    report = tmp_path / "report.xml"
    subprocess.run(
        [sys.executable, "-m", "pytest", "--confcutdir=backend/tests", "-q", f"--junitxml={report}", "backend/tests/test_planted.py"],
        cwd=tmp_path, capture_output=True, text=True, timeout=120,
    )
    statuses = {case.get("name"): _case_status(case) for case in ET.parse(report).getroot().iter("testcase")}
    assert statuses == {
        "test_clean": "passed",
        "test_prints_a_skip_line": "failed",
        "test_prints_a_skip_line_on_a_thread": "failed",
        "test_prints_a_skip_line_under_capsys": "failed",
        "test_raises_the_count": "failed",
        "test_names_what_it_does": "passed",
        "test_names_a_line_that_never_prints": "failed",
    }


def test_import_time_lines_are_only_the_phoenix_warning():
    """conftest.py blocks phoenix on purpose, so config.py's warning prints at every import, and only that one."""
    assert len(IMPORT_SKIP_LINES) == 1
    assert IMPORT_SKIP_LINES[0].startswith(PHOENIX_LINE)
    assert COUNTS_AFTER_IMPORT["startup_faults"] == 1
    assert COUNTS_AFTER_IMPORT["request_skips"] == 0
    assert COUNTS_AFTER_IMPORT["failed_requests"] == 0


# ------------------------------------------------------------------
# The counter
# ------------------------------------------------------------------
@pytest.mark.expected_skips(request_skips=1, startup_faults=1, failed_requests=1)
def test_count_skip_adds_one_to_its_own_kind():
    before = skip_report()
    for kind in KINDS:
        count_skip(kind)
    after = skip_report()
    assert {kind: after[kind] - before[kind] for kind in KINDS} == dict.fromkeys(KINDS, 1)


@pytest.mark.expected_skips(lines=["🚨 count_skip failed: KeyError: 'no_such_kind'"])
def test_count_skip_never_raises_and_names_the_failure():
    count_skip("no_such_kind")
    assert "no_such_kind" not in skip_report()


# ------------------------------------------------------------------
# A happy-path turn
# ------------------------------------------------------------------
@one_state
def test_a_happy_path_turn_leaves_the_count_unchanged(core):
    core.set_qa(rag_script(QUESTION, ANSWER))
    before = skip_report()

    chunks = run_chat(core.graph, QUESTION)

    after = skip_report()
    assert streamed_text(chunks) == ANSWER
    assert {kind: after[kind] for kind in KINDS} == {kind: before[kind] for kind in KINDS}


# ------------------------------------------------------------------
# /health
# ------------------------------------------------------------------
def call_health(app_module, monkeypatch):
    async def reachable():
        return "reachable"

    monkeypatch.setattr(app_module, "check_database", reachable)
    return asyncio.run(app_module.health_check(None))


@one_state
def test_health_keeps_its_fields_and_adds_numbers_only(core, routes, monkeypatch):  # noqa: F811
    health = call_health(routes, monkeypatch)
    skips = health.pop("skips")
    version = health.pop("version")
    assert isinstance(version, str)
    assert health == {
        "status": "online",
        "rag_hydrated": True,
        "ingestion_state": "done",
        "database": "reachable",
        "provider": "Hugging Face Spaces",
    }
    assert set(skips) == {*KINDS, "seconds_since_start"}
    assert all(type(value) is int and value >= 0 for value in skips.values())


@one_state
@pytest.mark.expected_skips(lines=["⚠️ [WARNING] Scope router failed"], request_skips=1)
def test_health_count_rises_with_a_skip_and_holds_no_error_text(core, routes, monkeypatch):  # noqa: F811
    class SecretFailure:
        async def ainvoke(self, messages, config=None, **kwargs):
            raise RuntimeError("SECRETTEXT from the provider")

    monkeypatch.setattr(agents, "fast_llm", SecretFailure())
    core.set_qa(rag_script(QUESTION, ANSWER))
    before = call_health(routes, monkeypatch)["skips"]["request_skips"]

    call_chat_stream(routes, message=QUESTION)

    health = call_health(routes, monkeypatch)
    assert health["skips"]["request_skips"] == before + 1
    assert "SECRETTEXT" not in json.dumps(health)
    assert QUESTION not in json.dumps(health)


@one_state
@pytest.mark.expected_skips(lines=["🚨 /health skip count failed: RuntimeError"])
def test_health_still_answers_when_the_count_fails(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(routes, "skip_report", raises)
    health = call_health(routes, monkeypatch)
    assert "skips" not in health
    assert health["status"] == "online"
    assert health["ingestion_state"] == "done"


@one_state
def test_health_reports_the_seconds_this_process_has_run(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(skip_counter.time, "monotonic", lambda: skip_counter._started_at + 42.9)
    assert call_health(routes, monkeypatch)["skips"]["seconds_since_start"] == 42


# ------------------------------------------------------------------
# request_skips: the app answers with less than it should
# ------------------------------------------------------------------
@one_state
@pytest.mark.expected_skips(lines=["⚠️ [WARNING] Scope router failed; defaulting to retrieval_node."], request_skips=1)
def test_scope_router_failure_counts(core, monkeypatch):
    monkeypatch.setattr(agents, "fast_llm", FailingModel())
    core.set_qa(rag_script(QUESTION, ANSWER))

    assert streamed_text(run_chat(core.graph, QUESTION)) == ANSWER


@one_state
@pytest.mark.expected_skips(lines=["🚨 [ERROR] expansion_llm.invoke failed: fake provider outage"], request_skips=1)
def test_query_expansion_failure_counts(core, monkeypatch):
    monkeypatch.setattr(search, "expansion_llm", FailingModel())
    assert "Rerankers score" in run_search(QUESTION)


@one_state
@pytest.mark.expected_skips(lines=["🚨 Error refining transcript: fake provider outage"], request_skips=1)
def test_refine_failure_counts(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(config, "fast_llm", FailingModel())
    response = asyncio.run(routes.refine_transcript(routes.RefineRequest(transcript="raw words"), object()))
    assert response == {"refined_transcript": "raw words"}


@pytest.mark.expected_skips(lines=["⚠️ [WARNING] get_weather_and_aqi failed: fake fault"], request_skips=1)
def test_weather_failure_counts(monkeypatch):
    monkeypatch.setattr(weather_aqi.requests, "get", raises)
    assert "An error occurred" in weather_aqi.get_weather_and_aqi.invoke({"location": "Delhi"})


# ------------------------------------------------------------------
# startup_faults. config.py's Phoenix site runs once, at import:
# test_import_time_lines_are_only_the_phoenix_warning covers it.
# ------------------------------------------------------------------
@pytest.mark.expected_skips(lines=["⚠️ [WARNING] Could not find the 'data' directory."], startup_faults=1)
def test_missing_data_folder_counts(monkeypatch):
    monkeypatch.setattr(config.os.path, "exists", lambda path: False)
    assert config.get_data_file_paths() == []


@pytest.mark.expected_skips(lines=["⚠️ [WARNING] No .md or .docx files found in "], startup_faults=1)
def test_empty_data_folder_counts(monkeypatch):
    monkeypatch.setattr(config.os.path, "exists", lambda path: True)
    monkeypatch.setattr(config.os.path, "isdir", lambda path: True)
    monkeypatch.setattr(config.os, "listdir", lambda path: [])
    assert config.get_data_file_paths() == []


@pytest.fixture
def quiet_ingest(monkeypatch):
    """An ingestion with an empty manifest and no files. A test sets what fails."""
    monkeypatch.setattr(ingest, "load_manifest", lambda: {"ingested_files": []})
    monkeypatch.setattr(ingest, "get_data_file_paths", lambda: [])


@pytest.mark.expected_skips(lines=["⚠️ Error checking docstore: fake fault"], startup_faults=1)
def test_docstore_check_failure_counts(quiet_ingest, monkeypatch):
    class BrokenStore:
        yield_keys = staticmethod(raises)

    monkeypatch.setattr(ingest, "store", BrokenStore())
    assert ingest._run_ingestion() == "done"


@pytest.mark.expected_skips(lines=["🚨 ERROR: fake missing folder"], startup_faults=1)
def test_missing_data_paths_count(quiet_ingest, monkeypatch):
    """Forced: get_data_file_paths has no raise of its own, so only a folder vanishing mid-call reaches this arm."""
    def missing():
        raise FileNotFoundError("fake missing folder")

    monkeypatch.setattr(ingest, "get_data_file_paths", missing)
    assert ingest._run_ingestion() == "failed"


@pytest.fixture
def one_docx(quiet_ingest, monkeypatch, tmp_path):
    monkeypatch.setattr(ingest, "get_data_file_paths", lambda: [str(tmp_path / "note.docx")])


@pytest.mark.expected_skips(lines=["⚠️ [WARNING] Conversion failed or produced empty file for "], startup_faults=1)
def test_empty_conversion_counts(one_docx, monkeypatch):
    monkeypatch.setattr(ingest.subprocess, "run", lambda *args, **kwargs: None)
    assert ingest._run_ingestion() == "done"


@pytest.mark.expected_skips(lines=["⚠️ [WARNING] Pandoc failed for "], startup_faults=1)
def test_pandoc_failure_counts(one_docx, monkeypatch):
    def pandoc_fails(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "pandoc", stderr="fake pandoc error")

    monkeypatch.setattr(ingest.subprocess, "run", pandoc_fails)
    assert ingest._run_ingestion() == "done"


@pytest.mark.expected_skips(lines=["⚠️ [WARNING] Unexpected error converting "], startup_faults=1)
def test_conversion_crash_counts(one_docx, monkeypatch):
    monkeypatch.setattr(ingest.subprocess, "run", raises)
    assert ingest._run_ingestion() == "done"


@pytest.mark.expected_skips(lines=["🚨 Auto-Ingestion failed: fake fault"], startup_faults=1)
def test_ingestion_failure_counts(monkeypatch):
    monkeypatch.setattr(ingest, "_ingestion_state", "not_started")
    monkeypatch.setattr(ingest, "_run_ingestion", raises)
    ingest.initialize_rag()
    assert ingest.get_ingestion_state() == "failed"


@pytest.mark.expected_skips(lines=["❌ Postgres Connection Error: fake fault"], startup_faults=1)
def test_table_setup_failure_counts(monkeypatch):
    monkeypatch.setattr(memory.psycopg, "connect", raises)
    memory.setup_database_tables()


# ------------------------------------------------------------------
# failed_requests: the caller got an error
# ------------------------------------------------------------------
THREAD = "thread-1"
INTERNAL_ERROR = {"error": "Internal error"}


@one_state
@pytest.mark.expected_skips(lines=["🚨 Ownership check error: fake fault"], failed_requests=1)
def test_chat_ownership_failure_counts(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(routes, "owns_thread", raises_async)
    response = asyncio.run(routes.chat_stream(routes.ChatRequest(message=QUESTION, thread_id=THREAD), object(), BROWSER_ID))
    assert response.status_code == 503


@one_state
@pytest.mark.expected_skips(lines=["🚨 Ownership check error: fake fault"], failed_requests=1)
def test_approve_ownership_failure_counts(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(routes, "owns_thread", raises_async)
    response = asyncio.run(routes.chat_approve(routes.ActionRequest(thread_id=THREAD, approve=True), object(), BROWSER_ID))
    assert response.status_code == 503


@one_state
@pytest.mark.expected_skips(lines=["🚨 Error fetching threads: fake fault"], failed_requests=1)
def test_thread_list_failure_counts(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(routes, "get_all_threads_history", raises_async)
    response = asyncio.run(routes.get_all_threads(20, 0, BROWSER_ID))
    assert response == {**INTERNAL_ERROR, "threads": [], "has_more": False}


@one_state
@pytest.mark.expected_skips(lines=["🚨 Error fetching thread state: fake fault"], failed_requests=1)
def test_thread_history_failure_counts(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(routes, "owns_thread", raises_async)
    response = asyncio.run(routes.get_thread_history(THREAD, BROWSER_ID))
    assert response == {**INTERNAL_ERROR, "messages": []}


@one_state
@pytest.mark.expected_skips(lines=["🚨 Delete Error: fake fault"], failed_requests=1)
def test_thread_delete_failure_counts(core, routes, monkeypatch):  # noqa: F811
    monkeypatch.setattr(routes, "delete_thread_from_db", raises_async)
    assert asyncio.run(routes.delete_thread(THREAD, BROWSER_ID)) == INTERNAL_ERROR


async def raises_async(*args, **kwargs):
    raise RuntimeError("fake fault")


class CreditLimitModel:
    """The measured OpenRouter key-limit refusal: 403, scope key_limit."""

    async def ainvoke(self, messages, config=None, **kwargs):
        raise openai.PermissionDeniedError(
            "fake key limit",
            response=httpx.Response(403, request=httpx.Request("POST", "http://openrouter.invalid")),
            body={"metadata": {"scope": "key_limit", "limit_source": "openrouter_key_limit"}},
        )


@one_state
@pytest.mark.expected_skips(lines=["🚨 Backend Crash Details:", "🚨 Raw Error: PermissionDeniedError("], failed_requests=1)
def test_credit_limit_refusal_counts_as_a_failed_request(core):
    """The caller gets the paused line and no answer, so it counts. DECISIONS.md says why."""
    core.set_qa(ScriptedModel(CreditLimitModel()))
    assert chat.DEMO_PAUSED_LINE in streamed_text(run_chat(core.graph, QUESTION))


# ------------------------------------------------------------------
# A new site cannot forget the count
# ------------------------------------------------------------------
SCANNED = (
    "backend/app.py",
    "backend/memory.py",
    "backend/core/agents.py",
    "backend/core/chat.py",
    "backend/core/config.py",
    "backend/core/guardrails.py",
    "backend/core/ingest.py",
    "backend/core/rate_limit.py",
    "backend/core/semantic_router.py",
    "backend/core/tools/search.py",
    "backend/core/tools/system.py",
    "backend/core/tools/weather_aqi.py",
)
COUNTING_CALLS = {"count_skip", "_error_events"}
EXCEPT_ARM = "except arm"
# File, function and the marker print's opening text (or EXCEPT_ARM), with the reason.
NOT_COUNTED = {
    ("backend/app.py", "check_database", "🚨 /health database check failed"): "the same response shows it as database, and tabs poll it",
    ("backend/app.py", "check_database", EXCEPT_ARM): "the same response shows it as database, and tabs poll it",
    ("backend/app.py", "health_check", "🚨 /health skip count failed"): "the count code itself failed, so it cannot count",
    ("backend/app.py", "health_check", EXCEPT_ARM): "the count code itself failed, so it cannot count",
    ("backend/core/ingest.py", "_run_ingestion", "⚠️ Vector Database missing"): "a normal ingest: new files were found",
    ("backend/core/guardrails.py", "get_content_length", EXCEPT_ARM): "len(str(data)) measures the same thing, so nothing is lost",
}


def _print_text(call):
    """A print's fixed text, with a gap for each value it fills in."""
    first = call.args[0] if call.args else None
    if isinstance(first, ast.Constant):
        return str(first.value)
    if isinstance(first, ast.JoinedStr):
        return "{}".join(str(part.value) for part in first.values if isinstance(part, ast.Constant))
    return ""


def _calls_in(statements, names=None):
    calls = (node for statement in statements for node in ast.walk(statement) if isinstance(node, ast.Call))
    return [call for call in calls if names is None or getattr(call.func, "id", "") in names]


def uncounted_sites(source):
    """How many times each (function, text) holds a marker print or except arm with no counting call.

    The count must be a statement of the same block, so a count behind an `if` does not pass.
    _error_events may sit deeper, because chat.py loops over what it returns.
    """
    found = Counter()

    def visit(node, function):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function = node.name
        if isinstance(node, ast.ExceptHandler):
            direct_names = {getattr(s.value.func, "id", "") for s in node.body if isinstance(s, ast.Expr) and isinstance(s.value, ast.Call)}
            if "count_skip" not in direct_names and not _calls_in(node.body, {"_error_events"}):
                found[(function, EXCEPT_ARM)] += 1
        for field in ("body", "orelse", "finalbody"):
            block = getattr(node, field, None)
            if not isinstance(block, list):
                continue
            direct = [s.value for s in block if isinstance(s, ast.Expr) and isinstance(s.value, ast.Call)]
            if any(getattr(call.func, "id", "") in COUNTING_CALLS for call in direct):
                continue
            for call in direct:
                text = _print_text(call)
                if getattr(call.func, "id", "") == "print" and SKIP_MARKERS.search(text):
                    found[(function, text.split("{")[0].rstrip(" :"))] += 1
        for child in ast.iter_child_nodes(node):
            visit(child, function)

    visit(ast.parse(source), "<module>")
    return found


def scanned_sites():
    sites = Counter()
    for name in SCANNED:
        for (function, text), times in uncounted_sites((REPO / name).read_text(encoding="utf-8")).items():
            sites[(name, function, text)] = times
    return sites


def test_every_site_counts_or_is_named():
    unnamed = scanned_sites() - Counter(NOT_COUNTED.keys())
    assert not unnamed, f"add count_skip, or name it in NOT_COUNTED with a reason: {sorted(unnamed.items())}"


def test_every_not_counted_entry_is_still_needed():
    stale = Counter(NOT_COUNTED.keys()) - scanned_sites()
    assert not stale, f"in NOT_COUNTED, but nothing needs it now: {sorted(stale)}"


def test_the_scan_covers_every_backend_module_with_a_print():
    """A new module outside SCANNED would be unseen, so every module with a marker print or an except is listed."""
    modules = [REPO / "backend/app.py", REPO / "backend/memory.py", *sorted((REPO / "backend/core").rglob("*.py"))]
    needing = set()
    for path in modules:
        relative = path.relative_to(REPO).as_posix()
        if relative == "backend/core/skip_counter.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        has_except = any(isinstance(node, ast.ExceptHandler) for node in ast.walk(tree))
        has_marker = any(getattr(call.func, "id", "") == "print" and SKIP_MARKERS.search(_print_text(call)) for call in _calls_in([tree]))
        if has_except or has_marker:
            needing.add(relative)
    assert needing <= set(SCANNED), f"add to SCANNED: {sorted(needing - set(SCANNED))}"


def test_every_count_call_names_a_real_kind():
    wrong = []
    for name in SCANNED:
        for call in _calls_in([ast.parse((REPO / name).read_text(encoding="utf-8"))], {"count_skip"}):
            if not (len(call.args) == 1 and isinstance(call.args[0], ast.Constant) and call.args[0].value in KINDS):
                wrong.append((name, call.lineno))
    assert not wrong, f"count_skip must name one of {KINDS}: {wrong}"


@pytest.mark.parametrize("source, expected", [
    ("try:\n    x()\nexcept Exception:\n    pass\n", {("<module>", EXCEPT_ARM): 1}),
    ("def f():\n    print('⚠️ [WARNING] gone')\n", {("f", "⚠️ [WARNING] gone"): 1}),
    ("def f(e):\n    print(f'🚨 bad {e}')\n", {("f", "🚨 bad"): 1}),
    ("def f():\n    print('⚠️ gone')\n    count_skip('request_skips')\n", {}),
    ("def f():\n    print('⚠️ gone')\n    if x:\n        count_skip('request_skips')\n", {("f", "⚠️ gone"): 1}),
    ("try:\n    x()\nexcept Exception:\n    count_skip('request_skips')\n", {}),
    ("try:\n    x()\nexcept Exception:\n    if y:\n        count_skip('request_skips')\n", {("<module>", EXCEPT_ARM): 1}),
    ("try:\n    x()\nexcept Exception as e:\n    for event in _error_events(e):\n        y(event)\n", {}),
    ("try:\n    x()\nexcept A:\n    pass\nexcept B:\n    pass\n", {("<module>", EXCEPT_ARM): 2}),
    ("def f():\n    print('✅ fine')\n", {}),
])
def test_the_scan_sees_each_form(source, expected):
    assert uncounted_sites(source) == Counter(expected)
