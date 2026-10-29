"""Pre-scoring source check for GWI v2 (docs/GWI_V2_PROTOCOL.md §10). Opens no scored data.

1. USGS ComCat query of fetch_gwi_v2.py, run on 2025 (outside the test window): header, rows.
2. English langlinks (redirects followed) for the 21 articles: editions found of the 12.
No pageviews are fetched. Run: python scripts/check_gwi_v2_sources.py
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from urllib.parse import quote

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.fetch_gwi_v2 import PLACEBOS, TEST, USGS_URL  # noqa: E402
from scripts.refresh_open_data import LANGLINKS_URL, PV_LANGS, _get  # noqa: E402

url = USGS_URL.replace("2026-11-01", "2025-01-01").replace("2027-10-31", "2025-12-31")
df = pd.read_csv(io.StringIO(_get(url).text))
print("USGS 2025 query:", url)
print("  columns:", list(df.columns)[:6], "... rows:", len(df), "; min mag", df["mag"].min())
for t in [TEST, *PLACEBOS]:
    page = _get(LANGLINKS_URL.format(title=quote(t)) + "&redirects=1").json()["query"]["pages"][0]
    langs = {"en"} | {ll["lang"] for ll in page.get("langlinks", [])}
    n = len([lg for lg in PV_LANGS if lg in langs])
    print(f"  {t} -> {page.get('title')}: {n}/12 editions" + ("  (< 8: would be dropped)" if n < 8 else ""))
