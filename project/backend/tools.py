import os
import re
import sys
import ast
import json
import operator
import tempfile
import subprocess
import urllib.parse
import urllib.request


def fetch_url(url: str) -> str:
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read(2048).decode("utf-8", errors="replace")
        preview = body[:500].strip()
        return f"GET {url}\nStatus: {status}\nContent-Type: {content_type}\n\n{preview}"
    except Exception as e:
        return f"fetch_url failed for {url!r}: {e}"


def code_exec(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if result.returncode == 0:
            return stdout if stdout else stderr if stderr else "(no output)"
        return f"Error:\n{stderr or stdout}"
    except subprocess.TimeoutExpired:
        return "Error: execution timed out (5s limit)"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def lint_python(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        tmp_path = f.name
    try:
        result = subprocess.run(
            ["pyflakes", tmp_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = (result.stdout + result.stderr).strip()
        if not output:
            return "No issues found."
        return output.replace(tmp_path, "<code>")
    except FileNotFoundError:
        return "Error: pyflakes is not installed. Run: pip install pyflakes"
    except subprocess.TimeoutExpired:
        return "Error: lint timed out (5s limit)"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def regex_test(pattern: str, text: str) -> str:
    try:
        matches = re.findall(pattern, text)
        return str(matches)
    except re.error as e:
        return f"Regex error: {e}"


_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPERATORS:
        return _SAFE_OPERATORS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPERATORS:
        return _SAFE_OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported operation: {ast.dump(node)}")


def calculate(expression: str) -> str:
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _eval_node(tree.body)
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as e:
        return f"Error: {e}"


def execute_tool(name: str, params: dict) -> str:
    if name == "fetch_url":
        return fetch_url(params.get("url", ""))
    if name == "code_exec":
        return code_exec(params.get("code", ""))
    if name == "lint_python":
        return lint_python(params.get("code", ""))
    if name == "regex_test":
        return regex_test(params.get("pattern", ""), params.get("text", ""))
    if name == "calculate":
        return calculate(params.get("expression", ""))
    return f"Unknown tool: {name!r}"


_TEXT_TOOL_NAMES: set[str] = {
    "fetch_url",
    "execute_python",
    "lint_python",
    "regex_test",
    "calculate",
}

TOOL_DEFINITIONS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": (
                "Fetch a URL and return the HTTP status, content-type, and a preview of the response body. "
                "ONLY call this when the user explicitly provides a URL (starting with http:// or https://) "
                "or uses words like 'fetch', 'GET', 'ping', 'curl', or 'check endpoint'. "
                "Do NOT call for general knowledge questions about technologies, organizations, or concepts."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Full URL to fetch, e.g. 'https://api.github.com/users/torvalds'",
                    }
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": (
                "Execute a Python code snippet and return stdout. "
                "Only call this when the user explicitly asks to run, execute, or evaluate code."
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


def dispatch_tool(fn_name: str, fn_args: dict) -> str:
    if fn_name == "fetch_url":
        return fetch_url(fn_args.get("url", ""))
    if fn_name == "execute_python":
        return code_exec(fn_args.get("code", ""))
    if fn_name == "lint_python":
        return lint_python(fn_args.get("code", ""))
    if fn_name == "regex_test":
        return regex_test(fn_args.get("pattern", ""), fn_args.get("text", ""))
    if fn_name == "calculate":
        return calculate(fn_args.get("expression", ""))
    return f"Unknown tool: {fn_name!r}"
