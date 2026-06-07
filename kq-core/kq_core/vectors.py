"""Vector math for dedup / nearest-neighbour. numpy is imported lazily.

The corpus (lessons + facts) is small (dozens to low thousands of rows), so a numpy
brute-force scan is sub-millisecond and needs no ANN index. If the optional ``sqlite-vec``
extra is installed a future revision can swap in a vec0 virtual table transparently;
the public surface here stays the same.
"""
from __future__ import annotations

from typing import List, Sequence, Tuple


def to_unit(vec):
    import numpy as np

    v = np.asarray(vec, dtype="float32")
    n = float(np.linalg.norm(v)) or 1.0
    return v / n


def cosine(a, b) -> float:
    """Cosine similarity of two vectors (handles non-unit inputs)."""
    import numpy as np

    a = np.asarray(a, dtype="float32")
    b = np.asarray(b, dtype="float32")
    na = float(np.linalg.norm(a)) or 1.0
    nb = float(np.linalg.norm(b)) or 1.0
    return float(np.dot(a, b) / (na * nb))


def max_cosine(qunit, candidates: Sequence) -> Tuple[float, int]:
    """Best cosine of unit-query vs a list of unit vectors. Returns (score, index)."""
    import numpy as np

    best, best_i = -1.0, -1
    q = np.asarray(qunit, dtype="float32")
    for i, c in enumerate(candidates):
        if c is None:
            continue
        c = np.asarray(c, dtype="float32")
        if c.shape != q.shape:
            continue
        s = float(np.dot(q, c))
        if s > best:
            best, best_i = s, i
    return best, best_i


def topk(qunit, ids: List, vectors: List, k: int = 8) -> List[Tuple]:
    """Top-k (id, cosine) for unit-query vs aligned (ids, unit-vectors)."""
    scored: List[Tuple] = []
    for _id, v in zip(ids, vectors):
        if v is None:
            continue
        scored.append((_id, cosine(qunit, v)))
    scored.sort(key=lambda kv: kv[1], reverse=True)
    return scored[:k]
