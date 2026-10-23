"""SMF test on EIA STEO forecasts (docs/SMF_PROTOCOL.md). Run once."""
import numpy as np
import pandas as pd
from emo.smf import compute_smf

ed = pd.read_csv("data/sources/eia_steo_co2/editions.csv")
dropped = [l for l in open("data/sources/eia_steo_co2/dropped.txt").read().splitlines() if l]
n_exp = 16 * 12 - 6  # Jan 2010 .. Jun 2025
print(f"editions expected {n_exp}, parsed {len(ed)}, dropped {len(dropped)}")
for d in dropped:
    print("  dropped:", d)
if len(dropped) > 0.10 * n_exp:
    print("NOT RUN: more than 10% of editions dropped (protocol §4)")
    raise SystemExit(0)

mer = pd.read_csv("data/sources/eia_mer_t11_01/T11_01.csv", dtype={"YYYYMM": str})
mer = mer[(mer["Description"] == "Total Energy CO2 Emissions") & ~mer["YYYYMM"].str.endswith("13")]
R = pd.to_numeric(mer.set_index(pd.PeriodIndex([f"{y[:4]}-{y[4:]}" for y in mer["YYYYMM"]], freq="M"))["Value"], errors="coerce")

P = pd.PeriodIndex(ed["P"], freq="M")
T = pd.PeriodIndex(ed["T"], freq="M")
model = pd.Series(np.log(ed["F_T"].to_numpy()) - np.log(ed["F_P"].to_numpy()), index=T)
realised = pd.Series(np.log(R.reindex(T).to_numpy()) - np.log(R.reindex(P).to_numpy()), index=T)
naive = pd.Series(np.log(R.reindex(P).to_numpy()) - np.log(R.reindex(P - 12).to_numpy()), index=T)
df = pd.DataFrame({"model": model, "realised": realised, "naive": naive}).dropna().sort_index()
df.index = df.index.to_timestamp()


def run(d, label):
    r = compute_smf(d["model"], d["realised"], max_lag_days=0, n_surrogates=999, seed=0)
    rn = compute_smf(d["naive"], d["realised"], max_lag_days=0, n_surrogates=999, seed=0)
    mse_m = float(((d["model"] - d["realised"]) ** 2).mean())
    mse_n = float(((d["naive"] - d["realised"]) ** 2).mean())
    c = {"p<0.05": r.p_value < 0.05, "SMF>0": r.smf_score > 0, "MSE_model<MSE_naive": mse_m < mse_n}
    verdict = "PASS" if all(c.values()) else "FAIL (" + ", ".join(k for k, v in c.items() if not v) + " not met)"
    print(f"[{label}] n={len(d)} T {d.index.min():%Y-%m}..{d.index.max():%Y-%m}")
    print(f"  best_corr={r.best_corr:.3f} null_corr_95={r.null_corr_95:.3f} smf={r.smf_score:.3f} "
          f"p={r.p_value:.4f} n_null={r.extra.get('n_null'):.0f} p_min={r.extra.get('p_min'):.4f}")
    print(f"  MSE_model={mse_m:.6f} MSE_naive={mse_n:.6f} ratio={mse_m / mse_n:.3f}")
    print(f"  naive vs realised: corr={rn.best_corr:.3f} smf={rn.smf_score:.3f} p={rn.p_value:.4f}")
    print(f"  verdict: {verdict}")


print("codes used:", dict(ed["code"].value_counts()))
run(df, "primary")
covid = (df.index >= "2020-03-01") & (df.index <= "2021-12-01")
run(df[~covid], "secondary: without 2020-03..2021-12 (no weight)")
