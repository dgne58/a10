from typing import Optional
from config import COST_PER_1M, FALLBACK_MODEL, MODEL_MAP
from memory import check_memory
from openrouter import call_with_fallback, compute_cost

HARD_KEYWORDS = {
    "why", "explain", "compare", "analyze", "critique",
    "implications", "evaluate", "derive", "prove", "pros and cons",
}
MEDIUM_KEYWORDS = {
    "how", "describe", "summarize", "difference between", "steps to", "what causes",
}
CODE_KEYWORDS = {
    "code", "function", "debug", "python", "javascript",
    "implement", "algorithm", "class", "error", "typescript",
}
MATH_KEYWORDS = {
    "calculate", "solve", "equation", "integral",
    "derivative", "probability", "theorem", "proof",
}
PROJECT_KEYWORDS = {
    "what does the project", "what models does", "what architecture",
    "what files", "which wiki", "what is the routing", "what components",
}


def classify(query: str) -> dict:
    q = query.lower()
    word_count = len(query.split())

    # Project/codebase questions should still go memory first, then fall
    # through to the cheapest model path if memory misses.
    if any(w in q for w in PROJECT_KEYWORDS):
        return {"complexity": "simple", "domain": "factual"}

    if any(w in q for w in CODE_KEYWORDS):
        domain = "code"
    elif any(w in q for w in MATH_KEYWORDS):
        domain = "math"
    else:
        domain = "factual"

    if any(w in q for w in HARD_KEYWORDS) or word_count > 40:
        complexity = "hard"
    elif any(w in q for w in MEDIUM_KEYWORDS) or word_count > 20 or domain in {"code", "math"}:
        complexity = "medium"
    else:
        complexity = "simple"

    return {"complexity": complexity, "domain": domain}


def select_branch(label: dict) -> str:
    mapping = {
        "simple": "cheap_model",
        "medium": "mid_model",
        "hard": "strong_model",
    }
    return mapping.get(label["complexity"], "strong_model")


def select_model(label: dict) -> str:
    branch = select_branch(label)
    return MODEL_MAP.get(branch, FALLBACK_MODEL)


def build_rationale(label: dict, branch: str, model_id: Optional[str]) -> str:
    branch_labels = {
        "memory_answer": "answered from local memory",
        "cheap_model": f"simple query -> cheapest model ({model_id})",
        "mid_model": f"medium query -> mid-tier model ({model_id})",
        "strong_model": f"hard query -> strong model ({model_id})",
    }
    complexity = label.get("complexity", "")
    domain = label.get("domain", "")
    label_str = f"{complexity} {domain}".strip().capitalize()
    return f"{label_str} - {branch_labels.get(branch, branch)}"


def _naive_cost(usage: dict) -> float:
    tokens = usage.get("total_tokens", 0)
    return round((tokens / 1_000_000) * COST_PER_1M.get("anthropic/claude-sonnet-4.6", 3.00), 8)


def route_and_call(query: str) -> dict:
    memory_hit = check_memory(query)
    if memory_hit:
        return memory_hit

    label = classify(query)
    branch = select_branch(label)
    model = MODEL_MAP.get(branch, FALLBACK_MODEL)
    result = call_with_fallback(model, query)
    actual_model = FALLBACK_MODEL if result["used_fallback"] else model
    cost = compute_cost(result["usage"], actual_model)
    rationale = build_rationale(label, branch, actual_model)

    return {
        "answer": result["answer"],
        "branch": branch,
        "model_used": actual_model,
        "rationale": rationale,
        "cost_usd": cost,
        "naive_cost_usd": _naive_cost(result["usage"]),
        "latency_ms": result["latency_ms"],
        "fallback": result["used_fallback"],
        "source_ref": None,
    }
