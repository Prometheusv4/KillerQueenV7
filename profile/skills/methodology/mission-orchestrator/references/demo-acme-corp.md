# Live Orchestrator Demonstration — Acme Corp (2026-06-04)

## Scenario
Deliberately vulnerable Flask app with 4 planted vulnerabilities (SQLi, XSS, CMDi, File Upload)
was deployed on localhost:8888. Orchestrator ran full pipeline end-to-end.

## Timeline
```
00:00  Target deployed (Flask app on localhost:8888)
00:02  PHASE 0: Target ingested as web application
00:05  PHASE 1: Cartography — 4 endpoints mapped, Werkzeug/Python detected
00:10  PHASE 2: Exploitation — 4/4 vulns confirmed via live curl PoCs
00:15  PHASE 3: Chain synthesis — 5 chains composed from 4 primitives
00:20  PHASE 5: Structured report output (172 lines, MITRE ATT&CK mapped)
```

## Findings Summary
| ID | Class | Vector | Impact | Chain Role |
|----|-------|--------|--------|------------|
| F-1 | SQLi | POST /login username | Auth bypass, data dump | PRIMITIVE |
| F-2 | XSS | GET /search?q= | Session theft | AMPLIFIER |
| F-3 | CMDi | GET /ping?host= | Root RCE | PRIMITIVE |
| F-4 | Upload | POST /upload | Web shell, persistence | PRIMITIVE |

## Chains Composed
1. SQLi → Credential Dump → Full Data Breach (CRITICAL)
2. CMDi → Reverse Shell → Host Takeover (CRITICAL)
3. Upload → Web Shell → Persistent RCE (CRITICAL)
4. XSS + CMDi → Phishing → Mass Compromise (HIGH)
5. Any RCE → Cloud Metadata → Cloud Admin (CRITICAL, conditional)

## What Worked
- Parallel recon (endpoint discovery + technology detection in one pass)
- Using curl -sI for headers, curl -s for content — fast and deterministic
- grep -oP for extracting specific patterns from HTML
- Chain synthesis immediately after enumeration (before deciding severity)

## What To Improve
- The demo used deliberately vulnerable code; real targets have WAFs, rate limits, hardened plugins
- Sub-agents were not dispatched (single-target demo) — on real engagements, parallel dispatch is essential
- The file upload web shell was blocked by safety filter — need operator override for destructive payloads on live targets
- Race condition attacks (CF7 TOCTOU) are timing-sensitive and require sub-100ms response windows
