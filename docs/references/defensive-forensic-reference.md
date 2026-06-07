# Defensive & Forensic Reference

## Comprehensive Techniques, Commands, Tools & Methodology

Extracted from 7 authoritative texts: The Art of Memory Forensics, Network Forensics 2012, The Practice of Network Security Monitoring, Packet Analysis with Wireshark, Blue Team Field Manual (BTFM), Immutable Security Controls, and CIS Controls v7.1.

---

## 1. MEMORY FORENSICS (The Art of Memory Forensics)

### 1.1 Volatility Framework Core Commands

#### Installation & Setup
```
git clone https://github.com/volatilityfoundation/volatility
cd volatility
python setup.py install
```

#### Basic Usage Pattern
```
python vol.py -f <memory.dmp> --profile=<PROFILE> <plugin>
```

#### Process Analysis Plugins
- **pslist** — Walk the doubly-linked list of _EPROCESS structures
- **pstree** — Parent/child process tree view
- **psscan** — Pool tag scanning for _EPROCESS (finds unlinked/hidden processes)
- **psxview** — Cross-view: compare pslist, psscan, thrdproc, pspcid, csrss, session, deskthrd
- **cmdline** / **CmdScan** — Recover process command line arguments
- **consoles** — Extract console command history (cmd.exe)

#### DLL & Module Analysis
- **dlllist** — List loaded DLLs per process (walk PEB Ldr data)
- **dlldump** — Extract DLLs from process memory
- **ldrmodules** — Cross-reference DLL lists from InLoadOrder, InInitOrder, InMemOrder (detect hidden DLLs)
- **moddump** — Dump kernel drivers
- **modules** / **modscan** — List kernel modules (linked list + pool scanning)

#### Memory Mapping & Extraction
- **memmap** — List virtual-to-physical address mappings per process
- **memdump** — Dump all addressable process memory to file
- **procdump** — Reconstruct process executable from memory
- **dumpfiles** — Extract cached files from memory (VAD-based)
- **vadinfo** / **vadtree** — Examine Virtual Address Descriptors
- **malfind** — Find hidden/injected code (VAD tag: VadS, PAGE_EXECUTE_READWRITE)

#### Registry Analysis
- **hivelist** — Locate registry hives in memory
- **hivedump** — Recursively list all keys/values in a hive
- **printkey** — Display specific registry key and subkeys
- **hashdump** — Extract password hashes from SAM
- **lsadump** — Extract LSA secrets
- **userassist** — Parse UserAssist keys (execution evidence)
- **shellbags** — Parse ShellBags (directory browsing history)
- **shimcache** / **appcompatcache** — Application compatibility cache (execution evidence)

#### Network Artifacts
- **connections** — TCP connections (XP/2003, from tcpip.sys)
- **connscan** — Pool scan for _TCPT_OBJECT (TCP endpoints)
- **sockets** — Open socket objects
- **sockscan** — Pool scan for _ADDRESS_OBJECT
- **netscan** — Network connections (Vista+, uses partition tables/bitmaps)
- **ethscan** — Hidden network connections via netstat technique

#### Malware Detection Plugins
- **malfind** — Detect injected code/DLLs based on VAD tags and permissions
- **apihooks** — Detect IAT/EAT/inline API hooks in processes/kernel
- **callbacks** — Enumerate kernel callbacks (PsSetCreateProcessNotifyRoutine, etc.)
- **driverirp** — Audit driver IRP function tables for hooks
- **devicetree** — Display driver device stack (detect filter drivers)
- **ssdt** — Display System Service Descriptor Table entries (detect SSDT hooks)
- **idt** — Display Interrupt Descriptor Table (detect IDT hooks)
- **gdt** — Display Global Descriptor Table
- **threads** — Enumerate threads, detect orphaned threads in kernel
- **timers** — Enumerate kernel timers (malware persistence)
- **mutantscan** — Pool scan for mutant objects (malware named mutexes)
- **filescan** — Pool scan for _FILE_OBJECT (hidden files)
- **driverscan** — Pool scan for _DRIVER_OBJECT (hidden drivers)
- **deskscan** — Pool scan for desktop objects
- **atoms** / **atomscan** — Global atom table enumeration
- **clipboard** — Extract clipboard contents
- **eventhooks** — Detect Windows event hooks (SetWinEventHook)
- **messagehooks** — Detect Windows message hooks (keyloggers)
- **iehistory** — Recover Internet Explorer browsing history

#### Event Logs & Timeline
- **evtlogs** — Extract Windows event logs from memory
- **timeliner** — Generate timeline from multiple memory artifacts
- **mftparser** — Parse MFT entries from memory
- **strings** — Extract ASCII/Unicode strings (per-process via **volshell**)

#### Linux-Specific Plugins
- **linux_pslist** / **linux_pstree** — Process listing
- **linux_psxview** — Cross-view process detection
- **linux_proc_maps** — Process memory maps
- **linux_bash** — Recover bash command history
- **linux_bash_hash** — Recover bash hash table
- **linux_lsof** — List open file handles
- **linux_netstat** — Network connections
- **linux_arp** — ARP cache
- **linux_ifconfig** — Network interfaces
- **linux_route_cache** — Route cache
- **linux_pkt_queues** — Queued network packets
- **linux_lsmod** — Loaded kernel modules
- **linux_check_syscall** — Audit system call table for hooks
- **linux_check_fop** — Check file operation hooks
- **linux_check_tty** — Check TTY handler hooks
- **linux_keyboard_notifier** — Keyboard notifier hooks
- **linux_netfilter** — Netfilter hooks
- **linux_hidden_modules** — Detect hidden kernel modules
- **linux_check_inline_kernel** — Inline hook detection
- **linux_plthook** — PLT/GOT hook detection
- **linux_malfind** — Process hollowing/injection detection
- **linux_recover_filesystem** — Recover files from memory
- **linux_find_file** — Locate files in page cache
- **linux_dentry_cache** — Walk dentry cache
- **linux_dmesg** — Kernel debug buffer
- **linux_mount** — Mounted filesystems
- **linux_enumerate_files** — Enumerate open files

#### Mac-Specific Plugins
- **mac_pslist** / **mac_pstree** — Process listing
- **mac_psxview** — Cross-view process detection
- **mac_proc_maps** — Process memory maps
- **mac_dyld_maps** — dyld shared cache mappings
- **mac_dump_maps** — Dump process memory mappings
- **mac_netstat** / **mac_lsof** — Network/file handle info
- **mac_ifconfig** — Network interfaces
- **mac_arp** — ARP cache
- **mac_list_files** — Enumerate file descriptors
- **mac_check_syscalls** — Audit syscall table
- **mac_check_trap_table** — Audit Mach trap table
- **mac_apihooks** — API hook detection
- **mac_ip_filters** — IP filter hooks
- **mac_keychaindump** — Extract keychain entries
- **mac_bash** / **mac_bash_hash** — Bash history analysis
- **mac_dmesg** — Kernel debug buffer
- **mac_dead_procs** / **mac_dead_sockets** — Recover terminated resources

### 1.2 Memory Acquisition Tools & Formats

