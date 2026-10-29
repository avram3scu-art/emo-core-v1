"""Severity-adjusted flood-loop test: synthetic FPR and power (docs/FLOOD_LOOP_PROTOCOL.md §8).

Session 2.11c, 29 Oct 2026. Class: infrastructure (synthetic data only; no flood
notification, pageview, discharge or activation record is read). Committed before its run.

Data model: the same as analysis/flood_loop_power.py (2.11b, §5), plus a measured
severity M = s + err * N(0,1) standing for the Gumbel reduced variate of simulated
discharge (protocol §7); err is the part of true severity (impact) that discharge misses.

Statistic (Freedman-Lane style, continuous adjustment):
  rA = residual of A from OLS on [1, M, M^2];
  eY = Y - p(M), p from logistic regression of Y on [1, M] (IRLS);
  T  = sum(rA * eY). One-sided permutation p: rA permuted across episodes, B = 999.
Variant "+n": both adjustments also include ln(n) (notification count) as a second proxy.
"""

import sys

import numpy as np

RNG = np.random.default_rng(20261029 + 3)
REPS = 2000
B = 999


def simulate(n, beta, rng, lam=0.6, g=1.0, rho=0.6, beta_shock=0.0, base=0.3, err=0.3):
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
    y = (rng.random(n) < 1 / (1 + np.exp(-(off + lin)))).astype(float)
    m = sev + err * rng.normal(size=n)
    keep = rng.random(n) >= 0.2
    return a[keep], y[keep], m[keep], np.log(notes[keep])


def logit_fit(x, y, iters=25):
    """IRLS with a small ridge so separation cannot blow up; returns fitted p."""
    w = np.zeros(x.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(x @ w, -30, 30)))
        h = x.T @ (x * (p * (1 - p))[:, None]) + 1e-3 * np.eye(x.shape[1])
        step = np.linalg.solve(h, x.T @ (y - p) - 1e-3 * w)
        w += step
        if np.abs(step).max() < 1e-8:
            break
    return 1 / (1 + np.exp(-np.clip(x @ w, -30, 30)))


def test_p(a, y, m, ln_n=None, rng=RNG, b=B):
    one = np.ones_like(m)
    xa = np.column_stack([one, m, m**2] + ([ln_n] if ln_n is not None else []))
    xy = np.column_stack([one, m] + ([ln_n] if ln_n is not None else []))
    ra = a - xa @ np.linalg.lstsq(xa, a, rcond=None)[0]
    ey = y - logit_fit(xy, y)
    t0 = ra @ ey
    perm = rng.random((b, len(a))).argsort(axis=1)
    tp = ra[perm] @ ey
    return (1 + np.sum(tp >= t0 - 1e-12)) / (1 + b)


def rate(n, beta, use_n=False, reps=REPS, **kw):
    hits = 0
    for _ in range(reps):
        a, y, m, ln_n = simulate(n, beta, RNG, **kw)
        if y.sum() < 2 or y.sum() > len(y) - 2:
            continue  # counted as no rejection
        hits += test_p(a, y, m, ln_n if use_n else None) <= 0.05
    return hits / reps


SCEN = {
    "A independent of severity (lam 0, g 1)": dict(lam=0.0),
    "A and Y both rise with severity (lam 0.6, g 1)": dict(),
    "strong confounding (lam 1.0, g 2)": dict(lam=1.0, g=2.0),
    "storm shock on A (beta_shock 0.5)": dict(beta_shock=0.5),
}
NS = [20, 30, 40, 45, 100]


def main():
    use_n = "--with-n" in sys.argv
    tag = "adjust M, M^2 and ln(n)" if use_n else "adjust M, M^2"
    print(f"{tag}; reps {REPS}, permutations {B}, alpha 0.05 one-sided, 20% of A missing, base 0.3")
    for err in [0.0, 0.3, 0.6]:
        print(f"FPR (beta 0), severity measurement error {err} SD")
        for name, kw in SCEN.items():
            print(f"  {name}: " + "  ".join(
                f"N{n} {rate(n, 0.0, use_n, err=err, **kw):.3f}" for n in NS))
    print("Power (lam 0.6, g 1, error 0.3): rows = log odds ratio per SD of A")
    for beta in [0.4, 0.7, 1.1]:
        print(f"  beta {beta} (OR {np.exp(beta):.1f}): " + "  ".join(
            f"N{n} {rate(n, beta, use_n, reps=1000):.3f}" for n in NS))


if __name__ == "__main__":
    main()
