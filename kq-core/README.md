# KQ Core

**Killer Queen Core** — the deterministic substrate behind the Killer Queen Hermes
profile. It turns the profile's *aspirational* "remember / adapt / learn / improve"
prose into real, executable behavior, exposed to the agent as a local **stdio MCP
server** (tools surface as `mcp_kq_*`). For **authorized security testing only**.

What it provides:

- **Persistent memory + learning** — a SQLite store with offline hybrid
  (vector + FTS5) retrieval, a closed learning loop (lesson dedup, a numeric
  confidence model, skill auto-generation), and a real engagement working-state board.
- **A MEMORY.md digest** — top high-confidence lessons written (atomically, inside a
  marker block) into Hermes's `~/.hermes/memories/MEMORY.md` so they are injected every
  session and survive context compression.
- **Responsible-use guardrails** — a hard `scope_check` Rules-of-Engagement gate, an
  append-only hash-chained `audit_log`, and a destructive-action confirmation pattern.

## Install

```bash
pip install .                 # core (FTS-only retrieval)
pip install '.[embeddings]'   # + local sentence-transformers semantic retrieval
hermes mcp add kq --command python --args -m kq_core.mcp_server \
    --env KQ_HOME="$HOME/.hermes/profiles/killer-queen"
kq init && kq migrate --profile ../profile && kq digest
```

If no embedding model is available the store runs in **FTS5 keyword-only** mode
(`kq doctor` reports the active mode). Nothing else changes.

## Layout

| Module | Responsibility |
|---|---|
| `store.py` | SQLite schema/migrations, CRUD, hybrid recall |
| `embeddings.py` / `vectors.py` | embedder (local → API → null/FTS) + cosine top-k |
| `learning.py` | dedup, confidence model, 5-trigger skill detection |
| `memory.py` / `findings.py` / `skillgen.py` | facts + digest / findings / SKILL.md drafts |
| `scope.py` / `audit.py` | RoE scope guard / append-only audit |
| `tools/` + `mcp_server.py` | the `mcp_kq_*` tool surface (stdio FastMCP) |
| `cli.py` / `migrate.py` | `kq init/migrate/digest/status/doctor/export` + importers |
