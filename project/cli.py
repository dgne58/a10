"""
dispatch CLI — developer assistant powered by the cost-aware LLM router.

Install:
    pip install -e .        # from project/ directory

Usage:
    dispatch "write a binary search in Python"
    dispatch -f script.py "what does this do"
    echo "what is BM25?" | dispatch
    dispatch run "print(sum(range(10)))"   # shortcut: always execute code directly
"""

import argparse
import itertools
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
from glob import glob
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CLASSIFIER_URL  = os.environ.get("CLASSIFIER_URL", "")
CHEAP_URL       = os.environ.get("CHEAP_MODEL_URL", "")
OPENROUTER_KEY  = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"
WIKI_ROOT       = Path(os.environ.get("ROUTER_WIKI_PATH", Path(__file__).parent.parent / "Wiki"))
BM25_THRESHOLD  = 12.0
_EXCLUDED_WIKI  = ("design-doc", "design_doc", "demo", "clipping")

MODEL_MAP = {
    "cheap_model":  "meta-llama/llama-3.1-8b-instruct",
    "mid_model":    "meta-llama/llama-3.1-70b-instruct",
    "strong_model": "anthropic/claude-haiku-4.5",
}
COST_PER_1M = {
    "meta-llama/llama-3.1-8b-instruct":  0.05,
    "meta-llama/llama-3.1-70b-instruct": 0.35,
    "anthropic/claude-haiku-4.5":        1.00,
    "anthropic/claude-sonnet-4.6":       3.00,
}

_RESET = "\033[0m"
_BOLD  = "\033[1m"
_MUTED = "\033[90m"
_COLORS = {
    "memory_answer":     "\033[92m",
    "cheap_model":       "\033[94m",
    "mid_model":         "\033[93m",
    "strong_model":      "\033[91m",
    "tool_call":         "\033[96m",
}

# ── Tool definitions (OpenAI function calling format) ─────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": (
                "Fetch a URL and return the HTTP status, content-type, and a preview of the response body. "
                "ONLY call this when the user explicitly provides a URL (starting with http:// or https://) "
                "or uses words like 'fetch', 'GET', 'ping', 'curl', or 'check endpoint'. "
                "Do NOT call for general knowledge questions about technologies, organizations, or concepts."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Full URL to fetch, e.g. 'https://api.github.com'"}
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": (
                "Execute a Python code snippet and return stdout. "
                "Only call this when the user explicitly asks to run, execute, or evaluate code."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"],
            },
        },
    },
]

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
        if any(ex in p.lower() for ex in _EXCLUDED_WIKI):
            continue
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                in_code = False
                for i, ln in enumerate(f, 1):
                    s = ln.strip()
                    if s.startswith("```"):
                        in_code = not in_code
                        continue
                    if in_code:
                        continue
                    if s.startswith(("{", "[", "|", "#!", "//", "$ ", "- {")):
                        continue
                    if len(s) > 30:
                        lines.append(s)
                        lpaths.append(f"{Path(p).relative_to(WIKI_ROOT)}:{i}")
        except OSError:
            pass
    if not lines:
        return
    _bm25 = BM25Okapi([l.lower().split() for l in lines])
    _corpus_lines, _corpus_paths = lines, lpaths


def search_wiki(query: str) -> dict | None:
    global _bm25
    if _bm25 is None:
        _load_bm25()
    if _bm25 is None:
        return None
    scores = _bm25.get_scores(query.lower().split())
    idx = int(scores.argmax())
    score = float(scores[idx])
    if score < BM25_THRESHOLD:
        return None
    return {"answer": _corpus_lines[idx], "source": _corpus_paths[idx], "score": score}

# ── Classifier ────────────────────────────────────────────────────────────────

_HARD_KW   = {"why", "explain", "compare", "analyze", "critique", "evaluate", "derive", "prove"}
_MEDIUM_KW = {"how", "describe", "summarize", "difference between", "steps to", "what causes"}
_CODE_KW   = {"code", "function", "debug", "python", "javascript", "implement", "algorithm", "class", "typescript"}
_PROJECT_KW = {"what does the project", "what models does", "what architecture",
               "what files", "which wiki", "what is the routing", "what components"}


def _rules_classify(query: str) -> dict:
    q  = query.lower()
    wc = len(query.split())
    if any(k in q for k in _PROJECT_KW):
        return {"complexity": "simple", "domain": "factual"}
    domain = "code" if any(k in q for k in _CODE_KW) else "factual"
    if any(k in q for k in _HARD_KW) or wc > 40:
        c = "hard"
    elif any(k in q for k in _MEDIUM_KW) or wc > 20 or domain == "code":
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
    return {"simple": "cheap_model", "medium": "mid_model"}.get(c, "strong_model")

