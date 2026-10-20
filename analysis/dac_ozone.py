"""DAC calibration case: ozone (known success). Warning -> policy -> delivery.

Delivery series: world consumption of CFCs + halons (ODP tonnes, OWID / UNEP Ozone Secretariat),
the only gases reported consistently from 1986 (carbon tetrachloride and methyl chloroform
reporting jumps between 1986 and 1989, a coverage artifact).
Dates with day precision unverified are marked in data/dac_ozone_events.csv.
Run from the repository root: python analysis/dac_ozone.py
"""
import sys
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from emo.metrics.dac.lag import warning_to_delivery_lag_days, warning_to_policy_lag_days  # noqa: E402
from emo.models.delivery_trace import DeliveryTrace  # noqa: E402
from emo.models.diagnostic_event import DiagnosticEvent  # noqa: E402
from emo.models.policy_instrument import PolicyInstrument  # noqa: E402

ev = pd.read_csv(root / "data/dac_ozone_events.csv").set_index("id")
z = pd.read_csv(root / "data/owid_ozone_depleting_substance_consumption.csv")
w = z[z.Entity == "World"].set_index("Year")
deliv = (w["Chlorofluorocarbons (CFCs)"] + w["Halons"]).sort_index()
base = deliv.loc[1986]

def first_year_below(frac):
    s = deliv[deliv.index >= 1987]
    hit = s[s <= base * frac]
    return int(hit.index[0]) if len(hit) else None

diag = {k: DiagnosticEvent(id=k, domain="ozone", hazard_type="stratospheric ozone depletion",
                           source=ev.loc[k, "description"], issued_at=ev.loc[k, "date"])
        for k in ["molina_rowland_1974", "farman_1985"]}
mp = PolicyInstrument(id="montreal_protocol", instrument_type="treaty", jurisdiction="global",
                      announced_at=ev.loc["montreal_protocol", "date"], effective_at=ev.loc["montreal_in_force", "date"])
print("Warning -> binding policy (Montreal Protocol, 1987-09-16):")
for k, d in diag.items():
    print(f"  {k:22s} {warning_to_policy_lag_days(d, mp) / 365.25:5.1f} years  ({ev.loc[k, 'date_precision']})")

print(f"\nDelivery: world CFC + halon consumption, 1986 baseline {base:,.0f} ODP t")
for frac, lab in [(0.5, "50%"), (0.1, "90%"), (0.01, "99%")]:
    y = first_year_below(frac)
    tr = DeliveryTrace(id=f"cut_{lab}", delivery_type="consumption reduction", jurisdiction="global",
                       started_at=f"{y}-01-01")
    print(f"  {lab} reduction reached in {y}: {(y - 1987)} yr after policy, "
          f"{warning_to_delivery_lag_days(diag['molina_rowland_1974'], tr) / 365.25:.0f} yr after first warning")
print("\nConversion: 1 binding treaty for 2 validated warnings; universal ratification (198 parties).")
