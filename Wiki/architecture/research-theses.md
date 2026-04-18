# Research Theses

## Overview
- Capture the strongest actionable claims supported by the clippings corpus.
- Distinguish implementation-relevant theses from broad background reading.
- Point each thesis toward the page or subsystem that operationalizes it.

## High-Confidence Theses

### 1. Persistent wiki memory is a practical accelerator for coding agents
- Repeated rediscovery is a real cost when sources are numerous and sessions are fragmented.
- The wiki should not be a prose archive. It should be an operational memory layer with narrow, linkable pages.
- This thesis is implemented by:
  - [[../components/knowledge-wiki|Knowledge Wiki]]
  - [[persistent-memory-vs-rag]]
  - [[../workflows/clippings-ingest-workflow|Clippings Ingest Workflow]]

### 2. Routing is the product differentiator, not mere multi-model access
- The routing literature consistently argues that query-level differences matter.
- Strong systems choose the cheapest path that still clears the quality bar.
- This thesis is implemented by:
  - [[../components/router|Router]]
  - [[../sources/task-aware-routing|Task-Aware Routing]]
  - [[../workflows/llm-routing-approaches|LLM Routing Approaches]]

### 3. MCP is a capability layer, not a full agent architecture
- MCP standardizes tool, resource, and prompt surfaces.
- It does not replace orchestration, runtime control, or project memory.
- This thesis is implemented by:
  - [[../components/mcp-control-plane|MCP Control Plane]]
  - [[../components/tool-surfaces|Tool Surfaces]]
  - [[../sources/mcp-agentic-workflows|MCP and Agentic Workflows]]

### 4. Runtime security and identity must be explicit
- Tool invocation, delegated actions, and external access create runtime risk.
- Security belongs in policy and infrastructure layers, not only in prompt instructions.
- This thesis is implemented by:
  - [[../components/policy-gateway|Policy Gateway]]
  - [[../components/envoy-ai-gateway|Envoy AI Gateway]]
  - [[../sources/security-networking-and-governance|Security, Networking, and Governance]]

### 5. Specialized models are useful only when routing and fallback are explicit
- Small models become credible when:
  - the task is narrow
  - evaluation exists
  - a stronger fallback path remains available
- This thesis is implemented by:
  - [[../sources/post-training-and-alignment|Post-Training and Alignment]]
  - [[../workflows/slm-fine-tuning-pipeline|SLM Fine-Tuning Pipeline]]
  - [[../workflows/routing-evaluation-loop|Routing Evaluation Loop]]

### 6. A clear demo beats a sprawling architecture story
- The corpus spans routing, alignment, MCP, security, networking, and implementation tooling.
- A winning hackathon story should compress that breadth into one understandable flow.
- This thesis is implemented by:
  - [[../workflows/demo-flow|Demo Flow]]
  - [[../00-preload/judging-demo-narrative|Judging and Demo Narrative]]
  - [[../00-preload/fallback-plans|Fallback Plans]]

## Medium-Confidence Theses

### 7. Rules-based routing is an acceptable and useful baseline
- It is transparent, fast to build, and easy to benchmark.
- The learned router, if added later, should beat the baseline rather than replace it conceptually.

### 8. The wiki itself can be part of the product story
- The internal engineering benefit is real.
- In a hackathon, it can also be shown as the grounding layer that keeps agents aligned with the evolving system.

### 9. Tool routing may be as important as model routing
- The corpus suggests that many requests differ not only in model difficulty but in whether they require external action at all.
- That means the router should classify "wiki answer vs tool path vs model path," not only "small vs large model."

## Open Questions
- Should the prototype emphasize model routing, tool routing, or a combined decision?
- Is a real fine-tuned SLM necessary, or is a specialized path with a clear placeholder acceptable?
- How much security policy should be live versus narrated?
- Does the demo need a UI, or is a trace-first API sufficient?

## Related Topics
- [[reference-driven-solution-shape]]
- [[persistent-memory-vs-rag]]
- [[../sources/corpus-overview|Corpus Overview]]
