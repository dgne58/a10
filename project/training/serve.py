"""
serve.py

Minimal FastAPI server that loads the merged classifier model via vLLM
and exposes a single POST /classify endpoint.

Prerequisites:
    pip install -r requirements.txt
    # Merge must already exist at models/router-classifier-merged/
    # (run train.py first)

Run:
    python serve.py                     # default port 8001
    python serve.py --port 8001

Returns:
    {"complexity": "simple"|"medium"|"hard"|"verify",
     "domain":     "factual"|"math"|"code"|"project"}
"""

import argparse
import json
import re
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams

# ── Config ────────────────────────────────────────────────────────────────────

ROOT       = Path(__file__).parent
MODEL_DIR  = ROOT / "models" / "router-classifier-merged"

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

VALID_COMPLEXITY = {"simple", "medium", "hard", "verify"}
VALID_DOMAIN     = {"factual", "math", "code", "project"}

FALLBACK = {"complexity": "hard", "domain": "factual"}

# ── Model loading ─────────────────────────────────────────────────────────────

print(f"Loading model from {MODEL_DIR} ...")
llm = LLM(
    model=str(MODEL_DIR),
    dtype="bfloat16",
    max_model_len=512,
    gpu_memory_utilization=0.4,   # classifier is small; leave room for other workloads
)

sampling = SamplingParams(
    temperature=0.0,   # deterministic
    max_tokens=32,     # JSON label fits in <20 tokens
)

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="Router Classifier", version="1.0")


class ClassifyRequest(BaseModel):
    query: str


class ClassifyResponse(BaseModel):
    complexity: str
    domain: str


def build_prompt(query: str) -> str:
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    messages = [
        {"role": "system",    "content": SYSTEM_PROMPT},
        {"role": "user",      "content": f"{INSTRUCTION}\n\n{query}"},
    ]
    return tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def parse_output(raw: str) -> dict:
    """Extract JSON from model output; fall back to FALLBACK on parse error."""
    raw = raw.strip()
    # strip markdown code fences if present
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    try:
        parsed = json.loads(raw)
        complexity = parsed.get("complexity", "")
        domain     = parsed.get("domain", "")
        if complexity not in VALID_COMPLEXITY or domain not in VALID_DOMAIN:
            return FALLBACK
        # project domain only valid with verify complexity
        if domain == "project" and complexity != "verify":
            complexity = "verify"
        return {"complexity": complexity, "domain": domain}
    except (json.JSONDecodeError, AttributeError):
        return FALLBACK


@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")

    prompt = build_prompt(req.query)
    outputs = llm.generate([prompt], sampling)
    raw = outputs[0].outputs[0].text
    result = parse_output(raw)
    return ClassifyResponse(**result)


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
