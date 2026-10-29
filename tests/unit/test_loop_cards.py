"""Synthetic checks of every rule of docs/LOOP_CARD_PROTOCOL.md (session 3.3).

No stream record is used: every record here is invented. Evidence class: infrastructure.
"""
import datetime as dt

import pytest

from emo.stream import cards as C

UTC = dt.UTC
NOW = dt.datetime(2027, 1, 15, tzinfo=UTC)


def gd(eid, typ="EQ", alert="orange", iso="PHL", frm="2027-01-01T03:00:00Z",
       to=None, glide=None, fetched="2027-01-01T04:17:00Z", lon=120.0, lat=10.0):
    return {"_emo_feed": "search", "_emo_fetched_at": fetched,
            "geometry": {"coordinates": [lon, lat]},
            "properties": {"eventtype": typ, "eventid": eid, "alertlevel": alert,
                           "iso3": iso, "fromdate": frm, "todate": to or frm,
                           "glide": glide}}


def us(eid, t, alert=None, lon=120.0, lat=10.0, fetched="2027-01-01T04:17:00Z"):
    return {"_emo_feed": "comcat", "id": eid, "_emo_fetched_at": fetched,
            "geometry": {"coordinates": [lon, lat, 10]},
            "properties": {"time": t, "alert": alert, "mag": 6.0}}


def cems(code, gdacs_id=None, countries=("PHL",), cat="Earthquake",
         ev="2027-01-01T03:00:00Z", act="2027-01-02T10:00:00Z", fetched="2027-01-03T04:17:00Z"):
    return {"code": code, "gdacsId": gdacs_id, "countries": list(countries),
            "category": cat, "eventTime": ev, "activationTime": act,
            "_emo_fetched_at": fetched}


def goev(eid, dtype="Earthquake", iso="PHL", start="2027-01-01", glide=None,
         created="2027-01-01T12:00:00Z", fetched="2027-01-02T04:17:00Z"):
    return {"_emo_feed": "event", "id": eid, "dtype": {"name": dtype},
            "countries": [{"iso3": iso}], "disaster_start_date": start, "glide": glide,
            "created_at": created, "_emo_fetched_at": fetched}


def goap(aid, event, atype=1, req=100.0, fund=0.0, start="2027-01-03",
         end="2027-06-30", created="2027-01-03T09:00:00Z", fetched="2027-01-04T04:17:00Z"):
    return {"_emo_feed": "appeal_running", "id": aid, "event": event, "atype": atype,
            "amount_requested": req, "amount_funded": fund, "start_date": start,
            "end_date": end, "created_at": created, "_emo_fetched_at": fetched}


def runs(gdacs=(), usgs=(), cems_=(), go=()):
    return [{"sources": {"gdacs": {"records": list(gdacs)}, "usgs": {"records": list(usgs)},
                         "cems": {"records": list(cems_)}, "ifrc_go": {"records": list(go)}}}]


def comp_of(comps, key):
    return next(c for c in comps if key in c)


# --- parsing ---------------------------------------------------------------------------
def test_parse_time_forms():
    assert C.parse_time("2027-01-02")[1] == "day"
    t, p = C.parse_time("2027-01-02T03:04:05Z")
    assert p == "time" and t.hour == 3
    assert C.parse_time(1798761600000)[1] == "time"
    assert C.parse_time("junk") == (None, "none") and C.parse_time(None) == (None, "none")


def test_glide_key_ignores_iso3_suffix_and_format():
    assert C.glide_key("EQ-2027-000012-PHL") == C.glide_key("eq2027000012")
    assert C.glide_key("EQ-2027-000012-PHL") != C.glide_key("EQ-2027-000013-PHL")
    assert C.glide_key("not a glide") is None


def test_iso3_from_strings_and_dicts_never_from_names():
    assert C.iso3_set("PHL,VNM") == {"PHL", "VNM"}
    assert C.iso3_set([{"iso3": "bgd"}]) == {"BGD"}
    assert C.iso3_set(["Philippines"]) == set()


