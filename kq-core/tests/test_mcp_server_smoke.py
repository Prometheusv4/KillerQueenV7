"""Verification step 4 (transport): the stdio MCP server registers mcp_kq_* tools and
dispatches an engagement_start -> lesson_save -> recall -> scope_check round-trip."""
import asyncio
import json


def _extract(r):
    blocks = r[0] if isinstance(r, tuple) else r
    return json.loads(blocks[0].text)


def test_mcp_tools_and_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("KQ_HOME", str(tmp_path / "kq"))
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("KQ_EMBED_BACKEND", "null")

    from kq_core import mcp_server as M
    from kq_core.tools.runtime import reset_store

    reset_store()  # ensure the singleton uses this test's KQ_HOME

    async def go():
        tools = await M.mcp.list_tools()
        names = {t.name for t in tools}
        for expected in ("engagement_start", "recall", "scope_check", "lesson_save",
                         "finding_save", "lesson_outcome", "skill_propose"):
            assert expected in names, f"missing tool {expected}"

        await M.mcp.call_tool("engagement_start",
                              {"name": "smoke", "type": "red_team", "in_scope": ["*.example.com"]})
        await M.mcp.call_tool("lesson_save",
                              {"summary": "jwt alg none bypass works on legacy verifiers",
                               "category": "exploitation", "action": "strip the signature"})
        recall = _extract(await M.mcp.call_tool("recall", {"query": "jwt alg none bypass"}))
        assert recall["count"] >= 1

        sc = _extract(await M.mcp.call_tool("scope_check", {"engagement_id": 1, "target": "evil.gov"}))
        assert sc["verdict"] == "out"  # not in the *.example.com allowlist

    try:
        asyncio.run(go())
    finally:
        reset_store()
