"""
prepare_dataset.py

Builds training/validation JSONL from:
  1. eval_results.json  (100 real MMLU questions with labels)
  2. Synthetic examples (hand-crafted per class to balance distribution)

Output format: Alpaca-style JSON list for Unsloth SFT.
Each record: {"instruction": ..., "input": <query>, "output": <json label>}

Run:
    python prepare_dataset.py
Outputs:
    data/train.json  (~350 examples)
    data/val.json    (~80 examples)
"""

import json
import random
import os
from pathlib import Path

SYSTEM_PROMPT = (
    "You are a query classifier for an LLM routing system. "
    "Given a user query, output a JSON object with two fields:\n"
    '  "complexity": one of "simple", "medium", "hard", "verify"\n'
    '  "domain":     one of "factual", "math", "code", "project"\n\n'
    "Rules:\n"
    '- "verify"  → query asks about this specific project\'s architecture, models, or files\n'
    '- "simple"  → short factual lookup, < 20 words, no reasoning required\n'
    '- "medium"  → requires explanation or multi-step description, 20-40 words\n'
    '- "hard"    → analysis, comparison, derivation, or long complex query\n'
    '- "code"    → involves programming, debugging, or software implementation\n'
    '- "math"    → involves calculation, equations, or proofs\n'
    '- "factual" → general knowledge not covered by other domains\n'
    '- "project" → only used when complexity is "verify"\n\n'
    "Output only the JSON object, no explanation."
)

INSTRUCTION = "Classify this query for LLM routing. Return only a JSON object."

# ── Synthetic examples per class ──────────────────────────────────────────────

