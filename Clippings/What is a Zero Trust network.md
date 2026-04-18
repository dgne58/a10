---
title: "What is a Zero Trust network?"
source: "https://www.cloudflare.com/learning/security/glossary/what-is-zero-trust/"
author:
published:
created: 2026-04-15
description: "Zero Trust is a security model based on maintaining strict access controls and not trusting anyone by default. Learn more about Zero Trust."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

## Zero Trust security | What is a Zero Trust network?

Zero Trust is a security model based on the principle of maintaining strict access controls and not trusting anyone by default, even those already inside the network perimeter.

#### Learning Objectives

After reading this article you will be able to:

- Define Zero Trust security
- Outline the technologies and principles behind Zero Trust
- Learn how to implement a Zero Trust security architecture

Copy article link

## Article Summary:

- Zero Trust is a security model where the core architecture assumes no entity, inside or outside the network, is trustworthy by default and requires strict verification.
- The fundamental Zero Trust principles include least-privilege access, continuous validation, and microsegmentation to minimize the attack surface and prevent lateral movement.
- SASE integration incorporates the Zero Trust security model as a core component, consolidating security and networking services to protect users working remotely and with cloud resources.

## What is Zero Trust security?

Zero Trust security is an IT security model that requires strict identity verification for every person and device trying to access resources on a private network, regardless of whether they are sitting within or outside of the network perimeter. [ZTNA](https://www.cloudflare.com/learning/access-management/what-is-ztna/) is the main technology associated with Zero Trust architecture; but Zero Trust is a [holistic approach to network security](https://www.cloudflare.com/the-net/future-of-networking/) that incorporates several different principles and technologies.

More simply put: traditional IT network security trusts anyone and anything inside the network. A Zero Trust architecture trusts no one and nothing.

Traditional IT network security is based on the [castle-and-moat](https://www.cloudflare.com/learning/access-management/castle-and-moat-network-security/) concept. In castle-and-moat security, it is hard to obtain access from outside the network, but everyone inside the network is trusted by default. The problem with this approach is that once an attacker gains access to the network, they have free rein over everything inside.

![Castle-and-Moat security model, users within the VPN are trusted](https://cf-assets.www.cloudflare.com/slt3lc6tev37/5Q5gi9cihPVrNEVvlnA2TV/45fba984653ae2d54e30652b466da784/castle-and-moat_security_model-resized.png)

This vulnerability in castle-and-moat security systems is exacerbated by the fact that companies no longer have their data in just one place. Today, information is often spread across [cloud](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/) vendors, which makes it more difficult to have a single security control for an entire network.

Zero Trust security means that no one is trusted by default from inside or outside the network, and verification is required from everyone trying to gain access to resources on the network. This added layer of security has been shown to prevent [data breaches](https://www.cloudflare.com/learning/security/what-is-a-data-breach/). [Studies have shown](https://www.ibm.com/downloads/cas/QMXVZX6R) that the average cost of a single data breach is over $3 million. Considering that figure, it should come as no surprise that many organizations are now eager to adopt a Zero Trust security policy.

Article

Elevating organizational trust with Zero Trust

Guide

The Zero Trust guide to securing aplication access

## What are the main principles behind Zero Trust?

#### Continuous monitoring and validation

The philosophy behind a Zero Trust network assumes that there are attackers both within and outside of the network, so no users or machines should be automatically trusted. Zero Trust verifies user identity and privileges as well as device identity and security. Logins and connections time out periodically once established, forcing users and devices to be continuously re-verified.

#### Least privilege

Another principle of Zero Trust security is [least-privilege access](https://www.cloudflare.com/learning/access-management/principle-of-least-privilege/). This means giving users only as much access as they need, like an army general giving soldiers information on a need-to-know basis. This minimizes each user’s exposure to sensitive parts of the network.

Implementing least privilege involves careful managing of user permissions. [VPNs](https://www.cloudflare.com/learning/access-management/what-is-a-vpn/) are not well-suited for least-privilege approaches to authorization, as logging in to a VPN gives a user access to the whole connected network.

#### Device access control

In addition to [controls on user access](https://www.cloudflare.com/learning/access-management/what-is-access-control/), Zero Trust also requires strict controls on device access. Zero Trust systems need to monitor how many different devices are trying to access their network, ensure that every device is authorized, and assess all devices to make sure they have not been compromised. This further minimizes the [attack surface](https://www.cloudflare.com/learning/security/what-is-an-attack-surface/) of the network.

#### Microsegmentation

Zero Trust networks also utilize [microsegmentation](https://www.cloudflare.com/learning/access-management/what-is-microsegmentation/). Microsegmentation is the practice of breaking up security perimeters into small zones to maintain separate access for separate parts of the network. For example, a network with files living in a single data center that utilizes microsegmentation may contain dozens of separate, secure zones. A person or program with access to one of those zones will not be able to access any of the other zones without separate authorization.

#### Preventing lateral movement

In network security, "lateral movement" is when an attacker moves within a network after gaining access to that network. [Lateral movement](https://www.cloudflare.com/learning/security/glossary/what-is-lateral-movement/) can be difficult to detect even if the attacker's entry point is discovered, because the attacker will have gone on to compromise other parts of the network.

Zero Trust is designed to contain attackers so that they cannot move laterally. Because Zero Trust access is segmented and has to be re-established periodically, an attacker cannot move across to other microsegments within the network. Once the attacker's presence is detected, the compromised device or user account can be quarantined, cut off from further access. (In a castle-and-moat model, if lateral movement is possible for the attacker, quarantining the original compromised device or user has little to no effect, since the attacker will already have reached other parts of the network.)

#### Multi-factor authentication (MFA)

[Multi-factor authentication (MFA)](https://www.cloudflare.com/learning/access-management/what-is-multi-factor-authentication/) is also a core value of Zero Trust security. MFA means requiring more than one piece of evidence to authenticate a user; just entering a password is not enough to gain access. A commonly seen application of MFA is the [2-factor authorization (2FA)](https://www.cloudflare.com/learning/access-management/what-is-two-factor-authentication/) used on online platforms like Facebook and Google. In addition to entering a password, users who enable 2FA for these services must also enter a code sent to another device, such as a mobile phone, thus providing two pieces of evidence that they are who they claim to be.

## What are the benefits of Zero Trust?

Zero Trust as a philosophy is better suited to modern IT environments than more traditional security approaches. With such a wide variety of users and devices accessing internal data, and with data stored both inside and outside the network (in [the cloud](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/)), it is far safer to assume that no user or device is trustworthy, than to assume that preventative security measures have plugged all the holes.

The primary benefit of applying Zero Trust principles is to help reduce an organization's attack surface. Additionally, Zero Trust minimizes the damage when an attack does occur by restricting the breach to one small area via microsegmentation, which also lowers the cost of recovery. Zero Trust reduces the impact of user credential theft and phishing attacks by requiring multiple authentication factors. It helps eliminate threats that [bypass](https://www.cloudflare.com/the-net/bypassing-mfa/) traditional perimeter-oriented protections.

And, by verifying every request, Zero Trust security reduces the risk posed by vulnerable devices, including IoT devices, which are often difficult to secure and update (see [IoT security](https://www.cloudflare.com/learning/security/glossary/iot-security/)).

## What is the history of Zero Trust security?

The term "Zero Trust" was coined by an analyst at Forrester Research Inc. in 2010 when the model for the concept was first presented. A few years later, Google announced that they had implemented Zero Trust security in their network, which led to a growing interest in adoption within the tech community. In 2019, Gartner, a global research and advisory firm, listed Zero Trust security access as a core component of [secure access service edge (SASE)](https://www.cloudflare.com/learning/access-management/what-is-sase/) solutions.

## What is Zero Trust Network Access (ZTNA)?

[Zero Trust Network Access (ZTNA)](https://www.cloudflare.com/the-net/zero-trust-network-access/) is the main technology that enables organizations to [implement Zero Trust security](https://www.cloudflare.com/learning/access-management/how-to-implement-zero-trust/). Similar to a [software-defined perimeter (SDP)](https://www.cloudflare.com/learning/access-management/software-defined-perimeter/), ZTNA conceals most infrastructure and services, setting up one-to-one encrypted connections between devices and the resources they need. Learn more about [how ZTNA works](https://www.cloudflare.com/learning/access-management/what-is-ztna/).

## What are some Zero Trust use cases?

Any organization that relies on a network and stores digital data will probably consider using a Zero Trust architecture. But some of the most common use cases for Zero Trust include:

**Replacing or augmenting a VPN:** Many organizations rely on VPNs to protect their data, but as described above, VPNs are often [not ideal](https://www.cloudflare.com/zero-trust/solutions/vpn-replacement/) for defending against today's risks.

**Securely supporting remote work:** While VPNs create bottlenecks and can slow productivity for [remote workers](https://www.cloudflare.com/learning/access-management/remote-workforce-security/), Zero Trust can extend [secure access control](https://www.cloudflare.com/learning/access-management/what-is-remote-access-security/) to connections from anywhere.

**Access control for cloud and multi-cloud:** A Zero Trust network verifies any request, no matter its source or destination. It can also help reduce the use of unauthorized cloud-based services (a situation called " [shadow IT](https://www.cloudflare.com/learning/access-management/what-is-shadow-it/) ") by controlling or blocking the use of unsanctioned apps.

**Onboarding third parties and contractors:** Zero Trust can quickly extend restricted, least-privilege access to [external parties](https://www.cloudflare.com/products/zero-trust/third-party-access/), who typically use computers that are not managed by internal IT teams.

**Rapidly onboarding new employees:** Zero Trust networks can also facilitate quickly onboarding new internal users, making them a good fit for fast-growing organizations. In contrast, a VPN may need to add more capacity to accommodate large numbers of new users.

## What are the main Zero Trust best practices?

- **Monitor network traffic and connected devices:** [Visibility](https://www.cloudflare.com/network-services/solutions/network-monitoring-tools/) is crucial in order for users and machines to be verified and authenticated.
- **Keep devices updated:** Vulnerabilities need to be patched as quickly as possible. Zero Trust networks should be able to restrict access to vulnerable devices (another reason why monitoring and validation are key).
- **Apply the principle of least privilege for everyone in the organization:** From executives to IT teams, everyone should have the least amount of access they need. This minimizes the damage if an end user account becomes compromised.
- **Partition the network:** Breaking up the network into smaller chunks helps ensure breaches are contained early, before they can spread. Microsegmentation is an effective way to do this.
- **Act as if the [network perimeter](https://www.cloudflare.com/learning/access-management/what-is-the-network-perimeter/) did not exist:** Unless a network is completely air-gapped (a rarity), the points where it touches the Internet or the cloud are probably too numerous to eliminate.
- **Use security keys for MFA:** Hardware-based [security tokens](https://www.cloudflare.com/learning/access-management/token-based-authentication/) are [demonstrably more secure](https://blog.cloudflare.com/2022-07-sms-phishing-attacks/) than soft tokens like one-time passcodes (OTPs) sent via SMS or email.
- **Incorporate threat intelligence:** Since attackers are constantly updating and refining their tactics, subscribing to the latest [threat intelligence](https://www.cloudflare.com/learning/security/glossary/what-is-threat-intelligence/) data feeds is critical for identifying threats before they spread.
- **Avoid motivating end users to circumvent security measures:** Just as overly strict password requirements incentivize users to recycle the same passwords over and over, forcing users to re-authenticate once an hour via multiple identity factors may be too much, ironically decreasing security. Always keep the end user's needs in mind.

## How to implement Zero Trust security

Zero Trust may sound complex, but [adopting](https://www.cloudflare.com/the-net/sase-network-transformation/) this security model can be relatively simple with the right technology partner. For instance, [Cloudflare One](https://www.cloudflare.com/zero-trust/) is a SASE platform that combines [networking services](https://www.cloudflare.com/network-security/) with a built-in Zero Trust approach to user and device access. With Cloudflare One, customers automatically implement [Zero Trust protection](https://www.cloudflare.com/sase/use-cases/) around all their assets and data.

## FAQs

#### What is the core philosophy behind Zero Trust security?

Zero Trust is built on the principle of "never trust, always verify." Unlike traditional security that trusts anyone inside a network, Zero Trust assumes that threats exist both inside and outside the network perimeter. Consequently, every person and device must undergo strict identity verification before gaining access to resources, regardless of their location or connectivity status.

#### How does Zero Trust differ from the "castle-and-moat" security model?

In a "castle-and-moat" model, an organization focuses on defending the network perimeter. Once someone is inside the "castle" (the network or VPN), they are trusted by default and can often move freely. Zero Trust removes this default trust, requiring continuous validation for every request and ensuring that gaining entry to the network does not grant automatic access to everything within it.

#### What is least-privilege access?

Least-privilege access involves giving users only the minimum level of access necessary to perform their specific jobs. By restricting permissions to a need-to-know basis, an organization can minimize the amount of sensitive data exposed if a single user account is compromised.

#### How does microsegmentation help contain security breaches?

Microsegmentation is the practice of dividing a network into small, isolated security zones. Because each zone requires separate authorization, an attacker who manages to break into one area is prevented from moving laterally to others. This quarantines the threat and limits the potential damage of a breach.

#### Why is multi-factor authentication (MFA) essential for Zero Trust?

MFA requires users to provide at least two different pieces of evidence to prove their identity, such as a password plus a code sent to a mobile device or a physical security key. This adds a critical layer of protection, as knowing a user's password alone is no longer enough for an attacker to gain access.

#### Can Zero Trust improve the experience for remote workers compared to a VPN?

While VPNs often create performance bottlenecks and grant broad network access that can be risky, Zero Trust provides secure, direct connections to specific applications. This approach supports remote work from any location without compromising security or slowing down productivity.

#### How does Zero Trust address risks associated with IoT devices?

Internet of Things (IoT) devices are notoriously difficult to secure and patch. Zero Trust mitigates this risk by constantly monitoring and verifying every device on the network. If an IoT device is found to be vulnerable or compromised, the Zero Trust model can automatically restrict its access to prevent it from being used as an entry point for an attack.

#### What is Zero Trust Network Access (ZTNA)?

ZTNA is the primary technology used to implement a Zero Trust architecture. It functions by hiding internal infrastructure and establishing secure, one-to-one encrypted connections between a user's device and the specific resource they are authorized to use, rather than connecting them to the entire private network.