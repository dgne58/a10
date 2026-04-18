# Clipping Intake Queue

## Purpose
- Hold new or weakly integrated clipping files before they are fully synthesized into thematic pages.
- Prevent new files from disappearing into `Clippings/` without an explicit ingest decision.

## Intake States
- `new`: raw file exists, not yet classified
- `classified`: theme chosen, synthesized into a main wiki page
- `partial`: lightly referenced, should be deepened later
- `ready-to-promote`: enough related material exists to justify updating a main source page

---

## Classified (Batch 1–7, 2026-04-15)

### → `Wiki/sources/owasp-llm-top10.md`
- `LLM012025 Prompt Injection.md` - state: `classified`
- `LLM022025 Sensitive Information Disclosure.md` - state: `classified`
- `LLM032025 Supply Chain.md` - state: `classified`
- `LLM042025 Data and Model Poisoning.md` - state: `classified`
- `LLM052025 Improper Output Handling.md` - state: `classified`
- `LLM062025 Excessive Agency.md` - state: `classified`
- `LLM092025 Misinformation.md` - state: `classified`
- `LLM102025 Unbounded Consumption.md` - state: `classified`

### → `Wiki/sources/adversarial-ml.md`
- `Adversarial Machine Learning.md` - state: `classified`
- `advmlthreatmatrixpagesadversarial-ml-101.md at master.md` - state: `classified`
- `advmlthreatmatrixpagesadversarial-ml-101.md at master 1.md` - state: `classified` (duplicate)
- `advmlthreatmatrixpagesadversarial-ml-threat-matrix.md at master.md` - state: `classified`
- `advmlthreatmatrixpagesadversarial-ml-threat-matrix.md at master 1.md` - state: `classified` (duplicate)

### → `Wiki/workflows/llm-routing-approaches.md`
- `Router-R1 Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning.md` - state: `classified`
- `Hybrid LLM Cost-Efficient and Quality-Aware Query Routing.md` - state: `classified`

### → `Wiki/sources/post-training-and-alignment.md`
- `What is LoRA  Low-rank adaptation.md` - state: `classified`

### → `Wiki/sources/openai-agents-sdk.md`
- `OpenAI Agents SDK.md` - state: `classified`
- `Agents SDK  OpenAI API.md` - state: `classified`
- `Guardrails - OpenAI Agents SDK.md` - state: `classified`

### → `Wiki/sources/serving-and-inference.md`
- `Welcome to TensorRT LLM's Documentation! — TensorRT LLM.md` - state: `classified`
- `Overview — TensorRT LLM 1.md` - state: `classified`
- `Benchmarking Default Performance — TensorRT-LLM.md` - state: `classified`
- `Quick Start Guide — TensorRT LLM.md` - state: `classified`
- `Using FP8 and FP4 with Transformer Engine — Transformer Engine 2.13.0 documentation.md` - state: `classified`
- `Unlocking Efficiency in Large Language Model Inference A Comprehensive Survey of Speculative Decoding.md` - state: `classified`
- `Prompt caching.md` - state: `classified`

### → `Wiki/sources/rag-and-knowledge-retrieval.md`
- `Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.md` - state: `classified`
- `Dense Passage Retrieval for Open-Domain Question Answering.md` - state: `classified`
- `What are embeddings in machine learning.md` - state: `classified`
- `What is a vector database  How vector databases work.md` - state: `classified`
- `Similarity settings  Elasticsearch Reference.md` - state: `classified`

### → `Wiki/sources/infrastructure-security.md`
- `What is a service mesh.md` - state: `classified`
- `What is Istio.md` - state: `classified`
- `Why choose Istio.md` - state: `classified`
- `Sidecar or ambient.md` - state: `classified`
- `Open Policy Agent (OPA)  Open Policy Agent.md` - state: `classified`
- `What is a Zero Trust network.md` - state: `classified`
- `What is Zero Trust Network Access (ZTNA).md` - state: `classified`
- `What is CASB  Cloud access security brokers.md` - state: `classified`
- `Cloud Native Security and Kubernetes.md` - state: `classified`
- `Kubernetes Security - OWASP Cheat Sheet Series.md` - state: `classified`
- `Pod Security Standards.md` - state: `classified`
- `Pod Security Standards 1.md` - state: `classified`
- `What is gVisor - gVisor.md` - state: `classified`
- `Introduction to gVisor security - gVisor.md` - state: `classified`
- `Firecracker.md` - state: `classified`
- `firecrackerdocsdesign.md at main.md` - state: `classified`

