# Certification & Reference Books — Deep-Read Extraction
## Techniques, Methodologies, Test Cases, and Frameworks

---

## 1. SYBEX CISSP 8TH EDITION (Official Study Guide)
*Authors: Mike Chapple, James Michael Stewart, Darril Gibson*

### 8 CISSP Domains
1. Security and Risk Management
2. Asset Security
3. Security Architecture and Engineering
4. Communication and Network Security
5. Identity and Access Management (IAM)
6. Security Assessment and Testing
7. Security Operations
8. Software Development Security

### CIA Triad (Core Principles)
- **Confidentiality**: Protection from unauthorized access/disclosure
- **Integrity**: Protection from unauthorized modification
- **Availability**: Timely and reliable access to systems/data
- **Top Priority**: Human safety always trumps all other security goals

### Security Governance Framework
- **Third-party governance**: COBIT-based auditing, on-site assessments, documentation review, ATO (Authorization to Operate), TATO (Temporary ATO)
- **Compliance**: PCI DSS, HIPAA, SOX, FERPA, Gramm-Leach-Bliley, GDPR, EU Data Protection Directive
- **Privacy**: PII definition, GDPR core elements
- **Documentation review** process: exchanged materials verified against standards before on-site inspection

### Access Control Models & Methodologies
- Physical security controls: Administrative, Technical, Physical
- Physical access control: Fencing, lighting, locks, mantraps, dogs, guards, CCTV, biometrics, smart/dumb cards
- **Functional order of controls**: Deterrence → Denial → Detection → Delay
- Wiring closet security, media storage, visitor handling, OEP (Occupant Emergency Plans)

### Encryption Algorithms & Cryptography
- **X.509 Digital Certificates**: Version, Serial Number, Signature Algorithm, Issuer Name, Validity Period, Subject Name, Subject Public Key
- **PKI Components**: CA (Certificate Authority), RA (Registration Authority), CRL (Certificate Revocation List), OCSP (Online Certificate Status Protocol)
- **Certificate Path Validation (CPV)**: Every link from root of trust to endpoint must be valid
- **Enrollment → Verification → Revocation** lifecycle
- **Key CAs**: Symantec, IdenTrust, AWS, GlobalSign, Comodo, DigiCert, Entrust, GoDaddy
- SSL/TLS features: client-server encryption, one-way/two-way auth, VPN (OpenVPN)

### Cloud Computing
- **Service Models**: SaaS (full apps via browser), PaaS (platform with OS/apps), IaaS (basic compute resources)
- **Deployment Models**: Public, Private, Community, Hybrid
- **NIST SP 800-145**: Standard definitions for cloud
- **NIST SP 800-144**: Security and privacy in public cloud
- Shared responsibility varies by model

### BCP/DRP Concepts
- **OEP (Occupant Emergency Plan)**: Personnel safety first; IT/business continuity secondary
- Privacy responsibilities, regulatory compliance

### Network Attacks & Defenses
- **ARP Cache Poisoning**: Falsified ARP replies; static ARP entries via scripts; man-in-the-middle enabler
- **DNS Cache Poisoning**: HOSTS file poisoning, authoritative DNS attacks, caching DNS attacks, DHCP-based DNS redirection
- **Java Sandbox**: Isolates Java code from OS; ActiveX has full Windows access

### Database Security
- **Polyinstantiation**: Multiple records at different classification levels for same primary key
- **Noise and Perturbation**: False/misleading data inserted to thwart confidentiality attacks
- **ODBC**: Proxy between apps and backend databases
- **NoSQL Types**: Key/value stores, Graph databases, Document stores (XML/JSON)

### Storage Types & Threats
- Primary (RAM), Secondary (disk/tape), Virtual memory, Virtual storage (RAM disk)
- Random access vs. Sequential access (tape)
- Volatile (RAM) vs. Nonvolatile (NVRAM, magnetic/optical)
- Covert channel attacks: storage channels between classification levels
- Encrypted filesystem for physical media protection

### Authentication Protocols
- **CHAP**: Challenge-response, encrypted, periodic reauthentication
- **PAP**: Cleartext, no encryption
- **EAP**: Framework for custom auth (smart cards, tokens, biometrics)
- **PEAP**: EAP in TLS tunnel; preferred for 802.11
- **LEAP**: Cisco proprietary, crackable via Asleap

### Social Engineering Defenses
- Guidelines: Train users on all communication forms; beware of trust exploitation, desire to assist, fear of reprimand

### Media Management
- Tape media: 2 copies (onsite + offsite), avoid magnetic fields, temperature-controlled transport, 24hr acclimation
- USB flash drive risks: malware infections, data theft
- Mobile: MDM, encryption, screen lock, GPS, remote wipe; CYOD preferred over BYOD

### Legal Framework
- Computer Fraud and Abuse Act, FISMA, DMCA, Economic Espionage Act (1996)
- Software licensing: Contractual, Shrink-wrap, Click-wrap
- California SB 1386: First statewide breach notification law

---

## 2. OFFICIAL (ISC)² GUIDE TO THE CCSP CBK
*Editor: Adam Gordon*

### 6 CCSP Domains
1. Architectural Concepts and Design Requirements
2. Cloud Data Security
3. Cloud Platform and Infrastructure Security
4. Cloud Application Security
5. Operations
6. Legal and Compliance

