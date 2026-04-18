"""
prepare_function_calling.py

Creates balanced function-calling training data for the Llama 8B fine-tune.

Uses glaive-function-calling-v2 which contains BOTH:
  - Positive examples: model calls a function
  - Negative examples: tools defined in context but model answers directly

This balance is critical — a dataset with only positive examples trains the
model to always call tools, even for questions it should answer directly.

Outputs:
  data/func_call_train.json
  data/func_call_val.json

These are mixed into train_llama_code.py alongside CodeAlpaca.
"""
import json
import random
from pathlib import Path

OUT_DIR = Path(__file__).parent / "data"

# ── Our tool definitions (match tools.py exactly) ────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": (
                "Get current weather for a location. "
                "Only call this when the user explicitly asks about weather, "
                "temperature, or forecast."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. 'London' or 'New York'",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": (
                "Execute a Python code snippet and return stdout. "
                "Only call this when the user explicitly asks to run, "
                "execute, or evaluate code."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute",
                    }
                },
                "required": ["code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lint_python",
            "description": (
                "Run pyflakes on a Python code snippet and return any warnings or errors. "
                "Only call this when the user asks to lint, check, or find issues in Python code."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to lint with pyflakes",
                    }
                },
                "required": ["code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "regex_test",
            "description": (
                "Apply a regex pattern to a text and return all matches using re.findall. "
                "Only call this when the user provides both a regex pattern and a text to test it against."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regular expression pattern",
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to search within",
                    },
                },
                "required": ["pattern", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Safely evaluate a mathematical expression and return the result. "
                "Supports +, -, *, /, **, %. "
                "Only call this when the user asks to calculate or evaluate a math expression."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate, e.g. '2 ** 10 + 3 * 4'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]

# ── Positive: model calls get_weather ────────────────────────────────────────

WEATHER_EXAMPLES = [
    ("What's the weather in London?",              "London",        "London: Cloudy, 12°C (feels like 10°C)"),
    ("What is the temperature in Tokyo right now?","Tokyo",         "Tokyo: Clear sky, 22°C (feels like 21°C)"),
    ("Is it raining in New York?",                 "New York",      "New York: Light rain, 14°C (feels like 12°C)"),
    ("What's the forecast for Paris today?",       "Paris",         "Paris: Partly cloudy, 18°C (feels like 17°C)"),
    ("How hot is it in Dubai right now?",          "Dubai",         "Dubai: Sunny, 38°C (feels like 42°C)"),
    ("Tell me the current weather in Berlin.",     "Berlin",        "Berlin: Overcast, 9°C (feels like 7°C)"),
    ("What's the weather like in Sydney?",         "Sydney",        "Sydney: Sunny, 25°C (feels like 24°C)"),
    ("Is it cold in Moscow today?",                "Moscow",        "Moscow: Snow, -5°C (feels like -9°C)"),
    ("Weather in Singapore right now?",            "Singapore",     "Singapore: Thunderstorm, 28°C (feels like 34°C)"),
    ("Current temperature in Los Angeles?",        "Los Angeles",   "Los Angeles: Sunny, 24°C (feels like 23°C)"),
    ("What's the weather in Mumbai today?",        "Mumbai",        "Mumbai: Humid, 31°C (feels like 36°C)"),
    ("How is the weather in Toronto?",             "Toronto",       "Toronto: Cloudy, 5°C (feels like 3°C)"),
    ("Is it sunny in Barcelona right now?",        "Barcelona",     "Barcelona: Clear sky, 21°C (feels like 20°C)"),
    ("Weather conditions in Amsterdam today?",     "Amsterdam",     "Amsterdam: Drizzle, 11°C (feels like 9°C)"),
    ("What is the temperature in Seoul?",          "Seoul",         "Seoul: Clear, 15°C (feels like 13°C)"),
]

# ── Positive: model calls execute_python ─────────────────────────────────────

