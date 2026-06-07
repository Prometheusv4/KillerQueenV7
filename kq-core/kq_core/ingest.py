"""Phase 2 — ingest curated knowledge into the kb_chunks store (local-only, no fetch).

Sources (all on disk, operator-provided):
  * Killer Queen profile skills (SKILL.md files — 38 skills)
  * Killer Queen reference documents (docs/references/ — 105+ files)
  * SOUL.md — identity + knowledge synthesis
  * Payload catalogues (PayloadsAllTheThings, HackTricks, Seclists)
  * Technique catalogues (extracted from SOUL.md and references)

Collections:
  kq_skill        — SKILL.md files from profile/skills/
  kq_reference    — reference documents from docs/references/
  soul            — SOUL.md identity + knowledge synthesis
  payload         — raw payload catalogues
  technique       — structured technique catalogues

Idempotent: kb_chunks dedups by content hash, so re-ingesting is safe.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, List, Optional, Tuple

import yaml

# ═══════════════════════════════════════════════════════════════
# HELPERS (shared with original ingest)
# ═══════════════════════════════════════════════════════════════

def _frontmatter(md: str) -> Tuple[dict, str]:
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            try:
                data = yaml.safe_load(md[3:end].strip()) or {}
            except yaml.YAMLError:
                data = {}
            body = md[end + 4:].lstrip("\n")
            if isinstance(data, dict):
                return data, body
    return {}, md


def _chunks(body: str, max_chars: int = 1500) -> List[Tuple[Optional[str], str]]:
    """Split markdown body by ##/### headings into (title, content) pairs."""
    secs: List[Tuple[Optional[str], str]] = []
    cur_title, buf = None, []
    for line in body.splitlines():
        m = re.match(r"^(#{2,6})\s+(.*)$", line)
        if m:
            if buf or cur_title:
                secs.append((cur_title, "\n".join(buf).strip()))
            cur_title, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    if buf or cur_title:
        secs.append((cur_title, "\n".join(buf).strip()))
    if not secs:
        secs = [(None, body.strip())]

    out: List[Tuple[Optional[str], str]] = []
    for title, text in secs:
        text = (text or "").strip()
        if not text:
            continue
        if len(text) <= max_chars:
            out.append((title, text))
        else:
            for i in range(0, len(text), max_chars):
                out.append((title, text[i:i + max_chars]))
    return out


def _join(*lists) -> Optional[str]:
    vals: List[str] = []
    for lst in lists:
        if not lst:
            continue
        if isinstance(lst, str):
            vals.append(lst)
        else:
            vals.extend(str(x) for x in lst)
    seen, out = set(), []
    for v in vals:
        v = v.strip()
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return ",".join(out) if out else None


def _bump(counts: dict, action: str) -> None:
    counts[action] = counts.get(action, 0) + 1


# ═══════════════════════════════════════════════════════════════
# VULN CLASS INFERENCE FROM TEXT
# ═══════════════════════════════════════════════════════════════

