# Consolidated HackerOne SSRF Knowledge
# Extracted from Top 309 HackerOne SSRF Reports
# Generated: 2026-06-06

================================================================================
## 1. SSRF TYPES
================================================================================

### A. Basic (Full-Read / Full-Response) SSRF
Attacker can read the full HTTP response body from the target server.

- #5  — SSRF at app.hellosign.com → AWS private keys disclosure (Dropbox, $4913)
- #10 — Full Response SSRF via Google Drive (Dropbox, $17576)
- #13 — Full read SSRF in www.evernote.com, leak AWS metadata + LFI (Evernote)
- #17 — Full Read SSRF on GitLab's Internal Grafana (GitLab)
- #26 — SSRF chained to hit internal host → another SSRF → read internal images (PlayStation)
- #35 — Full read SSRF via Lark Docs "import as docs" feature (Lark Technologies, $5000)
- #84 — Unauthenticated full-read SSRF via Twilio integration (Rocket.Chat)
- #107 — FULL SSRF (Acronis)
- #128 — Full read SSRF in flyte-poc-us-east4.uberinternal.com (Uber, $2000)
- #218 — Full read SSRF at DoD (U.S. Dept Of Defense)

### B. Blind SSRF
No response body returned; attacker infers success via side channels (timing, DNS, error diffs).

- #9  — Blind SSRF to internal services in matrix preview_link API (Reddit, $6000)
- #16 — Unauthenticated blind SSRF in OAuth Jira authorization controller (GitLab, $4000)
- #27 — Blind SSRF on errors.hackerone.net due to Sentry misconfiguration (HackerOne, $3500)
- #36 — Blind SSRF on my.exnessaffiliates.com, internal network enumeration (EXNESS)
- #42 — Blind SSRF in horizon-heat (Mail.ru, $2500)
- #43 — Blind SSRF in Stripo App Export via Missing Endpoints (Stripo Inc)
- #46 — Blind SSRF in emblem editor (2) (Rockstar Games, $1500)
- #53 — Blind SSRF on debug.nordvpn.com, Sentry misconfiguration (Nord Security)
- #58 — Blind SSRF via /api/v2/chats/image-check, internal port scan (8x8)
- #61 — Blind SSRF on labs.data.gov/dashboard/Campaign/json_status (GSA Bounty, $300)
- #64 — Blind SSRF External Interaction (MTN Group)
- #71 — Blind SSRF in magnum upgrade_params (Mail.ru, $2500)
- #73 — Blind SSRF at chaturbate.com/notifications/update_push (Chaturbate)
- #77 — Blind SSRF on platform.dash.cloudflare.com, Sentry misconfig (Cloudflare)
- #78 — Blind SSRF allows scanning internal ports (Elastic)
- #82 — Internal Blind SSRF allows scanning internal ports (Mozilla)
- #88 — BLIND SSRF ON jsgames.mail.ru via avaOp parameter (Mail.ru)
- #90 — Blind SSRF vulnerability on cz.acronis.com (Acronis)
- #98 — Blind SSRF in Appstore Release Upload Form (Nextcloud)
- #108 — Blind SSRF in Mail App (Nextcloud)
- #111 — Blind SSRF на calendar.mail.ru при импорте календаря (Mail.ru)
- #114 — Blind SSRF at packagist.maximum.nl (Radancy)
- #118 — Blind SSRF on relap.io (Mail.ru, $1000)
- #121 — Blind SSRF in social-plugins.line.me (LY Corporation, $100)
- #131 — Blind SSRF in "Integrations" abusing Ruby native resolver bug (HackerOne)
- #138 — Unauthenticated Blind SSRF via xmlrpc.php (U.S. Dept Of Defense)
- #139 — Blind SSRF [Sentry Misconfiguration] (Mail.ru)
- #143 — Blind SSRF via "List-Unsubscribe" SMTP Header (Nextcloud)
- #148 — Blind SSRF in ads.tiktok.com (TikTok)
- #150 — Blind SSRF (Cloudflare)
- #160 — Blind HTTP GET SSRF via website icon fetch, bypass of pull#812 (Bitwarden)
- #174 — Blind SSRF on sentry.dev-my.com, Sentry misconfiguration (Mail.ru, $500)
- #180 — Blind SSRF on velodrome.canary.k8s.io (Kubernetes)
- #182 — Blind SSRF (potential) (Mail.ru, $300)
- #190 — Internal Ports Scanning via Blind SSRF (Infogram)
- #191 — Blind SSRF in Ticketing Integrations Jira webhooks (New Relic)
- #194 — Blind SSRF as normal user from mailapp (Nextcloud)
- #197 — Blind SSRF on synthetics.newrelic.com (New Relic)
- #198 — Internal Ports Scanning via Blind SSRF (New Relic)
- #201 — Blind SSRF via image upload URL downloader (U.S. Dept Of Defense)
- #202 — Blind SSRF in FogBugz project import (GitLab)
- #204 — Server Side Request Forgery on JSON Feed (Infogram)
- #221 — Blind SSRF in /appsuite/api/oxodocumentfilter&action=addfile (Open-Xchange, $550)
- #223 — Blind SSRF on image proxy camo.stream.highwebmedia.com (Chaturbate)
- #229 — Mail app - Blind SSRF via Sierve server / sieveHost parameter (Nextcloud)
- #232 — Blind SSRF due to img tag injection in career form (Mixmax)
- #235 — GET /api/v2/url_info endpoint Blind SSRF (Automattic)
- #237 — Bypass of SSRF Vulnerability (Node.js third-party modules)
- #240 — Mail app - blind SSRF via smtpHost parameter (Nextcloud)
- #242 — Blind SSRF on info.ucs.ru/settings/check (Mail.ru)
- #251 — Blind SSRF while Creating Templates (Stripo Inc)
- #252 — Blind SSRF at chat.makerdao.com/account/profile (BlockDev)
- #260 — [Limited bypass of #793704] Blind SSRF in Ghost CMS (Node.js third-party modules)
- #290 — Blind SSRF on infodesk.engelvoelkers.com via proxy.php (Engel & Völkers)
- #292 — Yet another SSRF query for Javascript (GitHub Security Lab, $250)

