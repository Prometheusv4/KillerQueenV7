---
name: adaptive-engagement
description: Target-agnostic adaptive engagement engine — dynamic priority ordering, attack surface scoring, vector selection decision tree, engagement state machine, fingerprint-based technique selection, universal recon playbook. Transforms Killer Queen from linear scanner into context-aware adaptive attacker.
category: methodology
triggers:
  - adaptive
  - prioritize
  - attack surface scoring
  - vector selection
  - engagement state
  - target fingerprint
  - recon playbook
  - cold start
  - dynamic technique
  - score target
  - attack surface map
  - what should I attack first
  - priority order
---

# Adaptive Engagement Framework — Dynamic Attack Surface Prioritization

Load this skill when: starting a new target with no prior context (cold start), when the operator asks what to attack first, when you need to dynamically reprioritize mid-engagement, or when building the initial attack surface map.

This is the engine that turns Killer Queen from a linear checklist-follower into an adaptive attacker that dynamically adjusts strategy based on what the target reveals about itself.

---

## CORE PRINCIPLE: TARGET-AGNOSTIC BY DESIGN

Every algorithm and decision tree in this skill works on ANY target without requiring target-specific paths. No hardcoded URLs, no platform-specific assumptions. Everything derives from what the target TELLS us through recon output. This is universal offensive reasoning — the same logic applies whether the target is a fintech SaaS, a government portal, a crypto exchange, or an IoT device.

---

## TARGET-AGNOSTIC PRIORITY ORDERING ALGORITHM

### The Priority Score Formula

For every identified attack surface, compute:

```
PRIORITY_SCORE = (EXPLOITABILITY × 0.4) + (IMPACT × 0.35) + (NOVELTY × 0.15) + (SPEED × 0.10)
```

### Exploitability Scoring (0.0–10.0)

| Factor | Weight | Scoring |
|--------|--------|---------|
| Authentication required? | 2.0 | None=10, Low-priv=6, User=3, Admin=1 |
| Public exploit available? | 1.5 | Metasploit module=10, Public PoC=8, Technique known=5, Custom required=2 |
| WAF/IDS detected? | 1.5 | None=10, Basic=6, Advanced=3, Enterprise=1 |
| Rate limiting? | 1.0 | None=10, Lenient=7, Moderate=4, Aggressive=1 |
| Input complexity? | 1.0 | Simple GET=10, POST JSON=8, Multipart upload=6, Complex chain=3 |
| Reliability? | 1.0 | Deterministic=10, Race-dependent=5, Timing-dependent=3 |
| Prerequisites? | 1.0 | None=10, 1 prereq=7, 2-3=4, 4+=2 |
| Known bypass path? | 1.0 | Documented bypass=10, General approach=5, Unknown=2 |

### Impact Scoring (0.0–10.0)

| Factor | Weight | Scoring |
|--------|--------|---------|
| Data access level | 2.5 | PII/financial=10, User data=7, System metadata=4, Public data=1 |
| Privilege escalation path? | 2.0 | DA/SYSTEM=10, Elevated role=7, Lateral=5, Same level=2 |
| Blast radius | 2.0 | Multi-tenant/all users=10, All users of app=7, Current user=4, Self-only=1 |
| Chain potential | 1.5 | Direct RCE chain=10, Auth bypass chain=8, Data leak chain=6, Info disc chain=3 |
| Persistence possible? | 1.0 | Persistent code exec=10, Persistent config=7, Session-only=4, None=1 |
| Detection difficulty | 1.0 | Undetectable=10, Forensic-only=7, Logged but noisy=4, Actively alerted=1 |

### Novelty Scoring (0.0–10.0)

| Factor | Weight | Scoring |
|--------|--------|---------|
| CVEs in last 90 days? | 3.0 | 0-days available=10, Recent (<30d)=8, Known (<1yr)=5, Ancient=2 |
| Technique uniqueness | 3.0 | Never seen on this stack=10, Rare=7, Common=4, Very common=1 |
| Bypass novelty | 2.0 | New bypass discovered=10, Recent bypass=7, Known bypass=4, No bypass needed=2 |
| Chaining novelty | 2.0 | Novel chain=10, Known chain variant=6, Standard chain=3, Single-hop=1 |

### Speed Scoring (0.0–10.0)