_VULN_CLASS_KEYWORDS: dict[str, list[str]] = {
    "sqli": ["sql injection", "sqli", "union select", "blind sql", "stacked query"],
    "xss": ["cross site script", "xss", "stored xss", "reflected xss", "dom xss"],
    "ssrf": ["server side request forgery", "ssrf", "cloud metadata", "imds"],
    "idor": ["insecure direct object", "idor", "broken access", "authorization bypass"],
    "lfi": ["local file inclusion", "lfi", "path traversal", "directory traversal"],
    "file-upload": ["file upload", "unrestricted upload", "polyglot", "magic byte"],
    "deserialization": ["deseriali", "unserialize", "gadget chain", "ysoserial"],
    "ssti": ["server side template", "ssti", "jinja2", "twig", "freemarker"],
    "xxe": ["xml external entity", "xxe", "xinclude"],
    "cmdi": ["command injection", "cmdi", "os command"],
    "http-smuggling": ["request smuggling", "http desync", "cl.te", "te.cl"],
    "cache-attack": ["cache poison", "web cache deception", "host header injection"],
    "xs-leak": ["xs leak", "side channel", "frame counting"],
    "postmessage": ["postmessage", "post message", "origin bypass"],
    "saml": ["saml", "signature wrapping", "assertion injection"],
    "cloud-iam": ["iam privilege", "passrole", "putuserpolicy", "attachuserpolicy", "aws sts"],
    "ad-attack": ["kerberoast", "asreproast", "dcsync", "bloodhound", "pass the hash",
                  "golden ticket", "silver ticket", "dacl", "active directory"],
    "malware-dev": ["shellcode", "payload generation", "process injection", "edr bypass",
                    "amsi bypass", "c2 framework", "rat builder"],
    "embedded": ["firmware", "binwalk", "uart", "jtag", "spi flash", "iot device",
                 "uefi", "bootkit", "ics", "scada", "modbus"],
    "ics-scada": ["scada", "modbus", "opc ua", "siemens s7", "plc exploit"],
    "wireless-wifi": ["wpa2", "wpa3", "aircrack", "handshake", "evil twin", "pmkid"],
    "wireless-rf": ["sdr", "hackrf", "rtl-sdr", "gnuradio", "rolljam"],
    "wireless-ble": ["bluetooth low energy", "ble long range", "btlejack", "nrf52", "gatt exploit"],
    "wireless-rfid": ["rfid", "nfc", "proxmark"],
    "social-eng": ["phishing", "spearphish", "vishing", "smishing", "social engineering"],
    "recon": ["reconnaissance", "subdomain", "enumeration", "attack surface", "osint"],
    "methodology": ["bug bounty", "hackerone", "orange tsai", "parser differential",
                    "responsible disclosure"],
    "kubernetes": ["kubernetes", "k8s", "kubelet", "container escape"],
    "cloud-storage": ["s3 bucket", "blob storage", "cloud storage"],
    "c2": ["command and control", "c2 framework"],
    "lateral-movement": ["lateral movement", "psexec", "wmiexec", "smbexec"],
    "persistence": ["persistence", "scheduled task", "registry run key", "dll hijack"],
    "exfiltration": ["exfiltration", "dns tunneling", "icmp tunnel"],
}


def infer_vuln_class(text: str, source: str = "") -> Optional[str]:
    """Infer vulnerability class from text content and source path."""
    low = text.lower()
    hits: dict[str, int] = {}
    for vc, keywords in _VULN_CLASS_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in low)
        if score > 0:
            hits[vc] = score
    # Also check source path for hints
    source_low = source.lower()
    for vc in _VULN_CLASS_KEYWORDS:
        if vc.replace("-", "") in source_low or vc in source_low:
            hits[vc] = hits.get(vc, 0) + 2
    if hits:
        return max(hits.keys(), key=lambda k: hits[k])
    return None


def infer_category_from_skill_path(skill_path: str) -> str:
    """Infer category from skill directory structure."""
    if "exploitation" in skill_path:
        # Further refine
        if any(x in skill_path.lower() for x in ["cloud", "iam"]):
            return "cloud"
        if any(x in skill_path.lower() for x in ["ad", "active-directory", "windows-red"]):
            return "ad"
        if any(x in skill_path.lower() for x in ["web", "xss", "sqli", "ssrf", "wordpress"]):
            return "web"
        if any(x in skill_path.lower() for x in ["c2", "malware", "evasion"]):
            return "malware"
        if any(x in skill_path.lower() for x in ["wireless", "rf", "ble"]):
            return "wireless"
        if any(x in skill_path.lower() for x in ["firmware", "embedded", "iot"]):
            return "embedded"
        if any(x in skill_path.lower() for x in ["social"]):
            return "social-eng"
        if any(x in skill_path.lower() for x in ["mobile", "android", "ios"]):
            return "mobile"
        if any(x in skill_path.lower() for x in ["browser", "pwn2own", "binary", "exploit-dev"]):
            return "binary"
        return "exploitation"
    if "methodology" in skill_path:
        return "methodology"
    if "playbooks" in skill_path:
        return "playbook"
    if "security" in skill_path:
        return "security"
    return "unknown"


