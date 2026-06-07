---
name: testing-methodology
description: OWASP WSTG v4.2 testing methodology — 150+ test cases organized by phase. Maps every test to Prometheus tools and attack skills. Systematic web application security testing workflow from recon through reporting.
category: methodology
trigger: testing methodology, WSTG, web pentest methodology, security testing guide, penetration testing process, testing checklist, web app assessment
---

# Web Security Testing Methodology — OWASP WSTG v4.2
Source: https://owasp.org/www-project-web-security-testing-guide/v42/
150+ test cases across 12 phases

---

## TESTING WORKFLOW — Phase by Phase

### PHASE 1: Information Gathering (4.1 — 10 tests)
Map the target before attacking.

| ID | Test | Tool | Load Skill |
|----|------|------|-----------|
| 4.1.1 | Search Engine Discovery | Google dorks, Shodan | kali-tools-arsenal |
| 4.1.2 | Fingerprint Web Server | whatweb, wappalyzer, nmap -sV | kali-tools-arsenal |
| 4.1.3 | Review Metafiles | robots.txt, sitemap.xml, .well-known | web-attacks |
| 4.1.4 | Enumerate Applications | gobuster, ffuf, feroxbuster | web-attacks |
| 4.1.5 | Review Content for Leaks | View source, JS maps, comments | web-attacks |
| 4.1.6 | Identify Entry Points | Burp Spider, katana, gospider | web-attacks |
| 4.1.7 | Map Execution Paths | Burp Repeater, manual browsing | web-attacks |
| 4.1.8 | Fingerprint Framework | Wappalyzer, WhatWeb, headers | kali-tools-arsenal |
| 4.1.9 | Fingerprint Application | Custom 404, cookie analysis | web-attacks |
| 4.1.10 | Map Architecture | nmap, masscan, DNS enum | infrastructure-attacks |

**Deliverable:** Full asset map, technology stack, entry points, architecture diagram

---

### PHASE 2: Configuration & Deployment (4.2 — 11 tests)
Find misconfigurations before attacking logic.

| ID | Test | Tool | Load Skill |
|----|------|------|-----------|
| 4.2.1 | Network Infrastructure | nmap, testssl.sh, SSL Labs | infrastructure-attacks |
| 4.2.2 | Application Platform Config | Nuclei, Nikto, header analysis | web-attacks |
| 4.2.3 | File Extension Handling | .bak, .old, .php~, .swp | web-attacks |
| 4.2.4 | Backup & Unreferenced Files | gobuster, dirb, common backup names | web-attacks |
| 4.2.5 | Admin Interfaces | /admin, /wp-admin, /manager | web-attacks |
| 4.2.6 | HTTP Methods | OPTIONS, PUT, DELETE, TRACE | web-attacks |
| 4.2.7 | HSTS | curl -I, testssl.sh | web-attacks |
| 4.2.8 | Cross Domain Policy | crossdomain.xml, clientaccesspolicy.xml | web-attacks |
| 4.2.9 | File Permissions | Directory listing, accessible configs | web-attacks |
| 4.2.10 | Subdomain Takeover | subfinder, dig, CNAME analysis | infrastructure-attacks |
| 4.2.11 | Cloud Storage | S3/GCS bucket enumeration | infrastructure-attacks |

---

### PHASE 3: Identity Management (4.3 — 5 tests)

| ID | Test | Tool |
|----|------|------|
| 4.3.1 | Role Definitions | Manual role matrix testing |
| 4.3.2 | User Registration | Test validation, enumeration |
| 4.3.3 | Account Provisioning | Test workflow automation |
| 4.3.4 | Account Enumeration | Timing analysis, error differences |
| 4.3.5 | Weak Username Policy | Predictable usernames |

---

### PHASE 4: Authentication (4.4 — 10 tests)

| ID | Test | Tool | Load Skill |
|----|------|------|-----------|
| 4.4.1 | Credentials Over Encrypted Channel | Burp, Wireshark | web-attacks |
| 4.4.2 | Default Credentials | Default password lists, nuclei | web-attacks |
| 4.4.3 | Lock Out Mechanism | Burp Intruder, rate limit testing | web-attacks |
| 4.4.4 | Bypass Authentication | SQLi auth bypass, parameter manipulation | web-attacks |
| 4.4.5 | Remember Password | Cookie analysis, token replay | web-attacks |
| 4.4.6 | Browser Cache | Cache-Control headers, back button | web-attacks |
| 4.4.7 | Password Policy | Brute force, weak password testing | web-attacks |
| 4.4.8 | Security Questions | Guessable answers, OSINT | web-attacks |
| 4.4.9 | Password Reset | Token prediction, host header injection | web-attacks |
| 4.4.10 | Alternative Channel | Mobile API, legacy endpoints | mobile-attacks |

