---
title: "Sidecar or ambient?"
source: "https://istio.io/latest/docs/overview/dataplane-modes/"
author:
published:
created: 2026-04-15
description: "Learn about Istio's two dataplane modes and which you should use."
tags:
  - "clippings"
---
An Istio service mesh is logically split into a data plane and a control plane.

The data plane is the set of proxies that mediate and control all network communication between microservices. They also collect and report telemetry on all mesh traffic.

The control plane manages and configures the proxies in the data plane.

Istio supports two main data plane modes:

- **sidecar mode**, which deploys an Envoy proxy along with each pod that you start in your cluster, or running alongside services running on VMs.
- **ambient mode**, which uses a per-node Layer 4 proxy, and optionally a per-namespace Envoy proxy for Layer 7 features.

You can opt certain namespaces or workloads into each mode.

## Sidecar mode

Istio has been built on the sidecar pattern from its first release in 2017. Sidecar mode is well understood and thoroughly battle-tested, but comes with a resource cost and operational overhead.

- Each application you deploy has an Envoy proxy injected as a sidecar
- All proxies can process both Layer 4 and Layer 7

## Ambient mode

Launched in 2022, ambient mode was built to address the shortcomings reported by users of sidecar mode. As of Istio 1.22, it is production-ready for single cluster use cases.

- All traffic is proxied through a Layer 4-only node proxy
- Applications can opt in to routing through an Envoy proxy to get Layer 7 features

## Choosing between sidecar and ambient

Users often deploy a mesh to enable a zero-trust security posture as a first-step and then selectively enable L7 capabilities as needed. Ambient mesh allows those users to bypass the cost of L7 processing entirely when it’s not needed.

