from __future__ import annotations
import re
from typing import List, Dict

# Heuristic heading patterns:
# - Markdown headings: "#", "##"
# - Numbered headings: "1.", "1.2", "2)"
# - ALL CAPS short lines
MD_HEADING = re.compile(r"^(#{1,6})\s+(.+)$")
NUM_HEADING = re.compile(r"^(\d+(\.\d+)*[.)])\s+(.+)$")
ALLCAPS = re.compile(r"^[A-Z][A-Z\s0-9&,:/\-()]{5,80}$")

def parse_sections(text: str) -> List[Dict[str, str]]:
    lines = text.splitlines()

    sections: List[Dict[str, str]] = []
    current_title = "Preamble"
    current_buf: List[str] = []

    def flush():
        nonlocal current_buf, current_title
        chunk = "\n".join(current_buf).strip()
        if chunk:
            sections.append({"title": current_title.strip(), "text": chunk})
        current_buf = []

    for line in lines:
        raw = line.strip()
        if not raw:
            current_buf.append("")
            continue

        m = MD_HEADING.match(raw)
        if m:
            flush()
            current_title = m.group(2)
            continue

        m = NUM_HEADING.match(raw)
        if m:
            flush()
            current_title = m.group(3)
            continue

        if ALLCAPS.match(raw) and len(raw.split()) <= 10:
            flush()
            current_title = raw.title()
            continue

        current_buf.append(raw)

    flush()
    return sections
