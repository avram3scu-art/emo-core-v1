"""Loop power at the realized 2015-2025 sizes (docs/LOOP_PROTOCOL.md §15 guard part 2, §18 item 2).

Synthetic only. Reads data/loop_hurricanes/summary.json for counts only (no lag or link value).
"""
import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("loop_power", Path(__file__).with_name("loop_power.py"))
lp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lp)

SEED = 2026102931


def realized_counts():
    s = json.loads((ROOT / "data/loop_hurricanes/summary.json").read_text())
    seasons = [str(y) for y in s["seasons"]]
    ps, cc = s["per_season"], s["complete_cases_by_season_per_pair"]
    sizes = tuple(ps[y]["events"] for y in seasons)
    ny = tuple(ps[y]["Y_state"] for y in seasons)
    nf = tuple(ps[y]["F"] for y in seasons)
    nfy = tuple(cc["F~Y_state"][y] for y in seasons)
    return sizes, ny, nf, nfy


def impose(d, rng, sizes, ny, nf, nfy):
    """Realized missingness per season: lags on ny_s storms, F on nfy_s of them and nf_s - nfy_s others."""
    start = 0
    ymask = np.zeros(int(sum(sizes)), bool)
    fmask = np.zeros_like(ymask)
    for n, a, f, fy in zip(sizes, ny, nf, nfy, strict=True):
        idx = start + rng.permutation(n)
        yi, other = idx[:a], idx[a:]
        ymask[yi] = True
        fmask[yi[:fy]] = True
        fmask[other[: f - fy]] = True
        start += n
    d = dict(d)  # W and A stay complete (realized 52/52; P_MISS set to 0 in main)
    for k in lp.OUT:
        d[k] = np.where(ymask, d[k], np.nan)
    d["F"] = np.where(fmask, d["F"], np.nan)
    return d


def main():
    sizes, ny, nf, nfy = realized_counts()
    rng = np.random.default_rng(SEED)
    lp.STAT, lp.Y_SHOCK_SIGN, lp.P_MISS = "fe", -1.0, 0.0  # W, A always present; F, Y masked by impose()
    c5 = lp.coupling_coef(0.5)
    print("Loop power at realized 2015-2025 sizes (docs/LOOP_PROTOCOL.md §15, §18.2). Synthetic; counts only.")
    print(f"seed {SEED}, {lp.REPS} studies/cell, {lp.PERMS} permutations, STAT fe, Y_SHOCK_SIGN -1")
    print(f"sizes {sizes}; lags {ny}; F {nf}; F with lags {nfy}; coupling coefficient r=0.5: {c5:.3f}")
    for r in (0.0, 0.5):
        any_rej = true_rej = 0
        for _ in range(lp.REPS):
            d = impose(lp.simulate(rng, sizes, r=r), rng, sizes, ny, nf, nfy)
            adj = lp.holm([lp.h4_pair(d, x, y, rng)[0] for x, y in lp.PAIRS])
            any_rej += adj.min() < lp.ALPHA
            true_rej += adj[lp.PAIRS.index(lp.TRUE_PAIR)] < lp.ALPHA
        print(f"H4 r={r:.1f}: family-wise any {any_rej / lp.REPS:.3f} | true pair {true_rej / lp.REPS:.3f}", flush=True)
    for delta in (0.0, 1.0):
        rej = 0
        for _ in range(lp.REPS):
            d = impose(lp.simulate(rng, sizes, delta=delta, gamma_f=0.4), rng, sizes, ny, nf, nfy)
            rej += lp.holm([lp.h5_outcome(d, y, rng) for y in lp.OUT]).min() < lp.ALPHA
        print(f"H5 delta={delta:.0f}: rejection {rej / lp.REPS:.3f}", flush=True)


if __name__ == "__main__":
    main()
