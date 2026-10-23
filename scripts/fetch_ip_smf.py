"""Fetch inputs for SMF on industrial production (docs/SMF_PROTOCOL.md §12):
STEO 9atab row ZOTOIUS (leads 3, 6, 12; editions Jan 2010 .. Mar 2026), SPF
medianLevel.xlsx (sheet INDPROD used), FRED INDPRO."""
import datetime as dt
import hashlib
import io
import json
import sys
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from fetch_steo_smf import BASE, MON, UA, get, month_columns  # noqa: E402

SPF = ("https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/"
       "historical-data/medianLevel.xlsx?sc_lang=en&hash=E52F5DEF4551C3EBD24031A04CE6E98A")
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDPRO"


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
            df = book[next(s for s in book if s.strip().lower() == "9atab")]
            codes = df.iloc[:, 0].astype(str).str.strip()
            row = df[codes == "ZOTOIUS"].iloc[0]
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
                rows.append({"edition": stem + ext, "P": f"{year}-{mi+1:02d}", "h": h, "T": f"{T[0]}-{T[1]:02d}",
                             "code": "ZOTOIUS", "F_T": float(row.iloc[cols[T]]), "F_Tm12": float(row.iloc[cols[Tm]])})
            except Exception as e:
                dropped.append(f"{stem}: h={h}: {type(e).__name__}: {e}")

out = Path("data/sources/smf_ip")
out.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out / "steo_ip_editions.csv", index=False)
(out / "steo_dropped.txt").write_text("\n".join(dropped) + ("\n" if dropped else ""))
now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
src = {"steo_ip_editions.csv": {"source_url": BASE + "{mon}{yy}_base.xlsx|.xls, sheet 9atab, row ZOTOIUS", "downloaded_at": now,
                                "sha256": hashlib.sha256((out / "steo_ip_editions.csv").read_bytes()).hexdigest()}}
for name, url in (("medianLevel.xlsx", SPF), ("INDPRO.csv", FRED)):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
    (out / name).write_bytes(raw)
    src[name] = {"source_url": url, "downloaded_at": now, "sha256": hashlib.sha256(raw).hexdigest()}
(out / "SOURCES.json").write_text(json.dumps(src, indent=2) + "\n")
print(f"STEO rows {len(rows)}, dropped {len(dropped)}")
