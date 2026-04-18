"""Simple SSE probe for /api/route/stream.

Run from `project/`:
    python backend/test_stream.py
"""

from __future__ import annotations

import argparse
import json

import httpx


DEFAULT_URL = "http://localhost:5000/api/route/stream"
DEFAULT_QUERIES = [
    "what does enumerate do in python",
    "whats the weather in london",
    "run this code: print(2**10)",
]


def stream_query(query: str, url: str, timeout: float) -> None:
    print(f"\n--- {query} ---")
    with httpx.stream("POST", url, json={"query": query}, timeout=timeout) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line or not line.startswith("data: "):
                continue
            payload = json.loads(line[6:])
            print(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe the streaming route and print SSE payloads.")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Streaming endpoint URL. Defaults to {DEFAULT_URL}.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "queries",
        nargs="*",
        help="Optional queries to run. Defaults to the three canned stream checks.",
    )
    args = parser.parse_args()

    queries = args.queries or DEFAULT_QUERIES
    for query in queries:
        stream_query(query, url=args.url, timeout=args.timeout)


if __name__ == "__main__":
    main()
