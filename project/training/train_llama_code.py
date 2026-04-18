"""
train_llama_code.py

Fine-tunes Llama-3.1-8B-Instruct on Code Alpaca + function-calling data
using standard transformers + peft + trl (no Unsloth required).

Prerequisites (H200):
    pip install datasets trl transformers accelerate peft torch

Run:
    python train_llama_code.py

Outputs:
    training/models/llama-8b-code/         (LoRA adapter)
    training/models/llama-8b-code-merged/  (merged, ready for vLLM)
"""

import json
from pathlib import Path

import torch
from datasets import Dataset, concatenate_datasets
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig

BASE_MODEL   = "NousResearch/Meta-Llama-3.1-8B-Instruct"
DATA_DIR     = Path(__file__).parent / "data"
OUT_ADAPTER  = Path(__file__).parent / "models" / "llama-8b-code"
OUT_MERGED   = Path(__file__).parent / "models" / "llama-8b-code-merged"

MAX_SEQ_LEN  = 256
LORA_RANK    = 16
LORA_ALPHA   = 32
LORA_DROPOUT = 0.05
BATCH_SIZE   = 1
GRAD_ACCUM   = 16
EPOCHS       = 3
LR           = 2e-4


def load_dataset_from_json(path: Path) -> Dataset:
    data = json.load(open(path))
    return Dataset.from_list(data)


def format_prompt(row: dict, tokenizer) -> dict:
    # Pre-formatted rows already have "text"
    if row.get("text") is not None:
        return {"text": row["text"]}
    # Function-calling rows have "messages" + optional "tools"
    if "messages" in row:
        try:
            text = tokenizer.apply_chat_template(
                row["messages"],
                tools=row.get("tools"),
                tokenize=False,
                add_generation_prompt=False,
            )
            return {"text": text}
        except Exception:
            pass
    # CodeAlpaca format
    instruction = row["instruction"]
    inp = row.get("input", "").strip()
    system = row.get("system", "You are an expert software engineer.")
    user_content = f"{instruction}\n{inp}".strip() if inp else instruction
    text = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system}<|eot_id|>\n"
        f"<|start_header_id|>user<|end_header_id|>\n"
        f"{user_content}<|eot_id|>\n"
        f"<|start_header_id|>assistant<|end_header_id|>\n"
        f"{row['output']}<|eot_id|>"
    )
    return {"text": text}


def main() -> None:
    print(f"[train] Loading tokenizer from {BASE_MODEL} ...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    print(f"[train] Loading model (QLoRA 4-bit) ...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map={"": 0},
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)
    # prepare_model_for_kbit_training upcasts embeddings to float32 (~1GB extra).
    # Cast them back to bfloat16 to stay within the MIG memory budget.
    for module in model.modules():
        if hasattr(module, "weight") and module.weight is not None and module.weight.dtype == torch.float32:
            if module.weight.shape[0] > 10000:  # only large embedding tables
                module.weight.data = module.weight.data.to(torch.bfloat16)
    model.enable_input_require_grads()

    lora_config = LoraConfig(
        r=LORA_RANK,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ── Load datasets ─────────────────────────────────────────────────────────
    train_code = load_dataset_from_json(DATA_DIR / "code_alpaca_train.json")
    val_code   = load_dataset_from_json(DATA_DIR / "code_alpaca_val.json")

    fc_train_path = DATA_DIR / "func_call_train.json"
    fc_val_path   = DATA_DIR / "func_call_val.json"
    if fc_train_path.exists() and fc_val_path.exists():
        train_fc = load_dataset_from_json(fc_train_path)
        val_fc   = load_dataset_from_json(fc_val_path)
        print(f"[train] Mixing CodeAlpaca ({len(train_code)}) + func_call ({len(train_fc)}) ...")
        train_ds = concatenate_datasets([train_code, train_fc]).shuffle(seed=42)
        val_ds   = concatenate_datasets([val_code,   val_fc])
    else:
        print("[train] func_call data not found — run prepare_function_calling.py first.")
        train_ds = train_code
        val_ds   = val_code

    fmt = lambda row: format_prompt(row, tokenizer)
    train_ds = train_ds.map(fmt, remove_columns=train_ds.column_names)
    val_ds   = val_ds.map(fmt, remove_columns=val_ds.column_names)

    OUT_ADAPTER.mkdir(parents=True, exist_ok=True)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        dataset_text_field="text",
        args=SFTConfig(
            output_dir=str(OUT_ADAPTER),
            max_seq_length=MAX_SEQ_LEN,
            per_device_train_batch_size=BATCH_SIZE,
            gradient_accumulation_steps=GRAD_ACCUM,
            num_train_epochs=EPOCHS,
            learning_rate=LR,
            warmup_ratio=0.05,
            lr_scheduler_type="cosine",
            fp16=False,
            bf16=True,
            gradient_checkpointing=True,
            gradient_checkpointing_kwargs={"use_reentrant": False},
            logging_steps=20,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            report_to="none",
            seed=42,
        ),
    )

    print("[train] Starting training ...")
    trainer.train()

    print(f"[train] Saving adapter → {OUT_ADAPTER}")
    model.save_pretrained(str(OUT_ADAPTER))
    tokenizer.save_pretrained(str(OUT_ADAPTER))

    # ── Merge LoRA into base weights for vLLM ─────────────────────────────────
    print(f"[train] Merging LoRA into base weights → {OUT_MERGED}")
    OUT_MERGED.mkdir(parents=True, exist_ok=True)
    merged = model.merge_and_unload()
    merged.save_pretrained(str(OUT_MERGED), safe_serialization=True)
    tokenizer.save_pretrained(str(OUT_MERGED))

    print("[train] Done. Serve with:")
    print(f"  vllm serve {OUT_MERGED} --host 0.0.0.0 --port 8002 --gpu-memory-utilization 0.45")


if __name__ == "__main__":
    main()
