"""Synthetic false-positive rate and power for the flood-loop test (docs/FLOOD_LOOP_PROTOCOL.md).

Session 2.11b, 29 Oct 2026. Class: infrastructure (synthetic data only; no flood,
notification, pageview or activation record is read). Committed before its run.

Model per episode i (one EU country, one run of EFAS formal notifications):
  storm shock z_c ~ N(0,1), shared by episodes of one storm cluster (mean size 1.5);
  severity s_i = rho*z_c + sqrt(1-rho^2)*e_i;
  notifications n_i = 1 + Poisson(exp(0.2 + 0.6 s_i))  -> strata 1 / 2-3 / >=4;
  attention A_i = lam*s_i + u_i + beta_shock*z_c, missing with prob 0.2;
  activation Y_i ~ Bernoulli(logit^-1(a + g*s_i + beta*A_std_i)), a set for a 0.3 base rate.
Statistic (protocol §5): within-stratum centred rank sum of A over activated episodes,
one-sided permutation p (Y shuffled within strata), alpha 0.05.
"""

import numpy as np

RNG = np.random.default_rng(20261029)
REPS = 1000
B = 999


def stratum(n):
    return np.where(n == 1, 0, np.where(n <= 3, 1, 2))


def centred_ranks(a, s):
    """Within-stratum rank of A, centred and scaled to (-0.5, 0.5)."""
    c = np.zeros(len(a))
    for k in np.unique(s):
        m = s == k
        r = a[m].argsort().argsort() + 1.0
        c[m] = (r - (m.sum() + 1) / 2) / m.sum()
    return c


def perm_p(a, y, s, rng, b=B):
    """One-sided p: T = sum of centred ranks over activated episodes; Y shuffled within strata."""
    c = centred_ranks(a, s)
    t0 = c @ y
    tp = np.zeros(b)
    for k in np.unique(s):
        ix = np.flatnonzero(s == k)
        perm = rng.random((b, len(ix))).argsort(axis=1)
        tp += (c[ix][perm] * y[ix]).sum(axis=1)
    return (1 + np.sum(tp >= t0 - 1e-12)) / (1 + b)


def simulate(n, beta, rng, lam=0.6, g=1.0, rho=0.6, beta_shock=0.0, base=0.3):
    sizes = []
    while sum(sizes) < n:
        sizes.append(rng.geometric(1 / 1.5))
    cl = np.repeat(np.arange(len(sizes)), sizes)[:n]
    z = rng.normal(size=len(sizes))[cl]
    sev = rho * z + np.sqrt(1 - rho**2) * rng.normal(size=n)
    notes = 1 + rng.poisson(np.exp(0.2 + 0.6 * sev))
    a = lam * sev + rng.normal(size=n) + beta_shock * z
    a_std = (a - a.mean()) / a.std()
    lin = g * sev + beta * a_std
    off = np.log(base / (1 - base)) - np.log(np.mean(np.exp(lin)))
    y = (rng.random(n) < 1 / (1 + np.exp(-(off + lin)))).astype(int)
    keep = rng.random(n) >= 0.2
    return a[keep], y[keep], stratum(notes[keep])


def rate(n, beta, **kw):
    hits = 0
    for _ in range(REPS):
        a, y, s = simulate(n, beta, RNG, **kw)
        if y.sum() == 0 or y.sum() == len(y):
            continue
        hits += perm_p(a, y, s, RNG) <= 0.05
    return hits / REPS


def main():
    print(f"reps {REPS}, permutations {B}, alpha 0.05 one-sided, 20% of A missing, base activation 0.3")
    print("FPR (beta = 0): rows = scenario, columns = episodes N")
    ns = [20, 30, 40, 100]
    scen = {
        "A independent of severity (lam 0, g 1)": dict(lam=0.0),
        "A and Y both rise with severity (lam 0.6, g 1)": dict(),
        "strong confounding (lam 1.0, g 2)": dict(lam=1.0, g=2.0),
        "plus storm shock on A (beta_shock 0.5)": dict(beta_shock=0.5),
    }
    for name, kw in scen.items():
        print(f"  {name}: " + "  ".join(f"N{n} {rate(n, 0.0, **kw):.3f}" for n in ns))
    print("Power (lam 0.6, g 1): rows = beta per SD of A, i.e. log odds ratio")
    for beta in [0.4, 0.7, 1.1]:
        print(f"  beta {beta} (OR {np.exp(beta):.1f}): " + "  ".join(f"N{n} {rate(n, beta):.3f}" for n in ns))


if __name__ == "__main__":
    main()
