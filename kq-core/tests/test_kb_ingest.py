"""Phase 2 verification: ingest captures frontmatter mappings, kb_search retrieves +
filters by collection/vuln_class, and re-ingest is idempotent."""
import pytest

from kq_core import ingest
from kq_core.ingest import default_paths

_ANTH_SKILL = """---
name: analyzing-test-malware
description: Analyze test malware samples with the foo tool. Use when triaging a suspicious binary.
domain: cybersecurity
subdomain: malware-analysis
tags: [malware, ghidra]
mitre_attack: [T1059.001]
atlas_techniques: [AML.T0047]
nist_csf: [DE.CM-01]
---

## When to Use
When you have a suspicious binary to triage.

## Workflow
1. Run ghidra on the sample.
2. Extract the embedded config block.

## Verification
Config fields are present and decoded.
"""


def _make_anthropic(tmp_path):
    d = tmp_path / "anth" / "skills" / "analyzing-test-malware"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(_ANTH_SKILL, encoding="utf-8")
    return tmp_path / "anth"


def test_ingest_anthropic_captures_frontmatter_and_searches(store, tmp_path):
    root = _make_anthropic(tmp_path)
    c = ingest.ingest_anthropic_skills(store, root)
    assert c["files"] == 1 and c["inserted"] >= 2

    row = store.query_one(
        "SELECT mitre, nist, tags, collection FROM kb_chunks WHERE source='analyzing-test-malware' LIMIT 1")
    assert "T1059.001" in row["mitre"] and "AML.T0047" in row["mitre"]
    assert "DE.CM-01" in row["nist"]
    assert "malware" in row["tags"]
    assert row["collection"] == "anthropic_skill"

    res = store.kb_search("ghidra extract config malware", collection="anthropic_skill")
    assert res and res[0]["source"] == "analyzing-test-malware"
    # a different collection filter excludes it
    assert store.kb_search("ghidra extract config malware", collection="scope") == []


def test_ingest_idempotent(store, tmp_path):
    root = _make_anthropic(tmp_path)
    c1 = ingest.ingest_anthropic_skills(store, root)
    c2 = ingest.ingest_anthropic_skills(store, root)
    assert c2["inserted"] == 0 and c2["duplicate"] >= c1["inserted"]


def test_ingest_bughunter_real_corpus(store):
    paths = default_paths()
    if not paths["bughunter"]:
        pytest.skip("Claude-BugHunter corpus not present")
    c = ingest.ingest_bughunter(store, paths["bughunter"])
    assert c["inserted"] > 100
    res = store.kb_search("ssrf reaches cloud metadata credentials", vuln_class="ssrf")
    assert res and res[0]["vuln_class"] == "ssrf"
