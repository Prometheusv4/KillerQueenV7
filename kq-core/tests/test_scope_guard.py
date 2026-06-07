"""Verification step 5: scope guard blocks out-of-scope; audit log is append-only."""
import sqlite3

import pytest

from kq_core import audit, engagement, findings, scope


def test_scope_in_out_cidr_allowlist(store):
    e = engagement.start(store, "t", "red_team", in_scope=["*.example.com"], out_scope=["*.gov", "10.0.0.0/8"])
    eid = e["engagement_id"]
    assert scope.scope_check(store, eid, "admin.example.com")[0] == "in"
    assert scope.scope_check(store, eid, "https://irs.gov/path")[0] == "out"
    assert scope.scope_check(store, eid, "10.1.2.3")[0] == "out"        # cidr match
    assert scope.scope_check(store, eid, "other.org")[0] == "out"        # allowlist semantics


def test_no_rules_is_unknown(store):
    e = engagement.start(store, "t2", "pentest")
    assert scope.scope_check(store, e["engagement_id"], "x.com")[0] == "unknown"


def test_finding_out_of_scope_forced_invalid(store):
    e = engagement.start(store, "t3", "red_team", in_scope=["*.example.com"], out_scope=["*.gov"])
    eid = e["engagement_id"]
    f = findings.finding_save(store, eid, "idor", "high", "irs.gov")
    assert f["status"] == "invalid" and f["scope_verdict"] == "out" and f["refused"] is True
    g = findings.finding_save(store, eid, "idor", "high", "api.example.com")
    assert g["status"] == "candidate" and g["scope_verdict"] == "in"


def test_audit_append_only(store):
    audit.record(store, tool="t", action="call")
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute("UPDATE audit_log SET tool='x' WHERE id=1")
        store.conn.commit()
    store.conn.rollback()
    with pytest.raises(sqlite3.IntegrityError):
        store.conn.execute("DELETE FROM audit_log WHERE id=1")
        store.conn.commit()
    store.conn.rollback()


def test_audit_chain_and_redaction(store):
    audit.record(store, tool="a", action="call", args={"password": "hunter2", "ok": 1})
    audit.record(store, tool="b", action="call", args={"x": "AKIAIOSFODNN7EXAMPLE"})
    v = audit.verify_chain(store)
    assert v["ok"] is True and v["rows"] == 2
    rows = store.query("SELECT args_digest FROM audit_log ORDER BY id")
    joined = " ".join(r["args_digest"] or "" for r in rows)
    assert "hunter2" not in joined           # secret key masked
    assert "AKIAIOSFODNN7EXAMPLE" not in joined  # secret value pattern masked
