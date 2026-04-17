import json
import os
import sys
import time
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from router import route_and_call, classify, select_branch, build_rationale, _naive_cost
from memory import check_memory
from verifier import run_verification
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


@app.route("/api/health")
def health():
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
