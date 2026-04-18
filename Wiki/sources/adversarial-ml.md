---
tags: [security, adversarial-ml, attacks, mitre, nist, sources]
last_updated: 2026-04-15
---

# Adversarial Machine Learning

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Clippings/Adversarial Machine Learning.md` (NIST AI 100-2e, January 2024)
- `Clippings/advmlthreatmatrixpagesadversarial-ml-101.md at master.md`
- `Clippings/advmlthreatmatrixpagesadversarial-ml-101.md at master 1.md`
- `Clippings/advmlthreatmatrixpagesadversarial-ml-threat-matrix.md at master.md`
- `Clippings/advmlthreatmatrixpagesadversarial-ml-threat-matrix.md at master 1.md`
- `Clippings/Adversarial Attacks and Defences A Survey.md`
- `Clippings/A reading survey on adversarial machine learning Adversarial attacks and their understanding.md`
- `Clippings/Attacks in Adversarial Machine Learning A Systematic Survey from the Life-cycle Perspective.md` (Wu et al., arXiv 2302.09457v2, CUHK)
- `Clippings/How Deep Learning Sees the World A Survey on Adversarial Attacks & Defenses.md` (Costa et al., arXiv 2305.10862, 2023)
- `Clippings/A reading survey on adversarial machine learning Adversarial attacks and their understanding 1.md` (duplicate — absorbed)

---

## What is Adversarial Machine Learning?

Adversarial ML (AML) is the subfield covering intentional subversion of ML systems. Attackers exploit fundamental properties of statistical learning to:
- Force misclassifications (evasion)
- Poison training data (poisoning)
- Steal model behavior (extraction)
- Infer private training data (privacy attacks)

**Key insight**: These vulnerabilities are structural, not bugs. They follow from the way models generalize from finite data using statistical patterns.

---

## Life-Cycle Framework (Wu et al., 2023)

The most unified framework available. AML attacks are organized by where in the ML system life-cycle they occur.

### Five Stages

```
Pre-training → Training → Post-training → Deployment → Inference
     ↓              ↓            ↓              ↓           ↓
 Data poisoning  Backdoor   Weight attack   Bit-flip    Adversarial
 (dataset        injection  via param       (hardware)  examples
  corruption)    (training  modification               Backdoor
                 control)                              activation
