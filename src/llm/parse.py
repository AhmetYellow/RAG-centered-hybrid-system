from __future__ import annotations
import json

def extract_json(text: str):
    text = text.strip()

    # Remove fenced blocks
    if text.startswith("```"):
        text = text.strip("`")
        if "\n" in text:
            text = text.split("\n", 1)[1].strip()

    # Find JSON object boundaries
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output")

    return json.loads(text[start:end+1])
