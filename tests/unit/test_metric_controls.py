"""
Noise and signal controls for GWI, SMF and information-time.

Each metric must score (near) zero on pure noise and clearly above zero on
a planted signal. These are the M = 0 controls of the EMO metrics.
"""
import numpy as np
import pandas as pd

from emo.gwi import compute_gwi
from emo.info_time import compute_information_time
from emo.smf import compute_smf

T = pd.date_range("2020-01-01", periods=730, freq="D")


# --- GWI -----------------------------------------------------------------

def test_gwi_finds_no_ignitions_in_independent_noise():
    false_events = 0
    for seed in range(20):
        rng = np.random.default_rng(seed)
        df = pd.DataFrame(rng.normal(size=(len(T), 5)), index=T, columns=list("abcde"))
        false_events += len(compute_gwi(df).events)
    assert false_events <= 2  # expected about 1 across 20 runs at alpha = 0.05


def test_gwi_detects_planted_simultaneous_spikes():
    rng = np.random.default_rng(1)
    df = pd.DataFrame(rng.normal(size=(len(T), 5)), index=T, columns=list("abcde"))
    planted = T[[100, 300, 500]]
    df.loc[planted] += 4.0
    events = compute_gwi(df).events
    assert set(planted).issubset(set(events))


def test_gwi_does_not_fire_on_a_spike_in_one_stream():
    rng = np.random.default_rng(2)
    df = pd.DataFrame(rng.normal(size=(len(T), 5)), index=T, columns=list("abcde"))
    df.iloc[200, 0] += 10.0
    assert T[200] not in compute_gwi(df).events


# --- SMF -----------------------------------------------------------------

def test_smf_is_zero_for_unrelated_noise_most_of_the_time():
    zeros = 0
    for seed in range(20):
        rng = np.random.default_rng(seed)
        r = compute_smf(pd.Series(rng.normal(size=400)), pd.Series(rng.normal(size=400)),
                        max_lag_days=30, n_surrogates=99, seed=seed)
        zeros += r.smf_score == 0.0
    assert zeros >= 16  # about 95% expected


def test_smf_detects_a_model_that_tracks_reality_with_a_lag():
    rng = np.random.default_rng(3)
    truth = np.cumsum(rng.normal(size=420))
    model = pd.Series(truth[:400] + 0.5 * rng.normal(size=400))
    realised = pd.Series(truth[7:407])  # model leads reality by 7 steps
    r = compute_smf(model, realised, max_lag_days=30, n_surrogates=99)
    assert r.smf_score > 0.3
    assert r.p_value <= 0.05


def test_smf_null_uses_each_shift_once_and_reports_the_p_floor():
    # n = 25 annual points: admissible shifts 10..15, i.e. 6 distinct surrogates.
    rng = np.random.default_rng(0)
    x = np.cumsum(rng.normal(size=25))
    r = compute_smf(pd.Series(x), pd.Series(x + 0.1 * rng.normal(size=25)), n_surrogates=199)
    assert r.extra["n_null"] == 6
    assert r.extra["p_min"] == 1 / 7
    assert r.p_value >= 1 / 7  # v1.1 could report 1/200 here


def test_smf_null_is_capped_without_replacement_for_long_series():
    rng = np.random.default_rng(1)
    r = compute_smf(pd.Series(rng.normal(size=400)), pd.Series(rng.normal(size=400)), n_surrogates=99)
    assert r.extra["n_null"] == 99
    assert r.extra["p_min"] == 0.01


# --- Information-time ---------------------------------------------------

def test_tau_i_is_zero_for_flat_noisy_skill():
    zeros = 0
    for seed in range(20):
        rng = np.random.default_rng(seed)
        zeros += compute_information_time(pd.Series(0.65 + 0.05 * rng.normal(size=100))).tau_i == 0.0
    assert zeros >= 18


def test_tau_i_credits_steady_improvement():
    rng = np.random.default_rng(4)
    s = pd.Series(np.linspace(0.6, 0.7, 100) + 0.005 * rng.normal(size=100))
    r = compute_information_time(s)
    assert r.tau_i > 0.0
    assert abs(r.slope - 0.1 / 99) < 0.0003
