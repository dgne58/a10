# Design Doc V2 — Next Stage Upgrades

**Date:** 2026-04-18
**Status:** Pre-build — implement tomorrow
**Author:** Shiva

---

## 0. What Changed (Judge Feedback → Action Map)

| Judge feedback | What we build |
|---|---|
| Task-specific dataset — MMLU too generalist | **HumanEval** (164 Python problems, pass@1) — developer-native benchmark, not saturated at 8B scale |
| Karpathy RAG / memory system | **Wiki-backed memory** — BM25 over `Wiki/**/*.md`, cites source page + line |
| More model metrics and graphs | **4 new charts**: Pareto frontier, PGR curve, confusion matrix, training curves |
| Hook model up with tool calls | **5th branch: `tool_call`** — weather + sandboxed code execution |
| (New) Vertical / angle | **Developer assistant** — fine-tuned Llama 8B for coding, served locally on H200 |
| (New) CLI | **`router` CLI** — terminal tool, reads local wiki, hits H200 via ngrok |

Track merge note: MCP clients are described in their own docs as "a smart router." Frame your router as the decision layer above MCP — not competing, composing.

---

## 1. System Architecture

```
Developer's machine
├── router CLI (project/cli.py)
│   ├── BM25 over ./Wiki/**/*.md          free, local
│   ├── POST $CLASSIFIER_URL/classify     H200 via ngrok-A
│   ├── POST $CHEAP_MODEL_URL/v1/...      H200 vLLM via ngrok-B  (fine-tuned Llama 8B)
│   ├── POST openrouter.ai/v1/...         mid / strong models
│   └── tools: weather (wttr.in), code_exec (subprocess)
│
└── Web UI + Flask (existing, localhost:5000)
    └── same routing logic, same endpoints

H200 (remote)
├── :8001  serve.py (FastAPI)     Qwen2-1.5B classifier  ← already running
├── :8002  vllm serve             Llama 8B code (new)
└── ngrok exposes both ports
```

### Env vars for CLI

```bash
export CLASSIFIER_URL=https://xxxx.ngrok-free.app      # existing
export CHEAP_MODEL_URL=https://yyyy.ngrok-free.app/v1  # new (vLLM OpenAI-compat)
export OPENROUTER_API_KEY=sk-or-...
export ROUTER_WIKI_PATH=./Wiki                          # optional, default ./Wiki
```

---

## 2. Benchmark: HumanEval

### Why HumanEval

- 164 Python programming problems, pass@1 scoring
- Directly relevant to the "developer assistant" vertical
- Base Llama 8B scores ~33% — our fine-tuned model should hit 55-65%
- GPT-4o scores ~90% — shows clear routing rationale
- Runs in ~1 hour, no database or agent loop required
- Eval is objective: execute the tests, pass or fail

### New files

```
project/
  data/
    humaneval_100.json      ← downloaded (first 100 problems)
  scripts/
    run_humaneval.py        ← eval runner, writes humaneval_results.json
  backend/
    humaneval_results.json  ← generated, committed before demo
```

### `scripts/run_humaneval.py` (new file)

```python
"""
Evaluate router on HumanEval (100 Python problems).
Score: pass@1 — does the completion pass the unit tests?

Run:
    pip install datasets
    python scripts/run_humaneval.py

Outputs: backend/humaneval_results.json
"""
import json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from openrouter import call_model, compute_cost
from router import classify as rules_classify, select_branch, select_model
from config import MODEL_MAP

DATA_PATH = Path(__file__).parent.parent / "data" / "humaneval_100.json"
OUT_PATH  = Path(__file__).parent.parent / "backend" / "humaneval_results.json"
NAIVE_MODEL = "openai/gpt-4o"

SYSTEM = (
    "You are an expert Python programmer. Complete the function body. "
    "Output ONLY the code — no explanation, no markdown fences. "
    "Do not repeat the function signature."
)


def download_humaneval() -> list[dict]:
    from datasets import load_dataset
    ds = load_dataset("openai/openai_humaneval", split="test")
    samples = [dict(r) for r in list(ds)[:100]]
    DATA_PATH.parent.mkdir(exist_ok=True)
    json.dump(samples, open(DATA_PATH, "w"), indent=2)
    print(f"Saved {len(samples)} problems → {DATA_PATH}")
    return samples


def run_tests(prompt: str, completion: str, test: str, entry_point: str) -> bool:
    code = prompt + completion + "\n\n" + test + f"\n\ncheck({entry_point})\n"
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False


samples = json.load(open(DATA_PATH)) if DATA_PATH.exists() else download_humaneval()
results = []

for i, s in enumerate(samples):
    label  = rules_classify(s["prompt"])
    branch = select_branch(label)
    model  = select_model(label) or MODEL_MAP["cheap_model"]

    r_res   = call_model(model, s["prompt"], max_tokens=512, system=SYSTEM)
    r_pass  = run_tests(s["prompt"], r_res["answer"], s["test"], s["entry_point"])
    r_cost  = compute_cost(r_res["usage"], model)

    n_res   = call_model(NAIVE_MODEL, s["prompt"], max_tokens=512, system=SYSTEM)
    n_pass  = run_tests(s["prompt"], n_res["answer"], s["test"], s["entry_point"])
    n_cost  = compute_cost(n_res["usage"], NAIVE_MODEL)

    results.append({
        "task_id":       s["task_id"],
        "router_branch": branch,
        "router_model":  model,
        "router_pass":   r_pass,
        "router_cost":   r_cost,
        "naive_pass":    n_pass,
        "naive_cost":    n_cost,
        "label":         label,
    })

    print(f"  [{i+1:3}/100] {'PASS' if r_pass else 'FAIL'}  {branch}  {model.split('/')[-1]}")
    time.sleep(0.3)

json.dump(results, open(OUT_PATH, "w"), indent=2)

total    = len(results)
r_acc    = sum(r["router_pass"] for r in results) / total
n_acc    = sum(r["naive_pass"]  for r in results) / total
r_cost   = sum(r["router_cost"] for r in results)
n_cost   = sum(r["naive_cost"]  for r in results)
savings  = (1 - r_cost / n_cost) * 100

print(f"\nHumanEval  router={r_acc:.1%}  naive={n_acc:.1%}  savings={savings:.1f}%")
print(f"Saved → {OUT_PATH}")
```

