# backend/tests/conftest.py
"""Offline harness for the core contract tests.

Importing backend.core.config has side effects: it reads .env, needs
OPENROUTER_API_KEY, downloads an embedding model, opens ChromaDB and the
docstore on disk, and starts Phoenix tracing. Everything below the imports
replaces those before any backend module loads, so the tests need no network,
no .env and no Postgres. Guards record every Python-level socket connect, DNS
lookup and open() of a .env file, and a fixture fails the test that made one,
even when app code swallows the error. Sockets opened inside native code (for
example a C extension's own client) are not seen by these guards.
"""
import asyncio
import contextlib
import itertools
import json
import os
import socket
import sys
from types import ModuleType, SimpleNamespace

import pytest

# ------------------------------------------------------------------
# 1. Environment: a stub key, no real secrets, no database URL
# ------------------------------------------------------------------
STUB_OPENROUTER_KEY = "test-stub-openrouter-key"
os.environ["OPENROUTER_API_KEY"] = STUB_OPENROUTER_KEY
for _name in (
    "DATABASE_URL", "PGPASSWORD", "LANGCHAIN_API_KEY", "OPENAI_API_KEY",
    "WAQI_API_KEY", "MODEL_NAME", "EVAL_MODE", "PHOENIX_COLLECTOR_ENDPOINT",
):
    os.environ.pop(_name, None)
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# ------------------------------------------------------------------
# 2. Network guard: record and refuse every non-Unix socket connect
#    and every DNS lookup
# ------------------------------------------------------------------
NETWORK_ATTEMPTS: list = []


def _guard(real_method):
    def guarded(self, address):
        if self.family == socket.AF_UNIX:
            return real_method(self, address)
        NETWORK_ATTEMPTS.append(address)
        raise ConnectionRefusedError(f"network call blocked in tests: {address!r}")
    return guarded


def _guarded_getaddrinfo(host, port, *args, **kwargs):
    NETWORK_ATTEMPTS.append(("dns", host, port))
    raise socket.gaierror(f"DNS lookup blocked in tests: {host!r}")


socket.socket.connect = _guard(socket.socket.connect)
socket.socket.connect_ex = _guard(socket.socket.connect_ex)
socket.getaddrinfo = _guarded_getaddrinfo

# ------------------------------------------------------------------
# 2b. .env guard: record every open() of a file named .env, inside the
#     sandbox or not. An audit hook sees opens that app code catches.
# ------------------------------------------------------------------
DOTENV_OPENS: list = []


def _audit_dotenv_opens(event, args):
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        if os.path.basename(os.fsdecode(args[0])) == ".env":
            DOTENV_OPENS.append(os.fsdecode(args[0]))


sys.addaudithook(_audit_dotenv_opens)

# ------------------------------------------------------------------
# 3. Import-time fakes for config.py (config.py:14, :23-44, :89-99)
# ------------------------------------------------------------------
DOTENV_CALLS: list = []

import dotenv  # noqa: E402


def _no_dotenv(*args, **kwargs):
    """Replaces load_dotenv so config.py:14 never opens a .env file."""
    DOTENV_CALLS.append((args, kwargs))
    return False


dotenv.load_dotenv = _no_dotenv

# Tracing off: config.py's existing except branch prints one warning and goes on.
# The phoenix package itself is blocked too: its __init__ imports fastmcp, which reads .env.
sys.modules["openinference.instrumentation.langchain"] = None
sys.modules["phoenix"] = None
sys.modules["phoenix.otel"] = None

from langchain_core.embeddings import DeterministicFakeEmbedding  # noqa: E402
from langchain_core.stores import InMemoryByteStore  # noqa: E402
from langchain_core.vectorstores import InMemoryVectorStore  # noqa: E402
import langchain_classic.storage  # noqa: E402

# Stand-in modules, not patched real ones: importing the real langchain_chroma
# imports chromadb, whose Settings() reads .env from the working directory.
_fake_huggingface = ModuleType("langchain_huggingface")
_fake_huggingface.HuggingFaceEmbeddings = lambda **kwargs: DeterministicFakeEmbedding(size=32)
_fake_chroma = ModuleType("langchain_chroma")
# Every collection name config.py opens, in order; the tests check the set.
CHROMA_COLLECTIONS: list = []


