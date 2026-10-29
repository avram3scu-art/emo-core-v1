"""Hurricane loop tests: synthetic false-positive rate and power (docs/LOOP_PROTOCOL.md §9).

Synthetic data only: this module reads no file and opens no loop record.
Run once; output recorded in analysis/loop_power_output.txt.
"""
import math
from itertools import product

import numpy as np
from scipy.stats import rankdata

SEED = 2026102923
REPS = 2000
PERMS = 999
ALPHA = 0.05
DELTA_EQ = 0.3
KAPPA = 0.5          # share of the season shock common to every link and outcome
SIG_SEASON = 0.7     # SD of season shocks
P_MISS = 0.10        # each predictor missing at random
Y_SHOCK_SIGN = 1.0   # sign of the season shock in the lags; -1 mimics coupling (§13); 1 = recorded run
SIZES_HU = (2, 4, 2, 2, 6, 2, 3, 1, 5)          # planning assumption, unverified
SIZES_HUTS = tuple(2 * s for s in SIZES_HU)
PRED = ("F", "W", "A")
OUT = ("Ystate", "Yfed")
PAIRS = tuple(product(PRED, OUT))
TRUE_PAIR = ("A", "Ystate")
LN_SD = 0.6
LN_MEAN = math.exp(LN_SD**2 / 2)
LN_STD = math.sqrt((math.exp(LN_SD**2) - 1) * math.exp(LN_SD**2))


def skew_noise(rng, n):
    return (np.exp(LN_SD * rng.normal(size=n)) - LN_MEAN) / LN_STD


def simulate(rng, sizes, r=0.0, delta=0.0, gamma_f=0.0, p_drop=0.0, pair=TRUE_PAIR, c=None):
    """One synthetic study: one row per storm. r: population partial (rank) correlation of the
    coupled pair given the controls (via coupling_coef); c overrides it with a raw coefficient.
    delta: total residual decline of both lags over the seasons (noise SD units).
    gamma_f: lags depend on F (forecast gains route, for the H5 null)."""
    sizes = np.asarray(sizes)
    K, n = len(sizes), int(sizes.sum())
    season = np.repeat(np.arange(K), sizes)
    yz = (season - (K - 1) / 2) / max(np.arange(K).std(), 1e-9)
    V = rng.normal(size=n) + 0.5 * yz
    R64 = 0.5 * V + math.sqrt(0.75) * rng.normal(size=n)
    region = rng.choice(3, size=n, p=(0.45, 0.35, 0.20))
    reg = np.array([0.3, 0.0, -0.3])[region]
    g = rng.normal(size=K)

    def shock():
        return SIG_SEASON * (math.sqrt(KAPPA) * g + math.sqrt(1 - KAPPA) * rng.normal(size=K))[season]

    quad = 0.3 * (V**2 - 1)
    q = rng.normal(size=n)
    e = {k: rng.normal(size=n) for k in PRED}
    idio = {"F": (0.5 * q + e["F"]) / math.sqrt(1.25), "W": (0.5 * q + e["W"]) / math.sqrt(1.25), "A": e["A"]}
    X = {
        "F": 0.2 * V + quad + reg + shock() + 0.4 * yz + 0.5 * q + e["F"],
        "W": 0.3 * V + quad + reg + shock() + 0.2 * yz + 0.5 * q + e["W"],
        "A": 0.8 * V + quad + reg + shock() - 0.2 * yz + e["A"],
    }
    zW = (X["W"] - X["W"].mean()) / X["W"].std()
    em = (rng.random(n) < 1 / (1 + np.exp(-(0.5 + V + zW)))).astype(float)
    zF = (X["F"] - X["F"].mean()) / X["F"].std()
    if c is None:
        c = coupling_coef(r)
    trend = -delta * season / max(K - 1, 1)
    Y = {}
    for k, base, em_eff in (("Ystate", 1.0, -0.6), ("Yfed", 3.0, -0.3)):
        y = -0.4 * V + quad + reg + Y_SHOCK_SIGN * shock() + em_eff * em - gamma_f * zF + trend + skew_noise(rng, n)
        if pair[1] == k:
            y = y - c * idio[pair[0]]
        Y[k] = np.round(base + 2 * y)
    Y["Yfed"] = np.maximum(Y["Yfed"], 0)
    for k in PRED:
        X[k] = np.where(rng.random(n) < P_MISS, np.nan, X[k])
    drop = rng.random(n) < p_drop
    for k in OUT:
        Y[k] = np.where(drop, np.nan, Y[k])
    return {"season": season, "yz": yz, "V": V, "R64": R64, "region": region, "EMpre": em, **X, **Y}


_COEF: dict = {}


