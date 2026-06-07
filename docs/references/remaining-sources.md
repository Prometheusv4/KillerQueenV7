# Remaining Security Sources — Consolidated Knowledge Reference

Generated for Killer Queen project — extracted June 2025.

---

## 1. PENTESTER.LAND/WRITEUPS
**URL:** https://pentester.land/writeups/

### What It Provides
- Manually curated directory of thousands of bug bounty, responsible disclosure, and pentest writeups.
- Each entry includes: Title, Tags (vulnerability types), Target Program/Organization, Author (with Twitter handle), Bounty amount (USD), Publication Date.
- Downloadable as a single JSON file (~2.4MB) at https://pentester.land/writeups.json
- Searchable/sortable table — filter by tag (RCE, SSRF, XSS, IDOR, etc.), program (Google, Facebook, PayPal, etc.), author, bounty.
- Also publishes "The 5 Hacking NewsLetter" with weekly curated resources.
- Blog with conference notes and technique deep-dives.

### Best Techniques & Patterns Found
- **Tag-based filtering** reveals common bug classes across thousands of writeups:
  - Cross-Site Scripting (XSS)
  - Server-Side Request Forgery (SSRF)
  - Insecure Direct Object Reference (IDOR)
  - SQL Injection (SQLi)
  - Remote Code Execution (RCE)
  - Cross-Site Request Forgery (CSRF)
  - Authentication Bypass
  - Race Condition
  - Subdomain Takeover
  - 2FA Bypass
  - CORS Misconfiguration
  - Local File Inclusion (LFI)
- **High-value techniques from newsletters:**
  - Race Condition → RCE via file upload: exploit short window where uploaded file is temporarily stored on server before moving to S3; send reverse shell request during that window.
  - WAF bypass via "secondary contexts": identify other security appliances (e.g., Bluecoat proxy) in the request path and abuse parser differentials to slip payloads past WAF.
  - IDOR beyond simple ID incrementation: test encoded/hashed IDs, add IDs to requests that don't normally include them, change HTTP methods.
  - Parser differentials for file upload bypass.
- **Top programs targeted:** Google, Microsoft, Facebook, PayPal, Uber, Yahoo, Tesla, Amazon.
- **Highest bounties** cluster around RCE, SSRF, and auth bypass on critical assets.

### How Killer Queen Would Use This
- **Training data:** Download the JSON, parse writeups by vulnerability tag, extract technique descriptions for pattern recognition.
- **Prioritization:** Sort by bounty amount to identify highest-impact bug classes.
- **Target reconnaissance:** Search for specific program names to learn what vulns have been found before — reveals attack surface and security maturity.
- **Technique extraction:** Parse newsletter archives for concrete exploitation methodologies (race condition → RCE, WAF bypass chains, parser differentials).
- **Trend analysis:** Track publication dates to identify which vulnerability types are gaining/losing prevalence.

### Deep-Dive Priority Sections
- `writeups.json` full download for bulk analysis
- Newsletter archive: https://pentester.land/blog/ (technique-rich)
- Filter for `$5000+` bounties for highest-impact patterns

---

## 2. RMUSSER01/INFOSEC_REFERENCE
**URL:** https://github.com/rmusser01/Infosec_Reference

### What It Provides
- Massive information security reference — "Yellow Pages" for infosec knowledge.
- 541+ commits. HTML version: https://rmusser.net/docs
- Each topic is a separate markdown file in the `Draft/` directory.
- Covers offensive, defensive, and operational security.

### Table of Contents / Categories (Complete from README)
```
Pre-ATT&CK                          ATT&CK Stuff
Attacking & Securing Active Directory
Anonymity/OpSec/Privacy             Basic Security Information
BIOS/UEFI/Firmware Attacks/Defense   Building a Testing Lab
Car Hacking                         Career
Cheat Sheets                        Cloud
Conferences/Recordings              Containers
Courses & Training                  Cryptography & Encryption
CTFs & Wargames                     Darknets
Data Analysis & Visualization       Defense
Documentation & Reporting           Embedded Device Security
Exfiltration                        Exploit Development
Forensics                           Fuzzing
Hardware Hacking                    ICS/SCADA
Incident Response                   iOS
Linux                               Lock Picking / Physical Security
Logging & Monitoring                macOS
Malware Analysis                    Mobile Security
Network Security                    OSINT
Password Cracking & Attacks         Phishing / Social Engineering
Policy & Governance                 Post Exploitation
Privilege Escalation                Programming / Scripting
Red Teaming                         Reverse Engineering
RFID/NFC                            SDR (Software Defined Radio)
Security Tools                      SIEM
Social Engineering                  Threat Intelligence
VoIP                                Vulnerable Apps/Machines
Web Application Security            Windows
Wireless Security                   Writing/Presenting
```

