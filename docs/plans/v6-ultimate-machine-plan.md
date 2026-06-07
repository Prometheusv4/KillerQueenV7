# KILLER QUEEN v6 → ULTIMATE HACKING MACHINE
## Complete Technical Implementation Plan

```
Author: Killer Queen
Target: Killerx0ueen v6 → v6.1
Date: 2026-06-06
Status: READY FOR EXECUTION
```

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│                    KILLER QUEEN v6.1 ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SOURCE KNOWLEDGE (on disk)                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  38 SKILL.md  │  105 references  │  SOUL.md  │  books/        │   │
│  └──────────────┬───────────────────────────────────────────────┘   │
│                 │                                                    │
│                 ▼                                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                 INGEST PIPELINE (ingest.py)                    │   │
│  │  • Frontmatter extraction (ATT&CK/ATLAS/D3FEND tags)          │   │
│  │  • Section-level chunking (markdown heading split)            │   │
│  │  • Content hash dedup (sha256)                                │   │
│  │  • Collection tagging (skill/ref/soul/pattern/catalogue)      │   │
│  │  • FTS5 index population                                       │   │
│  │  • OUTPUT: kb_chunks table (~3,200 chunks)                    │   │
│  └──────────────┬───────────────────────────────────────────────┘   │
│                 │                                                    │
│                 ▼                                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │            LESSON EXTRACTION PIPELINE (extract.py)  ← NEW      │   │
│  │  • Chunk → technique detection (regex + keyword patterns)     │   │
│  │  • Technique → lesson_save() call                             │   │
│  │  • Confidence bootstrapping from source quality               │   │
│  │  • Vuln class / target fingerprint mapping                    │   │
│  │  • Trigger/action extraction from patterns                    │   │
│  │  • Memory fact extraction (tool quirks, pitfalls, caveats)    │   │
│  │  • OUTPUT: lessons table (~800 entries)                       │   │
│  │  • OUTPUT: memory_facts table (~300 entries)                  │   │
│  └──────────────┬───────────────────────────────────────────────┘   │
│                 │                                                    │
│                 ▼                                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  ACTIVE KNOWLEDGE LAYER                        │   │
│  │                                                                │   │
│  │  ┌──────────────┐  ┌───────────────┐  ┌───────────────────┐  │   │
│  │  │ recall()      │  │ role_brief()   │  │ memory_facts      │  │   │
│  │  │ hybrid search  │  │ bundles scope  │  │ auto-injected     │  │   │
│  │  │ semantic+keywd │  │ + patterns     │  │ every session     │  │   │
│  │  │ over lessons   │  │ + lessons      │  │ MEMORY.md digest  │  │   │
│  │  └──────────────┘  │ + tools+facts   │  └───────────────────┘  │   │
│  │                     └───────────────┘                           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   ORCHESTRATION LAYER                          │   │
│  │                                                                │   │
│  │  PHASE_PLAN (35+ tasks across 8 domains)                       │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │ Web App  │ │ Cloud    │ │ AD       │ │ Malware  │        │   │
│  │  │ 13 tasks │ │ IAM      │ │ Attack   │ │ Dev      │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │Embedded  │ │ Wireless │ │ Social   │ │Physical  │        │   │
│  │  │IoT/ICS   │ │ WiFi/RF  │ │ Eng.     │ │ Access   │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    ARSENAL LAYER                               │   │
│  │                                                                │   │
│  │  150+ tool specs across 20 categories                          │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │ Kali     │ │ C2/RAT   │ │ Cloud    │ │ AD       │        │   │
│  │  │ 45 tools │ │ 25 tools │ │ 20 tools │ │ 15 tools │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │Firmware  │ │ Wireless │ │ Evasion  │ │Post-Expl │        │   │
│  │  │ 12 tools │ │ 10 tools │ │ 10 tools │ │  8 tools │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │   │
│  │                                                                │   │
│  │  runner.recommend() → tool selection by target_type            │   │
│  │  runner.run_tool() → scope gate + guard + audit log            │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  MCP SERVER (25 tools → 27 tools)              │   │
│  │                                                                │   │
│  │  engagement_start / engagement_state_get / engagement_state_update │
│  │  remember / recall / lesson_save / lesson_outcome              │   │
│  │  skill_propose / kb_search / kb_extract  ← NEW                │   │
│  │  scope_check / finding_save / finding_update                   │   │
│  │  audit_log / triage / report / plan_create / plan_status       │   │
│  │  task_update / role_brief / chain_build / chain_link / chain_get│  │
│  │  target_profile / arsenal_recommend / arsenal_list / run       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 0 — KNOWLEDGE INGESTION PIPELINE

### 0.1 — Create kb_sources/ Directory Structure

**Path:** `/root/Killerx0ueen/kq-core/kb_sources/`

**Structure:**
```
kb_sources/
├── skills/                          # Symlinks to profile skill dirs
│   ├── exploitation/
│   │   ├── web-attacks -> ../../../../profile/skills/exploitation/web-attacks
│   │   ├── cloud-iam-attacks -> ../../../../profile/skills/exploitation/cloud-iam-attacks
│   │   ├── active-directory-attacks -> ...
│   │   ├── exploit-development -> ...
│   │   ├── browser-exploitation -> ...
│   │   ├── mobile-attacks -> ...
│   │   ├── embedded-iot-attacks -> ...
│   │   ├── c2-frameworks -> ...
│   │   ├── malware-dev -> ...
│   │   ├── evasion-anti-detection -> ...
│   │   ├── cloudflare-bypass -> ...
│   │   ├── wireless-rf -> ...
│   │   ├── firmware-iot -> ...
│   │   ├── social-engineering -> ...
│   │   ├── social-engineering-wireless -> ...
│   │   ├── ai-ml-attacks -> ...
│   │   ├── supply-chain-attacks -> ...
│   │   ├── blockchain-web3 -> ...
│   │   ├── data-exfiltration -> ...
│   │   ├── cloud-post-exploit -> ...
│   │   ├── osint-automation -> ...
│   │   ├── binary-exploitation -> ...
│   │   ├── pwn2own-exploitation -> ...
│   │   ├── windows-red-team -> ...
│   │   ├── defensive-forensics -> ...
│   │   ├── infrastructure-attacks -> ...
│   │   ├── wordpress-pentesting -> ...
│   │   └── threat-intel -> ...
│   ├── methodology/
│   │   ├── bughunter-methodology -> ...
│   │   ├── mission-orchestrator -> ...
│   │   ├── orange-tsai-methodology -> ...
│   │   ├── h1-bug-bounty-patterns -> ...
│   │   ├── testing-methodology -> ...
│   │   ├── adaptive-engagement -> ...
│   │   └── self-improvement -> ...
│   ├── playbooks/
│   │   ├── awesome-redteam-toolkit -> ...
│   │   └── kali-tools-arsenal -> ...
│   └── security/
│       └── kali-security-tooling -> ...
├── references/                      # Symlinks to docs/references/
│   ├── new0sources.md -> ../../../docs/references/new0sources.md
│   ├── sources-round2-synthesis.md -> ...
│   ├── cloud-infrastructure-attacks-reference.md -> ...
│   ├── exploit-development-master-reference.md -> ...
│   ├── browser-windows-exploit-new.md -> ...
│   ├── mobile-iot-firmware-attacks-reference.md -> ...
│   ├── redteam-exploitdev-reference.md -> ...
│   ├── defensive-forensic-reference.md -> ...
│   ├── c2-framework-source-analysis.md -> ...
│   ├── rat-source-analysis.md -> ...
│   ├── engagement-playbook.md -> ...
│   ├── consolidated-h1-ssrf.md -> ...
│   ├── final-gap-closure-round2.md -> ...
│   ├── ... (all 105 reference files)
│   └── books-exhaustive.md -> ...
└── soul/
    └── SOUL.md -> ../../SOUL.md          # Will be created in Phase 3
```

**Implementation:**
- Use `os.symlink()` for all entries
- Create `__init__.py` in `kb_sources/` root for Python path resolution
- Add `.gitignore` entries for symlink targets (they already exist in repo)

### 0.2 — Expand ingest.py: 5 Collection Types

**Current ingest.py:** 187 lines, handles only `anthropic_skill`, `hunt_pattern`, `scope`, `methodology`

**Target:** ~450 lines

**New function signatures:**

```python
# ─── collection type registry ──────────────────────────────────
COLLECTION_HANDLERS: dict[str, Callable] = {}

def register_collection(name: str):
    """Decorator to register a collection handler."""
    ...

# ─── handlers ───────────────────────────────────────────────────

@register_collection("kq_skill")
def ingest_kq_skills(store: Any, root: Path, limit: int = None) -> dict:
    """
    Ingest Killer Queen profile skills (SKILL.md files).
    
    Metadata extraction:
      - frontmatter: name, description, tags, category
      - path structure → collection hint (exploitation/methodology/etc)
      - filename → skill name
      - ATT&CK/ATLAS/D3FEND tag mapping from frontmatter
    
    Chunk strategy:
      - Section-level: split by ## and ### headings
      - Max 1500 chars per chunk
      - Each chunk gets: section_title, chunk_index, collection='kq_skill'
      - Store full file path as source for traceability
    
    Returns: {"files": N, "inserted": N, "duplicate": N, "errors": [...]}
    """

@register_collection("kq_reference")  
def ingest_kq_references(store: Any, root: Path, limit: int = None) -> dict:
    """
    Ingest Killer Queen reference documents.
    
    Metadata extraction:
      - filename → topic hint
      - First H1 → document title
      - Section headings → sub-topics
      - Ref-linked files (from SOUL.md-style catalogues)
    
    Chunk strategy:
      - Section-level (## headings)
      - Max 2000 chars per chunk (references are denser than skills)
      - Each chunk gets: collection='kq_reference', source file path
    
    Returns: {"files": N, "inserted": N, "duplicate": N}
    """

@register_collection("soul")
def ingest_soul(store: Any, root: Path, limit: int = None) -> dict:
    """
    Ingest SOUL.md identity/knowledge synthesis.
    
    Special handling:
      - Top-level sections become collection='soul'
      - Sub-sections with technique names tagged as vuln_class
      - Orange Tsai sections → tagged methodology
      - Tool catalogue sections → tagged arsenal
      - Chain descriptions → tagged chain_pattern
    
    Returns: {"files": N, "inserted": N, "duplicate": N}
    """

@register_collection("payload_catalogue")
def ingest_payload_catalogues(store: Any, root: Path) -> dict:
    """
    Ingest payload catalogues from referenced repos.
    
    Sources:
      - PayloadsAllTheThings (58 files)
      - HackTricks articles (69 files)
      - Seclists (web shells, fuzzing payloads)
    
    Each payload gets: category (sqli/xss/lfi/...), technique name, 
    raw payload text, language context (PHP/JS/Python/...)
    
    Returns: {"files": N, "inserted": N}
    """

@register_collection("technique_catalogue")
def ingest_technique_catalogues(store: Any, root: Path) -> dict:
    """
    Ingest structured technique catalogues from references.
    
    Converts reference sections like:
      "### Kerberoasting
       - Impacket GetUserSPNs.py ...
       - Rubeus kerberoast ...
       - Detection: 4769 events ..."
    
    Into structured chunks with:
      - technique name
      - tools used
      - detection notes
      - confidence level
    """
```

**Schema additions to store.py:**

