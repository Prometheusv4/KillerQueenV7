"""Embedder resolution: local sentence-transformers -> API -> null (FTS-only).

The whole module is import-light: ``sentence_transformers`` / ``torch`` and ``numpy`` are
imported lazily so that resolving to the Null embedder (e.g. on a box without torch, or
Python 3.14 where torch has no wheels yet) costs nothing and never raises.

An Embedder is any object exposing:
    .available : bool          # False -> caller should use FTS keyword mode
    .name      : str
    .dim       : int
    .encode(texts: list[str]) -> ndarray of shape (len(texts), dim)
"""
from __future__ import annotations

import json
import os
import urllib.request
from typing import Any, List, Optional

from . import config as _config


class NullEmbedder:
    """No semantic model available — the store falls back to FTS5/jaccard keyword mode."""

    available = False
    name = "null"
    dim = 0
    reason = "no embedding backend"

    def __init__(self, reason: str = "no embedding backend") -> None:
        self.reason = reason

    def encode(self, texts: List[str]):  # pragma: no cover - guarded by .available
        raise RuntimeError("NullEmbedder cannot encode; check .available first")


class SentenceTransformerEmbedder:
    """Local CPU embeddings via sentence-transformers (default all-MiniLM-L6-v2)."""

    available = True

    def __init__(self, model_name: str, model_dir: Optional[str] = None) -> None:
        from sentence_transformers import SentenceTransformer  # lazy (drags torch)

        # Prefer a vendored local directory (offline Kali); else the model name.
        source = model_dir or model_name
        self._model = SentenceTransformer(source, device="cpu")
        self.name = f"st:{model_name}"
        self.dim = int(self._model.get_sentence_embedding_dimension())

    def encode(self, texts: List[str]):
        return self._model.encode(
            list(texts), normalize_embeddings=False, convert_to_numpy=True, show_progress_bar=False
        )


class ApiEmbedder:
    """OpenAI-compatible embeddings endpoint (only used when online + configured).

    Kept dependency-free (urllib). Note: DeepSeek has no embeddings API, so this is a
    fallback for other providers only; the default/offline path is local or null.
    """

    available = True
    dim = 0

    def __init__(self, base_url: str, model: str, api_key: Optional[str]) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.name = f"api:{model}"

    def encode(self, texts: List[str]):
        import numpy as np  # lazy

        body = json.dumps({"model": self.model, "input": list(texts)}).encode("utf-8")
        req = urllib.request.Request(f"{self.base_url}/embeddings", data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (operator-configured)
            payload = json.loads(resp.read().decode("utf-8"))
        vecs = [item["embedding"] for item in payload["data"]]
        arr = np.asarray(vecs, dtype="float32")
        self.dim = int(arr.shape[1]) if arr.ndim == 2 else 0
        return arr


def get_embedder(cfg: Optional[_config.Config] = None) -> Any:
    """Resolve the best available embedder; never raises (falls back to Null)."""
    cfg = cfg or _config.get_config()

    backend = os.environ.get("KQ_EMBED_BACKEND", "").lower()
    if backend in ("null", "fts", "none", "off"):
        return NullEmbedder("forced by KQ_EMBED_BACKEND")

    # 1) Local sentence-transformers (preferred; offline-capable when vendored).
    model_dir = None
    if cfg.embed_model_dir is not None:
        candidate = cfg.embed_model_dir
        if candidate.exists():
            model_dir = str(candidate)
        else:
            vendored = cfg.models_dir / cfg.embed_model_name
            if vendored.exists():
                model_dir = str(vendored)
    else:
        vendored = cfg.models_dir / cfg.embed_model_name
        if vendored.exists():
            model_dir = str(vendored)
    try:
        return SentenceTransformerEmbedder(cfg.embed_model_name, model_dir=model_dir)
    except Exception:  # ImportError (no torch), OSError (offline + not vendored), etc.
        pass

    # 2) API embeddings, only if explicitly configured.
    if cfg.embed_api:
        try:
            return ApiEmbedder(
                base_url=cfg.embed_api,
                model=os.environ.get("KQ_EMBED_API_MODEL", "text-embedding-3-small"),
                api_key=os.environ.get("KQ_EMBED_API_KEY"),
            )
        except Exception:
            pass

    # 3) Keyword-only.
    return NullEmbedder("sentence-transformers unavailable and no embedding API configured")
