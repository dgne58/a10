---
tags: [routing, sources, papers]
last_updated: 2026-04-15
---

# Routing Papers

## Provenance
- Theme: `task-aware-routing`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why these matter

These papers define the state-of-the-art in LLM routing and directly inform what we should implement or cite at the hackathon.

---

## RouteLLM (UC Berkeley + Anyscale, arXiv 2406.18665, 2024)

- **Claim**: 2× cost reduction on MMLU/MT-Bench/GSM8K with no quality loss; up to 85% cost reduction.
- **Method**: Train router on human preference data (Chatbot Arena ~80K battles). Binary decision: route to strong or weak model.
- **Formal model**: Router R^α(q): if P(strong wins | q) ≥ α → strong model; else → weak model. Threshold α controls the cost/quality tradeoff.
- **Key insight**: Preference data is a rich signal for query difficulty. Routers trained on GPT-4/Mixtral generalize to Claude 3 Opus/Sonnet and Llama 3.1 70B/8B without retraining.

### Router Variants

| Router | Method | Notes |
|--------|--------|-------|
| `mf` (recommended) | Matrix factorization on preference data | Fastest; 155 req/s; $3.32/1M requests |
| `sw_ranking` | Similarity-weighted Elo (Bradley-Terry BT model) | No training; inference-time similarity search |
| `bert` | BERT classifier fine-tuned on preference data | 69 req/s; strong with data augmentation |
| `causal_llm` | Llama 3 8B instruction-following classifier | 42 req/s; best on math benchmarks |

### Performance (best config: mf + LLM-judge augmentation, MT Bench)
- **CPT(50%)** = 13.4% of queries need strong model to achieve 50% PGR
- **APGR** = 0.802 (60.4% improvement over random baseline)
- **CPT(80%)** = 31.3% (vs 80% for random)

### Key Engineering Details
- Drop-in OpenAI client replacement; also runs as OpenAI-compatible server
- Model string format: `router-mf-0.11593` (router name + threshold)
- Threshold calibration: `python -m routellm.calibrate_threshold --routers mf --strong-model-pct 0.5`
- Data augmentation critical: arena data alone → poor OOD generalization; augmenting with GPT-4-judge labels on 120K open-ended samples → major gains

### Metrics Glossary
- **PGR** (Performance Gap Recovered): `(router_perf - weak_perf) / (strong_perf - weak_perf)`
- **APGR**: area under the call-performance curve (aggregate across all thresholds)
- **CPT(x%)**: minimum % of strong model calls needed to achieve x% PGR

- **Sources**: `Clippings/RouteLLM Learning to Route LLMs with Preference Data 1.md` (paper), `Clippings/lm-sysRouteLLM ... 1.md` (GitHub README)
- [[../workflows/llm-routing-approaches|→ Full synthesis]]

---

## NVIDIA LLM Router Blueprint (2025)

- **Claim**: Production-ready blueprint with Docker deployment, training notebooks, and pre-configured providers.
- **Method**: Two strategies — intent classification (Qwen 1.7B) and auto-routing (CLIP + neural network).
- **Key insight**: Router returns a model *name*, not a proxied response. Decouples routing from inference.
- **Multimodal**: Handles text and image; routes VLMs vs text-only models via CLIP embeddings.
- **Code available**: Complete source, Docker Compose profiles, Gradio demo. GitHub: nvidia/llm-router-blueprint.
- **Source**: `Clippings/LLM Router Blueprint by NVIDIA.md`

---

## Task-Aware LLM Routing (Cold-Start)

- **Problem**: Most routing methods fail early when you have no training data for the specific task distribution.
- **Method**: Multi-Level Task-Profile-Guided Data Synthesis — synthesizes routing training data from task profiles without real preference labels.
- **Key insight**: You can bootstrap a router for a new domain without A/B eval data by generating synthetic preference data conditioned on a task profile.
- **Source**: `Clippings/Task-Aware LLM Routing with Multi-Level Task-Profile-Guided Data Synthesis for Cold-Start Scenarios.md`

---

## Multi-Model Routing (2026 Overview)

- **EquiRouter**: Fairness-aware routing; 17% cost reduction; prevents routing collapse.
- **GreenServ**: MAB-based online routing; no offline calibration; 22% accuracy gain, 31% energy reduction over 16 models.
- **Router-Suggest**: VLM vs text model routing for multi-turn dialog; 2.3–10× speedup.
- **TableDART**: 2.59M-parameter MLP gating for table understanding; +4.02% over SOTA on 7 benchmarks.
- **Source**: `Clippings/Multi-Model Routing Choosing the Best LLM per Task.md`

---

## OptiRoute (Freshworks, 2024)

- **Problem**: Real deployments do not optimize only for quality and cost; user-specific constraints can also include latency and non-functional criteria such as helpfulness, harmlessness, and honesty.
- **Method**: Hybrid routing engine with lightweight task analysis, complexity estimation, hierarchical filtering, and k-nearest-neighbor matching over model metadata.
- **Key idea**: Routing policy should expose both functional constraints and non-functional constraints instead of hiding everything behind one scalar score.
- **Relevance**:
  - strong fit for regulated or enterprise settings
  - supports personalized routing policies instead of one global threshold
  - reinforces the repo thesis that routing is path selection under multiple constraints, not just "cheap vs expensive"

