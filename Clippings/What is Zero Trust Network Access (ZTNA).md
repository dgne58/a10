---
title: "What is Zero Trust Network Access (ZTNA)?"
source: "https://www.cloudflare.com/learning/access-management/what-is-ztna/"
author:
published:
created: 2026-04-15
description: "ZTNA is the technology that enables organizations to implement a Zero Trust security model. Learn how ZTNA works, contrast ZTNA with VPNs, and more."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

Zero Trust Network Access (ZTNA) is the technology that enables organizations to implement a Zero Trust security model.

#### Learning Objectives

After reading this article you will be able to:

Copy article link

## What is ZTNA?

Zero Trust Network Access (ZTNA) is the technology that makes it possible to [implement a Zero Trust security model](https://www.cloudflare.com/learning/access-management/how-to-implement-zero-trust/). " [Zero Trust](https://www.cloudflare.com/learning/security/glossary/what-is-zero-trust/) " is an IT security model that assumes threats are present both inside and outside a network. Consequently, Zero Trust requires strict verification for every user and every device before authorizing them to access internal resources.

![Zero Trust Network Access ZTNA: Multiple security checks for user and device](https://cf-assets.www.cloudflare.com/slt3lc6tev37/1jOEf4X6jaguxmVlSnIsnV/01243b7d4d03636ef178c9f209e3ebbc/what_is_zero_trust_network_access_ZTNA-resized.png)

ZTNA is similar to the [software-defined perimeter](https://www.cloudflare.com/learning/access-management/software-defined-perimeter/) (SDP) approach to controlling access. In ZTNA, like in SDP, connected devices are not aware of any resources (applications, servers, etc.) on the network other than what they are connected to.

Imagine a scenario in which every resident gets a phone book with the phone numbers of every other resident of their city, and anyone can dial any number to contact any other person. Now imagine a scenario in which everyone has an unlisted phone number and one resident has to know another resident's phone number in order to call them. This second scenario offers a few advantages: no unwanted calls, no accidental calls to the wrong person, and no risk of unscrupulous persons using the city's phone book to fool or scam the residents.

ZTNA is like the second scenario. But instead of phone numbers, ZTNA uses "unlisted" [IP addresses](https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/), applications, and services. It sets up one-to-one connections between users and the resources they need, like when two people who need to contact each other exchange phone numbers. But unlike two people exchanging numbers, ZTNA connections need to be re-verified and recreated periodically.

Article

Elevating organizational trust with Zero Trust

Guide

The Zero Trust guide to securing aplication access

#### ZTNA vs. VPN

[Virtual private networks (VPNs)](https://www.cloudflare.com/learning/access-management/what-is-a-vpn/) are what many organizations use to [control access](https://www.cloudflare.com/learning/access-management/what-is-access-control/) instead of [ZTNA](https://www.cloudflare.com/the-net/zero-trust-network-access/). Once users are logged in to a VPN, they gain access to the entire network and all the resources on that network (this is often called the [castle-and-moat model](https://www.cloudflare.com/learning/access-management/castle-and-moat-network-security/)). ZTNA instead only grants access to the specific application requested and denies access to applications and data by default.

There are differences between ZTNA and VPNs on a technical level as well. Some of these differences include:

1. **OSI model layer:** Many VPNs run on the [IPsec protocol](https://www.cloudflare.com/learning/network-layer/what-is-ipsec/) at layer 3, the [network layer](https://www.cloudflare.com/learning/network-layer/what-is-the-network-layer/) in the [OSI model](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/). ZTNA typically operates on the [application layer](https://www.cloudflare.com/learning/ddos/what-is-layer-7/). (Some VPNs do run on the application layer using the [TLS protocol](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/) for [encryption](https://www.cloudflare.com/learning/ssl/what-is-encryption/) instead of IPsec; ZTNA usually has a similar approach.)
2. **Endpoint software installation:** [IPsec VPNs](https://www.cloudflare.com/learning/network-layer/ipsec-vs-ssl-vpn/) require the installation of software on all user devices. This is sometimes the case for ZTNA, but not always.
3. **Hardware:** VPNs often require the use of on-premise VPN servers, and user devices connect to these servers, typically by getting through their organization's perimeter [firewall](https://www.cloudflare.com/learning/security/what-is-a-firewall/). ZTNA can be configured in this way, but most often is delivered through [the cloud](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/), enabling users to connect from anywhere without impacting network performance.
4. **Level of connectivity:** ZTNA sets up one-to-one encrypted connections between a user's device and a given application or server. VPNs give users encrypted access to an entire [LAN](https://www.cloudflare.com/learning/network-layer/what-is-a-lan/) all at once. If a user's IP address connects with the network, it can connect with all IP addresses on that network.

Finally, VPNs are imprecise, largely treating users and devices the same, regardless of where they are and what they need to access. With "bring your own device" (BYOD) approaches becoming increasingly common, it is dangerous to allow this access, as any malware-compromised endpoint can then infect an entire network. For these reasons, VPNs are a frequent attack target.

## How does ZTNA work?

ZTNA is configured slightly differently by each organization or vendor. However, there are several underlying principles that remain consistent across ZTNA architectures:

- **Application vs. network access:** ZTNA treats application access separately from network access. Connecting to a network does not automatically grant a user the right to access an application.
- **Hidden IP addresses:** ZTNA does not expose IP addresses to the network. The rest of the network remains invisible to connected devices, except for the application or service they are connected to.
- **Device security:** ZTNA can incorporate the risk and security posture of devices as factors in access decisions. It does this by running software on the device itself (see "Agent-based ZTNA vs. service-based ZTNA" below) or by analyzing network traffic to and from the device.
- **Additional factors:** Unlike traditional access control, which only grants access based on user identity and role, ZTNA can evaluate risks associated with additional factors like user location, timing and frequency of requests, the apps and data being requested, and more. A user could sign in to a network or application, but if their device is not trusted, access is denied.
- **No MPLS:** ZTNA uses encrypted Internet connections over TLS instead of [MPLS](https://www.cloudflare.com/learning/network-layer/what-is-mpls/) -based [WAN](https://www.cloudflare.com/learning/network-layer/what-is-a-wan/) connections. Traditional corporate networks are built on private MPLS connections. ZTNA is built on the public Internet instead, using TLS encryption to keep network traffic private. ZTNA sets up small encrypted [tunnels](https://www.cloudflare.com/learning/network-layer/what-is-tunneling/) between a user and an application, as opposed to connecting a user to a larger network.
- **IdP and SSO:** Most [ZTNA solutions](https://www.cloudflare.com/sase/use-cases/) integrate with separate [identity providers (IdPs)](https://www.cloudflare.com/learning/access-management/what-is-an-identity-provider/), [single sign-on (SSO)](https://www.cloudflare.com/learning/access-management/what-is-sso/) platforms, or both. SSO allows users to authenticate identity for all applications; the IdP stores user identity and determines associated user privileges.
- **Agent vs. service:** ZTNA can either use an endpoint agent or be based in the cloud. The difference is explained below.

#### Agent-based ZTNA vs. service-based ZTNA

Agent-based ZTNA requires the installation of a software application called an "agent" on all [endpoint](https://www.cloudflare.com/learning/security/glossary/what-is-endpoint/) devices.

Service-based or cloud-based ZTNA is a cloud service rather than an endpoint application. It does not require the use or installation of an agent.

Organizations looking to [implement a Zero Trust philosophy](https://www.cloudflare.com/the-net/roadmap-zerotrust/) should consider what kind of ZTNA solution best [fits their needs](https://www.cloudflare.com/the-net/business-case-zero-trust/). For example, if an organization is concerned about a growing mix of managed and unmanaged devices, agent-based ZTNA may be an effective option. Alternatively, if an organization is primarily focused on locking down certain web-based apps, then the service-based model can be rolled out swiftly.

Another consideration is that service-based ZTNA may integrate easily with cloud applications but not as easily with on-premise infrastructure. If all network traffic has to go from on-premise endpoint devices to the cloud, then back to on-premise infrastructure, performance and reliability could be impacted drastically.

## What are other important ZTNA solution considerations?

**Vendor specialization:** Because [identity and access management (IAM)](https://www.cloudflare.com/learning/access-management/what-is-identity-and-access-management/), network services, and [network security](https://www.cloudflare.com/the-net/future-of-networking/) traditionally have all been separate, most ZTNA vendors typically specialize in one of these areas. Organizations should either look for a vendor with an area of specialization that fits their needs, or one that combines all three areas into one cohesive [network security solution](https://www.cloudflare.com/network-security/).

**Level of implementation:** Some organizations may have already invested in adjacent technology to support a Zero Trust strategy (e.g. IdP or endpoint protection providers), while some may need to build their entire ZTNA architecture from scratch. ZTNA vendors may offer point solutions to help organizations round out their ZTNA deployments, create entire ZTNA architectures, or both.

**Support for legacy applications:** Many organizations still have on-premise legacy applications that are critical for their business. Because it runs on the Internet, ZTNA supports cloud applications easily but may need additional configuration to support legacy applications.

**IdP integration:** Many organizations have an IdP already in place. Some ZTNA vendors work only with certain IdPs, forcing their customers to migrate their identity database to use their service. Others are IdP-agnostic — they can integrate with any IdP.

## How does ZTNA differ from Zero Trust Application Access (ZTAA)?

Zero Trust Application Access (ZTAA), also called Zero Trust [application security](https://www.cloudflare.com/application-services/solutions/), applies the same principles as ZTNA to application access rather than network access. ZTAA solutions verify user access to applications by integrating with IdP and SSO providers, encrypting connections, considering each access request for an application individually, and blocking or allowing on a request-by-request basis. ZTAA can be offered agentless via the browser, or using an endpoint agent.

To learn more, see [Zero Trust Security](https://www.cloudflare.com/learning/security/glossary/what-is-zero-trust/).

## How to get started with ZTNA

Cloudflare offers a ZTNA solution built on the Cloudflare global edge network for fast performance. [See the ZTNA solution page](https://www.cloudflare.com/sase/products/access/).

For further background information on the philosophy of Zero Trust, see our [article on Zero Trust security](https://www.cloudflare.com/learning/security/glossary/what-is-zero-trust/).

## FAQs

#### What is the difference between ZTNA and software-defined perimeter (SDP)?

Both ZTNA and SDP create a virtual barrier around internal resources, and SDP can be part of a Zero Trust model. However, SDP and ZTNA are implemented at different layers: SDP operates at the network layer, while ZTNA usually operates at the application layer. ZTNA is also more holistic than SDP: in addition to hiding unnecessary resources from users, ZTNA includes continual device security posture checks and analyzes other contextual factors for allowing access.

#### How does ZTNA support identity-based security controls?

ZTNA solutions integrate with external identity providers to verify user credentials and contextual attributes before granting application access. This identity-centric approach enables fine-grained access control based on the principle of least privilege.

#### Can ZTNA replace traditional network microsegmentation?

In a Zero Trust framework, ZTNA complements microsegmentation by focusing on application-level access while microsegmentation addresses network-level isolation. Together they make lateral movement considerably more difficult for external attackers and malicious insiders. The result is that threats are less likely to cause extensive damage.

#### What role does ZTNA play in a SASE (secure access service edge) framework?

ZTNA is a core component of a [SASE](https://www.cloudflare.com/learning/access-management/what-is-sase/) framework, providing secure application access within the broader cloud-delivered security model. It works alongside other SASE capabilities like CASB, SWG, [SD-WAN](https://www.cloudflare.com/learning/network-layer/what-is-an-sd-wan/), and NGFW to deliver comprehensive protection for modern distributed workforces.