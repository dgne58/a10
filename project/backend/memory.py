import os
import re
from glob import glob

_WIKI_LINK_RE = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")   # [[link|display]] → display
_WIKI_LINK_BARE_RE = re.compile(r"\[\[([^\]]+)\]\]")           # [[link]] → link


def _clean_wiki_text(text: str) -> str:
    text = _WIKI_LINK_RE.sub(r"\2", text)
    text = _WIKI_LINK_BARE_RE.sub(r"\1", text)
    return text

WIKI_ROOT = os.environ.get("ROUTER_WIKI_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "Wiki"))
SCORE_THRESHOLD = 10.0

# Files that contain planning/demo content rather than reference knowledge
_EXCLUDED_PATTERNS = ("design-doc", "design_doc", "demo", "clipping", "index", "readme", "toc", "00-index")

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
_corpus_paths: list[str] = []   # one entry per file (relative path)
_corpus_excerpts: list[str] = []  # first ~400 chars of prose per file


def _prose_lines(path: str) -> list[str]:
    """Extract prose lines from a markdown file, stripping frontmatter, code blocks, and noise."""
    result = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            raw_lines = f.readlines()

        in_frontmatter = False
        frontmatter_done = False
        in_code = False

        for i, line in enumerate(raw_lines):
            s = line.strip()
            # Handle YAML frontmatter block (--- ... ---)
            if i == 0 and s == "---":
                in_frontmatter = True
                continue
            if in_frontmatter:
                if s == "---":
                    in_frontmatter = False
                    frontmatter_done = True
                continue
            if s.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if s.startswith(("{", "[", "|", "#!", "//", "$ ", "- {")):
                continue
            if s.endswith(".md") or s.endswith(".md)"):
                continue
            s = _clean_wiki_text(s)
            if len(s) > 20:
                result.append(s)
    except OSError:
        pass
    return result


def _load_bm25() -> None:
    global _bm25, _corpus_paths, _corpus_excerpts
    try:
        from rank_bm25 import BM25Okapi
    except ImportError:
        return

    wiki_glob = os.path.join(WIKI_ROOT, "**", "*.md")
    paths = glob(wiki_glob, recursive=True)
    docs: list[str] = []
    doc_paths: list[str] = []
    excerpts: list[str] = []

    for path in paths:
        if any(p in path.lower() for p in _EXCLUDED_PATTERNS):
            continue
        lines = _prose_lines(path)
        if len(lines) < 3:
            continue
        full_text = " ".join(lines)
        excerpt = "\n".join(lines[:8])
        docs.append(full_text)
        doc_paths.append(os.path.relpath(path, WIKI_ROOT))
        excerpts.append(excerpt)

    if not docs:
        return

    tokenized = [d.lower().split() for d in docs]
    _bm25 = BM25Okapi(tokenized)
    _corpus_paths = doc_paths
    _corpus_excerpts = excerpts


def _get_page_content(source_ref: str, max_chars: int = 3000) -> str:
    """Read the full wiki page as prose (code blocks + noisy lines stripped)."""
    try:
        rel_path = source_ref.split(":")[0]
        full_path = os.path.join(WIKI_ROOT, rel_path)
        with open(full_path, encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        lines = _prose_lines(full_path)
        text = "\n".join(lines)
        return _clean_wiki_text(text)[:max_chars]
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
    page_content = _get_page_content(source_ref)
    snippet = _corpus_excerpts[best_idx]
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

    # Skip BM25 for code-shaped inputs (function stubs, HumanEval prompts, etc.)
    _is_code = "def " in query or '"""' in query or "'''" in query or "->" in query
    wiki_hit = None if _is_code else _search_wiki(query)
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
