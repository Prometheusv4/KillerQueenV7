# HackerOne Bug Bounty Patterns — What Actually Works
> Killer Queen analysis: No theory here. Only what's been proven to extract bounties from real targets. Compiled from 14,617+ disclosed reports, top researcher methodologies, and battle-tested patterns.

---

## TABLE OF CONTENTS
1. Vulnerability Classes That Pay (by frequency and payout ceiling)
2. The Payout Spectrum: $500 vs $10,000+
3. Exploit Chain Architecture
4. Recon Methodology That Successful Hunters Use
5. Common Misconfigurations That Keep Appearing
6. Chaining Low-Severity to Critical
7. Tools That Actually Ship Bounties
8. The Hunter Mindset

---

## 1. VULNERABILITY CLASSES THAT PAY

### 1.1 Cross-Site Scripting (XSS) — Most Frequent, Still Paying
- **Platform stat:** #1 vulnerability type by report volume across HackerOne (down 10% YoY as defenses improve)
- **NahamSec data:** ~18% of his valid submissions are XSS. Blind XSS = 1/3 of XSS earnings.
- **What's still paying:** Stored XSS in admin panels, support ticket systems, PDF generators rendered in-browser. Reflected XSS now needs CSP bypass for good payout.
- **Real examples from disclosed reports:**
  - Stored XSS in attachment-display via SameSite bypass (Nextcloud, 32 upvotes)
  - CSP bypass via CDN-hosted scripts (check `script-src` for jsdelivr, cdnjs, etc.)
  - SVG-based XSS: filter primitives bypass remote image blocking (Nextcloud, 42 upvotes)
  - CSS injection: unquoted body background attribute, position:fixed overlays for phishing (Nextcloud, 37+29 upvotes)
  - Rails::HTML::Sanitizer entity-encoded javascript: URL bypass (20 upvotes)
- **XSS param hotspots** (from disclosed reports): `from`, `next_url`, `translate`, `name`, `color`, `returnUrl`, `callback`, `q`, `msgId`, `url`, `productUpdate`, `advanced_val`
- **NahamSec technique:** Inject a unique tag like `<test123nhamasec>` first — easy to track in DevTools, see how it gets handled, spot reflections without triggering WAF.

### 1.2 IDOR / Broken Access Control — Most Lucrative Class
- **arXiv paper data (107 classified H1 reports, 2021-2026):**
  - Action-Level Object BOLA: 41.7% — unauthorized state-changing actions (delete, modify, trigger) on another user's objects
  - Direct Object Reference BOLA: 36.9% — direct ID manipulation to access peer objects
  - Tenant Isolation BOLA: 8.3% — cross-organization/tenant boundary access
  - Vertical privilege escalation (user→admin): 11.9% — overlooked in most guidance
- **Critical payouts from IDOR:** Fund transfers (Cosmos), PII exposure (USAF/DoD), org-wide access (HackerOne), Salesforce file downloads (DoD)
- **HackerOne 2025 data:** IDOR and access control bugs increased 18-29% year-over-year
- **35.7% of IDOR reports rated High or Critical**
- **Identifier types:** Sequential integers still appear in 36.9% of cases (even in 2023-2026). GraphQL Global IDs are base64-encoded sequential integers — decode, increment, re-encode.
- **Real examples from disclosed reports:**
  - Rocket.Chat RBAC bypass via `permissionRequired` typo — any auth user reads admin logs (21 upvotes)
  - Rocket.Chat complete auth bypass to admin via SQL Injection (46 upvotes)
  - Reddit IDOR: change any user's profile links by changing `id` parameter ($5,000)
  - Bykea IDOR: Broken Access Control in API operations
  - HackerOne self-bug: Residual malicious payloads after vulnerability fixes (56 upvotes)