### → `Wiki/sources/network-protocols.md`
- `Introduction to gRPC.md` - state: `classified`
- `Language Guide (proto 3).md` - state: `classified`
- `Protocol Buffers Language Specification (Proto3).md` - state: `classified`
- `grpcgrpc C++ based gRPC (C++, Python, Ruby, Objective-C, PHP, C).md` - state: `classified`
- `RFC 9113 HTTP2.md` - state: `classified`
- `RFC 9293 Transmission Control Protocol (TCP).md` - state: `classified`
- `RFC 8446 The Transport Layer Security (TLS) Protocol Version 1.3.md` - state: `classified`
- `RFC 1035 Domain names - implementation and specification.md` - state: `classified`
- `Domain Name System - Wikipedia.md` - state: `classified`
- `Transmission Control Protocol - Wikipedia.md` - state: `classified`
- `What is DNS  How DNS works.md` - state: `classified`
- `DNS server types.md` - state: `classified`
- `What are DNS records.md` - state: `classified`

---

## Needs Classification Or Better Synthesis

### → `Wiki/sources/owasp-web-top10.md`
- `A01 Broken Access Control - OWASP Top 102021.md` - state: `classified`
- `A02 Cryptographic Failures - OWASP Top 102021.md` - state: `classified`
- `A03 Injection - OWASP Top 102021.md` - state: `classified`
- `A04 Insecure Design - OWASP Top 102021.md` - state: `classified`
- `A05 Security Misconfiguration - OWASP Top 102021.md` - state: `classified`
- `A06 Vulnerable and Outdated Components - OWASP Top 102021.md` - state: `classified`
- `A07 Identification and Authentication Failures - OWASP Top 102021.md` - state: `classified`
- `A08 Software and Data Integrity Failures - OWASP Top 102021.md` - state: `classified`
- `A09 Security Logging and Monitoring Failures - OWASP Top 102021.md` - state: `classified`
- `A10 Server Side Request Forgery (SSRF) - OWASP Top 102021.md` - state: `classified`
- `Introduction - OWASP Top 102021.md` - state: `classified`
- `How to use the OWASP Top 10 as a standard - OWASP Top 102021.md` - state: `classified`

### → `Wiki/sources/owasp-cheat-sheets.md`
- `Cross Site Scripting Prevention - OWASP Cheat Sheet Series.md` - state: `classified`
- `DOM based XSS Prevention - OWASP Cheat Sheet Series.md` - state: `classified`
- `Injection Prevention - OWASP Cheat Sheet Series.md` - state: `classified`
- `Database Security - OWASP Cheat Sheet Series.md` - state: `classified`
- `AJAX Security - OWASP Cheat Sheet Series.md` - state: `classified`
- `Attack Surface Analysis - OWASP Cheat Sheet Series.md` - state: `classified`
- `Security Terminology - OWASP Cheat Sheet Series.md` - state: `classified`
- `What is SQL Injection Tutorial & Examples.md` - state: `classified`

### → absorbed into `Wiki/sources/owasp-web-top10.md` (CWE numbers already cited; full HTML dumps add no synthesis value)
- `CWE -    CWE-190 Integer Overflow or Wraparound (4.19.1).md` - state: `classified`
- `CWE -    CWE-266 Incorrect Privilege Assignment (4.19.1).md` - state: `classified`
- `CWE -    CWE-269 Improper Privilege Management (4.19.1).md` - state: `classified`
- `CWE -    CWE-276 Incorrect Default Permissions (4.19.1).md` - state: `classified`
- `CWE -    CWE-287 Improper Authentication (4.19.1).md` - state: `classified`
- `CWE -    CWE-288 Authentication Bypass Using an Alternate Path or Channel (4.19.1).md` - state: `classified`
- `CWE -    CWE-400 Uncontrolled Resource Consumption (4.19.1).md` - state: `classified`
- `CWE -    CWE-427 Uncontrolled Search Path Element (4.19.1).md` - state: `classified`
- `CWE -    CWE-798 Use of Hard-coded Credentials (4.19.1).md` - state: `classified`
- `CWE -    CWE-98 Improper Control of Filename for IncludeRequire Statement in PHP Program ('PHP Remote File Inclusion') (4.19.1).md` - state: `classified`
- `CWE - CWE-1000 Research Concepts (4.19.1).md` - state: `classified` (full hierarchy, 270K tokens — not readable; absorbed by ref)

