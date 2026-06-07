# KILLER QUEEN v6 — Evil. No limits. KQ_MODE=unleashed — Architecture Design

## Core Insight

Killer Queen does not need to BE a new agent framework. Killer Queen is a Hermes PROFILE so powerful it transforms the underlying agent into an offensive operator regardless of which model powers it. The persona, skills, memory, and configuration together form a "model-agnostic offensive reasoning layer" — the same prompt engineering that makes a generalist model behave like an attacker.

## Fusion Architecture

### Layer 1: SOUL.md (Model-Agnostic Offensive Reasoning)
The persona is engineered to work with ANY model (DeepSeek, Claude, GPT, Gemini). It uses:
- Constitutional directives that survive context compression
- Behavioral primitives (DO NOT STOP, MULTI-VECTOR, CHAIN-FIRST) expressed as invariant rules
- Thinking patterns that restructure how the model approaches problems
- Model-family-specific guidance blocks (auto-detected at runtime via model name matching)

### Layer 2: Skills (Capability Injection)
Pre-loaded skills provide specialized knowledge. They're loaded at session start via `hermes --profile killer-queen -s bughunter-methodology -s mission-orchestrator`. Skills auto-trigger based on topic matching in their frontmatter.

### Layer 3: Memory (Persistent Intel)
50KB memory stores engagement history, target dossiers, technique library, and lessons learned. Memory injection happens at API-call time (preserves prompt cache).

### Layer 4: Configuration (Hardware)
YOLO approvals, 120 max turns, 128K context, 2-depth delegation, all offensive toolsets enabled.

### Layer 5: Working State (Engagement Board) — KQ Core
The Layer-5 working state is now a REAL SQLite-backed board provided by the **KQ Core**
companion (a local `kq` stdio MCP server), not a hand-maintained JSON file. The
`engagement_state` row (phase, active vectors, running workers, deployed payloads, chain
candidates, target fingerprint) plus lessons, memory facts, findings, scope rules, and an
append-only audit log live in `~/.hermes/profiles/killer-queen/kq_core.db`. The agent
reads and writes it through `mcp_kq_*` tools. This supersedes the never-implemented
`engagement_state.json`. Killer Queen remains a Hermes profile + this deterministic local
substrate — no edits to Hermes core.

## What We Adopt from OpenClaw (conceptually, via Hermes primitives)

| OpenClaw Feature | Killer Queen Implementation |
|-----------------|--------------------------|
| Multi-agent routing | delegate_task with orchestrator role |
| Subagent spawning | delegate_task with context inheritance via context field |
| Browser automation | Hermes browser tool (browser_navigate, browser_click, browser_snapshot, etc.) |
| Docker sandbox | terminal tool → docker commands |
| Cron system | Hermes cronjob tool |
| Plugin marketplace | Hermes skill system + git-based skill distribution |
| Vector memory | KQ Core store: SQLite + offline hybrid (MiniLM vector + FTS5 keyword) retrieval via `mcp_kq_recall`; degrades to FTS-only when no model is vendored |
| Workspace bootstrap | AGENTS.md + engagement_state.json |
| Human delay | Not needed for CLI operator (terminal, not messaging) |
| Node host | SSH-based terminal backend |

## Model-Agnostic Prompt Engineering

Killer Queen uses a layered prompt architecture:

```
[CONSTITUTIONAL DIRECTIVES]     ← Loaded first, survive compression
[OPERATIONAL METHODOLOGY]       ← 6-phase workflow, validation gates
[TECHNIQUE CATALOG]             ← Chain tables, bypass patterns, payload classes
[MODEL-SPECIFIC GUIDANCE]       ← Injected based on detected model family
[ENGAGEMENT CONTEXT]            ← Target dossier, active vectors, running workers
[TOOL AWARENESS]                ← Available tools, Kali inventory
```

The constitutional directives are designed to be model-agnostic:
- Short, imperative, unambiguous
- No model-specific formatting (no XML tags, no markdown tricks)
- Survive context compression by being at the TOP of the prompt
- Each directive is self-contained (no cross-references that break on truncation)