### Cloud Computing Definitions & Characteristics (NIST-aligned)
- **On-Demand Self-Service**: Provision without human interaction
- **Broad Network Access**: Always-on, always-accessible
- **Resource Pooling**: Multi-tenant, dynamic scaling
- **Rapid Elasticity**: Scale up/down seamlessly
- **Measured Service**: Pay-per-use, metered billing

### Cloud Roles
- **Cloud Consumer**, **Cloud Provider**, **Cloud Service Broker (CSB)**, **Cloud Service Auditor**, **Cloud Carrier**

### Cloud Service Categories
- **IaaS**: Consumer deploys OS/apps; provider manages virtualization, servers, storage, networking
- **PaaS**: Consumer deploys apps; provider manages OS, middleware, runtime
- **SaaS**: Consumer uses provider's apps via thin client; provider manages everything

### Cloud Deployment Models
- **Public**: Available to any consumer; external CSP
- **Private**: Single organization; on-premises or dedicated third-party
- **Hybrid**: Combination of two or more models
- **Community**: Shared by organizations with common mission

### Cloud Secure Data Lifecycle (6 Phases)
1. Create
2. Store
3. Use
4. Share
5. Archive
6. Destroy

### Shared Responsibility Model
- Varies by service model (IaaS vs PaaS vs SaaS)
- Consumer always responsible for their data and access management

### Data Security Technologies
- **Data Loss Prevention (DLP)** in cloud
- **Data Dispersion**: Fragmenting data across multiple storage locations
- **Crypto-shredding**: Destroy encryption keys to render data unrecoverable (only reliable cloud disposal method)
- **IRM/DRM (Information/Digital Rights Management)**: Persistent protection; control printing, copy/paste, screen capture, watermarking, document expiration, audit trails

### CASB (Cloud Access Security Broker)
- Acts as intermediary between cloud users and providers
- Enforces security policies, provides visibility, data security, threat protection

### Cloud Attack Vectors
- Guest breakout
- Identity compromise (technical or social)
- API compromise (leaked credentials)
- Attacks on provider infrastructure
- Attacks on connecting infrastructure (cloud carrier)

### Compensating Controls (4 Criteria)
1. Meet intent and rigor of original requirement
2. Provide similar level of defense
3. Be "above and beyond" other requirements
4. Be commensurate with additional risk

### Physical & Environmental Controls
- Building access, computer floor access, cage/rack access
- Hypervisor access (API/management plane)
- Guest OS access, developer access, customer access
- Database access rights, vendor access, remote access

### Key Regulations
- HIPAA, PCI DSS, NERC CIP
- NIST SP 800-14, SP 800-123

### Data Retention Policy (4 Elements)
1. Retention periods
2. Data formats
3. Data security
4. Data retrieval procedures

### Continuous Operations Principles
- **Audit logging**: Detecting new events, adding new rules, reducing false positives
- **Contract/authority maintenance**: Updated regulatory contacts
- **Secure disposal**: Non-recoverable data removal
- **Incident response legal preparation**: Chain of custody, forensic procedures

### Virtualization & Clustering
- **DRS (Distributed Resource Scheduling)**: Automated VM placement and load balancing
- **Resource Sharing**: Reservations (minimum), Limits (maximum), Shares (priority-based allocation)
- **Stand-alone hosts** vs. **Clustered hosts** for high availability and disaster recovery

### Trust Services Principles (SOC Reports)
- Security, Availability, Processing Integrity, Confidentiality, Privacy
- SOC1/SOC2/SOC3 audit reports

### Legal & Compliance Frameworks
- **OECD Privacy & Security Guidelines** (2013 revision): National privacy strategies, privacy management programs, data security breach notification
- **APEC Privacy Framework**: 9 principles including Preventing Harm, Notice, Collection Limitation, Use of Personal Information, Choice, Integrity, Security Safeguards, Access and Correction, Accountability
- **Doctrine of the Proper Law**: Conflict of laws resolution
- **Tort Law**: Compensate victims, shift costs, discourage risky behavior, vindicate rights
- **Restatement (Second) Conflict of Laws**: Basis for deciding applicable law

---

## 3. WSTG v4.1 (Web Security Testing Guide)
*OWASP Project*

### Testing Methodology Overview
- Based on **black box approach**: Tester knows little about application
- Testing model: Tester + Tools/Methodology + Application
- **Passive Testing**: Understanding application logic, exploring as user, using HTTP proxy
- **Active Testing**: 11 sub-categories, **91 total controls**

