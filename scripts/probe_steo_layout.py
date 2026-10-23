"""Layout-only probe for the SMF case (session 7b). Prints sheet names and the
row labels / column headers that mention CO2 or carbon. It never prints data
values, so it can run before the SMF protocol is pre-registered."""
import io, re, sys, urllib.request
import pandas as pd

PAT = re.compile(r"co2|carbon", re.I)
UA = {"User-Agent": "emo-core-v1 layout probe (github.com/avram3scu-art/emo-core-v1)"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

for name in sys.argv[1:]:
    url = f"https://www.eia.gov/outlooks/steo/archives/{name}"
    try:
        book = pd.read_excel(io.BytesIO(get(url)), sheet_name=None, header=None)
    except Exception as e:
        print(f"{name}: FAILED {type(e).__name__}: {e}"); continue
    print(f"{name}: sheets {list(book)}")
    for sh, df in book.items():
        # labels live in the first few columns; dates in the first few rows
        for i in range(len(df)):
            labs = [str(v) for v in df.iloc[i, :3].tolist() if isinstance(v, str)]
            if any(PAT.search(l) for l in labs):
                print(f"  {sh} row {i}: {' | '.join(labs)}")
        hdr = [str(v) for v in df.iloc[:4, :].to_numpy().ravel() if not isinstance(v, (int, float))]
        dates = [h for h in hdr if re.match(r"\d{4}-\d{2}", h)]
        if dates:
            print(f"  {sh}: date header {dates[0]} .. {dates[-1]} ({len(dates)} cols)")

url = "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T11.01"
try:
    mer = pd.read_csv(io.BytesIO(get(url)))
    print("MER T11.01 columns:", list(mer.columns))
    print("MER descriptions:", sorted(mer["Description"].unique().tolist()) if "Description" in mer else "n/a")
    yyyymm = mer["YYYYMM"].astype(str) if "YYYYMM" in mer else None
    if yyyymm is not None:
        print("MER YYYYMM range:", yyyymm.min(), "..", yyyymm.max())
except Exception as e:
    print(f"MER: FAILED {type(e).__name__}: {e}")
