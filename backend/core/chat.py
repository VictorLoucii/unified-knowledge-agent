# backend/core/chat.py
import json
import asyncio
import openai
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

from backend.core.guardrails import (
    check_input_guardrail,
    mask_sensitive_data,
    get_content_length,
    get_last_tool_output_length,
)
from backend.memory import register_thread, start_title_generation
import time


def _thread_refused_events():
    """SSE events for a thread that belongs to another browser, without [DONE]; the runner sends it."""
    refused_event = {
        "event": "on_chat_model_stream",
        "name": "Ownership",
        "run_id": "thread_refused",
        "data": {"chunk": {"content": "This chat is not available."}},
    }
    return [f"data: {json.dumps(refused_event)}\n\n"]


# Fixed reply when OpenRouter refuses a call because the key's credit limit is
# spent. Measured 2026-10-28 with a $0-limit key: openai.PermissionDeniedError,
# status 403, body {"message": "Key limit exceeded (total limit). ...",
# "code": 403, "metadata": {"scope": "key_limit",
# "limit_source": "openrouter_key_limit", ...}}. Every other error keeps the
# general error event.
DEMO_PAUSED_LINE = "The demo is paused: it has used its credit for now. Please try again later."


def is_credit_limit_refusal(e: Exception) -> bool:
    """True only for the measured OpenRouter key-limit refusal (403, scope key_limit)."""
    if not isinstance(e, openai.PermissionDeniedError):
        return False
    body = e.body if isinstance(e.body, dict) else {}
    metadata = body.get("metadata")
    if not isinstance(metadata, dict):
        return False
    return metadata.get("scope") == "key_limit" and metadata.get("limit_source") == "openrouter_key_limit"


def _demo_paused_event():
    """SSE event with the fixed "demo paused" line, in the shape of the guardrail refusal."""
    paused_event = {
        "event": "on_chat_model_stream",
        "name": "CreditLimit",
        "run_id": "demo_paused",
        "data": {"chunk": {"content": DEMO_PAUSED_LINE}},
    }
    return f"data: {json.dumps(paused_event)}\n\n"


class ChatTurn:
    """One user message on its way through PRE_STEPS."""

    def __init__(self, user_message: str, thread_id: str, graph, async_pool, owner_id: str):
        self.user_message = user_message
        self.thread_id = thread_id
        self.graph = graph
        self.async_pool = async_pool
        self.owner_id = owner_id


class StepReply:
    """A pre-step's finished answer: its SSE events, without [DONE].

    The runner sends each event, waits `pause` seconds after each one, prints
    the dev line when `log` is set, then sends [DONE]. A step builds every
    event before it returns, so nothing reaches the client from a step that
    fails.
    """

    def __init__(self, events: list[str], pause: float = 0.0, log: str | None = None):
        self.events = events
        self.pause = pause
        self.log = log


def _error_events(e: Exception, user_message: str, start_time: float) -> list[str]:
    """Logs a failed turn and returns the events that end it. Call it inside an except block."""
    import traceback

    print("🚨 Backend Crash Details:")
    traceback.print_exc()

    print(f"🚨 Raw Error: {repr(e)}")
    if is_credit_limit_refusal(e):
        print("🔧 [__DEV__] generate_chat_responses | is_credit_limit_refusal matched (403, scope key_limit) | Response: demo paused line")
        events = [_demo_paused_event()]
    else:
        events = [f"data: {json.dumps({'event': 'on_error', 'name': 'error', 'run_id': 'error', 'data': {}})}\n\n"]
    print(f"🔧 [__DEV__] Query: '{user_message}' | Latency: {time.time() - start_time:.2f}s | Response: Error")
    return events + ["data: [DONE]\n\n"]


async def _guardrail_step(turn: ChatTurn) -> StepReply | None:
    """Core. Refuses a message the input guardrail flags, before any thread row is written."""
    # 1. Run Input Guardrail Check
    refusal = check_input_guardrail(turn.user_message)
    if refusal:
        error_event = {
            "event": "on_chat_model_stream",
            "name": "Guardrail",
            "run_id": "guardrail_violation",
            "data": {"chunk": {"content": refusal}},
        }
        return StepReply([f"data: {json.dumps(error_event)}\n\n"], log="Guardrail Refusal")
    return None