#### Acquisition Tools
- **WinPmem** / **winpmem** — Windows physical memory acquisition
- **OSXPmem** — Mac OS X memory acquisition
- **LiME** (Linux Memory Extractor) — Loadable kernel module, writes to disk or TCP
- **fmem** — Linux kernel module creating /dev/fmem
- **MoonSols Windows Memory Toolkit** — Win64dd, Win32dd
- **FTK Imager** — GUI + CLI memory capture
- **Mandiant Memoryze** — Agent-based memory acquisition
- **DumpIt** — Simple single-binary Windows memory dumper
- **Belkasoft Live RAM Capturer** — Windows memory acquisition
- **F-Response** — Remote read-only access to physical memory
- **Goldfish** — Mac OS X FireWire-based acquisition
- **Mac Memory Reader (MMR)** — Mac acquisition via FireWire

#### Dump Formats
- **Raw** — Most universal format, no headers/metadata
- **Windows Crash Dump** — _DMP_HEADER with PAGEDUMP/PAGEDU64 signature
- **Windows Hibernation File** (hiberfil.sys) — PO_MEMORY_IMAGE header, compressed
- **EWF (Expert Witness)** — EnCase format, requires libewf
- **HPAK** — HBGary format (physical + pagefile), HPAK magic signature
- **VMware** — .vmem (raw), .vmsn/.vmss (metadata, _VMWARE_HEADER 0xbed2bed0)
- **VirtualBox** — ELF64 core dump, PT_NOTE name VBCORE
- **QEMU** — ELF64 core dump, PT_NOTE name CORE

#### Conversion Tools
- **Volatility imagecopy** — Convert any supported format to raw
- **Volatility raw2dmp** — Convert raw to Windows crash dump
- **MoonSols MWMT** — Convert hibernation/crash dump to raw
- **VMware vmss2core** — Convert VMware saved state to crash dump

### 1.3 Key Forensic Artifacts in Memory

- **_EPROCESS** — Process structure (PID, PPID, create/exit time, token, VAD root)
- **PEB** — Process Environment Block (ImageBaseAddress, Ldr, ProcessParameters, command line)
- **VAD tree** — Virtual Address Descriptors (mapped files, injected regions)
- **Master File Table (MFT)** — NTFS metadata resident in memory
- **Registry hives** — SYSTEM, SOFTWARE, SAM, SECURITY, NTUSER.DAT cached in memory
- **Password hashes** — NTLM/LM hashes from SAM, cached credentials
- **LSA secrets** — Service account passwords, last logged on user
- **Network connections** — _TCPT_OBJECT, _ADDRESS_OBJECT, partition tables
- **DNS cache** — Resolved DNS queries in svchost.exe memory
- **Internet history** — IE history in process memory (index.dat equivalents)
- **Clipboard contents** — User clipboard data
- **TrueCrypt keys** — Encryption keys in driver device extension
- **Console history** — cmd.exe command buffers (CommandHistory)

### 1.4 Malware Injection Detection Patterns

| Technique | Volatility Detection |
|-----------|---------------------|
| DLL Injection (CreateRemoteThread) | malfind, dlllist, ldrmodules |
| Reflective DLL Injection | malfind (VAD with PAGE_EXECUTE_READWRITE) |
| Process Hollowing | procdump (comparing disk vs memory image) |
| PE Injection | malfind (PE headers in unexpected regions) |
| IAT Hooking | apihooks |
| EAT Hooking | apihooks |
| Inline Hooking | apihooks, disassembly in volshell |
| SSDT Hooking | ssdt |
| IRP Hooking | driverirp |
| IDT Hooking | idt |
| Kernel Callbacks | callbacks |
| DKOM (Direct Kernel Object Manipulation) | psxview, driverscan, modscan |
| Layered Filter Drivers | devicetree |

### 1.5 YARA Rule Integration

```
# Scan process memory with YARA
python vol.py -f memory.dmp --profile=Win7SP1x64 yarascan -p <PID> -y <rule.yar>

# Scan kernel memory with YARA
python vol.py -f memory.dmp --profile=Win7SP1x64 yarascan -K -y <rule.yar>
```

---

## 2. NETWORK FORENSICS (Network Forensics 2012)

### 2.1 OSCAR Investigation Methodology

1. **Obtain Information** — Incident details, environment, network topology, legal issues
2. **Strategize** — Assess resources, prioritize evidence, plan acquisition
3. **Collect Evidence** — Document, capture, store/transport, maintain chain of custody
4. **Analyze** — Correlation, timelines, events of interest, corroboration, interpretation
5. **Report** — Understandable by laypeople, defensible in detail, factual

### 2.2 Sources of Network-Based Evidence

| Source | Evidence Type |
|--------|---------------|
| Physical cabling | Taps (vampire, fiber, infrastructure) for traffic interception |
| Wireless (RF) | Management/control frames, MAC addresses, signal strength, WEP/WPA cracking |
| Switches | CAM tables (MAC-to-port mappings), SPAN/mirror ports |
| Routers | Routing tables, packet filter logs, NetFlow/IPFIX/sFlow export |
| DHCP Servers | IP-to-MAC lease logs with timestamps |
| DNS Servers | Query logs (timeline building, C2 identification) |
| Authentication Servers | Login success/failure logs, brute force detection |
| NIDS/NIPS | Alert data (Snort, Suricata), captured packet logs |
| Firewalls | ACL logs, denied/allowed traffic records |
| Web Proxies | Access logs, cached web objects, URL history |
| Application Servers | Server logs (web, mail, FTP, SSH, database) |
| Central Log Servers | Aggregated syslog, Windows Event Forwarding |

### 2.3 Evidence Collection Best Practices

- Acquire as soon as possible, lawfully
- Make cryptographically verifiable copies
- Sequester originals under restricted custody
- Analyze only copies
- Use reputable, reliable tools
- Document everything (date, time, source, method, investigator, chain of custody)

### 2.4 Packet Analysis Techniques

#### Protocol Identification Methods
1. Search for common binary/hex/ASCII values (e.g., 0x4500 = IPv4)
2. Leverage encapsulating protocol info (IP Protocol field, TCP/UDP port)
3. Analyze server function by IP/hostname
4. Test for recognizable protocol structures

#### Protocol Decoding
- Leverage automated decoders (Wireshark, tshark, tcpdump)
- Reference public documentation (RFCs, IANA)
- Write custom dissectors (Lua plugins)

#### Field Export
```
# tshark field extraction
tshark -r capture.pcap -T fields -e frame.number -e ip.addr -e udp

# PDML output
tshark -r capture.pcap -T pdml

# Custom Lua dissector
tshark -r capture.pcap -X lua_script:oft-dissector.lua -R "oft"
```

#### Flow Analysis
- Argus (ra client) for session/flow records
- NetFlow v5/v9, IPFIX, sFlow
- Flow record tools: SiLK, nfdump, flow-tools

#### Higher-Layer Analysis
- SMTP header analysis (Received chains, Message-ID, DKIM, SPF)
- HTTP request/response analysis (methods, status codes, User-Agent)
- OSCAR/AIM protocol analysis (OFT file transfers)
- File carving from TCP streams (HTTP attachments, FTP transfers)
- Email attachment extraction and analysis

### 2.5 Statistical Flow Analysis Commands

