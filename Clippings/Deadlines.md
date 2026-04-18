---
title: "Deadlines"
source: "https://grpc.io/docs/guides/deadlines/"
author:
published: 2025-07-06
created: 2026-04-15
description: "Explains how deadlines can be used to effectively deal with unreliable backends."
tags:
  - "clippings"
---
Explains how deadlines can be used to effectively deal with unreliable backends.

## Deadlines

Explains how deadlines can be used to effectively deal with unreliable backends.

### Overview

A deadline is used to specify a point in time past which a client is unwilling to wait for a response from a server. This simple idea is very important in building robust distributed systems. Clients that do not wait around unnecessarily and servers that know when to give up processing requests will improve the resource utilization and latency of your system.

Note that while some language APIs have the concept of a **deadline**, others use the idea of a **timeout**. When an API asks for a deadline, you provide a point in time which the call should not go past. A timeout is the max duration of time that the call can take. A timeout can be converted to a deadline by adding the timeout to the current time when the application starts a call. For simplicity, we will only refer to deadline in this document.

### Deadlines on the Client

By default, gRPC does not set a deadline which means it is possible for a client to end up waiting for a response effectively forever. To avoid this you should always explicitly set a realistic deadline in your clients. To determine the appropriate deadline you would ideally start with an educated guess based on what you know about your system (network latency, server processing time, etc.), validated by some load testing.

If a server has gone past the deadline when processing a request, the client will give up and fail the RPC with the `DEADLINE_EXCEEDED` status.

### Deadlines on the Server

A server might receive RPCs from a client with an unrealistically short deadline that would not give the server enough time to ever respond in time. This would result in the server just wasting valuable resources and in the worst case scenario, crash the server. A gRPC server deals with this situation by automatically cancelling a call (`CANCELLED` status) once a deadline set by the client has passed.

Please note that the server application is responsible for stopping any activity it has spawned to service the RPC. If your application is running a long-running process you should periodically check if the RPC that initiated it has been cancelled and if so, stop the processing.

#### Deadline Propagation

Your server might need to call another server to produce a response. In these cases where your server also acts as a client you would want to honor the deadline set by the original client. Automatically propagating the deadline from an incoming RPC to an outgoing one is supported by some gRPC implementations. In some languages this behavior needs to be explicitly enabled (e.g. C++) and in others it is enabled by default (e.g. Java and Go). Using this capability lets you avoid the error-prone approach of manually including the deadline for each outgoing RPC.

Since a deadline is set point in time, propagating it as-is to a server can be problematic as the clocks on the two servers might not be synchronized. To address this gRPC converts the deadline to a timeout from which the already elapsed time is already deducted. This shields your system from any clock skew issues.

```
#mermaid-1776283370844 {font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-1776283370844 .error-icon{fill:#552222;}#mermaid-1776283370844 .error-text{fill:#552222;stroke:#552222;}#mermaid-1776283370844 .edge-thickness-normal{stroke-width:2px;}#mermaid-1776283370844 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1776283370844 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1776283370844 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1776283370844 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1776283370844 .marker{fill:#666;stroke:#666;}#mermaid-1776283370844 .marker.cross{stroke:#666;}#mermaid-1776283370844 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1776283370844 .actor{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283370844 text.actor>tspan{fill:#333;stroke:none;}#mermaid-1776283370844 .actor-line{stroke:#666;}#mermaid-1776283370844 .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#mermaid-1776283370844 .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#mermaid-1776283370844 #arrowhead path{fill:#333;stroke:#333;}#mermaid-1776283370844 .sequenceNumber{fill:white;}#mermaid-1776283370844 #sequencenumber{fill:#333;}#mermaid-1776283370844 #crosshead path{fill:#333;stroke:#333;}#mermaid-1776283370844 .messageText{fill:#333;stroke:#333;}#mermaid-1776283370844 .labelBox{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283370844 .labelText,#mermaid-1776283370844 .labelText>tspan{fill:#333;stroke:none;}#mermaid-1776283370844 .loopText,#mermaid-1776283370844 .loopText>tspan{fill:#333;stroke:none;}#mermaid-1776283370844 .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(0, 0%, 83%);fill:hsl(0, 0%, 83%);}#mermaid-1776283370844 .note{stroke:#999;fill:#666;}#mermaid-1776283370844 .noteText,#mermaid-1776283370844 .noteText>tspan{fill:#fff;stroke:none;}#mermaid-1776283370844 .activation0{fill:#f4f4f4;stroke:#666;}#mermaid-1776283370844 .activation1{fill:#f4f4f4;stroke:#666;}#mermaid-1776283370844 .activation2{fill:#f4f4f4;stroke:#666;}#mermaid-1776283370844 .actorPopupMenu{position:absolute;}#mermaid-1776283370844 .actorPopupMenuPanel{position:absolute;fill:#eee;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#mermaid-1776283370844 .actor-man line{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283370844 .actor-man circle,#mermaid-1776283370844 line{stroke:hsl(0, 0%, 83%);fill:#eee;stroke-width:2px;}#mermaid-1776283370844 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}ClientUser ServerBilling ServerRequest at 13:00:00Should complete in 2sGetUserProfile(deadline: 13:00:02)0.5s spent beforecalling billing serverGetTransactionHistory(timeout: 1.5s)Retrieve transactionsIt's 13:00:02Time's up!Stop waiting for serverStop waiting for serverDEADLINE_EXCEEDEDStop waiting for serverCancelCancelClean up resources(after noticing that thecall was cancelled)
```

### Language Support

| Language | Example |
| --- | --- |
| Java | [Java example](https://github.com/grpc/grpc-java/tree/master/examples/src/main/java/io/grpc/examples/deadline) |
| Go | [Go example](https://github.com/grpc/grpc-go/tree/master/examples/features/deadline) |
| C++ | [C++ example](https://github.com/grpc/grpc/tree/master/examples/cpp/deadline) |
| Python | [Python example](https://github.com/grpc/grpc/tree/master/examples/python/timeout) |

### Other Resources

- [Deadlines blogpost](https://grpc.io/blog/deadlines/)

Last modified July 7, 2025: [Add link to C++ deadline example (#1445) (78db5a6)](https://github.com/grpc/grpc.io/commit/78db5a6f78ee0d3426cf53cee07739196d962ea2)