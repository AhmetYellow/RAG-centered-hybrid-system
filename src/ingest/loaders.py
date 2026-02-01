from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List
import hashlib

from .normalize import normalize_text
from .section_parser import parse_sections
from ..utils.io import read_text

@dataclass(frozen=True)
class Document:
    doc_id: str
    policy_name: str
    source_path: str
    text: str
    sections: List[dict]  # [{"title": str, "text": str}]

def _stable_doc_id(text: str, policy_name: str) -> str:
    h = hashlib.sha256()
    h.update(policy_name.encode("utf-8"))
    h.update(b"\n")
    h.update(text.encode("utf-8"))
    return h.hexdigest()[:16]

def load_plaintext_policy(path: Path) -> Document:
    policy_name = path.stem
    raw = read_text(path)
    norm = normalize_text(raw)
    sections = parse_sections(norm)
    doc_id = _stable_doc_id(norm, policy_name)
    return Document(
        doc_id=doc_id,
        policy_name=policy_name,
        source_path=str(path),
        text=norm,
        sections=sections,
    )

def load_policy_folder(folder: Path) -> List[Document]:
    docs: List[Document] = []
    for p in sorted(folder.glob("*.txt")):
        docs.append(load_plaintext_policy(p))
    return docs
