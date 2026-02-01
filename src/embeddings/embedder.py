from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import os


from openai import OpenAI

@dataclass
class EmbeddingConfig:
    model: str = "text-embedding-3-small"  # cheaper; switch to -3-large for best quality
    batch_size: int = 64

class OpenAIEmbedder:
    def __init__(self, cfg: EmbeddingConfig, api_key: Optional[str] = None):
        self.cfg = cfg
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Returns: np.ndarray shape (n, d) float32
        """
        vectors: List[List[float]] = []

        bs = self.cfg.batch_size
        for i in range(0, len(texts), bs):
            batch = texts[i:i+bs]
            # OpenAI embeddings endpoint
            resp = self.client.embeddings.create(
                model=self.cfg.model,
                input=batch,
            )
            # resp.data is in the same order as input
            for item in resp.data:
                vectors.append(item.embedding)

        arr = np.array(vectors, dtype=np.float32)
        return arr
