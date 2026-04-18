---
tags: [serving, inference, dynamo, tensorrt, vllm, nemo, speculative-decoding, quantization, prompt-caching]
sources: [ai-dynamodynamo, TensorRT-LLM, NVIDIA NeMo, vLLM Semantic Router, speculative-decoding-survey, prompt-caching]
last_updated: 2026-04-15
---

# Serving and Inference

## Provenance
- Theme: `task-aware-routing`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Clippings/Overview — TensorRT LLM.md`
- `Clippings/Overview — TensorRT LLM 1.md`
- `Clippings/Welcome to TensorRT LLM's Documentation!.md`
- `Clippings/Quick Start Guide — TensorRT LLM.md`
- `Clippings/Benchmarking Default Performance — TensorRT-LLM.md`
- `Clippings/Using FP8 and FP4 with Transformer Engine.md`
- `Clippings/Unlocking Efficiency in Large Language Model Inference A Comprehensive Survey of Speculative Decoding.md`
- `Clippings/Overview — NVIDIA NeMo Framework User Guide.md`
- `Clippings/Prompt caching.md`

---

## Layer View

```text
request
  -> gateway / policy layer (Envoy AI Gateway)
  -> routing / orchestration layer (Router, Agent)
  -> inference engine (vLLM, TensorRT-LLM, API)
  -> hardware (GPU, CPU, edge device)
```

The key insight: routing and serving are separate concerns. A router decides *which* model to use; a serving engine decides *how* to run it efficiently.

---

## TensorRT-LLM (NVIDIA)

NVIDIA's open-source inference optimization library built on PyTorch.

### Key capabilities
| Feature | Description |
|---------|-------------|
| **In-flight batching** | Dynamic batching: processes context + generation phases together, eliminating wait times |
| **Paged KV cache** | Intelligent block reuse and memory optimization; analogous to OS virtual memory for KV cache |
| **Speculative decoding** | Supports EAGLE, MTP, NGram algorithms |
| **FP8 quantization** | H100 and later GPUs; ~2× throughput, ~0.5× memory vs FP16 |
| **FP4 quantization** | B200 GPUs (Blackwell); further efficiency gain |
| **Chunked prefill** | Splits long context into manageable chunks for efficient processing |
| **LoRA support** | Multi-adapter with HuggingFace and NeMo formats |
| **Multi-GPU/node** | Tensor, pipeline, and expert parallelism |

### Models supported
DeepSeek R1/V3, Llama 3/4, Qwen2/3, Gemma 3, Phi 4, LLaVA-NeXT, FLUX, and many others. Day-0 support for popular models.

### Performance highlights
- DeepSeek R1: world-record inference on Blackwell GPUs
- Llama 4 Maverick: >1000 TPS/user on B200

### Hackathon relevance
- Strong inference story if NVIDIA GPU available
- Reference for quantization tradeoffs when comparing "cheap path" vs "strong path" serving costs
- Overkill if no compatible hardware; use vLLM instead

---

## Speculative Decoding (Survey 2024)

### The core insight
Autoregressive decoding is **memory-bandwidth bound**, not compute-bound. Each step loads all model parameters from HBM to on-chip cache to generate just *one* token — a massive inefficiency.

### How speculative decoding works
```
1. Drafter (small model): generates k candidate tokens quickly
2. Verifier (target LLM): processes all k tokens in parallel
3. Accept: keep tokens that match what target would generate
4. Reject: discard at first mismatch; generate correct token from target
5. Net effect: multiple tokens per round of target model memory access
```

Key property: **lossless** — final output distribution is identical to autoregressive target model.

### Drafter categories
| Drafter type | Description |
|-------------|-------------|
| Small independent model | Separate smaller LLM trained on same data |
| Draft heads (EAGLE, Medusa) | Extra FFN heads atop target model's hidden states |
| Non-autoregressive transformer | Parallel draft of multiple tokens at once |
| NGram lookup | Match recent context against prompt/output for cheap drafts |
| Self-speculative | Target model drafts via internal early-exit |

### Speedup factors
- Acceptance rate of drafts (higher = better)
- Draft generation speed (cheaper = better)
- Degree of parallelism in verification
- Typical reported speedups: 2-5× over autoregressive decoding

### Relevance to routing
Speculative decoding changes the tradeoff between cheap and strong models:
- Small-model draft + large-model verify can be faster than large-model autoregressive
- Hybrid routing can combine speculative decoding on the "strong path" to reduce its latency premium

---

## FP8 and FP4 Quantization

### Purpose
Reduce memory footprint and increase throughput by using lower-precision arithmetic.

