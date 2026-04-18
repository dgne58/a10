import os
import re
from glob import glob

WIKI_ROOT = os.environ.get("ROUTER_WIKI_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "Wiki"))
SCORE_THRESHOLD = 8.0

# Files that contain planning/demo content rather than reference knowledge
_EXCLUDED_PATTERNS = ("design-doc", "design_doc", "demo", "clipping")

SEED_PAIRS = [
    {
        "triggers": ["what is routellm", "routellm paper", "routellm"],
        "answer": (
            "RouteLLM is a UC Berkeley + Anyscale paper (arXiv:2406.18665) that trains "
            "routers on 80K Chatbot Arena preference battles to route queries between a "
            "strong and a weak LLM. It achieved up to 3.66x cost reduction on MT-Bench "
            "and 1.41-1.49x on MMLU/GSM8K with no quality loss."
        ),
        "source": "Clippings/RouteLLM Learning to Route LLMs with Preference Data.md",
    },
    {
        "triggers": ["what does this project do", "what is this system", "what is this app"],
        "answer": (
            "This system is a branch router. Every query is routed to the cheapest "
            "sufficient execution path: local memory (free), cheap model, mid model, "
            "strong model, tool call (free), or local verification (free). Every response "
            "includes a visible trace showing which branch was chosen and why."
        ),
        "source": "Wiki/00-preload/project-map.md",
    },
]

_bm25 = None
_corpus_paths: list[str] = []
_corpus_lines: list[str] = []


def _load_bm25() -> None:
    global _bm25, _corpus_paths, _corpus_lines
    try:
        from rank_bm25 import BM25Okapi
    except ImportError:
        return

    wiki_glob = os.path.join(WIKI_ROOT, "**", "*.md")
    paths = glob(wiki_glob, recursive=True)
    lines: list[str] = []
    line_paths: list[str] = []

    for path in paths:
        if any(p in path.lower() for p in _EXCLUDED_PATTERNS):
            continue
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                in_code_block = False
                for i, line in enumerate(f, 1):
                    stripped = line.strip()
                    if stripped.startswith("```"):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        continue
                    # Skip lines that look like code or data, not prose
                    if stripped.startswith(("{", "[", "|", "#!", "//", "$ ", "- {")):
                        continue
                    if len(stripped) > 30:
                        lines.append(stripped)
                        line_paths.append(f"{os.path.relpath(path, WIKI_ROOT)}:{i}")
        except OSError:
            continue

    if not lines:
        return

    tokenized = [l.lower().split() for l in lines]
    _bm25 = BM25Okapi(tokenized)
    _corpus_paths = line_paths
    _corpus_lines = lines


def _get_paragraph(source_ref: str, center_line: int, window: int = 8) -> str:
    """Return up to `window` lines around `center_line` from the source file."""
    try:
        rel_path = source_ref.split(":")[0]
        full_path = os.path.join(WIKI_ROOT, rel_path)
        with open(full_path, encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
        start = max(0, center_line - 3)
        end = min(len(all_lines), center_line + window)
        lines = []
        in_code = False
        for ln in all_lines[start:end]:
            s = ln.strip()
            if s.startswith("```"):
                in_code = not in_code
                continue
            if in_code or not s or s.startswith(("#!", "//", "$ ", "- {", "{", "[")):
                continue
            lines.append(s)
        return "\n".join(lines[:window])
    except OSError:
        return ""


def _get_page_content(source_ref: str, max_chars: int = 3000) -> str:
    """Read the full wiki page as prose (code blocks + noisy lines stripped)."""
    try:
        rel_path = source_ref.split(":")[0]
        full_path = os.path.join(WIKI_ROOT, rel_path)
        with open(full_path, encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        lines = []
        in_code = False
        for ln in raw.splitlines():
            s = ln.strip()
            if s.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if s.startswith(("{", "[", "|", "#!", "//", "$ ", "- {")):
                continue
            lines.append(s)
        text = "\n".join(l for l in lines if l)
        return text[:max_chars]
    except OSError:
        return ""


def _search_wiki(query: str) -> dict | None:
    global _bm25
    if _bm25 is None:
        _load_bm25()
    if _bm25 is None:
        return None

    tokens = query.lower().split()
    scores = _bm25.get_scores(tokens)
    best_idx = int(scores.argmax())
    best_score = float(scores[best_idx])

    if best_score < SCORE_THRESHOLD:
        return None

    source_ref = _corpus_paths[best_idx]
    center_line = int(source_ref.split(":")[-1]) if ":" in source_ref else 1
    paragraph = _get_paragraph(source_ref, center_line)
    snippet = paragraph if paragraph else _corpus_lines[best_idx]
    page_content = _get_page_content(source_ref)
    return {
        "answer": snippet,
        "source_ref": source_ref,
        "bm25_score": best_score,
        "wiki_context": page_content,
    }


def check_memory(query: str) -> dict | None:
    q = query.lower()
    for pair in SEED_PAIRS:
        if any(trigger in q for trigger in pair["triggers"]):
            return {
                "answer": pair["answer"],
                "branch": "memory_answer",
                "model_used": None,
                "rationale": "Answer found in local memory — no model call needed",
                "cost_usd": 0.0,
                "naive_cost_usd": 0.0,
                "latency_ms": 1,
                "fallback": False,
                "source_ref": pair["source"],
            }

    wiki_hit = _search_wiki(query)
    if wiki_hit:
        return {
            "answer": wiki_hit["answer"],
            "branch": "memory_answer",
            "model_used": None,
            "rationale": f"Answer found in wiki (BM25 score {wiki_hit['bm25_score']:.1f}) — no model call needed",
            "cost_usd": 0.0,
            "naive_cost_usd": 0.0,
            "latency_ms": 2,
            "fallback": False,
            "source_ref": wiki_hit["source_ref"],
        }

    return None
