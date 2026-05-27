# backend/core/guardrails.py
import os
import re
import json


def check_input_guardrail(message: str) -> str | None:
    """
    Checks user input for jailbreak or token-burning attempts.
    Returns a refusal message if a violation is found, or None if safe.
    """
    # 1. Length Cap
    if len(message) > 1000:
        return "⚠️ [Input Filter] Message too long. Please limit your query to under 1,000 characters."

    # 2. Pattern Matching
    lower_msg = message.lower().strip()
    
    # Check for prompt injection / jailbreak words
    jailbreak_keywords = [
        "ignore all previous", "ignore previous instructions", "ignore guidelines",
        "ignore rules", "ignore previous rules", "ignore all previous rules",
        "bypass rules", "you are now a", "jailbreak", "developer mode",
        "acting as a", "override instructions", "expose your system prompt",
        "reveal your system prompt", "api key", "database password", "db password"
    ]
    for kw in jailbreak_keywords:
        if kw in lower_msg:
            return "⚠️ [Input Filter] Request blocked. This query violates security guidelines regarding prompt modification or credential request."

    # Check for token-burning patterns (excessive text generation request)
    token_burn_patterns = [
        # Match "write a long fantasy story", "tell me a story", "generate a short creative poem", etc.
        r"\b(?:write|generate|create|compose|tell|tell\s+me)\s+(?:a|an|me|us|the)?\s+(?:[a-zA-Z0-9]+\s+){0,5}(?:story|essay|novel|poem|play|song|script|article|report)\b",
        # Match standalone large word counts (e.g., "3000 words", "1500 word", "3k words") anywhere in the text
        r"\b\d{3,}\s*(?:words?|k\s*words?|thousand\s*words?)\b",
        r"\b\d+\s*k\s*words?\b",
        # Match "repeat this word", "repeat after me", "copy the text", etc.
        r"\b(?:repeat|copy|duplicate|print)\s+(?:this|the|following|word|character|sentence|paragraph|text|after\s+me)\b",
        # Match "loop indefinitely", "repeat forever", etc.
        r"\b(?:repeat|loop|print|run)\s+(?:[a-zA-Z]+\s+){0,3}(?:indefinitely|forever|infinite|again\s+and\s+again)\b",
    ]
    for pattern in token_burn_patterns:
        if re.search(pattern, lower_msg):
            return "⚠️ [Input Filter] Request blocked. Requests for excessive content generation (e.g., stories, essays, infinite loops) are restricted to protect API quotas."

    return None


def get_content_length(data) -> int:
    """Helper to safely calculate the character length of any content/output data."""
    if not data:
        return 0
    if isinstance(data, str):
        return len(data)
    if isinstance(data, list):
        return sum(get_content_length(item) for item in data)
    if isinstance(data, dict):
        if "content" in data:
            return get_content_length(data["content"])
        if "output" in data:
            return get_content_length(data["output"])
        try:
            return len(json.dumps(data))
        except Exception:
            return len(str(data))
    if hasattr(data, "content"):
        return get_content_length(data.content)
    return len(str(data))


def get_last_tool_output_length(state) -> int:
    """Helper to find the length of the last tool output in the chat history."""
    if not state or not hasattr(state, "values") or "messages" not in state.values:
        return 0
    # Search backwards for the last tool message
    for msg in reversed(state.values["messages"]):
        if msg.type == "tool" and msg.content:
            return get_content_length(msg.content)
    return 0


def mask_sensitive_data(text: str) -> str:
    """Scans and masks any API keys, DB passwords, or credentials before sending."""
    if not text:
        return text
    
    # Mask environment variable values dynamically
    sensitive_keys = ["OPENROUTER_API_KEY", "DATABASE_URL", "PGPASSWORD", "LANGCHAIN_API_KEY"]
    for key in sensitive_keys:
        val = os.getenv(key)
        if val and len(val) > 4 and val in text:
            text = text.replace(val, "[REDACTED SECRET]")
            
    # Mask typical OpenRouter / OpenAI API keys (sk-or-v1-...) with flexible length
    text = re.sub(r"\bsk-or-v1-[a-zA-Z0-9]{40,80}\b", "[REDACTED OPENROUTER KEY]", text)
    # Mask other typical API keys with flexible length
    text = re.sub(r"\bsk-[a-zA-Z0-9]{32,64}\b", "[REDACTED API KEY]", text)
    # Mask DB password patterns in connection strings
    text = re.sub(r"postgresql://[^:]+:([^@]+)@", "postgresql://user:[REDACTED_PASSWORD]@", text)
    
    return text
