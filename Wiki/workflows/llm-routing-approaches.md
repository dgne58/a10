---
tags: [routing, llm, inference, cost-optimization]
sources: [RouteLLM, NVIDIA LLM Router Blueprint, Multi-Model Routing 2026, vLLM Iris]
last_updated: 2026-04-13
---

# LLM Routing Approaches

## Overview
- This page answers: which routing strategy should be implemented, what does each one optimize, and how do the tradeoffs compare?
- It is intentionally more implementation-oriented than [[../sources/task-aware-routing|Task-Aware Routing]].

## Core Problem
- Always sending requests to the strongest model wastes cost and latency.
- Always sending requests to the cheapest model degrades quality on the hard tail.
- A router seeks the cheapest path that still clears the quality bar for the current request.

## Taxonomy

| Approach | Mechanism | Strengths | Weaknesses | Cold-start fit |
| --- | --- | --- | --- | --- |
| Rules-based | explicit conditions over request features | simple, explainable | brittle if overly narrow | strong |
| Intent classification | classify request type, then map to route | cheap, easy to tune | depends on label quality | strong |
| Preference-based | learn strong vs weak decision from comparisons | good quality/cost tradeoff | needs preference data | weak |
| Embedding similarity | compare request to labeled examples | very fast | can drift on new domains | medium |
| Online adaptation | update decisions from live outcomes | adapts over time | harder to debug | medium |
| Signal chain | combine multiple heuristic or model signals | flexible and modular | more moving parts | medium |

## Rules-Based Router

### Mechanism
- use explicit features such as:
  - wiki hit or no wiki hit
  - task type
  - risk level
  - external-action need
  - modality

### Best use
- hackathon baseline
- transparent fallback path
- benchmark baseline against learned or classifier-based routes

## Intent Classification Router

### Mechanism
- classify the request into one of a small set of categories
- map each category to a route

### Best use
- when there is no preference data
- when categories are stable enough to be meaningful

### Caution
- category design matters more than classifier sophistication

## Preference-Based Router

### Mechanism
- learn when the weak path is good enough by training on preference or quality-gap signals

### Best use
- when a stable evaluation set or pairwise comparison set exists

### Why it matters
- this family is what makes routing feel principled rather than heuristic in the literature

## Embedding Similarity Router

### Mechanism
- represent the query as an embedding
- route based on nearest labeled examples or cluster membership

### Best use
- few-shot cold-start
- fast experimental baselines

## Online Or Adaptive Router

### Mechanism
- update policy based on observed outcomes, rewards, or contextual bandit logic

### Best use
- systems that run long enough to learn from their own traffic

### Caution
- hard to explain cleanly in a short demo unless the adaptation story is very constrained

## Signal-Chain Router

### Mechanism
- combine multiple signals:
  - domain
  - keyword
  - embedding
  - factuality or hallucination signal
  - user preference
  - feedback

### Best use
- when one signal is not sufficient
- when modular experimentation matters

## Decision Guide

```text
Need a transparent day-one router?
  -> use rules-based routing

Need a small learned step without preference data?
  -> use intent classification

Have comparison or preference data?
  -> use preference-based routing

Need few-shot cold-start behavior?
  -> use embedding similarity

Need to evolve from live outcomes?
  -> consider online adaptation
```

## Recommended Hackathon Progression
1. Start with rules-based routing.
2. Add intent classification or similarity routing if the baseline is too coarse.
3. Add preference-backed or learned routing only if evaluation data exists and the baseline is already stable.

## Minimal Implementation Shape

```python
def route(request):
    if request["can_answer_from_wiki"]:
        return "wiki"
    if request["needs_external_data"]:
        return "tool_path"
    if request["task_type"] in {"classification", "narrow_domain"}:
        return "cheap_or_specialized"
    return "strong_general"
```

## Evaluation Requirements
- every routing strategy should be compared against at least one baseline
- routing trace should expose why a path was selected
- a clever router without measurable benefit is a liability

## Advanced Approaches: RL-Based and Multi-Round Routing

