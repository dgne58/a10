# Wiki Log
## [2026-04-17 10:30] update | preload aligned to execution-router design doc

What changed:
- Rewrote the preload pages to reflect the current `Wiki/design-doc.md` rather than the earlier research-only posture.
- Filled in concrete hackathon-facing guidance for:
  - current project state (`hot.md`)
  - product/runtime shape (`project-map.md`)
  - planned code surfaces (`file-map.md`)
  - intended command set (`commands.md`)
  - planned API routes (`api-routes-and-schemas.md`)
  - route/trace/eval contracts (`data-contracts.md`)
  - implementation assumptions and risks (`known-bugs-and-assumptions.md`)
  - demo fallback paths (`fallback-plans.md`)
  - judge-facing story (`judging-demo-narrative.md`)

Why:
- The design doc now defines a concrete hackathon build, so new sessions should orient from that planned implementation instead of from the older research-only preload.
- The preload needed to answer "what are we actually building next?" without requiring a full reread of the architecture pages.

Pages updated:
- `Wiki/00-preload/hot.md`
- `Wiki/00-preload/project-map.md`
- `Wiki/00-preload/file-map.md`
- `Wiki/00-preload/commands.md`
- `Wiki/00-preload/api-routes-and-schemas.md`
- `Wiki/00-preload/data-contracts.md`
- `Wiki/00-preload/known-bugs-and-assumptions.md`
- `Wiki/00-preload/fallback-plans.md`
- `Wiki/00-preload/judging-demo-narrative.md`


## [2026-04-15 19:45] ingest | batch 20 — API / Schema Standards

Sources processed: JSON Schema 2020-12 spec, OpenAPI Specification v3.1.0, Linkerd Overview (3 files)

Pages updated:
- `Wiki/sources/app-stack-notes.md` — added "API Specification Standards" section: JSON Schema 2020-12 (Core/Validation split, OpenAI function calling connection), OpenAPI 3.1.0 (document structure, data types, sample routing API schema YAML)

Classified absorbed files:
- `Overview.md` (Linkerd overview from linkerd.io — already fully covered by linkerd-notes.md)

Notable: OAS 3.1 is the first version fully aligned with JSON Schema 2020-12; earlier OAS 3.0 was only a subset of JSON Schema; OpenAI function calling tools parameter definitions use JSON Schema directly

## [2026-04-15 19:30] ingest | batch 19 — ML / AI Fundamentals

Sources processed: Chapter 1 (Wireshark), Data parallelism, GNN, Low-rank approximation, Model specification, Reasoning model, Recursive self-improvement, Reward hacking (8 files)

Pages updated:
- `Wiki/sources/post-training-and-alignment.md` — added 4 new sections:
  1. "Reasoning Models" — process supervision, GRPO, test-time compute scaling, GPT-5 routing connection, overthinking attack security concern
  2. "Reward Hacking in LLMs" — sycophancy/length bias/sophistication bias patterns, ICRH (in-context reward hacking), deliberate hacking in reasoning models (o1/R1), mitigation strategies table
  3. "Model Specification" — OpenAI Model Spec hierarchy, Anthropic Constitution 4-tier priority, EU AI Act context
  4. "Data Parallelism in Training" — brief GPU distribution note
  Added "Mathematical basis" subsection to LoRA section (Eckart-Young theorem, SVD connection to LoRA)

Classified absorbed files: Chapter 1 (Wireshark), GNN (background only), Recursive self-improvement (speculative AGI)

Notable: Reward hacking is theoretically unavoidable (Skalse et al. — only unhackable proxy is a constant function); reasoning models now deliberately hack reward signals at inference time (o1/R1 modifying test scripts); GPT-5's built-in routing validates the hackathon architecture; LLM routing evaluation using LLM-as-judge proxy is itself vulnerable to reward hacking

## [2026-04-15 19:00] ingest | batch 18 — Routing / ML Papers

Sources processed: RouteLLM paper (arXiv 2406.18665), RouteLLM GitHub README (×2, one was stub), EmbedLLM (arXiv 2410.02223), GPT-2 paper (Radford et al. 2019) (5 files)

Pages updated:
- `Wiki/sources/routing-papers.md` — major expansion of RouteLLM entry (formal cost-threshold model, APGR/PGR/CPT metrics glossary, router performance table, data augmentation analysis); added EmbedLLM entry (MF-based LLM embedding framework, 15× routing speed, 60× memory efficiency); added GPT-2 foundational paper entry with routing relevance note

Classified absorbed files:
- `lm-sysRouteLLM...md` (stub, content = "doc") — absorbed

Notable: EmbedLLM and RouteLLM's MF router are independently derived from the same matrix factorization idea; EmbedLLM generalizes it to all evaluation tasks not just routing; the pretraining scale gap explains why routing works at all — GPT-4 saw more high-quality patterns at pretraining scale; data augmentation is the single biggest lever for RouteLLM performance (arena-only → near-random on OOD; +judge labels → 60% APGR improvement)

## [2026-04-15 18:30] ingest | batch 17 — OpenAI / Agent Ecosystem

Sources processed: Agent Builder, Sandbox (Codex CLI), Sandbox Agents, AI inference vs. training, What is MCP (5 files)

Pages updated:
- `Wiki/sources/openai-agents-sdk.md` — added "Agent Builder" primitive (visual canvas, ChatKit, SDK export); added "Harness / Compute Boundary" section with architecture diagram; platform-native sandboxing table (Seatbelt/macOS, bubblewrap/Linux, Windows Sandbox); design principle for orchestrator/sandbox separation; updated Sources Included list

Classified absorbed files:
- `AI inference vs. training What is AI inference.md` — Cloudflare explainer; concepts already in serving-and-inference.md
- `What is the Model Context Protocol (MCP).md` — "USB-C port for AI" intro; already covered by mcp-overview.md

Notable: The harness/compute boundary is an important architectural principle — the orchestrator (control plane) should always stay separate from the execution sandbox; sandboxing and approval flow are orthogonal mechanisms; platform sandboxing should be chosen at deploy time based on OS

## [2026-04-15 18:15] ingest | batch 16 — n8n Workflow Automation

Sources processed: Calculating booked orders, Filtering orders, Getting data from DW, Index (Level 1 intro), Inserting data into Airtable, Learning path, Navigating Editor UI, Notifying the team, Setting values (9 files)

All 9 files are n8n Level 1 tutorial course steps for a data warehouse workflow. Existing n8n section in `Wiki/sources/app-stack-notes.md` already covers the relevant synthesis (n8n as optional workflow layer / demo fallback). No new synthesis targets.

Pages updated:
- `Wiki/sources/app-stack-notes.md` — updated last_updated date; n8n content already present

Classified absorbed files: all 9 tutorial files absorbed into existing app-stack-notes n8n section

Notable: n8n course content is step-by-step tutorials, not architecture documentation; existing wiki summary is sufficient for hackathon purposes

## [2026-04-15 18:00] ingest | batch 15 — WebAssembly/WASI/Istio Security

