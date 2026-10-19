from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import binom


@dataclass
class GWIResult:
    """
    Result container for Global Workspace Ignition (GWI).

    gwi_series:
        Fraction of streams in a simultaneous high excursion at each time, in [0, 1].
    events:
        Timestamps where more streams are in excursion together than chance
        allows (binomial test against independent streams, corrected for the
        number of time steps tested).
    """

    gwi_series: pd.Series
    events: list[pd.Timestamp]
    metadata: dict[str, str]
    min_streams_for_event: int = 0
    expected_false_events: float = 0.0
    extra: dict[str, float] = field(default_factory=dict)


def compute_gwi(
    streams: pd.DataFrame,
    z_threshold: float = 2.0,
    alpha: float = 0.05,
) -> GWIResult:
    """
    Global Workspace Ignition: moments when many attention streams spike *together*.

    Parameters
    ----------
    streams:
        DataFrame indexed by time; columns are attention proxies
        (news volume, pageviews, search trends, ...).
    z_threshold:
        A stream is "in excursion" when its robust z-score
        (median / MAD) exceeds this value.
    alpha:
        Family-wise false-alarm rate across all time steps.

    Notes
    -----
    v1.0 thresholded its own composite at the 95th percentile, so it flagged
    about 5% of days as ignitions even for pure noise. Here an ignition is a
    coincidence that independent streams would rarely produce:

    - p = mean per-stream excursion rate (estimated from the data),
    - an event needs k streams in excursion together, with
      P(Binomial(n, p) >= k) < alpha / T (Bonferroni over T time steps).

    With fewer than three streams, or rare excursions, no event can reach
    significance, and none is reported.

    Assumptions and limits: streams are tested against independence. Streams
    that are always correlated (shared seasonality, shared outages) will
    produce events that reflect that coupling; remove known common drivers
    first. Serial correlation within a stream is not modelled.
    """
    if streams.empty or streams.shape[1] < 1:
        return GWIResult(pd.Series(dtype=float), [], {"definition": "empty"})

    df = streams.sort_index().astype(float).dropna(how="all")
    med = df.median()
    mad = (df - med).abs().median() * 1.4826
    mad = mad.where(mad > 0, df.std(ddof=0)).replace(0, np.nan)
    z = (df - med) / mad

    excursion = (z > z_threshold) & z.notna()
    n_valid = z.notna().sum(axis=1)
    count = excursion.sum(axis=1)
    gwi_series = (count / n_valid.replace(0, np.nan)).fillna(0.0).rename("gwi")

    n = int(df.shape[1])
    t = int(len(df))
    p = float(excursion.to_numpy().sum() / max(z.notna().to_numpy().sum(), 1))

    k_min = n + 1
    if 0 < p < 1:
        for k in range(1, n + 1):
            if binom.sf(k - 1, n, p) < alpha / max(t, 1):
                k_min = k
                break

    events = count[count >= k_min].index.to_list() if k_min <= n else []
    expected_false = float(t * binom.sf(k_min - 1, n, p)) if k_min <= n else 0.0

    return GWIResult(
        gwi_series=gwi_series,
        events=events,
        metadata={
            "definition": "coincident_excursions_binomial_v1.1",
            "z_threshold": f"{z_threshold:.2f}",
            "alpha": f"{alpha:.3f}",
        },
        min_streams_for_event=k_min if k_min <= n else 0,
        expected_false_events=expected_false,
        extra={"excursion_rate": p, "n_streams": float(n), "n_times": float(t)},
    )
