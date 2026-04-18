---
title: "Listener filters — envoy 1.38.0-dev-550d57 documentation"
source: "https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/listeners/listener_filters"
author:
published:
created: 2026-04-15
description:
tags:
  - "clippings"
---
## Listener filters

Envoy’s [listener filters](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-listenerfilter) may be used to manipulate connection metadata.

The main purpose of [listener filters](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-listenerfilter) are to make adding further system integration functions easier by not requiring changes to Envoy core functionality, and also to make interaction between multiple such features more explicit.

The API for [listener filters](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-listenerfilter) is relatively simple since ultimately these filters operate on newly accepted sockets.

Filters in the chain can stop and subsequently continue iteration to further filters. This allows for more complex scenarios such as calling a [rate limiting service](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_features/global_rate_limiting#arch-overview-global-rate-limit), etc.

Envoy includes several listener filters that are documented in this architecture overview as well as the [configuration reference](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/listener_filters/listener_filters#config-listener-filters).

## Filter chains

### Filter chain match

Network filters are [chained](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto#envoy-v3-api-field-config-listener-v3-listener-filter-chains) in an ordered list of [FilterChain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain).

Each listener can have multiple [FilterChain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) and an optional [default\_filter\_chain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener.proto#envoy-v3-api-field-config-listener-v3-listener-default-filter-chain).

Upon receiving a request, the [FilterChain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) with the most specific [match](https://www.envoyproxy.io/docs/envoy/latest/xds/type/matcher/v3/matcher.proto#envoy-v3-api-msg-xds-type-matcher-v3-matcher) criteria is used.

If no matching [FilterChain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) is found, the default filter chain will be used to serve the request, where configured, otherwise the connection will be closed.

### Filter chain only update

[Filter chains](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) can be updated independently.

Upon listener config update, if the listener manager determines that the listener update is a filter chain only update, the listener update will be executed by adding, updating and removing filter chains.

The connections owned by these destroying filter chains will be drained as described [here](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/operations/draining#arch-overview-draining).

If the new [filter chain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) and the old [filter chain](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#envoy-v3-api-msg-config-listener-v3-filterchain) is protobuf message equivalent, the corresponding filter chain runtime info survives. The connections owned by the survived filter chains remain open.

Not all the listener config updates can be executed by filter chain update. For example, if the listener metadata is updated within the new listener config, the new metadata must be picked up by the new filter chains. In this case, the entire listener is drained and updated.

## Network (L3/L4) filters

Network level (L3/L4) filters form the core of Envoy connection handling. The filter API allows for different sets of filters to be mixed and matched and attached to a given listener. There are three different types of network filters:

**Read**

Read filters are invoked when Envoy receives data from a downstream connection.

**Write**

Write filters are invoked when Envoy is about to send data to a downstream connection.

**Read/Write**

Read/Write filters are invoked both when Envoy receives data from a downstream connection and when it is about to send data to a downstream connection.

The API for network level filters is relatively simple since ultimately the filters operate on raw bytes and a small number of connection events (e.g., TLS handshake complete, connection disconnected locally or remotely, etc.).

Filters in the chain can stop and subsequently continue iteration to further filters. This allows for more complex scenarios such as calling a [rate limiting service](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_features/global_rate_limiting#arch-overview-global-rate-limit), etc.

Network level filters can also share state (static and dynamic) among themselves within the context of a single downstream connection. Refer to [data sharing between filters](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/advanced/data_sharing_between_filters#arch-overview-data-sharing-between-filters) for more details.

Tip

See the listener [configuration](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/network_filters/network_filters#config-network-filters) and [protobuf](https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/filters/network/http_connection_manager/v3/http_connection_manager.proto#envoy-v3-api-file-envoy-extensions-filters-network-http-connection-manager-v3-http-connection-manager-proto) sections for reference documentation.

See [here](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/listener/v3/listener_components.proto#extension-category-envoy-filters-network) for included filters.

### TCP proxy filter

The TCP proxy filter performs basic 1:1 network connection proxy between downstream clients and upstream clusters.

It can be used by itself as an stunnel replacement, or in conjunction with other filters such as the [MongoDB filter](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/other_protocols/mongo#arch-overview-mongo) or the [rate limit](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/network_filters/rate_limit_filter#config-network-filters-rate-limit) filter.

The TCP proxy filter will respect the [connection limits](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/circuit_breaker.proto#envoy-v3-api-field-config-cluster-v3-circuitbreakers-thresholds-max-connections) imposed by each upstream cluster’s global resource manager. The TCP proxy filter checks with the upstream cluster’s resource manager if it can create a connection without going over that cluster’s maximum number of connections, if it can’t the TCP proxy will not make the connection.

Tip

See the [TCP proxy configuration](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/network_filters/network_filters#config-network-filters) and [protobuf](https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/filters/network/tcp_proxy/v3/tcp_proxy.proto#envoy-v3-api-msg-extensions-filters-network-tcp-proxy-v3-tcpproxy) sections for reference documentation.

### UDP proxy filter

Envoy supports UDP proxy via the [UDP proxy listener filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/udp_filters/udp_proxy#config-udp-listener-filters-udp-proxy).

### DNS filter

Envoy supports responding to DNS requests by configuring a [UDP listener DNS Filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/udp_filters/dns_filter#config-udp-listener-filters-dns-filter).

The DNS filter supports responding to forward queries for `A` and `AAAA` records.

The answers are discovered from statically configured resources, clusters, or external DNS servers.

The filter will return DNS responses up to 512 bytes. If domains are configured with multiple addresses, or clusters with multiple endpoints, Envoy will return each discovered address up to the aforementioned size limit.

### Connection limiting filter

Envoy supports local (non-distributed) connection limiting of L4 connections via the [Connection limit filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/network_filters/connection_limit_filter#config-network-filters-connection-limit) and runtime connection limiting via the [Runtime listener connection limit](https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/runtime#config-listeners-runtime).