---
title: "Custom Load Balancing Policies"
source: "https://grpc.io/docs/guides/custom-load-balancing/"
author:
published: 2024-11-11
created: 2026-04-15
description: "Explains how custom load balancing policies can help optimize load balancing under unique circumstances."
tags:
  - "clippings"
---
Explains how custom load balancing policies can help optimize load balancing under unique circumstances.

## Custom Load Balancing Policies

Explains how custom load balancing policies can help optimize load balancing under unique circumstances.

### Overview

One of the key features of gRPC is load balancing, which allows requests from clients to be distributed across multiple servers. This helps prevent any one server from becoming overloaded and allows the system to scale up by adding more servers.

A gRPC load balancing policy is given a list of server IP addresses by the name resolver. The policy is responsible for maintaining connections (subchannels) to the servers and picking a connection to use when an RPC is sent.

### Implementing Your Own Policy

By default the `pick_first` policy will be used. This policy actually does no load balancing but just tries each address it gets from the name resolver and uses the first one it can connect to. By updating the gRPC service config you can also switch to using `round_robin` that connects to every address it gets and rotates through the connected backends for each RPC. There are also some other load balancing policies available, but the exact set varies by language. If the built-in policies do not meet your needs you can also implement your own custom policy.

This involves implementing a load balancer interface in the language you are using. At a high level, you will have to:

- Register your implementation in the load balancer registry so that it can be referred to from the service config
- Parse the JSON configuration object of your implementation. This allows your load balancer to be configured in the service config with any arbitrary JSON you choose to support
- Manage what backends to maintain a connection with
- Implement a `picker` that will choose which backend to connect to when an RPC is made. Note that this needs to be a fast operation as it is on the RPC call path
- To enable your load balancer, configure it in your service config

The exact steps vary by language, see the language support section for some concrete examples in your language.

```
#mermaid-1776283363426 {font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#000000;}#mermaid-1776283363426 .error-icon{fill:#552222;}#mermaid-1776283363426 .error-text{fill:#552222;stroke:#552222;}#mermaid-1776283363426 .edge-thickness-normal{stroke-width:2px;}#mermaid-1776283363426 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1776283363426 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1776283363426 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1776283363426 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1776283363426 .marker{fill:#666;stroke:#666;}#mermaid-1776283363426 .marker.cross{stroke:#666;}#mermaid-1776283363426 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1776283363426 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#000000;}#mermaid-1776283363426 .cluster-label text{fill:#333;}#mermaid-1776283363426 .cluster-label span{color:#333;}#mermaid-1776283363426 .label text,#mermaid-1776283363426 span{fill:#000000;color:#000000;}#mermaid-1776283363426 .node rect,#mermaid-1776283363426 .node circle,#mermaid-1776283363426 .node ellipse,#mermaid-1776283363426 .node polygon,#mermaid-1776283363426 .node path{fill:#eee;stroke:#999;stroke-width:1px;}#mermaid-1776283363426 .node .label{text-align:center;}#mermaid-1776283363426 .node.clickable{cursor:pointer;}#mermaid-1776283363426 .arrowheadPath{fill:#333333;}#mermaid-1776283363426 .edgePath .path{stroke:#666;stroke-width:2.0px;}#mermaid-1776283363426 .flowchart-link{stroke:#666;fill:none;}#mermaid-1776283363426 .edgeLabel{background-color:white;text-align:center;}#mermaid-1776283363426 .edgeLabel rect{opacity:0.5;background-color:white;fill:white;}#mermaid-1776283363426 .cluster rect{fill:hsl(0, 0%, 98.9215686275%);stroke:#707070;stroke-width:1px;}#mermaid-1776283363426 .cluster text{fill:#333;}#mermaid-1776283363426 .cluster span{color:#333;}#mermaid-1776283363426 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(-160, 0%, 93.3333333333%);border:1px solid #707070;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1776283363426 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}Provides addresses &
LB configProvides a pickerRequests
a subchannelManages subchannels
to backendsCreatesPicks oneName ResolverLoad BalancerChannelPickerSubchannel 1..n
```

### Backend Metrics

What if your load balancing policy needs real-time information about the backend servers? For this you can rely on backend metrics. You can have metrics provided to you either in-band, in the backend RPC responses, or out-of-band as separate RPCs from the backends. Standard metrics like CPU and memory utilization are provided, but you can also implement your own custom metrics.

For more information on this, please see the custom backend metrics [guide](https://grpc.io/docs/guides/custom-backend-metrics/)

### Service Mesh

If you have a service mesh setup where a central control plane is coordinating the configuration of your microservices, you cannot configure your custom load balancer directly via the service config. But support is provided to do this with the xDS protocol that your control plane uses to communicate with your gRPC clients. Please refer to your control plane documentation to determine how custom load balancing configuration is supported.

For more details, please see gRPC [proposal A52](https://github.com/grpc/proposal/blob/master/A52-xds-custom-lb-policies.md).

### Language Support

| Language | Example | Notes |
| --- | --- | --- |
| Java | [Java example](https://github.com/grpc/grpc-java/tree/master/examples/src/main/java/io/grpc/examples/customloadbalance) |  |
| Go | [Go example](https://github.com/grpc/grpc-go/tree/master/examples/features/customloadbalancer) |  |
| C++ |  | Not yet supported |

Last modified November 12, 2024: [Embed YouTube videos in different webpages (#1380) (196f408)](https://github.com/grpc/grpc.io/commit/196f408ae74741605fbb66f3ccf23b81fe384667)