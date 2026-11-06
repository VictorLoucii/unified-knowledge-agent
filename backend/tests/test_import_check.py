# backend/tests/test_import_check.py
"""The import check, and the check of the interrupt lists at the compile sites.

Static on purpose: a runtime check sees only the imports that ran, so it misses an
import inside a function nobody called. These tests read source, so they need no
fixture and run in milliseconds.

What this cannot see: attribute access after a package import
(`tools.weather_aqi.x` after `from backend.core import tools`) and a feature's name
held as plain text. The removal tests (test_removal.py) cover those by running, on
any code a core test calls; in a function no test calls, nothing sees them.
Refine and query expansion have one name each here and no module, and the latency
footer has nothing to import, so the removal tests are their main cover. See
DECISIONS.md, "What a removal test proves".
"""
import ast
from pathlib import Path

import pytest

from backend.core import agents

REPO = Path(__file__).parents[2]

FEATURE_MODULES = (
    "backend.core.fast_path_routes",
    "backend.core.tools.system",
    "backend.core.tools.weather_aqi",
)
# A name importable without naming the feature's module: a re-export or a function.
FEATURE_NAMES = (
    "backend.core.agents.WEATHER_TOOL_LINE",
    "backend.core.agents.llm_without_weather",
    "backend.core.agents.sensitive_tools",
    "backend.core.chat.resume_graph_stream",
    "backend.core.config.transcript_refine_enabled",
    "backend.core.config.weather_tool_enabled",
    "backend.core.semantic_router.FAST_PATH_INTERCEPTS",
    "backend.core.tools.get_system_time",
    "backend.core.tools.get_weather_and_aqi",
    "backend.core.tools.search.expansion_llm",
    "backend.memory.generate_title_from_llm",
    "backend.memory.start_title_generation",
)
DYNAMIC = "<dynamic import>"

# Named, not globbed: a glob finds the ignored scripts on one machine and not in CI.
TRACKED_ROOT_SCRIPTS = ("fetch_phoenix_logs.py", "generate_dataset.py", "test_retrieval.py", "test_stream.py")
MINIMUM_FILES = 30