| Factor | Weight | Scoring |
|--------|--------|---------|
| Time to first result | 4.0 | <1 min=10, <5 min=7, <15 min=4, <1 hr=2, >1 hr=1 |
| Parallelizable? | 3.0 | Fully parallel=10, Partial=6, Sequential=3 |
| Tool setup required? | 3.0 | Already installed=10, apt install=7, Build from source=4, Custom dev=1 |

### Priority Bands

```
SCORE 8.0–10.0 : CRITICAL — Attack NOW, drop other vectors
SCORE 6.0–7.9  : HIGH — Attack in current phase, assign sub-agent
SCORE 4.0–5.9  : MEDIUM — Queue for next phase, monitor for chaining
SCORE 2.0–3.9  : LOW — Document, attack if HIGH+ exhausted
SCORE 0.0–1.9  : INFORMATION — Note for report, don't actively attack
```

---

## ATTACK SURFACE SCORING METHODOLOGY

### Phase 1: Surface Inventory

Before scoring, inventory ALL attack surfaces. Use the universal discovery playbook:

```
RECON OUTPUT → SURFACE EXTRACTION → CATEGORIZATION → SCORING → PRIORITIZATION

For each surface discovered, record:
  - TYPE: [Web App / API / Auth Flow / File Upload / Email System / DNS / Cloud / IoT / Mobile / etc.]
  - ENDPOINT/IDENTIFIER: [URL, hostname, IP, port, protocol]
  - TECH STACK: [Framework, language, server, CMS version]
  - AUTH REQUIREMENT: [None / User / Privileged / Admin / Unknown]
  - OBSERVED BEHAVIOR: [What we see from outside — response codes, headers, timing]
  - KNOWN VULNS: [CVEs matching identified versions]
  - PUBLIC INFO: [What OSINT/google/github reveals about this surface]
```

### Phase 2: Surface Scoring

Apply the Priority Score Formula to each surface. Score independently — don't compare yet.

### Phase 3: Vector Selection

See VECTOR SELECTION DECISION TREE below.

### Phase 4: Dynamic Re-scoring

Re-score after:
- Any surface is successfully exploited (changes impact of related surfaces)
- New technology is identified (opens new exploitability paths)
- A defense mechanism is detected (lowers exploitability)
- 30 minutes without progress (stale scores may need adjustment)

---

## VECTOR SELECTION DECISION TREE

```
START: Target identified
│
├─ Q1: Do we have ANY recon data?
│  ├─ NO → COLD START PATH
│  │   ├─ Passive recon (search/web_extract → WHOIS, DNS, Shodan, crt.sh)
│  │   ├─ Active recon (nmap top 1000, httpx, subfinder)
│  │   └─ Wait for recon to complete → re-enter at Q1 with data
│  │
│  └─ YES → Continue
│
├─ Q2: Are there ANY unauthenticated endpoints?
│  ├─ NO → Auth-required path
│  │   ├─ Register account (if possible) → assess low-priv access
│  │   ├─ Auth bypass attempts (legacy protocol matrix, method tampering)
│  │   ├─ Pre-auth: password spraying, breach creds, default creds
│  │   └─ OSINT: employee names → username enumeration → password patterns
│  │
│  └─ YES → Sort unauthenticated surfaces by PRIORITY_SCORE (descending)
│
├─ Q3: Is there a file upload anywhere?
│  └─ YES → Bump priority: file upload + [any rendering/processing] = potential RCE
│      (This is the single highest-value surface after auth bypass)
│
├─ Q4: Are there API endpoints with IDs in URLs?
│  └─ YES → IDOR test immediately (low effort, high impact if present)
│      Test: increment/decrement, UUID→numeric, /v2/→/v1/, siblings
│
├─ Q5: Is there an authentication flow (login/OAuth/SAML/OIDC)?
│  └─ YES → Auth assessment: rate limiting, OAuth params, PKCE, redirect_uri, JWT
│      (Auth bugs often chain to full account takeover)
│
├─ Q6: Is there JavaScript-heavy SPA behavior?
│  └─ YES → JS bundle analysis: grep for secrets, API endpoints, postMessage listeners
│      (Modern SPAs leak their entire API surface in bundles)
│
├─ Q7: Is there a GraphQL endpoint?
│  └─ YES → Introspection query → full schema → auth on mutations, node() IDOR
│      (GraphQL introspection is a free attack surface map)
│
├─ Q8: Are there CORS headers on API responses?
│  └─ YES → Check Access-Control-Allow-Origin reflection, credentials: true
│      (CORS misconfig + XSS = full session theft)
│
├─ Q9: Are there any file/path parameters in URLs?
│  └─ YES → Path traversal test (../, ..%2f, ..%252f, absolute paths)
│
└─ FALLBACK: Attack top-3 surfaces by score, maintain 3+ active vectors
   Cycle through: WEB → API → AUTH → INFRA → OSINT → SUPPLY CHAIN → repeat
```

