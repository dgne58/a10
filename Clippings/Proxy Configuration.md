---
title: "Proxy Configuration"
source: "https://linkerd.io/2-edge/reference/proxy-configuration/"
author:
published:
created: 2026-04-15
description: "Linkerd provides a set of annotations that can be used to override the data plane proxy's configuration."
tags:
  - "clippings"
---
Linkerd provides a set of annotations that can be used to **override** the data plane proxy’s configuration. This is useful for **overriding** the default configurations of [auto-injected proxies](https://linkerd.io/2-edge/features/proxy-injection/).

The following is the list of supported annotations:

| Annotation | Description |
| --- | --- |
| `config.alpha.linkerd.io/proxy-enable-native-sidecar` | Enable KEP-753 native sidecars. This is a beta feature. It requires Kubernetes >= 1.29. If enabled,.proxy.waitBeforeExitSeconds should not be used. Deprecated in favor of config.beta.linkerd.io/proxy-enable-native-sidecar |
| `config.alpha.linkerd.io/proxy-wait-before-exit-seconds` | Adds a preStop hook to the proxy container to delay receiving SIGTERM signal from Kubernetes but no longer than pod’s `terminationGracePeriodSeconds`. Defaults to `0` |
| `config.beta.linkerd.io/proxy-enable-native-sidecar` | Enable KEP-753 native sidecars. This is a beta feature. It requires Kubernetes >= 1.29. If enabled,.proxy.waitBeforeExitSeconds should not be used. |
| `config.linkerd.io/access-log` | Enables HTTP access logging in the proxy. Accepted values are `apache`, to output the access log in the Appache Common Log Format, and `json`, to output the access log in JSON. |
| `config.linkerd.io/admin-port` | Proxy port to serve metrics on |
| `config.linkerd.io/close-wait-timeout` | Sets nf\_conntrack\_tcp\_timeout\_close\_wait. Accepts a duration string, e.g. `1m` or `3600s` |
| `config.linkerd.io/control-port` | Proxy port to use for control |
| `config.linkerd.io/debug-image` | Linkerd debug container image name |
| `config.linkerd.io/debug-image-pull-policy` | Docker image pull policy for debug image |
| `config.linkerd.io/debug-image-version` | Linkerd debug container image version |
| `config.linkerd.io/default-inbound-policy` | Proxy’s default inbound policy |
| `config.linkerd.io/enable-debug-sidecar` | Inject a debug sidecar for data plane debugging |
| `config.linkerd.io/enable-external-profiles` | Enable service profiles for non-Kubernetes services |
| `config.linkerd.io/image-pull-policy` | Docker image pull policy |
| `config.linkerd.io/inbound-port` | Proxy port to use for inbound traffic |
| `config.linkerd.io/init-image` | Linkerd init container image name |
| `config.linkerd.io/init-image-version` | Linkerd init container image version |
| `config.linkerd.io/opaque-ports` | Ports that skip the proxy’s protocol detection mechanism and are proxied opaquely. Comma-separated list of values, where each value can be a port number or a range `a-b`. |
| `config.linkerd.io/outbound-port` | Proxy port to use for outbound traffic |
| `config.linkerd.io/pod-inbound-ports` | Comma-separated list of (non-proxy) container ports exposed by the pod spec. Useful when other mutating webhooks inject sidecar containers after the proxy injector has run |
| `config.linkerd.io/proxy-await` | The application container will not start until the proxy is ready; accepted values are `enabled` and `disabled` |
| `config.linkerd.io/proxy-cpu-limit` | Maximum amount of CPU units that the proxy sidecar can use |
| `config.linkerd.io/proxy-cpu-ratio-limit` | Maximum ratio of proxy worker threads to total available CPUs on the node |
| `config.linkerd.io/proxy-cpu-request` | Amount of CPU units that the proxy sidecar requests |
| `config.linkerd.io/proxy-disable-inbound-protocol-detect-timeout` | When set to true, disables the protocol detection timeout on the inbound side of the proxy by setting it to a very high value |
| `config.linkerd.io/proxy-disable-outbound-protocol-detect-timeout` | When set to true, disables the protocol detection timeout on the outbound side of the proxy by setting it to a very high value |
| `config.linkerd.io/proxy-ephemeral-storage-limit` | Used to override the limitEphemeralStorage config |
| `config.linkerd.io/proxy-ephemeral-storage-request` | Used to override the requestEphemeralStorage config |
| `config.linkerd.io/proxy-gid` | Run the proxy under this group ID |
| `config.linkerd.io/proxy-image` | Linkerd proxy container image name |
| `config.linkerd.io/proxy-inbound-connect-timeout` | Inbound TCP connection timeout in the proxy. Defaults to `100ms` |
| `config.linkerd.io/proxy-inbound-discovery-cache-unused-timeout` | Maximum time allowed before an unused inbound discovery result is evicted from the cache. Defaults to `90s` |
| `config.linkerd.io/proxy-log-format` | Log format (plain or json) for the proxy |
| `config.linkerd.io/proxy-log-level` | Log level for the proxy |
| `config.linkerd.io/proxy-memory-limit` | Maximum amount of Memory that the proxy sidecar can use |
| `config.linkerd.io/proxy-memory-request` | Amount of Memory that the proxy sidecar requests |
| `config.linkerd.io/proxy-outbound-connect-timeout` | Used to configure the outbound TCP connection timeout in the proxy. Defaults to `1000ms` |
| `config.linkerd.io/proxy-outbound-discovery-cache-unused-timeout` | Maximum time allowed before an unused outbound discovery result is evicted from the cache. Defaults to `5s` |
| `config.linkerd.io/proxy-uid` | Run the proxy under this user ID |
| `config.linkerd.io/proxy-version` | Tag to be used for the Linkerd proxy images |
| `config.linkerd.io/shutdown-grace-period` | Grace period for graceful proxy shutdowns. If this timeout elapses before all open connections have completed, the proxy will terminate forcefully, closing any remaining connections. |
| `config.linkerd.io/skip-inbound-ports` | Ports that should skip the proxy and send directly to the application. Comma-separated list of values, where each value can be a port number or a range `a-b`. |
| `config.linkerd.io/skip-outbound-ports` | Outbound ports that should skip the proxy. Comma-separated list of values, where each value can be a port number or a range `a-b`. |
| `config.linkerd.io/skip-subnets` | Comma-separated list of subnets in valid CIDR format that should be skipped by the proxy |
| `linkerd.io/inject` | Controls whether or not a pod should be injected; accepted values are `enabled`, `disabled` and `ingress` |

For example, to update an auto-injected proxy’s CPU and memory resources, we insert the appropriate annotations into the `spec.template.metadata.annotations` of the owner’s pod spec, using `kubectl edit` like this:

```yaml
spec:
  template:
    metadata:
      annotations:
        config.linkerd.io/proxy-cpu-limit: '1'
        config.linkerd.io/proxy-cpu-request: '0.2'
        config.linkerd.io/proxy-memory-limit: 2Gi
        config.linkerd.io/proxy-memory-request: 128Mi
```

[See here](https://linkerd.io/2-edge/tasks/configuring-proxy-concurrency/) for details on tuning the proxy’s resource usage.

For proxies injected using the `linkerd inject` command, configuration can be overridden using the [command-line flags](https://linkerd.io/2-edge/reference/cli/inject/).

## Ingress Mode

> [!-warning] -warning
> #### Warning
> 
> When an ingress is meshed in `ingress` mode by using `linkerd.io/inject: ingress`, the ingress *must* be configured to remove the `l5d-dst-override` header to avoid creating an open relay to cluster-local and external endpoints.

Proxy ingress mode is a mode of operation designed to help Linkerd integrate with certain ingress controllers. Ingress mode is necessary if the ingress itself cannot be otherwise configured to use the Service port/ip as the destination.

When an individual Linkerd proxy is set to `ingress` mode, it will route requests based on their `:authority`, `Host`, or `l5d-dst-override` headers instead of their original destination. This will inform Linkerd to override the endpoint selection of the ingress container and to perform its own endpoint selection, enabling features such as per-route metrics and traffic splitting.

The proxy can be configured to run in `ingress` mode by using the `linkerd.io/inject: ingress` annotation rather than the default `linkerd.io/inject: enabled` annotation. This can also be done with the `--ingress` flag in the `inject` CLI command:

```bash
kubectl get deployment <ingress-controller> -n <ingress-namespace> -o yaml | linkerd inject --ingress - | kubectl apply -f -
```