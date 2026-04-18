---
tags: [fine-tuning, sft, dpo, rlhf, alignment, sources]
last_updated: 2026-04-13
---

# Fine-Tuning Notes

## Provenance
- Theme: `post-training-and-alignment`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why These Matter

These sources define the post-training strategies for adapting smaller models to domain-specific tasks. They are relevant to the "specialized model" side of the hackathon prompt.

## Practical Takeaways

From the small-model tuning material:
- narrow-domain specialization is plausible without a giant dataset
- parameter-efficient approaches such as LoRA and QLoRA are attractive for limited hardware
- data quality and task fit matter more than broad volume for a demo

## Alignment Method Ladder

| Method | Mechanism | Relative complexity | Good for |
| --- | --- | --- | --- |
| SFT | train on instruction and response pairs | low | domain adaptation, format compliance |
| DPO | optimize on preferred vs rejected pairs | medium | preference alignment without full RL stack |
| RLHF | preferences plus reward optimization | high | stronger alignment at higher operational cost |
| ORPO and related variants | combine supervised and preference-style signals | medium | experiments beyond plain SFT |

## Hackathon Interpretation

The safest stance for the project is:
- SFT or PEFT is enough if you truly train something
- a specialized path with a stronger fallback is already a solid story
- post-training should support the routing design, not consume the whole event

## Practical Recommendation

If the team chooses to train:
- keep the target task narrow
- keep the dataset small but high-signal
- measure whether the specialized path beats a generic baseline on a fixed scenario set

If the team does not train:
- keep this as architectural support material rather than an implemented claim

## Risks And Caveats

- This area becomes expensive quickly in time and compute.
- Safety and alignment claims are weak if the system lacks runtime controls.
- Do not imply a training pipeline exists unless it actually exists in the repo or demo.

## Related

- [[post-training-and-alignment]]
- [[../workflows/slm-fine-tuning-pipeline|SLM Fine-Tuning Pipeline]]
- [[../sources/task-aware-routing|Task-Aware Routing]]
