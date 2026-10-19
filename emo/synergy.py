from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class SynergyResult:
    """
    Result container for Gaussian O-information.

    synergy_index:
        Minus the O-information, in bits. Positive = synergy-dominated
        (the whole carries information no subset carries); negative =
        redundancy-dominated (streams repeat the same information);
        zero = independent streams, or no higher-order structure.
    o_information_bits:
        O-information Ω (Rosas et al. 2019), in bits. Ω > 0 means redundancy
        dominates, Ω < 0 means synergy dominates.
    total_correlation_bits:
        Total shared information among the streams (multi-information), in bits.
        Zero only when the streams are independent.
    per_stream_contribution:
        Each stream's share of the total variance (descriptive only).
    """

    synergy_index: float
    per_stream_contribution: dict[str, float]
    metadata: dict[str, str]
    o_information_bits: float = 0.0
    total_correlation_bits: float = 0.0
    n_samples: int = 0
    extra: dict[str, float] = field(default_factory=dict)


def _logdet_bits(c: np.ndarray) -> float:
    """log2 det of a positive-definite matrix (raises if not positive definite)."""
    sign, logdet = np.linalg.slogdet(c)
    if sign <= 0:
        raise np.linalg.LinAlgError("matrix is not positive definite")
    return float(logdet / np.log(2.0))


def compute_gaussian_synergy(df: pd.DataFrame, ridge: float = 1e-6) -> SynergyResult:
    """
    Gaussian O-information of a multivariate set of streams.

    Parameters
    ----------
    df:
        DataFrame with one column per stream, e.g.
        ["news", "papers", "policy", "ew_alerts"]; rows are time steps.
    ridge:
        Small value added to the correlation matrix diagonal so that nearly
        identical streams do not make the determinant zero.

    Notes
    -----
    Under a Gaussian approximation, entropies follow from the covariance
    matrix, and the (2πe) constants cancel. With R the correlation matrix
    (scale-free), n streams and logs in base 2:

        TC  = -1/2 log det R
        Ω   =  1/2 [ (n-2) log det R + Σ_j ( log R_jj - log det R_{-j} ) ]

    where R_{-j} is R with stream j removed. This is the O-information of
    Rosas, Mediano, Gastpar & Jensen (2019), Phys. Rev. E 100, 032305.
    For n = 2, Ω is identically zero: two streams can only share information
    pairwise, so a higher-order index needs at least three streams.

    Assumptions and limits: Gaussian, stationary, samples treated as
    independent (time-series autocorrelation inflates apparent precision).
    """
    clean = df.dropna()
    n = clean.shape[1]
    if clean.empty or n < 3 or clean.shape[0] < n + 2:
        return SynergyResult(
            0.0, {}, {"definition": "degenerate (needs >= 3 streams and > n+1 rows)"},
            n_samples=int(clean.shape[0]),
        )

    x = clean.to_numpy(dtype=float)
    sd = x.std(axis=0, ddof=1)
    keep = sd > 0
    if keep.sum() < 3:
        return SynergyResult(0.0, {}, {"definition": "degenerate (constant streams)"},
                             n_samples=int(clean.shape[0]))

    r = np.corrcoef(x[:, keep], rowvar=False)
    n = r.shape[0]
    r = r + ridge * np.eye(n)

    logdet_all = _logdet_bits(r)
    tc = -0.5 * logdet_all
    acc = (n - 2) * logdet_all
    for j in range(n):
        idx = [k for k in range(n) if k != j]
        acc += np.log2(r[j, j]) - _logdet_bits(r[np.ix_(idx, idx)])
    omega = 0.5 * acc

    variances = np.var(x, axis=0, ddof=1)
    total_var = float(variances.sum()) or 1.0
    per_stream = {
        col: float(v / total_var) for col, v in zip(clean.columns, variances, strict=False)
    }

    return SynergyResult(
        synergy_index=float(-omega),
        per_stream_contribution=per_stream,
        metadata={
            "definition": "gaussian_o_information_v1.1",
            "units": "bits",
            "sign": "synergy_index > 0: synergy-dominated; < 0: redundancy-dominated",
        },
        o_information_bits=float(omega),
        total_correlation_bits=float(tc),
        n_samples=int(clean.shape[0]),
    )