def _fake_chroma_store(**kwargs):
    CHROMA_COLLECTIONS.append(kwargs.get("collection_name"))
    return InMemoryVectorStore(embedding=kwargs["embedding_function"])


_fake_chroma.Chroma = _fake_chroma_store
sys.modules["langchain_huggingface"] = _fake_huggingface
sys.modules["langchain_chroma"] = _fake_chroma
langchain_classic.storage.LocalFileStore = lambda *args, **kwargs: InMemoryByteStore()

from langchain_core.callbacks import CallbackManagerForRetrieverRun  # noqa: E402
from langchain_core.documents import Document  # noqa: E402
from langchain_core.language_models.fake_chat_models import (  # noqa: E402
    FakeMessagesListChatModel,
    GenericFakeChatModel,
)
from langchain_core.messages import AIMessage  # noqa: E402
from langchain_core.retrievers import BaseRetriever  # noqa: E402
from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from psycopg.errors import ForeignKeyViolation  # noqa: E402
from pydantic import Field  # noqa: E402

from backend import memory  # noqa: E402
from backend.core import agents, chat, config  # noqa: E402
from backend.core.tools import search  # noqa: E402

assert DOTENV_CALLS, "config.py did not call the replaced load_dotenv; the .env guard is not in effect"
assert not DOTENV_OPENS, f".env opened while importing the backend: {DOTENV_OPENS}"
assert not NETWORK_ATTEMPTS, f"network calls attempted while importing the backend: {NETWORK_ATTEMPTS}"

# ------------------------------------------------------------------
# 4. Fakes injected per test
# ------------------------------------------------------------------
DONE = "data: [DONE]\n\n"
QUESTION = "How does the reranker pick context chunks?"
ANSWER = "The reranker scores each chunk against the query and keeps the top ten."
FALLBACK_TEXT = "I'm sorry, but that information is not available in my knowledge base."
RETRIEVED_TEXT = "Rerankers score each chunk against the query and keep the best ones."


class FakeRetriever(BaseRetriever):
    """Stands in for config.retriever; returns fresh copies of fixed documents."""

    docs: list = Field(default_factory=list)
    queries: list = Field(default_factory=list)

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun):
        self.queries.append(query)
        return [Document(page_content=d.page_content, metadata=dict(d.metadata)) for d in self.docs]


class FakeReranker:
    """Stands in for the CrossEncoder; scores every pair the same."""

    def __init__(self):
        self.pairs = []

    def predict(self, pairs):
        self.pairs.extend(pairs)
        return [0.5 for _ in pairs]


class StrictFakeMessagesListChatModel(FakeMessagesListChatModel):
    """FakeMessagesListChatModel that never wraps back to its first reply.

    chat.py and agents.py catch errors from fast_llm, so a raise alone would be
    swallowed; extra_calls lets the fixture fail the test at teardown.
    """

    calls: int = 0
    extra_calls: int = 0

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        if self.calls >= len(self.responses):
            self.extra_calls += 1
            raise AssertionError("fast_llm was called more often than the test scripted")
        self.calls += 1
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


class ScriptedModel:
    """Stands in for agents.llm_with_tools.

    Each ainvoke hands the call to the next fake model in the script. Two
    fakes are needed for one turn: FakeMessagesListChatModel keeps tool_calls
    but does not stream; GenericFakeChatModel streams but drops tool_calls.
    """

    def __init__(self, *models):
        self.models = list(models)
        self.calls = []

    async def ainvoke(self, messages, config=None, **kwargs):
        self.calls.append(list(messages))
        if not self.models:
            raise AssertionError("the answer model was called more often than the test scripted")
        return await self.models.pop(0).ainvoke(messages, config, **kwargs)


class FailingModel:
    """A model call that raises, as a provider outage would."""

    async def ainvoke(self, messages, config=None, **kwargs):
        raise RuntimeError("fake provider outage")


class NoPostgres:
    """Passed as async_pool: any use of it fails the test."""

    def __getattr__(self, name):
        raise AssertionError(f"Postgres reached: async_pool.{name}")


def _one_line(sql):
    return " ".join(sql.split())


