"""Layout-only probe (session 7e): electricity rows of STEO table 7a (codes and
labels, with any unit lines) and MER Table 7.6 descriptions/units. No values."""
import io, re, sys, urllib.request
import pandas as pd
UA = {"User-Agent": "emo-core-v1 layout probe (github.com/avram3scu-art/emo-core-v1)"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
for name in sys.argv[1:]:
    try:
        book = pd.read_excel(io.BytesIO(get("https://www.eia.gov/outlooks/steo/archives/" + name)), sheet_name=None, header=None)
    except Exception as e:
        print(name, "FAILED", type(e).__name__); continue
    sh = next((s for s in book if s.strip().lower() == "7atab"), None)
    print(f"{name}: 7atab present: {sh is not None}")
    if sh is None: continue
    df = book[sh]
    for i in range(len(df)):
        labs = [str(v).strip() for v in df.iloc[i, :2].tolist() if isinstance(v, str)]
        if labs and re.search(r"retail|sales|consumption|kilowatt|total", " ".join(labs), re.I):
            print(f"  row {i}: {' | '.join(labs)}")
for tbl in ("T07.06", "T07.01"):
    try:
        mer = pd.read_csv(io.BytesIO(get(f"https://www.eia.gov/totalenergy/data/browser/csv.php?tbl={tbl}")))
        print(tbl, "units:", sorted(mer["Unit"].unique().tolist()))
        print(tbl, "desc:", sorted(mer["Description"].unique().tolist()))
    except Exception as e:
        print(tbl, "FAILED", type(e).__name__)