### 11 Active Testing Categories (with Test IDs)
1. **Information Gathering** (WSTG-INFO): Search engine reconnaissance, web server fingerprinting, meta-files, enumeration, comments/metadata, entry points, execution paths, framework/application fingerprinting, architecture mapping
2. **Configuration & Deployment Management Testing** (WSTG-CONF): Network config, platform config, file extensions, backup/unreferenced files, admin interfaces, HTTP methods, HSTS, RIA cross-domain policy, file permissions, subdomain takeover, cloud storage
3. **Identity Management Testing** (WSTG-IDNT): Role definitions, registration, provisioning, account enumeration, username policy
4. **Authentication Testing** (WSTG-ATHN): Credentials over encrypted channel, default credentials, lockout mechanism, bypassing auth schema, remember password, browser cache, password policy, security questions, password change/reset, alternative channel
5. **Authorization Testing** (WSTG-ATHZ): Directory traversal/file include, bypassing auth schema, privilege escalation, IDOR
6. **Session Management Testing** (WSTG-SESS): Session management schema, cookies attributes, session fixation, exposed session variables, CSRF, logout, session timeout, session puzzling
7. **Input Validation Testing** (WSTG-INPV): Reflected/stored XSS, HTTP verb tampering, HTTP parameter pollution, SQL injection (Oracle/MySQL/SQL Server/PostgreSQL/MS Access/NoSQL/ORM/Client-side), LDAP injection, XML injection, SSI injection, XPath injection, IMAP/SMTP injection, Code injection (LFI/RFI), Command injection, Buffer overflow (heap/stack/format string), Incubated vulnerabilities, HTTP splitting/smuggling, HTTP incoming requests, Host header injection, Server-side template injection
8. **Error Handling** (WSTG-ERRH): Error codes, stack traces
9. **Weak Cryptography** (WSTG-CRYP): SSL/TLS ciphers, padding oracle, unencrypted channels, weak encryption
10. **Business Logic Testing** (WSTG-BUSL): Data validation, forge requests, integrity checks, process timing, function usage limits, circumvention of workflows, application misuse defenses, unexpected file uploads, malicious file uploads
11. **Client Side Testing** (WSTG-CLNT): DOM XSS, JavaScript execution, HTML injection, URL redirect, CSS injection, resource manipulation, CORS, cross-site flashing, clickjacking, WebSockets, web messaging, local storage, cross-site script inclusion

### Penetration Testing Methodologies (Referenced)
- **PTES (Penetration Testing Execution Standard)**: 7 phases — Pre-engagement, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post Exploitation, Reporting
- **PCI DSS Penetration Testing**: Requirement 11.3; external + internal; application layer + network layer
- **NIST 800-115**: Technical Guide to Information Security Testing and Assessment
- **ISSAF**: Comprehensive framework covering project management, password security, Unix/Windows DB assessment, wireless, switch/router/firewall, IDS/IPS, VPN, anti-virus, SAN, source code auditing, social engineering, physical security, BCP/DRP
- **OSSTMM**: Operational security metrics, trust analysis, workflow, human/physical/wireless/telecom/data network security testing, STAR reporting
- **Penetration Testing Framework**: Network footprinting, discovery/probing, enumeration, password cracking, vulnerability assessment, VoIP, wireless

### Specific Test Cases & Techniques

#### Information Gathering (WSTG-INFO-01 to -10)
- **Search Engine Discovery**: Google dorks (Google Hacking Database), cache: operator, site:/inurl:/intitle:/intext:/filetype: operators, Baidu, Bing, Shodan, DuckDuckGo, Startpage
- **Web Server Fingerprinting**: Banner grabbing (telnet, openssl), malformed requests, automated tools (nmap, Netcraft)
- **Meta-files**: robots.txt, sitemap.xml, crossdomain.xml, clientaccesspolicy.xml

#### HTTP Methods Testing (WSTG-CONF-06)
- **8 defined methods**: HEAD, GET, POST, PUT, DELETE, TRACE, OPTIONS, CONNECT
- **WebDAV extensions**: PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK
- **Risks**: PUT → upload malicious files; DELETE → deface/DoS; CONNECT → proxy abuse; TRACE → XST (Cross Site Tracing)
- **HEAD access control bypass**: HEAD treated as GET without body; may bypass auth constraints
- **Arbitrary HTTP methods bypass**: "JEFF", "CATS" treated as GET; bypass method-based access control

#### HSTS Testing (WSTG-CONF-07)
- Two directives: max-age, includeSubDomains

#### SQL Injection Exploitation Techniques
- **Classic SQL Injection**: `1' or '1' = '1`, `1' or '1' = '1'))/*`, `LIMIT 1/*`
- **Stacked Queries**: Multiple queries in one call
- **Fingerprinting DB**: Error messages (MySQL, Oracle, MSSQL, PostgreSQL); concatenation differences
- **UNION Exploitation**: ORDER BY for column count; NULL for type discovery; LIMIT for single-row
- **Boolean Exploitation (Blind SQLi)**: SUBSTRING + ASCII + character-by-character inference; LENGTH for termination
- **Error-Based Exploitation**: Force DB to reveal data in error messages; `UTL_INADDR.GET_HOST_NAME` (Oracle)
- **Out-of-Band Exploitation**: `UTL_HTTP.request` to exfiltrate via HTTP
- **Time Delay Exploitation**: `IF(version() like '5%', sleep(10), 'false'))`
- **Stored Procedure Injection**: Dynamic SQL within stored procedures

#### SQL Injection Signature Evasion
- **White Space manipulation**: Dropping/adding spaces, newlines, tabs
- **Null Bytes**: `%00` before blocked characters
- **SQL Comments**: Inline `/**/` to break keywords
- **URL Encoding**: `%27%20UNION%20SELECT`
- **Character Encoding**: `char(114,111,111,116)` for "root"
- **String Concatenation**: `EXEC('SEL' + 'ECT 1')`
- **Hex Encoding**: `unhex('726F6F74')`
- **Declare Variables**: Bypass signature-based WAF

