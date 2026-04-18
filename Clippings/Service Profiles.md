---
title: "Service Profiles"
source: "https://linkerd.io/2-edge/reference/service-profiles/"
author:
published:
created: 2026-04-15
description: "Details on the specification and what is possible with service profiles."
tags:
  - "clippings"
---
> [!-warning] -warning
> #### Warning
> 
> As of Linkerd 2.16, ServiceProfiles have been fully supplanted by [Gateway API types](https://linkerd.io/2-edge/features/gateway-api/), including for getting per-route metrics, specifying timeouts, and specifying retries. Service profiles continue to be supported for backwards compatibility, but will not receive further feature development.

[Service profiles](https://linkerd.io/2-edge/features/service-profiles/) provide Linkerd additional information about a service. This is a reference for everything that can be done with service profiles.

## Spec

A service profile spec must contain the following top level fields:

| field | value |
| --- | --- |
| `routes` | a list of [route](https://linkerd.io/2-edge/reference/service-profiles/#route) objects |
| `retryBudget` | a [retry budget](https://linkerd.io/2-edge/reference/service-profiles/#retry-budget) object that defines the maximum retry rate to this service |

## Route

A route object must contain the following fields:

| field | value |
| --- | --- |
| `name` | the name of this route as it will appear in the route label |
| `condition` | a [request match](https://linkerd.io/2-edge/reference/service-profiles/#request-match) object that defines if a request matches this route |
| `responseClasses` | (optional) a list of [response class](https://linkerd.io/2-edge/reference/service-profiles/#response-class) objects |
| `isRetryable` | indicates that requests to this route are always safe to retry and will cause the proxy to retry failed requests on this route whenever possible |
| `timeout` | the maximum amount of time to wait for a response (including retries) to complete after the request is sent |

## Request Match

A request match object must contain *exactly one* of the following fields:

| field | value |
| --- | --- |
| `pathRegex` | a regular expression to match the request path against |
| `method` | one of GET, POST, PUT, DELETE, OPTION, HEAD, TRACE |
| `all` | a list of [request match](https://linkerd.io/2-edge/reference/service-profiles/#request-match) objects which must *all* match |
| `any` | a list of [request match](https://linkerd.io/2-edge/reference/service-profiles/#request-match) objects, at least one of which must match |
| `not` | a [request match](https://linkerd.io/2-edge/reference/service-profiles/#request-match) object which must *not* match |

### Request Match Usage Examples

The simplest condition is a path regular expression:

```yaml
pathRegex: '/authors/\d+'
```

This is a condition that checks the request method:

```yaml
method: POST
```

If more than one condition field is set, all of them must be satisfied. This is equivalent to using the ‘all’ condition:

```yaml
all:
  - pathRegex: '/authors/\d+'
  - method: POST
```

Conditions can be combined using ‘all’, ‘any’, and ’not’:

```yaml
any:
  - all:
      - method: POST
      - pathRegex: '/authors/\d+'
  - all:
      - not:
          method: DELETE
      - pathRegex: /info.txt
```

## Response Class

A response class object must contain the following fields:

| field | value |
| --- | --- |
| `condition` | a [response match](https://linkerd.io/2-edge/reference/service-profiles/#response-match) object that defines if a response matches this response class |
| `isFailure` | a boolean that defines if these responses should be classified as failed |

## Response Match

A response match object must contain *exactly one* of the following fields:

| field | value |
| --- | --- |
| `status` | a [status range](https://linkerd.io/2-edge/reference/service-profiles/#status-range) object to match the response status code against |
| `all` | a list of [response match](https://linkerd.io/2-edge/reference/service-profiles/#response-match) objects which must *all* match |
| `any` | a list of [response match](https://linkerd.io/2-edge/reference/service-profiles/#response-match) objects, at least one of which must match |
| `not` | a [response match](https://linkerd.io/2-edge/reference/service-profiles/#response-match) object which must *not* match |

Response Match conditions can be combined in a similar way as shown above for [Request Match Usage Examples](https://linkerd.io/2-edge/reference/service-profiles/#request-match-usage-examples)

## Status Range

A status range object must contain *at least one* of the following fields. Specifying only one of min or max matches just that one status code.

| field | value |
| --- | --- |
| `min` | the status code must be greater than or equal to this value |
| `max` | the status code must be less than or equal to this value |

## Retry Budget

A retry budget specifies the maximum total number of retries that should be sent to this service as a ratio of the original request volume.

| field | value |
| --- | --- |
| `retryRatio` | the maximum ratio of retries requests to original requests |
| `minRetriesPerSecond` | allowance of retries per second in addition to those allowed by the retryRatio |
| `ttl` | indicates for how long requests should be considered for the purposes of calculating the retryRatio |