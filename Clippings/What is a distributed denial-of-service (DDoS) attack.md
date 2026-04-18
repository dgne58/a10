---
title: "What is a distributed denial-of-service (DDoS) attack?"
source: "https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/"
author:
published:
created: 2026-04-15
description: "A distributed denial-of-service (DDoS) attack is a malicious attempt to disrupt normal traffic to a web property. Learn about DDoS attacks and DDoS protection."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

## What is a DDoS attack?

DDoS attacks are a primary concern in Internet security today. Explore details about how DDoS attacks function, and how they can be stopped.

#### Learning Objectives

After reading this article you will be able to:

- Define a DDoS attack
- Explain the general structure of a DDoS attack
- Differentiate between the 3 major categories of DDoS attacks
- Understand several DDoS mitigation strategies

Related Content

---

#### Want to keep learning?

Subscribe to theNET, Cloudflare's monthly recap of the Internet's most popular insights!

Copy article link

## What is a DDoS attack?

<iframe src="https://iframe.videodelivery.net/9d692ec9201d9d47db4a91020b7cbd67?poster=https://videodelivery.net/9d692ec9201d9d47db4a91020b7cbd67/thumbnails/thumbnail.jpg?time=37s&amp;height=270" height="412" width="740" allow="accelerometer; gyroscope; autoplay; defaultTextTrack; encrypted-media; picture-in-picture;" allowfullscreen="true"></iframe>

A distributed denial-of-service (DDoS) attack is a malicious attempt to disrupt the normal traffic of a targeted server, service or network by overwhelming the target or its surrounding infrastructure with a flood of Internet traffic.