#### SSL/TLS Testing Minimum Checklist
- Weak ciphers must not be used (<128 bits, no NULL, no Anonymous DH)
- Weak protocols disabled (SSLv2, SSLv3)
- Renegotiation properly configured (disable Insecure Renegotiation, Client-initiated Renegotiation)
- No EXPORT cipher suites
- X.509 key length ≥1024 bits (RSA/DSA)
- Certificates not signed with MD5
- Keys generated with proper entropy (no Debian weak keys)
- **Additional**: Secure Renegotiation enabled, no MD5/RC4, protected from BEAST/CRIME, Forward Secrecy supported

#### Testing Tools Referenced
- **Info Gathering**: Google, Baidu, Bing, Shodan, DuckDuckGo, Startpage, binsearch.info
- **Server/SSL**: nmap (ssl-cert, ssl-enum-ciphers, http-methods scripts), TestSSLServer, SSLAudit, SSLScan, OpenSSL, Tenable Nessus, Qualys SSL Labs
- **Brute Force/Dir Enum**: OWASP ZAP (Forced Browse), THC-HYDRA, DirBuster, netsparker dictionary, FuzzDB
- **Manual**: netcat, telnet, curl, wget, socat

#### Reporting Template
1. Introduction (risk levels, GRC)
2. Test Parameters (objective, scope, schedule, targets, limitations, findings summary, remediation summary)
3. Findings (screenshots, affected item, technical description, resolution, CVSS severity rating)
4. Full test ID listing with severity and recommendations

---

## 4. OWASP TESTING GUIDE v4
*Project Leaders: Matteo Meucci and Andrew Muller*

### OTG Test Case IDs (Complete Mapping)

#### Information Gathering
- OTG-INFO-001: Search Engine Discovery and Reconnaissance
- OTG-INFO-002: Fingerprint Web Server
- OTG-INFO-003: Review Webserver Metafiles
- OTG-INFO-004: Enumerate Applications on Webserver
- OTG-INFO-005: Review Webpage Comments and Metadata
- OTG-INFO-006: Identify Application Entry Points
- OTG-INFO-007: Map Execution Paths Through Application
- OTG-INFO-008: Fingerprint Web Application Framework
- OTG-INFO-009: Fingerprint Web Application
- OTG-INFO-010: Map Application Architecture

#### Configuration and Deployment Management
- OTG-CONFIG-001: Test Network/Infrastructure Configuration
- OTG-CONFIG-002: Test Application Platform Configuration
- OTG-CONFIG-003: Test File Extensions Handling
- OTG-CONFIG-004: Review Old, Backup and Unreferenced Files
- OTG-CONFIG-005: Enumerate Infrastructure and Application Admin Interfaces
- OTG-CONFIG-006: Test HTTP Methods
- OTG-CONFIG-007: Test HTTP Strict Transport Security
- OTG-CONFIG-008: Test RIA Cross Domain Policy

#### Identity Management Testing
- OTG-IDENT-001: Test Role Definitions
- OTG-IDENT-002: Test User Registration Process
- OTG-IDENT-003: Test Account Provisioning Process
- OTG-IDENT-004: Testing for Account Enumeration
- OTG-IDENT-005: Testing for Weak Username Policy

#### Authentication Testing
- OTG-AUTHN-001: Credentials Transported over Encrypted Channel
- OTG-AUTHN-002: Default Credentials
- OTG-AUTHN-003: Weak Lock Out Mechanism
- OTG-AUTHN-004: Bypassing Authentication Schema
- OTG-AUTHN-005: Remember Password Functionality
- OTG-AUTHN-006: Browser Cache Weakness
- OTG-AUTHN-007: Weak Password Policy
- OTG-AUTHN-008: Weak Security Question/Answer
- OTG-AUTHN-009: Weak Password Change/Reset
- OTG-AUTHN-010: Weaker Authentication in Alternative Channel

#### Authorization Testing
- OTG-AUTHZ-001: Directory Traversal/File Include
- OTG-AUTHZ-002: Bypassing Authorization Schema
- OTG-AUTHZ-003: Privilege Escalation
- OTG-AUTHZ-004: Insecure Direct Object References

#### Session Management Testing
- OTG-SESS-001: Bypassing Session Management Schema
- OTG-SESS-002: Cookies Attributes
- OTG-SESS-003: Session Fixation
- OTG-SESS-004: Exposed Session Variables
- OTG-SESS-005: Cross Site Request Forgery (CSRF)
- OTG-SESS-006: Logout Functionality
- OTG-SESS-007: Session Timeout
- OTG-SESS-008: Session Puzzling

#### Input Validation Testing
- OTG-INPVAL-001: Reflected XSS
- OTG-INPVAL-002: Stored XSS
- OTG-INPVAL-003: HTTP Verb Tampering
- OTG-INPVAL-004: HTTP Parameter Pollution
- OTG-INPVAL-005: SQL Injection (Oracle, MySQL, SQL Server, PostgreSQL, MS Access, NoSQL, ORM)
- OTG-INPVAL-006: LDAP Injection
- OTG-INPVAL-007: ORM Injection
- OTG-INPVAL-008: XML Injection
- OTG-INPVAL-009: SSI Injection
- OTG-INPVAL-010: XPath Injection
- OTG-INPVAL-011: IMAP/SMTP Injection
- OTG-INPVAL-012: Code Injection (LFI/RFI)
- OTG-INPVAL-013: Command Injection
- OTG-INPVAL-014: Buffer Overflow (Heap, Stack, Format String)
- OTG-INPVAL-015: Incubated Vulnerabilities
- OTG-INPVAL-016: HTTP Splitting/Smuggling
- OTG-INPVAL-017: HTTP Incoming Requests
- OTG-INPVAL-018: Host Header Injection
- OTG-INPVAL-019: Server-Side Template Injection