async def _save_thread_step(turn: ChatTurn) -> StepReply | None:
    """Core. Writes the thread row before any later step can checkpoint, or refuses a thread another browser owns.

    It has no try of its own: a failed save ends the turn with the error
    event. Passing on without the row would fail the checkpoint foreign key,
    possibly after a model call.
    """
    # Save title before streaming starts
    owned, created = await register_thread(turn.async_pool, turn.thread_id, turn.user_message, turn.owner_id)
    if not owned:
        return StepReply(_thread_refused_events())
    if created:
        start_title_generation(turn.async_pool, turn.thread_id, turn.user_message)
    return None


async def _triage_step(turn: ChatTurn) -> StepReply | None:
    """Optional. Answers simple chatter with fast_llm; a failure is logged and passes on."""
    user_message = turn.user_message
    # 3. Input Classifier (Triage)
    from backend.core.config import fast_llm
    from langchain_core.messages import SystemMessage

    triage_sys_prompt = """You are a high-speed triage classifier for a technical knowledge base agent.
Your job is to determine if a user query requires searching the technical knowledge base OR analyzing the chat history.

Rules:
1. If the query is simple conversational chatter (e.g., "hello", "hi", "thanks", "how are you"), respond with a short, friendly, and helpful reply.
2. If the query asks about what you can do or your general capabilities (e.g., "what can you help me with?", "what do you do?"), and does NOT explicitly ask for an example, provide a short 1-2 sentence summary: you are Victor's AI assistant, trained on over 20+ internal documentation files covering agentic theory, Python, React Native, UI/UX guidelines, and detailed internship logs.
3. If the query requires ANY technical knowledge, log retrieval, debugging, code explanations, explicitly asks for an example of what you can help with (e.g., "give me an example"), asks about the current chat session/history, asks what kind of logs you have, or repeats your fallback messages, you MUST respond with EXACTLY the string "ROUTE_TO_CORE" and nothing else.
"""

    try:
        triage_response = await fast_llm.ainvoke([
            SystemMessage(content=triage_sys_prompt), 
            HumanMessage(content=user_message)
        ])
        triage_content = triage_response.content.strip()

        if triage_content != "ROUTE_TO_CORE":
            print(f"⚡ [TRIAGE] Handled by fast classifier: {triage_content}")
            
            # Stream chunks to client
            events = []
            chunk_size = 120
            for i in range(0, len(triage_content), chunk_size):
                chunk = triage_content[i:i+chunk_size]
                safe_output = mask_sensitive_data(chunk)
                stream_event = {
                    "event": "on_chat_model_stream",
                    "name": "chatbot",
                    "run_id": "triage_stream",
                    "data": {"chunk": {"content": safe_output}}
                }
                events.append(f"data: {json.dumps(stream_event)}\n\n")

            # Persist to postgres memory
            ai_msg = AIMessage(content=triage_content)
            config = {"configurable": {"thread_id": turn.thread_id}}
            await turn.graph.aupdate_state(config, {"messages": [HumanMessage(content=user_message), ai_msg]}, as_node="chatbot")
                
            return StepReply(events, pause=0.01, log=f"'{triage_content[:100].replace(chr(10), ' ')}...'")

        print("🔍 [TRIAGE] Routing to CORE LangGraph Pipeline...")
    except Exception as e:
        print(f"⚠️ [WARNING] Fast classifier failed, falling back to core: {e}")
    return None


# The chat pre-steps, in order. Each returns a StepReply (it handled the
# message) or None (pass it on); the core graph path runs when all pass on.
# Core steps have no try of their own, so a failure ends the turn with the
# error event; optional steps catch their own failure and pass on.
PRE_STEPS = (_guardrail_step, _save_thread_step, _triage_step)


