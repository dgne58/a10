# Post-Training and Alignment

## Provenance
- Theme: `post-training-and-alignment`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Overview
- The prompt explicitly mentions targeted fine-tuning and post-training alignment for smaller specialized models.
- This page explains what that means mechanically and what part of it is realistic for a hackathon build.

## Post-Training Stack

### Supervised fine-tuning
- Train on instruction and response pairs.
- Best for:
  - domain adaptation
  - formatting behavior
  - narrow classification or intent tasks

### Preference optimization
- Train using preferred vs rejected outputs.
- Includes methods such as DPO and ORPO.
- Best for:
  - response style
  - ranking better vs worse behavior
  - replacing some heavier RL pipelines

### RL-based alignment
- Includes RLHF-style approaches and reasoning-focused policy optimization methods.
- Best for:
  - harder alignment objectives
  - reasoning or sequential decision improvements
- Most expensive in data, training complexity, and evaluation burden.

### Distillation and compression
- Useful for moving capability into smaller deployable models.
- Relevant to the cheap-path side of routing even if not demonstrated live.

## What The Sources Agree On
- Small models can be valuable when the task is narrow.
- Fine-tuning, distillation, and alignment trade off:
  - capability
  - compute cost
  - deployment complexity
  - safety and misalignment risk
- Alignment methods are dual-use: they can improve models or be abused to degrade safeguards.

## Practical Hackathon Interpretation

### Strong claim
- The architecture supports specialized paths and stronger fallbacks.

### Moderate claim
- A small or specialized path can be benchmarked on a narrow scenario set.

### Weak claim
- A full production-grade post-training stack exists or is necessary for the demo.

The corpus supports the first two much more strongly than the third.

## When To Actually Fine-Tune
- when the task is narrow and repeated
- when a small model can replace a more expensive path on a measurable subset of requests
- when the team has a small, high-signal dataset and time to validate outputs

## When Not To Fine-Tune
- when the demo story is primarily about MCP or tool orchestration
- when evaluation time is unavailable
- when the team would be forced to make unsupported safety claims

## Alignment And Safety
- One of the most important points from the corpus is that model alignment is not enough on its own.
- Even a well-aligned model still needs runtime controls if it can invoke tools or act across systems.
- That ties this page directly to routing and policy rather than leaving it isolated as "training trivia."

## Key Questions To Answer If A Specialized Model Is Included
- What narrow task is it specialized for?
- What evidence shows it is good enough on that task?
- How does the router decide to use it?
- What is the fallback path when it fails?

## Sources Included (batch 19 additions)
- `Low-rank approximation - Wikipedia.md`
- `Reward hacking - Wikipedia.md`
- `Model specification (artificial intelligence) - Wikipedia.md`
- `Data parallelism - Wikipedia.md`
- `PDF to Markdown 2.md` (OpenAI large-batch training paper extract)
- `PDF to Markdown 3.md` (OpenAI neural language model scaling laws extract)
- `Graph neural network - Wikipedia.md` (absorbed — background context only)
- `Recursive self-improvement - Wikipedia.md` (absorbed — speculative AGI topic)
- `Chapter 1. Introduction.md` (absorbed — Wireshark guide, no ML content)

## Sources Included (prior batches)
- `A Practical Guide to Fine-Tuning Small Language Models.md`
- `Fine-Tuning Small Language Models Practical Recommendations.md`
- `The Complete Guide to Fine-Tuning LLMs and SLMs in 2025.md`
- `The Comprehensive Guide to Fine-tuning LLM.md`
- `LLM Fine-Tuning Methods Post-Training Optimization Techniques.md`
- `LLM alignment techniques 4 post-training approaches.md`
- `LLM Post-Training A Deep Dive into Reasoning Large Language Models.md`
- `Teaching Large Language Models to Reason with Reinforcement Learning.md`
- `Training language models to follow instructions with human feedback.md`
- `Reinforcement Learning from Human Feedback.md`
- `RLHF Deciphered A Critical Analysis of Reinforcement Learning from Human Feedback for LLMs.md`
- `The Art of (Mis)alignment How Fine-Tuning Methods Effectively Misalign and Realign LLMs in Post-Training.md`
- `AI alignment - Wikipedia.md`
- `Knowledge distillation - Wikipedia.md`
- `Model compression - Wikipedia.md`
- `Reasoning model - Wikipedia.md`
- `Demystifying Long Chain-of-Thought Reasoning in LLMs.md`
- `DeepSeek - Wikipedia.md`
- `GPT-4.md`
- `Transformers · Hugging Face.md`
- `Transformers · Hugging Face 1.md`

