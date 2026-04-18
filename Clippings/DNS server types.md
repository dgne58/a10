---
title: "DNS server types"
source: "https://www.cloudflare.com/learning/dns/dns-server-types/"
author:
published:
created: 2026-04-15
description: "The four main DNS server types are recursive resolvers, authoritative nameservers, TLD nameservers, and root nameservers."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

There are four different types of DNS servers that have to work in harmony to deliver a single webpage.

#### Learning Objectives

After reading this article you will be able to:

- Identify the four types of DNS server
- Understand how they work in harmony to fulfill DNS requests

Copy article link

### Free DNS included with any Cloudflare plan

## What are the different types of DNS server?

All DNS servers fall into one of four categories: Recursive resolvers, [root nameservers](https://www.cloudflare.com/learning/dns/glossary/dns-root-server/), TLD nameservers, and authoritative nameservers. In a typical DNS lookup (when there is no [caching](https://www.cloudflare.com/learning/cdn/what-is-caching/) in play), these four DNS servers work together in harmony to complete the task of delivering the [IP address](https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/) for a specified [domain](https://www.cloudflare.com/learning/dns/glossary/what-is-a-domain-name/) to the client (the client is usually a stub resolver - a simple resolver built into an operating system).

## What is a DNS recursive resolver?

![DNS recursive resolver](https://www.cloudflare.com/img/learning/dns/dns-server-types/recursive-resolver.png)

A recursive resolver (also known as a DNS recursor) is the first stop in a DNS query. The recursive resolver acts as a middleman between a client and a DNS nameserver. After receiving a DNS query from a web client, a recursive resolver will either respond with cached data, or send a request to a root nameserver, followed by another request to a TLD nameserver, and then one last request to an authoritative nameserver. After receiving a response from the authoritative nameserver containing the requested IP address, the recursive resolver then sends a response to the client.

During this process, the recursive resolver will cache information received from authoritative nameservers. When a client requests the IP address of a domain name that was recently requested by another client, the resolver can circumvent the process of communicating with the nameservers, and just deliver the client the requested record from its cache.

Most Internet users use a recursive resolver provided by their ISP, but there are other options available; for example [Cloudflare's 1.1.1.1](https://www.cloudflare.com/learning/dns/what-is-1.1.1.1/).

## What is a DNS root nameserver?

![DNS root nameserver](https://www.cloudflare.com/img/learning/dns/dns-server-types/root-nameserver.png)

The 13 DNS root nameservers are known to every recursive resolver, and they are the first stop in a recursive resolver’s quest for DNS records. A root server accepts a recursive resolver’s query which includes a domain name, and the root nameserver responds by directing the recursive resolver to a TLD nameserver, based on the extension of that domain (.com,.net,.org, etc.). The root nameservers are overseen by a nonprofit called the Internet Corporation for Assigned Names and Numbers (ICANN).

Note that while there are 13 root nameservers, that does not mean that there are only 13 machines in the root nameserver system. There are 13 types of root nameservers, but there are multiple copies of each one all over the world, which use [Anycast routing](https://www.cloudflare.com/learning/cdn/glossary/anycast-network/) to provide speedy responses. If you added up all the instances of root nameservers, you’d have over 600 different servers.

## What is a TLD nameserver?

![DNS TLD nameserver](https://www.cloudflare.com/img/learning/dns/dns-server-types/tld-nameserver.png)

A TLD nameserver maintains information for all the domain names that share a common domain extension, such as.com,.net, or whatever comes after the last dot in a URL. For example, a.com TLD nameserver contains information for every website that ends in ‘.com’. If a user was searching for google.com, after receiving a response from a root nameserver, the recursive resolver would then send a query to a.com TLD nameserver, which would respond by pointing to the authoritative nameserver (see below) for that domain.

Management of TLD nameservers is handled by the Internet Assigned Numbers Authority (IANA), which is a branch of ICANN. The IANA breaks up the TLD servers into two main groups:

- Generic top-level domains: These are domains that are not country specific, some of the best-known generic TLDs include.com, [.org](https://www.cloudflare.com/application-services/products/registrar/buy-org-domains/),.net,.edu, and.gov.
- Country code top-level domains: These include any domains that are specific to a country or state. Examples include.uk,.us,.ru, and.jp.

There is actually a third category for infrastructure domains, but it is almost never used. This category was created for the.arpa domain, which was a transitional domain used in the creation of modern DNS; its significance today is mostly historical.

## What is an authoritative nameserver?

When a recursive resolver receives a response from a TLD nameserver, that response will direct the resolver to an authoritative nameserver. The authoritative nameserver is usually the resolver’s last step in the journey for an IP address. The authoritative nameserver contains information specific to the domain name it serves (e.g. google.com) and it can provide a recursive resolver with the IP address of that server found in the [DNS A record](https://www.cloudflare.com/learning/dns/dns-records/dns-a-record/), or if the domain has a [CNAME record](https://www.cloudflare.com/learning/dns/dns-records/dns-cname-record/) (alias) it will provide the recursive resolver with an alias domain, at which point the recursive resolver will have to perform a whole new DNS lookup to procure a record from an authoritative nameserver (often an A record containing an IP address). [Cloudflare DNS](https://www.cloudflare.com/dns/) distributes authoritative nameservers, which come with Anycast routing to make them more reliable.