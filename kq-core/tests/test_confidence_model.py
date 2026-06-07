"""Verification step 3: confidence boosts on success, decays on failure, bands + archive."""
from kq_core import learning


def test_success_boost_and_failure_decay(store):
    r = learning.lesson_save(store, summary="alpha unique lesson tokens", category="tool", action_do="do x")
    assert r["confidence"] == 0.5
    o1 = learning.lesson_outcome(store, r["lesson_id"], "success")
    assert round(o1["confidence"], 4) == 0.625  # 0.5 + (1-0.5)*0.25
    o2 = learning.lesson_outcome(store, r["lesson_id"], "success")
    assert o2["confidence"] > o1["confidence"]

    r2 = learning.lesson_save(store, summary="beta distinct words zzz qqq", category="tool", action_do="do y")
    o3 = learning.lesson_outcome(store, r2["lesson_id"], "failure")
    assert round(o3["confidence"], 4) == 0.275  # 0.5 * 0.55


def test_band_reaches_high(store):
    r = learning.lesson_save(store, summary="gamma lesson www distinct", category="tool", action_do="z")
    for _ in range(4):
        learning.lesson_outcome(store, r["lesson_id"], "success")
    row = store.query_one("SELECT confidence, band FROM lessons WHERE id=?", (r["lesson_id"],))
    assert row["band"] == "HIGH" and row["confidence"] >= 0.75


def test_archive_on_repeated_failure(store):
    r = learning.lesson_save(store, summary="delta lesson qqq distinct", category="tool", action_do="z")
    lid = r["lesson_id"]
    learning.lesson_outcome(store, lid, "failure")          # 0.275, rev1 -> active
    o = learning.lesson_outcome(store, lid, "failure")      # 0.151, rev2 -> archived
    assert o["status"] == "archived"
    assert store.query_one("SELECT status FROM lessons WHERE id=?", (lid,))["status"] == "archived"
    # archived lessons drop out of recall
    assert store.recall("delta lesson qqq") == []


def test_outcome_unknown_lesson(store):
    assert learning.lesson_outcome(store, 999, "success")["ok"] is False
