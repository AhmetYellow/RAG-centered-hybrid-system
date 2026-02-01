from __future__ import annotations
from pathlib import Path
import json
from typing import List, Dict, Any

from ..utils.io import read_jsonl
from ..embeddings.embedder import OpenAIEmbedder, EmbeddingConfig
from ..vectorstore.faiss_store import FaissVectorStore

def main():
    chunks_dir = Path("data/chunks")
    index_dir = Path("indices/faiss/policies_v1")

    # Load all chunks from data/chunks/*.jsonl
    chunk_files = sorted(chunks_dir.glob("*.jsonl"))
    all_chunks: List[Dict[str, Any]] = []
    for f in chunk_files:
        all_chunks.extend(read_jsonl(f))

    print(f"Loaded {len(all_chunks)} chunks from {len(chunk_files)} files")

    texts = [c["text"] for c in all_chunks]
    chunk_ids = [c["chunk_id"] for c in all_chunks]

    # metadata stored alongside vectors (keep what you need for evidence)
    metadatas = [{
        "doc_id": c["doc_id"],
        "policy_name": c["policy_name"],
        "section_title": c["section_title"],
        "text": c["text"],
    } for c in all_chunks]

    embedder = OpenAIEmbedder(EmbeddingConfig(model="text-embedding-3-small", batch_size=64))
    vecs = embedder.embed_texts(texts)
    print(f"Embedded shape: {vecs.shape}")

    store = FaissVectorStore(dim=vecs.shape[1])
    store.add(vecs, chunk_ids, metadatas)
    store.save(index_dir)

    print(f"Saved FAISS index to {index_dir}")

if __name__ == "__main__":
    main()
