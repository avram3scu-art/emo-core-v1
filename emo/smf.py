from __future__ import annotations

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
        Number of circular-shift surrogates for the null distribution.

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
    - p_value = fraction of surrogates reaching best_corr.

    Unrelated series therefore score 0 about 95% of the time.
    """
    if model.empty or realised.empty:
        return SMFResult(0.0, 0, {"definition": "empty"})

    df = pd.concat({"model": model, "realised": realised}, axis=1).dropna().sort_index()
    n = len(df)
    if n < 10:
        return SMFResult(0.0, 0, {"definition": "too_few_points"})

    m = df["model"].to_numpy(dtype=float)
    r = df["realised"].to_numpy(dtype=float)
    max_lag = int(min(max(max_lag_days, 0), n // 2))
    min_overlap = max(10, n // 4)

    corrs = _lagged_corrs(m, r, max_lag, min_overlap)
    i_best = int(np.argmax(corrs))
    best = float(corrs[i_best])
    best_lag = i_best - max_lag
    if not np.isfinite(best):
        return SMFResult(0.0, 0, {"definition": "constant_series"})

    rng = np.random.default_rng(seed)
    shifts = rng.integers(min_overlap, n - min_overlap + 1, size=n_surrogates) if n > 2 * min_overlap else []
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
        metadata={"definition": "lag_corrected_corr_v1.1"},
        best_corr=best,
        null_corr_95=null95,
        p_value=p_value,
        extra={"n_points": float(n), "max_lag": float(max_lag)},
    )