### Sampled Deep-Dive: Cloud Section
- **Cloud-Agnostic Tools:** ScoutSuite (multi-cloud audit), CCAT (container attack), PacBot (compliance), Cloud Custodian (rules engine), CloudSploit (security scans).
- **AWS Attack Techniques:** DNS-based break-out from isolated networks (AmazonProvidedDNS bypasses security groups), IAM privilege escalation methods (21+ escalation paths documented), metadata SSRF → credential theft.
- **Key Talks:** Becky Weiss on AWS security fundamentals, Ben Potter on Well-Architected security.

### Sampled Deep-Dive: Building a Lab
- **Hypervisors:** VirtualBox, VMware Workstation/ESXi, Proxmox, Xen.
- **Vulnerable VMs:** Vulnhub, DetectionLab (Windows domain + security tooling), CloudGoat (vulnerable-by-design AWS), DVCA (cloud privilege escalation), lambhack (serverless).
- **Automation:** SecGen (randomly vulnerable VMs), CyRIS (cyber range), DockerSecurityPlayground.

### How Killer Queen Would Use This
- **Knowledge graph:** Parse the entire `Draft/` directory to build a categorized reference of tools, techniques, and resources.
- **Tool discovery:** Each section lists specific tools — extract for capability mapping.
- **Lab building:** The Building a Lab section provides recipes for creating vulnerable environments to test against.
- **Cloud attack mapping:** The Cloud section details AWS/Azure/GCP attack paths that Killer Queen could simulate.
- **Defense evasion:** Anonymity/OpSec, Exfiltration, and Post Exploitation sections directly relevant to operational security.

### Deep-Dive Priority Sections
1. `Draft/Web Application Security.md`
2. `Draft/Privilege Escalation.md`
3. `Draft/Post Exploitation.md`
4. `Draft/Exfiltration.md`
5. `Draft/AnonOpSecPrivacy.md`
6. `Draft/Cloud.md` (already partially extracted)
7. `Draft/Red Teaming.md`

---

## 3. 0XINFECTION REPOSITORIES (Beyond Awesome-WAF)
**URL:** https://github.com/0xInfection?tab=repositories
**Author:** Pinaki (@watchtowrlabs)

### Key Repositories (Beyond Awesome-WAF)

| Repository | Description | Usefulness |
|---|---|---|
| **XSRFProbe** | Prime CSRF/XSRF audit and exploitation toolkit. Advanced CSRF detection with multiple request generation strategies. | HIGH — automated CSRF testing, multi-vector probing |
| **TIDoS-Framework** | Offensive manual web application penetration testing framework. Modules: recon, scanning, enumeration, vulnerability assessment. | HIGH — all-in-one web app pentest, 5-phase attack |
| **SIPTorch** | SIP torture testing framework (RFC 4475). Tests SIP implementations for robustness. | MEDIUM — VoIP/SIP target assessment |
| **LogMePwn** | Fully automated Log4J RCE scanner for CVE-2021-44228. Super-fast, reliable, multi-vector validation. | HIGH — Log4Shell scanning, still relevant for unpatched systems |
| **EPScalate** | Exploit for EoP in QuickHeal Seqrite EPS (CVE-2023-31497). | LOW-MEDIUM — specific CVE exploit, reference for EoP technique |
| **PewSWITCH** | FreeSWITCH scanning/exploitation toolkit for CVE-2021-37624 and CVE-2021-41157. | MEDIUM — VoIP infrastructure exploitation |
| **vulninfra** | Finds secrets, tokens, and developer mistakes in codebases/infrastructure. | HIGH — secret scanning, cred discovery |
| **Bludger** | GitHub Actions automation toolkit. | MEDIUM — CI/CD pipeline interaction |

### How Killer Queen Would Use These
- **TIDoS-Framework:** Integrate as a web application assessment module — full recon-to-exploitation pipeline.
- **XSRFProbe:** Add CSRF testing to automated assessment workflows, especially for authenticated endpoints.
- **LogMePwn:** Include in initial reconnaissance phase for any Java-based target to check for Log4Shell.
- **vulninfra:** Use for secret/token discovery during target enumeration.
- **PewSWITCH + SIPTorch:** VoIP/SIP target assessment for telecom-adjacent targets.

---

## 4. VOULNET REPOSITORIES (Beyond barq)
**URL:** https://github.com/Voulnet?tab=repositories
**Author:** Mohammed ALDOUB

### Key Repositories (Beyond barq)

