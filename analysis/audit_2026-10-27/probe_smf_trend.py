"""Audit 2026-10-27: false-positive rate of compute_smf on unrelated trending series.

Question: the circular-shift null keeps each series' autocorrelation, but a shift
of a trending or random-walk series creates a jump at the wrap point. Does the
p-value stay near its nominal 5% for two INDEPENDENT series that share no
relation? Pre-stated expectation for a valid null: rejection rate about 0.05.
Synthetic only; 200 replications per condition; seed fixed.
Run: PYTHONPATH=. python analysis/audit_2026-10-27/probe_smf_trend.py
"""

import numpy as np
import pandas as pd

from emo.smf import compute_smf

rng = np.random.default_rng(20261027)
N_REP, N = 200, 120  # 10 years of monthly data

conds = {
    "white noise (control)": lambda: rng.normal(size=N),
    "independent random walks": lambda: np.cumsum(rng.normal(size=N)),
    "independent linear trends + noise": lambda: np.arange(N) * rng.uniform(0.02, 0.1) + rng.normal(size=N),
}
idx = pd.RangeIndex(N)
for name, gen in conds.items():
    rej = 0
    for _ in range(N_REP):
        res = compute_smf(pd.Series(gen(), idx), pd.Series(gen(), idx), n_surrogates=199, seed=int(rng.integers(1e9)))
        rej += res.p_value <= 0.05
    print(f"{name}: rejection rate at alpha 0.05 = {rej / N_REP:.3f} ({rej}/{N_REP})")
