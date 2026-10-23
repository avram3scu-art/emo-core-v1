"""SMF on SPF median unemployment forecasts (docs/SMF_PROTOCOL.md §11). Run once."""
import pandas as pd
from emo.smf import compute_smf

D = "data/sources/spf_unemp/"
u = pd.read_excel(D + "medianLevel.xlsx", sheet_name="UNEMP")
f = pd.read_csv(D + "UNRATE.csv")
f["q"] = pd.PeriodIndex(pd.to_datetime(f.iloc[:, 0]), freq="Q")
counts = f.groupby("q").size()
R = f.groupby("q")["UNRATE"].mean()[counts == 3]  # complete quarters only
q = pd.PeriodIndex([pd.Period(year=int(y), quarter=int(k), freq="Q") for y, k in zip(u["YEAR"], u["QUARTER"])])
u.index = q
last = pd.Period("2026Q3", freq="Q")
ALPHA = 0.05 / 3

for h in (1, 2, 4):
    col = f"UNEMP{h + 2}"
    T = q + h
    keep = T <= last
    expected = int(keep.sum())
    d = pd.DataFrame({"model": (u[col] - u["UNEMP1"]).to_numpy(),
                      "realised": (R.reindex(T).to_numpy() - R.reindex(q - 1).to_numpy())},
                     index=T.to_timestamp())[keep].dropna()
    n_drop = expected - len(d)
    print(f"\n=== horizon h={h} quarter(s) ({col}): surveys expected {expected}, used {len(d)}, dropped {n_drop}")
    if n_drop > 0.10 * expected:
        print("  NOT RUN: more than 10% dropped"); continue
    covid = (d.index >= "2020-01-01") & (d.index < "2022-01-01")
    for label, x in (("PRIMARY (without 2020Q1..2021Q4)", d[~covid]), ("full sample, no weight", d),
                     ("surveys 2010Q1+, without 2020-21, no weight", d[~covid & ((d.index.to_period("Q") - h) >= pd.Period("2010Q1", freq="Q"))])):
        r = compute_smf(x["model"], x["realised"], max_lag_days=0, n_surrogates=999, seed=0)
        mse_m = float(((x["model"] - x["realised"]) ** 2).mean()); mse_0 = float((x["realised"] ** 2).mean())
        c = {"p<0.0167": r.p_value < ALPHA, "SMF>0": r.smf_score > 0, "MSE_model<MSE_zero": mse_m < mse_0}
        v = "PASS" if all(c.values()) else "FAIL (" + ", ".join(k for k, ok in c.items() if not ok) + " not met)"
        print(f"  [{label}] n={len(x)} T {x.index.min():%Y-%m}..{x.index.max():%Y-%m}")
        print(f"    corr={r.best_corr:.3f} null95={r.null_corr_95:.3f} smf={r.smf_score:.3f} p={r.p_value:.4f} "
              f"n_null={r.extra.get('n_null', 0):.0f} p_min={r.extra.get('p_min', 1):.4f}")
        print(f"    MSE_model/MSE_zero={mse_m / mse_0:.3f}\n    verdict: {v}" + ("" if label.startswith("PRIMARY") else " (no weight)"))