| Repository | Description | Usefulness |
|---|---|---|
| **barq** | AWS Cloud Post-Exploitation Framework (already cataloged separately) | HIGH |
| **DVSA** | Damn Vulnerable Serverless Application — OWASP project. Vulnerable AWS serverless app with Cognito, Lambda, DynamoDB, SQS, SES. | HIGH — serverless security training/testing |
| **DVFaaS** | Damn Vulnerable Functions as a Service — intentionally vulnerable serverless functions for understanding serverless-specific vulns. | HIGH — serverless vulnerability research |
| **InjectMyServerlessEvent** | Sample AWS Lambda with Serverless Event Injection (OS command injection). | MEDIUM — demonstrates Lambda event injection technique |
| **Kuiper** | Digital Investigation Platform. | MEDIUM — forensics/IR tooling |
| **desharialize** | Tool related to deserialization (details sparse — likely deserialization exploitation/testing). | MEDIUM — deserialization research |
| **webhandler** | Bash simulator to control a server using PHP system functions (post-exploitation web shell). | MEDIUM — post-exploitation persistence |
| **CVE-2017-8759-Exploit-sample** | Exploit sample for CVE-2017-8759 (.NET framework RCE). | LOW — old CVE, reference value |
| **training-schedule** | Mohammed's public security training courses schedule. | LOW — learning resource pointer |

### How Killer Queen Would Use These
- **DVSA + DVFaaS:** Deploy as training ranges for serverless-specific attack techniques (event injection, IAM misconfigurations, function chaining).
- **InjectMyServerlessEvent:** Study the event injection pattern — applicable to any event-driven serverless architecture.
- **barq + serverless tools:** Combine for comprehensive cloud post-exploitation across both traditional cloud resources and serverless functions.
- **desharialize:** Use for deserialization vulnerability testing and exploitation development.
- **webhandler:** Reference implementation for web-shell-based command and control.

---

## 5. CLOUDFLARE-BYPASS (GitHub Topic — 242 Repos)
**URL:** https://github.com/topics/cloudflare-bypass

### Overview
242 public repositories tagged with `cloudflare-bypass`. These cover bot detection evasion, anti-scraping bypass, and DDoS protection circumvention. Categories include browser automation patches, proxy solutions, DDoS tools, and scraping frameworks.

### Top 10 Most Useful Tools/Techniques

| # | Tool | Technique | Why Useful |
|---|---|---|---|
| 1 | **ultrafunkamsterdam/undetected-chromedriver** | Patched Selenium Chromedriver — zero-config bypass of Distil/Imperva/DataDome/Cloudflare IUAM. | Most battle-tested; passes all major bot mitigation systems. Python-native. |
| 2 | **VeNoMouS/cloudscraper** | Python module that solves Cloudflare's JavaScript challenge by extracting and executing the challenge server-side. | Lightweight, doesn't require a browser. Good for API-style access. |
| 3 | **sarperavci/CloudflareBypassForScraping** | Cloudflare verification bypass specifically designed for scraping workflows. | Purpose-built for scraping; handles both JS challenge and Turnstile. |
| 4 | **CloakHQ/CloakBrowser** | Stealth Chromium with source-level fingerprint patches. Drop-in Playwright replacement. 30/30 bot detection tests passed. | Most comprehensive browser fingerprinting bypass. Playwright-compatible. |
| 5 | **Kaliiiiiiiiii-Vinyzu/patchright** | Undetected Playwright — patches CDP leaks at the browser level. Both Python and Node.js versions. | Modern alternative to undetected-chromedriver for Playwright users. |
| 6 | **cdpdriver/zendriver** | Blazing fast async undetectable web automation based on nodriver. Docker support. | Performance-focused; async-first; containerized deployment ready. |
| 7 | **ZFC-Digital/puppeteer-real-browser** | Puppeteer plugin that makes browser appear as a real user's browser, not an automation tool. | For Node.js/JS automation pipelines using Puppeteer. |
| 8 | **vvanglro/cf-clearance** | Extracts and reuses `cf_clearance` cookies — solve once, reuse with same IP+UA. | Minimal overhead; cookie-based bypass for repeat access. |
| 9 | **NoahCardoza/CloudProxy** | Proxy server that sits between your tool and the target, handling Cloudflare challenges transparently. | Architecture-friendly — no code changes to existing tools. |
| 10 | **omkarcloud/botasaurus** | "All in One Framework to Build Undefeatable Scrapers." Full framework approach. | Complete scraping framework with Cloudflare bypass built in. |

### Categorization by Technique
- **Browser Patching:** undetected-chromedriver, patchright, CloakBrowser, puppeteer-real-browser, botasaurus
- **JS Challenge Solving:** cloudscraper, cf-clearance
- **Proxy-Based:** CloudProxy, pupflare
- **DDoS-Specific:** MHDDoS, KARMA-DDoS (note: mainly for DDoS, not scraping)
- **AI/Agent-Focused:** camofox-browser, stealth-browser-mcp, vakra-dev/reader

