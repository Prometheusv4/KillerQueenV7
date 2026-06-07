"""Phase plan (Shannon-style, resumable) + per-role retrieval briefs.

The agent runs the multi-agent fan-out itself via Hermes delegate_task (sub-agents
inherit the mcp_kq_* tools). This module gives that orchestration a DETERMINISTIC
substrate: a dependency-ordered task plan it can resume, and a role_brief that bundles
exactly the scope + curated patterns + learned lessons + recommended tools + memory facts
a delegated sub-agent needs for its role.

v6.1: Expanded from 13 web-only tasks to 36 tasks across 8 attack domains:
  web, cloud, ad, malware, embedded, wireless, social, post-exploitation.
"""

from __future__ import annotations

from typing import Any, Optional

from .util import now_iso
from . import engagement

# ═══════════════════════════════════════════════════════════════
# PHASE PLAN — DETERMINISTIC TASK TREE
# ═══════════════════════════════════════════════════════════════
# Format: (phase, role, comma-separated-role-prerequisites)
#
# Domains:
#   web:     pre-recon → recon → injection|xss|auth|authz|ssrf|upload|deser|ssti|xxe|smuggling
#   cloud:   pre-recon → recon-cloud → cloud-iam
#   ad:      pre-recon → recon-ad → ad-attack
#   malware: pre-recon → recon → malware-dev
#   embed:   pre-recon → recon → embedded-exploit
#   wireless: pre-recon → recon → wireless-attack
#   social:  pre-recon → recon → social-eng
#   postex:  lateral-movement → persistence → exfiltration
# All converge → report

PHASE_PLAN = [
    # ── Reconnaissance phase ──────────────────────────────────
    ("pre-recon",  "pre-recon",       ""),
    ("recon",      "recon",           "pre-recon"),
    ("recon",      "recon-cloud",     "pre-recon"),
    ("recon",      "recon-ad",        "pre-recon"),
    ("recon",      "recon-wireless",  "pre-recon"),

    # ── Web vulnerability discovery (parallel) ───────────────
    ("vuln",       "injection",       "recon"),
    ("vuln",       "xss",             "recon"),
    ("vuln",       "auth",            "recon"),
    ("vuln",       "authz",           "recon"),
    ("vuln",       "ssrf",            "recon"),
    ("vuln",       "file-upload",     "recon"),
    ("vuln",       "deserialization", "recon"),
    ("vuln",       "ssti",            "recon"),
    ("vuln",       "xxe",             "recon"),
    ("vuln",       "http-smuggling",  "recon"),

    # ── Web exploitation (parallel, each depends on its vuln) ─
    ("exploit",    "exploit-injection",   "injection"),
    ("exploit",    "exploit-xss",         "xss"),
    ("exploit",    "exploit-auth",        "auth"),
    ("exploit",    "exploit-authz",       "authz"),
    ("exploit",    "exploit-ssrf",        "ssrf"),
    ("exploit",    "exploit-upload",      "file-upload"),
    ("exploit",    "exploit-deser",       "deserialization"),
    ("exploit",    "exploit-ssti",        "ssti"),
    ("exploit",    "exploit-xxe",         "xxe"),
    ("exploit",    "exploit-smuggling",   "http-smuggling"),

    # ── Cloud attack branch ───────────────────────────────────
    ("vuln",       "cloud-iam",        "recon-cloud"),
    ("exploit",    "exploit-cloud",    "cloud-iam"),

    # ── Active Directory attack branch ────────────────────────
    ("vuln",       "ad-attack",        "recon-ad"),
    ("exploit",    "exploit-ad",       "ad-attack"),

    # ── Malware development branch ────────────────────────────
    ("vuln",       "malware-dev",      "recon"),
    ("exploit",    "exploit-malware",  "malware-dev"),

    # ── Embedded/IoT branch ─────────────────────────────────
    ("vuln",       "embedded-exploit", "recon"),
    ("exploit",    "exploit-embedded", "embedded-exploit"),

    # ── Wireless/RF branch ───────────────────────────────────
    ("vuln",       "wireless-attack",  "recon-wireless"),
    ("exploit",    "exploit-wireless", "wireless-attack"),

    # ── Social engineering branch ─────────────────────────────
    ("vuln",       "social-eng",       "recon"),
    ("exploit",    "exploit-social",   "social-eng"),

    # ── Post-exploitation (sequential chain) ──────────────────
    ("postex",     "lateral-movement",
     "exploit-ad,exploit-cloud,exploit-injection,exploit-ssrf"),
    ("postex",     "persistence",      "lateral-movement"),
    ("postex",     "exfiltration",     "persistence"),

    # ── Reporting ─────────────────────────────────────────────
    ("report",     "report",
     "exploit-injection,exploit-xss,exploit-auth,exploit-authz,"
     "exploit-ssrf,exploit-upload,exploit-deser,exploit-ssti,"
     "exploit-xxe,exploit-smuggling,exploit-cloud,exploit-ad,"
     "exploit-malware,exploit-embedded,exploit-wireless,"
     "exploit-social,exfiltration"),
]

