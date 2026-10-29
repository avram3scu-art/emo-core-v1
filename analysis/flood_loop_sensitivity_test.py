"""Flood-loop sensitivity test (F13 repair): synthetic error rates and power.

Session 2.11d, 29 Oct 2026. Class: infrastructure (synthetic data only; no flood
notification, pageview, discharge or activation record is read). Committed before its run.
Protocol: docs/FLOOD_LOOP_PROTOCOL.md §9.

Estimand changed. The 2.11b/2.11c tests asked "is A associated with Y beyond measured
severity M?", whose null needs M to be exact. This test asks: "how large would the
unmeasured part of severity have to be to explain the observed A-Y association?"
The unmeasured part is parameterised as in §8: M = s + e*N(0,1), e in SD of true
severity s (reliability R = 1 / (1 + e^2) after M is standardised). Only e is assumed;
the loadings of severity on A (lam) and on Y (g) are estimated from the data at each e.

Statistic: T = rA . rY, the partial covariance of A and Y after OLS on [1, M, M^2].
Null at a given e (parametric bootstrap, H0: A and Y independent given true s):
  M standardised; R = 1/(1+e^2); s | M ~ N(R M, R(1-R)).
  A: slope b of A on M -> lam = b / R; noise var = resid var - lam^2 R(1-R) (floor 5%).
  Y: probit of Y on M, slope k1, intercept k0 -> true probit slope
     g = k1 / sqrt(R^2 - k1^2 R(1-R)) (capped at 10 when the root is not real),
     intercept c = k0 * sqrt(1 + g^2 R(1-R)).
  B draws of (s, A, Y) from that model given the observed M; T recomputed on each.
  p(e) = (1 + #{T_b >= T0}) / (1 + B), one-sided.
Reported: e* = largest e on the grid 0, 0.1, ..., 2.0 with p(e) <= 0.05 (e* = none if
p(0) > 0.05). Decision (fixed now): PASS iff p(E0) <= 0.05, E0 = 0.6, i.e. the
association survives a hidden severity error of 0.6 SD (the largest §8 scenario).
"""

import numpy as np
from scipy.stats import norm

E0 = 0.6
GRID = np.round(np.arange(0.0, 2.01, 0.1), 2)
B = 499
REPS = 2000
RNG = np.random.default_rng(20261029 + 4)


# ---------- data model: identical to analysis/flood_loop_severity_test.py (§8) ----------
def simulate(n, beta, rng, lam=0.6, g=1.0, rho=0.6, beta_shock=0.0, base=0.3, err=0.3):
    sizes = []
    while sum(sizes) < n:
        sizes.append(rng.geometric(1 / 1.5))
    cl = np.repeat(np.arange(len(sizes)), sizes)[:n]
    z = rng.normal(size=len(sizes))[cl]
    sev = rho * z + np.sqrt(1 - rho**2) * rng.normal(size=n)
    a = lam * sev + rng.normal(size=n) + beta_shock * z
    a_std = (a - a.mean()) / a.std()
    lin = g * sev + beta * a_std
    off = np.log(base / (1 - base)) - np.log(np.mean(np.exp(lin)))
    y = (rng.random(n) < 1 / (1 + np.exp(-(off + lin)))).astype(float)
    m = sev + err * rng.normal(size=n)
    keep = rng.random(n) >= 0.2
    return a[keep], y[keep], m[keep]


# ---------- the test (this is the registered procedure) ----------
def _resid_maker(m):
    x = np.column_stack([np.ones_like(m), m, m**2])
    q, _ = np.linalg.qr(x)
    return lambda v: v - (v @ q) @ q.T if v.ndim == 2 else v - q @ (q.T @ v)


