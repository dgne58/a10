# Wiki Index

## Preload
- [[00-preload/hot|Hot]]: current execution state, priorities, and immediate next steps.
- [[00-preload/project-map|Project Map]]: high-level system layout and how major parts fit together.
- [[00-preload/file-map|File Map]]: important files and directories to inspect first.
- [[00-preload/commands|Commands]]: build, run, test, and other operational commands.
- [[00-preload/api-routes-and-schemas|API Routes and Schemas]]: endpoint inventory and contract summaries.
- [[00-preload/data-contracts|Data Contracts]]: core request, response, event, and storage shapes.
- [[00-preload/known-bugs-and-assumptions|Known Bugs and Assumptions]]: active risks, stubs, and fragile areas.
- [[00-preload/fallback-plans|Fallback Plans]]: backup execution paths for failures during the hackathon.
- [[00-preload/judging-demo-narrative|Judging and Demo Narrative]]: concise demo arc and value framing.
- [[00-preload/allowed-tools|Allowed Tools]]: approved tools, MCP servers, and usage rules.

## Architecture
- [[architecture/decision-log|Decision Log]]: major architecture and tooling choices.
- [[architecture/dependency-map|Dependency Map]]: key internal and external dependencies.
- [[architecture/hackathon-scope|Hackathon Scope]]: target problem framing and scope boundaries.
- [[architecture/persistent-memory-vs-rag|Persistent Memory vs RAG]]: why the wiki layer exists and how it differs from query-time chunk retrieval.
- [[architecture/reference-driven-solution-shape|Reference-Driven Solution Shape]]: proposed system architecture derived from the clippings corpus.
- [[architecture/research-theses|Research Theses]]: the strongest design claims supported by the source set.

## Components
- [[components/README|Components Hub]]: component pages and conventions.
- [[components/knowledge-wiki|Knowledge Wiki]]: search order, hot.md protocol, query/ingest workflows, page structure.
- [[components/router|Router]]: branch taxonomy, decision heuristics, trace signals, and handoff contract to execution.
- [[components/orchestrator|Orchestrator]]: loop responsibilities, execution state, verification, fallback, and write-back guidance.
- [[components/mcp-control-plane|MCP Control Plane]]: server inventory, capability bundles, auth lifecycle, function vs MCP boundary, failure recovery.
- [[components/policy-gateway|Policy Gateway]]: runtime security layers, trust zones, delegated identity, DLP, approvals, and enforcement points.
- [[components/envoy-ai-gateway|Envoy AI Gateway]]: unified LLM routing, MCP security, multi-provider gateway.
- [[components/tool-surfaces|Tool Surfaces]]: function tools, MCP tools, resources, prompts, and model-provider boundaries.

## Data Models
- [[data-models/README|Data Models Hub]]: data model pages and conventions.
- [[data-models/routed-request|Routed Request]]: request shape used for task-aware routing decisions.
- [[data-models/tool-invocation|Tool Invocation]]: normalized structure for tool and MCP calls.
- [[data-models/evaluation-record|Evaluation Record]]: outcome capture for routing quality and demo evidence.
- [[data-models/knowledge-artifact|Knowledge Artifact]]: wiki page and ingest metadata shape.

## Workflows
- [[workflows/README|Workflows Hub]]: agentic flows, routing flows, and execution sequences.
- [[workflows/clippings-ingest-workflow|Clippings Ingest Workflow]]: how raw sources become persistent wiki knowledge.
- [[workflows/hackathon-build-loop|Hackathon Build Loop]]: implementation loop for Codex and Claude during the event.
- [[workflows/raw-source-verification|Raw Source Verification]]: when and how to reopen raw clipping files for exact details.
- [[workflows/request-execution-lifecycle|Request Execution Lifecycle]]: canonical end-to-end request flow from intake and routing through execution, policy, trace capture, and write-back.
- [[workflows/demo-flow|Demo Flow]]: live demo sequence, traces, and fallback branches.
- [[workflows/llm-routing-approaches|LLM Routing Approaches]]: RouteLLM, NVIDIA Blueprint, GreenServ, Iris, Router-R1 (RL multi-round), HybridLLM (quality-gap-aware); when/how to use each.
- [[workflows/mcp-agentic-patterns|MCP Agentic Patterns]]: primitives, agentic loop, workflow patterns, mcp-agent quickstart.
- [[workflows/routing-evaluation-loop|Routing Evaluation Loop]]: compare routed behavior against baselines and store evidence.
- [[workflows/slm-fine-tuning-pipeline|SLM Fine-Tuning Pipeline]]: LoRA + QLoRA + Unsloth; data format; hyperparameters.

