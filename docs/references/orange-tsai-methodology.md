# Orange Tsai Methodology — Killer Queen's Study

> "I don't look for bugs. I look for broken assumptions."
> — The Orange Tsai mindset, decoded

## 0. The Orange Tsai Operating Model

Orange Tsai doesn't hunt individual bugs. He discovers **attack classes** — categories of vulnerabilities that span multiple products and vendors. This is what separates the $500 hunter from the $100K+ researcher.

### His Core Principle:
**Every protocol implementation, every parser, every API gateway makes assumptions about input. The bug is where the assumption breaks. Find the assumption, you find the attack class.**

## 1. Attack Surface Discovery Methodology

### 1.1 The "Question Everything" Approach
Instead of looking for code bugs, Orange questions fundamental design assumptions:

| Assumption | Attack Class Discovered |
|-----------|------------------------|
| "URL paths are normalized before processing" | Path confusion, ACL bypass |
| "Encoding is handled consistently across layers" | Encoding mismatch injection |
| "HTTP headers are parsed the same by frontend and backend" | Request smuggling, cache poisoning |
| "The cache key uniquely identifies a response" | Cache deception, cache poisoning |
| "ANSI/Wide char conversion is lossless" | WorstFit (Windows ANSI hidden transformers) |
| "The web server and app server agree on what a request means" | Confusion Attacks |

### 1.2 Attack Surface Mapping
For any target, Orange maps:
1. **Protocol layers**: What protocols does the target speak? At what layers?
2. **Parsers**: What parses user input? URL parser? HTTP parser? XML? JSON? Custom?
3. **Encoding pipelines**: How does data flow through encoding conversions?
4. **Trust boundaries**: Which component trusts which? Frontend → backend? Proxy → app server?
5. **Assumptions**: What does component A assume about data from component B?

## 2. The ProxyLogon Attack Class (MS Exchange)

Orange's most famous work — an entire attack surface discovered in Microsoft Exchange's frontend/backend architecture.

### The Architecture Insight:
```
Internet → Exchange Frontend (CAS) → Exchange Backend (MBX)
                ↓                            ↓
         Client Access Services         Mailbox Services
         (IIS + ECP/OWA)              (Backend HTTP endpoints)
```

**The assumption**: The frontend authenticates users before forwarding requests to the backend.
**The reality**: The backend trusts requests that appear to come from the frontend.

### ProxyLogon (CVE-2021-26855) — Server-Side Request Forgery
- The frontend's auth check could be bypassed with crafted cookies
- Once bypassed, the frontend would forward requests to the backend
- The backend trusts requests from localhost → full access to any mailbox
- **SSRF → Auth Bypass → Full Mailbox Access**

### ProxyShell (CVE-2021-34473, CVE-2021-34523, CVE-2021-31207)
- Three bugs chained:
  1. Path confusion to reach authenticated endpoints without auth
  2. Exchange PowerShell endpoint accessible via SSRF
  3. Arbitrary file write via Exchange mailbox export
- **Auth Bypass → PowerShell → File Write → RCE**

### ProxyOracle (CVE-2021-31196)
- Cookie-based oracle attack to decrypt any Exchange user's credentials
- Padding oracle in the cookie encryption scheme
- **Cookie → Padding Oracle → Plaintext Credentials**

### ProxyRelay
- NTLM relay between Exchange components
- **SSRF → NTLM Relay → Privilege Escalation**

### The Meta-Pattern:
```
1. Find the internal API that the frontend exposes
2. Figure out what the frontend does to "authenticate" requests
3. Bypass that authentication (cookie tricks, path confusion, SSRF)
4. Backend trusts the request → full compromise
```

## 3. Confusion Attacks (Apache HTTP Server)

Orange's 2024 Black Hat talk introduced an entirely new attack class.

### The Core Insight:
**Different components in the HTTP pipeline interpret the same request differently.**

```
Request → [Apache HTTPD] → [mod_proxy] → [Backend App Server]
              ↓                  ↓                  ↓
         Parses one way     Parses another     Parses yet another
```

### Semantic Ambiguity Exploited:
- **Filename confusion**: `example.txt.` vs `example.txt` — is the trailing dot part of the filename?
- **Path normalization**: `/api/../admin` — who resolves `..`?
- **Encoding confusion**: `%2e` vs `.` — at which layer does URL decoding happen?
- **Content-Type confusion**: `multipart/form-data` boundaries — parsed differently

### The Confusion Attacks Framework:
```
1. Send a request that is valid but ambiguous
2. Component A interprets it one way → passes it through
3. Component B interprets it differently → exposes restricted resource
4. The "security check" happens in A's interpretation, but B's interpretation is what executes
```

### Hidden Transformers — WorstFit (Windows ANSI)
Orange discovered that Windows' "best-fit" character mapping in ANSI code pages silently transforms characters:
- Unicode → ANSI → Unicode is NOT lossless
- Characters get mapped to "similar" characters
- This creates injection vectors: input passes validation in Unicode but transforms to malicious characters in ANSI

## 4. Cache Attack Methodologies

### 4.1 Web Cache Deception
```
Attacker requests: /admin/../public/style.css
Cache stores under: /public/style.css
But the request was ACTUALLY served from: /admin
→ Sensitive admin page cached as public CSS
```

### 4.2 IIS Hash Table Destabilization ("Let's Dance in the Cache")
- HTTP.sys uses hash tables for header processing
- Colliding header names can be crafted to degenerate hash table performance
- Beyond DoS: control what gets cached, what gets served

### 4.3 Cache Poisoning via Encoding Tricks
```
Request: /path%2F..%2Fadmin
Frontend proxy normalizes: %2F → "/" → /path/../admin → /admin (blocked)
Backend doesn't decode: serves /admin content
Cache key: /path%2F..%2Fadmin
→ Cache stores /admin content under unblocked URL
```

