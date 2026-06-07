"""Draft a SKILL.md in the Anthropic Cybersecurity-Skills *gold-standard* template.

``skill_propose`` (in :mod:`kq_core.learning` via the tool layer) detects the trigger
conditions and calls :func:`draft_skill`. This module only *drafts* — it never writes to
disk. The agent then persists the draft through Hermes's ``skill_manage`` tool and
verifies it, keeping a clean responsibility boundary (KQ Core never writes outside its DB).
"""
from __future__ import annotations

from typing import List, Optional

import yaml

from .util import now_iso, slugify


def draft_skill(
    *,
    name_hint: str,
    category: str,
    summary: str = "",
    triggers_fired: Optional[List[dict]] = None,
    workflow_steps: Optional[List[str]] = None,
    prerequisites: Optional[List[str]] = None,
    verification: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    mitre_attack: Optional[List[str]] = None,
    nist_csf: Optional[List[str]] = None,
    source: Optional[str] = None,
) -> dict:
    """Return ``{name, frontmatter, body, markdown, suggested_path}`` for a new skill."""
    name = slugify(name_hint or summary or category or "captured-workflow")
    description = (summary or f"Captured {category} workflow.").strip()
    if not description.lower().startswith(("use ", "when ")):
        description = f"{description} Use when a similar {category} situation arises."

    frontmatter = {
        "name": name,
        "description": description,
        "domain": "cybersecurity",
        "subdomain": category,
        "tags": tags or [category],
        "version": "1.0",
        "author": "killer-queen",
        "license": "Apache-2.0",
    }
    if mitre_attack:
        frontmatter["mitre_attack"] = mitre_attack
    if nist_csf:
        frontmatter["nist_csf"] = nist_csf

    steps = workflow_steps or ["(capture the exact tool sequence that worked here)"]
    prereq = prerequisites or ["(tools / access / credentials this workflow assumed)"]
    verif = verification or ["(how to confirm the workflow succeeded)"]
    fired = ", ".join(t.get("id", "?") for t in (triggers_fired or [])) or "manual"

    body_lines = [
        "## When to Use",
        description,
        "",
        "## Prerequisites",
        *[f"- {p}" for p in prereq],
        "",
        "## Workflow",
        *[f"{i}. {s}" for i, s in enumerate(steps, 1)],
        "",
        "## Verification",
        *[f"- {v}" for v in verif],
        "",
        "## Provenance",
        f"- Auto-drafted by KQ Core on {now_iso()} (triggers: {fired}).",
    ]
    if source:
        body_lines.append(f"- Source: {source}")
    body = "\n".join(body_lines).rstrip() + "\n"

    fm = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).rstrip()
    markdown = f"---\n{fm}\n---\n\n{body}"
    return {
        "name": name,
        "frontmatter": frontmatter,
        "body": body,
        "markdown": markdown,
        "suggested_path": f"{category}/{name}/SKILL.md",
    }
