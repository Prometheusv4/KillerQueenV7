"""The deterministic learning loop: dedup, confidence model, trigger detection.

This is the module that makes "Killer Queen learns" *true* rather than prose. All
thresholds come from :class:`kq_core.config.Config` (env-overridable) so behaviour is
tunable without code changes.
"""
from __future__ import annotations

import json
from typing import Any, Optional

from . import vectors
from .util import jaccard, now_iso, parse_iso, tokenize

_LESSON_COLS = (
    "id, summary, category, trigger_when, action_do, rationale, confidence, band, "
    "revisions, successes, failures, source, embedding_id, status, target_fingerprint, "
    "vuln_class, created_at, updated_at, last_used_at"
)


def band_of(confidence: float) -> str:
    if confidence >= 0.75:
        return "HIGH"
    if confidence >= 0.45:
        return "MED"
    return "LOW"


def c_eff(store: Any, confidence: float, ref_ts: Optional[str], now: Optional[str] = None) -> float:
    """Staleness-decayed confidence for *ranking only* (never persisted)."""
    if not ref_ts:
        return confidence
    half = store.cfg.stale_halflife_days or 180.0
    try:
        age_days = max(0.0, (parse_iso(now or now_iso()) - parse_iso(ref_ts)).total_seconds() / 86400.0)
    except (ValueError, TypeError):
        return confidence
    return confidence * (0.5 ** (age_days / half))


def _dedup_match(store: Any, category: str, text: str, qunit) -> Optional[tuple[int, float]]:
    """Find an existing active lesson in ``category`` that this restates. Returns (id, sim)."""
    rows = store.query(
        "SELECT id, embedding_id, summary, trigger_when, action_do, rationale "
        "FROM lessons WHERE status='active' AND category=?",
        (category,),
    )
    if not rows:
        return None
    if qunit is not None:
        ids = [int(r["id"]) for r in rows]
        vecs = [store.get_unit_vector(r["embedding_id"]) for r in rows]
        sim, idx = vectors.max_cosine(qunit, vecs)
        if idx >= 0 and sim >= store.cfg.dedup_semantic:
            return ids[idx], sim
        return None
    # FTS / no-embedder mode: jaccard over token sets.
    qtok = tokenize(text)
    best, best_id = 0.0, -1
    for r in rows:
        cand = tokenize(f"{r['summary']} {r['trigger_when']} {r['action_do']} {r['rationale']}")
        s = jaccard(qtok, cand)
        if s > best:
            best, best_id = s, int(r["id"])
    if best_id >= 0 and best >= store.cfg.dedup_fts:
        return best_id, best
    return None


def lesson_save(
    store: Any,
    *,
    summary: str,
    category: str,
    trigger_when: str = "",
    action_do: str = "",
    rationale: str = "",
    source: Optional[str] = None,
    target_fingerprint: Optional[str] = None,
    vuln_class: Optional[str] = None,
) -> dict:
    """Insert a lesson, or merge into a near-duplicate (bumping revisions + confidence)."""
    text = f"{summary} {action_do}".strip()
    qunit = store.embed_query_unit(text) if store.semantic else None
    match = _dedup_match(store, category, text, qunit)
    ts = now_iso()

    if match is not None:
        lid, sim = match
        with store.lock:
            row = store.conn.execute("SELECT confidence FROM lessons WHERE id=?", (lid,)).fetchone()
            c = float(row["confidence"])
            c = c + (1.0 - c) * store.cfg.conf_corroborate  # weak corroboration
            store.conn.execute(
                "UPDATE lessons SET revisions=revisions+1, confidence=?, updated_at=?, last_used_at=? "
                "WHERE id=?",
                (round(c, 6), ts, ts, lid),
            )
            store.conn.commit()
        return {
            "ok": True, "lesson_id": lid, "action": "merged",
            "similarity": round(float(sim), 4), "confidence": round(c, 6), "band": band_of(c),
        }

    emb_id = store.put_embedding(text) if store.semantic else None
    c0 = store.cfg.conf_init
    with store.lock:
        cur = store.conn.execute(
            "INSERT INTO lessons(summary, category, trigger_when, action_do, rationale, confidence, "
            "source, embedding_id, target_fingerprint, vuln_class, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (summary, category, trigger_when, action_do, rationale, c0, source, emb_id,
             target_fingerprint, vuln_class, ts, ts),
        )
        store.conn.commit()
        lid = int(cur.lastrowid)
    return {"ok": True, "lesson_id": lid, "action": "inserted",
            "confidence": round(c0, 6), "band": band_of(c0)}