#### Error Handling
- OTG-ERR-001: Analysis of Error Codes
- OTG-ERR-002: Analysis of Stack Traces

#### Cryptography
- OTG-CRYPST-001: Weak SSL/TLS Ciphers, Insufficient Transport Layer Protection
- OTG-CRYPST-002: Padding Oracle
- OTG-CRYPST-003: Sensitive Information via Unencrypted Channels

#### Business Logic Testing
- OTG-BUSLOGIC-001: Business Logic Data Validation
- OTG-BUSLOGIC-002: Ability to Forge Requests
- OTG-BUSLOGIC-003: Integrity Checks
- OTG-BUSLOGIC-004: Process Timing
- OTG-BUSLOGIC-005: Function Usage Limits
- OTG-BUSLOGIC-006: Circumvention of Work Flows
- OTG-BUSLOGIC-007: Defenses Against Application Misuse
- OTG-BUSLOGIC-008: Upload of Unexpected File Types
- OTG-BUSLOGIC-009: Upload of Malicious Files

#### Client Side Testing
- OTG-CLIENT-001: DOM-based XSS
- OTG-CLIENT-002: JavaScript Execution
- OTG-CLIENT-003: HTML Injection
- OTG-CLIENT-004: Client Side URL Redirect
- OTG-CLIENT-005: CSS Injection
- OTG-CLIENT-006: Client Side Resource Manipulation
- OTG-CLIENT-007: Cross Origin Resource Sharing (CORS)
- OTG-CLIENT-008: Cross Site Flashing
- OTG-CLIENT-009: Clickjacking
- OTG-CLIENT-010: WebSockets
- OTG-CLIENT-011: Web Messaging
- OTG-CLIENT-012: Local Storage

### SDLC Testing Framework (5 Phases)
1. **Before Development Begins**: Define SDLC, review policies/standards, develop metrics criteria
2. **During Definition and Design**: Review security requirements, review design/architecture, threat modeling
3. **During Development**: Code review, code analysis (static)
4. **During Deployment**: Penetration testing, configuration management testing
5. **During Maintenance and Operations**: Operational management reviews, periodic health checks, change verification

### Testing Techniques Classification
- **Black Box**: No knowledge of internals
- **White Box**: Full access to source code, architecture
- **Gray Box**: Partial knowledge
- **Passive**: Observation, information gathering
- **Active**: Direct probing and exploitation

### HTTP Verb Tampering Detailed Technique
- **Manual**: Craft custom HTTP requests via netcat; test all 8 HTTP/1.1 methods + WebDAV
- **Automated**: Bash script iterating methods; nmap http-methods NSE script
- **Expected Result**: Only GET and POST should succeed; all others should return 405/501

### HTTP Parameter Pollution (HPP)
- Different platforms handle duplicate params differently (ASP concatenates, JSP takes first, etc.)
- Can bypass WAF filters (ModSecurity bypass example)
- Authentication bypass (Blogger vulnerability example)
- Apple Cups XSS via HPP

### Risk Rating & Reporting
- **CVSS (Common Vulnerability Scoring System)**: FIRST standard, v2/v3
- **Risk = Likelihood × Impact**
- Report categories: vulnerability type, security threat, root cause, testing technique, remediation, severity rating (High/Medium/Low + CVSS)

---

## 5. OWASP ASVS 3.0 (Application Security Verification Standard)
*Project Leads: Andrew van der Stock, Daniel Cuthbert, Jim Manico*

### Three Verification Levels
- **Level 1 (Opportunistic)**: All software; OWASP Top 10 defense; easy-to-discover vulns; can be verified via automated tools
- **Level 2 (Standard)**: Sensitive data apps; B2B transactions; healthcare; business-critical functions; skilled attackers
- **Level 3 (Advanced)**: Military, health/safety, critical infrastructure; defense in depth; modular architecture; highest trust

### 19 Verification Categories (V1-V19)
| V# | Category | Key Requirements |
|----|----------|------------------|
| V1 | Architecture, Design & Threat Modelling | STRIDE; component identification; threat model |
| V2 | Authentication | MFA; password policies; credential recovery; brute force protection |
| V3 | Session Management | Session ID entropy; secure cookies; logout/invalidation |
| V4 | Access Control | Least privilege; authorization enforcement; IDOR prevention |
| V5 | Malicious Input Handling | SQLi, XSS, injection prevention; input validation/encoding |
| V6 | Output Encoding/Escaping | Context-aware encoding |
| V7 | Cryptography at Rest | Strong algorithms; key management; no custom crypto |
| V8 | Error Handling & Logging | No sensitive data in errors; secure logging |
| V9 | Data Protection | Classification; encryption at rest; tokenization |
| V10 | Communications Security | TLS; certificate validation; HSTS |
| V11 | HTTP Security Configuration | Security headers (CSP, X-Frame-Options, etc.) |
| V12 | Security Configuration | Secure defaults; patching; hardening |
| V13 | Malicious Controls | Anti-malware; integrity verification |
| V14 | Internal Security | Internal network controls |
| V15 | Business Logic | Workflow enforcement; transaction limits |
| V16 | Files & Resources | File upload validation; path traversal prevention |
| V17 | Mobile | Mobile-specific security controls |
| V18 | Web Services | REST/SOAP security; API authentication |
| V19 | Configuration | Build/deployment security |

