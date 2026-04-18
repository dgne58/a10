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
from pathlib import Path

SYSTEM_PROMPT = (
    "You are a query classifier for an LLM routing system. "
    "Given a user query, output a JSON object with two fields:\n"
    '  "complexity": one of "simple", "medium", "hard"\n'
    '  "domain":     one of "factual", "math", "code"\n\n'
    "Rules:\n"
    '- "simple"  -> short factual or coding lookup, < 20 words, no reasoning required\n'
    '- "medium"  -> requires explanation or multi-step description, 20-40 words\n'
    '- "hard"    -> analysis, comparison, derivation, debugging, or architecture design\n'
    '- "code"    -> involves programming, debugging, or software implementation\n'
    '- "math"    -> involves calculation, equations, or proofs\n'
    '- "factual" -> general knowledge or project/codebase questions not covered by other domains\n\n'
    "Output only the JSON object, no explanation."
)

INSTRUCTION = "Classify this query for LLM routing. Return only a JSON object."

SYNTHETIC: list[dict] = [
    # simple / code — one-liners, quick syntax questions
    {"q": "How do I reverse a list in Python?",                              "c": "simple", "d": "code"},
    {"q": "What does the len() function do in Python?",                      "c": "simple", "d": "code"},
    {"q": "How do you declare a constant in JavaScript?",                    "c": "simple", "d": "code"},
    {"q": "What is the difference between == and === in JavaScript?",        "c": "simple", "d": "code"},
    {"q": "How do you create a virtual environment in Python?",              "c": "simple", "d": "code"},
    {"q": "What does git stash do?",                                         "c": "simple", "d": "code"},
    {"q": "How do you import a module in Python?",                           "c": "simple", "d": "code"},
    {"q": "What is a list comprehension in Python?",                         "c": "simple", "d": "code"},
    {"q": "How do you read a file in Python?",                               "c": "simple", "d": "code"},
    {"q": "What is the syntax for a lambda function in Python?",             "c": "simple", "d": "code"},
    {"q": "How do you check the type of a variable in Python?",              "c": "simple", "d": "code"},
    {"q": "What does pip install do?",                                       "c": "simple", "d": "code"},
    {"q": "How do you define a function in TypeScript?",                     "c": "simple", "d": "code"},
    {"q": "What is the difference between let and var in JavaScript?",       "c": "simple", "d": "code"},
    {"q": "How do you access a dictionary value in Python?",                 "c": "simple", "d": "code"},
    {"q": "What does the map() function do in Python?",                      "c": "simple", "d": "code"},
    {"q": "How do you handle exceptions in Python?",                         "c": "simple", "d": "code"},
    {"q": "What is the purpose of __init__ in a Python class?",              "c": "simple", "d": "code"},
    {"q": "How do you sort a list in Python?",                               "c": "simple", "d": "code"},
    {"q": "What is a tuple vs a list in Python?",                            "c": "simple", "d": "code"},

    # medium / code — explanations, multi-step how-tos
    {"q": "How does Python's garbage collector work?",                                      "c": "medium", "d": "code"},
    {"q": "Explain the difference between async and sync functions in JavaScript.",         "c": "medium", "d": "code"},
    {"q": "How do closures work in JavaScript? Give an example.",                           "c": "medium", "d": "code"},
    {"q": "What is the difference between a process and a thread?",                         "c": "medium", "d": "code"},
    {"q": "Explain how Python decorators work with a simple example.",                      "c": "medium", "d": "code"},
    {"q": "How does React's virtual DOM differ from the real DOM?",                         "c": "medium", "d": "code"},
    {"q": "Describe the steps to set up a REST API in Flask.",                              "c": "medium", "d": "code"},
    {"q": "What is the difference between SQL JOIN types (INNER, LEFT, RIGHT)?",            "c": "medium", "d": "code"},
    {"q": "How does Python's GIL affect multithreaded programs?",                           "c": "medium", "d": "code"},
    {"q": "Explain how Git branching and merging works.",                                   "c": "medium", "d": "code"},
    {"q": "What is Big O notation and how do you analyze algorithm complexity?",            "c": "medium", "d": "code"},
    {"q": "How does async/await work in Python's asyncio?",                                 "c": "medium", "d": "code"},
    {"q": "What is the difference between Docker and a virtual machine?",                   "c": "medium", "d": "code"},
    {"q": "Explain what CORS is and how to fix a CORS error in Flask.",                     "c": "medium", "d": "code"},
    {"q": "How do you use environment variables securely in a Python app?",                 "c": "medium", "d": "code"},
    {"q": "What is the difference between REST and GraphQL?",                               "c": "medium", "d": "code"},
    {"q": "How does Python's context manager protocol work?",                               "c": "medium", "d": "code"},
    {"q": "Explain the Model-View-Controller (MVC) pattern with an example.",               "c": "medium", "d": "code"},
    {"q": "How do you write a unit test for a function in Python using pytest?",            "c": "medium", "d": "code"},
    {"q": "What are Python generators and when should you use them?",                       "c": "medium", "d": "code"},

    # hard / code — implementations, debugging, architecture
    {"q": "Implement a thread-safe LRU cache in Python with O(1) get and put.",                                            "c": "hard", "d": "code"},
    {"q": "Debug this: def fib(n): return fib(n-1) + fib(n-2). Why does it crash and how do you fix it?",                 "c": "hard", "d": "code"},
    {"q": "Implement Dijkstra's shortest path algorithm in Python for a weighted directed graph.",                          "c": "hard", "d": "code"},
    {"q": "Write a Python decorator that retries a function up to 3 times with exponential backoff.",                      "c": "hard", "d": "code"},
    {"q": "Implement merge sort in Python and explain its O(n log n) time complexity.",                                    "c": "hard", "d": "code"},
    {"q": "Write a React custom hook that debounces a value with cleanup on unmount.",                                     "c": "hard", "d": "code"},
    {"q": "Implement a rate limiter using the token bucket algorithm in Python.",                                           "c": "hard", "d": "code"},
    {"q": "Implement consistent hashing in Python for a distributed key-value store.",                                     "c": "hard", "d": "code"},
    {"q": "Write a Python context manager that wraps database transactions with rollback on exception.",                    "c": "hard", "d": "code"},
    {"q": "Why does my React component re-render on every parent render even with React.memo? How do I fix it?",           "c": "hard", "d": "code"},
    {"q": "Implement a binary search tree in Python with insert, search, and in-order traversal.",                         "c": "hard", "d": "code"},
    {"q": "Write a Python async function that calls three APIs in parallel and aggregates results.",                        "c": "hard", "d": "code"},
    {"q": "Design a SQL schema for a multi-tenant SaaS app and explain your indexing strategy.",                           "c": "hard", "d": "code"},
    {"q": "Implement a pub-sub event system in Python using weak references to avoid memory leaks.",                       "c": "hard", "d": "code"},
    {"q": "Write a streaming tokenizer in Python that yields tokens lazily from a large file.",                            "c": "hard", "d": "code"},
    {"q": "What is the difference between a stack and a heap in memory management? How does Python use both?",             "c": "hard", "d": "code"},
    {"q": "Implement a trie data structure in Python for prefix-based autocomplete.",                                      "c": "hard", "d": "code"},
    {"q": "Write a Python function to flatten a deeply nested JSON object into a flat dict with dot-notation keys.",       "c": "hard", "d": "code"},
    {"q": "Implement a simple interpreter for arithmetic expressions using a recursive descent parser.",                    "c": "hard", "d": "code"},
    {"q": "Explain and implement the observer design pattern in Python.",                                                   "c": "hard", "d": "code"},

    # hard / code — HumanEval-style function stubs
    {"q": "def has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\"Return True if any two numbers in the list are closer to each other than threshold.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\"Split a string of nested parentheses into a list of balanced groups.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def truncate_number(number: float) -> float:\n    \"\"\"Return the decimal part of a positive floating point number.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def below_zero(operations: List[int]) -> bool:\n    \"\"\"Return True if the bank account balance ever falls below zero given a list of deposits/withdrawals.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def mean_absolute_deviation(numbers: List[float]) -> float:\n    \"\"\"Compute the mean absolute deviation of a list of numbers around the mean.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def intersperse(numbers: List[int], delimiter: int) -> List[int]:\n    \"\"\"Insert a delimiter between every two consecutive elements of the input list.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def parse_nested_parens(paren_string: str) -> List[int]:\n    \"\"\"Return the maximum nesting depth of each balanced parentheses group in the input.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def filter_by_substring(strings: List[str], substring: str) -> List[str]:\n    \"\"\"Filter a list of strings, returning only those that contain the given substring.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def sum_product(numbers: List[int]) -> Tuple[int, int]:\n    \"\"\"Return a tuple of the sum and product of all elements in the list.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def rolling_max(numbers: List[int]) -> List[int]:\n    \"\"\"Generate a list of rolling maximum elements found so far in the sequence.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def is_palindrome(string: str) -> bool:\n    \"\"\"Check if a given string is a palindrome, ignoring case and non-alphanumeric characters.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def make_palindrome(string: str) -> str:\n    \"\"\"Find the shortest palindrome that begins with the supplied string.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def string_xor(a: str, b: str) -> str:\n    \"\"\"XOR two binary strings digit by digit and return the result as a string.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def longest(strings: List[str]) -> Optional[str]:\n    \"\"\"Return the longest string in the list, or None if the list is empty.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def greatest_common_divisor(a: int, b: int) -> int:\n    \"\"\"Compute the greatest common divisor of two positive integers.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def all_prefixes(string: str) -> List[str]:\n    \"\"\"Return a list of all prefixes of the input string, from shortest to longest.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def string_sequence(n: int) -> str:\n    \"\"\"Return a string containing space-delimited numbers starting from 0 up to n inclusive.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def count_distinct_characters(string: str) -> int:\n    \"\"\"Return the number of distinct characters in a string, ignoring case.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def parse_music(music_string: str) -> List[int]:\n    \"\"\"Parse a string of musical notes ('o', 'o|', '.|') and return their durations in beats.\"\"\"\n", "c": "hard", "d": "code"},
    {"q": "def how_many_times(string: str, substring: str) -> int:\n    \"\"\"Count how many times a substring appears in a string, including overlapping occurrences.\"\"\"\n", "c": "hard", "d": "code"},

    # hard / math — algorithm complexity, proofs
    {"q": "What is the time complexity of quicksort in average and worst case? Why?",                 "c": "hard", "d": "math"},
    {"q": "Prove that the sum of the first n natural numbers is n(n+1)/2 using induction.",           "c": "hard", "d": "math"},
    {"q": "Solve the recurrence relation T(n) = 2T(n/2) + n using the master theorem.",              "c": "hard", "d": "math"},
    {"q": "What is the space complexity of depth-first search on a graph with V vertices and E edges?", "c": "hard", "d": "math"},
    {"q": "Prove that a binary heap supports insert and extract-min in O(log n).", "c": "hard", "d": "math"},
    {"q": "What is the time complexity of building a hash table with n elements?", "c": "hard", "d": "math"},
    {"q": "Analyze the amortized complexity of a dynamic array's push operation.", "c": "hard", "d": "math"},
    {"q": "What is the difference between P and NP complexity classes?", "c": "hard", "d": "math"},
    {"q": "Calculate the expected number of collisions in a hash table with n keys and m buckets.", "c": "hard", "d": "math"},
    {"q": "Prove that comparison-based sorting cannot be faster than O(n log n) in the worst case.", "c": "hard", "d": "math"},
    {"q": "What models does this router use?", "c": "simple", "d": "factual"},
    {"q": "What does the project architecture look like?", "c": "simple", "d": "factual"},
    {"q": "What files are in the backend?", "c": "simple", "d": "factual"},
    {"q": "What is the routing logic in this system?", "c": "simple", "d": "factual"},
    {"q": "Which wiki documents cover fine-tuning?", "c": "simple", "d": "factual"},
    {"q": "What components are in the system?", "c": "simple", "d": "factual"},
    {"q": "How does the memory branch work in this project?", "c": "simple", "d": "factual"},
    {"q": "What is the routing architecture of this codebase?", "c": "simple", "d": "factual"},
    {"q": "What models are mapped to which branches in config.py?", "c": "simple", "d": "factual"},
    {"q": "What is the eval benchmark approach for this router?", "c": "simple", "d": "factual"},
    {"q": "Describe the current classifier logic in router.py.", "c": "simple", "d": "factual"},
    {"q": "What are the routing branches in this system?", "c": "simple", "d": "factual"},
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
        complexity = r["label"]["complexity"]
        domain = r["label"]["domain"]
        if complexity == "verify":
            complexity = "simple"
        if domain == "project":
            domain = "factual"
        examples.append(format_example(
            query=r["question"],
            complexity=complexity,
            domain=domain,
        ))
    return examples


def main():
    root = Path(__file__).parent
    eval_path = root.parent / "backend" / "eval_results.json"
    out_dir = root / "data"
    out_dir.mkdir(exist_ok=True)

    real = load_eval_examples(str(eval_path))
    print(f"Real examples from eval: {len(real)}")

    synthetic = [format_example(s["q"], s["c"], s["d"]) for s in SYNTHETIC]
    print(f"Synthetic examples: {len(synthetic)}")

    all_examples = real + synthetic
    random.seed(42)
    random.shuffle(all_examples)

    split = int(len(all_examples) * 0.8)
    train = all_examples[:split]
    val = all_examples[split:]

    json.dump(train, open(out_dir / "train.json", "w"), indent=2)
    json.dump(val, open(out_dir / "val.json", "w"), indent=2)

    print(f"Train: {len(train)} | Val: {len(val)}")
    print(f"Saved to {out_dir}/")

    from collections import Counter

    def dist(examples):
        parsed = [json.loads(e["output"]) for e in examples]
        return Counter((p["complexity"], p["domain"]) for p in parsed)

    print("\nTrain distribution:")
    for (complexity, domain), count in sorted(dist(train).items()):
        print(f"  {complexity:8} / {domain:8}: {count}")


if __name__ == "__main__":
    main()
