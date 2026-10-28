"""Convert the ozone and climate DAC event CSVs to the DAC standard (docs/DAC_STANDARD.md §5).

Mapping rules were pre-registered in docs/DAC_STANDARD.md §5 (commit a4de996) before this ran.
Usage: python scripts/convert_dac_csv.py
"""

from __future__ import annotations

import calendar
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECONDARY_HOSTS = ("wikipedia.org", "undsci.berkeley.edu")
CASES = {
    "ozone": dict(t0="molina_rowland_1974", binding="montreal_protocol",
                  institution="Molina & Rowland (Nature), first published diagnosis"),
    "climate": dict(t0="charney_1979", binding="kyoto_adopted",
                    institution="US National Academy of Sciences (Charney report)"),
}


def _dates(date: str, precision: str) -> dict:
    y, m, _ = (int(x) for x in date.split("-"))
    if precision.startswith("day"):
        return {"date_status": "exact", "date_earliest": date, "date_latest": date}
    if precision.startswith("month"):
        last = calendar.monthrange(y, m)[1]
        lo, hi = f"{y:04d}-{m:02d}-01", f"{y:04d}-{m:02d}-{last:02d}"
    else:  # year_verified / year_unverified
        lo, hi = f"{y:04d}-01-01", f"{y:04d}-12-31"
    return {"date_status": "window", "date_earliest": lo, "date_latest": hi,
            "source_wording": f"date given as {date}, precision '{precision}' in the original file"}


def convert(name: str) -> dict:
    spec = CASES[name]
    rows = list(csv.DictReader((ROOT / f"data/dac_{name}_events.csv").open(encoding="utf-8")))
    events, alt_t0 = [], []
    for r in rows:
        if r["id"] == spec["t0"]:
            sub = "validation"
        elif r["id"] == spec["binding"]:
            sub = "binding_act"
        else:
            sub = "context"
            if r["stage"] == "diagnostic":
                alt_t0.append(r["id"])
        src = r["source"].strip()
        ev = {
            "event_id": r["id"],
            "sublayer": sub,
            **_dates(r["date"], r["date_precision"]),
            "description": r["description"],
            "source": src or "no source given",
            "source_type": "secondary" if (not src or any(h in src for h in SECONDARY_HOSTS)) else "primary",
        }
        events.append(ev)
    t0_year = next(r["date"][:4] for r in rows if r["id"] == spec["t0"])
    return {
        "standard_version": "1.1",
        "case": {
            "case_id": name,
            "t0_event_id": spec["t0"],
            "t0_institution": spec["institution"],
            "t0_rule": "First diagnostic event in the original event file",
            "alternative_t0": alt_t0,
            "response_scale": "International treaty system (all parties); national acts not coded",
            "start_rule": "First treaty adoption with binding cuts; frameworks without binding cuts excluded",
            "end_point": "not coded (no dated delivery events in the original file)",
            "inclusion_rules": {"binding_act": "Adoption of the first treaty with binding cuts"},
            "observation_window": {"start": f"{t0_year}-01-01", "end": "2026-10-26",
                                   "reason": "From the t0 year to the conversion date"},
            "source_pool": {"searched": ["sources listed per event in the original CSV"],
                            "search_date": "2026-10-26", "not_accessed": [],
                            "case_selection_reason": "Existing EMO comparison case (analysis/dac_compare_ozone_climate.py)"},
            "coding": {"coders": 1, "agreement": None, "rules_fixed_before_coding": False},
            "computation": {"code": "scripts/convert_dac_csv.py; emo/dac_standard.py"},
            "identification": "Not applicable: no orders or deliveries are coded, so no explanation of delay can be tested.",
        },
        "events": events,
    }


if __name__ == "__main__":
    from emo.dac_standard import compute_profile

    for name in CASES:
        data = convert(name)
        out = ROOT / f"data/dac_{name}_events.json"
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        prof = compute_profile(data)
        lag = prof["profiles"][0]["sublayers"]["binding_act"]["lag_from_t0"]
        print(f"{name}: wrote {out.relative_to(ROOT)}; binding_act lag from t0 {lag} days")
