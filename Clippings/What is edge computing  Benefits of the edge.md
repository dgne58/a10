---
title: "What is edge computing? | Benefits of the edge"
source: "https://www.cloudflare.com/learning/serverless/glossary/what-is-edge-computing/"
author:
published:
created: 2026-04-15
description: "Edge computing moves computing closer to data sources, reducing latency and bandwidth use. Learn more about edge computing."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

## What is edge computing?

Edge computing optimizes Internet devices and web applications by bringing computing closer to the source of the data. This minimizes the need for long distance communications between client and server, which reduces latency and bandwidth usage.

#### Learning Objectives

After reading this article you will be able to:

- Define edge computing
- Understand what it means to have code run at the network edge
- Outline the pros and cons of edge computing

Copy article link

## What is edge computing?

Edge computing is a networking philosophy focused on bringing computing as close to the source of data as possible in order to reduce latency and bandwidth use. In simpler terms, edge computing means running fewer processes in [the cloud](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/) and moving those processes to local places, such as on a user’s computer, an [IoT device](https://www.cloudflare.com/learning/ddos/glossary/internet-of-things-iot/), or an [edge server](https://www.cloudflare.com/learning/cdn/glossary/edge-server/). Bringing computation to the network’s edge minimizes the amount of long-distance communication that has to happen between a [client and server](https://www.cloudflare.com/learning/serverless/glossary/client-side-vs-server-side/).

## What is the network edge?

For Internet devices, the network edge is where the device, or the local network containing the device, communicates with the Internet. The edge is a bit of a fuzzy term; for example a user’s computer or the processor inside of an IoT camera can be considered the network edge, but the user’s router, ISP, or local edge server are also considered the edge. The important takeaway is that the edge of the network is geographically close to the device, unlike [origin servers](https://www.cloudflare.com/learning/cdn/glossary/origin-server/) and cloud servers, which can be very far from the devices they communicate with.

## What differentiates edge computing from other computing models?

The first computers were large, bulky machines that could only be accessed directly or via terminals that were basically an extension of the computer. With the invention of personal computers, computing could take place in a much more distributed fashion. For a time, personal computing was the dominant computing model. Applications ran and data was stored locally on a user's device, or sometimes within an on-premise data center.

Cloud computing, a more recent development, offered a number of advantages over this locally based, on-premise computing. Cloud services are centralized in a vendor-managed "cloud" (or collection of data centers) and can be accessed from any device over the Internet.

However, cloud computing can introduce [latency](https://www.cloudflare.com/learning/performance/glossary/what-is-latency/) because of the distance between users and the data centers where cloud services are hosted. Edge computing moves computing closer to end users to minimize the distance that data has to travel, while still retaining the centralized nature of cloud computing.

To summarize:

- Early computing: Centralized applications only running on one isolated computer
- Personal computing: Decentralized applications running locally
- Cloud computing: Centralized applications running in data centers
- Edge computing: Centralized applications running close to users, either on the device itself or on the network edge

## What is an example of edge computing?

Consider a building secured with dozens of high-definition IoT video cameras. These are "dumb" cameras that simply output a raw video signal and continuously [stream](https://www.cloudflare.com/learning/video/what-is-streaming/) that signal to a cloud server. On the cloud server, the video output from all the cameras is put through a motion-detection application to ensure that only clips featuring activity are saved to the server’s database. This means there is a constant and significant strain on the building’s Internet infrastructure, as significant bandwidth gets consumed by the high volume of video footage being transferred. Additionally, there is very heavy load on the cloud server that has to process the video footage from all the cameras simultaneously.

Now imagine that the motion sensor computation is moved to the network edge. What if each camera used its own internal computer to run the motion-detecting application and then sent footage to the cloud server as needed? This would result in a significant reduction in bandwidth use, because much of the camera footage will never have to travel to the cloud server.

Additionally, the cloud server would now only be responsible for storing the important footage, meaning that the server could communicate with a higher number of cameras without getting overloaded. This is what edge computing looks like.

## What are other possible use cases for edge computing?

Edge computing can be incorporated into a wide variety of applications, products, and services. A few possibilities include:

- Security system monitoring: As described above.
- IoT devices: Smart devices that connect to the Internet can benefit from running code on the device itself, rather than in the cloud, for more efficient user interactions.
- Self-driving cars: Autonomous vehicles need to react in real time, without waiting for instructions from a server.
- More efficient caching: By running code on a [CDN](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) edge network, an application can customize how content is cached to more efficiently serve content to users.
- Medical monitoring devices: It is crucial for medical devices to respond in real time without waiting to hear from a cloud server.
- Video conferencing: [Interactive live video](https://www.cloudflare.com/developer-platform/solutions/live-streaming/) takes quite a bit of bandwidth, so moving backend processes closer to the source of the video can decrease lag and latency.

## What are the benefits of edge computing?

#### Cost savings

As seen in the example above, edge computing helps minimize bandwidth use and server resources. Bandwidth and cloud resources are finite and cost money. With every household and office becoming equipped with smart cameras, printers, thermostats, and even toasters, Statista [predicts](https://www.statista.com/statistics/471264/iot-number-of-connected-devices-worldwide/) that by 2025 there will be over 75 billion IoT devices installed worldwide. In order to support all those devices, significant amounts of computation will have to be moved to the edge.

#### Performance

Another significant benefit of moving processes to the edge is to reduce latency. Every time a device needs to communicate with a distant server somewhere, that creates a delay. For example, two coworkers in the same office chatting over an IM platform might experience a sizable delay because each message has to be routed out of the building, communicate with a server somewhere across the globe, and be brought back before it appears on the recipient’s screen. If that process is brought to the edge, and the company’s internal router is in charge of transferring intra-office chats, that noticeable delay would not exist.

Similarly, when users of all kinds of web applications run into processes that have to communicate with an external server, they will encounter delays. The duration of these delays will vary based upon their available bandwidth and the location of the server, but these delays can be avoided altogether by bringing more processes to the network edge.

#### New functionality

In addition, edge computing can provide new functionality that wasn’t previously available. For example, a company can use edge computing to process and analyze their data at the edge, which makes it possible to do so in real time.

To recap, the key benefits of edge computing are:

- Decreased latency
- Decrease in bandwidth use and associated cost
- Decrease in server resources and associated cost
- Added functionality

## What are the drawbacks of edge computing?

One drawback of edge computing is that it can increase [attack vectors](https://www.cloudflare.com/learning/security/glossary/attack-vector/). With the addition of more "smart" devices into the mix, such as edge servers and IoT devices that have robust built-in computers, there are new opportunities for malicious attackers to compromise these devices.

Another drawback with edge computing is that it requires more local hardware. For example, while an IoT camera needs a built-in computer to send its raw video data to a web server, it would require a much more sophisticated computer with more processing power in order for it to run its own motion-detection algorithms. But the dropping costs of hardware are making it cheaper to build smarter devices.

One way to completely mitigate the need for extra hardware is to take advantage of edge servers. For example, with Cloudflare’s network of 330 geographically distributed edge locations, Cloudflare customers can have edge code running worldwide using [Cloudflare Workers](https://www.cloudflare.com/products/cloudflare-workers/).