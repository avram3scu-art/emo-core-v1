"""M1 guard (audit 2026-10-27; docs/SMF_PROTOCOL.md §13): compute_smf warns on non-stationary input."""

import warnings

import numpy as np
import pandas as pd

from emo.smf import compute_smf

N = 120


def _warn_rate(gen, reps=200, seed=7):
    rng = np.random.default_rng(seed)
    idx = pd.RangeIndex(N)
    hits = 0
    for _ in range(reps):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            res = compute_smf(pd.Series(gen(rng), idx), pd.Series(gen(rng), idx), n_surrogates=49)
        fired = any(issubclass(x.category, RuntimeWarning) for x in w)
        assert fired == (res.metadata["stationarity"] == "kpss_reject")
        hits += fired
    return hits / reps


def test_guard_fires_on_independent_trends():
    assert _warn_rate(lambda g: np.arange(N) * g.uniform(0.02, 0.1) + g.normal(size=N)) >= 0.95


def test_guard_quiet_on_white_noise():
    assert _warn_rate(lambda g: g.normal(size=N)) <= 0.05
