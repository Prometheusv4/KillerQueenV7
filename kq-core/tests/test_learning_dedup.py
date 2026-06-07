"""Verification step 2: learning dedups (both FTS jaccard and semantic cosine paths)."""
from kq_core import learning


def test_dedup_fts_merges_paraphrase(store):
    assert not store.semantic  # FTS keyword mode
    r1 = learning.lesson_save(store, summary="WordPress XMLRPC is the canonical legacy protocol endpoint",
                              category="recon", action_do="probe xmlrpc.php first")
    assert r1["action"] == "inserted"
    r2 = learning.lesson_save(store, summary="WordPress XMLRPC canonical legacy protocol endpoint",
                              category="recon", action_do="probe xmlrpc php first")
    assert r2["action"] == "merged"
    assert r2["lesson_id"] == r1["lesson_id"]

    r3 = learning.lesson_save(store, summary="AWS IMDSv1 SSRF yields temporary credentials",
                              category="recon", action_do="hit 169.254.169.254")
    assert r3["action"] == "inserted"

    assert store.query_one("SELECT revisions FROM lessons WHERE id=?", (r1["lesson_id"],))["revisions"] == 1
    assert store.query_one("SELECT COUNT(*) c FROM lessons")["c"] == 2


def test_dedup_semantic_merges(sem_store):
    s = sem_store
    assert s.semantic
    r1 = learning.lesson_save(s, summary="aws imds v1 ssrf yields temporary credentials",
                              category="exploitation", action_do="hit metadata endpoint")
    assert r1["action"] == "inserted"
    r2 = learning.lesson_save(s, summary="aws imds v1 ssrf yields temporary credentials now",
                              category="exploitation", action_do="hit metadata endpoint quickly")
    assert r2["action"] == "merged"
    assert r2["similarity"] >= 0.86

    r3 = learning.lesson_save(s, summary="jwt alg none signature stripping bypass",
                              category="exploitation", action_do="strip the sig")
    assert r3["action"] == "inserted"


def test_dedup_respects_category(store):
    a = learning.lesson_save(store, summary="same exact wording here friend", category="recon", action_do="z")
    b = learning.lesson_save(store, summary="same exact wording here friend", category="evasion", action_do="z")
    assert a["action"] == "inserted" and b["action"] == "inserted"  # different category -> not merged
