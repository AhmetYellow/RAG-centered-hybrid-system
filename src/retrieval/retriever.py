from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import tiktoken

from ..vectorstore.faiss_store import FaissVectorStore, Hit

@dataclass
class RetrievalConfig:
    k: int = 5
    similarity_threshold: float = 0.30   # tune later
    context_cap_tokens: int = 3000
    encoding: str = "cl100k_base"

@dataclass
class RetrievalResult:
    hits: List[Hit]
    used_chunks: List[Dict[str, Any]]  # includes chunk_id, section_title, text
    abstain: bool
    abstain_reason: Optional[str]

class Retriever:
    def __init__(self, store: FaissVectorStore, cfg: RetrievalConfig):
        self.store = store
        self.cfg = cfg
        self.enc = tiktoken.get_encoding(cfg.encoding)

    def _tokens(self, text: str) -> int:
        return len(self.enc.encode(text))

    def retrieve(self, query_vec, top_k: Optional[int] = None) -> RetrievalResult:
        k = top_k or self.cfg.k
        hits = self.store.search(query_vec, top_k=k)

        if not hits:
            return RetrievalResult(hits=[], used_chunks=[], abstain=True, abstain_reason="no_hits")

        best = hits[0].score
        if best < self.cfg.similarity_threshold:
            return RetrievalResult(
                hits=hits,
                used_chunks=[],
                abstain=True,
                abstain_reason=f"low_similarity(best={best:.3f})"
            )

        used = []
        total = 0
        for h in hits:
            chunk_text = h.metadata["text"]
            t = self._tokens(chunk_text)
            if total + t > self.cfg.context_cap_tokens:
                break
            used.append({
                "chunk_id": h.chunk_id,
                "section_title": h.metadata.get("section_title", ""),
                "text": chunk_text
            })
            total += t

        return RetrievalResult(hits=hits, used_chunks=used, abstain=False, abstain_reason=None)
