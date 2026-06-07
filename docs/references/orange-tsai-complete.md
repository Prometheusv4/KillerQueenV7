# Orange Tsai — Complete Technique Knowledge Base

> **Source**: orange_8361 (Orange Tsai), Principal Security Researcher at DEVCORE
> **Repository**: https://github.com/orangetw/My-Presentation-Slides
> **Blog**: https://blog.orange.tw/
> **Pwnie Awards**: Best Server-Side Bug 2019, 2021
> **Pwn2Own**: Champion & Master of Pwn 2021, 2022
> **Top 10 Web Hacking Techniques**: 1st place 2017, 2018

---

## ACHIEVEMENTS SUMMARY

- **RCE on**: Facebook (×2), Apple, Yahoo, Uber, GitHub, Twitter
- **Pwn2Own**: Sonos One (2021/2022), Exchange (2021), Multiple targets
- **CVEs**: 30+ assigned across multiple products
- **Known for**: Discovering new attack CLASSES (not just individual bugs)

---

## ATTACK CLASS PHILOSOPHY

Orange Tsai's research consistently follows a pattern: discover architectural flaws and systemic attack surfaces rather than individual bugs. His four pillars:

1. **架構 (Architecture)** — Find architectural weaknesses in widely-used systems
2. **底層 (Foundations)** — Exploit low-level mechanisms (encodings, parsers, protocols)
3. **不一致 (Inconsistency)** — Exploit semantic gaps between components
4. **跨應用 (Cross-Application)** — Chain bugs across different applications

---

# RESEARCH TIMELINE

---

## 2024 — WORSTFIT: Windows ANSI Best-Fit Attacks

**Talk**: Black Hat Europe 2024
**Slides**: `2024-WorstFit-Unveiling-Hidden-Transformers-in-Windows-ANSI.pdf`
**Co-author**: Splitline Huang
**Website**: https://worst.fit/

### Attack Class Discovered
**Best-Fit Character Conversion Abuse** — Windows' internal mechanism that maps UTF-16 characters to "closest" ANSI code page equivalents when an exact match doesn't exist.

### Root Cause
Windows dual API design (ANSI "A" vs Unicode "W") means ANSI APIs (`GetEnvironmentVariableA`, `getenv`, CRT `main()`) silently apply Best-Fit conversion via `RtlUnicodeStringToAnsiString` / `WideCharToMultiByte`.

### Three Attack Techniques

#### 1. CVE-2024-4577 — PHP-CGI Argument Injection (Bypass of CVE-2012-1823)
- **Threat Character**: `U+00AD` (soft hyphen) → `-` (dash) in Best-Fit
- **Affected Code Pages**: 932 (Japanese), 936 (Simplified Chinese), 950 (Traditional Chinese)
- **Payload**: `?%ADs` → bypasses PHP's 2012 patch that blocked query strings starting with `-`
- **Impact**: RCE on PHP-CGI installations on CJK Windows systems
- **How**: `getenv("QUERY_STRING")` returns ANSI, turning `%AD` into `-`, re-enabling argument parsing

