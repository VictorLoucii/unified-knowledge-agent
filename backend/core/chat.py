# backend/core/chat.py
import json
import asyncio
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

from backend.core.config import parse_problem_id, extract_problem_block, cache_vectorstore, SEMANTIC_CACHE_THRESHOLD
from backend.core.guardrails import (
    check_input_guardrail,
    mask_sensitive_data,
    get_content_length,
    get_last_tool_output_length,
)
from backend.memory import save_thread_title


def is_excluded_from_cache(message: str) -> bool:
    """Checks if a user query should be excluded from semantic caching."""
    if not message:
        return True
    
    # Exclude exact problem-log requests (since they are handled deterministically by Programmatic Bypass)
    if parse_problem_id(message):
        return True
    
    # Exclude short general phrases (e.g., "hi", "ok", "yes")
    clean_msg = message.strip().lower()
    common_short_phrases = {
        "hi", "hello", "hey", "ok", "yes", "no", "thanks", "thank you", "bye", "goodbye", "help",
        "yep", "yup", "sure", "correct", "perfect", "awesome", "great"
    }
    if len(clean_msg) < 4 or clean_msg in common_short_phrases:
        return True
    
    return False


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
            await graph.aupdate_state(config, {"messages": [HumanMessage(content=user_message), tool_msg, ai_msg]}, as_node="chatbot")

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

    # 2.5. Check Semantic Cache
    if not is_excluded_from_cache(user_message):
        try:
            results = cache_vectorstore.similarity_search_with_relevance_scores(user_message, k=1)
            if results and results[0][1] >= SEMANTIC_CACHE_THRESHOLD:
                match_doc, score = results[0]
                cached_response = match_doc.metadata.get("response")
                if cached_response:
                    print(f"🎯 [CACHE HIT] Found match with score {score:.4f} for: {user_message}")
                    # Save title before streaming starts
                    await save_thread_title(async_pool, thread_id, user_message)

                    # Persist state directly in PostgreSQL history
                    ai_msg = AIMessage(content=cached_response)
                    config = {"configurable": {"thread_id": thread_id}}
                    await graph.aupdate_state(config, {"messages": [HumanMessage(content=user_message), ai_msg]}, as_node="chatbot")

                    # Stream the response chunk by chunk to simulate natural real-time streaming
                    chunk_size = 120
                    for i in range(0, len(cached_response), chunk_size):
                        chunk = cached_response[i:i+chunk_size]
                        safe_output = mask_sensitive_data(chunk)
                        stream_event = {
                            "event": "on_chat_model_stream",
                            "name": "chatbot",
                            "run_id": "cache_stream",
                            "data": {"chunk": {"content": safe_output}}
                        }
                        yield f"data: {json.dumps(stream_event)}\n\n"
                        await asyncio.sleep(0.01)

                    yield "data: [DONE]\n\n"
                    return
        except Exception as e:
            print(f"⚠️ [WARNING] Semantic cache lookup failed: {e}")

    # 3. Input Classifier (Triage)
    from backend.core.config import fast_llm
    from langchain_core.messages import SystemMessage

    triage_sys_prompt = """You are a high-speed triage classifier for a technical knowledge base agent.
Your job is to determine if a user query requires searching the technical knowledge base OR analyzing the chat history.

Rules:
1. If the query is simple conversational chatter (e.g., "hello", "hi", "thanks", "how are you"), respond with a short, friendly, and helpful reply.
2. If the query is asking about what you can do or your capabilities (but does NOT specifically ask for an example), provide a short 1-2 sentence summary: you are the Nexteir Internal Knowledge Base, here to help with internship logs and technical queries.
3. If the query requires ANY technical knowledge, log retrieval, debugging, code explanations, asks for an example of what you can help with, OR asks about the current chat session/history (e.g., "what was my first question", "what did we discuss", "how many queries"), you MUST respond with EXACTLY the string "ROUTE_TO_CORE" and nothing else.
"""

    try:
        triage_response = await fast_llm.ainvoke([
            SystemMessage(content=triage_sys_prompt), 
            HumanMessage(content=user_message)
        ])
        triage_content = triage_response.content.strip()

        if triage_content != "ROUTE_TO_CORE":
            print(f"⚡ [TRIAGE] Handled by fast classifier: {triage_content}")
            # Save title before streaming starts
            await save_thread_title(async_pool, thread_id, user_message)
            
            # Persist to postgres memory
            ai_msg = AIMessage(content=triage_content)
            config = {"configurable": {"thread_id": thread_id}}
            await graph.aupdate_state(config, {"messages": [HumanMessage(content=user_message), ai_msg]}, as_node="chatbot")

            # Stream chunks to client
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
                yield f"data: {json.dumps(stream_event)}\n\n"
                await asyncio.sleep(0.01)
                
            yield "data: [DONE]\n\n"
            return

        print("🔍 [TRIAGE] Routing to CORE LangGraph Pipeline...")
    except Exception as e:
        print(f"⚠️ [WARNING] Fast classifier failed, falling back to core: {e}")

    inputs = {"messages": [HumanMessage(content=user_message)]}
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # Save title before streaming starts
        await save_thread_title(async_pool, thread_id, user_message)

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
        is_interrupted = state.next and "tools" in state.next

        if is_interrupted:
            # Send a special signal to the frontend
            interrupt_event = {
                "event": "on_agent_interrupt",
                "data": {"waiting_for": "tool_approval"}
            }
            yield f"data: {json.dumps(interrupt_event)}\n\n"
        else:
            # Save successful response to cache if not truncated and not excluded
            if generated_chars_count <= max_allowed and full_response.strip() and not is_excluded_from_cache(user_message):
                try:
                    cache_vectorstore.add_texts(
                        texts=[user_message],
                        metadatas=[{"response": full_response}]
                    )
                    print(f"💾 [CACHE STORE] Saved query and response to semantic cache.")
                except Exception as e:
                    print(f"⚠️ [WARNING] Failed to save query to semantic cache: {e}")

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
        is_interrupted = state.next and "tools" in state.next
        if is_interrupted:
            interrupt_event = {
                "event": "on_agent_interrupt",
                "data": {"waiting_for": "tool_approval"}
            }
            yield f"data: {json.dumps(interrupt_event)}\n\n"
        else:
            # Resolve the original user message from the thread history
            user_message = ""
            if state and hasattr(state, "values") and "messages" in state.values:
                for msg in reversed(state.values["messages"]):
                    if msg.type == "human":
                        user_message = msg.content
                        break
            # Save successful response to cache if not truncated and not excluded
            if user_message and generated_chars_count <= max_allowed and full_response.strip() and not is_excluded_from_cache(user_message):
                try:
                    cache_vectorstore.add_texts(
                        texts=[user_message],
                        metadatas=[{"response": full_response}]
                    )
                    print(f"💾 [CACHE STORE] Saved query and response to semantic cache from resume.")
                except Exception as e:
                    print(f"⚠️ [WARNING] Failed to save query to semantic cache from resume: {e}")

        yield "data: [DONE]\n\n"

    except Exception as e:
        import traceback
        print("🚨 resume_graph_stream Crash Details:")
        traceback.print_exc()
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"