class FakeRegistryPool:
    """Stands in for async_pool on the statements register_thread and start_title_generation run.

    rows maps thread_id to {"title": ..., "owner_id": ...}. Any other statement,
    or a reworded one, fails the test.
    """

    INSERT = _one_line("""
        INSERT INTO thread_metadata (thread_id, title, owner_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (thread_id) DO NOTHING
        RETURNING thread_id
    """)
    SELECT_OWNER = "SELECT owner_id FROM thread_metadata WHERE thread_id = %s"
    UPDATE_TITLE = "UPDATE thread_metadata SET title = %s WHERE thread_id = %s"

    def __init__(self):
        self.rows = {}

    @contextlib.asynccontextmanager
    async def connection(self):
        yield self

    @contextlib.asynccontextmanager
    async def cursor(self):
        yield _FakeRegistryCursor(self.rows)


class _FakeRegistryCursor:
    def __init__(self, rows):
        self.rows = rows
        self.result = None

    async def execute(self, sql, params):
        sql = _one_line(sql)
        if sql == FakeRegistryPool.INSERT:
            thread_id, title, owner_id = params
            if thread_id in self.rows:
                self.result = None
            else:
                self.rows[thread_id] = {"title": title, "owner_id": owner_id}
                self.result = (thread_id,)
        elif sql == FakeRegistryPool.SELECT_OWNER:
            row = self.rows.get(params[0])
            self.result = (row["owner_id"],) if row else None
        elif sql == FakeRegistryPool.UPDATE_TITLE:
            title, thread_id = params
            if thread_id in self.rows:
                self.rows[thread_id]["title"] = title
            self.result = None
        else:
            raise AssertionError(f"unexpected SQL in FakeRegistryPool: {sql}")

    async def fetchone(self):
        return self.result


class FkMemorySaver(MemorySaver):
    """MemorySaver that refuses a write for a thread with no registry row.

    Mimics the checkpoint foreign keys to thread_metadata (memory.py,
    setup_database_tables). Measured 2026-10-29 on postgres:16: each of the
    three checkpoint tables raises this error, sqlstate 23503.
    """

    def __init__(self, registry):
        super().__init__()
        self.registry = registry

    def _require_row(self, config, table, constraint):
        thread_id = config["configurable"]["thread_id"]
        if thread_id not in self.registry.rows:
            raise ForeignKeyViolation(
                f'insert or update on table "{table}" violates foreign key constraint '
                f'"{constraint}"\nDETAIL:  Key (thread_id)=({thread_id}) '
                f'is not present in table "thread_metadata".'
            )

    def put(self, config, checkpoint, metadata, new_versions):
        self._require_row(config, "checkpoints", "fk_cascade_metadata_checkpoints")
        return super().put(config, checkpoint, metadata, new_versions)

    def put_writes(self, config, writes, task_id, task_path=""):
        self._require_row(config, "checkpoint_writes", "fk_cascade_metadata_writes")
        return super().put_writes(config, writes, task_id, task_path)


def tool_call_turn(query: str) -> FakeMessagesListChatModel:
    """A qa_node step that calls search_knowledge_base with the query."""
    return FakeMessagesListChatModel(responses=[AIMessage(
        content="",
        tool_calls=[{"name": "search_knowledge_base", "args": {"query": query}, "id": "call_1"}],
    )])


def answer_turn(text: str) -> GenericFakeChatModel:
    """A qa_node step that streams the final answer word by word."""
    return GenericFakeChatModel(messages=iter([AIMessage(content=text)]))


def rag_script(query: str, answer: str) -> ScriptedModel:
    return ScriptedModel(tool_call_turn(query), answer_turn(answer))


@pytest.fixture(autouse=True)
def offline_only():
    """Fails any test during which code tried the network or opened .env."""
    NETWORK_ATTEMPTS.clear()
    DOTENV_OPENS.clear()
    yield
    assert not NETWORK_ATTEMPTS, f"network calls attempted: {NETWORK_ATTEMPTS}"
    assert not DOTENV_OPENS, f".env opened: {DOTENV_OPENS}"