- **Source**: `Clippings/PDF to Markdown.md` (OptiRoute paper extract)

---

## FrugalGPT (Stanford, 2023)

- **Problem**: Commercial LLM APIs have highly heterogeneous pricing; naive use of the strongest model everywhere is often economically unjustifiable.
- **Strategies**:
  - prompt adaptation
  - LLM approximation
  - LLM cascade
- **Claim**: LLM cascades can match a top model with up to 98% lower cost, or beat it at equal cost by combining models conditionally.
- **Key idea**: Routing is not only a classifier. It can be a staged cascade with fallback and re-ranking.
- **Relevance**:
  - gives a cost-first justification for multi-stage routing
  - supports a demo where cheap-path answers are accepted unless uncertainty or quality signals require escalation

- **Source**: `Clippings/PDF to Markdown 4.md` (FrugalGPT paper extract)

---

## vLLM Semantic Router (Iris, 2026)

- **Architecture**: Signal-Decision Plugin Chain — 6 signal types (domain, keyword, embedding, factual, feedback, preference).
- **LoRA multiplexing**: Shared base model + per-task LoRA adapters; avoids separate model per classification task.
- **HaluGate**: 3-stage hallucination detection pipeline integrated with function-calling.
- **Key**: Extensible by adding new signal plugins without architecture changes.
- **Source**: `Clippings/Bringing intelligent, efficient routing to open source AI with vLLM Semantic Router.md`

---

## KNN Router (pulzeai)

- Embedding-based KNN routing; fast inference, no training required.
- Good for cold-start when you have labeled examples but no preference data.
- Source: `Clippings/pulzeai-ossknn-router.md`

---

## EmbedLLM (UC Berkeley, arXiv 2410.02223, 2024)

- **Problem**: Hundreds of thousands of LLMs on HuggingFace; evaluating and routing each independently wastes compute.
- **Key idea**: Learn a compact vector embedding for each LLM via matrix factorization of a correctness matrix. One embedding → usable for routing, benchmarking, and performance forecasting simultaneously.

### How It Works

```
Training data: 112 LLMs × 36,054 questions → correctness matrix Y[i,j] ∈ {0,1}
Encoder: model embedding φ_m(M) ∈ R^d × question embedding φ_q(p) ∈ R^d
Decoder: ψ(v_m ⊙ v_q') → P(model M correctly answers question q)
Training objective: reconstruct correctness matrix via BCE loss
```

The reconstruction objective forces embeddings to capture model capability structure; the decoder then acts as a router — route to the model with highest predicted correctness score.

### Downstream Tasks (all via a single linear layer on top of embeddings)

| Task | Method | Notes |
|------|--------|-------|
| Model routing | argmax correctness score across model pool | Near single-best model accuracy |
| Correctness forecasting | Linear classifier on embeddings | 74% accuracy (vs 71% for KNN) |
| Benchmark accuracy prediction | Linear regression on embeddings | Statistically significant on 7/10 benchmarks |

### Performance
- **Routing speed**: 750 model selections/sec vs <50/sec for causal LLM router — **15× faster**
- **Memory**: <1GB GPU memory for training vs ~40GB for Llama-3-8B router — **60× cheaper**
- **Embedding quality**: Models with similar characteristics (7B, coding, bio/med) cluster in L2 distance space

### Probing Results
- Embeddings capture model family without explicit training on family labels
- MMLU inclusion in training data improves cross-benchmark accuracy prediction significantly
- GPQA (extremely hard benchmark) embedding accuracy degrades when other benchmarks are added — model capability on hard tasks does not transfer from easy-task embeddings

### Connection to RouteLLM
The `mf` router in RouteLLM uses the same matrix factorization approach independently. EmbedLLM generalizes this to a full evaluation framework: train once, apply embeddings to routing + forecasting + benchmarking.

- **Source**: `Clippings/EmbedLLM Learning Compact Representations of Large Language Models.md`

---

## GPT-2: Language Models are Unsupervised Multitask Learners (Radford et al., OpenAI, 2019)

This is the foundational paper establishing that large-scale language model pretraining enables zero-shot task transfer — without task-specific supervision.

- **Claim**: "Language models begin to learn [NLP tasks] without any explicit supervision when trained on a new dataset of millions of webpages (WebText)."
- **Model**: GPT-2, 1.5B parameter Transformer
- **Dataset**: WebText — ~40GB of outbound Reddit links (≥3 upvotes), ~8M documents
- **Zero-shot results**: 55 F1 on CoQA (matching 3 of 4 baselines trained on 127K+ examples); SOTA on 7/8 language modeling benchmarks in zero-shot setting
- **Key finding**: Model capacity is essential — performance scales log-linearly with model size across tasks
- **Limitation at publication**: 1.5B GPT-2 still underfits WebText — suggesting more scale would yield more capability

**Why this matters for routing**:
- Established the "pretraining + downstream transfer" paradigm all modern LLMs follow
- Explains why larger models outperform smaller ones on hard queries: they saw more relevant patterns in pretraining
- The quality gap between strong and weak models that routing exploits is rooted in pretraining scale differences

- **Source**: `Clippings/Language Models are Unsupervised Multitask Learners.md`