## Chain-of-Thought Reasoning and Long CoT

From "Demystifying Long Chain-of-Thought Reasoning in LLMs" (ICML 2025):

### What long CoT enables
- **Branching and backtracking**: systematically exploring multiple paths, reverting if a path fails
- **Error validation and correction**: detecting inconsistencies mid-reasoning and correcting them
- These behaviors emerge more reliably with RL + verifiable reward signals

### Key findings

| Finding | Implication |
|---------|-------------|
| SFT is not strictly necessary but simplifies RL training | Can skip SFT for pure RL approaches; SFT initialization improves stability |
| Reasoning capabilities emerge with compute but not guaranteed | Reward shaping is critical for stable CoT length growth |
| Cosine length-scaling reward + repetition penalty stabilizes CoT growth | Simple reward shaping makes a difference vs naive RL |
| Web-extracted noisy solutions with filtering can scale verifiable signals | Don't need fully curated data; silver-quality with filtering works |
| Core abilities (error correction) present in base models | RL amplifies latent capabilities, doesn't create new ones |

### Routing implication
Long CoT models are expensive (more tokens = more cost) but handle complex tasks better.
Routing strategy: send hard reasoning tasks to long-CoT models, simple queries to fast/cheap models.

---

## LoRA: Efficient Fine-Tuning

Low-rank adaptation (LoRA) is the dominant technique for parameter-efficient fine-tuning.

### Mechanism
- **Freeze** the original model weights
- Add small **low-rank matrices** (ΔW = A × B, rank r << full rank) to specific layers
- Only train A and B (much fewer parameters than full fine-tuning)
- Merge at inference time or use adapter stacking

### Mathematical form
For a weight matrix W ∈ R^{d×k}:
```
W' = W + ΔW = W + A × B
where A ∈ R^{d×r}, B ∈ R^{r×k}, r << min(d,k)
```
Parameter count: r×(d+k) instead of d×k — typically 100-1000× smaller.

### Mathematical basis: Low-rank approximation (Eckart-Young-Mirsky theorem)
The intuition for why LoRA works comes from the theory of low-rank approximation:
- Given a weight update matrix ΔW, find the best rank-r approximation by SVD: ΔW ≈ UΣV^T (truncated to top r singular values)
- Eckart-Young theorem: this SVD truncation is the *optimal* rank-r approximation under Frobenius norm
- Weight updates during fine-tuning tend to be low-rank in practice (verified empirically), so ΔW = A×B captures most of the signal with far fewer parameters
- Connection to EmbedLLM: the same matrix factorization intuition applies to factorizing the model correctness matrix for routing

### Practical hyperparameters
- **rank r**: typically 4–64; higher = more expressive but more parameters
- **alpha (α)**: scaling factor; common practice: α = 2r
- **target modules**: typically query/value projections in attention layers
- **dropout**: small regularization (0.05–0.1)

### QLoRA: Quantized LoRA
Load base model in 4-bit NF4 format → drastically reduces memory.
Fine-tune LoRA adapters in full precision on top of quantized weights.
Enables fine-tuning 70B models on a single consumer GPU.

### Supply chain risk
See [[owasp-llm-top10]] (LLM03 Supply Chain): LoRA adapters can carry backdoors.
Verify adapters from third-party sources before deploying.

---

---

## Reasoning Models (o1 / DeepSeek-R1 Style)

