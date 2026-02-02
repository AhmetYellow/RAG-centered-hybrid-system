from __future__ import annotations
from pathlib import Path

from ..decision.aggregate import run

def main():
    preds = Path("outputs/runs/20260201_155804/predictions.jsonl")
    out_dir = Path("outputs/runs/20260201_155804/decision_rules")
    run(preds, out_dir)

if __name__ == "__main__":
    main()
