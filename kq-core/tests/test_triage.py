"""Phase 3: triage gate verdicts, never-submit, CVSS, and finding application."""
from kq_core import engagement, findings, triage

_ALL_YES = {f"q{i}": True for i in range(1, 8)}


def test_gate_outcomes():
    assert triage.gate(_ALL_YES)["verdict"] == "PASS"
    assert triage.gate({**_ALL_YES, "q1": False})["verdict"] == "KILL"
    assert triage.gate({**_ALL_YES, "q3": False})["verdict"] == "KILL"
    assert triage.gate({**_ALL_YES, "q6": False})["verdict"] == "DOWNGRADE"
    assert triage.gate({**_ALL_YES, "q7": False}, chainable=True)["verdict"] == "CHAIN"
    assert triage.gate({**_ALL_YES, "q7": False}, chainable=False)["verdict"] == "KILL"


def test_never_submit_and_cvss():
    assert triage.never_submit_match("just a missing security header here")
    assert triage.never_submit_match("a real blind sqli with data") is None
    assert triage.cvss_lookup("auth_bypass_admin")["score"] == 9.8
    assert triage.severity_band(9.1) == "critical"
    assert triage.severity_band(7.5) == "high"
    assert triage.severity_band(0.0) == "info"


def test_triage_finding_applies_status(store):
    e = engagement.start(store, "t", "red_team", in_scope=["*.example.com"])
    eid = e["engagement_id"]
    f1 = findings.finding_save(store, eid, "ssrf", "high", "api.example.com")["finding_id"]
    f2 = findings.finding_save(store, eid, "xss", "medium", "app.example.com")["finding_id"]

    r1 = triage.triage_finding(store, f1, _ALL_YES)
    assert r1["verdict"] == "PASS" and r1["applied_status"] == "validated"
    assert store.query_one("SELECT status FROM findings WHERE id=?", (f1,))["status"] == "validated"

    r2 = triage.triage_finding(store, f2, {**_ALL_YES, "q1": False})
    assert r2["verdict"] == "KILL" and r2["applied_status"] == "invalid"
