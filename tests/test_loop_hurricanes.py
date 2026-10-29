"""Tests of the hurricane-loop event table (session 2.4; docs/LOOP_PROTOCOL.md §16)."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from emo import loop_hurricanes as lh

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "loop_hurricanes"


# ------------------------------------------------------------------ units (synthetic inputs)


def test_point_in_polygon_and_near_rule():
    sq = [np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)]
    hole = [sq[0], np.array([[0.4, 0.4], [0.6, 0.4], [0.6, 0.6], [0.4, 0.6], [0.4, 0.4]])]
    assert lh.point_in_rings(0.5, 0.5, sq)
    assert not lh.point_in_rings(0.5, 0.5, hole)
    polys = [("AA", sq)]
    assert lh.assign_state(0.5, 0.5, polys) == ("AA", 0.0)
    st, d = lh.assign_state(1.3, 0.5, polys)  # ~33 km east of the edge at the equator
    assert st == "AA" and 30 < d < 36
    st, d = lh.assign_state(1.6, 0.5, polys)  # ~67 km: beyond 50 km
    assert st == "" and d > 50


def test_parse_hurdat2_and_r64():
    lines = [
        (1, "AL091999,          TESTY,      2,"),
        (2, "19990801, 0000,  , TS, 25.0N,  80.0W,  50, 1000,   50,   50,   40,   40,    0,    0,    0,    0,    0,    0,    0,    0, -999"),
        (3, "19990801, 0630, L, HU, 25.5N,  80.5W,  65,  990,   60,   60,   50,   50,   30,   30,   20,   20,   15,   10,    0,    5, -999"),
    ]
    s = lh.parse_hurdat2(lines)["AL091999"]
    assert s.name == "TESTY" and len(s.records) == 2
    r = s.records[1]
    assert r.ident == "L" and r.time == dt.datetime(1999, 8, 1, 6, 30) and r.lon == -80.5 and max(r.r64) == 15


def test_type_route_amendment5():
    assert lh.type_route({"designatedIncidentTypes": "2,H,W"}, hu_only=True) == "code"
    assert lh.type_route({"designatedIncidentTypes": "4"}, hu_only=False) == "code"
    assert lh.type_route({"designatedIncidentTypes": "4"}, hu_only=True) == ""
    # filled field decides even if incidentType says Hurricane
    assert lh.type_route({"designatedIncidentTypes": "F", "incidentType": "Hurricane"}, hu_only=False) == ""
    assert lh.type_route({"designatedIncidentTypes": "", "incidentType": "Hurricane"}, hu_only=True) == "fallback"
    assert lh.type_route({"designatedIncidentTypes": "", "incidentType": "Tropical Storm"}, hu_only=True) == ""
    assert lh.type_route({"designatedIncidentTypes": "", "incidentType": "Tropical Storm"}, hu_only=False) == "fallback"


def _rec(i, num, typ, title, begin, decl, req="", state="FL"):
    return {"id": f"r{i}", "disasterNumber": str(num), "state": state, "declarationType": typ,
            "designatedIncidentTypes": "H", "incidentType": "Hurricane", "declarationTitle": title,
            "incidentBeginDate": begin, "declarationDate": decl, "declarationRequestDate": req,
            "incidentId": "x", "region": "4"}


def test_match_fema_rules():
    d0 = dt.date(2020, 9, 10)
    recs = [_rec(1, 4500, "DR", "HURRICANE TESTY", "2020-09-08T00:00:00.000Z", "2020-09-20T00:00:00.000Z", "2020-09-12T00:00:00.000Z"),
            _rec(2, 3500, "EM", "TROPICAL STORM OTHER", "2020-09-09T00:00:00.000Z", "2020-09-09T00:00:00.000Z"),
            _rec(3, 4501, "DR", "HURRICANE TESTY", "2020-08-20T00:00:00.000Z", "2020-09-01T00:00:00.000Z")]  # outside window
    m = lh.match_fema("Testy", "FL", d0, recs, [])
    assert m.status == "matched" and m.name_rule == "title" and [r["id"] for r in m.records] == ["r1"]
    m = lh.match_fema("Zeta", "FL", d0, recs, [])
    assert m.name_rule == "window" and {r["id"] for r in m.records} == {"r1", "r2"}
    m = lh.match_fema("Zeta", "FL", d0, recs, [dt.date(2020, 9, 15)])
    assert m.status == "unmatched" and m.reason == "ambiguous"
    assert lh.match_fema("Testy", "TX", d0, recs, []).reason == "no_candidate"
    g = lh.group_declarations([recs[0], {**recs[0], "id": "r9", "declarationRequestDate": "2020-09-11T00:00:00.000Z"}])
    assert g[0].request_date == dt.date(2020, 9, 11) and g[0].decl_date == dt.date(2020, 9, 20)


def test_whole_word():
    assert lh.whole_word("Ida", "HURRICANE IDA")
    assert not lh.whole_word("Ida", "FLORIDA FLOODING")


def test_track_skill_synthetic():
    st = lh.Storm("AL091999", "TESTY", 1, [
        lh.BestRecord(10, dt.datetime(1999, 8, 3, 0), "", "HU", 25.0, -80.0, 70, 990, (0, 0, 0, 0)),
        lh.BestRecord(11, dt.datetime(1999, 8, 3, 12), "", "HU", 26.0, -80.0, 70, 990, (0, 0, 0, 0)),
    ])
    errs = [lh.ErrLine(100, dt.datetime(1999, 8, 1, 0), "AL091999", 1.0, 50.0, 5.0),
            lh.ErrLine(101, dt.datetime(1999, 8, 1, 12), "AL091999", 1.0, 30.0, -5.0),
            lh.ErrLine(102, dt.datetime(1999, 8, 4, 0), "AL091999", 1.0, 30.0, 0.0)]  # not before t0
    base = {dt.datetime(1999, 8, 1, 0): lh.AdeckRec(7, dt.datetime(1999, 8, 1, 0), 26.0, -80.0, 80),
            dt.datetime(1999, 8, 1, 12): lh.AdeckRec(8, dt.datetime(1999, 8, 1, 12), 27.0, -80.0, 60)}
    sk = lh.track_skill(st, dt.datetime(1999, 8, 2, 0), errs, base)
    one_deg = lh.gc_nmi(25, -80, 26, -80)
    assert sk.n_lines == 2 and sk.ess48 == 2.0
    assert sk.f == pytest.approx(1 - 80 / (2 * one_deg))
    assert sk.f_int == pytest.approx(1 - 10 / 20)
    sk1 = lh.track_skill(st, dt.datetime(1999, 8, 1, 6), errs, base)
    assert sk1.f is None and sk1.reason == "f_ess_lt2"


def test_resolve_target_rules():
    titles = lh.candidate_titles("TESTY", 2020)
    q = {"query": {"redirects": [{"from": "Hurricane Testy", "to": "Hurricane Testy (2020)"}],
                   "pages": [{"title": "Hurricane Testy (2020)", "pageid": 1},
                             {"title": "Tropical Storm Testy (2020)", "missing": True}]}}
    assert lh.resolve_target(q, titles) == ("Hurricane Testy (2020)", "T1", ["Hurricane Testy"])
    q2 = {"query": {"pages": [{"title": "Hurricane Testy (2020)", "missing": True},
                              {"title": "Hurricane Testy", "pageid": 2, "pageprops": {"disambiguation": ""}},
                              {"title": "Tropical Storm Testy (2020)", "pageid": 3}]}}
    assert lh.resolve_target(q2, titles)[:2] == ("Tropical Storm Testy (2020)", "T3")
    q3 = {"query": {"pages": [{"title": t, "missing": True} for t in titles.values()]}}
    assert lh.resolve_target(q3, titles)[0] is None


def test_attention_window():
    s = [{"20200907": 10, "20200908": 20, "20200909": 30, "20200910": 1000}]
    a, tot = lh.attention(dt.date(2020, 9, 10), s)
    assert tot == 60 and a == pytest.approx(np.log10(61))


def test_parse_advdate():
    assert lh.parse_advdate("140701/0300") == dt.datetime(2014, 7, 1, 3, 0)
    assert lh.parse_advdate("1100 AM AST") is None
    assert lh.parse_advdate("400 PM CDT Mon Jun 19 2017") == dt.datetime(2017, 6, 19, 21, 0)
    assert lh.parse_advdate("1200 AM EDT Sat Oct 10 2020") == dt.datetime(2020, 10, 10, 4, 0)
    assert lh.parse_advdate("1100 AM XYZ Thu Aug 17 2017") is None


# ------------------------------------------------------------------ committed table


@pytest.mark.skipif(not (DATA / "loop_events.csv").exists(), reason="table not built")
def test_validator_passes_on_committed_table():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_loop_table.py")],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "failures=0" in r.stdout


@pytest.mark.skipif(not (DATA / "summary.json").exists(), reason="table not built")
def test_no_h4_h5_output_exists():
    s = json.loads((DATA / "summary.json").read_text())
    s.pop("note", None)
    text = json.dumps(s).lower()
    for word in ("corr", "kendall", "tau", "p_value", "pvalue", "holm", "trend", "slope"):
        assert word not in text
    for p in list(DATA.rglob("*")) + list((ROOT / "analysis").glob("loop_*")):
        n = p.name.lower()
        assert not any(k in n for k in ("h4", "h5", "loop_test", "loop_result")), p
