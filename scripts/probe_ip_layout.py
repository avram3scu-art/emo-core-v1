"""Layout-only probe (session 7g): industrial-production rows in STEO table 9a,
SPF INDPROD columns, FRED INDPRO range. Never prints data values."""
import io
import re
import urllib.request

import pandas as pd

UA = {"User-Agent": "emo-core-v1 layout probe (github.com/avram3scu-art/emo-core-v1)"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()
for name in ("jan10_base.xls", "jan15_base.xlsx", "jan20_base.xlsx", "oct26_base.xlsx"):
    try:
        book = pd.read_excel(io.BytesIO(get("https://www.eia.gov/outlooks/steo/archives/" + name)), sheet_name=None, header=None)
        df = book[next(s for s in book if s.strip().lower() == "9atab")]
        print(name)
        for i in range(len(df)):
            labs = [str(v).strip() for v in df.iloc[i, :2].tolist() if isinstance(v, str)]
            if labs and re.search(r"industrial|production|manufactur|index|unemploy|source|forecast", " ".join(labs), re.I):
                print(f"  row {i}: {' | '.join(l[:150] for l in labs)}")
    except Exception as e:
        print(name, "FAILED", type(e).__name__, e)
SPF = ("https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/"
       "historical-data/medianLevel.xlsx?sc_lang=en&hash=E52F5DEF4551C3EBD24031A04CE6E98A")
u = pd.read_excel(io.BytesIO(get(SPF)), sheet_name="INDPROD")
print("SPF INDPROD columns:", list(u.columns), "rows:", len(u), "first survey:", int(u["YEAR"].iloc[0]), int(u["QUARTER"].iloc[0]))
print("SPF INDPROD missing:", {k: int(v) for k, v in u.isna().sum().items()})
f = pd.read_csv(io.BytesIO(get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDPRO")))
print("FRED INDPRO columns:", list(f.columns), "range:", f.iloc[0, 0], "..", f.iloc[-1, 0])
