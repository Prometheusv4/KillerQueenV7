"""Verification: hybrid recall returns relevant, ranks by confidence, misses cleanly."""
from kq_core import learning, memory


def test_recall_relevant_and_miss(store):
    learning.lesson_save(store, summary="WordPress XMLRPC canonical legacy endpoint",
                         category="recon", action_do="probe xmlrpc")
    learning.lesson_save(store, summary="AWS IMDS SSRF metadata credentials",
                         category="exploitation", action_do="hit 169.254")
    memory.remember(store, "NetExec nxc installed at /usr/bin/nxc", kind="weapon")

    res = store.recall("xmlrpc legacy endpoint")
    assert res and res[0]["summary"].lower().startswith("wordpress")

    assert store.recall("totally unrelated zzz qux plover") == []

    facts = store.recall("netexec nxc", include=("fact",))
    assert facts and facts[0]["type"] == "fact"


def test_recall_confidence_tiebreak(store):
    learning.lesson_save(store, summary="sharedterm alpha one", category="tool", action_do="x")
    b = learning.lesson_save(store, summary="sharedterm beta two", category="tool", action_do="y")
    for _ in range(3):
        learning.lesson_outcome(store, b["lesson_id"], "success")  # b becomes higher confidence
    res = store.recall("sharedterm")
    assert len(res) == 2
    assert res[0]["id"] == b["lesson_id"]  # higher confidence ranks first on equal keyword score


def test_recall_semantic(sem_store):
    s = sem_store
    learning.lesson_save(s, summary="server side request forgery reaches cloud metadata",
                         category="exploitation", action_do="hit 169.254.169.254")
    learning.lesson_save(s, summary="cross site scripting in search parameter",
                         category="exploitation", action_do="inject script")
    res = s.recall("metadata cloud request forgery")
    assert res and "request forgery" in res[0]["summary"]


def test_recall_semantic_miss_returns_empty(sem_store):
    s = sem_store
    learning.lesson_save(s, summary="wordpress xmlrpc legacy protocol endpoint",
                         category="recon", action_do="probe xmlrpc")
    # No token overlap -> cosine below the semantic floor -> clean miss, not NN noise.
    assert s.recall("quantum chromodynamics unrelated zzz plover") == []