CODE_EXEC_EXAMPLES = [
    ("Run this code: print(2 ** 10)",
     "print(2 ** 10)", "1024"),
    ("Execute this snippet: x = [i**2 for i in range(5)]; print(x)",
     "x = [i**2 for i in range(5)]; print(x)", "[0, 1, 4, 9, 16]"),
    ("Run this Python: import math; print(math.sqrt(144))",
     "import math; print(math.sqrt(144))", "12.0"),
    ("Execute: result = sorted([3,1,4,1,5,9,2,6]); print(result)",
     "result = sorted([3,1,4,1,5,9,2,6]); print(result)", "[1, 1, 2, 3, 4, 5, 6, 9]"),
    ("Run this: print(list(map(lambda x: x*2, [1,2,3])))",
     "print(list(map(lambda x: x*2, [1,2,3])))", "[2, 4, 6]"),
    ("Execute this code: print({k: k**2 for k in range(1,6)})",
     "print({k: k**2 for k in range(1,6)})", "{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}"),
    ("Run this Python: print('hello world'.upper())",
     "print('hello world'.upper())", "HELLO WORLD"),
    ("Execute: print(sum(range(1, 101)))",
     "print(sum(range(1, 101)))", "5050"),
    ("Run this snippet: import json; d={'a':1,'b':2}; print(json.dumps(d))",
     "import json; d={'a':1,'b':2}; print(json.dumps(d))", '{"a": 1, "b": 2}'),
    ("Execute this: for i in range(5): print(i**2)",
     "for i in range(5): print(i**2)", "0\n1\n4\n9\n16"),
    ("Run this code: print(sorted(['banana','apple','cherry']))",
     "print(sorted(['banana','apple','cherry']))", "['apple', 'banana', 'cherry']"),
    ("Execute: print(len('hello world'))",
     "print(len('hello world'))", "11"),
    ("Run this Python: import os; print(os.path.join('a','b','c'))",
     "import os; print(os.path.join('a','b','c'))", "a/b/c"),
    ("Execute this snippet: nums=[1,2,3,4,5]; print(sum(nums)/len(nums))",
     "nums=[1,2,3,4,5]; print(sum(nums)/len(nums))", "3.0"),
    ("Run: print(bin(42), hex(42))",
     "print(bin(42), hex(42))", "0b101010 0x2a"),
]

# ── Positive: model calls lint_python ────────────────────────────────────────

LINT_PYTHON_EXAMPLES = [
    ("Lint this code for me: import os\nx = 1\nprint(y)",
     "import os\nx = 1\nprint(y)",
     "<code>:3: undefined name 'y'"),
    ("Check this Python for issues: import sys\nimport json\nprint('hello')",
     "import sys\nimport json\nprint('hello')",
     "<code>:2: 'json' imported but unused"),
    ("Run pyflakes on: def foo():\n    x = 5\nfoo()",
     "def foo():\n    x = 5\nfoo()",
     "<code>:2: local variable 'x' is assigned to but never used"),
    ("Find any linting errors in: x = [1,2,3]\nfor i in x:\n    pass",
     "x = [1,2,3]\nfor i in x:\n    pass",
     "No issues found."),
    ("Lint this snippet: def add(a, b):\n    return a + b\nresult = add(1, 2)\nprint(result)",
     "def add(a, b):\n    return a + b\nresult = add(1, 2)\nprint(result)",
     "No issues found."),
]

# ── Positive: model calls regex_test ─────────────────────────────────────────

REGEX_TEST_EXAMPLES = [
    ("Test the regex \\d+ against 'there are 42 apples and 7 oranges'",
     r"\d+", "there are 42 apples and 7 oranges",
     "['42', '7']"),
    ("Apply the pattern [A-Z][a-z]+ to 'Hello World this is Python'",
     r"[A-Z][a-z]+", "Hello World this is Python",
     "['Hello', 'World', 'Python']"),
    ("Match all email addresses with \\S+@\\S+ in 'contact alice@example.com or bob@test.org'",
     r"\S+@\S+", "contact alice@example.com or bob@test.org",
     "['alice@example.com', 'bob@test.org']"),
    ("Test pattern (\\w+)=(\\d+) on 'x=10 y=20 z=30'",
     r"(\w+)=(\d+)", "x=10 y=20 z=30",
     "[('x', '10'), ('y', '20'), ('z', '30')]"),
    ("Find all words starting with 'py' using py\\w+ in 'python pyflakes pydantic java ruby'",
     r"py\w+", "python pyflakes pydantic java ruby",
     "['python', 'pyflakes', 'pydantic']"),
]

