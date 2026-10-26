from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import theilslopes


@dataclass
class InfoTimeResult:
    """
    Information-time τ_I result.

    tau_i:
        Validated gain in predictive skill per time step: the lower bound of
        the 95% confidence interval of the skill trend, floored at 0.
        0 = no demonstrated improvement.
    total_positive_increments:
        Kept for backward compatibility: net skill gain over the record
        (trend slope x span, floored at 0).
    """

    tau_i: float
    total_positive_increments: float
    metadata: dict[str, str]
    slope: float = 0.0
    slope_ci_low: float = 0.0
    slope_ci_high: float = 0.0
    extra: dict[str, float] = field(default_factory=dict)


def _block_bootstrap_slope_ci(
    y: np.ndarray, x: np.ndarray, slope: float, intercept: float, block: int, n_boot: int, seed: int
) -> tuple[float, float]:
    """95% interval of the Theil–Sen slope from a moving-block bootstrap of residuals.

    Residuals around the fitted trend are resampled in circular blocks of `block` steps,
    which keeps short-range autocorrelation that the default (independent-errors)
    interval ignores.
    """
    rng = np.random.default_rng(seed)
    n = len(y)
    fit = intercept + slope * x
    resid = y - fit
    nb = int(np.ceil(n / block))
    slopes = np.empty(n_boot)
    for b in range(n_boot):
        starts = rng.integers(0, n, size=nb)
        idx = ((starts[:, None] + np.arange(block)[None, :]) % n).ravel()[:n]
        slopes[b] = theilslopes(fit + resid[idx], x)[0]
    lo, hi = np.quantile(slopes, [0.025, 0.975])
    return float(lo), float(hi)


def compute_information_time(
    skill_series: pd.Series, ci: str = "iid", block: int = 5, n_boot: int = 2000, seed: int = 0
) -> InfoTimeResult:
    """
    Information-time τ_I from a forecast-skill series (higher = better).

    Notes
    -----
    v1.0 summed only the positive step-to-step changes. That counts every
    upward wobble of noise as learning, so a flat noisy series scored 26x
    higher than a steadily improving one. Here τ_I is the trend in skill,
    estimated robustly (Theil–Sen slope with 95% interval), and only the part
    of the improvement the data can actually support is credited:

        τ_I = max(0, lower 95% bound of the slope)   [skill units per step]

    Steps are the series' own sampling steps; for unevenly spaced data the
    slope is per index step, not per calendar day.

    ci="iid" (default, v1.1): scipy's Theil–Sen interval, which assumes independent
    errors and is too narrow when skill is autocorrelated. ci="block" (v1.2): moving-block
    bootstrap of residuals (`block` steps, `n_boot` resamples, fixed `seed`).
    """
    s = skill_series.dropna().astype(float)
    n = len(s)
    if n < 3:
        return InfoTimeResult(0.0, 0.0, {"definition": "too_few_points"})

    x = np.arange(n, dtype=float)
    y = s.to_numpy()
    slope, intercept, lo, hi = theilslopes(y, x, alpha=0.95)
    definition = "theil_sen_lower_bound_v1.1"
    if ci == "block":
        lo, hi = _block_bootstrap_slope_ci(y, x, float(slope), float(intercept), block, n_boot, seed)
        definition = f"theil_sen_lower_bound_block{block}_v1.2"
    elif ci != "iid":
        raise ValueError("ci must be 'iid' or 'block'")
    tau_i = max(0.0, float(lo))
    net_gain = max(0.0, float(slope) * (n - 1))

    return InfoTimeResult(
        tau_i=tau_i,
        total_positive_increments=net_gain,
        metadata={"definition": definition, "units": "skill per step"},
        slope=float(slope),
        slope_ci_low=float(lo),
        slope_ci_high=float(hi),
        extra={"n_points": float(n)},
    )