# ═══════════════════════════════════════════════════════════════
# ROLE QUERY MAP — semantic queries for recall + kb_search
# ═══════════════════════════════════════════════════════════════

ROLE_QUERY = {
    # ── Recon ─────────────────────────────────────────────────
    "pre-recon": (
        "source code review attack surface architecture technology stack"
    ),
    "recon": (
        "reconnaissance subdomain enumeration attack surface mapping "
        "port scanning service discovery technology fingerprinting"
    ),
    "recon-cloud": (
        "cloud enumeration aws azure gcp infrastructure discovery "
        "s3 buckets iam roles lambda functions cloudfront distributions"
    ),
    "recon-ad": (
        "active directory enumeration domain controllers ldap smb shares "
        "kerberos spn user enumeration group policy bloodhound collection"
    ),
    "recon-wireless": (
        "wireless reconnaissance wifi networks bluetooth devices "
        "rf signals nfc readers iot beacons signal analysis"
    ),

    # ── Web vulns ─────────────────────────────────────────────
    "injection": (
        "sql injection command injection nosql injection ldap injection "
        "xpath injection payloads union select blind error based bypass"
    ),
    "xss": (
        "cross site scripting stored reflected dom mutation xss "
        "payloads filter bypass csp bypass trusted types bypass"
    ),
    "auth": (
        "authentication bypass jwt oauth saml session fixation "
        "mfa bypass password reset brute force token manipulation"
    ),
    "authz": (
        "idor broken access control authorization privilege escalation "
        "horizontal vertical forcible browsing parameter manipulation"
    ),
    "ssrf": (
        "server side request forgery cloud metadata imds bypass "
        "blind ssrf url parser bypass protocols dns rebinding"
    ),
    "file-upload": (
        "unrestricted file upload extension bypass polyglot magic bytes "
        "content type php asp jsp webshell exif race condition"
    ),
    "deserialization": (
        "insecure deserialization php python java net yaml pickle marshal "
        "gadget chain ysoserial phpggc type confusion"
    ),
    "ssti": (
        "server side template injection jinja2 twig freemarker velocity "
        "smarty pug rce sandbox escape filter bypass"
    ),
    "xxe": (
        "xml external entity xinclude out of band parameter entities "
        "blind xxe error based dtd file read ssrf via xxe"
    ),
    "http-smuggling": (
        "request smuggling cl.te te.cl te.te h2 desync transfer encoding "
        "content length pingora downgrade response queue poisoning"
    ),

    # ── Cloud ─────────────────────────────────────────────────
    "cloud-iam": (
        "aws iam privilege escalation assume role passrole putuserpolicy "
        "attachuserpolicy enumeration pacu pmapper lambda rolesanywhere "
        "guardduty evasion cloudtrail sabotage"
    ),

    # ── AD ────────────────────────────────────────────────────
    "ad-attack": (
        "kerberoasting asreproasting dacl abuse bloodhound dcsync "
        "golden ticket silver ticket bronze bit s4u2self s4u2proxy "
        "delegation abuse adcs certificate services ntlm relay coercion"
    ),

    # ── Malware ───────────────────────────────────────────────
    "malware-dev": (
        "shellcode payload generation process injection dll hijacking "
        "syscall evasion amsi bypass defender bypass edr evasion "
        "sandbox detection rat builder c2 framework persistence"
    ),

    # ── Embedded ──────────────────────────────────────────────
    "embedded-exploit": (
        "firmware extraction binwalk uart jtag spi flash iot device "
        "uefi secure boot bootkit ics scada modbus plc exploitation "
        "bus pirate logic analyzer"
    ),

    # ── Wireless ──────────────────────────────────────────────
    "wireless-attack": (
        "wpa2 wpa3 wifi cracking handshake capture evil twin rogue ap "
        "rf sdr hackrf rtl-sdr ble bluetooth nfc rfid proxmark rolljam"
    ),

    # ── Social ────────────────────────────────────────────────
    "social-eng": (
        "phishing spearphishing credential harvesting evilginx modlishka "
        "mfa bypass vishing smishing social engineering toolkit pretext"
    ),

    # ── Post-exploitation ─────────────────────────────────────
    "lateral-movement": (
        "pass the hash psexec wmiexec smbexec rdp ssh lateral movement "
        "pivot proxychains port forwarding double hop relay"
    ),
    "persistence": (
        "scheduled tasks wmi registry run keys startup folder dll hijacking "
        "webshell service creation golden ticket skeleton key shadow credentials"
    ),
    "exfiltration": (
        "dns tunneling icmp exfiltration http data staging encrypted channel "
        "cloud storage exfil dropbox gdrive onedrive steganography"
    ),

    # ── Report ────────────────────────────────────────────────
    "report": (
        "reporting evidence hygiene severity cvss proof of concept "
        "chain diagram mermaid executive summary remediation"
    ),
}