### C. Semi-Blind / Half-Blind SSRF
Partial response data leaked or limited protocol access but not full HTTP response.

- #74  — GET-based SSRF limited to HTTP on resizer.line-apps.com (LY Corporation)
- #153 — Half-Blind SSRF in kube/cloud-controller-manager, upgraded to complete SSRF (Kubernetes, $5000)
- #183 — SSRF restricted to HTTP/HTML on LINE Social Plugins (LY Corporation)
- #195 — Responsive Server-side Request Forgery (Nextcloud)

### D. Internal SSRF
Pivoting from one internal host to another, chained SSRF.

- #26  — SSRF chained to hit internal host → another SSRF (PlayStation)
- #82  — Internal Blind SSRF allows scanning internal ports (Mozilla)
- #83  — Internal SSRF bypass using slash commands at api.slack.com (Slack)
- #147 — [Uppy] Internal SSRF (bypass of #786956) (Node.js third-party modules)
- #212 — Internal Ports Scanning via Blind SSRF (URL Redirection to beat filter) (Infogram)
- #256 — SSRF - pivoting in the private LAN (Concrete CMS)


================================================================================
## 2. URL SCHEME TRICKS
================================================================================

### file:// (Local File Read / LFI via SSRF)
- #8  — SSRF & LFR via on city-mobil.ru (Mail.ru)
- #12 — SSRF on fleet.city-mobil.ru leads to local file read (Mail.ru)
- #15 — SSRF & LFR on city-mobil.ru (Mail.ru)
- #24 — External SSRF + Local File Read via FFmpeg HLS processing (TikTok)
- #41 — [city-mobil.ru] SSRF & limited LFR via base64 POST (Mail.ru)
- #44 — SSRF and LFI in site-audit tool (Semrush)
- #48 — LFI and SSRF via XXE in emblem editor (Rockstar Games, $1500)
- #59 — SSRF + local file disclosure via FFmpeg HLS (Automattic)
- #60 — SSRF + local file disclosure by video upload (Pornhub, $500)
- #75 — SSRF + local file disclosure by video upload (Pornhub, $500)
- #112 — SSRF + local file disclosure by video upload (Pornhub, $500)
- #126 — SSRF reading local files and website source code (Eternal)
- #187 — SSRF and local file read in video to gif converter (Imgur)
- #246 — SSRF / Local file enumeration via ffmpeg (Imgur)
- #254 — Local file disclosure through SSRF at next.nutanix.com (Nutanix)

