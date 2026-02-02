from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

SUPPORTED = "supported"
POSITIVE = {"supported", "conflicting"}

@dataclass
class RiskFinding:
    label: str
    severity: str          # low|medium|high
    rationale: str
    supporting_tasks: List[str]

def _is_positive(task_out: Dict[str, Any]) -> bool:
    return task_out.get("answer_type") in POSITIVE

def _evidence_text(task_out: Dict[str, Any]) -> str:
    ev = task_out.get("evidence", []) or []
    quotes = " ".join((e.get("quote", "") or "") for e in ev)
    return quotes.lower()

import re

def _is_supported(task_out: Dict[str, Any]) -> bool:
    return task_out.get("answer_type") == "supported"


def _explicit_sale(task_out: Dict[str, Any]) -> bool:
    txt = _evidence_text(task_out)

    # Common negations: "do not sell", "does not sell", "not sell"
    if re.search(r"\b(do|does)\s+not\s+sell\b", txt):
        return False
    if re.search(r"\bnot\s+sell\b", txt):
        return False

    # "sale" appears as a legal right (opt-out of sale) — not proof of actual selling
    if "opt out" in txt and "sale" in txt:
        return False
    if "right to opt" in txt and "sale" in txt:
        return False

    # Require stronger sale indicators
    # (this is conservative: fewer false positives)
    sale_positive = (
        re.search(r"\bwe\s+sell\b", txt) or
        re.search(r"\bmay\s+sell\b", txt) or
        re.search(r"\bsell\s+your\b", txt) or
        re.search(r"\bsold\s+to\b", txt) or
        re.search(r"\bpersonal\s+information\s+is\s+sold\b", txt)
    )

    return bool(sale_positive)


def apply_rules(task_outputs: Dict[str, Dict[str, Any]]) -> Tuple[List[RiskFinding], str]:
    findings: List[RiskFinding] = []

    # Helper flags (treat supported OR conflicting as positive)
    shares_third_party = _is_positive(task_outputs.get("THIRD_PARTY_SHARING", {}))
    shares_advertisers = _is_positive(task_outputs.get("SHARES_WITH_ADVERTISERS", {}))
    targeted_ads = _is_positive(task_outputs.get("TARGETED_ADS", {}))
    profiling = _is_positive(task_outputs.get("ANALYTICS_PROFILING", {}))
    ai_training = _is_positive(task_outputs.get("AI_TRAINING", {}))
    location = _is_positive(task_outputs.get("COLLECTS_LOCATION", {}))

    retention = _is_positive(task_outputs.get("RETENTION_PERIOD", {}))
    security = _is_positive(task_outputs.get("SECURITY_MEASURES", {}))
    delete_right = _is_positive(task_outputs.get("DELETE_RIGHT", {}))
    opt_out = _is_positive(task_outputs.get("OPT_OUT_SHARING", {}))



    # --- Data sale (guarded by explicit evidence text) ---
    data_sale_out = task_outputs.get("DATA_SALE", {})
    if _is_positive(data_sale_out) and _explicit_sale(data_sale_out):
        findings.append(RiskFinding(
            label="data sale",
            severity="high",
            rationale="Policy evidence explicitly indicates personal data is sold.",
            supporting_tasks=["DATA_SALE"]
        ))

    # --- Advertising / ad sharing ---
    shares_advertisers_supported = _is_supported(task_outputs.get("SHARES_WITH_ADVERTISERS", {}))

    if shares_advertisers or targeted_ads:
        supporting = []
        if shares_advertisers: supporting.append("SHARES_WITH_ADVERTISERS")
        if targeted_ads: supporting.append("TARGETED_ADS")

        findings.append(RiskFinding(
            label="advertising / ad sharing",
            severity="high" if shares_advertisers_supported else "medium",
            rationale="Policy indicates personal data is used and/or shared for advertising (possibly with conditions).",
            supporting_tasks=supporting
        ))


    # --- Third-party sharing ---
    if shares_third_party:
        findings.append(RiskFinding(
            label="third-party sharing",
            severity="medium",
            rationale="Policy indicates personal data is shared with third parties (e.g., service providers), possibly under conditions.",
            supporting_tasks=["THIRD_PARTY_SHARING"]
        ))

    # --- Profiling / personalization ---
    if profiling:
        findings.append(RiskFinding(
            label="profiling / personalization",
            severity="medium",
            rationale="Policy indicates analytics/profiling/personalization using personal data.",
            supporting_tasks=["ANALYTICS_PROFILING"]
        ))

    # --- AI training ---
    if ai_training:
        findings.append(RiskFinding(
            label="ai training / model improvement",
            severity="medium",
            rationale="Policy indicates data may be used to train or improve AI/ML models.",
            supporting_tasks=["AI_TRAINING"]
        ))

    # --- Location collection ---
    if location:
        findings.append(RiskFinding(
            label="location collection",
            severity="medium",
            rationale="Policy indicates location data may be collected.",
            supporting_tasks=["COLLECTS_LOCATION"]
        ))

    # --- Protections (kept for later use if you want downshifting) ---
    protections = 0
    if delete_right: protections += 1
    if opt_out: protections += 1
    if retention: protections += 1
    if security: protections += 1
    # (Not used right now in overall severity; you can add downshift later.)

    # Determine overall severity
    if any(f.severity == "high" for f in findings):
        overall = "high"
    elif any(f.severity == "medium" for f in findings):
        overall = "medium"
    else:
        overall = "low"

    return findings, overall