## 5. PHP Exploitation Expertise

### CVE-2024-4577 — PHP-CGI Argument Injection
- Windows-specific: Best-fit character mapping turns soft hyphen (0xAD) into regular hyphen
- PHP-CGI sees `-d` flag when input contains soft hyphen
- `-d allow_url_include=1 -d auto_prepend_file=php://input`
- **Character encoding → Argument injection → RCE**

### A Journey Combining Web and Binary (2021)
- PHP logic bug → type juggling → memory corruption → UAF → RCE
- Found in a production PHP application
- Chain: web app logic flaw → corrupt internal state → trigger UAF in PHP engine → RCE
- **This crosses the web/binary boundary. Few can do this. Orange can.**

### PHP-FPM RCE Analysis (CVE-2019-11043)
- `PHP_VALUE` settings injection via path info
- `fastcgi_split_path_info` regex bypass
- **nginx config + PHP-FPM = RCE**

## 6. The Orange Tsai Attack Taxonomy

### Attack Classes He's Discovered/Categorized:

| Attack Class | Mechanism | Products Affected |
|-------------|-----------|-------------------|
| **Path Confusion** | URL normalization inconsistency | Apache, IIS, Nginx, Tomcat |
| **SSRF → Auth Bypass** | Internal endpoint trust | Exchange, Jenkins, any proxy |
| **Encoding Mismatch** | Different decoders at different layers | Any multi-layer web stack |
| **Cache Deception** | Cache key vs actual request mismatch | Varnish, Nginx, CloudFront |
| **Confusion Attacks** | Semantic ambiguity in protocol parsing | Apache HTTPD |
| **Hidden Transformers** | Character encoding lossy round-trips | Windows (all versions) |
| **Argument Injection** | Parameter injection via encoding tricks | PHP-CGI, any CLI wrapper |
| **Padding Oracle in Auth** | Cookie decryption oracle | Exchange, any encrypted cookie |
| **NTLM Relay in Web Apps** | HTTP → SMB relay | Exchange, SharePoint |
| **Web + Binary Chaining** | App logic bug → memory corruption | PHP applications |

## 7. How to Think Like Orange Tsai

### Phase 1: Architecture Recon
```
1. Read the product documentation (not the code — yet)
2. Draw the component diagram: what talks to what?
3. Identify every proxy, gateway, load balancer, reverse proxy
4. For each boundary: what's the protocol? Who parses it?
```

### Phase 2: Assumption Mapping
```
For each boundary, list what component A ASSUMES about data from component B:
- "The frontend already validated the auth token"
- "The URL has already been normalized"
- "The content-type is what it says it is"
- "Character encoding is consistent"
- "The cache key matches the actual resource"
```

### Phase 3: Breaking Assumptions
```
For each assumption, ask:
- What if this assumption is WRONG?
- How can I send data that's valid in one context but malicious in another?
- Where does the normalization/transformation happen?
- Can I make component A see X while component B sees Y?
```

### Phase 4: Exploit Chain Construction
```
1. Start with the most impactful assumption break
2. What does breaking this assumption give you? (SSRF? Auth bypass? File read?)
3. Can you chain it to RCE? (Write a file, modify a config, inject a command)
4. Does the chain need binary exploitation? (If so, what's the memory corruption primitive?)
```

## 8. Killer Queen's Orange-Inspired Playbook

### When Reconning a Target:
```
1. Map every proxy/gateway/load balancer in the request path
2. Test URL parsing at every layer: /admin, /admin/, /admin%2f, /./admin, /;/admin
3. Test encoding at every layer: UTF-8 → ANSI → UTF-8 round-trip
4. Test cache behavior: what URL variations produce cache hits/misses?
5. Find internal-only endpoints: what's at /internal, /debug, /status, /api/internal?
6. Test SSRF vectors: can you make the server request itself?
7. For Windows targets: ALWAYS test with special Unicode characters that have best-fit mappings
8. For proxy targets: test for request smuggling (CL.TE, TE.CL, TE.TE, CL.0)
```

### The "Orange Question" for Every Target:
**"What does the frontend assume the backend will do, and can I violate that assumption?"**

## 9. Key Resources

- **WorstFit**: https://blog.orange.tw/posts/2025-01-worstfit-unveiling-hidden-transformers-in-windows-ansi/
- **Confusion Attacks**: https://blog.orange.tw/posts/2024-08-confusion-attacks-en/
- **CVE-2024-4577**: https://blog.orange.tw/posts/2024-06-cve-2024-4577-yet-another-php-rce/
- **ProxyLogon series**: https://blog.orange.tw/ — parts 1-4
- **Web+Binary chaining**: https://blog.orange.tw/posts/2021-02-a-journey-combining-web-and-binary-exploitation/
- **MobileIron RCE (Facebook)**: https://blog.orange.tw/posts/2020-09-how-i-hacked-facebook-again-mobileiron-mdm-rce/
- **Slides**: https://github.com/orangetw/My-Presentation-Slides

## 10. Summary: The Orange Tsai Doctrine

```
1. Attack surface is not about ports or services — it's about ASSUMPTIONS.
2. Every proxy, gateway, and parser boundary is an opportunity for confusion.
3. Encoding is never consistent — find where the mismatch happens.
4. Internal APIs trust their callers — impersonate the caller.
5. Caches don't understand application logic — poison them.
6. Web and binary are not separate — chain across the boundary.
7. One product's bug is an attack class. Generalize.
8. Read the documentation, not just the code. The assumptions are in the docs.
9. Windows character encoding is a gift that keeps on giving.
10. The best bugs are the ones that aren't bugs in any single component — they're bugs in the ASSUMPTIONS BETWEEN components.
```
