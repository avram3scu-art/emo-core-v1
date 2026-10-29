"""He direction test on the hurricane loop: synthetic FPR and power (docs/HE_CALIBRATION_PROTOCOL.md §10.5).

Synthetic data only. Model of §2 at the realized season sizes of §10.2, m = 3 letters,
plus a season shock (weight KAPPA) shared by He and every letter. T-D with a within-season
null (§10.3) and with the across-all null (§3). Run once; output analysis/he_loop_power_output.txt.
"""
from itertools import product

import numpy as np

SEED = 2026102991
REPS = 2000
PERMS = 999
CHUNK = 50
ALPHA = 0.05
CODING_ERR = 0.5
M = 3
SIZES = (2, 3, 2, 1, 5, 1, 3, 1, 5)  # 2016..2024, complete cases (summary.json counts)
BETAS = (0.0, 0.3, 0.5)
LAMBDAS = (0.0, 0.5)
KAPPAS = (0.0, 1.0)


def season_index():
    return np.repeat(np.arange(len(SIZES)), SIZES)


def permute(rng, shape, season, within):
    keys = rng.random(shape)
    if within:
        keys = keys + season * 10.0  # blocks are contiguous: sorting keeps each season's cases in it
    return np.argsort(keys, axis=-1)


def td_pvalues(rng, he, L, season, within):
    n = he.shape[1]
    i, j = np.triu_indices(n, 1)
    npairs = len(i)
    sH = np.sign(he[:, i] - he[:, j])
    mL = np.sign(L[:, :, i] - L[:, :, j]).mean(1)
    obs = (sH * mL).sum(1) / npairs
    p = np.empty(len(he))
    for s in range(0, len(he), CHUNK):
        e = min(s + CHUNK, len(he))
        perm = permute(rng, (e - s, PERMS, n), season, within)
        hp = np.take_along_axis(np.broadcast_to(he[s:e, None, :], perm.shape), perm, axis=2)
        null = (np.sign(hp[:, :, i] - hp[:, :, j]) * mL[s:e, None, :]).sum(-1) / npairs
        p[s:e] = (1 + (null >= obs[s:e, None] - 1e-12).sum(1)) / (PERMS + 1)
    return p


def simulate(rng, beta, lam, kappa, season):
    n = len(season)
    H = rng.normal(size=(REPS, n))
    Z = rng.normal(size=(REPS, len(SIZES)))[:, season]
    he = H + CODING_ERR * rng.normal(size=(REPS, n)) + kappa * Z
    G = rng.normal(size=(REPS, 1, n))
    U = rng.normal(size=(REPS, M, n))
    L = beta * H[:, None, :] + np.sqrt(1 - beta**2) * (np.sqrt(lam) * G + np.sqrt(1 - lam) * U)
    L = L + kappa * Z[:, None, :]
    return he, L


def main():
    rng = np.random.default_rng(SEED)
    season = season_index()
    print("He loop power (docs/HE_CALIBRATION_PROTOCOL.md §10.5). Synthetic data only.")
    print(f"seed {SEED}, {REPS} studies/cell, {PERMS} permutations, n {len(season)}, "
          f"season sizes {SIZES}, m {M}\n")
    print(f"{'beta':>5} {'lam':>4} {'kappa':>5} {'within':>7} {'across':>7}")
    worst = 0.0
    for beta, lam, kappa in product(BETAS, LAMBDAS, KAPPAS):
        he, L = simulate(rng, beta, lam, kappa, season)
        pw = (td_pvalues(rng, he, L, season, True) < ALPHA).mean()
        pa = (td_pvalues(rng, he, L, season, False) < ALPHA).mean()
        if beta == 0.0:
            worst = max(worst, pw)
        print(f"{beta:5.2f} {lam:4.1f} {kappa:5.1f} {pw:7.3f} {pa:7.3f}", flush=True)
    print(f"\nWithin-season FPR max over cells: {worst:.3f} (criterion <= 0.060: "
          f"{'met' if worst <= 0.060 else 'NOT met'})")


if __name__ == "__main__":
    main()
