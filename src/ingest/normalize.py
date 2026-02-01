from __future__ import annotations
import re

_WHITESPACE = re.compile(r"[ \t]+")
_MANY_NEWLINES = re.compile(r"\n{3,}")
_NONBREAKING = "\u00A0"

def normalize_text(text: str) -> str:
    # normalize newlines and spaces
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace(_NONBREAKING, " ")
    text = _WHITESPACE.sub(" ", text)
    # keep paragraph structure but remove excessive blank lines
    text = _MANY_NEWLINES.sub("\n\n", text)
    # strip lines
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()
