"""Information-time (tau_I) on NHC Atlantic official track errors, 1970-2025.

Skill = -error (or -log error for relative improvement). Years with fewer than
10 verified forecasts are excluded. Control: years shuffled, where tau_I > 0
should occur only about as often as the false-positive rate.
Run from the repository root:  python analysis/information_time_nhc.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from emo.info_time import compute_information_time  # noqa: E402

d = pd.read_csv(Path(__file__).resolve().parents[1] / "data/nhc_atlantic_official_track_errors_1970_2025.csv")


def pct(x):
    return 100 * (1 - np.exp(-x))


rows = []
print(f"{'lead':>5} {'years':>10} {'n':>3} {'trend n mi/yr':>14} {'95% CI':>16} {'tau_I':>6} {'%/yr':>7} {'95% CI':>14}")
for lead in [12, 24, 36, 48, 72, 96, 120]:
    s = d[(d.lead_h == lead) & (d.n_forecasts >= 10)].set_index("year").error_nmi.sort_index()
    r = compute_information_time(-s)
    rl = compute_information_time(-np.log(s))
    print(f"{lead:>4}h {s.index[0]}-{s.index[-1]} {len(s):>3} {-r.slope:>14.2f} "
          f"[{-r.slope_ci_high:6.2f},{-r.slope_ci_low:6.2f}] {r.tau_i:>6.2f} "
          f"{pct(rl.slope):>6.2f}% [{pct(rl.slope_ci_low):5.2f},{pct(rl.slope_ci_high):5.2f}]")
    rows.append((lead, s, pct(rl.slope), pct(rl.slope_ci_low), pct(rl.slope_ci_high)))

s = d[(d.lead_h == 48) & (d.n_forecasts >= 10)].set_index("year").error_nmi.sort_index()
rng = np.random.default_rng(0)
z = [compute_information_time(pd.Series(-rng.permutation(s.values))).tau_i for _ in range(200)]
print(f"control, 48 h, years shuffled: tau_I > 0 in {100 * np.mean(np.array(z) > 0):.1f}% of 200 runs")

# Figure: the data (left) and the per-lead rate of improvement with its 95% CI (right).
# Same numbers as the table above; nothing new is estimated. Not printed, so the text output is unchanged.
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

INK, MUTED, GRID = "#1f1f1d", "#6b6a66", "#e6e5e1"
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.6), dpi=200, gridspec_kw={"width_ratios": [1.6, 1]})
shades = plt.cm.Blues(np.linspace(0.35, 0.95, len(rows)))
for (lead, ser, *_), c in zip(rows, shades):
    a1.plot(ser.index, ser.values, color=c, lw=1.4)
    a1.text(ser.index[-1] + 0.6, ser.values[-1], f"{lead} h", fontsize=7.5, color=INK, va="center")
a1.set_yscale("log")
a1.set_yticks([20, 30, 50, 100, 200, 300, 500], ["20", "30", "50", "100", "200", "300", "500"])
a1.minorticks_off()
a1.set_ylabel("Mean official track error (n mi, log scale)", fontsize=9, color=INK)
a1.set_xlim(1969, 2031)
a1.set_title("NHC Atlantic official track errors, 1970–2025", loc="left", fontsize=10, color=INK)
leads = [r[0] for r in rows]
mid = np.array([r[2] for r in rows])
lo = np.array([min(r[3], r[4]) for r in rows])
hi = np.array([max(r[3], r[4]) for r in rows])
ypos = np.arange(len(rows))
a2.errorbar(mid, ypos, xerr=[mid - lo, hi - mid], fmt="o", color="#1f5f8b", ecolor=MUTED, capsize=3, ms=5)
a2.set_yticks(ypos, [f"{lead} h" for lead in leads])
a2.invert_yaxis()
a2.set_xlabel("Error falls by % per year (95% CI)", fontsize=9, color=INK)
a2.set_title("Information-time τ$_I$ as relative improvement", loc="left", fontsize=10, color=INK)
for ax in (a1, a2):
    ax.grid(color=GRID, lw=0.6)
    ax.tick_params(colors=MUTED, labelsize=8, length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
fig.text(0.01, 0.01, "Data: NHC verification (data/nhc_atlantic_official_track_errors_1970_2025.csv). "
         "Years with < 10 forecasts excluded. Script: analysis/information_time_nhc.py", fontsize=6.5, color=MUTED)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(Path(__file__).resolve().parent / "information_time_nhc.png")
