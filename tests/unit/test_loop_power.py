"""Checks on analysis/loop_power.py (docs/LOOP_PROTOCOL.md §9). Synthetic only, fast."""
import importlib.util
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

ROOT = Path(__file__).resolve().parents[2]


def _lp():
    spec = importlib.util.spec_from_file_location("lp", ROOT / "analysis/loop_power.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_within_season_permutation_stays_in_season():
    lp = _lp()
    season = np.array([2, 0, 1, 0, 2, 2, 1, 0, 3])
    perm = lp.within_perm(season, 200, np.random.default_rng(0))
    assert (season[perm] == season[None, :]).all()
    assert all(sorted(row) == list(range(len(season))) for row in perm)
    assert (perm != np.arange(len(season))).any()


def test_holm_matches_hand_example():
    lp = _lp()
    assert np.allclose(lp.holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
    assert np.allclose(lp.holm([0.5, 0.9]), [1.0, 1.0])


def test_kendall_matches_scipy():
    lp = _lp()
    rng = np.random.default_rng(1)
    t = np.arange(9.0)
    v = rng.normal(size=(5, 9))
    for row, k in zip(v, lp.kendall_rows(t, v), strict=True):
        assert abs(k - kendalltau(t, row).statistic) < 1e-12


def test_ecdf_mid_equals_rank_transform_on_sample():
    lp = _lp()
    x = np.array([3.0, 1.0, 2.0, 2.0, 5.0])
    assert np.allclose(lp.ecdf_mid(x, x), lp.u(x))


def test_residuals_orthogonal_to_controls():
    lp = _lp()
    d = lp.simulate(np.random.default_rng(2), lp.SIZES_HU)
    m = ~np.isnan(d["A"]) & ~np.isnan(d["Ystate"])
    C = lp.controls(d, m)
    assert np.allclose(C.T @ lp.resid(lp.u(d["A"][m]), C), 0, atol=1e-9)


def test_strong_coupling_detected_and_true_pair_named():
    lp = _lp()
    d = lp.simulate(np.random.default_rng(3), lp.SIZES_HUTS, c=4.0)
    p, r, _ = lp.h4_pair(d, "A", "Ystate", np.random.default_rng(4), B=199)
    assert p < 0.01 and r < 0


def test_within_season_null_roughly_calibrated():
    lp = _lp()
    rng = np.random.default_rng(5)
    ps = [lp.h4_pair(lp.simulate(rng, lp.SIZES_HU), "A", "Ystate", rng, B=99)[0] for _ in range(150)]
    assert np.mean(np.array(ps) < 0.05) < 0.12


def test_no_equivalence_reading_at_tiny_n():
    lp = _lp()
    assert not lp.equivalent(0.0, 8)
    assert lp.equivalent(0.0, 400)


def test_module_reads_no_file():
    src = (ROOT / "analysis/loop_power.py").read_text()
    for token in ("open(", "read_csv", "read_text", "loadtxt", "requests", "urlopen"):
        assert token not in src


def test_protocol_states_no_record_opened():
    text = (ROOT / "docs/LOOP_PROTOCOL.md").read_text()
    assert "No loop record was opened" in text


def test_fe_statistic_removes_season_shocks_exactly():
    lp = _lp()
    lp.STAT = "fe"
    d = lp.simulate(np.random.default_rng(6), lp.SIZES_HUTS)
    rX, rY, s = lp.pair_resid(d, "A", "Ystate")
    for k in np.unique(s):
        assert abs(rX[s == k].sum()) < 1e-9 and abs(rY[s == k].sum()) < 1e-9


def test_fe_strong_coupling_detected():
    lp = _lp()
    lp.STAT = "fe"
    d = lp.simulate(np.random.default_rng(3), lp.SIZES_HUTS, c=4.0)
    p, r, _ = lp.h4_pair(d, "A", "Ystate", np.random.default_rng(4), B=199)
    assert p < 0.01 and r < 0
