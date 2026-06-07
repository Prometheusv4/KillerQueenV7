"""Verification steps 1 & 4: digest renders lessons + corrections into MEMORY.md,
preserves operator-authored content outside the markers, and is idempotent."""
from kq_core import learning, memory


def test_digest_markers_and_content(store, tmp_path):
    learning.lesson_save(store, summary="XMLRPC canonical legacy endpoint", category="recon", action_do="probe")
    memory.remember(store, "always prefer ffuf over gobuster", scope="operator", kind="correction")
    target = tmp_path / "MEMORY.md"
    res = memory.write_digest(store, target)
    assert res["active_lessons"] == 1

    txt = target.read_text(encoding="utf-8")
    assert memory.BEGIN in txt and memory.END in txt
    assert "XMLRPC canonical legacy endpoint" in txt
    assert "ffuf over gobuster" in txt


def test_digest_preserves_external_content_and_is_idempotent(store, tmp_path):
    learning.lesson_save(store, summary="lesson one alpha distinct", category="tool", action_do="x")
    target = tmp_path / "MEMORY.md"
    target.write_text("# Hand-written operator memory\n- keep this line\n", encoding="utf-8")

    memory.write_digest(store, target)
    txt = target.read_text(encoding="utf-8")
    assert "keep this line" in txt and memory.BEGIN in txt

    memory.write_digest(store, target)  # second write
    txt2 = target.read_text(encoding="utf-8")
    assert txt2.count(memory.BEGIN) == 1 and txt2.count(memory.END) == 1
    assert "keep this line" in txt2
