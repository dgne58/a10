"""
train_llama_code.py

Fine-tunes Llama-3.1-8B-Instruct on Code Alpaca using Unsloth + LoRA.
Run this on the H200 after prepare_code_alpaca.py.

Prerequisites (H200):
    pip install unsloth datasets trl transformers accelerate peft

Run:
    python train_llama_code.py

Outputs:
    training/models/llama-8b-code/         (LoRA adapter)
    training/models/llama-8b-code-merged/  (merged, ready for vLLM)
"""

import json
from pathlib import Path

BASE_MODEL   = "meta-llama/Llama-3.1-8B-Instruct"
DATA_DIR     = Path(__file__).parent / "data"
OUT_ADAPTER  = Path(__file__).parent / "models" / "llama-8b-code"
OUT_MERGED   = Path(__file__).parent / "models" / "llama-8b-code-merged"

MAX_SEQ_LEN  = 1024
LORA_RANK    = 16
LORA_ALPHA   = 32
LORA_DROPOUT = 0.05
BATCH_SIZE   = 2
GRAD_ACCUM   = 8
EPOCHS       = 3
LR           = 2e-4


def load_dataset_from_json(path: Path):
    from datasets import Dataset
    data = json.load(open(path))
    return Dataset.from_list(data)


def format_prompt(row: dict) -> dict:
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
    from unsloth import FastLanguageModel
    from trl import SFTTrainer, SFTConfig

    print(f"[train] Loading {BASE_MODEL} ...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=BASE_MODEL,
        max_seq_length=MAX_SEQ_LEN,
        dtype=None,
        load_in_4bit=False,
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

    train_ds = load_dataset_from_json(DATA_DIR / "code_alpaca_train.json")
    val_ds   = load_dataset_from_json(DATA_DIR / "code_alpaca_val.json")

    train_ds = train_ds.map(format_prompt)
    val_ds   = val_ds.map(format_prompt)

    OUT_ADAPTER.mkdir(parents=True, exist_ok=True)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        dataset_text_field="text",
        args=SFTConfig(
            output_dir=str(OUT_ADAPTER),
            per_device_train_batch_size=BATCH_SIZE,
            gradient_accumulation_steps=GRAD_ACCUM,
            num_train_epochs=EPOCHS,
            learning_rate=LR,
            fp16=False,
            bf16=True,
            logging_steps=20,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            max_seq_length=MAX_SEQ_LEN,
            report_to="none",
        ),
    )

    print("[train] Starting training ...")
    trainer.train()

    print(f"[train] Saving adapter to {OUT_ADAPTER} ...")
    model.save_pretrained(str(OUT_ADAPTER))
    tokenizer.save_pretrained(str(OUT_ADAPTER))

    print(f"[train] Merging and saving to {OUT_MERGED} ...")
    OUT_MERGED.mkdir(parents=True, exist_ok=True)
    model.save_pretrained_merged(str(OUT_MERGED), tokenizer, save_method="merged_16bit")

    print(f"[train] Done. Serve with:")
    print(f"  vllm serve {OUT_MERGED} --host 0.0.0.0 --port 8002 --gpu-memory-utilization 0.45")


if __name__ == "__main__":
    main()