# ── Tool execution ────────────────────────────────────────────────────────────

def tool_fetch_url(url: str) -> str:
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read(2048).decode("utf-8", errors="replace")
        preview = body[:500].strip()
        return f"GET {url}\nStatus: {status}\nContent-Type: {content_type}\n\n{preview}"
    except Exception as e:
        return f"fetch_url failed for {url!r}: {e}"


def tool_code_exec(code: str) -> str:
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


def dispatch_tool(fn_name: str, fn_args: dict) -> str:
    if fn_name == "fetch_url":
        return tool_fetch_url(fn_args.get("url", ""))
    if fn_name == "execute_python":
        return tool_code_exec(fn_args.get("code", ""))
    return f"Unknown tool: {fn_name!r}"

# ── Model calls with tool support ─────────────────────────────────────────────

def _post(url: str, payload: dict, headers: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def _call_with_tools(url: str, payload: dict, headers: dict) -> tuple[str, float, str | None]:
    """
    Make one API call with tools. Returns (answer, cost, tool_name_used_or_None).
    If the model calls a tool, executes it and makes a follow-up call for the summary.
    """
    data = _post(url, payload, headers)
    choice = data["choices"][0]
    message = choice["message"]
    model = payload.get("model", "")

    if choice.get("finish_reason") == "tool_calls" and message.get("tool_calls"):
        tc = message["tool_calls"][0]
        fn_name = tc["function"]["name"]
        try:
            fn_args = json.loads(tc["function"]["arguments"])
        except (json.JSONDecodeError, ValueError):
            fn_args = {}

        tool_result = dispatch_tool(fn_name, fn_args)

        # Follow-up: model summarizes the tool result
        followup_messages = payload["messages"] + [
            {"role": "assistant", "content": None, "tool_calls": [tc]},
            {"role": "tool", "tool_call_id": tc["id"], "content": tool_result},
        ]
        followup_payload = {k: v for k, v in payload.items() if k != "tools"}
        followup_payload["messages"] = followup_messages
        followup_payload.pop("tool_choice", None)

        data2 = _post(url, followup_payload, headers)
        answer = data2["choices"][0]["message"].get("content", tool_result)
        tokens = data2.get("usage", {}).get("total_tokens", len(answer.split()))
        cost = round((tokens / 1_000_000) * COST_PER_1M.get(model, 0.35), 8)
        return answer, cost, fn_name

    answer = message.get("content", "")
    tokens = data.get("usage", {}).get("total_tokens", len(answer.split()))
    cost = round((tokens / 1_000_000) * COST_PER_1M.get(model, 0.35), 8)
    return answer, cost, None


def _openrouter_headers() -> dict:
    return {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://hackathon-router.dev",
    }


def call_model(branch: str, query: str) -> tuple[str, float, str, str | None]:
    """Returns (answer, cost, model_name, tool_used_or_None)."""
    if branch == "cheap_model" and CHEAP_URL:
        model = "llama-8b-code"
        url = f"{CHEAP_URL}/chat/completions"
        headers = {"Content-Type": "application/json"}
    else:
        model = MODEL_MAP.get(branch, MODEL_MAP["strong_model"])
        url = OPENROUTER_BASE
        headers = _openrouter_headers()

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": query}],
        "max_tokens": 1024,
        "stream": False,
        "tools": TOOL_DEFINITIONS,
        "tool_choice": "auto",
    }

    answer, cost, tool_used = _call_with_tools(url, payload, headers)
    display_name = "llama-8b-code (local)" if (branch == "cheap_model" and CHEAP_URL) else model
    return answer, cost, display_name, tool_used

# ── Display ───────────────────────────────────────────────────────────────────

def badge(branch: str, source: str, cost_usd: float, ms: int,
          tool_used: str | None = None) -> str:
    color    = _COLORS.get(branch, "")
    cost_str = f"${cost_usd:.6f}" if cost_usd > 0 else "free"
    tool_str = f"  {_MUTED}[tool: {tool_used}]{_RESET}" if tool_used else ""
    return f"{color}{_BOLD}[{branch}]{_RESET} {source}{tool_str}  {_MUTED}{cost_str}  {ms}ms{_RESET}"


# ── Spinner ───────────────────────────────────────────────────────────────────

_SPIN_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


class _Spinner:
    def __init__(self, label: str = "Thinking"):
        self.label = label
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._run, daemon=True)

    def start(self) -> "_Spinner":
        self._t.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        self._t.join(timeout=0.5)
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()

    def _run(self) -> None:
        for ch in itertools.cycle(_SPIN_FRAMES):
            if self._stop.is_set():
                break
            sys.stdout.write(f"\r{_MUTED}{ch}{_RESET} {self.label}…")
            sys.stdout.flush()
            time.sleep(0.08)


