"""Phase 4: phase plan (dependency ordering + resume) and per-role briefs — v6.1."""

from kq_core import engagement, orchestration as orch


def _role_ids(tasks):
    return {t["role"]: t["id"] for t in tasks}


def test_plan_dependencies(store):
    eid = engagement.start(store, "t", "red_team")["engagement_id"]
    st = orch.plan_create(store, eid)
    # v6.1: 41 tasks across 8 domains
    assert st["total"] == 41
    # Root should be runnable immediately
    assert "pre-recon" in st["runnable_now"]

    ids = _role_ids(st["tasks"])
    st = orch.task_update(store, eid, ids["pre-recon"], "done")
    assert "recon" in st["runnable_now"]

    st = orch.task_update(store, eid, ids["recon"], "done")
    runnable = set(st["runnable_now"])
    assert {"injection", "xss", "auth", "authz", "ssrf"}.issubset(runnable)

    st = orch.task_update(store, eid, ids["injection"], "done")
    assert "exploit-injection" in st["runnable_now"]

    # Skipping a vuln role unblocks its exploit
    st = orch.task_update(store, eid, ids["xss"], "skipped")
    assert "exploit-xss" in st["runnable_now"]


def test_plan_idempotent_resume(store):
    eid = engagement.start(store, "t2", "red_team")["engagement_id"]
    a = orch.plan_create(store, eid)
    b = orch.plan_create(store, eid)  # second call = no duplicate
    assert a["total"] == b["total"] == 41
    assert store.query_one(
        "SELECT COUNT(*) c FROM plan_tasks WHERE engagement_id=?",
        (eid,)
    )["c"] == 41


def test_role_brief_bundle(store):
    eid = engagement.start(store, "t3", "red_team",
                           in_scope=["*.example.com"])["engagement_id"]
    store.put_kb_chunk(
        collection="hunt_pattern", source="hunt-ssrf", title="ssrf",
        content="ssrf reaches cloud metadata 169.254 to steal credentials, bypass filters",
        vuln_class="ssrf", chunk_index=0,
    )
    b = orch.role_brief(store, "ssrf", "https://app.example.com", eid)
    assert b["ok"]
    assert b["base_role"] == "ssrf"
    assert b["vuln_class"] == "ssrf"
    assert len(b.get("instructions", "")) > 50
    # Scope from engagement should be present
    assert "*.example.com" in b.get("scope", {}).get("in_scope", [])