### Industry-Specific ASVS Guidance
| Industry | L1 (all) | L2 | L3 |
|----------|----------|----|-----|
| Finance/Insurance | All network accessible apps | Sensitive info (credit cards, PII), limited money transfer | Large sums, wire transfers, rapid transfers |
| Manufacturing/Professional/Transportation/Technology/Utilities/Defense | All apps | Internal/employee info, IP, trade secrets | Valuable IP, classified/secret data, safety-of-life systems |
| Healthcare | All apps | Small/moderate PHI, PII, payment data | Medical equipment control, large transaction POS |
| Retail/Food/Hospitality | All apps | Small/moderate payment data | Large transaction POS, full credit card numbers, SSN |

### STRIDE Threat Model (V1 Requirement)
- **S**poofing
- **T**ampering
- **R**epudiation
- **I**nformation Disclosure
- **D**enial of Service
- **E**levation of Privilege

### ASVS Use Cases
1. **Security Testing Guide**: Scope penetration tests; organize activities; frame findings
2. **Secure SDLC**: Generate epics/user stories; peer review checklist; automated unit/integration tests
3. **Security Architecture**: Fill gaps in SABSA/TOGAF for application security
4. **Secure Coding Checklists**: Fork and customize per organization
5. **Automated Testing**: Build fuzz/abuse test cases into CI/CD
6. **Secure Development Training**: Proactive controls focus vs. negative Top 10

### OWASP Projects Using ASVS
- **Security Knowledge Framework (SKF)**: Python-Flask web app for secure coding training
- **OWASP ZAP**: Integrated penetration testing tool with automated scanners
- **OWASP Cornucopia**: Card game for security requirements in Agile development

### CWE Mapping
- ASVS v3.0 provides mapping to CWE for likelihood of exploitation and consequence analysis

### Guidance for Certifying Organizations
- Must include: scope, verification findings (passed + failed), resolution guidance
- Keep: work papers, screenshots, exploit scripts, proxy logs
- Tool-only reports insufficient; must demonstrate thorough testing of ALL requirements

---

## 6. CYBERSECURITY FUNDAMENTALS (ISACA Study Guide)
*Published 2015*

### 6 Core Sections
1. Cybersecurity Introduction and Overview
2. Cybersecurity Concepts
3. Security Architecture Principles
4. Security of Networks, Systems, Applications and Data
5. Incident Response
6. Security Implications and Adoption of Evolving Technology

### Cybersecurity Definition
- "Protection of information assets by addressing threats to information processed, stored and transported by internetworked information systems"
- Cybersecurity is a **subset** of Information Security
- Information Security covers ALL formats (paper, digital, verbal); Cybersecurity focuses on digital/networked assets

### CIA Triad with Controls (Exhibit 1.4)
| Requirement | Impact/Consequences | Methods of Control |
|-------------|---------------------|---------------------|
| Confidentiality | Disclosure of protected info, loss of public confidence/competitive advantage, legal action, interference with national security | Access controls, file permissions, encryption |
| Integrity | Inaccuracy, fraud, erroneous decisions, system compromise | Logging, digital signatures, hashes, encryption, access controls |
| Availability | Loss of productivity/revenue, inability to make decisions | Redundancy, backups, access control |

### NIST/ENISA 5 Cybersecurity Functions
1. **Identify**: Organizational understanding to minimize risk
2. **Protect**: Safeguards to limit impact on critical services
3. **Detect**: Activities to identify cybersecurity events
4. **Respond**: Take action after learning of security event
5. **Recover**: Resilience and timely repair of capabilities

### Risk Management
- Risk = combination of threat likelihood and impact
- Internal/external business and technology drivers affect risk posture
- Situational awareness: organization-specific culture and environment

### Common Attack Types and Vectors
- APTs (Advanced Persistent Threats): Sophisticated, multi-vector, resource-rich adversaries
- Attack vectors: platforms/tools, network connectivity, IT complexity, user community, emerging tech

### Security Architecture Principles
- **OSI Model**: 7 layers
- **Defense in Depth**: Multiple layers of security controls
- **Firewalls**: Types and configurations
- **Isolation and Segmentation**: Network zoning
- **Monitoring, Detection and Logging**: IDS/IPS, SIEM
- **Encryption Fundamentals**: Symmetric vs asymmetric, hashing
- **Encryption Techniques**: AES, RSA, ECC
- **Encryption Applications**: TLS/SSL, VPN, disk encryption

### Process Controls
- **Risk Assessments**: Identify, analyze, evaluate risks
- **Vulnerability Management**: Scan → Prioritize → Remediate → Verify
- **Penetration Testing**: Simulated attacks to validate defenses

### Network Security
- Firewalls, IDS/IPS, VPNs, network segmentation
- Remote access technology and systems administration

### Operating System Security
- System hardening
- Patch management
- Configuration baselines

### Application Security
- Secure SDLC
- Software security testing (SAST, DAST)
- Input validation, output encoding