### New `app.py` route

```python
HUMANEVAL_PATH = os.path.join(os.path.dirname(__file__), "humaneval_results.json")

@app.route("/api/eval/humaneval")
def humaneval_summary():
    if not os.path.exists(HUMANEVAL_PATH):
        return jsonify({"error": "humaneval_results.json not found"}), 404
    data = json.load(open(HUMANEVAL_PATH))
    total = len(data)
    r_cost = sum(r["router_cost"] for r in data)
    n_cost = sum(r["naive_cost"]  for r in data)
    return jsonify({
        "total":             total,
        "router_pass_at_1":  round(sum(r["router_pass"] for r in data) / total, 4),
        "naive_pass_at_1":   round(sum(r["naive_pass"]  for r in data) / total, 4),
        "router_cost_usd":   round(r_cost, 6),
        "naive_cost_usd":    round(n_cost, 6),
        "cost_reduction_pct": round((1 - r_cost / n_cost) * 100, 1),
        "model_distribution": {
            m: sum(1 for r in data if r["router_model"] == m)
            for m in set(r["router_model"] for r in data)
        },
        "questions": data,
    })
```

### Note on `call_model` — add `system` kwarg

`openrouter.py` needs one small update to accept a system prompt:

```python
def call_model(model_id: str, query: str, max_tokens: int = 512,
               system: str | None = None) -> dict:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": query})
    # rest unchanged, replace the hardcoded messages=[...] line
```

---

## 3. Karpathy Wiki-Backed Memory

Full implementation in previous version is unchanged. Key summary:

- `memory.py` replaced with BM25 (`rank_bm25`) over `Wiki/**/*.md`
- Seed pairs stay as guaranteed demo fallback
- Returns `source_ref: Wiki/components/router.md:42` in the trace
- `pip install rank-bm25` added to `requirements.txt`
- SCORE_THRESHOLD = 3.0 — tune down if too few wiki hits

Stage line: *"Karpathy's LLM Wiki proposal — compile knowledge once, answer from it for free."*

---

## 4. Tool Call Branch

Full implementation in previous version is unchanged. Key summary:

- New `backend/tools.py`: `weather(location)` via wttr.in + `code_exec(code)` via subprocess
- `router.py`: TOOL_KEYWORDS + `tool_call` in `classify()` + `select_branch()`
- `app.py`: tool_call execution path in `route_stream()`
- `config.py`: add `"tool_call": "teal"` to BRANCH_COLORS

---

## 5. CLI Tool

### Install

```
project/
  cli.py          ← single-file CLI
  pyproject.toml  ← entry point: router = "cli:main"
```

Add to `pyproject.toml` (or create if not present):

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "router-cli"
version = "0.1.0"
dependencies = ["rank-bm25"]

