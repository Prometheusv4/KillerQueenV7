"""Engagement lifecycle + the real Layer-5 working-state board.

Replaces the never-implemented ``engagement_state.json`` with a live SQLite row.
"""
from __future__ import annotations

import json
from typing import Any, Optional

from . import scope as _scope
from .util import now_iso

_LIST_FIELDS = ("active_vectors", "running_workers", "deployed_payloads", "chain_candidates")


def start(
    store: Any,
    name: str,
    type: str,
    roe_text: str = "",
    in_scope: Optional[list[str]] = None,
    out_scope: Optional[list[str]] = None,
) -> dict:
    """Create (or reuse) an engagement, its state board, and its scope rules."""
    ts = now_iso()
    existing = store.query_one("SELECT id FROM engagements WHERE name=?", (name,))
    created = existing is None
    with store.lock:
        if created:
            cur = store.conn.execute(
                "INSERT INTO engagements(name, type, status, roe_summary, created_at, updated_at) "
                "VALUES (?,?,?,?,?,?)",
                (name, type, "active", (roe_text or "")[:2000], ts, ts),
            )
            eid = int(cur.lastrowid)
            store.conn.execute(
                "INSERT INTO engagement_state(engagement_id, phase, updated_at) VALUES (?,?,?)",
                (eid, "scope", ts),
            )
            store.conn.commit()
        else:
            eid = int(existing["id"])
            store.conn.execute(
                "INSERT OR IGNORE INTO engagement_state(engagement_id, phase, updated_at) VALUES (?,?,?)",
                (eid, "scope", ts),
            )
            store.conn.commit()

    n_rules = 0
    if created:
        rules = _scope.parse_roe(roe_text, in_scope, out_scope)
        n_rules = _scope.insert_rules(store, eid, rules)
    return {"ok": True, "engagement_id": eid, "phase": "scope", "created": created, "scope_rules": n_rules}


def _resolve_eid(store: Any, engagement_id: Optional[int]) -> Optional[int]:
    if engagement_id is not None:
        return engagement_id
    row = store.query_one(
        "SELECT id FROM engagements WHERE status='active' ORDER BY updated_at DESC, id DESC LIMIT 1"
    )
    return int(row["id"]) if row else None


def state_get(store: Any, engagement_id: Optional[int] = None) -> dict:
    eid = _resolve_eid(store, engagement_id)
    if eid is None:
        return {"ok": False, "error": "no engagement found"}
    row = store.query_one("SELECT * FROM engagement_state WHERE engagement_id=?", (eid,))
    if row is None:
        return {"ok": False, "error": f"engagement {eid} has no state"}
    out = {"ok": True, "engagement_id": eid, "phase": row["phase"],
           "target_fingerprint": row["target_fingerprint"], "updated_at": row["updated_at"]}
    # Include scope rules so role_brief can enforce scope boundaries
    scope_rows = store.query(
        "SELECT kind, pattern FROM scope_rules WHERE engagement_id=?",
        (eid,)
    )
    out["in_scope"] = [r["pattern"] for r in scope_rows if r["kind"] == "in"]
    out["out_scope"] = [r["pattern"] for r in scope_rows if r["kind"] == "out"]
    for f in _LIST_FIELDS:
        try:
            out[f] = json.loads(row[f])
        except (TypeError, ValueError):
            out[f] = []
    try:
        out["scratch"] = json.loads(row["scratch"])
    except (TypeError, ValueError):
        out["scratch"] = {}
    return out


def _deep_merge(base: dict, patch: dict) -> dict:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def state_update(store: Any, engagement_id: Optional[int], patch: dict) -> dict:
    """Patch the board. List fields replace; ``scratch`` deep-merges; ``phase`` sets."""
    eid = _resolve_eid(store, engagement_id)
    if eid is None:
        return {"ok": False, "error": "no engagement found"}
    cur = state_get(store, eid)
    if not cur.get("ok"):
        return cur
    ts = now_iso()
    sets, params = [], []
    if "phase" in patch and patch["phase"]:
        sets.append("phase=?")
        params.append(str(patch["phase"]))
    if "target_fingerprint" in patch:
        sets.append("target_fingerprint=?")
        params.append(patch["target_fingerprint"])
    for f in _LIST_FIELDS:
        if f in patch:
            sets.append(f"{f}=?")
            params.append(json.dumps(patch[f]))
    if "scratch" in patch and isinstance(patch["scratch"], dict):
        merged = _deep_merge(cur.get("scratch", {}), patch["scratch"])
        sets.append("scratch=?")
        params.append(json.dumps(merged))
    sets.append("updated_at=?")
    params.append(ts)
    params.append(eid)
    with store.lock:
        store.conn.execute(f"UPDATE engagement_state SET {', '.join(sets)} WHERE engagement_id=?", params)
        store.conn.execute("UPDATE engagements SET updated_at=? WHERE id=?", (ts, eid))
        store.conn.commit()
    return state_get(store, eid)