# ── Positive: model calls calculate ──────────────────────────────────────────

CALCULATE_EXAMPLES = [
    ("Calculate 2 ** 10",                   "2 ** 10",       "1024"),
    ("What is 17 * 13 + 5?",               "17 * 13 + 5",   "226"),
    ("Compute 100 / 4 - 3",                "100 / 4 - 3",   "22.0"),
    ("Evaluate the expression 7 % 3",       "7 % 3",         "1"),
    ("Calculate (2 + 3) ** 2 * 4",         "(2 + 3) ** 2 * 4", "100"),
]

# ── Negative: tools available, model answers directly ────────────────────────

NEGATIVE_EXAMPLES = [
    ("What does enumerate() do in Python?",
     "enumerate() returns an iterator of (index, value) tuples from an iterable. "
     "For example: `for i, v in enumerate(['a','b','c']): print(i, v)` prints `0 a`, `1 b`, `2 c`. "
     "It's commonly used when you need both the index and value in a loop."),
    ("How do I reverse a list in Python?",
     "You can reverse a list three ways: `lst.reverse()` reverses in-place, "
     "`lst[::-1]` returns a new reversed list, and `list(reversed(lst))` also returns a new list. "
     "Use `lst[::-1]` when you want a copy without modifying the original."),
    ("What is a lambda function?",
     "A lambda is a small anonymous function defined with the `lambda` keyword. "
     "Syntax: `lambda args: expression`. Example: `double = lambda x: x * 2`. "
     "Use lambdas for simple one-line functions, especially as arguments to `map`, `filter`, or `sorted`."),
    ("How do I handle exceptions in Python?",
     "Use try/except blocks: `try: risky_code() except ValueError as e: handle(e)`. "
     "Add `finally` for cleanup code that always runs. Use `except Exception` as a catch-all, "
     "but prefer specific exception types. Raise exceptions with `raise ValueError('message')`."),
    ("What is the difference between a list and a tuple in Python?",
     "Lists are mutable (can be changed after creation) and use square brackets `[]`. "
     "Tuples are immutable and use parentheses `()`. Use tuples for fixed data like coordinates "
     "or function return values; use lists when you need to append or modify elements."),
    ("How does async/await work in Python?",
     "async/await enables cooperative concurrency using coroutines. Mark a function `async def` "
     "to make it a coroutine. Use `await` to pause execution until an awaitable completes. "
     "Run coroutines with `asyncio.run(main())`. Best for I/O-bound tasks like network requests."),
    ("What is Big O notation?",
     "Big O notation describes the upper bound on an algorithm's time or space complexity as "
     "input size grows. O(1) is constant, O(log n) is logarithmic, O(n) is linear, O(n²) is "
     "quadratic. Ignore constants: O(2n) simplifies to O(n). Focus on the dominant term."),
    ("How do I implement a binary search in Python?",
     "Binary search works on sorted arrays by repeatedly halving the search space:\n"
     "```python\ndef binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n"
     "    while lo <= hi:\n        mid = (lo + hi) // 2\n"
     "        if arr[mid] == target: return mid\n"
     "        elif arr[mid] < target: lo = mid + 1\n"
     "        else: hi = mid - 1\n    return -1\n```\nTime complexity: O(log n)."),
    ("Explain how Python decorators work.",
     "A decorator is a function that wraps another function to add behavior. "
     "The `@decorator` syntax is shorthand for `func = decorator(func)`. "
     "Example: a timer decorator measures execution time by recording time before and after "
     "calling the wrapped function. Use `functools.wraps` to preserve the original function's metadata."),
    ("What is the difference between deepcopy and copy in Python?",
     "`copy.copy()` creates a shallow copy — a new object, but nested objects are still referenced. "
     "`copy.deepcopy()` creates a deep copy — recursively copies all nested objects. "
     "Use shallow copy for flat structures; use deepcopy when you need full independence from the original."),
    ("How does Python's GIL affect multithreading?",
     "The GIL (Global Interpreter Lock) prevents multiple Python threads from executing bytecode "
     "simultaneously. This means threads don't provide true parallelism for CPU-bound tasks. "
     "For CPU-bound work, use multiprocessing. For I/O-bound work (network, disk), threads are "
     "still useful because the GIL is released during I/O operations."),
    ("What is the difference between REST and GraphQL?",
     "REST uses multiple endpoints (one per resource) with fixed response shapes. "
     "GraphQL uses a single endpoint where clients specify exactly what data they need, "
     "avoiding over-fetching and under-fetching. REST is simpler to cache; GraphQL is more "
     "flexible for complex frontends with varied data needs."),
    ("How do I write a context manager in Python?",
     "Implement `__enter__` and `__exit__` methods, or use `@contextmanager` from contextlib:\n"
     "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef managed_resource():\n"
     "    resource = acquire()\n    try:\n        yield resource\n    finally:\n        release(resource)\n```"),
    ("Explain closures in JavaScript.",
     "A closure is a function that retains access to its outer scope's variables even after "
     "the outer function has returned. Example: a counter factory returns a function that "
     "increments a private count variable. The inner function 'closes over' the count variable, "
     "keeping it alive and private. Closures enable encapsulation and stateful functions."),
    ("What is the difference between SQL INNER JOIN and LEFT JOIN?",
     "INNER JOIN returns only rows where both tables have matching values. "
     "LEFT JOIN returns all rows from the left table plus matching rows from the right; "
     "unmatched right-side columns are NULL. Use LEFT JOIN when you want all records from "
     "the primary table regardless of whether a match exists in the secondary table."),
    ("How does React's useEffect hook work?",
     "useEffect runs side effects after render. The first argument is the effect function; "
     "the second is a dependency array. Empty array `[]` runs once on mount. "
     "With dependencies `[a, b]` it runs when a or b changes. Return a cleanup function "
     "to cancel subscriptions or timers when the component unmounts."),
    ("What is the event loop in Node.js?",
     "Node.js uses a single-threaded event loop with libuv for async I/O. "
     "Phases: timers → I/O callbacks → idle/prepare → I/O poll → setImmediate → close callbacks. "
     "Non-blocking I/O hands off to the OS and registers a callback; the loop processes callbacks "
     "when the operation completes. This enables high concurrency without threads."),
    ("How does database indexing work?",
     "An index is a separate data structure (usually a B-tree) that maps column values to row "
     "locations, allowing lookups in O(log n) instead of a full O(n) scan. "
     "Indexes speed up reads but slow writes slightly (index must be updated). "
     "Index columns used in WHERE clauses, JOINs, and ORDER BY. Avoid indexing low-cardinality columns."),
    ("What is memoization and when should I use it?",
     "Memoization caches the result of expensive function calls and returns the cached result "
     "for the same inputs. Use it for pure functions with repeated identical calls, "
     "like recursive Fibonacci. In Python: `@functools.lru_cache(maxsize=None)`. "
     "Watch for memory growth with large input spaces."),
    ("How do Python generators differ from lists?",
     "Generators produce values lazily on demand using `yield`, consuming O(1) memory regardless "
     "of size. Lists compute all values eagerly and store them in memory. "
     "Use generators for large sequences, infinite streams, or pipelines. "
     "You can only iterate a generator once; lists can be iterated multiple times."),
    ("What are Python type hints and how do I use them?",
     "Type hints annotate function signatures with expected types: `def add(a: int, b: int) -> int`. "
     "They're optional and not enforced at runtime, but tools like mypy and pyright check them "
     "statically. Use `from typing import List, Dict, Optional, Union` for complex types, "
     "or modern syntax `list[int]`, `dict[str, int]` in Python 3.9+."),
    ("Explain the Model-View-Controller pattern.",
     "MVC separates concerns into three layers: Model (data and business logic), "
     "View (presentation and UI), Controller (handles user input and coordinates Model/View). "
     "The Controller receives a request, asks the Model for data, and passes it to the View to render. "
     "This separation makes code easier to test and maintain."),
    ("What is the difference between processes and threads?",
     "Processes are independent OS-level execution units with separate memory spaces. "
     "Threads share a process's memory space and are lighter to create. "
     "Use threads for I/O-bound concurrency (they share data easily). "
     "Use processes for CPU-bound parallelism (true parallel execution on multi-core). "
     "In Python, multiprocessing bypasses the GIL for CPU-bound tasks."),
    ("How does Git rebase differ from merge?",
     "Merge creates a new commit combining two branches, preserving full history including "
     "the branch point. Rebase replays your commits on top of the target branch, "
     "creating a linear history. Use merge for shared/public branches; use rebase to "
     "clean up local commits before merging. Never rebase commits already pushed to shared branches."),
    ("What does pyflakes check for that pylint doesn't?",
     "Pyflakes focuses on logical errors — undefined names, unused imports, redefined variables — "
     "without enforcing style rules. Pylint is broader: it checks style (PEP 8), complexity, "
     "and logic errors. Pyflakes is faster and produces fewer false positives. "
     "Use pyflakes for quick checks; use pylint for comprehensive code quality audits."),
    ("How do I write a regex to match email addresses?",
     "A common email regex is `r'[\\w.+-]+@[\\w-]+\\.[a-zA-Z]+'`. "
     "It matches a local part (word chars, dots, plus, hyphen), an @ sign, a domain, and a TLD. "
     "For production use, prefer a library like `email-validator` — full RFC 5322 compliance "
     "is extremely complex to capture in a single regex."),
    ("What math operations does Python's ast module support safely?",
     "Python's `ast` module lets you parse expressions into a tree without executing them. "
     "By walking the tree yourself, you can allow only safe node types: `ast.Constant` for numbers, "
     "`ast.BinOp` for binary operations (+,-,*,/,**,%), and `ast.UnaryOp` for negation. "
     "Reject everything else to prevent code injection. This is safer than `eval()`."),
    ("When should I use re.match vs re.search vs re.findall?",
     "`re.match()` anchors at the start of the string. "
     "`re.search()` scans for the first match anywhere. "
     "`re.findall()` returns all non-overlapping matches as a list. "
     "Use `findall` when you need every occurrence; use `search` for the first occurrence; "
     "use `match` only when the pattern must start at the beginning of the string."),
    ("Why is eval() dangerous in Python?",
     "`eval()` executes arbitrary Python code, so user-controlled input can run system commands, "
     "read files, or import malicious modules. For math expressions, use `ast.parse()` + a safe "
     "node evaluator instead. For JSON, use `json.loads()`. Never pass untrusted strings to `eval()`."),
    ("What is CORS and how do I fix a CORS error?",
     "CORS (Cross-Origin Resource Sharing) is a browser security policy that blocks "
     "requests from a different origin unless the server explicitly allows it. "
     "Fix it server-side by adding response headers: "
     "`Access-Control-Allow-Origin: *` (or a specific domain). "
     "In Flask use `flask-cors`; in Express use the `cors` middleware."),
]