```
# Argus basic queries
ra -z -nnr argus-file.ra - 'host 10.30.30.20 and not udp'
ra -z -nnr argus-file.ra -s stime saddr sport dir daddr dport spkts dpkts state - 'tcp'

# Detect port sweeps (sequential IPs, single port)
ra -z -nnr argus-file.ra - 'host 10.30.30.20 and synack'

# Detect port scans (single host, multiple ports)
ra -z -t 2011/04/27.13:03:49+2s -nnr argus-file.ra -s dport - 'host 10.30.30.20' | sort -u | wc -l
```

### 2.6 NIDS/NIPS — Snort Essentials

#### Snort Architecture
```
# Test configuration
snort -T -c /etc/snort/snort.conf

# Run in IDS mode
snort -c snort.conf -i eth0 -A console

# Replay pcap through rules
snort -r capture.pcap -c snort.conf
```

#### Snort Rule Structure
```
alert tcp $EXTERNAL_NET any -> $HOME_NET 80 (msg:"WEB-ATTACKS"; flow:to_server,established; content:"union select"; sid:1000001;)
```

#### Snort Detection Modes
- Signature-based analysis (rule matching)
- Protocol awareness (anomaly detection in protocol fields)
- Behavioral analysis (threshold-based, statistical)
- Preprocessors: frag3, stream5, http_inspect, sfPortscan

### 2.7 Event Log Analysis

#### Windows Event Logs
- Application, Security, System, Setup, ForwardedEvents
- Event IDs: 4624 (logon), 4625 (failed logon), 4688 (process creation), 5140 (share access)
- **auditpol** — Configure audit policy
- **wevtutil** — Query/manage event logs
- **Get-EventLog** / **Get-WinEvent** — PowerShell log queries
- Windows Eventing 6.0 (Vista+): XML format, WS-Management/WinRM, subscription-based forwarding

#### Linux Logs
- /var/log/auth.log — Authentication events
- /var/log/syslog — System events
- /var/log/apache2/access.log — Web server access

### 2.8 Web Proxy Analysis

#### Squid Proxy
- Access log format: timestamp, duration, client IP, result code, bytes, method, URL, user, hierarchy, type
- Cache directory structure: L1/L2 hex-digit directories
- Web object extraction: find CRLF-CRLF (0x0D0A0D0A) marker, carve HTTP body

#### Analysis Tools
- Squidview — Interactive access log viewer
- SARG — Squid Analysis Report Generator
- Splunk — Log aggregation and analysis
- Shell tools: grep, awk, sort, uniq

---

## 3. NETWORK SECURITY MONITORING (The Practice of NSM)

### 3.1 NSM Data Types

| Data Type | Description | Tools |
|-----------|-------------|-------|
| **Full Content** | Complete packet captures (pcap) | netsniff-ng, dumpcap, tcpdump |
| **Extracted Content** | Files, images, objects carved from traffic | Bro, Xplico, NetworkMiner |
| **Session Data** | Call details: who, when, how, how much | Argus, SANCP, Sguil |
| **Transaction Data** | Protocol-specific request/reply details | Bro HTTP/DNS/SSL logs |
| **Statistical Data** | Traffic summaries, protocol distributions | Capinfos, Wireshark stats |
| **Metadata** | IP/domain registration, routing, threat intel | WHOIS, Robtex, threat feeds |
| **Alert Data** | IDS-triggered events | Snort, Suricata, Sguil, Snorby |

### 3.2 Security Onion (SO) Architecture

#### Core Components
- **Collection**: netsniff-ng (full packet capture), dumpcap, tcpdump
- **IDS engines**: Snort or Suricata (alert data)
- **Session data**: Argus, PRADS, SANCP
- **Transaction data**: Bro (conn.log, dns.log, http.log, ssh.log, ftp.log, ssl.log)
- **HIDS**: OSSEC
- **Consoles**: Sguil, Squert, Snorby, ELSA
- **Delivery**: barnyard2 (Snort unified2 -> database)
- **Transport**: autossh tunnels for sensor-to-server

#### Installation Options
- Stand-alone: single system (server + sensor on one box)
- Distributed: SO server + SO sensor(s), connected via autossh tunnels
- ISO-based or PPA-based (Ubuntu Server + SO packages)

#### Key Ports (SO Firewall)
- 22/tcp — OpenSSH
- 514 — Syslog
- 1514/udp — OSSEC
- 443/tcp — Apache (Snorby, Squert)
- 444/tcp — Snorby
- 7734/tcp — Sguil client
- 7736/tcp — Sguil agents
- 3154/tcp — ELSA

#### SO Scripts
- **/usr/sbin/nsm** — High-level NSM control (status, start, stop, restart)
- **/usr/sbin/nsm_all_del** — Delete all NSM data/configuration
- **/usr/sbin/nsm_sensor_clean** — Auto-clean when disk >90% (hourly cron)
- **/usr/sbin/nsm_sensor_ps-daily-restart** — Daily restart at midnight
- **sudo sosetup** — Setup wizard
- **sudo service nsm status** — Check NSM application status

#### Data Locations
- /nsm/sensor_data/<sensor>/dailylogs/YYYY-MM-DD/snort.log.<timestamp> (pcap format)
- /var/lib/mysql — Sguil database
- /nsm/bro/logs/ — Bro logs (conn, dns, http, ssh, ssl, etc.)

### 3.3 NSM Operations Process

**Collection -> Analysis -> Escalation -> Resolution**

#### Analysis Workflow
1. Start with **alert data** (Sguil/Snorby) for initial triage
2. Query **session data** (SANCP/Argus) for connection context
3. Review **transaction data** (Bro logs) for protocol details
4. Inspect **full content** (Wireshark/tshark) for granular analysis
5. Build **timeline** of events
6. **Corroborate** across multiple data sources
7. **Report** findings

#### Enterprise Security Cycle
- **Planning**: asset identification, threat modeling, sensor placement
- **Resistance**: hardening, patching, policy enforcement
- **Detection**: NSM data collection and analysis
- **Response**: containment, eradication, recovery

### 3.4 Command-Line Packet Analysis Tools

#### tcpdump
```
# Basic capture with ASCII display
tcpdump -n -A -r capture.pcap

# BPF filter examples
tcpdump -r capture.pcap 'host 192.168.1.1 and port 80'
tcpdump -r capture.pcap 'net 10.0.0.0/24'
tcpdump -w capture.pcap -i eth0 -c 1000
```

#### tshark
```
# Read pcap with display filter
tshark -r capture.pcap -R 'ip.addr==192.168.1.1'

# Field extraction
tshark -r capture.pcap -T fields -e frame.number -e ip.addr -e tcp.port

# Decode-As
tshark -r capture.pcap -d tcp.port==29008,http
```

#### Argus
```
# Examine session data
ra -z -nnr argus-file.ra

# Filter for specific host/port
ra -z -nnr argus-file.ra - 'host 10.0.0.5 and port 80'
```

### 3.5 Bro/Zeek Log Analysis

#### Key Bro Logs
- **conn.log** — Connection summary (src, dst, proto, service, duration, bytes)
- **dns.log** — DNS queries and replies
- **http.log** — HTTP requests (method, host, URI, user-agent, status, MIME type)
- **ssh.log** — SSH connections (client/server versions, auth status)
- **ssl.log** — SSL/TLS sessions (certificates, cipher suites)
- **ftp.log** — FTP commands and responses
- **files.log** — File transfers detected by Bro