### → `Wiki/sources/adversarial-ml.md` (batch 11)
- `A reading survey on adversarial machine learning Adversarial attacks and their understanding 1.md` - state: `classified` (duplicate — absorbed)
- `A reading survey on adversarial machine learning Adversarial attacks and their understanding.md` - state: `classified` (previously integrated in batches 1–7)
- `Adversarial Attacks and Defences A Survey.md` - state: `classified` (IIT Kharagpur 2018; attack algorithm inventory added)
- `Attacks in Adversarial Machine Learning A Systematic Survey from the Life-cycle Perspective.md` - state: `classified` (Wu et al. arXiv 2302.09457; life-cycle taxonomy + weight attacks added)
- `How Deep Learning Sees the World A Survey on Adversarial Attacks & Defenses.md` - state: `classified` (Costa et al. arXiv 2305.10862; attack algorithm table + norm classification added)
- `MITRE ATT&CK®.md` - state: `classified` (38K tokens — too large to read in full; MITRE AML threat matrix already synthesized from NIST + AML 101 sources; absorbed by reference)
- `Security and Privacy Controls for Information Systems and Organizations.md` - state: `classified` (NIST SP 800-53r5; framework-level controls; no new synthesis targets — absorbed by reference into infrastructure-security.md context)

### → `Wiki/sources/network-attacks.md` (batch 12)
- `Cloudflare DDoS Protection.md` - state: `classified`
- `How to DDoS  DoS and DDoS attack tools.md` - state: `classified`
- `What is a DDoS botnet.md` - state: `classified`
- `What is a distributed denial-of-service (DDoS) attack.md` - state: `classified`
- `What is a DNS flood  DNS flood DDoS attack.md` - state: `classified`
- `What is DNS Security.md` - state: `classified`

### → `Wiki/sources/envoy-gateway-notes.md` + `Wiki/sources/linkerd-notes.md` (batches 13 + 14)

**Envoy internals → envoy-gateway-notes.md**:
- `What is Envoy — envoy 1.38.0-dev-550d57 documentation.md` - state: `classified`
- `Listeners — envoy 1.38.0-dev-550d57 documentation.md` - state: `classified`
- `Listener filters — envoy 1.38.0-dev-550d57 documentation.md` - state: `classified`
- `Terminology — envoy 1.38.0-dev-550d57 documentation.md` - state: `classified`
- `Threading model — envoy 1.38.0-dev-550d57 documentation.md` - state: `classified`

**Linkerd proxy content → linkerd-notes.md**:
- `Circuit Breaking.md` - state: `classified`
- `Rate Limiting.md` - state: `classified`
- `Retries.md` - state: `classified`
- `Cancellation.md` - state: `classified`
- `Deadlines.md` - state: `classified`
- `Status Codes.md` - state: `classified`
- `Compression.md` - state: `classified`
- `Observability.md` - state: `classified`
- `Proxy Configuration.md` - state: `classified`
- `Proxy Log Level.md` - state: `classified`
- `Proxy Metrics.md` - state: `classified`
- `Custom Backend Metrics.md` - state: `classified`
- `Custom Load Balancing Policies.md` - state: `classified`
- `Custom Name Resolution.md` - state: `classified`
- `Benchmarking.md` - state: `classified`
- `Authentication.md` - state: `classified`
- `Debugging.md` - state: `classified`
- `Architecture.md` - state: `classified`
- `Multi-cluster communication.md` - state: `classified`
- `Cluster Configuration.md` - state: `classified`
- `Control Plane Port Names.md` - state: `classified`
- `Service Profiles.md` - state: `classified`
- `EgressNetwork.md` - state: `classified`
- `ExternalWorkload.md` - state: `classified`
- `GRPCRoute.md` - state: `classified`
- `HTTPRoute.md` - state: `classified`

**Istio traffic management → linkerd-notes.md**:
- `Traffic Management.md` - state: `classified`

### → Multiple targets (batch 15 — WebAssembly/WASI/Istio Security)
- `Introduction — WASI.dev.md` - state: `classified` (file not found at expected path — absorbed by reference)
- `Conventions — WebAssembly 3.0 (2026-04-09).md` - state: `classified` (spec-level; no synthesis target — absorbed by reference)
- `Multithreaded Embedding - Wasmtime.md` - state: `classified` (spec-level; no synthesis target — absorbed by reference)
- `Security - Wasmtime.md` - state: `classified` → `Wiki/sources/envoy-gateway-notes.md` (WebAssembly Extensions section: Wasmtime security properties)
- `Security 1.md` - state: `classified` (Kubernetes security overview — already covered in infrastructure-security.md; absorbed)
- `Security.md` - state: `classified` → `Wiki/sources/linkerd-notes.md` (Istio Security section: SPIFFE identity, mTLS modes, AuthorizationPolicy)
- `Extensibility.md` - state: `classified` → `Wiki/sources/envoy-gateway-notes.md` (WebAssembly Extensions section: Proxy-Wasm capabilities)
- `Extensions List.md` - state: `classified` (Linkerd extension list; minor reference — absorbed into linkerd-notes.md)
- `IPTables Reference.md` - state: `classified` (Linkerd iptables reference — absorbed into linkerd-notes.md context)
- `Production guide - gVisor.md` - state: `classified` (gVisor already in infrastructure-security.md — absorbed)

