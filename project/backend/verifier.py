import os

PROJECT_MAP_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "Wiki", "00-preload", "project-map.md"
)


def _score_line(line: str, query_words: set) -> int:
    line_words = set(line.lower().split())
    return len(query_words & line_words)


def verify_from_project_map(query: str) -> dict:
    try:
        with open(PROJECT_MAP_PATH, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return {"answer": "project-map.md not found.", "source": PROJECT_MAP_PATH, "line": None}

    query_words = set(query.lower().split()) - {"what", "the", "is", "does", "a", "an", "of", "for"}
    scored = [
        (_score_line(line, query_words), i, line.strip())
        for i, line in enumerate(lines)
        if line.strip() and not line.startswith("#")
    ]
    scored = [(s, i, l) for s, i, l in scored if s > 0]

    if not scored:
        return {
            "answer": "No matching fact found in project-map.md.",
            "source": "Wiki/00-preload/project-map.md",
            "line": None,
        }

    scored.sort(reverse=True)
    _, line_num, best_line = scored[0]
    return {
        "answer": best_line.lstrip("- "),
        "source": "Wiki/00-preload/project-map.md",
        "line": line_num + 1,
    }


def run_verification(query: str) -> dict:
    result = verify_from_project_map(query)
    source_ref = f"{result['source']}:{result['line']}" if result["line"] else result["source"]
    return {
        "answer": result["answer"],
        "branch": "verification_tool",
        "model_used": None,
        "rationale": "Query asks for a project fact — answered from local file, not model generation",
        "cost_usd": 0.0,
        "naive_cost_usd": 0.0,
        "latency_ms": 5,
        "fallback": False,
        "source_ref": source_ref,
    }
