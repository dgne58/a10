import os
import time
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


def call_model(model_id: str, query: str, max_tokens: int = 512) -> dict:
    t0 = time.monotonic()
    resp = httpx.post(
        f"{OPENROUTER_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "https://hackathon-router.dev",
            "X-Title": "Task-Aware Cost Router",
        },
        json={
            "model": model_id,
            "messages": [{"role": "user", "content": query}],
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


def call_with_fallback(model_id: str, query: str) -> dict:
    try:
        result = call_model(model_id, query)
        return {**result, "used_fallback": False}
    except Exception as e:
        result = call_model(FALLBACK_MODEL, query)
        return {**result, "used_fallback": True, "fallback_reason": str(e)}
