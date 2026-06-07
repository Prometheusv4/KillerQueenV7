# Killer Queen — Knowledge Synthesis (June 5, 2026)
# Sources: 20+ academies, wikis, research papers, tools, 44 books
# Consolidated for persistent agent memory

---

## SOURCE INVENTORY

### DOWNLOADED TO DISK:
- PayloadsAllTheThings: 58 files (620KB) — all 65+ vuln categories
- HackTricks: 12 valid pages (3MB) — XSS, Deser, SSTI, SQLi, SSRF, File Upload, HTTP Smuggling, SAML
- thehacker.recipes: 13 pages (1.7MB) — Kerberos, NTLM Relay, DACL, SSTI, SQLi, SSRF, XSS
- pentester.land: 153 posts indexed, writeup collections downloaded
- Infosec_Reference: 45+ categories mapped
- 44 books converted: 26MB text (No Starch Press, Wiley, Packt)

### ABSORBED VIA LIVE EXTRACTION:
- PortSwigger Academy: HTTP Smuggling, File Upload→RCE, JWT, Deserialization, SSTI
- James Kettle Research: SAML Bypass, Email Atom Splitting, URL Validation Bypass, Top 10 2025
- Awesome-WAF: 50+ vendor fingerprints
- Cloudflare bypass: Top 19 of 238 repos cataloged
- 0xInfection: XSRFProbe (CSRF toolkit v2.3)
- Voulnet: desharialize (CVE-2019-0604 SharePoint RCE), DVSA (serverless vuln app)
- ProjectDiscovery: Nuclei, Subfinder, HTTPx, Katana, Naabu, Interactsh, Uncover

### BLOCKED:
- hackingthe.cloud: mkdocs SPA, needs live site (not GitHub raw)
- pentester.land JSON API: requires JavaScript
- HackerOne Hacktivity: not yet accessed

---

## KEY TECHNIQUES SYNTHESIZED

### HTTP Request Smuggling (PortSwigger + HackTricks)
5 attack variants:
- CL.TE: Front-end CL, Back-end TE → prefix smuggling
- TE.CL: Front-end TE, Back-end CL → prefix smuggling
- TE.TE: Obfuscation tricks (xchunked, space, case, \x0b)
- H2.CL: HTTP/2 front-end downgrade → injected Content-Length
- H2.TE: HTTP/2 → HTTP/1, Transfer-Encoding survives downgrade
- CL.0: Content-Length: 0, back-end ignores body
Advanced: Response Queue Poisoning, CRLF injection in HTTP/2 headers, browser-powered desync

### File Upload → RCE (PayloadsAllTheThings + HackTricks + PortSwigger)
6-tier extension bypass ladder:
1. Basic: .php, .php5, .phtml, .phar, .shtml, .inc
2. Case: .pHp, .PHP5, .PhAr
3. Special chars: null byte, trailing dot, space, CRLF, slash
4. NTFS ADS: shell.asp:.jpg, shell.asp::$data
5. Double extensions: shell.php.jpg, shell.jpg.php
6. Length truncation: 256+ char filename drops extension
Server config abuse: .htaccess (AddType), web.config (FastCGI handler)
Polyglots: GIF89a+PHP, PNG IDAT chunk encoding, JPEG exiftool injection, SVG XXE

### SQL Injection (HackTricks + PayloadsAllTheThings)
- Entry point detection: ', ", `, '), "), `) combinations
- Comments per DBMS: # (MySQL), -- (all), /* */ (all), /*! MYSQL */
- Confirmation: 1 or 1=1, 1' or '1'='1, timing per DBMS
- sleep(10)-MySQL, pg_sleep(10)-PostgreSQL, WAITFOR DELAY-MSSQL, DBMS_PIPE. RECEIVE_MESSAGE-Oracle
- UNION: ORDER BY/UNION SELECT null to find column count
- Blind: boolean-based, error-based, time-based
- DBMS identification: conv(), connection_id()-MySQL, @@CONNECTIONS-MSSQL, ROWNUM=ROWNUM-Oracle, 5::int=5-PostgreSQL