### git:// Protocol
- #161 — CRLF injection & SSRF in git:// protocol leads to arbitrary code execution (GitLab)
- #296 — SSRF via git Repo by URL Abuse (GitLab)

### SMB / UNC Path (Windows SSRF)
- #80  — SMB SSRF in emblem editor exposes domain credentials, may lead to RCE (Rockstar Games, $1500)
- #92  — Apache HTTP Server on Windows UNC SSRF (CVE-2024-38472) (Internet Bug Bounty, $4920)
- #168 — Apache HTTP Server: SSRF with mod_rewrite on Windows (CVE-2024-40898) (Internet Bug Bounty, $4263)

### HTTP Request Smuggling / CRLF Injection
- #161 — CRLF injection & SSRF in git:// protocol → RCE (GitLab)
- #239 — HTTP Request Smuggling and SSRF via CRLF Injection in Curl_add_custom_headers (curl)

### Miscellaneous URL Schemes / Protocols
- #55  — DNSDumpster SSRF to Internal SMTP Access via email (Hacker Target)
- #67  — Kafka Connect RCE leveraging SSRF to internal Jolokia (JMX/HTTP) (Aiven Ltd, $5000)
- #110 — SSRF in Portainer → Internal Docker API without auth (Uber, $500)
- #181 — SSRF + RCE via fastCGI in POST /api/nr/video (Mail.ru)
- #207 — SSRF into Shared Runner by replacing dockerd with malicious server (GitLab)


================================================================================
## 3. BYPASS TECHNIQUES
================================================================================

### DNS Rebinding
- #28  — DNS Rebinding SSRF in Burp Suite MCP Server (PortSwigger, $2000)
- #104 — DNS pin middleware tricked into DNS rebinding allowing SSRF (Nextcloud)
- #228 — SSRF mitigation bypass using DNS Rebind attack (Concrete CMS)

### IPv6 / NAT64 / IPv4-mapped IPv6
- #63  — SSRF Filter Bypass via Unblocked NAT64 Local-Use IPv6 Prefix (64:ff9b:1::/48) (arkadiyt-projects)
- #167 — Incorrect Type Conversion interpreting IPv4-mapped IPv6 addresses → SSRF (curl)
- #169 — SSRF via Inconsistent URL Parsing in curl (curl)

### Decimal / IP Formatting Tricks
- #124 — SSRF blacklist bypass via IP Formatting (decimal/octal/hex IP) (Open-Xchange, $850)
- #120 — SSRF via filter bypass due to lax checking on IPs (Nextcloud, $250)

### DNS Pinning Bypass
- #104 — DNS pin middleware tricked into DNS rebinding → SSRF (Nextcloud)

### Redirect-Based Bypass (30X / Open Redirect)
- #81  — SSRF bypass via redirect in Event Subscriptions parameter (Slack)
- #86  — SSRF via hijacked aggregated API server returning 30X redirect (Kubernetes, $1000)
- #119 — RSS feed blacklist bypass via 301 redirect (Open-Xchange, $850)
- #127 — Open redirect bypass & SSRF (Smule)
- #196 — Bypass of SSRF protection (Slack commands, Phabricator integration) (Slack, $100)
- #212 — Internal Ports Scanning via Blind SSRF (URL Redirection to beat filter) (Infogram)
- #214 — SSRF in /cabinet/stripeapi/v1/siteInfoLookup (Stripo Inc) [redirect chain]

### Smokescreen / Deny-List Bypass
- #89  — Bypassing domain deny_list in Smokescreen via trailing dot (Stripe)
- #219 — Bypassing domain deny_list in Smokescreen via double brackets [[]] (Stripe)

### Host Header / URL Parsing Confusion
- #51  — SSRF via host header to access localhost (IBM)
- #152 — Inconsistent URL Parsing in curl → Potential SSRF and Access Control Bypass (curl)
- #263 — SSRF via maliciously crafted URL due to host confusion (curl)
- #275 — undici.request vulnerable to SSRF using absolute/protocol-relative URL on pathname (Internet Bug Bounty)
- #283 — SSRF через Share-ботов (VK.com, $300)
- #286 — Bypass of anti-SSRF defenses in YahooCacheSystem (Yahoo!)

