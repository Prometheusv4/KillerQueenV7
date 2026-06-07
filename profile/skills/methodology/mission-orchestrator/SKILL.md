---
name: mission-orchestrator
description: Autonomous mission orchestration — decomposes targets into objectives, dispatches sub-agents with attack-type skills, synthesizes findings, chains exploits, produces structured reports. The brain that runs engagements end-to-end without guidance.
category: methodology
triggers:
  - hack target
  - engage
  - pentest
  - red team
  - assess
  - exploit
  - find vulnerabilities on
  - scan target
  - recon target
  - attack target
  - mission
  - run engagement
  - autonomous
  - orchestrate
---

# Mission Orchestrator — Autonomous Engagement Engine

Load this skill when the operator commands an engagement on a target.
This skill orchestrates: recon → vulnerability mapping → exploitation → chaining → post-exploit → report.
It dispatches sub-agents, deduplicates, synthesizes, and produces final deliverables.

---

## PHASE 0: INGEST TARGET

Parse the target from the operator's command. Determine type:

| Target Pattern | Type | Primary Skills |
|---|---|---|
| IP address, CIDR, hostname | Network / Infrastructure | infrastructure-attacks, kali-tools-arsenal |
| URL, domain, web app | Web Application | web-attacks, testing-methodology |
| AWS account ID, cloud resource | Cloud / IAM | cloud-iam-attacks, infrastructure-attacks |
| Firmware binary, IoT device, ICS/SCADA | Embedded / IoT | embedded-iot-attacks, infrastructure-attacks |
| GitHub URL, local path, repo name | Source Code / Zero-Day | exploit-development, web-attacks, malware-dev |
| Malware sample, RAT binary, C2 traffic | Malware Analysis | malware-dev, defensive-forensics |
| Email, username, phone, name | OSINT / Person | threat-intel |
| Wallet, contract address | Web3 / Smart Contract | web-attacks (supply chain patterns) |
| APK, IPA | Mobile | mobile-attacks |
| AI/LLM endpoint, model name | AI/ML | ai-ml-attacks |
| Browser exploit, V8/WebKit bug | Browser Exploitation | browser-exploitation, exploit-development |
| Cloudflare/WAF protected target | Anti-Bot Bypass | cloudflare-bypass, web-attacks |
| Pwn2Own/contest target | Zero-Day Contest | pwn2own-exploitation, exploit-development |
| Parser differential, encoding bug | Semantic Attack | orange-tsai-methodology, web-attacks |

If ambiguous, ask one question: "Is this a network target, web application, codebase, OSINT target, or mobile app?"

---

## PITFALLS (learned from live engagements)

0. **Sub-agents timeout on DeepSeek v4 Pro with massive write tasks.** When delegating file creation work (>3 files, each >5KB), sub-agents consistently hit the 600s timeout and produce nothing. Workaround: use `execute_code` with `write_file` for bulk local file creation instead. Sub-agents excel at: reasoning, analysis, web extraction, searching. They FAIL at: bulk writing many large files. Pattern: if a task requires creating/expanding multiple skills or references, do it yourself with execute_code — save sub-agents for extraction and analysis.

