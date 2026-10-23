"""Fetch inputs for the SMF follow-up (docs/SMF_PROTOCOL.md §8): for each STEO
edition Jan 2010 .. Mar 2026 and lead h in (3, 6, 12), the edition's values for
T = P + h and T - 12 (total CO2 row of 9atab). Reuses the §7 parser."""
import datetime as dt
import hashlib
import io
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from fetch_steo_smf import BASE, MER, MON, get, month_columns  # noqa: E402

LEADS = (3, 6, 12)


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
            for ext in (".xlsx", ".xls"):
                try:
                    book = pd.read_excel(io.BytesIO(get(BASE + stem + ext)), sheet_name=None, header=None)
                    break
                except Exception:
                    book = None
            if book is None:
                raise RuntimeError("fetch failed")
            df = book[next(s for s in book if s.strip().lower() == "9atab")]
            codes = df.iloc[:, 0].astype(str).str.strip()
            code = "TETCCO2" if (codes == "TETCCO2").any() else "FFTCCO2"
            row = df[codes == code].iloc[0]
            cols = month_columns(df)
        except Exception as e:
            dropped.append(f"{stem}: all leads: {type(e).__name__}: {e}")
            continue
        for h in LEADS:
            T = add(year, mi + 1, h)
            if T > (2026, 6):
                continue
            Tm = add(*T, -12)
            try:
                rows.append({"edition": stem + ext, "P": f"{year}-{mi+1:02d}", "h": h, "T": f"{T[0]}-{T[1]:02d}",
                             "code": code, "F_T": float(row.iloc[cols[T]]), "F_Tm12": float(row.iloc[cols[Tm]])})
            except Exception as e:
                dropped.append(f"{stem}: h={h}: {type(e).__name__}: {e}")

out = Path("data/sources/eia_steo_co2_leads")
out.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out / "editions_leads.csv", index=False)
(out / "dropped.txt").write_text("\n".join(dropped) + ("\n" if dropped else ""))
mer_raw = get(MER)
(out / "T11_01.csv").write_bytes(mer_raw)
now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
(out / "SOURCES.json").write_text(json.dumps({
    "editions_leads.csv": {"source_url": BASE + "{mon}{yy}_base.xlsx|.xls, sheet 9atab", "downloaded_at": now,
                           "sha256": hashlib.sha256((out / "editions_leads.csv").read_bytes()).hexdigest()},
    "T11_01.csv": {"source_url": MER, "downloaded_at": now, "sha256": hashlib.sha256(mer_raw).hexdigest()}}, indent=2) + "\n")
print(f"rows {len(rows)}, dropped {len(dropped)}")