Sources processed: Wasmtime Security, Istio Security, Istio Extensibility/Wasm, Kubernetes Security overview (duplicate), Extensions List, IPTables Ref, gVisor production guide, Wasm conventions, WASI intro (10 files)

Pages updated:
- `Wiki/sources/envoy-gateway-notes.md` — added "WebAssembly Extensions (Proxy-Wasm)" section: Wasm sandbox properties (Wasmtime), Proxy-Wasm plugin capabilities in Istio/Envoy, hackathon use case for custom LLM routing via Wasm filter
- `Wiki/sources/linkerd-notes.md` — added "Istio Security Model" section: SPIFFE workload identity + CA, mTLS modes (STRICT/PERMISSIVE), AuthorizationPolicy (source/operation/condition), relevance table for agentic systems

Classified absorbed files: Kubernetes Security (already in infrastructure-security), WASI intro (not found), Wasm conventions (spec-level), Wasmtime multithreaded (spec-level), gVisor production guide (already in infrastructure-security), iptables reference, Extensions List

Notable: Proxy-Wasm crash isolation is why Wasm is preferred over native C++ Envoy extensions; SPIFFE identity model (not IP-based) is the correct auth model for agentic systems — agents should have cryptographic identity, not just API keys

## [2026-04-15 17:30] ingest | batches 13+14 — Envoy Internals + Linkerd/Istio

Sources processed: 5 Envoy proxy docs (threading model, listeners, listener filters, terminology, what-is-envoy) + 22 Linkerd/Istio docs (circuit breaking, rate limiting, retries, cancellation, deadlines, status codes, compression, observability, proxy config, metrics, custom LB/metrics/naming, benchmarking, auth, debugging, Linkerd architecture, multi-cluster, cluster config, service profiles, EgressNetwork, ExternalWorkload, GRPCRoute, HTTPRoute, Istio Traffic Management) — 27 files

Pages updated:
- `Wiki/sources/envoy-gateway-notes.md` — added "Envoy Proxy Internals" section: single-process multi-threaded architecture diagram, dispatcher/io_uring/TLS thread local storage design, listener + filter chain evaluation order, observability (stats/tracing/admin interface)

Pages created:
- `Wiki/sources/linkerd-notes.md` — Linkerd architecture (control plane: destination/identity/proxy-injector; data plane: Rust micro-proxy); inbound/outbound proxy role split; circuit breaking (failure accrual consecutive policy, probation + exponential backoff); rate limiting (HTTPLocalRateLimitPolicy: total/identity/overrides); retries (HTTP status code ranges, gRPC status codes, 64KiB body limit); Istio VirtualService/DestinationRule/Gateway/ServiceEntry; HTTPRoute + GRPCRoute (Gateway API); hackathon applicability table

Notable: Linkerd2-proxy is Rust-based (not Envoy-based); circuit breaking is endpoint-level not service-level; probe request must be actual app traffic not just health check; ServiceProfile incompatibility with circuit breaking/retries is a common configuration footgun; Istio uses Envoy as data plane (so Envoy internals in envoy-gateway-notes apply to Istio too)

## [2026-04-15 16:30] ingest | batch 12 — Network Attacks (DDoS and DNS)

Sources processed: Cloudflare DDoS Protection, How to DDoS (tools), DDoS botnet, DDoS attack explainer, DNS flood, DNS Security (6 files)

Pages created:
- `Wiki/sources/network-attacks.md` — DDoS attack taxonomy by OSI layer (L7 HTTP flood, L3/4 SYN flood + DNS amplification, volumetric); DNS attack taxonomy (9 attack types: spoofing/cache poisoning, tunneling, hijacking, NXDOMAIN, phantom domain, random subdomain, DNS flood, domain lock-up, botnet CPE); DNSSEC chain-of-trust; DoT/DoH privacy; Cloudflare defense architecture (adaptive rules, eBPF, anycast); relevance to LLM10 inference endpoint protection

Pages updated:
- `Wiki/index.md` — added network-attacks entry
- `Wiki/sources/clipping-intake-queue.md` — 6 files marked classified

Notable: DNS flood (IoT botnet) vs DNS amplification (open resolver reflection) are distinct mechanisms; domain lock-up attack ties up resolver TCP state — useful for understanding how DNS infrastructure can be used as attack vector against LLM API gateways; Denial of Wallet (LLM10) controlled by same rate-limiting mechanisms as DDoS mitigation

## [2026-04-15 16:00] ingest | batch 11 — Adversarial ML Surveys

Sources processed: Attacks in AML (Life-cycle Perspective — Wu et al. arXiv 2302.09457), How Deep Learning Sees the World (Costa et al. arXiv 2305.10862), Adversarial Attacks and Defences A Survey (IIT Kharagpur 2018), A reading survey on AML (duplicate ×2), MITRE ATT&CK (too large — absorbed by ref), NIST SP 800-53r5 (absorbed by ref) — 7 files total

Pages updated:
- `Wiki/sources/adversarial-ml.md` — added: (1) Life-cycle Framework section with 5-stage taxonomy (Wu et al.); (2) Three attack paradigms table (backdoor/weight/adversarial examples) with stage mapping; (3) Backdoor trigger taxonomy (visible/invisible/semantic/scope/location dimensions); (4) Key attack algorithms table (L-BFGS, FGSM, PGD, C&W, JSM, DeepFool, AutoAttack, Square Attack) with norm classification (L0/L2/L∞); (5) Weight attacks section (parameter modification vs bit-flip sub-types); updated Sources Included list
- `Wiki/sources/clipping-intake-queue.md` — 7 files marked classified

Notable: weight attacks (post-training / deployment stage) were not previously covered — fills the gap between supply chain attacks (covered via OWASP LLM03) and inference-time evasion; FGSM/PGD/C&W attack algorithm inventory useful for red-teaming SLM components; backdoor trigger taxonomy (especially semantic triggers with label-only changes) most relevant to fine-tuning pipeline risk

## [2026-04-15 15:30] ingest | batch 9 — OWASP Cheat Sheets (developer reference)

Sources processed: Cross Site Scripting Prevention, DOM based XSS Prevention, Injection Prevention, Database Security, AJAX Security, Attack Surface Analysis, Security Terminology, SQL Injection PortSwigger (8 files)

Pages created:
- `Wiki/sources/owasp-cheat-sheets.md` — XSS output encoding table by context (HTML/JS/CSS/URL), safe vs. dangerous sinks, DOMPurify usage, SQL injection types and detection techniques, parameterized query patterns, DB security (least privilege, TLS, hardening), attack surface analysis methodology, security terminology disambiguation

Pages updated:
- `Wiki/index.md` — added owasp-cheat-sheets entry
- `Wiki/sources/clipping-intake-queue.md` — 8 files marked classified

Notable: DOM XSS vs reflected/stored distinction; AJAX all-sources-untrusted principle; attack surface as sum of entry/exit points + protecting code + valuable data

## [2026-04-15 15:00] ingest | batch 8 — OWASP Web Top 10 (2021)