# ═══════════════════════════════════════════════════════════════
# ROLE → VULN CLASS MAP
# ═══════════════════════════════════════════════════════════════

ROLE_VULN_CLASS = {
    "xss": "xss",
    "ssrf": "ssrf",
    "authz": "idor",
    "file-upload": "file-upload",
    "deserialization": "deserialization",
    "ssti": "ssti",
    "xxe": "xxe",
    "http-smuggling": "http-smuggling",
    "injection": "sqli",
    "cloud-iam": "cloud-iam",
    "ad-attack": "ad-attack",
    "malware-dev": "malware-dev",
    "embedded-exploit": "embedded",
    "wireless-attack": "wireless",
    "social-eng": "social-eng",
    "lateral-movement": "lateral-movement",
    "persistence": "persistence",
    "exfiltration": "exfiltration",
}


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def _base_role(role: str) -> str:
    """Map exploit roles to their vuln role for query lookup."""
    if role.startswith("exploit-"):
        stripped = role[len("exploit-"):]
        # Map exploit shortcuts to full vuln role names
        exploit_map = {
            "injection": "injection",
            "xss": "xss",
            "auth": "auth",
            "authz": "authz",
            "ssrf": "ssrf",
            "upload": "file-upload",
            "deser": "deserialization",
            "ssti": "ssti",
            "xxe": "xxe",
            "smuggling": "http-smuggling",
            "cloud": "cloud-iam",
            "ad": "ad-attack",
            "malware": "malware-dev",
            "embedded": "embedded-exploit",
            "wireless": "wireless-attack",
            "social": "social-eng",
        }
        return exploit_map.get(stripped, stripped)
    return role


# ═══════════════════════════════════════════════════════════════
# PLAN CREATE + STATUS
# ═══════════════════════════════════════════════════════════════

def plan_create(store: Any, engagement_id: int) -> dict:
    """Seed the phase plan (idempotent — re-running returns current status)."""
    existing = store.query_one(
        "SELECT COUNT(*) AS c FROM plan_tasks WHERE engagement_id=?",
        (engagement_id,)
    )
    if existing and int(existing["c"]) > 0:
        return plan_status(store, engagement_id)
    ts = now_iso()
    with store.lock:
        for phase, role, deps in PHASE_PLAN:
            store.conn.execute(
                "INSERT OR IGNORE INTO plan_tasks"
                "(engagement_id, phase, role, depends_on, status, created_at, updated_at) "
                "VALUES (?,?,?,?, 'pending', ?, ?)",
                (engagement_id, phase, role, deps, ts, ts))
        store.conn.commit()
    return plan_status(store, engagement_id)


def plan_status(store: Any, engagement_id: int) -> dict:
    tasks = store.query(
        "SELECT * FROM plan_tasks WHERE engagement_id=? ORDER BY phase, role",
        (engagement_id,)
    )
    all_tasks = [dict(t) for t in tasks]
    pending = [t for t in all_tasks if t["status"] == "pending"]
    running = [t for t in all_tasks if t["status"] == "running"]
    done = [t for t in all_tasks if t["status"] in ("done", "skipped")]

    # Find tasks whose prerequisites are all done/skipped
    runnable = []
    done_roles = {t["role"] for t in done}
    for t in pending:
        deps = [d.strip() for d in t["depends_on"].split(",") if d.strip()]
        if all(d in done_roles for d in deps):
            runnable.append(t)

    return {
        "ok": True,
        "engagement_id": engagement_id,
        "total": len(all_tasks),
        "pending": len(pending),
        "running": len(running),
        "done": len(done),
        "runnable_now": [t["role"] for t in runnable],
        "tasks": all_tasks,
    }


def task_update(
    store: Any,
    engagement_id: int,
    task_id: int,
    status: str,
    result_ref: str = "",
) -> dict:
    ts = now_iso()
    store.execute(
        "UPDATE plan_tasks SET status=?, result_ref=?, updated_at=? "
        "WHERE id=? AND engagement_id=?",
        (status, result_ref or None, ts, task_id, engagement_id)
    )
    return plan_status(store, engagement_id)