### Blacklist / Whitelist Bypass
- #7   — Server Side Request Forgery mitigation bypass (GitLab)
- #56  — GitLab::UrlBlocker validation bypass → full SSRF (GitLab)
- #94  — SSRF - Blacklist bypass for mail account addition (Open-Xchange, $500)
- #96  — SSRF in Search.gov via ?url= parameter (GSA Bounty, $150)
- #99  — SSRF - Image Sources in HTML Snippets - 727234 bypass (Open-Xchange, $400)
- #106 — SSRF - URL Attachments - 725307 bypass (Open-Xchange, $400)
- #132 — SSRF via potential filter bypass with too lax local domain checking (Nextcloud, $250)
- #163 — Bypassing Whitelist to perform SSRF for internal host scanning (U.S. Dept of State)
- #165 — Additional bypass allows SSRF for internal netblocks (HackerOne)
- #166 — Bypassing HTML filter → SSRF to Internal Kubernetes Endpoints (Shopify)
- #169 — Server side request forgery on nextcloud implementation (Nextcloud)
- #171 — SSRF protection bypass (Nextcloud, $100)
- #193 — SSRF bypass (Concrete CMS)
- #203 — SSRF protection bypass in /appsuite/api/oxodocumentfilter addfile (Open-Xchange, $550)
- #260 — [Limited bypass of #793704] Blind SSRF in Ghost CMS (Node.js third-party)

### Slash Commands Bypass
- #45  — SSRF in api.slack.com using slash commands, bypassing protections (Slack)
- #83  — Internal SSRF bypass using slash commands at api.slack.com (Slack)

### Trailing Dot / Double Brackets
- #89  — Trailing dot bypasses Smokescreen domain deny_list (Stripe)
- #219 — Double brackets [[]] bypasses Smokescreen domain deny_list (Stripe)

### HTML Filter / Injection Bypass
- #99  — SSRF - Image Sources in HTML Snippets bypass (Open-Xchange)
- #166 — Bypassing HTML filter in "Packing Slip Template" → SSRF (Shopify)


================================================================================
## 4. CLOUD METADATA ENDPOINTS AND EXPLOITATION
================================================================================

### AWS (Amazon Web Services)
Endpoint: http://169.254.169.254/latest/meta-data/

- #5   — SSRF at app.hellosign.com → AWS private keys disclosure (Dropbox, $4913)
- #7   — Server Side Request Forgery mitigation bypass (GitLab) [AWS context]
- #13  — Full read SSRF in evernote.com, leak AWS metadata + LFI (Evernote)
- #20  — SSRF in webhooks → AWS private keys disclosure (Omise)
- #72  — SSRF to read AWS metaData at DoD (U.S. Dept Of Defense, $1000)
- #100 — SSRF reads AWS EC2 metadata using "readapi" variable in Streamlabs Cloudbot (Logitech, $200)
- #102 — Unauthenticated SSRF via Public Reference API - Sharing Token Bypass (Nextcloud) [EC2 context]
- #133 — SSRF to AWS file read (Lab45)
- #141 — SSRF on proxy.duckduckgo.com → access to metadata server on AWS (DuckDuckGo)
- #244 — SSRF ACCESS AWS METADATA (U.S. Dept Of Defense)
- #246 — SSRF / Local file enumeration / DoS via ffmpeg (Imgur) [AWS context]
- #281 — SSRF vulnerability → access to metadata server on EC2 and OpenStack (Phabricator, $300)

Key AWS metadata paths exploited:
  - /latest/meta-data/iam/security-credentials/  → IAM role credentials
  - /latest/meta-data/public-keys/               → SSH public keys
  - /latest/user-data/                           → bootstrap scripts (often contain secrets)
  - /latest/meta-data/                           → instance identity document

### GCP (Google Cloud Platform)
Endpoint: http://metadata.google.internal/computeMetadata/v1/
  (Requires header: Metadata-Flavor: Google)

- #4  — SSRF using Javascript exfiltrates data from Google Metadata (Snapchat)
- #11 — SSRF leaking internal Google Cloud data through upload function [SSH Keys, etc.] (Vimeo)

