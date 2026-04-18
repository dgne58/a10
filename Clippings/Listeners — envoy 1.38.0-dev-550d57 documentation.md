---
title: "Listeners — envoy 1.38.0-dev-550d57 documentation"
source: "https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/listeners/listeners#tcp"
author:
published:
created: 2026-04-15
description:
tags:
  - "clippings"
---
## Listeners

The Envoy configuration supports any number of listeners within a single process. Generally we recommend running a single Envoy per machine regardless of the number of configured listeners. This allows for easier operation and a single source of statistics.

Envoy supports both and listeners.

## TCP

Each listener is independently configured with [filter\_chains](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto#envoy-v3-api-field-config-listener-v3-listener-filter-chains), where an individual [filter\_chain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) is selected based on its [filter\_chain\_match](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchainmatch) criteria.

An individual [filter\_chain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) is composed of one or more network level (L3/L4) [filters](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/listeners/listener_filters#arch-overview-network-filters).

When a new connection is received on a listener, the appropriate [filter\_chain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) is selected, and the configured connection-local filter stack is instantiated and begins processing subsequent events.

The generic listener architecture is used to perform the vast majority of different proxy tasks that Envoy is used for (e.g., [rate limiting](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_features/global_rate_limiting#arch-overview-global-rate-limit), [TLS client authentication](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/security/ssl#arch-overview-ssl-auth-filter), [HTTP connection management](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_connection_management#arch-overview-http-conn-man), MongoDB [sniffing](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_protocols/mongo#arch-overview-mongo), raw [TCP proxy](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/listeners/listener_filters#arch-overview-tcp-proxy), etc.).

Listeners are optionally also configured with some number of [listener filters](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/listeners/listener_filters#arch-overview-listener-filters). These filters are processed before the network level filters, and have the opportunity to manipulate the connection metadata, usually to influence how the connection is processed by later filters or clusters.

Listeners can also be fetched dynamically via the [listener discovery service (LDS)](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/lds#config-listeners-lds).

Tip

See the Listener [configuration](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/listeners#config-listeners), [protobuf](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto#envoy-v3-api-file-envoy-config-listener-v3-listener-proto) and [components](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-file-envoy-config-listener-v3-listener-components-proto) sections for reference documentation.

## UDP

Envoy also supports UDP listeners and specifically [UDP listener filters](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/udp_filters/udp_filters#config-udp-listener-filters).

UDP listener filters are instantiated once per worker and are global to that worker.

Each listener filter processes each UDP datagram that is received by the worker listening on the port.

In practice, UDP listeners are configured with the `SO_REUSEPORT` kernel option which will cause the kernel to consistently hash each UDP 4-tuple to the same worker. This allows a UDP listener filter to be “session” oriented if it so desires. A built-in example of this functionality is the [UDP proxy](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/udp_filters/udp_proxy#config-udp-listener-filters-udp-proxy) listener filter.