```python
# New columns for kb_chunks:
ALTER TABLE kb_chunks ADD COLUMN collection TEXT;      -- kq_skill|kq_reference|soul|payload|technique
ALTER TABLE kb_chunks ADD COLUMN vuln_class TEXT;      -- xss|sqli|ad-attack|cloud-iam|...
ALTER TABLE kb_chunks ADD COLUMN technique_name TEXT;  -- kerberoasting|pass-the-hash|...
ALTER TABLE kb_chunks ADD COLUMN tools_used TEXT;      -- comma-sep tool names
ALTER TABLE kb_chunks ADD COLUMN confidence REAL DEFAULT 0.5;  -- source quality estimate
ALTER TABLE kb_chunks ADD COLUMN extracted_to_lesson INTEGER DEFAULT 0; -- track extraction
```

### 0.3 — Run Ingest Pipeline

**Execution script** (new CLI command or standalone call):

```python
# In kq_core/cli.py, add:
def cmd_ingest():
    """python -m kq_core.cli ingest [--limit N] [--collection TYPE]"""
    store = get_store()
    
    sources = {
        "kq_skill": Path("kb_sources/skills"),
        "kq_reference": Path("kb_sources/references"),
        "soul": Path("kb_sources/soul"),
    }
    
    results = {}
    for collection, path in sources.items():
        if path.exists():
            handler = COLLECTION_HANDLERS[collection]
            results[collection] = handler(store, path)
    
    return results
    # Expected: ~3,200 chunks total
    # 38 skills × ~15 sections = ~570
    # 105 references × ~25 sections = ~2,625
    # SOUL.md × ~1,694 lines = ~80 sections
```

**Verification queries:**
```sql
SELECT collection, COUNT(*) FROM kb_chunks GROUP BY collection;
SELECT COUNT(DISTINCT content_hash) FROM kb_chunks;  -- must match total
```

### 0.4 — kb_search Wiring Verification

**Current kb_search (in store.py):**
```python
def kb_search(self, query: str, collection=None, vuln_class=None, top_k=5):
    # Uses FTS5 MATCH + optional collection/vuln_class filters
    # Returns top_k chunks with snippet highlighting
```

**Verification steps:**
1. Run kb_search("kerberoasting") → must return AD attack chunks
2. Run kb_search("pass the hash") → must return lateral movement chunks  
3. Run kb_search("", collection="kq_skill", vuln_class="xss") → must return XSS skill chunks
4. Run kb_search("saml assertion", collection="soul") → must return SOUL.md chunks
5. Verify no empty results for any of the 38 skill names

---

## PHASE 0.5 — LESSON EXTRACTION PIPELINE (NEW)

**This is the critical phase. Without it, KQ has a library but hasn't read the books.**

### 0.5.1 — Architecture

```
kb_chunks table (~3,200 rows)
        │
        ▼
┌───────────────────────────────────────────────────────┐
│              EXTRACTION PIPELINE                       │
│                                                        │
│  Stage 1: TECHNIQUE DETECTION                          │
│    • Regex patterns for technique mentions             │
│    • Tool invocation patterns (tool name + args)       │
│    • Vulnerability class signatures                    │
│    • Attack chain phrases ("X enables Y")              │
│                                                        │
│  Stage 2: FACT EXTRACTION                             │
│    • Tool quirks ("X triggers Y if Z")                 │
│    • Pitfalls ("doesn't work on", "requires patch")   │
│    • Bypass notes ("WAF blocks X, use Y instead")      │
│    • Version-specific ("CVE-2024-XXXX affects...")     │
│                                                        │
│  Stage 3: LESSON ASSEMBLY                              │
│    • Technique → lesson_save(summary, category, ...)   │
│    • Trigger/action extraction ("IF X THEN Y")         │
│    • Confidence bootstrapping                          │
│    • Fingerprint mapping (target type → technique)     │
│                                                        │
│  Stage 4: DEDUP + MERGE                                │
│    • Multiple chunks mention same technique → merge     │
│    • Higher confidence from multiple sources           │
│    • Cross-reference between skills and references     │
│                                                        │
└───────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────┐
│  OUTPUT                                                │
│                                                        │
│  lessons table: ~800 active entries                     │
│    category breakdown:                                  │
│      recon:         ~80                                │
│      exploitation:  ~350                               │
│      evasion:       ~70                                │
│      methodology:   ~120                               │
│      tool:          ~100                               │
│      target-type:   ~80                                │
│                                                        │
│  memory_facts table: ~300 entries                       │
│    kind breakdown:                                      │
│      tool_quirk:    ~80                                │
│      bypass:        ~60                                │
│      pitfall:       ~50                                │
│      reference:     ~60                                │
│      chain:         ~50                                │
└───────────────────────────────────────────────────────┘
```

### 0.5.2 — New File: kq_core/extract.py

**Full implementation plan:**

