"""Tests for GWI v2 (emo/gwi_v2.py; docs/GWI_V2_PROTOCOL.md)."""

from __future__ import annotations

import datetime as dt
import itertools

import numpy as np
import pandas as pd
import pytest
from scipy.stats import binom

from emo.gwi_v2 import (
    block_permute,
    causal_z,
    common_mode,
    compute_gwi_v2,
    event_test,
    holm,
    poisson_binomial_sf,
)


def _views(days: pd.DatetimeIndex, n: int = 12, seed: int = 1, sept_step: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    out = {}
    for s in range(n):
        wk = rng.normal(0, 0.1, 7)
        step = sept_step * ((days.month >= 9) | (days.month <= 5))
        y = 7 + wk[days.dayofweek] + step + rng.normal(0, 0.1, len(days))
        out[f"s{s}"] = np.round(np.expm1(y))
    return pd.DataFrame(out, index=days)


DAYS = pd.date_range("2019-01-01", "2023-12-31", freq="D")


def test_causal_no_lookahead():
    v = _views(DAYS)
    cut = pd.Timestamp("2023-06-01")
    v2 = v.copy()
    v2.loc[cut:] = v2.loc[cut:] * 50  # change the future only
    a, b = compute_gwi_v2(v, 3e-4), compute_gwi_v2(v2, 3e-4)
    before = DAYS[DAYS < cut]
    pd.testing.assert_frame_equal(a.z.loc[before], b.z.loc[before])
    pd.testing.assert_series_equal(a.tail_p.loc[before], b.tail_p.loc[before])


def test_requires_gap_free_index():
    v = _views(DAYS).drop(DAYS[10])
    with pytest.raises(ValueError):
        causal_z(np.log1p(v))


def test_poisson_binomial_matches_brute_force_and_binomial():
    p = [0.1, 0.3, 0.05, 0.6]
    for k in range(6):
        brute = sum(np.prod([pi if b else 1 - pi for pi, b in zip(p, bits, strict=True)])
                    for bits in itertools.product([0, 1], repeat=4) if sum(bits) >= k)
        assert poisson_binomial_sf(np.array(p), k) == pytest.approx(brute)
    assert poisson_binomial_sf(np.full(12, 0.02), 4) == pytest.approx(binom.sf(3, 12, 0.02))


def test_seasonal_step_absorbed_and_real_spike_detected():
    v = _views(DAYS, sept_step=0.5)
    spike = pd.Timestamp("2023-03-15")
    v.loc[spike] = v.loc[spike] * 20
    r = compute_gwi_v2(v, 3e-4)
    sept23 = r.ignition.loc["2023-09-01":"2023-09-30"]
    assert sept23.sum() <= 1  # the yearly September step does not ignite
    assert bool(r.ignition.loc[spike])


def test_common_mode_flags_shared_days():
    idx = pd.date_range("2026-01-01", periods=30, freq="D")
    panel = pd.DataFrame(0.0, index=idx, columns=range(20))
    panel.iloc[10, :3] = 1.0  # 3 of 20 = 15 % on day 10
    flag = common_mode(pd.Series(False, index=idx), panel)
    assert flag.iloc[9] and flag.iloc[10] and flag.iloc[11]
    assert not flag.iloc[5] and not flag.iloc[13]
    panel.iloc[10, 2] = 0.0  # 2 of 20 = 10 %
    assert not common_mode(pd.Series(False, index=idx), panel).any()


def test_block_permute_keeps_rows_and_blocks():
    a = np.arange(40, dtype=float).reshape(20, 2)
    b = block_permute(a, 5, np.random.default_rng(0))
    assert sorted(b[:, 0]) == sorted(a[:, 0])
    np.testing.assert_array_equal(b[:, 1] - b[:, 0], np.ones(20))
    for start in range(0, 20, 5):
        blk = b[start:start + 5, 0]
        assert np.all(np.diff(blk) == 2)


def test_event_test_power_and_null():
    rng = np.random.default_rng(3)
    idx = pd.date_range("2026-11-01", periods=365, freq="D")
    pl = pd.DataFrame({m: (rng.random(365) < 0.005).astype(float) for m in range(20)}, index=idx)
    dates = [idx[i] for i in range(10, 350, 30)]
    t = pd.Series((rng.random(365) < 0.005).astype(float), index=idx)
    null = event_test(t, pl, dates, n_perm=499, seed=1)
    t2 = t.copy()
    t2.loc[dates] = 1.0
    hit = event_test(t2, pl, dates, n_perm=499, seed=1)
    assert hit["H"] == 1.0 and hit["p_H"] < 0.01 and hit["p_D"] < 0.01
    assert null["p_H"] > 0.05


def test_holm():
    assert holm([0.01, 0.04]) == [True, True]
    assert holm([0.03, 0.04]) == [False, False]
    assert holm([0.001, 0.2]) == [True, False]


def test_fetch_refuses_before_scoring_date(tmp_path, monkeypatch):
    from scripts import fetch_gwi_v2 as f

    monkeypatch.setattr(f, "OUT", tmp_path / "gwi_v2")
    assert f.main(today=dt.date(2027, 11, 14)) == 2
    assert not (tmp_path / "gwi_v2").exists()


def test_prospective_parameters_match_protocol():
    from analysis import gwi_v2_prospective as p
    from scripts import fetch_gwi_v2 as f

    assert p.ALPHA_DAY == 3e-4 and p.Q == 0.005
    assert p.W == (pd.Timestamp("2026-11-01"), pd.Timestamp("2027-10-31"))
    assert f.SCORING_DATE == dt.date(2027, 11, 15) and len(f.PLACEBOS) == 20
