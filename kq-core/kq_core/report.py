"""Engagement report generation (HTML / Markdown) — the non-terminal surface.

Pulls findings + stats from the store, redacts evidence (BugHunter hygiene), embeds the
Mermaid attack-chain diagram, and by default reports only *validated/reported* findings
(Shannon's no-exploit-no-report). HTML renders the diagram via the mermaid CDN.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from . import audit, diagram, findings as _findings
from .util import now_iso

_REPORTABLE = ("validated", "reported")
_SEV_COLOR = {"critical": "#ff4d6d", "high": "#fb923c", "medium": "#facc15", "low": "#4ade80", "info": "#9ca3af"}
_SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def _gather(store: Any, engagement_id: int, include_unvalidated: bool):
    eng = store.query_one("SELECT * FROM engagements WHERE id=?", (engagement_id,))
    all_rows = [dict(r) for r in store.query(
        "SELECT * FROM findings WHERE engagement_id=? ORDER BY id", (engagement_id,))]
    shown = [f for f in all_rows if include_unvalidated or f["status"] in _REPORTABLE]
    shown.sort(key=lambda f: _SEV_ORDER.get((f.get("severity") or "info").lower(), 9))
    excluded = len(all_rows) - len(shown)
    stats = _findings.finding_stats(store, engagement_id)
    st = store.query_one("SELECT chain_candidates FROM engagement_state WHERE engagement_id=?", (engagement_id,))
    try:
        chains = json.loads(st["chain_candidates"]) if st else []
    except (TypeError, ValueError):
        chains = []
    for f in shown:  # evidence hygiene
        if f.get("payload"):
            f["payload"] = audit._preview({"p": f["payload"]}, 200) or ""
    return eng, shown, excluded, stats, chains


def render_markdown(eng, shown, excluded, stats, chains, audit_info, mermaid) -> str:
    name = eng["name"] if eng else "engagement"
    lines = [f"# Killer Queen — Engagement Report: {name}", "",
             f"_Generated {now_iso()} · type: {eng['type'] if eng else '?'} · "
             f"audit chain ok: {audit_info['ok']} ({audit_info['rows']} rows)_", "",
             "## Executive Summary", ""]
    bysev = stats.get("by_severity", {})
    lines.append("| Severity | Count |"); lines.append("|---|---|")
    for sev in ("critical", "high", "medium", "low", "info"):
        lines.append(f"| {sev} | {bysev.get(sev, 0)} |")
    lines += ["", "## Attack Chain", "", "```mermaid", mermaid, "```", "",
              f"## Findings ({len(shown)} reportable)", ""]
    if shown:
        lines.append("| ID | Class | Severity | Target | Status | Verdict |")
        lines.append("|---|---|---|---|---|---|")
        for f in shown:
            lines.append(f"| {f['id']} | {f['vuln_class']} | {f['severity']} | {f['target']} | "
                         f"{f['status']} | {f['verdict']} |")
    else:
        lines.append("_No validated findings yet (no-exploit-no-report)._")
    lines += ["", f"> {excluded} unvalidated finding(s) excluded (no-exploit-no-report). "
                  "Evidence redacted for secrets/PII before display."]
    return "\n".join(lines) + "\n"


def render_html(eng, shown, excluded, stats, chains, audit_info, mermaid) -> str:
    name = eng["name"] if eng else "engagement"
    bysev = stats.get("by_severity", {})
    badges = "".join(
        f'<span class="badge" style="background:{_SEV_COLOR[s]}">{s}: {bysev.get(s, 0)}</span>'
        for s in ("critical", "high", "medium", "low", "info"))
    rows = "".join(
        f"<tr><td>{f['id']}</td><td>{f['vuln_class']}</td>"
        f'<td><b style="color:{_SEV_COLOR.get((f.get("severity") or "info").lower(), "#9ca3af")}">{f["severity"]}</b></td>'
        f"<td>{_esc(f['target'])}</td><td>{f['status']}</td><td>{f['verdict']}</td></tr>"
        for f in shown) or '<tr><td colspan="6">No validated findings (no-exploit-no-report).</td></tr>'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Killer Queen Report — {_esc(name)}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true,theme:'dark'}});</script>
<style>
 body{{background:#0d0d0f;color:#e5e7eb;font:14px/1.5 system-ui,sans-serif;margin:0 auto;max-width:1000px;padding:32px}}
 h1{{color:#ff4d6d}} h2{{color:#fb923c;border-bottom:1px solid #333;padding-bottom:4px;margin-top:32px}}
 .badge{{display:inline-block;padding:4px 10px;border-radius:6px;color:#000;font-weight:700;margin:2px}}
 table{{width:100%;border-collapse:collapse;margin-top:8px}} td,th{{border:1px solid #2a2a2e;padding:6px 10px;text-align:left}}
 th{{background:#17171b}} .mermaid{{background:#111;padding:16px;border-radius:8px}}
 .note{{color:#9ca3af;font-size:12px;margin-top:8px}}
</style></head><body>
<h1>Killer Queen — Engagement Report</h1>
<p><b>{_esc(name)}</b> · type: {eng['type'] if eng else '?'} · generated {now_iso()} ·
 audit chain ok: <b>{audit_info['ok']}</b> ({audit_info['rows']} rows)</p>
<h2>Executive Summary</h2><div>{badges}</div>
<h2>Attack Chain</h2><pre class="mermaid">{_esc(mermaid)}</pre>
<h2>Findings ({len(shown)} reportable)</h2>
<table><tr><th>ID</th><th>Class</th><th>Severity</th><th>Target</th><th>Status</th><th>Verdict</th></tr>{rows}</table>
<p class="note">{excluded} unvalidated finding(s) excluded (no-exploit-no-report). Evidence redacted for secrets/PII.</p>
</body></html>"""


def _esc(s: Any) -> str:
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def generate(store: Any, engagement_id: int, fmt: str = "html", include_unvalidated: bool = False,
             path: Optional[Path | str] = None) -> dict:
    from . import chain as _chain
    eng, shown, excluded, stats, chains = _gather(store, engagement_id, include_unvalidated)
    audit_info = audit.verify_chain(store)
    # Assemble + render the persistent attack-chain graph (fall back to a findings tree).
    _chain.assemble_from_findings(store, engagement_id)
    g = _chain.get_chain(store, engagement_id)
    target_label = eng["name"] if eng else "engagement"
    mermaid = diagram.mermaid_from_graph(g["nodes"], g["edges"]) if g["node_count"] > 1 \
        else diagram.mermaid_chain(target_label, shown, chains)
    body = render_html(eng, shown, excluded, stats, chains, audit_info, mermaid) if fmt == "html" \
        else render_markdown(eng, shown, excluded, stats, chains, audit_info, mermaid)
    ext = "html" if fmt == "html" else "md"
    store.cfg.exports_dir.mkdir(parents=True, exist_ok=True)
    out = Path(path) if path else store.cfg.exports_dir / f"report_engagement_{engagement_id}.{ext}"
    out.write_text(body, encoding="utf-8")
    return {"ok": True, "path": str(out), "format": fmt, "reportable": len(shown),
            "excluded": excluded, "by_severity": stats.get("by_severity", {})}
