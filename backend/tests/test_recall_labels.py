# backend/tests/test_recall_labels.py
"""The section recall: what the tools carry for it, what the model is sent, and the labels.

DECISIONS.md, "Recall counts sections, not problem numbers". Not a core file of
test_removal.py: it reads qa_dataset.json and the fast-path table, which the removal
copies do not carry.
"""
import ast
import asyncio
import json
from pathlib import Path

import pytest
from langchain_core.documents import Document
from langchain_core.load import dumps
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool

from backend.core import semantic_router
from backend.core.fast_path_routes import FAST_PATH_INTERCEPTS
from backend.core.tools import search
from backend.evals import check_section_labels
from backend.evals.recall import is_section_hit
from conftest import ANSWER, QUESTION, ScriptedModel, checkpoint_messages, rag_script, run_chat

REPO = Path(__file__).parents[2]
one_state = pytest.mark.switch_states("no_variable")
PLANTED_KEY = "planted fast path question"
PLANTED_SECTIONS = [{"source_file": "notes.md", "headers": {"Header 1": "Problem 9"}}]


def section(file, **headers):
    return {"source_file": file, "headers": {k.replace("_", " "): v for k, v in headers.items()}}


def search_with_artifact(query):
    """A tool call, as ToolNode makes it, so the result keeps its artifact."""
    call = {"name": "search_knowledge_base", "args": {"query": query}, "id": "call_t", "type": "tool_call"}
    return asyncio.run(search.search_knowledge_base.ainvoke(call))


