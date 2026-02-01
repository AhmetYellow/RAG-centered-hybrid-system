from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
import json
import numpy as np
import faiss

@dataclass
class Hit:
    chunk_id: str
    score: float          # cosine similarity if normalized
    metadata: Dict[str, Any]

class FaissVectorStore:
    """
    Simple FAISS index that uses cosine similarity via inner product on normalized vectors.
    """
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # inner product
        self.metadatas: List[Dict[str, Any]] = []
        self.ids: List[str] = []

    @staticmethod
    def _normalize(v: np.ndarray) -> np.ndarray:
        faiss.normalize_L2(v)
        return v

    def add(self, vectors: np.ndarray, chunk_ids: List[str], metadatas: List[Dict[str, Any]]):
        assert vectors.shape[0] == len(chunk_ids) == len(metadatas)
        assert vectors.shape[1] == self.dim

        vectors = vectors.astype(np.float32)
        vectors = self._normalize(vectors)

        self.index.add(vectors)
        self.ids.extend(chunk_ids)
        self.metadatas.extend(metadatas)

    def search(self, query_vec: np.ndarray, top_k: int) -> List[Hit]:
        q = query_vec.astype(np.float32).reshape(1, -1)
        q = self._normalize(q)

        scores, idxs = self.index.search(q, top_k)  # (1, k)
        hits: List[Hit] = []

        for score, ix in zip(scores[0], idxs[0]):
            if ix == -1:
                continue
            hits.append(Hit(
                chunk_id=self.ids[ix],
                score=float(score),
                metadata=self.metadatas[ix],
            ))
        return hits

    def save(self, folder: Path):
        folder.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(folder / "index.faiss"))
        (folder / "meta.json").write_text(json.dumps({
            "dim": self.dim,
            "ids": self.ids,
            "metadatas": self.metadatas,
        }, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, folder: Path) -> "FaissVectorStore":
        meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        index = faiss.read_index(str(folder / "index.faiss"))
        store = cls(dim=int(meta["dim"]))
        store.index = index
        store.ids = list(meta["ids"])
        store.metadatas = list(meta["metadatas"])
        return store
