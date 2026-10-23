"""GWI on real attention data: pre-registered test, docs/GWI_PROTOCOL.md (session 6).

Events: Atlantic major-hurricane landfalls 2016-2025 from NHC HURDAT2 (rule in §2).
Attention: daily Wikipedia pageviews, 12 language editions, test set "Tropical cyclone",
placebo set "Photosynthesis" (§3). Ignition rule: emo.gwi.compute_gwi, unchanged (§4).

If the pageview file is absent, prints the event list only.
Run from the repository root: python analysis/gwi_hurricanes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from emo.gwi import compute_gwi  # noqa: E402

HURDAT = ROOT / "data/sources/hurdat2_atlantic/hurdat2_atlantic.txt"
PAGEVIEWS = ROOT / "data/sources/wikipedia_pageviews_gwi/wikipedia_pageviews_gwi.csv"
START, END = pd.Timestamp("2016-01-01"), pd.Timestamp("2025-12-31")
MIN_KT, HALF, GAP, BASE = 96, 2, 10, 56
SEASON = range(6, 12)  # June-November


def landfall_events(path: Path = HURDAT) -> list[tuple[pd.Timestamp, str]]:
    """First landfall >= 96 kt per storm, 2016-2025; overlapping windows merged."""
    first: list[tuple[pd.Timestamp, str]] = []
    storm = None
    done = False
    for line in path.read_text().splitlines():
        f = [x.strip() for x in line.split(",")]
        if f[0].startswith("AL") and len(f[0]) == 8:  # storm header, e.g. "AL092017, HARVEY, 60,"
            storm, done = f"{f[1].title()} ({f[0]})", False
            continue
        if storm is None or done or len(f) < 7:
            continue
        day = pd.Timestamp(f[0])
        if f[2] == "L" and int(f[6]) >= MIN_KT and START <= day <= END:
            first.append((day, storm))
            done = True
    first.sort()
    merged: list[tuple[pd.Timestamp, str]] = []
    for day, name in first:
        if merged and (day - merged[-1][0]).days <= 2 * HALF:
            merged[-1] = (merged[-1][0], merged[-1][1] + " + " + name)
        else:
            merged.append((day, name))
    return merged


def streams(pv: pd.DataFrame, which: str) -> tuple[pd.DataFrame, list[str]]:
    sub = pv[pv["set"] == which]
    wide = sub.pivot_table(index="date", columns="lang", values="views", aggfunc="sum")
    wide.index = pd.to_datetime(wide.index)
    full = pd.date_range(START - pd.Timedelta(days=BASE + 5), END, freq="D")
    wide = wide.reindex(full).fillna(0.0)
    days = wide.loc[START:END]
    keep = [c for c in wide.columns if (days[c] == 0).mean() <= 0.05]
    excluded = [c for c in wide.columns if c not in keep]
    y = np.log1p(wide[keep])
    base = y.shift(1).rolling(BASE, min_periods=BASE).median()
    return (y - base).loc[START:END], excluded


def hit_shares(ign: set, events, controls) -> tuple[int, int, int, int]:
    def hit(d0, d1):
        return any(d in ign for d in pd.date_range(d0, d1))
    eh = sum(hit(d - pd.Timedelta(days=HALF), d + pd.Timedelta(days=HALF)) for d, _ in events)
    ch = sum(hit(a, b) for a, b in controls)
    return eh, len(events), ch, len(controls)


def control_blocks(events, season_only: bool):
    edays = [d for d, _ in events]
    out = []
    a = START
    while a + pd.Timedelta(days=4) <= END:
        b = a + pd.Timedelta(days=4)
        days = pd.date_range(a, b)
        far = all(min(abs((x - e).days) for e in edays) > GAP for x in days)
        if far and (not season_only or all(x.month in SEASON for x in days)):
            out.append((a, b))
        a = b + pd.Timedelta(days=1)
    return out


def main() -> int:
    events = landfall_events()
    print(f"Events (rule: first landfall >= {MIN_KT} kt per storm, {START.date()}..{END.date()}, "
          f"windows +/-{HALF} d merged): n = {len(events)}")
    for d, name in events:
        print(f"  {d.date()}  {name}")
    if not PAGEVIEWS.exists():
        print("Pageviews not fetched yet: test not run.")
        return 0
    if len(events) < 8:
        print("RESULT: NOT TESTABLE (fewer than 8 events)")
        return 0

    pv = pd.read_csv(PAGEVIEWS)
    ctrl = control_blocks(events, season_only=True)
    ctrl_all = control_blocks(events, season_only=False)
    verdict = {}
    for which in ("test", "placebo"):
        r, excluded = streams(pv, which)
        print(f"\n[{which}] streams used: {', '.join(r.columns)}; excluded (>5% zero days): {excluded or 'none'}")
        if r.shape[1] < 8:
            print(f"RESULT: NOT TESTABLE ({which} set has {r.shape[1]} streams)")
            return 0
        res = compute_gwi(r, z_threshold=2.0, alpha=0.05)
        ign = set(res.events)
        eh, en, ch, cn = hit_shares(ign, events, ctrl)
        _, p = fisher_exact([[eh, en - eh], [ch, cn - ch]], alternative="greater")
        _, _, cha, cna = hit_shares(ign, events, ctrl_all)
        print(f"  ignition days: {len(ign)} of {len(r)}; k_min = {res.min_streams_for_event} of {r.shape[1]}; "
              f"excursion rate p = {res.extra['excursion_rate']:.4f}; expected false ignitions = {res.expected_false_events:.3f}")
        print(f"  event windows hit: {eh}/{en} = {eh / en:.3f}")
        print(f"  control windows hit (Jun-Nov): {ch}/{cn} = {ch / max(cn, 1):.3f}; Fisher one-sided p = {p:.4g}")
        print(f"  [no weight] control windows hit (all year): {cha}/{cna} = {cha / max(cna, 1):.3f}")
        hits = [str(d.date()) for d, _ in events
                if any(x in ign for x in pd.date_range(d - pd.Timedelta(days=HALF), d + pd.Timedelta(days=HALF)))]
        print(f"  events hit: {', '.join(hits) or 'none'}")
        verdict[which] = (eh / en, p)
    h, p = verdict["test"]
    pp = verdict["placebo"][1]
    ok = h >= 0.5 and p < 0.05 and pp >= 0.05
    print(f"\nRESULT: {'PASS' if ok else 'FAIL'} (H >= 0.5: {h >= 0.5}; p < 0.05: {p < 0.05}; placebo p >= 0.05: {pp >= 0.05})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
