"""SMF on electricity retail sales (docs/SMF_PROTOCOL.md §10). Run once."""
import numpy as np
import pandas as pd
from emo.smf import compute_smf

D = "data/sources/eia_steo_elec/"
ed = pd.read_csv(D + "editions_elec.csv")
dropped = [l for l in open(D + "dropped.txt").read().splitlines() if l]
for d in dropped:
    print("dropped:", d)
mer = pd.read_csv(D + "T07_06.csv", dtype={"YYYYMM": str})
mer = mer[(mer["Description"] == "Electricity Sales to Ultimate Customers, Total") & ~mer["YYYYMM"].str.endswith("13")]
R = pd.to_numeric(mer.set_index(pd.PeriodIndex([f"{y[:4]}-{y[4:]}" for y in mer["YYYYMM"]], freq="M"))["Value"], errors="coerce")
ALPHA = 0.05 / 3


def months(a, b):  # editions Jan 2010 .. P = 2026-06 minus h
    return (b[0] - a[0]) * 12 + b[1] - a[1] + 1


for h in (3, 6, 12):
    e = ed[ed["h"] == h]
    last = pd.Period("2026-06", freq="M") - h
    expected = months((2010, 1), (last.year, last.month))
    n_drop = expected - len(e)
    print(f"\n=== lead h={h}: editions expected {expected}, used {len(e)}, dropped {n_drop}")
    if n_drop > 0.10 * expected:
        print("  NOT RUN: more than 10% dropped"); continue
    T = pd.PeriodIndex(e["T"], freq="M")
    model = pd.Series(np.log(e["F_T"].to_numpy()) - np.log(e["F_Tm12"].to_numpy()), index=T)
    real = pd.Series(np.log(R.reindex(T).to_numpy()) - np.log(R.reindex(T - 12).to_numpy()), index=T)
    P = T - h
    naive = pd.Series(np.log(R.reindex(P).to_numpy()) - np.log(R.reindex(P - 12).to_numpy()), index=T)
    df = pd.DataFrame({"model": model, "realised": real, "naive": naive}).dropna().sort_index()
    df.index = df.index.to_timestamp()
    covid = (df.index >= "2020-03-01") & (df.index <= "2021-12-01")
    for label, d in (("PRIMARY (without 2020-03..2021-12)", df[~covid]), ("full sample, no weight", df)):
        r = compute_smf(d["model"], d["realised"], max_lag_days=0, n_surrogates=999, seed=0)
        mse_m = float(((d["model"] - d["realised"]) ** 2).mean())
        mse_0 = float((d["realised"] ** 2).mean())
        mse_n = float(((d["naive"] - d["realised"]) ** 2).mean())
        c = {"p<0.0167": r.p_value < ALPHA, "SMF>0": r.smf_score > 0, "MSE_model<MSE_zero": mse_m < mse_0}
        v = "PASS" if all(c.values()) else "FAIL (" + ", ".join(k for k, ok in c.items() if not ok) + " not met)"
        print(f"  [{label}] n={len(d)} T {d.index.min():%Y-%m}..{d.index.max():%Y-%m}")
        print(f"    corr={r.best_corr:.3f} null95={r.null_corr_95:.3f} smf={r.smf_score:.3f} p={r.p_value:.4f} "
              f"n_null={r.extra.get('n_null', 0):.0f} p_min={r.extra.get('p_min', 1):.4f}")
        print(f"    MSE_model/MSE_zero={mse_m / mse_0:.3f}  MSE_model/MSE_persistence={mse_m / mse_n:.3f}")
        print(f"    verdict: {v}" + ("" if label.startswith("PRIMARY") else " (no weight)"))
print("\ncodes used:", dict(ed["code"].value_counts()))
