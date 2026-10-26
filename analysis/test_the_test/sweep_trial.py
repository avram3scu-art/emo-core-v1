"""
THE SCIENCE OF TRUTH - Section 9 robustness sweep.

Vectorised Monte Carlo of a classroom-randomised trial. Each scenario
departs from the Section 6 baseline in one respect (Section 9, A-K).
Four analyses are applied to every simulated trial:

  primary : OLS on classroom means, adjusted for baseline mean (Sec. 7)
  RI      : randomisation inference on baseline-adjusted classroom
            residuals, permuting at the unit actually randomised
  naive   : student-level OLS ignoring clustering (shown as a warning)
  CR      : student-level OLS, classroom cluster-robust SE (CR1, df G-1)

Effects are in SD units of the true (error-free) score. "target" is the
intention-to-treat effect the design actually delivers (it differs from
tau under partial fidelity or contamination).
"""
import csv
import numpy as np
from scipy.stats import t as tdist

R = 2000          # simulated trials per cell
P = 500           # permutations for RI
SEED = 20261026


def assign(rng, n_rep, G, k):
    """Balanced randomisation of G//k teachers (k classes each)."""
    nt = G // k
    order = np.argsort(rng.random((n_rep, nt)), axis=1)
    Tt = np.zeros((n_rep, nt))
    np.put_along_axis(Tt, order[:, : nt // 2], 1.0, axis=1)
    return np.repeat(Tt, k, axis=1)


def draw(rng, shape, heavy):
    if heavy:  # Student t(3) scaled to unit variance
        return rng.standard_t(3, size=shape) / np.sqrt(3.0)
    return rng.normal(size=shape)


def run_cell(rng, tau, G=80, n=20, size_sd=0, icc=0.10, rho=0.60, k=1,
             teacher_var=0.0, tau_sd=0.0, fidelity=1.0, contam=0.0,
             rel=1.0, att_rate=0.0, att_mech="random", heavy=False,
             teacher_level=False):
    T = assign(rng, R, G, k)

    if size_sd > 0:
        sizes = np.clip(np.rint(rng.normal(n, size_sd, (R, G))), 8, 32)
        M = 32
    else:
        sizes = np.full((R, G), n)
        M = n
    enrolled = np.arange(M)[None, None, :] < sizes[..., None]

    y0 = (np.sqrt(icc) * draw(rng, (R, G), heavy)[..., None]
          + np.sqrt(1 - icc) * draw(rng, (R, G, M), heavy))
    noise = (np.sqrt(icc) * draw(rng, (R, G), heavy)[..., None]
             + np.sqrt(1 - icc) * draw(rng, (R, G, M), heavy))
    te = np.repeat(rng.normal(size=(R, G // k)), k, axis=1)

    fid = rng.random((R, G)) < fidelity
    con = rng.random((R, G)) < contam
    tau_j = (tau * (T * fid + (1 - T) * con * 0.5)
             + tau_sd * rng.normal(size=(R, G)) * T)
    target = tau * (fidelity - 0.5 * contam)

    y1 = (rho * y0 + np.sqrt(1 - rho**2) * noise
          + np.sqrt(teacher_var) * te[..., None] + tau_j[..., None])

    # Measurement error (reliability rel on the unit-variance scale)
    if rel < 1:
        s = np.sqrt((1 - rel) / rel)
        y0o = y0 + s * rng.normal(size=y0.shape)
        y1o = y1 + s * rng.normal(size=y1.shape)
    else:
        y0o, y1o = y0, y1

    # Attrition
    obs = enrolled.copy()
    if att_rate > 0:
        if att_mech == "random":
            z = np.zeros_like(y0)
        elif att_mech == "baseline":      # low-baseline students leave
            z = -y0
        elif att_mech == "differential":  # low-outcome TREATED students leave
            z = -y1 * T[..., None]
        score = 1.5 * z + rng.logistic(size=y0.shape)
        score = np.where(enrolled, score, -np.inf).reshape(R, -1)
        kdrop = np.rint(att_rate * enrolled.sum((1, 2))).astype(int)
        ranks = np.argsort(np.argsort(-score, axis=1), axis=1)
        obs = enrolled & ~(ranks < kdrop[:, None]).reshape(R, G, M)

    w = obs.astype(float)
    nj = np.maximum(w.sum(2), 1)
    yb1 = (y1o * w).sum(2) / nj
    yb0 = (y0o * w).sum(2) / nj

    # --- primary: classroom-means OLS (or teacher-means if teacher_level)
    Gc = G
    if teacher_level and k > 1:
        Gc = G // k
        yb1 = yb1.reshape(R, Gc, k).mean(2)
        yb0 = yb0.reshape(R, Gc, k).mean(2)
        T_p = T[:, ::k]
    else:
        T_p = T
    X = np.stack([np.ones((R, Gc)), T_p, yb0], axis=2)
    XtX = np.einsum("rgi,rgj->rij", X, X)
    iXtX = np.linalg.inv(XtX)
    b = np.einsum("rij,rj->ri", iXtX, np.einsum("rgi,rg->ri", X, yb1))
    res = yb1 - np.einsum("rgi,ri->rg", X, b)
    df = Gc - 3
    se = np.sqrt((res**2).sum(1) / df * iXtX[:, 1, 1])
    p_prim = 2 * tdist.sf(np.abs(b[:, 1] / se), df)
    crit = tdist.ppf(0.975, df)
    cover = np.abs(b[:, 1] - target) <= crit * se

    # --- RI on baseline-adjusted residuals, permuting the randomised unit
    Z = np.stack([np.ones((R, Gc)), yb0], axis=2)
    g = np.linalg.solve(np.einsum("rgi,rgj->rij", Z, Z),
                        np.einsum("rgi,rg->ri", Z, yb1)[..., None])[..., 0]
    r = yb1 - np.einsum("rgi,ri->rg", Z, g)
    h = Gc / 2
    obs_stat = (r * (T_p / h - (1 - T_p) / h)).sum(1)
    Tp = assign(rng, P, Gc, 1 if Gc != G else k)
    perm = r @ (Tp / h - (1 - Tp) / h).T
    p_ri = (1 + (np.abs(perm) >= np.abs(obs_stat)[:, None] - 1e-12).sum(1)) / (P + 1)

    # --- student-level OLS: naive and cluster-robust
    Xi = np.stack([np.ones_like(y0o), np.broadcast_to(T[..., None], y0o.shape), y0o], axis=3)
    A = np.einsum("rgmi,rgmj,rgm->rij", Xi, Xi, w)
    iA = np.linalg.inv(A)
    bi = np.einsum("rij,rj->ri", iA, np.einsum("rgmi,rgm->ri", Xi, y1o * w))
    e = (y1o - np.einsum("rgmi,ri->rgm", Xi, bi)) * w
    N = w.sum((1, 2))
    se_n = np.sqrt((e**2).sum((1, 2)) / (N - 3) * iA[:, 1, 1])
    p_naive = 2 * tdist.sf(np.abs(bi[:, 1] / se_n), N - 3)
    sc = np.einsum("rgmi,rgm->rgi", Xi, e)
    meat = np.einsum("rgi,rgj->rij", sc, sc)
    V = iA @ meat @ iA * (G / (G - 1)) * ((N - 1) / (N - 3))[:, None, None]
    p_cr = 2 * tdist.sf(np.abs(bi[:, 1] / np.sqrt(V[:, 1, 1])), G - 1)

    return dict(
        target=target,
        primary=(p_prim < .05).mean(), RI=(p_ri < .05).mean(),
        naive=(p_naive < .05).mean(), CR=(p_cr < .05).mean(),
        est=b[:, 1].mean(), bias=b[:, 1].mean() - target,
        coverage=cover.mean(),
    )


SCENARIOS = [
    ("A/B baseline (Sec. 6)", {}, (0.0, 0.1, 0.2, 0.3)),
    ("C ICC=0.05", dict(icc=0.05), (0.0, 0.2)),
    ("C ICC=0.20", dict(icc=0.20), (0.0, 0.2)),
    ("D rho=0.40", dict(rho=0.40), (0.0, 0.2)),
    ("D rho=0.80", dict(rho=0.80), (0.0, 0.2)),
    ("E attrition 5% random", dict(att_rate=.05), (0.0, 0.2)),
    ("E attrition 15% random", dict(att_rate=.15), (0.0, 0.2)),
    ("E attrition 25% random", dict(att_rate=.25), (0.0, 0.2)),
    ("E attrition 25% baseline-related", dict(att_rate=.25, att_mech="baseline"), (0.0, 0.2)),
    ("E attrition 15% differential", dict(att_rate=.15, att_mech="differential"), (0.0, 0.2)),
    ("E attrition 25% differential", dict(att_rate=.25, att_mech="differential"), (0.0, 0.2)),
    ("F unequal sizes (SD 6, 8-32)", dict(size_sd=6), (0.0, 0.2)),
    ("G teacher var .05, 2 classes/teacher", dict(k=2, teacher_var=.05), (0.0, 0.2)),
    ("G effect heterogeneity SD .10", dict(tau_sd=.10), (0.0, 0.2)),
    ("H fidelity 75%", dict(fidelity=.75), (0.2,)),
    ("H fidelity 50%", dict(fidelity=.50), (0.2,)),
    ("I contamination 20%", dict(contam=.20), (0.2,)),
    ("I contamination 40%", dict(contam=.40), (0.2,)),
    ("J reliability 0.80", dict(rel=.80), (0.0, 0.2)),
    ("J reliability 0.60", dict(rel=.60), (0.0, 0.2)),
    ("K heavy tails t(3)", dict(heavy=True), (0.0, 0.2)),
    ("K only 20 classrooms", dict(G=20), (0.0, 0.2)),
]


def main():
    rng = np.random.default_rng(SEED)
    rows = []
    hdr = f"{'scenario':40s} {'tau':>4s} {'tgt':>5s} {'prim':>6s} {'RI':>6s} {'naive':>6s} {'CR':>6s} {'bias':>7s} {'cover':>6s}"
    print(hdr)
    print("-" * len(hdr))
    for name, kw, taus in SCENARIOS:
        for tau in taus:
            out = run_cell(rng, tau, **kw)
            rows.append(dict(scenario=name, tau=tau, **out))
            print(f"{name:40s} {tau:4.2f} {out['target']:5.2f} "
                  f"{out['primary']:6.3f} {out['RI']:6.3f} {out['naive']:6.3f} "
                  f"{out['CR']:6.3f} {out['bias']:+7.3f} {out['coverage']:6.3f}",
                  flush=True)
    with open("sweep_results.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    print(f"\nR={R} trials/cell, P={P} permutations, seed={SEED}. "
          f"MC SE of a 5% rate = {np.sqrt(.05*.95/R):.4f}")


if __name__ == "__main__":
    main()
