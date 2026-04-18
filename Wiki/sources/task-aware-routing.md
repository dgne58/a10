# Task-Aware Routing

## Provenance
- Theme: `task-aware-routing`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Overview
- This is the most direct match for the first half of the hackathon prompt.
- The corpus strongly supports routing as a quality, cost, latency, and risk optimization layer rather than a simple provider switch.
- The most important shift is conceptual: routing is not "which model do I like," but "which path is sufficient for this request."

## Core Problem
- Models differ by:
  - quality
  - cost
  - latency
  - modality support
  - domain specialization
- Queries also differ by:
  - difficulty
  - external-action needs
  - safety or approval risk
  - whether the answer already exists in the local wiki

Routing is therefore a decision problem over both the request and the available capability set.

## What Routing Assumes About LLMs

- LLMs are transformer-based deep-learning systems trained on large corpora and then adapted with fine-tuning, prompting, or post-training alignment.
- Their usefulness comes from broad transfer, not deterministic correctness.
- Their failure modes matter to routing:
  - hallucination
  - context sensitivity
  - variable latency and token cost
  - non-uniform capability across domains

That is why routing exists in the first place. If all models had identical cost, latency, and reliability, routing would collapse into a fixed default.

## Branch Types That Matter In Practice

The source set becomes much more coherent once routing is framed as path selection over six branch families:

| Branch | Typical trigger | Main advantage | Main risk |
| --- | --- | --- | --- |
| Wiki answer | local answerability is high | lowest cost and latency | stale or incomplete wiki |
| Cheap general model | simple summarization or transformation | low cost | underperformance on hard queries |
| Specialized model | narrow, repeated domain task | strong fit per dollar | brittle outside domain |
| Function tool | deterministic internal action | high reliability and testability | limited scope |
| MCP path | external context or externalized capability required | reusable integrations | auth and availability complexity |
| Strong general model | hard reasoning or ambiguous tasks | best quality ceiling | expensive and slower |

This branch taxonomy is more durable than naming providers because vendors and serving stacks can change while the branch logic remains valid.

## Routing Dimensions

| Dimension | Why it matters |
| --- | --- |
| Task type | code, analysis, classification, retrieval, tool use, multimodal |
| Difficulty | strong model may only be needed for the hard tail |
| Domain | specialized models and heuristics often work best in narrow domains |
| Modality | text-only and multimodal paths differ materially |
| Cost tolerance | some scenarios prefer cheaper paths |
| Latency tolerance | some scenarios prefer fast paths |
| Safety or approval risk | risky actions often need policy checks or stronger control |
| Local answerability | wiki-first can avoid many model calls entirely |

## Main Families Of Routing

### Rules-based routing
- Best baseline for a hackathon.
- Uses explicit conditions over request properties.
- Most transparent and easiest to demo.

### Intent or semantic classification
- Uses a classifier or small model to map query types to path choices.
- Attractive when there is not enough labeled routing data for a learned router.

### Preference-based routing
- Learns from comparisons or preference data between strong and weak paths.
- Strongly supported by RouteLLM-style work.

### Embedding or similarity routing
- Fast and usable under cold-start if a small labeled set exists.

### Online adaptation
- Multi-armed-bandit style methods help when the system must learn while running.
- Powerful conceptually, but more complex to defend in a hackathon unless kept simple.

## Routing Features And Signals

### Request-derived features
- task family
- domain
- prompt length and structure
- modality
- explicit risk markers
- need for external verification

### System-derived features
- wiki coverage
- tool availability
- auth state
- provider latency or cost tier
- whether approval would be required

### Why this distinction matters
- request-derived features say what the user seems to need
- system-derived features say what the platform can safely and cheaply do right now

Ignoring the second category produces routers that look clever on paper but fail in real operation.

## Cold-Start Problem
- Several papers emphasize that deployment often begins before domain-specific routing data exists.
- That makes cold-start a first-class design problem.

Mitigations from the corpus:
- rules-based baseline
- intent classification
- few-shot similarity routing
- synthetic data generation using task profiles or taxonomies

## Routing Beyond Model Choice

The corpus plus this project's structure suggest that routing should often decide among:
- answer from wiki
- use cheap or specialized model
- invoke tools or MCP surfaces
- escalate to stronger model

This is more useful than framing routing as only "small model vs large model."

## Practical Hackathon Policy

```text
1. If the answer already exists in the wiki, answer locally.
2. If the task is narrow, low-risk, and easy, use a cheaper or specialized path.
3. If the task requires external action or verification, use a tool or MCP path.
4. Otherwise, use the stronger general path.
```

That policy is simple enough to explain and strong enough to benchmark.

## Evaluation Strategy

Routing should be evaluated at the branch level, not just at the model-output level.

### Useful scenario families
- wiki-answerable architectural question
- narrow-domain transformation
- tool-required verification
- high-risk action requiring approval
- hard reasoning case that justifies escalation

### Metrics to compare
- quality or correctness
- latency
- estimated cost
- number of strong-model calls
- number of approvals required
- success rate under degraded capability conditions

### Important baseline
- "always use the strongest model" is the minimum comparison baseline.
- For tool-heavy workflows, a second useful baseline is "always use the tool path."

## What A Good Routing Trace Should Contain
- task category
- selected path
- rationale
- whether external action was required
- fallback availability
- estimated cost tier
- whether policy pressure affected the decision
- whether capability constraints ruled out alternative branches

## Constraints And Limitations
- overly opaque routing is hard to justify
- a router without evaluation looks arbitrary
- too many live dependencies make routing hard to test
- a "smart" router that does not consider tool availability is brittle
- generic "AI" explanations do not help unless they sharpen a concrete routing decision

## Sources Included
- `RouteLLM Learning to Route LLMs with Preference Data.md`
- `Task-Aware LLM Routing with Multi-Level Task-Profile-Guided Data Synthesis for Cold-Start Scenarios.md`
- `LLM Router Blueprint by NVIDIA.md`
- `LLM routing for quality, low-cost responses.md`
- `LLM Semantic Router Intelligent request routing for large language models.md`
- `Bringing intelligent, efficient routing to open source AI with vLLM Semantic Router.md`
- `Meet LLMRouter An Intelligent Routing System designed to Optimize LLM Inference by Dynamically Selecting the most Suitable Model for Each Query.md`
- `MetaLLM A High-performant and Cost-efficient Dynamic Framework for Wrapping LLMs.md`
- `Multi-Model Routing Choosing the Best LLM per Task.md`
- `Not-Diamondawesome-ai-model-routing A curated list of awesome approaches to AI model routing.md`
- `pulzeai-ossknn-router.md`
- `Overview — NVIDIA NeMo Framework User Guide.md`
- `Overview — TensorRT LLM.md`
- `Welcome to TensorRT LLM’s Documentation! — TensorRT LLM.md`
- `ai-dynamodynamo A Datacenter Scale Distributed Inference Serving Framework.md`
- `What is an LLM (large language model).md` (background absorbed into routing assumptions)
- `What is artificial intelligence (AI).md` (background absorbed into routing assumptions)

## Related Topics
- [[routing-papers]]
- [[../workflows/request-execution-lifecycle|Request Execution Lifecycle]]
- [[../workflows/llm-routing-approaches|LLM Routing Approaches]]
- [[../workflows/routing-evaluation-loop|Routing Evaluation Loop]]
- [[../components/router|Router]]
- [[../data-models/routed-request|Routed Request]]
- [[mcp-agentic-workflows]]