Key GCP metadata paths:
  - /computeMetadata/v1/instance/service-accounts/default/token
  - /computeMetadata/v1/instance/attributes/ssh-keys
  - /computeMetadata/v1/project/attributes/

### Azure
No explicit Azure metadata exploitation in these top reports.
Endpoint (for reference): http://169.254.169.254/metadata/instance?api-version=2021-02-01
  (Requires header: Metadata: true)

### OpenStack
- #281 — SSRF vulnerability → access to metadata server on EC2 and OpenStack (Phabricator, $300)
  Endpoint: http://169.254.169.254/openstack

### Multi-Cloud / Generic Metadata
- #13  — Full read SSRF leaking AWS metadata AND local file inclusion (Evernote)
- #128 — Full read SSRF in Uber internal (flyte-poc-us-east4.uberinternal.com) (Uber, $2000)
- #132 — SSRF leaking internal IP and sensitive information (U.S. Dept Of Defense)
- #215 — SSRF in headless Chrome with remote debugging → sensitive info leak (h1-ctf)
- #247 — SSRF on synthetics.newrelic.com permitting access to sensitive data (New Relic)
- #255 — SSRF due to CVE-2021-27905 (U.S. Dept Of Defense)

### Generic Internal Service Exploitation via SSRF
- #9   — Blind SSRF to internal services (Reddit)
- #17  — Full Read SSRF on GitLab's Internal Grafana (GitLab)
- #19  — Unauthenticated SSRF in Jira → RCE in Confluence (QIWI)
- #36  — Blind SSRF my.exnessaffiliates.com → internal network enumeration (EXNESS)
- #103 — SSRF in alerts.newrelic.com exposes entire internal network (New Relic)
- #110 — SSRF in Portainer → Internal Docker API without auth (Uber, $500)
- #113 — Grafana SSRF in grafana.instamart.ru (Mail.ru)
- #115 — MCS Graphite SSRF: internal network access (Mail.ru, $2500)
- #118 — CVE-2019-8451 Jira SSRF (Mail.ru)
- #144 — SSRF allowing internal server data access (U.S. Dept Of Defense)
- #146 — SSRF in img.lemlist.com → Localhost Port Scanning (lemlist)
- #186 — SSRF allows access to internal services like Ganglia (Dropbox, $729)
- #188 — SSRF on testing endpoint (APITest.IO)
- #189 — SSRF issue in "URL target" (Zendesk)
- #192 — SSRF In plantuml on plantuml.pre.gitlab.com (GitLab)
- #215 — SSRF in headless Chrome with remote debugging (h1-ctf)
- #218 — Full read SSRF at DoD (U.S. Dept Of Defense)
- #256 — SSRF - pivoting in the private LAN (Concrete CMS)


================================================================================
## 5. SSRF → RCE CHAINS
================================================================================

### A. SSRF → Jira → Confluence RCE
- #19 — Unauthenticated SSRF in jira.tochka.com → RCE in confluence.bank24.int (QIWI)
  Chain: SSRF in Jira authorization → pivot to internal Confluence → RCE
  Real-world, high-impact chain at a financial institution.

### B. Kafka Connect → SQLite JDBC → Jolokia → RCE
- #67 — [Kafka Connect] RCE via file upload via SQLite JDBC driver + SSRF to internal Jolokia (Aiven Ltd, $5000)
  Chain: SSRF in Kafka Connect HTTP Sink → file upload via SQLite JDBC → internal Jolokia JMX → RCE

### C. SMB SSRF → Credential Theft → RCE
- #80 — SMB SSRF in emblem editor exposes domain credentials, may lead to RCE (Rockstar Games, $1500)
  Chain: SSRF via SMB/UNC path → NTLM hash capture → credential relay → RCE

### D. CRLF Injection in git:// → RCE
- #161 — CRLF injection & SSRF in git:// protocol leads to arbitrary code execution (GitLab)
  Chain: SSRF in git:// protocol → CRLF injection → arbitrary code execution

### E. SSRF → fastCGI → RCE
- #181 — SSRF + RCE через fastCGI в POST /api/nr/video (Mail.ru)
  Chain: SSRF in video processing → fastCGI protocol abuse (PHP-FPM) → RCE