### Router-R1 (2025, UIUC)

**Key innovation**: Treats routing as a *sequential decision process* (multi-round), not a single one-shot dispatch.

**Mechanism**:
- Router itself is an LLM (Qwen2.5-3B or LLaMA-3.2-3B)
- Alternates between `<think>` (internal reasoning) and `<route>` (model invocation) actions
- Collects responses from pool LLMs, integrates them into evolving context
- Trained via RL (PPO/GRPO) with a composite reward:
  - Format reward: penalize malformed outputs (-1 if violated)
  - Outcome reward: exact-match correctness on task
  - Cost reward: inversely proportional to `model_size × output_tokens`
  - Hierarchical: format gates outcome+cost (broken format zeroes other rewards)

**Reward equation**:
```
r(x,y) = R_format + (1-α)·R_outcome + α·R_cost
```
where α controls performance/cost tradeoff.

**Generalization**: Conditions on simple model descriptors (pricing, latency, example perf) → zero-shot generalization to new models without retraining.

**Results**: Outperforms KNN Router, BERT Router, RouterDC, GraphRouter on 7 QA benchmarks. 14K training samples sufficient.

**Source**: `Clippings/Router-R1 Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning.md`

---

### HybridLLM (Microsoft, 2024)

**Key innovation**: Quality-gap-aware routing between small and large model, with dynamic quality threshold tunable at test time.

**Mechanism**:
- Train a BERT-style encoder (DeBERTa) as router, not a generative LLM
- Router predicts `Pr[H(x) ≥ 0]` where `H(x) = q(S(x)) - q(L(x))` (quality gap)
- Quality metric: BART score (not BLEU; correlates better with human judgment)
- "Easy" queries: those where small model response quality ≈ large model
- Threshold on router score determines fraction routed to small model

**Key insight**: ~20% of queries in general NLP datasets are "easy" (small model within threshold of large model quality). Up to 40% call reduction with <1% quality drop.

**Data transformation trick**: When small model significantly underperforms large model, transform labels from `Pr[H(x)≥0]` to `Pr[H(x)≥-t]` for learned offset `t` — improves router calibration in the wide-gap regime.

**Non-determinism handling**: Sample multiple responses per query during training (not just single response) to model stochastic quality distribution.

**Edge/cloud routing**: Users run small model locally (edge), call cloud API only for hard queries.

**Source**: `Clippings/Hybrid LLM Cost-Efficient and Quality-Aware Query Routing.md`

---

## Decision Guide

```text
Need a transparent day-one router?
  -> use rules-based routing

Need a small learned step without preference data?
  -> use intent classification

Have comparison or preference data?
  -> use preference-based routing

Need few-shot cold-start behavior?
  -> use embedding similarity

Need to evolve from live outcomes?
  -> consider online adaptation

Have RL training infrastructure + want multi-model coordination?
  -> consider Router-R1 approach

Have quality-labeled query pairs + want cost/quality threshold?
  -> HybridLLM approach (BERT-based, DeBERTa encoder)
```

## Recommended Hackathon Progression
1. Start with rules-based routing.
2. Add intent classification or similarity routing if the baseline is too coarse.
3. Add preference-backed or learned routing only if evaluation data exists and the baseline is already stable.
4. Use HybridLLM-style quality-gap approach if per-query quality signals are available.

## Minimal Implementation Shape

```python
def route(request):
    if request["can_answer_from_wiki"]:
        return "wiki"
    if request["needs_external_data"]:
        return "tool_path"
    if request["task_type"] in {"classification", "narrow_domain"}:
        return "cheap_or_specialized"
    return "strong_general"
```

## Evaluation Requirements
- every routing strategy should be compared against at least one baseline
- routing trace should expose why a path was selected
- a clever router without measurable benefit is a liability

## Related Topics
- [[../sources/task-aware-routing|Task-Aware Routing]]
- [[routing-evaluation-loop]]
- [[../components/router|Router]]
- [[../sources/routing-papers|Routing Papers]]
