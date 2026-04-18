---
title: OWASP Web Top 10 (2021)
type: source-synthesis
tags: [security, owasp, web, api, authentication, injection]
---

# OWASP Web Top 10 (2021)

Classic web application security risks. Distinct from [[owasp-llm-top10|OWASP LLM Top 10]] but overlapping in supply chain, injection, and access control themes.

## Provenance
- Theme: web application security
- Registry entry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
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

---

## Risk Summary Table

| # | Risk | Key CWEs | Incidence | Exploit | Impact |
|---|------|----------|-----------|---------|--------|
| A01 | Broken Access Control | CWE-200, CWE-352, CWE-862 | 3.81% (318K) | 6.92 | 5.93 |
| A02 | Cryptographic Failures | CWE-259, CWE-327, CWE-331 | 4.49% (233K) | 7.29 | 6.81 |
| A03 | Injection | CWE-79, CWE-89, CWE-73 | 3.37% (274K) | 7.25 | 7.15 |
| A04 | Insecure Design | CWE-209, CWE-256, CWE-501 | 3.00% (262K) | 6.46 | 6.78 |
| A05 | Security Misconfiguration | CWE-16, CWE-611 | 4.51% (208K) | 8.12 | 6.56 |
| A06 | Vulnerable/Outdated Components | CWE-1104 | 8.77% (30K) | 5.00 | 5.00 |
| A07 | Identification/Authentication Failures | CWE-287, CWE-384, CWE-798 | 2.55% (132K) | 7.40 | 6.50 |
| A08 | Software/Data Integrity Failures | CWE-494, CWE-502, CWE-829 | 2.05% (48K) | 6.94 | 7.94 |
| A09 | Security Logging/Monitoring Failures | CWE-778, CWE-117, CWE-532 | 6.51% (54K) | 6.87 | 4.99 |
| A10 | Server-Side Request Forgery (SSRF) | CWE-918 | 2.72% (9.5K) | 8.28 | 6.72 |

---

## A01 – Broken Access Control

**Most prevalent risk**: 94% of apps tested, 318K occurrences.

### Mechanism
- Least-privilege violations: access granted beyond intended scope
- Insecure Direct Object References (IDOR): attacker changes `?acct=123` to access other accounts
- Force browsing: reaching `/admin` as a non-admin
- CORS misconfiguration: API requests from unauthorized origins
- JWT tampering: replaying or modifying tokens to escalate privileges
- POST/PUT/DELETE missing auth checks (API-only gaps)

### Prevention
- **Deny by default** for non-public resources
- Centralize access control logic (one mechanism, reused everywhere)
- Enforce record ownership in data models (not just session-level checks)
- Invalidate stateful session IDs on logout; use short-lived JWTs + OAuth revocation for long-lived tokens
- Rate-limit API endpoints; log access control failures

### Agentic Relevance
- Agent tools invoking internal APIs must carry caller identity, not just session cookies
- MCP tool calls bypass browser-level CORS — enforce authorization at the tool/function layer
- See [[../components/policy-gateway|Policy Gateway]] for runtime enforcement patterns

---

## A02 – Cryptographic Failures

Previously "Sensitive Data Exposure" — reframed to focus on root cause (bad crypto) not symptom.

### Mechanism
- Cleartext transmission (HTTP, FTP, SMTP without STARTTLS)
- Weak/deprecated algorithms: MD5, SHA1, RC4, ECB mode, PKCS#1 v1.5
- Missing key rotation; hardcoded crypto keys in source
- Insufficient entropy (predictable IVs, weak PRNG seeding)
- Unsalted password hashes: rainbow-table attackable
- Auto-decryption: DB encrypts at rest but decrypts on read, negating protection against SQL injection exfil

### Prevention
- TLS for all transport; HSTS enforced
- **Argon2 / scrypt / bcrypt / PBKDF2** for password storage (adaptive, salted, work-factor based)
- AES-GCM or ChaCha20-Poly1305 for authenticated encryption
- CSPRNG for IV/nonce generation; never reuse IV for same key
- Avoid storing sensitive data longer than required; tokenize PII

### Agentic Relevance
- Tool API keys, OAuth tokens, agent secrets all in scope
- LLM inference endpoints commonly use API keys transmitted over HTTPS — verify TLS, avoid logging keys

---

## A03 – Injection

94% of apps tested; includes SQL, NoSQL, OS command, LDAP, XSS, template injection.

### Mechanism
- **SQL injection**: string concatenation into queries (`"SELECT ... WHERE id='" + input + "'"`)
- **XSS (reflected/stored/DOM)**: unsanitized user input rendered in HTML/JS context
- **Command injection**: `os.system("cmd " + user_input)`
- **ORM injection**: HQL/ORM queries still vulnerable if not parameterized
- **SSTI (Server-Side Template Injection)**: template engines evaluate attacker-controlled expressions
- **LDAP/XPath/XQuery injection**: same pattern across interpreters

### Prevention
- Parameterized queries / prepared statements (primary defense)
- ORM with parameterization (not raw HQL string concat)
- Input validation at system boundaries (positive allowlist preferred)
- Escape special chars for residual dynamic queries
- SAST/DAST/IAST tools in CI/CD pipeline to detect injection before production

