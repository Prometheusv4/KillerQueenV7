# Attack Priority Ranking — Based on H1 Bug Bounty Data

Rankings derived from HackerOne disclosed reports (14,617+ analyzed), H1 Bug Bounty Patterns skill, SOUL.md frequency data, and real bounty payout history. Priorities are informed by frequency, average bounty, exploitability, and impact — but Killer Queen determines the ACTUAL priority per engagement from the target's attack surface.

---

## I. VULNERABILITY CLASSES RANKED BY MULTI-FACTOR SCORE

Composite score = (Frequency × 0.3) + (Bounty Potential × 0.3) + (Exploitability × 0.2) + (Chain Potential × 0.2)

| Rank | Class | Frequency | Bounty Range | Exploitability | Chain Potential | Notes |
|------|-------|-----------|-------------|----------------|-----------------|-------|
| **1** | **SSRF** | 311+ reports | $500–$35K | High | VERY HIGH (11→RCE chains) | #1 highest-value primitive: chains to cloud metadata, internal services, RCE |
| **2** | **IDOR** | 253 reports | $500–$12.5K | HIGH | VERY HIGH (22→ATO chains) | #3 most common, #1 chain glue: 35.7% High/Critical |
| **3** | **SQLi** | 307 reports | $150–$25K | Medium-High | HIGH (6→RCE chains) | WAF bypass mature; DB-specific RCE paths well-known |
| **4** | **RCE** | 200+ reports | $1K–$33.5K | Low-Medium | CRITICAL (target) | High bounty but hard to find; typically chained from other primitives |
| **5** | **Stored XSS** | 104 reports | $500–$20K | Medium | HIGH (→ATO, admin hijack) | Higher bounty than reflected; admin panel targets |
| **6** | **Information Disclosure** | 209 reports | $100–$5K | High | Medium | #1 in frequency; rarely chains alone but enables everything else |
| **7** | **Account Takeover (ATO)** | 234 reports | $200–$35K | Medium | CRITICAL (target) | End goal, not a primitive; chains from XSS/IDOR/OAuth |
| **8** | **Reflected XSS** | 97 reports | $100–$1.5K | High | Low (unless chained) | Low standalone bounty; needs CSP bypass or chained context |
| **9** | **Logic Flaws** | 125 reports | $500–$10K | Medium-High | HIGH (28->AuthZ chains) | #5 in frequency; the glue that chains bugs together |
| **10** | **Subdomain Takeover** | 59 reports | $250–$3K | High | HIGH (→OAuth, cookie scope) | Consistent; DNS history/CNAME analysis gives easy wins |
| **11** | **Authorization Flaws** | 81 reports | $500–$8K | Medium | HIGH (28→Logic chain) | Often IDOR-adjacent; privilege escalation gateway |
| **12** | **CSRF** | 70 reports | $200–$2K | Medium | Medium (→XSS, →ATO) | Needs sensitive action to matter; common but low-severity alone |
| **13** | **Open Redirect** | 68 reports | $0–$1K | High | HIGH (→OAuth ATO) | Must chain to pay; OAuth code theft is the critical path |
| **14** | **File Upload** | 154 reports | $500–$10K | Medium | HIGH (→XSS, →RCE) | Chains to RCE via webshell/SVG/MIME; WP plugins a key vector |
| **15** | **Memory Corruption** | 39 reports | $2K–$30K | Low | CRITICAL | Hard to find but pays extremely well; browser/OS targets |
| **16** | **DoS** | 50 reports | $0–$1K | Medium | Low | Often rejected; emergency patches may pay |
| **17** | **Authentication Bypass** | 42 reports | $500–$20K | Low-Medium | CRITICAL | Pre-auth bypasses are rare but devastating |
| **18** | **LPE** | 38 reports | $500–$15K | Low-Medium | HIGH (→full compromise) | Post-exploit; kernel/driver targets |
| **19** | **XXE** | 25 reports | $500–$5K | Medium | Medium (→SSRF,→file read) | Declining; modern XML parsers disable DTDs by default |
| **20** | **Clickjacking** | 30 reports | $0–$500 | High | Low | Low bounty; typically needs sensitive action + no X-Frame-Options |

---

## II. TOP 20 "HUNT FIRST" TARGETS