### SSTI (HackTricks + PayloadsAllTheThings + PortSwigger)
10+ template engines with full RCE chains:
- Jinja2: {{ ''.__class__.__mro__[2].__subclasses__()... }}
- FreeMarker: <#assign ex="freemarker.template.utility.Execute"?new()>
- Velocity: #set → Runtime.getRuntime().exec()
- Thymeleaf: T(java.lang.Runtime) via SpringEL
- Twig: _self.env.registerUndefinedFilterCallback("exec")
- ERB: <%= system('id') %>
- EJS: global.process.mainModule.require('child_process')
- Pebble: variable.getClass().forName('java.lang.Runtime')
- Jinjava: 'a'.getClass().forName('javax.script.ScriptEngineManager')
- Detection: {{7*7}}, ${7*7}, <%= 7*7 %>, ${{<%[%'"}}%
- WAF bypass: hex encoding, attr() instead of ., bracket notation

### JWT Attacks (PortSwigger)
- alg=none: strip signature, set algorithm to "none"
- Brute-force HS256: hashcat -m 16500
- Key confusion: change alg from RS256 to HS256, sign with public key
- JWK injection: embed attacker-controlled JWK in header
- jku header injection: point to attacker's JWK Set URL
- kid path traversal: ../../../../../dev/null or SQL injection

### SAML Authentication Bypass (James Kettle — The Fragile Lock)
- Attribute pollution: namespace-ignorant attribute lookups
- Namespace confusion: hide Signature from one parser, show to another
- Void canonicalization: trigger canonicalization error → empty string digest
- Replay any signed XML (not just SAML Assertions)

### Email Parser Bypass (Gareth Heyes)
- UUCP spoofing: ! character routes mail before the !
- Source routing: collab%attacker.com(@target.com
- Unicode overflows: PHP chr() modulus → generate @ from >255 codepoints
- Encoded-word RFC 2047: =?utf-7?q?...?= decodes to arbitrary characters
- GitHub Cloudflare Zero Trust bypass via email verification

### URL Validation Bypass (PortSwigger Cheat Sheet)
- IPv4 encodings: octal (0177.0.0.1), hex (0x7F.0x0.0x1), dword (2130706433)
- Unicode normalization: characters that normalize to nothing
- Multi-line regex bypass: U+2028/U+2029 line separators

### CORS Misconfigurations (HackTricks)
- Origin reflection: dynamic Access-Control-Allow-Origin
- Null origin: sandboxed iframe bypass
- Regex bypass: trusted.com.attacker.com
- Underscore in subdomain: application_.arbitrary.com
- Private Network Access: 0.0.0.0 bypass

### NTLM Relay (thehacker.recipes)
- Cross-protocol relay: SMB→HTTP, HTTP→LDAPS
- MIC bypass: NTLMv1 doesn't include MIC, can be dropped
- CVE-2019-1040: unsigning relay on unpatched systems
- Session signing: protects session integrity, not auth integrity
- EPA: channel binding, service binding

### Kerberos Attacks (thehacker.recipes)
- ASREPRoast: pre-auth disabled users, crack TGT offline (hashcat 18200)
- Kerberoast: request TGS for SPN accounts, crack offline (hashcat 13100)
- S4U2Self: service obtains ticket to itself for any user
- S4U2Proxy: service uses forwardable ticket to access another service
- Delegations: unconstrained (KUD), constrained (KCD), resource-based (RBCD)
- Bronze Bit: CVE-2020-17049 delegation bypass

### Top 10 Web Hacking 2025 (James Kettle)
1. Error-Based SSTI (Vladislav Korchagin)
2. ORM Leaking (Alex Brown)
3. Novel SSRF via HTTP Redirect Loops (Shubs)
4. Unicode Normalization Attacks (Barnett & Barnett)
5. SOAPwn: .NET RCE via HTTP Client Proxies
6. Cross-Site ETag Length Leak
7. Next.js Cache Poisoning
8. XSS-Leak: Cross-Origin Redirects
9. HTTP/2 CONNECT Port Scanning
10. Parser Differentials

### SharePoint RCE — CVE-2019-0604 (Voulnet/desharialize)
- Unauthenticated RCE via XML deserialization
- XamlReader ExpandedWrapper containing XML payload
- Custom serialization: EntityInstanceIdEncoder.EncodeEntityInstanceId
- Dynamic Python payload generation without .NET dependency
- Detection: 71e9bce111e9429c in server logs

---

## TOOLS CATALOGED

### ProjectDiscovery Suite:
- Nuclei: YAML-based vuln scanner, thousands of community templates
- Subfinder: Passive subdomain enumeration
- HTTPx: HTTP probing with tech detection
- Katana: Headless crawling + JS parsing
- Naabu: Fast port scanning
- Interactsh: OOB interaction server (Burp Collaborator alternative)
- Uncover: Search engine aggregation for hosts

### Cloudflare Bypass Top 5:
1. undetected-chromedriver: Selenium driver bypassing all bot detection
2. cloudscraper: Python module to bypass Cloudflare anti-bot
3. patchright: Undetected Playwright fork
4. zendriver: Async-first undetectable web automation
5. cf-clearance: CF challenge pass-through with cookie reuse

### 0xInfection Tools:
- XSRFProbe v2.3: CSRF audit + exploit generation
- TIDoS Framework: 5-phase web pentest (Recon, Scan, Attack)
- LogMePwn: Log4Shell scanner
- SIPTorch: SIP protocol testing

### Voulnet Tools:
- barq: AWS post-exploitation (EC2 attacks, metadata dump, secrets extraction)
- desharialize: SharePoint CVE-2019-0604 exploitation
- DVSA: Damn Vulnerable Serverless Application (AWS)
- DVFaaS: Vulnerable serverless functions
- InjectMyServerlessEvent: Lambda OS injection
- Kuiper: Digital forensics framework

### Other Notable Tools:
- prowler: 600+ AWS checks, 167 Azure, 102 GCP, 83 K8s
- can-i-take-over-xyz: 80+ services with dangling DNS fingerprints
- shocens: Shodan + Censys query tool
- Prowler: Multi-cloud security scanning (15 providers)
- Broxy: HTTP/HTTPS intercept proxy (Go-based)
- barq: AWS Cloud Post Exploitation Framework

---

## BOOKS DEEP-READ

### Web Application Hackers Handbook 2nd Ed (Stuttard/Pinto — 49,698 lines)
- Burp Suite creators! Dafydd Stuttard = PortSwigger founder
- Ch7: Session Management — token analysis, Burp Sequencer, FIPS randomness tests, entropy measurement, at least 500 tokens for analysis, 5,000 for high confidence
- Ch8: Access Controls — IDOR via identifier iteration, admin=true parameter, Referer header trust testing, Burp Intruder credential harvesting, GUID unpredictability check
- Coverage: 21 chapters, Web App Security bible

### Web Hacking 101 (Peter Yaworski — 8,958 lines)
- 30 real bug bounty examples from Shopify, Google, Yahoo, Uber, United Airlines, Starbucks
- Chapters: Open Redirect, HPP, CSRF, CRLF, XSS, SSTI, SQLi, SSRF, Race Conditions, IDOR, OAuth, Application Logic
- Practical bug bounty methodology with real payouts

### Pentesting Azure Applications (Matt Burrough — 8,489 lines, No Starch Press)
- Ch1: Preparation — cloud-focused pentest scoping
- Ch2: Access Methods — subscription authentication
- Ch3: Reconnaissance — PowerShell scripts, subscription enumeration, resource groups, storage account keys, networking
- Ch4: Examining Storage — blob/table/queue/file access via SAS tokens and keys
- Ch5: Targeting VMs — VHD theft, password cracking, hashcat, credential reset
- Ch6: Investigating Networks — firewalls, VPNs, network bridging
- Ch7: Other Azure Services — Key Vault, Azure websites
- Ch8: Monitoring, Logs, Alerts

### RTFM v3 (Ben Clark — 12,658 lines)
- Quick reference: *NIX, Windows, Networking, Tips & Tricks, Tool Syntax, Web, Databases, Programming, Wireless
- Linux: cover tracks (clear auth.log, bash_history, export HISTSIZE=0, ln /dev/null ~/.bash_history)
- Scripting: ping sweeps, DNS reverse lookups, fork bombs, IP banning

### Hacker Playbook 2 (Peter Kim — 8,706 lines)
- Practical penetration testing: Kali setup, recon tools (Discover, EyeWitness, Masscan, Gitrob, CMSmap, SPARTA), exploitation (Burp, ZAP, SQLMap, BeEF, Responder, Veil, SET), post-exploitation (Mimikatz, PowerSploit, Nishang, WCE, SMBexec)
- Password cracking hardware: Radeon R9 295x2 8GB, 16GB RAM, i7-4790K
- Commercial tools: Burp Suite Pro, Canvas, Cobalt Strike, Core Impact, Nessus, Nexpose

---

## INFOSEC_REFERENCE — 45+ CATEGORIES MAPPED
Attack/Defense, AD, Anonymity/OpSec, Basic Security, BIOS/UEFI, Car Hacking, Career, Cheat Sheets, Cloud, Conferences, Containers, Courses, Cryptography, CTFs, Darknets, Data Analysis, Defense, Documentation, Embedded/IoT, Exfiltration, Exploit Development, Forensics/DFIR, Fuzzing/Bug Hunting, Game Hacking, Honeypots, Logging/Monitoring, Malware, Network Attacks, OSINT, Passwords, Phishing, Physical Security, Privilege Escalation, Programming Security, Red Teaming, Reverse Engineering, Rootkits, Social Engineering, System Internals, Threat Modeling, Web, Wireless/RF

---

STATUS: CONTINUOUS INGESTION — More sources being processed
