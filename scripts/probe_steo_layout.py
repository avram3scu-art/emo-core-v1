"""Layout-only probe for the SMF case (session 7b). For each STEO edition: does
table 9a carry a total CO2 row (code), and what are its first/last date column
labels and column count. For MER T11.01: column names, descriptions, date range.
Never prints data values, so it can run before the SMF protocol is registered."""
import io
import re
import sys
import urllib.request

import pandas as pd

UA = {"User-Agent": "emo-core-v1 layout probe (github.com/avram3scu-art/emo-core-v1)"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()

for name in sys.argv[1:]:
    try:
        book = pd.read_excel(io.BytesIO(get(f"https://www.eia.gov/outlooks/steo/archives/{name}")), sheet_name=None, header=None)
    except Exception as e:
        print(f"{name}: FAILED {type(e).__name__}"); continue
    sh = next((s for s in book if s.strip().lower() == "9atab"), None)
    if sh is None:
        print(f"{name}: no 9atab"); continue
    df = book[sh]
    codes = [str(c) for c in df.iloc[:, 0] if isinstance(c, str) and c.strip().endswith("CO2")]
    hdr = None
    for i in range(12):  # find the row holding dates
        row = df.iloc[i]
        d = [v for v in row if isinstance(v, (pd.Timestamp,)) or (isinstance(v, str) and re.match(r"^\d{4}-\d{2}", v))]
        if len(d) > 5:
            hdr = (i, str(d[0])[:7], str(d[-1])[:7], len(d)); break
    yrow = [str(v) for v in df.iloc[:8, :].to_numpy().ravel() if isinstance(v, str)][:6]
    print(f"{name}: CO2 codes {codes}; date row {hdr}; first strings {yrow}")

try:
    mer = pd.read_csv(io.BytesIO(get("https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T11.01")))
    print("MER cols", list(mer.columns))
    print("MER desc", sorted(mer["Description"].unique().tolist()))
    y = mer["YYYYMM"].astype(str)
    print("MER YYYYMM", y.min(), y.max(), "monthly rows (not 13):", int((~y.str.endswith("13")).sum()))
except Exception as e:
    print(f"MER: FAILED {type(e).__name__}: {e}")
