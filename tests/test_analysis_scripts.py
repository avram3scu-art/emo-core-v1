"""Checks on analysis/ code beyond its weekly runs.

Every analysis script must at least compile; the functions of the session-8 synergy
analysis are tested directly (the other scripts are top-level code, covered by the weekly
run and, for RDL and GWI, by the frozen-output check in scripts/weekly_run.py).
"""
import importlib.util
import py_compile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_every_analysis_script_compiles():
    for f in sorted((ROOT / "analysis").glob("*.py")):
        py_compile.compile(str(f), doraise=True)


def _synergy_module():
    spec = importlib.util.spec_from_file_location("synergy_climate", ROOT / "analysis/synergy_climate.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_residuals_remove_trend_and_season_exactly():
    m = _synergy_module()
    t = np.arange(m.T)
    season = np.tile(np.arange(12) * 0.1, m.T // 12)
    y = pd.DataFrame({"a": 2 + 0.03 * t + season, "b": -1 - 0.01 * t + 2 * season}, index=m.MONTHS)
    assert np.allclose(m.residuals(y).to_numpy(), 0, atol=1e-9)


def test_shift_pairs_obey_protocol():
    m = _synergy_module()
    pairs = m.shifts()
    assert len(pairs) == len(set(pairs)) == 7310
    for s2, s3 in pairs:
        d = abs(s2 - s3)
        assert 12 <= s2 <= 108 and 12 <= s3 <= 108 and min(d, m.T - d) >= 12