#### 2. Filename Smuggling (Path Traversal)
- **Threat Characters**:
  - `／` (U+FF0F Fullwidth solidus) → `/` (many code pages)
  - `＼` (U+FF3C Fullwidth reverse solidus) → `\` (many code pages)
  - `¥` (U+00A5 Yen sign) → `\` (Japanese CP932)
  - `₩` (U+20A9 Won sign) → `\` (Korean CP949)
- **Affected Code Pages**: 874, 125x, 932, 949
- **Relevant APIs**: `GetCurrentDirectoryA`, `getcwd`, `FindFirstFileA`, `GetFullPathNameA`
- **Demo**: Chrome V8 d8.exe, mruby `Dir.getwd`
- **Real-world case**: Cuckoo Sandbox RCE via malicious Unicode filename

#### 3. Argument Splitting (Command Injection)
- **Threat Characters**:
  - `＂` (U+FF02 Fullwidth quotation mark) → `"` (125x, 874)
  - `＼` (U+FF3C), `¥`, `₩` → `\`
- **Relevant APIs**: `GetCommandLineA`, CRT `main()`
- **How**: Libraries escape arguments correctly (PHP `escapeshellarg`, Python `subprocess.list2cmdline`), but when the child process reads command line via ANSI APIs, Best-Fit transforms characters AFTER escaping, breaking the escaping

### CVEs
- CVE-2024-4577 — PHP-CGI Argument Injection

### Target Software
- PHP-CGI on Windows (CJK locales)
- Any C/C++ application using ANSI APIs on Windows
- Cuckoo Sandbox, Chrome V8, mruby

---

## 2024 — CONFUSION ATTACKS: Apache HTTP Server

**Talk**: Black Hat USA 2024
**Slides**: `2024-Confusion-Attacks-Exploiting-Hidden-Semantic-Ambiguity-in-Apache-HTTP-Server!.pdf`
**Blog**: https://blog.orange.tw/posts/2024-08-confusion-attacks-en/

### Attack Class Discovered
**Semantic Ambiguity Exploitation** — Exploiting the fact that Apache's ~136 modules share a giant `request_rec` structure with no strict semantic contract, leading modules to disagree on what fields mean.

### Three Confusion Attack Families

#### 1. Filename Confusion
Modules disagree: is `r->filename` a filesystem path or a URL?

**Primitive 1-1: Truncation (via mod_rewrite)**
- `mod_rewrite` calls `splitout_queryargs()` which truncates at `?` (`%3F`), treating result as URL
- **Path Truncation**: `RewriteRule ^/user/(.+)$ /var/user/$1/profile.yml` → `%3F` drops `/profile.yml`
- **Mislead RewriteFlag Assignment**: `RewriteRule ^(.+\.php)$ $1 [H=application/x-httpd-php]` — truncation after regex match applies PHP handler to files like `1.gif%3Fooo.php` → backdoor

**Primitive 1-2: ACL Bypass (via mod_proxy + PHP-FPM)**
- `<Files "admin.php">` auth is bypassed because `mod_proxy` treats `r->filename` as URL, but auth modules treat it as path
- Request: `admin.php%3Fooo.php` — auth sees `admin.php?ooo.php` ≠ `admin.php`, grants access
- PHP-FPM normalizes by stripping query string, executes `admin.php` without auth

#### 2. DocumentRoot Confusion
`mod_rewrite` always tries to open BOTH the raw path and DocumentRoot-prefixed path

**Primitive 2-1: Server-Side Source Code Disclosure**
- CGI disclosure: access via absolute path bypasses `ScriptAlias`
- PHP disclosure: use different vhost without PHP handler

**Primitive 2-2: Local Gadgets Manipulation**
- Debian/Ubuntu `/usr/share` is readable
- Gadgets: `dump-env.php` (info disclosure), help.html (XSS), `proxy.php` (LFI/SSRF), legacy PHPUnit (RCE)

#### 3. Handler Confusion
Exploits `AddType` vs `AddHandler` ambiguity + legacy code from 1996
- XSS/CRLF injection in CGI response headers can transform to RCE via `mod_cgi` handler confusion
- `AddType` can be abused with `SetHandler` to execute arbitrary files
- 30+ case studies documented

### CVEs (9 new)
- CVE-2024-38472 — Windows UNC SSRF
- CVE-2024-39573 — mod_rewrite proxy handler substitution
- CVE-2024-38477 — DoS in mod_proxy
- CVE-2024-38476 — Malicious backend output runs local handlers via internal redirect
- CVE-2024-38475 — mod_rewrite weakness when first segment matches filesystem path
- CVE-2024-38474 — Encoded question marks in backreferences
- CVE-2024-38473 — mod_proxy proxy encoding problem
- CVE-2023-38709 — HTTP response splitting
- CVE-2024-?????? — [redacted]

### Exploitation Techniques (20 total)
- Path Truncation, Mislead RewriteFlag, ACL Bypass, CGI Source Disclosure, PHP Source Disclosure, Local Gadgets, Handler Confusion, Internal Redirect Abuse, Content-Type Confusion, and more

### Target Software
- Apache HTTP Server (all versions before 2.4.60), PHP-FPM, mod_rewrite, mod_proxy, mod_cgi

---

## 2022 — IIS Hash Table Cache Destabilization

**Talk**: Black Hat USA 2022, DEFCON, HITCON, CODE BLUE
**Slides**: `2022-Lets-Dance-in-the-Cache-Destabilizing-Hash-Table-on-Microsoft-IIS.pdf`

### Attack Class Discovered
**Hash Table Cache Poisoning** — Destabilizing IIS's internal hash table to cause authentication bypass via cache confusion.

### Key Technique
- Hash-flooding attack against IIS internal hash tables
- Degenerate hash table to single linked-list (O(n) instead of O(1))
- Manipulate caching behavior to serve incorrect/unauthorized responses
- All passwords valid demo — exploiting hash collisions to bypass auth

---

## 2021 — MICROSOFT EXCHANGE: The Proxy Era

**Talks**:
- Black Hat USA 2021: `2021-ProxyLogon-is-Just-the-Tip-of-the-Iceberg.pdf`
- POC2021/CODE BLUE/HITCON: `2021-The-Proxy-Era-Of-Microsoft-Exchange-Server.pdf`

### Attack Class Discovered
**Frontend-Backend Proxy Confusion** — Exploiting Exchange's Client Access Service (CAS) proxy architecture to access backend services without authentication.

### Architecture
Exchange split into Frontend (CAS proxy) and Backend (Mailbox). Frontend proxies HTTP requests to Backend, synchronizing state via custom HTTP headers.

### Four Attack Chains

#### 1. ProxyLogon (Pre-auth RCE)
- **CVE-2021-26855** — SSRF to access backend without auth
- **CVE-2021-27065** — Arbitrary file write via backend
- **Discovered with**: Volexity and MSTIC
- **Patch**: March 2021 (emergency out-of-band)
- **Impact**: 400,000+ Exchange servers exposed

#### 2. ProxyOracle (Plaintext Password Recovery)
- **CVE-2021-31196** — Cookie manipulation
- **CVE-2021-31195** — Response manipulation
- **Technique**: Chain backend access with cookie/header manipulation to recover plaintext credentials

#### 3. ProxyShell (Pre-auth RCE, Pwn2Own 2021)
- **CVE-2021-34473** — Path confusion
- **CVE-2021-34523** — Privilege escalation
- **CVE-2021-31207** — Arbitrary file write
- **Demo**: Pwn2Own 2021, working with ZDI

#### 4. ProxyRelay (Authentication Bypass)
- **CVE-2021-33768** — Relay attack
- **CVE-2021-33766** — Token manipulation
- **Technique**: Relay authentication tokens to read all victim's emails

### Key Techniques
- HTTP header blacklist bypass (custom headers like `X-CommonAccessToken`, `X-IsFromCafe`)
- Cookie forwarding manipulation
- Backend Rehydration Module abuse
- Kerberos ticket generation hijacking
- `CommonAccessToken` serialization manipulation
- `ShouldBackendRequestBeAnonymous()` bypass

### CVEs
- CVE-2021-26855, CVE-2021-27065, CVE-2021-31196, CVE-2021-31195
- CVE-2021-34473, CVE-2021-34523, CVE-2021-31207
- CVE-2021-33768, CVE-2021-33766, CVE-2021-28480, CVE-2021-28481

---

## 2021 — Web + Binary Exploitation Chain

**Talk**: RealWorld CTF Live Forum, OWASP Hong Kong
**Slides**: `2021-A-Journey-Combining-Web-and-Binary-Exploitation-in-Real-World.pdf`
**Blog**: https://blog.orange.tw/posts/2021-02-a-journey-combining-web-and-binary-exploitation/

### Attack Class Discovered
**Web-to-Binary Exploitation Chain** — Combining web application logic bugs with OS-level binary exploitation for full compromise

### Exploitation Chain Architecture

#### Stage 1: PHP Type Juggling → Secret Key Recovery
- **Target**: PHPWind (Chinese forum software)
- **Technique**: PHP type juggling — `md5(array())` returns `NULL`
- `password[]=` bypasses password check because `md5([])` = `NULL` = empty password for public forums
- Leak hashed `site_hash` via cookie manipulation
- Crack with HashCat (RTX 2080 Ti, ~1 hour for 8-char alphanumeric)

#### Stage 2: PHP Deserialization → Use-After-Free
- **CVE-2015-0273** — PHP Use-After-Free in `unserialize()` with DateTime/DateTimeZone
- Forge encrypted cookies using recovered `site_hash`
- Trigger `unserialize()` on attacker-controlled data via `PwOnlineService::forumOnline()`

#### Stage 3: Binary Exploitation
- **Target**: PHP 5.3.27 (ZTS — Zend Thread Safety build)
- **Challenge**: No known gadgets, no SoapClient/GMP, `__autoload` forbids slashes (no namespace bypass on Linux)
- **Solution**: Exploit CVE-2015-0277 (different from PornHub case which used non-ZTS build)
- Build Read/Write primitive → Control-flow hijack
- **Key difference from PornHub**: ZTS means `sapi_globals` location unknown (in TLS, not BSS)

### Key Techniques
- PHP Type Juggling (`md5(array())` → NULL)
- PRNG seed recovery (Mersenne Twister, 32-bit seed)
- xxTEA encryption reversal
- PHP UAF via DateTime __wakeup → `convert_to_long` frees string
- Read primitive via `R` type specifier in serialization
- Blind binary exploitation (unknown target environment)

### CVE
- CVE-2015-0273 (PHP UAF)
- CVE-2015-0277 (related UAF)

---

## 2020 — MobileIron MDM RCE (Facebook Again)

**Talk**: HITCON 2020
**Slides**: `2020-How-I-Hacked-Facebook-Again.pdf`

### Attack Class Discovered
**MDM Protocol Abuse** — Exploiting Mobile Device Management infrastructure

### Key Techniques
- **Architecture**: Reverse Proxy (Apache) → Tomcat → MI Server, with TLS Proxy
- **Bypass technique**: URL path manipulation to reach Hessian web services
  - Normal: `/mifs/services/fooService` (blocked)
  - Bypass: `/mifs/.;/services/fooService` (Apache mod_rewrite off-by-slash)
- **Hessian Deserialization**: Exploited Java Hessian binary protocol
  - Spring-AOP → JNDI Injection
  - XBean → JNDI Injection
  - Resin → JNDI Injection
  - ROME → RCE
- **JNDI Injection** for RCE

### Target
- MobileIron MDM (used by Facebook and 20,000+ enterprises)

---

## 2019 — SSL VPN Pre-auth RCE

**Talk**: Black Hat USA 2019, DEFCON, HITCON, CODE BLUE
**Slides**: `2019-blackhat-Infiltrating-Corporate-Intranet-Like-NSA.pdf`

### Attack Class Discovered
**SSL VPN Architecture Exploitation** — Systematic exploitation of SSL VPN products

### Two Major Chains

#### 1. Fortinet FortiGate SSL VPN — Pre-auth Root RCE
- Hard-core binary exploitation chain
- Magic backdoor technique
- Full root access on FortiGate SSL VPN appliances

#### 2. Pulse Secure SSL VPN — Pre-auth Root RCE
- Out-of-box web exploitation chain
- **Highest bug bounty from Twitter ever**
- Arbitrary file read → credential extraction → RCE

### Key Techniques
- Defense-in-depth bypass in SSL VPN gateways
- Web-based pre-auth exploitation
- Binary exploitation in embedded network appliances

### Target Software
- Fortinet FortiGate SSL VPN
- Pulse Secure SSL VPN
- Palo Alto GlobalProtect

---

## 2019 — Jenkins Meta-Programming RCE

**Talks**: Pass the Salt, Becks.io, HITB GSEC
**Slides**: `2019-Hacking-Jenkins-Pass-the-Salt.pdf`
**Blog Parts**: Hacking Jenkins Part 1 & 2

### Attack Class Discovered
**Compile-Time Meta-Programming Abuse** — Exploiting Groovy DSL's AST parsing phase to achieve code execution where runtime execution was blocked

### Exploitation Chain

#### Stage 1: ACL Bypass — CVE-2018-1000861
- Jenkins Stapler dynamic routing (`/foo/bar/1/baz/` → `Jenkins.getFoo().getBar(1).getBaz("orange")`)
- **Problem 1**: Every class inherits Object — `/class/classLoader/resource/index.jsp/content` accesses URLClassLoader
- **Problem 2**: URL prefix whitelist bypass via `getSecurityRealm().getUser(name).getSearch()`
- Combined: pre-auth SSRF + information leakage

#### Stage 2: Sandbox Bypass — CVE-2019-1003000/3001/3002
- Pipeline is Groovy DSL → only AST parsing in syntax check, no `execute()`
- **Meta-Programming insight**: Groovy AST transformations execute at compile-time during parsing
- `@Grab` annotation → downloads and loads JARs from attacker-controlled URL
- Compile-time annotation processing bypasses sandbox restrictions

### CVEs
- CVE-2018-1000600 — CSRF in GitHub Plugin
- CVE-2018-1000861 — Code execution through crafted URLs (ACL bypass)
- CVE-2018-1999002 — Arbitrary file read
- CVE-2018-1999046 — Unauthorized agent log access
- CVE-2019-1003000 — Sandbox Bypass in Script Security Plugin
- CVE-2019-1003001 — Sandbox Bypass
- CVE-2019-1003002 — Sandbox Bypass

### Target
- Jenkins CI/CD (all versions, Stapler framework)

---

## 2019 — SSRF: URL Parser Exploitation

**Talk**: Black Hat USA 2019 (presented at Black Hat Asia 2018)
**Slides**: `2019-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf`
**Blog**: GitHub Enterprise RCE chain

### Attack Class Discovered
**URL Parser Inconsistency** — Systematic exploitation of differences between URL parsers and URL requesters across programming languages

### Key Techniques

#### 1. CR-LF Injection in URL Protocols
- Inject `\r\n` into URL to smuggle protocols
- HTTP → SMTP smuggling: `http://127.0.0.1:25/%0D%0AHELO orange.tw%0D%0AMAIL FROM...`
- **TLS SNI smuggling**: Inject CR-LF into SNI field of TLS handshake (not encrypted!), smuggle SMTP over HTTPS
  ```
  https://127.0.0.1□%0D%0AHELO□orange.tw%0D%0AMAIL□FROM…:25/
  ```

