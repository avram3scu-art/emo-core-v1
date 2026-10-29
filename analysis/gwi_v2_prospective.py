"""GWI v2 prospective calibration and event tests, docs/GWI_V2_PROTOCOL.md §5-§6, §8.

Pre-registered (evidence class: pre-registered blind). Reads data/sources/gwi_v2/ written by
scripts/fetch_gwi_v2.py on or after the scoring date; prints "not yet" otherwise.
Run from the repository root: python analysis/gwi_v2_prospective.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from scipy.stats import binom

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from emo.gwi_v2 import (  # noqa: E402
    block_bootstrap_upper,
    common_mode,
    compute_gwi_v2,
    event_test,
    holm,
)

DATA = ROOT / "data/sources/gwi_v2"
ALPHA_DAY, Q = 3e-4, 0.005
W = (pd.Timestamp("2026-11-01"), pd.Timestamp("2027-10-31"))
DAYS = pd.date_range("2022-07-01", "2027-11-02", freq="D")
MIN_STREAMS, MIN_PLACEBOS, MIN_EVENTS, MERGE_DAYS, WIN = 8, 15, 8, 3, 3


def wide(long: pd.DataFrame) -> pd.DataFrame:
    w = long.pivot_table(index="date", columns="lang", values="views", aggfunc="sum")
    w.index = pd.to_datetime(w.index)
    w = w.reindex(DAYS).fillna(0.0)
    return w[[c for c in w.columns if (w[c] == 0).mean() <= 0.05]]


def events(usgs: pd.DataFrame) -> list[pd.Timestamp]:
    t = pd.to_datetime(usgs["time"], utc=True).dt.tz_localize(None).dt.normalize()
    t = sorted(t[(usgs["mag"] >= 7.0) & (t >= W[0]) & (t <= W[1])])
    out: list[pd.Timestamp] = []
    for d in t:
        if not out or (d - out[-1]).days > MERGE_DAYS:
            out.append(d)
    return out


def main() -> int:
    if not (DATA / "MANIFEST.txt").exists():
        print("GWI v2 prospective test: not yet (data are fetched on or after 2027-11-15).")
        return 0
    pv = pd.read_csv(DATA / "pageviews.csv")
    usgs = pd.read_csv(DATA / "usgs_m7.csv")
    print("Pre-registered: docs/GWI_V2_PROTOCOL.md; alpha_day 3e-4; q 0.005; window", W[0].date(), "..", W[1].date())
    arts = {}
    for s, g in pv.groupby("set"):
        w = wide(g)
        print(f"  {s}: {w.shape[1]} streams" + ("  (dropped: < 8)" if w.shape[1] < MIN_STREAMS else ""))
        if w.shape[1] >= MIN_STREAMS:
            arts[s] = compute_gwi_v2(w, ALPHA_DAY, MIN_STREAMS)
    plac = {s: r for s, r in arts.items() if s.startswith("placebo:")}
    ign = pd.DataFrame({s: r.ignition.astype(float).where(r.scored) for s, r in plac.items()}).loc[W[0]:W[1]]
    # calibration (§5)
    cal = "NOT TESTABLE"
    if len(plac) >= MIN_PLACEBOS:
        filt = pd.DataFrame({s: ((ign[s] == 1) & ~common_mode(ign[s] == 1, ign.drop(columns=s))).astype(float)
                             .where(ign[s].notna()) for s in ign})
        rate, upper = block_bootstrap_upper(filt, block=14, n_boot=4000, level=0.975, seed=0)
        ps = [float(binom.sf(int(filt[s].sum()) - 1, int(filt[s].notna().sum()), 2 * Q)) for s in filt]
        bad = [s for s, b in zip(filt.columns, holm(ps), strict=True) if b]
        cal = "PASS" if (upper <= 2 * Q and not bad) else "FAIL"
        print(f"Calibration: {len(plac)} placebo articles; pooled rate {rate:.4f}; upper 97.5% {upper:.4f}"
              f" (<= {2 * Q}); articles significantly above 2q (Holm): {bad or 'none'}")
        for s in filt:
            print(f"    {s}: {int(filt[s].sum())}/{int(filt[s].notna().sum())}")
    print("CALIBRATION RESULT:", cal)
    # event test (§6)
    ev = events(usgs)
    res_ev = "NOT TESTABLE"
    if "test" in arts and len(ev) >= MIN_EVENTS and len(plac) >= MIN_PLACEBOS:
        t_ign = arts["test"].ignition.loc[W[0]:W[1] + pd.Timedelta(days=WIN - 1)]
        pan = pd.DataFrame({s: r.ignition.astype(float).where(r.scored) for s, r in plac.items()}).reindex(t_ign.index)
        t_f = t_ign & ~common_mode(t_ign, pan)
        p_f = pd.DataFrame({s: (pan[s] == 1) & ~common_mode(pan[s] == 1, pan.drop(columns=s)) for s in pan})
        r = event_test(t_f, p_f, ev, block=14, n_perm=9999, length=WIN, seed=0)
        rej = holm([r["p_H"], r["p_D"]])
        res_ev = "PASS" if all(rej) else "FAIL"
        print(f"Events: n = {len(ev)} ({', '.join(str(d.date()) for d in ev)})")
        print(f"  H = {r['H']:.3f} (p {r['p_H']:.4f}); D = H - placebo = {r['D']:.3f} (p {r['p_D']:.4f}); Holm {rej}")
    else:
        print(f"Events: n = {len(ev)}; test article present: {'test' in arts}")
    print("EVENT RESULT:", res_ev)
    print("H2:", "supported at this test" if cal == res_ev == "PASS" else
          ("FAILS (PLAN §4)" if "FAIL" in (cal, res_ev) else "not testable"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