def test_hazard_crosswalk():
    assert C.hazard_from_text({"name": "Flash Flood"}) == "FL"
    assert C.hazard_from_text("Tropical Cyclone") == "TC"
    assert C.hazard_from_text("Tsunami after earthquake") == "TS"
    assert C.hazard_from_text("Epidemic") is None


# --- join rule ---------------------------------------------------------------------------
def test_k1_gdacs_id_links_cems():
    n = C.build_nodes(runs([gd(1)], cems_=[cems("EMSR900", gdacs_id=1)]))
    comps, edges = C.join(n)
    assert ("cems", "EMSR900") in comp_of(comps, ("gdacs", "EQ", "1"))
    assert any(e["rule"] == "K1_gdacsId" for e in edges)


def test_k1_shared_id_resolved_by_hazard_else_tie():
    n = C.build_nodes(runs([gd(5, "EQ"), gd(5, "TC")], cems_=[cems("E1", gdacs_id=5)]))
    comps, _ = C.join(n)
    assert ("cems", "E1") in comp_of(comps, ("gdacs", "EQ", "5"))
    n = C.build_nodes(runs([gd(5, "EQ"), gd(5, "TC")],
                           cems_=[cems("E2", gdacs_id=5, cat="Landslide")]))
    comps, edges = C.join(n)
    assert ("cems", "E2") not in comp_of(comps, ("gdacs", "EQ", "5"))
    assert any(e["note"] == "tie" for e in edges)


def test_k2_glide_and_k3_event_id():
    n = C.build_nodes(runs([gd(2, glide="EQ-2027-000001-PHL")],
                           go=[goev(77, glide="EQ-2027-000001"), goap(9, 77)]))
    comps, _ = C.join(n)
    c = comp_of(comps, ("gdacs", "EQ", "2"))
    assert {("go_event", "77"), ("go_appeal", "9")} <= c


def test_k3_appeal_event_as_dict():
    n = C.build_nodes(runs(go=[goev(3), goap(4, {"id": 3})]))
    comps, _ = C.join(n)
    assert ("go_appeal", "4") in comp_of(comps, ("go_event", "3"))


def test_f1_usgs_gdacs_time_distance():
    t = int(dt.datetime(2027, 1, 1, 3, 10, tzinfo=UTC).timestamp() * 1000)
    n = C.build_nodes(runs([gd(1)], usgs=[us("us1", t)]))
    comps, _ = C.join(n)
    assert ("usgs", "us1") in comp_of(comps, ("gdacs", "EQ", "1"))
    far = us("us2", t, lon=125.0)                      # ~550 km away
    late = us("us3", t + 3600 * 1000)                  # 70 min later
    n = C.build_nodes(runs([gd(1)], usgs=[far, late]))
    comps, _ = C.join(n)
    c = comp_of(comps, ("gdacs", "EQ", "1"))
    assert ("usgs", "us2") not in c and ("usgs", "us3") not in c


def test_f2_fallback_window_edges():
    # TC window -3 .. +7 days
    g = gd(1, "TC", frm="2027-01-10T00:00:00Z", to="2027-01-14T00:00:00Z")
    inside = goev(1, "Tropical Cyclone", start="2027-01-17")     # +7
    outside = goev(2, "Tropical Cyclone", start="2027-01-18")    # +8
    before = goev(3, "Tropical Cyclone", start="2027-01-07")     # -3
    n = C.build_nodes(runs([g], go=[inside, outside, before]))
    comps, _ = C.join(n)
    c = comp_of(comps, ("gdacs", "TC", "1"))
    assert ("go_event", "1") in c and ("go_event", "3") in c and ("go_event", "2") not in c


def test_f2_needs_iso3_and_hazard_and_never_for_drought():
    n = C.build_nodes(runs([gd(1, "FL", iso="BGD", frm="2027-01-01")],
                           go=[goev(1, "Flood", iso="IND"), goev(2, "Earthquake", iso="BGD"),
                               goev(3, "Flood", iso="BGD")]))
    comps, _ = C.join(n)
    c = comp_of(comps, ("gdacs", "FL", "1"))
    assert ("go_event", "3") in c and ("go_event", "1") not in c and ("go_event", "2") not in c
    n = C.build_nodes(runs([gd(1, "DR", iso="KEN", frm="2027-01-01")],
                           go=[goev(1, "Drought", iso="KEN", start="2027-01-01")]))
    comps, _ = C.join(n)
    assert ("go_event", "1") not in comp_of(comps, ("gdacs", "DR", "1"))


