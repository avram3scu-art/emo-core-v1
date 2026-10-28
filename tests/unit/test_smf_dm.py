"""Diebold–Mariano and Holm (docs/SMF_PROTOCOL.md §13): synthetic checks, committed before the run."""

import numpy as np

from emo.smf import diebold_mariano, holm


def test_dm_equal_loss_null_rejects_about_five_percent():
    rng = np.random.default_rng(1)
    rej = 0
    for _ in range(1000):
        y = rng.normal(size=150)
        a = y + rng.normal(size=150)  # two equally good forecasts
        b = y + rng.normal(size=150)
        rej += diebold_mariano((a - y) ** 2, (b - y) ** 2, lags=2)["p"] < 0.05
    assert 0.03 <= rej / 1000 <= 0.075


def test_dm_detects_clearly_better_forecast():
    rng = np.random.default_rng(2)
    y = rng.normal(size=150)
    good = y + 0.3 * rng.normal(size=150)
    r = diebold_mariano((good - y) ** 2, y ** 2, lags=11)
    assert r["p"] < 0.001 and r["mean_d"] < 0


def test_dm_worse_model_never_passes():
    rng = np.random.default_rng(3)
    y = rng.normal(size=150)
    bad = y + 2.0 * rng.normal(size=150)
    assert diebold_mariano((bad - y) ** 2, y ** 2, lags=11)["p"] > 0.5


def test_holm_matches_hand_computation():
    assert np.allclose(holm([0.01, 0.04, 0.03, 0.2]), [0.04, 0.09, 0.09, 0.2])