# ── Streaming ─────────────────────────────────────────────────────────────────

_TEXT_TOOL_NAMES = {"fetch_url", "execute_python", "lint_python", "regex_test", "calculate"}


def _parse_text_tool_call(text: str) -> dict | None:
    s = text.strip()
    if not (s.startswith("{") and s.endswith("}")):
        return None
    try:
        obj = json.loads(s)
    except json.JSONDecodeError:
        return None
    name = obj.get("name") or obj.get("function") or obj.get("tool")
    if name not in _TEXT_TOOL_NAMES:
        return None
    raw_args = obj.get("parameters") or obj.get("arguments") or obj.get("input") or {}
    args_str = json.dumps(raw_args) if isinstance(raw_args, dict) else str(raw_args)
    return {"id": "call_0", "type": "function", "function": {"name": name, "arguments": args_str}}


def _stream_tokens(url: str, payload: dict, headers: dict, buffer: bool = False):
    """Yield str tokens live. If tool call detected, yield {"tool_call": ...} and return.
    buffer=True delays token output until end (needed for local models that output
    tool calls as plain-text JSON rather than structured finish_reason)."""
    data = json.dumps({**payload, "stream": True}).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    buffered: list[str] = []
    accumulated_tc: dict[int, dict] = {}

    with urllib.request.urlopen(req, timeout=30) as resp:
        for raw in resp:
            line = raw.decode("utf-8", errors="replace").rstrip("\n")
            if not line.startswith("data: "):
                continue
            raw_data = line[6:]
            if raw_data.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(raw_data)
                choice = chunk["choices"][0]
                delta = choice.get("delta", {})
                finish = choice.get("finish_reason")
                content = delta.get("content") or ""
                if content:
                    if buffer:
                        buffered.append(content)
                    else:
                        yield content
                for tc_delta in delta.get("tool_calls", []):
                    idx = tc_delta.get("index", 0)
                    if idx not in accumulated_tc:
                        accumulated_tc[idx] = {
                            "id": tc_delta.get("id", "call_0"),
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        }
                    fn = tc_delta.get("function", {})
                    accumulated_tc[idx]["function"]["name"] += fn.get("name", "")
                    accumulated_tc[idx]["function"]["arguments"] += fn.get("arguments", "")
                if finish == "tool_calls" and accumulated_tc:
                    yield {"tool_call": accumulated_tc[0]}
                    return
            except (json.JSONDecodeError, KeyError, IndexError):
                continue

    if buffer:
        full = "".join(buffered)
        text_tc = _parse_text_tool_call(full)
        if text_tc:
            yield {"tool_call": text_tc}
            return
        for tok in buffered:
            yield tok


# ── Main routing ──────────────────────────────────────────────────────────────

def route(query: str) -> None:
    backend = os.environ.get("ROUTER_BACKEND", "").rstrip("/")
    if not backend:
        print("Error: ROUTER_BACKEND not set. Example:\n  export ROUTER_BACKEND=https://53ce-69-5-185-3.ngrok-free.app", file=sys.stderr)
        sys.exit(1)

    sp = _Spinner("Routing").start()
    t0 = time.monotonic()
    try:
        payload = json.dumps({"query": query}).encode()
        req = urllib.request.Request(
            f"{backend}/api/route",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except Exception as exc:
        sp.stop()
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    sp.stop()
    ms = int((time.monotonic() - t0) * 1000)

    branch   = data.get("branch", "unknown")
    answer   = data.get("answer", "")
    model    = data.get("model_used") or MODEL_MAP.get(branch, "")
    cost     = data.get("cost_usd", 0.0)
    print(badge(branch, model, cost, ms))
    print(answer)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="dispatch",
        description="Cost-aware LLM router — developer assistant",
    )
    parser.add_argument("query", nargs="?", default=None)
    parser.add_argument("-f", "--file", default=None, help="Prepend file contents to query")
    args = parser.parse_args()

    # `router run "print(1)"` → always execute code directly, no model
    if args.query and args.query.lower().startswith("run "):
        code = args.query[4:].strip()
        t0 = time.monotonic()
        result = tool_code_exec(code)
        ms = int((time.monotonic() - t0) * 1000)
        print(badge("tool_call", "subprocess", 0.0, ms))
        print(result)
        return

    if args.file:
        file_content = Path(args.file).read_text(encoding="utf-8")
        query = f"File: {args.file}\n```\n{file_content[:3000]}\n```\n\n{args.query or ''}".strip()
    elif args.query:
        query = args.query
    elif not sys.stdin.isatty():
        stdin = sys.stdin.read().strip()
        query = f"{stdin}\n\n{args.query}".strip() if args.query else stdin
    else:
        parser.print_help()
        sys.exit(0)

    route(query)


if __name__ == "__main__":
    main()
