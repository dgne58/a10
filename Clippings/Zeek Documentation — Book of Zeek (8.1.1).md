---
title: "Zeek Documentation — Book of Zeek (8.1.1)"
source: "https://docs.zeek.org/en/current/"
author:
published:
created: 2026-04-13
description:
tags:
  - "clippings"
---
![_images/zeek-logo-text.png](https://docs.zeek.org/en/current/_images/zeek-logo-text.png)

**Version 8.1.1**

## Zeek Documentation

Important

Make sure to read the.

The purpose of this manual is to assist the Zeek community with implementing Zeek in their environments. It includes material on Zeek’s unique capabilities, how to install it, how to interpret the default logs that Zeek generates, and how to modify Zeek to fit your needs. This documentation is the result of a volunteer community effort. If you would like to contribute, or want more information, please visit the [Zeek web page](https://zeek.org/getting-started-in-the-zeek-community/) for details on how to connect with the community.

Table of Contents

- [Get Started](https://docs.zeek.org/en/current/get-started.html)
	- [Installing Zeek](https://docs.zeek.org/en/current/install.html)
		- [Quick Start Guide](https://docs.zeek.org/en/current/quickstart.html)
		- [Zeek Cluster Setup](https://docs.zeek.org/en/current/cluster-setup.html)
		- [Building from Source](https://docs.zeek.org/en/current/building-from-source.html)
- [About Zeek](https://docs.zeek.org/en/current/about.html)
	- [What Is Zeek?](https://docs.zeek.org/en/current/about.html#what-is-zeek)
		- [Why Zeek?](https://docs.zeek.org/en/current/about.html#why-zeek)
		- [History](https://docs.zeek.org/en/current/about.html#history)
		- [Architecture](https://docs.zeek.org/en/current/about.html#architecture)
- [Monitoring With Zeek](https://docs.zeek.org/en/current/monitoring.html)
	- [Detection and Response Workflow](https://docs.zeek.org/en/current/monitoring.html#detection-and-response-workflow)
		- [Instrumentation and Collection](https://docs.zeek.org/en/current/monitoring.html#instrumentation-and-collection)
		- [Storage and Review](https://docs.zeek.org/en/current/monitoring.html#storage-and-review)
- [Zeek Log Formats and Inspection](https://docs.zeek.org/en/current/log-formats.html)
	- [Working with a Sample Trace](https://docs.zeek.org/en/current/log-formats.html#working-with-a-sample-trace)
		- [Zeek TSV Format Logs](https://docs.zeek.org/en/current/log-formats.html#zeek-tsv-format-logs)
		- [Zeek TSV Format and **awk**](https://docs.zeek.org/en/current/log-formats.html#zeek-tsv-format-and-awk)
		- [Zeek TSV Format and **zeek-cut**](https://docs.zeek.org/en/current/log-formats.html#zeek-tsv-format-and-zeek-cut)
		- [Zeek JSON Format Logs](https://docs.zeek.org/en/current/log-formats.html#zeek-json-format-logs)
		- [Zeek JSON Format and **jq**](https://docs.zeek.org/en/current/log-formats.html#zeek-json-format-and-jq)
		- [Log Schemas](https://docs.zeek.org/en/current/log-formats.html#log-schemas)
- [Zeek Logs](https://docs.zeek.org/en/current/logs/index.html)
	- [analyzer.log](https://docs.zeek.org/en/current/logs/analyzer.html)
		- [conn.log](https://docs.zeek.org/en/current/logs/conn.html)
		- [dns.log](https://docs.zeek.org/en/current/logs/dns.html)
		- [http.log](https://docs.zeek.org/en/current/logs/http.html)
		- [files.log](https://docs.zeek.org/en/current/logs/files.html)
		- [ftp.log](https://docs.zeek.org/en/current/logs/ftp.html)
		- [ssl.log](https://docs.zeek.org/en/current/logs/ssl.html)
		- [x509.log](https://docs.zeek.org/en/current/logs/x509.html)
		- [smtp.log](https://docs.zeek.org/en/current/logs/smtp.html)
		- [ssh.log](https://docs.zeek.org/en/current/logs/ssh.html)
		- [pe.log](https://docs.zeek.org/en/current/logs/pe.html)
		- [dhcp.log](https://docs.zeek.org/en/current/logs/dhcp.html)
		- [ntp.log](https://docs.zeek.org/en/current/logs/ntp.html)
		- [SMB Logs (plus DCE-RPC, Kerberos, NTLM)](https://docs.zeek.org/en/current/logs/smb.html)
		- [irc.log](https://docs.zeek.org/en/current/logs/irc.html)
		- [ldap.log and ldap\_search.log](https://docs.zeek.org/en/current/logs/ldap.html)
		- [postgresql.log](https://docs.zeek.org/en/current/logs/postgresql.html)
		- [quic.log](https://docs.zeek.org/en/current/logs/quic.html)
		- [rdp.log](https://docs.zeek.org/en/current/logs/rdp.html)
		- [traceroute.log](https://docs.zeek.org/en/current/logs/traceroute.html)
		- [tunnel.log](https://docs.zeek.org/en/current/logs/tunnel.html)
		- [known\_\*.log and software.log](https://docs.zeek.org/en/current/logs/known-and-software.html)
		- [weird.log and notice.log](https://docs.zeek.org/en/current/logs/weird-and-notice.html)
		- [capture\_loss.log and reporter.log](https://docs.zeek.org/en/current/logs/capture-loss-and-reporter.html)
- [Introduction to Scripting](https://docs.zeek.org/en/current/scripting/index.html)
	- [The Basics](https://docs.zeek.org/en/current/scripting/basics.html)
		- [Finding Potential Usage Errors](https://docs.zeek.org/en/current/scripting/usage.html)
		- [Event Groups](https://docs.zeek.org/en/current/scripting/event-groups.html)
		- [Use of `conn_id_ctx`](https://docs.zeek.org/en/current/scripting/conn-id-ctx.html)
		- [Tracing Events](https://docs.zeek.org/en/current/scripting/tracing-events.html)
		- [Script Optimization](https://docs.zeek.org/en/current/scripting/optimization.html)
		- [JavaScript](https://docs.zeek.org/en/current/scripting/javascript.html)
- [Frameworks](https://docs.zeek.org/en/current/frameworks/index.html)
	- [Broker Communication Framework](https://docs.zeek.org/en/current/frameworks/broker.html)
		- [Cluster Framework](https://docs.zeek.org/en/current/frameworks/cluster.html)
		- [Configuration Framework](https://docs.zeek.org/en/current/frameworks/configuration.html)
		- [File Analysis Framework](https://docs.zeek.org/en/current/frameworks/file-analysis.html)
		- [Input Framework](https://docs.zeek.org/en/current/frameworks/input.html)
		- [Intelligence Framework](https://docs.zeek.org/en/current/frameworks/intel.html)
		- [Logging Framework](https://docs.zeek.org/en/current/frameworks/logging.html)
		- [Management Framework](https://docs.zeek.org/en/current/frameworks/management.html)
		- [NetControl Framework](https://docs.zeek.org/en/current/frameworks/netcontrol.html)
		- [Notice Framework](https://docs.zeek.org/en/current/frameworks/notice.html)
		- [Packet Analysis](https://docs.zeek.org/en/current/frameworks/packet-analysis.html)
		- [Signature Framework](https://docs.zeek.org/en/current/frameworks/signatures.html)
		- [Storage Framework](https://docs.zeek.org/en/current/frameworks/storage.html)
		- [Summary Statistics](https://docs.zeek.org/en/current/frameworks/sumstats.html)
		- [Supervisor Framework](https://docs.zeek.org/en/current/frameworks/supervisor.html)
		- [Telemetry Framework](https://docs.zeek.org/en/current/frameworks/telemetry.html)
		- [TLS Decryption](https://docs.zeek.org/en/current/frameworks/tls-decryption.html)
- [Popular Customizations](https://docs.zeek.org/en/current/customizations.html)
	- [Log Enrichment](https://docs.zeek.org/en/current/customizations.html#log-enrichment)
		- [Log Writers](https://docs.zeek.org/en/current/customizations.html#log-writers)
		- [Logging](https://docs.zeek.org/en/current/customizations.html#logging)
		- [Profiling and Debugging](https://docs.zeek.org/en/current/customizations.html#profiling-and-debugging)
- [Troubleshooting](https://docs.zeek.org/en/current/troubleshooting.html)
	- [Memory Leaks and State Growth](https://docs.zeek.org/en/current/troubleshooting.html#memory-leaks-and-state-growth)
		- [CPU Profiling](https://docs.zeek.org/en/current/troubleshooting.html#cpu-profiling)
		- [Metrics and Stats](https://docs.zeek.org/en/current/troubleshooting.html#metrics-and-stats)
- [Script Reference](https://docs.zeek.org/en/current/script-reference/index.html)
	- [Operators](https://docs.zeek.org/en/current/script-reference/operators.html)
		- [Types](https://docs.zeek.org/en/current/script-reference/types.html)
		- [Attributes](https://docs.zeek.org/en/current/script-reference/attributes.html)
		- [Declarations and Statements](https://docs.zeek.org/en/current/script-reference/statements.html)
		- [Directives](https://docs.zeek.org/en/current/script-reference/directives.html)
		- [Log Files](https://docs.zeek.org/en/current/script-reference/log-files.html)
		- [Notices](https://docs.zeek.org/en/current/script-reference/notices.html)
		- [Packet Analyzers](https://docs.zeek.org/en/current/script-reference/packet-analyzers.html)
		- [Protocol Analyzers](https://docs.zeek.org/en/current/script-reference/proto-analyzers.html)
		- [File Analyzers](https://docs.zeek.org/en/current/script-reference/file-analyzers.html)
		- [Zeek Package Index](https://docs.zeek.org/en/current/script-reference/packages.html)
		- [Zeek Script Index](https://docs.zeek.org/en/current/script-reference/scripts.html)
		- [Zeekygen Example Script](https://docs.zeek.org/en/current/scripts/zeekygen/example.zeek.html)
- [Developer Guides](https://docs.zeek.org/en/current/devel/index.html)
	- [Writing Plugins](https://docs.zeek.org/en/current/devel/plugins.html)
		- [Writing Analyzers with Spicy](https://docs.zeek.org/en/current/devel/spicy/index.html)
		- [Interacting with Zeek using WebSockets](https://docs.zeek.org/en/current/devel/websocket-api.html)
		- [Contributor’s Guide](https://docs.zeek.org/en/current/devel/contributors.html)
		- [Maintainer’s Guide](https://docs.zeek.org/en/current/devel/maintainers.html)
		- [ZeroMQ Cluster Backend](https://docs.zeek.org/en/current/devel/cluster-backend-zeromq.html)
		- [Connection Handling](https://docs.zeek.org/en/current/devel/conn.html)
- [Subcomponents](https://docs.zeek.org/en/current/components/index.html)
- [Acknowledgements](https://docs.zeek.org/en/current/acknowledgements.html)

- [Index](https://docs.zeek.org/en/current/genindex.html)

## Documentation Versioning

Attention

Zeek publishes both *feature* and *long-term support* releases. By default, the Zeek documentation at [docs.zeek.org](https://docs.zeek.org/) points to whichever release is the most recent (or *current*). In the current documentation, you may also find a dropdown menu in the banner, which lets you select the documentation version. For your convenience, the most used versions are:

We typically keep the last version from each release cycle available. The current release cycle(s) (LTS and/or feature) will have all versions available, but some may be hidden in the UI dropdown menu.

Zeek’s version numbering scheme is described in the [Release Cadence](https://github.com/zeek/zeek/wiki/Release-Cadence) policy.