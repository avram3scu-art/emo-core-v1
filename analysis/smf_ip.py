"""SMF on industrial production, EIA STEO and SPF (docs/SMF_PROTOCOL.md §12). Run once."""
import numpy as np
import pandas as pd
from emo.smf import compute_smf

D = "data/sources/smf_ip/"
ALPHA = 0.05 / 3
f = pd.read_csv(D + "INDPRO.csv")
dates = pd.to_datetime(f.iloc[:, 0])
Rm = pd.Series(pd.to_numeric(f["INDPRO"], errors="coerce").to_numpy(), index=pd.PeriodIndex(dates, freq="M"))
q_of = pd.PeriodIndex(dates, freq="Q")
cnt = pd.Series(1, index=q_of).groupby(level=0).sum()
Rq = pd.Series(Rm.to_numpy(), index=q_of).groupby(level=0).mean()[cnt == 3]
verdicts = {}


def test(d, label, key, primary):
    r = compute_smf(d["model"], d["realised"], max_lag_days=0, n_surrogates=999, seed=0)
    mse_m = float(((d["model"] - d["realised"]) ** 2).mean()); mse_0 = float((d["realised"] ** 2).mean())
    c = {"p<0.0167": r.p_value < ALPHA, "SMF>0": r.smf_score > 0, "MSE_model<MSE_zero": mse_m < mse_0}
    v = "PASS" if all(c.values()) else "FAIL (" + ", ".join(k for k, ok in c.items() if not ok) + " not met)"
    if primary:
        verdicts[key] = v.split()[0]
    print(f"  [{label}] n={len(d)} T {d.index.min():%Y-%m}..{d.index.max():%Y-%m}")
    print(f"    corr={r.best_corr:.3f} null95={r.null_corr_95:.3f} smf={r.smf_score:.3f} p={r.p_value:.4f} "
          f"n_null={r.extra.get('n_null', 0):.0f} p_min={r.extra.get('p_min', 1):.4f}")
    print(f"    MSE_model/MSE_zero={mse_m / mse_0:.3f}\n    verdict: {v}" + ("" if primary else " (no weight)"))


print("##### EIA STEO, ZOTOIUS")
ed = pd.read_csv(D + "steo_ip_editions.csv")
for l in open(D + "steo_dropped.txt").read().splitlines():
    if l:
        print("dropped:", l)
for h in (3, 6, 12):
    e = ed[ed["h"] == h]
    last = pd.Period("2026-06", freq="M") - h
    expected = (last.year - 2010) * 12 + last.month
    print(f"\n=== EIA lead {h} months: editions expected {expected}, used {len(e)}, dropped {expected - len(e)}")
    if expected - len(e) > 0.10 * expected:
        print("  NOT RUN"); continue
    T = pd.PeriodIndex(e["T"], freq="M")
    d = pd.DataFrame({"model": np.log(e["F_T"].to_numpy()) - np.log(e["F_Tm12"].to_numpy()),
                      "realised": np.log(Rm.reindex(T).to_numpy()) - np.log(Rm.reindex(T - 12).to_numpy())},
                     index=T.to_timestamp()).dropna().sort_index()
    cov = (d.index >= "2020-03-01") & (d.index <= "2021-12-01")
    test(d[~cov], "PRIMARY (without 2020-03..2021-12)", f"EIA {h}m", True)
    test(d, "full sample", None, False)

print("\n##### SPF median, INDPROD")
try:
    u = pd.read_excel(D + "medianLevel.xlsx", sheet_name="INDPROD")
    need = ["YEAR", "QUARTER", "INDPROD1", "INDPROD3", "INDPROD4", "INDPROD6"]
    missing = [c for c in need if c not in u.columns]
    if missing:
        raise KeyError(f"columns missing {missing}; columns are {list(u.columns)}")
except Exception as ex:
    print("SPF NOT RUN (layout differs from assumption, §12):", ex); u = None
if u is not None:
    for c in u.columns[2:]:
        u[c] = pd.to_numeric(u[c], errors="coerce")
    q = pd.PeriodIndex([pd.Period(year=int(y), quarter=int(k), freq="Q") for y, k in zip(u["YEAR"], u["QUARTER"])])
    for h in (1, 2, 4):
        col = f"INDPROD{h + 2}"
        T = q + h
        keep = T <= pd.Period("2026Q3", freq="Q")
        expected = int(keep.sum())
        d = pd.DataFrame({"model": (np.log(u[col]) - np.log(u["INDPROD1"])).to_numpy(),
                          "realised": np.log(Rq.reindex(T).to_numpy()) - np.log(Rq.reindex(q - 1).to_numpy())},
                         index=T.to_timestamp())[keep].dropna()
        print(f"\n=== SPF horizon {h} quarter(s) ({col}): surveys expected {expected}, used {len(d)}, dropped {expected - len(d)}")
        if expected - len(d) > 0.10 * expected:
            print("  NOT RUN"); continue
        cov = (d.index >= "2020-01-01") & (d.index < "2022-01-01")
        test(d[~cov], "PRIMARY (without 2020Q1..2021Q4)", f"SPF {h}q", True)
        test(d, "full sample", None, False)

print("\n##### Profile (primary):", verdicts)
e12, s4 = verdicts.get("EIA 12m"), verdicts.get("SPF 4q")
reading = {("FAIL", "PASS"): "forecaster effect", ("FAIL", "FAIL"): "variable effect",
           ("PASS", "PASS"): "EIA energy failure is specific to energy variables",
           ("PASS", "FAIL"): "EIA PASS, SPF FAIL: reported as found, no reading"}.get((e12, s4), "not decidable (a test was not run)")
print("Reading rule (§12):", reading)
