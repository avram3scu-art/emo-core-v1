"""SMF v2, docs/SMF_PROTOCOL.md §15.6: false-positive rate and power from synthetic data only.

Run before any 2026 NHC data are fetched. Output: analysis/smf_v2_power_output.txt.
World: n storms; storm s has k_s ~ 2 + Poisson(10) forecasts; forecast differential
d = mu + u_s + e, with u_s an AR(1) (rho 0, 0.15 or 0.3 between consecutive storms) t5 storm effect (sd 1) and e a t5
within-storm term (sd 1, also AR(1) rho 0.7 within the storm). mu = -delta * sd(storm mean).
The test is emo.smf.smf_skill with clusters (storm means, DM lags emo.smf_nhc.DM_LAGS, one-sided), then Holm.
"""

import numpy as np

from emo.smf import smf_family, smf_skill
from emo.smf_nhc import ALPHA, DM_LAGS, MIN_STORMS


def t5(rng: np.random.Generator, n: int) -> np.ndarray:
    return rng.standard_t(5, n) / np.sqrt(5 / 3)


def ar1(x: np.ndarray, rho: float) -> np.ndarray:
    y = x.copy()
    for i in range(1, len(y)):
        y[i] = rho * y[i - 1] + np.sqrt(1 - rho**2) * x[i]
    return y


def one_test(rng: np.random.Generator, n: int, delta: float, name: str = "x", sd_mean: float = 1.0,
             rho: float = 0.15):
    k = 2 + rng.poisson(10, n)
    u = ar1(t5(rng, n), rho)
    d, cl = [], []
    for s in range(n):
        e = ar1(t5(rng, k[s]), 0.7)
        d.append(u[s] + e)
        cl += [s] * k[s]
    d = np.concatenate(d)
    d = d - delta * sd_mean
    bench = np.full_like(d, 100.0)
    return smf_skill(name, bench + d, bench, DM_LAGS, clusters=np.array(cl))


def storm_mean_sd(rng: np.random.Generator) -> float:
    """Empirical sd of a storm's mean differential at delta 0 (the unit of delta)."""
    m = []
    for _ in range(4000):
        k = 2 + rng.poisson(10)
        m.append(t5(rng, 1)[0] + ar1(t5(rng, k), 0.7).mean())
    return float(np.std(m))


def main() -> None:
    rng = np.random.default_rng(20261029)
    R = 2000
    sdm = storm_mean_sd(rng)
    lines = ["SMF v2 synthetic check (docs/SMF_PROTOCOL.md §15.6); seed 20261029; 2000 replications per cell",
             f"delta in units of the sd of a storm mean differential ({sdm:.3f})", ""]
    lines.append("Single test, one-sided DM-HLN on storm means: rejection rate at the family alpha and at alpha/6 (Holm worst case)")
    lines.append(f"family alpha = {ALPHA}")
    lines.append(f"{'rho':>5s} {'storms':>6s} {'delta':>6s} {'P(p<a)':>10s} {'P(p<a/6)':>12s}")
    for rho in (0.0, 0.15, 0.3):
        for n in (8, 12, 15, 20):
            for delta in (0.0, 0.5, 0.8, 1.0, 1.5):
                p = np.array([one_test(rng, n, delta, sd_mean=sdm, rho=rho).p for _ in range(R)])
                lines.append(f"{rho:5.2f} {n:6d} {delta:6.1f} {np.mean(p < ALPHA):10.3f} {np.mean(p < ALPHA / 6):12.3f}")
    lines.append("")
    lines.append("Family of 6 under the global null (independent tests, worst case for Holm): P(any PASS)")
    for rho in (0.0, 0.15, 0.3):
        for n in (8, 12, 20):
            anyp = 0
            for _ in range(R):
                fam = smf_family([one_test(rng, n, 0.0, f"t{j}", sd_mean=sdm, rho=rho) for j in range(6)],
                                 alpha=ALPHA, min_units=MIN_STORMS)
                anyp += any(t.verdict == "PASS" for t in fam)
            lines.append(f"rho {rho:4.2f} storms {n:3d}: {anyp / R:.3f}")
    out = "\n".join(lines) + "\n"
    print(out, end="")
    with open("analysis/smf_v2_power_output.txt", "w") as f:
        f.write(out)


if __name__ == "__main__":
    main()