#### Bro Log Querying
```
# Search compressed Bro logs
zcat dns.*.log.gz | bro-cut -d | grep <query>
zcat ssh.*.log.gz | bro-cut -d ts id.orig_h id.resp_h status client server
```

### 3.6 NIDS Tuning

- Start with Snort default rules, review alert frequency
- Tune by disabling noisy rules for known-benign traffic
- Use threshold.conf for rate-based suppression
- Regularly review and adjust based on network changes

---

## 4. PACKET ANALYSIS WITH WIRESHARK

### 4.1 Wireshark Capture Setup

#### Prerequisites
- Linux: kernel packet socket support (default)
- Windows: WinPcap/Npcap installed
- Promiscuous mode for full segment visibility
- Monitor mode for Wi-Fi captures

#### Capture Interfaces
```
eth0 — Ethernet
lo0 — Loopback
wlan0 — Wi-Fi (set monitor mode for 802.11 capture)
any — All interfaces (Linux)
```

#### Capture Options
- **Snaplength**: limit bytes per frame (snaplength=0 for full capture)
- **Promiscuous mode**: receive all packets on segment
- **Name Resolution**: MAC, network (DNS), transport (port names)
- **Capture Filter (BPF)**: pre-filter packets (`tcp port 80`, `host 192.168.1.1`)
- **Auto-capture**: rotating files by time or size

### 4.2 Wireshark Display Filters

#### Core Filter Syntax
```
ip.src == 10.0.0.1
ip.dst == 10.0.0.2
ip.addr == 192.168.1.1          # matches source or destination

tcp.port == 443
tcp.srcport == 2222
tcp.flags.syn == 1

http
http.request.method == "GET"
http.response.code == 200

dns
dns.qry.name == "example.com"
dns.qry.type == 1               # A record
dns.qry.type == 28              # AAAA record

ssl.record.content_type == 22   # Handshake
ssl.handshake.type == 1         # Client Hello
ssl.handshake.type == 2         # Server Hello
ssl.record.content_type == 24   # Heartbeat

eth.dst == ff:ff:ff:ff:ff:ff    # Broadcast
!arp                            # Exclude ARP
tcp.analysis.retransmission
tcp.analysis.duplicate_ack
tcp.analysis.zero_window
```

#### Compound Filters
```
(http.request.method == "GET") && (http.request.uri contains "login")
tcp.flags.syn == 1 && tcp.flags.ack == 0    # SYN only
ip.src == 10.0.0.0/24 && tcp.port == 3389   # RDP from subnet
tcp.flags == 0x0011                          # FIN+ACK
tcp.window_size < 2000
(http || dns) && !arp
```

### 4.3 Wireshark Features

#### Analysis Tools
- **Follow TCP Stream** — Right-click -> Follow -> TCP Stream
- **IO Graph** — Statistics -> IO Graph (throughput visualization)
- **Protocol Hierarchy** — Statistics -> Protocol Hierarchy
- **Endpoints** — Statistics -> Endpoints (top talkers)
- **Conversations** — Statistics -> Conversations (flow analysis)
- **Decode-As** — Analyze -> Decode As (override protocol detection)
- **Export Objects** — File -> Export Objects -> HTTP (extract files)
- **Firewall ACL Rules** — Tools -> Firewall ACL Rules
- **Coloring Rules** — View -> Coloring Rules (visual triage)

#### TCP Sequence Analysis Flags
- **TCP Retransmission** — Packet retransmitted (timer expired)
- **TCP Fast Retransmission** — Retransmission triggered by duplicate ACKs
- **TCP Dup-ACK** — Duplicate acknowledgment
- **TCP ZeroWindow** — Receiver buffer full (tcp.window_size == 0)
- **TCP Window Update** — Window size changed (ACK with new window)
- **TCP Keep-Alive** — Keep-alive probe
- **TCP Previous segment not captured** — Sequence gap

### 4.4 TCP Troubleshooting

#### CLOSE_WAIT
- Server sent FIN, client ACKed but didn't close its socket
- Indicates application bug (never calls close())
- Detect: `netstat -an | grep CLOSE_WAIT`
- Fix: ensure socket.close() is called

#### TIME_WAIT
- Active close side lingers for 2*MSL (typically 60s on Linux)
- `/proc/sys/net/ipv4/tcp_fin_timeout`
- Normal behavior; high count may indicate excessive short-lived connections

#### Latency Diagnosis
- **Ping** — RTT measurement
- **Traceroute** — hop count analysis
- **Wireshark HTTP response time**: add `http.time` column
- **TCP window size**: check `tcp.window_size_value`, ensure large values
- **Server latency vs wire latency**: compare handshake timing vs data transfer timing

#### SYN Flood Detection
- High count of SYN without corresponding ACK or data
- IO Graph: compare `tcp.flags.syn` count vs `tcp.flags.ack`
- Mitigation: SYN cookies, iptables rate limiting, ACL blocks

### 4.5 SSL/TLS Analysis

#### Handshake Message Types
| Type | Name | Wireshark Filter |
|------|------|-----------------|
| 1 | Client Hello | ssl.handshake.type == 1 |
| 2 | Server Hello | ssl.handshake.type == 2 |
| 11 | Certificate | ssl.handshake.type == 11 |
| 12 | Server Key Exchange | ssl.handshake.type == 12 |
| 13 | Certificate Request | ssl.handshake.type == 13 |
| 14 | Server Hello Done | ssl.handshake.type == 14 |
| 15 | Certificate Verify | ssl.handshake.type == 15 |
| 16 | Client Key Exchange | ssl.handshake.type == 16 |
| 20 | Finished | ssl.handshake.type == 20 |

#### Record Content Types
- 20 = ChangeCipherSpec
- 21 = Alert
- 22 = Handshake
- 23 = Application Data
- 24 = Heartbeat (Heartbleed: ssl.record.content_type == 24)

#### SSL Decryption
- RSA key exchange: Edit -> Preferences -> Protocols -> SSL -> RSA keys list (server private key + IP + port)
- Export SSL session keys (pre-master secret log)
- DHE/ECDHE: forward secrecy prevents passive decryption

#### SSL Debugging
```
# Check server SSL configuration
nmap --script ssl-cert,ssl-enum-ciphers -p 443 <target>

# Verify certificate chain
openssl verify -verbose -CAfile cacert.pem server.crt
openssl x509 -text -in server.crt

# Match modulus (same key for cert + private key)
openssl x509 -noout -modulus -in server.crt | openssl md5
openssl rsa -noout -modulus -in server.key | openssl md5
```

### 4.6 Application Layer Protocol Filters

#### DHCPv6
- Filter: `dhcpv6`
- Message types: SOLICIT(1), ADVERTISE(2), REQUEST(3), CONFIRM(4), RENEW(5), REBIND(6), REPLY(7), RELEASE(8), DECLINE(9)
- Four-message exchange (SARR): SOLICIT -> ADVERTISE -> REQUEST -> REPLY
- Two-message exchange: Rapid Commit option in SOLICIT
- Capture: `tcpdump -i any ip6 -vv -w dhcpv6.pcap -s0`
- Simulate: `dhclient -6 eth0`

