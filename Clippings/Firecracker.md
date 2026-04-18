---
title: "Firecracker"
source: "https://firecracker-microvm.github.io/"
author:
published:
created: 2026-04-15
description:
tags:
  - "clippings"
---
Secure and fast microVMs for serverless computing

[View on GitHub](https://github.com/firecracker-microvm/firecracker)

Firecracker enables you to deploy workloads in lightweight virtual machines, called microVMs, which provide enhanced security and workload isolation over traditional VMs, while enabling the speed and resource efficiency of containers. Firecracker was developed at Amazon Web Services to improve the customer experience of services like [AWS Lambda](https://aws.amazon.com/lambda/) and [AWS Fargate](https://aws.amazon.com/fargate/).

Firecracker is a virtual machine monitor (VMM) that uses the Linux Kernel-based Virtual Machine (KVM) to create and manage microVMs. Firecracker has a minimalist design. It excludes unnecessary devices and guest functionality to reduce the memory footprint and attack surface area of each microVM. This improves security, decreases the startup time, and increases hardware utilization. Firecracker is generally available on [64-bit Intel, AMD and Arm CPUs with support for hardware virtualization.](https://github.com/firecracker-microvm/firecracker#supported-platforms)

Firecracker is used by/integrated with (in alphabetical order): [appfleet](https://appfleet.com/), containerd via [firecracker-containerd](https://github.com/firecracker-microvm/firecracker-containerd), [Fly.io](https://fly.io/), [Kata Containers](https://github.com/kata-containers/documentation/wiki/Initial-release-of-Kata-Containers-with-Firecracker-support), [Koyeb](https://www.koyeb.com/), [Northflank](https://northflank.com/), [OpenNebula](https://opennebula.io/firecracker/), [Qovery](https://www.qovery.com/), [UniK](https://github.com/solo-io/unik), [webapp.io](https://webapp.io/), and [microvm.nix](https://github.com/astro/microvm.nix). Firecracker can run Linux and [OSv](http://blog.osv.io/blog/2019/04/19/making-OSv-run-on-firecraker) guests. Our latest roadmap can be found [here](https://github.com/orgs/firecracker-microvm/projects/42).

Benefits

![Security icon](https://firecracker-microvm.github.io/img/security-icon@3x.png)

Firecracker microVMs use KVM-based virtualizations that provide enhanced security over traditional VMs. This ensures that workloads from different end customers can run safely on the same machine. Firecracker also implements a minimal device model that excludes all non-essential functionality and reduces the attack surface area of the microVM.

![Speed icon](https://firecracker-microvm.github.io/img/speed-icon@3x.png)

In addition to a minimal device model, Firecracker also accelerates kernel loading and provides a minimal guest kernel configuration. This enables fast startup times. Firecracker initiates user space or application code in as little as 125 ms and supports microVM creation rates of up to 150 microVMs per second per host.

![hardware icon](https://firecracker-microvm.github.io/img/hardware-icon@3x.png)

Each Firecracker microVM runs with a reduced memory overhead of less than 5 MiB, enabling a high density of microVMs to be packed on each server. Firecracker provides a rate limiter built into every microVM. This enables optimized sharing of network and storage resources, even across thousands of microVMs.

The following diagram depicts an example host running Firecracker microVMs.

![Firecracker diagram](https://firecracker-microvm.github.io/img/graph-mobile@3x.png)

Firecracker runs in user space and uses the Linux Kernel-based Virtual Machine (KVM) to create microVMs. The fast startup time and low memory overhead of each microVM enables you to pack thousands of microVMs onto the same machine. This means that every function, container, or container group can be encapsulated with a virtual machine barrier, enabling workloads from different customers to run on the same machine, without any tradeoffs to security or efficiency. Firecracker is an [alternative to QEMU](https://www.redhat.com/en/blog/all-you-need-know-about-kvm-userspace), an established VMM with a general purpose and broad feature set that allows it to host a variety of guest operating systems.

You can control the Firecracker process via a RESTful API that enables common actions such as configuring the number of vCPUs or starting the machine. It provides built-in rate limiters, which allows you to granularly control network and storage resources used by thousands of microVMs on the same machine. You can create and configure rate limiters via the Firecracker API and define flexible rate limiters that support bursts or specific bandwidth/operations limitations. Firecracker also provides a metadata service that securely shares configuration information between the host and guest operating system. You can set up and configure the metadata service using the Firecracker API. Each Firecracker microVM is further isolated with common Linux user-space security barriers by a companion program called "jailer". The jailer provides a second line of defense in case the virtualization barrier is ever compromised.

FAQs

Firecracker was built by developers at Amazon Web Services to enable services such as [AWS Lambda](https://aws.amazon.com/lambda/) and [AWS Fargate](https://aws.amazon.com/fargate/) to improve resource utilization and customer experience, while providing the security and isolation required of public cloud infrastructure. Firecracker started from Chromium OS's Virtual Machine Monitor, [crosvm](https://chromium.googlesource.com/chromiumos/platform/crosvm/), an open source VMM written in Rust. Today, crosvm and Firecracker have diverged to serve very different customer needs. [Rust-vmm](https://github.com/rust-vmm) is an open source community where we collaborate with crosvm and other groups and individuals to build and share quality Rust virtualization components.

When we launched Lambda in November of 2014, we were focused on providing a secure [serverless](https://aws.amazon.com/serverless/) experience. At launch we used per-customer EC2 instances to provide strong security and isolation between customers. As Lambda grew, we saw the need for technology to provide a highly secure, flexible, and efficient runtime environment for services like Lambda and Fargate. Using our experience building isolated EC2 instances with hardware virtualization technology, we started an effort to build a VMM that was tailored to run serverless functions and integrate with container ecosystems.

The Firecracker VMM is built to be processor agnostic. 64-bit Intel, AMD and Arm CPUs with hardware virtualization support are generally available for production workloads.

Firecracker is written in Rust.

Yes. Firecracker is used by/integrated with (in alphabetical order): [appfleet](https://appfleet.com/), containerd via [firecracker-containerd](https://github.com/firecracker-microvm/firecracker-containerd), [Fly.io](https://fly.io/), [Kata Containers](https://github.com/kata-containers/documentation/wiki/Initial-release-of-Kata-Containers-with-Firecracker-support), [Koyeb](https://www.koyeb.com/), [Northflank](https://northflank.com/), [OpenNebula](https://opennebula.io/firecracker/), [Qovery](https://www.qovery.com/), [UniK](https://github.com/solo-io/unik), [webapp.io](https://webapp.io/), and [microvm.nix](https://github.com/astro/microvm.nix).

Firecracker is an [alternative to QEMU](https://www.redhat.com/en/blog/all-you-need-know-about-kvm-userspace) that is purpose-built for running serverless functions and containers safely and efficiently, and nothing more. Firecracker is written in Rust, provides a minimal required device model to the guest operating system while excluding non-essential functionality (only 5 emulated devices are available: virtio-net, virtio-block, virtio-vsock, serial console, and a minimal keyboard controller used only to stop the microVM). This, along with a streamlined kernel loading process enables a < 125 ms startup time and a < 5 MiB memory footprint. The Firecracker process also provides a RESTful control API, handles resource rate limiting for microVMs, and provides a microVM metadata service to enable the sharing of configuration data between the host and guest.

Firecracker supports Linux host and guest operating systems with kernel versions 4.14 and above, as well as [OSv](http://blog.osv.io/blog/2019/04/19/making-OSv-run-on-firecraker/) guests. The long-term support plan is still under discussion.

Firecracker is [licensed](https://github.com/firecracker-microvm/firecracker/blob/master/LICENSE) under Apache License, version 2.0, allowing you to freely use, copy, and distribute your changes under the terms of your choice. Read more about the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0). Crosvm code sections are licensed under a [BSD-3-Clause license](https://opensource.org/licenses/BSD-3-Clause) that also allows you to use, copy, and distribute your changes under the terms of your choice.

Firecracker is an AWS open source project that encourages contributions from customers and the developer community. Any contribution is welcome as long as it aligns with our [charter](https://github.com/firecracker-microvm/firecracker/blob/master/CHARTER.md). You can learn more about how to contribute in [CONTRIBUTING.md](https://github.com/firecracker-microvm/firecracker/blob/master/CONTRIBUTING.md) . You can chat with others in the community on the [Firecracker Slack workspace](https://join.slack.com/t/firecracker-microvm/shared_invite/zt-3v81btcpe-usCf8Qk7k1gUlSAEKKdYMg) .

Learn More[Read about why AWS decided to build Firecracker, and how it improves security and efficiency.](https://aws.amazon.com/blogs/aws/firecracker-lightweight-virtualization-for-serverless-computing)

[

Read about how to get started with Firecracker, where the project is headed, and how you can join, contribute, and collaborate.

](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/)

Get Involved