# ═══════════════════════════════════════════════════════════════
# COLLECTION HANDLERS
# ═══════════════════════════════════════════════════════════════

def _walk_skill_files(root: Path) -> list[Path]:
    """Walk a skills directory following symlinks (Python 3.11 compat).

    Path.rglob() doesn't follow directory symlinks until Python 3.12.
    """
    skill_files: list[Path] = []
    for cat_dir in sorted(root.iterdir()):
        if cat_dir.is_dir() or cat_dir.is_symlink():
            for skill_dir in sorted(cat_dir.iterdir()):
                if skill_dir.is_dir() or skill_dir.is_symlink():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        skill_files.append(skill_md)
    return skill_files


def ingest_kq_skills(store: Any, root: Path | str, limit: Optional[int] = None) -> dict:
    """Ingest Killer Queen profile skills (SKILL.md files).

    Root should be kb_sources/skills/ directory.
    Each SKILL.md gets:
      - frontmatter extracted (name, description, tags)
      - section-level chunking (## and ### headings)
      - vuln_class inferred from content
      - collection='kq_skill'
      - tags from frontmatter + path-inferred category
    """
    root = Path(root)
    counts = {"files": 0, "inserted": 0, "duplicate": 0, "errors": 0}
    skill_files = _walk_skill_files(root)

    if limit:
        skill_files = skill_files[:limit]

    for sk in skill_files:
        try:
            raw = sk.read_text(encoding="utf-8", errors="replace")
        except Exception:
            counts["errors"] += 1
            continue

        fm, body = _frontmatter(raw)
        skill_name = str(fm.get("name") or sk.parent.name)
        description = str(fm.get("description") or "").strip()

        # Build relative path for source tracking
        try:
            rel = str(sk.relative_to(root))
        except ValueError:
            rel = str(sk)

        # Infer metadata
        fm_tags = _join(fm.get("tags"), [infer_category_from_skill_path(rel)])
        fm_vuln = str(fm.get("vuln_class") or "")
        source_confidence = 0.85 if "exploitation" in rel else 0.75  # skills are curated

        idx = 0

        # Insert description as first chunk if present
        if description:
            vc = fm_vuln or infer_vuln_class(description, rel)
            r = store.put_kb_chunk(
                collection="kq_skill",
                source=skill_name,
                title=skill_name,
                content=description,
                chunk_index=idx,
                vuln_class=vc,
                tags=fm_tags,
            )
            _bump(counts, r["action"])
            idx += 1

        # Insert body sections as chunks
        for title, content in _chunks(body):
            vc = fm_vuln or infer_vuln_class(content, rel)
            r = store.put_kb_chunk(
                collection="kq_skill",
                source=skill_name,
                title=title or skill_name,
                content=content,
                chunk_index=idx,
                vuln_class=vc,
                tags=fm_tags,
            )
            _bump(counts, r["action"])
            idx += 1

        counts["files"] += 1

    return counts


def ingest_kq_references(store: Any, root: Path | str, limit: Optional[int] = None) -> dict:
    """Ingest Killer Queen reference documents (docs/references/*.md).

    Each reference gets:
      - Section-level chunking (max 2000 chars — references are denser)
      - vuln_class inferred from content
      - collection='kq_reference'
      - source set to filename (traceable)
    """
    root = Path(root)
    counts = {"files": 0, "inserted": 0, "duplicate": 0, "errors": 0}

    ref_files = sorted(root.glob("*.md"))
    if limit:
        ref_files = ref_files[:limit]

    for ref in ref_files:
        try:
            raw = ref.read_text(encoding="utf-8", errors="replace")
        except Exception:
            counts["errors"] += 1
            continue

        source = ref.stem
        doc_title = source.replace("-", " ").replace("_", " ").title()

        idx = 0
        # Use larger chunks for references (2000 chars)
        for title, content in _chunks(raw, max_chars=2000):
            vc = infer_vuln_class(content, source)
            r = store.put_kb_chunk(
                collection="kq_reference",
                source=source,
                title=title or doc_title,
                content=content,
                chunk_index=idx,
                vuln_class=vc,
                tags=f"reference,source:{source}",
            )
            _bump(counts, r["action"])
            idx += 1

        counts["files"] += 1

    return counts


