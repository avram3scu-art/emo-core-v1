"""GWI v2 synthetic checks (infrastructure; no real data). docs/GWI_V2_PROTOCOL.md §7.

A. Pipeline: false-ignition rate of v2 (alpha_day 3e-4; unfiltered and with the
   common-mode filter) on synthetic articles with weekday, annual and September-step
   seasonality, a December dip, serial correlation and shared factors.
B. Calibration decision rule (§5): P(PASS) when the true false-ignition rate is q, 2q, ...
C. Event test (§6): false-positive rate (no event effect) and power by number of events.
A2. Shared shocks (added at the session 2.6 review): as A, plus global episodes that lift every
   article for 3-20 days (school closures, holidays) and single-article event spikes; reports
   the false-ignition rate with and without the common-mode filter and the share of
   single-article spikes the filter keeps. Own seed, run last, so A-C are unchanged.
Run from the repository root: python analysis/gwi_v2_synthetic.py [--quick]
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
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

ALPHA_DAY, Q = 3e-4, 0.005
QUICK = "--quick" in sys.argv
RNG = np.random.default_rng(20261029)


# ---------- A ----------
def synth_article(days: pd.DatetimeIndex, common: np.ndarray, rng) -> pd.DataFrame:
    T, cols = len(days), {}
    art = np.zeros(T)
    for t in range(1, T):
        art[t] = 0.6 * art[t - 1] + rng.normal(0, 0.06)
    doy = days.dayofyear.to_numpy()
    for s in range(12):
        level = rng.uniform(5, 9)
        wk = rng.normal(0, 0.15, 7)
        amp = rng.uniform(0.05, 0.3)
        sept = rng.uniform(0.1, 0.4) * ((days.month >= 9) | (days.month <= 5)).astype(float)
        dec = -rng.uniform(0.1, 0.5) * (((days.month == 12) & (days.day >= 20)) | ((days.month == 1) & (days.day <= 3)))
        e = np.zeros(T)
        for t in range(1, T):
            e[t] = 0.5 * e[t - 1] + rng.normal(0, 0.12)
        y = (level + wk[days.dayofweek] + amp * np.sin(2 * np.pi * doy / 365.25 + rng.uniform(0, 6.3))
             + sept + dec + 0.002 * np.arange(T) / 365 + art + common + e)
        cols[f"s{s}"] = np.round(np.expm1(y))
    return pd.DataFrame(cols, index=days)


def part_a(n_art: int) -> None:
    days = pd.date_range("2022-01-01", "2026-12-31", freq="D")
    score = days[days >= "2026-01-01"]
    common = np.zeros(len(days))
    for t in range(1, len(days)):
        common[t] = 0.7 * common[t - 1] + RNG.normal(0, 0.03)
    res = []
    for _ in range(n_art):
        v = synth_article(days, common, RNG)
        r2 = compute_gwi_v2(v, ALPHA_DAY)
        res.append(r2.ignition.astype(float).where(r2.scored))
    p2 = pd.DataFrame(dict(enumerate(res))).loc[score]
    filt = pd.DataFrame({i: (p2[i] == 1) & ~common_mode(p2[i] == 1, p2.drop(columns=i)) for i in p2})
    sept = p2.index.month == 9
    print(f"A. {n_art} synthetic articles x 12 streams, scored year 2026 ({len(score)} days):")
    print(f"   v2 unfiltered:    rate {np.nanmean(p2.to_numpy()):.4f} (September {np.nanmean(p2[sept].to_numpy()):.4f})")
    print(f"   v2 filtered:      rate {filt.to_numpy().mean():.4f} (September {filt[sept].to_numpy().mean():.4f});"
          f" target q = {Q}")


def part_a2(n_art: int, seed: int = 2026102902) -> None:
    rng = np.random.default_rng(seed)
    days = pd.date_range("2022-01-01", "2026-12-31", freq="D")
    score = days[days >= "2026-01-01"]
    common = np.zeros(len(days))
    for t in range(1, len(days)):
        common[t] = 0.7 * common[t - 1] + rng.normal(0, 0.03)
    shock = np.zeros(len(days))
    for year in range(2022, 2027):
        for _ in range(3):
            start = int(rng.integers(0, 345)) + int(np.searchsorted(days, pd.Timestamp(f"{year}-01-01")))
            shock[start:start + int(rng.integers(3, 21))] = rng.uniform(0.4, 0.9)
    spike_days = sorted(rng.choice(np.where(days >= "2026-01-15")[0], 10, replace=False))
    res, spiked = [], []
    for i in range(n_art):
        v = synth_article(days, common + rng.uniform(0.5, 1.5) * shock, rng)
        if i < 10:  # article i gets one own spike on spike_days[i]
            v.iloc[spike_days[i]] *= 15
            spiked.append((i, days[spike_days[i]]))
        r2 = compute_gwi_v2(v, ALPHA_DAY)
        res.append(r2.ignition.astype(float).where(r2.scored))
    p2 = pd.DataFrame(dict(enumerate(res))).loc[score]
    filt = pd.DataFrame({i: (p2[i] == 1) & ~common_mode(p2[i] == 1, p2.drop(columns=i)) for i in p2})
    own = {(i, d) for i, d in spiked}
    keep_spike = np.mean([bool(filt.loc[d, i]) for i, d in spiked])
    hit_spike = np.mean([bool(p2.loc[d, i] == 1) for i, d in spiked])
    mask = pd.DataFrame(False, index=p2.index, columns=p2.columns)
    for i, d in own:
        mask.loc[d, i] = True
    sh = pd.Series(shock, index=days).loc[score] > 0
    unf = p2.where(~mask).to_numpy()
    fil = filt.where(~mask).astype(float).to_numpy()
    print(f"A2. Shared shocks: {n_art} synthetic articles, 3 global episodes a year (3-20 days), "
          f"{int(sh.sum())} shock days in 2026; {len(spiked)} single-article spikes:")
    print(f"   false-ignition rate unfiltered {np.nanmean(unf):.4f} (shock days {np.nanmean(unf[sh.to_numpy()]):.4f});"
          f" filtered {np.nanmean(fil):.4f} (shock days {np.nanmean(fil[sh.to_numpy()]):.4f}); target q = {Q}")
    print(f"   single-article spikes ignited {hit_spike:.2f}, kept by the filter {keep_spike:.2f}")


# ---------- B, C ----------
def clustered(T: int, rate: float, rng, cont: float = 0.33) -> np.ndarray:
    a = rate * (1 - cont) / (1 - rate)
    x = np.zeros(T)
    for t in range(1, T):
        x[t] = rng.random() < (cont if x[t - 1] else a)
    return x


def calibration_verdict(ign: pd.DataFrame) -> bool:
    rate, upper = block_bootstrap_upper(ign, n_boot=1000 if QUICK else 2000, seed=int(RNG.integers(1e9)))
    ps = [float(binom.sf(int(ign[c].sum()) - 1, int(ign[c].notna().sum()), 2 * Q)) for c in ign]
    bad = any(holm(ps))
    return (upper <= 2 * Q) and not bad


def part_b(reps: int) -> None:
    T, M = 365, 20
    print(f"B. Calibration rule, {M} articles x {T} days, clustered ignitions (mean run 1.5), {reps} reps:")
    for label, rates in [("all at 0.5q", [0.5 * Q] * M), ("all at q", [Q] * M),
                         ("all at 1.5q", [1.5 * Q] * M), ("all at 2q", [2 * Q] * M),
                         ("19 at q, 1 at 5q", [Q] * 19 + [5 * Q]),
                         ("heterogeneous, mean q", list(RNG.gamma(2, Q / 2, M)))]:
        passes = 0
        for _ in range(reps):
            ign = pd.DataFrame({m: clustered(T, min(r, 0.2), RNG) for m, r in enumerate(rates)})
            passes += calibration_verdict(ign)
        print(f"   {label:24s} P(PASS) = {passes / reps:.3f}")


def part_c(reps: int, n_perm: int) -> None:
    T, M = 365, 20
    idx = pd.date_range("2026-11-01", periods=T, freq="D")
    print(f"C. Event test, test article + {M} placebos, {reps} reps, {n_perm} permutations; "
          f"base window hit ~{1 - (1 - Q) ** 3:.3f}; PASS = both Holm-rejected at 0.05:")
    for n_ev in [8, 12, 15, 20]:
        line = []
        for h1 in [0.0, 0.3, 0.5, 0.7]:
            npass = 0
            for _ in range(reps):
                test = clustered(T, Q, RNG)
                pl = pd.DataFrame({m: clustered(T, Q, RNG) for m in range(M)}, index=idx)
                pos = np.sort(RNG.choice(np.arange(0, T - 3, 4), n_ev, replace=False))
                for p in pos:
                    if RNG.random() < h1:
                        test[p + int(RNG.integers(0, 3))] = 1
                res = event_test(pd.Series(test, index=idx), pl, [idx[p] for p in pos],
                                 n_perm=n_perm, seed=int(RNG.integers(1e9)))
                npass += all(holm([res["p_H"], res["p_D"]]))
            line.append(f"h1={h1:.1f}: {npass / reps:.3f}")
        print(f"   n={n_ev:2d}  " + "; ".join(line))


if __name__ == "__main__":
    part_a(6 if QUICK else 20)
    part_b(100 if QUICK else 500)
    part_c(50 if QUICK else 300, 199 if QUICK else 999)
    part_a2(6 if QUICK else 20)
