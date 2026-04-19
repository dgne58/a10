import json
import os
import time
import uuid
from collections.abc import Generator

import httpx
from dotenv import load_dotenv
from config import COST_PER_1M, FALLBACK_MODEL

load_dotenv()

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")


def compute_cost(usage: dict, model_id: str) -> float:
    total_tokens = usage.get("total_tokens", 0)
    rate = COST_PER_1M.get(model_id, 0.35)
    return round((total_tokens / 1_000_000) * rate, 8)


def call_model(model_id: str, query: str, max_tokens: int = 512, system: str | None = None) -> dict:
    t0 = time.monotonic()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": query})

    last_err: Exception | None = None
    for attempt in range(3):
        if attempt:
            time.sleep(2 ** attempt)
        try:
            resp = httpx.post(
                f"{OPENROUTER_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "HTTP-Referer": "https://hackathon-router.dev",
                    "X-Title": "Task-Aware Cost Router",
                },
                json={
                    "model": model_id,
                    "messages": messages,
                    "max_tokens": max_tokens,
                },
                timeout=60.0,
            )
            resp.raise_for_status()
            data = resp.json()
            if "choices" not in data:
                raise ValueError(f"No choices in response: {data}")
            latency_ms = int((time.monotonic() - t0) * 1000)
            usage = data.get("usage", {})
            return {
                "answer": data["choices"][0]["message"]["content"],
                "usage": usage,
                "latency_ms": latency_ms,
                "cost_usd": compute_cost(usage, model_id),
            }
        except (httpx.TimeoutException, httpx.HTTPStatusError, ValueError) as e:
            last_err = e
    raise RuntimeError(f"call_model failed after 3 attempts: {last_err}")


def stream_model(
    model_id: str,
    query: str,
    max_tokens: int = 512,
    system: str | None = None,
    messages: list[dict] | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> Generator[str, None, None]:
    """Yield text chunks from OpenRouter streaming completions.

    Pass `messages` directly to override the default user/system construction
    (used for tool follow-up calls where the conversation already exists).
    """
    if messages is None:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": query})
    _sm_endpoint = f"{base_url or OPENROUTER_BASE}/chat/completions"
    _sm_key = api_key or API_KEY
    _sm_headers: dict = {"Content-Type": "application/json"}
    if _sm_key:
        _sm_headers["Authorization"] = f"Bearer {_sm_key}"
    if not base_url:
        _sm_headers["HTTP-Referer"] = "https://hackathon-router.dev"
        _sm_headers["X-Title"] = "Task-Aware Cost Router"
    with httpx.stream(
        "POST",
        _sm_endpoint,
        headers=_sm_headers,
        json={
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
        },
        timeout=30.0,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line.startswith("data: "):
                continue
            payload = line[6:]
            if payload.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(payload)
                delta = chunk["choices"][0]["delta"].get("content") or ""
                if delta:
                    yield delta
            except (json.JSONDecodeError, KeyError, IndexError):
                continue


_TEXT_TOOL_NAMES = {"fetch_url", "execute_python", "lint_python", "regex_test", "calculate"}


def _parse_text_tool_call(text: str) -> dict | None:
    """Detect models that output tool calls as plain-text JSON instead of using
    finish_reason='tool_calls'. Returns a normalised tool_call dict or None."""
    stripped = text.strip()
    if not (stripped.startswith("{") and stripped.endswith("}")):
        return None
    try:
        obj = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    name = obj.get("name") or obj.get("function") or obj.get("tool")
    if name not in _TEXT_TOOL_NAMES:
        return None
    # Accept either "parameters" or "arguments" key
    raw_args = obj.get("parameters") or obj.get("arguments") or obj.get("input") or {}
    args_str = json.dumps(raw_args) if isinstance(raw_args, dict) else str(raw_args)
    return {
        "id": f"call_{uuid.uuid4().hex[:8]}",
        "type": "function",
        "function": {"name": name, "arguments": args_str},
    }


def stream_with_tools(
    model_id: str,
    messages: list[dict],
    tools: list[dict] | None = None,
    max_tokens: int = 1024,
    base_url: str | None = None,
    api_key: str | None = None,
) -> Generator[str | dict, None, None]:
    """Stream from OpenRouter with optional tool support.

    Yields str tokens for direct content. If the model calls a tool (via either
    structured finish_reason='tool_calls' OR plain-text JSON fallback), the final
    yielded item is {"tool_call": <tool_call_dict>} and no content tokens are emitted.
    """
    accumulated_tc: dict[int, dict] = {}
    buffered_tokens: list[str] = []

    payload: dict = {
        "model": model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": True,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    structured_tool_call = False

    endpoint = f"{base_url or OPENROUTER_BASE}/chat/completions"
    _key = api_key or API_KEY
    _headers: dict = {"Content-Type": "application/json"}
    if _key:
        _headers["Authorization"] = f"Bearer {_key}"
    if not base_url:
        _headers["HTTP-Referer"] = "https://hackathon-router.dev"
        _headers["X-Title"] = "Task-Aware Cost Router"

    with httpx.stream(
        "POST",
        endpoint,
        headers=_headers,
        json=payload,
        timeout=30.0,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line.startswith("data: "):
                continue
            raw = line[6:]
            if raw.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(raw)
                choice = chunk["choices"][0]
                delta = choice.get("delta", {})
                finish = choice.get("finish_reason")

                content = delta.get("content")
                if content:
                    buffered_tokens.append(content)

                for tc_delta in delta.get("tool_calls", []):
                    idx = tc_delta.get("index", 0)
                    if idx not in accumulated_tc:
                        accumulated_tc[idx] = {
                            "id": tc_delta.get("id", f"call_{uuid.uuid4().hex[:8]}"),
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        }
                    fn = tc_delta.get("function", {})
                    accumulated_tc[idx]["function"]["name"] += fn.get("name", "")
                    accumulated_tc[idx]["function"]["arguments"] += fn.get("arguments", "")

                if finish == "tool_calls" and accumulated_tc:
                    structured_tool_call = True
                    yield {"tool_call": accumulated_tc[0]}
                    return

            except (json.JSONDecodeError, KeyError, IndexError):
                continue

    # No structured tool call — check if model outputted a text-format tool call
    full_text = "".join(buffered_tokens)
    text_tc = _parse_text_tool_call(full_text)
    if text_tc:
        yield {"tool_call": text_tc}
        return

    # Normal content — flush buffered tokens
    for tok in buffered_tokens:
        yield tok


def stream_local_rag(
    wiki_context: str,
    query: str,
    cheap_url: str,
    max_tokens: int = 1024,
) -> Generator[str, None, None]:
    """Stream a RAG answer from the local vLLM endpoint using wiki page as context."""
    prompt = (
        "You are a technical assistant. Answer the question using only the context below. "
        "Be concise and direct.\n\n"
        f"Context:\n{wiki_context}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )
    payload = {
        "model": "llama-8b-code",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "stream": True,
    }
    with httpx.stream(
        "POST",
        f"{cheap_url}/chat/completions",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30.0,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line.startswith("data: "):
                continue
            raw = line[6:]
            if raw.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(raw)
                delta = chunk["choices"][0]["delta"].get("content") or ""
                if delta:
                    yield delta
            except (json.JSONDecodeError, KeyError, IndexError):
                continue


def call_with_fallback(model_id: str, query: str) -> dict:
    try:
        result = call_model(model_id, query)
        return {**result, "used_fallback": False}
    except Exception as e:
        result = call_model(FALLBACK_MODEL, query)
        return {**result, "used_fallback": True, "fallback_reason": str(e)}