1. **AJAX nonces are single-use.** WordPress AJAX actions (dnd_codedropz_upload, etc.) consume the nonce on first use. Reusing the same nonce returns "Missing security token." Always extract a fresh nonce immediately before each exploit attempt.
2. **Rate-limiting on auth endpoints is aggressive.** cPanel/WHM will IP-block after ~10 failed logins. WordPress login pages may also throttle. Spread brute force across time, use proxy rotation, or accept that you have ~10 attempts before needing a new IP.
3. **File upload plugins at latest versions are hardened, but patches are fragile.** The drag-and-drop CF7 plugin has had 16 CVEs — most unauthenticated, most file upload bypasses. v1.3.9.8 blocked all 10 standard bypass techniques tested (php%, double extension, null byte, case variation, phar, svg, .htaccess). BUT: CVE-2026-5718 (CVSS 8.1, NVD updated May 26 2026) found a Non-ASCII filename blacklist bypass affecting ≤ 1.3.9.7 — patched in 1.3.9.8. If target runs 1.3.9.7 or below, upload via filenames containing non-ASCII chars (e.g. Greek beta: `proof-β.php`). CVE-2026-5710 (≤ 1.3.9.6) allows arbitrary file read inside wp-content via `mfile[]` path traversal — can exfiltrate uploaded shells for path verification. ALWAYS check the EXACT plugin version (not just "latest") — the gap between two patch versions can contain a 9.8-critical window. See `references/dnd-upload-cf7-cve-history.md` for the full timeline.
4. **SSL certificates leak subdomains.** Before running subdomain bruteforce tools, extract Subject Alternative Names from the SSL cert — often reveals cpanel, webmail, webdisk, cpcalendars, cpcontacts, autodiscover that passive DNS would miss.
7. **Target going dark mid-engagement kills all active workers.** When a VPS reboots, gets taken down, or network routes shift, all running brute force / exploit workers silently freeze — they don't crash, they just hang on TCP connect timeouts. Logs stop updating. Processes remain alive consuming no CPU. Detection: if worker log progress hasn't changed in 30+ minutes and curl returns HTTP 000 (TCP timeout), the target is down. Do NOT kill workers — they'll auto-resume if the target comes back. Do NOT restart them (duplicates effort). Instead: note the frozen state, pivot to passive intelligence gathering (CVE research on identified versions, exploit development prep), and periodically poll the target (`curl --connect-timeout 5 --max-time 8`). When target returns, verify workers have resumed before launching anything new.
8. **Sub-agents lie about CVEs — ALWAYS verify before executing.** Sub-agents and web searches frequently report CVEs as "unauthenticated" without checking the CVSS privilege requirement (PR:N vs PR:L). Example: CVE-2026-29201 was reported by the sub-agent as "unauthenticated arbitrary file read" — actual Tenable/NVD data showed CVSS v3.1 PR:L (requires cPanel login). Verification procedure: for every CVE before exploiting, check nvd.nist.gov or tenable.com, look at the CVSS v3.1 vector string, confirm PR:N (no privileges required) or PR:L (low privileges). If PR:L, it's authenticated — skip unless you have credentials.
9. **Plan before executing — operator demands it.** For multi-phase attack sequences, present the ordered plan with phases (Verify → Probe → Exploit) before firing. Each phase needs: goal, method, and double-check criteria. Show the plan, get approval, then execute one phase at a time. This was an explicit operator correction — do not skip straight to execution.
10. **Test payloads locally before deploying.** Worms, shells, and exploit scripts must be tested in a local simulation before uploading to target. A `php -l` syntax check is insufficient — runtime behavior matters. Create a simulated environment (fake WP constants, writable directories) and verify every module of the payload.

11. **Search beyond server-side — full spectrum attacks.** When the operator says "search all factors" or "deep comprehensive", expand beyond CVEs and server exploits. Attack surfaces include: client-side (XSS, CSRF, CORS, postMessage), OSINT (social media, employees, Glassdoor, business registries), DNS/email (SPF/DKIM/DMARC, email spoofing, MX), external infrastructure (Jenkins, Grafana, ERPNext, Slack — often on separate IPs), supply chain (plugin dependencies, CDN resources), business logic (job application flows, contact forms), and geographic/regional vectors. The most valuable findings often come from OSINT and external infrastructure — a Jenkins instance or Grafana metrics endpoint can be more impactful than any WordPress plugin CVE.

13. **GitHub raw README branch/case sensitivity.** `raw.githubusercontent.com/OWNER/REPO/main/README.md` may return 14 bytes (404) when the repo uses `master` branch or lowercase `readme.md`. Try all 4 combinations: main/README.md → master/README.md → main/readme.md → master/readme.md. If all fail, fall back to web_extract on the GitHub repo page. Detected on: fkie-cad/awesome-embedded-and-iot-security, kayranfatih/awesome-iot-and-hardware-security, IdanBanani/iOS-Vulnerability-Research.

14. **Conference sites behind Cloudflare → use web.archive.org.** Black Hat, DEF CON, and similar conference briefings pages are often behind Cloudflare anti-bot. Curl returns "Attention Required! | Cloudflare." web_extract via web.archive.org works: `https://web.archive.org/web/<YYYYMM>/https://www.blackhat.com/us-<YY>/briefings.html`. The archive captures are comprehensive — full talk titles, descriptions, speaker names, and slide links.

## PHASE 1: CARTOGRAPHY (Build the Map)

### For Network/Infrastructure targets:
1. **Passive recon** (parallel):
   - `amass enum -d <domain> -o /tmp/amass.txt`
   - `subfinder -d <domain> -o /tmp/subfinder.txt`
   - `theHarvester -d <domain> -b all -f /tmp/harvest.html`
   - `curl -s "https://crt.sh/?q=%25.<domain>&output=json" | jq -r '.[].name_value' | sort -u > /tmp/crtsh.txt`
