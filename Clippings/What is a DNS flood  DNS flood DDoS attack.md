---
title: "What is a DNS flood? | DNS flood DDoS attack"
source: "https://www.cloudflare.com/learning/ddos/dns-flood-ddos-attack/"
author:
published:
created: 2026-04-15
description: "A DNS flood is a type of distributed denial-of-service attack (DDoS) where an attacker floods a particular domain’s DNS servers in an attempt to disrupt DNS resolution for that domain."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

A DNS flood is a DDoS attack that aims to flood and overwhelm a target DNS server.

#### Learning Objectives

After reading this article you will be able to:

- Define a DNS Flood DDoS attack
- Walkthough how a DNS flood attack disables a target
- Understand methods of mitigation for a DNS flood

Copy article link

## What is a DNS Flood?

Domain Name System ([DNS](https://www.cloudflare.com/learning/dns/what-is-dns/)) servers are the “phonebooks” of the Internet; they are the path through which Internet devices are able to lookup specific web servers in order to access Internet content. A DNS flood is a type of [distributed denial-of-service attack (DDoS)](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) where an attacker floods a particular domain’s DNS servers in an attempt to disrupt DNS resolution for that [domain](https://www.cloudflare.com/learning/dns/glossary/what-is-a-domain-name/). If a user is unable to find the phonebook, it cannot lookup the address in order to make the call for a particular resource. By disrupting DNS resolution, a DNS flood attack will compromise a website, API, or web application's ability respond to legitimate traffic. DNS flood attacks can be difficult to distinguish from normal heavy traffic because the large volume of traffic often comes from a multitude of unique locations, querying for real records on the domain, mimicking legitimate traffic.

## How does a DNS flood attack work?

![DNS Flood DDoS Attack Diagram](https://cf-assets.www.cloudflare.com/slt3lc6tev37/36x0QwH3pnMZIE0F0foIoB/0fa53ce6f40961f6b85fdbd338d4fd04/dns-flood-ddos-attack-diagram-2.svg)

The function of the Domain Name System is to translate between easy to remember names (e.g. example.com) and hard to remember addresses of website servers (e.g. 192.168.0.1), so successfully attacking DNS infrastructure makes the Internet unusable for most people. DNS flood attacks constitute a relatively new type of DNS-based attack that has proliferated with the rise of high bandwidth [Internet of Things (IoT)](https://www.cloudflare.com/learning/ddos/glossary/internet-of-things-iot/) [botnets](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-botnet/) like [Mirai](https://www.cloudflare.com/learning/ddos/glossary/mirai-botnet/). DNS flood attacks use the high bandwidth connections of IP cameras, DVR boxes and other IoT devices to directly overwhelm the DNS servers of major providers. The volume of requests from IoT devices overwhelms the DNS provider’s services and prevents legitimate users from accessing the provider's DNS servers.

DNS flood attacks differ from [DNS amplification attacks](https://www.cloudflare.com/learning/ddos/dns-amplification-ddos-attack/). Unlike DNS floods, DNS amplification attacks reflect and amplify traffic off unsecured DNS servers in order to hide the origin of the attack and increase its effectiveness. DNS amplification attacks use devices with smaller bandwidth connections to make numerous requests to unsecured [DNS servers](https://www.cloudflare.com/learning/dns/dns-server-types/). The devices make many small requests for very large [DNS records](https://www.cloudflare.com/learning/dns/dns-records/), but when making the requests, the attacker forges the return address to be that of the intended victim. The amplification allows the attacker to take out larger targets with only limited attack resources.

Under Attack?

[Talk to an expert](https://www.cloudflare.com/under-attack-hotline/)

## How can a DNS Flood attack be mitigated?

DNS floods represent a change from traditional amplification-based attack methods. With easily accessible high bandwidth botnets, attackers can now target large organizations. Until compromised IoT devices can be updated or replaced, the only way to withstand these types of attacks is to use a very large and highly distributed DNS system that can monitor, absorb, and block the attack traffic in realtime. Learn about how Cloudflare's [DDoS Protection](https://www.cloudflare.com/ddos/) protects against DNS flood attacks.