SYNTHETIC: list[dict] = [
    # simple / factual
    {"q": "What is the capital of Japan?",                   "c": "simple",  "d": "factual"},
    {"q": "Who wrote Romeo and Juliet?",                     "c": "simple",  "d": "factual"},
    {"q": "What year did World War II end?",                 "c": "simple",  "d": "factual"},
    {"q": "What is the boiling point of water in Celsius?",  "c": "simple",  "d": "factual"},
    {"q": "Name the largest planet in the solar system.",    "c": "simple",  "d": "factual"},
    {"q": "What currency does Brazil use?",                  "c": "simple",  "d": "factual"},
    {"q": "How many continents are there?",                  "c": "simple",  "d": "factual"},
    {"q": "What is the chemical symbol for gold?",           "c": "simple",  "d": "factual"},
    {"q": "Who painted the Mona Lisa?",                      "c": "simple",  "d": "factual"},
    {"q": "What is the speed of light?",                     "c": "simple",  "d": "factual"},
    {"q": "What language is spoken in Brazil?",              "c": "simple",  "d": "factual"},
    {"q": "How many bones are in the human body?",           "c": "simple",  "d": "factual"},
    {"q": "What is photosynthesis?",                         "c": "simple",  "d": "factual"},
    {"q": "What ocean is the largest?",                      "c": "simple",  "d": "factual"},
    {"q": "Who invented the telephone?",                     "c": "simple",  "d": "factual"},
    {"q": "What is the tallest mountain on Earth?",          "c": "simple",  "d": "factual"},
    {"q": "What is the atomic number of carbon?",            "c": "simple",  "d": "factual"},
    {"q": "What does DNA stand for?",                        "c": "simple",  "d": "factual"},
    {"q": "What is the capital of Australia?",               "c": "simple",  "d": "factual"},
    {"q": "When was the Eiffel Tower built?",                "c": "simple",  "d": "factual"},

    # medium / factual
    {"q": "Describe the main causes of the French Revolution.",        "c": "medium", "d": "factual"},
    {"q": "How does the immune system protect the body from infection?","c": "medium", "d": "factual"},
    {"q": "Summarize the key differences between RNA and DNA.",        "c": "medium", "d": "factual"},
    {"q": "What are the steps involved in the water cycle?",           "c": "medium", "d": "factual"},
    {"q": "How does natural selection drive evolution?",               "c": "medium", "d": "factual"},
    {"q": "Describe the difference between mitosis and meiosis.",      "c": "medium", "d": "factual"},
    {"q": "How does the stock market work?",                           "c": "medium", "d": "factual"},
    {"q": "What causes tides in the ocean?",                           "c": "medium", "d": "factual"},
    {"q": "Summarize the events that led to World War I.",             "c": "medium", "d": "factual"},
    {"q": "How does a vaccine trigger an immune response?",            "c": "medium", "d": "factual"},
    {"q": "Describe the structure of the United States government.",   "c": "medium", "d": "factual"},
    {"q": "What is the difference between weather and climate?",       "c": "medium", "d": "factual"},
    {"q": "How does the Federal Reserve control inflation?",           "c": "medium", "d": "factual"},
    {"q": "Explain how black holes form.",                             "c": "medium", "d": "factual"},
    {"q": "What are the main symptoms and causes of depression?",      "c": "medium", "d": "factual"},
    {"q": "Describe how a nuclear power plant generates electricity.",  "c": "medium", "d": "factual"},
    {"q": "Summarize the process of protein synthesis in cells.",      "c": "medium", "d": "factual"},
    {"q": "How does inflation affect consumer purchasing power?",      "c": "medium", "d": "factual"},
    {"q": "What causes earthquakes and how are they measured?",        "c": "medium", "d": "factual"},
    {"q": "Describe the phases of the moon and their causes.",         "c": "medium", "d": "factual"},

    # hard / factual
    {"q": "Analyze the long-term geopolitical implications of the Soviet Union's collapse on Eastern European NATO membership.",
     "c": "hard", "d": "factual"},
    {"q": "Compare and contrast Keynesian and monetarist approaches to managing recessions, citing historical examples.",
     "c": "hard", "d": "factual"},
    {"q": "Evaluate the ethical implications of CRISPR gene editing in human embryos, considering both therapeutic and enhancement applications.",
     "c": "hard", "d": "factual"},
    {"q": "Critique the evidence for and against the multiverse hypothesis in modern cosmology.",
     "c": "hard", "d": "factual"},
    {"q": "Analyze why antibiotic resistance is accelerating and what policy interventions are most supported by evidence.",
     "c": "hard", "d": "factual"},
    {"q": "Compare the effectiveness of carbon taxes versus cap-and-trade systems for reducing greenhouse gas emissions.",
     "c": "hard", "d": "factual"},
    {"q": "Explain the pros and cons of central bank digital currencies from the perspective of monetary policy and financial inclusion.",
     "c": "hard", "d": "factual"},
    {"q": "Evaluate the arguments for and against universal basic income using evidence from pilot programs.",
     "c": "hard", "d": "factual"},
    {"q": "Why do democracies sometimes elect authoritarian leaders? Analyze the sociological and economic factors.",
     "c": "hard", "d": "factual"},
    {"q": "Analyze the relationship between income inequality and social mobility across OECD countries.",
     "c": "hard", "d": "factual"},
    {"q": "Compare the theoretical frameworks of Rawlsian and utilitarian justice in the context of healthcare rationing.",
     "c": "hard", "d": "factual"},
    {"q": "What are the implications of quantum computing for current public-key cryptography systems?",
     "c": "hard", "d": "factual"},

    # hard / math
    {"q": "Derive the quadratic formula from first principles using completing the square.",                 "c": "hard", "d": "math"},
    {"q": "Solve the differential equation dy/dx = ky where k is a constant. Show all steps.",              "c": "hard", "d": "math"},
    {"q": "Prove that the sum of the first n natural numbers is n(n+1)/2 using mathematical induction.",    "c": "hard", "d": "math"},
    {"q": "Calculate the probability that a standard normal variable falls within 2 standard deviations.",  "c": "hard", "d": "math"},
    {"q": "Find the eigenvalues of the matrix [[3,1],[1,3]].",                                              "c": "hard", "d": "math"},
    {"q": "Evaluate the integral of x^2 * e^x from 0 to infinity.",                                        "c": "hard", "d": "math"},
    {"q": "Prove that the square root of 2 is irrational.",                                                 "c": "hard", "d": "math"},
    {"q": "Solve the system: 3x + 2y = 7, 5x - y = 3. Verify your answer.",                                "c": "hard", "d": "math"},
    {"q": "Derive the formula for the sum of a geometric series.",                                          "c": "hard", "d": "math"},
    {"q": "Calculate the compound interest on $10,000 at 5% annual rate compounded monthly for 3 years.",   "c": "hard", "d": "math"},
    {"q": "What is the expected value and variance of a binomial distribution with n=20, p=0.3?",           "c": "hard", "d": "math"},
    {"q": "Prove that there are infinitely many prime numbers.",                                             "c": "hard", "d": "math"},
    {"q": "Solve the recurrence relation T(n) = 2T(n/2) + n using the master theorem.",                    "c": "hard", "d": "math"},
    {"q": "Calculate the determinant of a 3x3 matrix [[1,2,3],[4,5,6],[7,8,9]] and explain its significance.",
     "c": "hard", "d": "math"},
    {"q": "Derive the Taylor series expansion for e^x around x=0 and prove its convergence.",              "c": "hard", "d": "math"},

    # hard / code
    {"q": "Implement a thread-safe LRU cache in Python with O(1) get and put operations.",                                         "c": "hard", "d": "code"},
    {"q": "Write a recursive function to solve the Tower of Hanoi problem and analyze its time complexity.",                        "c": "hard", "d": "code"},
    {"q": "Debug this Python code: def fib(n): return fib(n-1) + fib(n-2). Why does it fail and how do you fix it?",              "c": "hard", "d": "code"},
    {"q": "Implement Dijkstra's shortest path algorithm in Python for a weighted directed graph.",                                  "c": "hard", "d": "code"},
    {"q": "Write a JavaScript async function that fetches data from three URLs in parallel and returns when all complete.",         "c": "hard", "d": "code"},
    {"q": "Implement a binary search tree in TypeScript with insert, delete, and in-order traversal methods.",                     "c": "hard", "d": "code"},
    {"q": "Write a Python decorator that retries a function up to 3 times with exponential backoff on exception.",                 "c": "hard", "d": "code"},
    {"q": "Implement a rate limiter using the token bucket algorithm in Python.",                                                   "c": "hard", "d": "code"},
    {"q": "Write SQL to find the second highest salary in an employees table without using LIMIT.",                                 "c": "hard", "d": "code"},
    {"q": "Implement merge sort in Python and prove its O(n log n) time complexity.",                                              "c": "hard", "d": "code"},
    {"q": "Write a React hook that debounces a value with cleanup on unmount.",                                                     "c": "hard", "d": "code"},
    {"q": "Implement a producer-consumer queue in Python using threading primitives.",                                              "c": "hard", "d": "code"},
    {"q": "Write a Python context manager for database transactions with rollback on exception.",                                   "c": "hard", "d": "code"},
    {"q": "Implement consistent hashing in Python for a distributed cache.",                                                       "c": "hard", "d": "code"},
    {"q": "Debug: my React component re-renders on every parent render even with React.memo. Why and how to fix?",                 "c": "hard", "d": "code"},

    # verify / project
    {"q": "What models does this router use?",                                    "c": "verify", "d": "project"},
    {"q": "What does the project architecture look like?",                        "c": "verify", "d": "project"},
    {"q": "What files are in the backend?",                                       "c": "verify", "d": "project"},
    {"q": "What is the routing logic in this system?",                            "c": "verify", "d": "project"},
    {"q": "Which wiki documents cover fine-tuning?",                              "c": "verify", "d": "project"},
    {"q": "What components are in the system?",                                   "c": "verify", "d": "project"},
    {"q": "What does the design doc say about benchmarks?",                       "c": "verify", "d": "project"},
    {"q": "How does the memory branch work in this project?",                     "c": "verify", "d": "project"},
    {"q": "What is the routing architecture of this codebase?",                   "c": "verify", "d": "project"},
    {"q": "What models are mapped to which branches in config.py?",               "c": "verify", "d": "project"},
    {"q": "What is the eval benchmark approach for this router?",                 "c": "verify", "d": "project"},
    {"q": "What does the project do?",                                            "c": "verify", "d": "project"},
    {"q": "How is the verification tool implemented here?",                       "c": "verify", "d": "project"},
    {"q": "Describe the current classifier logic in router.py.",                  "c": "verify", "d": "project"},
    {"q": "What are the five routing branches in this system?",                   "c": "verify", "d": "project"},
]


