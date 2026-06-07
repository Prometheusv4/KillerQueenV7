"""Tiny shared helpers (stdlib-only)."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    """UTC timestamp, second precision, e.g. ``2026-06-06T05:12:33Z``."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(ts: str) -> datetime:
    """Parse an ISO timestamp (with or without trailing Z) to an aware datetime."""
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def canonical_json(obj: Any) -> str:
    """Deterministic JSON for hashing (sorted keys, no whitespace)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> set[str]:
    """Lowercase alphanumeric token set — used for the FTS-mode jaccard fallback."""
    return set(_TOKEN_RE.findall((text or "").lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def slugify(text: str, max_len: int = 48) -> str:
    """kebab-case slug for skill names: ``^[a-z0-9][a-z0-9._-]*$``-friendly."""
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    if not s:
        s = "item"
    if not s[0].isalnum():
        s = "x" + s
    return s[:max_len].rstrip("-")