```

### Three Attack Paradigms

| Paradigm | Stage(s) | Attack vector | What changes |
|---------|---------|---------------|--------------|
| **Backdoor attack** | Pre-training, Training, Inference | Poisoned samples injected into dataset; trigger activates at inference | Training data / training procedure |
| **Weight attack** | Post-training, Deployment, Inference | Directly modify trained model weights (continuous) or flip bits in memory (discrete) | Model parameters |
| **Adversarial examples** | Inference only | Craft perturbed input at query time; benign model misclassifies | Input sample |

**Key insight from Wu et al.**: all three paradigms share the same three conditions — stealthiness (attack must not be obvious), benign consistency (model behaves normally on clean inputs), and adversarial inconsistency (model misbehaves on adversarial inputs). The paradigms differ only in *which entity is perturbed*: the data, the weights, or the input sample.

### Backdoor Trigger Taxonomy

| Dimension | Variants |
|-----------|----------|
| **Visibility** | Visible (patch/sticker) vs. Invisible (alpha blending, steganography, adversarial perturbation, slight transformation) |
| **Semantics** | Non-semantic (checkerboard, noise) vs. Semantic (object attribute already in image — e.g., "red car with racing stripe") |
| **Scope** | Sample-specific (unique trigger per input) vs. Universal (same trigger for all) |
| **Location** | Patch-based vs. Frequency-domain vs. Transformation-based |

Invisible triggers are harder to detect in dataset audits. Semantic triggers are the stealthiest because the image is not modified — only the label is changed.

---

## NIST AI 100-2e Taxonomy (January 2024)

The authoritative NIST taxonomy organizes AML into two main branches:

### Predictive AI Attacks

#### Attack Classification Axes
| Axis | Dimensions |
|------|-----------|
| **Stage** | Training time vs. inference time |
| **Attacker goal** | Availability (DoS), integrity (misclassification), privacy (data leakage), abuse |
| **Attacker capability** | Modify training data, modify model, control inference inputs, observe outputs |
| **Attacker knowledge** | White-box (full access), grey-box (partial), black-box (query only) |
| **Data modality** | Image, audio, text, tabular, time-series, multimodal |

#### 2.1 Evasion Attacks (Inference Time)
Attacker modifies input at inference time to force a desired (mis)classification.

| Variant | Description |
|---------|-------------|
| **White-box evasion** | Attacker has access to model gradients; uses gradient-based optimization (FGSM, PGD, C&W attacks) |
| **Black-box evasion** | Only query access; use surrogate model or finite differences to estimate gradient |
| **Transferability** | Adversarial examples crafted against surrogate model often transfer to victim model |
| **Physical-domain attacks** | Printed adversarial patterns placed in physical scenes (STOP sign stickers etc.) |

Mitigations: adversarial training, input preprocessing (denoising), certified defenses, ensemble disagreement detection.

#### 2.2 Poisoning Attacks (Training Time)
Attacker injects malicious data into training pipeline.

| Variant | Description |
|---------|-------------|
| **Availability poisoning** | Degrade overall model accuracy |
| **Targeted poisoning** | Misclassify specific target inputs while maintaining accuracy elsewhere |
| **Backdoor / trojan** | Embed trigger that causes specific behavior when present; model appears normal otherwise |
| **Model poisoning** | Directly modify model weights (requires model-level access) |
| **Split-view poisoning** | Different data shown to validator vs. training pipeline |
| **Frontrunning poisoning** | Insert malicious data before validation can catch it |

Mitigations: data provenance tracking, anomaly detection on training data, adversarial robustness testing, federated learning isolation.

#### 2.3 Privacy Attacks (Inference Time)
| Attack | Description |
|--------|-------------|
| **Data reconstruction** | Reconstruct training inputs from model outputs or gradients |
| **Membership inference** | Determine whether specific data was in training set |
| **Model extraction** | Reconstruct functional copy of model via repeated API queries |
| **Property inference** | Infer aggregate properties of training data |

### Generative AI Attacks (LLM-specific)

#### 3.1 AI Supply Chain Attacks
- **Deserialization vulnerability**: Malicious code in `.pkl`/safetensors model files executes on load
- **Poisoning during pre-training**: Manipulate web-scale training data
- **Poisoning during fine-tuning**: LoRA adapters or PEFT checkpoints contain backdoors

#### 3.2 Direct Prompt Injection (inference time)
- Attacker controls the user prompt input
- Goal: data extraction, behavior manipulation, safety bypass
- Mitigations: system prompt constraints, output validation, privilege separation

#### 3.3 Indirect Prompt Injection (inference time)
- Malicious instructions embedded in external content the LLM retrieves
- Most dangerous in agentic/RAG settings where external data is trusted
- Varieties: availability violation (DoS agent), integrity violation (cause wrong action), privacy compromise (exfiltrate data), abuse violation (spam / misuse resources)

---

## MITRE Adversarial ML Threat Matrix

Modeled after ATT&CK Enterprise. Techniques come in two types:
- **Orange**: ML-specific techniques (no equivalent in traditional ATT&CK)
- **White**: General cybersecurity techniques also applicable to ML systems

### Key Tactics (ATT&CK-style columns)

| Tactic | Example Techniques |
|--------|-------------------|
| **Reconnaissance** | ML model discovery, gather training datasets, model replication via API |
| **ML Attack Staging** | Craft adversarial data, develop shadow models |
| **Initial Access** | Exploit public-facing MLaaS API, supply chain compromise |
| **Persistence** | Backdoor in model weights survives retraining |
| **Evasion** | Adversarial examples, encoding obfuscation |
| **Exfiltration** | Model extraction, training data leakage |
| **Impact** | Degrade model performance, biased outputs, system crash |

### ML-Specific Attack Techniques
1. **Model Replication (shadow model)**: Repeated API queries to build a functional equivalent model
2. **Alter pretrained weights**: Modify pretrained weights from public repos to create backdoored model
3. **Trojan attack (backdoor)**: Specific trigger input causes specific malicious output; otherwise normal behavior
4. **Membership inference**: Query model to determine if particular data was in training set
5. **Model extraction via API**: Build shadow model by using victim model as oracle

---

## Key Attack Algorithms (Evasion / Adversarial Examples)

Attacks are classified by **perturbation norm** (how much change is allowed):
- **L0**: minimize the number of pixels changed
- **L2** (Euclidean): minimize total squared change across all pixels
- **L∞**: minimize the maximum change to any single pixel (most dangerous — smallest per-pixel change, spreads across all pixels)

| Algorithm | Type | Norm | Description |
|-----------|------|------|-------------|
| **L-BFGS** | White-box | L2 | First adversarial attack (Szegedy 2014). Optimization-based; high L2 perturbation |
| **FGSM** | White-box | L∞ | Fast Gradient Sign Method. One-step; perturbs in gradient sign direction by ε. Fast but weak |
| **PGD** | White-box | L∞ | Projected Gradient Descent. Multi-step FGSM; strongest standard attack; used for adversarial training |
| **C&W** | White-box | L2/L0/L∞ | Carlini-Wagner. Optimization-based; produces minimal distortion; breaks many defenses |
| **JSM** (Saliency Maps) | White-box | L0 | Uses forward derivatives to find influential pixels; perturbs few pixels |
| **DeepFool** | White-box | L2 | Finds minimal perturbation to cross decision boundary; lower detectability than L-BFGS |
| **AutoAttack** | White-box | L∞ | Ensemble of attacks (APGD-CE, APGD-T, FAB, Square Attack); standard robustness benchmark |
| **Square Attack** | Black-box | L∞ | Query-efficient score-based; no gradient needed |
| **Surrogate/Transfer** | Black-box | Any | Craft on surrogate model; adversarial examples often transfer to victim model |

**Attacker goal × strength matrix**:
- Easiest: Confidence Reduction, White-box
- Hardest: Targeted misclassification, Black-box

---

## Attack Taxonomy: Train-time vs. Inference-time

```
TRAIN TIME                          INFERENCE TIME
──────────                          ──────────────
Data poisoning                      Evasion attacks
Backdoor injection                  Prompt injection (LLMs)
Supply chain compromise             Model extraction
LoRA adapter poisoning              Membership inference
Model weight tampering              Denial of service
                                    Privacy attacks
