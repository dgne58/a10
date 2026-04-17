"""
integrate.py

Drop-in patch showing how to replace the regex classify() in router.py
with an HTTP call to the local vLLM classifier server (serve.py).

Usage (from project/backend/):

    # Option A - monkey-patch at startup
    from training.integrate import install_classifier_patch
    install_classifier_patch()

    # Option B - copy classify_via_model() into router.py directly
    #             and remove the old classify() body.

The server must be running:
    cd project/training && python serve.py --port 8001
"""

import json
import urllib.error
import urllib.request
from typing import Literal

CLASSIFIER_URL = "http://localhost:8001/classify"
TIMEOUT_S = 2.0

Complexity = Literal["simple", "medium", "hard", "verify"]
Domain = Literal["factual", "math", "code", "project"]


def classify_via_model(query: str) -> dict[str, Complexity | Domain]:
    """
    Call the local vLLM classifier. Returns a router-compatible label dict.
    Raises RuntimeError on network or timeout error so caller can fall back.
    """
    payload = json.dumps({"query": query}).encode()
    req = urllib.request.Request(
        CLASSIFIER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            body = json.loads(resp.read())
            return {
                "complexity": body["complexity"],
                "domain": body["domain"],
            }
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"classifier server unavailable: {exc}") from exc


def install_classifier_patch() -> None:
    """
    Monkey-patch router.classify() to use the fine-tuned model with
    automatic fallback to the original regex implementation.

    Call once at app startup, before any requests are handled.
    """
    try:
        import router as _router  # noqa: PLC0415
    except ImportError:
        print("[integrate] Could not import router module - patch skipped.")
        return

    original_classify = _router.classify

    def patched_classify(query: str):
        try:
            return classify_via_model(query)
        except RuntimeError:
            return original_classify(query)

    _router.classify = patched_classify  # type: ignore[attr-defined]
    print("[integrate] router.classify() patched -> fine-tuned model with regex fallback.")


if __name__ == "__main__":
    test_cases = [
        "What is the capital of Japan?",
        "Derive the quadratic formula from completing the square.",
        "Implement a thread-safe LRU cache in Python.",
        "What models does this router use?",
    ]
    print("Testing classifier server at", CLASSIFIER_URL)
    print("-" * 60)
    for q in test_cases:
        try:
            label = classify_via_model(q)
            print(f"[{label['complexity']:8} / {label['domain']:8}]  {q[:60]}")
        except RuntimeError as err:
            print(f"[ERROR] {err}")
            print("  -> Start serve.py first: python serve.py --port 8001")
            break
