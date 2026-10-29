"""SMF v2 §15.6: synthetic probe of DM lags 0/1/2 and a sign-flip test on storm means (session 2.7).

Exploratory design aid, no weight. Run from the repository root with PYTHONPATH=.
Rates at alpha 0.05 under the null, 1500 replications; printed only.
"""

import numpy as np

from analysis.smf_v2_power import ar1, t5
from emo.smf import diebold_mariano

rng = np.random.default_rng(1)


def means(n: int, rho: float) -> np.ndarray:
    k = 2 + rng.poisson(10, n)
    u = ar1(t5(rng, n), rho)
    return np.array([u[s] + ar1(t5(rng, k[s]), 0.7).mean() for s in range(n)])


def signflip(m: np.ndarray, b: int = 199) -> float:
    obs = m.mean()
    s = rng.choice([-1, 1], size=(b, len(m)))
    return float((1 + np.sum((s * m).mean(1) <= obs)) / (b + 1))


for rho in (0.0, 0.3):
    for n in (8, 12, 20):
        r = {"L0": 0, "L1": 0, "L2": 0, "sf": 0}
        R = 1500
        for _ in range(R):
            m = means(n, rho)
            for L in (0, 1, 2):
                r[f"L{L}"] += diebold_mariano(m, 0 * m, L)["p"] < 0.05
            r["sf"] += signflip(m) < 0.05
        print(rho, n, {k: round(v / R, 3) for k, v in r.items()})