def test_f2_tie_rules():
    # two GDACS floods at equal distance: interval containment decides
    a = gd(1, "FL", iso="BGD", frm="2027-01-01", to="2027-01-20")
    b = gd(2, "FL", iso="BGD", frm="2027-01-09", to="2027-01-09")
    n = C.build_nodes(runs([a, b], go=[goev(1, "Flood", iso="BGD", start="2027-01-05")]))
    comps, _ = C.join(n)
    assert ("go_event", "1") in comp_of(comps, ("gdacs", "FL", "1"))
    # full tie: no link, logged
    a = gd(1, "FL", iso="BGD", frm="2027-01-01", to="2027-01-01")
    b = gd(2, "FL", iso="BGD", frm="2027-01-09", to="2027-01-09")
    n = C.build_nodes(runs([a, b], go=[goev(1, "Flood", iso="BGD", start="2027-01-05")]))
    comps, edges = C.join(n)
    assert any(len(c) == 1 and ("go_event", "1") in c for c in comps)
    assert any(e["note"] == "tie" and e["rule"] == "F2_iso3_hazard_window" for e in edges)


def test_explicit_key_blocks_fallback():
    g1 = gd(1, "FL", iso="BGD", frm="2027-01-01", glide="FL-2027-000005-BGD")
    g2 = gd(2, "FL", iso="BGD", frm="2027-01-04")
    ev = goev(1, "Flood", iso="BGD", start="2027-01-04", glide="FL-2027-000005")
    comps, _ = C.join(C.build_nodes(runs([g1, g2], go=[ev])))
    assert ("go_event", "1") in comp_of(comps, ("gdacs", "FL", "1"))
    assert ("go_event", "1") not in comp_of(comps, ("gdacs", "FL", "2"))


def test_eu27_cems_never_enters_nodes():
    n = C.build_nodes(runs([gd(1, iso="ITA")],
                           cems_=[cems("EMSR1", 1, countries=["Italy"]),
                                  cems("EMSR2", 1, countries=["ITA"])]))
    assert not any(k[0] == "cems" for k in n)


# --- rungs, statuses, stages -------------------------------------------------------------
def _card(rs, key, now=NOW, **kw):
    n = C.build_nodes(rs)
    comps, _ = C.join(n)
    return C.build_card(comp_of(comps, key), n, now, **kw)


def test_stage1_warning_only_not_yet_then_absent():
    rs = runs([gd(1)])
    c = _card(rs, ("gdacs", "EQ", "1"), now=dt.datetime(2027, 1, 5, tzinfo=UTC))
    assert c["stage"] == 1 and c["rungs"]["W"] == "present"
    assert c["rungs"]["R"] == "not yet" and c["rungs"]["D"] == "not yet"
    assert c["warning_precision"] == "onset-proxy"
    c = _card(rs, ("gdacs", "EQ", "1"), now=dt.datetime(2027, 4, 1, tzinfo=UTC))
    assert c["rungs"]["R"] == "absent" and c["rungs"]["D"] == "absent"


def test_missing_when_source_gap_of_seven_days():
    rs = runs([gd(1)])
    gaps = {"ifrc_go": {dt.date(2027, 1, 10) + dt.timedelta(days=i) for i in range(7)}}
    c = _card(rs, ("gdacs", "EQ", "1"), now=dt.datetime(2027, 4, 1, tzinfo=UTC),
              source_gaps=gaps)
    assert c["rungs"]["D"] == "missing" and c["rungs"]["R"] == "missing"
    gaps6 = {"ifrc_go": {dt.date(2027, 1, 10) + dt.timedelta(days=i) for i in range(6)}}
    c = _card(rs, ("gdacs", "EQ", "1"), now=dt.datetime(2027, 4, 1, tzinfo=UTC),
              source_gaps=gaps6)
    assert c["rungs"]["D"] == "absent"                 # a 6-day gap is recovered (window 7)