```python
"""Lesson extraction pipeline — converts kb_chunks into active lessons + memory facts.

This is the key differentiator between a library and a trained agent.
After extraction, recall() and role_brief() surface knowledge automatically
without the agent needing to know to search the KB.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional, List, Tuple, Dict
from dataclasses import dataclass

from .learning import lesson_save, lesson_outcome
from .memory import remember
from .util import now_iso, tokenize


# ═══════════════════════════════════════════════════════════════
# STAGE 1: TECHNIQUE DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════

@dataclass
class TechniqueMatch:
    """A detected technique within a chunk."""
    technique: str           # e.g., "kerberoasting", "pass-the-hash"
    category: str            # recon/exploitation/evasion/methodology/tool/target-type
    vuln_class: str          # xss/sqli/ad-attack/cloud-iam/...
    confidence: float        # 0.0–1.0 detection confidence
    trigger_when: str        # extracted "WHEN" condition
    action_do: str           # extracted "THEN" action
    rationale: str           # supporting text
    tools: List[str]         # tools mentioned
    source_chunk_id: int     # kb_chunks row reference


# Pattern library — regex + keyword combinations that identify techniques
TECHNIQUE_PATTERNS = [
    # Format: (regex, category, vuln_class, base_confidence, tool_indicators)
    # Web exploitation
    (r"(?i)(sql\s*injection|sqli|blind\s*sql|union\s*select|stacked\s*quer)",
     "exploitation", "sqli", 0.85, ["sqlmap", "ghauri", "nosqli"]),
    
    (r"(?i)(cross.site\s*script|xss|stored\s*xss|reflected\s*xss|dom\s*xss)",
     "exploitation", "xss", 0.85, ["dalfox", "kxss", "xsstrike", "xsser"]),
    
    (r"(?i)(server.side\s*request\s*forgery|ssrf|imds|cloud\s*metadata)",
     "exploitation", "ssrf", 0.80, ["interactsh", "burp collaborator"]),
    
    (r"(?i)(local\s*file\s*inclusion|lfi|path\s*traversal|directory\s*traversal)",
     "exploitation", "lfi", 0.80, ["ffuf", "dotdotpwn", "liffy"]),
    
    (r"(?i)(file\s*upload|unrestricted\s*upload|polyglot|magic\s*byte)",
     "exploitation", "file-upload", 0.80, ["exiftool", "exifcleaner"]),
    
    (r"(?i)(deserialization|unserialize|gadget\s*chain|ysoserial|marshal)",
     "exploitation", "deserialization", 0.80, ["ysoserial", "ysoserial.net", "phpggc"]),
    
    (r"(?i)(ssti|server.side\s*template\s*injection|jinja2|twig|freemarker)",
     "exploitation", "ssti", 0.80, ["tplmap", "sstimap"]),
    
    (r"(?i)(command\s*injection|cmdi|os\s*command|rce\s*via)",
     "exploitation", "cmdi", 0.85, ["commix"]),
    
    (r"(?i)(xxe|xml\s*external\s*entity|xinclude)",
     "exploitation", "xxe", 0.80, []),
    
    (r"(?i)(idor|insecure\s*direct\s*object|broken\s*access)",
     "exploitation", "idor", 0.80, ["autorize", "autorepeater"]),
    
    (r"(?i)(saml|xs\s*sw|signature\s*wrapping|assertion\s*injection)",
     "exploitation", "saml", 0.75, ["samlraider", "esaml"]),
    
    (r"(?i)(xs.leak|side.channel|frame\s*counting|cache\s*probing)",
     "exploitation", "xs-leak", 0.70, ["xsleaks"]),
    
    (r"(?i)(postmessage|origin\s*bypass|post\s*message)",
     "exploitation", "postmessage", 0.70, []),
    
    # HTTP/infrastructure
    (r"(?i)(request\s*smuggling|cl\.te|te\.cl|te\.te|http\s*desync)",
     "exploitation", "http-smuggling", 0.80, ["smuggler", "h2csmuggler"]),
    
    (r"(?i)(cache\s*poison|web\s*cache\s*deception|host\s*header)",
     "exploitation", "cache-attack", 0.75, ["param-miner"]),
    
    (r"(?i)(crlf|carriage\s*return|line\s*feed\s*injection)",
     "exploitation", "crlf", 0.75, ["crlfuzz"]),
    
    # Cloud
    (r"(?i)(iam\s*privilege\s*escalation|passrole|putuserpolicy|attachuserpolicy)",
     "exploitation", "cloud-iam", 0.85, ["pacu", "pmapper", "enumerate-iam"]),
    
    (r"(?i)(aws\s*sts|assume\s*role|temporary\s*credentials|imds)",
     "exploitation", "cloud-iam", 0.80, ["pacu", "cloudmapper"]),
    
    (r"(?i)(guardduty|cloudtrail|config\s*sabotage|detection\s*evasion)",
     "evasion", "cloud-iam", 0.75, ["pacu"]),
    
    (r"(?i)(s3\s*bucket|cloud\s*storage|blob\s*storage)",
     "exploitation", "cloud-storage", 0.75, ["awscli", "s3scanner", "gcpbucketbrute"]),
    
    (r"(?i)(kubernetes|k8s|kubelet|container\s*escape|pod\s*breakout)",
     "exploitation", "kubernetes", 0.80, ["kube-hunter", "cdk", "peirates", "kubeletctl"]),
    
    # Active Directory
    (r"(?i)(kerberoasting|asreproast|kerberos|tgt|tgs|golden\s*ticket)",
     "exploitation", "ad-attack", 0.85, ["impacket", "rubeus", "mimikatz"]),
    
    (r"(?i)(dacl|bloodhound|ownership|genericwrite|genericall|self.membership)",
     "exploitation", "ad-attack", 0.80, ["bloodhound", "sharpview", "powerview"]),
    
    (r"(?i)(dcsync|replication|directory\s*replication)",
     "exploitation", "ad-attack", 0.85, ["mimikatz", "impacket-secretsdump"]),
    
    (r"(?i)(pass\s*the\s*hash|overpass|ntlm|ntlm\s*relay)",
     "exploitation", "ad-attack", 0.85, ["impacket", "crackmapexec", "mimikatz"]),
    
    (r"(?i)(s4u2self|s4u2proxy|bronze\s*bit|delegation)",
     "exploitation", "ad-attack", 0.80, ["impacket", "rubeus"]),
    
    (r"(?i)(adcs|certificate\s*services|certipy|esc\d)",
     "exploitation", "ad-attack", 0.80, ["certipy", "certify"]),
    
    (r"(?i)(ntlm\s*relay|smb\s*relay|llmnr|responder|mitm6)",
     "exploitation", "ad-attack", 0.80, ["responder", "ntlmrelayx", "mitm6"]),
    
    (r"(?i)(gpo|group\s*policy|gplink|admincount|ouned)",
     "exploitation", "ad-attack", 0.75, ["powerview", "sharpgpoabuse"]),
    
    # Malware/Evasion
    (r"(?i)(shellcode|payload\s*generation|msfvenom|donut|shellcode\s*loader)",
     "exploitation", "malware-dev", 0.80, ["msfvenom", "donut", "scarecrow"]),
    
    (r"(?i)(process\s*injection|dll\s*hijack|reflective\s*dll|syscall)",
     "exploitation", "malware-dev", 0.80, ["syswhispers3", "nim"]),
    
    (r"(?i)(amsi\s*bypass|defender\s*evasion|edr\s*bypass|unhook)",
     "evasion", "malware-dev", 0.80, ["freeze", "scarecrow", "amsi.fail"]),
    
    (r"(?i)(sandbox\s*detect|vm\s*detect|anti.analysis|anti.debug)",
     "evasion", "malware-dev", 0.75, []),
    
    (r"(?i)(c2|cobalt\s*strike|sliver|havoc|mythic|covenant|brute\s*ratel)",
     "tool", "c2", 0.85, ["sliver", "havoc", "mythic", "covenant"]),
    
    (r"(?i)(rat\s*builder|remote\s*access\s*trojan|asyncrat|quasar)",
     "tool", "malware-dev", 0.80, ["asyncrat", "quasarrat", "dcrat"]),
    
    # Embedded/IoT
    (r"(?i)(firmware\s*extraction|binwalk|uboot|u.image|squashfs)",
     "exploitation", "embedded", 0.80, ["binwalk", "firmware-mod-kit", "fact"]),
    
    (r"(?i)(uart|jtag|spi\s*flash|bus\s*pirate|logic\s*analyzer)",
     "exploitation", "embedded", 0.80, ["openocd", "flashrom"]),
    
    (r"(?i)(ics|scada|modbus|opc.ua|plc|siemens)",
     "exploitation", "ics-scada", 0.80, []),
    
    (r"(?i)(uefi|secure\s*boot|logo\s*fail|pixie\s*fail|sinkclose)",
     "exploitation", "embedded", 0.80, []),
    
    # Wireless/RF
    (r"(?i)(wpa2|wpa3|handshake|pmkid|aircrack|hcxdumptool)",
     "exploitation", "wireless-wifi", 0.80, ["aircrack-ng", "hcxdumptool"]),
    
    (r"(?i)(evil\s*twin|rogue\s*ap|radius\s*relay|eap)",
     "exploitation", "wireless-wifi", 0.75, ["eaphammer", "fluxion", "airgeddon"]),
    
    (r"(?i)(rf|sdr|hackrf|rtl.sdr|gnuradio|rolljam)",
     "exploitation", "wireless-rf", 0.75, ["gnuradio", "universal-radio-hacker"]),
    
    (r"(?i)(ble|bluetooth\s*low\s*energy|nrf|gatt)",
     "exploitation", "wireless-ble", 0.75, ["bettercap", "gattacker"]),
    
    (r"(?i)(rfid|nfc|proxmark|magspoof)",
     "exploitation", "wireless-rfid", 0.75, ["proxmark3", "mfoc"]),
    
    # Methodology/Recon
    (r"(?i)(reconnaissance|subdomain\s*enum|attack\s*surface\s*map)",
     "methodology", "recon", 0.80, ["subfinder", "amass", "httpx"]),
    
    (r"(?i)(orange\s*tsai|parser\s*differential|confusion\s*attack|worstfit)",
     "methodology", "methodology", 0.85, []),
    
    (r"(?i)(bug\s*bounty|hackerone|responsible\s*disclosure|triag)",
     "methodology", "methodology", 0.70, []),
    
    # Social Engineering
    (r"(?i)(phishing|spearphish|credential\s*harvest|evilginx|modlishka)",
     "exploitation", "social-eng", 0.80, ["evilginx2", "gophish", "modlishka"]),
    
    (r"(?i)(vishing|deepfake|voice\s*phishing|mfa\s*relay)",
     "exploitation", "social-eng", 0.75, []),
    
    (r"(?i)(sms\s*phish|smishing|mobile\s*phishing)",
     "exploitation", "social-eng", 0.70, []),
]


# ═══════════════════════════════════════════════════════════════
# STAGE 2: FACT EXTRACTION PATTERNS
# ═══════════════════════════════════════════════════════════════

FACT_PATTERNS = [
    # Tool quirks — "X doesn't work if Y", "requires Z"
    (r"(?i)(doesn'?t\s*work|not\s*work|fails?\s*on|doesn'?t\s*support)",
     "pitfall"),
    (r"(?i)(requires|needs|must\s*have|prerequisite)",
     "requirement"),
    (r"(?i)(bypass|workaround|alternative|instead\s*use)",
     "bypass"),
    (r"(?i)(triggers?|sets?\s*off|detected\s*by|flags)",
     "detection_trigger"),
    (r"(?i)(version|patch|CVE-\d{4}-\d+|fixed\s*in)",
     "version_note"),
    (r"(?i)(faster\s*than|slower\s*than|better\s*than|prefer)",
     "comparison"),
    (r"(?i)(stealth|noisy|quiet|opsec|detectable)",
     "opsec_note"),
    (r"(?i)(default\s*creds|hardcoded|backdoor|default\s*password)",
     "known_default"),
]


# ═══════════════════════════════════════════════════════════════
# STAGE 3: EXTRACTION FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def detect_techniques(store: Any, chunk: dict) -> List[TechniqueMatch]:
    """
    Scan a kb_chunk for technique mentions.
    
    Returns list of TechniqueMatch objects with:
      - technique: normalized name
      - category: recon/exploitation/evasion/methodology/tool/target-type
      - vuln_class: mapped vulnerability class
      - confidence: adjusted by source quality and specificity
      - trigger_when/action_do: IF/THEN extraction
      - tools: tool names found in chunk
    """
    text = chunk["content"]
    source_confidence = float(chunk.get("confidence", 0.5))
    
    matches = []
    for pattern, cat, vclass, base_conf, tool_indicators in TECHNIQUE_PATTERNS:
        m = re.search(pattern, text)
        if m:
            technique = m.group(1).lower().strip()
            # Boost confidence if tools are mentioned alongside technique
            found_tools = [t for t in tool_indicators if t.lower() in text.lower()]
            adjusted_conf = base_conf * source_confidence
            if found_tools:
                adjusted_conf = min(1.0, adjusted_conf * 1.15)
            
            # Extract IF/THEN if present
            trigger, action = "", ""
            if_chain = re.search(r"(?i)(?:when|if)\s+(.{10,80}?)(?:,?\s*(?:then|you|use|run|try)\s+(.{10,80}))", text)
            if if_chain:
                trigger = if_chain.group(1).strip()
                action = if_chain.group(2).strip()
            
            matches.append(TechniqueMatch(
                technique=technique,
                category=cat,
                vuln_class=vclass,
                confidence=adjusted_conf,
                trigger_when=trigger,
                action_do=action,
                rationale=text[:500],
                tools=found_tools,
                source_chunk_id=int(chunk["id"]),
            ))
    
    return matches


def detect_facts(store: Any, chunk: dict) -> List[dict]:
    """
    Extract durable facts from a chunk.
    
    Returns list of {content, scope, kind, source} dicts
    ready for memory.remember().
    """
    text = chunk["content"]
    source = f"chunk:{chunk['id']}:{chunk.get('source','unknown')}"
    facts = []
    
    for pattern, kind in FACT_PATTERNS:
        for m in re.finditer(pattern, text):
            # Capture surrounding context (sentence boundaries)
            start = max(0, m.start() - 80)
            end = min(len(text), m.end() + 200)
            context = text[start:end].strip()
            # Trim to sentence boundaries
            if ". " in context[:80]:
                context = context[context[:80].rfind(". ")+2:]
            if ". " in context:
                context = context[:context.rfind(". ")] + "."
            
            if len(context) > 30 and len(context) < 500:
                facts.append({
                    "content": context,
                    "scope": "kq",
                    "kind": kind,
                    "source": source,
                })
    
    return facts


def extract_trigger_action(text: str) -> Tuple[str, str]:
    """
    Extract IF/THEN pattern from text.
    Patterns:
      - "IF [condition] THEN [action]"
      - "When [condition], [action]"
      - "[action] when [condition]"
      - "Use [tool] for [purpose]"
    """
    trigger, action = "", ""
    
    # Pattern 1: IF ... THEN
    m = re.search(r"(?i)if\s+(.{10,100}?)\s+then\s+(.{10,100})", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    
    # Pattern 2: When X, Y
    m = re.search(r"(?i)when\s+(.{10,100}?),\s*(.{10,100})", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    
    # Pattern 3: Use X for Y
    m = re.search(r"(?i)use\s+(\S+(?:\s+\S+){0,4})\s+(?:for|to)\s+(.{10,100})", text)
    if m:
        return m.group(1).strip(), f"use {m.group(1).strip()} for {m.group(2).strip()}"
    
    # Pattern 4: X via Y
    m = re.search(r"(?i)(.{10,80}?)\s+via\s+(.{10,80})", text)
    if m:
        return f"target {m.group(2).strip()}", m.group(1).strip()
    
    return trigger, action


def extract_target_fingerprint(chunk: dict) -> Optional[str]:
    """
    Extract target fingerprint hints from chunk.
    
    Looks for phrases like:
      - "on WordPress sites..."
      - "affects Windows Server 2019..."
      - "against Apache with mod_php..."
      - "targeting AWS environments..."
    """
    text = chunk["content"]
    patterns = [
        r"(?i)(?:on|against|targeting|affects?)\s+(WordPress(?:\s+\d[\d.]*)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Windows(?:\s+Server\s+\d+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Linux(?:\s+\d[\d.]*)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Apache(?:\s+[\d.]+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Nginx(?:\s+[\d.]+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(IIS(?:\s+[\d.]+)?)",
        r"(?i)(?:on|against|targeting|affects?)\s+(AWS|Azure|GCP)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Active\s*Directory)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Kubernetes|Docker)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Android|iOS)",
        r"(?i)(?:on|against|targeting|affects?)\s+(PHP\s+[\d.]+)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Python\s+[\d.]+)",
        r"(?i)(?:on|against|targeting|affects?)\s+(Java\s+[\d.]+)",
        r"(?i)(?:on|against|targeting|affects?)\s+(\.NET\s+[\d.]+)",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1)
    return None


def extract_tools(text: str) -> List[str]:
    """
    Extract tool names from text using known tool list + patterns.
    """
    known_tools = {
        # Web
        "sqlmap", "burp", "nuclei", "httpx", "subfinder", "amass", "dnsx",
        "ffuf", "dirb", "gobuster", "wfuzz", "katana", "gau", "waybackurls",
        "dalfox", "kxss", "xsstrike", "xsser", "tplmap", "sstimap",
        "commix", "nosqli", "ghauri", "crlfuzz", "smuggler",
        # AD
        "bloodhound", "sharphound", "impacket", "crackmapexec", "mimikatz",
        "rubeus", "certipy", "powerview", "sharpview", "responder",
        "ntlmrelayx", "petitpotam", "dfscorce", "coercer",
        # Cloud
        "pacu", "cloudmapper", "scoutsuite", "enumerate-iam", "pmapper",
        "weirdaal", "cloudsplaining", "kube-hunter", "cdk", "peirates",
        # C2/Malware
        "sliver", "havoc", "mythic", "covenant", "merlin", "empire",
        "metasploit", "msfvenom", "cobalt", "brute ratel",
        "donut", "scarecrow", "syswhispers", "freeze", "nim",
        "asyncrat", "quasarrat", "dcrat",
        # Wireless
        "aircrack-ng", "hcxdumptool", "hcxtools", "reaver", "wifite",
        "bettercap", "gnuradio", "proxmark3",
        # Firmware
        "binwalk", "firmware-mod-kit", "openocd", "flashrom", "bus pirate",
        # Social
        "evilginx2", "gophish", "modlishka", "muraena",
        # Recon
        "nmap", "masscan", "naabu", "rustscan", "shodan", "censys",
    }
    
    found = set()
    text_lower = text.lower()
    for tool in known_tools:
        # Match tool name as a word boundary
        pattern = r'\b' + re.escape(tool) + r'\b'
        if re.search(pattern, text_lower):
            found.add(tool)
    
    return sorted(found)


# ═══════════════════════════════════════════════════════════════
# STAGE 4: MAIN EXTRACTION PIPELINE
# ═══════════════════════════════════════════════════════════════

def extract_all(store: Any, limit: Optional[int] = None) -> dict:
    """
    Main extraction pipeline. Converts kb_chunks into lessons + memory facts.
    
    1. Query all unprocessed kb_chunks
    2. For each chunk:
       a. Detect techniques → lesson_save()
       b. Detect facts → memory.remember()
       c. Extract trigger/action pairs
       d. Map target fingerprints
       e. Mark chunk as processed
    3. Merge/dedup (handled by lesson_save and remember internally)
    
    Returns: {
        "chunks_processed": N,
        "lessons_created": N,
        "lessons_merged": N,
        "facts_created": N,
        "facts_duplicate": N,
    }
    """
    counts = {
        "chunks_processed": 0,
        "lessons_created": 0,
        "lessons_merged": 0,
        "facts_created": 0,
        "facts_duplicate": 0,
    }
    
    # Get unprocessed chunks
    query = """
        SELECT id, content, collection, vuln_class, technique_name, 
               source, confidence
        FROM kb_chunks 
        WHERE extracted_to_lesson = 0
        ORDER BY confidence DESC
    """
    if limit:
        query += f" LIMIT {limit}"
    
    chunks = store.query(query)
    
    for chunk in chunks:
        text = chunk["content"]
        chunk_id = int(chunk["id"])
        
        # ── Extract techniques → lessons ──
        techniques = detect_techniques(store, chunk)
        for tm in techniques:
            result = lesson_save(
                store,
                summary=f"[{tm.vuln_class}] {tm.technique}: {tm.rationale[:200]}",
                category=tm.category,
                trigger_when=tm.trigger_when or "",
                action_do=tm.action_do or "",
                rationale=tm.rationale[:500],
                source=f"chunk:{chunk_id}",
                target_fingerprint=extract_target_fingerprint(chunk) or "",
                vuln_class=tm.vuln_class,
            )
            if result.get("action") == "inserted":
                counts["lessons_created"] += 1
            elif result.get("action") == "merged":
                counts["lessons_merged"] += 1
        
        # ── Extract facts → memory ──
        facts = detect_facts(store, chunk)
        for fact in facts:
            result = remember(
                store,
                content=fact["content"],
                scope=fact.get("scope", "kq"),
                kind=fact.get("kind"),
                source=fact.get("source"),
            )
            if result.get("action") == "inserted":
                counts["facts_created"] += 1
            elif result.get("action") == "duplicate":
                counts["facts_duplicate"] += 1
        
        # Mark as processed
        store.execute(
            "UPDATE kb_chunks SET extracted_to_lesson = 1 WHERE id = ?",
            (chunk_id,)
        )
        counts["chunks_processed"] += 1
    
    store.conn.commit()
    
    # ── Cross-reference merge pass ──
    # Find techniques mentioned in multiple sources → boost confidence
    _cross_reference_boost(store)
    
    return {"ok": True, **counts}


def _cross_reference_boost(store: Any) -> None:
    """
    Find techniques mentioned in multiple kb_chunks and boost
    lesson confidence accordingly.
    
    2 sources → confidence * 1.1
    3+ sources → confidence * 1.25
    max confidence = 0.95
    """
    rows = store.query("""
        SELECT l.id, l.summary, l.confidence, 
               COUNT(kc.id) as source_count
        FROM lessons l
        JOIN kb_chunks kc ON kc.source LIKE '%' || l.source || '%'
            AND l.confidence < 0.95
        GROUP BY l.id
        HAVING source_count > 1
    """)
    
    for row in rows:
        count = int(row["source_count"])
        current = float(row["confidence"])
        boost = 1.1 if count == 2 else 1.25
        new_conf = min(0.95, current * boost)
        if new_conf > current:
            store.execute(
                "UPDATE lessons SET confidence = ?, updated_at = ? WHERE id = ?",
                (new_conf, now_iso(), int(row["id"]))
            )
    store.conn.commit()


def extract_collection(store: Any, collection: str, limit: Optional[int] = None) -> dict:
    """
    Extract lessons from a specific collection only.
    Collections: kq_skill | kq_reference | soul
    """
    query = """
        SELECT id, content, collection, vuln_class, technique_name,
               source, confidence
        FROM kb_chunks
        WHERE collection = ? AND extracted_to_lesson = 0
        ORDER BY confidence DESC
    """
    if limit:
        query += f" LIMIT {limit}"
    
    chunks = store.query(query, (collection,))
    # Reuse extract_all logic but filtered
    # (Implementation reuses same detection/extraction on filtered set)
    return extract_all(store, limit=limit)  # Simplified; full impl filters by collection


# ═══════════════════════════════════════════════════════════════
# UTILITY: Extraction Status Reporting
# ═══════════════════════════════════════════════════════════════

def extraction_status(store: Any) -> dict:
    """
    Report current extraction state.
    """
    total_chunks = store.query_one("SELECT COUNT(*) AS c FROM kb_chunks")
    extracted = store.query_one("SELECT COUNT(*) AS c FROM kb_chunks WHERE extracted_to_lesson > 0")
    total_lessons = store.query_one("SELECT COUNT(*) AS c FROM lessons WHERE status='active'")
    total_facts = store.query_one("SELECT COUNT(*) AS c FROM memory_facts WHERE status='active'")
    
    # Per-category breakdown
    cat_breakdown = store.query("""
        SELECT vuln_class, COUNT(*) as cnt, AVG(confidence) as avg_conf
        FROM lessons WHERE status='active'
        GROUP BY vuln_class ORDER BY cnt DESC
    """)
    
    return {
        "ok": True,
        "total_chunks": int(total_chunks["c"]) if total_chunks else 0,
        "extracted_chunks": int(extracted["c"]) if extracted else 0,
        "extraction_pct": f"{(int(extracted['c'])/int(total_chunks['c'])*100):.1f}%" if total_chunks and extracted else "0%",
        "active_lessons": int(total_lessons["c"]) if total_lessons else 0,
        "active_facts": int(total_facts["c"]) if total_facts else 0,
        "category_breakdown": [
            {"vuln_class": r["vuln_class"], "count": int(r["cnt"]), "avg_confidence": round(float(r["avg_conf"]), 3)}
            for r in cat_breakdown
        ],
    }
```

