"""Kali tool arsenal — catalog + scoped/audited runner + decision engine.

The runner can execute ANY installed tool by name; the catalog adds rich metadata
(command templates, target-type effectiveness, parameter optimization) for the most-used
tools so the decision engine can rank and the optimizer can tune. Every execution passes
the scope gate, the destructive-action guard, and the audit log.
"""
