# Training Environments

This folder now uses two separate Python environments.

## Why split them

The router classifier has two distinct runtime surfaces:

1. Training
   Files:
   - `prepare_dataset.py`
   - `train.py`

   Stack:
   - PyTorch
   - Unsloth
   - TRL
   - PEFT
   - Transformers

2. Serving
   Files:
   - `serve.py`
   - `integrate.py`

   Stack:
   - vLLM
   - FastAPI
   - Uvicorn
   - Pydantic
   - Transformers

These stacks should not share one pip environment by default because:

- Unsloth and vLLM have different binary expectations.
- Mixing them causes pip resolver backtracking.
- FlashAttention is optional for this classifier and should not block first-pass setup.

## Environment layout

### `requirements-train.txt`

Use this env to:
- build the dataset
- fine-tune the classifier

Install:

```bash
pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements-train.txt
```

### `requirements-serve.txt`

Use this env to:
- serve the merged model locally with vLLM
- expose `POST /classify`
- connect the backend router to the trained classifier

Install:

```bash
pip install -r requirements-serve.txt
```

## Suggested shell layout

```bash
python -m venv .venv-train
source .venv-train/bin/activate
pip install --upgrade pip
pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements-train.txt
```

```bash
python -m venv .venv-serve
source .venv-serve/bin/activate
pip install --upgrade pip
pip install -r requirements-serve.txt
```

## What this changes operationally

- Training failures no longer drag in `vllm`.
- Serving installs no longer drag in `unsloth`.
- You can debug data prep and LoRA training independently from model serving.
- First-pass setup on the H200 MIG slice becomes smaller and more predictable.

## Legacy file

`requirements.txt` now points to `requirements-train.txt` only.
It is kept as a compatibility shim for older instructions, not as the preferred install path.