```

---

## Attacker Knowledge Spectrum

```
Black-box (query only)  →  Grey-box (partial info)  →  White-box (full gradient access)
     ↓                           ↓                              ↓
 Model extraction          Surrogate model                 FGSM/PGD attacks
 API flooding               Transfer attacks              Exact gradient attacks
 Shadow model             Partial architecture           Certified adversarial examples
```

---

## Weight Attacks (Post-training and Deployment)

Weight attacks are distinct from both backdoor attacks (which target training data) and adversarial examples (which target inputs). They target **the trained model itself**, making them especially relevant to deployed ML serving infrastructure.

### Two Sub-types

| Sub-type | Stage | Mechanism | Threat context |
|---------|-------|-----------|---------------|
| **Parameter modification** | Post-training | Attacker with model access modifies weights in continuous space | Insider threat; compromised model registry; HuggingFace download |
| **Bit-flip attack** | Deployment | Attacker uses Rowhammer or similar hardware exploit to flip specific bits in DRAM holding model weights | Hardware-level attack on inference servers |

### Why Weight Attacks Matter for This Project

- A compromised LoRA adapter or fine-tuned SLM hosted on HuggingFace is a weight attack vehicle
- A model downloaded for routing tasks could have critical weights subtly modified
- **Mitigation**: hash-verify model files before loading; sign adapters; use sandboxed inference environments (Firecracker/gVisor)

---

## Defense Landscape

| Defense Category | Mechanism | Limitations |
|-----------------|-----------|-------------|
| **Adversarial training** | Augment training data with adversarial examples | Expensive; doesn't generalize to unseen attack types |
| **Input preprocessing** | Denoise/smooth inputs before inference | Can be bypassed with adaptive attacks |
| **Certified defenses** | Provable robustness within ε-ball (e.g., randomized smoothing) | Lower accuracy; limited to small ε |
| **Ensemble methods** | Multiple models must agree | Expensive; transferable attacks can bypass |
| **Detection** | Identify adversarial inputs by distribution shift | Arms race; adaptive adversaries can evade detectors |
| **Provenance tracking** | Data lineage via ML-BOM | Requires supply chain cooperation |
| **Differential privacy** | Add noise to training to limit memorization | Accuracy cost |

---

## Relevance to This Project

| Threat | Where it applies |
|--------|-----------------|
| Prompt injection (indirect) | RAG pipeline: malicious content in retrieved docs |
| Data poisoning | Fine-tuning SLMs with external datasets |
| Supply chain (LoRA) | Using pretrained adapters from HuggingFace |
| Model extraction | Exposing routing signals or model behavior via API |
| Backdoor in base model | Using any pretrained model as routing or SLM component |

---

## Related
- [[owasp-llm-top10]] — application-level security risks for LLMs (overlapping with AML)
- [[agentic-security-notes]] — runtime security for agentic systems
- [[../components/policy-gateway|Policy Gateway]] — runtime enforcement
- [[../workflows/slm-fine-tuning-pipeline|SLM Fine-Tuning Pipeline]] — training-time risks
- [[security-networking-and-governance]] — broader security context
