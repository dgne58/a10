---
title: "What is a LAN (local area network)?"
source: "https://www.cloudflare.com/learning/network-layer/what-is-a-lan/"
author:
published:
created: 2026-04-15
description: "A LAN, or local area network, is a group of connected computers that share a centralized Internet connection. Learn how LAN networks work."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

A LAN, or local area network, is a group of connected computing devices within a localized area that usually share a centralized Internet connection.

#### Learning Objectives

After reading this article you will be able to:

- Understand what 'LAN' stands for
- Learn about the equipment necessary to set up a LAN
- Compare LANs, WANs, and virtual LANs

Copy article link

## What is a LAN (local area network)?

A local area network (LAN) is a network contained within a small geographic area, usually within the same building. Home WiFi networks and [small business networks](https://www.cloudflare.com/small-business/) are common examples of LANs.

LANs can also be fairly large, although if they take up multiple buildings, it is usually more accurate to classify them as [wide area networks (WAN)](https://www.cloudflare.com/learning/network-layer/what-is-a-wan/) or [metropolitan area networks (MAN)](https://www.cloudflare.com/learning/network-layer/what-is-a-metropolitan-area-network/).

![Local Area Network LAN - Computers connect to router which connects to Internet](https://www.cloudflare.com/resources/images/slt3lc6tev37/78rJr5URxwDD9uyxKNpsiJ/d220f31e4b59c89290f04eed689ab5bb/what_is_LAN_diagram.png)

## How do LANs work?

Most LANs connect to the [Internet](https://www.cloudflare.com/learning/network-layer/how-does-the-internet-work/) at a central point: a [router](https://www.cloudflare.com/learning/network-layer/what-is-a-router/). Home LANs often use a single router, while LANs in larger spaces may additionally use [network switches](https://www.cloudflare.com/learning/network-layer/what-is-a-network-switch/) for more efficient packet delivery.

LANs almost always use Ethernet, WiFi, or both in order to connect devices within the network. Ethernet is a protocol for physical network connections that requires the use of Ethernet cables. WiFi is a protocol for connecting to a network via radio waves.

A variety of devices can connect to LANs, including servers, desktop computers, laptops, printers, IoT devices, and even game consoles. In offices, LANs are often used to provide shared access to internal employees to connected printers or servers.

## What equipment is needed to set up a LAN?

The simplest Internet-connected LANs require only a router and a way for computing devices to connect to the router, such as via Ethernet cables or a WiFi hotspot. LANs without an Internet connection need a switch for exchanging data. Large LANs, such as those in a large office building, may need additional routers or switches to more efficiently forward data to the right devices.

Not all LANs connect to the Internet. In fact, LANs predate the Internet: the first LANs were used in businesses in the late 1970s. (These old LANs used network protocols that are no longer in use today.) The only requirement for setting up a LAN is that the connected devices are able to exchange data. This usually requires a piece of networking equipment for packet switching, such as a network switch. Today, even non-Internet-connected LANs use the same networking protocols that are used on the Internet (such as [IP](https://www.cloudflare.com/learning/ddos/glossary/internet-protocol/)).

## What is a virtual LAN?

Virtual LANs, or VLANs, are a way of splitting up traffic on the same physical network into two networks. Imagine setting up two separate LANs, each with their own router and Internet connection, in the same room. VLANs are like that, but they are divided virtually using software instead of physically using hardware — only one router with one Internet connection is necessary.

VLANs help with network management, especially with very large LANs. By subdividing the network, administrators can manage the network much more easily. (VLANs are very different from [subnets](https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/), which are another way of subdividing networks for greater efficiency.)

## What is the difference between a LAN and a WAN?

A WAN, or wide area network, is a collection of connected LANs. It is a widespread network of local networks. A WAN can be any size, even thousands of miles wide; it is not restricted to a given area.

## How do LANs relate to the rest of the Internet?

The Internet is a network of networks. LANs usually connect to a much larger network, an [autonomous system (AS)](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/). ASes are very large networks with their own [routing](https://www.cloudflare.com/learning/network-layer/what-is-routing/) policies and with control over certain IP addresses. An Internet service provider (ISP) is one example of an AS.

Picture a LAN as a small network, that connects to a much larger network, that connects to other very large networks, all of which contain LANs. This is the Internet, and two computers connected to two different LANs thousands of miles apart can talk to each other by sending data over these connections between networks.

## How does Cloudflare protect LANs?

On-premise business infrastructure, such as LANs and their accompanying routers, switches, and servers, often face malicious attacks, including [DDoS](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) attacks. [Cloudflare Magic Transit](https://www.cloudflare.com/magic-transit/) protects on-premise networks and infrastructure from malicious attacks, in addition to accelerating legitimate network traffic. Cloudflare Magic Transit also [protects](https://www.cloudflare.com/network-security/) [cloud-hosted](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/) and [hybrid](https://www.cloudflare.com/learning/cloud/what-is-hybrid-cloud/) networks.