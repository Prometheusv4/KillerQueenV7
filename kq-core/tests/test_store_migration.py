"""Verification: migration imports real profile memory + references (idempotently),
and the responsible-use denylist skips worm-construction files."""
from pathlib import Path

import pytest

from kq_core import migrate

PROFILE_DIR = Path(__file__).resolve().parents[2] / "profile"
pytestmark = pytest.mark.skipif(not PROFILE_DIR.exists(), reason="profile/ not present")


def test_migrate_real_profile(store):
    c = migrate.migrate_profile(store, PROFILE_DIR)
    assert c["lessons_inserted"] >= 8          # the CRITICAL LESSONS bullets
    assert c["operator"] >= 5                   # OPERATOR.md directives/priorities
    assert c["references"] > 50                 # chunked reference corpus
    assert any("worm" in s for s in c["skipped"])  # denylist enforced + reported
    assert store.recall("xmlrpc legacy endpoint")  # migrated knowledge is retrievable


def test_migrate_idempotent(store):
    c1 = migrate.migrate_profile(store, PROFILE_DIR)
    c2 = migrate.migrate_profile(store, PROFILE_DIR)
    assert c2["lessons_inserted"] <= 2          # second pass merges, doesn't duplicate
    assert c2["lessons_merged"] >= c1["lessons_inserted"] - 2
    n = store.query_one("SELECT COUNT(*) c FROM lessons")["c"]
    assert n <= c1["lessons_inserted"] + 2      # no lesson explosion