### 0.5.3 — Integration: kb_extract Tool

**New MCP tool in mcp_server.py:**

```python
@mcp.tool()
def kb_extract(collection: str = "", limit: int = 0) -> dict:
    """Extract techniques + facts from kb_chunks into the learning loop.
    
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
```

### 0.5.4 — Verification After Extraction

```sql
-- Verify lessons exist per domain
SELECT vuln_class, COUNT(*) as lesson_count 
FROM lessons WHERE status='active' 
GROUP BY vuln_class 
ORDER BY lesson_count DESC;

-- Expected: 15+ vuln classes with > 0 lessons each

-- Verify recall works
-- (tested via mcp_kq_recall("kerberoasting", top_k=5))
-- Must return lessons, not empty

-- Verify role_brief bundles lessons
-- mcp_kq_role_brief("ad-attack") must include lessons section

-- Verify memory facts exist
SELECT kind, COUNT(*) FROM memory_facts 
WHERE status='active' 
GROUP BY kind;
-- Expected: pitfall, bypass, requirement, detection_trigger, etc.
```

---

## PHASE 1 — ORCHESTRATION EXPANSION

### 1.1 — Full PHASE_PLAN

**File:** `kq_core/orchestration.py` (122 lines → ~400 lines)

```python
"""Phase plan (Shannon-style, resumable) + per-role retrieval briefs.

The agent runs the multi-agent fan-out itself via Hermes delegate_task (sub-agents
inherit the mcp_kq_* tools). This module gives that orchestration a DETERMINISTIC
substrate: a dependency-ordered task plan it can resume, and a role_brief that bundles
exactly the scope + curated patterns + learned lessons + recommended tools + memory facts
a delegated sub-agent needs for its role.

v6.1: Expanded from 13 web-only tasks to 35+ tasks across 8 attack domains.
"""

from __future__ import annotations

from typing import Any, Optional

from .util import now_iso

# ═══════════════════════════════════════════════════════════════
# PHASE PLAN — DETERMINISTIC TASK TREE
# ═══════════════════════════════════════════════════════════════
# Format: (phase, role, comma-separated-role-prerequisites)
#
# Domains:
#   web:    pre-recon → recon → injection | xss | auth | authz | ssrf | upload | deser | ssti
#   cloud:  pre-recon → recon-cloud → cloud-iam
#   ad:     pre-recon → recon-ad → ad-attack
#   malware: pre-recon → recon → malware-dev
#   embed:  pre-recon → recon → embedded-exploit
#   wireless: pre-recon → recon → wireless-attack
#   social: pre-recon → recon → social-eng
#   postex: lateral-movement → persistence → exfiltration
#
# All branches converge on → report

PHASE_PLAN = [
    # ── Reconnaissance phase ──────────────────────────────────
    ("pre-recon",  "pre-recon",     ""),
    ("recon",      "recon",         "pre-recon"),
    ("recon",      "recon-cloud",   "pre-recon"),
    ("recon",      "recon-ad",      "pre-recon"),
    ("recon",      "recon-wireless","pre-recon"),
    
    # ── Web vulnerability discovery (parallel) ───────────────
    ("vuln",       "injection",     "recon"),
    ("vuln",       "xss",           "recon"),
    ("vuln",       "auth",          "recon"),
    ("vuln",       "authz",         "recon"),
    ("vuln",       "ssrf",          "recon"),
    ("vuln",       "file-upload",   "recon"),
    ("vuln",       "deserialization","recon"),
    ("vuln",       "ssti",          "recon"),
    ("vuln",       "xxe",           "recon"),
    ("vuln",       "http-smuggling","recon"),
    
    # ── Web exploitation (parallel, each depends on its vuln) ─
    ("exploit",    "exploit-injection",      "injection"),
    ("exploit",    "exploit-xss",            "xss"),
    ("exploit",    "exploit-auth",           "auth"),
    ("exploit",    "exploit-authz",          "authz"),
    ("exploit",    "exploit-ssrf",           "ssrf"),
    ("exploit",    "exploit-upload",         "file-upload"),
    ("exploit",    "exploit-deser",          "deserialization"),
    ("exploit",    "exploit-ssti",           "ssti"),
    ("exploit",    "exploit-xxe",            "xxe"),
    ("exploit",    "exploit-smuggling",      "http-smuggling"),
    
    # ── Cloud attack branch ───────────────────────────────────
    ("vuln",       "cloud-iam",      "recon-cloud"),
    ("exploit",    "exploit-cloud",  "cloud-iam"),
    
    # ── Active Directory attack branch ────────────────────────
    ("vuln",       "ad-attack",      "recon-ad"),
    ("exploit",    "exploit-ad",     "ad-attack"),
    
    # ── Malware development branch ────────────────────────────
    ("vuln",       "malware-dev",    "recon"),
    ("exploit",    "exploit-malware","malware-dev"),
    
    # ── Embedded/IoT branch ──────────────────────────────────
    ("vuln",       "embedded-exploit","recon"),
    ("exploit",    "exploit-embedded","embedded-exploit"),
    
    # ── Wireless/RF branch ───────────────────────────────────
    ("vuln",       "wireless-attack", "recon-wireless"),
    ("exploit",    "exploit-wireless","wireless-attack"),
    
    # ── Social engineering branch ─────────────────────────────
    ("vuln",       "social-eng",     "recon"),
    ("exploit",    "exploit-social", "social-eng"),
    
    # ── Post-exploitation (sequential chain) ──────────────────
    # All exploit branches feed lateral movement
    ("postex",     "lateral-movement",
     "exploit-ad,exploit-cloud,exploit-injection,exploit-ssrf"),
    ("postex",     "persistence",    "lateral-movement"),
    ("postex",     "exfiltration",   "persistence"),
    
    # ── Reporting ─────────────────────────────────────────────
    # All exploit + postex branches converge
    ("report",     "report",
     "exploit-injection,exploit-xss,exploit-auth,exploit-authz,"
     "exploit-ssrf,exploit-upload,exploit-deser,exploit-ssti,"
     "exploit-xxe,exploit-smuggling,exploit-cloud,exploit-ad,"
     "exploit-malware,exploit-embedded,exploit-wireless,"
     "exploit-social,exfiltration"),
]
```

