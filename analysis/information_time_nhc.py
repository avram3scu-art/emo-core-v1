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


print(f"{'lead':>5} {'years':>10} {'n':>3} {'trend n mi/yr':>14} {'95% CI':>16} {'tau_I':>6} {'%/yr':>7} {'95% CI':>14}")
for lead in [12, 24, 36, 48, 72, 96, 120]:
    s = d[(d.lead_h == lead) & (d.n_forecasts >= 10)].set_index("year").error_nmi.sort_index()
    r = compute_information_time(-s)
    rl = compute_information_time(-np.log(s))
    print(f"{lead:>4}h {s.index[0]}-{s.index[-1]} {len(s):>3} {-r.slope:>14.2f} "
          f"[{-r.slope_ci_high:6.2f},{-r.slope_ci_low:6.2f}] {r.tau_i:>6.2f} "
          f"{pct(rl.slope):>6.2f}% [{pct(rl.slope_ci_low):5.2f},{pct(rl.slope_ci_high):5.2f}]")

s = d[(d.lead_h == 48) & (d.n_forecasts >= 10)].set_index("year").error_nmi.sort_index()
rng = np.random.default_rng(0)
z = [compute_information_time(pd.Series(-rng.permutation(s.values))).tau_i for _ in range(200)]
print(f"control, 48 h, years shuffled: tau_I > 0 in {100 * np.mean(np.array(z) > 0):.1f}% of 200 runs")