@pytest.fixture
def core(monkeypatch):
    """Patches every model, store and Postgres call on the core path.

    Returns a namespace the test can adjust before it runs a turn.
    """
    registry_calls = []
    title_calls = []
    state = SimpleNamespace(registry_result=True)
    registry = FakeRegistryPool()

    async def fake_register_thread(async_pool, thread_id, user_message, owner_id):
        registry_calls.append((thread_id, user_message, owner_id))
        if not state.registry_result:
            return False, False
        # Writes the row FkMemorySaver checks, as the real INSERT would
        created = thread_id not in registry.rows
        title = user_message[:40] + ("..." if len(user_message) > 40 else "")
        registry.rows.setdefault(thread_id, {"title": title, "owner_id": owner_id})
        return True, created

    def fake_start_title_generation(async_pool, thread_id, user_message):
        title_calls.append((thread_id, user_message))

    retriever = FakeRetriever(docs=[Document(
        page_content=RETRIEVED_TEXT,
        metadata={"source": "data/notes.md", "Header 1": "Retrieval"},
    )])
    reranker = FakeReranker()
    # The scope router (agents.py) makes the turn's one fast_llm call.
    fast_llm = StrictFakeMessagesListChatModel(responses=[AIMessage(content="IN_SCOPE")])
    expansion_llm = GenericFakeChatModel(
        messages=itertools.cycle([AIMessage(content="EXPANSIONMARKER reranking\ncross encoder scores")]),
        name="Expansion_LLM",
    )

    monkeypatch.setattr(chat, "register_thread", fake_register_thread)
    monkeypatch.setattr(chat, "start_title_generation", fake_start_title_generation)
    monkeypatch.setattr(config, "fast_llm", fast_llm)
    monkeypatch.setattr(agents, "fast_llm", fast_llm)
    monkeypatch.setattr(search, "expansion_llm", expansion_llm)
    monkeypatch.setattr(search, "retriever", retriever)
    monkeypatch.setattr(search, "get_reranker", lambda: reranker)
    monkeypatch.setattr(search, "get_data_file_paths", lambda: [])

    ns = SimpleNamespace(
        state=state,
        registry_calls=registry_calls,
        title_calls=title_calls,
        registry=registry,
        retriever=retriever,
        reranker=reranker,
        fast_llm=fast_llm,
        qa=None,
    )

    def set_qa(model):
        ns.qa = model
        monkeypatch.setattr(agents, "llm_with_tools", model)

    def set_fast_replies(*replies):
        # fast_llm belongs to this fixture call, so plain assignment needs no undo.
        fast_llm.responses = [AIMessage(content=r) for r in replies]
        fast_llm.i = 0
        fast_llm.calls = 0

    def use_real_registry(title_model):
        # The real register_thread and start_title_generation, on the fake pool
        monkeypatch.setattr(chat, "register_thread", memory.register_thread)
        monkeypatch.setattr(chat, "start_title_generation", memory.start_title_generation)
        monkeypatch.setattr(config, "llm", title_model)

    ns.set_qa = set_qa
    ns.set_fast_replies = set_fast_replies
    ns.use_real_registry = use_real_registry
    # Same compile as app.py:73, with FkMemorySaver in place of AsyncPostgresSaver.
    ns.graph = agents.workflow.compile(checkpointer=FkMemorySaver(registry), interrupt_before=["sensitive_tools"])
    yield ns
    # A test that failed before run_chat drained its title task leaves it here; never carry it over
    memory._title_tasks.clear()
    assert fast_llm.extra_calls == 0, f"fast_llm got {fast_llm.extra_calls} call(s) beyond its script"


def run_chat(graph, message, thread_id="thread-1", owner_id="owner-1", pool=None):
    """Runs generate_chat_responses to the end and returns the raw SSE chunks.

    Then waits for every background title task, so a test sees its outcome
    and none is cancelled when the event loop closes.
    """

    async def collect():
        async_pool = pool if pool is not None else NoPostgres()
        chunks = [c async for c in chat.generate_chat_responses(message, thread_id, graph, async_pool, owner_id)]
        while memory._title_tasks:
            await asyncio.gather(*memory._title_tasks)
        return chunks

    return asyncio.run(collect())


def parse_events(chunks):
    return [json.loads(c[len("data: "):]) for c in chunks if c != DONE]


def streamed_text(chunks):
    """The text a browser shows: every on_chat_model_stream chunk, joined."""
    return "".join(
        e["data"]["chunk"]["content"]
        for e in parse_events(chunks)
        if e.get("event") == "on_chat_model_stream"
    )


def checkpoint_messages(graph, thread_id="thread-1"):
    state = asyncio.run(graph.aget_state({"configurable": {"thread_id": thread_id}}))
    return state.values.get("messages", [])
