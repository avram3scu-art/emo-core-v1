"""Fetch inputs for SMF on electricity retail sales (docs/SMF_PROTOCOL.md §10).
STEO 7atab: ELTCTWH (bkWh) if present, else EXTCPUS (bkWh/day) x days in month.
Leads 3, 6, 12; editions Jan 2010 .. Mar 2026. Realised: MER Table 7.6."""
import calendar, datetime as dt, hashlib, io, json, sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from fetch_steo_smf import BASE, MON, get, month_columns  # noqa: E402

MER = "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T07.06"


def add(y, m, k):
    i = y * 12 + (m - 1) + k
    return i // 12, i % 12 + 1


rows, dropped = [], []
for year in range(2010, 2027):
    for mi in range(12):
        if (year, mi) > (2026, 2):
            break
        stem = f"{MON[mi]}{year % 100:02d}_base"
        try:
            book = None
            for ext in (".xlsx", ".xls"):
                try:
                    book = pd.read_excel(io.BytesIO(get(BASE + stem + ext)), sheet_name=None, header=None)
                    break
                except Exception:
                    pass
            if book is None:
                raise RuntimeError("fetch failed")
            df = book[next(s for s in book if s.strip().lower() == "7atab")]
            codes = df.iloc[:, 0].astype(str).str.strip()
            code = "ELTCTWH" if (codes == "ELTCTWH").any() else "EXTCPUS"
            row = df[codes == code].iloc[0]
            cols = month_columns(df)
        except Exception as e:
            dropped.append(f"{stem}: all leads: {type(e).__name__}: {e}")
            continue
        for h in (3, 6, 12):
            T = add(year, mi + 1, h)
            if T > (2026, 6):
                continue
            Tm = add(*T, -12)
            try:
                k = (lambda ym: calendar.monthrange(*ym)[1]) if code == "EXTCPUS" else (lambda ym: 1)
                rows.append({"edition": stem + ext, "P": f"{year}-{mi+1:02d}", "h": h, "T": f"{T[0]}-{T[1]:02d}",
                             "code": code, "F_T": float(row.iloc[cols[T]]) * k(T), "F_Tm12": float(row.iloc[cols[Tm]]) * k(Tm)})
            except Exception as e:
                dropped.append(f"{stem}: h={h}: {type(e).__name__}: {e}")

out = Path("data/sources/eia_steo_elec"); out.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out / "editions_elec.csv", index=False)
(out / "dropped.txt").write_text("\n".join(dropped) + ("\n" if dropped else ""))
mer_raw = get(MER)
(out / "T07_06.csv").write_bytes(mer_raw)
now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
(out / "SOURCES.json").write_text(json.dumps({
    "editions_elec.csv": {"source_url": BASE + "{mon}{yy}_base.xlsx|.xls, sheet 7atab", "downloaded_at": now,
                          "sha256": hashlib.sha256((out / "editions_elec.csv").read_bytes()).hexdigest()},
    "T07_06.csv": {"source_url": MER, "downloaded_at": now, "sha256": hashlib.sha256(mer_raw).hexdigest()}}, indent=2) + "\n")
print(f"rows {len(rows)}, dropped {len(dropped)}")