---

### PHASE 5: Authorization (4.5 — 4 tests)

| ID | Test | Tool |
|----|------|------|
| 4.5.1 | Directory Traversal / File Include | dotdotpwn, ffuf, manual | web-attacks |
| 4.5.2 | Bypass Authorization | Role/ID swapping, forced browsing | web-attacks |
| 4.5.3 | Privilege Escalation | Vertical/horizontal escalation | web-attacks |
| 4.5.4 | IDOR | UUID/ID enumeration, parameter fuzzing | web-attacks |

---

### PHASE 6: Session Management (4.6 — 9 tests)

| ID | Test | Tool |
|----|------|------|
| 4.6.1 | Session Schema | Token entropy, predictable tokens | web-attacks |
| 4.6.2 | Cookie Attributes | HttpOnly, Secure, SameSite, Domain | web-attacks |
| 4.6.3 | Session Fixation | Pre-login token reuse | web-attacks |
| 4.6.4 | Exposed Session Variables | Debug output, error pages | web-attacks |
| 4.6.5 | CSRF | Missing tokens, bypass techniques | web-attacks |
| 4.6.6 | Logout Functionality | Session invalidation, back button | web-attacks |
| 4.6.7 | Session Timeout | Idle timeout, absolute timeout | web-attacks |
| 4.6.8 | Session Puzzling | Token reuse across contexts | web-attacks |
| 4.6.9 | Session Hijacking | Cookie theft, XSS→cookie, MITM | web-attacks |

---

### PHASE 7: Input Validation (4.7 — 19 test categories)

| ID | Test | Category | Load Skill |
|----|------|----------|-----------|
| 4.7.1 | Reflected XSS | XSS | web-attacks |
| 4.7.2 | Stored XSS | XSS | web-attacks |
| 4.7.3 | HTTP Verb Tampering | Config | web-attacks |
| 4.7.4 | HTTP Parameter Pollution | Logic | web-attacks |
| 4.7.5 | SQL Injection (8 sub-types) | Injection | web-attacks |
| 4.7.6 | LDAP Injection | Injection | web-attacks |
| 4.7.7 | XML Injection | Injection | web-attacks |
| 4.7.8 | SSI Injection | Injection | web-attacks |
| 4.7.9 | XPath Injection | Injection | web-attacks |
| 4.7.10 | IMAP/SMTP Injection | Injection | web-attacks |
| 4.7.11 | Code Injection / LFI/RFI | Injection | web-attacks |
| 4.7.12 | Command Injection | Injection | web-attacks |
| 4.7.13 | Format String | Injection | exploit-development |
| 4.7.14 | Incubated/Stored Injection | Injection | web-attacks |
| 4.7.15 | HTTP Splitting/Smuggling | Injection | web-attacks |
| 4.7.16 | HTTP Incoming Requests | Injection | web-attacks |
| 4.7.17 | Host Header Injection | Injection | web-attacks |
| 4.7.18 | SSTI | Injection | web-attacks |
| 4.7.19 | Server-Side Request Forgery | Injection | web-attacks |

---

### PHASE 8: Error Handling (4.8 — 3 tests)

| ID | Test | Purpose |
|----|------|---------|
| 4.8.1 | Error Codes | Stack traces, DB errors → info disclosure |
| 4.8.2 | Stack Traces | Reveal framework, paths, versions |
| 4.8.3 | Failing Open | Auth failure → default access |

---

### PHASE 9: Cryptography (4.9 — 5 tests)

| ID | Test | Tool |
|----|------|------|
| 4.9.1 | Weak SSL/TLS Ciphers | testssl.sh, sslscan |
| 4.9.2 | Padding Oracle | PadBuster, custom PoC |
| 4.9.3 | Sensitive Data in Transit | Burp, Wireshark |
| 4.9.4 | Weak Encryption | Hardcoded keys, ECB mode, weak IV |
| 4.9.5 | Cacheable HTTPS | Cache-Control: public on sensitive pages |

---

### PHASE 10: Business Logic (4.10 — 11 tests)

