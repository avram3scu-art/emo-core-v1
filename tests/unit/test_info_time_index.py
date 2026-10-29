"""τ_I is fitted on the series' time index, not on 0..n-1 (audit 2026-10-29, D1; session 2.1)."""

import numpy as np
import pandas as pd
import pytest

from emo.info_time import compute_information_time


def _gapped_years() -> pd.Series:
    # skill rises exactly 1.0 per year; years 1980-1989 are missing (cross-gap pairs
    # are the majority, so a per-step Theil-Sen median would be inflated)
    years = [y for y in range(1970, 2000) if not 1980 <= y <= 1989]
    return pd.Series([float(y - 1970) for y in years], index=years)


def test_gapped_numeric_index_gives_per_year_slope():
    r = compute_information_time(_gapped_years())
    assert r.slope == pytest.approx(1.0)
    assert r.metadata["units"] == "skill per index unit"
    assert r.total_positive_increments == pytest.approx(29.0)  # slope x span in years


def test_per_step_fit_would_be_wrong_on_the_same_gap():
    s = _gapped_years()
    per_step = compute_information_time(s.reset_index(drop=True))  # RangeIndex = old behaviour
    assert per_step.slope > 1.5  # a 10-year gap inflates a per-step slope


def test_datetime_index_gives_per_year_slope():
    days = pd.to_datetime(["2000-01-01", "2001-01-01", "2004-01-01", "2005-01-01", "2008-01-01"])
    x_years = np.asarray((days - days[0]) / pd.Timedelta(days=1)) / 365.25
    r = compute_information_time(pd.Series(2.0 * x_years, index=days))
    assert r.slope == pytest.approx(2.0)
    assert r.metadata["units"] == "skill per year"


def test_block_ci_runs_on_gapped_index():
    rng = np.random.default_rng(1)
    s = _gapped_years() + rng.normal(0, 0.1, 20)
    r = compute_information_time(s, ci="block", block=3, n_boot=200, seed=0)
    assert r.slope_ci_low <= r.slope <= r.slope_ci_high


def test_unsorted_index_is_refused():
    with pytest.raises(ValueError):
        compute_information_time(pd.Series([1.0, 2.0, 3.0], index=[3, 1, 2]))
