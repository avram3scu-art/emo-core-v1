"""DAC: the same measurement for ozone (calibration success) and climate (contrast).

Warning -> binding policy -> delivery. Delivery = world consumption/emissions relative to
the level at the first binding treaty. Ozone: CFC + halon consumption (OWID / UNEP), 1986
baseline. Climate: world fossil CO2 emissions (OWID / Global Carbon Project).
Run from the repository root: python analysis/dac_compare_ozone_climate.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import theilslopes

root = Path(__file__).resolve().parents[1]
z = pd.read_csv(root / "data/sources/owid_ozone_depleting_substance_consumption/owid_ozone_depleting_substance_consumption.csv")
zw = z[z.Entity == "World"].set_index("Year")
ozone = (zw["Chlorofluorocarbons (CFCs)"] + zw["Halons"]).sort_index()
c = pd.read_csv(root / "data/sources/owid_annual_co2_emissions/owid_annual_co2_emissions.csv")
co2 = c[c.Entity == "World"].set_index("Year")[c.columns[3]].sort_index() / 1e9  # Gt CO2



def _event_year(f: str, event_id: str) -> float:
    """Decimal year of an event, read from the DAC event file (single source of dates)."""
    e = pd.read_csv(root / "data" / f).set_index("id")
    d = pd.Timestamp(e.loc[event_id, "date"])
    return d.year + (d.dayofyear - 1) / (366 if d.is_leap_year else 365)


cases = {
    "Ozone": dict(series=ozone, warn=_event_year("dac_ozone_events.csv", "molina_rowland_1974"),
                  binding=_event_year("dac_ozone_events.csv", "montreal_protocol"), base_year=1986, unit="ODP t"),
    "Climate": dict(series=co2, warn=_event_year("dac_climate_events.csv", "charney_1979"),
                    binding=_event_year("dac_climate_events.csv", "kyoto_adopted"), base_year=1997, unit="Gt CO2"),
}
print(f"{'':10s}{'warning→binding':>17s}{'level vs baseline, years after binding treaty':>50s}")
print(f"{'':10s}{'(years)':>17s}{'+5':>10s}{'+10':>10s}{'+20':>10s}{'latest':>12s}")
for name, k in cases.items():
    s, b = k["series"], k["series"].loc[k["base_year"]]
    by = int(np.floor(k["binding"]))
    row = []
    for h in (5, 10, 20):
        y = by + h
        row.append(f"{100 * (s.loc[y] / b - 1):+.0f}%" if y in s.index else "n/a")
    last = s.index.max()
    print(f"{name:10s}{k['binding'] - k['warn']:>17.1f}{row[0]:>10s}{row[1]:>10s}{row[2]:>10s}"
          f"{100 * (s.loc[last] / b - 1):>+10.0f}% ({last})")

s = co2.loc[2016:2024]
sl, _, lo, hi = theilslopes(s.values, s.index)
print(f"\nClimate after Paris (2016-2024): {sl:+.2f} Gt CO2/yr [{lo:+.2f}, {hi:+.2f}]; "
      f"peak so far {co2.idxmax()} ({co2.max():.1f} Gt)")
peak_is_latest = co2.idxmax() == co2.index.max()
print("Climate: the highest emissions year is the latest year in the data; no peak yet observed."
      if peak_is_latest else f"Climate: emissions peaked in {co2.idxmax()} so far.")
print("Scope: Montreal bound all parties; Kyoto bound only listed developed countries, while delivery\n"
      "here is world CO2. The two rows are the same arithmetic, not equally binding commitments.")


def _level(k: dict, h: int) -> float:
    s = k["series"]
    return 100 * (s.loc[int(np.floor(k["binding"])) + h] / s.loc[k["base_year"]] - 1)

# Figure: level relative to the baseline, by years since the first binding treaty
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, MUTED, GRID, SURF = "#1f1f1d", "#6b6a66", "#e6e5e1", "#fcfcfb"
cols = {"Ozone": "#256abf", "Climate": "#c4462f"}
fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
ax.axhline(100, color=MUTED, lw=1, ls=(0, (3, 3)))
for name, k in cases.items():
    s, b = k["series"], k["series"].loc[k["base_year"]]
    by = int(np.floor(k["binding"]))
    t = s[s.index >= k["base_year"]]
    x, y = t.index - by, 100 * t.values / b
    ax.plot(x, y, color=cols[name], lw=2, solid_capstyle="round")
    ax.annotate(f"{name}  ({'Montreal 1987' if name == 'Ozone' else 'Kyoto 1997'})",
                (x[-1], y[-1]), xytext=(6, 0), textcoords="offset points", fontsize=9, color=INK, va="center")
ax.set_xlim(-2, 36); ax.set_ylim(-5, 175)
ax.set_xlabel("Years since the first binding treaty", color=INK, fontsize=9.5)
ax.set_ylabel("Level vs year of treaty (= 100)", color=INK, fontsize=9.5)
ax.grid(True, color=GRID, lw=0.8)
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
fig.suptitle("Warning to delivery: ozone vs climate", x=0.08, ha="left", fontsize=13, color=INK)
oz20, cl20 = _level(cases["Ozone"], 20), _level(cases["Climate"], 20)
ax.set_title(f"After 20 years: ozone consumption {oz20:+.0f}%, CO₂ {cl20:+.0f}% (Kyoto bound fewer parties).",
             loc="left", fontsize=9.5, color=MUTED, pad=8)
fig.text(0.08, 0.01, "Ozone: world CFC + halon consumption (OWID/UNEP), 1986 = 100. Climate: world fossil CO₂ (OWID/Global Carbon Project), 1997 = 100.",
         fontsize=6.8, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 0.9, 1))
fig.savefig(root / "analysis/dac_ozone_vs_climate.png", facecolor=SURF)
print("saved analysis/dac_ozone_vs_climate.png")
