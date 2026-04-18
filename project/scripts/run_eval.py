"""
Run once before/during hackathon to generate backend/eval_results.json.

Usage:
    # Rules-based classifier (default)
    python scripts/run_eval.py

    # Trained classifier via serve.py
    CLASSIFIER_URL=http://localhost:8001 python scripts/run_eval.py

    # Via ngrok
    CLASSIFIER_URL=https://xxxx.ngrok-free.app python scripts/run_eval.py
"""
import csv
import json
import os
import re
import sys
import time

import urllib.request
import urllib.error

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from openrouter import call_model, compute_cost
from router import classify as rules_classify, select_branch, select_model
from config import MODEL_MAP

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mmlu_100.csv")
OUT_PATH  = os.path.join(os.path.dirname(__file__), "..", "backend", "eval_results.json")
NAIVE_MODEL = "openai/gpt-4o"

PROMPT_TEMPLATE = (
    "{question}\n"
    "A: {A}\nB: {B}\nC: {C}\nD: {D}\n\n"
    "Answer with only the letter A, B, C, or D. No explanation."
)

CLASSIFIER_URL = os.getenv("CLASSIFIER_URL", "").rstrip("/")


def classify_via_server(question: str) -> dict:
    payload = json.dumps({"query": question}).encode()
    req = urllib.request.Request(
        f"{CLASSIFIER_URL}/classify",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = json.loads(resp.read())
        return {"complexity": body["complexity"], "domain": body["domain"]}


def classify(question: str) -> dict:
    if CLASSIFIER_URL:
        try:
            return classify_via_server(question)
        except Exception as e:
            print(f"  [!] classifier server error ({e}), falling back to rules")
    return rules_classify(question)


def extract_answer(text: str) -> str:
    match = re.search(r'\b([A-D])\b', text.strip())
    return match.group(1) if match else "?"


def run():
    classifier_mode = f"trained ({CLASSIFIER_URL})" if CLASSIFIER_URL else "rules-based"
    print(f"Classifier: {classifier_mode}")

    # Verify server is reachable before starting
    if CLASSIFIER_URL:
        try:
            req = urllib.request.Request(f"{CLASSIFIER_URL}/health")
            with urllib.request.urlopen(req, timeout=5):
                pass
            print(f"Classifier server reachable at {CLASSIFIER_URL}")
        except Exception as e:
            print(f"WARNING: classifier server unreachable ({e}) — will fall back to rules per question")

    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        questions = list(csv.DictReader(f))

    print(f"Running eval on {len(questions)} questions...\n")

    results = []
    for i, q in enumerate(questions):
        prompt = PROMPT_TEMPLATE.format(**q)
        label  = classify(q["question"])
        branch = select_branch(label)
        model  = select_model(label)

        if model is None:
            model  = MODEL_MAP["cheap_model"]
            branch = "cheap_model"
            print(f"  [!] verify branch on q{i+1}, forcing cheap_model")

        router_result = call_model(model, prompt, max_tokens=10)
        router_ans    = extract_answer(router_result["answer"])
        router_cost   = compute_cost(router_result["usage"], model)

        naive_result = call_model(NAIVE_MODEL, prompt, max_tokens=10)
        naive_ans    = extract_answer(naive_result["answer"])
        naive_cost   = compute_cost(naive_result["usage"], NAIVE_MODEL)

        correct_ans = q.get("answer", "").strip().upper()
        results.append({
            "id":             q.get("id", str(i)),
            "question":       q["question"],
            "correct_answer": correct_ans,
            "router_branch":  branch,
            "router_model":   model,
            "router_answer":  router_ans,
            "router_correct": router_ans == correct_ans,
            "router_cost":    router_cost,
            "naive_answer":   naive_ans,
            "naive_correct":  naive_ans == correct_ans,
            "naive_cost":     naive_cost,
            "label":          label,
            "classifier":     classifier_mode,
        })

        status = "OK" if router_ans == correct_ans else "XX"
        print(f"  [{i+1:3}/{len(questions)}] {status} router={router_ans} naive={naive_ans} "
              f"correct={correct_ans}  [{label['complexity']}/{label['domain']}]  "
              f"{model.split('/')[-1]}")
        time.sleep(0.3)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    total           = len(results)
    router_acc      = sum(r["router_correct"] for r in results) / total
    naive_acc       = sum(r["naive_correct"]  for r in results) / total
    router_cost_sum = sum(r["router_cost"]    for r in results)
    naive_cost_sum  = sum(r["naive_cost"]     for r in results)
    savings         = (1 - router_cost_sum / naive_cost_sum) * 100

    from collections import Counter
    dist = Counter(r["router_model"].split("/")[-1] for r in results)

    print(f"\n{'='*40}")
    print(f"Classifier     : {classifier_mode}")
    print(f"Router accuracy: {router_acc:.1%}  (naive: {naive_acc:.1%}, gap: {naive_acc - router_acc:+.1%})")
    print(f"Router cost    : ${router_cost_sum:.4f}  (naive: ${naive_cost_sum:.4f})")
    print(f"Cost savings   : {savings:.1f}%")
    print(f"Model dist     : {dict(dist)}")
    print(f"Saved to       : {OUT_PATH}")


if __name__ == "__main__":
    run()