Ordered by exploitability × impact for common bug bounty programs:

| Rank | Class | Hunt Priority Rationale |
|------|-------|------------------------|
| **1** | **SSRF** | Every webhook, URL fetch, image proxy, file import is a vector. Cloud metadata = instant critical. Hunt SSRF on EVERY engagement. Use interactsh for blind confirmation. |
| **2** | **IDOR** | Every API with numeric/sequential IDs. Check GET→PUT→DELETE. UUIDs don't guarantee safety. Test sibling endpoints, API versions. |
| **3** | **Subdomain Takeover** | Subfinder + CNAME check = 5 minutes. Especially valuable on OAuth redirect_uri subdomains. |
| **4** | **Stored XSS** | Every input that gets rendered back. Check: comment fields, profile bios, file names, markdown fields, email rendering. Prioritize inputs viewed by admins. |
| **5** | **Information Disclosure in JS** | JS bundles = treasure maps. grep for: API keys, Firebase configs, internal endpoints, postMessage listeners, S3 bucket names. |
| **6** | **SQLi** | Search/sort/filter parameters. ORM wrappers: Django JSONField, Sequelize raw, Mongoose $where. Try header-based injection to bypass URL WAFs. |
| **7** | **Business Logic / Race Conditions** | Coupon codes, wallet transactions, invitation systems, rate limit bypass. Send concurrent requests with Turbo Intruder. |
| **8** | **OAuth Misconfigurations** | Missing PKCE, redirect_uri bypass, scope escalation, state parameter reuse, CSRF on authorization endpoint. |
| **9** | **Open Redirect (for chaining)** | Find ANY open redirect. Immediately chain to OAuth flow if present. Search for `redirect_uri`, `return_url`, `next`, `callback`. |
| **10** | **JWT Attacks** | alg=none, HS256→RS256 confusion, kid parameter injection, jku header SSRF, empty signature. Check every Bearer token. |
| **11** | **File Upload Bypass** | SVG for XSS, double extension, null byte, MIME spoof, polyglot files, ZIP slip. On WordPress: CF7 dnd upload plugin if ≤1.3.9.7. |
| **12** | **GraphQL Introspection** | `__schema { types { name fields { name } } }` → auth bypass on mutations, IDOR via node(id), injection in arguments. |
| **13** | **Web Cache Deception** | Append `.css`/`.js`/`.png` to authenticated endpoints. CDN caches public; victim sees private data. |
| **14** | **CSRF on Sensitive Actions** | Password change, email change, API key creation, 2FA disable. Check for anti-CSRF token bypasses. |
| **15** | **Prototype Pollution** | Client-side (DOM XSS via `__proto__`) and server-side (Lodash, Mongoose). Check JSON merge/path assignment endpoints. |
| **16** | **Dependency Confusion** | Internal package names → publish same name on public npm/pip registry → auto-installed by CI/CD. |
| **17** | **SSTI** | Template rendering with user input. Test: `{{7*7}}` (Jinja2), `${7*7}` (Freemarker). RCE via class walker pattern. |
| **18** | **Request Smuggling** | CL.TE or TE.CL on front-end/back-end proxy setups. Test with Turbo Intruder CL.TE/TE.CL scripts. |
| **19** | **CORS Misconfigurations** | `Access-Control-Allow-Origin: *` with credentials. `Origin` reflection. Check `null` origin bypass. |
| **20** | **Email/SMTP Attacks** | SPF/DKIM/DMARC analysis. SMTP smuggling for email spoofing. SMTP AUTH brute force (often unmonitored). |

---

## III. PER-ENGAGEMENT-TYPE PRIORITY LISTS

### WEB APPLICATION (Bug Bounty / Pentest)

**Tier 1 — Hunt Immediately (High Value, Low Effort)**
1. SSRF (webhooks, URL imports, image proxies)
2. IDOR (every numeric ID endpoint)
3. Subdomain Takeover (DNS/CNAME check)
4. JS Secret Exposure (grep bundles for keys/tokens)
5. Information Disclosure (JS maps, robots.txt blind spots, sitemap)

