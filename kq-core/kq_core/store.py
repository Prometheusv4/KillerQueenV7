"""SQLite persistence backbone: schema/migrations, embeddings, FTS5, hybrid recall.

Import-light at module load (only stdlib). ``numpy`` and the embedder are imported
lazily inside the methods that need them, so importing :mod:`kq_core.store` never drags
in heavy deps.

Lesson columns use ``trigger_when`` / ``action_do`` (not ``trigger`` / ``action``) to
avoid SQLite reserved-word friction inside the FTS5 sync triggers; the MCP tool layer
maps the public ``trigger`` / ``action`` params onto these.
"""
from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Any, Iterable, Optional

from . import config as _config
from .util import now_iso, tokenize, jaccard

SCHEMA_VERSION = 2
_SEM_FLOOR = 0.15  # drop semantic-only candidates below this cosine (clean miss -> [])

_SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS engagements (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  type TEXT NOT NULL CHECK(type IN ('bug_bounty','red_team','pentest','full_spectrum')),
  status TEXT NOT NULL DEFAULT 'active',
  roe_summary TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  closed_at TEXT
);

CREATE TABLE IF NOT EXISTS engagement_state (
  engagement_id INTEGER PRIMARY KEY REFERENCES engagements(id) ON DELETE CASCADE,
  phase TEXT NOT NULL DEFAULT 'scope',
  active_vectors TEXT NOT NULL DEFAULT '[]',
  running_workers TEXT NOT NULL DEFAULT '[]',
  deployed_payloads TEXT NOT NULL DEFAULT '[]',
  chain_candidates TEXT NOT NULL DEFAULT '[]',
  target_fingerprint TEXT,
  scratch TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lessons (
  id INTEGER PRIMARY KEY,
  summary TEXT NOT NULL,
  category TEXT NOT NULL,
  trigger_when TEXT NOT NULL DEFAULT '',
  action_do TEXT NOT NULL DEFAULT '',
  rationale TEXT NOT NULL DEFAULT '',
  confidence REAL NOT NULL DEFAULT 0.5,
  band TEXT GENERATED ALWAYS AS (
    CASE WHEN confidence >= 0.75 THEN 'HIGH'
         WHEN confidence >= 0.45 THEN 'MED'
         ELSE 'LOW' END) VIRTUAL,
  revisions INTEGER NOT NULL DEFAULT 0,
  successes INTEGER NOT NULL DEFAULT 0,
  failures INTEGER NOT NULL DEFAULT 0,
  source TEXT,
  embedding_id INTEGER REFERENCES embeddings(id),
  status TEXT NOT NULL DEFAULT 'active',
  target_fingerprint TEXT,
  vuln_class TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  last_used_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_lessons_cat ON lessons(category, status);
CREATE INDEX IF NOT EXISTS idx_lessons_status ON lessons(status);

CREATE TABLE IF NOT EXISTS memory_facts (
  id INTEGER PRIMARY KEY,
  content TEXT NOT NULL,
  scope TEXT NOT NULL DEFAULT 'kq',
  kind TEXT,
  confidence REAL NOT NULL DEFAULT 0.6,
  source TEXT,
  embedding_id INTEGER REFERENCES embeddings(id),
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_facts_scope ON memory_facts(scope, status);
CREATE INDEX IF NOT EXISTS idx_facts_kind ON memory_facts(kind);

CREATE TABLE IF NOT EXISTS findings (
  id INTEGER PRIMARY KEY,
  engagement_id INTEGER REFERENCES engagements(id) ON DELETE CASCADE,
  vuln_class TEXT NOT NULL,
  severity TEXT NOT NULL DEFAULT 'info'
    CHECK(severity IN ('info','low','medium','high','critical')),
  target TEXT NOT NULL,
  url TEXT,
  payload TEXT,
  evidence_ref TEXT,
  status TEXT NOT NULL DEFAULT 'candidate'
    CHECK(status IN ('candidate','validated','reported','duplicate','invalid')),
  verdict TEXT NOT NULL DEFAULT 'unknown'
    CHECK(verdict IN ('unknown','exploited','blocked_by_security','out_of_scope_internal','false_positive')),
  scope_verdict TEXT NOT NULL DEFAULT 'unknown',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_findings_eng ON findings(engagement_id, status);

CREATE TABLE IF NOT EXISTS scope_rules (
  id INTEGER PRIMARY KEY,
  engagement_id INTEGER REFERENCES engagements(id) ON DELETE CASCADE,
  kind TEXT NOT NULL CHECK(kind IN ('in','out')),
  pattern TEXT NOT NULL,
  pattern_type TEXT NOT NULL DEFAULT 'glob'
    CHECK(pattern_type IN ('glob','regex','cidr','exact')),
  note TEXT,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_scope_eng ON scope_rules(engagement_id, kind);

CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY,
  ts TEXT NOT NULL,
  engagement_id INTEGER,
  actor TEXT NOT NULL DEFAULT 'agent',
  tool TEXT NOT NULL,
  action TEXT NOT NULL,
  target TEXT,
  verdict TEXT,
  args_digest TEXT,
  result_digest TEXT,
  prev_hash TEXT,
  row_hash TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit_log
  BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit_log
  BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;

CREATE TABLE IF NOT EXISTS tool_cache (
  cmd_hash TEXT PRIMARY KEY,
  target TEXT,
  result_ref TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS embeddings (
  id INTEGER PRIMARY KEY,
  dim INTEGER NOT NULL,
  model TEXT NOT NULL,
  vector BLOB NOT NULL,
  norm REAL NOT NULL
);

-- Phase 2: curated knowledge base (distinct from operational lessons/facts).
CREATE TABLE IF NOT EXISTS kb_chunks (
  id INTEGER PRIMARY KEY,
  collection TEXT NOT NULL,          -- anthropic_skill | hunt_pattern | scope | reference | tool_doc
  source TEXT NOT NULL,              -- skill name / relative path
  title TEXT,
  chunk_index INTEGER NOT NULL DEFAULT 0,
  vuln_class TEXT,
  mitre TEXT,                         -- comma-joined ATT&CK/ATLAS ids
  nist TEXT,                          -- comma-joined NIST CSF ids
  tags TEXT,
  content TEXT NOT NULL,
  content_hash TEXT,
  embedding_id INTEGER REFERENCES embeddings(id),
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL,
  extracted_to_lesson INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_kb_collection ON kb_chunks(collection, status);
CREATE INDEX IF NOT EXISTS idx_kb_extracted ON kb_chunks(extracted_to_lesson);
CREATE INDEX IF NOT EXISTS idx_kb_vuln ON kb_chunks(vuln_class);
CREATE INDEX IF NOT EXISTS idx_kb_source ON kb_chunks(source, chunk_index);
CREATE UNIQUE INDEX IF NOT EXISTS idx_kb_hash ON kb_chunks(content_hash);

-- Phase 4: persistent attack-chain graph + orchestration phase plan.
CREATE TABLE IF NOT EXISTS chain_nodes (
  id INTEGER PRIMARY KEY,
  engagement_id INTEGER REFERENCES engagements(id) ON DELETE CASCADE,
  node_type TEXT NOT NULL CHECK(node_type IN ('target','action','vulnerability')),
  label TEXT NOT NULL,
  ref_id INTEGER,
  risk_score INTEGER NOT NULL DEFAULT 0,
  metadata TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chain_nodes_eng ON chain_nodes(engagement_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_chain_node_ref ON chain_nodes(engagement_id, node_type, ref_id);

CREATE TABLE IF NOT EXISTS chain_edges (
  id INTEGER PRIMARY KEY,
  engagement_id INTEGER REFERENCES engagements(id) ON DELETE CASCADE,
  source_id INTEGER NOT NULL REFERENCES chain_nodes(id) ON DELETE CASCADE,
  target_id INTEGER NOT NULL REFERENCES chain_nodes(id) ON DELETE CASCADE,
  edge_type TEXT NOT NULL DEFAULT 'leads_to'
    CHECK(edge_type IN ('leads_to','discovers','enables','depends_on')),
  weight INTEGER NOT NULL DEFAULT 3,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chain_edges_eng ON chain_edges(engagement_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_chain_edge_uniq ON chain_edges(engagement_id, source_id, target_id);

CREATE TABLE IF NOT EXISTS plan_tasks (
  id INTEGER PRIMARY KEY,
  engagement_id INTEGER REFERENCES engagements(id) ON DELETE CASCADE,
  phase TEXT NOT NULL,
  role TEXT NOT NULL,
  depends_on TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK(status IN ('pending','running','done','skipped')),
  result_ref TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_plan_eng ON plan_tasks(engagement_id, status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_plan_role ON plan_tasks(engagement_id, role);
"""

# FTS5 mirrors are created separately so we can degrade gracefully if FTS5 is absent.
_FTS_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS lessons_fts USING fts5(
  summary, trigger_when, action_do, rationale,
  content='lessons', content_rowid='id'
);
CREATE TRIGGER IF NOT EXISTS lessons_ai AFTER INSERT ON lessons BEGIN
  INSERT INTO lessons_fts(rowid, summary, trigger_when, action_do, rationale)
  VALUES (new.id, new.summary, new.trigger_when, new.action_do, new.rationale);
END;
CREATE TRIGGER IF NOT EXISTS lessons_ad AFTER DELETE ON lessons BEGIN
  INSERT INTO lessons_fts(lessons_fts, rowid, summary, trigger_when, action_do, rationale)
  VALUES ('delete', old.id, old.summary, old.trigger_when, old.action_do, old.rationale);
END;
CREATE TRIGGER IF NOT EXISTS lessons_au AFTER UPDATE ON lessons BEGIN
  INSERT INTO lessons_fts(lessons_fts, rowid, summary, trigger_when, action_do, rationale)
  VALUES ('delete', old.id, old.summary, old.trigger_when, old.action_do, old.rationale);
  INSERT INTO lessons_fts(rowid, summary, trigger_when, action_do, rationale)
  VALUES (new.id, new.summary, new.trigger_when, new.action_do, new.rationale);
END;

CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
  content, content='memory_facts', content_rowid='id'
);
CREATE TRIGGER IF NOT EXISTS facts_ai AFTER INSERT ON memory_facts BEGIN
  INSERT INTO memory_fts(rowid, content) VALUES (new.id, new.content);
END;
CREATE TRIGGER IF NOT EXISTS facts_ad AFTER DELETE ON memory_facts BEGIN
  INSERT INTO memory_fts(memory_fts, rowid, content) VALUES ('delete', old.id, old.content);
END;
CREATE TRIGGER IF NOT EXISTS facts_au AFTER UPDATE ON memory_facts BEGIN
  INSERT INTO memory_fts(memory_fts, rowid, content) VALUES ('delete', old.id, old.content);
  INSERT INTO memory_fts(rowid, content) VALUES (new.id, new.content);
END;

CREATE VIRTUAL TABLE IF NOT EXISTS kb_fts USING fts5(
  title, content, tags, content='kb_chunks', content_rowid='id'
);
CREATE TRIGGER IF NOT EXISTS kb_ai AFTER INSERT ON kb_chunks BEGIN
  INSERT INTO kb_fts(rowid, title, content, tags) VALUES (new.id, new.title, new.content, new.tags);
END;
CREATE TRIGGER IF NOT EXISTS kb_ad AFTER DELETE ON kb_chunks BEGIN
  INSERT INTO kb_fts(kb_fts, rowid, title, content, tags) VALUES ('delete', old.id, old.title, old.content, old.tags);
END;
CREATE TRIGGER IF NOT EXISTS kb_au AFTER UPDATE ON kb_chunks BEGIN
  INSERT INTO kb_fts(kb_fts, rowid, title, content, tags) VALUES ('delete', old.id, old.title, old.content, old.tags);
  INSERT INTO kb_fts(rowid, title, content, tags) VALUES (new.id, new.title, new.content, new.tags);
END;
"""


def _fts_match_query(text: str) -> Optional[str]:
    """Turn arbitrary text into a safe FTS5 MATCH expression (``tok1 OR tok2 ...``)."""
    toks = [t for t in tokenize(text) if len(t) > 1]
    if not toks:
        return None
    return " OR ".join(sorted(toks))


class Store:
    """Owns the SQLite connection, schema, embeddings, and hybrid retrieval."""

    def __init__(
        self,
        db_path: Optional[Path | str] = None,
        *,
        cfg: Optional[_config.Config] = None,
        embedder: Any = None,
    ) -> None:
        if cfg is not None:
            self.cfg = cfg
        elif db_path is not None:
            self.cfg = _config.for_db(Path(db_path))
        else:
            self.cfg = _config.get_config()
        self.db_path = Path(db_path) if db_path is not None else self.cfg.db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.RLock()
        self._embedder = embedder  # may be None -> lazily resolved
        self._embedder_resolved = embedder is not None
        self.has_fts = False
        self.migrate()

    # ── lifecycle ────────────────────────────────────────────────────────────
    def migrate(self) -> None:
        with self.lock:
            self.conn.executescript(_SCHEMA_SQL)
            try:
                self.conn.executescript(_FTS_SQL)
                self.has_fts = True
            except sqlite3.OperationalError:
                self.has_fts = False  # FTS5 not compiled in -> keyword via LIKE/jaccard
            row = self.conn.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
            current = int(row["version"]) if row else 0
            if current < 2:
                # v1 → v2: add extracted_to_lesson column for knowledge extraction tracking
                try:
                    self.conn.execute(
                        "ALTER TABLE kb_chunks ADD COLUMN extracted_to_lesson INTEGER NOT NULL DEFAULT 0"
                    )
                except sqlite3.OperationalError:
                    pass  # column already exists
                self.conn.execute(
                    "INSERT OR REPLACE INTO schema_version(version) VALUES (?)",
                    (SCHEMA_VERSION,)
                )
            elif current == 0:
                self.conn.execute("INSERT INTO schema_version(version) VALUES (?)", (SCHEMA_VERSION,))
            self.conn.commit()

    def close(self) -> None:
        try:
            self.conn.commit()
        finally:
            self.conn.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ── tiny exec helpers (all writes take the lock) ──────────────────────────
    def execute(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        with self.lock:
            cur = self.conn.execute(sql, tuple(params))
            self.conn.commit()
            return cur

    def query(self, sql: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
        return self.conn.execute(sql, tuple(params)).fetchall()

    def query_one(self, sql: str, params: Iterable[Any] = ()) -> Optional[sqlite3.Row]:
        return self.conn.execute(sql, tuple(params)).fetchone()

    # ── embeddings ────────────────────────────────────────────────────────────
    @property
    def embedder(self) -> Any:
        if not self._embedder_resolved:
            from .embeddings import get_embedder  # lazy: may import torch
            self._embedder = get_embedder(self.cfg)
            self._embedder_resolved = True
        return self._embedder

    @property
    def semantic(self) -> bool:
        return bool(getattr(self.embedder, "available", False))

    def put_embedding(self, text: str) -> Optional[int]:
        """Embed ``text`` and persist the vector; returns its id, or None in FTS mode."""
        if not self.semantic:
            return None
        import numpy as np  # lazy

        vec = np.asarray(self.embedder.encode([text])[0], dtype="float32")
        norm = float(np.linalg.norm(vec)) or 1.0
        with self.lock:
            cur = self.conn.execute(
                "INSERT INTO embeddings(dim, model, vector, norm) VALUES (?,?,?,?)",
                (int(vec.shape[0]), self.embedder.name, vec.tobytes(), norm),
            )
            self.conn.commit()
            return int(cur.lastrowid)

    def get_unit_vector(self, embedding_id: Optional[int]):
        if embedding_id is None:
            return None
        import numpy as np  # lazy

        row = self.query_one("SELECT vector, norm FROM embeddings WHERE id=?", (embedding_id,))
        if row is None:
            return None
        vec = np.frombuffer(row["vector"], dtype="float32")
        norm = row["norm"] or 1.0
        return vec / norm

    def embed_query_unit(self, text: str):
        if not self.semantic:
            return None
        import numpy as np  # lazy

        vec = np.asarray(self.embedder.encode([text])[0], dtype="float32")
        norm = float(np.linalg.norm(vec)) or 1.0
        return vec / norm

    # ── keyword search ────────────────────────────────────────────────────────
    def _fts_scores(self, table: str, fts_table: str, query: str, limit: int) -> dict[int, float]:
        """Return {row_id: quality} where higher = better (BM25, min-max normalized)."""
        match = _fts_match_query(query)
        out: dict[int, float] = {}
        if match and self.has_fts:
            try:
                rows = self.conn.execute(
                    f"SELECT rowid, bm25({fts_table}) AS s FROM {fts_table} "
                    f"WHERE {fts_table} MATCH ? ORDER BY s LIMIT ?",
                    (match, limit),
                ).fetchall()
            except sqlite3.OperationalError:
                rows = []
            if rows:
                quals = {int(r["rowid"]): -float(r["s"]) for r in rows}  # higher = better
                lo, hi = min(quals.values()), max(quals.values())
                if hi > lo:  # floor matches at 0.1 so a real hit is never normalized to 0
                    return {rid: 0.1 + 0.9 * (q - lo) / (hi - lo) for rid, q in quals.items()}
                return {rid: 1.0 for rid in quals}  # single match / all-equal
        # Fallback: jaccard over tokens of the candidate's searchable text.
        qtok = tokenize(query)
        if not qtok:
            return out
        if table == "memory_facts":
            text_col = "content"
        elif table == "kb_chunks":
            text_col = "title || ' ' || content || ' ' || COALESCE(tags,'')"
        else:
            text_col = "summary || ' ' || trigger_when || ' ' || action_do || ' ' || rationale"
        rows = self.conn.execute(
            f"SELECT id, {text_col} AS t FROM {table} WHERE status='active'"
        ).fetchall()
        scored = {int(r["id"]): jaccard(qtok, tokenize(r["t"])) for r in rows}
        scored = {k: v for k, v in scored.items() if v > 0}
        return dict(sorted(scored.items(), key=lambda kv: kv[1], reverse=True)[:limit])

    # ── hybrid recall over lessons + facts ────────────────────────────────────
    def recall(
        self,
        query: str,
        *,
        kinds: Optional[list[str]] = None,
        vuln_class: Optional[str] = None,
        target_fingerprint: Optional[str] = None,
        min_confidence: float = 0.0,
        top_k: int = 8,
        include: tuple[str, ...] = ("lesson", "fact"),
    ) -> list[dict]:
        cands: list[dict] = []
        if "lesson" in include:
            sql = "SELECT * FROM lessons WHERE status='active' AND confidence >= ?"
            params: list[Any] = [min_confidence]
            if vuln_class:
                sql += " AND vuln_class = ?"
                params.append(vuln_class)
            if target_fingerprint:
                sql += " AND (target_fingerprint IS NULL OR target_fingerprint = ?)"
                params.append(target_fingerprint)
            for r in self.query(sql, params):
                d = dict(r)
                d["type"] = "lesson"
                d["_text"] = " ".join(
                    str(d.get(k) or "") for k in ("summary", "trigger_when", "action_do", "rationale")
                )
                cands.append(d)
        if "fact" in include:
            sql = "SELECT * FROM memory_facts WHERE status='active' AND confidence >= ?"
            params = [min_confidence]
            if kinds:
                sql += " AND kind IN (%s)" % ",".join("?" * len(kinds))
                params.extend(kinds)
            for r in self.query(sql, params):
                d = dict(r)
                d["type"] = "fact"
                d["_text"] = str(d.get("content") or "")
                cands.append(d)
        if not cands:
            return []

        pool = max(top_k * 6, 50)
        kw_lessons = self._fts_scores("lessons", "lessons_fts", query, pool) if "lesson" in include else {}
        kw_facts = self._fts_scores("memory_facts", "memory_fts", query, pool) if "fact" in include else {}

        qunit = self.embed_query_unit(query) if self.semantic else None
        sem: dict[tuple[str, int], float] = {}
        if qunit is not None:
            import numpy as np  # lazy

            for d in cands:
                v = self.get_unit_vector(d.get("embedding_id"))
                if v is not None and v.shape == qunit.shape:
                    sem[(d["type"], d["id"])] = float(np.dot(qunit, v))

        w = self.cfg.hybrid_weight
        results: list[dict] = []
        for d in cands:
            kwmap = kw_lessons if d["type"] == "lesson" else kw_facts
            has_kw = d["id"] in kwmap
            has_sem = (d["type"], d["id"]) in sem
            if not has_kw and not has_sem:
                continue
            kw = kwmap.get(d["id"], 0.0)
            sv = sem.get((d["type"], d["id"]), 0.0)
            if not has_kw and sv < _SEM_FLOOR:  # weak semantic-only match -> drop
                continue
            base = (w * sv + (1.0 - w) * kw) if qunit is not None else kw
            conf = float(d.get("confidence") or 0.0)
            d["score"] = round(base * (0.5 + 0.5 * conf), 6)
            d.pop("_text", None)
            results.append(d)
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    # ── knowledge base (Phase 2) ──────────────────────────────────────────────
    def unit_vectors_for(self, embedding_ids: list[int]) -> dict[int, Any]:
        """Batch-load unit vectors for many embedding ids (chunked IN queries)."""
        import numpy as np  # lazy

        out: dict[int, Any] = {}
        ids = [int(i) for i in embedding_ids if i]
        for i in range(0, len(ids), 800):
            batch = ids[i:i + 800]
            rows = self.conn.execute(
                f"SELECT id, vector, norm FROM embeddings WHERE id IN ({','.join('?' * len(batch))})",
                batch,
            ).fetchall()
            for r in rows:
                v = np.frombuffer(r["vector"], dtype="float32")
                out[int(r["id"])] = v / (r["norm"] or 1.0)
        return out

    def put_kb_chunk(
        self,
        *,
        collection: str,
        source: str,
        content: str,
        title: Optional[str] = None,
        chunk_index: int = 0,
        vuln_class: Optional[str] = None,
        mitre: Optional[str] = None,
        nist: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> dict:
        """Insert a KB chunk (idempotent by content hash); embeds if semantic."""
        import hashlib

        h = hashlib.sha256((collection + "\x00" + content).encode("utf-8")).hexdigest()
        existing = self.query_one("SELECT id FROM kb_chunks WHERE content_hash=?", (h,))
        if existing:
            return {"id": int(existing["id"]), "action": "duplicate"}
        emb_id = self.put_embedding(((title or "") + " " + content)[:1000]) if self.semantic else None
        ts = now_iso()
        with self.lock:
            cur = self.conn.execute(
                "INSERT OR IGNORE INTO kb_chunks(collection, source, title, chunk_index, vuln_class, "
                "mitre, nist, tags, content, content_hash, embedding_id, created_at) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (collection, source, title, chunk_index, vuln_class, mitre, nist, tags, content, h, emb_id, ts),
            )
            self.conn.commit()
            if cur.lastrowid:
                return {"id": int(cur.lastrowid), "action": "inserted"}
        row = self.query_one("SELECT id FROM kb_chunks WHERE content_hash=?", (h,))
        return {"id": int(row["id"]) if row else 0, "action": "duplicate"}

    def kb_search(
        self,
        query: str,
        *,
        collection: Optional[str] = None,
        vuln_class: Optional[str] = None,
        top_k: int = 5,
        expand: int = 1,
    ) -> list[dict]:
        sql = ("SELECT id, collection, source, title, chunk_index, vuln_class, mitre, nist, tags, "
               "content, embedding_id FROM kb_chunks WHERE status='active'")
        params: list[Any] = []
        if collection:
            sql += " AND collection=?"
            params.append(collection)
        if vuln_class:
            sql += " AND vuln_class=?"
            params.append(vuln_class)
        cands = [dict(r) for r in self.query(sql, params)]
        if not cands:
            return []

        pool = max(top_k * 8, 60)
        kw = self._fts_scores("kb_chunks", "kb_fts", query, pool)
        qunit = self.embed_query_unit(query) if self.semantic else None
        sem: dict[int, float] = {}
        if qunit is not None:
            import numpy as np  # lazy

            vmap = self.unit_vectors_for([d["embedding_id"] for d in cands if d.get("embedding_id")])
            for d in cands:
                v = vmap.get(d.get("embedding_id"))
                if v is not None and v.shape == qunit.shape:
                    sem[d["id"]] = float(np.dot(qunit, v))

        w = self.cfg.hybrid_weight
        results: list[dict] = []
        for d in cands:
            has_kw, has_sem = d["id"] in kw, d["id"] in sem
            if not has_kw and not has_sem:
                continue
            sv = sem.get(d["id"], 0.0)
            if not has_kw and sv < _SEM_FLOOR:  # weak semantic-only match -> drop
                continue
            base = (w * sv + (1.0 - w) * kw.get(d["id"], 0.0)) if qunit is not None \
                else kw.get(d["id"], 0.0)
            d["score"] = round(base, 6)
            results.append(d)
        results.sort(key=lambda x: x["score"], reverse=True)
        top = results[:top_k]

        if expand and top:
            for d in top:
                neigh = self.query(
                    "SELECT content FROM kb_chunks WHERE source=? AND status='active' "
                    "AND chunk_index BETWEEN ? AND ? AND id!=? ORDER BY chunk_index",
                    (d["source"], d["chunk_index"] - expand, d["chunk_index"] + expand, d["id"]),
                )
                if neigh:
                    d["context"] = "\n".join(r["content"] for r in neigh)[:1500]
        return top