#### DHCPv4 (BOOTP)
- Filter: `bootp`
- DORA exchange: DISCOVER -> OFFER -> REQUEST -> ACK
- `bootp.option.dhcp == 1` (DISCOVER), `bootp.option.dhcp == 2` (OFFER)
- Capture: `tcpdump udp port 67`

#### DNS
- Filter: `dns`
- Query types: A(1), NS(2), CNAME(5), SOA(6), PTR(12), MX(15), TXT(16), AAAA(28), AXFR(252), ANY(255)
- Query utilities: `dig`, `nslookup`

#### HTTP
- Filter: `http`
- `http.request.method == "GET"`, `http.response.code == 200`
- Form post password detection: look in Packet Bytes pane for POST body
- Top response time: add `http.time` column, sort descending

### 4.7 WLAN (802.11) Analysis

#### Frame Types
- Management (type 0): beacon(8), probe request(4), probe response(5), authentication(11), deauthentication(12), association(0), disassociation(10)
- Control (type 1): RTS(1b), CTS(1c), ACK(1d), PS-Poll(1a)
- Data (type 2): Data(20), QoS Data(28), Null(24)
- Display filter: `wlan.fc.type == 0` (management), `wlan.fc.type_subtype == 0x08` (beacon)

#### Key WLAN Filters
```
wlan_mgt.ssid == "MyNetwork"
wlan.fc.type_subtype == 0x08           # Beacon frames
wlan.fc.type_subtype == 0x04           # Probe requests
wlan.fc.type_subtype == 0x0c           # Deauthentication
wlan.fc.type_subtype == 0x0b           # Authentication
eapol                                    # EAPOL messages
wlan.da == fc:db:b3:1e:df:dd           # Filter by MAC
```

#### 802.1X EAPOL
- 4-way handshake (1 of 4, 2 of 4, 3 of 4, 4 of 4)
- WPA/WPA2 decryption: Edit -> Preferences -> IEEE 802.11 -> Decryption keys

### 4.8 Security Analysis with Wireshark

#### Heartbleed Detection (CVE-2014-0160)
- Filter: `ssl.record.content_type == 24`
- Heartbeat Request length < Heartbeat Response length indicates bleed
- Affected: OpenSSL 1.0.1 through 1.0.1f

#### DoS/DDoS Detection
- **SYN flood**: IO graph on tcp.flags.syn vs tcp.flags.ack (high SYN:ACK ratio)
- **ICMP flood**: IO graph on icmp (massive echo requests, no echo replies)
- **SSL flood**: Conversations -> high packet counts from single IP
- **DrDoS**: UDP amplification, spoofed source IP, small request -> large response

#### ARP Duplicate IP Detection (MITM)
- Filter: `arp.duplicate-address-frame`
- Same MAC claiming multiple IPs = ARP poisoning

#### Port Scanning Detection
- Host scan pattern: sequential or random ports from one source
- Nmap detection: SYN packets to 1000 common ports
- Examine: fast SYN packets without completing handshake

### 4.9 Alternative Packet Tools

| Tool | Purpose |
|------|---------|
| **Scapy** | Packet crafting, editing, replay, MITM |
| **Ettercap** | ARP spoofing, MITM, password sniffing |
| **Tcpreplay** | Packet replay for testing |
| **Snort** | IDS/IPS (signature-based detection) |
| **Cain** | ARP spoofing, password cracking (Windows) |
| **Kismet** | Wireless network detector/sniffer |
| **Riverbed AirPcap** | Commercial 802.11 capture adapter |
| **AirPcap** | Wireshark-integrated wireless capture |
| **tcpdump** | CLI packet capture (Linux/Unix standard) |
| **snoop** | CLI packet capture (Solaris standard) |
| **dumpcap** | Wireshark's capture engine (CLI only) |

---

## 5. BLUE TEAM FIELD MANUAL (BTFM)

### 5.1 Windows Hardening Commands

#### Registry Hardening
```
# Disable Remote Desktop
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /f /v fDenyTSConnections /t REG_DWORD /d 1

# Send NTLMv2 only, refuse LM and NTLM
reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa\ /v lmcompatibilitylevel /t REG_DWORD /d 5 /f

# Restrict anonymous access
reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v restrictanonymous /t REG_DWORD /d 1 /f

# Remove pass-the-hash hashes (requires password reset + reboot)
reg add HKLM\SYSTEM\CurrentControlSet\Control\Lsa /f /v NoLMHash /t REG_DWORD /d 1

# Disable administrative shares (Workstation)
reg add HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /f /v AutoShareWks /t REG_DWORD /d 0

# Require UAC
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 1 /f
```

#### Audit Policy (auditpol)
```
# Enable all categories success/failure
auditpol /set /category:* /success:enable /failure:enable

# Enable key subcategories
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Process Creation" /success:enable /failure:enable
auditpol /set /subcategory:"File System" /success:enable /failure:enable
auditpol /set /subcategory:"Registry" /success:enable /failure:enable
auditpol /set /subcategory:"Sensitive Privilege Use" /success:enable /failure:enable
```

#### Firewall (netsh / iptables)
```
# Enable firewall logging
netsh firewall set logging droppedpackets connections = enable

# Windows Firewall block incoming IP
netsh advfirewall firewall add rule name="Block Bad IP" dir=in remoteip=<BAD IP> action=block
```

### 5.2 Linux Hardening Commands

#### Services
```
# List services
service --status-all
ps -ef

# Disable service
update-rc.d <service> disable
service <service> stop

# List upstart jobs
initctl list
```

#### iptables
```
# Save/restore rules
iptables-save > firewall.out
iptables-restore < firewall.out

# Block IP/range
iptables -A INPUT -s 10.10.10.10 -j DROP
iptables -A INPUT -s 10.10.10.0/24 -j DROP

# Log denied packets
iptables -I INPUT 5 -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7

# Flush all rules
iptables -F
```

#### ufw (Uncomplicated Firewall)
```
ufw enable
ufw logging on
ufw allow 80/tcp
ufw deny from <BAD IP>
ufw status verbose
```

#### SYN Flood Mitigation (sysctl.conf)
```
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.tcp_max_tw_buckets = 1440000
net.ipv4.icmp_echo_ignore_all = 1
```

### 5.3 Linux Live Triage Commands

#### System Information
```
uname -a
uptime
timedatectl
mount
df -ah
```

#### User Investigation
```
# Current users
w

# Login history
lastlog
last
faillog -a

# Accounts with UID 0
awk -F: '($3 == "0") {print}' /etc/passwd

# Sudo access
cat /etc/sudoers

# Bash history
cat /root/.bash_history
```

#### Network Investigation
```
netstat -antup           # All connections with processes
netstat -nap             # Listening ports
lsof -i                  # Processes with network connections
arp -a                   # ARP cache
route                    # Routing table
```

#### Process Investigation
```
ps -aux                  # All processes
lsmod                    # Loaded kernel modules
lsof                     # Open files
lsof +L1                 # Unlinked processes (possible malware)
cat /proc/<PID>/exe > /tmp/suspicious.elf
```

#### Malware Scanning
```
# Rootkit scanners
chkrootkit
rkhunter --check

# System auditing
lynis audit system
tiger

# Malware detection
maldet -a /home/
```