def format_example(query: str, complexity: str, domain: str) -> dict:
    label = json.dumps({"complexity": complexity, "domain": domain})
    return {
        "instruction": INSTRUCTION,
        "input": query,
        "output": label,
        "system": SYSTEM_PROMPT,
    }


def load_eval_examples(eval_path: str) -> list[dict]:
    data = json.load(open(eval_path))
    examples = []
    for r in data:
        examples.append(format_example(
            query=r["question"],
            complexity=r["label"]["complexity"],
            domain=r["label"]["domain"],
        ))
    return examples


def main():
    root = Path(__file__).parent
    eval_path = root.parent / "backend" / "eval_results.json"
    out_dir = root / "data"
    out_dir.mkdir(exist_ok=True)

    # Load real examples
    real = load_eval_examples(str(eval_path))
    print(f"Real examples from eval: {len(real)}")

    # Build synthetic
    synthetic = [
        format_example(s["q"], s["c"], s["d"]) for s in SYNTHETIC
    ]
    print(f"Synthetic examples: {len(synthetic)}")

    all_examples = real + synthetic
    random.seed(42)
    random.shuffle(all_examples)

    # 80/20 split
    split = int(len(all_examples) * 0.8)
    train = all_examples[:split]
    val = all_examples[split:]

    json.dump(train, open(out_dir / "train.json", "w"), indent=2)
    json.dump(val,   open(out_dir / "val.json",   "w"), indent=2)

    print(f"Train: {len(train)} | Val: {len(val)}")
    print(f"Saved to {out_dir}/")

    # Class distribution report
    from collections import Counter
    def dist(examples):
        parsed = [json.loads(e["output"]) for e in examples]
        return Counter((p["complexity"], p["domain"]) for p in parsed)

    print("\nTrain distribution:")
    for (c, d), n in sorted(dist(train).items()):
        print(f"  {c:8} / {d:8}: {n}")


if __name__ == "__main__":
    main()