def coupling_coef(r):
    """Raw coefficient whose population partial rank correlation (statistic of §5) equals r.
    Found once per r by bisection on one large synthetic sample (400 seasons of 50, fixed seed)."""
    if r == 0:
        return 0.0
    if r not in _COEF:
        lo, hi = 0.0, 5.0
        for _ in range(30):
            mid = (lo + hi) / 2
            d = simulate(np.random.default_rng(7), (50,) * 400, c=mid)
            m = ~np.isnan(d["A"]) & ~np.isnan(d["Ystate"])
            C = controls(d, m)
            rr = -corr_rows(resid(u(d["A"][m]), C), resid(u(d["Ystate"][m]), C))
            lo, hi = (mid, hi) if rr < r else (lo, mid)
        _COEF[r] = (lo + hi) / 2
    return _COEF[r]


def u(x):
    """Mid-rank / n."""
    return (rankdata(x) - 0.5) / len(x)


def ecdf_mid(train, x):
    """Mid-rank position of x in the training sample (equals u() on the sample itself)."""
    t = np.sort(train)
    return (np.searchsorted(t, x, "left") + np.searchsorted(t, x, "right")) / (2 * len(t))


def controls(d, m, year=True, em=True, extra=None):
    cols = [np.ones(m.sum()), d["V"][m], d["R64"][m], (d["region"][m] == 1) * 1.0, (d["region"][m] == 2) * 1.0]
    if em:
        cols.append(d["EMpre"][m])
    if year:
        cols.append(d["yz"][m])
    if extra is not None:
        cols.append(extra[m])
    return np.column_stack(cols)


def resid(y, C):
    beta = np.linalg.lstsq(C, y, rcond=None)[0]
    return y - C @ beta


def within_perm(season, B, rng):
    """(B, n) index arrays; element i only ever receives a value from its own season."""
    n = len(season)
    idx0 = np.argsort(season, kind="stable")
    order = np.argsort(season[None, :] + rng.random((B, n)), axis=1)
    perm = np.empty((B, n), dtype=int)
    perm[:, idx0] = order
    return perm


def corr_rows(a, b):
    a = a - a.mean(-1, keepdims=True)
    b = b - b.mean(-1, keepdims=True)
    return (a * b).sum(-1) / np.sqrt((a * a).sum(-1) * (b * b).sum(-1))


def h4_pair(d, x, y, rng, B=PERMS, naive=False, em=True):
    """Returns (one-sided p, r, n_within)."""
    m = ~np.isnan(d[x]) & ~np.isnan(d[y])
    s = d["season"][m]
    C = controls(d, m, em=em)
    rX, rY = resid(u(d[x][m]), C), resid(u(d[y][m]), C)
    r = corr_rows(rX, rY)
    if naive:
        perm = np.argsort(rng.random((B, len(rX))), axis=1)
    else:
        perm = within_perm(s, B, rng)
    null = -corr_rows(rX[perm], rY[None, :])
    p = (1 + (null >= -r - 1e-12).sum()) / (B + 1)
    n_within = int(sum(c - 1 for c in np.bincount(s) if c > 1))
    return p, r, n_within


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    adj = np.empty_like(p)
    run = 0.0
    for i, j in enumerate(o):
        run = max(run, (len(p) - i) * p[j])
        adj[j] = min(run, 1.0)
    return adj


def equivalent(r, n_within, k_within=5, delta=DELTA_EQ):
    n_eff = n_within - k_within
    if n_eff <= 3:
        return False
    z, se = math.atanh(max(min(r, 0.999999), -0.999999)), 1 / math.sqrt(n_eff - 3)
    lo, hi = math.tanh(z - 1.645 * se), math.tanh(z + 1.645 * se)
    return -delta < lo and hi < delta


def kendall_rows(t, v):
    """Kendall tau-a of t (fixed) against each row of v."""
    i, j = np.triu_indices(len(t), 1)
    st = np.sign(t[i] - t[j])
    return (np.sign(v[..., i] - v[..., j]) * st).sum(-1) / len(i)


def h5_outcome(d, y, rng, B=PERMS):
    m = ~np.isnan(d["F"]) & ~np.isnan(d[y])
    C = controls(d, m, year=False, extra=d["F"])
    res = resid(u(d[y][m]), C)
    s = d["season"][m]
    seasons = np.unique(s)
    means = np.array([res[s == k].mean() for k in seasons])
    S = -kendall_rows(seasons.astype(float), means[None, :])[0]
    perm = np.argsort(rng.random((B, len(means))), axis=1)
    null = -kendall_rows(seasons.astype(float), means[perm])
    return (1 + (null >= S - 1e-12).sum()) / (B + 1)


