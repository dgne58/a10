MEMORY_PAIRS = [
    {
        "triggers": ["capital of france", "france capital"],
        "answer": "Paris.",
        "source": "hardcoded",
    },
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
            "strong model, or local verification (free). Every response includes a "
            "visible trace showing which branch was chosen and why."
        ),
        "source": "Wiki/00-preload/project-map.md",
    },
    {
        "triggers": ["how much does gpt-4 cost", "gpt-4o cost", "openai pricing"],
        "answer": "GPT-4o costs approximately $2.50 per 1M input tokens. GPT-4o Mini costs $0.15/1M. Llama 3.1 8B via OpenRouter costs $0.05/1M.",
        "source": "hardcoded",
    },
    {
        "triggers": ["what is the routing research", "berkeley routing", "cost reduction routing"],
        "answer": (
            "RouteLLM (Berkeley 2024) proved that only 13.4% of MT-Bench queries need "
            "the strong model to recover 50% of the quality gap. Routing the rest to "
            "a cheap model cuts cost by up to 3.66x with no meaningful quality loss."
        ),
        "source": "Wiki/sources/routing-papers.md",
    },
]


def check_memory(query: str) -> dict | None:
    q = query.lower()
    for pair in MEMORY_PAIRS:
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
    return None
