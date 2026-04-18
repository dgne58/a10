---
title: "What is CASB? | Cloud access security brokers"
source: "https://www.cloudflare.com/learning/access-management/what-is-a-casb/"
author:
published:
created: 2026-04-15
description: "A cloud access security broker, or CASB, offers security services to protect company cloud data from cyber attacks and data breaches. Learn about CASB security."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

A cloud access security broker (CASB) offers a number of services to protect companies that use cloud computing from data breaches and cyber attacks.

#### Learning Objectives

After reading this article you will be able to:

Copy article link

## Article Summary:

- A cloud access service broker (CASB) provides key visibility, data security, and threat protection for cloud-hosted applications and services.
- CASB deployment occurs via proxy or API methods, integrating with an identity provider to enforce granular user access controls and authentication policies.
- SASE integration incorporates the CASB as a crucial security element, consolidating data protection and policy enforcement across a unified cloud platform.

## What is a cloud access security broker (CASB)?

![casb](https://cf-assets.www.cloudflare.com/slt3lc6tev37/4wMGDsq0zsHHKTwSTpVRCY/28099e331608efda78c2d921fe720b8a/casb-cloud-discovery-visibility.png "casb")

A cloud access security broker, or CASB, is a type of [security solution](https://www.cloudflare.com/application-services/solutions/) that helps protect [cloud-hosted](https://www.cloudflare.com/learning/cloud/what-is-the-cloud/) services. CASBs help keep corporate [software-as-a-service (SaaS)](https://www.cloudflare.com/learning/cloud/what-is-saas/) applications, along with [infrastructure-as-a-service (IaaS)](https://www.cloudflare.com/learning/cloud/what-is-iaas/) and [platform-as-a-service (PaaS)](https://www.cloudflare.com/learning/serverless/glossary/platform-as-a-service-paas/) services, safe from cyber attacks and data leaks. Typically, CASB vendors offer their services as cloud-hosted software, although some CASBs also offer on-premise software or on-premise hardware appliances.

A number of different security technologies fall under the CASB umbrella, and a CASB solution will typically offer these technologies together in one bundled package. These technologies include [shadow IT](https://www.cloudflare.com/learning/access-management/what-is-shadow-it/) discovery, [access control](https://www.cloudflare.com/learning/access-management/what-is-access-control/), and [data loss prevention (DLP)](https://www.cloudflare.com/learning/access-management/what-is-dlp/), among several others.

Think of a CASB as being like a physical security firm that offers a number of services (surveillance, foot patrol, identity verification, etc.) to keep a facility safe, rather than a single security guard. Similarly, CASBs offer a variety of services rather than one, simplifying the process of cloud data protection.

![casb features](https://cf-assets.www.cloudflare.com/slt3lc6tev37/5bePPHiHIemCbdl9a3XGiY/efdbcecd38f33b21e589fa4dc12fd323/cloud-access-security-brokers-casb.png "four cloud access security broker casb pillars")

## What are the 4 pillars of CASB security?

[Gartner](https://www.gartner.com/en/information-technology/glossary/cloud-access-security-brokers-casbs), an influential industry analyst firm, defines four "pillars" for cloud access security brokers:

1. **Visibility:** CASB solutions help discover "shadow IT": systems and processes, especially cloud services, that are not officially documented and that may introduce unknown security risks.
2. **Data security:** CASBs prevent confidential data from leaving company-controlled systems, and help [protect the integrity of that data](https://www.cloudflare.com/the-net/data-protection-ai/). This [capability](https://www.cloudflare.com/the-net/ai-secure/) is especially relevant with the proliferation of AI tools into which employees may attempt to upload protected data. Important technologies for this area include [access control](https://www.cloudflare.com/learning/access-management/what-is-access-control/) and [data loss prevention (DLP)](https://www.cloudflare.com/learning/access-management/what-is-dlp/).
3. **Threat protection:** CASBs block external threats and attacks, in addition to stopping data leaks. Anti-malware detection, sandboxing, [packet](https://www.cloudflare.com/learning/network-layer/what-is-a-packet/) inspection, [URL filtering](https://www.cloudflare.com/learning/access-management/what-is-url-filtering/), and [browser isolation](https://www.cloudflare.com/learning/access-management/what-is-browser-isolation/) can all help block cyber attacks.
4. **Compliance:** Because the cloud is so spread out and is not under a company's control, it can be difficult for companies operating in the cloud to meet strict regulatory requirements like SOC 2, HIPAA, or the [GDPR](https://www.cloudflare.com/learning/privacy/what-is-the-gdpr/). Within certain industries and regions, companies that do not comply are at risk for penalties and fines. By implementing strong security controls, CASBs help companies that store data and run business processes in the cloud [achieve regulatory compliance](https://www.cloudflare.com/the-net/pursuing-privacy-first-security/data-localization/).

## What security capabilities do CASBs offer?

Most CASB solutions will offer some or all of the following security technologies:

- [Identity verification](https://www.cloudflare.com/learning/access-management/what-is-identity-and-access-management/): Ensures a user is who they claim to be by checking several identity factors, such as a password or possession of a physical [token](https://www.cloudflare.com/learning/access-management/token-based-authentication/)
- Access control: Controls what users can see and do within company-controlled applications
- Shadow IT discovery: Identifies the systems and services internal employees are using for business purposes without proper authorization
- Data loss prevention (DLP): Stops data leaks and prevents data from leaving company-owned platforms
- URL filtering: Blocks websites used by attackers for [phishing](https://www.cloudflare.com/learning/access-management/phishing-attack/) or [malware](https://www.cloudflare.com/learning/ddos/glossary/malware/) attacks
- Packet inspection: Inspects data entering or exiting the network for malicious activity
- Sandboxing: Runs programs and code in an isolated environment to determine whether or not it is malicious
- Browser isolation: Runs users' browsers on a remote server instead of on the users' devices, protecting the devices from potentially malicious code that can run in the browser
- Anti-malware detection: Identifies malicious software

This list is not exhaustive, as CASBs can offer a number of other security products in addition to those listed above. Some of these technologies are included in other types of security products as well. For instance, many [firewalls](https://www.cloudflare.com/learning/security/what-is-a-firewall/) offer packet inspection, and many [endpoint security](https://www.cloudflare.com/learning/security/glossary/endpoint-security/) products offer anti-malware. CASBs, however, package these technologies specifically for cloud computing.

To provide a full complement of CASB services, many major CASBs have at some point acquired a product or company that they bundle with their other previously existing products. They may also partner with external companies to offer additional services.

#### CASBs and DLP

While DLP has grown in importance as data regulatory frameworks (like the [GDPR](https://www.cloudflare.com/learning/privacy/what-is-the-gdpr/)) put pressure on organizations to maintain privacy and avoid data leaks, traditional DLP products come with weaknesses when it comes to securing the modern data landscape. Standalone DLP services are difficult to implement as an additional layer for cloud services. Bundling DLP in CASB solutions helps solve these challenges, enabling organizations to protect their data and maintain compliance.

## What are the benefits of CASBs?

In cloud computing, data is stored remotely and accessed over the Internet. As a result, companies using the cloud have limited control over where data is stored and how users access it. Users can access cloud data and applications on any Internet-connected device and from any network, not just the internal company-managed network. For instance, a user could log in to a company-managed SaaS app from an unsecured network on their personal device, which typically would not be possible for applications that run on on-premise computers and servers (unless [remote desktop](https://www.cloudflare.com/learning/access-management/what-is-the-remote-desktop-protocol/) is used).

Using the cloud also makes it harder to ensure that data stays private and secure, just as it is harder to prevent strangers from eavesdropping when conversing in a public place instead of in a private room.

To fully protect data in the cloud, organizations typically use security services that are cloud-based as well. Sometimes, they obtain these services from different vendors: using one platform for DLP, one for identity, one for anti-malware, and so on. But this approach to cloud security also creates challenges: several contracts have to be negotiated separately, security policies have to be configured numerous times, implementing and managing multiple platforms creates complexity for IT, etc.

CASBs are one [network security solution](https://www.cloudflare.com/network-security/) to these challenges. Purchasing these security measures from one cloud security broker instead of several different vendors means:

1. All the technologies involved work well together.
2. Simplified management of cloud security tools; IT teams can work with one vendor, instead of a half-dozen vendors. Additionally, many CASBs enable their customers to manage all cloud security services from a single dashboard.

## What are the challenges of using a CASB?

**Scalability:** CASBs have to manage a lot of data and multiple cloud platforms and applications. Companies should ensure their CASB vendor is able to scale up with them as they grow.

**Mitigation:** Not all CASBs offer the ability to stop security threats once they are identified. Depending on the situation, a CASB without mitigation capabilities may be of limited use to a company.

**Integration:** Companies must ensure their CASB will integrate with all their systems and infrastructure. Without complete integration, the CASB will not have full visibility into unauthorized IT and potential security threats.

**Data privacy:** Does the CASB vendor keep data private, or are they just one more external party touching sensitive data? If the CASB moves their customers' data to the cloud, how secure and private is it? These are especially important questions for organizations that operate under strict [data privacy](https://www.cloudflare.com/learning/privacy/what-is-data-privacy/) regulations.

## Who needs a CASB?

Most enterprises that rely partially or wholly on the cloud can benefit from working with a CASB vendor. Businesses that are struggling to [contain the growth of shadow IT](https://www.cloudflare.com/the-net/shadow-it/) — a major concern for many businesses today — can especially benefit from CASB services.

## How do CASBs integrate with SASE?

Secure access service edge, or [SASE](https://www.cloudflare.com/learning/access-management/what-is-sase/), is a cloud-based [network infrastructure](https://www.cloudflare.com/the-net/network-infrastructure/) model that consolidates networking and security services into a single service provider, making it simpler for companies to secure and manage network access across all connected devices. In the same way that CASBs bundle a variety of security services, SASE bundles [SD-WANs](https://www.cloudflare.com/learning/network-layer/what-is-a-wan/) (among other network capabilities) with CASBs, [secure web gateways (SWG)](https://www.cloudflare.com/learning/access-management/what-is-a-secure-web-gateway/), [Zero Trust Network Access (ZTNA)](https://www.cloudflare.com/learning/security/glossary/what-is-zero-trust/), [firewall-as-a-service (FWaaS)](https://www.cloudflare.com/learning/cloud/what-is-a-cloud-firewall/), and other network security functions. SASE solutions are built on top of a single global network.

## Does Cloudflare have a CASB offering?

Cloudflare One integrates CASB, DLP, Zero Trust, SWG, and browser isolation capabilities in a single platform. These [services](https://www.cloudflare.com/sase/use-cases/) are delivered from the Cloudflare network, as close to end users as possible, and can sit in front of on-premise, cloud, and hybrid networks. [Learn more about Cloudflare One](https://www.cloudflare.com/sase/).

## FAQs

#### What is a CASB?

A cloud access security broker (CASB) is a security tool that sits between users and cloud applications to monitor activity and enforce security policies. CASBs provide visibility, compliance enforcement, [data security](https://www.cloudflare.com/learning/cloud/what-is-dspm/), and threat protection for cloud services.

#### What are the four main functions of a CASB?

The four main functions of a CASB are visibility into cloud usage,, data security through access controls, threat protection against malicious activity, and compliance with regulations. These pillars form the core of CASB functionality as defined by Gartner.

#### How do CASBs address shadow IT?

CASBs help detect unauthorized cloud applications (which are known as shadow IT) by monitoring network traffic and providing visibility into all cloud services accessed by users. This visibility allows security teams to detect application usage, evaluate risks, and enforce appropriate policies for each application.

#### What are the different CASB deployment methods?

There are two primary ways to deploy CASB: either as a proxy that intercepts traffic, or via API and a more direct integration with cloud services. Some CASB providers also offer multimode CASBs that combine both proxy and API deployments.

#### How does a CASB integrate with existing security infrastructure?

CASBs typically integrate with identity providers, secure web gateways, and other security tools to create a cohesive security ecosystem. This integration enables consistent policy enforcement and enhances an organization's overall security posture across cloud environments.