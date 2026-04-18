---
title: "HTTPRoute"
source: "https://linkerd.io/2-edge/reference/httproute/"
author:
published:
created: 2026-04-15
description: "Reference guide to HTTPRoute resources."
tags:
  - "clippings"
---
An HTTPRoute is a Kubernetes resource which attaches to a “parent” resource, such as a [Service](https://kubernetes.io/docs/concepts/services-networking/service/), and defines a set of rules which match HTTP requests to that resource. These rules can be based on parameters such as path, method, headers, or other aspects of the HTTP request.

HTTPRoutes are used to configure various aspects of Linkerd’s behavior, and form part of [Linkerd’s support for the Gateway API](https://linkerd.io/2-edge/features/gateway-api/).

> [!-info] -info
> #### Note
> 
> The HTTPRoute resource is part of the Gateway API and is not Linkerd-specific. The canonical reference doc is the [Gateway API HTTPRoute documentation](https://gateway-api.sigs.k8s.io/api-types/httproute/). This page is intended as a *supplement* to that doc, and will detail how this type is used by Linkerd specifically.

## Inbound vs outbound HTTPRoutes

HTTPRoutes usage in Linkerd falls into two categories: configuration of *inbound* behavior and configuration of *outbound* behavior.

**Inbound behavior.** HTTPRoutes with a [Server](https://linkerd.io/2-edge/reference/authorization-policy/#server) as their parent resource configure policy for *inbound* traffic to pods which receive traffic to that [Server](https://linkerd.io/2-edge/reference/authorization-policy/#server). Inbound HTTPRoutes are used to configure fine-grained [per-route authorization and authentication policies](https://linkerd.io/2-edge/tasks/configuring-per-route-policy/).

**Outbound behavior.** HTTPRoutes with a [Service](https://kubernetes.io/docs/concepts/services-networking/service/) as their parent resource configure policies for *outbound* proxies in pods which are clients of that [Service](https://kubernetes.io/docs/concepts/services-networking/service/). Outbound policy includes [dynamic request routing](https://linkerd.io/2-edge/tasks/configuring-dynamic-request-routing/), adding request headers, modifying a request’s path, and reliability features such as [timeouts](https://linkerd.io/2-edge/reference/httproute/#httproutetimeouts).

> [!-warning] -warning
> #### Warning
> 
> **Outbound HTTPRoutes and [ServiceProfiles](https://linkerd.io/2-edge/reference/service-profiles/) provide overlapping configuration.** For backwards-compatibility reasons, a ServiceProfile will take precedence over HTTPRoutes which configure the same Service. If a ServiceProfile is defined for the parent Service of an HTTPRoute, proxies will use the ServiceProfile configuration, rather than the HTTPRoute configuration, as long as the ServiceProfile exists.

## Usage in practice

See important notes in the [Gateway API](https://gateway-api.sigs.k8s.io/) documentation about using these types in practice, including ownership of types and compatible versions.

## The policy.linkerd.io group

In earlier Linkerd versions, Linkerd provided a variant of the HTTPRoute resource in the `policy.linkerd.io` group. These versions are still supported but are not actively maintained; users are encouraged to switch to the canonical `gateway.networking.kubernetes.io` resources.

## HTTPRoute Spec

An HTTPRoute spec may contain the following top level fields:

| field | value |
| --- | --- |
| `parentRefs` | A set of [ParentReference](https://linkerd.io/2-edge/reference/httproute/#parentreference) s which indicate which \[Server\]s or Services this HTTPRoute attaches to. |
| `hostnames` | A set of hostnames that should match against the HTTP Host header. |
| `rules` | An array of [HTTPRouteRules](https://linkerd.io/2-edge/reference/httproute/#httprouterule). |

### parentReference

A reference to the parent resource this HTTPRoute is a part of.

HTTPRoutes can be attached to a [Server](https://linkerd.io/2-edge/reference/authorization-policy/#server) to allow defining an [authorization policy](https://linkerd.io/2-edge/reference/authorization-policy/#authorizationpolicy) for specific routes served on that Server.

HTTPRoutes can also be attached to a Service, in order to route requests depending on path, headers, query params, and/or verb. Requests can then be rerouted to different backend services. This can be used to perform [dynamic request routing](https://linkerd.io/2-edge/tasks/configuring-dynamic-request-routing/).

ParentReferences are namespaced, and may reference either a parent in the same namespace as the HTTPRoute, or one in a different namespace. As described in [GEP-1426](https://gateway-api.sigs.k8s.io/geps/gep-1426/#namespace-boundaries), a HTTPRoute with a `parentRef` that references a Service in the same namespace as the HTTPRoute is referred to as a *producer route*, while an HTTPRoute with a `parentRef` referencing a Service in a different namespace is referred to as a *consumer route*. A producer route will apply to requests originating from clients in any namespace. On the other hand, a consumer route is scoped to apply only to traffic originating in the HTTPRoute’s namespace. See the [“Namespace boundaries” section in GEP-1426](https://gateway-api.sigs.k8s.io/geps/gep-1426/#namespace-boundaries) for details on producer and consumer routes.

| field | value |
| --- | --- |
| `group` | The group of the referent. This must either be “policy.linkerd.io” (for Server) or “core” (for Service). |
| `kind` | The kind of the referent. This must be either “Server” or “Service”. |
| `port` | The targeted port number, when attaching to Services. |
| `namespace` | The namespace of the referent. When unspecified (or empty string), this refers to the local namespace of the Route. |
| `name` | The name of the referent. |

### httpRouteRule

HTTPRouteRule defines semantics for matching an HTTP request based on conditions (matches) and processing it (filters).

| field | value |
| --- | --- |
| `matches` | A list of [httpRouteMatches](https://linkerd.io/2-edge/reference/httproute/#httproutematch). Each match is independent, i.e. this rule will be matched if **any** one of the matches is satisfied. |
| `filters` | A list of [httpRouteFilters](https://linkerd.io/2-edge/reference/httproute/#httproutefilter) which will be applied to each request which matches this rule. |
| `backendRefs` | An array of [HTTPBackendRefs](https://linkerd.io/2-edge/reference/httproute/#httpbackendref) to declare where the traffic should be routed to (only allowed with Service [parentRefs](https://linkerd.io/2-edge/reference/httproute/#parentreference)). |
| `timeouts` | An optional [httpRouteTimeouts](https://linkerd.io/2-edge/reference/httproute/#httproutetimeouts) object which configures timeouts for requests matching this rule. |

### httpRouteMatch

HTTPRouteMatch defines the predicate used to match requests to a given action. Multiple match types are ANDed together, i.e. the match will evaluate to true only if all conditions are satisfied.

| field | value |
| --- | --- |
| `path` | An [httpPathMatch](https://linkerd.io/2-edge/reference/httproute/#httppathmatch). If this field is not specified, a default prefix match on the “/” path is provided. |
| `headers` | A list of [httpHeaderMatches](https://linkerd.io/2-edge/reference/httproute/#httpheadermatch). Multiple match values are ANDed together. |
| `queryParams` | A list of [httpQueryParamMatches](https://linkerd.io/2-edge/reference/httproute/#httpqueryparammatch). Multiple match values are ANDed together. |
| `method` | When specified, this route will be matched only if the request has the specified method. |

### httpPathMatch

`HTTPPathMatch` describes how to select a HTTP route by matching the HTTP request path.

| field | value |
| --- | --- |
| `type` | How to match against the path Value. One of: Exact, PathPrefix, RegularExpression. If this field is not specified, a default of “PathPrefix” is provided. |
| `value` | The HTTP path to match against. |

### httpHeaderMatch

`HTTPHeaderMatch` describes how to select a HTTP route by matching HTTP request headers.

| field | value |
| --- | --- |
| `type` | How to match against the value of the header. One of: Exact, RegularExpression. If this field is not specified, a default of “Exact” is provided. |
| `name` | The HTTP Header to be matched against. Name matching MUST be case insensitive. |
| `value` | Value of HTTP Header to be matched. |

### httpQueryParamMatch

`HTTPQueryParamMatch` describes how to select a HTTP route by matching HTTP query parameters.

| field | value |
| --- | --- |
| `type` | How to match against the value of the query parameter. One of: Exact, RegularExpression. If this field is not specified, a default of “Exact” is provided. |
| `name` | The HTTP query param to be matched. This must be an exact string match. |
| `value` | Value of HTTP query param to be matched. |

### httpRouteFilter

HTTPRouteFilter defines processing steps that must be completed during the request or response lifecycle.

| field | value |
| --- | --- |
| `type` | One of: RequestHeaderModifier, ResponseHeaderModifier, or RequestRedirect. |
| `requestHeaderModifier` | An [httpHeaderFilter](https://linkerd.io/2-edge/reference/httproute/#httpheaderfilter) which modifies request headers. |
| `responseHeaderModifier` | An [httpHeaderFilter](https://linkerd.io/2-edge/reference/httproute/#httpheaderfilter) which modifies response headers. |
| `requestRedirect` | An [httpRequestRedirectFilter](https://linkerd.io/2-edge/reference/httproute/#httprequestredirectfilter). |

### httpHeaderFilter

A filter which modifies HTTP request or response headers.

| field | value |
| --- | --- |
| `set` | A list of [httpHeaders](https://linkerd.io/2-edge/reference/httproute/#httpheader) to overwrite on the request or response. |
| `add` | A list of [httpHeaders](https://linkerd.io/2-edge/reference/httproute/#httpheader) to add on to the request or response, appending to any existing value. |
| `remove` | A list of header names to remove from the request or response. |

### httpHeader

`HTTPHeader` represents an HTTP Header name and value as defined by RFC 7230.

| field | value |
| --- | --- |
| `name` | Name of the HTTP Header to be matched. Name matching MUST be case insensitive. |
| `value` | Value of HTTP Header to be matched. |

### httpRequestRedirectFilter

`HTTPRequestRedirect` defines a filter that redirects a request.

| field | value |
| --- | --- |
| `scheme` | The scheme to be used in the value of the `Location` header in the response. When empty, the scheme of the request is used. |
| `hostname` | The hostname to be used in the value of the `Location` header in the response. When empty, the hostname of the request is used. |
| `path` | An [httpPathModfier](https://linkerd.io/2-edge/reference/httproute/#httppathmodfier) which modifies the path of the incoming request and uses the modified path in the `Location` header. |
| `port` | The port to be used in the value of the `Location` header in the response. When empty, port (if specified) of the request is used. |
| `statusCode` | The HTTP status code to be used in response. |

### httpPathModfier

`HTTPPathModifier` defines configuration for path modifiers.

| field | value |
| --- | --- |
| `type` | One of: ReplaceFullPath, ReplacePrefixMatch. |
| `replaceFullPath` | The value with which to replace the full path of a request during a rewrite or redirect. |
| `replacePrefixMatch` | The value with which to replace the prefix match of a request during a rewrite or redirect. |

### httpBackendRef

`HTTPBackendRef` defines the list of objects where matching requests should be sent to. Only allowed when a route has Service [parentRefs](https://linkerd.io/2-edge/reference/httproute/#parentreference).

| field | value |
| --- | --- |
| `name` | Name of service for this backend. |
| `port` | Destination port number for this backend. |
| `namespace` | Namespace of service for this backend. |
| `weight` | Proportion of requests sent to this backend. |

### httpRouteTimeouts

`HTTPRouteTimeouts` defines the timeouts that can be configured for an HTTP request.

Linkerd implements HTTPRoute timeouts as described in [GEP-1742](https://gateway-api.sigs.k8s.io/geps/gep-1742/). Timeout durations are specified as strings using the [Gateway API duration format](https://gateway-api.sigs.k8s.io/geps/gep-2257/#gateway-api-duration-format) specified by [GEP-2257](https://gateway-api.sigs.k8s.io/geps/gep-2257/) (e.g. 1h/1m/1s/1ms), and MUST be at least 1ms. A timeout field with duration 0 disables that timeout.

| field | value |
| --- | --- |
| `request` | Specifies the duration for processing an HTTP client request after which the proxy will time out if unable to send a response. When this field is unspecified or 0, the proxy will not enforce request timeouts. |
| `backendRequest` | Specifies a timeout for an individual request from the proxy to a backend service. This covers the time from when the request first starts being sent from the proxy to when the response has been received from the backend. When this field is unspecified or 0, the proxy will not enforce a backend request timeout, but may still enforce the `request` timeout, if one is configured. |

If retries are enabled, a request received by the proxy may be retried by sending it to a different backend. In this case, a new `backendRequest` timeout will be started for each retry request, but each retry request will count against the overall `request` timeout.

## HTTPRoute Examples

An HTTPRoute attached to a Server resource which matches GETs to `/authors.json` or `/authors/*`:

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: authors-get-route
  namespace: booksapp
spec:
  parentRefs:
    - name: authors-server
      kind: Server
      group: policy.linkerd.io
  rules:
    - matches:
        - path:
            value: "/authors.json"
          method: GET
        - path:
            value: "/authors/"
            type: "PathPrefix"
          method: GET
```

An HTTPRoute attached to a Service to perform header-based routing. If there’s a `x-faces-user: testuser` header in the request, the request is routed to the `smiley2` backend Service. Otherwise, the request is routed to the `smiley` backend Service.

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: smiley-a-b
  namespace: faces
spec:
  parentRefs:
    - name: smiley
      kind: Service
      group: core
      port: 80
  rules:
    - matches:
        - headers:
            - name: "x-faces-user"
              value: "testuser"
      backendRefs:
        - name: smiley2
          port: 80
    - backendRefs:
        - name: smiley
          port: 80
```