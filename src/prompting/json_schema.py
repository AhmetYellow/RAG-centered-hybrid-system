from __future__ import annotations
from typing import Dict, Any

REQUIRED_TOP_FIELDS = [
    "query", "policy_name", "answer_type", "short_answer",
    "risk_labels", "evidence", "reasoning_summary", "retrieval_debug"
]

def minimal_validate(obj: Dict[str, Any]) -> Dict[str, Any]:
    for k in REQUIRED_TOP_FIELDS:
        if k not in obj:
            raise ValueError(f"Missing required field: {k}")

    if obj["answer_type"] not in ["supported", "not_specified", "conflicting"]:
        raise ValueError("answer_type must be supported|not_specified|conflicting")

    if not isinstance(obj["evidence"], list):
        raise ValueError("evidence must be a list")

    if not isinstance(obj["risk_labels"], list):
        raise ValueError("risk_labels must be a list")

    return obj
