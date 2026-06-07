"""Append-only, tamper-evident audit log + secret redaction.

Every mutating ``mcp_kq_*`` call records one row. Rows are immutable (the DB triggers in
:mod:`kq_core.store` RAISE on UPDATE/DELETE) and chained:

    row_hash = sha256(prev_row_hash + canonical(row_fields))

so any later edit/removal breaks the chain and is detectable by ``verify_chain``. Args
and results are redacted (secrets masked) and truncated before storage — the log is for
*what happened*, never a place to spill credentials.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Optional

from .util import canonical_json, now_iso

# Keys whose values are always masked.
_SECRET_KEY_RE = re.compile(
    r"(pass(word|wd)?|secret|token|api[-_]?key|authorization|auth|cookie|session|"
    r"bearer|private[-_]?key|credential|passphrase)",
    re.IGNORECASE,
)
# Value shapes that look like secrets even without a telltale key.
_SECRET_VALUE_RES = [
    re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+"),  # JWT
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                                      # AWS key id
    re.compile(r"\b[A-Fa-f0-9]{40,}\b"),                                      # long hex secret
    re.compile(r"\b(gh[posu]_[A-Za-z0-9]{20,})\b"),                           # GitHub token
]
_REDACTED = "<redacted>"
_MAX_STR = 600


def _redact_str(s: str) -> str:
    for rx in _SECRET_VALUE_RES:
        s = rx.sub(_REDACTED, s)
    if len(s) > _MAX_STR:
        s = s[:_MAX_STR] + "…(truncated)"
    return s


def redact(obj: Any) -> Any:
    """Recursively mask secret-looking keys/values; truncate long strings."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str) and _SECRET_KEY_RE.search(k):
                out[k] = _REDACTED
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [redact(v) for v in obj]
    if isinstance(obj, str):
        return _redact_str(obj)
    return obj


def _preview(obj: Any, limit: int = 800) -> Optional[str]:
    if obj is None:
        return None
    try:
        s = canonical_json(redact(obj))
    except (TypeError, ValueError):
        s = _redact_str(str(obj))
    return s if len(s) <= limit else s[:limit] + "…"


def record(
    store: Any,
    *,
    tool: str,
    action: str,
    target: Optional[str] = None,
    verdict: Optional[str] = None,
    args: Any = None,
    result: Any = None,
    engagement_id: Optional[int] = None,
    actor: str = "agent",
) -> dict:
    """Append one audit row (hash-chained). Returns {'id', 'row_hash'}."""
    args_d = _preview(args)
    result_d = _preview(result)
    with store.lock:
        prev_row = store.conn.execute(
            "SELECT row_hash FROM audit_log ORDER BY id DESC LIMIT 1"
        ).fetchone()
        prev_hash = prev_row["row_hash"] if prev_row else ""
        ts = now_iso()
        core = canonical_json(
            {
                "ts": ts,
                "engagement_id": engagement_id,
                "actor": actor,
                "tool": tool,
                "action": action,
                "target": target,
                "verdict": verdict,
                "args_digest": args_d,
                "result_digest": result_d,
            }
        )
        row_hash = hashlib.sha256((prev_hash + core).encode("utf-8")).hexdigest()
        cur = store.conn.execute(
            "INSERT INTO audit_log(ts, engagement_id, actor, tool, action, target, verdict, "
            "args_digest, result_digest, prev_hash, row_hash) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (ts, engagement_id, actor, tool, action, target, verdict, args_d, result_d, prev_hash, row_hash),
        )
        store.conn.commit()
        return {"id": int(cur.lastrowid), "row_hash": row_hash}


def verify_chain(store: Any) -> dict:
    """Recompute the hash chain; returns {'ok', 'rows', 'broken_at'}."""
    rows = store.conn.execute(
        "SELECT id, ts, engagement_id, actor, tool, action, target, verdict, "
        "args_digest, result_digest, prev_hash, row_hash FROM audit_log ORDER BY id"
    ).fetchall()
    prev = ""
    for r in rows:
        core = canonical_json(
            {
                "ts": r["ts"],
                "engagement_id": r["engagement_id"],
                "actor": r["actor"],
                "tool": r["tool"],
                "action": r["action"],
                "target": r["target"],
                "verdict": r["verdict"],
                "args_digest": r["args_digest"],
                "result_digest": r["result_digest"],
            }
        )
        expect = hashlib.sha256((prev + core).encode("utf-8")).hexdigest()
        if r["prev_hash"] != prev or r["row_hash"] != expect:
            return {"ok": False, "rows": len(rows), "broken_at": int(r["id"])}
        prev = r["row_hash"]
    return {"ok": True, "rows": len(rows), "broken_at": None}
