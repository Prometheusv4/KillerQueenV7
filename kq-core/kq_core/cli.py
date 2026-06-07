"""``kq`` operator CLI: init | migrate | digest | status | doctor | export.

Offline-friendly and import-light (heavy deps load only when a command needs them).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from . import config as _config


def _store():
    from .store import Store  # lazy
    return Store()


def cmd_init(args) -> int:
    _config.ensure_dirs()
    s = _store()
    print(f"[kq] initialized store at {s.db_path}")
    print(f"[kq] FTS5: {'on' if s.has_fts else 'off (LIKE/jaccard fallback)'}")
    s.close()
    return 0


def cmd_migrate(args) -> int:
    from . import migrate as _migrate
    profile = Path(args.profile) if args.profile else (Path(__file__).resolve().parents[2] / "profile")
    if not profile.exists():
        print(f"[kq] profile dir not found: {profile}", file=sys.stderr)
        return 2
    s = _store()
    counts = _migrate.migrate_profile(s, profile)
    s.close()
    print(f"[kq] migrated from {profile}")
    for k, v in counts.items():
        print(f"      {k}: {v}")
    return 0


def cmd_digest(args) -> int:
    from . import memory as _memory
    s = _store()
    path = Path(args.path) if args.path else None
    res = _memory.write_digest(s, path)
    s.close()
    print(f"[kq] digest -> {res['path']} ({res['active_lessons']} lessons, {res['bytes']} bytes)")
    return 0


def cmd_status(args) -> int:
    s = _store()
    def c(sql):
        r = s.query_one(sql)
        return int(r["c"]) if r else 0
    print(f"[kq] store: {s.db_path}")
    print("      engagements :", c("SELECT COUNT(*) c FROM engagements"))
    print("      lessons     :", c("SELECT COUNT(*) c FROM lessons WHERE status='active'"), "active")
    print("      memory_facts:", c("SELECT COUNT(*) c FROM memory_facts WHERE status='active'"), "active")
    print("      findings    :", c("SELECT COUNT(*) c FROM findings"))
    print("      kb_chunks   :", c("SELECT COUNT(*) c FROM kb_chunks WHERE status='active'"), "active")
    by_coll = s.query("SELECT collection, COUNT(*) c FROM kb_chunks WHERE status='active' GROUP BY collection ORDER BY c DESC")
    for r in by_coll:
        print(f"        - {r['collection']}: {r['c']}")
    print("      audit rows  :", c("SELECT COUNT(*) c FROM audit_log"))
    s.close()
    return 0


def cmd_doctor(args) -> int:
    cfg = _config.get_config()
    s = _store()
    t0 = time.perf_counter()
    emb = s.embedder  # resolves the embedder (reports mode)
    resolve_ms = (time.perf_counter() - t0) * 1000
    t1 = time.perf_counter()
    s.recall("connectivity probe")
    rt_ms = (time.perf_counter() - t1) * 1000
    print("[kq] doctor")
    print(f"      KQ_HOME      : {cfg.kq_home}")
    print(f"      db_path      : {s.db_path} ({'exists' if s.db_path.exists() else 'MISSING'})")
    print(f"      FTS5         : {'on' if s.has_fts else 'off'}")
    print(f"      embedder     : {emb.name} (available={getattr(emb, 'available', False)})")
    if not getattr(emb, "available", False):
        print(f"                     reason: {getattr(emb, 'reason', 'n/a')} -> keyword-only mode")
    print(f"      model dir    : {cfg.models_dir} ({'present' if (cfg.models_dir / cfg.embed_model_name).exists() else 'not vendored'})")
    print(f"      MEMORY.md    : {cfg.memory_md} ({'exists' if cfg.memory_md.exists() else 'not yet written'})")
    print(f"      embedder resolve: {resolve_ms:.0f} ms | recall round-trip: {rt_ms:.1f} ms")
    s.close()
    return 0


def cmd_export(args) -> int:
    from .audit import verify_chain
    s = _store()
    cfg = s.cfg
    cfg.exports_dir.mkdir(parents=True, exist_ok=True)
    eid = args.engagement
    where = "WHERE engagement_id=?" if eid else ""
    params = (eid,) if eid else ()
    data = {
        "engagements": [dict(r) for r in s.query("SELECT * FROM engagements" + (" WHERE id=?" if eid else ""), params if eid else ())],
        "findings": [dict(r) for r in s.query(f"SELECT * FROM findings {where}", params)],
        "audit_log": [dict(r) for r in s.query(f"SELECT * FROM audit_log {where}", params)],
        "audit_chain": verify_chain(s),
    }
    name = f"engagement_{eid}.json" if eid else "export_all.json"
    out = cfg.exports_dir / name
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    s.close()
    print(f"[kq] exported -> {out} (audit chain ok={data['audit_chain']['ok']})")
    return 0


def cmd_ingest(args) -> int:
    from . import ingest as _ingest
    repo = Path(__file__).resolve().parents[2]
    auto = _ingest.default_paths(repo)
    anth = args.anthropic or auto["anthropic"]
    bh = args.bughunter or auto["bughunter"]
    sh = args.shannon or auto["shannon"]
    if not any([anth, bh, sh]):
        print("[kq] no corpora found. Pass --anthropic/--bughunter/--shannon <path>.", file=sys.stderr)
        print(f"      tried anthropic: {auto['anthropic']}", file=sys.stderr)
        return 2
    s = _store()
    res = _ingest.ingest_all(s, anthropic=anth, bughunter=bh, shannon=sh,
                             anthropic_limit=(args.limit or None))
    s.close()
    print("[kq] ingest complete:")
    for src, c in res.items():
        print(f"      {src}: {c}")
    return 0


def cmd_report(args) -> int:
    from . import report as _report
    s = _store()
    res = _report.generate(s, args.engagement, fmt=args.format, include_unvalidated=args.all)
    s.close()
    print(f"[kq] report -> {res['path']} ({res['reportable']} reportable, {res['excluded']} excluded)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kq", description="Killer Queen Core operator CLI")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="create the store + schema").set_defaults(func=cmd_init)
    mp = sub.add_parser("migrate", help="import profile memory + references")
    mp.add_argument("--profile", default=None, help="path to the profile/ directory")
    mp.set_defaults(func=cmd_migrate)
    dp = sub.add_parser("digest", help="write the MEMORY.md lessons digest")
    dp.add_argument("--path", default=None, help="override the MEMORY.md path")
    dp.set_defaults(func=cmd_digest)
    ip = sub.add_parser("ingest", help="ingest curated KB corpora (Anthropic skills / hunt patterns / scope)")
    ip.add_argument("--anthropic", default=None, help="path to Anthropic-Cybersecurity-Skills root")
    ip.add_argument("--bughunter", default=None, help="path to Claude-BugHunter-main")
    ip.add_argument("--shannon", default=None, help="path to shannon-main")
    ip.add_argument("--limit", type=int, default=0, help="cap Anthropic skills ingested (0 = all)")
    ip.set_defaults(func=cmd_ingest)
    sub.add_parser("status", help="counts summary").set_defaults(func=cmd_status)
    sub.add_parser("doctor", help="diagnostics (embedder mode, paths, latency)").set_defaults(func=cmd_doctor)
    ep = sub.add_parser("export", help="export findings + audit trail")
    ep.add_argument("--engagement", type=int, default=0, help="engagement id (0 = all)")
    ep.set_defaults(func=cmd_export)
    rp = sub.add_parser("report", help="generate an engagement report (html/md)")
    rp.add_argument("--engagement", type=int, required=True)
    rp.add_argument("--format", choices=["html", "md"], default="html")
    rp.add_argument("--all", action="store_true", help="include unvalidated findings")
    rp.set_defaults(func=cmd_report)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
