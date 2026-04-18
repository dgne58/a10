---
tags: [networking, grpc, protobuf, http2, tls, dns, routing, lan, internet, protocols, sources]
last_updated: 2026-04-15
---

# Network Protocols

## Provenance
- Theme: `protocols-and-observability`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Clippings/Introduction to gRPC.md`
- `Clippings/Language Guide (proto 3).md`
- `Clippings/Protocol Buffers Language Specification (Proto3).md`
- `Clippings/grpcgrpc C++ based gRPC.md`
- `Clippings/RFC 9113 HTTP2.md`
- `Clippings/RFC 9293 Transmission Control Protocol (TCP).md`
- `Clippings/RFC 8446 The Transport Layer Security (TLS) Protocol Version 1.3.md`
- `Clippings/RFC 1035 Domain names - implementation and specification.md`
- `Clippings/RFC 2616 Hypertext Transfer Protocol -- HTTP1.1.md`
- `Clippings/HTTPS - Wikipedia.md`
- `Clippings/How does the Internet work.md`
- `Clippings/What is a LAN (local area network).md`
- `Clippings/What is routing  IP routing.md`
- `Clippings/What is the network layer  Network vs. Internet layer.md`
- `Clippings/What is DNS  How DNS works.md`
- `Clippings/DNS server types.md`
- `Clippings/What are DNS records.md`
- `Clippings/Domain Name System - Wikipedia.md`
- `Clippings/Transmission Control Protocol - Wikipedia.md`
- `Clippings/User Datagram Protocol - Wikipedia.md`

---

## Internet Basics

### The Internet is a network of networks
- The Internet is not a single backbone or control center; it is a distributed system of independently operated networks that interconnect using shared protocols.
- Packet switching is the core scaling trick: a large message is broken into smaller packets, each packet is forwarded independently, and the destination reassembles the stream.
- Routers and switches play different roles:
  - switches move traffic inside one local network
  - routers forward traffic across network boundaries

### End-to-end request path

Loading a web page typically involves:
1. DNS resolution for the destination hostname
2. TCP connection setup
3. TLS handshake for confidentiality and server authentication
4. HTTP request and response exchange
5. Reassembly and rendering on the client

This sequencing matters for the hackathon because the project may expose:
- an HTTP API surface
- long-lived streaming responses
- tool or MCP calls that cross trust boundaries

### LAN, WAN, and the routing boundary
- A LAN is a geographically local network, usually one room, office, or building.
- A WAN is an interconnection of LANs across larger distances.
- VLANs are logical partitions over the same physical switching fabric; they segment traffic without requiring separate physical networks.
- The practical boundary for this repo's architecture is:
  - inside a LAN: switching, local addressing, east-west traffic
  - across LANs / AS boundaries: routing, policy, exposure to external attack traffic

### Why this matters for agentic systems
- The router/orchestrator design in this repo is an application-layer routing problem, but it still runs on top of real packet routing, real trust boundaries, and real latency budgets.
- Local wiki access, local services, remote model APIs, and MCP servers are not equal-cost paths. Physical distance and network hops still shape the user-visible result.

---

## gRPC

### Overview
gRPC (Google Remote Procedure Call) is a high-performance, open-source RPC framework. Client applications can call server methods as if they were local objects.

**Default transport**: HTTP/2  
**Default serialization**: Protocol Buffers (protobuf)  
**Supported languages**: C++, Python, Java, Go, Ruby, Node.js, and more

### How gRPC works
1. Define service interface in `.proto` file
2. Generate client/server code with `protoc` compiler
3. Client stub calls methods; gRPC handles serialization + transport
4. Server implements the interface and runs gRPC server

```proto
// Service definition
service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
  rpc SayHelloStreamReply (HelloRequest) returns (stream HelloReply) {}
}

// Message definitions
message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

### gRPC streaming modes
| Mode | Description |
|------|-------------|
| **Unary** | Single request, single response (standard RPC) |
| **Server streaming** | Single request, stream of responses |
| **Client streaming** | Stream of requests, single response |
| **Bidirectional streaming** | Both sides stream simultaneously |

### Advantages over REST
- Binary encoding (protobuf) → smaller messages, faster serialization
- HTTP/2 multiplexing → multiple concurrent requests on single connection
- Strong typing via proto schema
- Auto-generated clients in multiple languages
- Built-in streaming support

### Relevance to agentic systems
- Envoy uses gRPC for its control plane (xDS APIs) and ext_authz
- MCP over HTTP (SSE) vs gRPC: current MCP uses HTTP+SSE; gRPC is better for high-throughput scenarios
- Envoy Ext_Authz to OPA uses gRPC

---

## Protocol Buffers (Protobuf)

### Why protobuf?
- **Compact**: binary encoding is 3-10× smaller than equivalent JSON
- **Fast**: serialization/deserialization faster than JSON
- **Typed**: schema-first; backward/forward compatibility via field numbers
- **Code generation**: auto-generate typed classes in target language

### Proto3 syntax
```proto
syntax = "proto3";

package tutorial;

message Person {
  string name = 1;       // field number 1
  int32 id = 2;          // field number 2
  string email = 3;

  enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  message PhoneNumber {
    string number = 1;
    PhoneType type = 2;
  }

  repeated PhoneNumber phones = 4;  // repeated = array
}
```

### Field number rules
- Unique integer identifier (1-15: 1 byte encoding, 16-2047: 2 bytes)
- Never reuse field numbers (breaks compatibility)
- Fields 1-15 reserved for frequently occurring fields

### Wire types
| Wire type | Used for |
|-----------|---------|
| 0 | Varint (int32, bool, enum) |
| 1 | 64-bit (fixed64, double) |
| 2 | Length-delimited (string, bytes, nested message) |
| 5 | 32-bit (fixed32, float) |

