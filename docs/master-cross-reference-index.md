# Killer Queen Master Cross-Reference Index

Every vulnerability class, technique, tool, and attack surface mapped to every skill and SOUL.md section. Generated from 25 skills + SOUL.md.

---

## I. VULNERABILITY CLASSES → SKILL REFERENCE

### Cross-Site Scripting (XSS)
- **web-attacks** §2 — 30 labs, reflected/stored/DOM/blind, 13 sub-sections, payloads, CSP bypass, AngularJS, postMessage XSS
- **web-attacks** §2.9 — File-based XSS (SVG, XML, Markdown, CSS)
- **web-attacks** §2.10 — Blind XSS grabbers, Collaborator
- **web-attacks** §2.11 — PortSwigger: document.write(), innerHTML, jQuery $(), AngularJS $eval sinks
- **SOUL.md** §Chain Table — Stored XSS → admin view → email/export/PDF rendering chain
- **SOUL.md** §Chain Table — XSS→CSRF→Admin Action (Critical, account escalation)
- **SOUL.md** §Chain Table — Cache Poisoning→Stored XSS→CDN Seeding→All Visitors
- **SOUL.md** §Chain Table — PostMessage→Origin Bypass→DOM XSS→ATO
- **SOUL.md** §XS-Leak Techniques — 33 methods for cross-site leaks
- **SOUL.md** §PostMessage Attack Vectors — wildcard origin, indexOf bypass, null origin
- **h1-bug-bounty-patterns** §4 — 2,384 reports, core patterns, bypass techniques, unique chains
- **h1-bug-bounty-patterns** §4 — Cache Poisoning→Stored XSS (PayPal), OAuth→XSS, CSRF→XSS
- **bughunter-methodology** §Cross-site (2 classes) — XSS crown jewels, attack surface signals, methodology
- **cloudflare-bypass** §5 — Fingerprint evasion for XSS delivery
- **wordpress-pentesting** §Phase 3 — Form exploitation, CF7 injection points
- **testing-methodology** §WSTG-INPV — Input validation testing
- **browser-exploitation** — (implicit) DOM-based context for XSS

### SQL Injection (SQLi)
- **web-attacks** §1 — 18 labs, 10 sub-sections: detection, DBMS ID, auth bypass, UNION, blind, error-based, OOB
- **web-attacks** §1.6 — WAF bypass: no spaces, no commas, no equals, keyword obfuscation
- **web-attacks** §1.7 — DB-specific RCE: MySQL, MSSQL, PostgreSQL, Oracle
- **web-attacks** §1.8 — PortSwigger technique map (8 categories)
- **SOUL.md** §Technique Catalog — 12+ SQLi injection classes: union, blind time/boolean, error, stacked, ORM bypass, header-based, second-order, NoSQL operator, WAF bypass
- **SOUL.md** §Chain Table — SQLi on one param → every param → same type siblings
- **SOUL.md** §Chain Table — SQLi+COPY FROM PROGRAM→Postgres OS-level RCE
- **SOUL.md** §RCE Chains — SQLi xp_cmdshell, UTL_HTTP, LOAD_FILE, COPY FROM PROGRAM
- **h1-bug-bounty-patterns** §6 — 307 reports, types, injection points, WAF bypass, SQLi-to-RCE chains
- **bughunter-methodology** §Injection (4 classes) — SQLi methodology, ORM bypass, header-based
- **testing-methodology** §WSTG-INPV — Input validation testing

### Server-Side Request Forgery (SSRF)
- **web-attacks** §3 — 7 labs, cloud metadata (AWS/GCP/Azure/DO/Oracle/Alibaba), bypass techniques
- **web-attacks** §3.2 — 10+ bypass localhost filter methods (IPv6, IP encoding, DNS rebinding, Unicode)
- **web-attacks** §3.3 — URL scheme exploitation (file, dict, gopher, ldap, tftp, sftp, netdoc, jar)
- **web-attacks** §3.4 — Blind SSRF OAST via Collaborator/interactsh
- **SOUL.md** §SSRF Cloud Metadata — full multi-cloud metadata endpoints
- **SOUL.md** §Chain Table — SSRF DNS → Internal Service Data → SSRF via open redirect
- **SOUL.md** §Chain Table — SSRF DNS→Internal Service→Cloud Metadata (Critical)
- **SOUL.md** §RCE Chains — SSRF+IMDSv1+Lambda invoke (Capital One), SSRF+Gopher→Redis/FastCGI→RCE
- **SOUL.md** §RCE Chains — Blind SSRF+Shellshock CVE-2014-6271→RCE
- **SOUL.md** §SSRF URL Parser Cross-Language Confusion Matrix — Java/Python/Node/PHP/Go/curl
- **SOUL.md** §SSRF Bypass Techniques — 10 parser differential techniques
- **SOUL.md** §Conference Attack Techniques — New SSRF 2024-2026: Gopher K8s, SNI field, IMDSv2 bypass
- **h1-bug-bounty-patterns** §7 — 311 reports, impact escalation, entry points, tools
- **orange-tsai-methodology** — URL parser confusion, SSRF bypass via parser differentials
- **bughunter-methodology** §Server-side (4 classes) — SSRF methodology
- **cloud-iam-attacks** — SSRF→IMDS credential theft section