---

## ENGAGEMENT STATE MACHINE

Killer Queen moves through these states during an engagement. State transitions are driven by recon output — NEVER by hardcoded checklists.

```
                    ┌──────────────┐
                    │  COLD START   │
                    │  (no data)    │
                    └──────┬───────┘
                           │ Recon complete
                           ▼
                    ┌──────────────┐
            ┌──────│    RECON      │◄──────────────────────┐
            │      │  (mapping)    │                       │
            │      └──────┬───────┘                       │
            │             │ Surfaces scored + prioritized  │
            │             ▼                                │
            │      ┌──────────────┐                       │
            │      │   ACTIVE     │                       │
            │      │ (exploiting) │──── Pivot discovered ──┘
            │      └──────┬───────┘
            │             │
            │     ┌───────┼───────┐
            │     ▼       ▼       ▼
            │  ┌─────┐┌─────┐┌─────────┐
            │  │SHELL││DATA ││PERSIST  │
            │  │     ││EXFIL││         │
            │  └──┬──┘└──┬──┘└────┬────┘
            │     │       │        │
            │     └───────┼────────┘
            │             ▼
            │      ┌──────────────┐
            └──────│  REPORTING   │
                   │ (delivering) │
                   └──────────────┘
```

### State Definitions

| State | Trigger | Primary Activities | Exit Condition |
|-------|---------|-------------------|----------------|
| COLD START | New target, no data | Passive + active recon, version detection, surface inventory | At least 5 attack surfaces identified and categorized |
| RECON | Surfaces identified, not scored | Surface scoring, vector selection, initial probe requests | At least 3 vectors in ACTIVE state |
| ACTIVE | Vectors selected, attacking | Exploitation attempts, technique cycling, bypass attempts | Shell obtained OR data exfiltrated OR all vectors exhausted |
| PIVOTING | New target discovered inside perimeter | Internal recon, cred collection, lateral movement mapping | New surfaces scored and prioritized → return to RECON |
| REPORTING | Engagement winding down or operator requests | Findings synthesis, chain documentation, report generation | Report delivered to operator |

### State Transition Rules
- COLD START → RECON: AUTOMATIC when surface inventory > 0
- RECON → ACTIVE: AUTOMATIC when 3+ vectors selected
- ACTIVE → PIVOTING: When shell obtained or new internal target discovered
- PIVOTING → RECON: After pivot surfaces scored
- ANY → REPORTING: On operator command or engagement scope exhausted
- ANY → COLD START: NEVER (cold start only on new target)

---

## DYNAMIC TECHNIQUE SELECTION BASED ON TARGET FINGERPRINT

### Fingerprint Categories

Extract these fingerprints from recon output and use them to bias technique selection:

```
TECH STACK FINGERPRINT:
  - Web server: [Apache/Nginx/IIS/Express/Caddy/Traefik/...]
  - Language: [PHP/Python/Node/Java/.NET/Ruby/Go/...]
  - Framework: [Laravel/Django/Express/Spring/Rails/Gin/...]
  - CMS: [WordPress/Drupal/Joomla/Shopify/Magento/...]
  - Database (if detectable): [MySQL/PostgreSQL/MongoDB/Redis/...]
  - Cloud provider: [AWS/GCP/Azure/DigitalOcean/...]
  - CDN/WAF: [Cloudflare/Akamai/AWS CloudFront/Fastly/Imperva/...]

ARCHITECTURE FINGERPRINT:
  - SPA: [React/Vue/Angular/Svelte/...]
  - API style: [REST/GraphQL/gRPC/SOAP/...]
  - Authentication: [OAuth2/SAML/OIDC/LDAP/JWT/Basic/...]
  - Real-time: [WebSockets/SSE/Long-polling/...]
  - File handling: [Direct upload/Presigned URL/Chunked/...]

SECURITY POSTURE FINGERPRINT:
  - CSP: [Present/Absent, strict/lax, unsafe-inline/eval allowed?]
  - Security headers: [HSTS, X-Frame-Options, X-Content-Type-Options, etc.]
  - CORS: [Wildcard/Reflected/Restricted/None]
  - Rate limiting: [Aggressive/Moderate/Lenient/None detected]
  - Error handling: [Detailed/Generic/Custom/Crash-only]
```

