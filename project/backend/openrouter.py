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


def stream_model(model_id: str, query: str, max_tokens: int = 512, system: str | None = None) -> Generator[str, None, None]:
    """Yield text chunks from OpenRouter streaming completions."""
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


def call_with_fallback(model_id: str, query: str) -> dict:
    try:
        result = call_model(model_id, query)
        return {**result, "used_fallback": False}
    except Exception as e:
        result = call_model(FALLBACK_MODEL, query)
        return {**result, "used_fallback": True, "fallback_reason": str(e)}