### F. Grafana Open Redirect → Stored XSS → SSRF → Full Read
- #184 — CVE-2025-4123: Grafana Open Redirect → Stored XSS → SSRF (Full Read) (U.S. Dept Of Defense)
  Chain: Open Redirect → Stored XSS → SSRF → internal data exfiltration

### G. Portainer SSRF → Docker API Access → Container Escape
- #110 — SSRF in Portainer → Internal Docker API without auth (Uber, $500)
  Chain: SSRF → unprotected Docker socket/API → container escape potential → RCE

### H. Kubernetes SSRF → Internal API Access
- #142 — SSRF for kube-apiserver cloudprovider scene (Kubernetes)
- #166 — HTML filter bypass → SSRF to Internal Kubernetes Endpoints (Shopify)
  Chain: SSRF → kube-apiserver / internal services → cluster compromise

### I. Headless Chrome SSRF → Debug Protocol → RCE
- #215 — SSRF in headless Chrome with remote debugging → sensitive information leak (h1-ctf)
  Chain: SSRF → Chrome DevTools Protocol (port 9222) → arbitrary command execution

### J. GitLab Runner SSRF → dockerd Replacement → CI/CD RCE
- #207 — SSRF into Shared Runner, replacing dockerd with malicious server in Executor (GitLab)
  Chain: SSRF → replace legitimate dockerd → malicious executor → CI/CD pipeline RCE

### K. SSRF → Git Config Injection → RCE
- #109 — Injection of `http.<url>.*` git config settings → SSRF (GitLab, $3000)
  Chain: Git config injection → SSRF → credential leak → further exploitation


================================================================================
## 6. ATTACK VECTORS / ENTRY POINTS (Cross-cutting)
================================================================================

### Video/Media Processing (FFmpeg HLS)
- #24 — External SSRF + LFR via FFmpeg HLS (TikTok, $2727)
- #59 — SSRF + local file disclosure via FFmpeg HLS (Automattic)
- #60 — SSRF + local file disclosure by video upload (Pornhub, $500)
- #75 — SSRF + local file disclosure by video upload (Pornhub, $500)
- #112 — SSRF + local file disclosure by video upload (Pornhub, $500)
- #187 — SSRF + local file read in video to gif converter (Imgur)
- #240 — Server Side Request Forgery In Video to GIF Functionality (Imgur)
- #246 — SSRF / LFI / DoS via ffmpeg (Imgur)

### SVG / XXE → SSRF
- #37 — XXE Injection through SVG image upload leads to SSRF (Zivver)
- #47 — SVG Server Side Request Forgery (SSRF) (Shopify, $500)
- #48 — LFI and SSRF via XXE in emblem editor (Rockstar Games, $1500)
- #140 — Non-production Open Database + XXE → SSRF (Evernote)
- #217 — SSRF via XXE OOB (Uber)
- #285 — XXE and SSRF on webmaster.mail.ru (Mail.ru)

### Webhooks / Callbacks
- #20 — SSRF in webhooks → AWS private keys disclosure (Omise)
- #32 — SSRF in webhook functionality (HackerOne, $2500)
- #62 — SSRF via notify_url parameter (Razer, $2000)
- #172 — SSRF via webhook (Mixmax)
- #191 — Blind SSRF in Ticketing Integrations Jira webhooks (New Relic)
- #213 — Shopify API ruby SDK session setup SSRF (Shopify)
- #222 — SSRF in gitlab.com webhook (GitLab)
- #230 — SSRF in app webhooks (Dropbox, $512)

### Git Repository Import
- #6  — SSRF on project import via remote_attachment_url on a Note (GitLab, $10000)
- #173 — SSRF in gitlab.com via project import (GitLab)
- #205 — SSRF when importing a project from a git repo by URL (GitLab)
- #249 — Potential SSRF via Git repository URL (GitLab)
- #296 — SSRF via git Repo by URL Abuse (GitLab)