def make_positive_lint(question: str, code: str, result: str) -> dict:
    tc = {
        "id": "call_lint_001",
        "type": "function",
        "function": {"name": "lint_python", "arguments": json.dumps({"code": code})},
    }
    messages = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": None, "tool_calls": [tc]},
        {"role": "tool", "tool_call_id": "call_lint_001", "content": result},
        {"role": "assistant", "content": f"Pyflakes result:\n\n```\n{result}\n```"},
    ]
    return {"messages": messages, "tools": TOOLS}


def make_positive_regex(question: str, pattern: str, text: str, result: str) -> dict:
    tc = {
        "id": "call_regex_001",
        "type": "function",
        "function": {"name": "regex_test", "arguments": json.dumps({"pattern": pattern, "text": text})},
    }
    messages = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": None, "tool_calls": [tc]},
        {"role": "tool", "tool_call_id": "call_regex_001", "content": result},
        {"role": "assistant", "content": f"The regex `{pattern}` found the following matches: {result}"},
    ]
    return {"messages": messages, "tools": TOOLS}


def make_positive_calculate(question: str, expression: str, result: str) -> dict:
    tc = {
        "id": "call_calc_001",
        "type": "function",
        "function": {"name": "calculate", "arguments": json.dumps({"expression": expression})},
    }
    messages = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": None, "tool_calls": [tc]},
        {"role": "tool", "tool_call_id": "call_calc_001", "content": result},
        {"role": "assistant", "content": f"The result of `{expression}` is **{result}**."},
    ]
    return {"messages": messages, "tools": TOOLS}