### 5.4 Windows Live Triage Commands

#### System Information
```
systeminfo
hostname
echo %DATE% %TIME%
wmic csproduct get name
```

#### User Investigation
```
whoami
net users
net localgroup administrators
wmic useraccount list
doskey /history > history.txt
```

#### Network Investigation
```
netstat -naob          # All connections with process IDs
netstat -nr            # Routing table
arp -a                 # ARP cache
ipconfig /displaydns   # DNS cache
netsh wlan show all
```

#### Process/Services
```
tasklist /SVC
sc query
wmic process list brief
schtasks               # Scheduled tasks
```

#### Autorun Investigation
```
autorunsc -accepteula -m         # Hide Microsoft-signed
autorunsc -accepteula -a -c -i -e -f -l -m -v  # Full export to CSV
```

#### Log Collection
```
# Export event logs
wevtutil epl Security C:\backup\security.evtx
wevtutil epl System C:\backup\system.evtx
wevtutil epl Application C:\backup\application.evtx

# Check audit policy
auditpol /get /category:*
```

### 5.5 Network Monitoring (Linux)

#### tcpdump (BTFM)
```
# ASCII/HEX viewing
tcpdump -A
tcpdump -X

# Verbose with timestamps
tcpdump -tttt -n -vv

# Capture between hosts
tcpdump host 10.0.0.1 && host 10.0.0.2

# Rotating captures
tcpdump -pni any -s65535 -G 3600 -w any%Y-%m-%d_%H:%M:%S.pcap

# Grab cleartext passwords
tcpdump -n -A -s0 port http or port ftp or port smtp or port imap or port pop3 | egrep -i 'pass=|pwd=|login=|user='

# SSL certificate inspection
tcpdump -s 1500 -A '(tcp[((tcp[12:1] & 0xf0) >> 2)+5:1] = 0x01) and (tcp[((tcp[12:1] & 0xf0) >> 2):1] = 0x16)'

# Throughput measurement
tcpdump -w - | pv -bert > /dev/null
```

#### tshark (BTFM)
```
# Top talkers
tshark -n -c 150 | awk '{print $4}' | sort -n | uniq -c | sort -nr

# Protocol hierarchy
tshark -q -z io,phs -r capture.pcap

# Extract HTTP host + URI
tshark -R http.request -T fields -E separator=';' -e http.host -e http.request.uri

# DNS queries
tshark -n -e ip.src -e dns.qry.name -E separator=';' -T fields port 53

# Grab src/dst IPs
tshark -n -e ip.src -e ip.dst -T fields -E separator=, -R ip
```

### 5.6 Honey Techniques (BTFM)

#### Windows Honey Ports
```
# Create batch script to block scanners connecting on port 3333
echo @echo off for /L %%i in (1,1,1) do @for /f "tokens=3" %%j in ('netstat -nao ^| find ":3333"') do @for /f "tokens=1 delims=:" %%k in ("%%j") do netsh advfirewall firewall add rule name="HONEY TOKEN RULE" dir=in remoteip=%%k localport=any protocol=TCP action=block >> honey.bat
```

#### Linux Honey Ports
```
# Block any hosts connecting on port 2222
while [ 1 ]; do IP=`nc -v -l -p 2222 2>&1 > /dev/null | grep from | cut -d[ -f 3 | cut -d] -f 1`; iptables -A INPUT -p tcp -s ${IP} -j DROP; done

# Labrea tarpit for rogue scanning
labrea -z -s -o -b -v -i eth0 2>&1 | tee -a log.txt

# Netcat listeners
nc -v -k -l 80
nc -v -k -l 443
```

#### Passive DNS Monitoring
```
dnstop -l 3 eth0       # Live DNS monitoring (key '2' for query names)
dnstop -l 3 capture.pcap > dns_report.txt
```

#### Honey Hashes (Mimikatz Detection)
```
# Create fake admin process
runas /user:yourdomain.com\fakeadministratoraccount /netonly cmd.exe

# Query for remote access attempts (EventID 20274)
wevtutil qe System /q:"*[System[(EventID=20274)]]" /f:text /rd:true /c:1

# Query failed logins (EventID 4624/4625)
wevtutil qe Security /q:"*[System[(EventID=4624 or EventID=4625)]]" /f:text /rd:true /c:5
```

### 5.7 Malware Identification (Process Explorer Method)

1. Look for processes with: no icon, no description, unsigned, packed (purple in Process Explorer)
2. Add Verified Signer column, enable VirusTotal checking
3. Examine strings: right-click -> Properties -> Strings tab -> check for suspicious URLs
4. DLL view (Ctrl+D): look for unsigned DLLs, no description
5. Suspend -> Terminate suspicious processes
6. Clean Autoruns (verify code signatures, hide Microsoft entries, uncheck malicious entries)
7. Use Process Monitor for persistent malware

### 5.8 Memory & Disk Acquisition (BTFM)

#### Windows
```
# Remote memory dump via PsExec
psexec.exe \\<HOST> -u <DOMAIN>\<ADMIN> -p <PASS> -c mdd_1.3.exe -o C:\memory.dmp

# Volatility triage
python vol.py -f memory.dmp --profile=Win7SP1x64 pslist
python vol.py -f memory.dmp --profile=Win7SP1x64 malfind -D /output/

# Disk imaging (dc3dd)
dc3dd.exe if=\\.\c: of=D:\image.dd hash=md5 log=D:\image.log
```

#### Linux
```
# Memory dump (LiME)
insmod lime.ko "path=/media/usb/mem.lime format=raw"

# Process memory
cp /proc/<PID>/exe /save/location
gcore <PID>

# Disk imaging
dd if=/dev/sda | ssh user@remote "dd of=/backup/image.dd"
dc3dd if=/dev/sda of=/mnt/image.img hash=md5 log=/mnt/image.log
```

### 5.9 File Hash Analysis
```
# VirusTotal API
curl -v --request POST --url 'https://www.virustotal.com/vtapi/v2/file/report' -d apikey=<KEY> -d 'resource=<HASH>'
curl -v -F 'file=@/path/to/file' -F apikey=<KEY> https://www.virustotal.com/vtapi/v2/file/scan

# Team Cymru hash lookup
whois -h hash.cymru.com <HASH>
```

### 5.10 IPSEC Setup (Racoon)
```
# Install racoon
apt-get install racoon

# Configure /etc/racoon/racoon.conf with AES-256, SHA-256, DH group 2

# Pre-shared key
echo "<REMOTE_IP> <PRESHARED_PASSWORD>" >> /etc/racoon/psk.txt

# Restart
service setkey restart
setkey -D    # Verify security associations
```

---

## 6. IMMUTABLE SECURITY CONTROLS

### 6.1 Account Guardrails (AWS IAM Policies)

#### Region Restriction
```json
{
  "Effect": "Deny",
  "NotAction": ["iam:*", "organizations:*", "route53:*", "budgets:*", "waf:*", "cloudfront:*", "globalaccelerator:*", "importexport:*", "support:*", "health:*", "route53domains:*"],
  "Resource": "*",
  "Condition": {
    "StringNotEquals": { "aws:RequestedRegion": ["ap-south-1"] }
  }
}
```