[project.scripts]
router = "cli:main"
```

Install: `pip install -e .` from `project/` root.

### Usage

```bash
router "what does enumerate do in python"
router "debug this: def fib(n): return fib(n-1) + fib(n-2)"
router --file app.py "what does this function do"
cat traceback.txt | router "why is this failing"
router run "print(sum([1,2,3]))"
```

### `cli.py` (new file, project root)

```python
#!/usr/bin/env python3
"""
router — cost-aware LLM routing from your terminal.

Required env vars:
    OPENROUTER_API_KEY    for mid / strong model fallback
    CLASSIFIER_URL        ngrok URL for Qwen2-1.5B classifier
    CHEAP_MODEL_URL       ngrok vLLM URL for fine-tuned Llama 8B (OpenAI-compat)

Optional:
    ROUTER_WIKI_PATH      path to Wiki/ folder (default: ./Wiki)

Install:
    pip install -e .
    # then just: router "your question"
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.error
from pathlib import Path
from typing import Iterator

# ── ANSI ──────────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"; BLUE   = "\033[94m"; YELLOW = "\033[93m"
ORANGE = "\033[38;5;208m"; TEAL = "\033[96m"; PURPLE = "\033[95m"
MUTED  = "\033[90m"; BOLD   = "\033[1m";  RESET  = "\033[0m"

BRANCH_COLOR = {
    "memory_answer": GREEN, "cheap_model": BLUE, "mid_model": YELLOW,
    "strong_model": ORANGE, "tool_call": TEAL, "verification_tool": PURPLE,
}
BRANCH_LABEL = {
    "memory_answer": "wiki", "cheap_model": "fast", "mid_model": "mid",
    "strong_model": "strong", "tool_call": "tool", "verification_tool": "verify",
}

# ── Config ────────────────────────────────────────────────────────────────────
OR_KEY          = os.getenv("OPENROUTER_API_KEY", "")
CLASSIFIER_URL  = os.getenv("CLASSIFIER_URL", "").rstrip("/")
CHEAP_URL       = os.getenv("CHEAP_MODEL_URL", "").rstrip("/")
WIKI_ROOT       = Path(os.getenv("ROUTER_WIKI_PATH", "./Wiki"))
OR_BASE         = "https://openrouter.ai/api/v1"
MID_MODEL       = "meta-llama/llama-3.1-70b-instruct"
STRONG_MODEL    = "openai/gpt-4o-mini"
COST_PER_1M     = {"cheap_model": 0.05, "mid_model": 0.35, "strong_model": 0.15}

# ── Wiki BM25 ─────────────────────────────────────────────────────────────────
try:
    from rank_bm25 import BM25Okapi
    _HAS_BM25 = True
except ImportError:
    _HAS_BM25 = False

def _tok(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())

def _load_wiki():
    if not _HAS_BM25 or not WIKI_ROOT.exists():
        return [], None
    pages = []
    for md in WIKI_ROOT.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
            pages.append((str(md.relative_to(WIKI_ROOT.parent)), text, text.splitlines()))
        except Exception:
            continue
    if not pages:
        return [], None
    return pages, BM25Okapi([_tok(p[1]) for p in pages])

_PAGES, _BM25 = _load_wiki()

def search_wiki(query: str, threshold: float = 3.0) -> dict | None:
    if _BM25 is None:
        return None
    scores = _BM25.get_scores(_tok(query))
    idx = int(scores.argmax())
    if float(scores[idx]) < threshold:
        return None
    path, _, lines = _PAGES[idx]
    tokens = set(_tok(query))
    scored = [(sum(1 for t in tokens if t in _tok(l)), i, l)
              for i, l in enumerate(lines) if l.strip() and not l.startswith("#")]
    scored = [(s, i, l) for s, i, l in scored if s > 0]
    if not scored:
        return None
    scored.sort(reverse=True)
    _, li, best = scored[0]
    return {"answer": best.lstrip("- ").strip(),
            "source": f"{path}:{li+1}", "score": float(scores[idx])}

# ── Classifier ────────────────────────────────────────────────────────────────
TOOL_KW   = {"weather in", "weather for", "temperature in", "execute this", "run this code", "run this python"}
VERIFY_KW = {"what does the project", "what models does", "what architecture", "what files"}
HARD_KW   = {"why", "explain", "compare", "analyze", "critique", "evaluate", "derive", "prove"}
MED_KW    = {"how", "describe", "summarize", "difference between", "steps to"}
CODE_KW   = {"code", "function", "debug", "python", "javascript", "implement", "algorithm", "class", "error", "typescript"}
MATH_KW   = {"calculate", "solve", "equation", "integral", "derivative", "probability", "theorem"}

def _rules_classify(query: str) -> dict:
    q, wc = query.lower(), len(query.split())
    if any(w in q for w in TOOL_KW):
        d = "weather" if any(w in q for w in {"weather", "temperature"}) else "code_exec"
        return {"complexity": "tool", "domain": d}
    if any(w in q for w in VERIFY_KW):
        return {"complexity": "verify", "domain": "project"}
    d = "code" if any(w in q for w in CODE_KW) else \
        "math" if any(w in q for w in MATH_KW) else "factual"
    if any(w in q for w in HARD_KW) or wc > 40 or d in {"code", "math"}:
        c = "hard"
    elif any(w in q for w in MED_KW) or wc > 20:
        c = "medium"
    else:
        c = "simple"
    return {"complexity": c, "domain": d}

def classify(query: str) -> dict:
    if not CLASSIFIER_URL:
        return _rules_classify(query)
    try:
        payload = json.dumps({"query": query}).encode()
        req = urllib.request.Request(f"{CLASSIFIER_URL}/classify", data=payload,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = json.loads(resp.read())
        return {"complexity": body["complexity"], "domain": body["domain"]}
    except Exception:
        return _rules_classify(query)

def select_branch(label: dict) -> str:
    c = label["complexity"]
    if c == "tool":   return "tool_call"
    if c == "verify": return "verification_tool"
    return {"simple": "cheap_model", "medium": "mid_model", "hard": "strong_model"}.get(c, "strong_model")

# ── Model streaming ───────────────────────────────────────────────────────────
def _stream(base: str, model: str, messages: list, key: str) -> Iterator[str]:
    payload = json.dumps({"model": model, "messages": messages,
                          "stream": True, "max_tokens": 1024}).encode()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    if "openrouter" in base:
        headers["HTTP-Referer"] = "https://router-cli.dev"
    req = urllib.request.Request(f"{base}/chat/completions",
                                 data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        for raw in resp:
            line = raw.decode("utf-8").strip()
            if not line.startswith("data: ") or line == "data: [DONE]":
                continue
            try:
                delta = json.loads(line[6:])["choices"][0]["delta"].get("content", "")
                if delta:
                    yield delta
            except Exception:
                continue

def call_cheap(msgs: list) -> Iterator[str]:
    if CHEAP_URL:
        # vLLM OpenAI-compatible — model name doesn't matter, just use "local"
        yield from _stream(CHEAP_URL, "local", msgs, "local")
    else:
        yield from _stream(OR_BASE, "meta-llama/llama-3.1-8b-instruct", msgs, OR_KEY)

def call_mid(msgs: list)    -> Iterator[str]: yield from _stream(OR_BASE, MID_MODEL,    msgs, OR_KEY)
def call_strong(msgs: list) -> Iterator[str]: yield from _stream(OR_BASE, STRONG_MODEL, msgs, OR_KEY)

# ── Tools ─────────────────────────────────────────────────────────────────────
def tool_weather(location: str) -> str:
    try:
        url = f"https://wttr.in/{urllib.request.quote(location)}?format=j1"
        with urllib.request.urlopen(url, timeout=5) as resp:
            d = json.loads(resp.read())["current_condition"][0]
        return (f"{location}: {d['weatherDesc'][0]['value']}, "
                f"{d['temp_C']}°C / {d['temp_F']}°F, humidity {d['humidity']}%")
    except Exception as e:
        return f"Weather lookup failed: {e}"

def tool_code_exec(code: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code); path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=5)
        return r.stdout[:500] if r.returncode == 0 else f"Error: {r.stderr[:300]}"
    except subprocess.TimeoutExpired:
        return "Error: 5s timeout"

# ── Display ───────────────────────────────────────────────────────────────────
def badge(branch: str, source: str | None, cost: float, ms: int) -> None:
    c     = BRANCH_COLOR.get(branch, "")
    label = BRANCH_LABEL.get(branch, branch)
    src   = f"  {MUTED}{source}{RESET}" if source else ""
    cost_s = f"${cost:.6f}" if cost > 0 else "$0.00"
    print(f"\n{c}{BOLD}◆ {label}{RESET}{src}  {MUTED}{cost_s}  {ms}ms{RESET}\n")

# ── Routing ───────────────────────────────────────────────────────────────────
def route(query: str) -> None:
    t0 = time.monotonic()

    # 1. Wiki memory
    hit = search_wiki(query)
    if hit:
        badge("memory_answer", hit["source"], 0.0, int((time.monotonic()-t0)*1000))
        print(hit["answer"])
        return

    label  = classify(query)
    branch = select_branch(label)

    # 2. Tools
    if branch == "tool_call":
        domain = label.get("domain", "")
        if domain == "weather":
            loc = re.sub(r".*(weather in|temperature in|weather for)\s*", "",
                         query, flags=re.I).strip() or "New York"
            ans = tool_weather(loc)
        else:
            m    = re.search(r"```(?:python)?\s*([\s\S]+?)```", query, re.I)
            code = m.group(1).strip() if m else re.sub(
                r"(?:execute|run this|run)[:]*\s*", "", query, flags=re.I).strip()
            ans = tool_code_exec(code)
        badge("tool_call", None, 0.0, int((time.monotonic()-t0)*1000))
        print(ans)
        return

    # 3. Verify
    if branch == "verification_tool":
        fallback = search_wiki(query, threshold=1.0)
        badge("verification_tool", fallback["source"] if fallback else None,
              0.0, int((time.monotonic()-t0)*1000))
        print(fallback["answer"] if fallback else "No matching fact found locally.")
        return

    # 4. Model branches — stream tokens directly to terminal
    msgs   = [{"role": "user", "content": query}]
    caller = {"cheap_model": call_cheap, "mid_model": call_mid,
              "strong_model": call_strong}[branch]

    badge(branch, None, 0.0, 0)

    full = ""
    for tok in caller(msgs):
        print(tok, end="", flush=True)
        full += tok
    print()

    ms   = int((time.monotonic()-t0)*1000)
    cost = round((max(1, len(full.split())*1.3) / 1_000_000) * COST_PER_1M.get(branch, 0.15), 8)
    print(f"\n{MUTED}  ${cost:.6f}  {ms}ms{RESET}")

# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    # Special case: router run "code"
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        code = " ".join(sys.argv[2:])
        t0   = time.monotonic()
        badge("tool_call", None, 0.0, 0)
        print(tool_code_exec(code))
        print(f"\n{MUTED}  $0.00  {int((time.monotonic()-t0)*1000)}ms{RESET}")
        return

    parser = argparse.ArgumentParser(prog="router",
                                     description="Cost-aware LLM routing from your terminal.")
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--file", "-f", metavar="FILE")
    args = parser.parse_args()

    query = args.query

    # Pipe support: cat file.txt | router "why is this failing"
    if not sys.stdin.isatty():
        stdin = sys.stdin.read().strip()
        query = f"{stdin}\n\n{query}".strip() if query else stdin

    if not query:
        parser.print_help()
        return

    # File context
    if args.file:
        try:
            content = Path(args.file).read_text(encoding="utf-8")
            query = f"File: {args.file}\n```\n{content[:3000]}\n```\n\n{query}"
        except FileNotFoundError:
            print(f"File not found: {args.file}", file=sys.stderr)
            return

    route(query)

if __name__ == "__main__":
    main()
```

---

## 6. Dashboard: 4 New Charts

### New `app.py` endpoints

```python
@app.route("/api/eval/pareto")
def eval_pareto():
    if not os.path.exists(EVAL_PATH):
        return jsonify({"error": "eval_results.json not found"}), 404
    data  = json.load(open(EVAL_PATH))
    r_cost = sum(r["router_cost"]    for r in data)
    r_acc  = sum(r["router_correct"] for r in data) / len(data)
    n_cost = sum(r["naive_cost"]     for r in data)
    n_acc  = sum(r["naive_correct"]  for r in data) / len(data)
    cheap_per_q = 0.05 / 1_000_000 * 200  # ~200 tokens at $0.05/1M
    return jsonify({
        "points": [
            {"label": "Naive (all cheap)",  "cost": round(cheap_per_q * len(data), 6), "accuracy": 0.33,           "type": "baseline"},
            {"label": "Our Router",         "cost": round(r_cost, 6),                  "accuracy": round(r_acc, 4), "type": "router"},
            {"label": "Naive (all GPT-4o)", "cost": round(n_cost, 6),                  "accuracy": round(n_acc, 4), "type": "baseline"},
        ],
    })


@app.route("/api/eval/pgr")
def eval_pgr():
    if not os.path.exists(EVAL_PATH):
        return jsonify({"error": "eval_results.json not found"}), 404
    data  = json.load(open(EVAL_PATH))
    total = len(data)
    rank  = {"hard": 2, "medium": 1, "simple": 0, "verify": 0}
    ranked = sorted(data, key=lambda r: rank.get(r["label"]["complexity"], 0), reverse=True)
    strong_ids = {r["id"] for r in ranked}
    cheap_acc  = 0.33
    strong_acc = sum(r["naive_correct"] for r in data) / total
    curve = []
    for pct in range(0, 101, 5):
        n  = int(total * pct / 100)
        ids = {r["id"] for r in ranked[:n]}
        hits = sum(r["naive_correct"] if r["id"] in ids else
                   (1 if r["router_correct"] and r["router_branch"] == "cheap_model" else 0)
                   for r in data)
        acc = hits / total
        pgr = (acc - cheap_acc) / (strong_acc - cheap_acc) if strong_acc != cheap_acc else 0
        curve.append({"pct_strong": pct, "accuracy": round(acc, 4), "pgr": round(max(0, pgr), 4)})
    router_pct = sum(1 for r in data if r["router_branch"] == "strong_model") / total * 100
    router_pgr = (sum(r["router_correct"] for r in data) / total - cheap_acc) / (strong_acc - cheap_acc)
    return jsonify({"curve": curve, "router_pct_strong": round(router_pct, 1),
                    "router_pgr": round(max(0, router_pgr), 4)})


@app.route("/api/eval/confusion")
def eval_confusion():
    if not os.path.exists(EVAL_PATH):
        return jsonify({"error": "eval_results.json not found"}), 404
    data   = json.load(open(EVAL_PATH))
    matrix: dict[str, dict[str, int]] = {}
    for r in data:
        c = r["label"]["complexity"]
        b = r["router_branch"]
        matrix.setdefault(c, {})[b] = matrix.get(c, {}).get(b, 0) + 1
    return jsonify({"matrix": matrix})
```

Wire the three new React chart components (`pareto-chart.tsx`, `pgr-chart.tsx`, `confusion-matrix.tsx`) into `dashboard.tsx` — full component code in the previous doc version, unchanged.

---

## 7. Training Part A: Classifier (Qwen2-1.5B) — Coding-Focused Synthetic Examples

Update the `SYNTHETIC` list in `training/prepare_dataset.py`. Replace the current general-knowledge examples with developer-assistant queries. The classifier needs to be good at recognising coding questions, not geography questions.

**Drop all existing simple/medium/hard/factual examples. Replace with:**

```python
SYNTHETIC: list[dict] = [
    # simple / code — fast lookup, one-liner answers
    {"q": "What does enumerate() do in Python?",                       "c": "simple", "d": "code"},
    {"q": "How do I reverse a list in Python?",                        "c": "simple", "d": "code"},
    {"q": "What is a lambda function?",                                "c": "simple", "d": "code"},
    {"q": "What does the 'self' keyword do in Python?",                "c": "simple", "d": "code"},
    {"q": "How do I check the type of a variable in Python?",          "c": "simple", "d": "code"},
    {"q": "What is the difference between a list and a tuple?",        "c": "simple", "d": "code"},
    {"q": "How do I import a module in Python?",                       "c": "simple", "d": "code"},
    {"q": "What does zip() do?",                                       "c": "simple", "d": "code"},
    {"q": "How do I read a file in Python?",                           "c": "simple", "d": "code"},
    {"q": "What is the difference between == and is in Python?",       "c": "simple", "d": "code"},
    {"q": "How do I convert a string to an integer?",                  "c": "simple", "d": "code"},
    {"q": "What does list comprehension look like in Python?",         "c": "simple", "d": "code"},
    {"q": "How do I get the length of a list?",                        "c": "simple", "d": "code"},
    {"q": "What is the difference between append and extend?",         "c": "simple", "d": "code"},
    {"q": "How do I iterate over a dictionary?",                       "c": "simple", "d": "code"},
    {"q": "What does range() return?",                                 "c": "simple", "d": "code"},
    {"q": "How do I format a string with f-strings?",                  "c": "simple", "d": "code"},
    {"q": "What is None in Python?",                                   "c": "simple", "d": "code"},
    {"q": "How do I sort a list in Python?",                           "c": "simple", "d": "code"},
    {"q": "What does the * operator do when unpacking?",               "c": "simple", "d": "code"},

    # medium / code — multi-step explanations
    {"q": "How do I implement a binary search in Python?",                        "c": "medium", "d": "code"},
    {"q": "How does Python's garbage collector work?",                            "c": "medium", "d": "code"},
    {"q": "Describe how decorators work in Python.",                              "c": "medium", "d": "code"},
    {"q": "How do I handle exceptions properly in Python?",                       "c": "medium", "d": "code"},
    {"q": "What is the difference between deepcopy and copy in Python?",          "c": "medium", "d": "code"},
    {"q": "How do async/await work in Python?",                                   "c": "medium", "d": "code"},
    {"q": "How does React's useEffect hook work?",                                "c": "medium", "d": "code"},
    {"q": "What is the difference between props and state in React?",             "c": "medium", "d": "code"},
    {"q": "How do I set up a Flask REST API?",                                    "c": "medium", "d": "code"},
    {"q": "How does memoization work and when should I use it?",                  "c": "medium", "d": "code"},
    {"q": "Describe the steps to implement JWT authentication in a web app.",     "c": "medium", "d": "code"},
    {"q": "How do I use TypeScript generics?",                                    "c": "medium", "d": "code"},
    {"q": "What is the event loop in Node.js?",                                   "c": "medium", "d": "code"},
    {"q": "How does database indexing improve query performance?",                "c": "medium", "d": "code"},
    {"q": "What are Python generators and how do they differ from lists?",        "c": "medium", "d": "code"},
    {"q": "How do I write a context manager in Python?",                          "c": "medium", "d": "code"},
    {"q": "Describe how CSS flexbox layout works.",                               "c": "medium", "d": "code"},
    {"q": "How do I structure a React app with multiple pages?",                  "c": "medium", "d": "code"},
    {"q": "What is the difference between SQL and NoSQL databases?",              "c": "medium", "d": "code"},
    {"q": "How does Git rebase differ from Git merge?",                           "c": "medium", "d": "code"},

    # hard / code — analysis, debugging, architecture
    {"q": "Implement a thread-safe LRU cache in Python with O(1) get and put.",                      "c": "hard", "d": "code"},
    {"q": "Debug: my FastAPI endpoint is silently dropping requests under load. Why and how to fix?", "c": "hard", "d": "code"},
    {"q": "Implement Dijkstra's algorithm in Python for a weighted directed graph.",                  "c": "hard", "d": "code"},
    {"q": "Analyze the performance bottleneck in this database query and rewrite it.",                "c": "hard", "d": "code"},
    {"q": "Write a Python decorator that retries a function with exponential backoff.",               "c": "hard", "d": "code"},
    {"q": "Compare microservices vs monolith architecture — when should I use each?",                "c": "hard", "d": "code"},
    {"q": "Implement a rate limiter using the token bucket algorithm in Python.",                     "c": "hard", "d": "code"},
    {"q": "Debug: my React component re-renders on every parent render despite React.memo. Why?",    "c": "hard", "d": "code"},
    {"q": "Implement consistent hashing for a distributed cache in Python.",                         "c": "hard", "d": "code"},
    {"q": "Write a producer-consumer queue in Python using threading primitives.",                   "c": "hard", "d": "code"},
    {"q": "Explain why my async Python code has a race condition and how to fix it.",                 "c": "hard", "d": "code"},
    {"q": "Design a schema for a multi-tenant SaaS application in PostgreSQL.",                      "c": "hard", "d": "code"},
    {"q": "Implement merge sort and prove its O(n log n) time complexity.",                          "c": "hard", "d": "code"},
    {"q": "Why does my Python multiprocessing code deadlock and how do I fix it?",                   "c": "hard", "d": "code"},
    {"q": "Critique the architecture of this Flask app and suggest improvements.",                   "c": "hard", "d": "code"},

    # hard / math (keep some — devs need this too)
    {"q": "Derive the time complexity of a balanced BST insertion.",           "c": "hard", "d": "math"},
    {"q": "Prove that the sum of first n numbers is n(n+1)/2 by induction.",   "c": "hard", "d": "math"},
    {"q": "What is the expected number of hash collisions for n items in a table of size m?", "c": "hard", "d": "math"},
    {"q": "Solve the recurrence T(n) = 2T(n/2) + n using the master theorem.", "c": "hard", "d": "math"},
    {"q": "Calculate the probability of a hash collision with birthday paradox.", "c": "hard", "d": "math"},

    # tool / code_exec
    {"q": "Execute this Python: print(2 ** 10)",                               "c": "tool", "d": "code_exec"},
    {"q": "Run this code: import math; print(math.sqrt(144))",                 "c": "tool", "d": "code_exec"},
    {"q": "Execute: x = [1, 2, 3, 4, 5]; print(sum(x), max(x))",              "c": "tool", "d": "code_exec"},
    {"q": "Run this Python: print('hello world')",                             "c": "tool", "d": "code_exec"},
    {"q": "Execute code: for i in range(5): print(i**2)",                      "c": "tool", "d": "code_exec"},
    {"q": "Run this: import json; d={'a':1}; print(json.dumps(d))",            "c": "tool", "d": "code_exec"},
    {"q": "Execute this Python code: print(sorted([3,1,4,1,5,9]))",            "c": "tool", "d": "code_exec"},
    {"q": "What's the weather in London?",                                     "c": "tool", "d": "weather"},
    {"q": "Weather in Tokyo right now",                                        "c": "tool", "d": "weather"},
    {"q": "Current temperature in New York",                                   "c": "tool", "d": "weather"},

    # verify / project
    {"q": "What models does this router use?",                      "c": "verify", "d": "project"},
    {"q": "What does the project architecture look like?",          "c": "verify", "d": "project"},
    {"q": "What files are in the backend?",                         "c": "verify", "d": "project"},
    {"q": "What is the routing logic in this system?",              "c": "verify", "d": "project"},
    {"q": "Which wiki documents cover fine-tuning?",                "c": "verify", "d": "project"},
    {"q": "What components are in the system?",                     "c": "verify", "d": "project"},
    {"q": "How does the memory branch work in this project?",       "c": "verify", "d": "project"},
    {"q": "What models are mapped to which branches in config.py?", "c": "verify", "d": "project"},
    {"q": "What are the routing branches in this system?",          "c": "verify", "d": "project"},
    {"q": "Describe the current classifier logic in router.py.",    "c": "verify", "d": "project"},
]
```

Also update `SYSTEM_PROMPT` in `prepare_dataset.py` to include `"tool"` complexity and `"code_exec"` / `"weather"` domains — see Section 5 of the previous doc version.

---

## 8. Training Part B: Llama 8B Code Fine-tune

This is a **separate training job** from the classifier. Goal: fine-tune Llama 8B on coding instruction data so it actually generates better code. The classifier (Part A) learns to *route* better; this model learns to *answer* better.

### New files

```
project/training/
  train_llama_code.py     ← fine-tune Llama 8B on Code Alpaca subset
  prepare_code_alpaca.py  ← download + format Code Alpaca for SFT
  models/
    llama-8b-code/          ← LoRA adapter
    llama-8b-code-merged/   ← merged, ready for vLLM
```

### `training/prepare_code_alpaca.py` (new file)

```python
"""
Download Code Alpaca (20K coding instruction examples) and format for SFT.
Uses first 2000 examples for a fast training run on H200 (~45 min).

