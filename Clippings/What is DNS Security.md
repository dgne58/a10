---
title: "What is DNS Security?"
source: "https://www.cloudflare.com/learning/dns/dns-security/"
author:
published:
created: 2026-04-15
description: "DNS-based attacks have led to the adoption of DNS security protocols like DNSSEC. Learn about DNS security and privacy, and how to stop DNS-based attacks."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

DNS was not designed with security in mind, and there are many types of attacks created to exploit vulnerabilities in the DNS system.

#### Learning Objectives

After reading this article you will be able to:

Copy article link

### Free DNS included with any Cloudflare plan

## What is DNS security?

DNS security is the practice of protecting [DNS infrastructure](https://www.cloudflare.com/learning/dns/what-is-dns/) from cyber attacks in order to keep it performing quickly and reliably. An effective DNS security strategy incorporates a number of overlapping defenses, including establishing redundant DNS servers, applying security protocols like DNSSEC, and requiring rigorous DNS logging.

## Why is DNS security important?

Like many Internet [protocols](https://www.cloudflare.com/learning/network-layer/what-is-a-protocol/), the DNS system was not designed with security in mind and contains several design limitations. These limitations, combined with advances in technology, make DNS servers vulnerable to a broad spectrum of attacks, including spoofing, amplification, DoS (Denial of Service), or the interception of private [personal information](https://www.cloudflare.com/learning/privacy/what-is-personal-information/). And since DNS is an integral part of most Internet requests, it can be a prime target for attacks.

In addition, DNS attacks are frequently deployed in conjunction with other cyberattacks to distract security teams from the true target. An organization needs to be able to quickly mitigate DNS attacks so that they are not too busy to handle simultaneous attacks through other vectors.

## What are some common DNS attacks?

Attackers have found a number of ways to target and exploit DNS servers. Here are some of the most common DNS attacks:

**DNS spoofing/ [cache poisoning](https://www.cloudflare.com/learning/dns/dns-cache-poisoning/):** This is an attack where forged DNS data is introduced into a DNS resolver’s cache, resulting in the resolver returning an incorrect [IP address](https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/) for a domain. Instead of going to the correct website, traffic can be diverted to a malicious machine or anywhere else the attacker desires; often this will be a replica of the original site used for malicious purposes such as distributing [malware](https://www.cloudflare.com/learning/ddos/glossary/malware/) or collecting login information.

**DNS tunneling:** This attack uses other protocols to tunnel through DNS queries and responses. Attackers can use SSH, [TCP](https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/), or [HTTP](https://www.cloudflare.com/learning/ddos/glossary/hypertext-transfer-protocol-http/) to pass malware or stolen information into DNS queries, undetected by most [firewalls](https://www.cloudflare.com/learning/security/what-is-a-firewall/).

**DNS hijacking:** In DNS hijacking, the attacker redirects queries to a different domain name server. This can be done either with malware or with the unauthorized modification of a DNS server. Although the result is similar to that of DNS spoofing, this is a fundamentally different attack because it targets the [DNS record](https://www.cloudflare.com/learning/dns/dns-records/) of the website on the nameserver, rather than a resolver’s cache.

![DNS Hijacking](https://www.cloudflare.com/img/learning/dns/dns-security/dns-hijacking.png "DNS Hijacking")

**NXDOMAIN attack:** This is a type of DNS flood attack where an attacker inundates a DNS server with requests, asking for records that do not exist, in an attempt to cause a [denial-of-service](https://www.cloudflare.com/learning/ddos/glossary/denial-of-service/) for legitimate traffic. This can be accomplished using sophisticated attack tools that can auto-generate unique subdomains for each request. NXDOMAIN attacks can also target a recursive resolver with the goal of filling the resolver’s cache with junk requests.

**Phantom domain attack:** A phantom domain attack has a similar result to an NXDOMAIN attack on a DNS resolver. The attacker sets up a bunch of ‘phantom’ domain servers that either respond to requests very slowly or not at all. The resolver is then hit with a flood of requests to these domains and the resolver gets tied up waiting for responses, leading to slow [performance](https://www.cloudflare.com/learning/performance/why-site-speed-matters/) and denial-of-service.

**Random subdomain attack:** In this case, the attacker sends DNS queries for several random, nonexistent subdomains of one legitimate site. The goal is to create a denial-of-service for the domain’s authoritative nameserver, making it impossible to lookup the website from the nameserver. As a side effect, the ISP serving the attacker may also be impacted, as their recursive resolver's cache will be loaded with bad requests.

**Domain lock-up attack:** Attackers orchestrate this form of attack by setting up special domains and resolvers to create TCP connections with other legitimate resolvers. When the targeted resolvers send requests, these domains send back slow streams of random packets, tying up the resolver’s resources.

**Botnet-based CPE attack:** These attacks are carried out using CPE devices (Customer Premise Equipment; this is hardware given out by service providers for use by their customers, such as modems, [routers](https://www.cloudflare.com/learning/network-layer/what-is-a-router/), cable boxes, etc.). The attackers compromise the CPEs and the devices become part of a [botnet](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-botnet/), used to perform random subdomain attacks against one site or domain.

## What is DNSSEC?

DNS Security Extensions (DNSSEC) is a security protocol created to mitigate this problem. DNSSEC protects against attacks by digitally signing data to help ensure its validity. In order to ensure a secure lookup, the signing must happen at every level in the DNS lookup process.

This signing process is similar to someone signing a legal document with a pen; that person signs with a unique signature that no one else can create, and a court expert can look at that signature and verify that the document was signed by that person. These digital signatures ensure that data has not been tampered with.

DNSSEC implements a hierarchical digital signing policy across all layers of DNS. For example, in the case of a ‘google.com’ lookup, a [root DNS server](https://www.cloudflare.com/learning/dns/glossary/dns-root-server/) would sign a key for the [.COM nameserver](https://www.cloudflare.com/learning/dns/dns-server-types/), and the.COM nameserver would then sign a key for google.com’s [authoritative nameserver](https://www.cloudflare.com/learning/dns/dns-server-types/).

While improved security is always preferred, DNSSEC is designed to be backwards-compatible to ensure that traditional DNS lookups still resolve correctly, albeit without the added security. DNSSEC is meant to work with other security measures like [SSL](https://www.cloudflare.com/learning/ssl/what-is-ssl/) / [TLS](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/) as part of a holistic Internet security strategy.

DNSSEC creates a parent-child train of trust that travels all the way up to the [root zone](https://www.cloudflare.com/learning/dns/glossary/dns-zone/). This chain of trust cannot be compromised at any layer of DNS, or else the request will become open to an on-path attack.

To close the chain of trust, the root zone itself needs to be validated (proven to be free of tampering or fraud), and this is actually done using human intervention. Interestingly, in what’s called a [Root Zone Signing Ceremony](https://www.cloudflare.com/dns/dnssec/root-signing-ceremony/), selected individuals from around the world meet to sign the root DNSKEY RRset in a public and audited way.

[Here is a more detailed explanation of how DNSSEC works >>>](https://blog.cloudflare.com/dnssec-an-introduction/)

## What are other ways of protecting against DNS-based attacks?

In addition to DNSSEC, an operator of a DNS zone can take further measures to secure their servers. Over-provisioning infrastructure is one simple strategy to overcome [DDoS attacks](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/). Simply put, if your nameservers can handle several multiples more traffic than you expect, it is harder for a volume-based attack to overwhelm your server. Organizations can accomplish this by increasing their DNS server's total traffic capacity, by establishing [multiple redundant DNS servers](https://www.cloudflare.com/learning/dns/glossary/primary-secondary-dns/), and by using [load balancing](https://www.cloudflare.com/learning/performance/what-is-load-balancing/) to route DNS requests to healthy servers when one begins to perform poorly.

Another strategy still is a DNS firewall.

## What is a DNS firewall?

A DNS firewall is a tool that can provide a number of security and performance services for DNS servers. A DNS firewall sits between a user’s recursive resolver and the authoritative nameserver of the website or service they are trying to reach. The firewall can provide [rate limiting services](https://www.cloudflare.com/learning/bots/what-is-rate-limiting/) to shut down attackers trying to overwhelm the server. If the server does experience downtime as the result of an attack or for any other reason, the DNS firewall can keep the operator’s site or service up by serving DNS responses from cache.

In addition to its security features, a DNS firewall can also provide performance solutions such as faster DNS lookups and reduced bandwidth costs for the DNS operator. [Learn more about Cloudflare’s DNS firewall.](https://www.cloudflare.com/dns/dns-firewall/)

## DNS as a security tool

DNS resolvers can also be configured to provide security solutions for their end users (people browsing the Internet). Some DNS resolvers provide features such as [content filtering](https://www.cloudflare.com/learning/access-management/what-is-dns-filtering/), which can block sites known to distribute malware and [spam](https://www.cloudflare.com/learning/bots/what-is-a-spambot/), and botnet protection, which blocks communication with known botnets. Many of these secured DNS resolvers are free to use and a user can switch to one of these [recursive DNS](https://www.cloudflare.com/learning/dns/what-is-recursive-dns/) services by changing a single setting in their local router. [Cloudflare DNS](https://www.cloudflare.com/dns/) has an emphasis on security (and Cloudflare includes DNS filtering in its [SASE](https://www.cloudflare.com/learning/access-management/what-is-sase/) platform).

## Are DNS queries private?

Another important DNS security issue is [user privacy](https://www.cloudflare.com/learning/privacy/what-is-data-privacy/). DNS queries are not encrypted. Even if users use a DNS resolver like [1.1.1.1](https://www.cloudflare.com/learning/dns/what-is-1.1.1.1/) that does not track their activities, DNS queries travel over the Internet in plaintext. This means anyone who intercepts the query can see which websites the user is visiting.

This lack of privacy has an impact on security and, in some cases, human rights; if DNS queries are not private, then it becomes easier for governments to censor the Internet and for attackers to stalk users' online behavior.

[DNS over TLS and DNS over HTTPS](https://www.cloudflare.com/learning/dns/dns-over-tls/) are two standards for encrypting DNS queries in order to prevent external parties from being able to read them.

## Does Cloudflare offer DNS security?

Cloudflare's [DNS services](https://www.cloudflare.com/dns/) come with a wide variety of security features built-in, including DNSSEC, DDoS mitigation, multi-DNS functionality, and load balancing.

## FAQs

#### What is the primary purpose of DNS security?

DNS security focuses on safeguarding Domain Name System infrastructure against cyber attacks. Because the original DNS was not built with security or privacy in mind, specialized strategies such as using DNSSEC, redundant DNS servers, and rigorous logging are necessary to prevent service disruptions and protect data. Other security measures like DNS over TLS or DNS over HTTPS can help protect user privacy.

#### What is DNSSEC and how does it protect Internet users?

DNS Security Extensions (DNSSEC) is a protocol that uses digital signatures to verify the authenticity of DNS data. By creating a chain of trust from the root zone down to the specific domain, it ensures that the DNS lookup information a user receives has not been tampered with by attackers.

#### How does DNS spoofing, or cache poisoning, impact a website's visitors?

In a DNS spoofing attack, an attacker introduces fraudulent data into a DNS resolver's cache. This causes the resolver to send users to a malicious website instead of the intended destination, which can lead to malware distribution or the theft of login credentials.

#### What is the difference between DNS hijacking and DNS spoofing?

While both attacks redirect traffic, they target different areas. DNS spoofing alters the data stored in a resolver's cache. In contrast, DNS hijacking involves unauthorized changes to the actual DNS record on the nameserver or redirecting queries to a different nameserver entirely, often via malware.

#### How does a DNS firewall help defend against DDoS attacks?

A DNS firewall can provide rate limiting to block attackers trying to overwhelm the system and can keep a service online during an attack by serving DNS responses directly from its cache.

#### Why are standard DNS queries considered a privacy risk?

By default, DNS queries are sent in plaintext, meaning they are not encrypted. This allows anyone who intercepts the query to see which websites a user is visiting. To solve this, standards like DNS over TLS (DoT) and DNS over HTTPS (DoH) are used to encrypt queries and keep online behavior private.

#### What are NXDOMAIN and phantom domain attacks?

Both are types of flood attacks designed to cause a denial-of-service. An NXDOMAIN attack floods a server with requests for records that do not exist, while a phantom domain attack uses phantom servers that respond slowly or not at all to tie up the resolver’s resources.

#### How can over-provisioning infrastructure improve DNS security?

Over-provisioning involves setting up nameservers to handle significantly more traffic than expected. By increasing total capacity and using multiple redundant servers with load balancing, an organization makes it much harder for a volume-based DDoS attack to successfully overwhelm their services.