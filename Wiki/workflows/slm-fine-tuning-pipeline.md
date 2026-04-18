---
tags: [fine-tuning, slm, sft, lora, qlora, unsloth, post-training]
sources: [Practical Guide to Fine-Tuning SLMs, LLM Post-Training Survey]
last_updated: 2026-04-13
---

# SLM Fine-Tuning Pipeline

## Overview
- This page captures the concrete mechanics of a narrow, hackathon-feasible SLM tuning path.
- It exists to answer: what would it take to make a specialized cheap path credible?

## When To Use An SLM

| Need | SLM fit |
| --- | --- |
| narrow domain specialization | strong |
| low latency or local inference | strong |
| privacy or on-device constraints | strong |
| broad general-purpose reasoning | weak |

The routing implication is important: SLMs are valuable when they serve a narrow slice well enough to avoid stronger-model cost on that slice.

## Pipeline Structure

```text
choose task
  -> prepare narrow dataset
  -> load base model
  -> apply LoRA or QLoRA
  -> train with supervised fine-tuning
  -> evaluate on held-out scenarios
  -> expose as specialized routing path
```

## Key Components

### Base model
- small instruction-tuned model suitable for the target hardware

### LoRA
- adapter-based update that changes a small subset of weights indirectly through low-rank matrices
- preferred because it avoids full-model retraining

### QLoRA
- quantized variant useful when memory is tight

### Unsloth and trainer stack
- attractive because the clipped material emphasizes easier and faster adaptation for small-model experimentation

## Dataset Design
- the narrower the task, the better
- examples should reflect the exact decision or generation behavior the model will own
- likely best use in this project:
  - routing classification
  - narrow domain explanation
  - security or protocol categorization

## Training Guidance
- keep sequence lengths and batch sizes aligned with hardware reality
- favor quality and consistency of examples over raw dataset size
- validate on held-out scenarios that resemble the final routing slice

## Evaluation
- compare tuned SLM vs generic baseline on the exact narrow tasks it is meant to own
- if it does not outperform or materially reduce cost for that slice, do not route to it

## Connection To Router
- the router should not blindly prefer the SLM
- it should call the SLM only for the narrow domain where the evaluation supports it
- all other cases need either tool or stronger-model fallback

## Failure Modes
- overfitting to a tiny homogeneous dataset
- weak evaluation that overstates the SLM's utility
- routing broad queries into a narrow model
- spending too much of the event on training instead of on the product story

## Related Topics
- [[../sources/post-training-and-alignment|Post-Training and Alignment]]
- [[../sources/fine-tuning-notes|Fine-Tuning Notes]]
- [[../components/router|Router]]
- [[routing-evaluation-loop]]
