---
title: "Chapter 1. Introduction"
source: "https://www.wireshark.org/docs/wsug_html_chunked/ChapterIntroduction.html"
author:
published:
created: 2026-04-13
description:
tags:
  - "clippings"
---
<table width="100%"><tbody><tr><th colspan="3" align="center">Chapter 1. Introduction</th></tr><tr><td width="20%" align="left"><a href="https://www.wireshark.org/docs/wsug_html_chunked/PrefaceTypographicConventions.html">Prev</a></td><th width="60%" align="center"></th><td width="20%" align="right"><a href="https://www.wireshark.org/docs/wsug_html_chunked/ChIntroPlatforms.html">Next</a></td></tr></tbody></table>

---

## 1.1. What is Wireshark?

Wireshark is a network packet analyzer. A network packet analyzer presents captured packet data in as much detail as possible.

You could think of a network packet analyzer as a measuring device for examining what’s happening inside a network cable, just like an electrician uses a voltmeter for examining what’s happening inside an electric cable (but at a higher level, of course).

In the past, such tools were either very expensive, proprietary, or both. However, with the advent of Wireshark, that has changed. Wireshark is available for free, is open source, and is one of the best packet analyzers available today.

### 1.1.1. Some intended purposes

Here are some reasons people use Wireshark:

- Network administrators use it to *troubleshoot network problems*
- Network security engineers use it to *examine security problems*
- QA engineers use it to *verify network applications*
- Developers use it to *debug protocol implementations*
- People use it to *learn network protocol* internals

Wireshark can also be helpful in many other situations.

### 1.1.2. Features

The following are some of the many features Wireshark provides:

- Available for *UNIX* and *Windows*.
- *Capture* live packet data from a network interface.
- *Open* files containing packet data captured with tcpdump/WinDump, Wireshark, and many other packet capture programs.
- *Import* packets from text files containing hex dumps of packet data.
- Display packets with *very detailed protocol information*.
- *Save* packet data captured.
- *Export* some or all packets in a number of capture file formats.
- *Filter packets* on many criteria.
- *Search* for packets on many criteria.
- *Colorize* packet display based on filters.
- Create various *statistics*.
- …and *a lot more!*

However, to really appreciate its power you have to start using it.

[Figure 1.1, “Wireshark captures packets and lets you examine their contents.”](https://www.wireshark.org/docs/wsug_html_chunked/ChapterIntroduction.html#ChIntroFig1 "Figure 1.1. Wireshark captures packets and lets you examine their contents.") shows Wireshark having captured some packets and waiting for you to examine them.

**Figure 1.1. Wireshark captures packets and lets you examine their contents.**

![ws main](https://www.wireshark.org/docs/wsug_html_chunked/images/ws-main.png)  

### 1.1.3. Live capture from many different network media

Wireshark can capture traffic from many different network media types, including Ethernet, Wireless LAN, Bluetooth, USB, and more. The specific media types supported may be limited by several factors, including your hardware and operating system. An overview of the supported media types can be found at [https://wiki.wireshark.org/CaptureSetup/NetworkMedia](https://wiki.wireshark.org/CaptureSetup/NetworkMedia).

### 1.1.4. Import files from many other capture programs

Wireshark can open packet captures from a large number of capture programs. For a list of input formats see [Section 5.2.2, “Input File Formats”](https://www.wireshark.org/docs/wsug_html_chunked/ChIOOpenSection.html#ChIOInputFormatsSection "5.2.2. Input File Formats").

### 1.1.5. Export files for many other capture programs

Wireshark can save captured packets in many formats, including those used by other capture programs. For a list of output formats see [Section 5.3.2, “Output File Formats”](https://www.wireshark.org/docs/wsug_html_chunked/ChIOSaveSection.html#ChIOOutputFormatsSection "5.3.2. Output File Formats").

### 1.1.6. Many protocol dissectors

There are protocol dissectors (or decoders, as they are known in other products) for a great many protocols: see [Section B.5.3, “Windows temporary folder”](https://www.wireshark.org/docs/wsug_html_chunked/ChWindowsFolder.html#AppProtocols).

### 1.1.7. Open Source Software

Wireshark is an open source software project, and is released under the [GNU General Public License](https://www.gnu.org/licenses/gpl-2.0.html) (GPL). You can freely use Wireshark on any number of computers you like, without worrying about license keys or fees or such. In addition, all source code is freely available under the GPL. Because of that, it is very easy for people to add new protocols to Wireshark, either as plugins, or built into the source, and they often do!

### 1.1.8. What Wireshark is not

Here are some things Wireshark does not provide:

- Wireshark isn’t an intrusion detection system. It will not warn you when someone does strange things on your network that he/she isn’t allowed to do. However, if strange things happen, Wireshark might help you figure out what is really going on.
- Wireshark will not manipulate things on the network, it will only “measure” things from it. Wireshark doesn’t send packets on the network or do other active things (except domain name resolution, but that can be disabled).