import os
import sys
import json
import tempfile
import subprocess
import urllib.parse
import urllib.request


def weather(location: str) -> str:
    try:
        url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]
        feels = current["FeelsLikeC"]
        return f"{location}: {desc}, {temp_c}°C (feels like {feels}°C)"
    except Exception as e:
        return f"Weather unavailable for {location!r}: {e}"


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
    if name == "weather":
        return weather(params.get("location", ""))
    if name == "code_exec":
        return code_exec(params.get("code", ""))
    return f"Unknown tool: {name!r}"