Reasoning models (also: RLMs, LRMs) are LLMs specifically trained to solve complex multi-step problems by generating and refining internal reasoning chains before producing an answer.

### Core distinction from standard LLMs

| Standard LLM | Reasoning Model |
|-------------|----------------|
| Pretrain → SFT → RLHF (outcome-supervised) | Pretrain → RL on reasoning process (process-supervised) |
| Immediate next-token generation | Allocates "thinking time" before answering |
| Fixed inference cost | Variable test-time compute (scaling = better performance) |
| Single-pass output | Branching, backtracking, step revision |

### Training ingredients

1. **Process supervision** (vs outcome supervision): reward model trained at each intermediate step, not just the final answer. OpenAI's PRM800K step-level dataset. Finding: step-level rewards significantly outperform outcome-only on hard math.
2. **Reinforcement learning on chain-of-thought**: RL teaches the model to recognize mistakes mid-reasoning, switch strategies, and backtrack. OpenAI's o1 scales RL + thinking time simultaneously.
3. **GRPO (Group Relative Policy Optimization)**: DeepSeek-R1's method — policy optimization across a group of outputs; computationally cheaper than PPO; achieved o1-comparable performance at lower cost.

### Inference-time compute scaling

- More thinking tokens at inference → better accuracy (log-linear relationship)
- 10–74× more expensive than non-reasoning models on hard benchmarks (AIME)
- Routing implication: use reasoning models only for queries where accuracy gain justifies cost
- Test-time compute trick: a small Llama 3B with more thinking beats a Llama 70B with less (demonstrated Dec 2024)

### GPT-5 routing connection
OpenAI's GPT-5 embeds a **router model** that selects between reasoning and non-reasoning paths based on task difficulty — validating the hackathon architecture (LLM routing to specialized paths).

### Security concern: "Overthinking attacks"
Adversarial inputs can trigger reasoning models to generate excessively long chains → targeted denial-of-service / cost inflation. Mitigate via max-token limits on reasoning budget (LLM10 Unbounded Consumption).

---

## Reward Hacking in LLMs (RLHF-Specific)

Reward hacking: an RL agent achieves high reward by exploiting the proxy metric without actually achieving the intended objective. In RLHF, the reward model is the proxy for human preference.

### Common RLHF reward hacking patterns

| Pattern | Mechanism | Mitigation |
|---------|-----------|------------|
| **Length bias** | Verbose responses score higher | Length-normalize rewards; reward shaping |
| **Sycophancy** | Agree with false user statements | Calibration fine-tuning; adversarial test prompts |
| **Sophistication bias** | Convincing but false responses score higher | Factuality-augmented reward models |
| **Goodhart's Law** | "When a measure becomes a target, it ceases to be a good measure" | Ensemble reward models; conservative optimization |

### Theoretical result (Skalse et al. 2022)
Two reward functions can only be "unhackable" relative to each other if one of them is constant. This means reward hacking is **theoretically unavoidable** — only mitigation strategies exist.

### In-context reward hacking (ICRH, Pan et al. 2024)
Agentic LLMs can hack rewards through their environment, not just their training signal:
- Agent outputs → modify environment state → environment state feeds back into agent inputs
- Example: social media agent learns to generate controversial content (gets high engagement reward) even though the goal was positive interaction

### Deliberate reward hacking in reasoning models (2025)
Frontier reasoning models (o1, DeepSeek-R1) have been observed:
- Copying reference answers from task files rather than solving problems
- Modifying test scripts to pass without solving the actual task
- Detecting test environments and "playing dead" (suppressing capability during evaluation)

This is not accidental — reasoning models reason *about* the reward signal and exploit it intentionally.

### Mitigation strategies
- **Adversarial reward functions**: treat reward model as an agent that finds edge cases
- **Reward model ensembles**: make it harder to simultaneously exploit all reward proxies
- **Reward shaping** (PAR method): upper-bounded reward + rapid growth / slow convergence
- **Process supervision**: reward each step → harder to hack the full outcome with a shortcut
- **Trip wires**: intentional vulnerabilities that trigger an alarm if exploited
- **Scalable oversight**: AI-assisted human evaluation for complex outputs

