# Blocked Sources — Recovered Content
# Extracted June 2026

---

## BUGBOARD.RSECLOUD.COM — RECOVERED (10,000+ H1 reports)

Sample of recent reports with full vulnerability details:

- **3784125**: GnuTLS OCSP stapling CERT-ID binding bypass — variant of CVE-2020-8286
  - CVSS 7.4 (High), hardcoded index [0] trusts unrelated SingleResponse
  - curl built against GnuTLS, CURLOPT_SSL_VERIFYSTATUS bypassed
- **3717552**: CURLOPT_PROXY_CRLFILE silently ignored on backends without support
- **3718265**: Shared HSTS cache accessed without lock (race condition)
- **3776535**: RTSP Digest auth state leaks across origins on reused handle
- **3776433**: TFTP upload ignores --continue-at, leaks local file prefix
- **3774977**: libcurl 8.20.0 ignores Digest domain protection space
- **3766065**: CURLOPT_COOKIE leaked to cross-origin redirect target
- **3650504**: Missing access control linking banners/campaigns (Revive Adserver)
- **3653196**: Blind SQL injection via clientid in zone-include.php (Revive Adserver)

Platform: curl is the most-reported project on the dashboard.

---

## BHUSA 2017 GIST — RECOVERED

Full Black Hat USA 2017 session catalogue:

DAY 1:
- Web Cache Deception Attack (Omer Gil)
- SQLite Multi-Target Exploitation (many birds, one stone)
- Serverless Runtime Hacking (AWS Lambda, Azure Functions)
- Cracking the Lens: HTTP Hidden Attack Surface
- The Art of Securing 100 Products
- Protecting Pentests: Secure Testing Recommendations
- Cumulus Cloud Exploitation Toolkit (Arsenal)
- WSSIP WebSocket Manipulation Proxy (Arsenal)
- CSP Auditor (Arsenal)

DAY 2:
- Skype & Type: Keystroke Leakage Over VoIP
- Datacenter Orchestration Security (Kubernetes, Mesos, Docker at Scale)
- Game of Chromes: Zombie Chrome Extensions
- Friday the 13th: JSON Attacks
- Docker API RCE + Shadow Containers + Hypervisor Persistence
- New Era of SSRF: URL Parser Exploitation in Trending Languages
- FuzzAPI: REST API Fuzzing (Arsenal)
- NOPE Proxy: Non-HTTP Proxy Extension (Arsenal)
- ThreadFix: Web Application Attack Surface Calculation (Arsenal)

---

## GOOGLE 0DAY SPREADSHEET — PARTIAL

Introduction tab recovered with methodology and scope rules:
- Tracks 0-days detected in-the-wild from July 15, 2014
- Excludes EOL software, post-disclosure exploitation
- Includes Equation Group and Hacking Team leaks
- Year tabs (2026-2014) blocked by auth
- BUT: RCA page already extracted has 60+ CVEs with root cause analysis
  (deeper technical content than the spreadsheet's metadata)

---

## STILL BLOCKED (4 sources):

| Source | Blocker |
|--------|---------|
| ddosi.org full dataset | WordPress API timed out |
| infosecinstitute.com ICS | Cloudflare bot protection |
| H1 reports 3475626, 2899858 | Needs HackerOne auth |
| kslr/simple-cloudflare-bypass | Empty/error response |

---
*Generated June 2026*
