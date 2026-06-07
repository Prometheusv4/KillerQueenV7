"""Phase 4: attack-chain graph — DAG enforcement, assembly from findings, linking."""
from kq_core import chain, engagement, findings, triage

_ALL_YES = {f"q{i}": True for i in range(1, 8)}


def test_chain_dag_rejects_cycle(store):
    eid = engagement.start(store, "t", "red_team")["engagement_id"]
    a = chain.add_node(store, eid, "action", "a")["node_id"]
    b = chain.add_node(store, eid, "action", "b")["node_id"]
    c = chain.add_node(store, eid, "action", "c")["node_id"]
    assert chain.add_edge(store, eid, a, b)["ok"]
    assert chain.add_edge(store, eid, b, c)["ok"]
    assert chain.add_edge(store, eid, c, a)["ok"] is False   # would close a loop
    assert chain.add_edge(store, eid, a, a)["ok"] is False   # self-loop


def test_assemble_from_findings(store):
    eid = engagement.start(store, "acme", "red_team", in_scope=["*.example.com"])["engagement_id"]
    f1 = findings.finding_save(store, eid, "ssrf", "critical", "api.example.com")["finding_id"]
    f2 = findings.finding_save(store, eid, "idor", "high", "app.example.com")["finding_id"]
    triage.triage_finding(store, f1, _ALL_YES)
    triage.triage_finding(store, f2, _ALL_YES)
    res = chain.assemble_from_findings(store, eid)
    assert res["vuln_nodes"] == 2
    g = chain.get_chain(store, eid)
    assert g["node_count"] == 3 and g["edge_count"] == 2     # target + 2 vulns, 2 discovers
    assert any("ssrf" in c for c in g["critical_nodes"])     # severity critical -> risk 90
    # idempotent assemble doesn't duplicate
    chain.assemble_from_findings(store, eid)
    assert chain.get_chain(store, eid)["node_count"] == 3


def test_link_findings_cycle_guard(store):
    eid = engagement.start(store, "t2", "red_team", in_scope=["*.example.com"])["engagement_id"]
    f1 = findings.finding_save(store, eid, "ssrf", "high", "a.example.com")["finding_id"]
    f2 = findings.finding_save(store, eid, "rce", "critical", "a.example.com")["finding_id"]
    assert chain.link_findings(store, eid, f1, f2, "enables")["ok"]
    assert chain.link_findings(store, eid, f2, f1, "enables")["ok"] is False  # reverse = cycle


def test_chain_candidate_import(store):
    eid = engagement.start(store, "t3", "red_team", in_scope=["*.example.com"])["engagement_id"]
    f1 = findings.finding_save(store, eid, "ssrf", "high", "a.example.com")["finding_id"]
    f2 = findings.finding_save(store, eid, "rce", "critical", "a.example.com")["finding_id"]
    triage.triage_finding(store, f1, _ALL_YES)
    triage.triage_finding(store, f2, _ALL_YES)
    engagement.state_update(store, eid, {"chain_candidates": [{"hops": [f1, f2]}]})
    res = chain.assemble_from_findings(store, eid)
    assert res["chain_edges"] >= 1