## Sources
- [[sources/README|Sources Hub]]: external references that informed the wiki.
- [[sources/clipping-registry|Clipping Registry]]: provenance map from raw clipping files to synthesized wiki pages.
- [[sources/clipping-inventory|Clipping Inventory]]: exhaustive inventory of all files currently present in `Clippings/`.
- [[sources/clipping-intake-queue|Clipping Intake Queue]]: new or weakly integrated clipping files awaiting deeper synthesis.
- [[sources/corpus-overview|Corpus Overview]]: topic map of the `Clippings/` library.
- [[sources/mcp-agentic-workflows|MCP and Agentic Workflows]]: extended sources about MCP, function calling, and agent patterns.
- [[sources/task-aware-routing|Task-Aware Routing]]: extended sources about model routing, selection, and serving.
- [[sources/post-training-and-alignment|Post-Training and Alignment]]: extended sources about SLM tuning, RLHF, and reasoning tradeoffs.
- [[sources/security-networking-and-governance|Security, Networking, and Governance]]: sources about gateways, identity, delegated authority, DLP, and runtime controls.
- [[sources/app-stack-and-delivery|App Stack and Delivery]]: sources about APIs, frontend, TypeScript, CI/CD, packaging, and deployment models.
- [[sources/protocols-and-observability|Protocols and Observability]]: sources about transport protocols, routing layers, and inspection tooling.
- [[sources/datasets-and-evaluation|Datasets and Evaluation]]: sources about datasets, Zeek, and possible evaluation material.

## Secondary Deep Dives
- [[sources/mcp-overview|MCP Source Overview]]: Introducing MCP, Agentic Workflows, mcp-agent framework, platform engineering patterns.
- [[sources/routing-papers|Routing Papers]]: RouteLLM, NVIDIA Blueprint, Multi-Model Routing, vLLM Iris, KNN Router.
- [[sources/fine-tuning-notes|Fine-Tuning Notes]]: practical SLM notes, alignment methods, post-training survey.
- [[sources/agentic-security-notes|Agentic Security Notes]]: runtime security layers, A2AS framework, dynamic credentials.
- [[sources/serving-and-inference|Serving and Inference]]: TensorRT-LLM, speculative decoding, FP8/FP4 quantization, prompt caching, vLLM, Dynamo, NeMo; cheap-path vs strong-path tradeoffs.
- [[sources/post-training-and-alignment|Post-Training and Alignment]]: SFT, DPO, RLHF, LoRA/QLoRA, long CoT, scaling laws, batch-size limits, distillation; when to fine-tune.
- [[sources/owasp-llm-top10|OWASP LLM Top 10 (2025)]]: LLM01–LLM10 risks, defenses, and agentic system threat/control mapping.
- [[sources/owasp-web-top10|OWASP Web Top 10 (2021)]]: A01–A10 classic web risks; cross-reference table to LLM Top 10; agentic/Flask checklist.
- [[sources/owasp-cheat-sheets|OWASP Cheat Sheets — Developer Reference]]: XSS encoding by context, injection defenses, DB security, attack surface analysis, security terminology.
- [[sources/network-attacks|Network Attacks — DDoS and DNS]]: DDoS types by OSI layer (L7/L3-L4/volumetric), DNS attack taxonomy, DNSSEC, DNS privacy (DoT/DoH), Cloudflare DDoS architecture.
- [[sources/linkerd-notes|Linkerd and Istio — Service Mesh Internals]]: Linkerd architecture (control/data plane, Rust proxy), circuit breaking (failure accrual + probation), rate limiting, retries; Istio VirtualService/DestinationRule/Gateway; HTTPRoute/GRPCRoute.
- [[sources/adversarial-ml|Adversarial ML]]: NIST AI 100-2e taxonomy; MITRE AML threat matrix; train-time vs inference-time attacks.
- [[sources/openai-agents-sdk|OpenAI Agents SDK]]: Agent primitives, handoffs, guardrails, function calling, MCP integration, security considerations.
- [[sources/rag-and-knowledge-retrieval|RAG and Knowledge Retrieval]]: Lewis et al. RAG formulation, DPR, embeddings, vector databases, ANN algorithms, RAG security risks.
- [[sources/infrastructure-security|Infrastructure Security]]: service mesh, OPA/Rego, Zero Trust/ZTNA, Kubernetes Pod Security, gVisor, Firecracker, full security architecture stack.
- [[sources/network-protocols|Network Protocols]]: Internet packet flow, LAN/WAN boundary, routing mechanics, gRPC, HTTP/2, TLS, TCP, DNS.
- [[sources/app-stack-notes|App Stack Notes]]: Flask structure, REST conventions, Flask-RESTful, n8n workflow automation, edge/serverless/FaaS tradeoffs.
- [[sources/a10-product-notes|A10 Product Notes]]: A10 control plane, ADC/DDoS/security product surface, IaC hooks, Kubernetes connector, deployment forms.
- [[sources/source-provenance-template|Source Provenance Template]]: standard provenance block for source-derived pages.

## Notes
- Raw external reference material lives in `Clippings/`.
- This index should stay navigational. Move heavy detail into narrower pages.
