"""Fetch inputs for SMF on SPF unemployment forecasts (docs/SMF_PROTOCOL.md §11)."""
import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

UA = {"User-Agent": "emo-core-v1 SMF test (github.com/avram3scu-art/emo-core-v1)"}
SPF = ("https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/"
       "historical-data/medianLevel.xlsx?sc_lang=en&hash=E52F5DEF4551C3EBD24031A04CE6E98A")
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE"
out = Path("data/sources/spf_unemp"); out.mkdir(parents=True, exist_ok=True)
now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
src = {}
for name, url in (("medianLevel.xlsx", SPF), ("UNRATE.csv", FRED)):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
    (out / name).write_bytes(raw)
    src[name] = {"source_url": url, "downloaded_at": now, "sha256": hashlib.sha256(raw).hexdigest()}
(out / "SOURCES.json").write_text(json.dumps(src, indent=2) + "\n")
print("fetched", list(src))
