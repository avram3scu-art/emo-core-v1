"""Layout-only probe (session 7f): SPF medianLevel.xlsx sheet names, UNEMP sheet
column names and survey-date range; FRED UNRATE CSV header and date range.
Never prints forecast or data values."""
import io, urllib.request
import pandas as pd
UA = {"User-Agent": "emo-core-v1 layout probe (github.com/avram3scu-art/emo-core-v1)"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()
SPF = ("https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/"
       "historical-data/medianLevel.xlsx?sc_lang=en&hash=E52F5DEF4551C3EBD24031A04CE6E98A")
try:
    book = pd.read_excel(io.BytesIO(get(SPF)), sheet_name=None)
    print("sheets:", list(book))
    u = book.get("UNEMP")
    if u is not None:
        print("UNEMP columns:", list(u.columns), "rows:", len(u))
        print("UNEMP survey range:", int(u["YEAR"].min()), int(u["QUARTER"].iloc[0]), "..", int(u["YEAR"].max()), int(u["QUARTER"].iloc[-1]))
        print("UNEMP missing per column:", u.isna().sum().to_dict())
except Exception as e:
    print("SPF FAILED", type(e).__name__, e)
try:
    f = pd.read_csv(io.BytesIO(get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE")))
    print("FRED columns:", list(f.columns), "range:", f.iloc[0, 0], "..", f.iloc[-1, 0], "rows:", len(f))
except Exception as e:
    print("FRED FAILED", type(e).__name__, e)