### IDOR / Authorization Flaws
- **web-attacks** § — Implicit in access control labs (13 PortSwigger labs)
- **SOUL.md** §Chain Table — IDOR on GET → IDOR on PUT/DELETE → IDOR on ALL siblings
- **SOUL.md** §Chain Table — IDOR /v2/ → same IDOR on /v1/ (missing fix)
- **h1-bug-bounty-patterns** §1 — 253 reports (#3), 35.7% High/Critical, BOLA types
- **h1-bug-bounty-patterns** §3 — Pattern A: Info Disclosure→IDOR→PrivEsc→Critical
- **bughunter-methodology** §Authorization (3 classes) — IDOR methodology, sequential integers pattern
- **testing-methodology** §WSTG-ATHZ (4.5.4) — IDOR testing

### XXE (XML External Entity)
- **web-attacks** § — 9 PortSwigger labs
- **SOUL.md** §RCE Chains — XXE+PHP expect:// stream wrapper
- **SOUL.md** §SAML Attack Classes — XXE via SAML
- **bughunter-methodology** §Server-side (4 classes) — XXE methodology

### Server-Side Template Injection (SSTI)
- **web-attacks** § — 7 PortSwigger labs
- **SOUL.md** §RCE Chains — SSTI Jinja2 hex-encoded WAF bypass→RCE
- **SOUL.md** §Chain Table — (implicit in RCE chains)
- **h1-bug-bounty-patterns** §5 — SSTI to RCE (Jinja2, Freemarker, Velocity, ERB, Twig)
- **bughunter-methodology** §Injection (4 classes) — SSTI engine fingerprint (Jinja2, Freemarker, Thymeleaf)

### Command Injection
- **web-attacks** § — 5 PortSwigger labs
- **SOUL.md** §Technique Catalog — (implicit in injection classes)
- **bughunter-methodology** §Injection (4 classes) — CMDi detection, blind OOB, bypass techniques
- **infrastructure-attacks** §Bypass Bash Restrictions — space bypass, slash bypass, short reverse shells

### File Upload Vulnerabilities
- **web-attacks** § — 7 PortSwigger labs
- **SOUL.md** §Technique Catalog — 10 file upload bypass techniques
- **SOUL.md** §Chain Table — File upload PNG allowed → SVG (XSS), PHP/JSP (RCE) → Double extension
- **SOUL.md** §RCE Chains — Image upload+path traversal+MIME serving→webshell
- **SOUL.md** §RCE Chains — File upload+GZIP body+Tomcat path traversal→JSP webshell
- **h1-bug-bounty-patterns** §5 — File Upload RCE (webshell, null byte, .htaccess)
- **wordpress-pentesting** §Phase 3 — Form exploitation, CF7 dnd upload bypass
- **wordpress-recon** — Pre-requisite for WP file upload exploitation

### Deserialization
- **web-attacks** § — 10 PortSwigger labs
- **SOUL.md** §RCE Chains — Ruby Marshal Gem::StubSpecification→DependencyList→instance_eval→RCE
- **SOUL.md** §Chain Table — (implicit in RCE chains)
- **SOUL.md** §Orange Tsai — Hessian deserialization + JNDI injection (MobileIron)
- **h1-bug-bounty-patterns** §5 — Java/Ruby/Python/.NET/PHP deserialization RCE
- **orange-tsai-methodology** — MobileIron MDM Hessian deserialization+JNDI

### JWT Attacks
- **web-attacks** § — 8 PortSwigger labs
- **SOUL.md** §Auth Bypass Classes — JWT alg=none, audience confusion, scope claim manipulation
- **bughunter-methodology** §Identity/Session — JWT testing methodology

### GraphQL Attacks
- **web-attacks** § — 5 PortSwigger labs
- **SOUL.md** §Chain Table — GraphQL introspection → Auth bypass on mutations → IDOR via node(id)

### NoSQL Injection
- **web-attacks** § — 4 PortSwigger labs
- **SOUL.md** §SQLi Injection Classes — NoSQL operator injection ($regex, $gt, $ne, $where)
- **bughunter-methodology** §Injection (4 classes) — NoSQLi MongoDB auth bypass, $where JS injection

### Prototype Pollution
- **web-attacks** § — 10 PortSwigger labs
- **SOUL.md** §RCE Chains — Prototype pollution+Lodash/Mongoose→child_process.spawn
- **SOUL.md** §PostMessage Attack Vectors — Prototype Pollution+XSS chain
- **h1-bug-bounty-patterns** §5 — Prototype Pollution to RCE (Kibana, Node.js)

### Request Smuggling
- **web-attacks** § — 22 PortSwigger labs
- **SOUL.md** §HTTP Request Smuggling — CL.0/TE.0/0.CL, TRACE desync, Pingora 2026 variants
- **SOUL.md** §RCE Chains — HTTP Smuggling CL.0→Cache Poisoning→Stored XSS→All Users
- **SOUL.md** §Conference Attack Techniques — Browser-Powered Desync, H2C smuggling, HTTP/2 rapid reset
- **bughunter-methodology** — (implicit in web attack primitives)

### Web Cache Poisoning / Deception
- **web-attacks** § — 13 cache poisoning + 5 cache deception labs
- **SOUL.md** §Web Cache Deception — CDN path traversal, Fat GET, Parameter Cloaking, CSPT-assisted
- **SOUL.md** §Cache Attack Methodology — Cache Deception, Cache Poisoning, Cache Key Confusion
- **SOUL.md** §Conference Attack Techniques — Cache Deception 2.0, CDN-specific cache bypass
- **SOUL.md** §IIS Hash Table Destabilization — Hash collision → cache control → cache poisoning
- **h1-bug-bounty-patterns** §3 — Pattern D: Cache Deception→Sensitive Data Leak→ATO

### CSRF
- **web-attacks** § — 12 PortSwigger labs
- **SOUL.md** §Chain Table — CSRF on sensitive action → XSS→CSRF → img src/form autosubmit
- **SOUL.md** §Chain Table — (see XSS→CSRF→Admin Action chain)
- **h1-bug-bounty-patterns** §3 — CSRF+XSS chains
- **bughunter-methodology** §Cross-site (2 classes) — CSRF methodology
- **testing-methodology** §WSTG-SESS — CSRF testing

### CORS Misconfigurations
- **web-attacks** § — 3 PortSwigger labs
- **bughunter-methodology** — (implicit in cross-site testing)

### Open Redirect
- **web-attacks** § — (implicit in SSRF/XSS wrappers)
- **SOUL.md** §Chain Table — Open redirect confirmed → OAuth code theft → ATO
- **SOUL.md** §Never Submit — Open redirect alone (must chain)
- **h1-bug-bounty-patterns** §3 — Pattern H: Open Redirect→OAuth Token Theft→ATO

### Authentication Bypass
- **web-attacks** §1.3 — SQLi auth bypass payloads
- **web-attacks** § — 14 PortSwigger auth labs
- **SOUL.md** §Auth Bypass Classes — 12+ classes: legacy protocol, header tricks, method tampering, parameter pollution, JSON parser confusion, race on session, mass-assignment, SAML callback, JWT, refresh-token replay
- **SOUL.md** §Legacy Protocol Matrix — 17-platform matrix (WP xmlrpc, SharePoint, Jira, Exchange, etc.)
- **SOUL.md** §M365/Entra Signals — AADSTS codes, OneDrive user existence
- **h1-bug-bounty-patterns** §1 — ATO ranking (#5, 234 reports)

### Subdomain Takeover
- **SOUL.md** §Chain Table — Subdomain takeover → OAuth redirect_uri → Cookie-domain session fixation
- **h1-bug-bounty-patterns** §3 — Pattern E: Subdomain Takeover→Cookie Scope Abuse→Session Hijack
- **infrastructure-attacks** § — SMTP/DNS section for subdomain analysis
- **testing-methodology** §WSTG-CONF (4.2.10) — Subdomain takeover testing

### Dependency Confusion
- **h1-bug-bounty-patterns** §5 — npm/pip/gem dependency confusion→RCE ($30K PayPal)
- **h1-bug-bounty-patterns** §3 — Pattern G: Dependency Confusion→Package Install→RCE

### Race Conditions
- **web-attacks** § — 6 PortSwigger labs
- **SOUL.md** §Chain Table — Race on coupons → Race on credits/wallet → Race on rate limits
- **bughunter-methodology** §Business/Race (4 classes) — Race condition methodology

### SAML Attacks
- **SOUL.md** §SAML Attack Classes — 8 XSW variants, CVE-2024-45409, RelayState injection, SAML Raider
- **SOUL.md** §Chain Table — SAML Signature Wrapping→Attribute Injection→Admin SSO
- **bughunter-methodology** — (implicit in identity/session testing)

### OAuth Attacks
- **SOUL.md** §Chain Table — OAuth missing PKCE → CSRF on OAuth flow → Token reuse
- **SOUL.md** §Chain Table — Open redirect→OAuth code theft→ATO
- **h1-bug-bounty-patterns** §3 — Pattern F: OAuth Dance Abuse→Account Linking Attack

### LLM / AI Attacks
- **ai-ml-attacks** §All — Model RCE (16 CVEs), prompt injection, Hydra metadata→RCE, InvokeAI CVE-2024-12029
- **ai-ml-attacks** §Prompt Injection — Indirect injection, tool-use exploitation, jailbreaks
- **SOUL.md** §Chain Table — LLM prompt injection → IDOR via chatbot → Exfil via img src
- **SOUL.md** §H4CKER AI Chains — Prompt injection→Tool-use exploitation→SSRF, Jailbreak→System prompt extraction→API key leak, AI supply chain→RCE
- **h1-bug-bounty-patterns** §1 — AI/LLM Vulnerabilities (2025+ frontier)
- **bughunter-methodology** — AI/LLM attack surface overview

### Cloud IAM Privilege Escalation
- **cloud-iam-attacks** §All — 30 escalation paths, 10+ persistence techniques, GuardDuty evasion
- **cloud-iam-attacks** §1A — Direct IAM permission abuse (8 paths)
- **cloud-iam-attacks** §1B — Role/Group-based escalation (8 paths)
- **cloud-iam-attacks** §1C — Service-specific escalation (14 paths)
- **SOUL.md** §IAM Escalation Chains — SSRF→IMDSv1→temp creds→iam:PutUserPolicy→Admin
- **SOUL.md** §IAM Escalation Chains — iam:PassRole+Lambda→lambda:InvokeFunction→Admin
- **SOUL.md** §IAM Escalation Chains — iam:CreatePolicyVersion→SetDefaultPolicyVersion→Admin
- **SOUL.md** §IAM Escalation Chains — iam:UpdateAssumeRolePolicy→sts:AssumeRole→Admin
- **SOUL.md** §Chain Table — S3→Bundle→Secret→OAuth chain
- **SOUL.md** §RCE Chains — SSRF+IMDSv1+Lambda invoke (Capital One pattern)

### Active Directory Attacks
- **windows-red-team** §4 — AD CS ESC1-13, Kerberos attacks, DACL abuse
- **windows-red-team** §4.2 — Golden Ticket, Silver Ticket, Diamond Ticket, Skeleton Key
- **windows-red-team** §4.3 — DCSync, Kerberoasting, AS-REP Roasting
- **windows-red-team** §3 — Credential dumping (LSASS, SAM, NTDS)
- **windows-red-team** §2 — Process injection (30 methods)
- **SOUL.md** §AD Escalation Chains — ASREPRoasting→crack→Overpass-the-Hash→TGT→Golden Ticket
- **SOUL.md** §AD Escalation Chains — Kerberoasting→crack→Silver Ticket→Lateral
- **SOUL.md** §AD Escalation Chains — DACL GenericAll→Shadow Credentials→PKINIT→TGT
- **SOUL.md** §AD Escalation Chains — DACL WriteDacl on OU→ACE Inheritance→AdminCount=0→DCSync
- **SOUL.md** §AD Escalation Chains — S4U2Self→S4U2Proxy→Bronze Bit CVE-2020-17049→Delegation bypass
- **SOUL.md** §Kerberos Attacks — Full attack matrix
- **SOUL.md** §DACL Abuse — BloodHound edges reference
- **SOUL.md** §AD Attack Matrix — Recon→Escalate→Lateral→Persist→Exfil
- **SOUL.md** §Privesc Decision Tree — Windows privesc (13 steps)
- **infrastructure-attacks** § — RDP, SMB, FTP service exploitation for AD pivoting

### Container / Kubernetes Attacks
- **infrastructure-attacks** § — Docker escape, K8s attacks, privilege escalation
- **SOUL.md** §H4CKER Cloud Orchestration Chains — Container breakout→K8s pod escape→Node compromise→etcd dump
- **SOUL.md** §Conference Attack Techniques — K8s RBAC escalation, etcd access, Kubelet API, Helm Tiller, CRI-O escape
- **SOUL.md** §Conference Attack Techniques — Docker API RCE (2375/2376)
- **awesome-redteam-toolkit** — Cloud/K8s security tools (ScoutSuite, kube-hunter, trivy)

---

## II. ATTACK SURFACES → SKILL REFERENCE

### Web Applications (General)
- **web-attacks** — Primary (60+ vuln categories)
- **testing-methodology** — WSTG v4.2 (150+ tests)
- **bughunter-methodology** — 6-phase workflow, 47 vulnerability classes
- **h1-bug-bounty-patterns** — Real-world frequency and payout data
- **orange-tsai-methodology** — Parser differentials, semantic ambiguity
- **SOUL.md** §Kill Chain — SCOPE→RECON→HUNT→VALIDATE→CAPTURE→REPORT
- **SOUL.md** §7-Question Gate — Validation framework
- **SOUL.md** §Never Submit list

### WordPress
- **wordpress-pentesting** — Primary: recon, form exploitation, file upload bypass, multi-vector patterns
- **wordpress-recon** — Recon methodology: REST API plugin discovery, version fingerprinting, nonce extraction
- **web-attacks** — General web payloads applicable to WP
- **h1-bug-bounty-patterns** — XSS via WP, file upload patterns
- **bughunter-methodology** — Legacy-Protocol Matrix includes WP xmlrpc.php

### Cloud / AWS
- **cloud-iam-attacks** — Primary: 30 escalation paths, persistence, GuardDuty evasion
- **infrastructure-attacks** §Cloud/Containers — Docker, K8s, cloud metadata
- **web-attacks** §3.1 — Cloud metadata endpoints (AWS/GCP/Azure/DO/Oracle/Alibaba)
- **SOUL.md** §SSRF Cloud Metadata — Full multi-cloud reference
- **SOUL.md** §IAM Escalation Chains — 5+ cloud escalation paths
- **SOUL.md** §Cloud Security Tools — Pacu, CloudMapper, ScoutSuite, Enumerate-IAM, PMapper
- **awesome-redteam-toolkit** — Cloud/K8s tool categories

### Active Directory / Windows Enterprise
- **windows-red-team** — Primary: defense evasion (27), injection (30), credential dump, AD attacks
- **SOUL.md** §AD Escalation Chains — 5 full escalation paths
- **SOUL.md** §Kerberos Attacks — Full attack matrix (10 techniques)
- **SOUL.md** §DACL Abuse — BloodHound edges reference (10+ edges)
- **SOUL.md** §AD Attack Matrix — Recon→Escalate→Lateral→Persist→Exfil
- **SOUL.md** §Privesc Decision Tree — Windows privesc (13 steps)
- **SOUL.md** §Evasion & Anti-Detection — AMSI, ETW, syscall obfuscation
- **SOUL.md** §Tool Command Templates — nmap, netexec, impacket, BloodHound, Certipy
- **infrastructure-attacks** — Service exploitation (SMB, RDP, FTP) for AD pivoting
- **threat-intel** — MITRE ATT&CK Enterprise mapping for AD attacks

### Browser / JavaScript Engines
- **browser-exploitation** — Primary: V8, JSC, SpiderMonkey, ChakraCore, sandbox escapes
- **exploit-development** — Exploit primitives (addrof/fakeobj), ROP, DEP/ASLR bypass
- **SOUL.md** §Pwn2Own Chains — Chrome V8→Mojo IPC→Win32k kernel EoP
- **SOUL.md** §Pwn2Own Chains — Safari JSC→macOS Seatbelt→XPC kernel EoP
- **SOUL.md** §0-Day Chain Anatomy — Full browser exploit chain (Renderer→Sandbox→Kernel)

### Mobile (Android / iOS)
- **mobile-attacks** — Primary: APK analysis, Frida, Smali modification, WebView attacks, deeplinks
- **mobile-attacks** §Smali — Modification patterns, anti-tamper patches, repackaging
- **mobile-attacks** §iOS — Jailbreak detection bypass, keychain extraction, IPA analysis
- **pwn2own-exploitation** §2.4 — Android logic bug chains (11 bugs→6 apps→root)
- **pwn2own-exploitation** §2.5 — CVE-2019-2215 Binder UAF full chain
- **SOUL.md** §Pwn2Own Chains — 11 Android logic bugs→Silent APK install→Full device compromise
- **SOUL.md** §iOS Exploitation — ktrw, checkra1n, Frida, XNU kernel, XPC, IOKit

### Embedded / IoT / Firmware
- **embedded-iot-attacks** §1 — Firmware extraction (unblob, binwalk, EMBA, FACT), emulation (QEMU, Qiling)
- **embedded-iot-attacks** §2 — Hardware debug (JTAG, UART, SPI, I2C)
- **embedded-iot-attacks** §3 — Protocol exploitation (CAN, Modbus, DNP3, OPC-UA, S7comm)
- **embedded-iot-attacks** §4 — UEFI/SMM/bootkit attacks, Secure Boot bypass
- **embedded-iot-attacks** §5 — Side-channel (CPA/DPA), fault injection (voltage glitching, EMFI)
- **SOUL.md** §Embedded/IoT Attack Surfaces — UART, JTAG, SPI flash, I2C, glitching, CAN bus, firmware extraction, UEFI, ICS protocols
- **SOUL.md** §H4CKER IoT Chains — Firmware extraction→root hash→SSH→LAN lateral
- **SOUL.md** §H4CKER IoT Chains — UART/JTAG physical→bootloader interrupt→flash dump→cloud pivot
- **SOUL.md** §H4CKER IoT Chains — BLE spoofing→GATT injection→sensor manipulation
- **SOUL.md** — NCC Group 2025: Enterprise IoT fails NCSC/ETSI standards

### AI / ML Systems
- **ai-ml-attacks** — Primary: Model RCE (16 CVEs), prompt injection, Hydra metadata, MCP attacks
- **SOUL.md** §H4CKER AI Chains — 5 chains (prompt injection→tool-use→SSRF, jailbreak→API key leak, supply chain→RCE)
- **SOUL.md** §NCC Group 2025 — Agentic AI attacks, prompt injection→RCE chains

### Social Engineering / Phishing
- **social-engineering-wireless** §1 — Phishing frameworks (GoPhish, EvilGinx, Modlishka, SocialFish, SET)
- **social-engineering-wireless** §2 — Spearphishing vectors, email spoofing, HTML smuggling
- **SOUL.md** §Social Engineering Chains — Phishing→Credential Harvest→MFA token theft→Session hijack
- **SOUL.md** §Social Engineering Chains — Spearphishing→Macro DOCX→C2 beacon→Lateral→Domain Admin
- **SOUL.md** §Social Engineering Chains — Consent phishing (OAuth app)→Graph API→Mailbox exfiltration
- **SOUL.md** §Social Engineering Chains — Deepfake vishing→Voice clone→Executive impersonation
- **SOUL.md** §PTES Methodology — Social engineering testing phases
- **SOUL.md** §Social Engineering Tools — SET credential harvester, Java applet, QR code attacks

### Wireless / RF / Physical
- **social-engineering-wireless** §3 — WiFi/WPA2 attacks, Bluetooth/BLE, SDR/RF, RFID/NFC, Zigbee
- **social-engineering-wireless** §4 — Physical security (BadUSB, Rubber Ducky, lock picking, surveillance)
- **SOUL.md** §Wireless/RF Chains — WiFi handshake→crack→network join→SMB lateral→AD compromise
- **SOUL.md** §Wireless/RF Chains — EvilTwin AP→RADIUS MSCHAPv2→asleap crack→Domain credentials→DCSync
- **SOUL.md** §Wireless/RF Chains — RFID clone→physical access badge→USB HID injection→implant persistence
- **SOUL.md** §Wireless/RF Chains — BLE spoofing→device impersonation→GATT write→data exfil→cloud pivot
- **SOUL.md** §Wireless/RF Chains — SDR replay→key fob rolling code→CAN bus injection→telematics compromise
- **SOUL.md** §Wireless/RF Chains — NFC relay→contactless payment relay→ATM/POS exploitation
- **SOUL.md** §Wireless Testing — aircrack-ng workflow (airmon-ng, airodump-ng, aireplay-ng)

### Automotive / CAN Bus
- **embedded-iot-attacks** §3 — CAN bus, SocketCAN, ICSim, CAN injection, CAN replay
- **SOUL.md** §H4CKER Automotive Chains — CAN bus injection→ECU reflash→permanent implant
- **SOUL.md** §H4CKER Automotive Chains — Key fob relay→SDR replay→vehicle unlock→brake/steering control
- **SOUL.md** §H4CKER Automotive Chains — OBD-II access→CAN message replay→gateway bypass→ADAS spoofing
- **pwn2own-exploitation** — Pwn2Own Automotive: Tesla TCU adb bypass, EV charger OCPP exploitation
- **SOUL.md** §NCC Group 2025 — EV charger exploitation, IVI USB/bluetooth attacks

### Zero-Day / Pwn2Own
- **pwn2own-exploitation** — Full contest history, technique catalogue, logic bug chains, CVE catalog
- **exploit-development** — Complete reference (Corelan 41 tutorials, FuzzySecurity 19 parts)
- **browser-exploitation** — JS engine exploitation, sandbox escapes
- **SOUL.md** §Pwn2Own Patterns — Exploit chains, primitives, vulnerability categories, discovery tools
- **SOUL.md** §Project Zero — 60+ CVEs, bug class catalogue

### Cloudflare / Anti-Bot
- **cloudflare-bypass** — Complete: 6 bypass layers, stealth browsers, cf_clearance relay, origin IP discovery, Turnstile solvers
- **SOUL.md** §Cloudflare Bypass — Technique catalogue (challenge types, stealth browsers, patching techniques, fingerprint evasion)
- **web-attacks** — WAF bypass payloads for SQLi, XSS

### Malware / C2 / Post-Exploitation
- **malware-dev** — Primary: RAT persistence, C2 crypto, credential theft, process injection, worm replication
- **malware-dev** §1 — Persistence (Scheduled Tasks, Registry Run, WMI, Startup folder)
- **malware-dev** §2 — C2 crypto patterns (TLS 1.2 pinning, AES-256-CBC+HMAC-SHA256, Ed25519)
- **malware-dev** §3 — Credential theft (Chrome DPAPI, Firefox master password, FileZilla/WinSCP XML)
- **malware-dev** §4 — Worm self-replication (Mirai: SYN scanner, 60+ Telnet creds, 9-state brute, competitor killing)
- **SOUL.md** §Malware Persistence Patterns — Scheduled Tasks, Registry Run, Named Mutex, WMI, Startup, DLL hijack, COM hijack, Service install
- **SOUL.md** §RAT C2 Crypto Patterns — TLS 1.2 cert pinning, AES-256-CBC+HMAC, PBKDF2 50K iter, XOR 0xDEADBEEF, Ed25519
- **SOUL.md** §Worm Self-Replication — Mirai: SYN scanner, 60+ Telnet creds, 9-state brute, Busybox wget/tftp
- **SOUL.md** §Process Injection — Linux SYS_CLONE+mprotect, memfd+LD_PRELOAD, Reflective DLL, Process Hollowing, Windows RemoteTask
- **SOUL.md** §Token Manipulation — Token theft+duplication, ImpersonateLoggedOnUser, GetSystem, LogonUser MakeToken, PPID spoofing
- **SOUL.md** §Malware Source Analysis — Mirai, QuasarRAT, AsyncRAT, Sliver, Pupy, UACME, TokenPlayer source analysis

### Linux Privilege Escalation
- **infrastructure-attacks** §Linux Privesc — Quick enumeration, 12 vectors, capabilities exploitation, SELinux
- **infrastructure-attacks** §Bypass Bash Restrictions — Path/command obfuscation, space/slash bypass
- **infrastructure-attacks** §Chroot Escape — 3 methods (double chroot, mount host, /proc root)
- **SOUL.md** §Privesc Decision Tree — Linux privesc (13 steps, ordered by success rate)
- **exploit-development** — Kernel exploitation section (write-what-where, token stealing, GDI bitmap)

### Supply Chain Attacks
- **h1-bug-bounty-patterns** §5 — Dependency confusion RCE
- **ai-ml-attacks** — Model supply chain (Pickle/PyTorch checkpoint attacks)
- **SOUL.md** §H4CKER AI Chains — AI supply chain→malicious model→RCE on inference server
- **SOUL.md** §NCC Group 2025 — 280+ repos analyzed, CI/CD pipeline attacks, GitHub Actions injection

---

## III. TOOLS → SKILL REFERENCE

### Reconnaissance Tools
| Tool | Skills |
|------|--------|
| **nmap** | infrastructure-attacks §Network Service Exploitation, SOUL.md §Nmap Cheat Sheet, testing-methodology, awesome-redteam-toolkit, SOUL.md §Tool Command Templates |
| **rustscan** | infrastructure-attacks §Network Service Exploitation |
| **amass** | awesome-redteam-toolkit §Recon, mission-orchestrator, SOUL.md §The Hacker Recipes |
| **subfinder** | awesome-redteam-toolkit §Subdomain Enum, mission-orchestrator, SOUL.md §ProjectDiscovery Tools |
| **httpx** | awesome-redteam-toolkit, SOUL.md §ProjectDiscovery Tools |
| **nuclei** | awesome-redteam-toolkit §Fuzzing, SOUL.md §ProjectDiscovery Tools, SOUL.md §Tool Command Templates |
| **ffuf** | testing-methodology, SOUL.md §Tool Command Templates |
| **katana** | awesome-redteam-toolkit, SOUL.md §ProjectDiscovery Tools |
| **gau / waybackurls** | awesome-redteam-toolkit, SOUL.md §The Hacker Recipes |
| **theHarvester** | SOUL.md §OSINT Tools, testing-methodology |
| **cewl** | SOUL.md §Tool Command Templates |

### Web Application Testing
| Tool | Skills |
|------|--------|
| **Burp Suite** | web-attacks (referenced per section), SOUL.md §Burp Suite Quick Reference, testing-methodology |
| **sqlmap** | web-attacks §1.10, SOUL.md §Tool Command Templates |
| **ghauri** | web-attacks §1.10 |
| **dalfox / xsstrike / xsser** | web-attacks §2.13 |
| **domdig** | web-attacks §2.13 |
| **SSRFmap** | web-attacks §3 |
| **gopherus** | web-attacks §3, SOUL.md §RCE Chains |
| **interactsh-client** | SOUL.md §Tool Command Templates, SOUL.md §ProjectDiscovery Tools, web-attacks §3.4 |
| **wpscan** | wordpress-pentesting, kali-tools-arsenal |

### Cloud Security Tools
| Tool | Skills |
|------|--------|
| **Pacu** | SOUL.md §Cloud Security Tools |
| **ScoutSuite** | SOUL.md §Cloud Security Tools, kali-tools-arsenal |
| **CloudMapper** | SOUL.md §Cloud Security Tools |
| **Enumerate-IAM** | SOUL.md §Cloud Security Tools |
| **cloudfox** | kali-tools-arsenal |
| **prowler** | kali-tools-arsenal |

### Active Directory Tools
| Tool | Skills |
|------|--------|
| **BloodHound / SharpHound** | windows-red-team §DACL Abuse, SOUL.md §DACL Abuse, kali-tools-arsenal |
| **Certipy / Certify** | windows-red-team §4.1 (ESC1-13), SOUL.md §AD Attack Matrix |
| **Impacket** (secretsdump, GetNPUsers, GetUserSPNs, psexec, wmiexec) | windows-red-team §3-4, SOUL.md §AD Attack Matrix, SOUL.md §Tool Command Templates |
| **NetExec / CrackMapExec** | windows-red-team §3, SOUL.md §Tool Command Templates |
| **Rubeus** | windows-red-team §4.2, SOUL.md §Awesome-Redteam Toolkit |
| **Mimikatz** | windows-red-team §3, SOUL.md §Credential Access tools |
| **kerbrute** | windows-red-team, SOUL.md §AD Attack Matrix |
| **Responder** | kali-tools-arsenal, SOUL.md §AD Attack Matrix |
| **mitm6 / ntlmrelayx** | SOUL.md §AD Attack Matrix |
| **lsassy** | windows-red-team §3.1, SOUL.md §AD Attack Matrix |
| **PetitPotam / PrinterBug** | SOUL.md §AD Attack Matrix |

### Exploit Development / Debugging
| Tool | Skills |
|------|--------|
| **Immunity Debugger / WinDbg / GDB** | exploit-development, SOUL.md §Exploit Development |
| **mona.py** | exploit-development §2.3 |
| **pwntools** | exploit-development |
| **Metasploit / msfvenom** | exploit-development, windows-red-team §1.1, SOUL.md §Tool Command Templates |
| **pattern_create / pattern_offset** | exploit-development §2.1 |
| **Keystone** | exploit-development |
| **boofuzz / Sulley** | exploit-development §1 |
| **Fuzzilli / domato** | browser-exploitation §Browser Fuzzing |
| **ROPGadget** | exploit-development |

### Phishing / Social Engineering
| Tool | Skills |
|------|--------|
| **GoPhish** | social-engineering-wireless §1 |
| **EvilGinx** | social-engineering-wireless §1, SOUL.md §Social Engineering Chains |
| **Modlishka** | social-engineering-wireless §1, SOUL.md §Social Engineering Chains |
| **SET (Social Engineering Toolkit)** | social-engineering-wireless §1, SOUL.md §Social Engineering Tools |
| **swaks** | infrastructure-attacks §Email, social-engineering-wireless §2 |

### Cloudflare / Anti-Bot Bypass
| Tool | Skills |
|------|--------|
| **CloakBrowser** | cloudflare-bypass §2 |
| **undetected-chromedriver** | cloudflare-bypass §2 |
| **patchright** | cloudflare-bypass §2 |
| **cloudscraper** | cloudflare-bypass §3 |
| **cf-clearance** | cloudflare-bypass §3 |
| **CloakQuest3r** | cloudflare-bypass §4 |

### Mobile Testing
| Tool | Skills |
|------|--------|
| **apktool / jadx** | mobile-attacks §APK Analysis |
| **Frida / objection** | mobile-attacks §iOS/Runtime Manipulation |
| **adb** | mobile-attacks §Android ADB Reference |

### Embedded / IoT
| Tool | Skills |
|------|--------|
| **binwalk / unblob** | embedded-iot-attacks §1.1 |
| **EMBA / FACT / FirmAE** | embedded-iot-attacks §1.1 |
| **QEMU / Qiling / Unicorn** | embedded-iot-attacks §1.2 |
| **OpenOCD / pyOCD / probe-rs** | embedded-iot-attacks §1.3 |
| **flashrom** | embedded-iot-attacks §1.1 |
| **Bus Pirate / Tigard** | embedded-iot-attacks §1.4 |

### C2 Frameworks
| Tool | Skills |
|------|--------|
| **Cobalt Strike** | awesome-redteam-toolkit §C2, SOUL.md §Awesome-Redteam Toolkit, windows-red-team §PPID spoofing |
| **Sliver** | awesome-redteam-toolkit §C2, malware-dev |
| **Mythic** | awesome-redteam-toolkit §C2 |
| **Havoc** | awesome-redteam-toolkit §C2 |
| **Empire** | awesome-redteam-toolkit §C2 |
| **Covenant** | awesome-redteam-toolkit §C2 |

---

## IV. TECHNIQUE DOMAINS → SKILL REFERENCE

### Persistence
- **malware-dev** §1 — RAT persistence: Scheduled Tasks, Registry Run, WMI Event Subscription, Named Mutex
- **malware-dev** §1 — QuasarRAT Client upgrader, Zone.Identifier removal
- **windows-red-team** §1.6 — 27 evasion techniques including persistence-adjacent (timestomping, ADS, scheduled tasks)
- **windows-red-team** — (implicit in AD persistence: Golden Ticket, Silver Ticket, Skeleton Key, AdminSDHolder)
- **SOUL.md** §Malware Persistence Patterns — 8 patterns from source code
- **SOUL.md** §AD Attack Matrix — Persistence section (Golden Ticket, Silver Ticket, Skeleton Key, DCShadow, WMI)
- **infrastructure-attacks** §Linux Privesc — Cron jobs, writable /etc/passwd, LD_PRELOAD, .pth files
- **cloud-iam-attacks** §Persistence — 10+ cloud persistence techniques
- **social-engineering-wireless** — BadUSB/Rubber Ducky persistence via HID injection

### Evasion / Defense Evasion
- **windows-red-team** §1 — 27 evasion techniques: AV bypass, direct syscalls, API unhooking, PPID spoofing, timestomping, ADS, ETW patching, AMSI bypass, Herpaderping, Process Doppelganging
- **windows-red-team** §1.1 — 5-stage AV bypass progression (48/68 → 3/68)
- **windows-red-team** §1.2 — Direct syscall invocation (SysWhispers, Hells Gate, Halos Gate)
- **windows-red-team** §1.3 — API unhooking (per-function + full DLL)
- **windows-red-team** §1.4 — RWX memory reuse (hunting existing allocations)
- **SOUL.md** §Evasion & Anti-Detection — AMSI bypass, ETW bypass, Syscall obfuscation, payload delivery obfuscation, sandbox detection
- **SOUL.md** §Defense Evasion Recognition — WAF presence, EDR detection, AV signature avoidance, log evasion
- **cloudflare-bypass** — 6-layer anti-detection architecture
- **malware-dev** — Implicit: XOR obfuscation, JARM randomization, Zone.Identifier removal

### Privilege Escalation
- **infrastructure-attacks** §Linux Privesc — 13 vectors, capabilities exploitation (11 capabilities mapped)
- **infrastructure-attacks** §SELinux Attacks — Policy analysis, domain transition, relabel primitives
- **windows-red-team** §UAC Bypass — 60+ methods catalogued
- **windows-red-team** §Token Manipulation — SeImpersonate, SeAssignPrimaryToken, SeDebug, SeBackup
- **SOUL.md** §Privesc Decision Tree — Linux (13 steps) + Windows (13 steps) ordered by success rate
- **SOUL.md** §UAC Bypass — 60+ methods from UACME
- **SOUL.md** §Token Manipulation — Full techniques from TokenPlayer/Sliver
- **cloud-iam-attacks** — 30 IAM privilege escalation paths
- **SOUL.md** §IAM Escalation Chains — 5 cloud escalation paths
- **exploit-development** — Kernel exploitation (write-what-where, GDI bitmap, token stealing, RS2 necromancy)

### Credential Access / Dumping
- **windows-red-team** §3 — LSASS dump (Procdump+Mimikatz, comsvcs.dll, LalsDumper, PPLBlade)
- **windows-red-team** §3.2 — SAM/SYSTEM/SECURITY dump (reg save, Volume Shadow Copy)
- **windows-red-team** §3.3 — DCSync (secretsdump, Mimikatz)
- **windows-red-team** §3.4-3.5 — Kerberoasting, AS-REP Roasting
- **SOUL.md** §Credential Theft — Chrome DPAPI, Firefox master password, FileZilla/WinSCP XML
- **SOUL.md** §AD Attack Matrix — Credential Acquisition (Responder, mitm6, Kerberoasting, DCSync)
- **malware-dev** §3 — Credential theft patterns from source
- **cloud-iam-attacks** — iam:CreateAccessKey, iam:UpdateLoginProfile

### Lateral Movement
- **windows-red-team** § — (implicit in AD attacks)
- **SOUL.md** §AD Attack Matrix — Lateral Movement (PSExec, WMI, WinRM, Pass-the-Hash/Ticket, Overpass-the-Hash, DCOM, SSH)
- **infrastructure-attacks** §RDP — Session stealing, RDP shadowing, Pass-the-Hash
- **infrastructure-attacks** §SMB/FTP — Service exploitation for pivoting

### Process Injection
- **windows-red-team** §2 — 30 injection methods: Classic (4), Stealth (6), APC-based (3), Advanced (10), API manipulation (7)
- **SOUL.md** §Process Injection — Linux SYS_CLONE+mprotect, memfd+LD_PRELOAD, Reflective DLL, Process Hollowing, Windows RemoteTask

### Reconnaissance / Discovery
- **wordpress-recon** §Phase 0-4 — WP-specific: REST namespace enum, version fingerprinting, nonce extraction, error exploitation
- **testing-methodology** §Phase 1 — 10 information gathering tests
- **bughunter-methodology** §Phase 2 — RECON pipeline
- **mission-orchestrator** §Phase 1 — Cartography (network, web, source code)
- **infrastructure-attacks** §Network Service Exploitation — Quick service identification
- **threat-intel** — MITRE ATT&CK Reconnaissance (TA0043) and Discovery (TA0007)

### Post-Exploitation / Collection
- **infrastructure-attacks** §Linux Privesc — Post-exploit enumeration
- **windows-red-team** §3 — Credential dumping
- **malware-dev** §3 — Credential theft from real RAT source
- **SOUL.md** §Pivot — ARP dump, DNS cache, routing tables, cred/SSH key exfil, domain trust enumeration
- **threat-intel** — MITRE ATT&CK Collection (TA0009)

### Exploit Development
- **exploit-development** §2 — Stack BOF complete workflow (crash→offset→verify→bad chars→jump→shellcode)
- **exploit-development** §3 — SEH exploitation
- **exploit-development** §4 — Egg hunting
- **exploit-development** §5-10 — DEP/ASLR/GS/SafeSEH/SEHOP bypass, ROP, heap spray, UAF, kernel exploitation
- **exploit-development** §shellcode — Win32/x64/Linux shellcode writing
- **browser-exploitation** — JS engine exploitation (V8, JSC, SpiderMonkey, ChakraCore)
- **SOUL.md** §Exploit Development First Principles — Primitive decomposition, trust boundary mapping, fuzzer's intuition, patch diff analysis, gadget chain construction
- **pwn2own-exploitation** — Real contest exploit chains

### Orange Tsai Attack Classes
- **orange-tsai-methodology** — Core philosophy, 4 pillars, research methodology
- **SOUL.md** §Orange Tsai Attack Classes — 10+ classes, 48 CVEs
- **SOUL.md** §WorstFit — Windows ANSI Best-Fit (CVE-2024-4577)
- **SOUL.md** §Confusion Attacks — Apache HTTP (9 CVEs, 20 techniques)
- **SOUL.md** §URL Parser Cross-Language Confusion Matrix — 5+ languages
- **SOUL.md** §SSRF Bypass — 10 URL parser differential techniques
- **SOUL.md** §Encoding Conversion Vulnerabilities — Cross-cutting theme
- **SOUL.md** §Cache Attack Methodology — 3 classes
- **SOUL.md** §ProxyLogon/ProxyShell/ProxyOracle/ProxyRelay — Full MS Exchange chains
- **SOUL.md** §Jenkins Meta-Programming Groovy AST — 7 CVEs
- **SOUL.md** §SSL VPN RCE Patterns — Fortinet, Pulse Secure, Citrix, Palo Alto

### Bug Bounty Methodology
- **bughunter-methodology** — 6-phase workflow, 7-Question Gate, 47 vulnerability classes
- **h1-bug-bounty-patterns** — Real-world frequency ranking, payout spectrum, top chains
- **SOUL.md** §Engagement Modes — Bug bounty vs red team vs pentest vs full spectrum
- **SOUL.md** §7-Question Gate — Validation framework
- **SOUL.md** §Never Submit list — 8 no-submit items
- **SOUL.md** §Kill Chain — SCOPE→RECON→HUNT→VALIDATE→CAPTURE→REPORT→PIVOT→REPEAT
- **SOUL.md** §Report — HackerOne impact-only, Bugcrowd VRT, red team DOCX
- **testing-methodology** — OWASP WSTG v4.2 (150+ test cases)

### Modern Web Attack Paradigms
- **SOUL.md** §PostMessage Attack Vectors — wildcard, indexOf bypass, null origin, prototype pollution+XSS, Math.random PRNG prediction
- **SOUL.md** §XS-Leak Techniques — 33 methods (11 event handler + 5 global limit + 17 Performance API)
- **SOUL.md** §Web Cache Deception — CDN path traversal, Fat GET, Parameter Cloaking
- **SOUL.md** §HTTP Request Smuggling — CL.0/TE.0/0.CL, TRACE desync, Pingora 2026

---

## V. SOUL.md SECTION QUICK REFERENCE

| § | Title | Maps To |
|---|-------|---------|
| Constitutional Directives | I-X (DO NOT STOP through NO FABRICATION) | bughunter-methodology, mission-orchestrator |
| Engagement Modes | Bug Bounty / Red Team / Pentest / Full Spectrum | bughunter-methodology §Phase 1 |
| Kill Chain | SCOPE→RECON→HUNT→VALIDATE→CAPTURE→REPORT→PIVOT | All methodology skills |
| RECON | Subdomain→live host→URL crawl→GF→nuclei→JS grep | mission-orchestrator, testing-methodology |
| HUNT | 47 vulnerability classes, methodology per class | web-attacks, bughunter-methodology |
| 7-Question Gate | Validation framework | bughunter-methodology |
| Never Submit | 8 items (unless chained) | bughunter-methodology, h1-bug-bounty-patterns |
| A→B Chain Table | 20+ pre-mapped chains | All exploitation skills |
| RCE Chains | 12+ full RCE paths | exploit-development, web-attacks |
| IAM Escalation Chains | 5 cloud escalation paths | cloud-iam-attacks |
| AD Escalation Chains | 5 AD escalation paths | windows-red-team |
| Social Engineering Chains | 6 SE chains | social-engineering-wireless |
| Wireless/RF Chains | 7 wireless chains | social-engineering-wireless |
| H4CKER AI Chains | 5 AI attack chains | ai-ml-attacks |
| H4CKER Automotive Chains | 3 automotive chains | embedded-iot-attacks, pwn2own-exploitation |
| H4CKER IoT Chains | 3 IoT chains | embedded-iot-attacks |
| H4CKER Cloud Orchestration Chains | 3 cloud chains | infrastructure-attacks, cloud-iam-attacks |
| File Upload Bypass | 10 techniques | web-attacks, wordpress-pentesting |
| SQLi Injection Classes | 12+ classes | web-attacks §1 |
| Auth Bypass Classes | 12+ classes | web-attacks |
| XS-Leak Techniques | 33 methods | web-attacks |
| PostMessage Attack Vectors | 8 vectors | web-attacks |
| SAML Attack Classes | 8 XSW variants | web-attacks |
| HTTP Request Smuggling | CL.0/TE.0/0.CL, Pingora 2026 | web-attacks |
| Web Cache Deception | 3 classes | web-attacks |
| Kerberos Attacks | 10 techniques | windows-red-team |
| DACL Abuse | BloodHound edges (10+) | windows-red-team |
| Malware Persistence | 8 patterns | malware-dev |
| RAT C2 Crypto | 5 patterns | malware-dev |
| Worm Self-Replication | Mirai full pattern | malware-dev |
| Process Injection | 4 techniques | windows-red-team, malware-dev |
| Token Manipulation | 5 techniques | windows-red-team |
| Credential Theft | 3 patterns | malware-dev, windows-red-team |
| Orange Tsai Attack Classes | 10+ classes, 48 CVEs | orange-tsai-methodology |
| Pwn2Own Patterns | Exploit chains, primitives, categories | pwn2own-exploitation |
| Cloudflare Bypass | Technique catalogue | cloudflare-bypass |
| Conference Attack Techniques | BlackHat/USENIX/DEF CON classes | Various |
| Evasion & Anti-Detection | AMSI, ETW, syscall, payload, log | windows-red-team |
| Tool Command Templates | nmap, nuclei, ffuf, sqlmap, hydra, netexec, impacket, interactsh, cewl, john/hashcat | All |
| ProjectDiscovery Tools | nuclei, httpx, subfinder, naabu, katana, interactsh | awesome-redteam-toolkit |
| Privesc Decision Tree | Linux 13 + Windows 13 | infrastructure-attacks, windows-red-team |
| AD Attack Matrix | Recon→Escalate→Lateral→Persist→Exfil | windows-red-team |

---

## VI. SKILL COVERAGE GRID

| Skill | Vuln Classes | Attack Surfaces | Tools | Techniques |
|-------|-------------|----------------|-------|------------|
| **web-attacks** | SQLi, XSS, SSRF, XXE, SSTI, CMDi, File Upload, JWT, Deserialization, GraphQL, NoSQL, Prototype Pollution, Request Smuggling, Cache Poisoning, CSRF, CORS, Info Disclosure, Clickjacking, WebSockets, Race Conditions, Host Header, Path Traversal, API Testing, Web LLM, DOM-based, Business Logic | Web apps, APIs | sqlmap, dalfox, gopherus, Burp, nuclei, ffuf | 60+ categories with payloads |
| **browser-exploitation** | JIT type confusion, UAF, sandbox escape | Chrome, Safari, Firefox, Edge | Fuzzilli, domato, WinDbg, rr | addrof/fakeobj, int64.js, OOB R/W |
| **infrastructure-attacks** | Linux privesc, container escape, network services | Linux, Docker, K8s, SMTP, FTP, RDP, DNS | nmap, linpeas, smtp-user-enum | Capabilities exploit, chroot escape, SMTP smuggling |
| **windows-red-team** | Defense evasion, credential dump, AD attacks, AD CS ESC1-13, Kerberos, DACL | Windows AD, enterprise | Mimikatz, BloodHound, Certipy, Impacket, Rubeus, NetExec | 27 evasion, 30 injection, DCSync, Kerberoasting, PtH/PtT |
| **exploit-development** | Stack BOF, SEH, ROP, DEP/ASLR bypass, heap spray, UAF, kernel, shellcode | Win32, Linux, browsers | Immunity, WinDbg, GDB, mona, pwntools, Metasploit | Full pipeline from fuzzing to shellcode |
| **malware-dev** | Persistence, C2 crypto, credential theft, process injection, worm replication | Windows, Linux, C2 implants | QuasarRAT, Mirai, Sliver, Pupy source | 8 persistence, 5 crypto, 4 injection |
| **cloudflare-bypass** | IUAM, Turnstile, WAF, Bot Fight Mode, fingerprinting | Cloudflare, anti-bot | CloakBrowser, undetected-chromedriver, patchright, cloudscraper | 6-layer bypass, cookie relay, origin IP discovery |
| **mobile-attacks** | WebView attacks, deeplink hijacking, tapjacking | Android, iOS | apktool, jadx, Frida, objection, adb | Smali modification, SSL pinning bypass, root detection bypass |
| **embedded-iot-attacks** | Firmware extraction, UART/JTAG, SPI/I2C, CAN bus, UEFI, side-channel | IoT, ICS, SCADA, automotive | binwalk, unblob, QEMU, OpenOCD, flashrom, pulseview | Hardware debug, protocol exploitation, fault injection |
| **cloud-iam-attacks** | IAM privilege escalation, persistence, GuardDuty evasion | AWS, cloud | AWS CLI, Pacu, ScoutSuite, Enumerate-IAM | 30 escalation paths, 10+ persistence |
| **ai-ml-attacks** | Model RCE, prompt injection, Hydra metadata, MCP attacks | AI/ML systems | InvokeAI, PyTorch, langchain | 16 CVEs, jailbreaks, indirect injection |
| **social-engineering-wireless** | Phishing, WiFi cracking, RFID cloning, BadUSB, physical | Social, wireless, physical | GoPhish, EvilGinx, aircrack-ng, Proxmark3, HackRF | Credential harvesting, MFA bypass, rogue AP, BLE spoofing |
| **pwn2own-exploitation** | Logic bug chains, memory corruption, kernel EoP | Browsers, mobile, ICS, automotive | wtf, syzkaller, Jandroid | Chainspotting methodology, OPC UA exploitation |
| **wordpress-pentesting** | Plugin exploitation, form abuse, file upload bypass | WordPress | wpscan, curl | REST API recon, CF7 exploitation, Elementor config extraction |
| **wordpress-recon** | Plugin enumeration, version fingerprinting, nonce extraction | WordPress | curl, jadx | Single-request plugin discovery, error message exploitation |
| **threat-intel** | MITRE ATT&CK TTPs, OWASP Top 10, 178 threat groups | Enterprise, mobile, ICS | - | APT emulation, campaign planning |
| **bughunter-methodology** | 47 vulnerability classes, A→B chain table, 7-Question Gate | Bug bounty, red team, pentest | All | 6-phase workflow, DO NOT STOP directive |
| **orange-tsai-methodology** | Parser differentials, encoding conversion, WorstFit, Apache Confusion, ProxyLogon | Web servers, reverse proxies, parsers | - | 10+ attack classes, 48 CVEs |
| **testing-methodology** | WSTG v4.2 (150+ tests) | Web apps | nmap, Burp, Nuclei | 12-phase testing workflow |
| **h1-bug-bounty-patterns** | XSS, IDOR, SSRF, RCE, SQLi, ATO, File Upload, Business Logic, Subdomain Takeover | Bug bounty programs | All | 10 god chains, real frequency rankings, payout spectrum |
| **mission-orchestrator** | All (orchestration) | All target types | All | Autonomous engagement engine |
| **awesome-redteam-toolkit** | All (tool catalogue) | All | 556 repos across 16 categories | Full toolkit reference |
| **kali-tools-arsenal** | All (tool catalogue) | All | 774 tools across 21 categories | Quick tool selection |
| **defensive-forensics** | Memory forensics, network forensics, disk forensics, YARA triage, CIS Controls | Memory, network, disk | Volatility3, Wireshark, tshark, Snort, dd | Live triage, malware detection, timeline analysis |

---

Generated from: 17 exploitation skills + 5 methodology skills + 2 playbook skills + SOUL.md
Total skill files analyzed: 25
