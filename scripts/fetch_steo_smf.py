"""Fetch inputs for the SMF test (docs/SMF_PROTOCOL.md, session 7).

STEO editions Jan 2010 .. Jun 2025: from sheet 9atab, total CO2 row (TETCCO2,
else FFTCCO2), the edition's value for its own month P and for P + 12.
MER Table 11.1: raw CSV. Writes data/sources/eia_steo_co2/editions.csv,
data/sources/eia_mer_t11_01/T11_01.csv and data/sources/eia_smf_SOURCES.json
(own file; data/MANIFEST.json belongs to the weekly run)."""
import datetime as dt
import hashlib
import io
import json
import re
import time
import urllib.request
from pathlib import Path

import pandas as pd

UA = {"User-Agent": "emo-core-v1 SMF test (github.com/avram3scu-art/emo-core-v1)"}
MON = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
BASE = "https://www.eia.gov/outlooks/steo/archives/"
MER = "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T11.01"


def get(url, tries=3):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(5)


def month_columns(df):
    """Map (year, month) -> column index from the month and year header rows."""
    labels = {m.capitalize(): i + 1 for i, m in enumerate(MON)}
    for r in range(min(15, len(df))):
        row = df.iloc[r]
        cols = [c for c in range(df.shape[1]) if isinstance(row.iloc[c], str) and row.iloc[c].strip()[:3] in labels]
        if len(cols) < 12:
            continue
        for ry in list(range(r - 1, max(-1, r - 4), -1)) + list(range(r + 1, min(len(df), r + 4))):
            yrow, year, out, found = df.iloc[ry], None, {}, 0
            for c in range(df.shape[1]):
                v = yrow.iloc[c]
                m = re.fullmatch(r"(19|20)\d\d", str(v).strip().split(".")[0]) if pd.notna(v) else None
                if m:
                    year, found = int(m.group(0)), found + 1
                if c in cols and year:
                    out[(year, labels[row.iloc[c].strip()[:3]])] = c
            if found >= 2:
                return out
    raise ValueError("month/year header not found")


def edition(year, mi):
    stem = f"{MON[mi]}{year % 100:02d}_base"
    err = None
    for ext in (".xlsx", ".xls"):
        try:
            raw = get(BASE + stem + ext)
            book = pd.read_excel(io.BytesIO(raw), sheet_name=None, header=None)
            break
        except Exception as e:
            err = e
    else:
        raise RuntimeError(f"fetch failed: {type(err).__name__}")
    sh = next(s for s in book if s.strip().lower() == "9atab")
    df = book[sh]
    codes = df.iloc[:, 0].astype(str).str.strip()
    code = "TETCCO2" if (codes == "TETCCO2").any() else "FFTCCO2"
    row = df[codes == code].iloc[0]
    cols = month_columns(df)
    p = (year, mi + 1)
    t = (year + 1, mi + 1)
    fp, ft = float(row.iloc[cols[p]]), float(row.iloc[cols[t]])
    return {"edition": stem + ext, "P": f"{year}-{mi+1:02d}", "T": f"{year+1}-{mi+1:02d}",
            "code": code, "F_P": fp, "F_T": ft, "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    rows, dropped = [], []
    for year in range(2010, 2026):
        for mi in range(12):
            if (year, mi) > (2025, 5):
                break
            try:
                rows.append(edition(year, mi))
            except Exception as e:
                dropped.append(f"{MON[mi]}{year % 100:02d}: {type(e).__name__}: {e}")
    out = Path("data/sources/eia_steo_co2"); out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / "editions.csv", index=False)
    (out / "dropped.txt").write_text("\n".join(dropped) + ("\n" if dropped else ""))
    mer_raw = get(MER)
    mout = Path("data/sources/eia_mer_t11_01"); mout.mkdir(parents=True, exist_ok=True)
    (mout / "T11_01.csv").write_bytes(mer_raw)
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    src = {"eia_steo_co2/editions.csv": {"source_url": BASE + "{mon}{yy}_base.xlsx|.xls, sheet 9atab",
                                         "downloaded_at": now, "sha256": hashlib.sha256((out / "editions.csv").read_bytes()).hexdigest()},
           "eia_mer_t11_01/T11_01.csv": {"source_url": MER, "downloaded_at": now, "sha256": hashlib.sha256(mer_raw).hexdigest()}}
    Path("data/sources/eia_smf_SOURCES.json").write_text(json.dumps(src, indent=2) + "\n")
    print(f"editions parsed {len(rows)}, dropped {len(dropped)}")


if __name__ == "__main__":
    main()