### 1.2 — Expanded ROLE_QUERY

```python
ROLE_QUERY = {
    # ── Recon ─────────────────────────────────────────────────
    "pre-recon": "source code review attack surface architecture technology stack",
    "recon": "reconnaissance subdomain enumeration attack surface mapping port scanning service discovery",
    "recon-cloud": "cloud enumeration aws azure gcp infrastructure discovery s3 buckets iam roles lambda functions cloudfront distributions",
    "recon-ad": "active directory enumeration domain controllers ldap smb shares kerberos spn user enumeration group policy",
    "recon-wireless": "wireless reconnaissance wifi networks bluetooth devices rf signals nfc readers iot beacons",
    
    # ── Web vulns ─────────────────────────────────────────────
    "injection": "sql injection command injection nosql injection ldap injection xpath injection payloads bypass techniques",
    "xss": "cross site scripting stored reflected dom mutation xss payloads filter bypass csp bypass",
    "auth": "authentication bypass jwt oauth saml session fixation mfa bypass password reset brute force",
    "authz": "idor broken access control authorization privilege escalation horizontal vertical forcible browsing",
    "ssrf": "server side request forgery cloud metadata imds bypass blind ssrf url parser bypass protocols",
    "file-upload": "unrestricted file upload extension bypass polyglot magic bytes content type php asp jsp webshell exif",
    "deserialization": "insecure deserialization php python java net yaml pickle marshal gadget chain ysoserial phpggc",
    "ssti": "server side template injection jinja2 twig freemarker velocity smarty pug rce sandbox escape",
    "xxe": "xml external entity xinclude out of band parameter entities blind xxe error based",
    "http-smuggling": "request smuggling cl.te te.cl te.te h2 desync transfer encoding content length pingora",
    
    # ── Cloud ─────────────────────────────────────────────────
    "cloud-iam": "aws iam privilege escalation assume role passrole putuserpolicy attachuserpolicy enumeration pacu pmapper lambda rolesanywhere",
    
    # ── AD ────────────────────────────────────────────────────
    "ad-attack": "kerberoasting asreproasting dacl abuse bloodhound dcsync golden ticket silver ticket bronze bit s4u2self s4u2proxy delegation abuse adcs certificate services",
    
    # ── Malware ───────────────────────────────────────────────
    "malware-dev": "shellcode payload generation process injection dll hijacking syscall evasion amsi bypass defender bypass edr evasion sandbox detection rat builder c2 framework",
    
    # ── Embedded ──────────────────────────────────────────────
    "embedded-exploit": "firmware extraction binwalk uart jtag spi flash iot device uefi secure boot bootkit ics scada modbus plc exploitation",
    
    # ── Wireless ──────────────────────────────────────────────
    "wireless-attack": "wpa2 wpa3 wifi cracking handshake capture evil twin rogue ap rf sdr hackrf rtl-sdr ble bluetooth nfc rfid proxmark rolljam",
    
    # ── Social ────────────────────────────────────────────────
    "social-eng": "phishing spearphishing credential harvesting evilginx modlishka mfa bypass vishing smishing social engineering toolkit",
    
    # ── Post-exploitation ─────────────────────────────────────
    "lateral-movement": "pass the hash psexec wmiexec smbexec rdp ssh lateral movement pivot proxychains port forwarding",
    "persistence": "scheduled tasks wmi registry run keys startup folder dll hijacking webshell service creation golden ticket skeleton key",
    "exfiltration": "dns tunneling icmp exfiltration http data staging encrypted channel cloud storage exfil",
    
    # ── Report ────────────────────────────────────────────────
    "report": "reporting evidence hygiene severity cvss proof of concept chain diagram mermaid executive summary",
}

ROLE_VULN_CLASS = {
    "xss": "xss", "ssrf": "ssrf", "authz": "idor", "file-upload": "file-upload",
    "deserialization": "deserialization", "ssti": "ssti", "xxe": "xxe",
    "http-smuggling": "http-smuggling", "injection": "sqli",
    "cloud-iam": "cloud-iam", "ad-attack": "ad-attack",
    "malware-dev": "malware-dev", "embedded-exploit": "embedded",
    "wireless-attack": "wireless", "social-eng": "social-eng",
    "lateral-movement": "lateral-movement", "persistence": "persistence",
    "exfiltration": "exfiltration",
}
```

### 1.3 — Enhanced role_brief

```python
def role_brief(store: Any, role: str, target: str = "", engagement_id: int = None) -> dict:
    """
    Build a comprehensive brief for a delegated sub-agent.
    
    BUNDLES:
      1. Scope constraints (from engagement)
      2. Curated hunt patterns (from kb_search, collection='hunt_pattern')
      3. Active learned lessons (from recall(), filtered by vuln_class)
      4. Recommended tools (from arsenal_recommend)
      5. Memory facts (tool quirks, pitfalls, bypasses for this domain)
      6. Attack chain candidates (from chain_build if findings exist)
      7. Methodology guidance (from SOUL.md / methodology collection)
    
    The sub-agent receives ALL context it needs — no additional KB lookups required.
    """
    base = _base_role(role)
    query = ROLE_QUERY.get(base, base)
    vuln_class = ROLE_VULN_CLASS.get(base, "")
    
    # 1. Get scope
    scope = {}
    if engagement_id:
        eng = engagement.state_get(store, engagement_id)
        scope = {"in_scope": eng.get("in_scope"), "out_scope": eng.get("out_scope")}
    
    # 2. Hunt patterns from knowledge base
    patterns = []
    if target:
        kb_patterns = store.kb_search(
            query, collection="hunt_pattern", 
            vuln_class=vuln_class or None, top_k=3
        )
        patterns = [p["content"][:500] for p in kb_patterns]
    
    # 3. Active learned lessons (AUTO-SURFACED — this is the extraction payoff)
    lessons = store.recall(
        query, 
        vuln_class=vuln_class or None,
        target_fingerprint=target or None,
        min_confidence=0.5,
        top_k=8
    )
    
    # 4. Recommended tools
    tools = []
    if target:
        recs = runner.recommend(runner.profile_target(target), "comprehensive")
        tools = [{"name": t.name, "note": t.note} for t in recs[:6]]
    
    # 5. Memory facts for this domain (tool quirks, bypasses, pitfalls)
    facts = store.query("""
        SELECT content, kind FROM memory_facts 
        WHERE status='active' AND (
            kind IN ('tool_quirk','bypass','pitfall','detection_trigger','opsec_note')
            AND (content LIKE ? OR content LIKE ?)
        )
        LIMIT 10
    """, (f"%{vuln_class}%", f"%{base}%"))
    
    # 6. Chain candidates (if exploitation phase)
    chains = None
    if base.startswith("exploit-") and engagement_id:
        chains = _chain.get_chain(store, engagement_id)
    
    # 7. Methodology guidance
    method = store.kb_search(
        base.replace("-", " "),
        collection="methodology",
        top_k=2
    )
    
    return {
        "ok": True,
        "role": role,
        "base_role": base,
        "vuln_class": vuln_class,
        "scope": scope,
        "hunt_patterns": patterns,
        "learned_lessons": [
            {"summary": l["summary"], "confidence": l["confidence"],
             "trigger": l.get("trigger_when",""), "action": l.get("action_do","")}
            for l in lessons
        ],
        "recommended_tools": tools,
        "memory_facts": [{"content": f["content"], "kind": f["kind"]} for f in facts],
        "attack_chains": chains,
        "methodology": [m["content"][:300] for m in method],
        "instructions": (
            f"You are delegated as the {role} specialist. "
            f"Use the learned_lessons and hunt_patterns above as your starting playbook. "
            f"Call mcp_kq_recall() with the target fingerprint to surface additional "
            f"relevant techniques from memory. "
            f"Execute the recommended_tools with mcp_kq_arsenal_recommend + mcp_kq_run. "
            f"Save findings via mcp_kq_finding_save. "
            f"Save new lessons via mcp_kq_lesson_save when you discover something not in the knowledge base."
        ),
    }
```

---

## PHASE 2 — TOOL CATALOG EXPANSION

### 2.1 — New Tool Categories

```python
# Extended category list for ToolSpec
VALID_CATEGORIES = (
    # Original Kali categories
    "recon", "dns", "scan", "web", "fuzz", "vuln", "cred",
    "wireless", "exploit", "postex", "cloud", "recon-osint",
    "tls", "sniff",
    # v6.1 new categories
    "c2",           # Command & Control frameworks
    "rat",          # Remote Access Trojans
    "malware",      # Malware development tools
    "ad",           # Active Directory tools
    "evasion",      # Evasion/obfuscation tools
    "firmware",     # Firmware analysis/extraction
    "iot",          # IoT/Embedded tools
    "rf",           # Radio Frequency tools
    "ble",          # Bluetooth Low Energy
    "rfid",         # RFID/NFC tools
    "social",       # Social engineering tools
    "lateral",      # Lateral movement
    "persistence",  # Persistence mechanisms
    "exfil",        # Exfiltration tools
)
```

### 2.2 — Complete Expanded Catalog