|  | **Sidecar** | **Ambient** |
| --- | --- | --- |
| Traffic management | Full Istio feature set | Full Istio feature set (requires using waypoint) |
| Security | Full Istio feature set | Full Istio feature set: encryption and L4 authorization in ambient mode. Requires waypoints for L7 authorization. |
| Observability | Full Istio feature set | Full Istio feature set: L4 telemetry in ambient mode; L7 observability when using waypoint |
| Extensibility | Full Istio feature set | Via [WebAssembly plugins](https://istio.io/latest/docs/ambient/usage/extend-waypoint-wasm) (requires using waypoint)   The EnvoyFilter API is not supported. |
| Adding workloads to the mesh | Label a namespace and restart all pods to have sidecars added | Label a namespace - no pod restart required |
| Incremental deployment | Binary: sidecar is injected or it isn't | Gradual: L4 is always on, L7 can be added by configuration |
| Lifecycle management | Proxies managed by application developer | Platform administrator |
| Utilization of resources | Wasteful; CPU and memory resources must be provisioned for worst case usage of each individual pod | Waypoint proxies can be auto-scaled like any other Kubernetes deployment.   A workload with many replicas can use one waypoint, vs. each one having its own sidecar. |
| Average resource cost | Large | Small |
| Average latency (p90/p99) | 0.63ms-0.88ms | Ambient: 0.16ms-0.20ms   Waypoint: 0.40ms-0.50ms |
| L7 processing steps | 2 (source and destination sidecar) | 1 (destination waypoint) |
| Configuration at scale | Requires [configuration of the scope of each sidecar](https://istio.io/latest/docs/ops/configuration/mesh/configuration-scoping/) to reduce configuration | Works without custom configuration |
| Supports "server-first" protocols | [Requires configuration](https://istio.io/latest/docs/ops/deployment/application-requirements/#server-first-protocols) | Yes |
| Support for Kubernetes Jobs | Complicated by long life of sidecar | Transparent |
| Security model | Strongest: each workload has its own keys | Strong: each node agent has only the keys for workloads on that node |
| Compromised application pod   gives access to mesh keys | Yes | No |
| Support | Stable, including multi-cluster | Stable, only single-cluster |
| Platforms supported | Kubernetes (any CNI)   Virtual machines | Kubernetes (any CNI) |

## Layer 4 vs Layer 7 features

The overhead for processing protocols at Layer 7 is substantially higher than processing network packets at Layer 4. For a given service, if your requirements can be met at L4, service mesh can be delivered at substantially lower cost.

### Security

|  | L4 | L7 |
| --- | --- | --- |
| Encryption | All traffic between pods is encrypted using mTLS. | N/A—service identity in Istio is based on TLS. |
| Service-to-service authentication | SPIFFE, via mTLS certificates. Istio issues a short-lived X.509 certificate that encodes the pod's service account identity. | N/A—service identity in Istio is based on TLS. |
| Service-to-service authorization | Network-based authorization, plus identity-based policy, e.g.: - A can accept inbound calls from only "10.2.0.0/16"; - A can call B. | Full policy, e.g.: - A can GET /foo on B only with valid end-user credentials containing the READ scope. |
| End-user authentication | N/A—we can't apply per-user settings. | Local authentication of JWTs, support for remote authentication via OAuth and OIDC flows. |
| End-user authorization | N/A—see above. | Service-to-service policies can be extended to require [end-user credentials with specific scopes, issuers, principal, audiences, etc.](https://istio.io/latest/docs/reference/config/security/conditions/)   Full user-to-resource access can be implemented using external authorization, allowing per-request policy with decisions from an external service, e.g. OPA. |

### Observability

|  | L4 | L7 |
| --- | --- | --- |
| Logging | Basic network information: network 5-tuple, bytes sent/received, etc. [See Envoy docs](https://www.envoyproxy.io/docs/envoy/latest/configuration/observability/access_log/usage#command-operators). | [Full request metadata logging](https://www.envoyproxy.io/docs/envoy/latest/configuration/observability/access_log/usage#command-operators), in addition to basic network information. |
| Tracing | Not today; possible eventually with HBONE. | Envoy participates in distributed tracing. [See Istio overview on tracing](https://istio.io/latest/docs/tasks/observability/distributed-tracing/overview/). |
| Metrics | TCP only (bytes sent/received, number of packets, etc.). | L7 RED metrics: rate of requests, rate of errors, request duration (latency). |

### Traffic management

|  | L4 | L7 |
| --- | --- | --- |
| Load balancing | Connection level only. [See TCP traffic shifting task](https://istio.io/latest/docs/tasks/traffic-management/tcp-traffic-shifting/). | Per request, enabling e.g. canary deployments, gRPC traffic, etc. [See HTTP traffic shifting task](https://istio.io/latest/docs/tasks/traffic-management/traffic-shifting/). |
| Circuit breaking | [TCP only](https://istio.io/latest/docs/reference/config/networking/destination-rule/#ConnectionPoolSettings-TCPSettings). | [HTTP settings](https://istio.io/latest/docs/reference/config/networking/destination-rule/#ConnectionPoolSettings-HTTPSettings) in addition to TCP. |
| Outlier detection | On connection establishment/failure. | On request success/failure. |
| Rate limiting | [Rate limit on L4 connection data only, on connection establishment](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/network_filters/rate_limit_filter#config-network-filters-rate-limit), with global and local rate limiting options. | [Rate limit on L7 request metadata](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/rate_limit_filter#config-http-filters-rate-limit), per request. |
| Timeouts | Connection establishment only (connection keep-alive is configured via circuit breaking settings). | Per request. |
| Retries | Retry connection establishment | Retry per request failure. |
| Fault injection | N/A—fault injection cannot be configured on TCP connections. | Full application and connection-level faults ([timeouts, delays, specific response codes](https://istio.io/latest/docs/tasks/traffic-management/fault-injection/)). |
| Traffic mirroring | N/A—HTTP only | [Percentage-based mirroring of requests to multiple backends](https://istio.io/latest/docs/tasks/traffic-management/mirroring/). |