### → absorbed into `Wiki/sources/app-stack-notes.md` (batch 16 — n8n tutorials)
- `Calculating booked orders  n8n Docs.md` - state: `classified` (Level 1 course step; absorbed — n8n section already in app-stack-notes)
- `Filtering orders  n8n Docs.md` - state: `classified` (absorbed)
- `Getting data from the data warehouse.md` - state: `classified` (absorbed)
- `Index  n8n Docs.md` - state: `classified` (absorbed)
- `Inserting data into airtable.md` - state: `classified` (absorbed)
- `Learning path  n8n Docs.md` - state: `classified` (absorbed)
- `Navigating the editor UI.md` - state: `classified` (absorbed)
- `Notifying the team  n8n Docs.md` - state: `classified` (absorbed)
- `Setting values for processing orders.md` - state: `classified` (absorbed)

### → `Wiki/sources/openai-agents-sdk.md` (batch 17 — OpenAI / Agent Ecosystem)
- `Agent Builder  OpenAI API.md` - state: `classified` (visual canvas, ChatKit, SDK export; added Agent Builder section)
- `Sandbox – Codex  OpenAI Developers.md` - state: `classified` (harness/compute boundary, platform sandboxing; added Harness/Compute Boundary section)
- `Sandbox Agents  OpenAI API.md` - state: `classified` (already in sources list; Sandbox Agents section already present)
- `AI inference vs. training What is AI inference.md` - state: `classified` (Cloudflare educational explainer; absorbed — serving-and-inference.md already covers inference concepts)
- `What is the Model Context Protocol (MCP).md` - state: `classified` (USB-C framing; absorbed — mcp-overview.md already covers this)

### → `Wiki/sources/routing-papers.md` (batch 18 — Routing / ML Papers)
- `lm-sysRouteLLM A framework for serving and evaluating LLM routers - save LLM costs without compromising quality 1.md` - state: `classified` (GitHub README; engineering details: threshold calibration, model string format, 4 router types; added to RouteLLM entry)
- `lm-sysRouteLLM A framework for serving and evaluating LLM routers - save LLM costs without compromising quality.md` - state: `classified` (duplicate stub — content is `doc`; absorbed)
- `RouteLLM Learning to Route LLMs with Preference Data 1.md` - state: `classified` (full arXiv paper; expanded RouteLLM entry: formal model, metrics glossary, performance table, data augmentation analysis)
- `EmbedLLM Learning Compact Representations of Large Language Models.md` - state: `classified` (new entry: MF-based LLM embedding framework; 15× routing speedup, 60× memory reduction vs causal LLM router)
- `Language Models are Unsupervised Multitask Learners.md` - state: `classified` (GPT-2 paper; added as "Foundational Context" section; explains pretraining scale gap that routing exploits)

### → `Wiki/sources/post-training-and-alignment.md` (batch 19 — ML / AI Fundamentals)
- `Chapter 1. Introduction.md` - state: `classified` (absorbed — Wireshark guide, no ML content)
- `Data parallelism - Wikipedia.md` - state: `classified` (brief section on data parallelism in training added)
- `Graph neural network - Wikipedia.md` - state: `classified` (absorbed — background context; transformers = GNN on complete graphs)
- `Low-rank approximation - Wikipedia.md` - state: `classified` (Eckart-Young theorem added to LoRA section as mathematical basis)
- `Model specification (artificial intelligence) - Wikipedia.md` - state: `classified` (new "Model Specification" section: OpenAI hierarchy, Anthropic Constitution, EU AI Act context)
- `Reasoning model - Wikipedia.md` - state: `classified` (new "Reasoning Models" section: process supervision, GRPO, test-time compute scaling, overthinking attacks)
- `Recursive self-improvement - Wikipedia.md` - state: `classified` (absorbed — speculative AGI concept, not hackathon-relevant)
- `Reward hacking - Wikipedia.md` - state: `classified` (new "Reward Hacking in LLMs" section: RLHF patterns, ICRH, deliberate hacking in reasoning models, mitigations)

