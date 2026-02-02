from __future__ import annotations
from pathlib import Path
from datetime import datetime

from ..utils.io import read_jsonl, write_jsonl
from ..vectorstore.faiss_store import FaissVectorStore
from ..embeddings.embedder import OpenAIEmbedder, EmbeddingConfig
from ..retrieval.retriever import Retriever, RetrievalConfig
from ..prompting.templates import SYSTEM_PROMPT, build_user_prompt
from ..llm.client import OpenAILLM, LLMConfig
from ..llm.parse import extract_json
from ..prompting.json_schema import minimal_validate
from ..tasks.taskset import TASKS

def main():
    store = FaissVectorStore.load(Path("indices/faiss/policies_v1"))
    embedder = OpenAIEmbedder(EmbeddingConfig(model="text-embedding-3-small"))
    retriever = Retriever(store, RetrievalConfig(k=5, similarity_threshold=0.30, context_cap_tokens=3000))
    llm = OpenAILLM(LLMConfig(model="gpt-4o-mini", temperature=0.0))

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("outputs/runs") / run_id
    out_path = out_dir / "predictions.jsonl"

    rows = []

    # Iterate over chunk files just to collect doc/policy names quickly
    for chunk_file in sorted(Path("data/chunks").glob("*.jsonl")):
        chunks = read_jsonl(chunk_file)
        if not chunks:
            continue
        policy_name = chunks[0]["policy_name"]
        doc_id = chunks[0]["doc_id"]

        for task in TASKS:
            query = task["question"]
            qvec = embedder.embed_texts([query])[0]
            r = retriever.retrieve(qvec)

            if r.abstain:
                obj = {
                    "query": query,
                    "policy_name": policy_name,
                    "answer_type": "not_specified",
                    "short_answer": "Not specified in the provided policy excerpts.",
                    "risk_labels": [],
                    "evidence": [],
                    "reasoning_summary": f"Retriever abstained: {r.abstain_reason}",
                    "retrieval_debug": {"k": retriever.cfg.k, "used_chunks": [], "note": r.abstain_reason},
                }
                rows.append({**task, "doc_id": doc_id, **obj})
                continue

            user_prompt = build_user_prompt(policy_name, query, r.used_chunks)
            raw = llm.generate(SYSTEM_PROMPT, user_prompt)

            obj = extract_json(raw)
            obj["retrieval_debug"] = {
                "k": retriever.cfg.k,
                "used_chunks": [c["chunk_id"] for c in r.used_chunks],
                "note": "ok"
            }

            minimal_validate(obj)

            rows.append({
                "doc_id": doc_id,
                **task,
                **obj
            })

        print(f"Done: {policy_name}")

    write_jsonl(out_path, rows)
    print(f"Wrote {len(rows)} records to {out_path}")

if __name__ == "__main__":
    main()