#### Allow Only Required Services
Deny-wildcard with explicit Allow list of approved service prefixes.

#### Prevent Account/Billing Modification
Deny: `aws-portal:ModifyAccount`, `aws-portal:ModifyBilling`, `aws-portal:ModifyPaymentMethods`

#### Restrict Root User
Deny all actions with condition: `aws:PrincipalArn` contains `arn:aws:iam::*:root`

#### Deny IAM User/Access Key Creation
Deny: `iam:CreateAccessKey`, `iam:CreateUser`

#### Protect IAM Roles
Deny: `iam:AttachRolePolicy`, `iam:DeleteRole`, `iam:DeleteRolePolicy`, `iam:DetachRolePolicy`, `iam:UpdateRole`, `iam:UpdateAssumeRolePolicy`

#### Prevent Leaving AWS Organization
Deny: `organizations:LeaveOrganization`

### 6.2 Protecting Security Baseline

#### CloudTrail Protection
Deny: `cloudtrail:StopLogging`, `cloudtrail:DeleteTrail`

#### AWS Config Protection
Deny: `config:DeleteConfigRule`, `config:DeleteConfigurationRecorder`, `config:DeleteDeliveryChannel`, `config:StopConfigurationRecorder`

#### GuardDuty Protection
Deny: `guardduty:DeleteDetector`, `guardduty:DeleteInvitations`, `guardduty:DeleteIPSet`, `guardduty:DeleteMembers`, `guardduty:DeleteThreatIntelSet`, `guardduty:DisassociateFromMasterAccount`, `guardduty:StopMonitoringMembers`

#### CloudWatch Protection
Deny: `cloudwatch:DeleteAlarms`, `cloudwatch:DeleteDashboards`, `cloudwatch:DisableAlarmActions`, `cloudwatch:PutDashboard`, `cloudwatch:PutMetricAlarm`, `cloudwatch:SetAlarmState`

#### VPC Flow Logs Protection
Deny: `ec2:DeleteFlowLogs`, `logs:DeleteLogGroup`, `logs:DeleteLogStream`

#### Prevent Unauthorized Internet Access
Deny: `ec2:AttachInternetGateway`, `ec2:CreateInternetGateway`, `ec2:CreateVpcPeeringConnection`, `ec2:AcceptVpcPeeringConnection`

#### VPC Connectivity Protection
Deny all internet gateway, NAT gateway, VPN gateway, peering modifications

#### AWS Security Hub / Macie Protection
Deny: `securityhub:DeleteInvitations`, `securityhub:DisableSecurityHub`, `macie2:DisableMacie`

### 6.3 Data Guardrails

#### S3 Region Restriction
Deny `s3:CreateBucket` with condition on `s3:LocationConstraint`

#### S3 Deletion Prevention
Deny: `s3:DeleteBucket`, `s3:DeleteObject`, `s3:DeleteObjectVersion`

#### S3 Encryption Requirement
Deny `s3:PutObject` if `s3:x-amz-server-side-encryption` != AES256

#### S3 Public Access Block Protection
Deny: `s3:PutBucketPublicAccessBlock`

#### KMS Key Protection
Deny: `kms:ScheduleKeyDeletion`, `kms:Delete*`

### 6.4 EC2 Instance Controls

#### Instance Type Restriction
Deny `ec2:RunInstances` unless `ec2:InstanceType` matches allowed type

#### IMDSv2 Requirement
Deny `ec2:RunInstances` if `ec2:MetadataHttpTokens` != `required`
Deny `ec2:ModifyInstanceMetadataOptions`

#### MFA for Stop/Terminate
Deny `ec2:StopInstances`, `ec2:TerminateInstances` if `aws:MultiFactorAuthPresent` = false

#### EC2 Encryption Requirement
Deny `ec2:RunInstances` if `ec2:Encrypted` = false

---

## 7. CIS CONTROLS v7.1

### 7.1 Basic Controls (CIS 1-6)

#### CIS 1: Inventory and Control of Hardware Assets
- 1.1: Active discovery tool (scan network for devices)
- 1.2: Passive asset discovery (listen on network interfaces)
- 1.3: DHCP logging for asset inventory updates
- 1.4: Maintain detailed asset inventory (all IT assets)
- 1.5: Record network address, MAC, machine name, owner, department
- 1.6: Address unauthorized assets (remove, quarantine, or update inventory)
- 1.7: Port-level access control (802.1x, NAC)
- 1.8: Client certificates for hardware authentication

#### CIS 2: Inventory and Control of Software Assets
- 2.1: Maintain authorized software inventory
- 2.2: Ensure software is vendor-supported
- 2.3: Software inventory tools (automated)
- 2.4: Track: name, version, publisher, install date
- 2.5: Integrate software + hardware inventories
- 2.6: Address unapproved software
- 2.7: Application whitelisting
- 2.8: Whitelist libraries (*.dll, *.ocx, *.so)
- 2.9: Whitelist scripts (*.ps1, *.py, macros) — require digital signatures
- 2.10: Physically/logically segregate high-risk applications

#### CIS 3: Continuous Vulnerability Management
- 3.1: SCAP-compliant vulnerability scanning (weekly or more frequent)
- 3.2: Authenticated scanning (agents or credentialed remote scanners)
- 3.3: Dedicated assessment accounts (tied to specific machines)
- 3.4: Automated OS patch management
- 3.5: Automated third-party software patch management
- 3.6: Back-to-back scan comparison (verify remediation)
- 3.7: Risk-rating process for vulnerability prioritization

#### CIS 4: Controlled Use of Administrative Privileges
- 4.1: Inventory administrative accounts
- 4.2: Change default passwords before deployment
- 4.3: Dedicated secondary accounts for administrative activities
- 4.4: Unique passwords per system (when MFA unavailable)
- 4.5: Multi-factor authentication for all administrative access
- 4.6: Dedicated admin workstations (segmented, no Internet/email)
- 4.7: Limit access to scripting tools (PowerShell, Python)
- 4.8: Log/alert on admin group membership changes
- 4.9: Log/alert on unsuccessful admin logins

#### CIS 5: Secure Configuration for Hardware and Software
- 5.1: Documented security configuration standards
- 5.2: Maintain secure images/templates
- 5.3: Securely store master images (integrity monitoring)
- 5.4: System configuration management tools (automated enforcement)
- 5.5: SCAP-compliant configuration monitoring (detect unauthorized changes)

#### CIS 6: Maintenance, Monitoring and Analysis of Audit Logs
- 6.1: Three synchronized time sources (NTP)
- 6.2: Activate local logging on all systems/networking devices
- 6.3: Enable detailed logging (source, date, user, timestamp, addresses)
- 6.4: Adequate log storage
- 6.5: Central log management (aggregation)
- 6.6: Deploy SIEM or log analytic tools
- 6.7: Regular log review
- 6.8: Regular SIEM tuning

### 7.2 Foundational Controls (CIS 7-16)

#### CIS 7: Email and Web Browser Protections
- 7.1: Only fully supported browsers/email clients
- 7.2: Disable unauthorized browser/email plugins
- 7.3: Limit scripting languages in browsers/email
- 7.4: Network-based URL filters
- 7.5: URL categorization services (block uncategorized)
- 7.6: Log all URL requests
- 7.7: DNS filtering services
- 7.8: DMARC/DKIM/SPF implementation
- 7.9: Block unnecessary email attachment file types
- 7.10: Sandbox email attachments

