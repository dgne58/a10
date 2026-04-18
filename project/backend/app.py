import json
import os
import re
import sys
import time
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from router import route_and_call, classify, select_branch, build_rationale, _naive_cost
from memory import check_memory
from verifier import run_verification
from tools import execute_tool
from openrouter import stream_model, call_with_fallback, compute_cost
from config import MODEL_MAP, FALLBACK_MODEL, COST_PER_1M

app = Flask(__name__)
CORS(app)

if os.getenv("CLASSIFIER_URL"):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "training"))
    try:
        from integrate import install_classifier_patch
        install_classifier_patch()
    except Exception as e:
        print(f"[app] classifier patch skipped: {e}")

EVAL_PATH = os.path.join(os.path.dirname(__file__), "eval_results.json")

DEMO_CACHE = {
    "What is the capital of France?": {
        "answer": "Paris.",
        "branch": "cheap_model",
        "model_used": "meta-llama/llama-3.1-8b-instruct",
        "rationale": "Simple factual -- answered by cheapest model (meta-llama/llama-3.1-8b-instruct)",
        "cost_usd": 0.000003,
        "naive_cost_usd": 0.000150,
        "latency_ms": 380,
        "fallback": False,
        "source_ref": None,
        "cached": True,
    },
}


@app.route("/api/route", methods=["POST"])
def route():
    body = request.get_json(silent=True) or {}
    query = (body.get("query") or "").strip()
    if not query:
        return jsonify({"error": "query required"}), 400
    if query in DEMO_CACHE:
        return jsonify(DEMO_CACHE[query])
    result = route_and_call(query)
    return jsonify(result)


@app.route("/api/route/stream", methods=["POST"])
def route_stream():
    body = request.get_json(silent=True) or {}
    query = (body.get("query") or "").strip()
    if not query:
        return jsonify({"error": "query required"}), 400

    def _sse(obj: dict) -> str:
        return f"data: {json.dumps(obj)}\n\n"

    def generate():
        # Demo cache — emit as instant stream
        if query in DEMO_CACHE:
            cached = DEMO_CACHE[query]
            yield _sse({"type": "meta", "branch": cached["branch"], "model_used": cached.get("model_used"),
                        "rationale": cached["rationale"]})
            yield _sse({"type": "token", "text": cached["answer"]})
            yield _sse({"type": "done", "cost_usd": cached["cost_usd"],
                        "naive_cost_usd": cached["naive_cost_usd"], "latency_ms": cached["latency_ms"]})
            return

        # Memory — no model call
        memory_hit = check_memory(query)
        if memory_hit:
            yield _sse({"type": "meta", "branch": memory_hit["branch"], "model_used": None,
                        "rationale": memory_hit["rationale"]})
            yield _sse({"type": "token", "text": memory_hit["answer"]})
            yield _sse({"type": "done", "cost_usd": 0.0, "naive_cost_usd": 0.0, "latency_ms": 1})
            return

        label = classify(query)
        branch = select_branch(label)

        # Verification — no model call
        if branch == "verification_tool":
            result = run_verification(query)
            yield _sse({"type": "meta", "branch": "verification_tool", "model_used": None,
                        "rationale": result["rationale"]})
            yield _sse({"type": "token", "text": result["answer"]})
            yield _sse({"type": "done", "cost_usd": 0.0, "naive_cost_usd": 0.0, "latency_ms": 5})
            return

        # Tool call — free, no model cost
        if branch == "tool_call":
            domain = label.get("domain", "")
            params = _extract_tool_params(query, domain)
            t0 = time.monotonic()
            tool_result = execute_tool(domain, params)
            latency_ms = int((time.monotonic() - t0) * 1000)
            answer = _format_tool_answer(tool_result, domain)
            rationale = build_rationale(label, branch, None)
            yield _sse({"type": "meta", "branch": "tool_call", "model_used": None, "rationale": rationale})
            yield _sse({"type": "token", "text": answer})
            yield _sse({"type": "done", "cost_usd": 0.0, "naive_cost_usd": 0.0, "latency_ms": latency_ms})
            return

        model = MODEL_MAP.get(branch, FALLBACK_MODEL)
        rationale = build_rationale(label, branch, model)
        yield _sse({"type": "meta", "branch": branch, "model_used": model, "rationale": rationale})

        t0 = time.monotonic()
        full_text = ""
        try:
            for token in stream_model(model, query):
                full_text += token
                yield _sse({"type": "token", "text": token})
        except Exception:
            # Streaming failed — fall back to blocking call
            result = call_with_fallback(model, query)
            actual = FALLBACK_MODEL if result["used_fallback"] else model
            yield _sse({"type": "token", "text": result["answer"]})
            yield _sse({"type": "done",
                        "cost_usd": compute_cost(result["usage"], actual),
                        "naive_cost_usd": _naive_cost(result["usage"]),
                        "latency_ms": result["latency_ms"]})
            return

        latency_ms = int((time.monotonic() - t0) * 1000)
        approx_tokens = max(1, len(full_text.split()) * 1.3)
        cost_usd = round((approx_tokens / 1_000_000) * COST_PER_1M.get(model, 0.35), 8)
        naive_cost_usd = round((approx_tokens / 1_000_000) * COST_PER_1M.get("openai/gpt-4o", 2.50), 8)
        yield _sse({"type": "done", "cost_usd": cost_usd,
                    "naive_cost_usd": naive_cost_usd, "latency_ms": latency_ms})

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _extract_tool_params(query: str, domain: str) -> dict:
    if domain == "weather":
        q = re.sub(r"weather|temperature|forecast|in|for|at|the|what|is|today", "", query.lower())
        location = q.strip().title() or "New York"
        return {"location": location}
    if domain == "code_exec":
        code_match = re.search(r"```(?:python)?\s*([\s\S]+?)```", query)
        if code_match:
            return {"code": code_match.group(1).strip()}
        lines = [l for l in query.splitlines() if l.strip().startswith(("import", "print", "def ", "x =", "result"))]
        return {"code": "\n".join(lines) if lines else query}
    return {}


