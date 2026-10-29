"""SMF v2 (docs/SMF_PROTOCOL.md §14–§15): definition, family rule, NHC parsing and pairing. Synthetic only."""

import datetime as dt
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from emo.loop_hurricanes import parse_hurdat2
from emo.smf import compute_smf, smf_correlation, smf_family, smf_skill
from emo.smf_nhc import (
    ALPHA,
    MIN_STORMS,
    build_pairs,
    parse_adeck_base,
    parse_error_file,
    score,
)

ROOT = Path(__file__).resolve().parents[2]


def test_skill_detects_better_forecaster_and_not_worse():
    rng = np.random.default_rng(5)
    bench = np.abs(rng.normal(100, 30, 200))
    good = smf_skill("g", bench * 0.6 + rng.normal(0, 5, 200), bench, lags=2)
    bad = smf_skill("b", bench * 1.3, bench, lags=2)
    assert good.skill > 0.3 and good.p < 0.001
    assert bad.skill < 0 and bad.p > 0.5


def test_clustered_skill_uses_one_unit_per_cluster_in_order():
    lm = np.array([1.0, 1.0, 5.0, 5.0, 5.0, 2.0])
    lb = np.array([2.0, 2.0, 4.0, 4.0, 4.0, 4.0])
    cl = np.array(["A", "A", "B", "B", "B", "C"])
    r = smf_skill("x", lm, lb, lags=0, clusters=cl)
    assert r.n == 6 and r.n_units == 3
    assert np.isclose(r.mean_d, np.mean([-1.0, 1.0, -2.0]))


def test_clustered_null_false_positive_rate_near_alpha():
    rng = np.random.default_rng(7)
    rej = 0
    for _ in range(600):
        cl, d = [], []
        for s in range(15):
            k = 2 + rng.poisson(10)
            u = rng.normal()
            d += list(u + rng.normal(size=k))
            cl += [s] * k
        b = np.full(len(d), 50.0)
        rej += smf_skill("n", b + np.array(d), b, lags=2, clusters=np.array(cl)).p < 0.05
    assert 0.02 <= rej / 600 <= 0.085


def test_family_holm_size_guard_and_verdicts():
    t = [smf_skill("a", np.full(20, 1.0) + np.r_[0.1, -0.1] .repeat(10), np.full(20, 3.0), 0),
         smf_skill("b", np.full(20, 3.0) + np.r_[0.1, -0.1].repeat(10), np.full(20, 1.0), 0),
         smf_skill("c", np.array([1.0, 2.0]), np.array([2.0, 3.0]), 0)]
    smf_family(t, alpha=0.05, min_units=5)
    assert t[0].verdict == "PASS" and t[1].verdict == "FAIL"
    assert t[2].verdict == "cannot be tested at this size" and np.isnan(t[2].p_holm)


def test_correlation_extra_equals_frozen_v12():
    rng = np.random.default_rng(3)
    idx = pd.date_range("2020-01-01", periods=80, freq="MS")
    x = pd.Series(rng.normal(size=80), index=idx)
    y = pd.Series(0.5 * x.to_numpy() + rng.normal(size=80), index=idx)
    a = compute_smf(x, y, max_lag_days=3, n_surrogates=99, seed=1)
    b = smf_correlation(x, y, max_lag=3, n_surrogates=99, seed=1)
    assert (a.smf_score, a.lag_days, a.p_value, a.best_corr) == (b.smf_score, b.lag_days, b.p_value, b.best_corr)
    assert a.metadata["definition"] == "lag_corrected_corr_v1.2"
    assert b.metadata["role"] == "descriptive_extra"


# ---------------------------------------------------------------- NHC parsing and pairing (synthetic lines)

def err_line(t: str, stmid: str, trk: dict, inten: dict) -> str:
    ess = ["1.00"] * 10
    tk = ["-9999.0"] * 11
    it = ["-9999.0"] * 11
    pos = {24: 2, 48: 4, 72: 6}
    for h, v in trk.items():
        tk[pos[h]] = f"{v:.1f}"
    for h, v in inten.items():
        it[pos[h]] = f"{v:.1f}"
    return " ".join([t, stmid, *ess, "25.0", "70.0", "50", *tk, *it])


def test_error_file_columns_follow_header():
    e = parse_error_file([(12, err_line("01-08-2026/12:00:00", "AL052026", {24: 30, 48: 55, 72: 90}, {48: -12}))])[0]
    assert e.stmid == "AL052026" and e.t == dt.datetime(2026, 8, 1, 12)
    assert e.trk == {24: 30.0, 48: 55.0, 72: 90.0} and e.inten[48] == -12.0 and e.inten[24] == -9999.0


def hurdat(stmid: str) -> list[tuple[int, str]]:
    out = [(1, f"{stmid},            TEST,      5,")]
    for i, h in enumerate(range(0, 96, 6)):
        t = dt.datetime(2026, 8, 1, 12) + dt.timedelta(hours=h)
        out.append((2 + i, f"{t:%Y%m%d}, {t:%H%M},  , TS, 25.0N,  70.0W,  60,  990,"
                           "   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, -999"))
    return out


def adeck(stmid: str, tau: int, lat: str, lon: str, v: int) -> str:
    return f"AL, {stmid[2:4]}, 2026080112, 03, OCD5, {tau:3d}, {lat}, {lon}, {v:3d}"


def test_pairs_and_baseline_errors():
    storms = parse_hurdat2(hurdat("AL052026"))
    errs = parse_error_file([(12, err_line("01-08-2026/12:00:00", "AL052026", {48: 55}, {48: -12}))])
    base = {"AL052026": parse_adeck_base([(7, adeck("AL052026", 48, "260N", "700W", 70))])}
    p = build_pairs(errs, storms, base, 2026)
    trk = [x for x in p if x.var == "track"][0]
    inten = [x for x in p if x.var == "intensity"][0]
    assert trk.ofcl == 55.0 and abs(trk.base - 60.0) < 0.1  # 1 degree of latitude = 60 n mi
    assert inten.ofcl == 12.0 and inten.base == 10.0
    assert build_pairs(errs, storms, base, 2025) == []


def test_score_marks_small_season_untestable():
    storms = {}
    errs, base = [], {}
    for s in range(MIN_STORMS - 1):
        sid = f"AL{s + 1:02d}2026"
        storms.update(parse_hurdat2(hurdat(sid)))
        errs += parse_error_file([(12 + s, err_line("01-08-2026/12:00:00", sid, {48: 20}, {}))])
        base[sid] = parse_adeck_base([(7, adeck(sid, 48, "260N", "700W", 70))])
    tests = score(build_pairs(errs, storms, base, 2026))
    assert len(tests) == 6 and all(t.verdict == "cannot be tested at this size" for t in tests)
    assert ALPHA == 0.025


def test_scripts_refuse_without_data():
    r = subprocess.run([sys.executable, str(ROOT / "analysis" / "smf_v2_nhc2026.py")], capture_output=True, text=True)
    assert r.returncode == 2 and "refused" in r.stdout
    if dt.date.today() < dt.date(2027, 5, 1):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "fetch_smf_v2_nhc.py"), "x"], capture_output=True, text=True)
        assert r.returncode == 2 and "refused" in r.stdout
