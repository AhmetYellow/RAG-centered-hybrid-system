from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    policy_name: str
    section_title: str
    text: str
    start_char: int
    end_char: int