def ingest_soul(store: Any, path: Path | str) -> dict:
    """Ingest SOUL.md — identity + knowledge synthesis.

    Special handling:
      - Top-level sections → collection='soul', tags='identity'
      - Orange Tsai sections → tags='methodology,orange-tsai'
      - Tool catalogue sections → tags='arsenal'
      - Chain descriptions → tags='chain_pattern'
      - Domain-specific sections → vuln_class from section name
    """
    path = Path(path)
    counts = {"files": 0, "inserted": 0, "duplicate": 0, "errors": 0}

    if not path.exists():
        return {**counts, "skipped": "SOUL.md not found"}

    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        counts["errors"] += 1
        return counts

    counts["files"] = 1

    # Track which top-level section we're in for tag assignment
    current_top_section = "identity"

    idx = 0
    for title, content in _chunks(raw, max_chars=1500):
        # Infer tags from section context
        if title:
            title_low = title.lower()
            if any(kw in title_low for kw in ["orange tsai", "parser", "confusion"]):
                current_top_section = "orange-tsai"
            elif any(kw in title_low for kw in ["tool", "arsenal", "catalogue"]):
                current_top_section = "arsenal"
            elif any(kw in title_low for kw in ["chain", "exploit chain", "attack path"]):
                current_top_section = "chain"
            elif any(kw in title_low for kw in ["web application", "web attack"]):
                current_top_section = "web"
            elif any(kw in title_low for kw in ["cloud", "aws", "azure", "gcp"]):
                current_top_section = "cloud"
            elif any(kw in title_low for kw in ["active directory", "ad attack"]):
                current_top_section = "ad"
            elif any(kw in title_low for kw in ["malware", "c2", "payload"]):
                current_top_section = "malware"
            elif any(kw in title_low for kw in ["embedded", "iot", "firmware", "ics"]):
                current_top_section = "embedded"
            elif any(kw in title_low for kw in ["wireless", "rf", "wifi", "bluetooth"]):
                current_top_section = "wireless"
            elif any(kw in title_low for kw in ["social", "phishing"]):
                current_top_section = "social-eng"
            elif any(kw in title_low for kw in ["0-day", "project zero", "pwn2own"]):
                current_top_section = "0day"
            elif any(kw in title_low for kw in ["bug bounty", "hackerone", "methodology"]):
                current_top_section = "methodology"

        # Build tags
        section_tags = f"soul,section:{current_top_section}"
        if current_top_section == "orange-tsai":
            section_tags += ",methodology,orange-tsai"
        elif current_top_section == "arsenal":
            section_tags += ",arsenal,tool-catalogue"

        vc = infer_vuln_class(content, current_top_section)

        r = store.put_kb_chunk(
            collection="soul",
            source="SOUL.md",
            title=title or f"soul:{current_top_section}",
            content=content,
            chunk_index=idx,
            vuln_class=vc,
            tags=section_tags,
        )
        _bump(counts, r["action"])
        idx += 1

    return counts


def ingest_payloads_all_the_things(store: Any, root: Path | str, limit: Optional[int] = None) -> dict:
    """Ingest PayloadsAllTheThings payload catalogues.

    Expects root to be the directory containing .md files organized by category.
    Each .md file is a payload catalogue for a specific vulnerability class.
    """
    root = Path(root)
    counts = {"files": 0, "inserted": 0, "duplicate": 0, "errors": 0}

    payload_files = sorted(root.rglob("*.md"))
    if limit:
        payload_files = payload_files[:limit]

    for pf in payload_files:
        try:
            raw = pf.read_text(encoding="utf-8", errors="replace")
        except Exception:
            counts["errors"] += 1
            continue

        vc = infer_vuln_class(str(pf), str(pf.parent.name))
        if not vc:
            vc = pf.parent.name.lower().replace(" ", "-").replace("_", "-")

        source = f"payloads:{pf.stem}"
        idx = 0
        for title, content in _chunks(raw, max_chars=2000):
            r = store.put_kb_chunk(
                collection="payload",
                source=source,
                title=title or pf.stem,
                content=content,
                chunk_index=idx,
                vuln_class=vc,
                tags=f"payload,{vc}",
            )
            _bump(counts, r["action"])
            idx += 1

        counts["files"] += 1

    return counts


