"""Persistent attack-chain graph (CyberStrikeAI node/edge model) + the runtime DAG cycle
check their code lacked. Nodes: target | action | vulnerability. Edges: leads_to |
discovers | enables | depends_on. Assembled from findings; feeds the report diagram.
"""
from __future__ import annotations

import json
from typing import Any, Optional, Tuple

from .diagram import _reachable
from .util import now_iso

_RISK = {"critical": 90, "high": 80, "medium": 60, "low": 40, "info": 20}


def risk_of_severity(sev: Optional[str]) -> int:
    return _RISK.get((sev or "info").lower(), 20)


def _find_node(store: Any, eid: int, node_type: str, ref_id: Optional[int], label: str) -> Optional[int]:
    if ref_id is not None:
        row = store.query_one(
            "SELECT id FROM chain_nodes WHERE engagement_id=? AND node_type=? AND ref_id=?",
            (eid, node_type, ref_id))
    else:
        row = store.query_one(
            "SELECT id FROM chain_nodes WHERE engagement_id=? AND node_type=? AND label=? AND ref_id IS NULL",
            (eid, node_type, label))
    return int(row["id"]) if row else None


def add_node(store: Any, engagement_id: int, node_type: str, label: str,
             ref_id: Optional[int] = None, risk_score: int = 0, metadata: Optional[dict] = None) -> dict:
    existing = _find_node(store, engagement_id, node_type, ref_id, label)
    if existing:
        return {"ok": True, "node_id": existing, "action": "exists"}
    cur = store.execute(
        "INSERT INTO chain_nodes(engagement_id, node_type, label, ref_id, risk_score, metadata, created_at) "
        "VALUES (?,?,?,?,?,?,?)",
        (engagement_id, node_type, label, ref_id, int(risk_score), json.dumps(metadata or {}), now_iso()))
    return {"ok": True, "node_id": int(cur.lastrowid), "action": "inserted"}


def _edges(store: Any, eid: int) -> list[Tuple[int, int]]:
    return [(int(r["source_id"]), int(r["target_id"]))
            for r in store.query("SELECT source_id, target_id FROM chain_edges WHERE engagement_id=?", (eid,))]


def _would_cycle(edges: list[Tuple[int, int]], a: int, b: int) -> bool:
    if a == b:
        return True
    adj: dict = {}
    for s, t in edges:
        adj.setdefault(s, set()).add(t)
    return _reachable(adj, b, a)  # b already reaches a -> a->b closes a loop


def add_edge(store: Any, engagement_id: int, source_id: int, target_id: int,
             edge_type: str = "leads_to", weight: int = 3) -> dict:
    for nid in (source_id, target_id):
        if not store.query_one("SELECT 1 FROM chain_nodes WHERE id=? AND engagement_id=?", (nid, engagement_id)):
            return {"ok": False, "error": f"node {nid} not in engagement {engagement_id}"}
    if _would_cycle(_edges(store, engagement_id), source_id, target_id):
        return {"ok": False, "error": "edge would create a cycle (the chain graph must stay a DAG)"}
    cur = store.execute(
        "INSERT OR IGNORE INTO chain_edges(engagement_id, source_id, target_id, edge_type, weight, created_at) "
        "VALUES (?,?,?,?,?,?)",
        (engagement_id, source_id, target_id, edge_type, int(weight), now_iso()))
    return {"ok": True, "edge_id": int(cur.lastrowid) or None}


def _ensure_finding_node(store: Any, eid: int, finding_id: int) -> Optional[int]:
    f = store.query_one("SELECT id, vuln_class, severity, target FROM findings WHERE id=? AND engagement_id=?",
                        (finding_id, eid))
    if not f:
        return None
    return add_node(store, eid, "vulnerability", f"{f['vuln_class']} @ {f['target']}",
                    ref_id=int(f["id"]), risk_score=risk_of_severity(f["severity"]))["node_id"]


def link_findings(store: Any, engagement_id: int, source_finding_id: int, target_finding_id: int,
                  edge_type: str = "enables") -> dict:
    src = _ensure_finding_node(store, engagement_id, source_finding_id)
    dst = _ensure_finding_node(store, engagement_id, target_finding_id)
    if not src or not dst:
        return {"ok": False, "error": "finding(s) not found in this engagement"}
    return add_edge(store, engagement_id, src, dst, edge_type)


def assemble_from_findings(store: Any, engagement_id: int,
                           statuses: Tuple[str, ...] = ("validated", "reported")) -> dict:
    eng = store.query_one("SELECT name FROM engagements WHERE id=?", (engagement_id,))
    target_node = add_node(store, engagement_id, "target", eng["name"] if eng else "target")["node_id"]
    rows = store.query(
        "SELECT id, vuln_class, severity, target FROM findings WHERE engagement_id=? AND status IN (%s)"
        % ",".join("?" * len(statuses)),
        (engagement_id, *statuses))
    n = 0
    for f in rows:
        nid = add_node(store, engagement_id, "vulnerability", f"{f['vuln_class']} @ {f['target']}",
                       ref_id=int(f["id"]), risk_score=risk_of_severity(f["severity"]))["node_id"]
        add_edge(store, engagement_id, target_node, nid, "discovers")
        n += 1
    # Import operator-asserted chains (engagement_state.chain_candidates: [{hops:[finding_id...]}]).
    st = store.query_one("SELECT chain_candidates FROM engagement_state WHERE engagement_id=?", (engagement_id,))
    linked = 0
    if st:
        try:
            chains = json.loads(st["chain_candidates"])
        except (TypeError, ValueError):
            chains = []
        for ch in chains:
            hops = ch.get("hops", []) if isinstance(ch, dict) else []
            for a, b in zip(hops, hops[1:]):
                r = link_findings(store, engagement_id, a, b, "enables")
                if r.get("ok"):
                    linked += 1
    return {"ok": True, "target_node": target_node, "vuln_nodes": n, "chain_edges": linked}


def get_chain(store: Any, engagement_id: int) -> dict:
    nodes = [dict(r) for r in store.query(
        "SELECT id, node_type, label, ref_id, risk_score FROM chain_nodes WHERE engagement_id=? ORDER BY id",
        (engagement_id,))]
    edges = [dict(r) for r in store.query(
        "SELECT source_id, target_id, edge_type, weight FROM chain_edges WHERE engagement_id=? ORDER BY id",
        (engagement_id,))]
    critical = [n["label"] for n in nodes if n["node_type"] == "vulnerability" and n["risk_score"] >= 80]
    return {"ok": True, "nodes": nodes, "edges": edges, "node_count": len(nodes),
            "edge_count": len(edges), "critical_nodes": critical}