def test_flood_has_no_warning_source():
    c = _card(runs([gd(1, "FL", alert="red", iso="BGD")]), ("gdacs", "FL", "1"))
    assert c["rungs"]["W"] == "no source" and c["stage"] == 0


def test_gdacs_alert_upgraded_later_is_snapshot_time():
    s1 = gd(1, "TC", alert="green", frm="2027-01-01T00:00:00Z", fetched="2027-01-01T04:17:00Z")
    s2 = gd(1, "TC", alert="orange", frm="2027-01-01T00:00:00Z", fetched="2027-01-03T04:17:00Z")
    c = _card(runs([s1, s2]), ("gdacs", "TC", "1"))
    assert c["warning_precision"] == "snapshot" and c["t_warning"].startswith("2027-01-03")


def test_pager_yellow_is_warning():
    t = int(dt.datetime(2027, 1, 1, 3, 0, tzinfo=UTC).timestamp() * 1000)
    c = _card(runs(usgs=[us("u1", t, alert="yellow")]), ("usgs", "u1"))
    assert c["rungs"]["W"] == "present" and c["stage"] == 1


def test_stage2_3_4_5_and_collapse():
    g = gd(1, glide="EQ-2027-000001-PHL")
    ev = goev(7, glide="EQ-2027-000001")
    c = _card(runs([g], go=[ev]), ("gdacs", "EQ", "1"))
    assert c["stage"] == 2
    c = _card(runs([g], go=[ev, goap(1, 7)]), ("gdacs", "EQ", "1"))
    assert c["stage"] == 3 and c["lag_onset_decision_days"] == pytest.approx(2.25, abs=0.01)
    funded = goap(1, 7, fund=30.0, fetched="2027-01-06T04:17:00Z")
    c = _card(runs([g], go=[ev, goap(1, 7), funded]), ("gdacs", "EQ", "1"))
    assert c["stage"] == 4 and c["stage_label"] == "funded, fragmented"
    rs = runs([g], cems_=[cems("EMSR5", 1)], go=[ev, goap(1, 7), funded])
    c = _card(rs, ("gdacs", "EQ", "1"))
    assert c["stage"] == 5 and c["decision_systems"] == ["CEMS", "IFRC"]
    c = _card(rs, ("gdacs", "EQ", "1"), now=dt.datetime(2027, 9, 1, tzinfo=UTC))
    assert c["closed"] and c["collapsed"] is True
    assert c["stage_label"] == "coordinated, then collapsed"


def test_dref_counts_as_money_and_learning_flag():
    g = gd(1, glide="EQ-2027-000001-PHL")
    ev = goev(7, glide="EQ-2027-000001")
    full = goap(1, 7, atype=1, req=100, fund=80, fetched="2027-01-05T04:17:00Z")
    rs = runs([g], cems_=[cems("EMSR5", 1)], go=[ev, goap(2, 7, atype=0, req=10), full])
    later = dt.datetime(2027, 9, 1, tzinfo=UTC)
    c = _card(rs, ("gdacs", "EQ", "1"), now=later, prior_lags={("PHL", "EQ"): 5.0})
    assert c["collapsed"] is False and c["learned"] is True and c["stage"] == 6
    c = _card(rs, ("gdacs", "EQ", "1"), now=later, prior_lags={("PHL", "EQ"): 1.0})
    assert c["stage"] == 5 and c["learned"] is False
    c = _card(rs, ("gdacs", "EQ", "1"), now=later, prior_lags={})
    assert c["learned"] is None


def test_eu27_card_withholds_cems():
    c = _card(runs([gd(1, iso="ITA")]), ("gdacs", "EQ", "1"))
    assert c["eu27"] and c["rungs"]["CEMS"] == "withheld" and c["rungs"]["C"] == "withheld"


def test_attention_none_means_no_source_and_counts_as_recognition():
    rs = runs([gd(1)])
    c = _card(rs, ("gdacs", "EQ", "1"))
    assert c["rungs"]["A"] == "no source"
    att = {"status": "present", "t": dt.datetime(2027, 1, 2, tzinfo=UTC), "title": "X"}
    c = _card(rs, ("gdacs", "EQ", "1"), attention=att)
    assert c["rungs"]["R"] == "present" and c["stage"] == 2