### LLM Parallel
- [[owasp-llm-top10|LLM01 Prompt Injection]] is the LLM analog of A03 — user input changes interpreter behavior
- Indirect injection via RAG vectors = stored XSS analog

---

## A04 – Insecure Design

New in 2021. Design-time failure vs. implementation defect — distinct remediation paths.

### Core Distinction
- **Insecure design**: required security controls were never architected. Can't be fixed by better code.
- **Implementation defect**: correct design, broken execution. Code fix sufficient.

### Failure Patterns
- Business logic attacks: cinema chain booking example — no rate limiting on group reservations allows mass seat exhaustion
- Bot scalping: no anti-bot design for high-demand item releases
- Insecure credential recovery: "security questions" prohibited by NIST 800-63b
- Missing trust boundary definition (CWE-501)

### Prevention
- Threat modeling integrated into sprint planning / refinement
- Paved road components (pre-approved, pre-secured building blocks)
- Misuse case modeling alongside use cases
- Tier segregation by exposure and protection classification

### Agentic Relevance
- Multi-agent orchestration needs explicit trust boundaries between agents
- Tool calls from orchestrator to sub-agents must not inherit ambient authority
- See [[../architecture/research-theses|Research Theses]] on least-privilege for agentic flows

---

## A05 – Security Misconfiguration

90% of apps tested; 4th most common by occurrence rate. Cloud-era misconfiguration is dominant vector.

### Mechanism
- Default credentials unchanged (admin/admin)
- Unnecessary services/features/ports enabled
- Verbose error messages leaking stack traces
- Missing security headers (CSP, HSTS, X-Frame-Options, etc.)
- Open S3 buckets / cloud storage with public-read ACL
- XXE via misconfigured XML parsers (CWE-611)
- Outdated framework defaults (e.g., Spring, Struts with insecure defaults)

### Prevention
- Automated hardening scripts (identical config across dev/QA/prod, different secrets)
- Minimal platform: strip unused components, samples, docs
- Security headers sent on all responses
- Cloud storage ACL audits as part of pipeline
- Infrastructure as Code (IaC) with security linting (checkov, tfsec)

### Agentic Relevance
- MCP server configs that expose all tools by default violate least-privilege
- Envoy admin interface should not be publicly exposed (see [[../components/envoy-ai-gateway|Envoy AI Gateway]])

---

## A06 – Vulnerable and Outdated Components

Highest average incidence (8.77%); only category with no CVE mapping (default 5.0 weight).

### Mechanism
- Unknown dependency versions (transitive deps especially dangerous)
- Components running with full application privileges — any flaw = full compromise
- Struts 2 RCE (CVE-2017-5638), Heartbleed, Log4Shell are classic examples
- IoT/embedded: patching impossible, exposure permanent

### Prevention
- **SCA (Software Composition Analysis)**: OWASP Dependency-Check, Snyk, Dependabot
- Monitor CVE/NVD feeds; subscribe to security bulletins for used packages
- Obtain components only from official, signed sources
- Virtual patching (WAF rules) for components that can't be updated
- Remove unused dependencies

### Agentic Relevance
- LLM supply chain (A08 overlap): Python packages for ML inference may carry vulnerabilities
- See [[owasp-llm-top10|LLM03 Supply Chain]] for model-specific supply chain risks

---

## A07 – Identification and Authentication Failures

Previously "Broken Authentication"; now includes identity failures (not just session/password).

### Mechanism
- Credential stuffing: automated login with leaked password lists
- Brute force: no lockout or rate limiting
- Weak/default passwords; no MFA
- Session ID in URL (logged in proxies, referrers)
- Session ID not regenerated after login (session fixation — CWE-384)
- Sessions not invalidated on logout or timeout
- "Knowledge-based" recovery (security questions) — prohibited by NIST 800-63b

