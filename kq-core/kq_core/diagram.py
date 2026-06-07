"""Assemble a Mermaid attack-chain diagram from findings + chain_candidates.

CyberStrikeAI-style typed nodes/edges (target -> action/vuln), with the runtime cycle
check their code lacked: if networkx is present we drop back edges that would create a
cycle so the rendered graph stays a DAG.
"""
from __future__ import annotations

import re
from typing import Any, List, Optional

_SEV_CLASS = {"critical": "crit", "high": "high", "medium": "med", "low": "low", "info": "info"}


def _san(text: str, limit: int = 60) -> str:
    s = re.sub(r'["\[\]<>{}|]', " ", str(text or ""))
    s = s.replace("\n", " ").strip()
    return (s[:limit] + "…") if len(s) > limit else s


def _fid(x: Any) -> str:
    return "F" + re.sub(r"[^A-Za-z0-9]", "", str(x))


def mermaid_chain(target: str, findings: List[dict], chains: Optional[List[dict]] = None) -> str:
    lines = ["flowchart LR", '  T(["🎯 ' + _san(target, 40) + '"])']
    valid_ids = set()
    for f in findings:
        nid = _fid(f["id"])
        valid_ids.add(str(f["id"]))
        sev = (f.get("severity") or "info").lower()
        label = f"{_san(f.get('vuln_class'), 24)} ({sev})<br/>{_san(f.get('target'), 28)}"
        lines.append(f'  {nid}["{label}"]:::{_SEV_CLASS.get(sev, "info")}')
        lines.append(f"  T --> {nid}")

    edges: List[tuple] = []
    for ch in (chains or []):
        hops = [str(h) for h in ch.get("hops", []) if str(h) in valid_ids]
        for a, b in zip(hops, hops[1:]):
            edges.append((a, b))

    edges = _drop_cycles(edges)
    for a, b in edges:
        lines.append(f"  {_fid(a)} -. chain .-> {_fid(b)}")

    lines += [
        "  classDef crit fill:#7d1128,stroke:#ff4d6d,color:#fff;",
        "  classDef high fill:#9a3412,stroke:#fb923c,color:#fff;",
        "  classDef med fill:#854d0e,stroke:#facc15,color:#fff;",
        "  classDef low fill:#14532d,stroke:#4ade80,color:#fff;",
        "  classDef info fill:#1f2937,stroke:#9ca3af,color:#fff;",
    ]
    return "\n".join(lines)


def mermaid_from_graph(nodes: List[dict], edges: List[dict]) -> str:
    """Render the persistent chain graph (chain_nodes/chain_edges) as Mermaid."""
    lines = ["flowchart LR"]

    def cls(n: dict) -> str:
        if n["node_type"] == "target":
            return "tgt"
        r = n.get("risk_score", 0)
        return "crit" if r >= 80 else "high" if r >= 60 else "med" if r >= 40 else "info"

    for n in nodes:
        nid = "N" + str(n["id"])
        label = _san(n["label"], 40)
        if n["node_type"] == "target":
            lines.append(f'  {nid}(["🎯 {label}"]):::tgt')
        else:
            lines.append(f'  {nid}["{label}<br/>risk {n.get("risk_score", 0)}"]:::{cls(n)}')
    for e in edges:
        lines.append(f'  N{e["source_id"]} -- {e["edge_type"]} --> N{e["target_id"]}')
    lines += [
        "  classDef tgt fill:#1e3a8a,stroke:#60a5fa,color:#fff;",
        "  classDef crit fill:#7d1128,stroke:#ff4d6d,color:#fff;",
        "  classDef high fill:#9a3412,stroke:#fb923c,color:#fff;",
        "  classDef med fill:#854d0e,stroke:#facc15,color:#fff;",
        "  classDef low fill:#14532d,stroke:#4ade80,color:#fff;",
        "  classDef info fill:#1f2937,stroke:#9ca3af,color:#fff;",
    ]
    return "\n".join(lines)


def _drop_cycles(edges: List[tuple]) -> List[tuple]:
    """Keep the graph acyclic. Uses networkx if available, else a simple DFS guard."""
    try:
        import networkx as nx

        g = nx.DiGraph()
        kept = []
        for a, b in edges:
            g.add_edge(a, b)
            try:
                nx.find_cycle(g)
                g.remove_edge(a, b)  # this edge introduced a cycle -> drop it
            except nx.NetworkXNoCycle:
                kept.append((a, b))
        return kept
    except Exception:
        # Fallback: drop any edge whose endpoints are already connected in reverse.
        adj: dict = {}
        kept = []
        for a, b in edges:
            if _reachable(adj, b, a):
                continue
            adj.setdefault(a, set()).add(b)
            kept.append((a, b))
        return kept


def _reachable(adj: dict, src: str, dst: str) -> bool:
    seen, stack = set(), [src]
    while stack:
        n = stack.pop()
        if n == dst:
            return True
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj.get(n, ()))
    return False
