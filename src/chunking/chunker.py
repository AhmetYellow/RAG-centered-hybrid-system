from __future__ import annotations
from dataclasses import asdict
from typing import List, Iterable
import hashlib

import tiktoken

from .schemas import Chunk
from ..ingest.loaders import Document

def _chunk_id(doc_id: str, section_title: str, i: int) -> str:
    h = hashlib.sha256(f"{doc_id}|{section_title}|{i}".encode("utf-8")).hexdigest()
    return h[:16]

class SectionAwareChunker:
    def __init__(
        self,
        model_encoding: str = "cl100k_base",
        target_tokens: int = 600,
        overlap_tokens: int = 100,
    ):
        assert target_tokens > overlap_tokens, "target_tokens must be > overlap_tokens"
        self.enc = tiktoken.get_encoding(model_encoding)
        self.target_tokens = target_tokens
        self.overlap_tokens = overlap_tokens

    def _count_tokens(self, text: str) -> int:
        return len(self.enc.encode(text))

    def chunk_document(self, doc: Document) -> List[Chunk]:
        chunks: List[Chunk] = []
        global_char_cursor = 0  # best-effort offset in full doc text

        # Build a char index for sections in the normalized full text
        # (simple approach: search; acceptable for v1)
        full_text = doc.text

        for sec in doc.sections:
            title = sec["title"]
            sec_text = sec["text"].strip()
            if not sec_text:
                continue

            # locate section text inside doc.text (best effort)
            start = full_text.find(sec_text)
            if start == -1:
                start = global_char_cursor
            end = start + len(sec_text)
            global_char_cursor = max(global_char_cursor, end)

            # token-based chunking within section
            tokens = self.enc.encode(sec_text)
            n = len(tokens)
            i = 0
            chunk_index = 0

            while i < n:
                j = min(i + self.target_tokens, n)
                chunk_tokens = tokens[i:j]
                chunk_text = self.enc.decode(chunk_tokens).strip()

                # approximate char offsets within section (best-effort)
                # we compute by finding chunk_text within sec_text starting from prev offset
                local_start = sec_text.find(chunk_text, max(0, (i - self.overlap_tokens)))
                if local_start == -1:
                    local_start = 0
                local_end = local_start + len(chunk_text)

                chunk = Chunk(
                    chunk_id=_chunk_id(doc.doc_id, title, chunk_index),
                    doc_id=doc.doc_id,
                    policy_name=doc.policy_name,
                    section_title=title,
                    text=chunk_text,
                    start_char=start + local_start,
                    end_char=start + local_end,
                )
                chunks.append(chunk)
                chunk_index += 1

                if j == n:
                    break
                i = j - self.overlap_tokens  # overlap

        return chunks

def chunks_to_jsonl(chunks: Iterable[Chunk]) -> List[dict]:
    return [asdict(c) for c in chunks]
