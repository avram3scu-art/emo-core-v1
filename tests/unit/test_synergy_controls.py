"""
Control tests for Gaussian O-information (emo.synergy).

Each test feeds data where the right answer is known in advance:
independent streams, pure redundancy, pure synergy, and an exact
analytic value. A metric that fails these cannot be trusted on real data.
"""
import numpy as np
import pandas as pd

from emo.synergy import compute_gaussian_synergy

N = 20000


def _df(cols):
    return pd.DataFrame(cols)


def test_independent_streams_score_zero():
    rng = np.random.default_rng(1)
    r = compute_gaussian_synergy(_df({k: rng.normal(size=N) for k in "abcd"}))
    assert abs(r.o_information_bits) < 0.01
    assert r.total_correlation_bits < 0.01


def test_redundant_streams_are_redundancy_dominated():
    # Three noisy copies of one common driver: the same information, repeated.
    rng = np.random.default_rng(2)
    z = rng.normal(size=N)
    r = compute_gaussian_synergy(_df({k: z + 0.5 * rng.normal(size=N) for k in "abc"}))
    assert r.o_information_bits > 0.3
    assert r.synergy_index < -0.3


def test_sum_of_independent_causes_is_synergy_dominated():
    # c = a + b: a and b are independent, only the triple carries the relation.
    rng = np.random.default_rng(3)
    a, b = rng.normal(size=N), rng.normal(size=N)
    c = a + b + 0.3 * rng.normal(size=N)
    r = compute_gaussian_synergy(_df({"a": a, "b": b, "c": c}))
    assert r.o_information_bits < -0.3
    assert r.synergy_index > 0.3


def test_matches_direct_entropy_formula():
    # Independent check: Ω = (n-2)H(X) + Σ_j [H(X_j) - H(X_-j)] with full
    # Gaussian entropies (2πe constants kept), on an exact covariance.
    rng = np.random.default_rng(4)
    a = rng.normal(size=(4, 4))
    cov = a @ a.T + 0.5 * np.eye(4)
    sd = np.sqrt(np.diag(cov))
    corr = cov / np.outer(sd, sd)

    def h(c):
        k = c.shape[0]
        return 0.5 * np.log2((2 * np.pi * np.e) ** k * np.linalg.det(c))

    n = 4
    omega = (n - 2) * h(cov)
    for j in range(n):
        idx = [i for i in range(n) if i != j]
        omega += h(cov[[j]][:, [j]]) - h(cov[np.ix_(idx, idx)])

    x = rng.multivariate_normal(np.zeros(4), corr, size=400000)
    r = compute_gaussian_synergy(pd.DataFrame(x, columns=list("abcd")))
    assert abs(r.o_information_bits - omega) < 0.02


def test_two_streams_are_degenerate():
    rng = np.random.default_rng(5)
    r = compute_gaussian_synergy(_df({"a": rng.normal(size=100), "b": rng.normal(size=100)}))
    assert r.synergy_index == 0.0
    assert r.metadata["definition"].startswith("degenerate")