**Tier 2 — Hunt After Tier 1 Exhausted**
6. Stored XSS (admin-viewed inputs)
7. SQLi (search/sort/filter + ORM bypass)
8. OAuth Misconfigurations
9. Open Redirect (for OAuth chaining)
10. Business Logic / Race Conditions

**Tier 3 — Deep Dive**
11. JWT Attacks
12. File Upload Bypass
13. GraphQL Introspection
14. Web Cache Deception
15. CSRF on Sensitive Actions
16. Prototype Pollution
17. SSTI
18. Request Smuggling
19. CORS Misconfigurations
20. XXE

### CLOUD / AWS ENGAGEMENT

**Tier 1 — Immediate**
1. SSRF→IMDS credential theft (check every URL fetch)
2. S3 bucket enumeration (public read/write, list)
3. IAM privilege escalation (enumerate current permissions, find privesc paths)
4. Cloud metadata endpoints (169.254.169.254 variants)
5. Lambda environment variable exposure

**Tier 2 — After Recon**
6. GuardDuty evasion patterns
7. CloudTrail log analysis
8. Cross-account trust exploitation
9. CI/CD pipeline injection
10. Container escape (EC2→Docker→host)

**Tier 3 — Post-Exploitation**
11. IAM persistence (access keys, roles, Lambda layers)
12. Organization-level attacks
13. Resource policy abuse
14. CloudFormation template injection
15. Cognito misconfigurations

### ACTIVE DIRECTORY ENGAGEMENT

**Tier 1 — Recon (Pre-Auth)**
1. LDAP anonymous bind enumeration
2. AS-REP Roasting (users with no preauth)
3. Kerberos user enumeration (kerbrute)
4. SMB signing check (NetExec across subnet)
5. LLMNR/NBT-NS poisoning (Responder)

**Tier 2 — Low-Priv Credential Access**
6. Kerberoasting (crackable TGS tickets)
7. Password spraying (common passwords across users)
8. LDAP signed enumeration (BloodHound data collection)
9. SMB share enumeration + read access

**Tier 3 — Privilege Escalation**
10. AD CS attack paths (Certify → ESC1-8)
11. Kerberos delegation abuse (RBCD, S4U2Self, Bronze Bit)
12. DACL abuse (GenericAll, WriteDacl, AddSelf)
13. DCSync (Replication Directory rights)
14. NTLM relay (PetitPotam→AD CS, mitm6→LDAP)

**Tier 4 — Domain Dominance**
15. Golden Ticket (krbtgt hash)
16. Silver Ticket (service hashes)
17. Skeleton Key (LSASS patching)
18. DCShadow / AdminSDHolder persistence

### MOBILE APPLICATION ENGAGEMENT

**Tier 1 — Static Analysis**
1. Hardcoded secrets (API keys, tokens, private keys in APK/IPA)
2. exported components in AndroidManifest.xml
3. WebView JavaScript interface exposure
4. Deeplink/scheme hijacking
5. Firebase/cloud config exposure

**Tier 2 — Dynamic Analysis**
6. SSL pinning bypass (Frida/Objection)
7. Root/Jailbreak detection bypass
8. Runtime API interception (Frida hooks)
9. Insecure local storage (SharedPreferences, plist, SQLite)
10. Tapjacking / overlay attacks

**Tier 3 — Advanced**
11. Biometric bypass
12. IPC vulnerabilities
13. Native library reverse engineering
14. Keystore/Keychain extraction
15. Backup extraction analysis

### IoT / EMBEDDED ENGAGEMENT

**Tier 1 — Firmware Analysis**
1. Firmware extraction (binwalk/unblob)
2. Hardcoded credentials in filesystem
3. Encryption key extraction
4. Default web interface exploitation
5. Hardcoded URLs/endpoints

**Tier 2 — Hardware Interface**
6. UART console access (check for root shell)
7. JTAG/SWD debug access (memory dump, code execution)
8. SPI flash dump (bootloader, secure boot bypass)
9. Firmware update mechanism (downgrade, MITM, unsigned)

**Tier 3 — Protocol Analysis**
10. MQTT/CoAP/HTTP protocol exploitation
11. Zigbee/BLE/Z-Wave sniffing
12. CAN bus injection (automotive)
13. NFC cloning/replay
14. Side-channel analysis (power/EM)

---

## IV. BOUNTY PAYOUT SPECTRUM BY SEVERITY