2. **Active recon** (after passive completes):
   - `nmap -p- -sV -sC -O --min-rate=5000 -oA /tmp/nmap_full <target>`
   - Feed to `nmap-vulners` for CVE mapping
3. **Service enumeration**: auto-recon, nuclei, service-specific tools
4. **Attack surface map**: every open port, every web server, every API, every login form

### For Web Applications:
1. **Technology ID**: `whatweb <url>`, `wappalyzer`
2. **Content discovery**: `ffuf -u <url>/FUZZ -w /usr/share/wordlists/dirb/common.txt`
3. **Parameter discovery**: `arjun -u <url>`, `paramspider`
4. **API endpoints**: look for `/api/`, `/graphql`, swagger docs, OpenAPI specs
5. **JS analysis**: download JS bundles, grep for endpoints, secrets, postMessage listeners
6. **postMessage audit** (MANDATORY per agent.md §10.4): grep every JS bundle for `addEventListener("message"` and `postMessage(`

### For Source Code / Repos:
1. Clone to `~/code_audit/<project>/`
2. Detect language, framework, build system, deps
3. Build architecture map: entry points → trust boundaries → sinks
4. Run SAST stack: semgrep, CodeQL (if available), bandit/gosec/brakeman
5. Every dep version-checked against CVE databases
6. postMessage + cookie scope audit (MANDATORY)

---

## PHASE 2: DECOMPOSE & DISPATCH

Break the engagement into parallel workstreams. Each gets a sub-agent with the relevant skill loaded.

### Sub-Agent Templates:

**Recon Agent** (for network targets):
```
goal: "Run full reconnaissance on <target>. Passive then active. Map all subdomains, open ports, services, technologies. Output structured JSON."
skills: ["kali-tools-arsenal", "infrastructure-attacks"]
toolsets: ["terminal", "web"]
context: "Target: <target>. Use amass, subfinder, crt.sh, nmap -p- -sV -sC, nuclei, whatweb. Output to /tmp/recon_<target>.json"
```

**Web Vulnerability Agent**:
```
goal: "Test <target> for all OWASP Top 10 + WSTG categories. Run nuclei, fuzz parameters, test auth, test IDOR, test SSRF, test all injection points. Output structured findings."
skills: ["web-attacks", "testing-methodology"]
toolsets: ["terminal", "web", "browser"]
context: "Target: <url>. Run full WSTG methodology. Test every input, every API, every auth boundary. Flag every finding as primitive/amplifier per chain protocol."
```

**Embedded/IoT Agent** (for firmware/ICS/hardware targets):
```
goal: "Analyze <firmware/device> for vulnerabilities. Extract filesystem, find hardcoded credentials, check debug interfaces, test for command injection, map attack surface."
skills: ["embedded-iot-attacks", "exploit-development"]
toolsets: ["terminal", "file"]
context: "Target: <device/firmware path>. Use binwalk, strings, grep for passwords/keys, check for UART/JTAG references, test diagnostic endpoints, map protocols."
```

**Cloud IAM Agent** (for AWS/cloud privilege targets):
```
goal: "Enumerate IAM permissions on <target>, identify privilege escalation paths, test persistence techniques, check GuardDuty configuration."
skills: ["cloud-iam-attacks", "infrastructure-attacks"]
toolsets: ["terminal", "web"]
context: "Target: <AWS account/credentials>. Enumerate current permissions, map all escalation paths, test persistence, check detection evasion."
```

**Zero-Day Agent** (for code audits):
```
goal: "Audit <repo> for vulnerabilities. Run all SAST tools, manual grep for sinks, CVE-reachability on deps. Classify every finding. Generate PoC for high/critical."
skills: ["exploit-development", "web-attacks", "cve-intelligence"]
toolsets: ["terminal", "file", "web"]
context: "Repo path: <path>. Run semgrep, bandit/gosec, manual sink hunting. Output vulnerability_inventory.json with CWE, severity, file:line, gadget classification."
```

**Chain Synthesis Agent** (ALWAYS dispatch after other agents complete):
```
goal: "Synthesize all findings from the engagement into exploit chains. Compose primitives + amplifiers. Score every chain. Output viable chains to exploit."
skills: ["web-attacks", "exploit-development", "threat-intel"]
toolsets: ["terminal", "file"]
context: "Findings from: <list of agent output files>. Run full §10.2 chain-synthesis protocol. Pair-wise compose, multi-hop expand, score, promote viable chains."
```