async def generate_chat_responses(user_message: str, thread_id: str, graph, async_pool, owner_id: str):
    """
    Handles input validation, LLM bypass check for direct problem queries,
    and streams responses from the LangGraph workflow.
    """
    start_time = time.time()
    turn = ChatTurn(user_message, thread_id, graph, async_pool, owner_id)
    for step in PRE_STEPS:
        try:
            reply = await step(turn)
        except Exception as e:
            for event in _error_events(e, user_message, start_time):
                yield event
            return
        if reply is not None:
            for event in reply.events:
                yield event
                if reply.pause:
                    await asyncio.sleep(reply.pause)
            if reply.log is not None:
                print(f"🔧 [__DEV__] Query: '{user_message}' | Latency: {time.time() - start_time:.2f}s | Response: {reply.log}")
            yield "data: [DONE]\n\n"
            return

    inputs = {"messages": [HumanMessage(content=user_message)]}
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # Get initial state to find if any tools ran in previous turns (for follow-ups)
        state = await graph.aget_state(config)
        last_tool_output_length = get_last_tool_output_length(state)

        generated_chars_count = 0
        full_response = ""
        stream_buffer = ""
        BUFFER_WINDOW = 120
        max_allowed = max(2000, last_tool_output_length + 1500)

        async for event in graph.astream_events(inputs, config, version="v2"):
            kind = event["event"]

            safe_event = {
                "event": kind,
                "name": event.get("name", ""),
                "run_id": event.get("run_id", ""),
                "data": {},
            }

            if kind == "on_chat_model_stream":
                # Block the expansion LLM from leaking into the UI stream
                if event.get("name") == "Expansion_LLM":
                    continue

                chunk = event["data"].get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    content = chunk.content
                    stream_buffer += content

                    if len(stream_buffer) > BUFFER_WINDOW:
                        to_output = stream_buffer[:-BUFFER_WINDOW]
                        stream_buffer = stream_buffer[-BUFFER_WINDOW:]

                        safe_output = mask_sensitive_data(to_output)
                        generated_chars_count += len(safe_output)

                        if generated_chars_count > max_allowed:
                            warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                            safe_event["data"]["chunk"] = {"content": warning}
                            yield f"data: {json.dumps(safe_event)}\n\n"
                            print(f"🔧 [__DEV__] Query: '{user_message}' | Latency: {time.time() - start_time:.2f}s | Response: Truncated")
                            yield "data: [DONE]\n\n"
                            return

                        safe_event["data"]["chunk"] = {"content": safe_output}
                        yield f"data: {json.dumps(safe_event)}\n\n"
                        full_response += safe_output

            elif kind in ["on_tool_start", "on_tool_end"]:
                if kind == "on_tool_end":
                    tool_output = event["data"].get("output")
                    if tool_output:
                        last_tool_output_length = get_content_length(tool_output)
                        max_allowed = max(2000, last_tool_output_length + 1500)
                yield f"data: {json.dumps(safe_event)}\n\n"

            elif kind == "on_chain_end" and event.get("name") in ["fast_path_node", "conversational_node", "fallback"]:
                output_data = event.get("data", {}).get("output", {})
                if isinstance(output_data, dict) and "messages" in output_data:
                    for msg in output_data["messages"]:
                        if msg.__class__.__name__ == "AIMessage" and msg.content:
                            content = msg.content
                            chunk_size = 120
                            for i in range(0, len(content), chunk_size):
                                chunk = content[i:i+chunk_size]
                                safe_output = mask_sensitive_data(chunk)
                                stream_event = {
                                    "event": "on_chat_model_stream",
                                    "name": "fast_path_node",
                                    "run_id": event.get("run_id", "fast_path_stream"),
                                    "data": {"chunk": {"content": safe_output}}
                                }
                                yield f"data: {json.dumps(stream_event)}\n\n"
                                await asyncio.sleep(0.01)
                            full_response += mask_sensitive_data(content)


        # Flush remaining buffer
        if stream_buffer:
            safe_output = mask_sensitive_data(stream_buffer)
            generated_chars_count += len(safe_output)

            flush_event = {
                "event": "on_chat_model_stream",
                "name": "chatbot",
                "run_id": "flush_buffer",
                "data": {"chunk": {"content": safe_output}}
            }

            if generated_chars_count > max_allowed:
                warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                flush_event["data"]["chunk"]["content"] = warning
                yield f"data: {json.dumps(flush_event)}\n\n"
            else:
                yield f"data: {json.dumps(flush_event)}\n\n"
                full_response += safe_output

        # Check if the graph is currently interrupted
        state = await graph.aget_state(config)
        is_interrupted = state.next and "sensitive_tools" in state.next

        if is_interrupted:
            # Send a special signal to the frontend
            interrupt_event = {
                "event": "on_agent_interrupt",
                "data": {"waiting_for": "tool_approval"}
            }
            yield f"data: {json.dumps(interrupt_event)}\n\n"

        print(f"🔧 [__DEV__] Query: '{user_message}' | Latency: {time.time() - start_time:.2f}s | Response: '{full_response[:100].replace(chr(10), ' ')}...'")
        yield "data: [DONE]\n\n"

    except Exception as e:
        for event in _error_events(e, user_message, start_time):
            yield event