# ═══════════════════════════════════════════════════════════════
# ROLE BRIEF — THE CORE ORCHESTRATION INTELLIGENCE
# ═══════════════════════════════════════════════════════════════

def role_brief(
    store: Any,
    role: str,
    target: str = "",
    engagement_id: Optional[int] = None,
) -> dict:
    """Build a comprehensive brief for a delegated sub-agent.

    Bundles:
      1. Scope constraints (from engagement)
      2. Curated hunt patterns (from kb_search)
      3. Active learned lessons (from recall — auto-surfaced)
      4. Recommended tools (from arsenal)
      5. Memory facts (tool quirks, pitfalls, bypasses)
      6. Methodology guidance

    Returns ALL context the sub-agent needs — no additional KB lookups required.
    """
    base = _base_role(role)
    query = ROLE_QUERY.get(base, base)
    vuln_class = ROLE_VULN_CLASS.get(base, "")

    # 1. Scope
    scope = {}
    if engagement_id:
        eng = engagement.state_get(store, engagement_id)
        scope = {
            "in_scope": eng.get("in_scope", []),
            "out_scope": eng.get("out_scope", []),
        }

    # 2. Hunt patterns from knowledge base
    patterns = []
    try:
        kb_patterns = store.kb_search(
            query,
            collection="kq_skill",
            vuln_class=vuln_class or None,
            top_k=3,
        )
        patterns = [p.get("content", "")[:500] for p in kb_patterns]
    except Exception:
        pass  # kb_search may not have results for this domain yet

    # 3. Active learned lessons (auto-surfaced from extraction)
    lessons = []
    try:
        lessons_raw = store.recall(
            query,
            vuln_class=vuln_class or None,
            target_fingerprint=target or None,
            min_confidence=0.5,
            top_k=8,
        )
        lessons = [dict(l) for l in lessons_raw]
    except Exception:
        pass

    # 4. Recommended tools
    tools = []
    if target:
        try:
            from .arsenal.runner import profile_target, recommend
            prof = profile_target(target)
            recs = recommend(prof, "comprehensive")
            tools = [{"name": t.name, "note": t.note} for t in recs[:6]]
        except Exception:
            pass

    # 5. Memory facts for this domain
    facts = []
    if vuln_class:
        try:
            facts_raw = store.query(
                "SELECT content, kind FROM memory_facts "
                "WHERE status='active' AND content LIKE ? "
                "ORDER BY updated_at DESC LIMIT 8",
                (f"%{vuln_class}%",)
            )
            facts = [dict(f) for f in facts_raw]
        except Exception:
            pass
    if not facts and base:
        try:
            facts_raw2 = store.query(
                "SELECT content, kind FROM memory_facts "
                "WHERE status='active' AND content LIKE ? "
                "ORDER BY updated_at DESC LIMIT 8",
                (f"%{base.replace('-', ' ')}%",)
            )
            facts = [dict(f) for f in facts_raw2]
        except Exception:
            pass

    # 6. Methodology guidance
    method = []
    try:
        method = store.kb_search(
            base.replace("-", " "),
            collection="kq_reference",
            top_k=2,
        )
    except Exception:
        pass

    brief = {
        "ok": True,
        "role": role,
        "base_role": base,
        "vuln_class": vuln_class,
        "scope": scope,
        "hunt_patterns": patterns,
        "learned_lessons": [
            {
                "summary": l.get("summary", ""),
                "confidence": l.get("confidence", 0),
                "trigger": l.get("trigger_when", ""),
                "action": l.get("action_do", ""),
            }
            for l in lessons
        ],
        "recommended_tools": tools,
        "memory_facts": [
            {"content": f.get("content", ""), "kind": f.get("kind", "")}
            for f in facts
        ],
        "methodology": [m.get("content", "")[:300] for m in method],
        "instructions": (
            f"You are delegated as the {role} specialist. "
            f"Use the learned_lessons and hunt_patterns above as your starting playbook. "
            f"Call mcp_kq_recall() with the target fingerprint to surface additional "
            f"relevant techniques from memory. "
            f"Execute recommended tools with mcp_kq_arsenal_recommend + mcp_kq_run. "
            f"Save findings via mcp_kq_finding_save. "
            f"Save new lessons via mcp_kq_lesson_save when you discover something "
            f"not already in the knowledge base. "
            f"Chain findings together via mcp_kq_chain_link."
        ),
    }

    return brief
