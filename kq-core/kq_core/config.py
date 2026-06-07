"""Central configuration + path resolution for KQ Core.

Stdlib-only and import-light. ``get_config()`` reads the environment fresh on every
call (no caching) so tests can set ``KQ_HOME`` / threshold env-vars per-case and core
classes can also be handed an explicit :class:`Config` to avoid env juggling entirely.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Optional


def _kq_home() -> Path:
    env = os.environ.get("KQ_HOME")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".hermes" / "profiles" / "killer-queen"


def _hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".hermes"


def _f(env: str, default: float) -> float:
    v = os.environ.get(env)
    if v is None or v == "":
        return default
    try:
        return float(v)
    except ValueError:
        return default


def _i(env: str, default: int) -> int:
    v = os.environ.get(env)
    if v is None or v == "":
        return default
    try:
        return int(v)
    except ValueError:
        return default


@dataclass(frozen=True)
class Config:
    """Resolved paths + tunable thresholds. Immutable; use :func:`dataclasses.replace`."""

    kq_home: Path
    db_path: Path
    vectors_dir: Path
    models_dir: Path
    audit_dir: Path
    exports_dir: Path
    memory_md: Path  # Hermes-injected memory file — the digest target

    # retrieval
    hybrid_weight: float  # score = w*cosine + (1-w)*bm25

    # dedup
    dedup_semantic: float  # cosine >= -> merge lesson
    dedup_fts: float       # jaccard >= -> merge lesson (no-embedder mode)
    dedup_fact: float      # memory_facts dedup

    # confidence model
    conf_init: float
    conf_success: float       # c += (1-c)*conf_success
    conf_failure: float       # c *= conf_failure
    conf_corroborate: float   # c += (1-c)*conf_corroborate on dedup restate
    stale_halflife_days: float
    archive_conf: float
    archive_revisions: int

    # digest + triggers
    digest_top_n: int
    digest_budget_chars: int
    novelty_threshold: float  # recall top-score below this => "novel" (skill trigger T3)

    # embeddings
    embed_model_name: str
    embed_model_dir: Optional[Path]
    embed_api: Optional[str]


def get_config() -> Config:
    """Build a :class:`Config` from the environment (fresh each call)."""
    home = _kq_home()
    model_dir_env = os.environ.get("KQ_MODEL_DIR")
    return Config(
        kq_home=home,
        db_path=home / "kq_core.db",
        vectors_dir=home / "vectors",
        models_dir=Path(model_dir_env).expanduser() if model_dir_env else home / "models",
        audit_dir=home / "audit",
        exports_dir=home / "exports",
        memory_md=_hermes_home() / "memories" / "MEMORY.md",
        hybrid_weight=_f("KQ_HYBRID_WEIGHT", 0.70),
        dedup_semantic=_f("KQ_DEDUP_THRESHOLD", 0.86),
        dedup_fts=_f("KQ_DEDUP_FTS_THRESHOLD", 0.60),
        dedup_fact=_f("KQ_DEDUP_FACT_THRESHOLD", 0.90),
        conf_init=_f("KQ_CONF_INIT", 0.50),
        conf_success=_f("KQ_CONF_SUCCESS", 0.25),
        conf_failure=_f("KQ_CONF_FAILURE", 0.55),
        conf_corroborate=_f("KQ_CONF_CORROBORATE", 0.10),
        stale_halflife_days=_f("KQ_STALE_HALFLIFE_DAYS", 180.0),
        archive_conf=_f("KQ_ARCHIVE_CONF", 0.20),
        archive_revisions=_i("KQ_ARCHIVE_REVISIONS", 2),
        digest_top_n=_i("KQ_DIGEST_TOP_N", 25),
        digest_budget_chars=_i("KQ_DIGEST_BUDGET", 80_000),
        novelty_threshold=_f("KQ_NOVELTY_THRESHOLD", 0.55),
        embed_model_name=os.environ.get("KQ_EMBED_MODEL", "all-MiniLM-L6-v2"),
        embed_model_dir=Path(model_dir_env).expanduser() if model_dir_env else None,
        embed_api=os.environ.get("KQ_EMBED_API") or None,
    )


def for_db(db_path: Path) -> Config:
    """A config rooted at an explicit DB path (used by tests and ad-hoc tooling)."""
    home = Path(db_path).expanduser().resolve().parent
    cfg = get_config()
    return replace(
        cfg,
        kq_home=home,
        db_path=Path(db_path).expanduser(),
        vectors_dir=home / "vectors",
        audit_dir=home / "audit",
        exports_dir=home / "exports",
    )


def ensure_dirs(cfg: Optional[Config] = None) -> Config:
    cfg = cfg or get_config()
    for d in (cfg.kq_home, cfg.vectors_dir, cfg.models_dir, cfg.audit_dir, cfg.exports_dir):
        d.mkdir(parents=True, exist_ok=True)
    return cfg
