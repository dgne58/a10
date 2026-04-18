---
title: "What is a DDoS botnet?"
source: "https://www.cloudflare.com/learning/ddos/what-is-a-ddos-botnet/"
author:
published:
created: 2026-04-15
description: "A botnet refers to a group of devices which have been infected by malware and have come under the control of a malicious actor. Learn more about botnets."
tags:
  - "clippings"
---
Preview Mode

[Documentation](https://staging.mrk.cfdata.org/mrk/redwood-blade-repository/)

Botnet attacks are responsible for the largest DDoS attacks on record. Learn how devices become infected with botnet malware, how bots are remotely controlled, and how to protect a network from a botnet infestation.

#### Learning Objectives

After reading this article you will be able to:

- Define a DDoS botnet
- Explain why botnets are created
- Understand how botnets are remotely controlled by attackers
- Reason about strategies for disabling a botnet and preventing infection

Related Content

---

#### Want to keep learning?

Subscribe to theNET, Cloudflare's monthly recap of the Internet's most popular insights!

Copy article link

## What is a Botnet?

<iframe src="https://iframe.videodelivery.net/70c576e543a0da34b3aa75c7f27732b0?poster=https://videodelivery.net/70c576e543a0da34b3aa75c7f27732b0/thumbnails/thumbnail.jpg?time=21s&amp;height=270" height="412" width="740" allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;" allowfullscreen="true"></iframe>

A botnet refers to a group of computers which have been infected by malware and have come under the control of a malicious actor. The term botnet is a portmanteau from the words robot and network and each infected device is called a [bot](https://www.cloudflare.com/learning/bots/what-is-a-bot/). Botnets can be designed to accomplish illegal or malicious tasks including sending [spam](https://en.wikipedia.org/wiki/Email_spam), stealing data, [ransomware](https://www.avg.com/en/signal/what-is-ransomware), [fraudulently clicking on ads](https://www.cloudflare.com/learning/bots/what-is-click-fraud/) or [distributed denial-of-service (DDoS) attacks](https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/).

While some [malware](https://www.cloudflare.com/learning/ddos/glossary/malware/), such as ransomware, will have a direct impact on the owner of the device, DDoS botnet malware can have different levels of visibility; some malware is designed to take total control of a device, while other malware runs silently as a background process while waiting silently for instructions from the attacker or “bot herder.”

Self-propagating botnets recruit additional bots through a variety of different channels. Pathways for infection include the exploitation of website vulnerabilities, Trojan horse malware, and cracking weak authentication to gain remote access. Once access has been obtained, all of these methods for infection result in the installation of malware on the target device, allowing remote control by the operator of the botnet. Once a device is infected, it may attempt to self-propagate the botnet malware by recruiting other hardware devices in the surrounding network.

While it's infeasible to pinpoint the exact numbers of bots in a particular botnet, estimations for total number of bots in a sophisticated botnet have ranged in size from a few thousand to greater than a million.

![DDoS Botnet attack animation](https://www.cloudflare.com/img/learning/ddos/what-is-a-ddos-botnet/ddos-botnet-attack-cropped.png)

#### Examples of large DDoS botnets

- [Mirai botnet](https://www.cloudflare.com/learning/ddos/glossary/mirai-botnet/)
- [Meris botnet](https://blog.cloudflare.com/meris-botnet/)
- [Aisuru-Kimwolf botnet](https://www.cloudflare.com/learning/ddos/glossary/aisuru-kimwolf-botnet/)

## Why are botnets created?

Reasons for using a botnet ranges from activism to state-sponsored disruption, with many attacks being carried out simply for profit. Hiring botnet services online is relatively inexpensive, especially in relationship to the amount of damage they can cause. The barrier to creating a botnet is also low enough to make it a lucrative business for some software developers, especially in geographic locations where regulation and law enforcement are limited. This combination has led to a proliferation of online services offering attack-for-hire.

## How is a botnet controlled?

A core characteristic of a botnet is the ability to receive updated instructions from the bot herder. The ability to communicate with each bot in the network allows the attacker to alternate attack vectors, change the targeted [IP address](https://www.cloudflare.com/learning/dns/glossary/what-is-my-ip-address/), terminate an attack, and other customized actions. Botnet designs vary, but the control structures can be broken down into two general categories:

#### The client/server botnet model

The [client/server model](https://www.cloudflare.com/learning/serverless/glossary/client-side-vs-server-side/) mimics the traditional remote workstation workflow where each individual machine connects to a centralized server (or a small number of centralized servers) in order to access information. In this model each bot will connect to a command-and-control center (CnC) resource like a web domain or an IRC channel in order to receive instructions. By using these centralized repositories to serve up new commands for the botnet, an attacker simply needs to modify the source material that each botnet consumes from a command center in order to update instructions to the infected machines. The centralized server in control of the botnet may be a device owned and operated by the attacker, or it may be an infected device.

A number of popular centralized botnet topologies have been observed, including:

Star Network Topology

![Star network topology animation](https://www.cloudflare.com/img/learning/ddos/what-is-a-ddos-botnet/ddos-botnet-star-network-topology.png)

Multi Server Network Topology

![Multi server network topology animation](https://www.cloudflare.com/img/learning/ddos/what-is-a-ddos-botnet/ddos-botnet-multi-server-network-topology.png)

Hierarchical Network Topology

![Hierarchical network topology animation](https://www.cloudflare.com/img/learning/ddos/what-is-a-ddos-botnet/ddos-botnet-hierarchical-network-topology.png)

In any of these client/server models, each bot will connect to a command center resource like a web domain or an IRC channel in order to receive instructions. By using these centralized repositories to serve up new commands for the botnet, an attacker simply needs to modify the source material that each botnet consumes from a command center in order to update instructions to the infected machines.

Hand-in-hand with the simplicity of updating instructions to the botnet from a limited number of centralized sources is the vulnerability of those machines; in order to remove a botnet with a centralized server, only the server needs to be disrupted. As a result of this vulnerability, the creators of botnet malware have evolved and moved towards a new model that is less susceptible to disruption via a single or a few points of failure.

#### The peer-to-peer botnet model

To circumvent the vulnerabilities of the client/server model, botnets have more recently been designed using components of decentralized peer-to-peer filesharing. Embedding the control structure inside the botnet eliminates the single point-of-failure present in a botnet with a centralized server, making mitigation efforts more difficult. P2P bots can be both clients and command centers, working hand-in-hand with their neighboring nodes to propagate data.

Peer to peer botnets maintain a list of trusted computers with which they can give and receive communications and update their malware. By limiting the number of other machines the bot connects to, each bot is only exposed to adjacent devices, making it harder to track and more difficult to mitigate. Lacking a centralized command server makes a peer-to-peer botnet more vulnerable to control by someone other than the botnet’s creator. To protect against loss of control, decentralized botnets are typically encrypted so that access is limited.

![Peer-to-peer network topology animation](https://www.cloudflare.com/img/learning/ddos/what-is-a-ddos-botnet/ddos-botnet-peer-to-peer.png)

## How do IoT devices become a botnet?

No one does their Internet banking through the wireless CCTV camera they put in the backyard to watch the bird feeder, but that doesn't mean the device is incapable of making the necessary network requests. The power of [IoT](https://www.cloudflare.com/learning/ddos/glossary/internet-of-things-iot/) devices coupled with weak or poorly configured security creates an opening for botnet malware to recruit new bots into the collective. An uptick in IoT devices has resulted in a new landscape for DDoS attacks, as many devices are poorly configured and vulnerable.

If an IoT device’s vulnerability is hardcoded into firmware, updates are more difficult. To mitigate risk, IoT devices with outdated firmware should be updated as default credentials commonly remain unchanged from the initial installation of the device. Many discount manufacturers of hardware are not incentivized to make their devices more secure, making the vulnerability posed from botnet malware to IoT devices remain an unsolved security risk.

## How is an existing botnet disabled?

#### Disable a botnet’s control centers:

Botnets designed using a command-and-control schema can be more easily disabled once the control centers can be identified. Cutting off the head at the points of failure can take the whole botnet offline. As a result, system administrators and law enforcement officials focus on closing down the control centers of these botnets. This process is more difficult if the command center operates in a country where law enforcement is less capable or willing to intervene.

#### Eliminate infection on individual devices:

For individual computers, strategies to regain control over the machine include running antivirus software, reinstalling software from a safe backup, or starting over from a clean machine after reformatting the system. For IoT devices, strategies may include flashing the firmware, running a factory reset or otherwise formatting the device. If these option are infeasible, other strategies may be available from the device’s manufacturer or a system administrator.

## How can you protect devices from becoming part of a botnet?

#### Create secure passwords:

For many vulnerable devices, reducing exposure to botnet vulnerability can be as simple as changing the administrative credentials to something other than the default username and password. Creating a secure password makes [brute force cracking](https://www.cloudflare.com/learning/security/threats/brute-force-attack/) difficult, creating a very secure password makes brute force cracking virtually impossible. For example, a device infected with the [Mirai](https://www.cloudflare.com/learning/ddos/glossary/mirai-botnet/) malware will scan IP addresses looking for responding devices. Once a device responds to a ping request, the bot will attempt to login to that found device with a preset list of default credentials. If the default password has been changed and a secure password has been implemented, the bot will give up and move on, looking for more vulnerable devices.

#### Allow only trusted execution of third-party code:

If you adopt the mobile phone model of software execution, only allowed applications may run, granting more control to terminate software deemed as malicious, botnets included. Only an exploitation of the supervisor software (i.e. kernel) may result in exploitation of the device. This hinges on having a secure kernel in the first place, which most IoT devices do not have, and is more applicable to machines that are running third party software.

#### Periodic system wipe/restores:

Restoring to a known good state after a set time will remove any gunk a system has collected, botnet software included. This strategy, when used as a preventative measure, ensures even silently running malware gets thrown out with trash.

#### Implement good ingress and egress filtering practices:

Other more advanced strategies include filtering practices at network routers and [firewalls](https://www.cloudflare.com/learning/security/what-is-a-firewall/). A principle of secure network design is layering: you have the least restriction around publicly accessible resources, while continually beefing up security for things you deem sensitive. Additionally, anything that crosses these boundaries has to be scrutinized: network traffic, usb drives, etc. Quality filtering practices increase the likelihood that DDoS malware and their methods of propagation and communication will be caught before entering or leaving the network.

If you are currently under attack, there are steps you can take to get out from under the pressure. If you are on Cloudflare already, you can follow [these steps](https://support.cloudflare.com/hc/en-us/articles/200170196-I-am-under-DDoS-attack-what-do-I-do-) to mitigate your attack. The DDoS protection that we implement at Cloudflare is multifaceted in order to mitigate the many possible attack vectors. Learn more about Cloudflare's [DDoS Protection](https://www.cloudflare.com/ddos/).