def probit_fit(m, y, iters=50):
    """Fisher scoring for P(Y=1) = Phi(k0 + k1 m), small ridge against separation."""
    x = np.column_stack([np.ones_like(m), m])
    w = np.zeros(2)
    for _ in range(iters):
        eta = np.clip(x @ w, -8, 8)
        p = np.clip(norm.cdf(eta), 1e-9, 1 - 1e-9)
        d = norm.pdf(eta)
        score = x.T @ ((y - p) * d / (p * (1 - p))) - 1e-3 * w
        info = x.T @ (x * (d**2 / (p * (1 - p)))[:, None]) + 1e-3 * np.eye(2)
        step = np.linalg.solve(info, score)
        w += step
        if np.abs(step).max() < 1e-9:
            break
    return w


def null_pvalue(a, y, m, e, rng, b=B):
    """One-sided p of T = rA.rY against the null with hidden severity error e (SD)."""
    m = (m - m.mean()) / m.std()
    res = _resid_maker(m)
    t0 = res(a) @ res(y)
    r = 1.0 / (1.0 + e**2)
    v = r * (1 - r)
    bA = np.polyfit(m, a, 1)
    lam = bA[0] / r
    rv = np.var(a - np.polyval(bA, m))
    su2 = max(rv - lam**2 * v, 0.05 * rv)
    k0, k1 = probit_fit(m, y)
    den = r**2 - k1**2 * v
    g = 10.0 if den <= 0 else min(abs(k1) / np.sqrt(den), 10.0) * np.sign(k1)
    c = k0 * np.sqrt(1 + g**2 * v)
    n = len(m)
    s = r * m + np.sqrt(v) * rng.normal(size=(b, n))
    ab = lam * s + np.sqrt(su2) * rng.normal(size=(b, n))
    yb = (c + g * s + rng.normal(size=(b, n)) > 0).astype(float)
    tb = np.sum(res(ab) * res(yb), axis=1)
    return (1 + np.sum(tb >= t0 - 1e-12)) / (1 + b)


def e_star(a, y, m, rng, grid=GRID, b=B):
    """Largest grid e at which the association is still significant; None if not at e = 0."""
    best = None
    for e in grid:
        if null_pvalue(a, y, m, e, rng, b) <= 0.05:
            best = float(e)
        else:
            break
    return best


# ---------- synthetic checks ----------
def rate(n, beta, e0, reps=REPS, **kw):
    hits = 0
    for _ in range(reps):
        a, y, m = simulate(n, beta, RNG, **kw)
        if y.sum() < 2 or y.sum() > len(y) - 2:
            continue  # counted as no rejection
        hits += null_pvalue(a, y, m, e0, RNG) <= 0.05
    return hits / reps


SCEN = {
    "A independent of severity (lam 0, g 1)": dict(lam=0.0),
    "A and Y both rise with severity (lam 0.6, g 1)": dict(),
    "strong confounding (lam 1.0, g 2)": dict(lam=1.0, g=2.0),
    "storm shock on A (beta_shock 0.5)": dict(beta_shock=0.5),
}
NS = [20, 30, 40, 45, 100]


def main():
    print(f"reps {REPS}, null draws {B}, alpha 0.05 one-sided, 20% of A missing, base 0.3")
    for e0 in [E0, 0.3]:
        tag = "REGISTERED decision" if e0 == E0 else "information only"
        print(f"== decision at assumed hidden error e0 = {e0} ({tag})")
        print("Error rate (beta 0) by true severity error:")
        for err in [0.0, 0.3, 0.6]:
            for name, kw in SCEN.items():
                print(f"  err {err} | {name}: " + "  ".join(
                    f"N{n} {rate(n, 0.0, e0, err=err, **kw):.3f}" for n in NS))
        print("Power (lam 0.6, g 1, true error 0.3), rows = OR per SD of A:")
        for beta in [0.4, 0.7, 1.1]:
            print(f"  OR {np.exp(beta):.1f}: " + "  ".join(
                f"N{n} {rate(n, beta, e0, reps=1000):.3f}" for n in NS))


if __name__ == "__main__":
    main()
