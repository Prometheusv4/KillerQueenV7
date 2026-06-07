"""Thin MCP tool wrappers over the KQ Core domain modules.

Each wrapper validates inputs, performs the operation, writes an ``audit_log`` row for
mutations, and returns a JSON-serializable dict ``{"ok": bool, ...}``. The wrappers are
registered onto the FastMCP server in :mod:`kq_core.mcp_server` and surface to the agent
as ``mcp_kq_<name>``.
"""
