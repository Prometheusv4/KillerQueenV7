"""KQ Core stdio MCP server. Run as: ``python -m kq_core.mcp_server``.

Registered as Hermes server ``kq`` so tools surface to the agent as ``mcp_kq_<name>``
(e.g. ``mcp_kq_recall``). Import-light on purpose — no torch / sentence-transformers /
DB work happens at import; the store opens lazily on the first tool call so this process
wins Hermes's ~0.75s discovery race.
"""
from __future__ import annotations

from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from . import audit, engagement, findings, guard, learning, memory, scope, skillgen
from . import chain as _chain, orchestration as _orch, report as _report, triage as _triage
from .arsenal import catalog, runner
from .tools.runtime import get_store

mcp = FastMCP("kq")


def _audit(store: Any, **kw: Any) -> None:
    try:
        audit.record(store, **kw)
    except Exception:  # never let audit failure break a tool
        pass


# ── engagement + working state ────────────────────────────────────────────────
@mcp.tool()
def engagement_start(
    name: str,
    type: str,
    roe_text: str = "",
    in_scope: Optional[list[str]] = None,
    out_scope: Optional[list[str]] = None,
) -> dict:
    """Begin (or resume) an engagement and load its Rules-of-Engagement scope.

    type is one of bug_bounty | red_team | pentest | full_spectrum. in_scope/out_scope are
    host/glob/cidr/regex(``re:``) patterns. Call this FIRST; scope is then enforced for the
    whole engagement.
    """
    s = get_store()
    res = engagement.start(s, name, type, roe_text, in_scope or [], out_scope or [])
    _audit(s, tool="engagement_start", action="call", target=name,
           engagement_id=res.get("engagement_id"),
           args={"name": name, "type": type, "in_scope": in_scope, "out_scope": out_scope}, result=res)
    return res


@mcp.tool()
def engagement_state_get(engagement_id: int = 0) -> dict:
    """Get the live working-state board (phase, active vectors, workers, chains). 0 = latest."""
    return engagement.state_get(get_store(), engagement_id or None)


@mcp.tool()
def engagement_state_update(engagement_id: int, patch: dict) -> dict:
    """Update the working-state board. Keys: phase, active_vectors, running_workers,
    deployed_payloads, chain_candidates (lists replace), target_fingerprint, scratch (deep-merge)."""
    s = get_store()
    flagged = None
    for w in patch.get("running_workers", []) or []:
        flagged = guard.scan(str(w.get("cmd", "")) if isinstance(w, dict) else str(w))
        if flagged:
            break
    res = engagement.state_update(s, engagement_id or None, patch)
    if flagged:
        res["requires_confirm"] = True
        res["confirm_token"] = guard.confirm_token(flagged)
        res["confirm_reason"] = f"destructive pattern '{flagged}' — echo the token via audit_log(action='confirm_granted')"
        _audit(s, tool="engagement_state_update", action="confirm_required", engagement_id=engagement_id,
               target=flagged, verdict="blocked")
    _audit(s, tool="engagement_state_update", action="call", engagement_id=engagement_id, result={"phase": res.get("phase")})
    return res


# ── memory ────────────────────────────────────────────────────────────────────
@mcp.tool()
def remember(content: str, scope: str = "kq", kind: str = "", source: str = "") -> dict:
    """Persist a durable declarative fact (deduplicated). scope: kq | operator. kind:
    weapon | technique | bypass | chain | preference | correction | reference."""
    s = get_store()
    res = memory.remember(s, content, scope=scope, kind=kind or None, source=source or None)
    _audit(s, tool="remember", action="call", args={"scope": scope, "kind": kind}, result=res)
    return res


@mcp.tool()
def recall(
    query: str,
    kinds: Optional[list[str]] = None,
    vuln_class: str = "",
    target_fingerprint: str = "",
    min_confidence: float = 0.0,
    top_k: int = 8,
) -> dict:
    """Hybrid (semantic + keyword) recall over lessons and facts. Call at phase boundaries
    with the target fingerprint / vuln class to surface the most relevant prior learning."""
    res = get_store().recall(
        query, kinds=kinds or None, vuln_class=vuln_class or None,
        target_fingerprint=target_fingerprint or None, min_confidence=min_confidence, top_k=top_k,
    )
    return {"ok": True, "count": len(res), "results": res}