### 1.3 Server-Side Request Forgery (SSRF) — NahamSec's #1 Earner
- **25% of NahamSec's total career bug bounty earnings** from SSRF
- New life in 2024-2025 due to cloud-native architectures and API-heavy apps
- **Critical win condition:** Reach cloud metadata (169.254.169.254), pivot to internal services, hit admin panels
- **Key technique — run your own interactsh server:** Burp Collaborator and public interactsh domains are blocked by companies. Self-hosted OOB server = the difference between landing and missing.
- **Bypass URL validation:** encoding tricks, obfuscation, trusted-resource-list abuse (CDN URLs, CSP-allowed hosts), open redirect chains
- **Non-obvious SSRF surfaces:** social media link fields, PDF insertion endpoints, webhook configurations, file import features
- **Real RCE payouts from disclosed reports:**
  - PayPal RCE via npm misconfig (internal libraries from public registry): $30,000
  - GitLab RCE via DecompressedArchiveSizeValidator: $33,510
  - GitLab RCE via ExifTool metadata removal: $20,000
  - GitLab RCE via unsafe Kramdown options: $20,000
  - Uber RCE via Flask Jinja2 Template Injection: $10,000
  - Twitter VPN pre-auth RCE: $20,160

### 1.4 Account Takeover — Consistently $10K+
- **234 top disclosed ATO reports** on HackerOne
- **Top ATO patterns (by upvotes):**
  1. Leaked session cookie → ATO (HackerOne, 1,624 upvotes, $20,000)
  2. Password reset without user interaction (GitLab, 919 upvotes, $35,000)
  3. HTTP Request Smuggling → mass session theft (Slack, 864 upvotes)
  4. OAuth/OpenID misconfig → account linking abuse
  5. CSRF on email change / OAuth connect → ATO
  6. Web Cache Deception → sensitive data caching
  7. JWT misconfiguration (`none` algorithm, missing signature verification)

### 1.5 SQL Injection — Modern API Focus
- **Where to find it in 2025-2026:** API parameters, GraphQL queries, search filters, mobile endpoints
- **GraphQL injection is under-hunted:** Use the same UNION/Boolean tests on resolver arguments
- **WAF bypass tamper scripts for sqlmap:** `space2comment`, `between`, `randomcase`
- **Real examples:** Rocket.Chat SQL Injection → complete auth bypass (46 upvotes), Blind SQLi in zone-include.php (BugBoard, High severity)

### 1.6 Information Disclosure — High Volume, Variable Payout
- **Top disclosed info disclosure from reddelexc repo:**
  - Uber sensitive user info via `userUuid` parameter: 641 upvotes
  - IDOR API endpoint leaking sensitive user info (Razer): 172 upvotes, $375
  - Unauthenticated API access to system browser functions (DoD): 96 upvotes
  - API key leaks in JavaScript source (Stripe, JumpCloud): 146+ upvotes
