"""F8.8: summary of the six frozen PPE profiles, written before the manuscript's tables are opened.

For each case and reading: first firm order, first binding act, first delivery (event ids, dates, lag from
t0 in days), counter-measure, missing sublayers; for cases with paired orders, every paired lag and the
identification profile per good. Writes data/dac_ppe/frozen_summary.md. Run from the repository root.
"""

import json
from pathlib import Path

D = Path("data/dac_ppe")
SUBS = ("firm_order", "binding_act", "delivery", "counter_measure")


def dates(events, ids, reading):
    out = []
    for e in events:
        if e["event_id"] in ids and (not e.get("reading") or reading.get(e["event_id"]) in (None, e.get("reading"))):
            a, b = e.get("date_earliest"), e.get("date_latest")
            out.append(a if a == b else f"{a}..{b}")
    return ", ".join(sorted(set(x for x in out if x)))


def main() -> None:
    lines = ["# Frozen PPE profiles (F8.8, written before the manuscript's tables were opened)", ""]
    for case in ("BE", "FR", "DE", "NL", "SE", "EU"):
        data = json.loads((D / f"{case}.json").read_text(encoding="utf-8"))
        prof = json.loads((D / f"{case}_profile.json").read_text(encoding="utf-8"))
        ev = data["events"]
        lines += [f"## {case}", "", f"End point: {prof['end_point']}. Missing: {', '.join(prof['missing']) or 'none'}.", "",
                  "| Reading | Sublayer | Event(s) | Date(s) | Lag from t0 (days) |", "|---|---|---|---|---|"]
        for p in prof["profiles"]:
            r = p["reading"]
            rl = ", ".join(f"{k}={v}" for k, v in r.items()) or "-"
            for s in SUBS:
                x = p["sublayers"].get(s)
                if x:
                    lag = x["lag_from_t0"]
                    lines.append(f"| {rl} | {s} | {', '.join(x['first_event_ids'])} | {dates(ev, x['first_event_ids'], r)} | "
                                 f"{lag['min_days']}–{lag['max_days']} |")
            for k, v in p.get("secondary_end_points", {}).items():
                lines.append(f"| {rl} | delivery (secondary: {k}) | {v} | | |")
            if p["paired_order_to_delivery"]:
                lines += ["", f"Paired order-to-delivery lags ({rl}):", ""]
                for q in p["paired_order_to_delivery"]:
                    lines.append(f"- {json.dumps(q, ensure_ascii=False)}")
            if p.get("identification"):
                lines += ["", f"Identification ({rl}): {json.dumps(p['identification'], ensure_ascii=False)}", ""]
        lines.append("")
    (D / "frozen_summary.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