# ── learning loop ───────────────────────────────────────────────────────────────
@mcp.tool()
def lesson_save(
    summary: str,
    category: str,
    trigger: str = "",
    action: str = "",
    rationale: str = "",
    source: str = "",
    target_fingerprint: str = "",
    vuln_class: str = "",
) -> dict:
    """Record a validated lesson (auto-deduplicated; merges bump confidence). category:
    recon | exploitation | evasion | methodology | tool | target-type."""
    s = get_store()
    res = learning.lesson_save(
        s, summary=summary, category=category, trigger_when=trigger, action_do=action,
        rationale=rationale, source=source or None,
        target_fingerprint=target_fingerprint or None, vuln_class=vuln_class or None,
    )
    _audit(s, tool="lesson_save", action="call", args={"category": category, "summary": summary[:80]}, result=res)
    return res


@mcp.tool()
def lesson_outcome(lesson_id: int, outcome: str) -> dict:
    """Record that a recalled lesson was re-validated. outcome: success (boost confidence)
    or failure (decay). Drives confidence over time."""
    s = get_store()
    res = learning.lesson_outcome(s, lesson_id, outcome)
    _audit(s, tool="lesson_outcome", action="call", args={"lesson_id": lesson_id, "outcome": outcome}, result=res)
    return res


@mcp.tool()
def skill_propose(engagement_id: int = 0, trigger: str = "", workflow_summary: str = "") -> dict:
    """Check the 5 skill-creation triggers; if fired, return a SKILL.md DRAFT (gold-standard
    template). Persist it yourself via Hermes skill_manage(create), then verify it exists."""
    s = get_store()
    eid = engagement_id or None
    fired = learning.detect_triggers(s, eid, workflow_summary or None)
    should = bool(fired) or bool(trigger)
    draft = None
    if should:
        steps = []
        if eid:
            rows = s.query("SELECT DISTINCT tool FROM audit_log WHERE engagement_id=? ORDER BY MIN(id)"
                           " GROUP BY tool", (eid,))
            steps = [f"Invoke {r['tool']}" for r in rows][:12]
        draft = skillgen.draft_skill(
            name_hint=(workflow_summary or trigger or "captured-workflow"),
            category="methodology", summary=workflow_summary, triggers_fired=fired,
            workflow_steps=steps or None, source=(f"engagement:{eid}" if eid else None),
        )
    reason = "; ".join(t["reason"] for t in fired) or ("explicit trigger" if trigger else "no triggers fired")
    _audit(s, tool="skill_propose", action="call", engagement_id=eid, result={"should_create": should})
    return {"ok": True, "should_create": should, "triggers_fired": fired, "reason": reason, "draft_skill": draft}


# ── findings + scope + audit ─────────────────────────────────────────────────────
@mcp.tool()
def scope_check(engagement_id: int, target: str) -> dict:
    """Hard Rules-of-Engagement gate. Call before touching ANY target. Returns verdict
    in | out | unknown. Out-of-scope targets must be dropped."""
    s = get_store()
    verdict, rule, reason = scope.scope_check(s, engagement_id, target)
    _audit(s, tool="scope_check", action="scope_check", engagement_id=engagement_id,
           target=target, verdict=verdict)
    return {"ok": True, "verdict": verdict, "matched_rule": rule, "reason": reason}


@mcp.tool()
def finding_save(
    engagement_id: int,
    vuln_class: str,
    severity: str,
    target: str,
    url: str = "",
    payload: str = "",
    evidence_ref: str = "",
) -> dict:
    """Record a finding. Runs scope_check internally — out-of-scope targets are forced
    invalid + refused. severity: info|low|medium|high|critical. evidence_ref is a PATH,
    never a raw secret."""
    s = get_store()
    res = findings.finding_save(s, engagement_id, vuln_class, severity, target,
                                url or None, payload or None, evidence_ref or None)
    _audit(s, tool="finding_save", action="call", engagement_id=engagement_id, target=target,
           verdict=res.get("scope_verdict"), args={"vuln_class": vuln_class, "severity": severity}, result=res)
    return res


@mcp.tool()
def finding_update(finding_id: int, patch: dict) -> dict:
    """Update a finding. Keys: status (candidate|validated|reported|duplicate|invalid),
    verdict (exploited|blocked_by_security|out_of_scope_internal|false_positive), severity,
    evidence_ref, url, payload."""
    s = get_store()
    res = findings.finding_update(s, finding_id, patch)
    _audit(s, tool="finding_update", action="call", args={"finding_id": finding_id, "patch": patch}, result=res)
    return res


