---
title: "User Datagram Protocol - Wikipedia"
source: "https://en.wikipedia.org/wiki/User_Datagram_Protocol"
author:
  - "[[Contributors to Wikimedia projects]]"
published: 2001-08-23
created: 2026-04-13
description:
tags:
  - "clippings"
---
In [computer networking](https://en.wikipedia.org/wiki/Computer_network "Computer network"), the **User Datagram Protocol** (**UDP**) is one of the core [communication protocols](https://en.wikipedia.org/wiki/Communication_protocol "Communication protocol") of the [Internet protocol suite](https://en.wikipedia.org/wiki/Internet_protocol_suite "Internet protocol suite") used to send messages (transported as [datagrams](https://en.wikipedia.org/wiki/Datagram "Datagram") in [packets](https://en.wikipedia.org/wiki/Network_packet "Network packet")) to other hosts on an [Internet Protocol](https://en.wikipedia.org/wiki/Internet_Protocol "Internet Protocol") (IP) network. Within an IP network, UDP does not require prior communication to set up [communication channels](https://en.wikipedia.org/wiki/Communication_channel "Communication channel") or data paths.

UDP is a [connectionless](https://en.wikipedia.org/wiki/Connectionless "Connectionless") protocol, meaning that messages are sent without negotiating a connection and that UDP does not keep track of what it has sent.[^1] [^2] UDP provides [checksums](https://en.wikipedia.org/wiki/Checksum "Checksum") for [data integrity](https://en.wikipedia.org/wiki/Data_integrity "Data integrity"), and [port numbers](https://en.wikipedia.org/wiki/Port_numbers "Port numbers") for addressing different functions at the source and destination of the datagram. It has no [handshaking](https://en.wikipedia.org/wiki/Handshake_\(computing\) "Handshake (computing)") dialogues and thus exposes the user's program to any [unreliability](https://en.wikipedia.org/wiki/Reliability_\(computer_networking\) "Reliability (computer networking)") of the underlying network; there is no guarantee of delivery, ordering, or duplicate protection. If error-correction facilities are needed at the network interface level, an application may instead use [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") (TCP) or [Stream Control Transmission Protocol](https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol "Stream Control Transmission Protocol") (SCTP), which are designed for this purpose.

UDP is suitable for purposes where error checking and correction are either not necessary or are performed in the application; UDP avoids the overhead of such processing in the [protocol stack](https://en.wikipedia.org/wiki/Protocol_stack "Protocol stack"). Time-sensitive applications often use UDP because dropping packets is preferable to waiting for packets delayed due to [retransmission](https://en.wikipedia.org/wiki/Retransmission_\(data_networks\) "Retransmission (data networks)"), which may not be an option in a [real-time system](https://en.wikipedia.org/wiki/Real-time_system "Real-time system").[^3]

The protocol was designed by [David P. Reed](https://en.wikipedia.org/wiki/David_P._Reed "David P. Reed") in 1980 and formally defined in [RFC](https://en.wikipedia.org/wiki/RFC_\(identifier\) "RFC (identifier)") [768](https://www.rfc-editor.org/rfc/rfc768).

## Attributes

UDP is a simple message-oriented [transport layer](https://en.wikipedia.org/wiki/Transport_layer "Transport layer") protocol that is documented in RFC [768](https://www.rfc-editor.org/rfc/rfc768). Although UDP provides integrity verification (via [checksum](https://en.wikipedia.org/wiki/Checksum "Checksum")) of the header and payload,[^4] it provides no guarantees to the [upper layer protocol](https://en.wikipedia.org/wiki/Upper_layer_protocol "Upper layer protocol") for message delivery and the UDP layer retains no state of UDP messages once sent. For this reason, UDP sometimes is referred to as *[Unreliable](https://en.wikipedia.org/wiki/Reliability_\(computer_networking\) "Reliability (computer networking)") Datagram Protocol*.[^5] If transmission reliability is desired, it must be implemented in the user's application.

A number of UDP's attributes make it especially suited for certain applications.

- It is *transaction-oriented*, suitable for simple query-response protocols such as the [Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System "Domain Name System") or the [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol "Network Time Protocol").
- It provides *[datagrams](https://en.wikipedia.org/wiki/Datagram "Datagram")*, suitable for modeling other protocols such as [IP tunneling](https://en.wikipedia.org/wiki/IP_tunneling "IP tunneling") or [remote procedure call](https://en.wikipedia.org/wiki/Remote_procedure_call "Remote procedure call") and the [Network File System](https://en.wikipedia.org/wiki/Network_File_System "Network File System").
- It is *simple*, suitable for [bootstrapping](https://en.wikipedia.org/wiki/Bootstrapping "Bootstrapping") or other purposes without a full [protocol stack](https://en.wikipedia.org/wiki/Protocol_stack "Protocol stack"), such as the [DHCP](https://en.wikipedia.org/wiki/DHCP "DHCP") and [Trivial File Transfer Protocol](https://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol "Trivial File Transfer Protocol").
- It is *stateless*, suitable for very large numbers of clients, such as in [streaming media](https://en.wikipedia.org/wiki/Streaming_media "Streaming media") applications like [IPTV](https://en.wikipedia.org/wiki/IPTV "IPTV").
- The *lack of retransmission delays* makes it suitable for real-time applications such as [Voice over IP](https://en.wikipedia.org/wiki/Voice_over_IP "Voice over IP"), [online games](https://en.wikipedia.org/wiki/Online_games "Online games"), and many protocols using [Real Time Streaming Protocol](https://en.wikipedia.org/wiki/Real_Time_Streaming_Protocol "Real Time Streaming Protocol").
- Because it supports [multicast](https://en.wikipedia.org/wiki/Multicast "Multicast"), it is suitable for broadcast information, such as in many kinds of [service discovery](https://en.wikipedia.org/wiki/Service_discovery "Service discovery") and shared information such as [Precision Time Protocol](https://en.wikipedia.org/wiki/Precision_Time_Protocol "Precision Time Protocol") and [Routing Information Protocol](https://en.wikipedia.org/wiki/Routing_Information_Protocol "Routing Information Protocol").

## Ports

Applications can use [datagram sockets](https://en.wikipedia.org/wiki/Datagram_socket "Datagram socket") to establish host-to-host communications. An application binds a socket to its endpoint of data transmission, which is a combination of an [IP address](https://en.wikipedia.org/wiki/IP_address "IP address") and a [port](https://en.wikipedia.org/wiki/Port_\(computer_networking\) "Port (computer networking)"). In this way, UDP provides application [multiplexing](https://en.wikipedia.org/wiki/Multiplexing "Multiplexing"). A port is a software structure that is identified by the [port number](https://en.wikipedia.org/wiki/Port_number "Port number"), a 16-bit integer value, allowing for port numbers between 0 and 65535. Port 0 is reserved, but is a permissible source port value if the sending process does not expect messages in response.

The [Internet Assigned Numbers Authority](https://en.wikipedia.org/wiki/Internet_Assigned_Numbers_Authority "Internet Assigned Numbers Authority") (IANA) has divided port numbers into three ranges.[^6] Port numbers 0 through 1023 are used for common, well-known services. On [Unix](https://en.wikipedia.org/wiki/Unix "Unix") -like [operating systems](https://en.wikipedia.org/wiki/Operating_system "Operating system"), using one of these ports requires [superuser](https://en.wikipedia.org/wiki/Superuser "Superuser") operating permission. Port numbers 1024 through 49151 are the [registered ports](https://en.wikipedia.org/wiki/Registered_port "Registered port") used for IANA-registered services. Ports 49152 through 65535 are dynamic ports that are not officially designated for any specific service and may be used for any purpose. These may also be used as [ephemeral ports](https://en.wikipedia.org/wiki/Ephemeral_port "Ephemeral port"), which software running on the host may use to dynamically create communications endpoints as needed.[^6]

## UDP datagram structure

A UDP datagram consists of a datagram *header* followed by a *data* section (the payload data for the application). The UDP datagram header consists of 4 fields, each of which is 2 bytes (16 bits):[^3]

<table><caption>UDP header format <sup><a href="#fn:7">7</a></sup></caption><tbody><tr><th><i>Offset</i></th><th><a href="https://en.wikipedia.org/wiki/Octet_(computing)">Octet</a></th><th colspan="8">0</th><th colspan="8">1</th><th colspan="8">2</th><th colspan="8">3</th></tr><tr><th>Octet</th><th><a href="https://en.wikipedia.org/wiki/Bit">Bit</a></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th><th>21</th><th>22</th><th>23</th><th>24</th><th>25</th><th>26</th><th>27</th><th>28</th><th>29</th><th>30</th><th>31</th></tr><tr><th>0</th><th>0</th><td colspan="16"><i>Source Port</i></td><td colspan="16"><i>Destination Port</i></td></tr><tr><th>4</th><th>32</th><td colspan="16"><i>Length</i></td><td colspan="16"><i>Checksum</i></td></tr><tr><th>8</th><th>64</th><td colspan="32" rowspan="3"><i>Data</i></td></tr><tr><th>12</th><th>96</th></tr><tr><th>⋮</th><th>⋮</th></tr></tbody></table>

The use of the *Checksum* and *Source Port* fields is optional in IPv4 (light purple background in table). In IPv6, only the *Source Port* field is optional. If not used, these fields should be set to zero.[^7]

Source Port: 16 bits

This field identifies the sender's port, when used, and should be assumed to be the port to reply to if needed. If the source host is the client, the port number is likely to be an ephemeral port. If the source host is the server, the port number is likely to be a [well-known port](https://en.wikipedia.org/wiki/Well-known_port "Well-known port") number from 0 to 1023.[^6]

Destination Port: 16 bits

This field identifies the receiver's port and is required. Similar to the source port number, if the client is the destination host then the port number will likely be an ephemeral port number, and if the destination host is the server, then the port number will likely be a well-known port number.[^6]

Length: 16 bits

This field specifies the length in bytes of the UDP datagram (the header fields and Data field) in [octets](https://en.wikipedia.org/wiki/Octet_\(computing\) "Octet (computing)"). The minimum length is 8 bytes, the length of the header. The field size sets a theoretical limit of 65,535 bytes (8-byte header + 65,527 bytes of data) for a UDP datagram. However, the actual limit for the data length, which is imposed by the underlying [IPv4](https://en.wikipedia.org/wiki/IPv4 "IPv4") protocol, is 65,507 bytes (65,535 bytes − 8-byte UDP header − 20-byte [IP header](https://en.wikipedia.org/wiki/IPv4_header "IPv4 header")).[^8]

Using IPv6 [jumbograms](https://en.wikipedia.org/wiki/Jumbogram "Jumbogram") it is possible to have UDP datagrams of size greater than 65,535 bytes. The length field is set to zero if the length of the UDP header plus UDP data is greater than 65,535.[^9]

[Checksum](https://en.wikipedia.org/wiki/Internet_checksum "Internet checksum"): 16 bits

The checksum field may be used for error-checking of the header and data. This field is optional in IPv4, and mandatory in most cases in IPv6.[^10]

Data: Variable

The payload of the UDP packet.

## Checksum computation

The method used to compute the checksum is defined in RFC [768](https://www.rfc-editor.org/rfc/rfc768), and efficient calculation is discussed in RFC [1071](https://www.rfc-editor.org/rfc/rfc1071):

> Checksum is the 16-bit [ones' complement](https://en.wikipedia.org/wiki/Ones%27_complement "Ones' complement") of the ones' complement sum of a pseudo header of information from the IP header, the UDP header, and the data, padded with zero octets at the end (if necessary) to make a multiple of two octets.[^7]

In other words, all 16-bit words are summed using ones' complement arithmetic. Add the 16-bit values up. On each addition, if a carry-out (17th bit) is produced, swing that 17th carry bit around and add it to the least significant bit of the running total.[^11] Finally, the sum is then ones' complemented to yield the value of the UDP checksum field.

If the checksum calculation results in the value zero (all 16 bits 0) it should be sent as the ones' complement (all 1s) as a zero-value checksum indicates no checksum has been calculated.[^7] In this case, any specific processing is not required at the receiver, because all 0s and all 1s are equal to zero in 1's complement arithmetic.

The differences between [IPv4](https://en.wikipedia.org/wiki/IPv4 "IPv4") and [IPv6](https://en.wikipedia.org/wiki/IPv6 "IPv6") are in the pseudo header used to compute the checksum, and that the checksum is not optional in IPv6.[^12] Under specific conditions, a UDP application using IPv6 is allowed to use a zero UDP zero-checksum mode with a tunnel protocol.[^13]

When UDP runs over IPv4, the checksum is computed using a *pseudo header* that contains some of the same information from the real [IPv4 header](https://en.wikipedia.org/wiki/IPv4_header "IPv4 header").[^7]<sup><span title="Page / location: 2">: 2</span> </sup> The pseudo header is not the real IPv4 header used to send an IP packet, it is used only for the checksum calculation. UDP checksum computation is optional for IPv4. If a checksum is not used, it should be set to the value zero.

<table><caption>UDP pseudo-header for checksum computation (IPv4)</caption><tbody><tr><th><i>Offset</i></th><th><a href="https://en.wikipedia.org/wiki/Octet_(computing)">Octet</a></th><th colspan="8">0</th><th colspan="8">1</th><th colspan="8">2</th><th colspan="8">3</th></tr><tr><th>Octet</th><th><a href="https://en.wikipedia.org/wiki/Bit">Bit</a></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th><th>21</th><th>22</th><th>23</th><th>24</th><th>25</th><th>26</th><th>27</th><th>28</th><th>29</th><th>30</th><th>31</th></tr><tr><th>0</th><th>0</th><td colspan="32"><i>Source Address</i></td></tr><tr><th>4</th><th>32</th><td colspan="32"><i>Destination Address</i></td></tr><tr><th>8</th><th>64</th><td colspan="8"><i>Zeroes</i></td><td colspan="8"><i>Protocol</i></td><td colspan="16"><i>UDP Length</i></td></tr><tr><th>12</th><th>96</th><td colspan="16"><i>Source Port</i></td><td colspan="16"><i>Destination Port</i></td></tr><tr><th>16</th><th>128</th><td colspan="16"><i>Length</i></td><td colspan="16"><i>Checksum</i></td></tr><tr><th>20</th><th>160</th><td colspan="32" rowspan="3"><i>Data</i></td></tr><tr><th>24</th><th>192</th></tr><tr><th>⋮</th><th>⋮</th></tr></tbody></table>

The checksum is calculated over the following fields:

Source Address: 32 bits

The source address from the IPv4 header.

Destination Address: 32 bits

The destination address from the IPv4 header.

Zeroes: 8 bits; Zeroes == 0

All zeroes.

Protocol: 8 bits

The [protocol value](https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers "List of IP protocol numbers") for UDP: 17 (or 0x11).

UDP length: 16 bits

The length of the UDP header and data (measured in octets).

As IPv6 has larger addresses and a different header layout, the method used to compute the checksum is changed accordingly:[^10]<sup><span title="Location: §8.1">: §8.1</span></sup>

> Any transport or other upper-layer protocol that includes the addresses from the IP header in its checksum computation must be modified for use over IPv6, to include the 128-bit IPv6 addresses instead of 32-bit IPv4 addresses.

When computing the checksum, again a pseudo header is used that mimics the real [IPv6 header](https://en.wikipedia.org/wiki/IPv6_header "IPv6 header"):

<table><caption>UDP pseudo-header for checksum computation (IPv6)</caption><tbody><tr><th><i>Offset</i></th><th><a href="https://en.wikipedia.org/wiki/Octet_(computing)">Octet</a></th><th colspan="8">0</th><th colspan="8">1</th><th colspan="8">2</th><th colspan="8">3</th></tr><tr><th>Octet</th><th><a href="https://en.wikipedia.org/wiki/Bit">Bit</a></th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th><th>21</th><th>22</th><th>23</th><th>24</th><th>25</th><th>26</th><th>27</th><th>28</th><th>29</th><th>30</th><th>31</th></tr><tr><th>0</th><th>0</th><td colspan="32" rowspan="4"><i>Source address</i></td></tr><tr><th>4</th><th>32</th></tr><tr><th>8</th><th>64</th></tr><tr><th>12</th><th>96</th></tr><tr><th>16</th><th>128</th><td colspan="32" rowspan="4"><i>Destination address</i></td></tr><tr><th>20</th><th>160</th></tr><tr><th>24</th><th>192</th></tr><tr><th>28</th><th>224</th></tr><tr><th>32</th><th>256</th><td colspan="32"><i>UDP length</i></td></tr><tr><th>36</th><th>288</th><td colspan="24"><i>Zeroes (0)</i></td><td colspan="8"><i>Next Header (17)</i></td></tr><tr><th>40</th><th>320</th><td colspan="16"><i>Source port</i></td><td colspan="16"><i>Destination port</i></td></tr><tr><th>44</th><th>352</th><td colspan="16"><i>Length</i></td><td colspan="16"><i>Checksum</i></td></tr><tr><th>48</th><th>384</th><td colspan="32" rowspan="3"><i>Data</i></td></tr><tr><th>52</th><th>416</th></tr><tr><th>⋮</th><th>⋮</th></tr></tbody></table>

The checksum is computed over the following fields:

Source address: 128 bits

The address in the IPv6 header.

Destination address: 128 bits

The final destination; if the IPv6 packet does not contain a Routing header, TCP uses the destination address in the IPv6 header, otherwise, at the originating node, it uses the address in the last element of the Routing header, and, at the receiving node, it uses the destination address in the IPv6 header.

UDP length: 32 bits

The length of the UDP header and data (measured in octets).

Zeroes: 24 bits; Zeroes == 0

All zeroes.

Next Header: 8 bits

The [transport layer](https://en.wikipedia.org/wiki/Transport_layer "Transport layer") protocol value for UDP: 17.

## Reliability and congestion control

Lacking reliability, UDP applications may encounter some packet loss, reordering, errors or duplication. If using UDP, the end-user applications must provide any necessary handshaking, such as real-time confirmation that the message has been received. Certain applications (e.g., TFTP) may incorporate rudimentary reliability mechanisms at the application layer as required.[^6] For applications demanding a high degree of reliability, an alternative protocol such as the [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") may be used instead.

Most often, UDP applications do not employ reliability mechanisms and may even be hindered by them. [Streaming media](https://en.wikipedia.org/wiki/Streaming_media "Streaming media"), real-time multiplayer games and [voice over IP](https://en.wikipedia.org/wiki/Voice_over_IP "Voice over IP") (VoIP) are typical applications that leverage UDP. In these particular applications, loss of packets is not usually a fatal problem. In VoIP, for example, latency and jitter are the primary concerns. The use of TCP would cause jitter if any packets were lost, as TCP does not provide subsequent data to the application while it is requesting a re-send of the missing data.

## Applications

Numerous key Internet applications use UDP, including: the [Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System "Domain Name System") (DNS), the [Simple Network Management Protocol](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol "Simple Network Management Protocol") (SNMP), the [Routing Information Protocol](https://en.wikipedia.org/wiki/Routing_Information_Protocol "Routing Information Protocol") (RIP) [^3] and the [Dynamic Host Configuration Protocol](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol "Dynamic Host Configuration Protocol") (DHCP).

Voice and video traffic is generally transmitted using UDP. Real-time video and [audio streaming protocols](https://en.wikipedia.org/wiki/Audio_over_IP "Audio over IP") are designed to handle the occasional lost packets, so only slight degradation in quality occurs, compared to the large delays that would occur if lost packets were retransmitted. Because both TCP and UDP run over the same network, in the mid-2000s a few businesses found that an increase in UDP traffic from these real-time applications slightly hindered the performance of applications using TCP such as [point of sale](https://en.wikipedia.org/wiki/Point_of_sale "Point of sale"), [accounting](https://en.wikipedia.org/wiki/Accounting_software "Accounting software"), and [database](https://en.wikipedia.org/wiki/Database_management_system "Database management system") systems (when TCP detects packet loss, it will throttle back its data rate usage).[^14]

Some [VPN](https://en.wikipedia.org/wiki/VPN "VPN") systems, such as [OpenVPN](https://en.wikipedia.org/wiki/OpenVPN "OpenVPN"), support operation over UDP and provide application-layer error checking as well as mechanisms to enhance transmission reliability. [WireGuard](https://en.wikipedia.org/wiki/WireGuard "WireGuard") uses UDP and performs error checking, but does not provide any reliability guarantees; reliability is delegated to upper-layer protocols within the tunnel or to end applications.

[QUIC](https://en.wikipedia.org/wiki/QUIC "QUIC") is a transport protocol built on top of UDP. QUIC provides a reliable and secure connection. [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3 "HTTP/3") uses QUIC as opposed to earlier versions of [HTTPS](https://en.wikipedia.org/wiki/HTTPS "HTTPS") which use a combination of [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") and [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security "Transport Layer Security") to ensure reliability and security respectively. This means that HTTP/3 uses a single handshake to set up a connection, rather than having two separate handshakes for TCP and TLS, meaning the overall time to establish a connection is reduced.[^15]

## Comparison of UDP and TCP

[Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol "Transmission Control Protocol") is a connection-oriented protocol and requires handshaking to set up end-to-end communications. Once a connection is set up, user data may be sent bi-directionally over the connection.

- *Reliable* – TCP manages message acknowledgment, retransmission and timeouts. Multiple attempts to deliver the message are made. If data gets lost along the way, it will be resent. In TCP, there's either no missing data or, in case of multiple timeouts, the connection is dropped.
- *Ordered* – If two messages are sent over a connection in sequence, the first message will reach the receiving application first. When data segments arrive in the wrong order, TCP buffers the out-of-order data until all data can be properly re-ordered and delivered to the application.
- *Heavyweight* – TCP requires three packets to set up a socket connection before any user data can be sent. TCP handles reliability and [congestion control](https://en.wikipedia.org/wiki/Congestion_control "Congestion control").
- *Streaming* – Data is read as a [byte](https://en.wikipedia.org/wiki/Byte "Byte") stream; no distinguishing indications are transmitted to signal message (segment) boundaries.

User Datagram Protocol is a simpler message-based [connectionless protocol](https://en.wikipedia.org/wiki/Connectionless_protocol "Connectionless protocol"). Connectionless protocols do not set up a dedicated end-to-end connection. Communication is achieved by transmitting information in one direction from source to destination without verifying the readiness or state of the receiver.

- *Unreliable* – When a UDP message is sent, it cannot be known if it will reach its destination; it could get lost along the way. There is no concept of acknowledgment, retransmission, or timeout.
- *Not ordered* – If two messages are sent to the same recipient, the order in which they arrive cannot be guaranteed.
- *Lightweight* – There is no ordering of messages, no tracking connections, etc. It is a very simple transport layer designed on top of IP.
- *Datagrams* – Packets are sent individually and are checked for integrity on arrival. Packets have definite boundaries, which are honored upon receipt; a read operation at the receiver socket will yield an entire message as it was originally sent.
- *No congestion control* – UDP itself does not avoid congestion. Congestion control measures must be implemented at the application level or in the network.
- *Broadcasts* – being connectionless, UDP can broadcast - sent packets can be addressed to be receivable by all devices on the subnet.
- *Multicast* – a multicast mode of operation is supported whereby a single datagram packet can be automatically routed without duplication to a group of subscribers.

## Standards

[^1]: Castelli, Matthew J. (2003). *Network Sales and Services Handbook*. Cisco Press. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [9781587050909](https://en.wikipedia.org/wiki/Special:BookSources/9781587050909 "Special:BookSources/9781587050909").

[^2]: Stanek, William (2015). *Windows Command Line: The Personal Trainer for Windows 8.1 Windows Server 2012 and Windows Server 2012 R2*. Stanek & Associates. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [9781627164139](https://en.wikipedia.org/wiki/Special:BookSources/9781627164139 "Special:BookSources/9781627164139").

[^3]: Kurose, J. F.; Ross, K. W. (2010). *Computer Networking: A Top-Down Approach* (5th ed.). Boston, MA: Pearson Education. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-13-136548-3](https://en.wikipedia.org/wiki/Special:BookSources/978-0-13-136548-3 "Special:BookSources/978-0-13-136548-3").

[^4]: Clark, M.P. (2003). *Data Networks IP and the Internet, 1st ed*. West Sussex, England: John Wiley & Sons Ltd.

[^5]: Techwriters Future (2008). ["UDP Protocol Overview"](http://ipv6.com/articles/general/User-Datagram-Protocol.htm). Ipv6.com. Retrieved 20 December 2025.

[^6]: Forouzan, B.A. (2000). *TCP/IP: Protocol Suite, 1st ed*. New Delhi, India: Tata McGraw-Hill Publishing Company Limited.

[^7]: [J. Postel](https://en.wikipedia.org/wiki/Jon_Postel "Jon Postel"), ed. (28 August 1980). [*User Datagram Protocol*](https://www.rfc-editor.org/rfc/rfc768). [IETF](https://en.wikipedia.org/wiki/IETF "IETF"). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC0768](https://doi.org/10.17487%2FRFC0768). STD 6. [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [768](https://datatracker.ietf.org/doc/html/rfc768). *Internet Standard 6.*

[^8]: Stevens, W. Richard (1994). *TCP/IP Illustrated: The protocols*. Vol. 1 (2 ed.). Addison-Wesley. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-20-163346-7](https://en.wikipedia.org/wiki/Special:BookSources/978-0-20-163346-7 "Special:BookSources/978-0-20-163346-7").

[^9]: D. Borman; [S. Deering](https://en.wikipedia.org/wiki/Steve_Deering "Steve Deering"); R. Hinden (August 1999). [*IPv6 Jumbograms*](https://www.rfc-editor.org/rfc/rfc2675). Network Working Group. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC2675](https://doi.org/10.17487%2FRFC2675). [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [2675](https://datatracker.ietf.org/doc/html/rfc2675). *Proposed Standard.* Obsoletes RFC [2147](https://www.rfc-editor.org/rfc/rfc2147).

[^10]: [S. Deering](https://en.wikipedia.org/wiki/Steve_Deering "Steve Deering"); R. Hinden (July 2017). [*Internet Protocol, Version 6 (IPv6) Specification*](https://www.rfc-editor.org/rfc/rfc8200). [Internet Engineering Task Force](https://en.wikipedia.org/wiki/Internet_Engineering_Task_Force "Internet Engineering Task Force"). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC8200](https://doi.org/10.17487%2FRFC8200). STD 86. [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [8200](https://datatracker.ietf.org/doc/html/rfc8200). *Internet Standard 86.* Obsoletes RFC [2460](https://www.rfc-editor.org/rfc/rfc2460).

[^11]: ["Compute 16-bit Ones' Complement Sum"](https://web.archive.org/web/20201117162031/http://mathforum.org/library/drmath/view/54379.html). *mathforum.org*. John. 20 March 2002. Archived from [the original](http://mathforum.org/library/drmath/view/54379.html) ([email](https://en.wikipedia.org/wiki/Email "Email")) on 17 November 2020. Retrieved 5 November 2014.

[^12]: [*Internet Protocol, Version 6 (IPv6) Specification*](https://www.rfc-editor.org/rfc/rfc8200#page-27-28). [IETF](https://en.wikipedia.org/wiki/Internet_Engineering_Task_Force "Internet Engineering Task Force"). p. 27-28. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC8200](https://doi.org/10.17487%2FRFC8200). [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [8200](https://datatracker.ietf.org/doc/html/rfc8200).

[^13]: [*Internet Protocol, Version 6 (IPv6) Specification*](https://www.rfc-editor.org/rfc/rfc8085#page-23). [IETF](https://en.wikipedia.org/wiki/Internet_Engineering_Task_Force "Internet Engineering Task Force"). p. 23. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.17487/RFC8085](https://doi.org/10.17487%2FRFC8085). [RFC](https://en.wikipedia.org/wiki/Request_for_Comments "Request for Comments") [8085](https://datatracker.ietf.org/doc/html/rfc8085).

[^14]: ["The impact of UDP on Data Applications"](http://www.networkperformancedaily.com/2007/08/whiteboard_series_nice_guys_fi.html). Networkperformancedaily.com. Retrieved 17 August 2011.

[^15]: ["QUIC, a multiplexed stream transport over UDP"](https://www.chromium.org/quic). *chromium.org*. Retrieved 17 February 2021.