"""
run_humaneval.py

Downloads the first 100 HumanEval problems, runs each through the router,
and records pass@1 vs the naive GPT-4o baseline.

Run:
    python run_humaneval.py           # uses router (classifier + branches)
    python run_humaneval.py --limit 20  # quick smoke-test

Output: backend/humaneval_results.json
"""

import json
import os
import sys
import re
import tempfile
import subprocess
import argparse
from pathlib import Path

# make backend importable
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from openrouter import call_model
from router import classify, select_branch, build_rationale, _naive_cost
from memory import check_memory
from config import MODEL_MAP, FALLBACK_MODEL, COST_PER_1M

HUMANEVAL_PATH = Path(__file__).parent.parent / "backend" / "humaneval_results.json"
STRONG_MODEL = "openai/gpt-4o-mini"
CODE_SYSTEM = "Complete the Python function body. Output ONLY the code — no explanation, no markdown fences, no extra text."


def download_humaneval(limit: int) -> list[dict]:
    try:
        from datasets import load_dataset
        ds = load_dataset("openai/openai_humaneval", split="test", trust_remote_code=True)
        return list(ds)[:limit]
    except Exception as e:
        print(f"[humaneval] datasets download failed: {e}")
        print("[humaneval] Install with: pip install datasets")
        sys.exit(1)


def run_tests(completion: str, test: str, entry_point: str) -> bool:
    code = completion + "\n\n" + test + f"\ncheck({entry_point})"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(
            [sys.executable, tmp],
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def extract_code(raw: str) -> str:
    fence = re.search(r"```(?:python)?\s*([\s\S]+?)```", raw)
    if fence:
        return fence.group(1).strip()
    return raw.strip()


def call_router(prompt: str) -> tuple[str, str, float]:
    """Returns (completion, branch, cost_usd)."""
    mem = check_memory(prompt)
    if mem:
        return mem["answer"], "memory_answer", 0.0

    label = classify(prompt)
    branch = select_branch(label)

    if branch in {"verification_tool", "memory_answer"}:
        branch = "cheap_model"

    model = MODEL_MAP.get(branch, FALLBACK_MODEL)
    result = call_model(model, prompt, max_tokens=512, system=CODE_SYSTEM)
    cost = result["cost_usd"]
    return extract_code(result["answer"]), branch, cost


def call_naive(prompt: str) -> tuple[str, float]:
    result = call_model(STRONG_MODEL, prompt, max_tokens=512, system=CODE_SYSTEM)
    return extract_code(result["answer"]), result["cost_usd"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--skip-naive", action="store_true",
                        help="Skip GPT-4o-mini baseline (faster, no cost)")
    args = parser.parse_args()

    problems = download_humaneval(args.limit)
    print(f"[humaneval] Running {len(problems)} problems...")

    results = []
    for i, prob in enumerate(problems):
        task_id = prob["task_id"]
        prompt = prob["prompt"]
        test = prob["test"]
        entry = prob["entry_point"]

        router_comp, branch, router_cost = call_router(prompt)
        router_pass = run_tests(router_comp, test, entry)

        if not args.skip_naive:
            naive_comp, naive_cost = call_naive(prompt)
            naive_pass = run_tests(naive_comp, test, entry)
        else:
            naive_comp, naive_cost, naive_pass = "", 0.0, False

        rec = {
            "task_id": task_id,
            "router_branch": branch,
            "router_model": MODEL_MAP.get(branch, FALLBACK_MODEL),
            "router_pass": router_pass,
            "router_cost": router_cost,
            "naive_pass": naive_pass,
            "naive_cost": naive_cost,
            "label": branch,
        }
        results.append(rec)

        status = "PASS" if router_pass else "FAIL"
        print(f"[{i+1:3}/{len(problems)}] {task_id} | {branch:15} | router={status}")

    json.dump(results, open(HUMANEVAL_PATH, "w"), indent=2)
    total = len(results)
    r_pass = sum(1 for r in results if r["router_pass"])
    n_pass = sum(1 for r in results if r["naive_pass"])
    print(f"\nRouter  pass@1: {r_pass}/{total} = {r_pass/total:.1%}")
    print(f"Naive   pass@1: {n_pass}/{total} = {n_pass/total:.1%}")
    print(f"Router  cost:   ${sum(r['router_cost'] for r in results):.4f}")
    print(f"Naive   cost:   ${sum(r['naive_cost'] for r in results):.4f}")
    print(f"\nSaved → {HUMANEVAL_PATH}")


if __name__ == "__main__":
    main()