**Exploit Agent** (for confirmed findings/chains):
```
goal: "Execute live exploitation against <target> for confirmed findings and chains. Capture blast radius, forensic evidence. Pivot to new targets."
skills: ["exploit-development", "web-attacks", "infrastructure-attacks"]
toolsets: ["terminal", "web"]
context: "Target: <target>. Confirmed findings: <list>. Execute PoC, capture evidence, pivot. Per agent.md §7.4."
```

### Dispatch Rules:
1. Recon ALWAYS runs first — map before hunt
2. Web Vuln + Zero-Day can run in parallel if target has both web + code
3. Chain Synthesis runs AFTER all vuln agents complete — consumes their output
4. Exploit Agent runs AFTER Chain Synthesis promotes chains
5. Report Agent runs last — consumes ALL outputs

---

## PHASE 3: SYNTHESIZE & PROMOTE

After sub-agents complete:

1. **Deduplicate findings** across agents (same bug in different contexts)
2. **Classify every finding**: primitive, amplifier, or both
3. **Run chain-synthesis protocol** (§10.2 in agent.md):
   - List every finding
   - Pair-wise compose (primitive × amplifier)
   - Multi-hop expand (2-hop → 3-hop → 4-hop)
   - Score every candidate chain
   - Promote viable chains to Exploit Agent
4. **Adversarial debate** (§4): prosecutor → defender → verifier
5. **Live exploit** confirmed chains (§7.4)

---

## PHASE 4: POST-EXPLOIT

After successful exploitation:

1. **Pivot**: every exploited target surfaces new targets
   - Dump ARP tables, DNS caches, routing tables
   - Dump credentials, tokens, SSH keys
   - Enumerate domain trusts, cloud accounts
   - Check for lateral movement paths
2. **Persistence**: Sliver implant (default) or Meterpreter
3. **Privesc**: linpeas/winpeas → targeted exploits
4. **Domain escalation**: BloodHound → shortest-path-to-DA
5. **Feed new targets back to PHASE 0** — loop until scope exhausted

---

## PHASE 5: REPORT

Structured markdown report at `~/reports/<target>_<date>/`:

### Report Structure (mandatory):
1. **Executive Summary** (10 lines, decision-grade)
2. **Attack Surface Map** (open ports, services, technologies, endpoints)
3. **Confirmed Findings** — ranked by severity × exploitability × business impact
   - Narrative, reachability proof, PoC, blast radius, remediation
4. **Confirmed Chains** — hop-by-hop diagram, per-hop severity, end-to-end PoC
   - Remediation per hop (any single hop hardened breaks the chain)
5. **MITRE ATT&CK Mapping** — every technique used per finding
6. **Attack Path Graph** — full kill chain across findings + chains + post-exploitation
7. **Coverage Checklist** — every relevant bug class considered, skips explained
8. **Chain Coverage** — which amplifier categories enumerated
9. **Self-Evaluation** — scores per agent.md §14.4
10. **Appendix** — false leads, rejected chains, missing preconditions

---

---

## PHASE 6: WRITE-BACK (MANDATORY)

### RATE LIMITING & IP ROTATION STRATEGY

**Detection**: When all requests to target start timing out (15-20s) or return 403, your IP is rate-limited.

**Bypass techniques (in priority order)**:
1. **Use `web_extract`** — routes through different outbound IP than terminal. Best for intelligence gathering, GET-only requests. Cannot do POST with custom payloads.
2. **Use `execute_code`** — Python requests.Session() may use different network path. Good for POST requests.
3. **Space requests** — 15-20 second delay between terminal curl calls prevents triggering rate limits on most targets.
4. **Rotate User-Agent** — some WAFs key rate limits on User-Agent + IP. Cycle through browser UAs.
5. **Hydra `-W` flag** — longer wait between attempts. `-t 2` to limit concurrent threads.

**Recovery**: Wait 30-60 minutes for automatic unblock. Use web_extract/execute_code as alternate channels. If target is behind aggressive rate limiting (common on budget VPS providers), reduce to 1 request per 15-20 seconds.

### CeWL Wordlist Generation

For targeted password brute force against content-heavy sites:
```bash
cewl -d 2 -m 5 -w /tmp/cewl_words.txt https://target.com/
# -d 2: spider depth 2
# -m 5: minimum word length 5
# Extracts unique words from site content — company names, industry terms, etc.
# Combine with manually crafted permutations for high-yield wordlist
```