# Each entry is a file and a target, with its reason. An entry nothing needs fails too.
ALLOWED = {
    ("backend/core/tools/__init__.py", "backend.core.tools.system"): "registration line",
    ("backend/core/tools/__init__.py", "backend.core.tools.weather_aqi"): "registration line",
    ("backend/core/semantic_router.py", "backend.core.fast_path_routes"): "registration line",
    ("backend/core/chat.py", "backend.memory.start_title_generation"): "registration line",
    ("backend/app.py", "backend.core.chat.resume_graph_stream"): "registration line: the approve route",
    ("backend/app.py", "backend.core.config.transcript_refine_enabled"): "registration line: the refine route",
    ("backend/core/agents.py", "backend.core.config.weather_tool_enabled"): "registration line: the graph's weather choice",
    ("backend/core/tools/weather_aqi.py", "backend.core.config.weather_tool_enabled"): "the weather feature's own module",
    ("backend/evals/check_fast_path.py", "backend.core.fast_path_routes"): "guards the table and goes with it",
    ("backend/evals/check_section_labels.py", "backend.core.fast_path_routes"): "checks the table's recall labels and goes with it",
    ("backend/tests/test_core_switches.py", "backend.core.tools.weather_aqi"): "tests the weather feature",
    ("backend/tests/test_no_silent_skips.py", "backend.core.tools.weather_aqi"): "tests the weather tool's skip count",
    # These two files name every feature in text, to look for it.
    ("backend/tests/test_import_check.py", "backend.core.fast_path_routes"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.tools.system"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.tools.weather_aqi"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.agents.WEATHER_TOOL_LINE"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.agents.llm_without_weather"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.agents.sensitive_tools"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.semantic_router.FAST_PATH_INTERCEPTS"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.chat.resume_graph_stream"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.config.transcript_refine_enabled"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.config.weather_tool_enabled"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.tools.search.expansion_llm"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.tools.get_system_time"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.core.tools.get_weather_and_aqi"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.memory.generate_title_from_llm"): "this check's own list",
    ("backend/tests/test_import_check.py", "backend.memory.start_title_generation"): "this check's own list",
    ("backend/tests/test_removal.py", "backend.core.fast_path_routes"): "its probe looks for the module",
    ("backend/tests/test_recall_labels.py", "backend.core.fast_path_routes"): "tests the table's recall labels",
    ("backend/tests/test_removal.py", "backend.core.tools.system"): "its probe looks for the module",
    ("backend/tests/test_removal.py", "backend.core.tools.weather_aqi"): "its probe looks for the module",
}


def package_of(relative_path):
    """The package a file's relative imports start from."""
    parts = Path(relative_path).with_suffix("").parts
    return ".".join(parts[:-1])


def _resolve(node, package):
    if not node.level:
        return node.module or ""
    base = package.split(".")
    base = base[:len(base) - (node.level - 1)]
    return ".".join(base + ([node.module] if node.module else []))


def _targets_of_dotted_name(name):
    """Every feature a dotted name reaches: the module itself, or anything inside it."""
    found = {m for m in FEATURE_MODULES if name == m or name.startswith(m + ".")}
    found |= {n for n in FEATURE_NAMES if name == n}
    return found


def _is_dynamic_import(node):
    func = node.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
    return name in ("import_module", "__import__")


def feature_targets(source, relative_path="backend/core/planted.py"):
    """Returns the set of features one file reaches by import, or names as a dotted string."""
    package = package_of(relative_path)
    found = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found |= _targets_of_dotted_name(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = _resolve(node, package)
            found |= _targets_of_dotted_name(module)
            for alias in node.names:
                if alias.name == "*":
                    # A star import brings in whatever the package holds.
                    found |= {t for t in FEATURE_MODULES + FEATURE_NAMES if t.rpartition(".")[0] == module}
                else:
                    found |= _targets_of_dotted_name(f"{module}.{alias.name}")
        elif isinstance(node, ast.Call) and _is_dynamic_import(node):
            # A lone absolute name reaches the dotted-string branch below on its own. Anything
            # else, such as a relative name or a fromlist, can reach a feature unseen.
            first = node.args[0] if node.args else None
            fixed = (
                len(node.args) == 1 and not node.keywords
                and isinstance(first, ast.Constant) and isinstance(first.value, str)
                and not first.value.startswith(".")
            )
            if not fixed:
                found.add(DYNAMIC)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            # A dotted string, such as a patch("backend.core.tools.weather_aqi.requests") target.
            found |= {t for t in FEATURE_MODULES + FEATURE_NAMES if t in node.value}
    return found


def scanned_files():
    files = [p for p in (REPO / "backend").rglob("*.py") if "__pycache__" not in p.parts]
    return sorted(files) + [REPO / name for name in TRACKED_ROOT_SCRIPTS]


def flagged_imports():
    flagged = set()
    for path in scanned_files():
        relative = path.relative_to(REPO).as_posix()
        for target in feature_targets(path.read_text(encoding="utf-8"), relative):
            flagged.add((relative, target))
    return flagged


def test_the_scan_covers_the_backend():
    """An empty scan would pass every check below, so its size is checked first."""
    files = scanned_files()
    relative = {p.relative_to(REPO).as_posix() for p in files}
    assert len(files) >= MINIMUM_FILES
    assert {"backend/app.py", "backend/memory.py", "backend/core/agents.py", "backend/evals/eval.py"} <= relative


def test_no_module_imports_a_feature_outside_its_named_exceptions():
    unexpected = flagged_imports() - set(ALLOWED)
    assert not unexpected, f"not in ALLOWED: {sorted(unexpected)}"


def test_every_exception_is_still_needed():
    stale = set(ALLOWED) - flagged_imports()
    assert not stale, f"in ALLOWED, but nothing needs it now: {sorted(stale)}"


@pytest.mark.parametrize("source, expected", [
    ("import backend.core.fast_path_routes", "backend.core.fast_path_routes"),
    ("from backend.core.fast_path_routes import FAST_PATH_INTERCEPTS", "backend.core.fast_path_routes"),
    ("from backend.core.tools import weather_aqi", "backend.core.tools.weather_aqi"),
    ("from backend.core.tools import get_weather_and_aqi", "backend.core.tools.get_weather_and_aqi"),
    ("from backend.memory import start_title_generation", "backend.memory.start_title_generation"),
    ("from .tools.weather_aqi import WEATHER_OFF_RESULT", "backend.core.tools.weather_aqi"),
    ("from .tools import system", "backend.core.tools.system"),
    ("from backend.core.tools import *", "backend.core.tools.weather_aqi"),
    ("def later():\n    from backend.core.tools.system import get_system_time", "backend.core.tools.system"),
    ("async def later():\n    import backend.core.fast_path_routes", "backend.core.fast_path_routes"),
    ("import importlib\nimportlib.import_module('backend.core.tools.system')", "backend.core.tools.system"),
    ("import importlib\nname = 'x'\nimportlib.import_module(name)", DYNAMIC),
    ("__import__(name)", DYNAMIC),
    ("import importlib\nimportlib.import_module('.weather_aqi', 'backend.core.tools')", DYNAMIC),
    ("__import__('backend.core.tools', fromlist=['weather_aqi'])", DYNAMIC),
    ("def later():\n    from backend.core.chat import resume_graph_stream", "backend.core.chat.resume_graph_stream"),
    ("patch('backend.core.tools.weather_aqi.requests')", "backend.core.tools.weather_aqi"),
])
def test_the_check_sees_each_form_of_import(source, expected):
    assert expected in feature_targets(source)


def test_the_check_leaves_core_imports_alone():
    source = (
        "from backend.core.config import fast_llm\nfrom backend.core.tools import tools\nimport os\n"
        "import importlib\nimportlib.import_module('json')"
    )
    assert feature_targets(source) == set()


def test_a_relative_import_resolves_from_its_own_package():
    source = "from .weather_aqi import get_weather_and_aqi"
    assert feature_targets(source, "backend/core/tools/__init__.py") == {"backend.core.tools.weather_aqi"}
    assert feature_targets(source, "backend/evals/planted.py") == set()


# ------------------------------------------------------------------
# Interrupt lists at the compile sites
# ------------------------------------------------------------------
COMPILE_SITES = {"backend/app.py", "backend/core/agents.py", "backend/evals/eval.py", "backend/evals/run_topic_cases.py", "backend/tests/conftest.py", "test_stream.py"}


def compile_calls(source):
    """Each workflow.compile(...) call, as its interrupt_before list, or [] if it has none."""
    calls = []
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "compile"):
            continue
        receiver = node.func.value
        receiver_name = receiver.attr if isinstance(receiver, ast.Attribute) else getattr(receiver, "id", "")
        if receiver_name != "workflow":
            continue
        names = [ast.literal_eval(k.value) for k in node.keywords if k.arg == "interrupt_before"]
        calls.append(names[0] if names else [])
    return calls


def test_every_interrupt_list_names_a_real_node():
    """A name with no node raises at compile; at app.py that is at startup, where no other test looks."""
    sites = {}
    for path in scanned_files():
        calls = compile_calls(path.read_text(encoding="utf-8"))
        if calls:
            sites[path.relative_to(REPO).as_posix()] = calls
    assert set(sites) == COMPILE_SITES
    missing = {site: name for site, calls in sites.items() for names in calls for name in names if name not in agents.workflow.nodes}
    assert not missing, f"interrupt_before names no node: {missing}"
