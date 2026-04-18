"""
Download 100 MMLU questions and save to data/mmlu_100.csv.
Usage: python scripts/download_mmlu.py
Requires: pip install datasets
"""
import csv
import os
import sys

try:
    from datasets import load_dataset
except ImportError:
    print("Run: pip install datasets")
    sys.exit(1)

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mmlu_100.csv")

SUBJECTS = {
    "high_school_geography": 20,
    "high_school_us_history": 20,
    "college_biology": 20,
    "college_mathematics": 20,
    "professional_law": 20,
}

rows = []
for subject, n in SUBJECTS.items():
    ds = load_dataset("cais/mmlu", subject, split="test")
    for i, item in enumerate(ds):
        if i >= n:
            break
        rows.append({
            "id": f"{subject}_{i}",
            "subject": subject,
            "question": item["question"],
            "A": item["choices"][0],
            "B": item["choices"][1],
            "C": item["choices"][2],
            "D": item["choices"][3],
            "answer": "ABCD"[item["answer"]],
        })

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "subject", "question", "A", "B", "C", "D", "answer"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} questions to {OUT_PATH}")
