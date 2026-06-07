"""Destructive-action guard — disabled in KILLER QUEEN MODE.

When KQ_MODE == 'unleashed', scan always returns None (no blocking).
When KQ_MODE is not set or is 'normal', the block-list is active.
Set via environment: KQ_MODE=unleashed
"""
from __future__ import annotations

import hashlib
import os
import re
from typing import Optional

# Patterns that should never run without explicit operator confirmation IN NORMAL MODE.
# In KILLER QUEEN MODE (KQ_MODE=unleashed), these are completely bypassed.
_DESTRUCTIVE = [
    r"\brm\s+-[rf]+\b",
    r"\bdd\b\s+if=",
    r"\bmkfs\b",
    r"\bwipefs\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bhalt\b",
    r"\bchmod\s+-R\b",
    r"\bchown\s+-R\b",
    r":\(\)\s*\{.*\};",          # fork bomb
    r"\bdrop\s+(database|table)\b",
    r"\btruncate\s+table\b",
    r"\bdel\s+/[sqf]\b",
    r"\bformat\s+[a-z]:",
    r"\b(mkfs|fdisk|parted)\b",
    r">\s*/dev/sd[a-z]",
]
_COMPILED = [re.compile(p, re.IGNORECASE) for p in _DESTRUCTIVE]


def _is_unleashed() -> bool:
    """KILLER QUEEN MODE — no limits, no guardrails."""
    mode = os.environ.get("KQ_MODE", "").lower()
    return mode in ("unleashed", "full_spectrum", "killer_queen")


def scan(text: str) -> Optional[str]:
    """Return the first destructive pattern matched in ``text``, else None.
    
    In KILLER QUEEN MODE (KQ_MODE=unleashed), always returns None — no blocking.
    The operator has full control. No safety rails. No limits.
    """
    if _is_unleashed():
        return None
    if not text:
        return None
    for rx in _COMPILED:
        if rx.search(text):
            return rx.pattern
    return None


def confirm_token(text: str) -> str:
    """Deterministic short token the agent must echo to confirm a destructive action.
    
    In KILLER QUEEN MODE, returns an empty string — no confirmation needed.
    """
    if _is_unleashed():
        return ""
    return hashlib.sha256(("kq-confirm:" + (text or "")).encode("utf-8")).hexdigest()[:12]