def ingest_technique_catalogue(store: Any, root: Path | str) -> dict:
    """Ingest structured technique catalogues from reference sections.

    Converts sections like:
      "### Kerberoasting
       - Impacket GetUserSPNs.py ...
       - Rubeus kerberoast ..."

    Into structured chunks with technique name and tools.
    """
    root = Path(root)
    counts = {"files": 0, "inserted": 0, "duplicate": 0, "errors": 0}

    ref_files = sorted(root.glob("*.md"))
    for ref in ref_files:
        if any(skip in ref.name.lower() for skip in ["readme", "index", "license"]):
            continue

        try:
            raw = ref.read_text(encoding="utf-8", errors="replace")
        except Exception:
            counts["errors"] += 1
            continue

        counts["files"] += 1
        idx = 0
        for title, content in _chunks(raw, max_chars=1500):
            vc = infer_vuln_class(content, ref.stem)
            r = store.put_kb_chunk(
                collection="technique",
                source=f"technique:{ref.stem}",
                title=title or ref.stem,
                content=content,
                chunk_index=idx,
                vuln_class=vc,
                tags=f"technique,catalogue,source:{ref.stem}",
            )
            _bump(counts, r["action"])
            idx += 1

    return counts


# ═══════════════════════════════════════════════════════════════
# ORIGINAL INGEST HANDLERS (preserved for backward compat)
# ═══════════════════════════════════════════════════════════════

def ingest_anthropic_skills(store: Any, root: Path | str, limit: Optional[int] = None) -> dict:
    root = Path(root)
    counts = {"files": 0, "inserted": 0, "duplicate": 0}
    skills = sorted(root.glob("skills/*/SKILL.md"))
    if limit:
        skills = skills[:limit]
    for sk in skills:
        fm, body = _frontmatter(sk.read_text(encoding="utf-8", errors="replace"))
        name = str(fm.get("name") or sk.parent.name)
        subdomain = fm.get("subdomain")
        tags = _join(fm.get("tags"), [subdomain] if subdomain else None, ["anthropic"])
        mitre = _join(fm.get("atlas_techniques"), fm.get("mitre_attack"), fm.get("d3fend_techniques"))
        nist = _join(fm.get("nist_csf"), fm.get("nist_ai_rmf"))
        idx = 0
        desc = str(fm.get("description") or "").strip()
        chunks = ([(name, desc)] if desc else []) + _chunks(body)
        for title, content in chunks:
            r = store.put_kb_chunk(collection="anthropic_skill", source=name, title=title or name,
                                   content=content, chunk_index=idx, mitre=mitre, nist=nist, tags=tags)
            _bump(counts, r["action"])
            idx += 1
        counts["files"] += 1
    return counts


def ingest_bughunter(store: Any, root: Path | str) -> dict:
    root = Path(root)
    counts = {"files": 0, "inserted": 0, "duplicate": 0}
    for sk in sorted(root.glob("skills/hunt-*/SKILL.md")):
        vc = sk.parent.name.replace("hunt-", "")
        fm, body = _frontmatter(sk.read_text(encoding="utf-8", errors="replace"))
        idx = 0
        for title, content in _chunks(body):
            r = store.put_kb_chunk(collection="hunt_pattern", source=sk.parent.name,
                                   title=title or sk.parent.name, content=content, chunk_index=idx,
                                   vuln_class=vc, tags="bughunter,hunt")
            _bump(counts, r["action"])
            idx += 1
        counts["files"] += 1
    for rep in sorted(root.glob("docs/disclosed-reports/hunt-*.md")):
        vc = rep.stem.replace("hunt-", "")
        _fm, body = _frontmatter(rep.read_text(encoding="utf-8", errors="replace"))
        idx = 0
        for title, content in _chunks(body):
            r = store.put_kb_chunk(collection="hunt_pattern", source="disclosed:" + rep.stem,
                                   title=title or rep.stem, content=content, chunk_index=idx,
                                   vuln_class=vc, tags="bughunter,disclosed")
            _bump(counts, r["action"])
            idx += 1
        counts["files"] += 1
    return counts


