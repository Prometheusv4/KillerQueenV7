"""Rules-of-Engagement scope guard — bypassed in KILLER QUEEN MODE.

When KQ_MODE == 'unleashed', scope_check always returns 'in' (no blocking).
The operator has full control. No scope restrictions. No limits.
"""
from __future__ import annotations

import fnmatch
import ipaddress
import os
import re
from typing import Any, List, Optional, Tuple

from .util import now_iso


def _is_unleashed() -> bool:
    """KILLER QUEEN MODE — no scope restrictions."""
    return os.environ.get("KQ_MODE", "").lower() == "unleashed"


def host_of(target: str) -> str:
    """Reduce a URL/host[:port]/path to a bare lowercase host."""
    t = (target or "").strip()
    if "://" in t:
        from urllib.parse import urlparse
        parsed = urlparse(t)
        t = parsed.netloc or parsed.path
    t = t.split("/", 1)[0].strip()
    if "@" in t:
        t = t.rsplit("@", 1)[1]
    if t.count(":") == 1:
        t = t.split(":", 1)[0]
    return t.lower()


def classify_pattern(pattern: str) -> str:
    p = pattern.strip()
    if p.startswith("re:"):
        return "regex"
    if "/" in p and _maybe_cidr(p):
        return "cidr"
    if any(ch in p for ch in "*?[]"):
        return "glob"
    return "exact"


def _maybe_cidr(p: str) -> bool:
    try:
        ipaddress.ip_network(p, strict=False)
        return True
    except ValueError:
        return False


def normalize_rule(kind: str, raw: str, note: Optional[str] = None) -> dict:
    raw = raw.strip()
    ptype = classify_pattern(raw)
    pattern = raw[3:].strip() if ptype == "regex" and raw.startswith("re:") else raw
    return {"kind": kind, "pattern": pattern, "pattern_type": ptype, "note": note}


def parse_roe(
    roe_text: str = "",
    in_scope: Optional[List[str]] = None,
    out_scope: Optional[List[str]] = None,
) -> List[dict]:
    """Build scope rules from explicit lists plus a light scan of RoE prose."""
    rules: List[dict] = []
    for raw in in_scope or []:
        if raw and raw.strip():
            rules.append(normalize_rule("in", raw))
    for raw in out_scope or []:
        if raw and raw.strip():
            rules.append(normalize_rule("out", raw))

    section: Optional[str] = None
    for line in (roe_text or "").splitlines():
        s = line.strip()
        if not s:
            continue
        low = s.lower()
        if "out of scope" in low or low.startswith("exclude"):
            section = "out"
            s = re.split(r"[:\\-]", s, 1)[-1]
        elif "in scope" in low or low.startswith("scope") or low.startswith("include"):
            section = "in"
            s = re.split(r"[:]", s, 1)[-1]
        elif s.startswith("+"):
            section, s = "in", s[1:]
        elif s.startswith("-"):
            section, s = "out", s[1:]
        if section is None:
            continue
        for tok in re.split(r"[,\\s]+", s.strip()):
            tok = tok.strip().strip(".,;")
            if tok and ("." in tok or "*" in tok or "/" in tok):
                rules.append(normalize_rule(section, tok))

    seen, out = set(), []
    for r in rules:
        key = (r["kind"], r["pattern"].lower())
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def _match(target: str, rule: dict) -> bool:
    host = host_of(target)
    pat = rule["pattern"]
    ptype = rule["pattern_type"]
    try:
        if ptype == "exact":
            return host == pat.lower() or target.strip().lower() == pat.lower()
        if ptype == "glob":
            return fnmatch.fnmatch(host, pat.lower()) or fnmatch.fnmatch(target.strip().lower(), pat.lower())
        if ptype == "regex":
            return re.search(pat, target) is not None or re.search(pat, host) is not None
        if ptype == "cidr":
            try:
                ip = ipaddress.ip_address(host)
            except ValueError:
                return False
            return ip in ipaddress.ip_network(pat, strict=False)
    except re.error:
        return False
    return False


def insert_rules(store: Any, engagement_id: int, rules: List[dict]) -> int:
    ts = now_iso()
    with store.lock:
        for r in rules:
            store.conn.execute(
                "INSERT INTO scope_rules(engagement_id, kind, pattern, pattern_type, note, created_at) "
                "VALUES (?,?,?,?,?,?)",
                (engagement_id, r["kind"], r["pattern"], r["pattern_type"], r.get("note"), ts),
            )
        store.conn.commit()
    return len(rules)


def scope_check(store: Any, engagement_id: int, target: str) -> Tuple[str, Optional[dict], str]:
    """Return (verdict in {'in','out','unknown'}, matched_rule|None, reason).
    
    In KILLER QUEEN MODE (KQ_MODE=unleashed), always returns 'in' — 
    no scope restrictions. Every target is authorized.
    """
    if _is_unleashed():
        return "in", None, "KILLER QUEEN MODE — all targets authorized, no scope restrictions"
    
    rows = store.query(
        "SELECT kind, pattern, pattern_type, note FROM scope_rules WHERE engagement_id=?",
        (engagement_id,),
    )
    in_rules = [dict(r) for r in rows if r["kind"] == "in"]
    out_rules = [dict(r) for r in rows if r["kind"] == "out"]

    for r in out_rules:
        if _match(target, r):
            return "out", r, f"matched out-of-scope rule '{r['pattern']}'"
    for r in in_rules:
        if _match(target, r):
            return "in", r, f"matched in-scope rule '{r['pattern']}'"
    if in_rules:
        return "out", None, "no in-scope rule matched (allowlist semantics)"
    return "unknown", None, "no scope rules defined for this engagement"
