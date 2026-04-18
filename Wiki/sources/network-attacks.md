---
title: Network Attacks — DDoS and DNS
type: source-synthesis
tags: [security, ddos, dns, network, botnet, cloudflare, sources]
last_updated: 2026-04-15
---

# Network Attacks — DDoS and DNS

Operational reference synthesizing Cloudflare learning content on DDoS attack types, DNS-based attacks, and mitigation techniques. Complements [[infrastructure-security|Infrastructure Security]] with network-layer threat patterns.

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Cloudflare DDoS Protection.md`
- `How to DDoS  DoS and DDoS attack tools.md`
- `What is a DDoS botnet.md`
- `What is a distributed denial-of-service (DDoS) attack.md`
- `What is a DNS flood  DNS flood DDoS attack.md`
- `What is DNS Security.md`

---

## 1. DDoS Attack Overview

A **distributed denial-of-service (DDoS) attack** overwhelms a target server/service/network with traffic from many compromised machines (a **botnet**). The distributed nature makes it hard to distinguish attack traffic from legitimate traffic.

**Botnet structure**:
- Devices infected with malware become **bots** (zombies)
- An attacker (bot herder) remotely commands the botnet via C2 channel
- Self-propagating botnets recruit additional bots (exploit website vulns, Trojans, weak auth)
- Modern IoT botnets (Mirai, Meris) leverage cameras, DVRs, routers for high-bandwidth attacks

---

## 2. DDoS Attack Types by OSI Layer

| Layer | Category | Example Attacks |
|-------|----------|----------------|
| **L7 — Application** | Exhaust server resource generating responses | HTTP flood, HTTPS flood |
| **L3/4 — Protocol** | Exhaust state tables on firewalls, load balancers | SYN flood, ACK flood, IP fragmentation |
| **L3/4 — Volumetric** | Consume all available bandwidth | DNS amplification, UDP flood, ICMP flood |

### L7 — HTTP Flood
- Client sends massive GET/POST requests; server must execute queries and load files for each
- Hard to distinguish from legitimate traffic spike
- Complex variants use randomized IPs, referrers, user agents, and random URLs

### L3/4 — SYN Flood
- Exploits TCP 3-way handshake: attacker sends SYN packets with **spoofed source IPs**
- Server sends SYN-ACK and waits for final ACK that never arrives → half-open connections exhaust server state table
- Defense: SYN cookies (server validates via cookie before allocating state)

### L3/4 — DNS Amplification
- Attacker sends small DNS queries to **open resolvers** with **victim's spoofed source IP**
- DNS resolver sends large responses (e.g., ANY record) to victim
- Amplification factor: up to 70×; requires only small attacking bandwidth
- Distinct from DNS flood: flood uses direct botnet bandwidth; amplification leverages reflection

---

## 3. DNS-Specific Attack Taxonomy

| Attack | Mechanism | Impact |
|--------|-----------|--------|
| **DNS spoofing / cache poisoning** | Inject forged records into resolver cache | Redirect traffic to malicious servers |
| **DNS tunneling** | Encode data (SSH, HTTP, malware) inside DNS queries/responses | Bypass firewalls; exfiltrate data via DNS |
| **DNS hijacking** | Redirect queries to rogue nameserver (via malware or unauthorized NS modification) | Intercept all traffic for a domain |
| **NXDOMAIN flood** | Flood DNS server with queries for nonexistent records | Exhaust resolver; DoS for legitimate lookups |
| **Phantom domain attack** | Resolver flooded with queries to ghost servers that respond slowly | Ties up resolver waiting for responses |
| **Random subdomain attack** | Many queries for random nonexistent subdomains of legitimate domain | DoS authoritative nameserver; corrupts resolver cache |
| **DNS flood (IoT botnet)** | High-bandwidth IoT devices flood DNS provider directly | Overwhelm DNS provider without amplification |
| **Domain lock-up attack** | Attacker's domains respond with slow random packets to legitimate resolvers | Ties up resolver TCP connections |
| **Botnet CPE attack** | Compromised CPE (modem/router/cable box) perform random subdomain attacks | Distributed attack from ISP infrastructure |

**Key distinction**:
- DNS spoofing = corrupts **resolver cache** (resolver is the victim)
- DNS hijacking = modifies **authoritative NS record** or redirects queries to rogue NS (registry/zone is the victim)

---

## 4. DNS Security Controls

### DNSSEC (DNS Security Extensions)
- Adds **digital signatures** to DNS records at each delegation level
- Chain of trust: root zone → TLD (.com) → authoritative NS for domain
- Protects against cache poisoning and spoofing (cannot verify modified records)
- Backwards-compatible; designed to work alongside TLS/SSL
- Root Zone Signing Ceremony: humans physically sign root DNSKEY in public audited event

### DNS Privacy
- Standard DNS queries travel in **plaintext** → eavesdroppers see all visited domains
- **DoT (DNS over TLS)**: encrypts DNS over TCP port 853
- **DoH (DNS over HTTPS)**: encrypts DNS inside HTTPS traffic on port 443 (harder to block)

### DNS Firewall
- Sits between recursive resolver and authoritative NS
- Provides: rate limiting, attack traffic blocking, cached response serving during outages
- Also: content filtering (block malware/phishing domains), botnet protection (block known C2 domains)

### Infrastructure Hardening
- Over-provision: nameservers sized for multiples of expected peak traffic
- Redundant DNS servers across multiple providers and geographies
- Load balancing across healthy DNS instances
- Anycast routing: route DNS traffic to nearest PoP to dilute volumetric attacks

---

## 5. Cloudflare DDoS Protection Architecture

Cloudflare's defense is **autonomous** — real-time detection + mitigation without manual intervention.

| Feature | Description |
|---------|-------------|
| **Managed Rulesets** | Dynamic rules for L3/4 and L7; customizable sensitivity |
| **Adaptive DDoS Protection** | Learns traffic baselines; adapts to sophisticated attacks |
| **Advanced TCP Protection** | Detects out-of-state TCP attacks (randomized/spoofed ACK, SYN-ACK floods) |
| **Advanced DNS Protection** | Handles fully randomized DNS attacks (random prefix attacks) |
| **Programmable Flow Protection** | Custom eBPF packet logic for UDP-based L7 protocols |
| **Anycast network** | Attack traffic absorbed across 250+ PoPs globally |
| **Rate limiting** | Per-source throttling on DNS and HTTP endpoints |

**Relevance**: Cloudflare's architecture mirrors what's needed for LLM inference endpoint protection — rate limiting, adaptive profiling, and L7 filtering applied to `/v1/completions` or `/chat` endpoints.

---

## 6. Relevance to This Project

| Threat | Where It Applies |
|--------|-----------------|
| **HTTP flood against LLM endpoint** | OWASP LLM10 (Unbounded Consumption) — inference endpoint becomes DDoS target; rate limiting + Cloudflare WAF mitigate |
| **DNS hijacking of LLM API gateway** | Envoy AI Gateway or routing proxy relies on DNS; DNS spoofing redirects to rogue LLM |
| **DNS amplification from inference server** | If LLM server queries open DNS resolvers without DNSSEC, amplification attacks can poison its resolver |
| **Botnet as SLM fine-tuning data source** | Scraped training data may originate from botnet-infected sites; poisoning risk (LLM04) |
| **LLM10 — Denial of Wallet** | Rate limiting controls (same mechanisms as DDoS mitigation) protect against token-cost DoW attacks |

---

## Related
- [[network-protocols|Network Protocols]] — DNS, TCP, TLS protocol specs
- [[infrastructure-security|Infrastructure Security]] — service mesh, Zero Trust, network segmentation
- [[owasp-llm-top10|OWASP LLM Top 10 (2025)]] — LLM10 (Unbounded Consumption)
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — rate limiting and L7 filtering for LLM traffic
- [[../components/policy-gateway|Policy Gateway]] — application-layer enforcement
