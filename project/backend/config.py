MODEL_MAP = {
    "cheap_model":       "meta-llama/llama-3.1-8b-instruct",
    "mid_model":         "meta-llama/llama-3.1-70b-instruct",
    "strong_model":      "anthropic/claude-haiku-4.5",
}

FALLBACK_MODEL = "anthropic/claude-sonnet-4.6"

COST_PER_1M = {
    "meta-llama/llama-3.1-8b-instruct":  0.05,
    "meta-llama/llama-3.1-70b-instruct": 0.35,
    "openai/gpt-4o-mini":                0.15,
    "openai/gpt-4o":                     2.50,
    "anthropic/claude-haiku-4.5":        1.00,
    "anthropic/claude-sonnet-4.6":       3.00,
}

BRANCH_COLORS = {
    "memory_answer":     "green",
    "cheap_model":       "blue",
    "mid_model":         "yellow",
    "strong_model":      "orange",
}
