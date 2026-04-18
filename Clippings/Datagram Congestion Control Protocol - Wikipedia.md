---
title: "Datagram Congestion Control Protocol - Wikipedia"
source: "https://en.wikipedia.org/wiki/Datagram_Congestion_Control_Protocol"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2004-09-25
created: 2026-04-13
description:
tags:
  - "clippings"
---
In [computer networking](https://en.wikipedia.org/wiki/Computer_networking "Computer networking"), the **Datagram Congestion Control Protocol** (**DCCP**) is a message-oriented [transport layer](https://en.wikipedia.org/wiki/Transport_layer "Transport layer") [protocol](https://en.wikipedia.org/wiki/Communication_protocol "Communication protocol"). DCCP implements reliable connection setup, teardown, [Explicit Congestion Notification](https://en.wikipedia.org/wiki/Explicit_Congestion_Notification "Explicit Congestion Notification") (ECN), [congestion control](https://en.wikipedia.org/wiki/Congestion_control "Congestion control"), and feature negotiation. The [IETF](https://en.wikipedia.org/wiki/IETF "IETF") published DCCP as [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [4340](https://www.rfc-editor.org/rfc/rfc4340), a [proposed standard](https://en.wikipedia.org/wiki/Proposed_standard "Proposed standard"), in March 2006. [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [4336](https://www.rfc-editor.org/rfc/rfc4336) provides an introduction.

## Operation

DCCP provides a way to gain access to congestion-control mechanisms without having to implement them at the [application layer](https://en.wikipedia.org/wiki/Application_layer "Application layer"). It allows for flow-based semantics like in [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") (TCP) but does not provide reliable in-order delivery. Sequenced delivery within multiple streams, as in the [Stream Control Transmission Protocol](https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol "Stream Control Transmission Protocol") (SCTP), is not available in DCCP. A DCCP connection contains [acknowledgment](https://en.wikipedia.org/wiki/Acknowledgement_\(data_networks\) "Acknowledgement (data networks)") traffic as well as data traffic. Acknowledgments inform a sender whether its packets have arrived, and whether they were marked by [Explicit Congestion Notification](https://en.wikipedia.org/wiki/Explicit_Congestion_Notification "Explicit Congestion Notification") (ECN). Acknowledgements are transmitted as reliably as the congestion control mechanism in use requires, possibly completely reliably.

DCCP has the option for very long (48-bit) [sequence numbers](https://en.wikipedia.org/wiki/Sequence_number "Sequence number") corresponding to a packet ID, rather than a byte ID as in TCP. The long length of the sequence numbers aims to guard against "some blind attacks, such as the injection of DCCP-Resets into the connection".[^1]

## Applications

DCCP is useful for applications with timing constraints on the delivery of data. Such applications include [streaming media](https://en.wikipedia.org/wiki/Streaming_media "Streaming media"), [multiplayer online games](https://en.wikipedia.org/wiki/Multiplayer_online_game "Multiplayer online game") and [Internet telephony](https://en.wikipedia.org/wiki/Internet_telephony "Internet telephony"). In such applications, old messages quickly become useless, so that getting new messages is preferred to resending lost messages. As of 2017 such applications have often either settled for TCP or used [User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol "User Datagram Protocol") (UDP) and implemented their own congestion-control mechanisms, or have no congestion control at all. While being useful for these applications, DCCP can also serve as a general congestion-control mechanism for UDP-based applications, by adding, as needed, mechanisms for reliable or in-order delivery on top of UDP/DCCP. In this context, DCCP allows the use of different, but generally [TCP-friendly](https://en.wikipedia.org/wiki/TCP_Friendly_Rate_Control "TCP Friendly Rate Control"), congestion-control mechanisms.

## Implementations

The following operating systems implement DCCP:

- [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD "FreeBSD"), version 5.1 [^2] as patch
- [Linux](https://en.wikipedia.org/wiki/Linux "Linux") since version 2.6.14,[^3] but marked deprecated since version 6.4 due to lack of maintenance and scheduled for removal in 2025.[^4] Linux 6.16 drops DCCP.[^5]
	- DCCP was removed from Linux 6.16.[^6] [^7]

Userspace library:

- [DCCP-TP](http://www.phelan-4.com/dccp-tp/) [Archived](https://web.archive.org/web/20080723104232/http://www.phelan-4.com/dccp-tp/) 2008-07-23 at the [Wayback Machine](https://en.wikipedia.org/wiki/Wayback_Machine "Wayback Machine") implementation is optimized for portability, but has had no changes since June 2008.[^8]
- [GoDCCP](https://github.com/petar/GoDCCP) purpose of this implementation is to provide a standardized, portable NAT-friendly framework for peer-to-peer communications with flexible congestion control, depending on application.

## Packet structure

The DCCP generic header takes different forms depending on the value of X, the Extended Sequence Numbers bit. If X is one, the Sequence Number field is 48 bits long, and the generic header takes 16 bytes, as follows.

<table><caption>DCCP generic header (X = 1)</caption><tbody><tr><th><i>Offset</i></th><th><a href="https://en.wikipedia.org/wiki/Octet_(computing)">Octet</a></th><th colspan="8">0</th><th colspan="8">1</th><th colspan="8">2</th><th colspan="8">3</th></tr><tr><th>Octet</th><th><a href="https://en.wikipedia.org/wiki/Bit">Bit</a></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th><th>21</th><th>22</th><th>23</th><th>24</th><th>25</th><th>26</th><th>27</th><th>28</th><th>29</th><th>30</th><th>31</th></tr><tr><th>0</th><th>0</th><td colspan="16"><i>Source Port</i></td><td colspan="16"><i>Destination Port</i></td></tr><tr><th>4</th><th>32</th><td colspan="8"><i>Data Offset</i></td><td colspan="4"><i>CCVal</i></td><td colspan="4"><i>CsCov</i></td><td colspan="16"><i>Checksum</i></td></tr><tr><th>8</th><th>64</th><td colspan="3"><i>Res</i></td><td colspan="4"><i>Type</i></td><td colspan="1"><i><abbr>X</abbr></i></td><td colspan="8"><i>Reserved</i></td><td colspan="16"><i>Sequence Number (high bits)</i> ↴</td></tr><tr><th>12</th><th>96</th><td colspan="32"><i>↪Sequence Number</i></td></tr></tbody></table>

If X is zero, only the low 24 bits of the Sequence Number are transmitted, and the generic header is 12 bytes long.

<table><caption>DCCP generic header (X = 0)</caption><tbody><tr><th><i>Offset</i></th><th><a href="https://en.wikipedia.org/wiki/Octet_(computing)">Octet</a></th><th colspan="8">0</th><th colspan="8">1</th><th colspan="8">2</th><th colspan="8">3</th></tr><tr><th>Octet</th><th><a href="https://en.wikipedia.org/wiki/Bit">Bit</a></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th><th>21</th><th>22</th><th>23</th><th>24</th><th>25</th><th>26</th><th>27</th><th>28</th><th>29</th><th>30</th><th>31</th></tr><tr><th>0</th><th>0</th><td colspan="16"><i>Source Port</i></td><td colspan="16"><i>Destination Port</i></td></tr><tr><th>4</th><th>32</th><td colspan="8"><i>Data Offset</i></td><td colspan="4"><i>CCVal</i></td><td colspan="4"><i>CsCov</i></td><td colspan="16"><i>Checksum</i></td></tr><tr><th>8</th><th>64</th><td colspan="3"><i>Res</i></td><td colspan="4"><i>Type</i></td><td colspan="1"><i><abbr>X</abbr></i></td><td colspan="24"><i>Sequence Number</i></td></tr></tbody></table>

Source Port: 16 bits

Identifies the sending port.

Destination Port: 16 bits

Identifies the receiving port.

Data Offset: 8 bits

The offset from the start of the packet's DCCP header to the start of its application data area, in 32-bit words.

CCVal: 4 bits

Used by the HC-Sender CCID.

Checksum Coverage (CsCov): 4 bits

Checksum Coverage determines the parts of the packet that are covered by the Checksum field.

Checksum: 16 bits

The [Internet checksum](https://en.wikipedia.org/wiki/Internet_checksum "Internet checksum") of the packet's DCCP header (including options), a network-layer pseudoheader, and, depending on Checksum Coverage, all, some, or none of the application data.

Reserved (Res): 3 bits; Res == 0

Senders MUST set this field to all zeroes on generated packets, and receivers MUST ignore its value.

Type: 4 bits

The Type field specifies the type of the packet.

Extended Sequence Numbers (X): 1 bit

Set to one to indicate the use of an extended generic header with 48-bit Sequence and Acknowledgement Numbers.

Sequence Number: 48 or 24 bits

Identifies the packet uniquely in the sequence of all packets the source sent on this connection.

## Current development

Similarly to the extension of [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") protocol adding multipath capability ([MPTCP](https://en.wikipedia.org/wiki/MPTCP "MPTCP")), a multipath extension of DCCP is under discussion at the IETF,[^9] correspondingly denoted as [MP-DCCP](https://en.wikipedia.org/w/index.php?title=Multipath_DCCP&action=edit&redlink=1 "Multipath DCCP (page does not exist)"). First implementations have already been developed, tested, and presented in a collaborative approach between operators and academia [^10] and are available as an open source solution.

[^1]: [RFC 4340 section 7.6](http://tools.ietf.org/html/rfc4340#section-7.6)

[^2]: ["\[dccp\] FreeBSD implementation"](https://www.ietf.org/mail-archive/web/dccp/current/msg00508.html). *www.ietf.org*. Retrieved 18 April 2018.

[^3]: ["Linux gets DCCP \[LWN.net\]"](https://lwn.net/Articles/149756/). *lwn.net*. Retrieved 18 April 2018.

[^4]: ["dccp: Print deprecation notice"](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=b144fcaf46d43b1471ad6e4de66235b8cebb3c87). *kernel.org*.

[^5]: ["Linux 6.16 Expected To Remove Datagram Congestion Control Protocol "DCCP" Networking"](https://www.phoronix.com/news/Linux-6.16-Net-Next-Drops-DCCP). *www.phoronix.com*. Retrieved 15 April 2025.

[^6]: ["Linux 6.16 Expected To Remove Datagram Congestion Control Protocol "DCCP" Networking"](https://www.phoronix.com/news/Linux-6.16-Net-Next-Drops-DCCP). *www.phoronix.com*. Retrieved 29 May 2025.

[^7]: ["Merge branch 'net-retire-dccp-socket'"](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8bb3212be4b45f7a6089e45dda7dfe9abcee4d65). *git.kernel.org*.

[^8]: ["Change log for the dccp-tp wiki, retrieved June 13, 2011"](https://web.archive.org/web/20111004105003/http://www.phelan-4.com/dccp-tp/tiki-lastchanges.php?days=0). Archived from [the original](http://www.phelan-4.com/dccp-tp/tiki-lastchanges.php?days=0) on October 4, 2011. Retrieved June 13, 2011.

[^9]: Amend, Markus; Brunstrom, Anna; Kassler, Aneas; Rakocevic, Veselin; Johnson, Stephen (9 November 2021). ["DCCP Extensions for Multipath Operation with Multiple Addresses"](https://datatracker.ietf.org/doc/draft-ietf-tsvwg-multipath-dccp/).

[^10]: ["Multipath extension for DCCP"](https://multipath-dccp.org/).