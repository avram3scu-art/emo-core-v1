"""Every coded PPE case file (data/dac_ppe/<case>.json) validates and its committed profile is current."""

import json
from pathlib import Path

import pytest

from emo.dac_standard import compute_profile, load_event_file

D = Path(__file__).resolve().parents[2] / "data/dac_ppe"
CASES = sorted(D.glob("[A-Z][A-Z].json"))


@pytest.mark.parametrize("path", CASES, ids=[p.stem for p in CASES])
def test_case_file_valid_and_profile_current(path):
    prof = compute_profile(load_event_file(path))
    committed = json.loads((D / f"{path.stem}_profile.json").read_text(encoding="utf-8"))
    assert prof == committed, f"rerun scripts/dac_ppe_outputs.py for {path.stem}"


def test_belgian_file_is_coded():
    assert (D / "BE.json").exists() and (D / "BE_orders.csv").exists()


def _annex5_rows():
    """(PDF page, row number) of every entry in the committed Belgian Annex 5 text."""
    import re
    lines = (D.parent / "sources/dac_ppe/BE_annex5.txt").read_text(encoding="utf-8").split("\n")
    rows, page = set(), None
    for i, ln in enumerate(lines):
        m = re.search(r"===== PDF page (\d+)", ln)
        if m:
            page = int(m.group(1))
            continue
        m = re.match(r"^\s{40,}(\d{2})/(\d{2})/(\d{4})\s{2,}", ln)
        if m:
            j = i - 1
            while j > 0 and not lines[j].strip():
                j -= 1
            if lines[j].strip().isdigit():
                rows.add((page, lines[j].strip(), f"{m.group(3)}-{m.group(2)}-{m.group(1)}"))
    return rows


def test_belgian_citations_point_to_existing_rows():
    """Every 'PDF p. N, row R' cited in BE.json is an entry with row number R on page N of Annex 5."""
    import re
    rows = _annex5_rows()
    pages = {(r[0], r[1]) for r in rows}
    bad, n = [], 0
    for e in json.loads((D / "BE.json").read_text(encoding="utf-8"))["events"]:
        m = re.search(r"PDF p\. (\d+), row (\d+)", e["source"])
        if not m:
            continue
        n += 1
        key = (int(m.group(1)), m.group(2))
        if key not in pages:
            bad.append((e["event_id"], key, "row not on page"))
        # the row's own date must be the event's date, except deliveries (their date is stated in the order's row)
        elif e["sublayer"] != "delivery" and e.get("date_earliest") and (*key, e["date_earliest"]) not in rows:
            bad.append((e["event_id"], key, "row date differs"))
    assert n and not bad, bad