DDoS attacks achieve effectiveness by utilizing multiple compromised computer systems as sources of attack traffic. Exploited machines can include computers and other networked resources such as [IoT devices](https://www.cloudflare.com/learning/ddos/glossary/internet-of-things-iot/).

From a high level, a DDoS attack is like an unexpected traffic jam clogging up the highway, preventing regular traffic from arriving at its destination.

![DDoS attack traffic metaphor](https://cf-assets.www.cloudflare.com/slt3lc6tev37/7xwaGxGINeyxavVbrXO6M1/24f139faac6094044adaa84c82394962/ddos_attack_traffic_metaphor.png "DDoS attack traffic metaphor")

Guide

5 things to consider when mitigating DDoS attacks

Report

Secure your DNS infrastructure

  

## How does a DDoS attack work?

DDoS attacks are carried out with networks of Internet-connected machines.

These networks consist of computers and other devices (such as IoT devices)which have been infected with [malware](https://www.cloudflare.com/learning/ddos/glossary/malware/), allowing them to be controlled remotely by an attacker. These individual devices are referred to as [bots](https://www.cloudflare.com/learning/bots/what-is-a-bot/) (or zombies), and a group of bots is called a [botnet](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-botnet/).

Once a botnet has been established, the attacker is able to direct an attack by sending remote instructions to each bot.

When a victim’s server or network is targeted by the botnet, each bot sends requests to the target’s [IP address](https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/), potentially causing the server or network to become overwhelmed, resulting in a [denial-of-service](https://www.cloudflare.com/learning/ddos/glossary/denial-of-service/) to normal traffic.

Because each bot is a legitimate Internet device, separating the attack traffic from normal traffic can be difficult.

  

## How to identify a DDoS attack

The most obvious symptom of a DDoS attack is a site or service suddenly becoming slow or unavailable. But since a number of causes — such a legitimate spike in traffic — can create similar performance issues, further investigation is usually required. Traffic analytics tools can help you spot some of these telltale signs of a DDoS attack:

- Suspicious amounts of traffic originating from a single IP address or IP range
- A flood of traffic from users who share a single behavioral profile, such as device type, geolocation, or web browser version
- An unexplained surge in requests to a single page or endpoint
- Odd traffic patterns such as spikes at odd hours of the day or patterns that appear to be unnatural (e.g. a spike every 10 minutes)

There are other, more specific signs of DDoS attack that can vary depending on the type of attack.

## What are some common types of DDoS attacks?

Different types of DDoS attacks target varying components of a network connection. In order to understand how different DDoS attacks work, it is necessary to know how a network connection is made.

A network connection on the Internet is composed of many different components or “layers”. Like building a house from the ground up, each layer in the model has a different purpose.

The [OSI model](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/), shown below, is a conceptual framework used to describe network connectivity in 7 distinct layers.

![The OSI model 7 layers: application, presentation, session, transport, network, data link, physical](https://cf-assets.www.cloudflare.com/slt3lc6tev37/6ZH2Etm3LlFHTgmkjLmkxp/59ff240fb3ebdc7794ffaa6e1d69b7c2/osi_model_7_layers.png "The OSI model")

While nearly all DDoS attacks involve overwhelming a target device or network with traffic, attacks can be divided into three categories. An attacker may use one or more different attack vectors, or cycle attack vectors in response to counter measures taken by the target.

## Application layer attacks

#### The goal of the attack:

Sometimes referred to as a [layer 7](https://www.cloudflare.com/learning/ddos/what-is-layer-7/) DDoS attack (in reference to the 7th layer of the OSI model), the goal of these attacks is to exhaust the target’s resources to create a denial-of-service.

The attacks target the layer where web pages are generated on the server and delivered in response to [HTTP](https://www.cloudflare.com/learning/ddos/glossary/hypertext-transfer-protocol-http/) requests. A single HTTP request is computationally cheap to execute on the client side, but it can be expensive for the target server to respond to, as the server often loads multiple files and runs database queries in order to create a web page.

Layer 7 attacks are difficult to defend against, since it can be hard to differentiate malicious traffic from legitimate traffic.

#### Application layer attack example:

![HTTP flood DDoS attack: multiple bot HTTP GET requests to victim](https://cf-assets.www.cloudflare.com/slt3lc6tev37/3jlyZeWRy9eBz3tyEk9mxA/96eab064524495e8f6b2647f1f7b9d60/application_layer_ddos_example.png "Application layer DDoS attack example")

#### HTTP flood

This attack is similar to pressing refresh in a web browser over and over on many different computers at once – large numbers of HTTP requests flood the server, resulting in denial-of-service.

This type of attack ranges from simple to complex.

Simpler implementations may access one URL with the same range of attacking IP addresses, referrers and user agents. Complex versions may use a large number of attacking IP addresses, and target random urls using random referrers and user agents.

## Protocol attacks

#### The goal of the attack:

Protocol attacks, also known as a state-exhaustion attacks, cause a service disruption by over-consuming server resources and/or the resources of network equipment like [firewalls](https://www.cloudflare.com/learning/security/what-is-a-firewall/) and load balancers.

Protocol attacks utilize weaknesses in layer 3 and layer 4 of the protocol stack to render the target inaccessible.

#### Protocol attack example:

![Protocol DDoS attack example: SYN flood: spoofed SYN packets](https://cf-assets.www.cloudflare.com/slt3lc6tev37/38KdcqNuv0l0jF4ohUI7bj/44a3f60c5352984258f72a1e69e1bbdd/syn_flood_ddos_example.png "Protocol DDoS attack example")

#### SYN flood

[A SYN Flood](https://www.cloudflare.com/learning/ddos/syn-flood-ddos-attack/) is analogous to a worker in a supply room receiving requests from the front of the store.

The worker receives a request, goes and gets the package, and waits for confirmation before bringing the package out front. The worker then gets many more package requests without confirmation until they can’t carry any more packages, become overwhelmed, and requests start going unanswered.

This attack exploits the [TCP handshake](https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/) — the sequence of communications by which two computers initiate a network connection — by sending a target a large number of TCP “Initial Connection Request” SYN packets with [spoofed](https://www.cloudflare.com/learning/ddos/glossary/ip-spoofing/) source IP addresses.

The target machine responds to each connection request and then waits for the final step in the handshake, which never occurs, exhausting the target’s resources in the process.

## Volumetric attacks

#### The goal of the attack:

This category of attacks attempts to create congestion by consuming all available bandwidth between the target and the larger Internet. Large amounts of data are sent to a target by using a form of amplification or another means of creating massive traffic, such as requests from a botnet.

#### Amplification example:

![Amplification DDoS attack example: DNS amplification: spoofed DNS requests](https://cf-assets.www.cloudflare.com/slt3lc6tev37/1FIBEeoyzoa64lVGlWKaRV/3b878bb03df1729b48cd3f667cdfe3de/amplification_ddos_example.png "Amplification DDoS attack example")

#### DNS Amplification

A [DNS amplification](https://www.cloudflare.com/learning/ddos/dns-amplification-ddos-attack/) is like if someone were to call a restaurant and say “I’ll have one of everything, please call me back and repeat my whole order,” where the callback number actually belongs to the victim. With very little effort, a long response is generated and sent to the victim.

By making a request to an open [DNS](https://www.cloudflare.com/learning/dns/what-is-dns/) server with a spoofed IP address (the IP address of the victim), the target IP address then receives a response from the server.

## What is the process for mitigating a DDoS attack?

The key concern in mitigating a DDoS attack is differentiating between attack traffic and normal traffic.

For example, if a product release has a company’s website swamped with eager customers, cutting off all traffic is a mistake. If that company suddenly has a surge in traffic from known attackers, efforts to alleviate an attack are probably necessary.

The difficulty lies in telling the real customers apart from the attack traffic.

In the modern Internet, DDoS traffic comes in many forms. The traffic can vary in design from un-spoofed single source attacks to complex and adaptive multi-vector attacks.

A multi-vector DDoS attack uses multiple attack pathways in order to overwhelm a target in different ways, potentially distracting mitigation efforts on any one trajectory.

An attack that targets multiple layers of the protocol stack at the same time, such as a DNS amplification (targeting layers 3/4) coupled with an [HTTP flood](https://www.cloudflare.com/learning/ddos/http-flood-ddos-attack/) (targeting layer 7) is an example of multi-vector DDoS.

Mitigating a multi-vector DDoS attack requires a variety of strategies in order to counter different trajectories.

Generally speaking, the more complex the attack, the more likely it is that the attack traffic will be difficult to separate from normal traffic - the goal of the attacker is to blend in as much as possible, making mitigation efforts as inefficient as possible.

Mitigation attempts that involve dropping or limiting traffic indiscriminately may throw good traffic out with the bad, and the attack may also modify and adapt to circumvent countermeasures. In order to overcome a complex attempt at disruption, a layered solution will give the greatest benefit.

#### Blackhole routing

One solution available to virtually all network admins is to create a [blackhole](https://www.cloudflare.com/learning/ddos/glossary/ddos-blackhole-routing/) route and funnel traffic into that route. In its simplest form, when blackhole filtering is implemented without specific restriction criteria, both legitimate and malicious network traffic is routed to a null route, or blackhole, and dropped from the network.

If an Internet property is experiencing a DDoS attack, the property’s Internet service provider (ISP) may send all the site’s traffic into a blackhole as a defense. This is not an ideal solution, as it effectively gives the attacker their desired goal: it makes the network inaccessible.

#### Rate limiting

Limiting the number of requests a server will accept over a certain time window is also a way of mitigating denial-of-service attacks.

---

While rate limiting is useful in [slowing web scrapers from stealing content](https://www.cloudflare.com/learning/ai/how-to-prevent-web-scraping/) and for mitigating [brute force](https://www.cloudflare.com/learning/bots/brute-force-attack/) login attempts, it alone will likely be insufficient to handle a complex DDoS attack effectively.

Nevertheless, rate limiting is a useful component in an effective DDoS mitigation strategy. Learn about [Cloudflare's rate limiting](https://www.cloudflare.com/application-services/products/rate-limiting/)

#### Web application firewall

A [Web Application Firewall (WAF)](https://www.cloudflare.com/learning/ddos/glossary/web-application-firewall-waf/) is a tool that can assist in mitigating a layer 7 DDoS attack. By putting a WAF between the Internet and an origin server, the WAF may act as a [reverse proxy](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/), protecting the targeted server from certain types of malicious traffic.

By filtering requests based on a series of rules used to identify DDoS tools, layer 7 attacks can be impeded. One key value of an effective WAF is the ability to [quickly implement custom rules](https://developers.cloudflare.com/firewall/) in response to an attack. Learn about [Cloudflare's WAF](https://www.cloudflare.com/application-services/products/waf/).

#### Anycast network diffusion

This mitigation approach uses an Anycast network to scatter the attack traffic across a network of distributed servers to the point where the traffic is absorbed by the network.

Like channeling a rushing river down separate smaller channels, this approach spreads the impact of the distributed attack traffic to the point where it becomes manageable, diffusing any disruptive capability.

The reliability of an [Anycast network](https://www.cloudflare.com/learning/cdn/glossary/anycast-network/) to mitigate a DDoS attack is dependent on the size of the attack and the size and efficiency of the network. An important part of the DDoS mitigation implemented by Cloudflare is the use of an Anycast distributed network.

Cloudflare has a 477 Tbps network, which is an order of magnitude greater than the largest DDoS attack recorded.

If you are currently [under attack](https://www.cloudflare.com/under-attack-hotline/), there are steps you can take to get out from under the pressure. If you are on Cloudflare already, you can follow [these steps](https://support.cloudflare.com/hc/en-us/articles/200170196-I-am-under-DDoS-attack-what-do-I-do-) to mitigate your attack.

The DDoS protection that we implement at Cloudflare is multifaceted in order to mitigate the many possible attack vectors. Learn more about Cloudflare's [DDoS protection](https://www.cloudflare.com/ddos/) and how it works.