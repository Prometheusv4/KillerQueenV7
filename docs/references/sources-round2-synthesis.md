# New Sources Synthesis — Round 2 (June 2026)
# ALL new knowledge extracted from operator's second source list

---

## DDOSI.ORG H1 DASHBOARD (14,617 reports, 15 accessible)

Notable recent reports:
- **Shopify**: UAF in MRubyEngine#initialize → local RCE (report #3679660)
- **Node.js**: Incomplete fix CVE-2026-21637 — loadSNI() in _tls_wrap.js lacks try/catch → DoS
- **Rocket.Chat**: RBAC bypass via `permissionRequired` typo → admin-only log access
- **Rocket.Chat**: Complete auth bypass to admin via SQL injection (#3564655, 46 upvotes)
- **Nextcloud**: SVG filter primitives bypass remote image blocking → email tracking
- **Nextcloud**: `position: fixed !important` bypasses CSS sanitizer → full-viewport phishing
- **Nextcloud**: Unquoted body background attribute → CSS injection bypass
- **Nextcloud**: SMIL values + `by` attributes bypass remote image blocking
- **Nextcloud**: Stored XSS in attachment-display exploitable through SameSite
- **curl**: IPv6 zoneid omitted from host identity → cross-realm credential leak
- **curl**: Digest auth state leak on cross-origin redirect via Netrc
- **curl**: RTSP session header reuse across hosts on same easy handle
- **curl**: CURLOPT_AUTOREFERER leaks previous URL to different origin
- **Ruby on Rails**: Entity-encoded control-character-split javascript: URL bypass in sanitizer
- **HackerOne**: Residual malicious payloads after vulnerability fixes

Pattern: JS-heavy SPA — pagination not working via web_extract. 14,617 entries total.

---

## ORANGE TSAI BLOG (blog.orange.tw)

Key articles:
- **WorstFit (2025)**: Hidden transformers in Windows ANSI — best-fit mapping exploits
- **Confusion Attacks (2024)**: Semantic ambiguity in Apache HTTP Server — pre-auth RCE
- **CVE-2024-4577**: PHP CGI argument injection — yet another PHP RCE
- **ProxyLogon (2021)**: MS Exchange pre-auth RCE chain
- **ProxyShell (2021)**: MS Exchange post-auth RCE
- **ProxyOracle (2021)**: MS Exchange cookie decryption → credential theft
- **ProxyRelay (2022)**: MS Exchange NTLM relay → RCE
- **Journey Combining Web + Binary (2021)**: PHP logic bugs + PHP UAF → production RCE
- **Facebook Hack (2020)**: Unauthenticated RCE on MobileIron MDM
- **GPON Modem RCE (2019)**: ISP modem remote code execution
- **OSEE from Web Dog (2025)**: Web security researcher's guide to Advanced Windows Exploitation

Methodology: Multi-layer attacks — reverse proxy → app → cache. Parser logic bugs across layers. Web + binary exploitation chained.

---

## PWN2OWN (labs.reversec.com + Wikipedia)

FROM REVERSEC LABS:
- **Samsung S20 RCE (2020)**: Galaxy Store app WebView JS interface → silent APK install via NFC/WiFi MITM
- **Jandroid (2019)**: Automated APK scanning for logic bugs — configurable templates
- **Safari Pwn2Own 2018**: Two Safari vulns (CVE-2018-4199, CVE-2018-4196) → full macOS compromise
- **Safari Wasm (2018)**: CVE-2018-4121 — heap underflow in WebAssembly on macOS 10.13.3
- **Huawei Mate 9 Pro (2017)**: Logic bugs in Huawei Reader + HIApp
- **Chainspotting (2018)**: 11 logic bugs across 6 Android apps → silent APK installation
- **Amazon Fire Phone (2015)**: 3 bugs chained → RCE, no memory corruption
- **Win32k Kernel (2013)**: Pool overflow in Windows 7 to escape Chrome sandbox
- **NFC (2014)**: NFC-based zero-days on mobile

FROM WIKIPEDIA:
- 2007-2024 full history: browsers, OS, mobile, virtualization, automotive, IoT
- Top prize: $200,000 (2023 Tesla)
- 51 zero-days in single year (2017, $833,000)
- VUPEN: 11 distinct zero-days, $400,000 (2014)
- lokihardt: $225,000 breaking IE11, Chrome, Safari (2015)
- Chrome sandbox escape via Win32k.sys kernel pool overflow (2013)
- VMware virtual machine escape first achieved (2017)
- Tesla Model 3 hacked (2019)
- iPhone 14 hacked (2023)

---

## PTES (Penetration Testing Execution Standard)

7 phases:
1. Pre-engagement Interactions
2. Intelligence Gathering (OSINT, HUMINT, SIGINT)
3. Threat Modeling
4. Vulnerability Analysis
5. Exploitation
6. Post Exploitation
7. Reporting

Technical Guidelines sub-standard for execution details.

---

## iOS VULNERABILITY RESEARCH (IdanBanani)

Key resources:
- **Kernel Debugging**: Google Project Zero ktrw
- **Jailbreaking**: checkra1n
- **FRIDA**: Dynamic instrumentation — OBTS v4 talk, DFRWS EU workshop, frida-boot
- **0day In the Wild**: Google Project Zero spreadsheet
- **IOKit Reversing**: Apple IOKit fundamentals, reversing tips
- **XPC Exploitation**: XPC internals, sandbox share case studies
- **Fuzzing**: Project Zero "fuzzing iOS code on macOS at native speed"
- **XNU kernel source**: github.com/apple/darwin-xnu
- **Key blogs**: bazad.github.io, ZecOps, put.as papers
- **Objective by the Sea**: v1-v4 conference talks

---

## PACU IAM PRIVILEGE ESCALATION (pwnedlabs.io)

Vulnerable policy pattern:
```json
{"Action": ["iam:Get*", "iam:List*", "iam:Put*"], "Resource": "*"}
```

Attack: `iam:Put*` → `PutUserPolicy` → attach admin inline policy to self
Pacu module: `iam__privesc_scan` auto-detects and exploits
Prevention: deny `iam:PutUserPolicy` via SCP, use Access Analyzer

---

## PTES METHODOLOGY

7-phase standard: Pre-engagement → Intel Gathering → Threat Modeling → Vulnerability Analysis → Exploitation → Post Exploitation → Reporting. Technical Guidelines sub-standard available for execution details.

---
*Generated June 2026 — for integration into Killer Queen*