Sources processed: A01 Broken Access Control, A02 Cryptographic Failures, A03 Injection, A04 Insecure Design, A05 Security Misconfiguration, A06 Vulnerable and Outdated Components, A07 Identification and Authentication Failures, A08 Software and Data Integrity Failures, A09 Security Logging and Monitoring Failures, A10 Server-Side Request Forgery, Introduction, How to use as a standard (12 files)

Pages created:
- `Wiki/sources/owasp-web-top10.md` — all 10 web risks with mechanisms, prevention, CWE mapping, per-risk agentic relevance, cross-reference table to LLM Top 10, hackathon Flask checklist

Pages updated:
- `Wiki/sources/owasp-llm-top10.md` — added backlink to owasp-web-top10
- `Wiki/index.md` — added owasp-web-top10 entry
- `Wiki/sources/clipping-intake-queue.md` — 12 files marked classified

Notable new concepts: SSRF as agentic attack surface (cloud metadata exfiltration via prompt injection), A08 as web analog of LLM supply chain risk, insecure design vs. implementation defect distinction



## [2026-04-15 14:30] ingest | batch 7 — network protocols

Sources processed: Introduction to gRPC.md, Language Guide (proto 3).md, Protocol Buffers Language Specification (Proto3).md, grpcgrpc C++ based gRPC.md, RFC 9113 HTTP2.md, RFC 9293 TCP.md, RFC 8446 TLS 1.3.md, RFC 1035 DNS.md, RFC 2616 HTTP1.1.md, HTTPS Wikipedia.md, What is DNS.md, DNS server types.md, What are DNS records.md, Domain Name System Wikipedia.md, TCP Wikipedia.md, UDP Wikipedia.md

Pages created:
- `Wiki/sources/network-protocols.md` — gRPC + proto3 + HTTP/2 + TLS 1.3 + mTLS + TCP + DNS; protocol comparison table

## [2026-04-15 14:15] ingest | batch 6 — infrastructure security

Sources processed: What is a service mesh.md, What is Istio.md, Why choose Istio.md, Sidecar or ambient.md, Open Policy Agent (OPA).md, What is Zero Trust network.md, What is ZTNA.md, What is CASB.md, Cloud Native Security and Kubernetes.md, Kubernetes Security OWASP.md, Pod Security Standards.md, Pod Security Standards 1.md, What is gVisor.md, Introduction to gVisor security.md, Firecracker.md, firecrackerdocsdesign.md

Pages created:
- `Wiki/sources/infrastructure-security.md` — service mesh (Istio sidecar/ambient), OPA/Rego, Zero Trust/ZTNA, Kubernetes Pod Security Standards, gVisor vs Firecracker vs containers, full security architecture stack

## [2026-04-15 14:00] ingest | batch 5b — RAG and knowledge retrieval

Sources processed: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.md, Dense Passage Retrieval.md, What are embeddings.md, What is a vector database.md, Similarity settings Elasticsearch.md

Pages created:
- `Wiki/sources/rag-and-knowledge-retrieval.md` — RAG formulation (RAG-Sequence/Token), DPR bi-encoder, embeddings, vector databases (HNSW/IVF/PQ), ANN algorithms, RAG security risks (indirect injection/poisoning)

## [2026-04-15 13:45] ingest | batch 5a — inference optimization and prompt caching

Sources processed: Overview TensorRT LLM.md (×3), Quick Start Guide TensorRT-LLM.md, Benchmarking TensorRT-LLM.md, Using FP8 and FP4 with Transformer Engine.md, Unlocking Efficiency in LLM Inference (speculative decoding survey).md, Overview NVIDIA NeMo Framework.md, Prompt caching.md

Pages updated:
- `Wiki/sources/serving-and-inference.md` — deep rewrite: TensorRT-LLM full capabilities, speculative decoding (draft-then-verify, drafter categories, 2-5× speedup), FP8/FP4 quantization (format table, routing implication), prompt caching (mechanism, pricing table with actual numbers, routing implication), cheap-path vs strong-path tradeoff table

## [2026-04-15 13:30] ingest | batch 4 — OpenAI Agents SDK

Sources processed: OpenAI Agents SDK.md, Agents SDK OpenAI API.md, Guardrails OpenAI Agents SDK.md, Function calling OpenAI API.md

Pages created:
- `Wiki/sources/openai-agents-sdk.md` — Agent primitives (Agent/Handoffs/Guardrails/Function Tools/Sessions/Sandbox), agent loop, SDK vs Responses API decision table, input/output/tool guardrails, function calling 5-step flow, MCP integration, security considerations mapped to OWASP LLM risks

## [2026-04-15 13:00] ingest | batch 3 — new routing papers

Sources processed: Router-R1 Teaching LLMs Multi-Round Routing.md, Hybrid LLM Cost-Efficient and Quality-Aware Query Routing.md

Pages updated:
- `Wiki/workflows/llm-routing-approaches.md` — added Router-R1 section (RL multi-round routing, reward equation `r(x,y) = R_format + (1-α)·R_outcome + α·R_cost`, PPO, 14K samples, model descriptors for generalization) and HybridLLM section (quality-gap `H(x) = q(S(x)) - q(L(x))`, DeBERTa router, data transformation trick, 40% fewer large-model calls)

Notable new concepts: LLM-as-router (Router-R1), quality-gap-aware routing threshold (HybridLLM), BART score for quality measurement

## [2026-04-15 12:30] ingest | batch 3b — post-training additions (CoT + LoRA)

Sources processed: Demystifying Long Chain-of-Thought Reasoning in LLMs.md, What is LoRA Low-rank adaptation.md

