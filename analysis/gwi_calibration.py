"""GWI calibration test, pre-registered in docs/GWI_CALIBRATION_PROTOCOL.md.

Threshold f_cal calibrated on the coincidence fraction of the reference placebo
"Photosynthesis" (2016-2025, target q = 0.005 ignition days per day), then applied
unchanged to held-out placebo articles (2016-01-01..2026-10-18), to Photosynthesis in
2026, and to the session-6 hurricane test.

If the calibration pageview file is absent, says so and stops.
Run from the repository root: python analysis/gwi_calibration.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))

from emo.gwi import calibrate_fraction_threshold, coincidence_fraction, compute_gwi  # noqa: E402
import gwi_hurricanes as gh  # noqa: E402

PV6 = gh.PAGEVIEWS
PVC = ROOT / "data/sources/wikipedia_pageviews_gwi_calibration/wikipedia_pageviews_gwi_calibration.csv"
TRAIN = (pd.Timestamp("2016-01-01"), pd.Timestamp("2025-12-31"))
HELD_END = pd.Timestamp("2026-10-18")
T26 = (pd.Timestamp("2026-01-01"), HELD_END)
Q, BASE, MIN_STREAMS = 0.005, 56, 8
EPS = 1e-9


def build_r(long: pd.DataFrame, start, end, excl_period) -> tuple[pd.DataFrame, list[str]]:
    wide = long.pivot_table(index="date", columns="lang", values="views", aggfunc="sum")
    wide.index = pd.to_datetime(wide.index)
    wide = wide.reindex(pd.date_range(start - pd.Timedelta(days=BASE + 5), end, freq="D")).fillna(0.0)
    days = wide.loc[excl_period[0]:excl_period[1]]
    keep = [c for c in wide.columns if (days[c] == 0).mean() <= 0.05]
    excluded = [c for c in wide.columns if c not in keep]
    y = np.log1p(wide[keep])
    base = y.shift(1).rolling(BASE, min_periods=BASE).median()
    return (y - base).loc[start:end], excluded


def rate(g: pd.Series, f: float, a, b) -> tuple[int, int]:
    s = g.loc[a:b]
    return int((s >= f - EPS).sum()), len(s)


def main() -> int:
    if not PV6.exists() or not PVC.exists():
        print("Calibration pageviews not fetched yet: test not run.")
        return 0
    pv6, pvc = pd.read_csv(PV6), pd.read_csv(PVC)
    print("Pre-registered: docs/GWI_CALIBRATION_PROTOCOL.md; q = 0.005; z > 2.0; training 2016-01-01..2025-12-31")

    # Reference: session-6 Photosynthesis (to 2025-12-31) + calibration file after that date.
    ref6 = pv6[pv6["set"] == "placebo"]
    ref26 = pvc[(pvc["set"] == "reference_2026") & (pd.to_datetime(pvc["date"]) > TRAIN[1])]
    ref = pd.concat([ref6, ref26])
    r_ref, ex = build_r(ref, TRAIN[0], HELD_END, TRAIN)
    n = r_ref.shape[1]
    print(f"\n[reference Photosynthesis] streams: {', '.join(r_ref.columns)}; excluded: {ex or 'none'}")
    g_ref = coincidence_fraction(r_ref, *TRAIN)
    f_cal = calibrate_fraction_threshold(g_ref.loc[TRAIN[0]:TRAIN[1]], n, Q)
    if not np.isfinite(f_cal):
        print("RESULT: FAIL (no threshold reaches q on the reference)")
        return 0
    k = round(f_cal * n)
    kb = compute_gwi(r_ref.loc[TRAIN[0]:TRAIN[1]]).min_streams_for_event
    tr, tn = rate(g_ref, f_cal, *TRAIN)
    print(f"  f_cal = {f_cal:.4f} (k = {k} of {n}); [no weight] binomial k_min = {kb}; training rate {tr}/{tn} = {tr / tn:.4f}")
    c2, c2n = rate(g_ref, f_cal, *T26)
    ok2 = c2 / c2n <= 2 * Q
    print(f"  2026 (time held out): {c2}/{c2n} = {c2 / c2n:.4f}; <= {2 * Q}: {ok2}")

    # Held-out articles.
    held = []
    for name in sorted(s for s in pvc["set"].unique() if s.startswith("heldout_")):
        r, ex = build_r(pvc[pvc["set"] == name], TRAIN[0], HELD_END, (TRAIN[0], HELD_END))
        title = pvc.loc[(pvc["set"] == name) & (pvc["lang"] == "en"), "title"]
        title = title.iloc[0] if len(title) else name
        if r.shape[1] < MIN_STREAMS:
            print(f"\n[{title}] dropped: {r.shape[1]} streams (< {MIN_STREAMS})")
            continue
        g = coincidence_fraction(r, *TRAIN)
        h, hn = rate(g, f_cal, TRAIN[0], HELD_END)
        h26, h26n = rate(g, f_cal, *T26)
        ok = h / hn <= 2 * Q
        held.append(ok)
        print(f"\n[{title}] streams: {', '.join(r.columns)}; excluded: {ex or 'none'}")
        print(f"  rate 2016-01-01..2026-10-18: {h}/{hn} = {h / hn:.4f}; <= {2 * Q}: {ok}")
        print(f"  [no weight] 2026 only: {h26}/{h26n} = {h26 / h26n:.4f}")
    if len(held) < 2:
        print("\nRESULT: NOT TESTABLE (fewer than 2 held-out articles)")
        return 0
    ok1 = all(held)

    # Discrimination on session-6 events (seen data), calibrated rule.
    events = gh.landfall_events()
    ctrl = gh.control_blocks(events, season_only=True)
    out = {}
    for which in ("test", "placebo"):
        r, _ = gh.streams(pv6, which)
        g = coincidence_fraction(r, gh.START, gh.END)
        ign = set(g.index[g >= f_cal - EPS])
        eh, en, ch, cn = gh.hit_shares(ign, events, ctrl)
        _, p = fisher_exact([[eh, en - eh], [ch, cn - ch]], alternative="greater")
        out[which] = (eh, en, ch, cn, p, len(ign))
    eh, en, ch, cn, p, ni = out["test"]
    ok3 = eh / en >= 0.5 and p < 0.05
    print(f"\n[Tropical cyclone, session-6 events, calibrated rule] ignition days {ni}; "
          f"events hit {eh}/{en} = {eh / en:.3f}; controls {ch}/{cn} = {ch / cn:.3f}; Fisher p = {p:.4g}")
    eh, en, ch, cn, p, ni = out["placebo"]
    print(f"  [no weight] placebo rerun: ignition days {ni}; events hit {eh}/{en}; controls {ch}/{cn}; p = {p:.4g}")

    passed = ok1 and ok2 and ok3
    print(f"\nRESULT: {'PASS' if passed else 'FAIL'} (held-out articles <= 2q: {ok1}; 2026 <= 2q: {ok2}; "
          f"discrimination kept: {ok3})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
