"""Synergy (Gaussian O-information) on three real climate streams.

Pre-registered in docs/SYNERGY_PROTOCOL.md (commit e4c160c); run once.
"""
import datetime as dt
import json
from pathlib import Path

import numpy as np
import pandas as pd

from emo.synergy import compute_gaussian_synergy

SRC = Path("data/sources/synergy_climate")
MONTHS = [f"{y}-{m:02d}" for y in range(2016, 2026) for m in range(1, 13)]
T = len(MONTHS)


def _month_key(key: str, val) -> str:
    try:
        return dt.date.fromisoformat(key[:10]).strftime("%Y-%m")
    except ValueError:
        name = val.get("name", key) if isinstance(val, dict) else key
        return dt.datetime.strptime(name, "%B %Y").strftime("%Y-%m")


def load() -> tuple[pd.DataFrame, dict]:
    notes = {}
    sci = json.loads((SRC / "openalex_climate_change_monthly.json").read_text())
    science = {k: int(v["count"]) for k, v in sci.items()}

    fr = json.loads((SRC / "fedreg_climate_change_monthly.json").read_text())
    policy: dict[str, int] = {}
    for k, v in fr.items():
        c = v["count"] if isinstance(v, dict) else int(v)
        policy[_month_key(k, v)] = int(c)
    absent = [m for m in MONTHS if m not in policy]
    notes["policy_months_absent_from_facet_set_to_0"] = len(absent)
    for m in absent:
        policy[m] = 0

    attention = dict.fromkeys(MONTHS, 0)
    for t in ("Climate_change", "Global_warming"):
        items = json.loads((SRC / f"pageviews_en_{t}_monthly.json").read_text())["items"]
        got = {f"{i['timestamp'][:4]}-{i['timestamp'][4:6]}": int(i["views"]) for i in items}
        miss = [m for m in MONTHS if m not in got]
        if miss:
            raise RuntimeError(f"pageviews {t}: {len(miss)} months missing")
        for m in MONTHS:
            attention[m] += got[m]

    miss = [m for m in MONTHS if m not in science]
    if miss:
        raise RuntimeError(f"science: {len(miss)} months missing")
    df = pd.DataFrame({"science": [science[m] for m in MONTHS],
                       "policy": [policy[m] for m in MONTHS],
                       "attention": [attention[m] for m in MONTHS]}, index=MONTHS)
    return df, notes


def residuals(y: pd.DataFrame) -> pd.DataFrame:
    """OLS residuals on intercept, linear trend and 11 month dummies (§3)."""
    t = np.arange(T, dtype=float)
    month = np.array([int(m[5:]) for m in y.index])
    cols = [np.ones(T), t] + [(month == k).astype(float) for k in range(2, 13)]
    X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X, y.to_numpy(), rcond=None)
    return pd.DataFrame(y.to_numpy() - X @ beta, index=y.index, columns=y.columns)


def shifts() -> list[tuple[int, int]]:
    out = []
    for s2 in range(12, 109):
        for s3 in range(12, 109):
            d = abs(s2 - s3)
            if min(d, T - d) >= 12:
                out.append((s2, s3))
    return out


def main() -> None:
    counts, notes = load()
    y = np.log(counts + 1.0)
    e = residuals(y)

    obs = compute_gaussian_synergy(e)
    s_obs, tc_obs = obs.synergy_index, obs.total_correlation_bits
    pairs = shifts()
    s_null, tc_null = [], []
    sci, pol, att = (e[c].to_numpy() for c in ("science", "policy", "attention"))
    for s2, s3 in pairs:
        df = pd.DataFrame({"science": sci, "policy": np.roll(pol, s2), "attention": np.roll(att, s3)})
        r = compute_gaussian_synergy(df)
        s_null.append(r.synergy_index)
        tc_null.append(r.total_correlation_bits)
    s_null, tc_null = np.array(s_null), np.array(tc_null)
    n = len(pairs)
    p_syn = (1 + int((s_null >= s_obs).sum())) / (1 + n)
    p_red = (1 + int((s_null <= s_obs).sum())) / (1 + n)
    p_tc = (1 + int((tc_null >= tc_obs).sum())) / (1 + n)
    if p_syn <= 0.025:
        verdict = "PASS (synergy on real streams)"
    elif p_red <= 0.025:
        verdict = "FAIL - redundancy-dominated"
    else:
        verdict = "FAIL - no higher-order structure distinguishable from the null"

    raw = compute_gaussian_synergy(y)
    corr = e.corr()
    print("Synergy on real streams: climate change, monthly 2016-01..2025-12 (docs/SYNERGY_PROTOCOL.md)")
    print(f"T = {T}; zero-count months (science, policy, attention): "
          f"{int((counts.science == 0).sum())}, {int((counts.policy == 0).sum())}, {int((counts.attention == 0).sum())}")
    print(f"notes: {notes}")
    print("monthly count range: " + "; ".join(f"{c} {counts[c].min()}..{counts[c].max()}" for c in counts))
    print(f"S_obs (synergy index, bits) = {s_obs:.4f}   Omega = {obs.o_information_bits:.4f}")
    print(f"null: N = {n}; S_null mean {s_null.mean():.4f}, 2.5% {np.quantile(s_null, .025):.4f}, "
          f"97.5% {np.quantile(s_null, .975):.4f}")
    print(f"p_syn = {p_syn:.4f}   p_red = {p_red:.4f}")
    print(f"VERDICT: {verdict}")
    print("-- no weight on verdict --")
    print(f"TC_obs = {tc_obs:.4f} bits; null 95% {np.quantile(tc_null, .95):.4f}; p_tc = {p_tc:.4f}")
    print(f"residual correlations: sci-pol {corr.loc['science', 'policy']:.3f}, "
          f"sci-att {corr.loc['science', 'attention']:.3f}, pol-att {corr.loc['policy', 'attention']:.3f}")
    print(f"raw ln(c+1), no detrending: S = {raw.synergy_index:.4f}, TC = {raw.total_correlation_bits:.4f}")


if __name__ == "__main__":
    main()