### How Killer Queen Would Use These
- **Target enumeration:** Use cloudscraper or cf-clearance to scrape Cloudflare-protected targets for reconnaissance.
- **Authenticated testing:** undetected-chromedriver or patchright for browser-based authenticated testing of Cloudflare-protected apps.
- **API access:** cf-clearance cookie approach for lightweight, repeatable API access to Cloudflare-protected endpoints.
- **Operational security:** Avoid tools in the DDoS category unless testing resilience.
- **Preferred stack:** undetected-chromedriver (Python) + cloudscraper (Python) for most use cases; patchright if Playwright is preferred.

---

## 6. SECURITYTRAILS (GitHub Topic — 8 Repos)
**URL:** https://github.com/topics/securitytrails

### Overview
8 public repositories using the SecurityTrails API for domain intelligence, DNS reconnaissance, and subdomain discovery.

### All 8 Repositories

| Repository | Description | Usefulness |
|---|---|---|
| **badchars/osint-mcp-server** | OSINT MCP server for AI agents — 37 tools, 12 sources including SecurityTrails, Shodan, VirusTotal, Censys, DNS recon, WHOIS, cert transparency, BGP, Wayback, GeoIP. | HIGHEST — comprehensive OSINT for AI agents via MCP protocol |
| **Macmod/NameScraper** | Selenium scraper for public domain search tools. | MEDIUM — domain discovery |
| **xpl0ited1/submonitor** | Subdomain monitor with Slack/Discord/Telegram reporting. | HIGH — continuous subdomain monitoring with alerts |
| **HanibalAntePortas/get-acq** | Gather companies acquired by a given domain via SecurityTrails API. | MEDIUM — acquisition mapping for attack surface expansion |
| **hrbrmstr/securitytrails** | R package: Tools to query SecurityTrails API. | LOW — R ecosystem only |
| **SaidSecurity/OSINT-tool-Telegram-Bot** | Telegram bot for domain intelligence (DNS, IP, subdomains) via SecurityTrails API. | MEDIUM — convenient interface for mobile OSINT |
| **akioukun/perses** | Simple subdomain fetcher using SecurityTrails API. | LOW-MEDIUM — lightweight subdomain discovery |
| **hangmansROP/securitytrailsapi** | Python wrapper around SecurityTrails API. | MEDIUM — reusable API wrapper |

### How Killer Queen Would Use These
- **osint-mcp-server (highest value):** If Killer Queen uses Model Context Protocol (MCP), this provides 37 OSINT tools natively. Direct integration for automated attack surface mapping.
- **submonitor:** Set up continuous subdomain monitoring on targets — alert on new subdomains for expanded attack surface.
- **get-acq:** Map corporate acquisitions to find forgotten/less-secured subsidiary domains.
- **perses + securitytrailsapi:** Basic subdomain enumeration building blocks for custom recon pipelines.

---

## CROSS-SOURCE PATTERNS & SYNTHESIS

### Killer Queen Integration Roadmap

1. **Reconnaissance Layer:** Combine pentester.land program data + SecurityTrails API tools + cloudflare-bypass for access.
2. **Vulnerability Knowledge Base:** Parse pentester.land writeups JSON to build a tagged database of exploitation techniques organized by vuln class.
3. **Lab Environment:** Use Infosec_Reference lab-building guides + Voulnet's DVSA/DVFaaS to create test ranges.
4. **Tool Arsenal:** 
   - Web assessment: TIDoS-Framework + XSRFProbe (0xInfection)
   - Cloud exploitation: barq (Voulnet) + CloudGoat/ScoutSuite (from Infosec_Reference)
   - Serverless: DVSA, DVFaaS, InjectMyServerlessEvent (Voulnet)
   - WAF bypass: Awesome-WAF (0xInfection) + pentester.land secondary context techniques
   - Browser automation: undetected-chromedriver + cloudscraper
5. **Continuous Monitoring:** submonitor (SecurityTrails ecosystem) + LogMePwn (0xInfection) for vulnerability scanning.

### Highest-Value "Quick Wins"
- pentester.land JSON → extract all `$10,000+` bounty writeup techniques
- Infosec_Reference's `Privilege Escalation` and `Post Exploitation` sections
- undetected-chromedriver for any Cloudflare-protected target access
- osint-mcp-server for comprehensive passive recon via MCP
- DVSA deployment for serverless attack training

### Gaps / Needs Further Investigation
- pentester.land: Actual JSON parsing needed (2.4MB file — requires local download and analysis)
- Infosec_Reference: Only Cloud and Lab sections deep-dived; 40+ other sections need extraction
- 0xInfection: TIDoS-Framework module listing needed for full capability mapping
- Voulnet: desharialize needs deeper investigation (sparse public description)
- cloudflare-bypass: Only top 20 of 242 repos reviewed; others may contain specialized techniques
