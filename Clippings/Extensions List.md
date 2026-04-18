---
title: "Extensions List"
source: "https://linkerd.io/2-edge/reference/extension-list/"
author:
published:
created: 2026-04-15
description: "List of Linkerd extensions that can be added to the installation for additional functionality"
tags:
  - "clippings"
---
Linkerd provides a mix of built-in and third-party [extensions](https://linkerd.io/2-edge/tasks/extensions/) to add additional functionality to the base installation. The following is the list of known extensions:

| Name | Description |
| --- | --- |
| [multicluster](https://github.com/linkerd/linkerd2/tree/main/multicluster/charts/linkerd-multicluster) | Built-in extension that enables multicluster support for Linkerd. |
| [smi](https://github.com/linkerd/linkerd-smi/tree/main/charts/linkerd-smi) | The Linkerd SMI extension helps users to have SMI functionality in Linkerd-enabled Kubernetes clusters. |
| [tapshark](https://github.com/adleong/tapshark) | Wireshark inspired ncurses-style CLI for Linkerd Tap |
| [viz](https://github.com/linkerd/linkerd2/tree/main/viz/charts/linkerd-viz) | Built-in extension that provides observability and visualization components for Linkerd. |
| [easyauth](https://github.com/aatarasoff/linkerd-easyauth) | Simplify the Linkerd Authorization Policies management. |

If you have an extension for Linkerd and it is not on the list, [please edit this page!](https://github.com/linkerd/website/edit/main/linkerd.io/data/extension-list.yaml)