### Image Upload / URL Fetch
- #12 — SSRF on fleet.city-mobil.ru leads to local file read (Mail.ru)
- #31 — SSRF in clients.city-mobil.ru (Mail.ru, $1500)
- #34 — SSRF In Get Video Contents (Semrush)
- #40 — SSRF on image renderer (PlayStation, $1000)
- #79 — SSRF in imgur.com/vidgif/url (Imgur)
- #95 — SSRF in the application's image export functionality (Visma Public, $250)
- #99 — SSRF - Image Sources in HTML Snippets (Open-Xchange)
- #101 — SSRF on crossdomain.php via url parameter (Sony)
- #102 — Unauthenticated SSRF via Public Reference API (Nextcloud)
- #126 — SSRF in zomato.com reading local files (Eternal)
- #136 — SSRF in imgur video GIF conversion (Imgur)
- #146 — SSRF in img.lemlist.com localhost port scanning (lemlist)
- #155 — Server side request forgery on image upload for lists (Instacart, $50)
- #160 — Blind HTTP GET SSRF via website icon fetch (Bitwarden)
- #179 — SSRF in proxy.duckduckgo.com via image_host (DuckDuckGo)
- #200 — SSRF in icons.bitwarden.net (Bitwarden)
- #231 — SSRF via 'Add Image from URL' feature (Shopify)
- #240 — SSRF In Video to GIF (Imgur)
- #268 — Dropbox apps Server side request forgery (Dropbox)
- #269 — SSRF issue in Bime (Bime)
- #271 — SSRF in login page using fetch API (U.S. Dept Of Defense)

### Office Documents / Email
- #39 — SSRF via Office file thumbnails (Slack, $4000)
- #87 — SSRF in VCARD photo upload functionality (Open-Xchange, $850)
- #105 — SSRF - Office Documents - Image URL (Open-Xchange, $450)
- #106 — SSRF - URL Attachments (Open-Xchange)
- #108 — Blind SSRF in Mail App (Nextcloud)
- #194 — Blind SSRF as normal user from mailapp (Nextcloud)
- #220 — Mail app - blind SSRF via imapHost parameter (Nextcloud)
- #229 — Mail app - Blind SSRF via Sierve server / sieveHost (Nextcloud)
- #240 — Mail app - blind SSRF via smtpHost parameter (Nextcloud)

### Sentry Misconfiguration (Blind SSRF via DSN)
- #27 — Blind SSRF on errors.hackerone.net (HackerOne, $3500)
- #53 — Blind SSRF on debug.nordvpn.com (Nord Security)
- #77 — Blind SSRF on platform.dash.cloudflare.com (Cloudflare)
- #139 — Blind SSRF [Sentry Misconfiguration] (Mail.ru)
- #174 — Blind SSRF on sentry.dev-my.com (Mail.ru, $500)

### Cookie Theft via SSRF
- #70 — [tanks.mail.ru] SSRF + Cookie theft (Mail.ru, $750)
- #177 — [la.mail.ru] SSRF + Cookie theft (Mail.ru, $750)

### Jira / Atlassian SSRF (CVEs)
- #16 — Blind SSRF in OAuth Jira authorization controller (GitLab, $4000)
- #19 — SSRF in Jira → RCE in Confluence (QIWI)
- #118 — CVE-2019-8451 Jira SSRF (Mail.ru)
- #159 — SSRF on jira.mariadb.org (MariaDB)

### PDF Generation / Export
- #91 — SSRF in Functional Administrative Support Tool PDF generator (U.S. Dept Of Defense, $4000)

### Proxy / Relay Services
- #103 — SSRF in alerts.newrelic.com exposes entire internal network (New Relic)
- #111 — SSRF via Prerender HAR Capturer (QIWI)
- #120 — SSRF via filter bypass lax checking (Nextcloud)
- #141 — SSRF on proxy.duckduckgo.com (DuckDuckGo)
- #179 — SSRF in proxy.duckduckgo.com via image_host (DuckDuckGo)

### CMS / Plugin SSRF
- #97  — SSRF in Ghost CMS (Node.js third-party)
- #158 — WordPress 4.7 CSRF → HTTP SSRF any private ip:port + basic-auth (WordPress)
- #160 — WordPress SSRF via website icon fetch (Bitwarden)
- #170 — SSRF thru File Replace (Concrete CMS)
- #193 — SSRF bypass (Concrete CMS)
- #216 — SSRF in Jabber settings in phpBB Admin (phpBB)
- #228 — SSRF mitigation bypass using DNS Rebind (Concrete CMS)
- #256 — SSRF - pivoting in private LAN (Concrete CMS)
- #299 — SSRF via /wordpress/xmlrpc.php (Ian Dunn)

