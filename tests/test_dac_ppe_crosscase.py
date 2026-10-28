"""F9: the rank-pattern search in analysis/dac_ppe_crosscase.py equals brute force over every integer date."""

import importlib.util
import itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cc", ROOT / "analysis/dac_ppe_crosscase.py")
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)


def brute(wx, wy):
    vals = []
    for x in itertools.product(*[range(lo, hi + 1) for lo, hi in wx]):
        rx = cc.ranks(list(x))
        for y in itertools.product(*[range(lo, hi + 1) for lo, hi in wy]):
            v = cc.spearman_ranks(rx, cc.ranks(list(y)))
            if v is not None:
                vals.append(v)
    return min(vals), max(vals)


def test_rank_search_equals_brute_force():
    # BE reading C, DE reading A, NL, SE (first order, first delivery), days from t0
    wx = [(34, 34), (29, 39), (36, 39), (2, 30)]
    wy = [(46, 46), (41, 50), (51, 52), (47, 61)]
    a, b = cc.range_over(wx, wy), brute(wx, wy)
    assert abs(a[0] - b[0]) < 1e-12 and abs(a[1] - b[1]) < 1e-12, (a, b)


def test_spread_equals_brute_force():
    w = [(46, 46), (41, 50), (51, 52), (47, 61)]
    s = [max(x) - min(x) for x in itertools.product(*[range(lo, hi + 1) for lo, hi in w])]
    assert cc.spread(w) == (min(s), max(s))
