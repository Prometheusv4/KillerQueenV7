"""Phase 3: arsenal runner — profiling, decision engine, command build, guardrails, cache."""
from kq_core import engagement
from kq_core.arsenal import runner


def test_target_profiling():
    assert runner.profile_target("https://app.example.com/x").target_type == "web"
    assert runner.profile_target("example.com").target_type == "domain"
    assert runner.profile_target("10.0.0.5").target_type == "host"
    assert runner.profile_target("10.0.0.0/24").target_type == "network"


def test_decision_engine_ranks():
    web = runner.recommend(runner.profile_target("https://x.com"), "comprehensive", 5)
    assert "nuclei" in [t.name for t in web]
    quick = runner.recommend(runner.profile_target("x.com"), "quick")
    assert len(quick) <= 3
    stealth = runner.recommend(runner.profile_target("https://x.com"), "stealth")
    assert all(t.passive for t in stealth)


def test_build_command():
    argv, spec = runner.build_command("nmap", "10.0.0.5")
    assert argv[0] == "nmap" and "10.0.0.5" in argv and spec.binary == "nmap"
    gen, spec2 = runner.build_command("customtool", "x.com", extra="--flag v")
    assert gen == ["customtool", "--flag", "v", "x.com"] and spec2 is None


def test_classify_error():
    assert runner.classify_error(0, "", False) == "ok"
    assert runner.classify_error(-1, "timeout", True) == "timeout"
    assert runner.classify_error(1, "Permission denied (are you root?)", False) == "permission"
    assert runner.classify_error(1, "could not resolve host", False) == "network"
    assert runner.classify_error(2, "usage: nmap [opts]", False) == "syntax"


def test_run_tool_scope_refusal(store):
    e = engagement.start(store, "t", "red_team", in_scope=["*.example.com"], out_scope=["*.gov"])
    r = runner.run_tool(store, e["engagement_id"], "nmap", "irs.gov")
    assert r["refused"] is True and r["scope_verdict"] == "out"


def test_run_tool_destructive_requires_confirm(store):
    e = engagement.start(store, "t", "red_team")
    r = runner.run_tool(store, e["engagement_id"], "rm", "", extra="-rf /tmp/zzz")
    assert r.get("requires_confirm") is True and r.get("confirm_token")
    # without the token the command is NOT executed (no run audit row of action=run_tool ok)


def test_run_tool_not_installed(store):
    e = engagement.start(store, "t", "red_team", in_scope=["*.example.com"])
    r = runner.run_tool(store, e["engagement_id"], "definitely_not_installed_xyz", "app.example.com")
    assert r.get("error") == "not_installed"


def test_run_tool_real_exec_and_cache(store):
    e = engagement.start(store, "t", "red_team")
    # python is available on PATH; harmless --version exercises the real exec + cache path.
    r1 = runner.run_tool(store, e["engagement_id"], "python", "", extra="--version")
    assert r1["ok"] is True and r1["error_class"] == "ok" and "Python" in r1["stdout"]
    r2 = runner.run_tool(store, e["engagement_id"], "python", "", extra="--version")
    assert r2.get("cached") is True