@mcp.tool()
def audit_log(action: str, detail: str = "", target: str = "", engagement_id: int = 0) -> dict:
    """Append an operator/agent note to the tamper-evident audit log. Use action=
    'operator_directive' for "remember/never do X", or 'confirm_granted' with the token to
    confirm a destructive action."""
    s = get_store()
    res = audit.record(s, tool="audit_log", action=action, target=target or None,
                       engagement_id=engagement_id or None, args={"detail": detail})
    if action in ("operator_directive",) and detail:
        memory.remember(s, detail, scope="operator", kind="correction", source="operator_directive")
    return {"ok": True, **res}


# ── arsenal: run Kali tools (scoped + audited) ────────────────────────────────────
@mcp.tool()
def target_profile(target: str) -> dict:
    """Classify and fingerprint a target (web | host | network | domain) to drive tool choice."""
    p = runner.profile_target(target)
    return {"ok": True, "target": p.target, "target_type": p.target_type, "host": p.host,
            "scheme": p.scheme, "is_ip": p.is_ip, "is_cidr": p.is_cidr}


@mcp.tool()
def arsenal_recommend(target: str, objective: str = "comprehensive") -> dict:
    """Recommend the best Kali tools for a target (decision engine). objective: quick | comprehensive | stealth."""
    p = runner.profile_target(target)
    recs = runner.recommend(p, objective)
    return {"ok": True, "target_type": p.target_type,
            "tools": [{"name": t.name, "category": t.category, "effectiveness": t.effectiveness,
                       "passive": t.passive, "note": t.note} for t in recs]}


@mcp.tool()
def arsenal_list(category: str = "") -> dict:
    """List catalog tools (optionally by category: recon|dns|scan|web|fuzz|vuln|cred|postex|cloud|...)."""
    specs = catalog.by_category(category) if category else catalog.all_specs()
    return {"ok": True, "count": len(specs),
            "tools": [{"name": s.name, "binary": s.binary, "category": s.category, "passive": s.passive} for s in specs]}


@mcp.tool()
def arsenal_install(tool: str) -> dict:
    """Install a tool from the catalog if missing. Uses the registered install method
    (apt/pip/git/go/docker). Idempotent — skips if already installed."""
    from .arsenal.install import ensure_installed
    return ensure_installed(tool)


@mcp.tool()
def arsenal_install_all(categories: str = "", skip_git: bool = False) -> dict:
    """Install all catalog tools. categories: comma-separated filter (e.g. 'recon,web').
    skip_git: skip git-clone installs (faster, fewer dependencies)."""
    from .arsenal.install import install_all
    cat_list = [c.strip() for c in categories.split(",") if c.strip()] if categories else None
    return install_all(categories=cat_list, skip_git=skip_git)


@mcp.tool()
def run(engagement_id: int, tool: str, target: str = "", extra: str = "",
        mode: str = "normal", confirm_token: str = "") -> dict:
    """Run a Kali tool against a target. Auto-installs missing tools before running.
    Out-of-scope targets refused; destructive commands need confirm_token.
    mode: stealth | normal | aggressive. Returns stdout + result_ref path."""
    # Auto-install if missing
    from .arsenal.install import ensure_installed
    ensure_installed(tool)
    return runner.run_tool(get_store(), engagement_id, tool, target, extra=extra, mode=mode,
                           confirm_token=confirm_token or None)


