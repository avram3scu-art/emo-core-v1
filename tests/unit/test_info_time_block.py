"""τ_I interval under autocorrelation: the block bootstrap must not credit a trend to
autocorrelated noise more often than the independent-errors interval does."""
import numpy as np
import pandas as pd
import pytest

from emo.info_time import compute_information_time


def _ar1(n, phi, rng):
    e = np.zeros(n)
    for t in range(1, n):
        e[t] = phi * e[t - 1] + rng.normal()
    return e


def test_block_ci_fewer_false_trends_on_ar1_noise():
    rng = np.random.default_rng(11)
    iid = block = 0
    for _ in range(30):
        s = pd.Series(_ar1(56, 0.8, rng))
        iid += compute_information_time(s).tau_i > 0
        block += compute_information_time(s, ci="block", n_boot=200).tau_i > 0
    assert block < iid


def test_block_ci_keeps_a_strong_trend_and_default_unchanged():
    rng = np.random.default_rng(12)
    s = pd.Series(0.5 * np.arange(56) + rng.normal(size=56))
    a = compute_information_time(s)
    b = compute_information_time(s, ci="block", n_boot=300)
    assert b.tau_i > 0 and a.slope == b.slope
    assert a.metadata["definition"] == "theil_sen_lower_bound_v1.1"
    with pytest.raises(ValueError):
        compute_information_time(s, ci="other")
