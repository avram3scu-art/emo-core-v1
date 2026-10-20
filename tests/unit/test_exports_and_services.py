import numpy as np
import pandas as pd

import emo
from emo.services.metrics import MetricEngine


def test_package_exports_real_functions():
    for name in ["compute_organismality_index", "compute_gwi", "compute_smf",
                 "compute_information_time", "compute_gaussian_synergy"]:
        assert name in emo.__all__, name


def test_smf_from_dataframe_runs():
    rng = np.random.default_rng(0)
    truth = np.cumsum(rng.normal(size=300))
    df = pd.DataFrame({"model": truth + 0.3 * rng.normal(size=300), "realised": truth})
    out = MetricEngine().smf_from_dataframe(df, n_surrogates=49)
    assert out["smf_score"] > 0.3