---

## HTTP/2 (RFC 9113)

HTTP/2 is the successor to HTTP/1.1. Key improvements:

### Key features
| Feature | Description |
|---------|-------------|
| **Binary framing** | Messages encoded as binary frames, not text |
| **Multiplexing** | Multiple streams on single TCP connection (no head-of-line blocking at HTTP layer) |
| **Header compression** | HPACK algorithm compresses redundant headers |
| **Server push** | Server can send resources before client requests them |
| **Stream prioritization** | Assign weights to concurrent streams |

### Connection model
```
Single TCP connection
  ├── Stream 1: GET /api/resource
  ├── Stream 3: POST /api/data  (concurrent)
  └── Stream 5: GET /api/other  (concurrent)
```

HTTP/1.1 required new TCP connection per request (or limited pipelining). HTTP/2 multiplexes over one.

### Relevance
- gRPC requires HTTP/2
- Envoy proxy runs on HTTP/2 internally
- Modern LLM APIs use HTTP/2 for lower latency

---

## TLS 1.3 (RFC 8446)

TLS (Transport Layer Security) 1.3 is the current standard for encrypted transport.

### Improvements over TLS 1.2
| Aspect | TLS 1.2 | TLS 1.3 |
|--------|---------|---------|
| Handshake latency | 2 RTT | 1 RTT (0-RTT resumption available) |
| Cipher suites | Many, some weak | Only strong suites |
| Key exchange | RSA + DHE options | Ephemeral only (Perfect Forward Secrecy) |
| Legacy algorithms | Supported | Removed (MD5, SHA-1, RC4) |

### 1-RTT Handshake
```
Client → Server: ClientHello (key share)
Server → Client: ServerHello + Certificate + Finished
Client → Server: Finished + Application Data
```

### Perfect Forward Secrecy
TLS 1.3 mandates ephemeral key exchange (ECDHE). Past sessions cannot be decrypted even if long-term private key is later compromised.

### mTLS (Mutual TLS)
Both client and server present certificates:
- Standard TLS: server-only authentication
- mTLS: bidirectional authentication
- Used by: Istio/Envoy service mesh, SPIFFE workload identity, internal API auth

### Relevance to agentic systems
- mTLS between agents and tool servers ensures identity verification
- Envoy AI Gateway uses mTLS for SPIFFE/SVID workload identity
- Prevents impersonation of agents or tools

---

## TCP (RFC 9293)

### Key properties
- **Connection-oriented**: 3-way handshake (SYN, SYN-ACK, ACK)
- **Reliable**: guaranteed delivery via acknowledgments + retransmission
- **Ordered**: packets delivered in sequence
- **Flow control**: receiver-based window size
- **Congestion control**: CUBIC, BBR algorithms

### Overhead
- Per-connection state maintained at both endpoints
- Slow start + congestion avoidance affects initial throughput
- Head-of-line blocking at TCP level (HTTP/2 over TCP still suffers)

**QUIC (HTTP/3)**: Addresses TCP's head-of-line blocking by using UDP with per-stream reliability.

---

## DNS

### How DNS works
1. Client queries local resolver (stub resolver)
2. Resolver queries root nameserver → TLD nameserver → authoritative nameserver
3. Recursive resolution with caching at each level

### Record types
| Type | Description |
|------|-------------|
| A | IPv4 address for hostname |
| AAAA | IPv6 address |
| CNAME | Canonical name alias |
| MX | Mail exchange |
| TXT | Text record (SPF, DKIM, etc.) |
| SRV | Service location (host, port, weight, priority) |
| NS | Authoritative nameserver |
| SOA | Start of authority |

### DNS security
- **DNSSEC**: Cryptographic signatures on DNS records (authenticity, not confidentiality)
- **DoH (DNS over HTTPS)**: Encrypt DNS queries to prevent eavesdropping
- **DoT (DNS over TLS)**: Alternative encrypted DNS transport

### Relevance
- Envoy uses DNS for service discovery (in non-Kubernetes environments)
- Service meshes integrate with Kubernetes DNS
- DNS as attack vector: DNS rebinding, DNS hijacking

---

## Routing Mechanics

### Static vs dynamic routing
- **Static routing**: a human defines routes explicitly; simple but brittle when topology changes.
- **Dynamic routing**: routers update forwarding decisions automatically based on observed topology and routing protocols; essential for large or changing networks.

### Common routing protocols
| Protocol | Scope | Purpose |
|----------|-------|---------|
| IP | packet layer | carries source and destination addressing |
| BGP | between autonomous systems | announces reachability between large networks |
| OSPF | within one autonomous system | shortest-path routing inside a managed network |
| RIP | within one autonomous system | simpler hop-count-based routing |

### Hackathon interpretation
- If the demo grows beyond a single API process, the team should separate:
  - local service routing and discovery
  - application-level request routing between model/tool/wiki paths
- The same word, "routing," appears at multiple layers. Be explicit about which one is being discussed.

## Protocol Comparison Table

| Protocol | Transport | Format | Use case |
|----------|-----------|--------|---------|
| REST/HTTP | TCP | JSON/XML | APIs, web services |
| gRPC | HTTP/2 | Protobuf | Internal microservices, high throughput |
| WebSocket | TCP | Any | Real-time bidirectional |
| SSE | HTTP | Text | Server-to-client streaming |
| QUIC | UDP | Binary | HTTP/3, low-latency transport |
| MCP (current) | HTTP+SSE | JSON | LLM tool protocol |

---

## Related
- [[../components/envoy-ai-gateway|Envoy AI Gateway]] — uses gRPC for control plane, HTTP/2 for data plane
- [[infrastructure-security]] — TLS, mTLS, service mesh security
- [[../sources/protocols-and-observability|Protocols and Observability]] — source hub
