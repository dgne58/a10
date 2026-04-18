---
title: "Stream Control Transmission Protocol - Wikipedia"
source: "https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2003-12-16
created: 2026-04-13
description:
tags:
  - "clippings"
---
The **Stream Control Transmission Protocol** (**SCTP**) is a [computer networking](https://en.wikipedia.org/wiki/Computer_networking "Computer networking") [communications protocol](https://en.wikipedia.org/wiki/Communications_protocol "Communications protocol") in the [transport layer](https://en.wikipedia.org/wiki/Transport_layer "Transport layer") of the [Internet protocol suite](https://en.wikipedia.org/wiki/Internet_protocol_suite "Internet protocol suite"). Originally intended for [Signaling System 7](https://en.wikipedia.org/wiki/Signaling_System_7 "Signaling System 7") (SS7) message transport in telecommunication, the protocol provides the message-oriented feature of the [User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol "User Datagram Protocol") (UDP) while ensuring reliable, in-sequence transport of messages with [congestion control](https://en.wikipedia.org/wiki/TCP_congestion_control "TCP congestion control") like the [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") (TCP). Unlike UDP and TCP, the protocol supports [multihoming](https://en.wikipedia.org/wiki/Multihoming "Multihoming") and redundant paths to increase resilience and reliability.

SCTP is standardized by the [Internet Engineering Task Force](https://en.wikipedia.org/wiki/Internet_Engineering_Task_Force "Internet Engineering Task Force") (IETF) in [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [9260](https://www.rfc-editor.org/rfc/rfc9260). The SCTP reference implementation was released as part of [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD") version 7 and has since been widely ported to other platforms.

## Formal oversight

The [IETF](https://en.wikipedia.org/wiki/IETF "IETF") Signaling Transport ([SIGTRAN](https://en.wikipedia.org/wiki/SIGTRAN "SIGTRAN")) working group defined the protocol (number 132 [^3]) in October 2000,[^4] and the IETF Transport Area (TSVWG) working group maintains it. [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [9260](https://www.rfc-editor.org/rfc/rfc9260) defines the protocol. [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3286](https://www.rfc-editor.org/rfc/rfc3286) provides an introduction.

## Message-based multi-streaming

SCTP applications submit data for transmission in messages (groups of bytes) to the SCTP transport layer. SCTP places messages and control information into separate *chunks* (data chunks and control chunks), each identified by a *chunk header*. The protocol can fragment a message into multiple data chunks, but each data chunk contains data from only one user message. SCTP bundles the chunks into SCTP packets. The SCTP packet, which is submitted to the [Internet Protocol](https://en.wikipedia.org/wiki/Internet_Protocol "Internet Protocol"), consists of a packet header, SCTP control chunks (when necessary), followed by SCTP data chunks (when available).

SCTP may be characterized as message-oriented, meaning it transports a sequence of messages (each being a group of bytes), rather than transporting an unbroken stream of bytes as in TCP. As in UDP, in SCTP a sender sends a message in one operation, and that exact message is passed to the receiving application process in one operation. In contrast, TCP is a stream-oriented protocol, transporting [streams of bytes](https://en.wikipedia.org/wiki/Byte_stream "Byte stream") reliably and in order. However TCP does not allow the receiver to know how many times the sender application called on the TCP transport passing it groups of bytes to be sent out. At the sender, TCP simply appends more bytes to a queue of bytes waiting to go out over the network, rather than having to keep a queue of individual separate outbound messages which must be preserved as such.

The term *multi-streaming* refers to the capability of SCTP to transmit several independent streams of chunks in parallel, for example transmitting [web page](https://en.wikipedia.org/wiki/Web_page "Web page") images simultaneously with the web page text. In essence, it involves bundling several connections into a single SCTP association, operating on messages (or chunks) rather than bytes.

TCP preserves byte order in the stream by including a byte sequence number with each [segment](https://en.wikipedia.org/wiki/TCP_segment "TCP segment"). SCTP, on the other hand, assigns a sequence number or a message-id [^1] to each *message* sent in a stream. This allows independent ordering of messages in different streams. However, message ordering is optional in SCTP; a receiving application may choose to process messages in the order of receipt instead of in the order of sending.

## Features

Features of SCTP include:

- Reliable transmission of both ordered and unordered data streams
- Multihoming support in which one or both endpoints of a connection can consist of more than one IP address, enabling transparent fail-over between redundant network paths
- Delivery of chunks within independent streams eliminates unnecessary [head-of-line blocking](https://en.wikipedia.org/wiki/Head-of-line_blocking "Head-of-line blocking"), as opposed to TCP byte-stream delivery.
- Explicit partial reliability
- Path selection and monitoring to select a primary data transmission path and test the connectivity of the transmission path
- Validation and acknowledgment mechanisms protect against [flooding attacks](https://en.wikipedia.org/wiki/SYN_flood "SYN flood") and provide notification of duplicated or missing data chunks.
- Improved error detection suitable for [Ethernet jumbo frames](https://en.wikipedia.org/wiki/Jumbo_frames "Jumbo frames")

The designers of SCTP originally intended it for the transport of telephony (i.e. Signaling System 7) over Internet Protocol, with the goal of duplicating some of the reliability attributes of the SS7 signaling network in IP. This IETF effort is known as [SIGTRAN](https://en.wikipedia.org/wiki/SIGTRAN "SIGTRAN"). In the meantime, other uses have been proposed, for example, the [Diameter](https://en.wikipedia.org/wiki/Diameter_\(protocol\) "Diameter (protocol)") protocol [^5] and [Reliable Server Pooling](https://en.wikipedia.org/wiki/Reliable_Server_Pooling "Reliable Server Pooling") (RSerPool).[^6]

## Motivation and adoption

TCP has provided the primary means to transfer data reliably across the Internet. However, TCP has imposed limitations on several applications. From [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [4960](https://www.rfc-editor.org/rfc/rfc4960):

- TCP provides both reliable data transfer and strict order-of-transmission delivery of data. Some applications need reliable transfer without sequence maintenance, while others would be satisfied with partial ordering of the data. In both of these cases, the head-of-line blocking property of TCP causes unnecessary delay.
- For applications exchanging distinct records or messages, the stream-oriented nature of TCP requires the addition of explicit markers or other encoding to delineate the individual records.
- In order to avoid sending many small IP packets where one single larger packet would have sufficed, the TCP implementation may delay transmitting data while waiting for possibly more data being queued by the application ([Nagle's algorithm](https://en.wikipedia.org/wiki/Nagle%27s_algorithm "Nagle's algorithm")). Although many TCP implementations allow the disabling of Nagle's algorithm, this is not required by the specification. SCTP, on the other hand, allows undelayed transmission to be configured as a default for an association, eliminating any undesired delays, but at the cost of higher transfer overhead.[^7]
- The limited scope of TCP sockets complicates the task of providing highly-available data transfer capability using multihomed hosts.
- TCP is relatively vulnerable to denial-of-service attacks, such as [SYN attacks](https://en.wikipedia.org/wiki/SYN_attack "SYN attack").

Adoption of SCTP has been slowed by lack of awareness, lack of implementations (particularly in Microsoft Windows), lack of application support and lack of network support.[^8]

SCTP has seen adoption in the [mobile telephony](https://en.wikipedia.org/wiki/Mobile_telephony "Mobile telephony") space as the transport protocol for several [core network interfaces](https://en.wikipedia.org/wiki/System_Architecture_Evolution#EPC_protocol_stack "System Architecture Evolution").[^9]

## Multihoming

![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/SCTP-Multihoming.png/500px-SCTP-Multihoming.png)

SCTP multihoming

![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/SCTP-LocalMultihoming-RemoteSinglehoming.png/500px-SCTP-LocalMultihoming-RemoteSinglehoming.png)

Asymmetric multihoming: local multihoming to remote single homing

![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/SCTP-LocalSinglehoming-RemoteMultihoming.png/500px-SCTP-LocalSinglehoming-RemoteMultihoming.png)

Asymmetric multihoming: local single homing to remote multihoming

SCTP provides redundant paths to increase reliability.

Each SCTP end point needs to check reachability of the primary and redundant addresses of the remote end point using a [heartbeat](https://en.wikipedia.org/wiki/Heartbeat_\(computing\) "Heartbeat (computing)"). Each SCTP end point needs to acknowledge the heartbeats it receives from the remote end point.

When SCTP sends a message to a remote address, the source interface will only be decided by the routing table of the host (and not by SCTP).

In asymmetric multihoming, one of the two endpoints does not support multihoming.

In local multihoming and remote single homing, if the remote primary address is not reachable, the SCTP association fails even if an alternate path is possible.

## Packet structure

An SCTP packet consists of two basic sections:

1. The *common header*, which occupies the first 12 bytes and is highlighted in blue.
2. The *data chunks*, which occupy the remaining portion of the packet. The first chunk is highlighted in green, and the last of *N* chunks (Chunk N) is highlighted in red.

<table><tbody><tr><th>Bits</th><th colspan="8" width="25%">0–7</th><th colspan="8" width="25%">8–15</th><th colspan="8" width="25%">16–23</th><th colspan="8" width="25%">24–31</th></tr><tr><th>+0</th><td colspan="16">Source port</td><td colspan="16">Destination port</td></tr><tr><th>32</th><td colspan="32">Verification tag</td></tr><tr><th>64</th><td colspan="32">Checksum</td></tr><tr><th>96</th><td colspan="8">Chunk 1 type</td><td colspan="8">Chunk 1 flags</td><td colspan="16">Chunk 1 length</td></tr><tr><th>128</th><td colspan="32">Chunk 1 data</td></tr><tr><th>…</th><td colspan="32">…</td></tr><tr><th>…</th><td colspan="8">Chunk <i>N</i> type</td><td colspan="8">Chunk <i>N</i> flags</td><td colspan="16">Chunk <i>N</i> length</td></tr><tr><th>…</th><td colspan="32">Chunk <i>N</i> data</td></tr></tbody></table>

Each chunk starts with a one-byte type identifier, with 15 chunk types defined by [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [9260](https://www.rfc-editor.org/rfc/rfc9260), and at least 5 more defined by additional RFCs.[^2] Eight flag bits, a two-byte length field, and the data compose the remainder of the chunk. If the chunk does not form a multiple of 4 bytes (i.e., the length is not a multiple of 4), then it is padded with zeros, which are not included in the chunk length. The two-byte length field limits each chunk to a 65,535-byte length (including the type, flags and length fields).

## Security

Although encryption was not part of the original SCTP design, SCTP was designed with features for improved security, such as 4-way [handshake](https://en.wikipedia.org/wiki/Handshake_\(computing\) "Handshake (computing)") (compared to [TCP 3-way handshake](https://en.wikipedia.org/wiki/Three-way_handshake#Connection_establishment "Three-way handshake")) to protect against [SYN flooding](https://en.wikipedia.org/wiki/SYN_flood "SYN flood") attacks, and large "cookies" for association verification and authenticity.

Reliability was also a key part of the security design of SCTP. Multihoming enables an association to stay open even when some routes and interfaces are down. This is of particular importance for [SIGTRAN](https://en.wikipedia.org/wiki/SIGTRAN "SIGTRAN") as it carries [SS7](https://en.wikipedia.org/wiki/Signaling_System_7 "Signaling System 7") over an IP network using SCTP, and requires strong resilience during link outages to maintain telecommunication service even when enduring network anomalies.

## Implementations

The SCTP reference implementation runs on FreeBSD, Mac OS X, Microsoft Windows, and Linux.[^10]

The following [operating systems](https://en.wikipedia.org/wiki/Operating_system "Operating system") implement SCTP:

- [AIX](https://en.wikipedia.org/wiki/AIX "AIX") Version 5 and newer
- [NetBSD](https://en.wikipedia.org/wiki/NetBSD "NetBSD") [^11] since 8.0 [^12]
- [Cisco IOS](https://en.wikipedia.org/wiki/Cisco_IOS "Cisco IOS") 12 and above
- [DragonFly BSD](https://en.wikipedia.org/wiki/DragonFly_BSD "DragonFly BSD") since version 1.4, however support is being deprecated in version 4.2 [^13]
- [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD"), version 7 and above, contains the reference SCTP implementation [^14]
- [HP-UX](https://en.wikipedia.org/wiki/HP-UX "HP-UX"), 11i v2 and above [^15]
- [illumos](https://en.wikipedia.org/wiki/Illumos "Illumos")
- [Linux](https://en.wikipedia.org/wiki/Linux "Linux") kernel 2.4 and above
- [QNX](https://en.wikipedia.org/wiki/QNX "QNX") Neutrino Realtime OS,[^16] 6.3.0 to 6.3.2, deprecated since 6.4.0 [^17]
- [Tru64](https://en.wikipedia.org/wiki/Tru64 "Tru64") with the Compaq SCTP add-on package
- Sun [Solaris](https://en.wikipedia.org/wiki/Solaris_\(operating_system\) "Solaris (operating system)") 10 and above [^18]
- [VxWorks](https://en.wikipedia.org/wiki/VxWorks "VxWorks") versions 6.2.x to 6.4.x, and 6.7 and newer

Third-party drivers:

- [Microsoft Windows](https://en.wikipedia.org/wiki/Microsoft_Windows "Microsoft Windows"):
	- The SctpDrv kernel driver is a port of the BSD SCTP stack to Windows (Abandoned after 2012) [^19]
- [MacOS](https://en.wikipedia.org/wiki/MacOS "MacOS"):
	- SCTP Network Kernel Extension for Mac OS X [^20]

[Userspace](https://en.wikipedia.org/wiki/Userspace "Userspace") library:

- Portable SCTP userland stack [^21]
- The SCTP library [^22]
	- [Windows XP](https://en.wikipedia.org/wiki/Windows_XP "Windows XP") port [^23]
- [Oracle Java SE 7](https://en.wikipedia.org/wiki/Java_version_history#Java_SE_7 "Java version history")
- [Erlang/OTP](https://en.wikipedia.org/wiki/Erlang/OTP "Erlang/OTP")

The following applications implement SCTP:

- [WebRTC](https://en.wikipedia.org/wiki/WebRTC "WebRTC")
- [NetFlow](https://en.wikipedia.org/wiki/NetFlow "NetFlow")

### Tunneling over UDP

In the absence of native SCTP support in operating systems, it is possible to [tunnel](https://en.wikipedia.org/wiki/Tunneling_protocol "Tunneling protocol") SCTP over UDP,[^24] as well as to map TCP API calls to SCTP calls so existing applications can use SCTP without modification.[^25]

## RFCs

- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [9260](https://www.rfc-editor.org/rfc/rfc9260) Stream Control Transmission Protocol
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [8540](https://www.rfc-editor.org/rfc/rfc8540) Stream Control Transmission Protocol: Errata and Issues in RFC 4960 (obsoleted by RFC 9260)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [7829](https://www.rfc-editor.org/rfc/rfc7829) SCTP-PF: A Quick Failover Algorithm for the Stream Control Transmission Protocol
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [7765](https://www.rfc-editor.org/rfc/rfc7765) TCP and Stream Control Transmission Protocol (SCTP) RTO Restart
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [7496](https://www.rfc-editor.org/rfc/rfc7496) Additional Policies for the Partially Reliable Stream Control Transmission Protocol Extension
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [7053](https://www.rfc-editor.org/rfc/rfc7053) SACK-IMMEDIATELY Extension for the Stream Control Transmission Protocol (obsoleted by RFC 9260)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [6951](https://www.rfc-editor.org/rfc/rfc6951) UDP Encapsulation of Stream Control Transmission Protocol (SCTP) Packets for End-Host to End-Host Communication
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [6525](https://www.rfc-editor.org/rfc/rfc6525) Stream Control Transmission Protocol (SCTP) Stream Reconfiguration
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [6458](https://www.rfc-editor.org/rfc/rfc6458) Sockets API Extensions for the Stream Control Transmission Protocol (SCTP)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [6096](https://www.rfc-editor.org/rfc/rfc6096) Stream Control Transmission Protocol (SCTP) Chunk Flags Registration (obsoleted by RFC 9260)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [5062](https://www.rfc-editor.org/rfc/rfc5062) Security Attacks Found Against the Stream Control Transmission Protocol (SCTP) and Current Countermeasures
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [5061](https://www.rfc-editor.org/rfc/rfc5061) Stream Control Transmission Protocol (SCTP) Dynamic Address Reconfiguration
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [5043](https://www.rfc-editor.org/rfc/rfc5043) Stream Control Transmission Protocol (SCTP) Direct Data Placement (DDP) Adaptation
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [4960](https://www.rfc-editor.org/rfc/rfc4960) Stream Control Transmission Protocol (obsoleted by RFC 9260)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [4895](https://www.rfc-editor.org/rfc/rfc4895) Authenticated Chunks for the Stream Control Transmission Protocol (SCTP)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [4820](https://www.rfc-editor.org/rfc/rfc4820) Padding Chunk and Parameter for the Stream Control Transmission Protocol (SCTP)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [4460](https://www.rfc-editor.org/rfc/rfc4460) Stream Control Transmission Protocol (SCTP) Specification Errata and Issues (obsoleted by RFC 9260)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3873](https://www.rfc-editor.org/rfc/rfc3873) Stream Control Transmission Protocol (SCTP) [Management Information Base](https://en.wikipedia.org/wiki/Management_Information_Base "Management Information Base") (MIB)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3758](https://www.rfc-editor.org/rfc/rfc3758) Stream Control Transmission Protocol (SCTP) Partial Reliability Extension
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3554](https://www.rfc-editor.org/rfc/rfc3554) On the Use of Stream Control Transmission Protocol (SCTP) with [IPsec](https://en.wikipedia.org/wiki/IPsec "IPsec")
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3436](https://www.rfc-editor.org/rfc/rfc3436) Transport Layer Security over Stream Control Transmission Protocol
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3309](https://www.rfc-editor.org/rfc/rfc3309) Stream Control Transmission Protocol (SCTP) Checksum Change (obsoleted by RFC 4960)
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3286](https://www.rfc-editor.org/rfc/rfc3286) An Introduction to the Stream Control Transmission Protocol
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [3257](https://www.rfc-editor.org/rfc/rfc3257) Stream Control Transmission Protocol Applicability Statement
- [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [2960](https://www.rfc-editor.org/rfc/rfc2960) Stream Control Transmission Protocol (updated by RFC 3309 and obsoleted by RFC 4960)

[^1]: The [DATA chunk](https://en.wikipedia.org/wiki/SCTP_packet_structure#DATA_chunk "SCTP packet structure") uses a sequence number for ordered messages, the [I-DATA chunk](https://en.wikipedia.org/wiki/SCTP_packet_structure#I-DATA_chunk "SCTP packet structure"), which solves some problems with the original DATA chunk, uses a message-id for all messages

[^2]: See [SCTP packet structure](https://en.wikipedia.org/wiki/SCTP_packet_structure "SCTP packet structure") for more details.

[^3]: ["Protocol Numbers"](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml). *iana.org*. [IANA](https://en.wikipedia.org/wiki/IANA "IANA"). Retrieved 2014-09-09.

[^4]: [*Stream Control Transmission Protocol*](https://www.rfc-editor.org/rfc/rfc2960). [IETF](https://en.wikipedia.org/wiki/IETF "IETF"). October 2000. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC2960](https://doi.org/10.17487%2FRFC2960). [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [2960](https://datatracker.ietf.org/doc/html/rfc2960).

[^5]: ["Transport"](https://datatracker.ietf.org/doc/html/rfc3588#section-2.1). [*Diameter Base Protocol*](https://www.rfc-editor.org/rfc/rfc3588). [IETF](https://en.wikipedia.org/wiki/IETF "IETF"). sec. 2.1. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC3588](https://doi.org/10.17487%2FRFC3588). [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [3588](https://datatracker.ietf.org/doc/html/rfc3588). Retrieved 2012-05-18.

[^6]: ["Example Scenario Using RSerPool Session Services"](https://datatracker.ietf.org/doc/html/rfc5351#section-4.2). [*An Overview of Reliable Server Pooling Protocols*](https://www.rfc-editor.org/rfc/rfc5351). [IETF](https://en.wikipedia.org/wiki/IETF "IETF"). p. 10. sec. 4.2. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC5351](https://doi.org/10.17487%2FRFC5351). [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [5351](https://datatracker.ietf.org/doc/html/rfc5351).

[^7]: [RFC 9260, section 1.5.5](https://tools.ietf.org/html/rfc9260#section-1.5.5)

[^8]: Hogg, Scott. ["What About Stream Control Transmission Protocol (SCTP)?"](https://web.archive.org/web/20140830095541/http://www.networkworld.com/article/2222277/cisco-subnet/what-about-stream-control-transmission-protocol--sctp--.html). *Network World*. Archived from [the original](http://www.networkworld.com/article/2222277/cisco-subnet/what-about-stream-control-transmission-protocol--sctp--.html) on August 30, 2014. Retrieved 2017-10-04.

[^9]: Olsson, Magnus; Mulligan, Catherine; Sultana, Shabnam; Rommer, Stefan; Frid, Lars (2013). *EPC and 4G packet networks: driving the mobile broadband revolution* (2nd ed.). Amsterdam Boston: Elsevier/AP, Academic Press is an imprint of Elsevier. p. 491. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-12-394595-2](https://en.wikipedia.org/wiki/Special:BookSources/978-0-12-394595-2 "Special:BookSources/978-0-12-394595-2").

[^10]: ["Reference Implementation for SCTP - RFC4960"](https://github.com/sctplab/sctp-refimpl). *[GitHub](https://en.wikipedia.org/wiki/GitHub "GitHub")*. Retrieved 2013-10-14. This is the reference implementation for SCTP. It is portable and runs on FreeBSD/MAC-OS/Windows and in User Space (including linux).

[^11]: ["sys/netinet/sctp.h"](http://bxr.su/n/sys/netinet/sctp.h). *BSD Cross Reference*. [NetBSD](https://en.wikipedia.org/wiki/NetBSD "NetBSD"). 2017-06-27. Retrieved 2019-01-21.

[^12]: ["man4/sctp.4"](http://bxr.su/n/share/man/man4/sctp.4). *BSD Cross Reference*. [NetBSD](https://en.wikipedia.org/wiki/NetBSD "NetBSD"). 2018-07-31. Retrieved 2019-01-21.

[^13]: ["DragonFly Removes SCTP"](http://lists.dragonflybsd.org/pipermail/commits/2015-January/417496.html). *Lists.dragonflybsd.org*. 7 January 2015. Retrieved 2016-04-28.

[^14]: ["About FreeBSD's Technological Advances"](http://www.freebsd.org/features.html). The FreeBSD Project. 2008-03-09. Retrieved 2008-09-13. SCTP: FreeBSD 7.0 is the reference implementation for the new IETF Stream Control Transmission Protocol (SCTP) protocol, intended to support VoIP, telecommunications, and other applications with strong reliability and variable quality transmission through features such as multi-path delivery, fail-over, and multi-streaming.

[^15]: ["Stream Control Transmission Protocol (SCTP)"](http://h20293.www2.hp.com/portal/swdepot/displayInstallInfo.do?productNumber=SCTP). Hewlett-Packard Development Company.

[^16]: ["TCP/IP Networking"](http://www.qnx.com/developers/docs/6.3.0SP3/neutrino/sys_arch/tcpip.html#SCTP). *QNX Developer Support*. QNX Software Systems. Retrieved 2008-09-13.["What's New in this Reference"](http://www.qnx.com/developers/docs/6.5.0/topic/com.qnx.doc.neutrino_lib_ref/whats_new.html). *QNX Library Reference*. QNX Software Systems. Retrieved 2012-12-18.

[^17]: ["QNX Software Development Platform 6.4.0"](http://www.qnx.com/developers/docs/660/index.jsp?topic=%2Fcom.qnx.doc.neutrino.utilities%2Ftopic%2Fwhats_new_64.html).

[^18]: ["Solaris 10 Operating System Networking — Extreme Network Performance"](http://www.sun.com/software/solaris/ds/network_performance.jsp#1). [Sun Microsystems](https://en.wikipedia.org/wiki/Sun_Microsystems "Sun Microsystems"). Retrieved 2008-09-13.

[^19]: ["SctpDrv: an SCTP driver for Microsoft Windows"](https://web.archive.org/web/20171008083650/http://www.bluestop.org:80/SctpDrv/). Archived from [the original](http://www.bluestop.org/SctpDrv) on 2017-10-08. Retrieved 2022-01-04.

[^20]: ["SCTP Network Kernel Extension for Mac OS X"](https://github.com/sctplab/SCTP_NKE_ElCapitan). *[GitHub](https://en.wikipedia.org/wiki/GitHub "GitHub")*. 23 September 2021.

[^21]: ["sctplab/usrsctp"](https://github.com/sctplab/usrsctp). *Github*. Retrieved 21 September 2021.

[^22]: ["sctplib and socketapi: The User-Space SCTP Library (sctplib) and Socket API Library (socketapi)"](https://www.nntb.no/~dreibh/sctplib/). 2025-07-09. Retrieved 2025-07-09.

[^23]: ["Windows SCTP library installer"](http://www.sctp.be/sctplib/index.htm). Retrieved 2011-02-04.

[^24]: Tuexen, Michael; Stewart, Randall R. (May 2013). [*UDP Encapsulation of Stream Control Transmission Protocol (SCTP) Packets for End-Host to End-Host Communication*](https://www.rfc-editor.org/rfc/rfc6951). [IETF](https://en.wikipedia.org/wiki/IETF "IETF"). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC6951](https://doi.org/10.17487%2FRFC6951). [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [6951](https://datatracker.ietf.org/doc/html/rfc6951).

[^25]: Bickhart, Ryan; Paul D. Amer; Randall R. Stewart (2007). ["Transparent TCP-to-SCTP Translation Shim Layer"](http://www.cis.udel.edu/~amer/PEL/poc/pdf/EuroBSDCon2007-bickhart-SCTP-Shim-layer.pdf) (PDF). Retrieved 2008-09-13.

[^26]: D. Wing; A. Yourtchenko (April 2012). ["Happy Eyeballs: Success with Dual-Stack Hosts"](https://tools.ietf.org/html/rfc6555). *tools.ietf.org*. [IETF](https://en.wikipedia.org/wiki/IETF "IETF").

[^27]: Khademi, Naeem; Brunstrom, Anna; Hurtig, Per; Grinnemo, Karl-Johan (July 21, 2016). ["Happy Eyeballs for Transport Selection"](https://tools.ietf.org/html/draft-grinnemo-taps-he). *tools.ietf.org*. [IETF](https://en.wikipedia.org/wiki/IETF "IETF"). Retrieved 2017-01-09.