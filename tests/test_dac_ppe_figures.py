"""F13: the China supply events drawn in Figures 1-2 match their committed sources and their day numbers."""

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T0 = dt.date(2020, 1, 30)


def _day(s: str) -> int:
    return (dt.date.fromisoformat(s) - T0).days


def test_china_events_quote_their_sources_and_days_match_dates():
    ev = json.loads((ROOT / "data/dac_ppe/china_supply_events.json").read_text(encoding="utf-8"))["events"]
    assert len(ev) == 3
    for e in ev:
        text = (ROOT / "data/sources/lit" / e["source_file"]).read_text(encoding="utf-8")
        assert e["phrase"] in text, e["id"]
        if e["kind"] == "line":
            assert e["day"] == _day(e["date"]), e["id"]
        else:
            assert (e["day_start"], e["day_end"]) == (_day(e["date_start"]), _day(e["date_end"])), e["id"]
