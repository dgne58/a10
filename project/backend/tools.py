import os
import sys
import json
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
            return stdout if stdout else "(no output)"
        return f"Error (exit {result.returncode}):\n{stderr}"
    except subprocess.TimeoutExpired:
        return "Error: execution timed out (5s limit)"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def execute_tool(name: str, params: dict) -> str:
    if name == "fetch_url":
        return fetch_url(params.get("url", ""))
    if name == "code_exec":
        return code_exec(params.get("code", ""))
    return f"Unknown tool: {name!r}"


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
]


def dispatch_tool(fn_name: str, fn_args: dict) -> str:
    if fn_name == "fetch_url":
        return fetch_url(fn_args.get("url", ""))
    if fn_name == "execute_python":
        return code_exec(fn_args.get("code", ""))
    return f"Unknown tool: {fn_name!r}"
