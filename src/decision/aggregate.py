from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import json
from typing import Dict, Any, List

from ..utils.io import read_jsonl, write_json, write_jsonl
from .rules import apply_rules, RiskFinding

def build_doc_report(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    policy_name = rows[0]["policy_name"]
    doc_id = rows[0]["doc_id"]

    task_map: Dict[str, Dict[str, Any]] = {r["task_id"]: r for r in rows}
    findings, overall = apply_rules(task_map)

    # Attach evidence snippets from the tasks that triggered findings
    evidence_bank = []
    for f in findings:
        for tid in f.supporting_tasks:
            r = task_map.get(tid)
            if not r:
                continue
            for ev in r.get("evidence", []):
                evidence_bank.append({
                    "task_id": tid,
                    "label": f.label,
                    "chunk_id": ev.get("chunk_id"),
                    "section_title": ev.get("section_title"),
                    "quote": ev.get("quote"),
                })

    return {
        "doc_id": doc_id,
        "policy_name": policy_name,
        "overall_severity": overall,
        "findings": [asdict(x) for x in findings],
        "evidence": evidence_bank,
        "task_outputs": {tid: {
            "answer_type": task_map[tid].get("answer_type"),
            "short_answer": task_map[tid].get("short_answer"),
            "evidence": task_map[tid].get("evidence", []),
        } for tid in task_map}
    }

def write_markdown(report: Dict[str, Any], out_path: Path) -> None:
    lines = []
    lines.append(f"# {report['policy_name']} — Risk Report")
    lines.append("")
    lines.append(f"**Overall severity:** {report['overall_severity']}")
    lines.append("")

    lines.append("## Findings")
    if not report["findings"]:
        lines.append("- No major risks detected by current rules baseline.")
    else:
        for f in report["findings"]:
            lines.append(f"- **{f['label']}** — {f['severity']}: {f['rationale']} (tasks: {', '.join(f['supporting_tasks'])})")
    lines.append("")

    lines.append("## Evidence (snippets)")
    if not report["evidence"]:
        lines.append("- (none)")
    else:
        for ev in report["evidence"][:30]:
            lines.append(f"- **{ev['label']}** / {ev['task_id']} — `{ev['chunk_id']}` ({ev['section_title']}): {ev['quote']}")
    lines.append("")

    lines.append("## Task outputs (summary)")
    for tid, t in report["task_outputs"].items():
        lines.append(f"- **{tid}**: `{t['answer_type']}` — {t['short_answer']}")
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")

def run(predictions_path: Path, out_dir: Path) -> None:
    rows = read_jsonl(predictions_path)
    by_policy: Dict[str, List[Dict[str, Any]]] = {}
    for r in rows:
        by_policy.setdefault(r["policy_name"], []).append(r)

    out_dir.mkdir(parents=True, exist_ok=True)

    reports = []
    for policy_name, group in by_policy.items():
        group = sorted(group, key=lambda x: x["task_id"])
        rep = build_doc_report(group)
        reports.append(rep)

        write_json(out_dir / f"{policy_name}.json", rep)
        write_markdown(rep, out_dir / f"{policy_name}.md")
        print(f"Wrote report for {policy_name}")

    # Summary file
    summary = [{
        "policy_name": r["policy_name"],
        "doc_id": r["doc_id"],
        "overall_severity": r["overall_severity"],
        "findings": [f["label"] for f in r["findings"]],
    } for r in reports]

    write_json(out_dir / "summary.json", {"reports": summary})
    write_jsonl(out_dir / "summary.jsonl", summary)
    print(f"Wrote summary to {out_dir}")

