"""Shared fixtures. Every fixture isolates KQ_HOME *and* HERMES_HOME under tmp_path so a
test can never touch the real ~/.hermes. The semantic path is exercised with a
deterministic in-process FakeEmbedder (TF over md5-hashed bins) — no torch, no downloads.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import pytest

# Make the kq_core package importable without an install step.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PROFILE_DIR = Path(__file__).resolve().parents[2] / "profile"


class FakeEmbedder:
    """Deterministic term-frequency embedder for tests (no torch)."""

    available = True
    name = "fake-tf"
    dim = 256

    def encode(self, texts):
        import numpy as np

        out = np.zeros((len(texts), self.dim), dtype="float32")
        for i, t in enumerate(texts):
            for tok in re.findall(r"[a-z0-9]+", (t or "").lower()):
                b = int(hashlib.md5(tok.encode()).hexdigest(), 16) % self.dim
                out[i, b] += 1.0
        return out


def _isolate(monkeypatch, tmp_path, backend="null"):
    monkeypatch.setenv("KQ_HOME", str(tmp_path / "kq"))
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
    monkeypatch.setenv("KQ_EMBED_BACKEND", backend)


@pytest.fixture
def store(tmp_path, monkeypatch):
    """FTS5 keyword-only store (null embedder)."""
    _isolate(monkeypatch, tmp_path, "null")
    from kq_core.store import Store

    s = Store()
    yield s
    s.close()


@pytest.fixture
def sem_store(tmp_path, monkeypatch):
    """Store with the deterministic FakeEmbedder (semantic path)."""
    _isolate(monkeypatch, tmp_path, "")  # don't force null; we inject the embedder
    from kq_core.store import Store

    s = Store(embedder=FakeEmbedder())
    yield s
    s.close()