| ID | Test | Example |
|----|------|---------|
| 4.10.1 | Data Validation | Negative prices, unreasonable quantities |
| 4.10.2 | Forced Browsing | Access admin after partial auth |
| 4.10.3 | Integrity Checks | Modify price in request, replay attacks |
| 4.10.4 | Process Timing | Race conditions, double-submit |
| 4.10.5 | Function Limits | Coupon reuse, referral abuse |
| 4.10.6 | Workflow Circumvention | Skip payment step, edit order after submit |
| 4.10.7 | Upload Unexpected Files | Malware via "profile picture" |
| 4.10.8 | Trust of Client-Side | Price validation only client-side |
| 4.10.9 | Misuse of Functionality | Use search for DoS, email spam |
| 4.10.10 | Fake Captcha | No server-side validation |
| 4.10.11 | Flash/Applet Misuse | Deprecated but check legacy |

---

### PHASE 11: Client-Side (4.11 — 13 tests)

| ID | Test | Tool | Load Skill |
|----|------|------|-----------|
| 4.11.1 | DOM XSS | DOM Invader, browser devtools | web-attacks |
| 4.11.2 | JavaScript Execution | Code review, CSP bypass | web-attacks |
| 4.11.3 | HTML Injection | Manual, Burp | web-attacks |
| 4.11.4 | Client URL Redirect | Open redirect via JS | web-attacks |
| 4.11.5 | CSS Injection | Style attribute, CSS-based exfil | web-attacks |
| 4.11.6 | Resource Manipulation | Script src, iframe src | web-attacks |
| 4.11.7 | Cross-Origin Resource Sharing | Origin header tests | web-attacks |
| 4.11.8 | Cross-Site Flashing | SWF analysis (legacy) | web-attacks |
| 4.11.9 | Clickjacking | X-Frame-Options, frame busting | web-attacks |
| 4.11.10 | WebSockets | WS message manipulation | web-attacks |
| 4.11.11 | Web Messaging | postMessage origin bypass | web-attacks |
| 4.11.12 | Local Storage | Sensitive data in localStorage | web-attacks |
| 4.11.13 | Web SQL/IndexedDB | Client-side database inspection | web-attacks |

---

### PHASE 12: API Testing (4.12 — 2 tests)

| ID | Test | Purpose |
|----|------|---------|
| 4.12.1 | REST API | Mass assignment, auth per endpoint, rate limit |
| 4.12.2 | GraphQL | Introspection, batching, depth limit, field suggesting |
| 4.12.3 | SOAP/WS | WSDL enumeration, XXE in SOAP |

---

## TESTING PRIORITY MATRIX

| Priority | Phase | Reason |
|----------|-------|--------|
| P0 | Info Gathering (4.1) | No attack possible without map |
| P0 | Config (4.2.1-4.2.2) | Quick wins from misconfig |
| P1 | Input Validation (4.7) | Highest impact vulns (SQLi, XSS, SSTI) |
| P1 | Auth (4.4) | Account takeover potential |
| P2 | Authorization (4.5) | Privilege escalation |
| P2 | Session (4.6) | Session hijacking |
| P3 | Business Logic (4.10) | Complex, time-intensive |
| P3 | Client-Side (4.11) | Lower impact unless chained |
| P4 | Cryptography (4.9) | Specialized, less common |

---

## TOOL-TO-PHASE MAPPING

```
Phase 1   → nmap, whatweb, gobuster, ffuf, gospider, katana, subfinder, Shodan
Phase 2   → nuclei, nikto, testssl.sh, wpscan
Phase 3-6 → Burp Suite, manual testing, Burp Intruder
Phase 7   → sqlmap, dalfox, xsstrike, commix, ssrfmap, tplmap
Phase 8   → Manual, Burp Repeater
Phase 9   → testssl.sh, sslscan, PadBuster
Phase 10  → Manual, Burp, browser devtools
Phase 11  → DOM Invader, Burp, browser devtools
Phase 12  → Postman, Burp, GraphQL voyager
```

## REPORTING TEMPLATE

Each finding must include:
- WSTG ID (e.g., WSTG-ID: 4.7.5)
- OWASP Top 10 Category (e.g., A05:2025-Injection)
- MITRE ATT&CK Technique (e.g., T1190)
- CVSS Score
- Evidence (request/response, screenshots)
- Remediation (per WSTG guidance)

## CROSS-SKILL REFERENCE
- Execute tests → web-attacks, exploit-development, windows-red-team, infrastructure-attacks, ai-ml-attacks, mobile-attacks
- Plan operations → threat-intel
- Select tools → kali-tools-arsenal