def blind_test(d_known, d_blind, rng, pair=TRUE_PAIR, B=PERMS):
    x, y = pair
    mk = ~np.isnan(d_known[x]) & ~np.isnan(d_known[y])
    mb = ~np.isnan(d_blind[x]) & ~np.isnan(d_blind[y])
    if mb.sum() < 2:
        return 1.0
    Ck, Cb = controls(d_known, mk), controls(d_blind, mb)
    ux_k, uy_k = u(d_known[x][mk]), u(d_known[y][mk])
    bx = np.linalg.lstsq(Ck, ux_k, rcond=None)[0]
    by = np.linalg.lstsq(Ck, uy_k, rcond=None)[0]
    rX = ecdf_mid(d_known[x][mk], d_blind[x][mb]) - Cb @ bx
    rY = ecdf_mid(d_known[y][mk], d_blind[y][mb]) - Cb @ by
    S = -(rX * rY).sum()
    perm = within_perm(d_blind["season"][mb], B, rng)
    null = -(rX[perm] * rY[None, :]).sum(-1)
    return (1 + (null >= S - 1e-12).sum()) / (B + 1)


def split(d, k_known):
    """Split a simulated study into its known seasons (index < k_known) and the rest."""
    a = d["season"] < k_known
    known = {k: v[a] for k, v in d.items()}
    blind = {k: v[~a] for k, v in d.items()}
    blind["season"] = blind["season"] - k_known
    return known, blind


def h4_cell(rng, sizes, r, p_drop=0.0, reps=REPS, naive=False, em=True):
    any_rej = true_rej = eq0 = 0
    for _ in range(reps):
        d = simulate(rng, sizes, r=r, p_drop=p_drop)
        res = [h4_pair(d, x, y, rng, naive=naive, em=em) for x, y in PAIRS]
        adj = holm([p for p, _, _ in res])
        any_rej += adj.min() < ALPHA
        true_rej += adj[PAIRS.index(TRUE_PAIR)] < ALPHA
        _, rr, nw = res[PAIRS.index(TRUE_PAIR)]
        eq0 += equivalent(rr, nw)
    return any_rej / reps, true_rej / reps, eq0 / reps


def h5_cell(rng, sizes, delta, reps=REPS):
    rej = 0
    for _ in range(reps):
        d = simulate(rng, sizes, delta=delta, gamma_f=0.4)
        adj = holm([h5_outcome(d, y, rng) for y in OUT])
        rej += adj.min() < ALPHA
    return rej / reps


def blind_cell(rng, blind_sizes, r, reps=REPS):
    rej = 0
    k = len(SIZES_HU)
    for _ in range(reps):
        d = simulate(rng, SIZES_HU + tuple(blind_sizes), r=r)
        known, blind = split(d, k)
        rej += blind_test(known, blind, rng) < ALPHA
    return rej / reps


def main():
    rng = np.random.default_rng(SEED)
    coefs = {r: coupling_coef(r) for r in (0.3, 0.5)}
    print("Hurricane loop power (docs/LOOP_PROTOCOL.md §9). Synthetic data only; no loop record read.")
    print(f"seed {SEED}, {REPS} studies/cell, {PERMS} permutations; MC SE of a 5% rate "
          f"{math.sqrt(0.05 * 0.95 / REPS):.4f}")
    print("coupling coefficient for population partial r: "
          + ", ".join(f"r={r}: c={c:.3f}" for r, c in coefs.items()))
    print(f"sizes HU {SIZES_HU} (n={sum(SIZES_HU)}), HU+TS {SIZES_HUTS} (n={sum(SIZES_HUTS)})\n")

    print("H4 (6 pairs, Holm): family-wise rejection | true pair rejected | 'no effect' read on true pair")
    designs = (("HU", SIZES_HU, 0.0), ("HU 25% unmatched", SIZES_HU, 0.25), ("HU+TS", SIZES_HUTS, 0.0))
    for name, sizes, p_drop in designs:
        for r in (0.0, 0.3, 0.5):
            a, t, e = h4_cell(rng, sizes, r, p_drop)
            print(f"  {name:17s} r={r:.1f} within-season: any {a:.3f} | true {t:.3f} | no-effect {e:.3f}", flush=True)
    for name, sizes, p_drop in (designs[0], designs[2]):
        a, _, _ = h4_cell(rng, sizes, 0.0, p_drop, naive=True)
        print(f"  {name:17s} r=0.0 naive null:    any {a:.3f}", flush=True)
        a, _, _ = h4_cell(rng, sizes, 0.0, p_drop, em=False)
        print(f"  {name:17s} r=0.0 EMpre dropped: any {a:.3f}", flush=True)

    print("\nH5 (2 outcomes, Holm; severity-mix and forecast-gain trends present): rejection rate")
    for name, sizes in (("HU", SIZES_HU), ("HU+TS", SIZES_HUTS)):
        for delta in (0.0, 1.0, 2.0):
            print(f"  {name:6s} seasons={len(sizes)} delta={delta:.1f}: {h5_cell(rng, sizes, delta):.3f}", flush=True)

    print("\nBlind arm (one pair, frozen HU fit): rejection rate")
    for bs in ((4,), (6,), (4, 4, 4), (4, 4, 4, 4, 4)):
        for r in (0.0, 0.5):
            print(f"  blind sizes {str(bs):16s} r={r:.1f}: {blind_cell(rng, bs, r):.3f}", flush=True)


if __name__ == "__main__":
    main()
