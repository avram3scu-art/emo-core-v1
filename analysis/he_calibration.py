"""He direction test: calibration of candidate tests (docs/HE_CALIBRATION_PROTOCOL.md).

Synthetic data only. Run once; output recorded in analysis/he_calibration_output.txt.
"""
import math
from itertools import product

import numpy as np

SEED = 20261029
REPS = 2000
PERMS = 499
CHUNK = 100
ALPHA = 0.05
CODING_ERR = 0.5
BETAS = (0.0, 0.3, 0.5)
LAMBDAS = (0.0, 0.5)
MS = (3, 5)
NS = (3, 8, 12, 20, 30)


def mahonian_cdf(n):
    """P(number of discordant pairs <= d) under independence, d = 0..n(n-1)/2."""
    dist = np.array([1.0])
    for k in range(2, n + 1):
        new = np.zeros(len(dist) + k - 1)
        for j in range(k):
            new[j : j + len(dist)] += dist
        dist = new
    return np.cumsum(dist) / math.factorial(n)


def simulate(rng, n, m, beta, lam):
    R = REPS
    H = rng.normal(size=(R, n))
    he = H + CODING_ERR * rng.normal(size=(R, n))
    G = rng.normal(size=(R, 1, n))
    U = rng.normal(size=(R, m, n))
    # letters already sign-flipped so the predicted direction is positive for all
    L = beta * H[:, None, :] + np.sqrt(1 - beta**2) * (np.sqrt(lam) * G + np.sqrt(1 - lam) * U)
    return he, L


def run_cell(rng, n, m, beta, lam, cdf):
    he, L = simulate(rng, n, m, beta, lam)
    i, j = np.triu_indices(n, 1)
    npairs = len(i)
    sH = np.sign(he[:, i] - he[:, j])                 # (R, pairs)
    sL = np.sign(L[:, :, i] - L[:, :, j])             # (R, m, pairs)
    tau = (sL * sH[:, None, :]).sum(-1) / npairs      # (R, m)
    disc = np.rint((npairs - tau * npairs) / 2).astype(int)
    p_letter = cdf[disc]                              # exact one-sided Kendall p

    t_a = (tau > 0).sum(1) >= math.ceil(m / 2)
    t_b = (p_letter < ALPHA).any(1)
    t_c = p_letter.min(1) < ALPHA / m                 # Holm: any rejection iff min p < alpha/m

    mL = sL.mean(1)                                   # (R, pairs)
    obs = (sH * mL).sum(1) / npairs
    p_d = np.empty(REPS)
    for s in range(0, REPS, CHUNK):
        e = min(s + CHUNK, REPS)
        perm = np.argsort(rng.random((e - s, PERMS, n)), axis=2)
        hp = np.take_along_axis(np.broadcast_to(he[s:e, None, :], perm.shape), perm, axis=2)
        sHp = np.sign(hp[:, :, i] - hp[:, :, j])
        null = (sHp * mL[s:e, None, :]).sum(-1) / npairs
        p_d[s:e] = (1 + (null >= obs[s:e, None] - 1e-12).sum(1)) / (PERMS + 1)
    t_d = p_d < ALPHA
    return {"T-A": t_a.mean(), "T-B": t_b.mean(), "T-C": t_c.mean(), "T-D": t_d.mean()}


def main():
    rng = np.random.default_rng(SEED)
    tests = ("T-A", "T-B", "T-C", "T-D")
    res = {}
    print("He calibration (docs/HE_CALIBRATION_PROTOCOL.md). Synthetic data only.")
    print(f"seed {SEED}, {REPS} studies/cell, {PERMS} permutations, coding error SD {CODING_ERR}")
    print(f"MC SE of a 5% rate: {math.sqrt(0.05 * 0.95 / REPS):.4f}\n")
    print(f"{'n':>3} {'m':>2} {'beta':>5} {'lam':>4} " + " ".join(f"{t:>6}" for t in tests))
    for n in NS:
        cdf = mahonian_cdf(n)
        for m, beta, lam in product(MS, BETAS, LAMBDAS):
            r = run_cell(rng, n, m, beta, lam, cdf)
            res[(n, m, beta, lam)] = r
            print(f"{n:3d} {m:2d} {beta:5.2f} {lam:4.1f} " + " ".join(f"{r[t]:6.3f}" for t in tests),
                  flush=True)

    print("\nUsable = FPR <= 0.060 at beta 0 (both lambda) AND power >= 0.80 at beta 0.5 (both lambda)")
    for m in MS:
        for t in tests:
            ok = [n for n in NS
                  if all(res[(n, m, 0.0, lam)][t] <= 0.060 for lam in LAMBDAS)
                  and all(res[(n, m, 0.5, lam)][t] >= 0.80 for lam in LAMBDAS)]
            calib = [n for n in NS if all(res[(n, m, 0.0, lam)][t] <= 0.060 for lam in LAMBDAS)]
            print(f"m={m} {t}: smallest usable n = {ok[0] if ok else 'none up to 30'}; "
                  f"FPR within limit at n = {calib if calib else 'none'}")


if __name__ == "__main__":
    main()
