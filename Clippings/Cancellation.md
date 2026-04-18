---
title: "Cancellation"
source: "https://grpc.io/docs/guides/cancellation/"
author:
published: 2024-02-28
created: 2026-04-15
description: "Explains how and when to cancel RPCs."
tags:
  - "clippings"
---
Explains how and when to cancel RPCs.

## Cancellation

Explains how and when to cancel RPCs.

### Overview

When a gRPC client is no longer interested in the result of an RPC call, it may *cancel* to signal this discontinuation of interest to the server. [Deadline](https://grpc.io/docs/guides/deadlines/) expiration and I/O errors also trigger cancellation. When an RPC is cancelled, the server should stop any ongoing computation and end its side of the stream. Often, servers are also clients to upstream servers, so that cancellation operation should ideally propagate to all ongoing computation in the system that was initiated due to the original client RPC call.

A client may cancel an RPC for several reasons. The data it requested may have been made irrelevant or the author of the client may want to be a good citizen of the server and conserve compute resources.

```
#mermaid-1776283348731 {font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-1776283348731 .error-icon{fill:#552222;}#mermaid-1776283348731 .error-text{fill:#552222;stroke:#552222;}#mermaid-1776283348731 .edge-thickness-normal{stroke-width:2px;}#mermaid-1776283348731 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1776283348731 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1776283348731 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1776283348731 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1776283348731 .marker{fill:#666;stroke:#666;}#mermaid-1776283348731 .marker.cross{stroke:#666;}#mermaid-1776283348731 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1776283348731 .actor{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283348731 text.actor>tspan{fill:#333;stroke:none;}#mermaid-1776283348731 .actor-line{stroke:#666;}#mermaid-1776283348731 .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#mermaid-1776283348731 .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#mermaid-1776283348731 #arrowhead path{fill:#333;stroke:#333;}#mermaid-1776283348731 .sequenceNumber{fill:white;}#mermaid-1776283348731 #sequencenumber{fill:#333;}#mermaid-1776283348731 #crosshead path{fill:#333;stroke:#333;}#mermaid-1776283348731 .messageText{fill:#333;stroke:#333;}#mermaid-1776283348731 .labelBox{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283348731 .labelText,#mermaid-1776283348731 .labelText>tspan{fill:#333;stroke:none;}#mermaid-1776283348731 .loopText,#mermaid-1776283348731 .loopText>tspan{fill:#333;stroke:none;}#mermaid-1776283348731 .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(0, 0%, 83%);fill:hsl(0, 0%, 83%);}#mermaid-1776283348731 .note{stroke:#999;fill:#666;}#mermaid-1776283348731 .noteText,#mermaid-1776283348731 .noteText>tspan{fill:#fff;stroke:none;}#mermaid-1776283348731 .activation0{fill:#f4f4f4;stroke:#666;}#mermaid-1776283348731 .activation1{fill:#f4f4f4;stroke:#666;}#mermaid-1776283348731 .activation2{fill:#f4f4f4;stroke:#666;}#mermaid-1776283348731 .actorPopupMenu{position:absolute;}#mermaid-1776283348731 .actorPopupMenuPanel{position:absolute;fill:#eee;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#mermaid-1776283348731 .actor-man line{stroke:hsl(0, 0%, 83%);fill:#eee;}#mermaid-1776283348731 .actor-man circle,#mermaid-1776283348731 line{stroke:hsl(0, 0%, 83%);fill:#eee;stroke-width:2px;}#mermaid-1776283348731 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}ClientServer 1Server 2CancelCancelClientServer 1Server 2
```

### Cancelling an RPC Call on the Client Side

A client cancels an RPC call by calling a method on the call object or, in some languages, on the accompanying context object. While gRPC clients do not provide additional details to the server about the reason for the cancellation, the cancel API call takes a string describing the reason, which will result in a client-side exception and/or log containing the provided reason. When a server is notified of the cancellation of an RPC, the application-provided server handler may be busy processing the request. The gRPC library in general does not have a mechanism to interrupt the application-provided server handler, so the server handler must coordinate with the gRPC library to ensure that local processing of the request ceases. Therefore, if an RPC is long-lived, its server handler must periodically check if the RPC it is servicing has been cancelled and if it has, cease processing. Some languages will also support automatic cancellation of anyoutgoing RPCs, while in others, the author of the server handler is responsible for this.

```
#mermaid-1776283348745 {font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-1776283348745 .error-icon{fill:#552222;}#mermaid-1776283348745 .error-text{fill:#552222;stroke:#552222;}#mermaid-1776283348745 .edge-thickness-normal{stroke-width:2px;}#mermaid-1776283348745 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1776283348745 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1776283348745 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1776283348745 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1776283348745 .marker{fill:#666;stroke:#666;}#mermaid-1776283348745 .marker.cross{stroke:#666;}#mermaid-1776283348745 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1776283348745 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#000000;}#mermaid-1776283348745 .cluster-label text{fill:#333;}#mermaid-1776283348745 .cluster-label span{color:#333;}#mermaid-1776283348745 .label text,#mermaid-1776283348745 span{fill:#000000;color:#000000;}#mermaid-1776283348745 .node rect,#mermaid-1776283348745 .node circle,#mermaid-1776283348745 .node ellipse,#mermaid-1776283348745 .node polygon,#mermaid-1776283348745 .node path{fill:#eee;stroke:#999;stroke-width:1px;}#mermaid-1776283348745 .node .label{text-align:center;}#mermaid-1776283348745 .node.clickable{cursor:pointer;}#mermaid-1776283348745 .arrowheadPath{fill:#333333;}#mermaid-1776283348745 .edgePath .path{stroke:#666;stroke-width:2.0px;}#mermaid-1776283348745 .flowchart-link{stroke:#666;fill:none;}#mermaid-1776283348745 .edgeLabel{background-color:white;text-align:center;}#mermaid-1776283348745 .edgeLabel rect{opacity:0.5;background-color:white;fill:white;}#mermaid-1776283348745 .cluster rect{fill:hsl(0, 0%, 98.9215686275%);stroke:#707070;stroke-width:1px;}#mermaid-1776283348745 .cluster text{fill:#333;}#mermaid-1776283348745 .cluster span{color:#333;}#mermaid-1776283348745 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(-160, 0%, 93.3333333333%);border:1px solid #707070;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1776283348745 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}CANCELCANCELServer1falsetrueperform some workcancelled?cancel upstream RPCsexit RPC handlerClientServer2
```

### Language Support

| Language | Example | Notes |
| --- | --- | --- |
| Java | [Example](https://github.com/grpc/grpc-java/tree/master/examples/src/main/java/io/grpc/examples/cancellation) | Automatically cancels outgoing RPCs |
| Go | [Example](https://github.com/grpc/grpc-go/tree/master/examples/features/cancellation) | Automatically cancels outgoing RPCs |
| C++ | [Example](https://github.com/grpc/grpc/tree/master/examples/cpp/cancellation) | Automatically cancels outgoing RPCs |
| Python | [Example](https://github.com/grpc/grpc/tree/master/examples/python/cancellation) |  |

Last modified February 29, 2024: [Use absolute paths instead of absolute URLs (#1268) (4f733b4)](https://github.com/grpc/grpc.io/commit/4f733b4438ecfacd807c943c9f757a7a55044156)