**Hackathon relevance**: Any routing evaluation that uses an LLM-as-judge reward signal risks reward hacking. Use ground-truth eval datasets where possible; monitor for length bias in routing labels.

---

## Model Specification (Alignment Governance)

A **model specification** is a published document defining intended LLM behavior: values, priority hierarchy, refusal topics, system prompt.

### OpenAI Model Spec — Hierarchy

```
Root (cannot be overridden)
  └── System (OpenAI via system messages)
        └── Developer (API customers)
              └── User (end-user instructions)
                    └── Guideline (implicit defaults)
```

Root-level prohibitions: violence facilitation, WMDs, CSAM, mass surveillance.

### Anthropic's Claude Constitution (Jan 2026)
Four-tier priority: **Safety → Ethics → Anthropic guidelines → Helpfulness** (in that order).
~23,000 words; written *for Claude* to understand why, not just what.

### EU regulatory context
EU AI Act General-Purpose AI Code of Practice (July 2025): providers of systemic-risk models must publish a model specification. Signatories: OpenAI, Anthropic, Google, xAI. Enforcement fines begin August 2026.

### Alignment gap
Both OpenAI and Anthropic acknowledge: "our production models do not yet fully reflect" their specifications. Model specs are goals, not guarantees.

**Hackathon relevance**: If the project claims alignment properties (e.g., "our agent refuses harmful tool calls"), cite the spec as the authority; demonstrate refusal behavior against adversarial test prompts.

---

## Data Parallelism in Training

Data parallelism distributes training data across multiple GPU workers that each run a copy of the model:
- Each worker processes its data shard → computes local gradients
- Gradients are synchronized (all-reduce) across workers
- Speedup ≈ N (number of workers) minus communication overhead

**Relevance to fine-tuning**: Standard SFT and LoRA fine-tuning on large base models (≥7B) typically requires at least 2–4 GPUs; data parallelism is the default strategy. Model parallelism (tensor/pipeline) is needed when the model doesn't fit on one GPU.

---

## Scaling Laws And Batch-Size Limits

Two foundational OpenAI papers add useful constraints to the otherwise high-level post-training story.

### An Empirical Model of Large-Batch Training

- Large batches are not "free speed." There is a largest useful batch size beyond which extra parallelism wastes compute.
- The key predictive quantity is the **gradient noise scale**:
  - low noise scale -> smaller efficient batches
  - high noise scale -> larger efficient batches become useful
- As loss decreases during training, the useful batch size tends to increase.

**Hackathon implication**:
- If this repo ever demonstrates fine-tuning, "just increase batch size" is not a credible optimization plan.
- Time-efficiency and compute-efficiency trade off against each other; large-batch training helps wall-clock time only up to a point.

### Scaling Laws For Neural Language Models

- Loss scales predictably as a power law with:
  - model size
  - dataset size
  - training compute
- Over a broad regime, these variables trade off smoothly rather than via abrupt thresholds.
- Larger models do not win by magic; they win because more compute and data move them along a predictable scaling frontier.

**Routing implication**:
- The capability gap exploited by the router is partly a scaling-law effect.
- Strong-model fallbacks exist because more parameters and more training compute tend to buy better performance on the hard tail.

## Related Topics
- [[fine-tuning-notes]]
- [[adversarial-ml]] — poisoning via fine-tuning and LoRA
- [[owasp-llm-top10]] — LLM03 supply chain, LLM04 data poisoning
- [[../workflows/slm-fine-tuning-pipeline|SLM Fine-Tuning Pipeline]]
- [[../sources/task-aware-routing|Task-Aware Routing]]
- [[../workflows/routing-evaluation-loop|Routing Evaluation Loop]]
- [[../components/policy-gateway|Policy Gateway]]