- **Key pattern:** Information disclosure alone rarely pays big unless it chains to critical impact or exposes truly confidential data (e.g., HackerOne's own bug reports: $10,000 policy)

### 1.7 Business Logic / Race Conditions — High Value, Harder to Find
- HackerOne: 10% of crypto/blockchain vulns are logical bugs, 45% of findings from certain programs
- **Race condition gold mines:** redeeming single-use codes multiple times, manipulating balances via simultaneous transfers, bypassing rate limits on auth endpoints
- **Web Cache Deception growing:** Complex CDN/caching setups → trick cache into storing sensitive dynamic content as static

### 1.8 Subdomain Takeover — Low Effort, Consistent Medium Payout
- **Report #2899858 (Mozilla):** Subdomain takeover via unclaimed cloud resources
- Still works in 2026 because DNS hygiene is hard at scale
- **Key tools:** `subfinder`, `amass`, `dnsx`, `nuclei` (takeover templates)

### 1.9 Supply Chain / Dependency Confusion
- Alex Birsan's dependency confusion hit Apple, Microsoft, PayPal, Uber, Yelp
- **Focus:** Do internal package names leak? Can you upload a public package with the same name? CI/CD pipeline injection points?
- **NahamSec quote:** "If you're not looking at supply chain attacks in 2025, you're leaving serious money on the table."

### 1.10 AI/LLM Vulnerabilities — Emerging Frontier
- **HackerOne 2025 report:** Nearly 10% of researchers now specialize in AI
- **48% of security leaders** named GenAI as a top risk
- **Growing attack surface:** Prompt injection, model extraction, training data poisoning, RAG pipeline abuse

---

## 2. THE PAYOUT SPECTRUM: $500 vs $10,000+

### What $500 Bugs Look Like:
- Reflected XSS with no CSP bypass
- Open redirect (standalone, no chain)
- Low-impact information disclosure (non-sensitive data)
- Missing security headers (clickjacking, HSTS)
- Self-XSS or unexploitable stored XSS
- Rate limiting issues on non-critical endpoints
- Subdomain takeover on non-production/test domains

### What $5,000-$10,000 Bugs Look Like:
- Stored XSS in admin panels or multi-tenant apps
- Blind XSS that hits internal dashboards
- SSRF reaching cloud metadata or internal services
- IDOR that exposes PII or financial data
- SQL Injection with data extraction (not just confirmation)
- Account takeover via chained misconfigurations

### What $20,000-$35,000+ Bugs Look Like:
- Pre-auth RCE (Twitter VPN RCE: $20,160)
- RCE via dependency/package confusion (PayPal: $30,000, GitLab: $33,510)
- Account takeover at scale (GitLab password reset ATO: $35,000)
- Authentication bypass to admin/sensitive functions
- Critical info disclosure of confidential vulnerability data (HackerOne policy: $10K minimum)
- Multi-step exploit chains that turn auth user → admin → RCE
- Access to HackerOne's own bug database or triage system ($10K-20K policy)

### THE DIFFERENCE:
1. **Impact, not just existence:** Can you prove data exfiltration, not just "the bug exists"?
2. **Chain potential:** Can you show how this + another bug = critical?
3. **Reproduction quality:** Clear PoC with actual impact screenshots/logs
4. **Uniqueness:** Did you find something scanners missed? Unique methodology = higher payout
5. **Program maturity:** Mature programs pay more for novel, well-documented findings

---

## 3. EXPLOIT CHAIN ARCHITECTURE

### The Classic Chain Patterns That Ship:

**Pattern A: Info Disclosure → IDOR → Privilege Escalation → Critical**
- Leak user UUIDs/IDs from one endpoint → use at another endpoint without auth check → access admin functions
- Example: Salesforce ContentDocument IDs leaked via Aura API → used at download endpoint → file access (DoD #2623715)

**Pattern B: SSRF → Internal Service → RCE / Data Exfiltration**
- Webhook URL → SSRF to metadata service → steal IAM creds → pivot to internal services
- Open redirect + SSRF: bypass URL allowlists by bouncing through trusted hosts
- CSP/CDN allowlist abuse: if `script-src` allows CDN, host your payload there

**Pattern C: XSS → Session Theft → Account Takeover**
- Blind XSS hits admin panel → steal admin session → full platform compromise
- Stored XSS in user profile → victim's session cookie exfiltrated → ATO
- CSRF + XSS: force victim action + session hijack

**Pattern D: Cache Deception → Sensitive Data Leak → Account Takeover**
- Append `.css`/`.js`/`.png` to dynamic endpoint → cache stores private response as static → public access
- Check `X-Cache: HIT` and `Age` headers on sensitive endpoints

**Pattern E: Subdomain Takeover → Cookie Scope Abuse → Session Hijack**
- Take over abandoned subdomain → receive cookies scoped to parent domain → hijack sessions

**Pattern F: OAuth Dance Abuse → Account Linking Attack**
- Missing/invalid `state` parameter → CSRF on OAuth flow → link attacker's identity provider to victim's account
- `redirect_uri` validation bypass → steal authorization code

---

## 4. RECON METHODOLOGY THAT SUCCESSFUL HUNTERS USE

### Phase 1: Surface Mapping (Passive)
- **Subdomain enumeration:** `subfinder`, `amass` (passive), `crt.sh`, GitHub dorking
- **ASN enumeration:** `amass intel`, `Shodan`, `Censys` — find IP blocks owned by target
- **Reverse DNS:** Discover hidden subdomains
- **Cloud asset discovery:** `cloud_enum`, `awsbucketdump`, `s3scanner`

### Phase 2: Live Host Probing
- `httpx`, `httprobe` → filter by status codes, content-length, technologies
- Focus on: non-200 responses with interesting content, dev/staging/admin hosts, API gateways

### Phase 3: JavaScript Gold Mining
- **Tools:** `subjs`, `JSFinder`, `LinkFinder`, `gf` (pattern matching)
- **What to grep for in JS:**
  - API keys: `apiKey`, `api_key`, `token`, `secret`, `password`, `authorization`
  - Internal endpoints: `/api/`, `/graphql`, `/internal/`, `/admin/`, `/v2/`, `/beta/`
  - GraphQL: queries, mutations, introspection data
  - Hardcoded credentials, S3 bucket names, internal hostnames
  - `postMessage` / `addEventListener('message'` → potential origin confusion
- **NahamSec's trick:** Use `gf` patterns to extract URLs/endpoints/secrets from JS at scale

### Phase 4: URL Discovery & Parameter Mining
- **Archive crawling:** `gau` (getallurls), `waybackurls`, `ParamSpider`
- **Live crawling:** `katana`, `gospider`, `hakrawler`
- **Parameter brute-force:** `Arjun`, `ffuf` with param wordlists
- **Focus on:** Redirect parameters, file paths, IDs, callback URLs

### Phase 5: Content Discovery
- `feroxbuster`, `ffuf`, `dirsearch` (recursive)
- Wordlists: Seclists, Assetnote, custom target-specific
- **Look for:** `.git/`, `.env`, `backup.zip`, `wp-config.php.bak`, `phpinfo.php`, Swagger/OpenAPI docs, GraphQL playground, `.DS_Store`

### Phase 6: API Enumeration
- `kiterunner` for API endpoint brute-force
- Postman collections, Swagger/OpenAPI specs
- GraphQL: use **InQL** Burp extension → auto-generate schema → fuzz every queryable field

### Phase 7: The "Two-Eye" Approach
1. **First eye:** Automated tools (nuclei, zap, custom scripts) — catch low-hanging fruit
2. **Second eye:** Manual analysis — understand business logic, chain vulnerabilities, test assumptions that scanners can't

### Advanced Recon Tactics from Top Earners:
- **Monitor new features:** Check changelogs, UI changes, network requests for newly added endpoints. The $10,000 H1 comments leak was found this way.
- **Compare interfaces:** What's visible via UI vs API vs export/download? Discrepancies = bugs.
- **GitHub dorking for secrets:** `GitDorker`, search for `filename:.npmrc _auth`, `filename:.env DB_PASSWORD`
- **Google dorking:** `site:target.com ext:log`, `site:target.com inurl:admin`, `site:target.com intitle:"index of"`
- **Test export/download/backup functions:** These often bypass UI-level access controls

---

## 5. COMMON MISCONFIGURATIONS THAT KEEP APPEARING

### Access Control:
- **Missing object-level authorization on API endpoints** (THE #1 pattern)
- GraphQL resolvers without ownership checks
- Admin endpoints discoverable but only "hidden" by UI
- `permissionRequired` typos in middleware (Rocket.Chat — actual bug)
- Forgetting to apply access control to export/download/archive functions
- API keys that work even after account deactivation

### Authentication:
- Password reset tokens that never expire or are predictable
- JWT `alg: none` accepted or `HS256` confusion with public key
- OAuth `state` parameter not validated → CSRF linking attack
- Missing email verification on email change
- Session cookies without `Secure`/`HttpOnly`/`SameSite`
- Rate limiting absent on login, password reset, 2FA, and SMS endpoints

### Input Validation / Injection:
- File upload accepting `.php`, `.jsp`, `.svg` without sanitization
- SVG upload without sanitization → stored XSS via `<script>`, `<foreignObject>`, event handlers
- GraphQL allowing introspection in production → full schema leak
- XXE still possible in older XML parsers (SOAP, SAML, document conversion)
- Template injection in user-controlled templates, email subjects, report names

### Infrastructure:
- Cloud storage buckets with list/read permissions
- Subdomain DNS records pointing to unclaimed cloud resources (takeover)
- `.git` directory exposed on web root
- Debug mode enabled in production (Django DEBUG=True, Laravel debug, Spring Boot actuator)
- Internal services exposed on public IPs
- CI/CD pipeline logs leaking secrets

### CORS & CSP:
- `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`
- `Access-Control-Allow-Origin` reflecting the `Origin` header value
- `Content-Security-Policy` allowing `unsafe-inline` or `unsafe-eval`
- CSP allowing CDN domains where you can host payloads (jsdelivr, unpkg, cdnjs)

### Caching:
- Dynamic/sensitive pages returning `Cache-Control: public`
- CDN caching authenticated responses due to missing `Vary: Cookie`
- `X-Cache: HIT` on endpoints returning PII

---

## 6. CHAINING LOW-SEVERITY → CRITICAL

### Proven Chain Recipes:

**Recipe 1: Open Redirect → SSRF → Metadata → RCE**
```
Find open redirect on trusted domain
  → Use it in SSRF endpoint that only allows that domain
    → Redirect bounces to 169.254.169.254
      → Steal IAM credentials
        → Pivot to RCE on EC2
```

**Recipe 2: Info Leak → IDOR Enumeration → Mass Data Theft**
```
Find UUID/ID leak in response headers or error messages
  → Harvest IDs from public endpoints (search, share, collaboration features)
    → Use discovered IDs at API endpoints lacking ownership checks
      → Exfiltrate PII/financial data at scale
```

**Recipe 3: XSS + CSRF → Account Takeover**
```
Find self-XSS or reflected XSS
  → Chain with CSRF on sensitive action (email change, OAuth link)
    → Victim clicks link → XSS fires → CSRF executes in background
      → Complete account takeover
```

**Recipe 4: Rate Limit Bypass → Brute Force → ATO**
```
Find rate limit that resets on IP change or uses weak identifier
  → Brute force password reset tokens or 2FA codes
    → Access victim account
```

**Recipe 5: Subdomain Takeover → Cookie Scope → Session Hijack**
```
Find dangling DNS → claim cloud resource
  → Cookies scoped to *.target.com sent to your server
    → Hijack main application session
```

**Recipe 6: Cache Deception → PII Leak → Identity Theft**
```
Find dynamic endpoint that returns user data
  → Append .css to URL path
    → CDN caches response as static
      → Access other users' cached PII
```

**Recipe 7: CSRF + IDOR → Mass Account Modification**
```
CSRF on profile update endpoint (no anti-CSRF token)
  → IDOR parameter in request allows targeting other users
    → Mass-modify all user profiles via single CSRF payload
```

### Key Insight from the arXiv BOLA Study:
- **Chained Disclosure BOLA** (4.8% of confirmed cases): Identifier leaked from one endpoint, used at another. Hunters who trace identifiers across endpoints find bugs others miss.
- **Workflow-Context BOLA** (6.0%): Authorization bypass because of object lifecycle state — after deactivation, archival, or draft mode. Test object states.

---

## 7. TOOLS THAT ACTUALLY SHIP BOUNTIES

### Core Stack (every successful hunter runs these):
| Tool | Purpose |
|------|---------|
| **Burp Suite Pro** | Interception, repeater, intruder, collaborator |
| **Caido** | Modern alternative to Burp, HTTPQL for caching analysis |
| **ffuf** | Fast fuzzing (directories, parameters, vhosts) |
| **nuclei** | Template-based vulnerability scanning |
| **subfinder + amass** | Subdomain enumeration |
| **httpx** | Live host probing with tech detection |
| **katana** | Headless crawling, JS extraction |
| **gau + waybackurls** | Historical URL collection |
| **sqlmap** | SQL injection automation |

### Specialized Tools:
| Tool | Use Case |
|------|----------|
| **interactsh-client** (self-hosted) | OOB/Blind SSRF detection (DON'T use public server) |
| **InQL** (Burp extension) | GraphQL schema extraction and query fuzzing |
| **Authz** (Burp extension) | Automated IDOR testing with session tokens |
| **Arjun** | HTTP parameter discovery |
| **kiterunner** | API endpoint brute-force |
| **cloud_enum** | Cloud asset enumeration (S3, Azure, GCP) |
| **GitDorker** | Automated GitHub dorking |
| **LinkFinder** | Endpoint discovery from JavaScript |
| **gf** | Pattern matching (secrets, endpoints, parameters) |
| **subjs + JSFinder** | JavaScript file extraction |

### Local LLM Integration (2026 pattern):
```bash
ollama pull mistral  # or deepseek, llama3
```
- Pipe Burp responses to local LLM for rapid triage
- Pattern recognition without sending target data externally
- Payload generation for WAF bypass, filter evasion
- Analyzing large JS files for hidden endpoints/secrets

### Automation Stack for $10K+ Workflows:
- **git-exposure scanning:** `git-dumper`, `trufflehog` → finding leaked repos
- **nuclei + custom templates:** Customize for target tech stack
- **Burp + Turbo Intruder:** Race condition testing, high-throughput fuzzing
- **Custom Python scripts:** Automate consistency checks between UI/API/export views

---

## 8. THE HUNTER MINDSET

### What Separates Top Earners ($400K-$600K/yr) from the Rest:

1. **Depth over breadth:** Master one target. Understand its architecture, tech stack, business logic. The average hunter gives up after 2-3 hours. Top hunters spend days on one app.

2. **System understanding > scanning:** 25% of NahamSec's earnings came from SSRF because he deeply understands URL parsing, backend request handling, and validation bypass techniques — not because he ran a tool.

3. **New features = fresh attack surface:** The $10,000 HackerOne comments leak was found by noticing a just-released "Export as .zip" feature and testing visibility assumptions. Monitor changelogs, new endpoints, UI changes.

4. **Challenge every assumption:**
   - "Limited disclosure" — does it apply to exports/downloads?
   - "Admin only" — is it enforced or just hidden in UI?
   - "Internal library" — is it on the public registry?
   - "Secure flag" — does the cookie actually have it everywhere?

5. **Impact > cleverness:** Programs pay for business impact. A simple IDOR that exposes all user PII pays more than a technically impressive XSS on a static page. Lead with impact.

6. **Persistence beats talent:** Bug hunting is not a sprint. The most successful hunters submit consistently over years. HackerOne's top earners cleared $400K-600K in 2025.

7. **Self-host your infrastructure:** Public Burp Collaborator/interactsh servers are blocked by most mature programs. Self-host your OOB listener. This alone separates hunters who find blind SSRF from those who don't.

8. **Read disclosed reports:** Learn from what's already been found. The reddelexc/hackerone-reports repo has categorized hundreds of top reports. The BugBoard has 10,000+ searchable reports. The ddosi.org dashboard has 14,617 entries.

9. **Two-eye principle:** Automated tools catch the low fruit. Manual analysis finds the critical chains. Don't rely exclusively on either.

10. **Report quality matters:** Clear executive summary + step-by-step reproduction + actual impact evidence + remediation suggestion = faster triage, higher payout, better reputation.

---

## SOURCES SYNTHESIZED

- **ddosi.org/hackerone-report.html** — Dashboard of 14,617 H1 reports with program, title, bounty, vuln type
- **bugboard.rsecloud.com/hackerone_reports** — 10,000+ searchable disclosed reports with severity and dates
- **hackerone.com/reports/3475626** — LinkedIn: Session Cookie Leakage via Static WebViewerFragment (could not extract directly; identified via search)
- **hackerone.com/reports/2899858** — Mozilla: Subdomain takeover via unclaimed cloud resource (could not extract directly; identified via search)
- **hackerone.com/lp/top-ten-vulnerabilities** — H1 Top 10 Vuln Types, 78,042 valid vulns, XSS #1, 12% YoY increase
- **nahamsec.com** — NahamSec's high-value vuln methodology (SSRF = 25% earnings, XSS = 18% submissions)
- **redfoxsec.com** — Common bug bounty vulns 2026 with tools and PoC commands
- **arXiv 2605.25865v1** — BOLA empirical taxonomy: 107 classified H1 reports, 6-family taxonomy, 78.5% confirmed BOLA
- **GitHub: reddelexc/hackerone-reports** — Tops by bug type: RCE (331 reports), XSS, Account Takeover (234), Info Disclosure, SSRF, CSRF, API, Mobile, GraphQL
- **GitHub: amrelsagaei/Bug-Bounty-Hunting-Methodology-2025** — 7-phase recon methodology
- **InfoSec Writeups: $10,000 Bounty** — H1 report #182358, comments leak via Export as .zip, found by monitoring new features
- **Infosec Writeups: $5,000 IDOR** — Reddit profile link manipulation via IDOR on `id` parameter
- **HackerOne 2025 HPSR** — $81M paid in bounties (13% YoY), AI vulns growing, 48% leaders see GenAI as top risk

---

*Generated 2026-06-06. This is a living document — patterns evolve. Keep hunting.*
