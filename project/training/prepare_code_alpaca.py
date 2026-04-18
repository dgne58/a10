"""
prepare_code_alpaca.py

Downloads sahil2801/CodeAlpaca-20k and prepares training data
for fine-tuning Llama 3.1 8B on coding tasks.

Run:
    python prepare_code_alpaca.py

Output:
    training/data/code_alpaca_train.json  (~1800 examples)
    training/data/code_alpaca_val.json    (~200 examples)
"""

import json
import random
from pathlib import Path

LIMIT = 2000
SPLIT_RATIO = 0.9
SYSTEM_PROMPT = (
    "You are an expert software engineer. "
    "Answer coding questions clearly and concisely with working code examples."
)

OUT_DIR = Path(__file__).parent / "data"


def main() -> None:
    try:
        from datasets import load_dataset
    except ImportError:
        print("Install with: pip install datasets")
        raise

    print("[code_alpaca] Downloading sahil2801/CodeAlpaca-20k ...")
    ds = load_dataset("sahil2801/CodeAlpaca-20k", split="train", trust_remote_code=True)
    raw = list(ds)[:LIMIT]
    print(f"[code_alpaca] Using {len(raw)} examples")

    examples = [
        {
            "instruction": r["instruction"],
            "input": r.get("input", ""),
            "output": r["output"],
            "system": SYSTEM_PROMPT,
        }
        for r in raw
    ]

    random.seed(42)
    random.shuffle(examples)

    split = int(len(examples) * SPLIT_RATIO)
    train = examples[:split]
    val = examples[split:]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json.dump(train, open(OUT_DIR / "code_alpaca_train.json", "w"), indent=2)
    json.dump(val,   open(OUT_DIR / "code_alpaca_val.json",   "w"), indent=2)

    print(f"[code_alpaca] Train: {len(train)} | Val: {len(val)}")
    print(f"[code_alpaca] Saved to {OUT_DIR}/")


if __name__ == "__main__":
    main()