### Data Security
- Classification
- Encryption at rest and in transit
- DLP (Data Loss Prevention)

### Incident Response
- **Event vs. Incident**: Event = observable occurrence; Incident = violation or threat of violation
- Incident Response Phases: Preparation → Detection/Analysis → Containment/Eradication/Recovery → Post-Incident Activity
- **Investigations**: Legal holds, preservation, chain of custody
- **Forensics**: Digital forensic data processing, network traffic analysis

### BCP/DRP
- Business Continuity Planning
- Disaster Recovery Planning
- Continuity of Operations

### Emerging Technology
- **Mobile**: Vulnerabilities, threats, risks; BYOD
- **Consumerization of IT**
- **Cloud and Digital Collaboration**: Security implications

### Cybersecurity Skills Gap (2013 Data)
- Estimated 410K-510K infosec professionals worldwide
- 53% job growth expected by 2018
- 56% of organizations report too few security professionals

---

## 7. OWASP TOP 10 - 2017
*The Ten Most Critical Web Application Security Risks*

### Risk Rating Methodology
| Factor | Scale |
|--------|-------|
| Threat Agents | App-specific |
| Exploitability | Easy (3), Average (2), Difficult (1) |
| Weakness Prevalence | Widespread (3), Common (2), Uncommon (1) |
| Weakness Detectability | Easy (3), Average (2), Difficult (1) |
| Technical Impacts | Severe (3), Moderate (2), Minor (1) |
| Business Impacts | Business-specific |

### Top 10 Risks

#### A1:2017 — Injection
- **Exploitability: 3, Prevalence: 2, Detectability: 3, Technical: 3**
- Types: SQL, NoSQL, OS command, ORM, LDAP, Expression Language (EL), OGNL
- **Detection**: Source code review (best), SAST/DAST in CI/CD pipeline, automated testing of all parameters/headers/URL/cookies/JSON/SOAP/XML
- **Prevention**: Safe API (parameterized interface), ORMs, whitelist server-side input validation, escape special characters, LIMIT controls
- **CWE**: 77 (Command Injection), 89 (SQL Injection), 564 (Hibernate), 917 (EL Injection)

#### A2:2017 — Broken Authentication
- **Exploitability: 3, Prevalence: 2, Detectability: 2, Technical: 3**
- Attacks: Credential stuffing, brute force, dictionary attacks
- **Prevention**: MFA, no default credentials, weak-password checks against top 10000 worst passwords, NIST 800-63B password policies, account enumeration hardening, rate limiting, secure session manager (server-side, high-entropy session IDs, proper invalidation)
- **CWE**: 287 (Improper Authentication), 384 (Session Fixation)

#### A3:2017 — Sensitive Data Exposure
- **Exploitability: 2, Prevalence: 3, Detectability: 2, Technical: 3**
- **Detection**: Check for cleartext transmission (HTTP, SMTP, FTP), cleartext storage, old/weak crypto, default keys, missing HSTS
- **Prevention**: Classify data, don't store unnecessarily, encrypt at rest (AES), encrypt in transit (TLS with PFS), disable caching, use Argon2/scrypt/bcrypt/PBKDF2 for passwords, enforce via HSTS
- **CWE**: 220, 310, 311, 312, 319, 326, 327, 359

#### A4:2017 — XML External Entities (XXE) [NEW]
- **Exploitability: 2, Prevalence: 2, Detectability: 3, Technical: 3**
- Attack vectors: File URI handler disclosure, internal port scanning, remote code execution, DoS
- **Detection**: SAST inspects dependencies/config; DAST requires manual steps
- **Prevention**: Disable DTDs/XML external entities, patch XML processors, use less complex formats (JSON), input validation

#### A5:2017 — Broken Access Control [MERGED: IDOR + Missing Function Level Access]
- **Exploitability: 2, Prevalence: 2, Detectability: 2, Technical: 3**
- Merged: A4-Insecure Direct Object References + A7-Missing Function Level Access Control (from 2013)
- Flaws: Access other users' accounts, view sensitive files, modify data, change access rights

#### A6:2017 — Security Misconfiguration
- **Exploitability: 3, Prevalence: 3, Detectability: 3, Technical: 2**
- Most commonly seen issue
- Causes: Insecure defaults, incomplete configs, open cloud storage, misconfigured HTTP headers, verbose errors
- All OS/frameworks/libraries/apps must be securely configured AND patched/upgraded

#### A7:2017 — Cross-Site Scripting (XSS)
- **Exploitability: 3, Prevalence: 3, Detectability: 3, Technical: 2**
- Types: Reflected XSS, Stored XSS, DOM XSS
- Effects: Hijack sessions, deface sites, redirect users

#### A8:2017 — Insecure Deserialization [NEW, Community]
- **Exploitability: 1, Prevalence: 2, Detectability: 2, Technical: 3**
- Leads to remote code execution
- Also enables: replay attacks, injection attacks, privilege escalation
- **Prevention**: Do not accept serialized objects from untrusted sources, integrity checks, isolate deserialization code, log/monitor

#### A9:2017 — Using Components with Known Vulnerabilities
- **Exploitability: 2, Prevalence: 3, Detectability: 2, Technical: 2**
- Components run with same privileges as application
- **Prevention**: Remove unused dependencies, monitor CVE/NVD, use software composition analysis tools, subscribe to security bulletins