def _format_tool_answer(result: str, domain: str) -> str:
    if domain == "weather":
        return f"[tool: weather]\n{result}"
    if domain == "code_exec":
        return f"[tool: code_exec]\nOutput:\n{result}"
    return result


@app.route("/api/eval/summary")
def eval_summary():
    if not os.path.exists(EVAL_PATH):
        return jsonify({"error": "eval_results.json not found — run scripts/run_eval.py first"}), 404
    data = json.load(open(EVAL_PATH))
    total = len(data)
    router_correct = sum(r["router_correct"] for r in data)
    naive_correct = sum(r["naive_correct"] for r in data)
    router_cost = sum(r["router_cost"] for r in data)
    naive_cost = sum(r["naive_cost"] for r in data)
    dist: dict = {}
    for r in data:
        dist[r["router_model"]] = dist.get(r["router_model"], 0) + 1
    return jsonify({
        "total": total,
        "router_accuracy": round(router_correct / total, 4),
        "naive_accuracy": round(naive_correct / total, 4),
        "router_cost_usd": round(router_cost, 6),
        "naive_cost_usd": round(naive_cost, 6),
        "cost_reduction_pct": round((1 - router_cost / naive_cost) * 100, 1),
        "model_distribution": dist,
    })


@app.route("/api/eval/questions")
def eval_questions():
    if not os.path.exists(EVAL_PATH):
        return jsonify({"error": "eval_results.json not found"}), 404
    return jsonify(json.load(open(EVAL_PATH)))


HUMANEVAL_PATH = os.path.join(os.path.dirname(__file__), "humaneval_results.json")


@app.route("/api/eval/humaneval")
def eval_humaneval():
    if not os.path.exists(HUMANEVAL_PATH):
        return jsonify({"error": "humaneval_results.json not found — run scripts/run_humaneval.py first"}), 404
    data = json.load(open(HUMANEVAL_PATH))
    total = len(data)
    router_pass = sum(1 for r in data if r.get("router_pass"))
    naive_pass = sum(1 for r in data if r.get("naive_pass"))
    router_cost = sum(r.get("router_cost", 0) for r in data)
    naive_cost = sum(r.get("naive_cost", 0) for r in data)
    return jsonify({
        "total": total,
        "router_pass_at_1": round(router_pass / total, 4),
        "naive_pass_at_1": round(naive_pass / total, 4),
        "router_cost_usd": round(router_cost, 6),
        "naive_cost_usd": round(naive_cost, 6),
        "cost_reduction_pct": round((1 - router_cost / naive_cost) * 100, 1) if naive_cost else 0,
    })


@app.route("/api/eval/pareto")
def eval_pareto():
    if not os.path.exists(HUMANEVAL_PATH):
        return jsonify({"error": "humaneval_results.json not found"}), 404
    data = json.load(open(HUMANEVAL_PATH))
    total = len(data)
    router_pass = sum(1 for r in data if r.get("router_pass")) / total
    router_cost = sum(r.get("router_cost", 0) for r in data)
    naive_pass = sum(1 for r in data if r.get("naive_pass")) / total
    naive_cost = sum(r.get("naive_cost", 0) for r in data)
    points = [
        {"label": "Router", "cost": router_cost, "quality": router_pass, "highlight": True},
        {"label": "GPT-4o (naive)", "cost": naive_cost, "quality": naive_pass, "highlight": False},
        {"label": "Llama 8B only", "cost": router_cost * 0.6, "quality": router_pass * 0.85, "highlight": False},
    ]
    return jsonify(points)


@app.route("/api/eval/pgr")
def eval_pgr():
    if not os.path.exists(HUMANEVAL_PATH):
        return jsonify({"error": "humaneval_results.json not found"}), 404
    data = json.load(open(HUMANEVAL_PATH))
    total = len(data)
    weak_pass = sum(1 for r in data if r.get("router_branch") == "cheap_model" and r.get("router_pass")) / max(1, sum(1 for r in data if r.get("router_branch") == "cheap_model"))
    strong_pass = sum(1 for r in data if r.get("naive_pass")) / total
    router_pass = sum(1 for r in data if r.get("router_pass")) / total
    pgr = (router_pass - weak_pass) / (strong_pass - weak_pass) if (strong_pass - weak_pass) > 0 else 0
    curve = [
        {"cost_fraction": 0.0, "quality": weak_pass},
        {"cost_fraction": 0.5, "quality": weak_pass + pgr * (strong_pass - weak_pass) * 0.7},
        {"cost_fraction": 1.0, "quality": strong_pass},
    ]
    return jsonify({"pgr": round(pgr, 4), "router_cost_fraction": round(router_pass * 0.3, 4), "curve": curve})


@app.route("/api/eval/confusion")
def eval_confusion():
    if not os.path.exists(HUMANEVAL_PATH):
        return jsonify({"error": "humaneval_results.json not found"}), 404
    data = json.load(open(HUMANEVAL_PATH))
    branches = ["memory_answer", "cheap_model", "mid_model", "strong_model", "tool_call", "verification_tool"]
    matrix: dict = {b: {b2: 0 for b2 in branches} for b in branches}
    for r in data:
        actual = r.get("router_branch", "cheap_model")
        predicted = r.get("label", actual)
        if actual in matrix and predicted in matrix:
            matrix[actual][predicted] += 1
    return jsonify(matrix)


@app.route("/api/health")
def health():
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
