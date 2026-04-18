"""
router CLI — developer assistant powered by the cost-aware LLM router.

Install:
    pip install -e .        # from project/ directory

Usage:
    router "write a binary search in Python"
    router -f script.py     # route a file's content
    echo "what is BM25?" | router
    router run "print(sum(range(10)))"   # shortcut: always tool_call/code_exec
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from glob import glob
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CLASSIFIER_URL   = os.environ.get("CLASSIFIER_URL", "")
CHEAP_URL        = os.environ.get("CHEAP_MODEL_URL", "")   # vLLM OpenAI-compat
OPENROUTER_KEY   = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE  = "https://openrouter.ai/api/v1/chat/completions"
WIKI_ROOT        = Path(os.environ.get("ROUTER_WIKI_PATH", Path(__file__).parent.parent / "Wiki"))
BM25_THRESHOLD   = 3.0

MODEL_MAP = {
    "cheap_model":  "meta-llama/llama-3.1-8b-instruct",
    "mid_model":    "meta-llama/llama-3.1-70b-instruct",
    "strong_model": "openai/gpt-4o-mini",
}
COST_PER_1M = {
    "meta-llama/llama-3.1-8b-instruct":  0.05,
    "meta-llama/llama-3.1-70b-instruct": 0.35,
    "openai/gpt-4o-mini":                0.15,
    "openai/gpt-4o":                     2.50,
}

# ANSI colours
_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_COLORS = {
    "memory_answer":     "\033[92m",
    "cheap_model":       "\033[94m",
    "mid_model":         "\033[93m",
    "strong_model":      "\033[91m",
    "tool_call":         "\033[96m",
    "verification_tool": "\033[95m",
}

# ── BM25 wiki search ──────────────────────────────────────────────────────────

_bm25 = None
_corpus_lines: list[str] = []
_corpus_paths: list[str] = []


def _load_bm25() -> None:
    global _bm25, _corpus_lines, _corpus_paths
    try:
        from rank_bm25 import BM25Okapi
    except ImportError:
        return
    paths = glob(str(WIKI_ROOT / "**" / "*.md"), recursive=True)
    lines, lpaths = [], []
    for p in paths:
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                for i, ln in enumerate(f, 1):
                    s = ln.strip()
                    if len(s) > 30:
                        lines.append(s)
                        lpaths.append(f"{Path(p).relative_to(WIKI_ROOT)}:{i}")
        except OSError:
            pass
    if not lines:
        return
    _bm25 = BM25Okapi([l.lower().split() for l in lines])
    _corpus_lines, _corpus_paths = lines, lpaths


def search_wiki(query: str, threshold: float = BM25_THRESHOLD) -> dict | None:
    global _bm25
    if _bm25 is None:
        _load_bm25()
    if _bm25 is None:
        return None
    scores = _bm25.get_scores(query.lower().split())
    idx = int(scores.argmax())
    score = float(scores[idx])
    if score < threshold:
        return None
    return {"answer": _corpus_lines[idx], "source": _corpus_paths[idx], "score": score}

# ── Classifier ────────────────────────────────────────────────────────────────

_HARD_KW   = {"why", "explain", "compare", "analyze", "critique", "evaluate", "derive", "prove"}
_MEDIUM_KW = {"how", "describe", "summarize", "difference between", "steps to", "what causes"}
_CODE_KW   = {"code", "function", "debug", "python", "javascript", "implement", "algorithm", "class", "typescript"}
_WEATHER_KW = {"weather", "temperature", "forecast", "raining", "sunny", "celsius", "fahrenheit"}
_EXEC_KW    = {"run this", "execute this", "run the code", "what does this print", "output of this"}


def _rules_classify(query: str) -> dict:
    q = query.lower()
    wc = len(query.split())
    if any(k in q for k in _EXEC_KW):
        return {"complexity": "tool", "domain": "code_exec"}
    if any(k in q for k in _WEATHER_KW):
        return {"complexity": "tool", "domain": "weather"}
    domain = "code" if any(k in q for k in _CODE_KW) else "factual"
    if any(k in q for k in _HARD_KW) or wc > 40 or domain == "code":
        c = "hard"
    elif any(k in q for k in _MEDIUM_KW) or wc > 20:
        c = "medium"
    else:
        c = "simple"
    return {"complexity": c, "domain": domain}


def classify(query: str) -> dict:
    if not CLASSIFIER_URL:
        return _rules_classify(query)
    try:
        payload = json.dumps({"query": query}).encode()
        req = urllib.request.Request(
            f"{CLASSIFIER_URL}/classify",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read())
    except Exception:
        return _rules_classify(query)


def select_branch(label: dict) -> str:
    c = label.get("complexity", "hard")
    if c == "tool":
        return "tool_call"
    if c == "verify":
        return "verification_tool"
    return {"simple": "cheap_model", "medium": "mid_model"}.get(c, "strong_model")

# ── Model callers ─────────────────────────────────────────────────────────────

def _openrouter_post(model: str, messages: list[dict]) -> tuple[str, float]:
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": 512,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        OPENROUTER_BASE,
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hackathon-router.dev",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read())
    answer = data["choices"][0]["message"]["content"]
    tokens = data.get("usage", {}).get("total_tokens", len(answer.split()))
    cost = round((tokens / 1_000_000) * COST_PER_1M.get(model, 0.35), 8)
    return answer, cost


def _vllm_post(messages: list[dict]) -> tuple[str, float]:
    payload = json.dumps({
        "model": "llama-8b-code",
        "messages": messages,
        "max_tokens": 512,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        f"{CHEAP_URL}/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read())
    answer = data["choices"][0]["message"]["content"]
    tokens = data.get("usage", {}).get("total_tokens", len(answer.split()))
    cost = round((tokens / 1_000_000) * COST_PER_1M.get("meta-llama/llama-3.1-8b-instruct", 0.05), 8)
    return answer, cost


def call_cheap(query: str) -> tuple[str, float, str]:
    sys_msg = {"role": "system", "content": "You are an expert software engineer. Be concise."}
    msgs = [sys_msg, {"role": "user", "content": query}]
    if CHEAP_URL:
        a, c = _vllm_post(msgs)
        return a, c, "llama-8b-code (local)"
    a, c = _openrouter_post(MODEL_MAP["cheap_model"], msgs)
    return a, c, MODEL_MAP["cheap_model"]


def call_mid(query: str) -> tuple[str, float, str]:
    model = MODEL_MAP["mid_model"]
    a, c = _openrouter_post(model, [{"role": "user", "content": query}])
    return a, c, model


def call_strong(query: str) -> tuple[str, float, str]:
    model = MODEL_MAP["strong_model"]
    a, c = _openrouter_post(model, [{"role": "user", "content": query}])
    return a, c, model

# ── Tools ─────────────────────────────────────────────────────────────────────

def tool_weather(location: str) -> str:
    url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        cur = data["current_condition"][0]
        return f"{location}: {cur['weatherDesc'][0]['value']}, {cur['temp_C']}°C (feels {cur['FeelsLikeC']}°C)"
    except Exception as e:
        return f"Weather unavailable for {location!r}: {e}"


def tool_code_exec(code: str) -> str:
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp = f.name
    try:
        r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=5)
        out = r.stdout.strip()
        err = r.stderr.strip()
        return out if r.returncode == 0 else f"Error:\n{err}"
    except subprocess.TimeoutExpired:
        return "Error: timed out (5s)"
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def _extract_weather_location(query: str) -> str:
    q = re.sub(r"weather|temperature|forecast|in|for|at|the|what|is|today|right|now|degrees?", "", query.lower())
    return q.strip().title() or "New York"


def _extract_code(query: str) -> str:
    m = re.search(r"```(?:python)?\s*([\s\S]+?)```", query)
    if m:
        return m.group(1).strip()
    lines = [l for l in query.splitlines() if l.strip().startswith(("import", "print", "def ", "x =", "result", "for ", "while "))]
    return "\n".join(lines) if lines else query

# ── Display ───────────────────────────────────────────────────────────────────

def badge(branch: str, source: str, cost_usd: float, ms: int) -> str:
    color = _COLORS.get(branch, "")
    cost_str = f"${cost_usd:.6f}" if cost_usd > 0 else "free"
    return f"{color}{_BOLD}[{branch}]{_RESET} via {source}  {cost_str}  {ms}ms"

# ── Main routing ──────────────────────────────────────────────────────────────

def route(query: str) -> None:
    t0 = time.monotonic()

    # Seed pair check (instant)
    SEED_TRIGGERS = {
        "what is routellm": "RouteLLM is a UC Berkeley + Anyscale router paper (arXiv:2406.18665). Up to 3.66x cost reduction on MT-Bench.",
        "what does this project do": "Branch router: routes queries to memory, cheap/mid/strong model, tool, or verification — cheapest sufficient path.",
    }
    for trigger, answer in SEED_TRIGGERS.items():
        if trigger in query.lower():
            ms = int((time.monotonic() - t0) * 1000)
            print(badge("memory_answer", "seed pairs", 0.0, ms))
            print(answer)
            return

    # Wiki BM25 search
    hit = search_wiki(query)
    if hit:
        ms = int((time.monotonic() - t0) * 1000)
        print(badge("memory_answer", hit["source"], 0.0, ms))
        print(hit["answer"])
        return

    label = classify(query)
    branch = select_branch(label)

    if branch == "tool_call":
        domain = label.get("domain", "")
        if domain == "weather":
            loc = _extract_weather_location(query)
            result = tool_weather(loc)
            source = f"wttr.in/{loc}"
        else:
            code = _extract_code(query)
            result = tool_code_exec(code)
            source = "subprocess"
        ms = int((time.monotonic() - t0) * 1000)
        print(badge("tool_call", source, 0.0, ms))
        print(result)
        return

    if branch == "verification_tool":
        # read project-map.md if available
        map_path = WIKI_ROOT / "00-preload" / "project-map.md"
        if map_path.exists():
            answer = map_path.read_text(encoding="utf-8")[:800]
        else:
            answer = "project-map.md not found — run from the repo root."
        ms = int((time.monotonic() - t0) * 1000)
        print(badge("verification_tool", str(map_path), 0.0, ms))
        print(answer)
        return

    if branch == "cheap_model":
        answer, cost, model_name = call_cheap(query)
    elif branch == "mid_model":
        answer, cost, model_name = call_mid(query)
    else:
        answer, cost, model_name = call_strong(query)

    ms = int((time.monotonic() - t0) * 1000)
    print(badge(branch, model_name, cost, ms))
    print(answer)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="router",
        description="Cost-aware LLM router — developer assistant",
    )
    parser.add_argument("query", nargs="?", default=None,
                        help="Query string. Use 'run <code>' to force code execution.")
    parser.add_argument("-f", "--file", default=None,
                        help="Route the contents of a file")
    args = parser.parse_args()

    # Special: `router run "print(1)"` → always code_exec
    if args.query and args.query.lower().startswith("run "):
        code = args.query[4:].strip()
        t0 = time.monotonic()
        result = tool_code_exec(code)
        ms = int((time.monotonic() - t0) * 1000)
        print(badge("tool_call", "subprocess", 0.0, ms))
        print(result)
        return

    if args.file:
        query = Path(args.file).read_text(encoding="utf-8")
    elif args.query:
        query = args.query
    elif not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    else:
        parser.print_help()
        sys.exit(0)

    route(query)


if __name__ == "__main__":
    main()
