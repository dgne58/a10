"""
serve.py

Minimal FastAPI server that loads the merged classifier model via Transformers
and exposes a single POST /classify endpoint.

Prerequisites:
    pip install -r requirements-serve.txt
    # Merge must already exist at models/router-classifier-merged/
    # (run train.py first)

Run:
    python serve.py                     # default port 8001
    python serve.py --port 8001
"""

import argparse
import json
import re
from pathlib import Path

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# ── Config ────────────────────────────────────────────────────────────────────

ROOT      = Path(__file__).parent
MODEL_DIR = ROOT / "models" / "router-classifier-merged"

SYSTEM_PROMPT = (
    "You are a query classifier for an LLM routing system. "
    "Given a user query, output a JSON object with two fields:\n"
    '  "complexity": one of "simple", "medium", "hard", "verify", "tool"\n'
    '  "domain":     one of "factual", "math", "code", "project", "weather", "code_exec"\n\n'
    "Rules:\n"
    '- "tool"    → query asks to execute code or check weather (use domain "code_exec" or "weather")\n'
    '- "verify"  → query asks about this specific project\'s architecture, models, or files\n'
    '- "simple"  → short factual or coding lookup, < 20 words, no reasoning required\n'
    '- "medium"  → requires explanation or multi-step description, 20-40 words\n'
    '- "hard"    → analysis, comparison, derivation, debugging, or architecture design\n'
    '- "code"    → involves programming, debugging, or software implementation\n'
    '- "math"    → involves calculation, equations, or proofs\n'
    '- "factual" → general knowledge not covered by other domains\n'
    '- "project" → only used when complexity is "verify"\n'
    '- "weather" → only used when complexity is "tool"\n'
    '- "code_exec" → only used when complexity is "tool"\n\n'
    "Output only the JSON object, no explanation."
)

INSTRUCTION = "Classify this query for LLM routing. Return only a JSON object."

VALID_COMPLEXITY = {"simple", "medium", "hard", "verify", "tool"}
VALID_DOMAIN     = {"factual", "math", "code", "project", "weather", "code_exec"}

FALLBACK = {"complexity": "hard", "domain": "factual"}

MAX_NEW_TOKENS = 32

# ── Model loading ─────────────────────────────────────────────────────────────

print(f"Loading model from {MODEL_DIR} ...")
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
model = AutoModelForCausalLM.from_pretrained(
    str(MODEL_DIR),
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
model.eval()
print(f"Model loaded on {device}.")

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="Router Classifier", version="1.0")


class ClassifyRequest(BaseModel):
    query: str


class ClassifyResponse(BaseModel):
    complexity: str
    domain: str


def build_prompt(query: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"{INSTRUCTION}\n\n{query}"},
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def parse_output(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    try:
        parsed = json.loads(raw)
        complexity = parsed.get("complexity", "")
        domain     = parsed.get("domain", "")
        if complexity not in VALID_COMPLEXITY or domain not in VALID_DOMAIN:
            return FALLBACK
        if domain == "project" and complexity != "verify":
            complexity = "verify"
        if domain in {"weather", "code_exec"} and complexity != "tool":
            complexity = "tool"
        return {"complexity": complexity, "domain": domain}
    except (json.JSONDecodeError, AttributeError):
        return FALLBACK


@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")

    prompt = build_prompt(req.query)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
    raw = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return ClassifyResponse(**parse_output(raw))


@app.get("/health")
def health():
    return {"status": "ok", "model": str(MODEL_DIR)}


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)