def lesson_outcome(store: Any, lesson_id: int, outcome: str) -> dict:
    """Boost (success) or decay (failure) a lesson's confidence on re-validation."""
    row = store.query_one("SELECT confidence, revisions FROM lessons WHERE id=?", (lesson_id,))
    if row is None:
        return {"ok": False, "error": f"lesson {lesson_id} not found"}
    c = float(row["confidence"])
    ts = now_iso()
    if outcome == "success":
        c = c + (1.0 - c) * store.cfg.conf_success
        col = "successes"
    elif outcome == "failure":
        c = c * store.cfg.conf_failure
        col = "failures"
    else:
        return {"ok": False, "error": "outcome must be 'success' or 'failure'"}

    status = "active"
    archive = (c < store.cfg.archive_conf) and ((int(row["revisions"]) + 1) >= store.cfg.archive_revisions)
    with store.lock:
        store.conn.execute(
            f"UPDATE lessons SET confidence=?, {col}={col}+1, revisions=revisions+1, "
            f"updated_at=?, last_used_at=?, status=? WHERE id=?",
            (round(c, 6), ts, ts, "archived" if archive else "active", lesson_id),
        )
        store.conn.commit()
    if archive:
        status = "archived"
    return {"ok": True, "lesson_id": lesson_id, "confidence": round(c, 6),
            "band": band_of(c), "status": status}


# ── 5-trigger detection ──────────────────────────────────────────────────────

def detect_triggers(store: Any, engagement_id: Optional[int], workflow_summary: Optional[str] = None) -> list[dict]:
    """Evaluate the five skill-creation triggers against real store/audit data."""
    fired: list[dict] = []

    if engagement_id is not None:
        # T1 — high-complexity workflow: >=5 distinct tools used this engagement.
        row = store.query_one(
            "SELECT COUNT(DISTINCT tool) AS c FROM audit_log WHERE engagement_id=?",
            (engagement_id,),
        )
        if row and int(row["c"]) >= 5:
            fired.append({"id": "T1", "reason": f"{int(row['c'])} distinct tools used this engagement"})

        # T2 — a tricky error overcome (>=3 attempts + a recorded resolution) in scratch.
        st = store.query_one(
            "SELECT scratch FROM engagement_state WHERE engagement_id=?", (engagement_id,)
        )
        if st:
            try:
                errors = (json.loads(st["scratch"]) or {}).get("errors", {})
            except (TypeError, ValueError, json.JSONDecodeError):
                errors = {}
            for sig, info in (errors.items() if isinstance(errors, dict) else []):
                if isinstance(info, dict) and int(info.get("attempts", 0)) >= 3 and info.get("resolution"):
                    fired.append({"id": "T2", "reason": f"error '{sig}' solved after {info['attempts']} attempts"})
                    break

        # T5 — explicit operator directive recorded this engagement.
        row = store.query_one(
            "SELECT COUNT(*) AS c FROM audit_log WHERE engagement_id=? AND action='operator_directive'",
            (engagement_id,),
        )
        if row and int(row["c"]) > 0:
            fired.append({"id": "T5", "reason": "operator directive recorded"})

    # T4 — a corroborated lesson cluster (>=2 independent restatements).
    row = store.query_one("SELECT COUNT(*) AS c FROM lessons WHERE status='active' AND revisions>=2")
    if row and int(row["c"]) > 0:
        fired.append({"id": "T4", "reason": f"{int(row['c'])} corroborated lesson(s) (revisions>=2)"})

    # T3 — novel workflow: nothing in memory covers this summary.
    if workflow_summary:
        res = store.recall(workflow_summary, top_k=1)
        top = res[0]["score"] if res else 0.0
        if top < store.cfg.novelty_threshold:
            fired.append({"id": "T3", "reason": f"novel (best recall score {top:.2f} < {store.cfg.novelty_threshold})"})

    return fired
