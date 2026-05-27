# backend/core/chat.py
import json
import asyncio
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

from backend.core.config import parse_problem_id, extract_problem_block
from backend.core.guardrails import (
    check_input_guardrail,
    mask_sensitive_data,
    get_content_length,
    get_last_tool_output_length,
)
from backend.memory import save_thread_title


async def generate_chat_responses(user_message: str, thread_id: str, graph, async_pool):
    """
    Handles input validation, LLM bypass check for direct problem queries,
    and streams responses from the LangGraph workflow.
    """
    # 1. Run Input Guardrail Check
    refusal = check_input_guardrail(user_message)
    if refusal:
        # Save title before streaming starts
        await save_thread_title(async_pool, thread_id, user_message)
        error_event = {
            "event": "on_chat_model_stream",
            "name": "Guardrail",
            "run_id": "guardrail_violation",
            "data": {"chunk": {"content": refusal}},
        }
        yield f"data: {json.dumps(error_event)}\n\n"
        yield "data: [DONE]\n\n"
        return

    # 2. Check for Programmatic LLM Bypass Candidate
    problem_id = parse_problem_id(user_message)
    if problem_id:
        block = extract_problem_block(problem_id)
        if block:
            # Save title before streaming starts
            await save_thread_title(async_pool, thread_id, user_message)

            # Persist state directly in PostgreSQL history
            tool_msg = ToolMessage(
                content=f"<!-- RETRIEVED_PROBLEM_IDS: [{problem_id}] -->",
                name="search_internship_history",
                tool_call_id="bypass_tool_call_id"
            )
            ai_msg = AIMessage(content=block)

            config = {"configurable": {"thread_id": thread_id}}
            await graph.aupdate_state(config, {"messages": [HumanMessage(content=user_message), tool_msg, ai_msg]})

            # Stream the response chunk by chunk to simulate natural real-time streaming
            chunk_size = 120
            for i in range(0, len(block), chunk_size):
                chunk = block[i:i+chunk_size]
                safe_output = mask_sensitive_data(chunk)
                stream_event = {
                    "event": "on_chat_model_stream",
                    "name": "chatbot",
                    "run_id": "bypass_stream",
                    "data": {"chunk": {"content": safe_output}}
                }
                yield f"data: {json.dumps(stream_event)}\n\n"
                await asyncio.sleep(0.01)

            yield "data: [DONE]\n\n"
            return

    inputs = {"messages": [HumanMessage(content=user_message)]}
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # Save title before streaming starts
        await save_thread_title(async_pool, thread_id, user_message)

        # Get initial state to find if any tools ran in previous turns (for follow-ups)
        state = await graph.aget_state(config)
        last_tool_output_length = get_last_tool_output_length(state)

        generated_chars_count = 0
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
                            yield "data: [DONE]\n\n"
                            return

                        safe_event["data"]["chunk"] = {"content": safe_output}
                        yield f"data: {json.dumps(safe_event)}\n\n"

            elif kind in ["on_tool_start", "on_tool_end"]:
                if kind == "on_tool_end":
                    tool_output = event["data"].get("output")
                    if tool_output:
                        last_tool_output_length = get_content_length(tool_output)
                        max_allowed = max(2000, last_tool_output_length + 1500)
                yield f"data: {json.dumps(safe_event)}\n\n"

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

        # Check if the graph is currently interrupted
        state = await graph.aget_state(config)
        if state.next and "tools" in state.next:
            # Send a special signal to the frontend
            interrupt_event = {
                "event": "on_agent_interrupt",
                "data": {"waiting_for": "tool_approval"}
            }
            yield f"data: {json.dumps(interrupt_event)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        import traceback

        print("🚨 Backend Crash Details:")
        traceback.print_exc()

        print(f"🚨 Raw Error: {repr(e)}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"


async def resume_graph_stream(thread_id: str, graph):
    """Resumes the graph from the exact point it was paused."""
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state = await graph.aget_state(config)
        print(f"🤖 [DEBUG] resume_graph_stream state for thread {thread_id}: next = {state.next if state else None}")

        last_tool_output_length = get_last_tool_output_length(state)
        generated_chars_count = 0
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

            elif kind in ["on_tool_start", "on_tool_end"]:
                if kind == "on_tool_end":
                    tool_output = event["data"].get("output")
                    if tool_output:
                        last_tool_output_length = get_content_length(tool_output)
                        max_allowed = max(2000, last_tool_output_length + 1500)
                yield f"data: {json.dumps(safe_event)}\n\n"

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

        # Check if it hit ANOTHER interrupt (unlikely, but good practice)
        state = await graph.aget_state(config)
        if state.next and "tools" in state.next:
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
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"
