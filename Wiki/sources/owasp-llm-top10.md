---
tags: [security, llm, owasp, agentic, prompt-injection, supply-chain, sources]
last_updated: 2026-04-15
---

# OWASP LLM Top 10 (2025)

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Clippings/LLM012025 Prompt Injection.md`
- `Clippings/LLM022025 Sensitive Information Disclosure.md`
- `Clippings/LLM032025 Supply Chain.md`
- `Clippings/LLM042025 Data and Model Poisoning.md`
- `Clippings/LLM052025 Improper Output Handling.md`
- `Clippings/LLM062025 Excessive Agency.md`
- `Clippings/LLM092025 Misinformation.md`
- `Clippings/LLM102025 Unbounded Consumption.md`

---

## Overview

The OWASP LLM Top 10 (2025 edition) defines the ten most critical vulnerabilities in LLM-integrated systems. These complement—and in many cases extend—the classic OWASP Web Top 10 with LLM-specific threat patterns.

Most relevant to this project: LLM01 (prompt injection), LLM06 (excessive agency), and LLM10 (unbounded consumption) map directly to the agentic security and routing tracks.

---

## LLM01: Prompt Injection

### What it is
User prompts (or injected content in retrieved data) alter the LLM's behavior in unintended ways. Inputs need not be human-readable — the model parses them.

### Types
| Type | Description |
|------|-------------|
| **Direct injection** | User's prompt directly overrides system instructions |
| **Indirect injection** | Malicious instructions hidden in external content (webpages, documents, tool results) that the LLM reads |
| **Jailbreaking** | A subclass of injection that bypasses safety constraints entirely |
| **Multimodal injection** | Instructions hidden in images processed by multimodal models |
| **Adversarial suffix** | Appended token strings that trigger unexpected behavior |
| **Multilingual/obfuscated** | Base64, emoji, or cross-language encoding to bypass filters |

### Why RAG and fine-tuning don't fully solve it
- RAG increases the attack surface (attacker controls document content)
- Fine-tuned safety filters don't generalize to all injection vectors
- Both increase the probability of indirect injection (more content surfaces)

### Defenses
1. Constrain model behavior via system prompt with explicit capability limits
2. Define and validate output formats; use deterministic validation
3. Input/output semantic filtering + RAG Triad checks
4. **Privilege control and least privilege**: API tokens for tools should be in code, not in the model
5. **Human-in-the-loop** for privileged operations
6. Segregate untrusted external content clearly
7. Adversarial testing and red-teaming

### Connection to agentic systems
Indirect injection is especially dangerous when the agent reads tool outputs or retrieves documents — these may contain attacker-controlled content that redirects agent actions.

---

## LLM02: Sensitive Information Disclosure

### What it is
LLM outputs expose PII, financial data, credentials, proprietary algorithms, or training data.

### Key mechanisms
- **Training data memorization**: Model memorizes and reproduces sensitive training examples
- **Model inversion attacks**: Disclosed training data enables reconstruction of inputs
- **System prompt leakage**: Model reveals its own instructions
- **Cross-user contamination**: Inadequate session isolation leaks one user's data to another

### Defenses
- Data sanitization before training (scrub PII, credentials)
- Input validation to filter sensitive data entering context
- Least-privilege access to external data sources
- Differential privacy in training
- System prompt: explicitly forbid output of certain data types (imperfect — can be bypassed)

---

## LLM03: Supply Chain

### What it is
Attacks targeting the model, training data, dependencies, or deployment platform — analogous to software supply chain attacks but extended to ML artifacts.

### LLM-specific supply chain risks
| Vector | Description |
|--------|-------------|
| Vulnerable pretrained model | Backdoors or biases in base model (PoisonGPT scenario) |
| Malicious LoRA adapter | Compromised fine-tuning adapter injected via vLLM/OpenLLM |
| Model merge poisoning | Collaborative merges on HuggingFace used to inject malicious behavior |
| Malicious pickling | Executable code embedded in `.pkl`-format model weights |
| PyPI/npm package compromise | Vulnerable Python/JS dependencies used during ML dev |
| GPU memory leakage (LeftoverLocals) | Sensitive data leaked from GPU VRAM across processes |
| On-device model tampering | Mobile apps repackaged with tampered model weights |

### Defenses
1. SBOM (Software Bill of Materials) including ML artifacts (OWASP CycloneDX)
2. Model integrity verification (hash + signing)
3. Vet HuggingFace models rigorously before use
4. Use AI Red Teaming on third-party models before deployment
5. Patch vulnerable dependencies; maintain inventory

---

## LLM04: Data and Model Poisoning

### What it is
Manipulation of training data or model weights to introduce backdoors, biases, or exploitable behaviors.

### Attack vectors
| Vector | Mechanism |
|--------|-----------|
| Split-view poisoning | Different data shown to validators vs training pipeline |
| Frontrunning poisoning | Insert malicious data before it can be reviewed |
| Backdoor injection | Trigger-based: model behaves normally except when specific input triggers it |
| RAG poisoning | Poison the retrieval corpus, not the model weights |
| Fine-tuning removal of RLHF | Fine-tune to remove alignment (documented with GPT-4) |
| Sleeper agent | Model appears aligned during training, activates maliciously later |

### Defenses
- Data version control (DVC) + anomaly detection on training data
- Strict sandboxing during training
- ML-BOM (OWASP CycloneDX) for data provenance tracking
- Test with adversarial techniques + red-team during inference
- RAG: use grounding and source verification to reduce hallucination paths

---

## LLM05: Improper Output Handling

### What it is
LLM outputs passed downstream without sanitization or validation → XSS, SSRF, SQL injection, RCE, path traversal.

### Key risk factors
- LLM granted privileges beyond end-user scope (privilege escalation via output)
- Third-party extensions don't validate LLM-generated inputs
- Output used as-is in shells, SQL queries, email templates, file paths

### Attack patterns
| Output destination | Risk |
|-------------------|------|
| `exec()` / shell | Remote code execution |
| HTML render | XSS (JavaScript injection) |
| SQL query builder | SQL injection |
| File path construction | Path traversal |
| Email template | Phishing / XSS |
| Code generation suggestion | Package hallucination → malware |

### Defenses
1. Treat LLM output as untrusted user input (zero-trust to model)
2. Context-aware output encoding (HTML-escape for web, parameterized for SQL)
3. CSP headers to mitigate XSS from LLM-generated content
4. OWASP ASVS validation guidelines
5. Logging and anomaly detection on LLM outputs

---

## LLM06: Excessive Agency

### What it is
An LLM agent causes damaging actions due to hallucination, ambiguous prompts, or adversarial manipulation — enabled by excessive functionality, permissions, or autonomy.

### Root causes
| Root cause | Example |
|-----------|---------|
| Excessive functionality | Extension exposes delete/modify when only read is needed |
| Excessive permissions | Read-only agent connects with identity having INSERT/DELETE rights |
| Excessive autonomy | High-impact actions taken without human confirmation |
| Stale/unused plugins | Old extension left attached to agent after being superseded |

### Key principle: the agent's blast radius = its capabilities × its permissions × its autonomy
Reduce all three independently.

### Defenses
1. **Least-privilege extensions**: Only expose functions needed for the task
2. **Least-privilege identities**: Agents authenticate with minimal-scope credentials (OAuth with read-only scopes)
3. **Track user authorization**: Actions on behalf of user should run with that user's scope only
4. **Human-in-the-loop**: Require approval for high-impact operations
5. **Downstream authorization**: Enforce in the system being called, not just in the LLM layer
6. **Rate limiting**: Slows damage even if controls are partially bypassed
7. **Monitoring and logging**: Detect and respond to abnormal tool call patterns

### Connection to policy gateway
LLM06 directly defines why the [[../components/policy-gateway|Policy Gateway]] component exists. The gateway implements the downstream authorization, human approval paths, and rate limiting that mitigate this risk.

---

## LLM09: Misinformation

### What it is
LLM produces plausible but false or misleading information (hallucinations, fabricated citations, biased outputs).

### Key risk patterns
- Factual inaccuracies in high-stakes domains (healthcare, legal)
- Package hallucination → developers install malware-infected libraries
- Fabricated legal citations used in proceedings
- Overreliance: users fail to cross-check because output seems authoritative

### Defenses
- RAG with verified knowledge bases to ground responses
- Fine-tuning on domain-specific, high-quality data
- Human oversight for high-stakes outputs
- Automatic validation for key claims
- Clear UI labeling of AI-generated content and its limitations

---

## LLM10: Unbounded Consumption (DoS / DoW / Model Theft)

### What it is
Uncontrolled inference volume → resource exhaustion, financial attack (Denial of Wallet), or model extraction.

### Attack patterns
| Pattern | Mechanism |
|---------|-----------|
| Variable-length flood | Many requests of varying lengths exhaust memory/CPU |
| Denial of Wallet (DoW) | High request volume against pay-per-token API runs up cost |
| Continuous context overflow | Inputs exceed context window → excessive compute |
| Resource-intensive queries | Complex patterns trigger LLM's worst-case processing |
| Model extraction via API | Repeated careful queries reconstruct model behavior |
| Functional replication | Use model to generate synthetic training data for a shadow model |
| Side-channel attacks | Exploit input filtering to leak model weights or architecture |

### Defenses
1. Rate limiting and user quotas
2. Input size limits and context window capping
3. Timeout and throttling on expensive operations
4. Sandbox techniques: restrict LLM network access
5. Restrict/obfuscate `logit_bias` and `logprobs` in API responses
6. Watermarking to detect unauthorized model replication
7. Graceful degradation under load
8. Anomaly detection for unusual query patterns

---

## Threat → Control Mapping for Agentic Systems

| OWASP Risk | Agentic Control Point |
|-----------|----------------------|
| LLM01 (prompt injection) | Input sanitization at perception layer; indirect content segregation |
| LLM02 (information disclosure) | Data sanitization; least privilege on retrieval |
| LLM03 (supply chain) | Model provenance verification; SBOM |
| LLM04 (poisoning) | Training data versioning; RAG grounding |
| LLM05 (improper output) | Zero-trust output validation; parameterized downstream calls |
| LLM06 (excessive agency) | Least-privilege tools; human approval for high-risk actions |
| LLM09 (misinformation) | RAG grounding; human oversight for critical outputs |
| LLM10 (unbounded consumption) | Rate limiting; input size limits; resource monitoring |

---

## Related
- [[owasp-web-top10|OWASP Web Top 10 (2021)]] — classic web app risks; cross-reference table in that page
- [[agentic-security-notes]] — runtime security framework, A2AS, dynamic credentials
- [[../components/policy-gateway|Policy Gateway]] — implementation of LLM06 controls
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — network-layer rate limiting, RBAC on tool calls
- [[security-networking-and-governance]] — broader threat landscape
- [[adversarial-ml]] — technical attacks on model weights and training data