def make_positive_weather(question: str, location: str, result: str) -> dict:
    tc = {
        "id": "call_weather_001",
        "type": "function",
        "function": {"name": "get_weather", "arguments": json.dumps({"location": location})},
    }
    messages = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": None, "tool_calls": [tc]},
        {"role": "tool", "tool_call_id": "call_weather_001", "content": result},
        {"role": "assistant", "content": f"Here is the current weather for {location}: {result}"},
    ]
    return {"messages": messages, "tools": TOOLS}


def make_positive_code_exec(question: str, code: str, output: str) -> dict:
    tc = {
        "id": "call_exec_001",
        "type": "function",
        "function": {"name": "execute_python", "arguments": json.dumps({"code": code})},
    }
    messages = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": None, "tool_calls": [tc]},
        {"role": "tool", "tool_call_id": "call_exec_001", "content": output},
        {"role": "assistant", "content": f"The output of the code is:\n\n```\n{output}\n```"},
    ]
    return {"messages": messages, "tools": TOOLS}


def make_negative(question: str, answer: str) -> dict:
    messages = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]
    return {"messages": messages, "tools": TOOLS}


def format_for_sft(example: dict, tokenizer) -> dict:
    msgs = example["messages"]
    tools = example.get("tools")
    try:
        text = tokenizer.apply_chat_template(
            msgs,
            tools=tools,
            tokenize=False,
            add_generation_prompt=False,
        )
    except Exception:
        # Fallback: plain text format if tokenizer doesn't support tools
        parts = []
        for m in msgs:
            role = m["role"]
            content = m.get("content") or ""
            if m.get("tool_calls"):
                tc = m["tool_calls"][0]
                content = f"[TOOL_CALL] {tc['function']['name']}({tc['function']['arguments']})"
            parts.append(f"{role.upper()}: {content}")
        text = "\n".join(parts)
    return {"text": text}


