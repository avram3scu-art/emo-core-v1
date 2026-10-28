"""DAC calibration case: ozone (known success). Warning -> policy -> delivery.

Since 28 Oct 2026 (fix session F7) the event dates come from the DAC-standard file
data/dac_ozone_events.json and the lags from emo/dac_standard.py, as ranges over every date
consistent with each source's precision (the old version printed one value per lag and used
emo/metrics/dac, now deleted). Each diagnostic event listed in the file (t0 and alternative t0)
is tried as t0.

Delivery series: world consumption of CFCs + halons (ODP tonnes, OWID / UNEP Ozone Secretariat),
the only gases reported consistently from 1986 (carbon tetrachloride and methyl chloroform
reporting jumps between 1986 and 1989, a coverage artifact). Year precision.
Run from the repository root: python analysis/dac_ozone.py
"""
import copy
import json
import sys
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from emo.dac_standard import compute_profile  # noqa: E402

case = json.loads((root / "data/dac_ozone_events.json").read_text(encoding="utf-8"))
z = pd.read_csv(root / "data/sources/owid_ozone_depleting_substance_consumption/owid_ozone_depleting_substance_consumption.csv")
w = z[z.Entity == "World"].set_index("Year")
deliv = (w["Chlorofluorocarbons (CFCs)"] + w["Halons"]).sort_index()
base = deliv.loc[1986]


def first_year_below(frac):
    s = deliv[deliv.index >= 1987]
    hit = s[s <= base * frac]
    return int(hit.index[0]) if len(hit) else None


def with_t0(data, eid):
    """Copy of the case with event `eid` as t0 (sublayer validation) and the old t0 as context."""
    d = copy.deepcopy(data)
    old = d["case"]["t0_event_id"]
    for ev in d["events"]:
        if ev["event_id"] == eid:
            ev["sublayer"] = "validation"
        elif ev["event_id"] == old:
            ev["sublayer"] = "context"
    d["case"]["t0_event_id"] = eid
    return d


events = {e["event_id"]: e for e in case["events"]}
binding = next(e for e in case["events"] if e["sublayer"] == "binding_act")
print(f"Warning -> binding policy ({binding['event_id']}, {binding['date_earliest']}), days (min-max over consistent dates):")
for eid in [case["case"]["t0_event_id"], *case["case"]["alternative_t0"]]:
    lag = compute_profile(with_t0(case, eid))["profiles"][0]["sublayers"]["binding_act"]["lag_from_t0"]
    e = events[eid]
    print(f"  {eid:22s} {lag['min_days']:5d}-{lag['max_days']:5d} d  ({lag['min_days'] / 365.25:.1f}-{lag['max_days'] / 365.25:.1f} y; "
          f"t0 known {e['date_earliest']}..{e['date_latest']})")

t0 = events[case["case"]["t0_event_id"]]
t0_year = int(t0["date_earliest"][:4])
pol_year = int(binding["date_earliest"][:4])
print(f"\nDelivery: world CFC + halon consumption, 1986 baseline {base:,.0f} ODP t (year precision)")
for frac, lab in [(0.5, "50%"), (0.1, "90%"), (0.01, "99%")]:
    y = first_year_below(frac)
    print(f"  {lab} reduction reached in {y}: {y - pol_year} yr after policy year, {y - t0_year} yr after first-warning year")
print(f"\nConversion: 1 binding treaty for {1 + len(case['case']['alternative_t0'])} validated warnings; universal ratification (198 parties).")