def load_dataset():
    with open(REPO / "backend/evals/qa_dataset.json", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------
# What the search tool and fast_path_node carry
# ------------------------------------------------------------------

@one_state
def test_vector_search_artifact_lists_the_sections_of_the_chunks(core):
    core.retriever.docs = [
        Document(page_content="Rerankers score chunks.", metadata={"source_file": "notes.md", "Header 1": "A", "Header 2": "B"}),
        Document(page_content="Chunks are scored again.", metadata={"source_file": "other.md", "Header 1": "C"}),
    ]

    message = search_with_artifact(QUESTION)

    assert "Rerankers score chunks." in message.content
    got = sorted(json.dumps(s, sort_keys=True) for s in message.artifact["retrieved_sections"])
    assert got == sorted(json.dumps(s, sort_keys=True) for s in [
        section("notes.md", Header_1="A", Header_2="B"),
        section("other.md", Header_1="C"),
    ])


@one_state
def test_a_section_that_starts_past_the_size_cut_does_not_count(core):
    # Each block is cut to 10000 characters, so the fourth starts past the 30000 cut.
    core.retriever.docs = [
        Document(page_content=f"{n}" * 12000, metadata={"source_file": "big.md", "Header 1": f"S{n}"})
        for n in range(4)
    ]

    message = search_with_artifact(QUESTION)

    names = [s["headers"]["Header 1"] for s in message.artifact["retrieved_sections"]]
    seen = [f"S{n}" for n in range(4) if f"Section Hierarchy: # S{n}\n" in message.content]
    assert len(names) == 3
    assert sorted(names) == sorted(seen)


@pytest.mark.switch_states("no_variable")
def test_a_table_hit_carries_the_entry_sections(core, monkeypatch):
    monkeypatch.setattr(semantic_router, "FAST_PATH_INTERCEPTS", {
        PLANTED_KEY: {"output": "Stored.", "target_id": "planted_id", "target_sections": PLANTED_SECTIONS},
    })
    core.set_fast_replies()
    core.set_qa(ScriptedModel())

    run_chat(core.graph, PLANTED_KEY)

    tool_messages = [m for m in checkpoint_messages(core.graph) if isinstance(m, ToolMessage)]
    assert [m.artifact for m in tool_messages] == [{"retrieved_sections": PLANTED_SECTIONS}]


@pytest.mark.switch_states("no_variable")
def test_a_table_entry_without_sections_carries_an_empty_list(core, monkeypatch):
    monkeypatch.setattr(semantic_router, "FAST_PATH_INTERCEPTS", {
        PLANTED_KEY: {"output": "Stored.", "target_id": "planted_id"},
    })
    core.set_fast_replies()
    core.set_qa(ScriptedModel())

    run_chat(core.graph, PLANTED_KEY)

    tool_messages = [m for m in checkpoint_messages(core.graph) if isinstance(m, ToolMessage)]
    assert [m.artifact for m in tool_messages] == [{"retrieved_sections": []}]


# ------------------------------------------------------------------
# What the model is sent: the eval's cache keys must not change
# ------------------------------------------------------------------

@one_state
def test_the_model_gets_the_tool_message_without_its_artifact(core):
    core.set_fast_replies("IN_SCOPE")
    core.set_qa(rag_script(QUESTION, ANSWER))

    run_chat(core.graph, QUESTION)

    stored = [m for m in checkpoint_messages(core.graph) if isinstance(m, ToolMessage)]
    sent = [m for m in core.qa.calls[1] if isinstance(m, ToolMessage)]
    assert len(stored) == len(sent) == 1
    assert stored[0].artifact["retrieved_sections"]
    assert sent[0].artifact is None
    # The cache key (langchain_core's dumps of the list) equals that of the message before artifacts.
    before = ToolMessage(content=sent[0].content, name=sent[0].name, tool_call_id=sent[0].tool_call_id)
    assert dumps([sent[0].model_copy(update={"id": None})]) == dumps([before])


def test_the_tool_schema_the_model_is_bound_with_is_unchanged():
    """bind_tools puts this schema into the cache's llm_string; response_format must not change it."""
    plain = tool(search.search_knowledge_base.coroutine)
    assert convert_to_openai_tool(search.search_knowledge_base) == convert_to_openai_tool(plain)


# ------------------------------------------------------------------
# The hit rule
# ------------------------------------------------------------------

def test_a_hit_is_the_same_file_and_the_same_headers_at_the_same_levels():
    target = [section("a.md", Header_1="P"), section("a.md", Header_1="Q", Header_3="R")]

    assert is_section_hit(target, [section("a.md", Header_1="P")])
    assert is_section_hit(target, [section("x.md", Header_1="Z"), section("a.md", Header_1="Q", Header_3="R")])
    assert not is_section_hit(target, [section("b.md", Header_1="P")])
    assert not is_section_hit(target, [section("a.md", Header_1="P", Header_2="child")])
    assert not is_section_hit(target, [section("a.md", Header_1="Q")])
    assert not is_section_hit(target, [section("a.md", Header_1="Q", Header_2="R")])
    assert not is_section_hit(target, [])


# ------------------------------------------------------------------
# The labels
# ------------------------------------------------------------------

def test_every_row_with_an_old_id_carries_sections_and_no_other_row_does():
    dataset = load_dataset()
    rows = [(f"case {n}", c.get("target_problem_id"), c.get("target_sections")) for n, c in enumerate(dataset, 1)]
    rows += [(f"entry {k!r}", e.get("target_id"), e.get("target_sections")) for k, e in FAST_PATH_INTERCEPTS.items()]

    wrong = [name for name, old_id, sections in rows if (old_id is not None) != bool(sections)]
    assert not wrong, wrong
    assert sum(1 for c in dataset if c.get("target_sections")) == 34
    assert sum(1 for e in FAST_PATH_INTERCEPTS.values() if e.get("target_sections")) == 26


@pytest.mark.parametrize("switch_state", ["fast_path_on"], indirect=True)
def test_a_labelled_case_the_fast_path_answers_carries_the_label_it_copies(switch_state):
    """A fast-path hit copies the label the router returns, so a case with another label would always miss.

    Calls the router itself, so a change to its lookup is seen here, the Problem-N branch too.
    """
    mismatched = []
    for n, case in enumerate(load_dataset(), 1):
        if not case.get("target_sections"):
            continue
        route = asyncio.run(semantic_router.route_query(case["query"]))
        if route["route_category"] == "FAST_PATH" and case["target_sections"] != route.get("fast_path_target_sections"):
            mismatched.append(n)
    assert not mismatched


def test_the_label_check_copies_the_preprocessing_of_ingest():
    tree = ast.parse((REPO / "backend/core/ingest.py").read_text(encoding="utf-8"))
    subs = tuple(
        (node.args[0].value, node.args[1].value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "sub"
        and len(node.args) == 3 and getattr(node.args[2], "id", "") == "markdown_document"
    )
    assert len(subs) == 4
    assert subs == check_section_labels.INGEST_SUBS