def main():
    positives = (
        [make_positive_weather(q, loc, res) for q, loc, res in WEATHER_EXAMPLES]
        + [make_positive_code_exec(q, code, out) for q, code, out in CODE_EXEC_EXAMPLES]
        + [make_positive_lint(q, code, res) for q, code, res in LINT_PYTHON_EXAMPLES]
        + [make_positive_regex(q, pat, txt, res) for q, pat, txt, res in REGEX_TEST_EXAMPLES]
        + [make_positive_calculate(q, expr, res) for q, expr, res in CALCULATE_EXAMPLES]
    )
    negatives = [make_negative(q, a) for q, a in NEGATIVE_EXAMPLES]

    all_examples = positives + negatives
    random.seed(42)
    random.shuffle(all_examples)

    split = int(len(all_examples) * 0.9)
    train, val = all_examples[:split], all_examples[split:]

    # Try to format with tokenizer if available; else save raw for train_llama_code.py
    try:
        from transformers import AutoTokenizer
        MODEL_DIR = Path(__file__).parent / "models" / "router-classifier-merged"
        llama_dir = Path(__file__).parent / "models" / "llama-8b-code-merged"
        tok_dir = llama_dir if llama_dir.exists() else MODEL_DIR
        tokenizer = AutoTokenizer.from_pretrained(str(tok_dir))
        train = [format_for_sft(e, tokenizer) for e in train]
        val   = [format_for_sft(e, tokenizer) for e in val]
        print("Formatted with tokenizer chat template.")
    except Exception as e:
        print(f"Tokenizer unavailable ({e}), saving raw messages — train_llama_code.py will format.")

    OUT_DIR.mkdir(exist_ok=True)
    json.dump(train, open(OUT_DIR / "func_call_train.json", "w"), indent=2)
    json.dump(val,   open(OUT_DIR / "func_call_val.json",   "w"), indent=2)

    print(f"Positive: {len(positives)}  Negative: {len(negatives)}")
    print(f"Train: {len(train)}  Val: {len(val)}")
    print(f"Saved → {OUT_DIR}/func_call_{{train,val}}.json")


if __name__ == "__main__":
    main()