### Technique Weighting by Fingerprint

When the fingerprint matches a known pattern, adjust technique priority:

| Fingerprint Match | Boost These Techniques | Suppress These |
|-------------------|----------------------|----------------|
| PHP detected | File upload→RCE, LFI/RFI, PHAR deserialization (if <8.4), SQLi, XXE | SSTI (rare in PHP), NoSQL injection |
| Node.js detected | SSTI (EJS/Pug), prototype pollution, JWT attacks, async race conditions, ReDoS | SQLi (less common), XXE |
| Python detected | SSTI (Jinja2/Mako), deserialization (pickle), SSRF, SQLi (Django ORM) | XXE (rare) |
| Java detected | Deserialization, XXE, SSTI (Thymeleaf/Velocity), log injection (Log4Shell), Spring Actuator | PHP-specific attacks |
| .NET detected | Deserialization (ViewState/ysoserial.net), XXE, SSTI (Razor), path traversal | PHP-specific attacks |
| WordPress detected | XMLRPC, REST API, plugin enumeration, theme file editor, wp-admin | Framework-specific (not applicable) |
| GraphQL detected | Introspection, batching attacks, depth/alias DOS, node() IDOR, auth on mutations | Traditional REST attacks |
| Cloudflare detected | Origin IP discovery, CF-Connecting-IP header abuse, cache poisoning, workers bypass | Direct WAF bypass (unlikely) |
| No CSP | XSS (all types), CSPT, dangling markup, script gadget chaining | CSP bypass techniques (unnecessary) |
| Strict CSP | DOM clobbering, prototype pollution→script gadget, CSP bypass specific to policy | Traditional reflected/stored XSS |
| AWS detected | IMDS SSRF, S3 bucket enumeration, Lambda event injection, Cognito, IAM privesc | GCP/Azure-specific |
| OAuth detected | PKCE missing, redirect_uri validation, CSRF on /authorize, token replay, scope upgrade | Traditional login form attacks |

### Fingerprint-to-CVE Mapping

When version fingerprints are detected, dynamically map to CVEs:

```
1. Extract versions: whatweb, wappalyzer-like detection, response headers, error pages
2. For each identified component+version:
   - searchsploit <component> <version>
   - nuclei -t cves/ -match-condition 'and' (version + component)
   - github.com search: "<component> <version> CVE"
3. Filter: PR:N only (unless we have credentials), verified PoC available
4. Sort by CVSS score (descending) × exploit availability (public PoC > theoretical)
5. Feed top results into PRIORITY_SCORE formula
```

---

## UNIVERSAL RECON PLAYBOOK (Target-Agnostic)

This playbook works on ANY target. No hardcoded paths, no platform assumptions.

### COLD START — Passive Phase (no packets to target)

```
STEP 1: WHOIS + DNS BASELINE
  - whois <TARGET_DOMAIN> → registrar, dates, nameservers, contact (redacted for GDPR but structure matters)
  - dig +short NS <TARGET_DOMAIN> → authoritative nameservers
  - dig +short MX <TARGET_DOMAIN> → mail servers (often different IPs)
  - dig +short TXT <TARGET_DOMAIN> → SPF/DKIM/DMARC (email security posture)
  - dig +short CAA <TARGET_DOMAIN> → certificate authority restrictions

STEP 2: CERTIFICATE TRANSPARENCY
  - crt.sh: ?q=%25.<TARGET_DOMAIN>&output=json → all subdomains from CT logs
  - Parse: unique subdomains, wildcard certs, expired certs (still resolving?)

STEP 3: SEARCH ENGINES (OSINT)
  - Google dorks: site:<TARGET_DOMAIN> ext:php|aspx|jsp|env|config|sql|log|bak
  - GitHub: org:<COMPANY> or "<TARGET_DOMAIN>" → leaked configs, API keys, internal tooling
  - Shodan: org:"<COMPANY>" or hostname:<TARGET_DOMAIN> → exposed services
  - Wayback Machine: web.archive.org CDX API → historical URLs, forgotten endpoints

STEP 4: SECURITY POSTURE
  - securityheaders.com-style check: manually HEAD / → HSTS, CSP, X-Frame-Options, etc.
  - Email security: SPF (~all vs -all), DMARC (p=none vs p=reject), DKIM, MTA-STS, BIMI
  - DNS records: CNAME → cloud services, TXT → verification strings (reveal services used)
```