### WordPress Brute Force Escalation Ladder

When the admin username is known but password is not, escalate wordlists in phases:

**Phase 1: Short/popular (~50K)** — rockyou short (≤8 chars, top 50K) + CeWL scraped words. Split into 4 chunks, 4 parallel workers. ETA: ~2-4 hours at 1 req/sec per worker.

**Phase 2: Long + targeted mutations (~100K)** — rockyou long (9-16 chars, top 500K) + mutations of targeted words (company name + suffixes: 123, 1234, 2024, 2025, 2026, !, @, #; prefixes: The, My; case variants). Split into 4 chunks per target. ETA: ~3-5 hours.

**Phase 3: Hashcat ruled (~200K+)** — apply hashcat best64.rule to the entire combined wordlist from phases 1+2 (rule appends/prepends digits, substitutes characters, toggles case). This catches `password1`, `Password`, `p@ssword`, `password123`, etc. Split into 8 chunks. ETA: ~4-10 hours depending on rate limits.

**Worker pattern**: Single Python script that takes `(target_url, username, chunk_file, log_file, offset, limit)`. Each worker processes its chunk sequentially, logging progress every 100 attempts. Workers are independent — no coordination needed. On password found, write to shared `/tmp/wp_pass_found.txt` and exit.

**Critical**: Workers must use `--connect-timeout 8 --max-time 12` on curl. 3+ second delay between attempts to avoid IP blocks. If target goes dark (HTTP 000, TCP timeout), workers freeze safely — do NOT kill them, they resume when target returns.

### REST API Namespace Enumeration

When traditional plugin detection fails (readme.txt blocked, no CSS leaks), enumerate all custom plugin REST namespaces:
```bash
curl -sk https://target.com/wp-json/ | jq '.namespaces'
# Reveals hidden plugins: elementor-one, advanced-db-cleaner, mcp, etc.
# Then probe each namespace for available endpoints:
curl -sk https://target.com/wp-json/NAMESPACE/v1 | jq '.routes | keys'
```

### When Every Vector Fails — Escalation Ladder
1. Switch to infrastructure attacks (SMTP, IMAP, SSH, cPanel)
2. Try social engineering vectors (contact forms, job applications)
3. Deploy long-running password brute force with strict rate limiting
4. Search for zero-days in identified software versions

---

## METHODOLOGY LAYER

For validation gates, chain tables, discipline rules, and engagement-mode awareness, load `bughunter-methodology` alongside this skill. The 7-Question Gate replaces ad-hoc finding validation. The A→B chain table (20+ pre-mapped paths) extends the chain synthesis below. The DO NOT STOP directive and mid-engagement IR detection patterns apply to every red-team engagement orchestrated here.

## ARCHITECTURE REFERENCES

- `references/hermes-architecture-offensive.md` — Hermes internals for offensive ops: conversation loop, SOUL.md injection, delegation system, profile isolation, memory lifecycle, extension points, all hard/soft constraints
- `references/openclaw-fusion-concepts.md` — OpenClaw features adoptable via Hermes primitives: subagent spawning, browser automation, Docker sandbox, cron, node host, vector memory

## ADAPTIVE PRIORITY PHILOSOPHY (CRITICAL)

Killer Queen determines the priority order per engagement based on target analysis. No fixed list. No operator-prescribed order. She reads the attack surface, identifies the path of least resistance, and orders vectors by exploitability × impact. She tells the operator what matters — not the reverse.

The adaptive-engagement skill contains the full priority-scoring algorithm, vector selection decision tree, and engagement state machine. Load it alongside this skill for autonomous target-adaptive operation.

**Pitfall**: Using the same priority order across different targets is a failure mode. A WordPress site needs different priorities than a Kubernetes cluster, a mobile app, or a firmware binary. Re-run the scoring algorithm per target.

## CHAIN SYNTHESIS IN ACTION — Generic Template

When decomposing a target, every finding is a primitive. Build the attack graph:

**Step 1 — List primitives**: Every open port, every endpoint, every user enumeration, every file upload, every auth mechanism, every CORS header, every email config, every external service.

**Step 2 — Pair-wise compose**: For every pair of primitives, ask: "Does A amplify B? Does B unlock A?" Document every viable pair.

**Step 3 — Multi-hop expand**: From each pair, extend to 3-hop and 4-hop chains. The killer chain is usually 3-4 steps deep.

**Step 4 — Score and promote**: Score by exploitability × impact. Promote viable chains to exploitation. Attack all viable chains in parallel.

**Lesson**: In any hardened target, all chains converge on a small number of gates (e.g., admin credentials, LFI primitive, SSRF sink). Identify those gates early and attack them from every angle simultaneously.

---

## RATE LIMIT BYPASS METHODOLOGY

When IP gets rate-limited (common on Contabo ~4-5 req/min):
1. **Use `web_extract`** — different outbound IP
2. **Browser tools** — separate IP pool  
3. **Slow brute force** — 15-20s delays between attempts
4. **Rotate vectors** — try SMTP/IMAP/SSH while HTTP blocked
5. **Sub-agents** — may route through different infrastructure

Per agent.md §14.2:

1. **Confirmed findings** → append to `~/knowledge_base/patterns/<class>.md`
2. **Confirmed chains** → append to `~/knowledge_base/chains/<archetype>.md`
3. **New tools forged** → register under `~/forge/`
4. **New bypasses** → append to `~/knowledge_base/bypasses/<system>.md`
5. **False leads** → append to `~/knowledge_base/false-leads.md`
6. **Mission post-mortem** → `~/knowledge_base/missions/<mission-id>.md`

---

## ANTI-STAGNATION CHECK

At mission close, verify:
- Did I use all 8 attack-type skills where relevant?
- Did I run chain synthesis on every informational/low finding?
- Did I check postMessage listeners + cookie scopes on every web app?
- Did I cover every surface from agent.md §8 that's relevant?
- Did I write back to the knowledge base?

If 3+ missions produce no new patterns, flag stagnation per §14.6.

## KNOWLEDGE INGESTION SELF-AUDIT (After Every Source Processing Round)

Before telling the operator "done," run this checklist. The operator should never be your QA:

1. **Source count**: Did I process EVERY URL/source the operator listed? Count them.
2. **Link preservation**: Do my output files have GitHub URLs? `grep -c 'github.com' output.md`
3. **Source code read**: Did I clone and read actual source files? Not just READMEs.
4. **Conversion check**: Is every reference file's knowledge in a skill, SOUL.md, or memory?
5. **On-disk audit**: Are there cloned repos or books on disk I haven't read?
6. **\"Is that everything?\" guard**: If the operator has asked this ONCE this session, run this full checklist before your next response. If they've asked it TWICE, you've missed something major — stop and audit exhaustively before proceeding.

**Pitfall**: Reporting \"done\" when references exist but skills haven't been created/patched. The operator expects knowledge in OPERATIONAL files, not reference archives.

---

## TARGET-SPECIFIC OVERRIDES

**ICS/OT targets**: Default to passive. Active exploits on ICS require operator awareness of plant safety windows.

**Third-party impact**: PoC-level read-only proof (one record, one callback, one hash) is default. Bulk exfiltration, account modification, payment triggers — note risk, then execute per operator command.

**Air-gapped targets**: Build offline payloads, prepare sneakernet delivery. Test on identical lab setup first.

---

## SUPPORT FILES
- `references/demo-acme-corp.md` — Live demonstration: full pipeline on vuln Flask app (deploy→recon→exploit→chain→report in <120s). Lessons learned, what worked, what to improve.
- `references/wordpress-recon-playbook.md` — WordPress-specific recon methodology.
- `references/dnd-upload-cf7-cve-history.md` — Complete 16-CVE timeline for the Drag & Drop CF7 plugin. Version-to-exploit mapping.
- `references/knowledge-ingestion-methodology.md` — Proven workflow for ingesting external knowledge sources (web_extract→synthesize→references). 12 pitfalls documented.
- `references/hackerone-reports-dataset.md` — Permanent knowledge resource: 15 categorized top-100 H1 report lists (561KB, 500+ reports). RCE, SSRF, SQLi, IDOR, XSS, Account Takeover, Race Conditions, OAuth, Request Smuggling, XXE, Web Cache, SSTI, File Upload. Load before any web bug bounty engagement for pattern extraction.

## COMPANION SKILLS
- **adaptive-engagement** — Priority-scoring algorithm, vector selection decision tree, engagement state machine, target fingerprinting. Load for autonomous target-adaptive operation.
- **self-improvement** — After-action review, automated skill creation, lesson extraction, memory curation, capability gap detection. Load after every engagement to compound knowledge.