#### 2. URL Parser Confusion Matrix
| Library | Host Injection | Path Injection | Port Injection |
|---------|---------------|----------------|----------------|
| Python httplib | ✓ | ✓ | ✓ |
| Python urllib | ✓ | ✓ | - |
| Ruby Net::HTTP | ✓ | ✓ | ✓ |
| Java net.URL | ✓ | - | - |
| Perl LWP | - | ✓ | - |
| NodeJS http | ✓ | - | - |
| PHP http_wrapper | - | ✓ | - |
| cURL | - | ✓ | - |

#### 3. Specific Bypass Techniques
- **Double port**: `http://127.0.0.1:11211:80/` — PHP parse_url sees port 80, actual request goes to 11211
- **Fragment confusion**: `http://google.com#@evil.com/` — PHP parse_url sees google.com, cURL connects to evil.com
- **Multiple @ signs**: `http://foo@evil.com:80@google.com/` — most parsers get confused
- **NodeJS Unicode**: `／` (U+FF0F) → `/`, `Ｎ` (U+FF2E) → bypass `..` check
- **NodeJS CR-LF bypass**: Unicode `－＊` (U+FF0D U+FF0A) → `\r\n` after HTTP module encoding
- **GLibc NSS**: `ns_name_pton()` features

### Real-World Impact
- GitHub Enterprise RCE via SSRF chain (4 chained bugs)
- Redis, Memcached, Elastic, SMTP smuggling

