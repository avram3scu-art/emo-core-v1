"""Unit tests for the calibrated GWI rule (docs/GWI_CALIBRATION_PROTOCOL.md §2)."""

import numpy as np
import pandas as pd

from emo.gwi import calibrate_fraction_threshold, coincidence_fraction


def test_threshold_respects_target_rate():
    rng = np.random.default_rng(1)
    idx = pd.date_range("2016-01-01", periods=3000, freq="D")
    common = rng.normal(size=len(idx))[:, None]
    r = pd.DataFrame(0.7 * common + rng.normal(size=(len(idx), 12)), index=idx)
    g = coincidence_fraction(r, idx[0], idx[-1])
    f = calibrate_fraction_threshold(g, 12, q=0.005)
    assert np.isfinite(f)
    assert np.mean(g >= f - 1e-9) <= 0.005
    # one step lower would exceed the target
    assert np.mean(g >= f - 1 / 12 - 1e-9) > 0.005


def test_frozen_scale_flags_later_shift():
    idx = pd.date_range("2016-01-01", periods=400, freq="D")
    rng = np.random.default_rng(2)
    r = pd.DataFrame(rng.normal(size=(400, 10)), index=idx)
    r.iloc[300:] += 10.0  # later period shifted up for every stream
    g = coincidence_fraction(r, idx[0], idx[299])
    assert g.iloc[:300].mean() < 0.1
    assert (g.iloc[300:] == 1.0).all()


def test_no_qualifying_threshold_returns_inf():
    g = pd.Series([1.0] * 10)
    assert calibrate_fraction_threshold(g, 4, q=0.005) == float("inf")
