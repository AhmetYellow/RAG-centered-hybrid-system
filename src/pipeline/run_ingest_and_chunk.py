from __future__ import annotations
from pathlib import Path

from ..ingest.loaders import load_policy_folder
from ..chunking.chunker import SectionAwareChunker, chunks_to_jsonl
from ..utils.io import write_json, write_jsonl

def main():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    chunks_dir = Path("data/chunks")

    docs = load_policy_folder(raw_dir)
    print(f"Loaded {len(docs)} plaintext policies from {raw_dir}")

    chunker = SectionAwareChunker(target_tokens=600, overlap_tokens=100)

    for doc in docs:
        # save processed doc
        processed_path = processed_dir / f"{doc.doc_id}.json"
        write_json(processed_path, {
            "doc_id": doc.doc_id,
            "policy_name": doc.policy_name,
            "source_path": doc.source_path,
            "text": doc.text,
            "sections": doc.sections,
        })

        # chunk and save chunks
        chunks = chunker.chunk_document(doc)
        out_path = chunks_dir / f"{doc.doc_id}.jsonl"
        write_jsonl(out_path, chunks_to_jsonl(chunks))

        print(f"{doc.policy_name}: sections={len(doc.sections)} chunks={len(chunks)} -> {out_path}")

if __name__ == "__main__":
    main()
