"""Fetch inputs for SMF lead 18 (docs/SMF_PROTOCOL.md §9): Jan-Jun STEO editions
2010-2024, values for T = P + 18 and T - 12 = P + 6. Same parser as §7/§8."""
import io
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from fetch_steo_smf import BASE, MON, get, month_columns  # noqa: E402

rows, dropped = [], []
for year in range(2010, 2025):
    for mi in range(6):
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
            code = "TETCCO2" if (codes == "TETCCO2").any() else "FFTCCO2"
            row = df[codes == code].iloc[0]
            cols = month_columns(df)
            i = year * 12 + mi + 18
            T, Tm = (i // 12, i % 12 + 1), ((i - 12) // 12, (i - 12) % 12 + 1)
            rows.append({"edition": stem + ext, "P": f"{year}-{mi+1:02d}", "h": 18, "T": f"{T[0]}-{T[1]:02d}",
                         "code": code, "F_T": float(row.iloc[cols[T]]), "F_Tm12": float(row.iloc[cols[Tm]])})
        except Exception as e:
            dropped.append(f"{stem}: {type(e).__name__}: {e}")
out = Path("data/sources/eia_steo_co2_h18"); out.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out / "editions_h18.csv", index=False)
(out / "dropped.txt").write_text("\n".join(dropped) + ("\n" if dropped else ""))
print(f"rows {len(rows)}, dropped {len(dropped)}")