---

## OWASP ASVS 3.0 — VERIFICATION REQUIREMENTS (V1-V19)

Source: OWASP Application Security Verification Standard 3.0 — full requirement structure.

### Verification Levels
- **Level 1 (Opportunistic)**: Defends against OWASP Top 10; suitable for low-value apps; can be automated
- **Level 2 (Standard)**: Sensitive data, B2B transactions, healthcare, PII
- **Level 3 (Advanced)**: Critical apps (military, health/safety, critical infrastructure, financial wire transfers)

### V1: Architecture, Design and Threat Modeling
- STRIDE threat modeling (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation)
- Security architecture documentation
- Attack surface analysis and reduction
- Component trust boundaries
- Centralized security controls implementation

### V2: Authentication Verification
- Password policies (min length, complexity, NIST 800-63 alignment)
- MFA/2FA implementation
- Credential recovery (secure token generation, time-limited)
- No default credentials
- Weak-password checks against known lists
- Account lockout after N failed attempts
- Credential transmission over encrypted channels only

### V3: Session Management
- Secure session ID generation (cryptographically random, >64 bits entropy)
- Session cookies: HttpOnly, Secure, SameSite, Path, Domain attributes
- Session invalidation on logout (server-side)
- Idle timeout + absolute timeout enforcement
- Session ID rotation after login (prevent fixation)
- No session IDs in URL
- Concurrent session controls

### V4: Access Control
- Deny by default architecture
- Record-level ownership enforcement
- JWT/Token invalidation server-side
- Disable directory listing
- Log access control failures
- Rate-limit API/controller access
- CORS misconfiguration prevention

### V5: Malicious Input Handling (Input Validation)
- Parameterized queries / ORM / stored procedures for SQL
- Input validation: whitelist approach
- Type checking (string, int, boolean)
- Length limits on all inputs
- File upload validation (MIME type, extension, content verification)
- Command injection prevention (avoid shell, use library calls)
- LDAP/XPath/XML injection prevention

### V6: Output Encoding/Escaping (XSS Prevention)
- Context-sensitive escaping (HTML body, attribute, JavaScript, CSS, URL)
- CSP (Content-Security-Policy) headers
- Frameworks with auto-escaping (React, Angular, Rails)
- DOM-based XSS prevention (avoid dangerous JS sinks)

### V7: Cryptography at Rest
- Approved algorithms: AES-256, RSA-2048+, ECDSA on secp256r1/secp384r1
- Key management: separate from data, HSM or secure keystore
- Password storage: Argon2 > scrypt > bcrypt > PBKDF2 (salted, adaptive)
- No deprecated algorithms: MD5, SHA1, RC4, DES, 3DES, ECB mode

### V8: Error Handling and Logging
- No stack traces or verbose errors to client
- Centralized logging with integrity protection
- Log: authentication events, access control failures, input validation failures
- Sensitive data redaction in logs (passwords, tokens, PII)
- Log retention aligned with regulatory requirements

### V9: Data Protection
- Data classification and handling procedures
- Encryption at rest for sensitive data
- TLS for data in transit (TLS 1.2+)
- No sensitive data in client-side storage (localStorage, cookies without protection)
- Secure deletion procedures

### V10: Communications Security
- TLS 1.2+ with PFS (Perfect Forward Secrecy) cipher suites
- Certificate validation (hostname, expiry, chain trust)
- HSTS header (max-age >= 1 year, includeSubDomains, preload)
- No mixed content (all resources over HTTPS)
- Certificate pinning for mobile apps

### V11: HTTP Security Configuration
- Security headers: X-Content-Type-Options: nosniff
- X-Frame-Options: DENY or Content-Security-Policy: frame-ancestors
- X-XSS-Protection: 1; mode=block (legacy)
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy (Feature-Policy) for browser features
- Cache-Control: no-store for sensitive pages

### V12: Security Configuration
- Minimal platform: remove unnecessary features, accounts, services
- Repeatable hardening process
- Segmented architecture (tiers)
- Patch management process
- Automated configuration verification

### V13: Malicious Controls
- Code integrity verification (digital signatures)
- Anti-malware controls
- Application integrity checks
- Separation of duties in development pipeline

### V14: Internal Security (Separation of Duties)
- Administrative access separate from user access
- Segregation of duties for sensitive operations
- Audit trail for administrative actions
- Four-eyes principle for critical changes