Run:
    pip install datasets
    python prepare_code_alpaca.py
Outputs:
    data/code_alpaca_train.json
    data/code_alpaca_val.json
"""
import json, random
from pathlib import Path
from datasets import load_dataset

SYSTEM = (
    "You are an expert software engineer. "
    "Answer coding questions clearly and concisely. "
    "Provide working code examples where relevant."
)

OUT_DIR = Path(__file__).parent / "data"

ds = load_dataset("sahil2801/CodeAlpaca-20k", split="train")
samples = list(ds)[:2000]
random.seed(42)
random.shuffle(samples)

def fmt(s: dict) -> dict:
    user_content = s["instruction"]
    if s.get("input", "").strip():
        user_content += f"\n\n{s['input']}"
    return {
        "instruction": "Answer this coding question.",
        "input":       user_content,
        "output":      s["output"],
        "system":      SYSTEM,
    }

all_ex = [fmt(s) for s in samples]
split  = int(len(all_ex) * 0.9)
train, val = all_ex[:split], all_ex[split:]

OUT_DIR.mkdir(exist_ok=True)
json.dump(train, open(OUT_DIR / "code_alpaca_train.json", "w"), indent=2)
json.dump(val,   open(OUT_DIR / "code_alpaca_val.json",   "w"), indent=2)
print(f"Train: {len(train)}  Val: {len(val)}")
```

### `training/train_llama_code.py` (new file)

```python
"""
Fine-tune Llama 3.1 8B Instruct on Code Alpaca subset.
Same LoRA config as the classifier but different base model.