### Formats
| Format | Bits | Memory reduction vs FP16 | Supported hardware |
|--------|------|--------------------------|-------------------|
| FP16/BF16 | 16 | baseline | All modern GPUs |
| INT8 | 8 | ~2× | Most GPUs |
| FP8 | 8 | ~2× | H100, Hopper arch |
| FP4 | 4 | ~4× | B200, Blackwell arch |

### FP8 key properties
- Two variants: E4M3 (higher precision) and E5M2 (higher range)
- Hardware acceleration via Transformer Engine on H100+
- Per-tensor or per-channel scaling
- Minimal accuracy loss vs FP16 for most tasks

### FP4 (NVFP4)
- New format introduced with Blackwell architecture
- Enables loading weights in FP4 with automatic kernel selection
- Combines 4-bit weights with FP8 activations in practice

### Routing implication
Quantized models can be part of the "cheap path" even at large parameter counts:
- 70B model at INT4 can be faster/cheaper than 13B at FP16
- Quantization level is a first-class routing dimension alongside model size

---

## Prompt Caching (Claude API)

### Mechanism
Cache KV state for a prefix of the prompt; on repeated requests that share that prefix, skip recomputation.

```
Request 1: process full prompt → cache prefix KV state (5min or 1hr TTL)
Request 2: same prefix → load cached KV → only process new tokens
```

### Configuration
- **Automatic caching**: single `cache_control` field at request root; system auto-manages cache breakpoint
- **Explicit breakpoints**: `cache_control` on specific content blocks for fine-grained control

```python
# Automatic caching
{
    "cache_control": {"type": "ephemeral"},  # 5-min TTL
    "system": "...",
    "messages": [...]
}
```

### Pricing (Claude Opus 4.6)
| Operation | Price per MTok |
|-----------|---------------|
| Base input | $5.00 |
| 5-min cache write | $6.25 (25% premium) |
| 1-hr cache write | $10.00 |
| Cache hit / refresh | $0.50 (90% discount) |
| Output | $25.00 |

### Use cases
- Long system prompts reused across many requests (routing instructions, wiki context)
- Multi-turn conversations (growing message history cached automatically)
- RAG workflows with stable context windows

### Routing implication
Prompt caching fundamentally changes cost model for repeated-context queries:
- First call: expensive (write cost slightly above base)
- Subsequent calls: 90% cheaper on the cached portion
- Wiki preload + cached system prompt = very cheap repeated queries
- Cache TTL (5 min / 1 hr) needs to match request cadence

---

## vLLM

Strong open-source inference server.

**Key features**:
- PagedAttention for memory-efficient KV cache
- Continuous batching (like TRT-LLM in-flight batching)
- OpenAI-compatible API endpoint
- LoRA adapter support
- Semantic router integration (see [[task-aware-routing]])
- Supports speculative decoding

**Hackathon relevance**: Best option for local/self-hosted model path. Can sit behind router as the "cheap path" endpoint.

---

## Dynamo (NVIDIA)

Distributed inference orchestration layer above inference engines.

**Key features**:
- Coordinates across multi-GPU/multi-node setups
- Disaggregated prefill and decode (different hardware for prefill vs decode)
- KV-aware routing: route requests to nodes that already have relevant KV cache

**Hackathon relevance**: Reference architecture — overkill for single-machine hackathon builds.

---

## NeMo Framework

NVIDIA's framework for training and customizing LLMs.

**Key features**:
- SFT, RLHF, DPO pipelines
- Multimodal model training
- NeMo-Guardrails integration for safety

**Hackathon relevance**: Supports the story that specialized models can be fine-tuned and served. Reference for SLM fine-tuning pipeline.

---

## Key Tradeoff Table

| Dimension | Cheap path | Strong path |
|-----------|-----------|-------------|
| Model size | 3B–13B parameters | 70B+ or proprietary |
| Quantization | INT4/FP4 | FP16/BF16 |
| Serving | vLLM locally | Cloud API |
| Latency | Low (fast model) | Higher (big model) |
| Cost | Very low | High per token |
| Quality | Good for easy tasks | Required for hard tasks |
| Speculative decoding | Drafter role | Verifier role |
| Prompt caching | High ROI (many queries) | High ROI (expensive base) |

---

## Related
- [[task-aware-routing]] — routing approaches and model selection
- [[../components/router|Router]] — routing component design
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — gateway layer above serving
- [[../workflows/slm-fine-tuning-pipeline|SLM Fine-Tuning Pipeline]] — training side
- [[../workflows/llm-routing-approaches|LLM Routing Approaches]] — when to use each serving path
