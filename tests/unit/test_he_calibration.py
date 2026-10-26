"""The exact Kendall null used by analysis/he_calibration.py matches scipy's exact test."""
import importlib.util
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

ROOT = Path(__file__).resolve().parents[2]


def _hc():
    spec = importlib.util.spec_from_file_location("hc", ROOT / "analysis/he_calibration.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_mahonian_null_matches_scipy_exact():
    hc = _hc()
    rng = np.random.default_rng(0)
    for n in (3, 5, 8, 12):
        cdf = hc.mahonian_cdf(n)
        assert abs(cdf[-1] - 1) < 1e-12
        npairs = n * (n - 1) // 2
        for _ in range(20):
            x, y = rng.normal(size=n), rng.normal(size=n)
            tau, p = kendalltau(x, y, alternative="greater", method="exact")
            disc = round((npairs - tau * npairs) / 2)
            assert abs(cdf[disc] - p) < 1e-9
