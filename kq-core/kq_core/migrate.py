"""Import the existing Killer Queen profile memory + references into the store.

Idempotent: dedup means re-running ``kq migrate`` corroborates rather than duplicates.

Responsible-use: reference files whose sole purpose is worm/self-propagation are NOT
auto-indexed (the agent shouldn't have self-propagating-malware construction guides in
always-on retrieval). Skipped files are reported, never silently dropped.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from . import learning, memory

# Filenames we refuse to auto-index (worm self-propagation). Logged, not silent.
_DENYLIST = ("worm",)

_CATEGORY_KEYWORDS = {
    "recon": ["recon", "nmap", "subdomain", "enumerat", "osint", " dns", "port scan", "fingerprint", "wp-json"],
    "exploitation": ["sqli", "sql injection", "xss", "ssrf", "idor", "rce", "upload", "jwt", "oauth",
                     "xxe", "deserial", "payload", "exploit", "injection", "smuggl", "ssti"],
    "evasion": ["waf", "edr", "amsi", "etw", "evasion", "bypass", "obfuscat", "sandbox", "proxy"],
    "tool": ["sqlmap", "nuclei", "ffuf", "wpscan", "requests", "curl", "hydra", " flag"],
    "target-type": ["wordpress", "cpanel", "m365", "entra", "azure", "aws", "contabo", "plugin", "cf7", "dnd"],
}


def infer_category(text: str) -> str:
    low = (text or "").lower()
    for cat, kws in _CATEGORY_KEYWORDS.items():
        if any(k in low for k in kws):
            return cat
    return "methodology"


def _sections(md: str) -> list[tuple[int, str, str]]:
    """Split markdown into (level, title, body) blocks at ## / ### headings."""
    out: list[tuple[int, str, str]] = []
    cur_level, cur_title, buf = 0, "", []
    for line in md.splitlines():
        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            if cur_title or buf:
                out.append((cur_level, cur_title, "\n".join(buf).strip()))
            cur_level, cur_title, buf = len(m.group(1)), m.group(2).strip(), []
        else:
            buf.append(line)
    if cur_title or buf:
        out.append((cur_level, cur_title, "\n".join(buf).strip()))
    return out


def _bullets(body: str) -> list[str]:
    out = []
    for line in body.splitlines():
        s = line.strip()
        m = re.match(r"^(?:[-*]|\d+\.)\s+(.*)$", s)
        if m and m.group(1).strip():
            out.append(m.group(1).strip())
    return out


def _import_killer_queen(store: Any, path: Path, counts: dict) -> None:
    md = path.read_text(encoding="utf-8", errors="replace")
    src = "migrated:KILLER-QUEEN.md"
    for level, title, body in _sections(md):
        up = title.upper()
        if "ENGAGEMENT STATE" in up:
            continue
        if "LESSON" in up:
            for b in _bullets(body):
                r = learning.lesson_save(store, summary=b, category=infer_category(b), source=src)
                counts["lessons_" + r["action"]] = counts.get("lessons_" + r["action"], 0) + 1
        elif "WEAPON" in up or "INVENTORY" in up:
            text = (title + "\n" + body).strip()
            if body:
                memory.remember(store, text[:1500], kind="weapon", source=src)
                counts["facts"] += 1
        elif "TECHNIQUE" in up or "LIBRARY" in up:
            if body:
                memory.remember(store, f"{title}: {body}"[:1500], kind="technique", source=src)
                counts["facts"] += 1
        elif body:
            memory.remember(store, f"{title}: {body}"[:1500], kind="reference", source=src)
            counts["facts"] += 1


def _import_operator(store: Any, path: Path, counts: dict) -> None:
    md = path.read_text(encoding="utf-8", errors="replace")
    src = "migrated:OPERATOR.md"
    for level, title, body in _sections(md):
        up = title.upper()
        kind = "correction" if ("DIRECTIVE" in up or "CORRECTION" in up) else "preference"
        items = _bullets(body) or ([body] if body.strip() else [])
        for it in items:
            memory.remember(store, f"{title}: {it}"[:800], scope="operator", kind=kind, source=src)
            counts["operator"] += 1


def _import_reference(store: Any, path: Path, relpath: str, counts: dict, max_blocks: int = 60) -> None:
    md = path.read_text(encoding="utf-8", errors="replace")
    secs = _sections(md)
    blocks = 0
    if not secs or all(not b for _l, _t, b in secs):
        # No headings — chunk the raw text.
        text = md.strip()
        for i in range(0, min(len(text), max_blocks * 1500), 1500):
            memory.remember(store, f"[{relpath}] {text[i:i + 1500]}", kind="reference", source=relpath)
            counts["references"] += 1
            blocks += 1
            if blocks >= max_blocks:
                break
        return
    for _level, title, body in secs:
        if not body.strip():
            continue
        memory.remember(store, f"[{relpath} > {title}] {body}"[:1500], kind="reference", source=relpath)
        counts["references"] += 1
        blocks += 1
        if blocks >= max_blocks:
            break


def migrate_profile(store: Any, profile_dir: Path | str) -> dict:
    """Import KILLER-QUEEN.md + OPERATOR.md + skills/**/references + docs/references."""
    profile_dir = Path(profile_dir)
    counts: dict = {"lessons_inserted": 0, "lessons_merged": 0, "facts": 0,
                    "operator": 0, "references": 0, "files": 0, "skipped": []}

    km = profile_dir / "memories" / "KILLER-QUEEN.md"
    if km.exists():
        _import_killer_queen(store, km, counts)
    om = profile_dir / "memories" / "OPERATOR.md"
    if om.exists():
        _import_operator(store, om, counts)

    ref_globs = list((profile_dir / "skills").glob("**/references/*.md"))
    docs_refs = profile_dir.parent / "docs" / "references"
    if docs_refs.exists():
        ref_globs += list(docs_refs.glob("*.md"))
    for ref in ref_globs:
        name = ref.name.lower()
        if any(d in name for d in _DENYLIST):
            counts["skipped"].append(str(ref.name))
            continue
        try:
            rel = str(ref.relative_to(profile_dir.parent))
        except ValueError:
            rel = ref.name
        _import_reference(store, ref, rel, counts)
        counts["files"] += 1

    return counts
