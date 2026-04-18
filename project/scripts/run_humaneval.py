"""
run_humaneval.py

Downloads the first 100 HumanEval problems, runs each through the router,
and records pass@1 vs the naive Claude Sonnet baseline.

Run:
    python run_humaneval.py             # uses router (classifier + branches)
    python run_humaneval.py --limit 20  # quick smoke-test

Output: backend/humaneval_results.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

# Make backend importable.
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from config import FALLBACK_MODEL, MODEL_MAP  # noqa: E402
from memory import check_memory  # noqa: E402
from openrouter import call_model  # noqa: E402
from router import classify, select_branch  # noqa: E402

HUMANEVAL_PATH = Path(__file__).parent.parent / "backend" / "humaneval_results.json"
STRONG_MODEL = "anthropic/claude-sonnet-4.6"
CODE_SYSTEM = (
    "Complete the Python function. Return ONLY the full function definition, "
    "with valid Python indentation. No explanation, no markdown fences, no extra text."
)


def download_humaneval(limit: int) -> list[dict]:
    try:
        from datasets import load_dataset

        ds = load_dataset("openai/openai_humaneval", split="test", trust_remote_code=True)
        return list(ds)[:limit]
    except Exception as exc:
        print(f"[humaneval] datasets download failed: {exc}")
        print("[humaneval] Install with: pip install datasets")
        sys.exit(1)


def extract_code(raw: str) -> str:
    """Extract code without destroying the indentation of body-only completions."""
    fence = re.search(r"```(?:python)?\s*([\s\S]+?)```", raw, flags=re.IGNORECASE)
    if fence:
        return fence.group(1).strip("\r\n")
    return raw.strip("\r\n")


def _indent_width(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def normalize_body_completion(completion: str) -> str:
    """Normalize body-only completions to a single function-body indent level."""
    lines = completion.strip("\r\n").splitlines()
    if not lines:
        return ""

    first_nonempty = next((line for line in lines if line.strip()), "")
    first_indent = _indent_width(first_nonempty)
    normalized: list[str] = []
    for line in lines:
        if not line.strip():
            normalized.append("")
            continue
        normalized.append(line[first_indent:] if _indent_width(line) >= first_indent else line.lstrip())

    rest_indents = [_indent_width(line) for line in normalized[1:] if line.strip()]
    extra_rest_indent = min(rest_indents) if rest_indents else 0
    if extra_rest_indent >= 4:
        adjusted = [normalized[0]]
        for line in normalized[1:]:
            if line.strip():
                adjusted.append(
                    line[extra_rest_indent:] if _indent_width(line) >= extra_rest_indent else line.lstrip()
                )
            else:
                adjusted.append("")
        normalized = adjusted

    return "\n".join(normalized)


def assemble_candidate_code(prompt: str, completion: str, test: str, entry_point: str) -> str:
    """Build the executable HumanEval program for a model completion."""
    if re.search(rf"(^|\n)\s*def\s+{re.escape(entry_point)}\s*\(", completion):
        full_fn = completion
    else:
        # Body-only completions frequently come back with zero indentation on
        # the first line and relative indentation on later lines. Re-indent the
        # entire body one level so it sits inside the provided function stub.
        body = normalize_body_completion(completion)
        body = textwrap.indent(body, "    ", lambda line: bool(line.strip()))
        full_fn = prompt + body
    return "from typing import *\n\n" + full_fn + "\n\n" + test + f"\ncheck({entry_point})"


def run_tests(
    prompt: str,
    completion: str,
    test: str,
    entry_point: str,
    debug: bool = False,
    debug_label: str | None = None,
) -> bool:
    code = assemble_candidate_code(prompt, completion, test, entry_point)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as handle:
        handle.write(code)
        tmp = handle.name

    try:
        result = subprocess.run(
            [sys.executable, tmp],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if debug and result.returncode != 0:
            label = f" ({debug_label})" if debug_label else ""
            print(f"\n[humaneval] First failure debug{label}")
            print("[humaneval] --- assembled code ---")
            print(code)
            print("[humaneval] --- stdout ---")
            print(result.stdout or "(empty)")
            print("[humaneval] --- stderr ---")
            print(result.stderr or "(empty)")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        if debug:
            label = f" ({debug_label})" if debug_label else ""
            print(f"\n[humaneval] First failure debug{label}")
            print("[humaneval] --- assembled code ---")
            print(code)
            print("[humaneval] --- stdout ---")
            print("(empty)")
            print("[humaneval] --- stderr ---")
            print("Error: execution timed out (10s limit)")
        return False
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def call_router(prompt: str) -> tuple[str, str, float]:
    """Returns (completion, branch, cost_usd)."""
    mem = check_memory(prompt)
    if mem:
        return mem["answer"], "memory_answer", 0.0

    label = classify(prompt)
    branch = select_branch(label)

    model = MODEL_MAP.get(branch, FALLBACK_MODEL)
    result = call_model(model, prompt, max_tokens=1024, system=CODE_SYSTEM)
    return extract_code(result["answer"]), branch, result["cost_usd"]


def call_naive(prompt: str) -> tuple[str, float]:
    result = call_model(STRONG_MODEL, prompt, max_tokens=1024, system=CODE_SYSTEM)
    return extract_code(result["answer"]), result["cost_usd"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument(
        "--skip-naive",
        action="store_true",
        help="Skip Claude Sonnet baseline (faster, lower cost).",
    )
    parser.add_argument(
        "--debug-first-failure",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Print the exact assembled code and subprocess output for the first failing case.",
    )
    args = parser.parse_args()

    problems = download_humaneval(args.limit)
    print(f"[humaneval] Running {len(problems)} problems...")

    results: list[dict] = []
    logged_failure = False

    for index, problem in enumerate(problems):
        task_id = problem["task_id"]
        prompt = problem["prompt"]
        test = problem["test"]
        entry = problem["entry_point"]

        router_comp, branch, router_cost = call_router(prompt)
        router_pass = run_tests(
            prompt,
            router_comp,
            test,
            entry,
            debug=args.debug_first_failure and not logged_failure,
            debug_label=f"{task_id} router/{branch}",
        )
        if not router_pass and args.debug_first_failure and not logged_failure:
            logged_failure = True

        if not args.skip_naive:
            naive_comp, naive_cost = call_naive(prompt)
            naive_pass = run_tests(
                prompt,
                naive_comp,
                test,
                entry,
                debug=args.debug_first_failure and not logged_failure,
                debug_label=f"{task_id} naive/{STRONG_MODEL}",
            )
            if not naive_pass and args.debug_first_failure and not logged_failure:
                logged_failure = True
        else:
            naive_comp, naive_cost, naive_pass = "", 0.0, False

        record = {
            "task_id": task_id,
            "router_branch": branch,
            "router_model": MODEL_MAP.get(branch, FALLBACK_MODEL),
            "router_pass": router_pass,
            "router_cost": router_cost,
            "naive_pass": naive_pass,
            "naive_cost": naive_cost,
            "label": branch,
        }
        results.append(record)

        status = "PASS" if router_pass else "FAIL"
        print(f"[{index + 1:3}/{len(problems)}] {task_id} | {branch:15} | router={status}")

    with open(HUMANEVAL_PATH, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)

    total = len(results)
    router_passes = sum(1 for result in results if result["router_pass"])
    naive_passes = sum(1 for result in results if result["naive_pass"])
    print(f"\nRouter  pass@1: {router_passes}/{total} = {router_passes / total:.1%}")
    print(f"Naive   pass@1: {naive_passes}/{total} = {naive_passes / total:.1%}")
    print(f"Router  cost:   ${sum(result['router_cost'] for result in results):.4f}")
    print(f"Naive   cost:   ${sum(result['naive_cost'] for result in results):.4f}")
    print(f"\nSaved -> {HUMANEVAL_PATH}")


if __name__ == "__main__":
    main()