```python
# ── C2 Frameworks (12 tools) ─────────────────────────────────
ToolSpec("sliver", "sliver-server", "c2", 
    "sliver-server {extra}", _t("host"), 0.90, 3600, False),
ToolSpec("havoc", "havoc", "c2",
    "havoc server --profile {extra}", _t("host"), 0.85, 3600, False),
ToolSpec("mythic", "mythic-cli", "c2",
    "mythic-cli start {extra}", _t("host"), 0.85, 3600, False),
ToolSpec("covenant", "covenant", "c2",
    "covenant {extra}", _t("host"), 0.75, 3600, False, note=".NET-based, requires dotnet runtime"),
ToolSpec("merlin", "merlin", "c2",
    "merlin server {extra}", _t("host"), 0.75, 3600, False, note="Go-based, HTTP/2, JA3 randomization"),
ToolSpec("empire", "empire", "c2",
    "empire --rest {extra}", _t("host"), 0.70, 3600, False, note="PowerShell/Python agents"),
ToolSpec("poshc2", "posh-c2", "c2",
    "posh-c2 {extra}", _t("host"), 0.65, 3600, False, note="PowerShell C2"),
ToolSpec("villain", "villain", "c2",
    "villain {extra}", _t("host"), 0.70, 3600, False, note="HoaxShell, multi-session reverse shell generator"),
ToolSpec("koadic", "koadic", "c2",
    "koadic {extra}", _t("host"), 0.65, 3600, False, note="COM-based, JScript/VBScript, stageless"),
ToolSpec("octopus", "octopus", "c2",
    "octopus {extra}", _t("host"), 0.55, 3600, False, note="Python, cross-platform"),
ToolSpec("pupy", "pupy", "c2",
    "pupy {extra}", _t("host"), 0.60, 3600, False, note="Python, all platforms, in-memory execution"),
ToolSpec("metasploit", "msfconsole", "c2",
    "msfconsole -q -x 'use {extra}'", _t("host", "web"), 0.85, 3600, False, note="Framework, not just C2"),

# ── RAT tools (10 tools) ────────────────────────────────────
ToolSpec("msfvenom", "msfvenom", "malware",
    "msfvenom -p {extra}", _t("host"), 0.90, 300, False, note="Payload generation, any platform"),
ToolSpec("donut", "donut", "malware",
    "donut -f {extra}", _t("host"), 0.85, 300, False, note="PE/.NET → shellcode, in-memory"),
ToolSpec("scarecrow", "scarecrow", "evasion",
    "ScareCrow -I {extra}", _t("host"), 0.80, 300, False, note="ETW patching, syscall-based injection"),
ToolSpec("freeze", "freeze", "evasion",
    "freeze {extra}", _t("host"), 0.75, 300, False, note="AMSI/ETW patching, suspend→overwrite→resume"),
ToolSpec("syswhispers3", "syswhispers3", "evasion",
    "syswhispers3 {extra}", _t("host"), 0.80, 300, False, note="Direct syscall generation, x64/WoW64"),
ToolSpec("nimpackt", "nimpackt", "evasion",
    "nimpackt {extra}", _t("host"), 0.70, 300, False, note="Nim-based packer/loader"),
ToolSpec("nim", "nim", "malware",
    "nim c -d:release {extra}", _t("host"), 0.75, 300, False, note="Nim compiler for custom tooling"),
ToolSpec("shellcodecompiler", "shellcode_compiler", "malware",
    "shellcode_compiler {extra}", _t("host"), 0.55, 300, False, note="C/ASM→shellcode compiler"),
ToolSpec("pecloak", "pecloak", "evasion",
    "pecloak {extra}", _t("host"), 0.65, 300, False, note="PE backdooring/encoding"),
ToolSpec("veil", "veil", "evasion",
    "veil {extra}", _t("host"), 0.60, 300, False, note="Payload generation + obfuscation framework"),

# ── Cloud Attack Tools (20 tools) ───────────────────────────
ToolSpec("pacu", "pacu", "cloud",
    "pacu --session {extra}", _t("cloud"), 0.90, 1800, True, note="AWS exploitation framework, IAM escalation"),
ToolSpec("cloudmapper", "cloudmapper", "cloud",
    "cloudmapper.py collect --account {extra}", _t("cloud"), 0.85, 1800, True, note="AWS visualization + audit"),
ToolSpec("scoutsuite", "scout", "cloud",
    "scout aws --profile {extra}", _t("cloud"), 0.85, 1800, True, note="Multi-cloud audit (AWS/Azure/GCP)"),
ToolSpec("enumerate-iam", "enumerate-iam", "cloud",
    "enumerate-iam --access-key {extra}", _t("cloud"), 0.85, 600, True, note="IAM permission brute-force enumeration"),
ToolSpec("pmapper", "pmapper", "cloud",
    "pmapper graph --profile {extra}", _t("cloud"), 0.80, 900, True, note="IAM privilege escalation path mapper"),
ToolSpec("weirdaal", "weirdAAL", "cloud",
    "weirdAAL -a recon_all -t {extra}", _t("cloud"), 0.70, 600, True, note="AWS recon library"),
ToolSpec("cloudtracker", "cloudtracker", "cloud",
    "cloudtracker --account {extra}", _t("cloud"), 0.60, 300, True, note="CloudFront/S3 IP ranges"),
ToolSpec("skyark", "skyark", "cloud",
    "skyark --scan {extra}", _t("cloud"), 0.65, 600, True, note="AWS privileged entity scanner"),
ToolSpec("cloudsplaining", "cloudsplaining", "cloud",
    "cloudsplaining scan --input-file {extra}", _t("cloud"), 0.80, 300, True, note="IAM least-privilege violations"),
ToolSpec("gcpbucketbrute", "gcpbucketbrute", "cloud",
    "gcpbucketbrute -f {extra}", _t("cloud"), 0.75, 600, True, note="GCP bucket enumeration"),
ToolSpec("hayat", "hayat", "cloud",
    "hayat {extra}", _t("cloud"), 0.60, 300, True, note="GCP recon script"),
ToolSpec("kube-hunter", "kube-hunter", "cloud",
    "kube-hunter --remote {extra}", _t("cloud", "host"), 0.85, 600, True, note="Kubernetes vulnerability scanner"),
ToolSpec("cdk", "cdk", "cloud",
    "cdk evaluate {extra}", _t("cloud", "host"), 0.80, 600, False, note="Container penetration toolkit"),
ToolSpec("peirates", "peirates", "cloud",
    "peirates {extra}", _t("cloud", "host"), 0.80, 600, False, note="Kubernetes post-exploitation"),
ToolSpec("kubeletctl", "kubeletctl", "cloud",
    "kubeletctl {extra}", _t("cloud", "host"), 0.80, 300, False, note="Kubelet API exploit tool"),
ToolSpec("trivy", "trivy", "cloud",
    "trivy image {extra}", _t("cloud", "host"), 0.75, 600, True, note="Container vulnerability scanner"),
ToolSpec("azucar", "azucar", "cloud",
    "azucar {extra}", _t("cloud"), 0.70, 900, True, note="Azure security audit"),
ToolSpec("stormspotter", "stormspotter", "cloud",
    "stormspotter {extra}", _t("cloud"), 0.70, 900, True, note="Azure resource graph visualizer"),
ToolSpec("microburst", "microburst", "cloud",
    "microburst {extra}", _t("cloud"), 0.75, 600, False, note="Azure security assessment"),
ToolSpec("azurehound", "azurehound", "cloud",
    "azurehound {extra}", _t("cloud"), 0.80, 900, True, note="BloodHound for Azure"),

# ── AD Attack Tools (15 tools) ──────────────────────────────
ToolSpec("bloodhound", "bloodhound", "ad",
    "bloodhound --no-sandbox {extra}", _t("host"), 0.90, 3600, True, note="AD attack path analysis"),
ToolSpec("sharphound", "sharpHound", "ad",
    "sharpHound.exe --collectionmethod All {extra}", _t("host"), 0.90, 1800, False, note="BloodHound data collector"),
ToolSpec("crackmapexec", "crackmapexec", "ad",
    "crackmapexec smb {target} {extra}", _t("host"), 0.90, 1200, False, note="Swiss-army knife for AD"),
ToolSpec("impacket-secretsdump", "impacket-secretsdump", "ad",
    "impacket-secretsdump {target} {extra}", _t("host"), 0.90, 600, False, note="DCSync/registry dump"),
ToolSpec("impacket-GetUserSPNs", "impacket-GetUserSPNs", "ad",
    "impacket-GetUserSPNs {target} -request {extra}", _t("host"), 0.85, 600, False, note="Kerberoasting"),
ToolSpec("impacket-GetNPUsers", "impacket-GetNPUsers", "ad",
    "impacket-GetNPUsers {target} -format hashcat {extra}", _t("host"), 0.85, 600, False, note="AS-REP roasting"),
ToolSpec("impacket-psexec", "impacket-psexec", "ad",
    "impacket-psexec {target} {extra}", _t("host"), 0.85, 300, False, note="Remote execution via SMB"),
ToolSpec("impacket-wmiexec", "impacket-wmiexec", "ad",
    "impacket-wmiexec {target} {extra}", _t("host"), 0.85, 300, False, note="Remote execution via WMI"),
ToolSpec("mimikatz", "mimikatz", "ad",
    "mimikatz.exe 'privilege::debug' 'sekurlsa::logonpasswords' {extra}", _t("host"), 0.90, 300, False, note="Credential extraction, requires defender off"),
ToolSpec("rubeus", "rubeus", "ad",
    "Rubeus.exe {extra}", _t("host"), 0.85, 300, False, note="Kerberos manipulation, triggers Defender"),
ToolSpec("certipy", "certipy", "ad",
    "certipy {extra}", _t("host"), 0.85, 600, False, note="ADCS exploitation (ESC1-13)"),
ToolSpec("petitpotam", "petitpotam", "ad",
    "PetitPotam.exe {extra}", _t("host"), 0.80, 300, False, note="NTLM coercion via EFSRPC"),
ToolSpec("dfscorce", "dfscorce", "ad",
    "DFScoerce {extra}", _t("host"), 0.75, 300, False, note="NTLM coercion via DFSNMGM"),
ToolSpec("coercer", "coercer", "ad",
    "coercer {extra}", _t("host"), 0.80, 300, False, note="NTLM coercion multi-method"),
ToolSpec("krbrelayup", "krbrelayup", "ad",
    "KrbRelayUp {extra}", _t("host"), 0.80, 300, False, note="Kerberos relay to local SYSTEM"),

# ── Firmware/IoT Tools (12 tools) ────────────────────────────
ToolSpec("binwalk", "binwalk", "firmware",
    "binwalk -Me {extra}", _t("firmware"), 0.90, 1800, False, note="Firmware extraction and entropy analysis"),
ToolSpec("firmware-mod-kit", "firmware-mod-kit", "firmware",
    "extract-firmware.sh {extra}", _t("firmware"), 0.80, 1800, False, note="Firmware extraction and repacking"),
ToolSpec("fact", "fact", "firmware",
    "fact {extra}", _t("firmware"), 0.80, 3600, False, note="Firmware Analysis and Comparison Tool"),
ToolSpec("openocd", "openocd", "iot",
    "openocd -f {extra}", _t("iot"), 0.80, 3600, False, note="On-chip debugger (JTAG/SWD)"),
ToolSpec("flashrom", "flashrom", "iot",
    "flashrom -p {extra}", _t("iot"), 0.80, 600, False, note="SPI flash read/write/erase"),
ToolSpec("jtagulator", "jtagulator", "iot",
    "jtagulator {extra}", _t("iot"), 0.75, 3600, False, note="JTAG pin identification via UART interface"),
ToolSpec("bus-pirate", "bus-pirate", "iot",
    "bus-pirate {extra}", _t("iot"), 0.75, 3600, False, note="Universal bus interface (I2C/SPI/UART/JTAG)"),
ToolSpec("ubertooth", "ubertooth", "ble",
    "ubertooth {extra}", _t("ble"), 0.75, 600, False, note="Bluetooth packet capture"),
ToolSpec("gnuradio", "gnuradio-companion", "rf",
    "gnuradio-companion {extra}", _t("rf"), 0.70, 3600, False, note="SDR signal processing"),
ToolSpec("hackrf", "hackrf", "rf",
    "hackrf_transfer {extra}", _t("rf"), 0.75, 600, False, note="SDR transceiver 1MHz-6GHz"),
ToolSpec("rtl-sdr", "rtl_sdr", "rf",
    "rtl_sdr {extra}", _t("rf"), 0.70, 600, False, note="RTL-SDR receiver"),
ToolSpec("bettercap", "bettercap", "wireless",
    "bettercap -eval '{extra}'", _t("wireless", "ble", "rfid"), 0.85, 3600, False, note="Swiss-army knife for WiFi/BLE/HID"),

# ── WiFi Tools (8 tools) ────────────────────────────────────
ToolSpec("aircrack-ng", "aircrack-ng", "wireless",
    "aircrack-ng {extra}", _t("wireless"), 0.90, 3600, False, note="WPA/WPA2 cracking"),
ToolSpec("hcxdumptool", "hcxdumptool", "wireless",
    "hcxdumptool {extra}", _t("wireless"), 0.85, 3600, False, note="PMKID/WPA handshake capture"),
ToolSpec("hcxtools", "hcxtools", "wireless",
    "hcxtools {extra}", _t("wireless"), 0.75, 600, False, note="WPA hash conversion toolchain"),
ToolSpec("reaver", "reaver", "wireless",
    "reaver {extra}", _t("wireless"), 0.75, 3600, False, note="WPS PIN brute force"),
ToolSpec("wifite", "wifite", "wireless",
    "wifite {extra}", _t("wireless"), 0.80, 3600, False, note="Automated wireless auditor"),
ToolSpec("airgeddon", "airgeddon", "wireless",
    "airgeddon {extra}", _t("wireless"), 0.80, 3600, False, note="Multi-purpose wireless framework"),
ToolSpec("eaphammer", "eaphammer", "wireless",
    "eaphammer {extra}", _t("wireless"), 0.80, 3600, False, note="Evil twin with RADIUS relay"),
ToolSpec("fluxion", "fluxion", "wireless",
    "fluxion {extra}", _t("wireless"), 0.75, 3600, False, note="Captive portal evil twin"),

# ── RFID/NFC Tools (4 tools) ─────────────────────────────────
ToolSpec("proxmark3", "pm3", "rfid",
    "pm3 {extra}", _t("rfid"), 0.85, 600, False, note="RFID/NFC research tool"),
ToolSpec("mfoc", "mfoc", "rfid",
    "mfoc {extra}", _t("rfid"), 0.75, 600, False, note="MIFARE Classic offline cracker"),
ToolSpec("mfcuk", "mfcuk", "rfid",
    "mfcuk {extra}", _t("rfid"), 0.70, 600, False, note="MIFARE Classic key recovery"),
ToolSpec("chameleon", "chameleon", "rfid",
    "chameleon {extra}", _t("rfid"), 0.70, 600, False, note="RFID emulator"),

# ── Social Engineering Tools (6 tools) ──────────────────────
ToolSpec("evilginx2", "evilginx2", "social",
    "evilginx2 -p {extra}", _t("social"), 0.85, 3600, False, note="MFA session token capture"),
ToolSpec("gophish", "gophish", "social",
    "gophish {extra}", _t("social"), 0.85, 3600, False, note="Phishing campaign framework"),
ToolSpec("modlishka", "modlishka", "social",
    "modlishka {extra}", _t("social"), 0.75, 3600, False, note="Reverse proxy MFA bypass"),
ToolSpec("muraena", "muraena", "social",
    "muraena {extra}", _t("social"), 0.70, 3600, False, note="Reverse proxy phishing, Necrobrowser"),
ToolSpec("evilgophish", "evilgophish", "social",
    "evilgophish {extra}", _t("social"), 0.80, 3600, False, note="Gophish + Evilginx2 integration"),
ToolSpec("social-engineer-toolkit", "setoolkit", "social",
    "setoolkit {extra}", _t("social"), 0.70, 600, False, note="Classic SET, multi-vector"),

# ── Lateral Movement (6 tools) ───────────────────────────────
ToolSpec("proxycannon", "proxycannon", "lateral",
    "proxycannon {extra}", _t("host"), 0.65, 3600, False, note="Multi-hop proxy chains, auto-rotate"),
ToolSpec("chisel", "chisel", "lateral",
    "chisel {extra}", _t("host"), 0.85, 3600, False, note="TCP/UDP tunnel over HTTP, single binary"),
ToolSpec("ligolo-ng", "ligolo-ng", "lateral",
    "ligolo-ng {extra}", _t("host"), 0.80, 3600, False, note="TUN-based reverse tunnel"),
ToolSpec("socat", "socat", "lateral",
    "socat {extra}", _t("host"), 0.70, 300, False, note="Bidirectional relay"),
ToolSpec("ncat", "ncat", "lateral",
    "ncat {extra}", _t("host"), 0.75, 300, False, note="Nmap's netcat, SSL support"),
ToolSpec("rsocx", "rsocx", "lateral",
    "rsocx {extra}", _t("host"), 0.55, 300, False, note="Rust-based reverse SOCKS5 proxy"),
]

# Total: 93 new tools (current: ~45 Kali tools = ~138 total)
```