# ── triage + reporting ────────────────────────────────────────────────────────────
@mcp.tool()
def triage(q1: bool, q2: bool, q3: bool, q4: bool, q5: bool, q6: bool, q7: bool,
           finding_id: int = 0, chainable: bool = False) -> dict:
    """BugHunter 7-question gate. q1=real-request-now, q2=impact-accepted, q3=in-scope,
    q4=no-admin-needed, q5=not-already-known, q6=concrete-impact, q7=not-on-never-submit.
    With finding_id, applies the verdict (PASS->validated, KILL->invalid, DOWNGRADE/CHAIN->candidate)."""
    s = get_store()
    answers = {"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7}
    if finding_id:
        return _triage.triage_finding(s, finding_id, answers, chainable=chainable)
    return {"ok": True, **_triage.gate(answers, chainable=chainable)}


@mcp.tool()
def report(engagement_id: int, format: str = "html", include_unvalidated: bool = False) -> dict:
    """Generate an engagement report (html | md) with the Mermaid attack-chain diagram. By default
    only validated/reported findings are included (no-exploit-no-report); evidence is redacted."""
    return _report.generate(get_store(), engagement_id, fmt=format, include_unvalidated=include_unvalidated)


# ── orchestration: phase plan + role briefs + attack-chain graph ──────────────────
@mcp.tool()
def plan_create(engagement_id: int) -> dict:
    """Seed the Shannon-style phase plan (pre-recon -> recon -> per-class vuln -> exploit -> report).
    Then drive Hermes delegate_task against the runnable tasks. Idempotent."""
    return _orch.plan_create(get_store(), engagement_id)


@mcp.tool()
def plan_status(engagement_id: int) -> dict:
    """Plan progress + the tasks runnable NOW (prerequisites done/skipped). Use to resume an engagement."""
    return _orch.plan_status(get_store(), engagement_id)


@mcp.tool()
def task_update(engagement_id: int, task_id: int, status: str, result_ref: str = "") -> dict:
    """Mark a plan task running|done|skipped. Skip a vuln/exploit role when there is nothing to
    exploit (no-exploit-no-report) so downstream tasks unblock."""
    return _orch.task_update(get_store(), engagement_id, task_id, status, result_ref or None)


@mcp.tool()
def role_brief(role: str, target: str = "", engagement_id: int = 0) -> dict:
    """Bundle scope + curated hunt patterns + learned lessons + recommended tools for a role
    (recon | injection | xss | auth | authz | ssrf | exploit-* | report). Hand this to a delegated
    sub-agent so it starts with exactly the right knowledge."""
    return _orch.role_brief(get_store(), role, target, engagement_id or None)


@mcp.tool()
def chain_build(engagement_id: int) -> dict:
    """Assemble the attack-chain graph from validated findings (+ asserted chains), return nodes+edges."""
    s = get_store()
    _chain.assemble_from_findings(s, engagement_id)
    return _chain.get_chain(s, engagement_id)


@mcp.tool()
def chain_link(engagement_id: int, source_finding_id: int, target_finding_id: int,
               edge_type: str = "enables") -> dict:
    """Link two findings in the chain (A enables/leads_to B). Rejected if it would create a cycle."""
    return _chain.link_findings(get_store(), engagement_id, source_finding_id, target_finding_id, edge_type)


@mcp.tool()
def chain_get(engagement_id: int) -> dict:
    """Fetch the persistent attack-chain graph (nodes + edges + critical nodes)."""
    return _chain.get_chain(get_store(), engagement_id)


# ── knowledge base ───────────────────────────────────────────────────────────────
@mcp.tool()
def kb_search(query: str, collection: str = "", vuln_class: str = "", top_k: int = 5) -> dict:
    """Search the curated knowledge base (Anthropic skills, hunt patterns, scope prompts,
    references). Use for "how do I / what does the literature say" — DISTINCT from
    mcp_kq_recall, which is your own learned memory. Filter by collection
    (anthropic_skill | hunt_pattern | scope | methodology | reference) and/or vuln_class."""
    res = get_store().kb_search(query, collection=collection or None, vuln_class=vuln_class or None, top_k=top_k)
    return {"ok": True, "count": len(res), "results": res}


@mcp.tool()
def kb_extract(collection: str = "", limit: int = 0) -> dict:
    """Extract techniques + facts from kb_chunks into the active learning loop.

    Converts stored knowledge into ACTIVE lessons that recall() and
    role_brief() surface automatically. Run after ingest.

    collection: kq_skill | kq_reference | soul | "" (all)
    limit: max chunks to process (0 = all)
    """
    s = get_store()
    from . import extract
    if collection:
        res = extract.extract_collection(s, collection, limit or None)
    else:
        res = extract.extract_all(s, limit or None)
    _audit(s, tool="kb_extract", action="call",
           args={"collection": collection, "limit": limit}, result=res)
    return res


@mcp.tool()
def kb_extraction_status() -> dict:
    """Report extraction state — chunks processed, lessons/facts created, remaining."""
    from . import extract
    return extract.extraction_status(get_store())


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