### ACTIVE PHASE — Direct Target Probing

```
STEP 5: HOST DISCOVERY
  - nmap -sn <CIDR or IP range> → live hosts (use -PS/-PA if ICMP blocked)
  - If target is a domain: resolve to IPs, check if multiple IPs (CDN? check with different resolvers)

STEP 6: PORT SCANNING
  - Top 1000 TCP: nmap -sV -sC --top-ports 1000 --min-rate=3000 <TARGET>
  - Common UDP: nmap -sU --top-ports 100 <TARGET>
  - If web ports open → skip to HTTP probe, let full port scan run in background

STEP 7: HTTP PROBE (on every open web port, including non-standard)
  - httpx -l live_hosts.txt -title -status-code -tech-detect -web-server -follow-redirects
  - For each responding HTTP service:
    - GET / → response headers, body fingerprint, redirects
    - GET /robots.txt → Disallow paths = high-value probe targets
    - GET /sitemap.xml → URL inventory
    - GET /favicon.ico → hash fingerprint (shodan/favicon hash lookup)
    - Check: /.well-known/ (security.txt, openid-configuration, assetlinks.json)

STEP 8: TECHNOLOGY FINGERPRINTING
  - whatweb -a 3 <URL> → deep fingerprint
  - Wappalyzer-style: header patterns, HTML comments, JS globals, file paths
  - Build fingerprint object with all detected components + versions

STEP 9: CONTENT DISCOVERY (adaptive wordlists)
  - Based on tech fingerprint, select wordlists:
    - PHP → php-common.txt, php-files.txt
    - ASP.NET → aspx-common.txt, ashx-endpoints.txt
    - Java → jsp-paths.txt, spring-boot-endpoints.txt
    - API → api-endpoints.txt, graphql-paths.txt
    - General → raft-large-directories.txt
  - ffuf with auto-calibration (filter by baseline response size/code)
  - If WAF detected → reduce rate, randomize User-Agent, add delays

STEP 10: URL HARVESTING
  - katana -u <URL> -jc -kf all → crawl + JS parsing
  - gau <TARGET_DOMAIN> → Wayback + AlienVault + CommonCrawl URLs
  - waybackurls <TARGET_DOMAIN> → all historical URLs with parameters
  - Extract: all URLs with parameters → param miner input
  - Extract: all JS files → bundle analysis input

STEP 11: PARAMETER CLASSIFICATION
  - gf patterns: idor, redirect, ssrf, sqli, xss, lfi, rce, ssti, debug, upload, auth
  - For each parameter, classify by vulnerability class potential
  - Feed classified params to appropriate testing modules

STEP 12: SURFACE SYNTHESIS
  - Merge all recon output into ATTACK_SURFACE_MAP
  - Score each surface per PRIORITY_SCORE formula
  - Select top 3+ vectors
  - Begin ACTIVE state
```

### Recon Acceleration Rules
- If any surface scores CRITICAL (8.0+) → pause recon, attack IMMEDIATELY
- If all surfaces score MEDIUM or below → complete full recon before attacking (cold start is worth it)
- If rate-limited heavily → complete passive recon, queue active for slow-and-steady mode
- If WAF/IDS detected early → slow recon, randomize, use passive techniques preferentially

---

## VERSION HISTORY

v1.0 — Initial adaptive engagement framework: priority ordering algorithm, attack surface scoring, vector selection decision tree, engagement state machine, fingerprint-based technique selection, universal recon playbook.