#### CIS 8: Malware Defenses
- 8.1: Centrally managed anti-malware
- 8.2: Updated scanning engine and signatures
- 8.3: OS anti-exploitation: DEP, ASLR
- 8.4: Auto-scan removable media
- 8.5: Disable auto-run for removable media
- 8.6: Centralize anti-malware logging
- 8.7: DNS query logging
- 8.8: Command-line audit logging (PowerShell, Bash)

#### CIS 9: Limitation and Control of Network Ports, Protocols, Services
- 9.1: Associate active ports/services with asset inventory
- 9.2: Only approved ports/protocols/services running
- 9.3: Regular automated port scans
- 9.4: Host-based firewalls (default-deny)
- 9.5: Application firewalls in front of critical servers

#### CIS 10: Data Recovery Capabilities
- 10.1: Regular automated backups
- 10.2: Complete system backups (imaging)
- 10.3: Test data restoration
- 10.4: Protect backups (physical security or encryption)
- 10.5: At least one offline backup destination

#### CIS 11: Secure Configuration for Network Devices
- 11.1: Documented security standards for network devices
- 11.2: Document traffic rules with business justification
- 11.3: Automated verification of device configs
- 11.4: Latest stable security updates on network devices
- 11.5: MFA + encrypted sessions for network device management
- 11.6: Dedicated workstations for network admin tasks
- 11.7: Dedicated management network (separate VLANs or physical)

#### CIS 12: Boundary Defense
- 12.1: Inventory of network boundaries
- 12.2: Regular scans for unauthorized boundary connections
- 12.3: Deny known malicious IPs
- 12.4: Deny unauthorized ports
- 12.5: Record packets at boundaries
- 12.6: Network-based IDS at boundaries
- 12.7: Network-based IPS at boundaries
- 12.8: NetFlow collection on boundary devices
- 12.9: Application layer proxy (authenticated)
- 12.10: Decrypt traffic at proxy (with whitelist exceptions)
- 12.11: MFA for remote logins
- 12.12: Scan remote devices before network access

#### CIS 13: Data Protection
- 13.1: Inventory sensitive information
- 13.2: Remove sensitive data/systems not regularly accessed
- 13.3: Monitor/block unauthorized sensitive data transfers (DLP)
- 13.4: Only authorized cloud storage/email providers
- 13.5: Detect unauthorized encryption on outbound traffic
- 13.6: Encrypt mobile device data
- 13.7: Managed USB devices (inventory, allow only specific)
- 13.8: Disable write to external removable media
- 13.9: Encrypt data on USB storage

#### CIS 14: Controlled Access Based on Need to Know
- 14.1: Segment network by data sensitivity (VLANs)
- 14.2: Firewall filtering between VLANs
- 14.3: Disable workstation-to-workstation communication (private VLANs, micro-segmentation)
- 14.4: Encrypt sensitive information in transit
- 14.5: Active discovery for sensitive data
- 14.6: Access control lists on file systems, applications, databases
- 14.7: Host-based DLP for access control
- 14.8: Encrypt sensitive data at rest (secondary auth not OS-integrated)
- 14.9: Detailed logging for sensitive data access/changes (FIM/SIEM)

#### CIS 15: Wireless Access Control
- 15.1: Inventory authorized wireless access points
- 15.2: Detect unauthorized WAPs (vulnerability scanning)
- 15.3: Wireless IDS (WIDS)
- 15.4: Disable wireless on devices that don't need it
- 15.5: Limit wireless clients to authorized networks
- 15.6: Disable ad-hoc (peer-to-peer) wireless
- 15.7: AES encryption for wireless
- 15.8: EAP/TLS with mutual, multi-factor authentication
- 15.9: Disable Bluetooth/NFC unless business-required
- 15.10: Separate wireless network for personal/untrusted devices

#### CIS 16: Account Monitoring and Control
- 16.1: Inventory authentication systems
- 16.2: Centralized authentication (few points as possible)
- 16.3: Multi-factor authentication for all user accounts
- 16.4: Encrypt/hash all stored credentials (with salt)
- 16.5: Encrypt credential transmission
- 16.6: Inventory all accounts by authentication system
- 16.7: Automated account revocation upon termination/change
- 16.8: Disable unassociated accounts
- 16.9: Auto-disable dormant accounts (period of inactivity)
- 16.10: Account expiration dates
- 16.11: Auto-lock workstation sessions after inactivity
- 16.12: Monitor deactivated account access attempts
- 16.13: Alert on login behavior deviation (time, location, duration)

### 7.3 Organizational Controls (CIS 17-20)

#### CIS 17: Security Awareness and Training
- Skills gap analysis, training delivery, awareness program
- Train on secure authentication, social engineering, data handling
- Train on identifying and reporting incidents

#### CIS 18: Application Software Security
- Secure coding practices, error checking, supported software
- Trusted third-party components, standardized encryption
- Static/dynamic code analysis, WAF deployment
- Separate production/non-production, database hardening

#### CIS 19: Incident Response and Management
- Documented IR procedures, assigned roles
- Organization-wide reporting standards
- Contact info for law enforcement, ISAC partners
- Periodic incident scenario exercises and scoring schema

#### CIS 20: Penetration Tests and Red Team Exercises
- Full-scope penetration testing program
- Regular external and internal pentests
- Periodic Red Team exercises
- Test beds for non-production elements
- Document results in machine-readable standards (SCAP)

---

## INDEX OF KEY COMMANDS

### Volatility Quick Reference
```
python vol.py -f memory.dmp imageinfo                          # Profile detection
python vol.py -f memory.dmp --profile=<PROFILE> pslist         # Process list
python vol.py -f memory.dmp --profile=<PROFILE> pstree         # Process tree
python vol.py -f memory.dmp --profile=<PROFILE> psscan         # Hidden processes
python vol.py -f memory.dmp --profile=<PROFILE> netscan        # Network connections
python vol.py -f memory.dmp --profile=<PROFILE> malfind -D out # Malware detection
python vol.py -f memory.dmp --profile=<PROFILE> apihooks       # API hooks
python vol.py -f memory.dmp --profile=<PROFILE> hashdump       # Password hashes
python vol.py -f memory.dmp --profile=<PROFILE> timeliner      # Full timeline
```

### Wireshark Quick Reference
```
ip.addr == 192.168.1.1            # Host filter
tcp.port == 443                    # Port filter
http.request.method == "GET"       # HTTP method
tcp.flags.syn == 1                 # SYN packets
dns.qry.name contains "evil"       # DNS queries
Follow TCP Stream                  # Reconstruct session
Statistics > IO Graph              # Throughput analysis
Statistics > Protocol Hierarchy    # Protocol distribution
```

### BTFM Incident Response Quick Start
```
# Windows: systeminfo, netstat -naob, tasklist /SVC, autorunsc -m
# Linux: uname -a, ps -aux, netstat -antup, lsmod, lsof
# Memory dump: winpmem, LiME, fmem
# Disk image: dc3dd, dd
# Volatility: pslist -> netscan -> malfind -> apihooks
```