#### A10:2017 — Insufficient Logging & Monitoring [NEW, Community]
- **Exploitability: 2, Prevalence: 3, Detectability: 1, Technical: 2**
- Average breach detection time: >200 days
- Typically detected by external parties, not internal processes
- **Prevention**: Log all login/access control/server-side validation failures; ensure logs have adequate context for security monitoring; establish effective monitoring and alerting; establish incident response and recovery plan

### Changes from 2013 to 2017
| 2013 → | 2017 |
|---------|------|
| A1 Injection | → A1 Injection |
| A2 Broken Auth/Session | → A2 Broken Authentication |
| A3 XSS | → A7 XSS (moved down) |
| A4 IDOR [Merged] | → A5 Broken Access Control (merged with A7) |
| A5 Security Misconfig | → A6 Security Misconfig |
| A6 Sensitive Data Exposure | → A3 Sensitive Data Exposure (moved up) |
| A7 Missing Function Level Access [Merged] | → A5 Broken Access Control (merged with A4) |
| A8 CSRF | → **Retired** (only 5% prevalence, frameworks include CSRF defenses) |
| A9 Using Known Vuln Components | → A9 Using Known Vuln Components |
| A10 Unvalidated Redirects | → **Retired** (~8% prevalence, edged out by XXE) |
| **NEW** | → A4 XXE |
| **NEW** | → A8 Insecure Deserialization |
| **NEW** | → A10 Insufficient Logging & Monitoring |

### Key Supporting OWASP Resources (Referenced)
- OWASP Proactive Controls
- OWASP ASVS
- OWASP Testing Guide
- OWASP Cheat Sheet Series
- OWASP Software Assurance Maturity Model (SAMM)
- OWASP Dependency Check
- OWASP ZAP (Zed Attack Proxy)
- OWASP Security Knowledge Framework (SKF)
- OWASP Cornucopia

### External Standards Referenced
- ISO 31000: Risk Management Standard
- ISO 27001: ISMS
- NIST Cyber Framework (US)
- ASD Strategic Mitigations (AU)
- NIST CVSS 3.0
- Microsoft Threat Modelling Tool
- NIST 800-63B (Password Guidelines)

---

## CROSS-REFERENCE: Common Frameworks Across All 7 Books

### CIA Triad
Present in: CISSP, Cybersecurity Fundamentals, CCSP (implicit)

### Risk Management
- **CISSP**: COBIT, third-party governance, documentation review, ATO
- **CCSP**: Risk management driven data separation, SOC reports
- **OWASP Top 10**: OWASP Risk Rating Methodology (Exploitability × Prevalence × Detectability × Impact)
- **Cybersecurity Fundamentals**: Risk assessment process; NIST Cyber Framework
- **OWASP Testing Guide**: CVSS v2/v3

### Encryption Standards
- **CISSP**: X.509, PKI (CA, RA, CRL, OCSP), SSL/TLS
- **WSTG/OTG**: SSL/TLS minimum checklist (≥128-bit, no SSLv2/3, no MD5, Forward Secrecy, no RC4)
- **OWASP Top 10**: Argon2, scrypt, bcrypt, PBKDF2 for passwords; AES for data at rest; TLS with PFS for transit
- **CCSP**: Crypto-shredding for cloud disposal

### Penetration Testing Methodologies
- **PTES** (7 phases): Pre-engagement → Intel Gathering → Threat Modeling → Vulnerability Analysis → Exploitation → Post Exploitation → Reporting
- **PCI DSS**: Requirement 11.3; external + internal; application + network layer
- **NIST 800-115**: Technical Guide to Information Security Testing
- **ISSAF**: Comprehensive framework with 20+ assessment areas
- **OSSTMM**: Operational security, trust analysis, STAR reporting
- **OWASP Testing Framework**: 5 SDLC phases, 12 testing categories, 91 controls

### Access Control Models
- **CISSP**: Administrative, Technical, Physical controls; deterrent → denial → detection → delay
- **ASVS V4**: Access Control Verification Requirements
- **OWASP Top 10 A5**: Broken Access Control
- **CCSP**: Multi-tenant access control (building, computer floor, cage/rack, hypervisor, guest OS, developer, customer, database, vendor, remote)

### Cloud Security Frameworks
- **CISSP**: SaaS/PaaS/IaaS, Public/Private/Community/Hybrid, NIST SP 800-145/800-144
- **CCSP**: Full cloud architecture, shared responsibility, cloud data lifecycle (6 phases), compensating controls, CASB, DRS/clustering
- **OWASP Top 10 A6**: Open cloud storage as security misconfiguration
- **WSTG-CONF**: Cloud storage testing (WSTG-CONF-11)

### SDLC Security Integration
- **OWASP ASVS**: Used as blueprint for Secure Coding Checklist; integrated into Agile sprints
- **OWASP Testing Guide**: 5-phase SDLC testing framework
- **OWASP Top 10**: Push left, right, everywhere; SAMM for maturity
- **CISSP**: Software Development Security Domain

### Incident Response & BCP/DRP
- **CISSP**: OEP, BCP, DRP; human safety first
- **Cybersecurity Fundamentals**: Event vs. Incident; preparation → detection → containment → recovery; forensics; legal holds
- **CCSP**: Audit logging, incident response legal preparation, chain of custody
