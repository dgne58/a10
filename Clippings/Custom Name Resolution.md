---
title: "Custom Name Resolution"
source: "https://grpc.io/docs/guides/custom-name-resolution/"
author:
published: 2025-04-22
created: 2026-04-15
description: "Explains standard name resolution, the custom name resolver interface, and how to write an implementation."
tags:
  - "clippings"
---
Explains standard name resolution, the custom name resolver interface, and how to write an implementation.

## Custom Name Resolution

Explains standard name resolution, the custom name resolver interface, and how to write an implementation.

### Overview

Name resolution is fundamentally about service discovery. When sending a gRPC request, the client must determine the IP address of the service name. Name resolution is often thought to be the same as [DNS](https://www.ietf.org/rfc/rfc1035.txt). In practice however, DNS is usually augmented with extensions or completely replaced to enable name resolution.

When making a request with a gRPC client, by default, DNS name resolution is used. However, various other name resolution mechanisms may be used:

| Resolver | Example | Notes |
| --- | --- | --- |
| DNS | `grpc.io:50051` | By default, DNS is assumed. |
| DNS | `dns:///grpc.io:50051` | The extra slash is used to provide an authority |
| Unix Domain Socket | `unix:///run/containerd/containerd.sock` |  |
| xDS | `xds:///wallet.grpcwallet.io` |  |
| IPv4 | `ipv4:198.51.100.123:50051` | Only supported in some languages |

> [!info] Note
> The triple slashes above (`///`) may look unfamiliar if you are used to the double slashes of HTTP, such as `https://grpc.io`. These *target strings* follow the format for [RFC-3986](https://datatracker.ietf.org/doc/html/rfc3986) URIs. The string following the first two slashes and preceding the third (if there is a third at all) is the *authority*. The authority string identifies a server which contains the URIs of all resources. In the case of a conventional HTTP request, the authority over the URI is the server to which the request will be sent. In other cases, the authority will be the identity of the name resolution server, while the resource itself lives on some other server. Some name resolvers have no need for an authority. In this case, the authority string is left empty, resulting in three slashes in a row.

Several languages support an interface to allow the user to define their own name resolvers, so that you may define how to resolve any given name. Once registered, a name resolver with the *scheme* `my-resolver` will be picked up when a target string begins with `my-resolver:`. For example, requests to `my-resolver:///my-service` would now use the `my-resolver` name resolver implementation.

### Custom Name Resolvers

You might consider using a custom name resolver whenever you would like to augment or replace DNS for service discovery. For example, this interface has been used in the past to use [Apache Zookeeper](https://zookeeper.apache.org/) to look up service names. It has also been used to directly interface with the Kubernetes API server for service lookup based on headless Service resources.

One reason why it might be particularly useful to use a custom name resolver rather than standard DNS is that this interface is *reactive*. Within standard DNS, a client looks up the address for a particular service at the beginning of the connection and maintains its connection to that address for the lifetime of the connection. However, custom name resolvers may be watch-based. That is, they can receive updates from the name server over time and therefore respond intelligently to backend failure as well as backend scale-ups and backend scale-downs.

In addition, a custom name resolver may provide the client connection with a *service config*. A service config is a JSON object that defines arbitrary configuration specifying how traffic should be routed to and load balanced across a particular service. At its most basic, this can be used to specify things like that a particular service should use the round robin load balancing policy vs. pick first. However, when a custom name resolver is used in conjunction with arbitrary service config and a [*custom load balancing policy*](https://grpc.io/docs/guides/custom-load-balancing/), very complex traffic management systems such as xDS may be constructed.

#### Life of a Target String

While the exact interface for custom name resolvers differs from language to language, the general structure is the same. The client registers an implementation of a *name resolver provider* to a process-global registry close to the start of the process. The name resolver provider will be called by the gRPC library with a target strings intended for the custom name resolver. Given that target string, the name resolver provider will return an instance of a name resolver, which will interact with the client connection to direct the request according to the target string.

```
#mermaid-1776283366793 {font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-1776283366793 .error-icon{fill:#552222;}#mermaid-1776283366793 .error-text{fill:#552222;stroke:#552222;}#mermaid-1776283366793 .edge-thickness-normal{stroke-width:2px;}#mermaid-1776283366793 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1776283366793 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1776283366793 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1776283366793 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1776283366793 .marker{fill:#666;stroke:#666;}#mermaid-1776283366793 .marker.cross{stroke:#666;}#mermaid-1776283366793 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1776283366793 .actor{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283366793 text.actor>tspan{fill:#333;stroke:none;}#mermaid-1776283366793 .actor-line{stroke:#666;}#mermaid-1776283366793 .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#mermaid-1776283366793 .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#mermaid-1776283366793 #arrowhead path{fill:#333;stroke:#333;}#mermaid-1776283366793 .sequenceNumber{fill:white;}#mermaid-1776283366793 #sequencenumber{fill:#333;}#mermaid-1776283366793 #crosshead path{fill:#333;stroke:#333;}#mermaid-1776283366793 .messageText{fill:#333;stroke:#333;}#mermaid-1776283366793 .labelBox{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283366793 .labelText,#mermaid-1776283366793 .labelText>tspan{fill:#333;stroke:none;}#mermaid-1776283366793 .loopText,#mermaid-1776283366793 .loopText>tspan{fill:#333;stroke:none;}#mermaid-1776283366793 .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(0, 0%, 83%);fill:hsl(0, 0%, 83%);}#mermaid-1776283366793 .note{stroke:#999;fill:#666;}#mermaid-1776283366793 .noteText,#mermaid-1776283366793 .noteText>tspan{fill:#fff;stroke:none;}#mermaid-1776283366793 .activation0{fill:#f4f4f4;stroke:#666;}#mermaid-1776283366793 .activation1{fill:#f4f4f4;stroke:#666;}#mermaid-1776283366793 .activation2{fill:#f4f4f4;stroke:#666;}#mermaid-1776283366793 .actorPopupMenu{position:absolute;}#mermaid-1776283366793 .actorPopupMenuPanel{position:absolute;fill:#eee;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#mermaid-1776283366793 .actor-man line{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283366793 .actor-man circle,#mermaid-1776283366793 line{stroke:hsl(0, 0%, 83%);fill:#eee;stroke-width:2px;}#mermaid-1776283366793 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}ClientgRPCNameResolverProviderNameResolverRequest to my-resolver:///my-servicerequests NameResolverreturns NameResolverdelegates resolutionaddressesClientgRPCNameResolverProviderNameResolver
```

### Language Support

| Language | Example |
| --- | --- |
| Java | [Example](https://github.com/grpc/grpc-java/tree/master/examples/src/main/java/io/grpc/examples/nameresolve) |
| Go | [Example](https://github.com/grpc/grpc-go/tree/master/examples/features/name_resolving) |
| C++ | Not supported |
| Python | Not supported |

Last modified April 23, 2025: [Update unix resolver scheme in custom-name-resolution.md (#1423) (695a785)](https://github.com/grpc/grpc.io/commit/695a785a18cf54e78dc03e4957fc0319eed79fd0)