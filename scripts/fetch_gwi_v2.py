"""Fetch the data of the GWI v2 prospective test (docs/GWI_V2_PROTOCOL.md §3, §8).

Refuses to run before the scoring date (2027-11-15), so no scored day can be opened early.
Writes data/sources/gwi_v2/: pageviews.csv, usgs_m7.csv, MANIFEST.txt (SHA-256).
Runs in the one-off workflow .github/workflows/gwi_v2_fetch.yml (Wikimedia rate-limits
Claude's workspace). Run from the repository root: python scripts/fetch_gwi_v2.py
"""

from __future__ import annotations

import datetime as dt
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.refresh_open_data import _get, _pageviews_csv  # noqa: E402

SCORING_DATE = dt.date(2027, 11, 15)
OUT = ROOT / "data/sources/gwi_v2"
FETCH_START, FETCH_END = "20220701", "20271102"
TEST = "Earthquake"
PLACEBOS = ["Photosynthesis", "Prime number", "Pythagorean theorem", "Mitochondrion",
            "Periodic table", "Atom", "Cell (biology)", "Fraction", "Triangle", "Water cycle",
            "Leaf", "Bird", "Tree", "River", "Chess", "Piano", "Bread", "Algebra", "Circle", "Fern"]
USGS_URL = ("https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&eventtype=earthquake"
            "&starttime=2026-11-01T00:00:00&endtime=2027-10-31T23:59:59&minmagnitude=7.0&orderby=time-asc")


def main(today: dt.date | None = None) -> int:
    today = today or dt.date.today()
    if today < SCORING_DATE:
        print(f"Refused: scoring date is {SCORING_DATE}; today is {today}. No data fetched.")
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    sets = {"test": (TEST, FETCH_START, FETCH_END)}
    sets |= {f"placebo:{t}": (t, FETCH_START, FETCH_END) for t in PLACEBOS}
    pv, rows = _pageviews_csv(sets, strict=False, follow_redirects=True)
    (OUT / "pageviews.csv").write_bytes(pv)
    eq = _get(USGS_URL).content
    (OUT / "usgs_m7.csv").write_bytes(eq)
    man = [f"fetched_utc {dt.datetime.now(dt.UTC).isoformat()}", f"usgs_url {USGS_URL}",
           f"pageview_rows {rows}"]
    for f in ("pageviews.csv", "usgs_m7.csv"):
        man.append(f"sha256 {f} {hashlib.sha256((OUT / f).read_bytes()).hexdigest()}")
    (OUT / "MANIFEST.txt").write_text("\n".join(man) + "\n")
    print("\n".join(man))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
