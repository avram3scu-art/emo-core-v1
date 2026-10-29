"""Flood loop, option (b): news-pressure reduced form. Synthetic error rate and power.

Session 2.11d-ext, 29 Oct 2026. Class: infrastructure (synthetic data only; no flood
notification, pageview, discharge or activation record is read). Committed before its run.
Protocol: docs/FLOOD_LOOP_PROTOCOL.md §10.

Estimand: does competing news pressure NP on d0, d0+1 (in the country's language
Wikipedia, flood articles excluded) lower the chance of a CEMS activation Y?
NP is set by other news, so flood severity cannot cause it; the reduced form NP -> Y
needs no severity measure. Route (documented): competing news crowds out disaster
coverage and relief (news droughts / news floods; source in the protocol).

Data model (as §5/§8, plus NP):
  storm clusters (mean size 1.5) share a date, so they share a date component of NP;
  season k in 0..3 drawn with weights (0.3, 0.2, 0.2, 0.3);
  severity s = rho z + sqrt(1-rho^2) e + sev_season[k];
  NP = np_season[k] + sqrt(0.5) d_cluster + sqrt(0.5) e_i;
  A = lam s + kappa NP + u + beta_shock z;  Y ~ logit(off + g s + beta A_std + gam NP).
Statistic (registered): cluster-level, one-sided (NP lowers Y):
  x_c = mean NP of cluster c centred within season; r_c = sum of (Y - season mean Y) in c;
  T = -sum_c x_c r_c; p by permuting x across clusters within season, B = 999.
Clusters in real data: episodes whose d0 lie within 3 days of each other (any country).
Also shown (not registered): the same statistic at episode level.
"""

import numpy as np

RNG = np.random.default_rng(20261029 + 5)
REPS = 2000
B = 999
SEASON_W = np.array([0.3, 0.2, 0.2, 0.3])


def simulate(n, rng, lam=0.6, g=1.0, rho=0.6, beta_shock=0.0, base=0.3, beta=0.0,
             kappa=0.0, gam=0.0, season_conf=0.0):
    sizes = []
    while sum(sizes) < n:
        sizes.append(rng.geometric(1 / 1.5))
    k = len(sizes)
    cl = np.repeat(np.arange(k), sizes)[:n]
    season = rng.choice(4, size=k, p=SEASON_W)[cl]
    z = rng.normal(size=k)[cl]
    d = rng.normal(size=k)[cl]
    shift = season_conf * np.array([1.0, -0.5, -1.0, 0.5])
    sev = rho * z + np.sqrt(1 - rho**2) * rng.normal(size=n) + shift[season]
    npres = shift[season] + np.sqrt(0.5) * d + np.sqrt(0.5) * rng.normal(size=n)
    a = lam * sev + kappa * npres + rng.normal(size=n) + beta_shock * z
    a_std = (a - a.mean()) / a.std()
    lin = g * sev + beta * a_std + gam * npres
    off = np.log(base / (1 - base)) - np.log(np.mean(np.exp(lin)))
    y = (rng.random(n) < 1 / (1 + np.exp(-(off + lin)))).astype(float)
    return npres, y, season, cl


def _centre(v, s):
    out = v.astype(float).copy()
    for k in np.unique(s):
        m = s == k
        out[m] -= v[m].mean()
    return out


def cluster_p(npres, y, season, cl, rng, b=B):
    ids = np.unique(cl)
    cs = np.array([season[cl == c][0] for c in ids])
    yc = _centre(y, season)
    x = np.array([npres[cl == c].mean() for c in ids])
    x = _centre(x, cs)
    r = np.array([yc[cl == c].sum() for c in ids])
    t0 = -(x @ r)
    tp = np.zeros(b)
    for k in np.unique(cs):
        ix = np.flatnonzero(cs == k)
        perm = rng.random((b, len(ix))).argsort(axis=1)
        tp += -(x[ix][perm] @ r[ix])
    return (1 + np.sum(tp >= t0 - 1e-12)) / (1 + b)


def episode_p(npres, y, season, cl, rng, b=B):
    x = _centre(npres, season)
    yc = _centre(y, season)
    t0 = -(x @ yc)
    tp = np.zeros(b)
    for k in np.unique(season):
        ix = np.flatnonzero(season == k)
        perm = rng.random((b, len(ix))).argsort(axis=1)
        tp += -(x[ix][perm] @ yc[ix])
    return (1 + np.sum(tp >= t0 - 1e-12)) / (1 + b)


def rate(n, test, reps=REPS, **kw):
    hits = 0
    for _ in range(reps):
        npres, y, season, cl = simulate(n, RNG, **kw)
        if y.sum() < 2 or y.sum() > len(y) - 2:
            continue  # counted as no rejection
        hits += test(npres, y, season, cl, RNG) <= 0.05
    return hits / reps


SCEN = {
    "A independent of severity (lam 0, g 1)": dict(lam=0.0),
    "A and Y both rise with severity (lam 0.6, g 1)": dict(),
    "strong confounding (lam 1.0, g 2)": dict(lam=1.0, g=2.0),
    "storm shock on A (beta_shock 0.5)": dict(beta_shock=0.5),
    "season shifts severity and NP (strong confounding + season 1.0)": dict(lam=1.0, g=2.0, season_conf=1.0),
}
POWER = {
    "OR 2 per SD of A, kappa -0.3": dict(beta=0.7, kappa=-0.3),
    "OR 3 per SD of A, kappa -0.3": dict(beta=1.1, kappa=-0.3),
    "OR 3 per SD of A, kappa -0.6": dict(beta=1.1, kappa=-0.6),
    "direct NP effect on Y, OR 0.5 per SD NP": dict(gam=-0.7),
}
NS = [20, 30, 40, 45, 100]


def main():
    print(f"reps {REPS}, permutations {B}, alpha 0.05 one-sided, base 0.3; no A or M used")
    for name, test in [("cluster-level (REGISTERED)", cluster_p), ("episode-level (information)", episode_p)]:
        print(f"== {name}")
        print("Error rate (no NP effect, beta 0) under the §5/§8 scenarios (severity error irrelevant: no M):")
        for sname, kw in SCEN.items():
            print(f"  {sname}: " + "  ".join(f"N{n} {rate(n, test, **kw):.3f}" for n in NS))
        print("Power (lam 0.6, g 1):")
        for pname, kw in POWER.items():
            print(f"  {pname}: " + "  ".join(f"N{n} {rate(n, test, reps=1000, **kw):.3f}" for n in NS))


if __name__ == "__main__":
    main()
