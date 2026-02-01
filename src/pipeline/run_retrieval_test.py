from __future__ import annotations
from pathlib import Path

from ..embeddings.embedder import OpenAIEmbedder, EmbeddingConfig
from ..vectorstore.faiss_store import FaissVectorStore
from ..retrieval.retriever import Retriever, RetrievalConfig

def main():
    store = FaissVectorStore.load(Path("indices/faiss/policies_v1"))
    embedder = OpenAIEmbedder(EmbeddingConfig(model="text-embedding-3-small"))
    retriever = Retriever(store, RetrievalConfig(k=5, similarity_threshold=0.30, context_cap_tokens=3000))

    query = "Does this policy share personal data with third parties?"
    qvec = embedder.embed_texts([query])[0]

    result = retriever.retrieve(qvec)

    print("ABSTAIN:", result.abstain, result.abstain_reason)
    print("TOP HITS:")
    for h in result.hits[:5]:
        print(f"  score={h.score:.3f} chunk_id={h.chunk_id} section={h.metadata.get('section_title')}")
    print("\nUSED CHUNKS:")
    for c in result.used_chunks:
        print(f"\n--- {c['chunk_id']} | {c['section_title']} ---\n{c['text'][:400]}...")

if __name__ == "__main__":
    main()