Run:
    python train_llama_code.py

Outputs:
    models/llama-8b-code/          ← adapter
    models/llama-8b-code-merged/   ← merged model, serve with vLLM
"""
import os
from pathlib import Path
import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer
import json

BASE   = os.getenv("LLAMA_BASE_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
ROOT   = Path(__file__).parent
OUT    = ROOT / "models" / "llama-8b-code"
MERGED = ROOT / "models" / "llama-8b-code-merged"
DATA   = ROOT / "data"

tokenizer = AutoTokenizer.from_pretrained(BASE)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16, device_map="auto")
model.config.use_cache = False
model.gradient_checkpointing_enable()

lora = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
)
model = get_peft_model(model, lora)
model.print_trainable_parameters()

def fmt(ex: dict) -> dict:
    msgs = [
        {"role": "system",    "content": ex["system"]},
        {"role": "user",      "content": f"{ex['instruction']}\n\n{ex['input']}"},
        {"role": "assistant", "content": ex["output"]},
    ]
    return {"text": tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)}

def load(path: Path):
    records = json.load(open(path))
    ds = Dataset.from_list(records)
    return ds.map(fmt, remove_columns=ds.column_names)

train_ds = load(DATA / "code_alpaca_train.json")
val_ds   = load(DATA / "code_alpaca_val.json")
print(f"Train: {len(train_ds)}  Val: {len(val_ds)}")

OUT.mkdir(parents=True, exist_ok=True)

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer,
    train_dataset=train_ds, eval_dataset=val_ds,
    args=SFTConfig(
        output_dir=str(OUT), dataset_text_field="text",
        max_seq_length=1024,
        per_device_train_batch_size=2, gradient_accumulation_steps=8,
        num_train_epochs=3, learning_rate=2e-4, warmup_ratio=0.05,
        lr_scheduler_type="cosine", bf16=True,
        logging_steps=10, evaluation_strategy="epoch",
        save_strategy="epoch", load_best_model_at_end=True,
        metric_for_best_model="eval_loss", report_to="none", seed=42,
    ),
)
trainer.train()

model.save_pretrained(str(OUT))
tokenizer.save_pretrained(str(OUT))

MERGED.mkdir(parents=True, exist_ok=True)
merged = model.merge_and_unload()
merged.save_pretrained(str(MERGED), safe_serialization=True)
tokenizer.save_pretrained(str(MERGED))
print(f"Done. Merged → {MERGED}")
```

---

## 9. H200 Serving Setup

Two processes on the H200, two ngrok tunnels.

```bash
# Terminal 1 — classifier (already exists)
cd project/training
python serve.py --port 8001
# ngrok http 8001 → CLASSIFIER_URL

# Terminal 2 — fine-tuned Llama 8B via vLLM (new)
pip install vllm
vllm serve project/training/models/llama-8b-code-merged \
    --port 8002 \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.45   # leaves headroom for classifier
# ngrok http 8002 → CHEAP_MODEL_URL
```

`--gpu-memory-utilization 0.45` splits the H200 roughly 45% for Llama 8B + 10% for classifier + remainder free.

vLLM exposes an OpenAI-compatible endpoint at `:8002/v1/chat/completions`. The CLI's `call_cheap()` hits this directly with model name `"local"` — vLLM ignores the model name and uses whatever is loaded.

The Flask server (`app.py`) also picks this up automatically via `CHEAP_MODEL_URL` if you wire it into `openrouter.py` — treat it as another provider with base URL override.

---

## 10. File Change Map

| File | Type | What |
|---|---|---|
| `backend/memory.py` | Full rewrite | BM25 wiki search + seed fallback |
| `backend/router.py` | Modify | TOOL_KEYWORDS, tool_call in classify/select_branch/rationale |
| `backend/config.py` | Modify | add `tool_call` to BRANCH_COLORS |
| `backend/tools.py` | New | weather + code_exec |
| `backend/app.py` | Modify | tool_call path in route_stream; /humaneval, /pareto, /pgr, /confusion routes |
| `backend/openrouter.py` | Modify | add `system` kwarg to `call_model()` |
| `backend/humaneval_results.json` | Generated | committed before demo |
| `data/humaneval_100.json` | Generated | downloaded |
| `scripts/run_humaneval.py` | New | HumanEval runner |
| `training/prepare_dataset.py` | Modify | replace synthetic examples with coding-focused ones; add tool/verify classes |
| `training/prepare_code_alpaca.py` | New | download + format Code Alpaca |
| `training/train_llama_code.py` | New | fine-tune Llama 8B on Code Alpaca |
| `training/serve.py` | Modify | update SYSTEM_PROMPT + valid labels to include `tool` and `code_exec`/`weather` |
| `frontend/src/components/ui/pareto-chart.tsx` | New | Pareto scatter |
| `frontend/src/components/ui/pgr-chart.tsx` | New | PGR curve |
| `frontend/src/components/ui/confusion-matrix.tsx` | New | 4×4 heatmap |
| `frontend/src/components/ui/dashboard.tsx` | Modify | wire 3 new charts |
| `cli.py` | New | CLI entry point |
| `pyproject.toml` | New/modify | `router = "cli:main"` entry point |
| `requirements.txt` | Modify | add `rank-bm25` |

---

## 11. Hourly Schedule

| Hour | Goal | Done when |
|---|---|---|
| H0 | `pip install rank-bm25` · rewrite `memory.py` · smoke test wiki search | `python -c "from memory import check_memory; print(check_memory('what is the router'))"` returns wiki hit |
| H1 | `prepare_code_alpaca.py` runs · `train_llama_code.py` starts on H200 | Training loss printing; walk away and let it run |
| H2 | `run_humaneval.py` · `humaneval_results.json` committed | `GET /api/eval/humaneval` returns valid JSON |
| H3 | `tools.py` · TOOL_KEYWORDS in `router.py` · tool_call path in `app.py` | `router "what's the weather in London"` returns real weather |
| H4 | vLLM serving fine-tuned Llama 8B on H200 (if training done) · ngrok tunnel up | `curl $CHEAP_MODEL_URL/v1/models` returns 200 |
| H5 | `/api/eval/pareto` + `/pgr` + `/confusion` endpoints | All three return valid JSON |
| H6 | React: pareto-chart + pgr-chart + confusion-matrix wired into dashboard | Charts render with real data |
| H7 | `cli.py` + `pyproject.toml` · `pip install -e .` works · all 5 branches demo from terminal | `router "debug this: def fib(n): return fib(n-1) + fib(n-2)"` returns answer |
| H8 | Update classifier `prepare_dataset.py` with coding synthetic examples · retrain Qwen2 if time | New `data/train.json` has coding-focused examples |
| Buffer | Fix whatever broke. Rehearse demo arc 3×. | Ship |

**Priority if time-constrained:**
1. Memory (H0) — biggest narrative win, 1 hour
2. HumanEval eval (H2) — judges specifically asked for task-specific benchmark
3. CLI (H7) — best demo moment for developer audience
4. Llama fine-tune (H1/H4) — if training finishes in time, huge upgrade; if not, fall back to OpenRouter Llama 8B
5. Charts (H5-H6) — polish, do after core features work

---

## 12. Demo Arc — Developer Assistant

**Audience:** developers and engineers (both tracks)
**Setting:** terminal open alongside browser

### Setup line
> "Every developer assistant today uses the same model for every question. 'What does enumerate do?' goes to GPT-4. 'Debug my deadlock' goes to GPT-4. We built the routing layer that changes that."

### 9-step demo

1. **Wiki hit** — terminal: `router "how does the routing classifier work"`
   → `◆ wiki  Wiki/components/router.md:14  $0.00  3ms`
   → answer streams from the wiki
   → *"Karpathy's LLM Wiki — compiled knowledge, answered for free."*

2. **Cheap model** — terminal: `router "what does enumerate do in python"`
   → `◆ fast  $0.000003  420ms`
   → Llama 8B (fine-tuned, on your H200) answers
   → *"Simple lookup. Fine-tuned Llama 8B. Runs on our hardware. Zero API cost."*

3. **Tool call** — terminal: `router run "print(sorted([3,1,4,1,5,9]))"`
   → `◆ tool  $0.00  48ms` → `[1, 1, 3, 4, 5, 9]`
   → *"Doesn't generate. Executes."*

4. **File context** — terminal: `router --file backend/router.py "why does this misroute medium queries"`
   → reads the file, routes to strong model, streams analysis
   → *"File context in one flag."*

5. **Pipe** — terminal: `cat traceback.txt | router "why is this failing"`
   → mid or strong depending on error complexity
   → *"Works with your existing shell workflow."*

6. **Strong model** — terminal: `router "compare async vs threading in Python for IO-bound workloads"`
   → `◆ strong  gpt-4o-mini  $0.000015  1.4s`
   → *"Hard analysis question. Only now does it escalate."*

7. **Switch to browser** — cost ticker: "6 queries. Router: $X. Naive GPT-4o: $Y."
   → *"Everything you just saw — 5 of those 6 queries cost nothing or near-nothing."*

8. **Dashboard — HumanEval tab** — PGR curve + Pareto frontier
   → *"We evaluated on HumanEval — OpenAI's Python benchmark. Our fine-tuned 8B handles [X]% of problems correctly. The router escalates to strong only when necessary. Same pass@1, [Y]% cheaper."*

9. **Close**
   > *"This isn't a chatbot. It's a routing layer. Drop it into any codebase — `pip install -e .`, three env vars — and your developer assistant stops paying GPT-4 prices for questions that don't need GPT-4."*

---

## 13. Risks

| Risk | Mitigation |
|---|---|
| Llama 8B fine-tune not done in time | Fall back to OpenRouter Llama 8B — CLI `call_cheap()` already handles this via `if CHEAP_URL` check |
| vLLM OOM on H200 | Lower `--gpu-memory-utilization` to 0.35; or pause classifier server during Llama serving |
| `wttr.in` down during demo | `tool_weather()` returns error string, not crash; prepare a hardcoded weather fallback |
| `code_exec` sandbox: malicious/infinite loop code during demo | Only run pre-approved demo snippets; subprocess timeout=5s kills infinite loops |
| BM25 returns wrong wiki page | SCORE_THRESHOLD=3.0 prevents low-confidence hits; seed pairs catch the guaranteed demo queries |
| HumanEval pass rate lower than expected | Reframe: "Our fine-tuned model handles [X]% at zero API cost. RouteLLM showed routing doesn't need to match — it needs to be good enough at the right cost." |
| ngrok tunnel drops during demo | Have backup: run both models locally via OpenRouter; demo still works, just without "local model" story |
| CLI streaming broken on Windows | `cli.py` uses `urllib` + raw SSE parsing — should work; test early |
