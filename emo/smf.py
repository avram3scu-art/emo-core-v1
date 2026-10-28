from __future__ import annotations

import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class SMFResult:
    """
    Self-Model Fidelity (SMF) result.

    smf_score:
        In [0, 1]. Correlation between a model's expectation and what was
        realised, *in excess of what chance alone produces* under the same
        lag search. 0 = no evidence of fidelity.
    lag_days:
        Lag at which the best correlation was found (positive = model leads).
    """

    smf_score: float
    lag_days: int
    metadata: dict[str, str]
    best_corr: float = 0.0
    null_corr_95: float = 0.0
    p_value: float = 1.0
    extra: dict[str, float] = field(default_factory=dict)


KPSS_CRIT_1PCT = 0.739  # KPSS level-stationarity test, 1% critical value


def kpss_level(x: np.ndarray) -> float:
    """KPSS statistic for level stationarity (Bartlett long-run variance, lag int(4 (n/100)^0.25)).

    Large values reject stationarity (trend or unit root). docs/SMF_PROTOCOL.md §13 (M1 guard).
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    e = x - x.mean()
    s = np.cumsum(e)
    lags = int(4 * (n / 100) ** 0.25)
    v = float(e @ e) / n
    for j in range(1, min(lags, n - 1) + 1):
        v += 2.0 * (1.0 - j / (lags + 1.0)) * float(e[j:] @ e[:-j]) / n
    return float(s @ s) / (n * n * v) if v > 0 else float("inf")


def _lagged_corrs(m: np.ndarray, r: np.ndarray, max_lag: int, min_overlap: int) -> np.ndarray:
    out = np.full(2 * max_lag + 1, -np.inf)
    n = len(m)
    for i, lag in enumerate(range(-max_lag, max_lag + 1)):
        if lag < 0:
            a, b = m[-lag:], r[: n + lag]
        elif lag > 0:
            a, b = m[: n - lag], r[lag:]
        else:
            a, b = m, r
        if len(a) < min_overlap or a.std() == 0 or b.std() == 0:
            continue
        out[i] = np.corrcoef(a, b)[0, 1]
    return out


def compute_smf(
    model: pd.Series,
    realised: pd.Series,
    max_lag_days: int = 0,
    n_surrogates: int = 199,
    seed: int = 0,
) -> SMFResult:
    """
    Self-Model Fidelity: does what a system expects track what then happens?

    Parameters
    ----------
    model, realised:
        Time-indexed series (model expectation, realised outcome).
    max_lag_days:
        Lag search range in samples. Default 0: no search, the honest choice
        when the lag is known in advance. If a search is used, the score is
        corrected for it (see Notes).
    n_surrogates:
        Maximum number of circular-shift surrogates for the null; each distinct
        shift is used at most once (see Notes).

    Notes
    -----
    v1.0 took the best correlation over +/-365 lags and mapped it to (r+1)/2,
    so two unrelated noise series scored about 0.57. Here:

    - best_corr = maximum correlation over the allowed lags;
    - the same search is run on surrogates in which `realised` is circularly
      shifted by a random amount (this keeps each series' own autocorrelation
      but breaks any real relation);
    - smf_score = max(0, (best_corr - null95) / (1 - null95)), where null95 is
      the 95th percentile of the surrogate maxima;
    - p_value = (1 + surrogates reaching best_corr) / (1 + surrogates).

    For unrelated *stationary* series the score is 0 about 95% of the time. The null is not
    valid for trending or unit-root series: two independent linear trends pass 100% of the time
    and two independent random walks 32% (audit 2026-10-27, probe M1). A KPSS test on both
    inputs (1% level) raises a RuntimeWarning and sets metadata["stationarity"] = "kpss_reject";
    difference such series (e.g. 12-month changes) before use.

    v1.2 (2026-10-23): the admissible shifts are [min_overlap, n - min_overlap],
    which for short series are few (n = 25 gives 6). v1.1 drew 199 shifts with
    replacement from that set and counted repeats as independent, so it could
    report p = 0.005 where the honest floor was 1/7. Now each distinct shift is
    used at most once: all of them when there are no more than `n_surrogates`,
    otherwise `n_surrogates` drawn without replacement. `extra["n_null"]` is the
    number of surrogates used and `extra["p_min"]` = 1 / (1 + n_null), the
    smallest p-value the series can produce. If p_min exceeds the chosen alpha,
    the series is too short for the test, whatever the data.
    """
    if model.empty or realised.empty:
        return SMFResult(0.0, 0, {"definition": "empty"})

    df = pd.concat({"model": model, "realised": realised}, axis=1).dropna().sort_index()
    n = len(df)
    if n < 10:
        return SMFResult(0.0, 0, {"definition": "too_few_points"})

    m = df["model"].to_numpy(dtype=float)
    r = df["realised"].to_numpy(dtype=float)
    # M1 guard (audit 2026-10-27; docs/SMF_PROTOCOL.md §13): the circular-shift null is valid
    # only for stationary input. On trending or unit-root series it rejects far too often
    # (independent trends 100%, random walks 32% at nominal 5%). Warn; results are unchanged.
    kpss = max(kpss_level(m), kpss_level(r))
    stationarity = "kpss_reject" if kpss > KPSS_CRIT_1PCT else "kpss_ok"
    if stationarity == "kpss_reject":
        warnings.warn(
            f"compute_smf: input fails a KPSS stationarity test (stat {kpss:.2f} > {KPSS_CRIT_1PCT}); "
            "the circular-shift null is not valid for trending or unit-root series. Difference the series first.",
            RuntimeWarning, stacklevel=2)
    max_lag = int(min(max(max_lag_days, 0), n // 2))
    min_overlap = max(10, n // 4)

    corrs = _lagged_corrs(m, r, max_lag, min_overlap)
    i_best = int(np.argmax(corrs))
    best = float(corrs[i_best])
    best_lag = i_best - max_lag
    if not np.isfinite(best):
        return SMFResult(0.0, 0, {"definition": "constant_series"})

    rng = np.random.default_rng(seed)
    admissible = np.arange(min_overlap, n - min_overlap + 1) if n > 2 * min_overlap else np.array([], dtype=int)
    if len(admissible) > n_surrogates:
        shifts = rng.choice(admissible, size=n_surrogates, replace=False)
    else:
        shifts = admissible
    null_max = np.array(
        [np.max(_lagged_corrs(m, np.roll(r, int(s)), max_lag, min_overlap)) for s in shifts]
    )
    if len(null_max) == 0:
        return SMFResult(0.0, best_lag, {"definition": "series_too_short_for_null"}, best_corr=best)

    null95 = float(np.quantile(null_max, 0.95))
    p_value = float((1 + np.sum(null_max >= best)) / (1 + len(null_max)))
    score = max(0.0, (best - null95) / (1.0 - null95)) if null95 < 1 else 0.0

    return SMFResult(
        smf_score=float(min(score, 1.0)),
        lag_days=best_lag,
        metadata={"definition": "lag_corrected_corr_v1.2", "stationarity": stationarity},
        best_corr=best,
        null_corr_95=null95,
        p_value=p_value,
        extra={
            "n_points": float(n),
            "max_lag": float(max_lag),
            "n_null": float(len(null_max)),
            "p_min": 1.0 / (1 + len(null_max)),
        },
    )


def diebold_mariano(loss_model: np.ndarray, loss_bench: np.ndarray, lags: int) -> dict[str, float]:
    """One-sided Diebold–Mariano test that the model's loss is smaller than the benchmark's.

    d_t = loss_model_t - loss_bench_t. Long-run variance: Newey–West (Bartlett weights,
    `lags` lags). Harvey–Leybourne–Newbold small-sample correction with k = lags + 1;
    p = P(t_{n-1} < HLN) (H1: mean(d) < 0). docs/SMF_PROTOCOL.md §13.
    Returns nan statistics if the variance estimate is not positive.
    """
    from scipy.stats import t as student_t

    d = np.asarray(loss_model, dtype=float) - np.asarray(loss_bench, dtype=float)
    n = len(d)
    dc = d - d.mean()
    v = float(dc @ dc) / n
    for j in range(1, min(lags, n - 1) + 1):
        v += 2.0 * (1.0 - j / (lags + 1.0)) * float(dc[j:] @ dc[:-j]) / n
    if not v > 0:
        return {"n": float(n), "mean_d": float(d.mean()), "dm": float("nan"), "hln": float("nan"), "p": float("nan")}
    dm = float(d.mean() / np.sqrt(v / n))
    k = lags + 1
    hln = dm * float(np.sqrt((n + 1 - 2 * k + k * (k - 1) / n) / n))
    return {"n": float(n), "mean_d": float(d.mean()), "dm": dm, "hln": hln,
            "p": float(student_t.cdf(hln, df=n - 1))}


def holm(pvalues: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (family-wise error), same order as the input."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adj = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvalues[i]))
        adj[i] = running
    return adj