async def resume_graph_stream(thread_id: str, graph):
    """Resumes the graph from the exact point it was paused."""
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state = await graph.aget_state(config)
        print(f"🤖 [DEBUG] resume_graph_stream state for thread {thread_id}: next = {state.next if state else None}")

        last_tool_output_length = get_last_tool_output_length(state)
        generated_chars_count = 0
        full_response = ""
        stream_buffer = ""
        BUFFER_WINDOW = 120
        max_allowed = max(2000, last_tool_output_length + 1500)

        # Passing 'None' tells LangGraph to pick up exactly where it left off
        async for event in graph.astream_events(None, config, version="v2"):
            kind = event["event"]
            safe_event = {
                "event": kind,
                "name": event.get("name", ""),
                "run_id": event.get("run_id", ""),
                "data": {},
            }

            if kind == "on_chat_model_stream":
                if event.get("name") == "Expansion_LLM":
                    continue
                chunk = event["data"].get("chunk")
                if chunk and hasattr(chunk, "content") and chunk.content:
                    content = chunk.content
                    stream_buffer += content

                    if len(stream_buffer) > BUFFER_WINDOW:
                        to_output = stream_buffer[:-BUFFER_WINDOW]
                        stream_buffer = stream_buffer[-BUFFER_WINDOW:]

                        safe_output = mask_sensitive_data(to_output)
                        generated_chars_count += len(safe_output)

                        if generated_chars_count > max_allowed:
                            warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                            safe_event["data"]["chunk"] = {"content": warning}
                            yield f"data: {json.dumps(safe_event)}\n\n"
                            yield "data: [DONE]\n\n"
                            return

                        safe_event["data"]["chunk"] = {"content": safe_output}
                        yield f"data: {json.dumps(safe_event)}\n\n"
                        full_response += safe_output

            elif kind in ["on_tool_start", "on_tool_end"]:
                if kind == "on_tool_end":
                    tool_output = event["data"].get("output")
                    if tool_output:
                        last_tool_output_length = get_content_length(tool_output)
                        max_allowed = max(2000, last_tool_output_length + 1500)
                yield f"data: {json.dumps(safe_event)}\n\n"

            elif kind == "on_chain_end" and event.get("name") in ["fast_path_node", "conversational_node", "fallback"]:
                output_data = event.get("data", {}).get("output", {})
                if isinstance(output_data, dict) and "messages" in output_data:
                    for msg in output_data["messages"]:
                        if msg.__class__.__name__ == "AIMessage" and msg.content:
                            content = msg.content
                            chunk_size = 120
                            for i in range(0, len(content), chunk_size):
                                chunk = content[i:i+chunk_size]
                                safe_output = mask_sensitive_data(chunk)
                                stream_event = {
                                    "event": "on_chat_model_stream",
                                    "name": "fast_path_node",
                                    "run_id": event.get("run_id", "fast_path_stream"),
                                    "data": {"chunk": {"content": safe_output}}
                                }
                                yield f"data: {json.dumps(stream_event)}\n\n"
                                await asyncio.sleep(0.01)
                            full_response += mask_sensitive_data(content)


        # Flush remaining buffer
        if stream_buffer:
            safe_output = mask_sensitive_data(stream_buffer)
            generated_chars_count += len(safe_output)

            flush_event = {
                "event": "on_chat_model_stream",
                "name": "chatbot",
                "run_id": "flush_buffer",
                "data": {"chunk": {"content": safe_output}}
            }

            if generated_chars_count > max_allowed:
                warning = "\n\n⚠️ [Output Truncated: Security Guardrail - Response length limit exceeded to prevent token abuse]"
                flush_event["data"]["chunk"]["content"] = warning
                yield f"data: {json.dumps(flush_event)}\n\n"
            else:
                yield f"data: {json.dumps(flush_event)}\n\n"
                full_response += safe_output

        # Check if it hit ANOTHER interrupt (unlikely, but good practice)
        state = await graph.aget_state(config)
        is_interrupted = state.next and "sensitive_tools" in state.next
        if is_interrupted:
            interrupt_event = {
                "event": "on_agent_interrupt",
                "data": {"waiting_for": "tool_approval"}
            }
            yield f"data: {json.dumps(interrupt_event)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        import traceback
        print("🚨 resume_graph_stream Crash Details:")
        traceback.print_exc()
        if is_credit_limit_refusal(e):
            print("🔧 [__DEV__] resume_graph_stream | is_credit_limit_refusal matched (403, scope key_limit) | Response: demo paused line")
            yield _demo_paused_event()
        else:
            yield f"data: {json.dumps({'event': 'on_error', 'name': 'error', 'run_id': 'error', 'data': {}})}\n\n"
        yield "data: [DONE]\n\n"
