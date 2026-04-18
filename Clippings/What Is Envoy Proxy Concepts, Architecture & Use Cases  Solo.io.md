---
title: "What Is Envoy Proxy? Concepts, Architecture & Use Cases | Solo.io"
source: "https://www.solo.io/topics/omni/envoy-proxy"
author:
published:
created: 2026-04-13
description: "Envoy creates a transparent network that helps troubleshoot and handle cloud-native applications."
tags:
  - "clippings"
---
## What Is Envoy Proxy?

As organizations adopt microservices, a basic part of the architecture is a network layer 7 (application layer) proxy. In large microservices environments, L7 proxies provide observability, resiliency, and routing, making it transparent to external services that they are accessing a large network of microservices.

The [Envoy Proxy](https://www.envoyproxy.io/) is an open source, high-performance, small-footprint edge and service proxy. It works similarly to software load balancers like NGINX and HAProxy. It was originally created by Lyft, and is now a large open source project with an active base of contributors. The project has been adopted by the [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io/) and is now at [Graduated](https://www.cncf.io/) project maturity.

[Get an introduction to Envoy Proxy](https://academy.solo.io/get-started-with-envoy-proxy-with-fundamentals-for-envoy-certification)

## Envoy Proxy: Architecture

Envoy creates a transparent network that helps troubleshoot and handle cloud-native applications. It’s an independent executable that runs with a real-world application, is easily deployable, and supports any programming language.

An Envoy Proxy is an L3/L4 proxy with a list of filters, which can connect and enable different TCP/UDP proxy processes. Additionally, it supports HTTP L7 filters since HTTP is crucial for cloud-native applications and TLS termination. It has advanced load balancing functions like circuit breaking and auto-retry, and can route gPRC requests and responses. Its configuration is manageable through an API that can push updates dynamically, even while the cluster is running.

Envoy has a multi-threaded architecture and uses a single process within it. The primary thread controls different coordination operations, and worker threads handle the processing, filtering, and forwarding. Once a listener accepts some incoming connection, a worker thread gets allocated to it till the end of the process.

Hence, Envoy is usually single-threaded and has some complex code that handles coordination between the different worker threads. It is advisable to configure the number of worker threads equal to the number of hardware threads on the system.

## Envoy Proxy with Gloo Mesh or Gloo Gateway

As a data plane, Envoy can serve multiple important functions:

- Proxy for Istio Service Mesh
- Kubernetes Ingress
- API-GW
- Integrate with WebAssembly
- Integrate with GraphQL

Envoy has proven to be a highly-scalable and flexible, especially in Kubernetes and cloud-native environments. This is why Solo.io chose Envoy to be the consistent data plane in [Gloo Edge](https://docs.solo.io/gloo-edge/latest/), [Gloo Gateway](https://www.solo.io/products/gloo-gateway/) and [Gloo Mesh](https://www.solo.io/products/gloo-mesh/). This consistent use of Envoy enables companies to learn one technology for filtering and security, and apply that knowledge to multiple use-cases.

Get started with Envoy Proxy in Gloo Platform today.

## Use Cases for Envoy Proxy

There are two main uses for Envoy proxy: for Ingress/Egress in a service mesh (service proxy) and as an API gateway.

### Envoy as a Sidecar

Envoy can serve as an L3 or L4 application or sidecar proxy in a service mesh that enables communication between services. The Envoy instance has the same lifecycle as the proxy’s parent application, allowing the extension of applications across multiple technology stacks—this includes legacy apps that don’t offer extensibility.

All application requests to traverse Envoy through the following listeners:

- **Ingress listeners** —take requests from other services in a service mesh and forward them to the local application related to the Envoy sidecar instance.
- **Egress listeners—** take requests from the local application related to the Envoy sidecar instance and forwards them to other services in the network.

**The picture below shows how the Envoy proxy can attach to the application to enable communication using ingress and egress listeners.**

![](https://cdn.prod.website-files.com/6704482c45ef6ead081645ff/670d9cd74c04b9cf108fbb14_ingress-egress-traffic.webp)

### Envoy as API Gateway

Envoy proxy can serve as an API gateway and ‘front proxy’ that sits between the application and the client request. Envoy accepts inbound traffic, collates the information in each request, and directs it to its destination within the service mesh. The image below demonstrates the use of Envoy as a ‘front proxy’ or ‘edge proxy,’ which will get requests from other networks. As an API gateway, the Envoy proxy is responsible for functionality such as traffic routing, load balancing, authentication, and monitoring at the edge.

![](https://cdn.prod.website-files.com/6704482c45ef6ead081645ff/670d9cd729608f954c51191d_edge-traffic.webp)