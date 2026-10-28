"""Write the profile and the order-file view of each coded PPE case (docs/DAC_PPE_CODING.md).

For data/dac_ppe/<case>.json: validates it, writes <case>_profile.json (emo/dac_standard.py,
all readings) and, if it has paired orders, <case>_orders.csv: one row per firm order and reading
with its paired delivery (the manuscript's "order file", derived from the validated event file).
Run from the repository root: python scripts/dac_ppe_outputs.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from emo.dac_standard import compute_profile, load_event_file

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data/dac_ppe"


def main() -> None:
    for f in sorted(D.glob("[A-Z][A-Z].json")):
        data = load_event_file(f)
        prof = compute_profile(data)
        (D / f"{f.stem}_profile.json").write_text(json.dumps(prof, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        ev = data["events"]
        dels = {e["pairs_with"]: e for e in ev if e.get("pairs_with")}
        rows = []
        for o in (e for e in ev if e["sublayer"] == "firm_order" and e["event_id"] in dels):
            d = dels[o["event_id"]]
            rows.append({"order_id": o["event_id"], "reading": o.get("reading", ""), "good": o.get("good", ""),
                         "order_date": o.get("date_earliest", o["date_status"]),
                         "delivery_id": d["event_id"], "delivery_date": d.get("date_earliest", d["date_status"]),
                         "delivery_end_point": d.get("end_point", ""), "order_source": o["source"], "delivery_source": d["source"]})
        if rows:
            with (D / f"{f.stem}_orders.csv").open("w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
        print(f"{f.stem}: valid; profile written; {len(rows)} order-file rows")


if __name__ == "__main__":
    main()