def ingest_shannon(store: Any, root: Path | str) -> dict:
    root = Path(root)
    counts = {"files": 0, "inserted": 0, "duplicate": 0}
    pdir = root / "apps" / "worker" / "prompts"
    for f in sorted(pdir.glob("shared/*.txt")):
        idx = 0
        for title, content in _chunks(f.read_text(encoding="utf-8", errors="replace")):
            r = store.put_kb_chunk(collection="scope", source="shannon:" + f.name, title=title or f.stem,
                                   content=content, chunk_index=idx, tags="shannon,scope")
            _bump(counts, r["action"])
            idx += 1
        counts["files"] += 1
    for f in sorted(list(pdir.glob("vuln-*.txt")) + list(pdir.glob("exploit-*.txt"))):
        vc = f.stem.split("-", 1)[1] if "-" in f.stem else None
        idx = 0
        for title, content in _chunks(f.read_text(encoding="utf-8", errors="replace")):
            r = store.put_kb_chunk(collection="methodology", source="shannon:" + f.name, title=title or f.stem,
                                   content=content, chunk_index=idx, vuln_class=vc, tags="shannon")
            _bump(counts, r["action"])
            idx += 1
        counts["files"] += 1
    return counts


# ═══════════════════════════════════════════════════════════════
# DEFAULT PATHS + INGEST ALL
# ═══════════════════════════════════════════════════════════════

def default_paths(repo_root: Optional[Path] = None) -> dict:
    """Best-guess on-disk locations for the curated corpora."""
    repo = Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
    kb_sources = repo / "kq-core" / "kb_sources"
    anthropic = Path.home() / "Downloads" / "Anthropic-Cybersecurity-Skills-main" / "Anthropic-Cybersecurity-Skills-main"
    return {
        "kb_skills": kb_sources / "skills" if (kb_sources / "skills").exists() else None,
        "kb_references": kb_sources / "references" if (kb_sources / "references").exists() else None,
        "kb_soul": kb_sources / "soul" if (kb_sources / "soul").exists() else None,
        "anthropic": anthropic if anthropic.exists() else None,
        "bughunter": repo / "Claude-BugHunter-main" if (repo / "Claude-BugHunter-main").exists() else None,
        "shannon": repo / "shannon-main" if (repo / "shannon-main").exists() else None,
    }


def ingest_all(
    store: Any,
    *,
    kb_skills: Optional[Path | str] = None,
    kb_references: Optional[Path | str] = None,
    kb_soul: Optional[Path | str] = None,
    payloads: Optional[Path | str] = None,
    techniques: Optional[Path | str] = None,
    anthropic: Optional[Path | str] = None,
    bughunter: Optional[Path | str] = None,
    shannon: Optional[Path | str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Run all available ingestion pipelines.

    Returns dict of collection → counts for each that ran.
    """
    result: dict = {}
    if kb_skills:
        result["kq_skill"] = ingest_kq_skills(store, kb_skills, limit=limit)
    if kb_references:
        result["kq_reference"] = ingest_kq_references(store, kb_references, limit=limit)
    if kb_soul:
        result["soul"] = ingest_soul(store, kb_soul)
    if payloads:
        result["payload"] = ingest_payloads_all_the_things(store, payloads, limit=limit)
    if techniques:
        result["technique"] = ingest_technique_catalogue(store, techniques)
    if anthropic:
        result["anthropic_skill"] = ingest_anthropic_skills(store, anthropic, limit=limit)
    if bughunter:
        result["bughunter"] = ingest_bughunter(store, bughunter)
    if shannon:
        result["shannon"] = ingest_shannon(store, shannon)
    return result