---

## 2018 — Breaking Parser Logic: Path Normalization

**Talk**: Black Hat USA 2018, DEFCON, CODE BLUE, Hack.lu
**Slides**: `2018-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out.pdf`
**Blog**: Amazon Collaboration System RCE (4 chained bugs)

### Attack Class Discovered
**Path Normalization Inconsistency** — Systematic exploitation of differences between path normalization algorithms and filesystem behavior

### CVEs Discovered (8+)

| CVE | Software | Description |
|-----|----------|-------------|
| CVE-2018-1271 | Spring Framework | Directory Traversal on Windows (bypass of CVE-2014-3625) |
| CVE-2018-3760 | Ruby on Rails | Path traversal in Sprockets (file:// scheme bypass) |
| CVE-2018-9159 | Spark Framework | Code infectivity (copied Spring's broken cleanPath) |
| CVE-2018-1999002 | Jenkins | Arbitrary file read |
| CVE-2018-14371 | Mojarra (JSF) | 5-year-old CVE-2013-3827 bypass |
| CVE-2018-7212 | Sinatra | Path traversal |
| CVE-2018-6184 | Next.js | Path traversal |
| CVE-2018-3732 | resolve-path (npm) | Path traversal |

### Key Techniques

#### Spring Framework CVE-2018-1271
- `cleanPath()` algorithm bug: empty elements not handled correctly
- `/foo//../` → `/foo/` (cleanPath) but → `/` (filesystem)
- `/foo///../../` → `/foo/` (cleanPath) but → `/../` (filesystem)
- Double encoding: `%255c` → `%5c` → `\` to bypass URL decode → cleanup → filesystem

#### Ruby on Rails CVE-2018-3760 (Sprockets)
- `file://` scheme bypasses `absolute_path?` check
- Double encoding bypass: `%252e%252e` → `%2e%2e` after first decode → `..` after second decode
- RCE via ERB template injection: `?type=text/plain` forces rendering of .erb files

#### Nginx Off-by-Slash
- `location /static { alias /home/app/static/; }` — missing trailing slash
- `http://server/static../settings.py` → `/home/app/static/../settings.py`

#### Java EE Path Parameter
- `http://example.com/foo;name=orange/bar/` — Tomcat/Jetty strip path params, Apache/Nginx/IIS keep them
- McDonald's Hong Kong bypass demo: `..;x/manager/html` bypasses reverse proxy path check

#### Grails
- `QUOTED_FILE_SEPARATOR` = `\Q/\E` (result of `Pattern.quote("/")`)
- `..\Q/\E` becomes `../` after `replace()` → new traversal vector

#### Polyglot URL File Path
- `new URL("file:///etc/passwd?/../../Windows/win.ini")` — Linux sees path with `?`, Windows sees UNC

---

## 2019 — DEVCORE Conference: Chunghwa Telecom Modem RCE

**Slides**: `2019-devcore-conference-orange-tsai.pdf`

### Key Technique
- Remote Code Execution on HiNet GPON Modem
- Web-based exploitation of ISP-provided CPE equipment
- Command injection via diag endpoint with blacklist bypass using `?` tail

### Blacklist Bypass Technique
```c
char *BLACKLISTS = "|<>(){}`;";
```
Bypass: `nonexistent? && cat /etc/passwd` — the `?` causes sub-command to fail, then `&&` executes arbitrary command

---

## 2014 — RDP Backdoor Detection

**Slides**: `2014-hitcon-rdp-backdoor.pdf`

### Technique
- RDP Protocol analysis for backdoor detection
- Sticky Keys (sethc.exe) replacement backdoor detection
- Image File Execution Options (IFEO) backdoor detection
- RDP version fingerprinting via protocol behavior differences
- File System Virtual Channel Extension version detection

---

## EARLY RESEARCH (2011-2015)

### 2015: Epic Tricks in Web Hacking
**Slides**: `2015-tricks-in-web-hacking.pdf`

Key techniques:
- **Perl list-to-hash coercion**: `('A','Apple','C',@list)` where @list=('Ba','Ba','Banana') creates a 4-element list
- **Windows filename bypasses**: `shell.php ` (trailing space), `shell.<`, `shell"php` — all become `shell.php`
- **Windows NTFS ADS**: `download.php::$data` bypass
- **MySQL UDF privilege escalation**: `INTO OUTFILE 'plugins::$index_allocation'` creates directory via NTFS
- **Chinese character encoding for WAF bypass**: `%u4E0A` → newline equivalent bypassing regex
- **PHP `preg_replace` `/e` modifier RCE**: `preg_replace('@(\w+)'.$depr.'([^'.$depr.'\/]+)@e', ...)` → code execution

### 2013: Django Security
**Slides**: `2013-pycon-hacker-see-django.pdf`
- Django SECRET_KEY leakage → Pickle deserialization RCE
- `django.core.signing` uses Pickle for signed cookies
- CVE-2013-0305 reported

### 2013: SQL Injection Tricks
**Slides**: `2013-chroot-meetup-sql-injection-tricks.pdf`
- MySQL Error-based injection: `NAME_CONST()` duplicate column technique
- `floor(rand(0)*2)` group by duplicate entry error
- Deep Blind Injection: hex-based timing (one char in 2 requests)
- MySQL Trigger-based persistence

### 2012: PHP Security
**Slides**: `2012-phpconf-security-in-php.pdf`
- Windows filename truncation bypasses: `config.php.`, `config.php///.`, `c>>>>>.<///`
- PHP double-quote evaluation: `${@phpinfo()}` in config files
- GBK/GB2312 multi-byte encoding SQL injection: `%cc'` → valid 2-byte char that consumes the backslash from `addslashes`

---

## BLOG POSTS — FULL TECHNIQUE EXTRACTION

### WorstFit (2025-01)
**URL**: https://blog.orange.tw/posts/2025-01-worstfit-unveiling-hidden-transformers-in-windows-ansi/

Full techniques extracted and detailed above under "2024 - WORSTFIT".

Additional details from blog:
- Best-Fit mapping tool: https://worst.fit/mapping/
- Fictional story about balance manipulation via `∞` → `8` Best-Fit
- Companion site: https://worst.fit/
- Open-source coordination challenge: fixes span compilers, C/C++ runtime, and individual applications

### Confusion Attacks (2024-08)
**URL**: https://blog.orange.tw/posts/2024-08-confusion-attacks-en/

Full techniques extracted and detailed above under "2024 - CONFUSION ATTACKS".

Additional blog details:
- Apache HTTP Server patched in version 2.4.60
- Akamai released immediate WAF mitigations
- For Filename Confusion, key code at `modules/mappers/mod_rewrite.c#L4141`
- For DocumentRoot Confusion, key code at `modules/mappers/mod_rewrite.c#L4939`
- 3 Confusion Attack types, 9 CVEs, 20 exploitation techniques, 30+ case studies

### A Journey Combining Web and Binary (2021-02)
**URL**: https://blog.orange.tw/posts/2021-02-a-journey-combining-web-and-binary-exploitation/

Full techniques extracted and detailed above under "2021 - Web + Binary Exploitation Chain".

Additional blog details:
- Target: PHPWind (Chinese forum software)
- Co-author: Meh Chang
- PHP version: 5.3.27 (DLL hijacking + Type Juggling chain)
- CVE-2015-0273 for UAF, different exploitation from PornHub case

---

## AWARDS & RECOGNITION

- **2017**: 1st place, Top 10 Web Hacking Techniques — "A New Era of SSRF"
- **2018**: 1st place, Top 10 Web Hacking Techniques — "Breaking Parser Logic"
- **2019**: Pwnie Awards "Best Server-Side Bug" — SSL VPN RCE
- **2019**: 4th place, Top 10 Web Hacking Techniques — "Abusing Meta Programming"
- **2020**: 7th place, Top 10 Web Hacking Techniques — "Unauthenticated RCE on MobileIron MDM"
- **2021**: Pwnie Awards "Best Server-Side Bug" — MS Exchange ProxyLogon
- **2021**: Champion & Master of Pwn, Pwn2Own Austin
- **2021**: 3rd place, Top 10 Web Hacking Techniques — "A New Attack Surface on MS Exchange"
- **2022**: Champion & Master of Pwn, Pwn2Own Toronto

---

## RESEARCH METHODOLOGY (from slides)

Orange Tsai's approach to finding vulnerabilities:
1. **Hunt forgotten knowledge** — rediscover old, overlooked attack vectors
2. **Collect diversity** — test same concept across many implementations
3. **No idea is too stupid** — iterate and refine
4. **Move beyond known techniques** — create new attack classes, not just find bugs
5. **变强公式 (Formula for improving)**: Find motivation → Deliberately challenge N+1 → Solve: gain fun & achievement → Fail: reflect, analyze difference between "solvable" and "unsolvable"

---

## REPOSITORY STRUCTURE

All presentation slides live at: https://github.com/orangetw/My-Presentation-Slides

```
data/
├── 2024-WorstFit-Unveiling-Hidden-Transformers-in-Windows-ANSI.pdf
├── 2024-Confusion-Attacks-Exploiting-Hidden-Semantic-Ambiguity-in-Apache-HTTP-Server!.pdf
├── 2023-A-3-Years-Tale-of-Hacking-a-Pwn2Own-Target.pdf
├── 2023-From-Zero-to-Hero-A-Journey-to-the-Championship-of-Pwn2Own.pdf
├── 2023-WEBCONF-from-2013-to-2023-the-Evolution-of-Web-Security.pdf
├── 2022-Lets-Dance-in-the-Cache-Destabilizing-Hash-Table-on-Microsoft-IIS.pdf
├── 2021-ProxyLogon-is-Just-the-Tip-of-the-Iceberg.pdf
├── 2021-The-Proxy-Era-Of-Microsoft-Exchange-Server.pdf
├── 2021-A-Journey-Combining-Web-and-Binary-Exploitation-in-Real-World.pdf
├── 2020-How-I-Hacked-Facebook-Again.pdf
├── 2019-blackhat-Infiltrating-Corporate-Intranet-Like-NSA.pdf
├── 2019-Hacking-Jenkins-Pass-the-Salt.pdf
├── 2019-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf
├── 2018-Breaking-Parser-Logic-Take-Your-Path-Normalization-Off-And-Pop-0days-Out.pdf
├── 2018-tdoh-conf-javascript-ver.pdf
├── 2018-xz-whitehat-summit.pdf
└── (earlier talks: 2011-2016)
```

---

*Generated: 2026-06-06 | Sources: Orange Tsai's GitHub repo + 3 blog posts*