def test_population_rule():
    n = C.build_nodes(runs([gd(1, alert="green"), gd(2)], go=[goev(5, "Epidemic"),
                                                              goap(6, 5)]))
    comps, _ = C.join(n)
    pop = C.card_population(comps, n)
    keys = set().union(*pop)
    assert ("gdacs", "EQ", "2") in keys
    assert ("gdacs", "EQ", "1") not in keys            # green, no decision
    assert ("go_appeal", "6") not in keys              # epidemic: not a natural hazard


def test_safe_aggregate_has_no_eu27_cems_trace():
    rs = runs([gd(1, iso="ITA", typ="FL")],
              cems_=[cems("EMSR1", 1, countries=["Italy"], cat="Flood")])
    n = C.build_nodes(rs)
    comps, _ = C.join(n)
    agg = C.safe_aggregate([C.build_card(c, n, NOW) for c in comps])
    rs2 = runs([gd(1, iso="ITA", typ="FL")])
    n2 = C.build_nodes(rs2)
    agg2 = C.safe_aggregate([C.build_card(c, n2, NOW) for c in C.join(n2)[0]])
    assert agg == agg2                                 # with or without the EU27 record


# --- pageview rule and E2 filters -------------------------------------------------------
def test_candidate_titles():
    assert "Hurricane Melissa" in C.candidate_titles("TC", 2027, None, "MELISSA-27")
    assert C.candidate_titles("EQ", 2027, "Peru", None)[0] == "2027 Peru earthquake"
    assert C.candidate_titles("VO", 2027, "Peru", "Misti") == []


def test_match_article_rules():
    on = dt.date(2027, 3, 1)
    ok = {"title": "2027 Peru earthquake", "exists": True, "ns": 0,
          "created": dt.date(2027, 3, 1)}
    assert C.match_article([ok, dict(ok)], on) == ("present", "2027 Peru earthquake")
    old = dict(ok, created=dt.date(2020, 1, 1))
    assert C.match_article([old], on) == ("none", None)
    dis = dict(ok, disambiguation=True)
    season = dict(ok, title="2027 Pacific hurricane season")
    lst = dict(ok, title="List of earthquakes in 2027")
    sec = dict(ok, section_redirect=True)
    assert C.match_article([dis, season, lst, sec], on) == ("none", None)
    other = dict(ok, title="2027 Peru earthquakes")
    assert C.match_article([ok, other], on) == ("ambiguous", None)


def test_e2a_earthquakes_and_placebos():
    d = dt.date(2027, 3, 1)
    ev = {"hazard": "EQ", "onset": d, "iso3": {"PER"}, "magnitudes": [6.9]}
    assert C.e2_refusal(ev, dt.date(2027, 3, 2)).startswith("E2a")
    assert C.e2_refusal(dict(ev, magnitudes=[None]), d).startswith("E2a")
    assert C.e2_refusal(dict(ev, magnitudes=[6.5]), d) is None
    assert C.e2_refusal(dict(ev, onset=dt.date(2028, 1, 1), magnitudes=[7.5]), d) is None
    assert C.e2_refusal(dict(ev, magnitudes=[6.0]), d, title="Mitochondria").startswith("E2a")


def test_e2c_floods_and_rivers():
    d = dt.date(2027, 3, 1)
    eu = {"hazard": "FL", "onset": d, "iso3": {"ITA"}}
    assert C.e2_refusal(eu, d).startswith("E2c")
    assert C.e2_refusal({"hazard": "FL", "onset": d, "iso3": set()}, d).startswith("E2c")
    non = {"hazard": "FL", "onset": d, "iso3": {"BGD"}}
    assert C.e2_refusal(non, d, title="2027 Bangladesh floods") is None
    assert C.e2_refusal(non, d, title="2027 Central European floods").startswith("E2c")
    assert C.e2_refusal(non, d, title="Padma River").startswith("E2c")
    assert C.e2_refusal({"hazard": "EQ", "onset": dt.date(2028, 2, 1), "iso3": {"PER"},
                         "magnitudes": [6]}, d, title="2028 Peru floods") is None


