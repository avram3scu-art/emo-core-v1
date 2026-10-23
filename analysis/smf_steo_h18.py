"""SMF lead 18 (docs/SMF_PROTOCOL.md §9). Run once. Realised: the MER file
fetched for §8 (data/sources/eia_steo_co2_leads/T11_01.csv)."""
import numpy as np
import pandas as pd
from emo.smf import compute_smf

e = pd.read_csv("data/sources/eia_steo_co2_h18/editions_h18.csv")
dropped = [l for l in open("data/sources/eia_steo_co2_h18/dropped.txt").read().splitlines() if l]
print(f"editions expected 90, used {len(e)}, dropped {len(dropped)}")
for d in dropped:
    print("  dropped:", d)
if len(dropped) > 9:
    print("NOT RUN: more than 10% dropped"); raise SystemExit(0)
mer = pd.read_csv("data/sources/eia_steo_co2_leads/T11_01.csv", dtype={"YYYYMM": str})
mer = mer[(mer["Description"] == "Total Energy CO2 Emissions") & ~mer["YYYYMM"].str.endswith("13")]
R = pd.to_numeric(mer.set_index(pd.PeriodIndex([f"{y[:4]}-{y[4:]}" for y in mer["YYYYMM"]], freq="M"))["Value"], errors="coerce")
T = pd.PeriodIndex(e["T"], freq="M")
model = pd.Series(np.log(e["F_T"].to_numpy()) - np.log(e["F_Tm12"].to_numpy()), index=T)
real = pd.Series(np.log(R.reindex(T).to_numpy()) - np.log(R.reindex(T - 12).to_numpy()), index=T)
df = pd.DataFrame({"model": model, "realised": real}).dropna().sort_index()
df.index = df.index.to_timestamp()
covid = (df.index >= "2020-03-01") & (df.index <= "2021-12-01")
for label, d in (("PRIMARY (without 2020-03..2021-12)", df[~covid]), ("full sample, no weight", df)):
    r = compute_smf(d["model"], d["realised"], max_lag_days=0, n_surrogates=999, seed=0)
    mse_m = float(((d["model"] - d["realised"]) ** 2).mean()); mse_0 = float((d["realised"] ** 2).mean())
    c = {"p<0.05": r.p_value < 0.05, "SMF>0": r.smf_score > 0, "MSE_model<MSE_zero": mse_m < mse_0}
    v = "PASS" if all(c.values()) else "FAIL (" + ", ".join(k for k, ok in c.items() if not ok) + " not met)"
    print(f"[{label}] n={len(d)} T {d.index.min():%Y-%m}..{d.index.max():%Y-%m}")
    print(f"  corr={r.best_corr:.3f} null95={r.null_corr_95:.3f} smf={r.smf_score:.3f} p={r.p_value:.4f} "
          f"n_null={r.extra.get('n_null', 0):.0f} p_min={r.extra.get('p_min', 1):.4f}")
    print(f"  MSE_model/MSE_zero={mse_m / mse_0:.3f}\n  verdict: {v}" + ("" if label.startswith("PRIMARY") else " (no weight)"))
