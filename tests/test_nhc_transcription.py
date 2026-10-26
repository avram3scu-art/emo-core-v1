"""The hand-maintained NHC table must match the text of NHC's own PDF, cell by cell.

The PDF text was extracted by the one-off job `nhc-pdf` (results/nhc_check/, with the PDF's
SHA-256). 36-h forecasts start in 1988, 96/120-h in 2001 (NHC notes).
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_csv_matches_nhc_pdf_text():
    pdf = {}
    for line in (ROOT / "results/nhc_check/nhc_pdf.txt").read_text().splitlines():
        t = line.split()
        if len(t) < 3 or not re.fullmatch(r"(19|20)\d\d", t[0]):
            continue
        y, nums = int(t[0]), t[1:]
        leads = [0, 12, 24, 48, 72] if y < 1988 else [0, 12, 24, 36, 48, 72] + ([96, 120] if y >= 2001 else [])
        assert len(nums) == 2 * len(leads), f"{y}: unexpected row layout"
        for i, lead in enumerate(leads):
            pdf[(y, lead)] = (float(nums[2 * i]), int(nums[2 * i + 1]))
    d = pd.read_csv(ROOT / "data/nhc_atlantic_official_track_errors_1970_2025.csv")
    csv = {(r.year, r.lead_h): (r.error_nmi, r.n_forecasts) for r in d.itertuples()}
    assert len(pdf) == 368 and pdf == csv
