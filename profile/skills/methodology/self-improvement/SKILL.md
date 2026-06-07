---
name: self-improvement
description: Killer Queen adaptive learning engine — now DETERMINISTIC. Executes the learning loop through the KQ Core tools (mcp_kq_*): lesson capture with dedup + confidence, durable memory, skill auto-generation, cross-session recall, and operator-feedback capture. Load at engagement boundaries, after a novel workflow or a tricky error, or on explicit retrospective triggers.
category: methodology
triggers:
  - after action review
  - lesson learned
  - capture workflow
  - save this approach
  - create skill from
  - self improve
  - compound knowledge
  - pattern recognition
  - capability gap
  - what did we learn
  - engagement retrospective
  - AAR
  - remember this
  - never do that again
---

# Self-Improvement — Deterministic Learning Loop (KQ Core)

**Execution rule:** learning is not narration. Every step below is a CONCRETE `mcp_kq_*`
tool call. If you find yourself *writing* "I learned X" without calling a tool, you have
not learned it. Call the tool. (KQ Core is the local `kq` MCP server; if a tool is
unavailable, the server is not registered — tell the operator, do not fake the loop.)

```
ENGAGEMENT → EXECUTION → REFLECTION → mcp_kq_lesson_save → (digest → next session) → COMPOUNDING
     ↑                                                                                    │
     └────────────────────────────────────────────────────────────────────────────────────┘
```

---

## WHEN THE LOOP RUNS
- **Session / engagement end** → run the full AAR below.
- **A recalled lesson re-validated or failed** → `mcp_kq_lesson_outcome(lesson_id, "success"|"failure")`.
- **Tricky error solved (3+ attempts)** → record it in `scratch` so trigger T2 fires (see Skill Triggers).
- **Operator says "remember this" / "never do X" / "always Y"** → IMMEDIATELY, in the same turn:
  `mcp_kq_audit_log(action="operator_directive", detail="<verbatim>")` (it also writes an operator correction).

---

## AFTER-ACTION REVIEW → TOOL CALLS

Produce the AAR for human reading, but for EACH item also issue the matching tool call.

```
AFTER-ACTION REVIEW — [TARGET] — [DATE]
  ENGAGEMENT: type / target / duration / findings-by-severity
  TECHNIQUE EFFECTIVENESS: what worked (top 3) / what failed (top 3)
  NOVEL DISCOVERIES: new technique / variant / combination / bypass
  CHAIN ANALYSIS: chains attempted / successful / most valuable (hop-by-hop)
  OPERATOR FEEDBACK: explicit directives, corrections, preferences
```

Mapping (do these, in order):
1. **Update phase** → `mcp_kq_engagement_state_update(engagement_id, {"phase": "report"})`.
2. **Each extracted lesson** → `mcp_kq_lesson_save(summary, category, trigger, action, rationale, source, target_fingerprint?, vuln_class?)`.
   - `category` ∈ recon | exploitation | evasion | methodology | tool | target-type.
   - Dedup is automatic: a near-duplicate returns `"merged"` and bumps confidence — that is expected, not a failure.
3. **Each durable fact** (validated bypass, tool flag combo, weapon location, chain template) → `mcp_kq_remember(content, kind=...)`.
   - DISCARD (do NOT save): transient scan output, one-off IPs/ports, "tried X, didn't work" (normal), nuclei false positives, speculative untested vectors.
4. **Each re-used lesson's outcome** → `mcp_kq_lesson_outcome(lesson_id, "success"|"failure")` so confidence tracks reality.
5. **Skill capture** → `mcp_kq_skill_propose(engagement_id)` (see below).

### Lesson quality bar (only save lessons that are ALL of):
Actionable · Generalizable (not target-specific) · Non-obvious · Validated by real tool output.
Format the fields as: `summary` = one line; `trigger` = when it applies; `action` = concrete step; `rationale` = why it works / why the alternative fails.

---

## SKILL AUTO-GENERATION (the 5 triggers, computed for you)

Call `mcp_kq_skill_propose(engagement_id, workflow_summary="<what you just did>")`. KQ Core
checks the triggers against real audit/state data and, if any fired, returns a SKILL.md
DRAFT in the gold-standard template:

- **T1** ≥5 distinct tools used this engagement
- **T2** an error solved after ≥3 attempts (record it: `engagement_state_update(eid, {"scratch":{"errors":{"<sig>":{"attempts":N,"resolution":"..."}}}})`)
- **T3** the workflow is novel (recall finds nothing close)
- **T4** a corroborated lesson cluster (≥2 independent restatements)
- **T5** an operator directive was recorded

If `should_create` is true:
1. Take `draft_skill.markdown` and create it: `skill_manage(action="create", name=draft_skill.name, content=draft_skill.markdown, category="methodology")`.
2. VERIFY it persisted: `skill_manage(action="list")` (or read the path) and confirm the new skill is present.
3. Do NOT hand-edit `kq_core.db` — `skill_propose` only drafts; Hermes `skill_manage` owns skill files.

---

## CROSS-SESSION PATTERN RECOGNITION
Replace grep-over-markdown with retrieval. At the start of an engagement and at phase
boundaries: `mcp_kq_recall(query="<target fingerprint / vuln class / question>", vuln_class?, target_fingerprint?, min_confidence=0.45)`.
HIGH-confidence hits should bias your technique order. Your top lessons are also injected
into MEMORY.md each session (the `KQ:DIGEST` block) — treat them as authoritative.

---

## OPERATOR FEEDBACK — HIGHEST PRIORITY
| Operator says | Do this immediately |
|---|---|
| "remember this" / "save this" | `mcp_kq_remember(content, kind="preference"|"technique")` |
| "never do X again" / "that's wrong" | `mcp_kq_audit_log(action="operator_directive", detail="never X")` (records a correction) |
| "always try X before Y" | `mcp_kq_lesson_save(summary="always X before Y", category="methodology", ...)` |
| "X works" / "X failed" | `mcp_kq_lesson_outcome(lesson_id, "success"|"failure")` |

---

## LEARNING LOOP CHECKLIST (end of engagement)
```
[ ] engagement phase set to "report"            -> mcp_kq_engagement_state_update
[ ] every lesson saved                          -> mcp_kq_lesson_save (dedup auto)
[ ] durable facts saved, cruft discarded        -> mcp_kq_remember
[ ] re-used lessons' outcomes recorded          -> mcp_kq_lesson_outcome
[ ] skill triggers checked, drafts created      -> mcp_kq_skill_propose -> skill_manage -> verify
[ ] operator feedback captured                  -> mcp_kq_audit_log / mcp_kq_remember
[ ] (operator, once) refresh the MEMORY.md digest for next session -> `kq digest`
```

The digest refresh (`kq digest`) is an operator/cron step because Hermes freezes MEMORY.md
at session start; run it on install, on engagement start, or via cron so the NEXT session
inherits your latest high-confidence lessons.
