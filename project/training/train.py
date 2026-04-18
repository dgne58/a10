"""
train.py

Fine-tune a small instruct model for query classification (routing labels)
using plain Transformers + PEFT + TRL.

This path is designed for a constrained GPU slice, not a full H200.

Prerequisites:
    pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cu121
    pip install -r requirements-train.txt

Run:
    python train.py

Outputs:
    models/router-classifier/          (LoRA adapter weights)
    models/router-classifier-merged/   (merged model, ready for vLLM)
"""

from pathlib import Path
import json
import os

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

BASE_MODEL = os.getenv("ROUTER_BASE_MODEL", "Qwen/Qwen2-1.5B-Instruct")
MAX_SEQ_LEN = int(os.getenv("ROUTER_MAX_SEQ_LEN", "512"))
LORA_RANK = int(os.getenv("ROUTER_LORA_RANK", "16"))
LORA_ALPHA = int(os.getenv("ROUTER_LORA_ALPHA", "32"))
LORA_DROPOUT = float(os.getenv("ROUTER_LORA_DROPOUT", "0.05"))
BATCH_SIZE = int(os.getenv("ROUTER_BATCH_SIZE", "1"))
GRAD_ACCUM = int(os.getenv("ROUTER_GRAD_ACCUM", "16"))
EPOCHS = int(os.getenv("ROUTER_EPOCHS", "4"))
LR = float(os.getenv("ROUTER_LR", "2e-4"))
WARMUP_RATIO = float(os.getenv("ROUTER_WARMUP_RATIO", "0.05"))

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "models" / "router-classifier"
MERGED_DIR = ROOT / "models" / "router-classifier-merged"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Loading base model...")
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
model.config.use_cache = False
model.gradient_checkpointing_enable()

lora_config = LoraConfig(
    r=LORA_RANK,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

print("Training config:")
print(f"  BASE_MODEL={BASE_MODEL}")
print(f"  MAX_SEQ_LEN={MAX_SEQ_LEN}")
print(f"  LORA_RANK={LORA_RANK}")
print(f"  LORA_ALPHA={LORA_ALPHA}")
print(f"  LORA_DROPOUT={LORA_DROPOUT}")
print(f"  BATCH_SIZE={BATCH_SIZE}")
print(f"  GRAD_ACCUM={GRAD_ACCUM}")
print(f"  EPOCHS={EPOCHS}")
print(f"  LR={LR}")
print(f"  WARMUP_RATIO={WARMUP_RATIO}")


def format_prompt(example: dict) -> dict:
    messages = [
        {"role": "system", "content": example["system"]},
        {"role": "user", "content": f"{example['instruction']}\n\n{example['input']}"},
        {"role": "assistant", "content": example["output"]},
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False,
    )
    return {"text": text}


def load_dataset(path: Path) -> Dataset:
    with open(path, encoding="utf-8") as handle:
        records = json.load(handle)
    ds = Dataset.from_list(records)
    return ds.map(format_prompt, remove_columns=ds.column_names)


print("Loading datasets...")
train_ds = load_dataset(DATA_DIR / "train.json")
val_ds = load_dataset(DATA_DIR / "val.json")
print(f"Train: {len(train_ds)} | Val: {len(val_ds)}")
print("Sample formatted prompt:\n", train_ds[0]["text"][:400])

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    args=SFTConfig(
        output_dir=str(OUTPUT_DIR),
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LEN,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        num_train_epochs=EPOCHS,
        learning_rate=LR,
        warmup_ratio=WARMUP_RATIO,
        lr_scheduler_type="cosine",
        fp16=False,
        bf16=True,
        logging_steps=10,
        evaluation_strategy="no",
        save_strategy="epoch",
        load_best_model_at_end=False,
        report_to="none",
        seed=42,
    ),
)

print("\nStarting training...")
trainer.train()

print(f"\nSaving LoRA adapter to {OUTPUT_DIR}")
model.save_pretrained(str(OUTPUT_DIR))
tokenizer.save_pretrained(str(OUTPUT_DIR))

print(f"\nMerging adapter into base model and saving to {MERGED_DIR}")
MERGED_DIR.mkdir(parents=True, exist_ok=True)
merged_model = model.merge_and_unload()
merged_model.save_pretrained(str(MERGED_DIR), safe_serialization=True)
tokenizer.save_pretrained(str(MERGED_DIR))

print("\nDone. Merged model ready for vLLM serving.")
print(f"  Adapter:  {OUTPUT_DIR}")
print(f"  Merged:   {MERGED_DIR}")
