"""GWI v2: coincident attention excursions with a causal, per-stream seasonal baseline.

Repair of GWI v1.1 (`emo/gwi.py`, kept unchanged) for audit defects D2-D4
(`docs/AUDIT_2026-10-29.md`); protocol `docs/GWI_V2_PROTOCOL.md`.

- D2 (look-ahead): every quantity for day t uses days before t only.
- D4 (calendar drivers, serial correlation): baseline = same-weekday level of the
  last 8 weeks + the seasonal miss of that baseline at the same time of year in
  earlier years (364-day lags, so weekdays line up); event tests use a
  block-permutation null that keeps each series' serial dependence.
- D3 (pooled rate): per-stream excursion rates, Poisson-binomial tail for the
  number of streams in excursion together.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd

Z_THRESHOLD = 2.0
N_WEEKS = 8
MAX_YEARS = 3
MIN_YEARS = 2
SEASON_HALF = 3
SCALE_DAYS = 365
MIN_SCALE = 180
MAD_K = 1.4826


def _shift(a: np.ndarray, k: int) -> np.ndarray:
    """Rows moved down by k (row t holds row t-k); first k rows NaN."""
    out = np.full_like(a, np.nan)
    if k < len(a):
        out[k:] = a[: len(a) - k]
    return out


def causal_z(y: pd.DataFrame) -> pd.DataFrame:
    """Causal robust z-scores of y (log views; daily, gap-free index; one column per stream).

    b_t = L_t + S_t, with L_t = median of y over t-7k (k = 1..8) and
    S_t = median over earlier years j = 1..3 (at least 2) of the median of
    (y - L) over days t-364j-3 .. t-364j+3. Residual r = y - b; z = (r - m) / s
    with m, s = median and 1.4826 * MAD of r over days t-365 .. t-1 (at least 180).
    Days without enough history are NaN.
    """
    idx = y.index
    if len(idx) > 1 and not (pd.Series(idx).diff().dropna() == pd.Timedelta(days=1)).all():
        raise ValueError("y must have a gap-free daily index")
    Y = y.to_numpy(dtype=float)
    lags = np.stack([_shift(Y, 7 * k) for k in range(1, N_WEEKS + 1)])
    L = np.median(lags, axis=0)  # NaN unless all 8 weeks exist
    R0 = Y - L
    per_year = []
    for j in range(1, MAX_YEARS + 1):
        win = np.stack([_shift(R0, 364 * j + d) for d in range(-SEASON_HALF, SEASON_HALF + 1)])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            per_year.append(np.nanmedian(win, axis=0))
    py = np.stack(per_year)
    n_years = np.isfinite(py).sum(axis=0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        S = np.nanmedian(py, axis=0)
    S[n_years < MIN_YEARS] = np.nan
    r = R0 - S
    z = np.full_like(r, np.nan)
    for t in range(len(r)):
        lo = max(0, t - SCALE_DAYS)
        w = r[lo:t]
        ok = np.isfinite(w).sum(axis=0)
        if w.shape[0] == 0:
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            m = np.nanmedian(w, axis=0)
            s = MAD_K * np.nanmedian(np.abs(w - m), axis=0)
        good = (ok >= MIN_SCALE) & (s > 0) & np.isfinite(r[t])
        z[t, good] = (r[t, good] - m[good]) / s[good]
    return pd.DataFrame(z, index=idx, columns=y.columns)


def poisson_binomial_sf(p: np.ndarray, k: int) -> float:
    """P(K >= k) for K = sum of independent Bernoulli(p_i)."""
    p = np.asarray(p, dtype=float)
    if k <= 0:
        return 1.0
    if k > len(p):
        return 0.0
    dist = np.zeros(len(p) + 1)
    dist[0] = 1.0
    for pi in p:
        dist[1:] = dist[1:] * (1 - pi) + dist[:-1] * pi
        dist[0] *= 1 - pi
    return float(min(1.0, dist[k:].sum()))


@dataclass
class GWI2Result:
    z: pd.DataFrame
    excursion: pd.DataFrame
    count: pd.Series
    tail_p: pd.Series
    ignition: pd.Series  # bool; NaN-free; False on days that cannot be scored
    scored: pd.Series  # bool: day had enough history in at least MIN_STREAMS streams


def compute_gwi_v2(views: pd.DataFrame, alpha_day: float, min_streams: int = 8) -> GWI2Result:
    """Ignition days of one article from daily views (columns = language streams).

    A stream is in excursion on day t when its causal z > 2. Its excursion rate
    p_i,t = (excursions + 0.5) / (scored days + 1) over days t-365 .. t-1. With K_t
    streams in excursion, the tail P_t = P(PoissonBinomial(p_.,t) >= K_t); day t
    ignites when P_t < alpha_day. A day is scored only if at least min_streams
    streams have z and a rate from at least 180 past days.
    """
    y = np.log1p(views.astype(float))
    z = causal_z(y)
    exc = (z > Z_THRESHOLD) & z.notna()
    valid = z.notna()
    e_past = exc.astype(float).where(valid).shift(1).rolling(SCALE_DAYS, min_periods=MIN_SCALE).sum()
    n_past = valid.astype(float).shift(1).rolling(SCALE_DAYS, min_periods=1).sum()
    rate = ((e_past + 0.5) / (n_past + 1.0)).where(n_past >= MIN_SCALE)
    usable = valid & rate.notna()
    count = (exc & usable).sum(axis=1)
    n_use = usable.sum(axis=1)
    scored = n_use >= min_streams
    tail = pd.Series(np.nan, index=views.index)
    R = rate.to_numpy()
    U = usable.to_numpy()
    for i in range(len(views.index)):
        if scored.iloc[i]:
            tail.iloc[i] = poisson_binomial_sf(R[i, U[i]], int(count.iloc[i]))
    ign = (tail < alpha_day) & scored
    return GWI2Result(z, exc & usable, count, tail, ign.fillna(False), scored)


COMMON_FRAC = 0.15
COMMON_HALF = 1


def common_mode(ign: pd.Series, panel: pd.DataFrame, frac: float = COMMON_FRAC,
                half: int = COMMON_HALF) -> pd.Series:
    """True on days when at least `frac` of the panel articles (scored that day) ignite
    within +-`half` days. panel: days x articles of 1/0 (NaN = unscored); it must not
    contain the article being filtered (leave it out). Global shocks that move every
    topic (e.g. school closures) are not attention to a specific hazard.
    """
    pan = panel.reindex(ign.index)
    near = pan.rolling(2 * half + 1, center=True, min_periods=1).max()
    share = near.mean(axis=1, skipna=True)
    return (share >= frac).fillna(False)


def filtered_ignition(ign: pd.Series, panel: pd.DataFrame) -> pd.Series:
    """Ignitions that are not common-mode (protocol §3.4)."""
    return ign & ~common_mode(ign, panel)


# ---------- calibration test (protocol §5) ----------

def block_bootstrap_upper(ign: pd.DataFrame, block: int = 14, n_boot: int = 4000, level: float = 0.975,
                          seed: int = 0) -> tuple[float, float]:
    """Pooled false-ignition rate and its one-sided upper bound.

    ign: days x articles, 1/0 for scored days, NaN for unscored. Blocks of `block`
    consecutive days within one article are resampled with replacement (keeps runs
    of ignitions together). Returns (rate, upper bound at `level`).
    """
    a = ign.to_numpy(dtype=float)
    T, M = a.shape
    nb = T // block
    sums, cnts = [], []
    for m in range(M):
        for b in range(nb):
            seg = a[b * block:(b + 1) * block, m]
            ok = np.isfinite(seg)
            if ok.any():
                sums.append(seg[ok].sum())
                cnts.append(ok.sum())
    sums_a, cnts_a = np.array(sums), np.array(cnts)
    if cnts_a.sum() == 0:
        return float("nan"), float("nan")
    rate = sums_a.sum() / cnts_a.sum()
    rng = np.random.default_rng(seed)
    k = len(sums_a)
    pick = rng.integers(0, k, size=(n_boot, k))
    boots = sums_a[pick].sum(axis=1) / cnts_a[pick].sum(axis=1)
    return float(rate), float(np.quantile(boots, level))


# ---------- event test (protocol §6) ----------

def window_hits(ign: pd.Series, dates: list[pd.Timestamp], length: int = 3) -> np.ndarray:
    """1 if ignition on any day d .. d+length-1 for each event date d."""
    s = ign.astype(float)
    out = []
    for d in dates:
        w = s.loc[d:d + pd.Timedelta(days=length - 1)]
        out.append(float(w.max()) if len(w) else np.nan)
    return np.array(out)


def block_permute(a: np.ndarray, block: int, rng: np.random.Generator) -> np.ndarray:
    """Rows of a (days x series) cut into consecutive blocks, blocks shuffled jointly for all series."""
    T = a.shape[0]
    starts = np.arange(0, T, block)
    order = rng.permutation(len(starts))
    return np.concatenate([a[starts[i]:starts[i] + block] for i in order], axis=0)[:T]


def event_test(test_ign: pd.Series, placebo_ign: pd.DataFrame, dates: list[pd.Timestamp],
               block: int = 14, n_perm: int = 9999, length: int = 3, seed: int = 0) -> dict:
    """Two one-sided statistics with a joint block-permutation null.

    H = share of event windows with a test-article ignition.
    D = H - mean over placebo articles of their share of event windows with an ignition.
    Null: the days x articles ignition matrix (test and placebos together) is cut into
    `block`-day blocks and the blocks are shuffled, event dates fixed. This keeps each
    series' serial dependence and the cross-article dependence, and breaks any link
    with the event dates. p = (1 + #null >= observed) / (1 + n_perm).
    """
    idx = test_ign.index
    mat = pd.concat([test_ign.astype(float), placebo_ign.reindex(idx).astype(float)], axis=1).fillna(0.0)
    a = mat.to_numpy()
    pos = [idx.get_loc(d) for d in dates]

    def stats(arr: np.ndarray) -> tuple[float, float]:
        hits = np.array([arr[p:p + length].max(axis=0) for p in pos])
        h = hits[:, 0].mean()
        hp = hits[:, 1:].mean() if hits.shape[1] > 1 else 0.0
        return h, h - hp

    h_obs, d_obs = stats(a)
    rng = np.random.default_rng(seed)
    ge_h = ge_d = 0
    for _ in range(n_perm):
        h, d = stats(block_permute(a, block, rng))
        ge_h += h >= h_obs - 1e-12
        ge_d += d >= d_obs - 1e-12
    return {"H": float(h_obs), "D": float(d_obs),
            "p_H": (1 + ge_h) / (1 + n_perm), "p_D": (1 + ge_d) / (1 + n_perm)}


def holm(ps: list[float], alpha: float = 0.05) -> list[bool]:
    order = np.argsort(ps)
    rej = [False] * len(ps)
    for rank, i in enumerate(order):
        if ps[i] <= alpha / (len(ps) - rank):
            rej[i] = True
        else:
            break
    return rej
