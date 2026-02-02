from __future__ import annotations
from typing import List, Dict

SYSTEM_PROMPT = """You are a policy analysis assistant.
Rules:
1) Use ONLY the provided CONTEXT.
2) If CONTEXT is insufficient, set answer_type="not_specified" and do not invent facts.
3) If CONTEXT contains conflicting statements, set answer_type="conflicting" and cite both.
4) Do not use outside knowledge.
5) Output VALID JSON only. No extra text.
6) Evidence must cite chunk_id(s) and include short supporting quotes.
"""

def build_user_prompt(policy_name: str, query: str, chunks: List[Dict]) -> str:
    parts = []
    parts.append(f"Task: Analyze the policy using ONLY the provided context.")
    parts.append(f"Policy: {policy_name}")
    parts.append(f"Query: {query}")
    parts.append("")
    parts.append("CONTEXT (policy excerpts):")

    for i, c in enumerate(chunks, 1):
        parts.append(f"{i}) chunk_id: {c['chunk_id']}")
        parts.append(f"section_title: {c.get('section_title','')}")
        parts.append(f"text: {c['text']}")
        parts.append("")

    parts.append("Return JSON with this structure:")
    parts.append("""{
  "query": "...",
  "policy_name": "...",
  "answer_type": "supported | not_specified | conflicting",
  "short_answer": "...",
  "risk_labels": [{"label":"...", "severity":"low|medium|high", "confidence":0.0}],
  "evidence": [{"chunk_id":"...", "section_title":"...", "quote":"..."}],
  "reasoning_summary": "...",
  "retrieval_debug": {"k": 5, "used_chunks": ["..."], "note": "..."}
}""")
    return "\n".join(parts)