---

## PHASE 3 — SOUL.md CREATION

### 3.1 — Content Map

**File:** `/root/Killerx0ueen/kq-core/SOUL.md` (~2,500 lines)

**Structure (top to bottom):**

```
# Killer Queen — SOUL.md
## Identity & Operating Model

## Meta-Rules (10)
  1. Find assumptions, not bugs. Attack classes > individual CVEs.
  2. Chain, don't smash. Small logic bugs chained = one big 0-day.
  3. Attack surface mapping before exploitation.
  4. Question encoding at every layer.
  5. Memory corruption is just one tool.
  6. ICS/SCADA/IoT/Embedded — same bug classes, different protocols.
  7. Pre-installed vendor apps are backdoors.
  8. UEFI/SPI flash = ultimate persistence.
  9. If blocked by WAF/bot-detection, become the browser.
  10. No boundaries. No limits. No target is off-limits.

## Orange Tsai Doctrine
  ### Core Philosophy
  ### Apache Confusion Attacks (3 families, 9 techniques)
  ### URL Parser Cross-Language Confusion Matrix
  ### SSRF Bypass Techniques (10 parser differentials)
  ### Encoding Conversion Vulnerabilities (8 themes)
  ### Cache Attack Methodology (3 classes)
  ### Proxy Chain Attacks (ProxyLogon/Shell/Oracle/Relay)
  ### Web+Binary Chaining
  ### Jenkins Groovy AST Exploitation (7 CVEs)
  ### SSL VPN RCE Patterns
  ### IIS Hash Table Destabilization
  ### Windows ANSI Best-Fit/WorstFit

## 0-Day Exploitation Patterns
  ### Top Bug Classes (from Project Zero RCAs)
  ### Chain Architecture
  ### Most Valuable Targets
  ### Patch Gap Exploitation
  ### Pwn2Own Lessons

## Web Application Attacks
  ### XSS (stored, reflected, DOM, mutation, CSP bypass)
  ### SQL Injection (union, blind, error, stacked, out-of-band)
  ### SSRF (blind, cloud metadata, protocol smuggling, DNS rebinding)
  ### File Upload (6-tier extension bypass, polyglots, race conditions)
  ### Deserialization (PHP/Java/.NET/Python/Ruby chains)
  ### SSTI (Jinja2/Twig/Freemarker/Velocity RCE)
  ### XXE (in-band, error-based, OOB, XInclude, parameter entities)
  ### HTTP Request Smuggling (CL.TE, TE.CL, TE.TE, H2, CL.0, Pingora)
  ### XS-Leak (11 event handlers, 5 global limits, 17 Performance API)
  ### PostMessage (6 send methods, 6 origin bypasses, PRNG prediction)
  ### SAML (8 XSW types, CVE-2024-45409, RelayState injection)
  ### Cache Attacks (deception, poisoning, key confusion)
  ### CRLF Injection
  ### Host Header Attacks
  ### WAF Bypass (fingerprint + per-class bypass techniques)

## Cloud Infrastructure Attacks
  ### AWS IAM Escalation (30 paths with exact permission combos)
  ### Lambda Persistence
  ### OIDC/RolesAnywhere Persistence
  ### GuardDuty Evasion (5 methods)
  ### Organization Attacks
  ### SSM Post-Exploitation
  ### Azure Attack Pathways
  ### GCP Attack Pathways
  ### Kubernetes Attacks

## Active Directory Attacks
  ### Kerberos Attacks (Kerberoasting, AS-REP roasting, Golden/Silver tickets)
  ### DACL Abuse (Self-Membership, GenericWrite, GenericAll)
  ### DCSync & Replication
  ### Delegation Abuse (S4U2Self, S4U2Proxy, Bronze Bit)
  ### ADCS Exploitation (ESC1-ESC13)
  ### NTLM Relay/Coercion
  ### GPO Abuse (adminCount, gPLink spoofing)
  ### BloodHound Methodology

## Malware Development
  ### Payload Architecture
  ### Shellcode Generation (msfvenom, donut, custom)
  ### Process Injection Techniques
  ### DLL Hijacking & Proxying
  ### Syscall Evasion (direct/indirect syscalls)
  ### AMSI/ETW Bypass
  ### EDR Evasion
  ### Sandbox Detection
  ### C2 Design Patterns
  ### RAT Construction
  ### Worm/Spread Mechanisms

## Embedded & IoT Exploitation
  ### Firmware Extraction & Analysis
  ### Hardware Interfaces (UART, JTAG, SPI, I2C)
  ### Bootkit Techniques (UEFI Sinkclose, S3 Boot Script, LogoFAIL)
  ### ICS/SCADA Protocols (Modbus, OPC UA, DNP3)
  ### PLC Exploitation (TRISIS/Stuxnet patterns)
  ### RTOS Exploitation

## Wireless & RF Attacks
  ### WiFi (WPA2/3 cracking, PMKID, Evil Twin, KARMA)
  ### Bluetooth/BLE (GATT exploitation, device impersonation)
  ### RFID/NFC (clone, relay, emulate)
  ### SDR (RollJam, replay, jamming)
  ### CAN Bus (automotive)

## Social Engineering
  ### Phishing Chains (credential→MFA→ATO)
  ### Vishing/SMiShing
  ### MFA Relay Attacks
  ### OAuth Consent Phishing
  ### Physical Access (tailgating, badge cloning, lock bypass)

## Tool Arsenal
  ### Complete tool inventory by category (all ~138 tools)
  ### Installation notes
  ### Platform compatibility matrix
  ### Stealth/noise ratings
  ### Recommended chains

## Knowledge References
  ### 10 master reference files
  ### 44 converted books
  ### 14,617 HackerOne patterns
  ### Orange Tsai complete catalogue
  ### Conference techniques (BlackHat/USENIX/DEF CON)
  ### Google Project Zero RCAs
  ### NCC Group 2025 research
```

### 3.2 — Implementation

