---
title: "Control Plane Port Names"
source: "https://linkerd.io/2-edge/reference/controlplane-port-names/"
author:
published:
created: 2026-04-15
description: "Reference guide to Linkerd control plane port names."
tags:
  - "clippings"
---
Linkerd’s control plane components expose various ports for communication and administration. Each container port is assigned a unique name to enable precise references from Services, probes, and monitoring configurations.

The following table lists control plane container port names:

| Component | Port Name | Protocol |
| --- | --- | --- |
| destination | `dest-grpc` | gRPC |
| destination | `dest-admin` | HTTP |
| sp-validator | `spval-admin` | HTTP |
| policy-controller | `policy-grpc` | gRPC |
| policy-controller | `policy-admin` | HTTP |
| identity | `ident-grpc` | gRPC |
| identity | `ident-admin` | HTTP |
| proxy-injector | `injector-admin` | HTTP |
| linkerd2-cni | `repair-admin` | HTTP |