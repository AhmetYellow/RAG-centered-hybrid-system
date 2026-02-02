from __future__ import annotations
from pathlib import Path
import json
import csv
from collections import defaultdict

def main():
    preds = Path("outputs/runs/20260201_155804/predictions.jsonl")
    out_csv = preds.parent / "results_table.csv"
    out_stats = preds.parent / "results_stats.json"

    rows = [json.loads(l) for l in preds.read_text(encoding="utf-8").splitlines() if l.strip()]

    by_policy = defaultdict(list)
    for r in rows:
        by_policy[r["policy_name"]].append(r)

    def yn(task_id: str, task_map) -> str:
        v = task_map.get(task_id, {}).get("answer_type", "not_specified")
        return "yes" if v in ("supported", "conflicting") else "no"

    table = []
    for policy, rs in by_policy.items():
        task_map = {r["task_id"]: r for r in rs}

        protections = sum([
            1 if yn("DELETE_RIGHT", task_map) == "yes" else 0,
            1 if yn("OPT_OUT_SHARING", task_map) == "yes" else 0,
            1 if yn("RETENTION_PERIOD", task_map) == "yes" else 0,
            1 if yn("SECURITY_MEASURES", task_map) == "yes" else 0,
        ])

        counts = defaultdict(int)
        for r in rs:
            counts[r["answer_type"]] += 1

        table.append({
            "policy_name": policy,
            "doc_id": rs[0]["doc_id"],
            "third_party_sharing": yn("THIRD_PARTY_SHARING", task_map),
            "ad_sharing": yn("SHARES_WITH_ADVERTISERS", task_map),
            "targeted_ads": yn("TARGETED_ADS", task_map),
            "profiling": yn("ANALYTICS_PROFILING", task_map),
            "ai_training": yn("AI_TRAINING", task_map),
            "location_collection": yn("COLLECTS_LOCATION", task_map),
            "protections_count": protections,
            "supported_count": counts["supported"],
            "conflicting_count": counts["conflicting"],
            "not_specified_count": counts["not_specified"],
        })

    # Write CSV
    fieldnames = list(table[0].keys()) if table else []
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in table:
            w.writerow(r)

    # Write small stats JSON
    out_stats.write_text(json.dumps({
        "num_policies": len(table),
        "num_records": len(rows),
        "csv_path": str(out_csv),
    }, indent=2), encoding="utf-8")

    print(f"Wrote {len(table)} policy rows to {out_csv}")
    print(f"Wrote stats to {out_stats}")

if __name__ == "__main__":
    main()