### V15: Business Logic
- Workflow enforcement (can't skip steps)
- Transaction limits and verification
- Abuse case modeling
- Race condition prevention

### V16: Files and Resources
- File upload scanning for malware
- File type/content validation
- File storage outside web root
- Authenticated file access only
- File size limits and quota enforcement

### V17: Mobile Verification
- Secure local storage (Keychain on iOS, Keystore on Android)
- Certificate pinning
- No sensitive data in app backups
- Biometric authentication integration
- Jailbreak/root detection (informational)

### V18: Web Services (REST, SOAP)
- Authentication per endpoint
- Input validation on all service methods
- Rate limiting
- CORS configuration review
- SOAP: DTD/Entity processing disabled (XXE prevention)
- GraphQL: query depth/complexity limits, introspection disabled in production

### V19: Configuration
- Build pipeline security
- Dependency vulnerability scanning
- Secret management (no hardcoded keys, use vault)
- Environment separation (dev/staging/prod configs isolated)

### Industry-Specific ASVS Level Guidance
| Sector | Level | Rationale |
|--------|-------|-----------|
| Finance/Insurance | L3 | Sensitive financial data, wire transfers |
| Manufacturing/Defense | L3 | IP/trade secrets, national security |
| Healthcare | L3 | HIPAA, medical equipment/records |
| Retail/Hospitality | L2 | Payment data (PCI), personal info |
| E-commerce | L2 | Payment + PII |
| Gaming | L2 | User accounts, payment data |
| SaaS/Startup | L1-L2 | Depends on data sensitivity |

### Tools Using ASVS
- **OWASP Security Knowledge Framework (SKF)**: Training and ASVS integration
- **OWASP ZAP**: Passive/active scanning aligned with ASVS
- **OWASP Cornucopia**: Card game for threat modeling per ASVS

---

## WSTG-CONF DETAILED TEST CASES (Expanded from v4.1)

### WSTG-CONF-05: Enumerate Admin Interfaces
**Discovery Methods:**
- Directory brute-forcing: /admin, /administrator, /manager, /console
- Google dorks: `site:target.com inurl:admin`, `intitle:"admin login"`
- Source code comments: `<!-- admin panel at /secret-admin -->`
- robots.txt entries: `Disallow: /admin-panel/`
- Default credentials lists (admin/admin, admin/password)

**Framework-Specific Paths:**
- **IBM WebSphere**: /admin, /admin-authz.xml, /admin.conf, /ibm/console
- **PHP**: /phpinfo, /phpmyadmin/, /phpMyAdmin/, /phppgadmin
- **FrontPage**: /admin.dll, /admin.exe, /author.dll, /author.exe
- **WebLogic**: /AdminCaptureRootCA, /AdminClients, /AdminJDBC, /console
- **WordPress**: wp-admin/, wp-admin/admin-ajax.php, /wp-login.php
- **Tomcat**: /manager/html, /host-manager/html
- **Jenkins**: /jenkins/login, /jenkins/script
- **Django**: /admin/, /admin/login/

**Tools:** OWASP ZAP Forced Browse, THC-HYDRA, FuzzDB admin paths lists, gobuster, ffuf

### WSTG-CONF-06: HTTP Methods Testing
**Methods to Test:**
- OPTIONS: Reveals allowed methods via Allow header
- PUT: File upload potential (check with empty PUT → 201 Created)
- DELETE: Resource removal potential
- TRACE: Cross-Site Tracing (XST) attack — bypasses HttpOnly cookie
- CONNECT: Proxy functionality abuse
- HEAD: May bypass auth (some frameworks treat HEAD as GET without auth)
- Arbitrary methods (JEFF, CATS): May be treated as GET by some frameworks

**Testing Commands:**
```bash
# Method enumeration
nc target 80 <<< "OPTIONS / HTTP/1.1\r\nHost: target\r\n\r\n"
nmap -p 443 --script http-methods localhost

# PUT test
curl -X PUT -d "test" https://target.com/newfile.txt

# TRACE test (XST)
curl -X TRACE -H "Cookie: session=test" https://target.com/
```

### WSTG-CONF-07: HTTP Strict Transport Security
**Checks:**
- `Strict-Transport-Security` header present?
- `max-age` >= 31536000 (1 year)?
- `includeSubDomains` directive?
- `preload` directive for HSTS preload list?
- HTTPS redirect from HTTP (301/302)?

**Testing:**
```bash
curl -sI https://target.com | grep -i strict
testssl.sh https://target.com
```