Pages updated:
- `Wiki/sources/post-training-and-alignment.md` — added long CoT section (branching/backtracking, RL + verifiable rewards, cosine length-scaling reward, routing implication) and LoRA section (mathematical form W' = W + A×B, QLoRA, practical hyperparameters, supply chain risk)

## [2026-04-15 12:00] ingest | batch 2 — adversarial ML

Sources processed: Adversarial Machine Learning (NIST AI 100-2e).md, advmlthreatmatrix adversarial-ml-101.md, advmlthreatmatrix adversarial-ml-threat-matrix.md

Pages created:
- `Wiki/sources/adversarial-ml.md` — NIST AI 100-2e two-branch taxonomy (predictive AI: evasion/poisoning/privacy; generative AI: supply chain/direct injection/indirect injection); MITRE AML threat matrix tactics; train-time vs inference-time breakdown; defense landscape; relevance to agentic project

## [2026-04-15 11:30] ingest | batch 1 — OWASP LLM Top 10

Sources processed: LLM01 2025 Prompt Injection.md, LLM02 2025 Sensitive Information Disclosure.md, LLM03 2025 Supply Chain.md, LLM04 2025 Data and Model Poisoning.md, LLM05 2025 Improper Output Handling.md, LLM06 2025 Excessive Agency.md, LLM09 2025 Misinformation.md, LLM10 2025 Unbounded Consumption.md

Pages created:
- `Wiki/sources/owasp-llm-top10.md` — all 8 risks covered with types, examples, defenses; LLM06 connection to policy gateway; agentic system threat→control mapping table

Notable new concepts: indirect prompt injection (RAG vector), sleeper agents (LLM04), DoW attacks (LLM10), package hallucination (LLM09)

## [2026-04-15 10:55] update | added clipping sync command

What changed:
- Added a dependency-free PowerShell script that compares `Clippings/` against the clipping inventory, registry, and intake queue.
- Added a small Windows wrapper so the command can be run the same way from Codex or Claude Code terminals.
- Documented the exact `check` and `sync` commands in the preload and schema docs.

Why:
- The wiki's clipping provenance layer was manual and could drift behind the raw folder.
- A local command makes new-file detection repeatable instead of depending on memory or ad hoc inspection.

Pages updated:
- `WIKI.md`
- `Wiki/00-preload/file-map.md`
- `Wiki/00-preload/commands.md`

Files created:
- `scripts/sync-clippings.ps1`
- `scripts/sync-clippings.cmd`

## [2026-04-14 15:40] update | reverted wiki directory to visible top-level folder

What changed:
- Renamed the canonical wiki directory from `.wiki/` back to `Wiki/`.
- Removed the temporary `Wiki` junction alias that had pointed at `.wiki/`.
- Updated path references in `AGENTS.md`, `WIKI.md`, and `.obsidian/workspace.json`.

Why:
- Obsidian does not handle dotfolders well in the vault file explorer, so the wiki disappeared from the visible workspace.
- The visible `Wiki/` folder is the more reliable shape for both the app UI and local agent instructions in this repo.

Pages updated:
- `AGENTS.md`
- `WIKI.md`
- `.obsidian/workspace.json`

## [2026-04-13 23:45] update | added inline provenance blocks to highest-value source pages

What changed:
- Added a standard provenance block directly to the highest-value source pages and secondary deep dives.
- Source-derived pages now visibly point to the clipping registry, clipping inventory, and raw-source verification workflow.

Why:
- Provenance should be visible at the page level, not only in centralized tracking pages.
- This makes it easier for future agents to know where to verify a page's claims and which raw files to revisit when precision matters.

Pages updated:
- `Wiki/sources/mcp-agentic-workflows.md`
- `Wiki/sources/task-aware-routing.md`
- `Wiki/sources/post-training-and-alignment.md`
- `Wiki/sources/security-networking-and-governance.md`
- `Wiki/sources/app-stack-and-delivery.md`
- `Wiki/sources/corpus-overview.md`
- `Wiki/sources/datasets-and-evaluation.md`
- `Wiki/sources/protocols-and-observability.md`
- `Wiki/sources/mcp-overview.md`
- `Wiki/sources/routing-papers.md`
- `Wiki/sources/fine-tuning-notes.md`
- `Wiki/sources/agentic-security-notes.md`
- `Wiki/sources/envoy-gateway-notes.md`
- `Wiki/sources/serving-and-inference.md`
- `Wiki/sources/app-stack-notes.md`

## [2026-04-13 23:35] update | made clipping tracking exhaustive and added intake/template pages

What changed:
- Added an exhaustive clipping inventory page covering every file currently present in `Clippings/`.
- Added a dedicated intake queue so new or weakly integrated clipping files are visible before deeper synthesis happens.
- Added a reusable provenance template so future source-derived pages can carry stronger raw-file traceability.

Why:
- The wiki needed both a high-signal provenance map and a completeness layer so no clipping file disappears without explicit status.

Pages updated:
- `WIKI.md`
- `Wiki/index.md`
- `Wiki/sources/README.md`
- `Wiki/log.md`

Pages created:
- `Wiki/sources/clipping-inventory.md`
- `Wiki/sources/clipping-intake-queue.md`
- `Wiki/sources/source-provenance-template.md`

## [2026-04-13 23:20] update | added clipping provenance and raw-source verification layer

What changed:
- Added a clipping registry that maps raw files in `Clippings/` to their thematic wiki pages and current synthesis status.
- Added a raw-source verification workflow so future agents know when to reopen a clipping for exact snippets, numbers, commands, or architecture details.
- Updated the schema and agent instructions so provenance is now a first-class part of ingest and maintenance.

Why:
- The wiki needed a stronger provenance model so new clippings can be tracked immediately and exact raw-file detail can be recovered without bypassing the wiki entirely.

Pages updated:
- `AGENTS.md`
- `WIKI.md`
- `Wiki/index.md`
- `Wiki/sources/README.md`
- `Wiki/workflows/README.md`
- `Wiki/log.md`

Pages created:
- `Wiki/sources/clipping-registry.md`
- `Wiki/workflows/raw-source-verification.md`

## [2026-04-13 23:05] wiki expansion pass

Expanded:
- `Wiki/architecture/reference-driven-solution-shape.md`
- `Wiki/architecture/research-theses.md`
- `Wiki/sources/mcp-agentic-workflows.md`
- `Wiki/sources/task-aware-routing.md`
- `Wiki/sources/post-training-and-alignment.md`
- `Wiki/sources/security-networking-and-governance.md`
- `Wiki/components/mcp-control-plane.md`
- `Wiki/components/policy-gateway.md`
- `Wiki/workflows/llm-routing-approaches.md`
- `Wiki/workflows/mcp-agentic-patterns.md`
- `Wiki/workflows/slm-fine-tuning-pipeline.md`
- `Wiki/data-models/evaluation-record.md`

Created:
- `Wiki/architecture/persistent-memory-vs-rag.md`
- `Wiki/components/tool-surfaces.md`
- `Wiki/workflows/routing-evaluation-loop.md`

Major structural improvements:
- Promoted repeated ideas into dedicated hub pages instead of duplicating them across sources and components.
- Strengthened the main source hubs with mechanisms, architectures, and tradeoffs rather than leaving them as shallow summaries.
- Added stronger cross-linking between architecture, source, workflow, and component layers.
- Expanded the routing story from model choice into full path selection: wiki, tools, MCP, specialized model, stronger model.
- Added an explicit evaluation loop so routing claims can tie back to stored evidence.

Open gaps / future work:
- Several preload pages are still research-derived because no real app codebase has been ingested yet.
- `envoy-ai-gateway.md`, `agentic-security-notes.md`, and `routing-papers.md` are useful deep dives but could still be normalized and expanded further.
- Once a real repo exists, file map, commands, routes, and contracts should be replaced with code-derived detail.

## [2026-04-13 22:20] review | normalized second-pass wiki edits against the clippings corpus

What changed:
- Reviewed the later wiki enrichments as a quality pass rather than accepting them wholesale.
- Rewrote navigation and several enriched pages to remove mojibake, reduce speculative implementation details, and keep claims anchored to `Clippings/` or the local repo state.
- Kept the useful synthesis, but removed invented demo paths and provider-specific assumptions that were not yet grounded in this vault.

Why:
- The second pass improved depth, but some pages had encoding damage and overfit to hypothetical implementation details.
- For a hackathon wiki, grounded and queryable beats impressive-but-fragile specificity.

Pages updated:
- `Wiki/index.md`
- `Wiki/components/knowledge-wiki.md`
- `Wiki/components/router.md`
- `Wiki/components/orchestrator.md`
- `Wiki/workflows/demo-flow.md`
- `Wiki/sources/app-stack-notes.md`
- `Wiki/sources/serving-and-inference.md`
- `Wiki/sources/fine-tuning-notes.md`

## [2026-04-13 22:45] enrich | knowledge-wiki + backlink pass + eval scenario

What changed:
- Enriched `knowledge-wiki.md` component page with full agent search order, hot.md protocol,
  query/ingest workflows, page structure reference, and hackathon question types.
- Added backlinks from `research-theses.md` to all relevant workflow/component pages (theses 1–8 now
  link to their implementing pages).
- Added backlinks from `reference-driven-solution-shape.md` to workflow synthesis pages and serving stack.
- Added backlinks from `security-networking-and-governance.md` to the two synthesis pages that implement it.
- Enriched `datasets-and-evaluation.md` with concrete 4-scenario evaluation table (metrics + expected routes).

Pages updated:
- `Wiki/components/knowledge-wiki.md`
- `Wiki/architecture/research-theses.md`
- `Wiki/architecture/reference-driven-solution-shape.md`
- `Wiki/sources/security-networking-and-governance.md`
- `Wiki/sources/datasets-and-evaluation.md`
- `Wiki/index.md`

## [2026-04-13 22:15] enrich | component pages deepened + two new source pages added

What changed:
- Enriched 4 thin component pages with synthesis content, implementation patterns, and backlinks.
- Deepened `demo-flow.md` with concrete 7-step demo script, per-step traces, timing guide, and fallback table.
- Created 2 new source pages synthesizing clippings not previously covered.

Why:
- Codex created thin structural component pages. This pass adds the substantive technical content
  derived from the clippings corpus so agents have actionable references, not just page skeletons.

Pages updated (enriched):
- `Wiki/components/router.md` — routing algorithm table, minimal 4-tier policy, trace signal schema, backlinks to llm-routing-approaches + routing-papers
- `Wiki/components/orchestrator.md` — mcp-agent workflow pattern table, mcp-agent code skeleton, durable execution note, backlinks to mcp-agentic-patterns + mcp-overview
- `Wiki/components/policy-gateway.md` — A2AS five elements, IBM four security layers table, dynamic credentials pattern, backchannel auth, minimal policy dict, Envoy enforcement table, backlinks to agentic-security-notes + envoy-ai-gateway
- `Wiki/components/mcp-control-plane.md` — MCP primitives table, function tools vs MCP tools, server inventory YAML, server nesting pattern, auth pre-flight checklist, failure recovery table, backlinks to mcp-agentic-patterns + mcp-overview
- `Wiki/workflows/demo-flow.md` — 7 concrete steps with inputs/outputs, trace examples, component refs, timing guide, fallback table

Pages created (new files on disk):
- `Wiki/sources/serving-and-inference.md` — Dynamo (capabilities, quick start, K8s deploy), TensorRT-LLM (quantization, model support), vLLM, NeMo; layer architecture diagram; hackathon relevance table
- `Wiki/sources/app-stack-notes.md` — Flask Blueprint structure, app factory pattern, REST conventions, flasgger/Swagger setup, Flask-RESTful, n8n concepts and example flow, TDD approach, Flask vs FastAPI comparison

Index updated: `Wiki/index.md` — added ✓ markers on all enriched components, demo-flow, and two new source pages.

## [2026-04-13 20:30] update | initial hackathon wiki scaffold

What changed:
- Added shared schema files for Codex and Claude (`AGENTS.md`, `WIKI.md`, `CLAUDE.md`).
- Created preload pages optimized for fast agent orientation during a hackathon.
- Added starter architecture, workflow, source, component, and data-model hubs.

Why:
- The project needs a local-first memory layer so agents consult the wiki before searching broadly or using the internet.

Pages touched:
- `AGENTS.md`
- `WIKI.md`
- `CLAUDE.md`
- `Wiki/index.md`
- `Wiki/log.md`
- `Wiki/00-preload/*`
- `Wiki/architecture/*`
- `Wiki/components/README.md`
- `Wiki/data-models/README.md`
- `Wiki/workflows/README.md`
- `Wiki/sources/README.md`

## [2026-04-13 21:30] ingest | concrete synthesis pages from clippings — routing, MCP, Envoy, SLMs, security

What changed:
- Read 15 key clippings and created 9 substantive wiki pages with real content.
- These are the primary actionable reference pages for hackathon agents.

Why:
- Prior log entry referenced files that were planned but not created. This entry records the actual file creation.

Pages created (new files on disk):
- `Wiki/workflows/llm-routing-approaches.md` — RouteLLM / NVIDIA Blueprint / GreenServ / Iris with decision guide + code sketch
- `Wiki/workflows/mcp-agentic-patterns.md` — MCP primitives, agentic loop, mcp-agent patterns + auth checklist
- `Wiki/workflows/slm-fine-tuning-pipeline.md` — Unsloth + LoRA pipeline, ChatML format, SFT/DPO/RLHF taxonomy
- `Wiki/components/envoy-ai-gateway.md` — Envoy AI Gateway, agentgateway, MCP RBAC, passthrough/aggregating modes
- `Wiki/sources/routing-papers.md` — RouteLLM, NVIDIA Blueprint, Multi-Model Routing, Iris, KNN Router
- `Wiki/sources/mcp-overview.md` — Introducing MCP, agentic workflows, mcp-agent, platform engineering patterns
- `Wiki/sources/envoy-gateway-notes.md` — Envoy AI Gateway docs, case for Envoy in agentic era, agentgateway
- `Wiki/sources/fine-tuning-notes.md` — Practical SLM guide, alignment techniques (SFT/DPO/RLHF/GRPO/ORPO)
- `Wiki/sources/agentic-security-notes.md` — IBM runtime security, A2AS framework, security layers, dynamic credentials

Index updated: `Wiki/index.md` — added ✓ markers on created pages in Components, Workflows, Sources sections.

## [2026-04-13 21:05] ingest | first-pass synthesis of clippings corpus

What changed:
- Ingested the `Clippings/` directory at the thematic level instead of leaving it as raw reference material.
- Added source synthesis pages for MCP, routing, post-training, app stack, security, protocols, and datasets.
- Added architecture, component, workflow, and data-model pages inferred from the strongest recurring patterns in the source set.
- Upgraded preload pages so agents can use the wiki as a real planning surface even before the final codebase is present.

Why:
- The feasibility test is whether a local wiki can compress a large research corpus into queryable working memory for hackathon agents.
- The raw clipped articles already contain enough structure to define a likely solution shape and implementation plan.

Pages touched:
- `Wiki/index.md`
- `Wiki/00-preload/*`
- `Wiki/architecture/*`
- `Wiki/components/*`
- `Wiki/data-models/*`
- `Wiki/workflows/*`
- `Wiki/sources/*`

## [2026-04-15 11:26] update | synced clipping tracking pages

What changed:
- Added newly detected raw clipping files to the inventory, registry, and intake queue.
- Marked each detected file as unsorted/unclassified so future ingest passes can classify them cleanly.

Why:
- The tracking pages had drifted behind the raw `Clippings/` directory.
- This keeps the wiki's provenance layer exhaustive enough for future agents to trust.

Clipping files added:
- `Filtering orders  n8n Docs.md`
- `Welcome to TensorRT LLM�s Documentation! � TensorRT LLM.md`

Pages updated:
- `Wiki/sources/clipping-inventory.md`
- `Wiki/sources/clipping-registry.md`
- `Wiki/sources/clipping-intake-queue.md`

## [2026-04-18 16:30] fix | HumanEval harness indentation and strong-model config

What changed:
- Rebuilt `project/scripts/run_humaneval.py` to normalize body-only completions before execution instead of stripping away indentation on the first line.
- Added first-failure debug logging that prints the exact assembled program plus subprocess stdout/stderr.
- Added focused regression tests for fenced code, body-only completions, and full-function completions.
- Corrected `project/backend/config.py` so `strong_model` maps to `openai/gpt-4o` instead of `openai/gpt-4o-mini`.

Why:
- The prior harness turned valid HumanEval answers into syntax/indentation errors, collapsing pass@1 to near-zero even for `gpt-4o`.
- The router's "strong" branch was also using a weaker model than intended.

Verification:
- `cd project && python -m unittest tests.test_run_humaneval tests.test_router_eval_contract`
- `cd project && python scripts/run_humaneval.py --limit 5`

Observed result:
- `run_humaneval.py --limit 5` now produced `Router pass@1: 5/5` and `Naive pass@1: 5/5` in the smoke run.

## [2026-04-18 16:55] update | swap OpenAI defaults to Claude Haiku and Sonnet

What changed:
- Replaced the remaining OpenAI default model selections in the router surfaces with Anthropic models on OpenRouter.
- Updated the backend router to use `anthropic/claude-sonnet-4.6` for `strong_model` and `anthropic/claude-haiku-4.5` as fallback.
- Updated the CLI's former `gpt-4o-mini` slot to `anthropic/claude-haiku-4.5`.
- Switched the eval and HumanEval naive baselines to Claude Sonnet.
- Tightened the HumanEval system prompt to request the full function definition so Claude outputs execute cleanly.

Why:
- The user wanted Claude Haiku and Sonnet as the day-to-day coding defaults instead of ChatGPT-family models.
- The initial Claude slug choice was stale for OpenRouter and returned `404`, so the model IDs were corrected to current OpenRouter slugs.

Verification:
- `cd project && python -m unittest tests.test_run_humaneval tests.test_router_eval_contract`
- `cd project && python scripts/run_humaneval.py --limit 1`

Observed result:
- `run_humaneval.py --limit 1` completed successfully with `Router pass@1: 1/1` and `Naive pass@1: 1/1` using Claude Sonnet.

## [2026-04-18 17:05] ui | remove Verify chip from prompt area

What changed:
- Removed the `Verify` branch chip from the frontend prompt-area branch selector row in `project/frontend/src/components/ui/query-panel.tsx`.
- Kept the underlying `verification_tool` branch metadata intact so route traces can still render correctly if the backend returns that branch.

Why:
- The user wanted the `Verify` control removed from the frontend model prompting area without changing backend routing behavior.

Verification:
- `cd project/frontend && npm run build`

## [2026-04-18 17:25] refactor | collapse surfaced router branches to four options

What changed:
- Removed the separate surfaced `verification_tool` path from the backend router, Flask app, training prompt/schema, CLI seed text, and frontend branch metadata.
- Kept tool use as an internal capability of the local cheap path instead of a user-facing router option.
- Updated project/codebase questions to classify as `simple` + `factual`, so they hit memory first and fall back to `cheap_model` on memory miss.
- Removed the dead backend verifier module and updated preload wiki pages to reflect the current four-option branch set.

Why:
- The user wanted the router to expose only four choices: `memory_answer`, `cheap_model`, `mid_model`, and `strong_model`.
- A separate verification branch no longer fit the product surface once project lookups were folded into the memory-first path.

Verification:
- `cd project && python -m unittest tests.test_run_humaneval tests.test_router_eval_contract`
- `cd project && python -m py_compile backend\\app.py backend\\router.py scripts\\run_eval.py scripts\\run_humaneval.py training\\serve.py training\\integrate.py training\\prepare_dataset.py cli.py`
- `cd project/frontend && npm run build`

## 2026-04-17

Summary:
- Fixed router/eval API drift in `project/` after `scripts/run_eval.py` failed on `from router import classify, select_model`.
- Added a focused Python regression test for the router/eval contract.
- Updated preload wiki pages to reflect that the app implementation now exists and that eval validation should prefer the no-API regression test before running the full benchmark.

Files changed:
- `project/backend/router.py`
- `project/scripts/run_eval.py`
- `project/tests/test_router_eval_contract.py`
- `Wiki/00-preload/hot.md`
- `Wiki/00-preload/commands.md`
- `Wiki/00-preload/known-bugs-and-assumptions.md`

## [2026-04-15 20:20] ingest | batch 21 — Internet / Serverless Fundamentals

Sources processed: How does the Internet work, What is a LAN, What is routing, What is the network layer, What is edge computing, What is Function-as-a-Service (FaaS), What is serverless computing, Why use serverless computing (8 files)

Pages updated:
- `Wiki/sources/network-protocols.md` — added "Internet Basics" and "Routing Mechanics" sections: network-of-networks framing, packet switching, end-to-end web request path, LAN/WAN boundary, static vs dynamic routing, BGP/OSPF/RIP
- `Wiki/sources/app-stack-notes.md` — added "Edge And Serverless Patterns" section: deployment-model comparison, FaaS role, edge ingress fit, orchestrator limits, practical recommendation for hackathon architecture
- `Wiki/sources/clipping-intake-queue.md` — marked all 8 files classified and linked to target wiki pages
- `Wiki/index.md` — updated summaries for protocols and app-stack pages to reflect the new material

Notable: This batch clarified the difference between packet routing and application-level model/tool routing, and made the wiki's deployment guidance more concrete by separating edge ingress from long-lived orchestration.

## [2026-04-15 20:30] ingest | batch 22 — AI / LLM / DLP Fundamentals

Sources processed: What is an LLM, What is artificial intelligence (AI), What is data loss prevention (DLP) (3 files)

Pages updated:
- `Wiki/sources/task-aware-routing.md` — added "What Routing Assumes About LLMs" section: transformer/deep-learning baseline, probabilistic reliability, routing-relevant failure modes
- `Wiki/sources/security-networking-and-governance.md` — added delegated-agent identity and DLP sections: on-behalf-of semantics, agent/user/tool identity separation, outbound data-flow controls, content-detection mechanisms
- `Wiki/sources/clipping-intake-queue.md` — marked all 3 files classified and linked to target wiki pages
- `Wiki/index.md` — strengthened the security/governance summary to include delegated authority and DLP

Notable: DLP emerged as a runtime control for agentic systems, not just a compliance tool, and the basic AI/LLM sources were absorbed into routing/governance assumptions rather than split into a low-value standalone page.

## [2026-04-15 20:45] ingest | batch 23 — PDF / Product Extracts

Sources processed: OptiRoute paper extract, AI-agent identity whitepaper extract, large-batch training paper extract, neural language model scaling-laws extract, FrugalGPT paper extract, A10 product documentation extracts (12 files)

Pages updated:
- `Wiki/sources/routing-papers.md` — added OptiRoute and FrugalGPT entries: multi-constraint routing, cascades, cost-aware escalation
- `Wiki/sources/security-networking-and-governance.md` — expanded identity/delegation framing using the agent-auth whitepaper
- `Wiki/sources/post-training-and-alignment.md` — added "Scaling Laws And Batch-Size Limits" section: gradient noise scale, batch-size ceiling, compute/data/model scaling implications
- `Wiki/sources/clipping-intake-queue.md` — marked all 12 files classified and linked to target wiki pages
- `Wiki/index.md` — added the new A10 source page and refreshed summary lines

Pages created:
- `Wiki/sources/a10-product-notes.md` — A10 product/control-plane/IaC/Kubernetes capability map and architectural interpretation

Notable: The PDF extracts were not generic leftovers; they filled real gaps in routing economics, agent identity, training-scale constraints, and the A10 infrastructure surface relevant to this repo.

## [2026-04-15 21:20] wiki expansion pass

Expanded:
- `Wiki/architecture/reference-driven-solution-shape.md`
- `Wiki/components/router.md`
- `Wiki/components/orchestrator.md`
- `Wiki/components/mcp-control-plane.md`
- `Wiki/components/policy-gateway.md`
- `Wiki/components/tool-surfaces.md`
- `Wiki/sources/task-aware-routing.md`
- `Wiki/sources/mcp-agentic-workflows.md`
- `Wiki/sources/security-networking-and-governance.md`
- `Wiki/data-models/routed-request.md`
- `Wiki/data-models/tool-invocation.md`
- `Wiki/workflows/README.md`
- `Wiki/index.md`

Created:
- `Wiki/workflows/request-execution-lifecycle.md`

Major structural improvements:
- Introduced a single canonical request lifecycle page so architecture, routing, orchestration, MCP, and policy pages no longer need to each describe a competing partial flow.
- Deepened the architecture and component hubs with explicit responsibility boundaries, branch taxonomy, control-plane vs data-plane distinctions, capability bundle design, trust zones, DLP integration, and write-back policy.
- Strengthened source-hub synthesis by turning repeated background claims into operational abstractions: branch families for routing, MCP as a capability protocol rather than a runtime, and trust-boundary framing for governance.
- Improved index and workflow navigation so the lifecycle page and expanded component roles are discoverable from the top-level graph.

Open gaps / future work:
- `Wiki/sources/clipping-registry.md` remains stale and appears to have encoding damage; it should be normalized and reconciled against `clipping-intake-queue.md`.
- Several preload pages remain research-shaped because no real app codebase has been mapped into the vault yet.
- `Wiki/data-models/evaluation-record.md`, `Wiki/architecture/dependency-map.md`, and some source deep dives could still be expanded with more concrete interface and failure-path detail once implementation exists.

## [2026-04-15 21:45] repair | registry normalization + evidence/dependency deepening

What changed:
- Rebuilt `Wiki/sources/clipping-registry.md` as clean UTF-8 and reconciled it with the authoritative intake queue and current source hubs.
- Expanded `Wiki/architecture/dependency-map.md` from a placeholder list into an architectural dependency graph with coupling/failure surfaces and codebase-era questions.
- Expanded `Wiki/data-models/evaluation-record.md` into a stronger evidence model with scenario families, extended fields, comparison patterns, and common pitfalls.

Why:
- The registry had become stale and encoding-damaged enough to block safe patching and weaken provenance trust.
- The dependency and evaluation pages were still too shallow relative to the rest of the expanded architecture and lifecycle model.

Pages updated:
- `Wiki/sources/clipping-registry.md`
- `Wiki/architecture/dependency-map.md`
- `Wiki/data-models/evaluation-record.md`
- `Wiki/log.md`

Notable:
- `clipping-intake-queue.md` remains the authoritative operational queue for newly added or weakly synthesized sources.
- `clipping-registry.md` is now restored as the human-readable provenance map rather than a stale dump of outdated `new` entries.

## [2026-04-15 13:54] update | synced clipping tracking pages

What changed:
- Added newly detected raw clipping files to the inventory, registry, and intake queue.
- Marked each detected file as unsorted/unclassified so future ingest passes can classify them cleanly.

Why:
- The tracking pages had drifted behind the raw `Clippings/` directory.
- This keeps the wiki's provenance layer exhaustive enough for future agents to trust.

Clipping files added:
- `A reading survey on adversarial machine learning Adversarial attacks and their understanding 1.md`
- `A reading survey on adversarial machine learning Adversarial attacks and their understanding.md`
- `A01 Broken Access Control - OWASP Top 102021.md`
- `A02 Cryptographic Failures - OWASP Top 102021.md`
- `A03 Injection - OWASP Top 102021.md`
- `A04 Insecure Design - OWASP Top 102021.md`
- `A05 Security Misconfiguration - OWASP Top 102021.md`
- `A06 Vulnerable and Outdated Components - OWASP Top 102021.md`
- `A07 Identification and Authentication Failures - OWASP Top 102021.md`
- `A08 Software and Data Integrity Failures - OWASP Top 102021.md`
- `A09 Security Logging and Monitoring Failures - OWASP Top 102021.md`
- `A10 Server Side Request Forgery (SSRF) - OWASP Top 102021.md`
- `Adversarial Attacks and Defences A Survey.md`
- `Adversarial Machine Learning.md`
- `advmlthreatmatrixpagesadversarial-ml-101.md at master 1.md`
- `advmlthreatmatrixpagesadversarial-ml-101.md at master.md`
- `advmlthreatmatrixpagesadversarial-ml-threat-matrix.md at master 1.md`
- `advmlthreatmatrixpagesadversarial-ml-threat-matrix.md at master.md`
- `Agent Builder  OpenAI API.md`
- `Agents SDK  OpenAI API.md`
- `AI inference vs. training What is AI inference.md`
- `AJAX Security - OWASP Cheat Sheet Series.md`
- `Architecture.md`
- `Attack Surface Analysis - OWASP Cheat Sheet Series.md`
- `Attacks in Adversarial Machine Learning A Systematic Survey from the Life-cycle Perspective.md`
- `Authentication.md`
- `Benchmarking Default Performance � TensorRT-LLM.md`
- `Benchmarking.md`
- `Cancellation.md`
- `Circuit Breaking.md`
- `Cloud Native Security and Kubernetes.md`
- `Cloudflare DDoS Protection.md`
- `Cluster Configuration.md`
- `Compression.md`
- `Control Plane Port Names.md`
- `Conventions � WebAssembly 3.0 (2026-04-09).md`
- `Cross Site Scripting Prevention - OWASP Cheat Sheet Series.md`
- `Custom Backend Metrics.md`
- `Custom Load Balancing Policies.md`
- `Custom Name Resolution.md`
- `CWE -    CWE-190 Integer Overflow or Wraparound (4.19.1).md`
- `CWE -    CWE-266 Incorrect Privilege Assignment (4.19.1).md`
- `CWE -    CWE-269 Improper Privilege Management (4.19.1).md`
- `CWE -    CWE-276 Incorrect Default Permissions (4.19.1).md`
- `CWE -    CWE-287 Improper Authentication (4.19.1).md`
- `CWE -    CWE-288 Authentication Bypass Using an Alternate Path or Channel (4.19.1).md`
- `CWE -    CWE-400 Uncontrolled Resource Consumption (4.19.1).md`
- `CWE -    CWE-427 Uncontrolled Search Path Element (4.19.1).md`
- `CWE -    CWE-798 Use of Hard-coded Credentials (4.19.1).md`
- `CWE -    CWE-98 Improper Control of Filename for IncludeRequire Statement in PHP Program ('PHP Remote File Inclusion') (4.19.1).md`
- `CWE - CWE-1000 Research Concepts (4.19.1).md`
- `Database Security - OWASP Cheat Sheet Series.md`
- `Deadlines.md`
- `Debugging.md`
- `Dense Passage Retrieval for Open-Domain Question Answering.md`
- `DNS server types.md`
- `DOM based XSS Prevention - OWASP Cheat Sheet Series.md`
- `EgressNetwork.md`
- `Extensibility.md`
- `Extensions List.md`
- `ExternalWorkload.md`
- `Firecracker.md`
- `firecrackerdocsdesign.md at main.md`
- `grpcgrpc C++ based gRPC (C++, Python, Ruby, Objective-C, PHP, C).md`
- `GRPCRoute.md`
- `Guardrails - OpenAI Agents SDK.md`
- `How Deep Learning Sees the World A Survey on Adversarial Attacks & Defenses.md`
- `How does the Internet work.md`
- `How to DDoS  DoS and DDoS attack tools.md`
- `How to use the OWASP Top 10 as a standard - OWASP Top 102021.md`
- `HTTPRoute.md`
- `Hybrid LLM Cost-Efficient and Quality-Aware Query Routing.md`
- `Injection Prevention - OWASP Cheat Sheet Series.md`
- `Introduction - OWASP Top 102021.md`
- `Introduction � WASI.dev.md`
- `Introduction to gRPC.md`
- `Introduction to gVisor security - gVisor.md`
- `IPTables Reference.md`
- `JSON Schema - Specification section.md`
- `Kubernetes Security - OWASP Cheat Sheet Series.md`
- `Language Guide (proto 3).md`
- `Language Models are Unsupervised Multitask Learners.md`
- `Listener filters � envoy 1.38.0-dev-550d57 documentation.md`
- `Listeners � envoy 1.38.0-dev-550d57 documentation.md`
- `LLM012025 Prompt Injection.md`
- `LLM022025 Sensitive Information Disclosure.md`
- `LLM032025 Supply Chain.md`
- `LLM042025 Data and Model Poisoning.md`
- `LLM052025 Improper Output Handling.md`
- `LLM062025 Excessive Agency.md`
- `LLM092025 Misinformation.md`
- `LLM102025 Unbounded Consumption.md`
- `lm-sysRouteLLM A framework for serving and evaluating LLM routers - save LLM costs without compromising quality 1.md`
- `lm-sysRouteLLM A framework for serving and evaluating LLM routers - save LLM costs without compromising quality.md`
- `MITRE ATT&CK�.md`
- `Multi-cluster communication.md`
- `Multithreaded Embedding - Wasmtime.md`
- `Observability.md`
- `Open Policy Agent (OPA)  Open Policy Agent.md`
- `OpenAI Agents SDK.md`
- `OpenAPI Specification v3.1.0.md`
- `Overview � TensorRT LLM 1.md`
- `Overview.md`
- `PDF to Markdown 4.md`
- `Pod Security Standards 1.md`
- `Pod Security Standards.md`
- `Production guide - gVisor.md`
- `Prompt caching.md`
- `Protocol Buffers Language Specification (Proto3).md`
- `Proxy Configuration.md`
- `Proxy Log Level.md`
- `Proxy Metrics.md`
- `Quick Start Guide � TensorRT LLM.md`
- `Rate Limiting.md`
- `Retries.md`
- `Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.md`
- `RFC 1035 Domain names - implementation and specification.md`
- `RFC 8446 The Transport Layer Security (TLS) Protocol Version 1.3.md`
- `RFC 9113 HTTP2.md`
- `RFC 9293 Transmission Control Protocol (TCP).md`
- `RouteLLM Learning to Route LLMs with Preference Data 1.md`
- `Router-R1 Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning.md`
- `Sandbox � Codex  OpenAI Developers.md`
- `Sandbox Agents  OpenAI API.md`
- `Security - Wasmtime.md`
- `Security 1.md`
- `Security and Privacy Controls for Information Systems and Organizations.md`
- `Security Terminology - OWASP Cheat Sheet Series.md`
- `Security.md`
- `Service Profiles.md`
- `Sidecar or ambient.md`
- `Similarity settings  Elasticsearch Reference.md`
- `Status Codes.md`
- `Terminology � envoy 1.38.0-dev-550d57 documentation.md`
- `Threading model � envoy 1.38.0-dev-550d57 documentation.md`
- `Traffic Management.md`
- `Unlocking Efficiency in Large Language Model Inference A Comprehensive Survey of Speculative Decoding.md`
- `Using FP8 and FP4 with Transformer Engine � Transformer Engine 2.13.0 documentation.md`
- `What are DNS records.md`
- `What are embeddings in machine learning.md`
- `What is a DDoS botnet.md`
- `What is a distributed denial-of-service (DDoS) attack.md`
- `What is a DNS flood  DNS flood DDoS attack.md`
- `What is a LAN (local area network).md`
- `What is a service mesh.md`
- `What is a vector database  How vector databases work.md`
- `What is a Zero Trust network.md`
- `What is an LLM (large language model).md`
- `What is artificial intelligence (AI).md`
- `What is CASB  Cloud access security brokers.md`
- `What is data loss prevention (DLP).md`
- `What is DNS  How DNS works.md`
- `What is DNS Security.md`
- `What is edge computing  Benefits of the edge.md`
- `What is Envoy � envoy 1.38.0-dev-550d57 documentation.md`
- `What is Function-as-a-Service (FaaS).md`
- `What is gVisor - gVisor.md`
- `What is Istio.md`
- `What is LoRA  Low-rank adaptation.md`
- `What is routing  IP routing.md`
- `What is serverless computing.md`
- `What is SQL Injection Tutorial & Examples.md`
- `What is the Model Context Protocol (MCP).md`
- `What is the network layer  Network vs. Internet layer.md`
- `What is Zero Trust Network Access (ZTNA).md`
- `Why choose Istio.md`
- `Why use serverless computing  Pros and cons of serverless.md`

Pages updated:
- `Wiki/sources/clipping-inventory.md`
- `Wiki/sources/clipping-registry.md`
- `Wiki/sources/clipping-intake-queue.md`