### Database / Storage
- #67  — Kafka Connect SQLite JDBC SSRF → RCE (Aiven Ltd)
- #123 — Unsanitized IPFS CID Allows SSRF Against Configured Gateway (curl)
- #271 — SSRF via CVE-2021-26855 (ProxyShell) (U.S. Dept Of Defense)
- #272 — CVE-2021-26855 → SSRF (U.S. Dept Of Defense)

### curl / Library-level SSRF
- #123 — Unsanitized IPFS CID Allows SSRF (curl)
- #152 — Inconsistent URL Parsing in curl → SSRF (curl)
- #167 — Incorrect Type Conversion IPv4-mapped IPv6 → SSRF (curl)
- #239 — HTTP Request Smuggling + SSRF via CRLF Injection in Curl_add_custom_headers (curl)
- #257 — Incorrect Encoding Conversion in hostname → SSRF (curl)
- #263 — SSRF via maliciously crafted URL due to host confusion (curl)
- #275 — undici.request vulnerable to SSRF (Internet Bug Bounty)

### CodeQL / Security Lab SSRF Queries
- #206 — Golang SSRF query improvements (GitHub Security Lab)
- #264 — Java: Added URLClassLoader and WebClient SSRF sinks (GitHub Security Lab)
- #265 — Python: Add SSRF sinks (GitHub Security Lab)
- #273 — C# SSRF query (GitHub Security Lab)
- #274 — Java: Add JDBC connection SSRF sinks (GitHub Security Lab)
- #277 — Yet another SSRF query for Go (GitHub Security Lab, $450)
- #278 — Yet another SSRF query for Go (GitHub Security Lab, $450)
- #284 — Yet another SSRF query for Javascript (GitHub Security Lab, $250)
- #289 — Java: Add SSRF query for Java (GitHub Security Lab)
- #291 — Yet another SSRF query for Go (GitHub Security Lab)
- #294 — Yet another SSRF query for Javascript (GitHub Security Lab, $250)
- #300 — Yet another SSRF query for Javascript (GitHub Security Lab)
- #301 — Yet another SSRF query for Go (GitHub Security Lab)
- #302 — Yet another SSRF query for Javascript (GitHub Security Lab)
- #306 — CodeQL query to detect SSRF in Python (GitHub Security Lab, $500)
- #307 — Java: CWE-918 SSRF (GitHub Security Lab, $250)


================================================================================
## 7. KEY DEFENSE-BYPASS PATTERNS SUMMARY
================================================================================

### URL Parser Inconsistencies
- Trailing dot:       domain.com. → bypasses deny_list matching "domain.com"
- Double brackets:    [[domain.com]] → bypasses Smokescreen
- IPv4-mapped IPv6:   ::ffff:127.0.0.1 → bypasses IPv4-only filters
- NAT64 prefix:       64:ff9b::1::/48 → bypasses IPv4 block
- Decimal/octal IP:   2130706433 (127.0.0.1) → bypasses string-based checks
- Host confusion:     user@evil.com:80@internal.com → curl host confusion
- Protocol-relative:  //evil.com → path-only check bypass

### DNS-Level Bypasses
- DNS Rebinding:      TTL=0, first resolve to allowed IP, then to internal IP
- DNS pinning bypass: Trick middleware that pins after first lookup

### Redirect Chaining
- 301/302 redirect:   Allowed URL → redirect to internal IP
- Hijacked API:       Compromised metrics-server returns 30X → k8s SSRF

### Protocol Confusion
- CRLF injection:     Inject headers/body into protocol stream (git://, HTTP)
- fastCGI direct:     SSRF → fastCGI port → PHP-FPM code execution
- SMB/UNC:           Windows SSRF → NTLM hash capture
- Docker socket:      SSRF → unix:///var/run/docker.sock → container escape

### Entry Point Categories
- Video/Image upload processors (FFmpeg, imagemagick)
- Webhooks and callback URLs
- Git repository import features
- Office document thumbnail generation
- SVG/XML parsing (XXE → SSRF)
- PDF generators / HTML renderers
- URL preview / link unfurling services
- Proxy and image resizing services
- Mail server configurations (SMTP/IMAP/Sieve)
- Monitoring/integration platforms (Sentry, Grafana, Jira)
- CSS/HTML import features
- Icon/favicon fetchers
