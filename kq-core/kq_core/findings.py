"""Findings store: lifecycle ``status`` + exploitation ``verdict`` (two orthogonal axes).

``finding_save`` *internally* runs the scope guard so the safety invariant holds even if
the agent forgets the explicit ``scope_check`` call: an out-of-scope target is forced to
``status='invalid'`` and the caller is told to drop it.
"""
from __future__ import annotations

from typing import Any, Optional

from . import scope as _scope
from .util import now_iso

_SEVERITIES = {"info", "low", "medium", "high", "critical"}
_STATUSES = {"candidate", "validated", "reported", "duplicate", "invalid"}
_VERDICTS = {"unknown", "exploited", "blocked_by_security", "out_of_scope_internal", "false_positive"}


def finding_save(
    store: Any,
    engagement_id: int,
    vuln_class: str,
    severity: str,
    target: str,
    url: Optional[str] = None,
    payload: Optional[str] = None,
    evidence_ref: Optional[str] = None,
) -> dict:
    sev = (severity or "info").lower()
    if sev not in _SEVERITIES:
        sev = "info"
    verdict, rule, reason = _scope.scope_check(store, engagement_id, target)
    status = "invalid" if verdict == "out" else "candidate"
    ts = now_iso()
    with store.lock:
        cur = store.conn.execute(
            "INSERT INTO findings(engagement_id, vuln_class, severity, target, url, payload, "
            "evidence_ref, status, scope_verdict, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (engagement_id, vuln_class, sev, target, url, payload, evidence_ref, status, verdict, ts, ts),
        )
        store.conn.commit()
        fid = int(cur.lastrowid)
    return {"ok": True, "finding_id": fid, "scope_verdict": verdict, "status": status,
            "reason": reason, "refused": verdict == "out"}


def finding_update(store: Any, finding_id: int, patch: dict) -> dict:
    row = store.query_one("SELECT id FROM findings WHERE id=?", (finding_id,))
    if row is None:
        return {"ok": False, "error": f"finding {finding_id} not found"}
    sets, params = [], []
    if "status" in patch and patch["status"] in _STATUSES:
        sets.append("status=?")
        params.append(patch["status"])
    if "verdict" in patch and patch["verdict"] in _VERDICTS:
        sets.append("verdict=?")
        params.append(patch["verdict"])
    if "severity" in patch and (patch["severity"] or "").lower() in _SEVERITIES:
        sets.append("severity=?")
        params.append(patch["severity"].lower())
    for f in ("evidence_ref", "url", "payload"):
        if f in patch:
            sets.append(f"{f}=?")
            params.append(patch[f])
    if not sets:
        return {"ok": False, "error": "no valid fields to update"}
    sets.append("updated_at=?")
    params.append(now_iso())
    params.append(finding_id)
    store.execute(f"UPDATE findings SET {', '.join(sets)} WHERE id=?", params)
    return {"ok": True, "finding_id": finding_id}


def finding_stats(store: Any, engagement_id: Optional[int] = None) -> dict:
    where = "WHERE engagement_id=?" if engagement_id is not None else ""
    params = (engagement_id,) if engagement_id is not None else ()
    by_sev = {r["severity"]: r["c"] for r in store.query(
        f"SELECT severity, COUNT(*) AS c FROM findings {where} GROUP BY severity", params)}
    by_status = {r["status"]: r["c"] for r in store.query(
        f"SELECT status, COUNT(*) AS c FROM findings {where} GROUP BY status", params)}
    total = store.query_one(f"SELECT COUNT(*) AS c FROM findings {where}", params)
    return {"ok": True, "total": int(total["c"]) if total else 0,
            "by_severity": by_sev, "by_status": by_status}
