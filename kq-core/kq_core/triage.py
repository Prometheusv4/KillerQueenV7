"""Finding triage — BugHunter's 7-question gate + Never-Submit list + CVSS helper.

The agent reasons out the seven yes/no answers; this module turns them into a DETERMINISTIC
verdict (PASS / DOWNGRADE / CHAIN / KILL) and applies it to the finding (lifecycle status).
This is what keeps invalid/duplicate noise out of reports.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

SEVEN_QUESTIONS = [
    ("q1", "Can I demonstrate this with a real HTTP request RIGHT NOW?"),
    ("q2", "Is this impact type accepted by the program?"),
    ("q3", "Is the vulnerable asset owned by and in scope for the program?"),
    ("q4", "Does this work WITHOUT admin/privileged access?"),
    ("q5", "Is this NOT already known/disclosed/documented behavior?"),
    ("q6", "Can I prove impact beyond 'technically possible'?"),
    ("q7", "Is this NOT on the never-submit list?"),
]

NEVER_SUBMIT = [
    "missing security header", "missing header", "self-xss", "self xss",
    "open redirect alone", "ssrf dns-only", "ssrf dns only", "blind ssrf no data",
    "rate limit on non-sensitive", "admin can do", "could theoretically",
    "logout csrf", "mixed content", "clickjacking non-sensitive", "clickjacking on non-sensitive",
    "banner disclosure", "version disclosure alone", "introspection only", "missing dmarc",
]

# (vector, base score, severity) presets — BugHunter's quick reference.
CVSS_PRESETS = {
    "idor_read_pii": ("AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N", 6.5, "Medium"),
    "auth_bypass_admin": ("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", 9.8, "Critical"),
    "ssrf_metadata": ("AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N", 9.1, "Critical"),
    "stored_xss": ("AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N", 8.2, "High"),
}

DISCIPLINE_RULES = [
    "Marker discipline: use an 8+ char unique non-English marker for reflection/SSRF (no dictionary words).",
    "Body-diff rule: a bypass claim needs a response BODY diff, not just a status-code change.",
    "Statistical-sample rule: timing claims need n>=10 interleaved trials and a 2-sigma separation.",
    "Multi-tool reproduction: Critical/High must reproduce via TWO independent tools (e.g. curl + Burp).",
    "OOB-or-it-didn't-happen: blind SSRF/RCE/XXE require an out-of-band callback (interactsh/Collaborator).",
]


def never_submit_match(text: str) -> Optional[str]:
    low = (text or "").lower()
    for pat in NEVER_SUBMIT:
        if pat in low:
            return pat
    return None


def severity_band(score: float) -> str:
    if score >= 9.0:
        return "critical"
    if score >= 7.0:
        return "high"
    if score >= 4.0:
        return "medium"
    if score > 0.0:
        return "low"
    return "info"


def cvss_lookup(preset: str) -> Optional[dict]:
    v = CVSS_PRESETS.get(preset)
    if not v:
        return None
    return {"preset": preset, "vector": v[0], "score": v[1], "severity": v[2]}


def gate(answers: Dict[str, bool], chainable: bool = False) -> dict:
    """Apply the 7-question gate. answers: {'q1'..'q7': bool}. Returns the verdict."""
    a = {k: bool(answers.get(k, False)) for k, _ in SEVEN_QUESTIONS}
    failed = [k for k, _ in SEVEN_QUESTIONS if not a[k]]

    # First NO (in order) decides — mirrors the BugHunter gate.
    for k in ("q1", "q2", "q3", "q4", "q5"):
        if not a[k]:
            return {"verdict": "KILL", "failed": failed, "reason": _q(k) + " -> KILL"}
    if not a["q6"]:
        return {"verdict": "DOWNGRADE", "failed": failed,
                "reason": "Only 'technically possible' (Q6 no) -> DOWNGRADE; prove concrete impact or lower severity."}
    if not a["q7"]:
        if chainable:
            return {"verdict": "CHAIN", "failed": failed,
                    "reason": "On never-submit list but chainable -> report the CHAIN, not the primitive alone."}
        return {"verdict": "KILL", "failed": failed,
                "reason": "On never-submit list and not chainable -> KILL."}
    return {"verdict": "PASS", "failed": [], "reason": "All seven gates passed."}


def _q(key: str) -> str:
    return dict(SEVEN_QUESTIONS).get(key, key)


def triage_finding(store: Any, finding_id: int, answers: Dict[str, bool], chainable: bool = False) -> dict:
    """Run the gate and apply the lifecycle status to the finding."""
    from . import findings as _findings

    row = store.query_one("SELECT id, vuln_class, severity FROM findings WHERE id=?", (finding_id,))
    if row is None:
        return {"ok": False, "error": f"finding {finding_id} not found"}
    result = gate(answers, chainable=chainable)
    status_map = {"PASS": "validated", "KILL": "invalid", "CHAIN": "candidate", "DOWNGRADE": "candidate"}
    patch = {"status": status_map[result["verdict"]]}
    if result["verdict"] == "DOWNGRADE":
        patch["severity"] = "low"
    _findings.finding_update(store, finding_id, patch)
    result.update({"ok": True, "finding_id": finding_id, "applied_status": patch["status"]})
    return result