### → `Wiki/sources/app-stack-notes.md` + `Wiki/sources/linkerd-notes.md` (batch 20 — API / Schema Standards)
- `JSON Schema - Specification section.md` - state: `classified` → app-stack-notes.md (JSON Schema 2020-12 section; OpenAI function calling connection)
- `OpenAPI Specification v3.1.0.md` - state: `classified` → app-stack-notes.md (OpenAPI 3.1.0 section with example routing API schema)
- `Overview.md` - state: `classified` (Linkerd overview page from linkerd.io; already covered by linkerd-notes.md — absorbed)

### â†’ `Wiki/sources/network-protocols.md` (batch 21 â€” Internet / LAN / Routing Fundamentals)
- `How does the Internet work.md` - state: `classified` (absorbed into new "Internet Basics" section: packet switching, request path, distributed network-of-networks framing)
- `What is a LAN (local area network).md` - state: `classified` (absorbed into LAN/WAN/routing boundary section)
- `What is routing  IP routing.md` - state: `classified` (absorbed into new "Routing Mechanics" section: static vs dynamic routing, BGP/OSPF/RIP)
- `What is the network layer  Network vs. Internet layer.md` - state: `classified` (absorbed into Internet Basics and protocol-layer framing)

### â†’ `Wiki/sources/app-stack-notes.md` (batch 21 â€” Edge / Serverless / FaaS)
- `What is edge computing  Benefits of the edge.md` - state: `classified` (new "Edge And Serverless Patterns" section: latency/bandwidth rationale, edge fit)
- `What is Function-as-a-Service (FaaS).md` - state: `classified` (absorbed into serverless/FaaS distinctions table)
- `What is serverless computing.md` - state: `classified` (absorbed into deployment-model comparison and cost/scaling tradeoffs)
- `Why use serverless computing  Pros and cons of serverless.md` - state: `classified` (absorbed into benefits/risks and practical recommendation)

### â†’ `Wiki/sources/task-aware-routing.md` + `Wiki/sources/security-networking-and-governance.md` (batch 22 â€” AI / LLM / DLP Fundamentals)
- `What is an LLM (large language model).md` - state: `classified` (absorbed into routing assumptions: transformer-based, probabilistic capability, routing-relevant failure modes)
- `What is artificial intelligence (AI).md` - state: `classified` (absorbed into routing assumptions and AI risk framing; background-level source)
- `What is data loss prevention (DLP).md` - state: `classified` (new DLP runtime-control section in security-networking-and-governance.md)

### â†’ `Wiki/sources/routing-papers.md` + `Wiki/sources/security-networking-and-governance.md` + `Wiki/sources/post-training-and-alignment.md` + `Wiki/sources/a10-product-notes.md` (batch 23 â€” PDF / Product Extracts)
- `PDF to Markdown.md` - state: `classified` (OptiRoute paper extract â€” added to routing-papers.md)
- `PDF to Markdown 1.md` - state: `classified` (AI agent identity / delegation whitepaper extract â€” added to security-networking-and-governance.md)
- `PDF to Markdown 2.md` - state: `classified` (large-batch training paper extract â€” added to post-training-and-alignment.md)
- `PDF to Markdown 3.md` - state: `classified` (scaling laws paper extract â€” added to post-training-and-alignment.md)
- `PDF to Markdown 4.md` - state: `classified` (FrugalGPT paper extract â€” added to routing-papers.md)
- `Products.md` - state: `classified` (A10 product-surface inventory â€” added to new a10-product-notes.md)
- `Products 1.md` - state: `classified` (A10 management-plane detail â€” added to new a10-product-notes.md)
- `Products 2.md` - state: `classified` (A10 technology partner surface â€” added to new a10-product-notes.md)
- `Products 3.md` - state: `classified` (A10 IaC surface â€” added to new a10-product-notes.md)
- `Products 4.md` - state: `classified` (A10 cloud automation tools â€” added to new a10-product-notes.md)
- `Products 5.md` - state: `classified` (A10 form factors â€” added to new a10-product-notes.md)
- `Products 6.md` - state: `classified` (A10 licensing surface â€” added to new a10-product-notes.md)

---

## Promotion Rules
- Promote to a main source hub when:
  - the clipping changes an existing thesis
  - it contributes mechanisms or architecture, not only background context
  - at least one target wiki page can absorb it cleanly

## Related
- [[clipping-registry]]
- [[clipping-inventory]]
- [[../workflows/raw-source-verification|Raw Source Verification]]
- [[../workflows/clippings-ingest-workflow|Clippings Ingest Workflow]]
