"""KQ Core — deterministic memory/learning/scope/audit substrate for Killer Queen.

Kept intentionally import-light: importing ``kq_core`` must NOT drag in the store,
embeddings, torch, or the MCP SDK. The stdio MCP server (``python -m
kq_core.mcp_server``) must start fast enough to win Hermes's ~0.75s discovery race,
so heavy imports happen lazily inside the modules that need them.
"""

__version__ = "0.1.0"
