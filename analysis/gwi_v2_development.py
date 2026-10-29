"""GWI v2 development on SEEN data (exploratory; no weight in any verdict).

docs/GWI_V2_PROTOCOL.md §4: chooses alpha_day on pageviews already opened in sessions 6
and the calibration session (Photosynthesis, Prime number, Pythagorean theorem; scored days
2018-01-01 .. 2026-10-18). Rule fixed before this run: alpha_day = the largest value in
ALPHAS whose false-ignition rate is <= q = 0.005 on every development placebo article.
Also reports, without weight, the session-6 hurricane contrast with the v2 rule.
Run from the repository root: python analysis/gwi_v2_development.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from emo.gwi_v2 import compute_gwi_v2, window_hits  # noqa: E402

PV6 = ROOT / "data/sources/wikipedia_pageviews_gwi/wikipedia_pageviews_gwi.csv"
PVC = ROOT / "data/sources/wikipedia_pageviews_gwi_calibration/wikipedia_pageviews_gwi_calibration.csv"
ALPHAS = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5]
Q = 0.005
SCORE = (pd.Timestamp("2018-01-01"), pd.Timestamp("2026-10-18"))
EVENTS = ["2016-10-04", "2016-11-24", "2017-08-26", "2017-09-06", "2017-09-19", "2018-10-10",
          "2019-09-01", "2020-08-27", "2020-10-28", "2020-11-03", "2020-11-17", "2021-08-21",
          "2021-08-29", "2022-09-20", "2022-09-27", "2023-08-30", "2024-07-01", "2024-09-27",
          "2024-10-10", "2024-11-06", "2025-10-28"]  # docs/GWI_PROTOCOL.md §2.1


def wide(long: pd.DataFrame, end: pd.Timestamp) -> pd.DataFrame:
    w = long.pivot_table(index="date", columns="lang", values="views", aggfunc="sum")
    w.index = pd.to_datetime(w.index)
    w = w.reindex(pd.date_range("2015-11-01", end, freq="D")).fillna(0.0)
    keep = [c for c in w.columns if (w[c] == 0).mean() <= 0.05]
    return w[keep]


def main() -> int:
    pv6, pvc = pd.read_csv(PV6), pd.read_csv(PVC)
    photo = pd.concat([pv6[pv6.set == "placebo"], pvc[pvc.set == "reference_2026"]])
    photo = photo.drop_duplicates(["lang", "date"], keep="last")
    arts = {"Photosynthesis": wide(photo, SCORE[1]),
            "Prime number": wide(pvc[pvc.set == "heldout_prime"], SCORE[1]),
            "Pythagorean theorem": wide(pvc[pvc.set == "heldout_pythagorean"], SCORE[1])}
    print("EXPLORATORY, seen data. q =", Q, "; scored days", SCORE[0].date(), "..", SCORE[1].date())
    res = {a: compute_gwi_v2(v, alpha_day=1.0) for a, v in arts.items()}
    chosen = None
    for al in ALPHAS:
        row = []
        for a, r in res.items():
            sc = r.scored.loc[SCORE[0]:SCORE[1]]
            ig = ((r.tail_p < al) & r.scored).loc[SCORE[0]:SCORE[1]]
            n, k = int(sc.sum()), int(ig.sum())
            sept = int(ig[ig.index.month == 9].sum())
            row.append((a, k, n, k / max(n, 1), sept))
        ok = all(x[3] <= Q for x in row)
        print(f"alpha_day={al:.0e}: " + "; ".join(f"{a} {k}/{n}={rt:.4f} (Sep {s})" for a, k, n, rt, s in row)
              + ("  <= q all" if ok else ""))
        if ok and chosen is None:
            chosen = al
    print("CHOSEN alpha_day =", chosen)
    if chosen is None:
        return 1
    # no-weight check: session-6 hurricane contrast with v2
    tc = compute_gwi_v2(wide(pv6[pv6.set == "test"], pd.Timestamp("2025-12-31")), alpha_day=chosen)
    ign = tc.ignition
    ev = [pd.Timestamp(d) for d in EVENTS if pd.Timestamp(d) >= SCORE[0]]
    h = window_hits(ign, ev)
    days = pd.date_range(SCORE[0], "2025-12-31", freq="D")
    near = set()
    for d in ev:
        near |= set(pd.date_range(d - pd.Timedelta(days=7), d + pd.Timedelta(days=9)))
    ctrl = [d for d in days[::3] if d.month in (6, 7, 8, 9, 10, 11) and d not in near]
    hc = window_hits(ign, ctrl)
    print(f"[no weight] Tropical cyclone v2: events hit {np.nansum(h):.0f}/{len(ev)}; "
          f"Jun-Nov control windows {np.nansum(hc):.0f}/{len(ctrl)}; all-days ignition rate "
          f"{ign.loc[SCORE[0]:].mean():.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
