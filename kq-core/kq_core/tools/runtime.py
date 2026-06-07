"""Process-wide Store singleton shared by the MCP tool functions.

Created lazily on first use so importing :mod:`kq_core.mcp_server` (which must win the
~0.75s Hermes discovery race) never opens the DB or resolves the embedder at import time.
"""
from __future__ import annotations

import threading
from typing import Optional

from ..store import Store

_STORE: Optional[Store] = None
_LOCK = threading.Lock()


def get_store() -> Store:
    global _STORE
    if _STORE is None:
        with _LOCK:
            if _STORE is None:
                _STORE = Store()  # resolves KQ_HOME via config.get_config()
    return _STORE


def reset_store() -> None:
    """Test hook: drop the singleton so the next get_store() rebuilds it."""
    global _STORE
    with _LOCK:
        if _STORE is not None:
            try:
                _STORE.close()
            except Exception:
                pass
        _STORE = None
