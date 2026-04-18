---
tags: [a10, adc, ddos, cgnat, ssli, iac, kubernetes, sources]
last_updated: 2026-04-15
---

# A10 Product Notes

## Provenance
- Theme: `security-networking-and-governance`
- Registry: [[clipping-registry]]
- Inventory: [[clipping-inventory]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Why This Matters

The `Products*.md` clippings are not deep technical guides by themselves, but together they expose the operational surface area of the A10 platform. For this repo, that is useful because it shows where A10 can sit in the runtime architecture:
- traffic management and ADC
- DDoS detection and mitigation
- firewall / SSL inspection / CGNAT
- centralized control plane
- IaC and cloud deployment hooks
- Kubernetes connectivity and observability

## Product Surface

### Traffic, security, and network functions
- ADC / server load balancing
- global server load balancing
- DDoS detection and mitigation
- SSL inspection / encrypt-decrypt
- IPsec VPN and firewall functions
- CGNAT for IPv4 preservation and IPv6 transition

### Management plane
- **A10 Control / Harmony Controller** act as centralized management surfaces for service delivery and operations.
- This is the closest A10-native analogue in the corpus to a control plane coordinating multiple deployed network functions.

### Infrastructure as code
- ARM PowerShell
- AWS CloudFormation
- Ansible via axAPI and CLI
- Terraform provider
- Venafi integration for certificate workflows

This makes A10 operationally compatible with the same delivery patterns the repo already tracks elsewhere: declarative provisioning, repeatable rollout, and cert automation.

### Cloud and Kubernetes integrations
- OpenStack Octavia integration
- Thunder Kubernetes Connector
- Thunder Observability Agent

These matter because they make A10 part of a modern service environment rather than only an on-prem appliance story.

### Form factors and licensing
- physical appliance
- virtual appliance
- container
- bare metal
- global license management / capacity pooling

## Architecture Interpretation

For the hackathon architecture, A10 products map most cleanly to the **edge / ingress / enforcement** side of the system:
- front-door traffic handling
- availability and load balancing
- DDoS mitigation
- SSL/TLS inspection and policy enforcement
- external exposure of APIs and services

They are not a substitute for:
- application-layer agent orchestration
- wiki memory
- MCP tool semantics

Instead, they are the surrounding network and delivery substrate.

## Practical Use In This Wiki

If the prototype eventually targets A10 infrastructure, this page should become the hub for:
- which A10 component is relevant
- which automation surface to use
- which deployment model applies
- which observability/control-plane hooks exist

For now, it is a capability inventory rather than a design commitment.

## Sources Included
- `Clippings/Products.md`
- `Clippings/Products 1.md`
- `Clippings/Products 2.md`
- `Clippings/Products 3.md`
- `Clippings/Products 4.md`
- `Clippings/Products 5.md`
- `Clippings/Products 6.md`

## Related
- [[security-networking-and-governance]]
- [[envoy-gateway-notes]]
- [[linkerd-notes]]
- [[../components/policy-gateway|Policy Gateway]]
- [[../components/envoy-ai-gateway|Envoy AI Gateway]]
