"""
train.py

Fine-tune Llama 3.1 8B Instruct for query classification (routing labels).
Uses Unsloth for fast LoRA training on H200.

Prerequisites:
    pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cu121
    pip install -r requirements-train.txt
    huggingface-cli login     # accept Meta license at hf.co/meta-llama

Run:
    python train.py

Outputs:
    models/router-classifier/   (LoRA adapter weights)
    models/router-classifier-merged/  (merged model, ready for vLLM)
"""

import json
import torch
from pathlib import Path
from datasets import Dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

# ── Config ────────────────────────────────────────────────────────────────────

BASE_MODEL   = "unsloth/Meta-Llama-3.1-8B-Instruct"
MAX_SEQ_LEN  = 512
LORA_RANK    = 16
LORA_ALPHA   = 32
LORA_DROPOUT = 0.05
BATCH_SIZE   = 4
GRAD_ACCUM   = 4          # effective batch = 16
EPOCHS       = 4
LR           = 2e-4
WARMUP_RATIO = 0.05

ROOT        = Path(__file__).parent
DATA_DIR    = ROOT / "data"
OUTPUT_DIR  = ROOT / "models" / "router-classifier"
MERGED_DIR  = ROOT / "models" / "router-classifier-merged"

# ── Load model + tokenizer ────────────────────────────────────────────────────

print("Loading base model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=BASE_MODEL,
    max_seq_length=MAX_SEQ_LEN,
    dtype=torch.bfloat16,
    load_in_4bit=False,      # H200 has 141GB — no need to quantize
)

model = FastLanguageModel.get_peft_model(
    model,
    r=LORA_RANK,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)

print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")

# ── Format dataset ────────────────────────────────────────────────────────────

def format_prompt(example: dict) -> dict:
    """Convert Alpaca-style record to chat template string."""
    messages = [
        {"role": "system",    "content": example["system"]},
        {"role": "user",      "content": f"{example['instruction']}\n\n{example['input']}"},
        {"role": "assistant", "content": example["output"]},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    return {"text": text}


def load_dataset(path: Path) -> Dataset:
    records = json.load(open(path))
    ds = Dataset.from_list(records)
    return ds.map(format_prompt, remove_columns=ds.column_names)


print("Loading datasets...")
train_ds = load_dataset(DATA_DIR / "train.json")
val_ds   = load_dataset(DATA_DIR / "val.json")
print(f"Train: {len(train_ds)} | Val: {len(val_ds)}")
print("Sample formatted prompt:\n", train_ds[0]["text"][:400])

# ── Trainer ───────────────────────────────────────────────────────────────────

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    args=SFTConfig(
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
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        output_dir=str(OUTPUT_DIR),
        report_to="none",
        seed=42,
    ),
)

print("\nStarting training...")
trainer.train()

# ── Save adapter ──────────────────────────────────────────────────────────────

print(f"\nSaving LoRA adapter to {OUTPUT_DIR}")
model.save_pretrained(str(OUTPUT_DIR))
tokenizer.save_pretrained(str(OUTPUT_DIR))

# ── Merge + save for vLLM ────────────────────────────────────────────────────

print(f"\nMerging adapter into base model and saving to {MERGED_DIR}")
MERGED_DIR.mkdir(parents=True, exist_ok=True)
model.save_pretrained_merged(str(MERGED_DIR), tokenizer, save_method="merged_16bit")

print("\nDone. Merged model ready for vLLM serving.")
print(f"  Adapter:  {OUTPUT_DIR}")
print(f"  Merged:   {MERGED_DIR}")
