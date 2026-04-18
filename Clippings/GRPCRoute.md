---
title: "GRPCRoute"
source: "https://linkerd.io/2-edge/reference/grpcroute/"
author:
published:
created: 2026-04-15
description: "Reference guide to GRPCRoute resources."
tags:
  - "clippings"
---
A GRPCRoute is a Kubernetes resource which attaches to a “parent” resource, such as a [Service](https://kubernetes.io/docs/concepts/services-networking/service/), and defines a set of rules which match gRPC requests to that resource. These rules can be based on parameters such as path, method, headers, or other aspects of the gRPC request.

GRPCRoutes are used to configure various aspects of Linkerd’s behavior, and form part of [Linkerd’s support for the Gateway API](https://linkerd.io/2-edge/features/gateway-api/).

> [!-info] -info
> #### Note
> 
> The GRPCRoute resource is part of the Gateway API and is not Linkerd-specific. The canonical reference doc is the [Gateway API GRPCRoute documentation](https://gateway-api.sigs.k8s.io/api-types/grpcroute/). This page is intended as a *supplement* to that doc, and will detail how this type is used by Linkerd specifically.

## Inbound vs outbound GRPCRoutes

GRPCRoutes usage in Linkerd falls into two categories: configuration of *inbound* behavior and configuration of *outbound* behavior.

**Inbound behavior.** GRPCRoutes with a [Server](https://linkerd.io/2-edge/reference/authorization-policy/#server) as their parent resource configure policy for *inbound* traffic to pods which receive traffic to that [Server](https://linkerd.io/2-edge/reference/authorization-policy/#server). Inbound GRPCRoutes are used to configure fine-grained [per-route authorization and authentication policies](https://linkerd.io/2-edge/tasks/configuring-per-route-policy/).

**Outbound behavior.** GRPCRoutes with a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) as their parent resource configure policies for *outbound* proxies in pods which are clients of that [Service](https://kubernetes.io/docs/concepts/services-networking/service/). Outbound policy includes [dynamic request routing](https://linkerd.io/2-edge/tasks/configuring-dynamic-request-routing/), adding request headers, modifying a request’s path, and reliability features such as timeouts.

> [!-warning] -warning
> #### Warning
> 
> **Outbound GRPCRoutes and [ServiceProfiles](https://linkerd.io/2-edge/reference/service-profiles/) provide overlapping configuration.** For backwards-compatibility reasons, a ServiceProfile will take precedence over GRPCRoutes which configure the same Service. If a ServiceProfile is defined for the parent Service of an GRPCRoute, proxies will use the ServiceProfile configuration, rather than the GRPCRoute configuration, as long as the ServiceProfile exists.

## Usage in practice

See important notes in the [Gateway API](https://gateway-api.sigs.k8s.io/) documentation about using these types in practice, including ownership of types and compatible versions.

## GRPCRoute Examples

This example demonstrates how to split traffic between two backends. A portion of requests is directed to the `smiley2` backend Service, while the rest go to the `smiley` backend Service.

```yaml
apiVersion: gateway.networking.k8s.io/v1alpha2
kind: GRPCRoute
metadata:
  name: smiley-a-b
  namespace: faces
spec:
  parentRefs:
    - name: smiley
      kind: Service
      group: core
      port: 50051
  rules:
    - backendRefs:
        - name: smiley
          port: 50051
          weight: 40
        - name: smiley2
          port: 80
          weight: 50051
```