"""Synthetic false-positive rate and power for amendments 7-9 (docs/LOOP_PROTOCOL.md §20.4).

Synthetic only. Reads data/loop_hurricanes/summary.json for counts only (no lag or link value),
through analysis/loop_power_realized.py, to reproduce the realized 2015-2025 sizes and missingness.
"""
import importlib.util
import math
from pathlib import Path

import numpy as np
from scipy.stats import binom, binomtest


def _load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lp = _load("loop_power")
lr = _load("loop_power_realized")

SEED = 2026102940
EVENTS_PER_BLIND_SEASON = 5
PAIR = ("A", "Ystate")  # amendment 8


def blind_study(rng, known, K, m, r, q):
    """One study: realized known history + K blind seasons of 5 events, lags on m of them,
    A missing among lag storms with probability ~q (more often for weak storms)."""
    sizes, ny, nf, nfy = known
    d = lp.simulate(rng, sizes + (EVENTS_PER_BLIND_SEASON,) * K, r=r)
    dk, db = lp.split(d, len(sizes))
    dk = lr.impose(dk, rng, sizes, ny, nf, nfy)
    n = len(db["season"])
    lag = np.zeros(n, bool)
    for s in range(K):
        idx = np.flatnonzero(db["season"] == s)
        lag[rng.permutation(idx)[:m]] = True
    for k in lp.OUT:
        db[k] = np.where(lag, db[k], np.nan)
    if q > 0:
        p = np.clip(q * 2 / (1 + np.exp(db["V"])), 0, 1)
        db["A"] = np.where(lag & (rng.random(n) < p), np.nan, db["A"])
    return dk, db


def blind_cell(rng, known, K, m, r, q=0.0):
    rej = 0
    for _ in range(lp.REPS):
        dk, db = blind_study(rng, known, K, m, r, q)
        rej += lp.blind_test(dk, db, rng, pair=PAIR) < lp.ALPHA
    return rej / lp.REPS


def sequential_cell(rng, known, K=10, m=2):
    """§7 as registered: a test each December on the pooled blind seasons so far; any rejection at r = 0."""
    any_rej = 0
    for _ in range(lp.REPS):
        dk, db = blind_study(rng, known, K, m, 0.0, 0.0)
        for k in range(1, K + 1):
            sub = {key: v[db["season"] < k] for key, v in db.items()}
            if lp.blind_test(dk, sub, rng, pair=PAIR) < lp.ALPHA:
                any_rej += 1
                break
    return any_rej / lp.REPS


def h3r_exact(n=12, alpha=0.05):
    crit = next(x for x in range(n + 1) if binom.sf(x - 1, n, 0.5) < alpha)
    return crit, {p: binom.sf(crit - 1, n, p) for p in (0.5, 0.7, 0.8, 0.9, 0.95)}


def h3r_clustered(rng, p, rho=0.2, n_min=12, reps=20000):
    """Season clustering: per-season share ~ Beta(mean p, ICC rho); seasons of 2-3 D events;
    test run once when the pooled D first reaches n_min."""
    ab = 1 / rho - 1
    rej = 0
    for _ in range(reps):
        x = n = 0
        while n < n_min:
            ds = int(rng.integers(2, 4))
            th = rng.beta(p * ab, (1 - p) * ab)
            x += int(rng.binomial(ds, th))
            n += ds
        rej += binomtest(x, n, 0.5, alternative="greater").pvalue < 0.05
    return rej / reps


def main():
    known = lr.realized_counts()
    rng = np.random.default_rng(SEED)
    lp.STAT, lp.Y_SHOCK_SIGN, lp.P_MISS = "fe", -1.0, 0.0
    c5, c3 = lp.coupling_coef(0.5), lp.coupling_coef(0.3)
    print("Loop 2027+ blind arm and H3r (docs/LOOP_PROTOCOL.md §20.4). Synthetic; counts only.")
    print(f"seed {SEED}, {lp.REPS} studies/cell, {lp.PERMS} permutations, STAT fe, Y_SHOCK_SIGN -1, "
          f"pair {PAIR}; coupling coef r=0.3 {c3:.3f}, r=0.5 {c5:.3f}; MC SE of 5% "
          f"{math.sqrt(0.05 * 0.95 / lp.REPS):.4f}")
    print(f"known history: sizes {known[0]}; lags {known[1]}")
    print("Blind arm (amendment 8), q = 0 (no A missing among lag storms)")
    for m in (2, 4):
        for K in (1, 3, 5, 10):
            fpr = blind_cell(rng, known, K, m, 0.0)
            pw = blind_cell(rng, known, K, m, 0.5)
            extra = f" | power r=0.3 {blind_cell(rng, known, K, m, 0.3):.3f}" if m == 2 else ""
            print(f"  m={m} K={K:2d} (blind lags {m * K:2d}): FPR {fpr:.3f} | power r=0.5 {pw:.3f}{extra}", flush=True)
    print("Amendment 9: A missing among lag storms, q = 0.25, severity-dependent; m = 2")
    for K in (1, 3, 5, 10):
        print(f"  K={K:2d}: FPR {blind_cell(rng, known, K, 2, 0.0, 0.25):.3f} | "
              f"power r=0.5 {blind_cell(rng, known, K, 2, 0.5, 0.25):.3f}", flush=True)
    lp.KAPPA, lp.SIG_SEASON = 0.9, 1.5
    print("Stress (KAPPA 0.9, SIG_SEASON 1.5), m = 2, r = 0")
    for K in (1, 5, 10):
        print(f"  K={K:2d}: FPR {blind_cell(rng, known, K, 2, 0.0):.3f}", flush=True)
    lp.KAPPA, lp.SIG_SEASON = 0.5, 0.7
    print(f"§7 schedule as registered (test each December, 10 blind seasons, m = 2, r = 0): "
          f"any rejection {sequential_cell(rng, known):.3f}", flush=True)
    crit, ex = h3r_exact()
    print(f"H3r (amendment 7), D = 12: PASS needs >= {crit} measured; exact rejection by true share: "
          + ", ".join(f"{p}: {v:.3f}" for p, v in ex.items()))
    rng2 = np.random.default_rng(SEED + 1)
    print("H3r with season clustering (ICC 0.2, seasons of 2-3, run at pooled D >= 12; 20,000 runs): "
          + ", ".join(f"{p}: {h3r_clustered(rng2, p):.3f}" for p in (0.5, 0.8, 0.9, 0.95)))


if __name__ == "__main__":
    main()
