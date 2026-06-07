"""Phase 3: report generation (no-exploit-no-report, mermaid) + DAG cycle handling."""
from kq_core import diagram, engagement, findings, report, triage

_ALL_YES = {f"q{i}": True for i in range(1, 8)}


def test_report_html_no_exploit_no_report(store, tmp_path):
    e = engagement.start(store, "acme", "red_team", in_scope=["*.example.com"])
    eid = e["engagement_id"]
    f1 = findings.finding_save(store, eid, "ssrf", "high", "api.example.com")["finding_id"]
    f2 = findings.finding_save(store, eid, "xss", "medium", "app.example.com")["finding_id"]
    triage.triage_finding(store, f1, _ALL_YES)               # -> validated
    triage.triage_finding(store, f2, {**_ALL_YES, "q1": False})  # -> invalid

    res = report.generate(store, eid, fmt="html")
    assert res["reportable"] == 1 and res["excluded"] == 1
    html = open(res["path"], encoding="utf-8").read()
    assert 'class="mermaid"' in html
    assert "ssrf" in html and "xss" not in html  # only validated finding shown

    md = report.generate(store, eid, fmt="md")
    assert md["path"].endswith(".md")
    assert "```mermaid" in open(md["path"], encoding="utf-8").read()


def test_report_includes_unvalidated_when_asked(store):
    e = engagement.start(store, "acme2", "red_team", in_scope=["*.example.com"])
    eid = e["engagement_id"]
    findings.finding_save(store, eid, "idor", "high", "api.example.com")  # stays candidate
    res = report.generate(store, eid, fmt="html", include_unvalidated=True)
    assert res["reportable"] == 1


def test_diagram_is_acyclic():
    kept = diagram._drop_cycles([("1", "2"), ("2", "3"), ("3", "1")])
    assert ("3", "1") not in kept and len(kept) == 2
    mm = diagram.mermaid_chain("acme", [{"id": 1, "vuln_class": "ssrf", "severity": "high", "target": "a.example.com"}],
                               [{"hops": [1], "severity": "high"}])
    assert mm.startswith("flowchart LR") and "F1" in mm
