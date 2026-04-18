import json
import os
import time
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
        timeout=15.0,
    )
    resp.raise_for_status()
    data = resp.json()
    latency_ms = int((time.monotonic() - t0) * 1000)
    usage = data.get("usage", {})
    return {
        "answer": data["choices"][0]["message"]["content"],
        "usage": usage,
        "latency_ms": latency_ms,
        "cost_usd": compute_cost(usage, model_id),
    }


def stream_model(
    model_id: str,
    query: str,
    max_tokens: int = 512,
    system: str | None = None,
    messages: list[dict] | None = None,
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
    with httpx.stream(
        "POST",
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


def stream_with_tools(
    model_id: str,
    messages: list[dict],
    tools: list[dict] | None = None,
    max_tokens: int = 1024,
) -> Generator[str | dict, None, None]:
    """Stream from OpenRouter with optional tool support.

    Yields str tokens for direct content. If the model calls a tool, the final
    yielded item is {"tool_call": <tool_call_dict>} and content will be empty.
    """
    accumulated_tc: dict[int, dict] = {}

    payload: dict = {
        "model": model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": True,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    with httpx.stream(
        "POST",
        f"{OPENROUTER_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "https://hackathon-router.dev",
            "X-Title": "Task-Aware Cost Router",
        },
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
                    yield content

                for tc_delta in delta.get("tool_calls", []):
                    idx = tc_delta.get("index", 0)
                    if idx not in accumulated_tc:
                        accumulated_tc[idx] = {
                            "id": tc_delta.get("id", ""),
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        }
                    fn = tc_delta.get("function", {})
                    accumulated_tc[idx]["function"]["name"] += fn.get("name", "")
                    accumulated_tc[idx]["function"]["arguments"] += fn.get("arguments", "")

                if finish == "tool_calls" and accumulated_tc:
                    yield {"tool_call": accumulated_tc[0]}

            except (json.JSONDecodeError, KeyError, IndexError):
                continue


def call_with_fallback(model_id: str, query: str) -> dict:
    try:
        result = call_model(model_id, query)
        return {**result, "used_fallback": False}
    except Exception as e:
        result = call_model(FALLBACK_MODEL, query)
        return {**result, "used_fallback": True, "fallback_reason": str(e)}