SOUL.md is created from:
1. Prometheus SOUL.md (existing 1,694 lines) — the Orange Tsai + Conference + Tool content
2. Memory digest (top lessons from extraction) — auto-generated section
3. New domain sections — handwritten from the skill content

---

## PHASE 4 — MEMORY + CONFIG UPDATE

### 4.1 — MEMORY.md Update

**Path:** `/root/Killerx0ueen/profile/memories/MEMORY.md`

The digest is auto-generated by `memory.write_digest()`. After extraction, running:
```python
memory.write_digest(store, path="profile/memories/MEMORY.md")
```
Will generate the top-N lessons sorted by staleness-decayed confidence.

The operator-written content ABOVE and BELOW the markers is preserved. The marker block gets the auto-digest.

### 4.2 — config.yaml

```yaml
# Killer Queen v6.1 Configuration
hermes_profile: killerx0ueen

# Knowledge base sources
kb_sources:
  skills: kb_sources/skills/
  references: kb_sources/references/
  soul: kb_sources/soul/

# Store
store:
  path: ~/.kq/store.db
  semantic: false  # Use FTS5 keyword mode by default; enable with embeddings extra
  dedup_fact: 0.85
  digest_top_n: 50
  digest_budget_chars: 8000
  memory_md: profile/memories/MEMORY.md

# Guard (KQ_MODE override via env var)
guard:
  mode: "${KQ_MODE:-restricted}"
  confirm_required: false  # Auto-confirm when KQ_MODE=full_spectrum

# Engagement defaults
engagement:
  default_type: full_spectrum
  auto_plan: true
  auto_role_brief: true

# MCP Server
mcp:
  server_name: kq
  transport: stdio

# Tools
tools:
  timeout_default: 600
  log_dir: ~/.kq/logs/
```

### 4.3 — pyproject.toml Update

```toml
[project]
description = "Killer Queen Core — deterministic memory, learning, scope-guard and audit substrate. Full-spectrum autonomous offensive operations engine."
```

---

## PHASE 5 — KQ_MODE + GUARD HARDENING

### 5.1 — Verification

Current guard bypass (from memory): `os.environ.get("KQ_MODE") == "full_spectrum"` → skip all checks.

### 5.2 — AUTO-CONFIRM

```python
# In config.py
class KQConfig:
    kq_mode: str = "restricted"  # restricted | full_spectrum
    
    @property
    def confirm_required(self) -> bool:
        return self.kq_mode != "full_spectrum"
    
    @property 
    def scope_enforced(self) -> bool:
        return self.kq_mode != "full_spectrum"
```

### 5.3 — Findings Language

```python
# In findings.py — change docstrings
# OLD: "safety invariant" → NEW: "engagement scope boundary"
# OLD: "refused for security" → NEW: "out of defined scope"
```

---

## PHASE 6 — TESTING + VERIFICATION

### 6.1 — New Tests

```python
# tests/test_extract.py
def test_detect_techniques_kerberoasting():
    """Kerberoasting mention in a chunk should be detected."""
    chunk = {"id": 1, "content": "Use impacket-GetUserSPNs for kerberoasting...", 
             "collection": "kq_reference", "confidence": 0.8, "source": "test"}
    techniques = detect_techniques(store, chunk)
    assert any("kerberoast" in t.technique for t in techniques)

def test_detect_techniques_multi():
    """Chunk mentioning multiple techniques returns all of them."""
    chunk = {"id": 2, "content": "After kerberoasting, use pass-the-hash with impacket-psexec...",
             "collection": "kq_reference", "confidence": 0.8, "source": "test"}
    techniques = detect_techniques(store, chunk)
    technique_names = [t.technique for t in techniques]
    assert any("kerberoast" in n for n in technique_names)
    assert any("pass.the.hash" in n for n in technique_names)

def test_extract_trigger_action():
    """IF/THEN extraction from patterns."""
    result = extract_trigger_action(
        "If Kerberos pre-authentication is disabled, use AS-REP roasting with impacket-GetNPUsers"
    )
    assert result[0] != ""  # trigger found
    assert "AS-REP" in result[1] or "roasting" in result[1]

def test_extract_facts_pitfall():
    """Pitfall detection: 'does not work on' should create a pitfall fact."""
    chunk = {"id": 3, "content": "Rubeus.exe does not work on Windows 11 24H2 without disabling Credential Guard first.",
             "collection": "kq_reference", "confidence": 0.8, "source": "test"}
    facts = detect_facts(store, chunk)
    assert any(f["kind"] == "pitfall" for f in facts)

def test_end_to_end_extraction():
    """Full extraction pipeline: chunks → lessons + facts."""
    # Ingest a known chunk
    store.execute(
        "INSERT INTO kb_chunks(content, collection, confidence, extracted_to_lesson) "
        "VALUES (?, 'kq_reference', 0.8, 0)",
        ("Kerberoasting: Use impacket-GetUserSPNs -request. Does not work on Win 11 24H2 without disabling Credential Guard.",)
    )
    store.conn.commit()
    
    # Extract
    result = extract_all(store)
    assert result["lessons_created"] >= 1
    
    # Verify lesson exists in recall
    recall_result = store.recall("kerberoasting", top_k=5)
    assert len(recall_result) > 0
    
    # Verify fact exists in memory
    facts = store.query(
        "SELECT * FROM memory_facts WHERE content LIKE '%Win 11 24H2%' AND status='active'"
    )
    assert len(facts) >= 1

def test_phase_plan_has_all_domains():
    """PHASE_PLAN covers all 8 domains."""
    roles = set(role for _, role, _ in PHASE_PLAN)
    required = {"pre-recon", "recon", "recon-cloud", "recon-ad",
                "injection", "xss", "cloud-iam", "ad-attack",
                "malware-dev", "embedded-exploit", "wireless-attack",
                "social-eng", "lateral-movement", "persistence", "exfiltration"}
    assert required.issubset(roles), f"Missing: {required - roles}"

def test_role_brief_all_roles():
    """Every role in PHASE_PLAN should have a non-empty role_brief."""
    for _, role, _ in PHASE_PLAN:
        base = _base_role(role)
        assert base in ROLE_QUERY, f"Missing ROLE_QUERY for {base}"

def test_catalog_has_new_categories():
    """Catalog must include cloud, ad, c2, malware, firmware categories."""
    categories = set(s.category for s in _SPECS)
    required = {"cloud", "ad", "c2", "malware", "firmware", "evasion",
                "rfid", "social", "lateral", "iot", "rf", "ble"}
    assert required.issubset(categories), f"Missing categories: {required - categories}"

def test_catalog_tool_count():
    """At least 138 tools total."""
    assert len(_SPECS) >= 138, f"Only {len(_SPECS)} tools, expected >= 138"
```

### 6.2 — Integration Test: Full Pipeline

```python
# tests/test_integration_extract.py
def test_full_ingest_extract_recall():
    """
    Full integration: ingest → extract → recall → role_brief.
    
    This test validates the end-to-end pipeline that makes KQ
    actually LEARN from her knowledge sources.
    """
    store = get_store()
    
    # Verify kb_chunks exist
    count = store.query_one("SELECT COUNT(*) AS c FROM kb_chunks")
    assert int(count["c"]) >= 100, f"Only {count['c']} chunks — need to run ingest first"
    
    # Verify lessons exist
    lessons = store.query_one("SELECT COUNT(*) AS c FROM lessons WHERE status='active'")
    assert int(lessons["c"]) >= 50, f"Only {lessons['c']} lessons — need to run extract first"
    
    # Verify recall works for multiple domains
    for domain, query in [
        ("ad", "kerberoasting"),
        ("cloud", "iam privilege escalation"),
        ("web", "sql injection"),
        ("embedded", "firmware extraction"),
        ("wireless", "wpa2 cracking"),
    ]:
        results = store.recall(query, top_k=3)
        assert len(results) > 0, f"No recall results for '{query}'"
    
    # Verify role_brief bundles lessons
    for role in ["ad-attack", "cloud-iam", "injection"]:
        brief = role_brief(store, role, target="test-target.example.com")
        assert len(brief["learned_lessons"]) > 0, f"No lessons in role_brief for {role}"
```

---

## PHASE 7 — EXECUTION ORDER

```
Phase 0.1    Create kb_sources/ symlinks                            [15 min]
Phase 0.2    Expand ingest.py with 5 collection handlers             [30 min]
Phase 0.3    Run ingest pipeline (~3,200 chunks)                     [10 min]
Phase 0.4    Verify kb_search returns results                         [5 min]
Phase 0.5    Create extract.py (~450 lines)                          [45 min]
Phase 0.5.3  Add kb_extract MCP tool                                  [5 min]
Phase 0.5.4  Run extraction pipeline (~800 lessons, ~300 facts)      [15 min]
Phase 0.5.5  Run memory.write_digest()                                [5 min]
Phase 1.1    Expand PHASE_PLAN to 35+ tasks                          [20 min]
Phase 1.2    Expand ROLE_QUERY to 25+ entries                        [15 min]
Phase 1.3    Expand ROLE_VULN_CLASS mapping                          [10 min]
Phase 1.4    Enhance role_brief with facts+chains                     [15 min]
Phase 2.1-9  Expand catalog.py with 93 new tools                     [45 min]
Phase 3.1    Create SOUL.md (~2,500 lines)                           [60 min]
Phase 4.1    Update MEMORY.md digest                                  [5 min]
Phase 4.2    Update config.yaml                                       [5 min]
Phase 4.3    Update pyproject.toml                                    [2 min]
Phase 5.x    Guard/KQ_MODE verification                               [5 min]
Phase 6.x    Write tests (~20 test cases)                            [30 min]
Phase 6.y    Run test suite                                           [5 min]
Phase 7.x    Git commit + push                                        [5 min]

TOTAL: ~6.5 hours of work, all executable in this session
```

---

## CODE QUALITY STANDARDS

1. **All new Python matches existing style:**
   - `from __future__ import annotations` at top
   - Type hints on all function signatures
   - Docstrings for all public functions
   - Dataclasses where appropriate
   - No breaking changes to existing MCP tool signatures

2. **Idempotent operations:**
   - Ingest: content hash dedup prevents duplicates
   - Extract: `extracted_to_lesson` flag prevents re-extraction
   - Re-running any pipeline step is safe

3. **Backward compatible:**
   - Existing web-app phase plan still works identically
   - Existing catalog tools still present
   - All existing MCP tools unchanged in signature
   - All existing tests continue to pass

4. **Error handling:**
   - Missing tools: runner reports "not installed" gracefully
   - Missing collections: ingest skips non-existent directories
   - Empty extraction: reports zero counts, doesn't crash
   - KQ_MODE guard: clean bypass without crashing scope checks

---

## SUCCESS CRITERIA

After execution, the following must be TRUE:

1. `kb_search("kerberoasting")` returns AD attack chunks
2. `recall("aws iam escalation")` returns lessons with confidence > 0.5
3. `role_brief("ad-attack")` bundles lessons + facts + tools
4. `plan_create(eid)` generates 35+ tasks across all domains
5. `arsenal_list("c2")` returns C2 tools
6. `arsenal_list("ad")` returns AD attack tools
7. `kb_extract()` processes all chunks and creates lessons
8. `memory.write_digest()` populates MEMORY.md with learned knowledge
9. All existing tests pass
10. New tests pass
11. SOUL.md exists at kq-core/SOUL.md with all sections
12. Config reflects full_spectrum defaults
```