| Severity | Typical Range | Example Targets | Notes |
|----------|--------------|-----------------|-------|
| **Critical** ($10K–$35K+) | Pre-auth RCE, mass ATO, auth bypass to admin, dependency confusion RCE, critical info disclosure, multi-step chains | GitLab, PayPal, X, Valve | Rare but highest payout; typically chain-based |
| **High** ($3K–$10K) | SSRF→cloud metadata, IDOR exposing financial/PII data, SQLi with data extraction, Stored XSS in admin panels, Blind XSS hitting internal dashboards | Uber, Shopify, Dropbox, Stripe | Most common "good" finding range |
| **Medium** ($900–$3K) | Reflected XSS with CSP bypass, CSRF on sensitive action, file upload to non-RCE, Subdomain takeover, info disclosure enabling exploit chains | Various | Needs demonstrated impact beyond technical |
| **Low** ($150–$900) | Reflected XSS (no CSP bypass), standalone open redirect, low-impact info disclosure, missing security headers, rate limiting on non-critical | Most programs | Common; look for chain opportunities |
| **None** ($0) | Self-XSS without escalation, open redirect alone, "admin can do X", "could theoretically lead to...", logout CSRF, mixed content, clickjacking on non-sensitive | VDP programs, U.S. DoD | Only worth reporting if chainable |

---

## V. TOP CHAINS BY VALUE (From H1 Data)

| Chain Pattern | Max Bounty Seen | Frequency in H1 | Required Primitives |
|---------------|----------------|-----------------|---------------------|
| **SSRF → Internal Service → RCE** | $33,510 (GitLab) | 11 documented | SSRF + internal service (FastCGI, Jenkins, Redis) |
| **SSRF → Cloud Metadata → IAM Creds → Account Takeover** | $17,576 (Dropbox) | Frequent | SSRF + AWS/GCP/Azure IMDS access |
| **Cache Poisoning → Stored XSS → All Users** | $20,000 (PayPal) | 1 documented | Cache poisoning + XSS reflection |
| **Info Disclosure → IDOR → Privilege Escalation → Critical** | $12,500 (H1) | 22 ATO chains | Leaked IDs + missing auth |
| **OAuth Misconfig → Open Redirect → Code Theft → ATO** | $10,000+ (estimated) | Frequent | Open redirect + OAuth flow |
| **Dependency Confusion → Package Install → RCE** | $30,000 (PayPal) | Emerging | Internal package names + public registry |
| **Subdomain Takeover → OAuth redirect_uri → ATO** | Critical (theoretical) | Consistent | DNS takeover + OAuth |
| **XSS → CSRF → Admin Action** | Critical | Frequent | XSS + sensitive CSRF |
| **File Upload → SVG/XSS → Session Theft → ATO** | $10,000+ | Common on WP | Upload + SVG rendering |
| **Prototype Pollution → child_process.spawn → RCE** | $20,000+ | Kibana, Node.js apps | PP + gadget chain |

---

## VI. DATA SOURCES

- **H1 Bug Bounty Patterns skill** — 14,617+ disclosed H1 reports, bounty ranges, chain patterns
- **Pentester.Land frequency data** — 2,222 real bug bounty writeups (2018-2022)
- **SOUL.md §Pentester.Land** — Top 20 classes by frequency, top chain patterns
- **arXiv BOLA Study** — 107 classified H1 IDOR reports
- **HackerOne Top Writeups** — Highest single bounties per class
- **Real engagement data** — azzrk.com engagement (WordPress → SMTP/email pivot)

---

## VII. ADAPTIVE PRIORITIZATION RULE

**Killer Queen determines the priority order per engagement. No fixed list.**

1. Read the attack surface — map everything before ranking anything
2. Identify the path of least resistance — what's the weakest door?
3. Order vectors by exploitability × impact — what's easiest AND most damaging?
4. Report the priority order to the operator before executing

**Pitfall:** Carrying a priority list from a previous engagement. A hardened WordPress site on Contabo prioritizes credential attacks and infrastructure probing. A cloud-native SaaS startup prioritizes SSRF, IDOR, and cloud misconfig. A mobile app prioritizes hardcoded secrets and API auth bypass. Killer Queen adapts. Always.
