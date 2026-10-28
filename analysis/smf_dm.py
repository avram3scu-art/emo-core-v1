"""SMF §13: Diebold–Mariano re-analysis of the deciding condition (docs/SMF_PROTOCOL.md §13). Run once.

Series rebuilt exactly as in analysis/smf_steo_leads.py (§8), smf_steo_elec.py (§10),
smf_spf.py (§11) and smf_ip.py (§12): same files, same 2020-21 exclusion (primary samples).
Committed data only, no refetch.
"""
import numpy as np
import pandas as pd

from emo.smf import compute_smf, diebold_mariano, holm


def eia_monthly(editions: pd.DataFrame, R: pd.Series, h: int) -> pd.DataFrame:
    e = editions[editions["h"] == h]
    T = pd.PeriodIndex(e["T"], freq="M")
    d = pd.DataFrame({"model": np.log(e["F_T"].to_numpy()) - np.log(e["F_Tm12"].to_numpy()),
                      "realised": np.log(R.reindex(T).to_numpy()) - np.log(R.reindex(T - 12).to_numpy())},
                     index=T.to_timestamp()).dropna().sort_index()
    cov = (d.index >= "2020-03-01") & (d.index <= "2021-12-01")
    return d[~cov]


def mer(path: str, desc: str) -> pd.Series:
    m = pd.read_csv(path, dtype={"YYYYMM": str})
    m = m[(m["Description"] == desc) & ~m["YYYYMM"].str.endswith("13")]
    idx = pd.PeriodIndex([f"{y[:4]}-{y[4:]}" for y in m["YYYYMM"]], freq="M")
    return pd.to_numeric(m.set_index(idx)["Value"], errors="coerce")


def spf(u: pd.DataFrame, name: str, R: pd.Series, h: int, log: bool) -> pd.DataFrame:
    q = pd.PeriodIndex([pd.Period(year=int(y), quarter=int(k), freq="Q") for y, k in zip(u["YEAR"], u["QUARTER"], strict=True)])
    T = q + h
    keep = T <= pd.Period("2026Q3", freq="Q")
    f = np.log if log else (lambda x: x)
    d = pd.DataFrame({"model": (f(u[f"{name}{h + 2}"]) - f(u[f"{name}1"])).to_numpy(),
                      "realised": f(R.reindex(T).to_numpy()) - f(R.reindex(q - 1).to_numpy())},
                     index=T.to_timestamp())[keep].dropna()
    cov = (d.index >= "2020-01-01") & (d.index < "2022-01-01")
    return d[~cov]


samples: list[tuple[str, pd.DataFrame, int]] = []

# §8 EIA CO2
D = "data/sources/eia_steo_co2_leads/"
R = mer(D + "T11_01.csv", "Total Energy CO2 Emissions")
ed = pd.read_csv(D + "editions_leads.csv")
for h in (3, 6, 12):
    samples.append((f"§8 EIA CO2 {h}m", eia_monthly(ed, R, h), max(11, h + 1)))
# §10 EIA electricity
D = "data/sources/eia_steo_elec/"
R = mer(D + "T07_06.csv", "Electricity Sales to Ultimate Customers, Total")
ed = pd.read_csv(D + "editions_elec.csv")
for h in (3, 6, 12):
    samples.append((f"§10 EIA electricity {h}m", eia_monthly(ed, R, h), max(11, h + 1)))
# §11 SPF unemployment
D = "data/sources/spf_unemp/"
u = pd.read_excel(D + "medianLevel.xlsx", sheet_name="UNEMP")
f = pd.read_csv(D + "UNRATE.csv")
f["q"] = pd.PeriodIndex(pd.to_datetime(f.iloc[:, 0]), freq="Q")
cnt = f.groupby("q").size()
Rq = f.groupby("q")["UNRATE"].mean()[cnt == 3]
for h in (1, 2, 4):
    samples.append((f"§11 SPF unemployment {h}q", spf(u, "UNEMP", Rq, h, log=False), h))
# §12 industrial production
D = "data/sources/smf_ip/"
f = pd.read_csv(D + "INDPRO.csv")
dates = pd.to_datetime(f.iloc[:, 0])
Rm = pd.Series(pd.to_numeric(f["INDPRO"], errors="coerce").to_numpy(), index=pd.PeriodIndex(dates, freq="M"))
q_of = pd.PeriodIndex(dates, freq="Q")
cnt = pd.Series(1, index=q_of).groupby(level=0).sum()
Rq = pd.Series(Rm.to_numpy(), index=q_of).groupby(level=0).mean()[cnt == 3]
ed = pd.read_csv(D + "steo_ip_editions.csv")
for h in (3, 6, 12):
    samples.append((f"§12 EIA IP {h}m", eia_monthly(ed, Rm, h), max(11, h + 1)))
u = pd.read_excel(D + "medianLevel.xlsx", sheet_name="INDPROD")
for c in u.columns[2:]:
    u[c] = pd.to_numeric(u[c], errors="coerce")
for h in (1, 2, 4):
    samples.append((f"§12 SPF IP {h}q", spf(u, "INDPROD", Rq, h, log=True), h))

rows = []
for name, d, L in samples:
    r = diebold_mariano(((d["model"] - d["realised"]) ** 2).to_numpy(), (d["realised"] ** 2).to_numpy(), L)
    s = compute_smf(d["model"], d["realised"], max_lag_days=0, n_surrogates=999, seed=0)
    ratio = float(((d["model"] - d["realised"]) ** 2).mean() / (d["realised"] ** 2).mean())
    rows.append((name, d, L, r, s, ratio))
adj = holm([r["p"] for _, _, _, r, _, _ in rows])

print("SMF §13: Diebold-Mariano (HLN) vs 'no change', one-sided; Holm over 15; alpha 0.05")
print(f"{'sample':28s} {'n':>4s} {'L':>3s} {'MSE ratio':>9s} {'DM':>7s} {'HLN':>7s} {'p':>8s} {'p_Holm':>8s}  old-conds  DM  verdict")
for (name, d, L, r, s, ratio), pa in zip(rows, adj, strict=True):
    old = s.p_value < 0.05 / 3 and s.smf_score > 0
    dm_pass = pa < 0.05
    verdict = "PASS" if old and dm_pass else "FAIL"
    print(f"{name:28s} {len(d):4d} {L:3d} {ratio:9.3f} {r['dm']:7.2f} {r['hln']:7.2f} {r['p']:8.4f} {pa:8.4f}  "
          f"{'yes' if old else 'no ':3s}        {'yes' if dm_pass else 'no ':3s} {verdict}")