def test_e2d_atlantic_storms():
    d = dt.date(2027, 9, 1)
    us_ = {"hazard": "TC", "onset": d, "iso3": {"USA"}, "lat": 25, "lon": -80}
    assert C.e2_refusal(us_, d).startswith("E2d")
    unk = {"hazard": "TC", "onset": d, "iso3": {"MEX"}}
    assert C.e2_refusal(unk, d).startswith("E2d")          # no position: refused
    pac = {"hazard": "TC", "onset": d, "iso3": {"PHL"}, "lat": 15, "lon": 125}
    assert C.e2_refusal(pac, d) is None
    old = {"hazard": "TC", "onset": dt.date(2026, 12, 1), "iso3": {"USA"}, "lat": 25,
           "lon": -80}
    assert C.e2_refusal(old, d) is None


def test_e2_flags_off_until_scoring():
    assert C.GWI_V2_SCORED is False and C.FLOOD_TEST_SCORED is False
    assert C.HURRICANE_SEASONS_SCORED == set()


def test_pageview_url_is_english_per_article_only():
    u = C.pageview_url("2027 Peru earthquake", dt.date(2027, 2, 22), dt.date(2027, 3, 31))
    assert "/per-article/en.wikipedia/all-access/user/2027_Peru_earthquake/daily/" in u


def test_attention_threshold():
    on = dt.date(2027, 3, 1)
    assert C.attention_from_views({on + dt.timedelta(days=3): 1000}, on) == (
        "present", on + dt.timedelta(days=3))
    assert C.attention_from_views({on - dt.timedelta(days=1): 9999,
                                   on + dt.timedelta(days=31): 9999}, on)[0] == "absent"


# --- H3 stream test ---------------------------------------------------------------------
def _unit(m, cl):
    return {"measurable": m, "cluster": cl}


def test_h3_unit_population_and_measurability():
    g = gd(1, glide="EQ-2027-000001-PHL")
    ev = goev(7, glide="EQ-2027-000001")
    c = _card(runs([g], go=[ev, goap(1, 7)]), ("gdacs", "EQ", "1"))
    u = C.h3_unit(c)
    assert u["measurable"] is True
    c = _card(runs(go=[goev(8, start="2027-01-01"), goap(2, 8)]), ("go_event", "8"))
    u = C.h3_unit(c)
    assert u is not None and u["measurable"] is False      # unanchored counts against
    c = _card(runs([gd(1, iso="ITA")], go=[goev(9, iso="ITA"), goap(3, 9)]),
              ("gdacs", "EQ", "1"))
    assert C.h3_unit(c) is None                            # EU27 out of the test
    c = _card(runs([gd(1, frm="2027-06-05T00:00:00Z")]), ("gdacs", "EQ", "1"))
    assert C.h3_unit(c) is None                            # no decision / outside window


def test_h3_score_verdicts():
    pas = [_unit(True, (i,)) for i in range(40)] + [_unit(False, (100 + i,)) for i in range(10)]
    assert C.h3_score(pas)["verdict"] == "PASS"
    fail = [_unit(False, (i,)) for i in range(40)] + [_unit(True, (100 + i,)) for i in range(10)]
    assert C.h3_score(fail)["verdict"] == "FAIL"
    mid = [_unit(i % 2 == 0, (i,)) for i in range(50)]
    assert C.h3_score(mid)["verdict"] == "not decided at this size"
    small = [_unit(True, (i,)) for i in range(19)]
    assert C.h3_score(small)["verdict"] == "not testable at this size"
    # clusters: many measurable units in one cluster cannot carry a PASS alone
    clump = [_unit(True, ("A",)) for _ in range(40)] + [_unit(False, (i,)) for i in range(25)]
    assert C.h3_score(clump)["verdict"] != "PASS"


def test_cp_bounds_known_values():
    lo, hi = C.cp_bounds(35, 50)
    assert 0.57 < lo < 0.58 and 0.80 < hi < 0.81