### Prevention
- MFA everywhere (hardware tokens, TOTP, passkeys)
- Server-side session manager generating high-entropy IDs after login
- NIST 800-63b password policy: length over complexity, no forced rotation, breach-check on registration
- Same-message responses for account enumeration prevention (don't leak "user not found" vs "wrong password")
- Increasing delay on failed attempts; alert on credential stuffing patterns

### Agentic Relevance
- Agent-to-agent auth (A2AS) must not rely on shared secrets or ambient credentials
- See [[../sources/agentic-security-notes|Agentic Security Notes]] for dynamic credential patterns

---

## A08 – Software and Data Integrity Failures

New in 2021. Highest average impact weight (7.94). Covers CI/CD integrity and deserialization.

### Mechanism
- **Unsigned firmware/software updates**: no verification → attacker-supplied updates accepted
- **SolarWinds-style supply chain**: trusted build process compromised; 18K orgs received malicious update
- **Insecure deserialization**: Java `rO0` base64 payloads → RCE via Java Serial Killer
- **Insecure CI/CD**: unauthorized code injection into build pipeline (CodeCov compromise)
- **CDN dependency tampering**: loading npm/CDN assets without SRI hashes

### Prevention
- Digital signatures on all software artifacts (Sigstore, GPG, Cosign)
- Pin dependencies; use lockfiles; verify hashes
- SRI (`integrity=` attribute) on CDN script tags
- Segregated CI/CD with access control and audit trail
- Code review gates before merge to main/release branches
- Avoid deserializing untrusted data; prefer JSON over Java serialization

### LLM Parallel
- [[owasp-llm-top10|LLM03 Supply Chain]]: malicious model weights / datasets share the same integrity-failure root cause
- [[../sources/adversarial-ml|Adversarial ML]]: data poisoning during training = A08 at the ML data layer

---

## A09 – Security Logging and Monitoring Failures

Community survey #3. Hard to test; critical for breach detection.

### Mechanism
- No logs for login failures, privilege escalation, high-value transactions
- Logs stored only locally → lost on compromise
- No alerting thresholds; no incident response plan
- Log injection: attacker-controlled data written to logs without encoding
- Breach dwell time: 7+ year undetected breach (health plan case study)

### Prevention
- Log: all auth events, access control failures, input validation failures, with sufficient context (user, IP, timestamp)
- Structured logging format (JSON → SIEM ingest)
- Append-only audit tables for high-value transaction trails
- ELK/Splunk/Datadog: centralized log correlation with alert rules
- NIST 800-61r2 incident response plan
- DAST scans should trigger alerts; verify during pentest

### Agentic Relevance
- Every tool call and model decision should be traceable (trace ID, agent ID, inputs, outputs)
- Routing decisions must be logged to support evaluation (see [[../workflows/routing-evaluation-loop|Routing Evaluation Loop]])
- Log injection risk: if LLM output is written to logs without sanitization, prompt injection can corrupt audit trail

---

## A10 – Server-Side Request Forgery (SSRF)

Community #1 in survey. Low incidence (2.72%) but high exploit (8.28) and impact (6.72).

### Mechanism
- App fetches user-supplied URL without validation → attacker controls target
- Internal network scanning: determine open ports on internal hosts
- Cloud metadata exfiltration: `http://169.254.169.254/latest/meta-data/` (AWS IMDS)
- Local file inclusion: `file:///etc/passwd`
- Pivot to internal services: Redis, Elasticsearch, internal admin APIs

### Prevention (Defense in Depth)
- **Network layer**: deny-by-default egress; segment URL-fetching functionality in isolated network
- **Application layer**:
  - Validate and sanitize all URL inputs
  - Positive allowlist for URL schema + host + port
  - Disable HTTP redirects (prevent redirect-based bypass)
  - Do not return raw responses to clients
  - Awareness of DNS rebinding and TOCTOU race conditions
- **Do NOT** use deny-lists or regex alone — trivially bypassed

### Agentic Relevance
- **Critical for agentic systems**: LLM tools that fetch URLs (web search, document retrieval) are SSRF attack surfaces
- Prompt injection can coerce an agent to call `http://169.254.169.254/` via a crafted tool input
- Envoy + OPA policy can enforce egress allowlists (see [[../components/policy-gateway|Policy Gateway]])
- See [[owasp-llm-top10|LLM06 Excessive Agency]] — SSRF is a concrete exploitation path

---

## Cross-Reference: Web Top 10 ↔ LLM Top 10

| Web A0x | LLM Analog | Connection |
|---------|-----------|------------|
| A01 Broken Access Control | LLM06 Excessive Agency | Agent takes unauthorized actions due to missing authz |
| A03 Injection | LLM01 Prompt Injection | User input changes interpreter/model behavior |
| A08 Software Integrity | LLM03 Supply Chain | Model weight or package tampering |
| A10 SSRF | LLM06 Excessive Agency | Agent tool calls fetch internal URLs |
| A09 Logging Failures | LLM06 / observability gap | Missing trace = missing breach detection |
| A02 Crypto Failures | LLM02 Sensitive Disclosure | Exposed model outputs contain PII/secrets |

---

## Hackathon Checklist (Minimal Web-Safe Baseline)

For the Flask/API layer:

- [ ] All routes: verify authentication and authorization before data access (A01)
- [ ] API keys / secrets: environment variables only, never in code (A02)
- [ ] All user input: parameterized queries or ORM (A03)
- [ ] Remove debug/sample routes from production (A05)
- [ ] Log all auth failures and tool calls with context (A09)
- [ ] URL-fetching tools: validate against allowlist before request (A10)
- [ ] Python dependencies: pin with `requirements.txt` + audit via `pip-audit` (A06)
- [ ] CI: add SRI/hash verification for any CDN assets (A08)

---

## Related
- [[owasp-llm-top10|OWASP LLM Top 10 (2025)]] — LLM-specific risks
- [[adversarial-ml|Adversarial ML]] — train-time attack taxonomy
- [[infrastructure-security|Infrastructure Security]] — service mesh, OPA, Zero Trust
- [[../components/policy-gateway|Policy Gateway]] — runtime enforcement
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — rate limiting, auth at gateway layer
- [[agentic-security-notes|Agentic Security Notes]] — A2AS framework, dynamic credentials
