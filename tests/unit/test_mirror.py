"""Synthetic checks of the field-presence check and the card job (session 3.4).

Every record is invented. Evidence class: infrastructure.
"""
import datetime as dt
import json

from emo.stream import mirror as M
from emo.stream import presence as P
from emo.stream import store
from tests.unit.test_loop_cards import cems, gd, goap, goev, runs, us

UTC = dt.UTC
NOW = dt.datetime(2027, 1, 15, tzinfo=UTC)


class Untouchable(dict):
    """A record whose fields other than `countries` must never be read."""

    def get(self, k, default=None):
        assert k == "countries", f"EU27 CEMS field read: {k}"
        return super().get(k, default)

    def __getitem__(self, k):
        assert k == "countries", f"EU27 CEMS field read: {k}"
        return super().__getitem__(k)

    def __iter__(self):
        raise AssertionError("EU27 CEMS keys listed")


def test_eu27_cems_never_read_and_not_counted():
    eu = [Untouchable(code=f"EU{i}", countries=["Germany"], category="Fire") for i in range(30)]
    rs = runs(cems_=eu + [cems(f"C{i}", countries=("PHL",)) for i in range(20)])
    groups = P.latest_records(rs)
    assert len(groups["cems"]) == 20
    agg = P.presence(rs)
    assert agg["cems"]["fields"]["countries"] == {"present": 1.0, "parses": 1.0}


def test_small_groups_hidden_and_shares_floored():
    rs = runs(gdacs=[gd(i) for i in range(19)])
    assert P.presence(rs)["gdacs/search"] == "n<20"
    # 21 records, 20 with a glide: 20/21 = 0.952 -> floored to 0.95
    recs = [gd(i, glide=f"EQ-2027-{i:06d}-PHL") for i in range(20)] + [gd(99)]
    s = P.presence(runs(gdacs=recs))["gdacs/search"]["fields"]["p.glide"]
    assert s == {"present": 0.95, "parses": 0.95}


def test_dedup_by_node_key_uses_latest_snapshot():
    recs = [gd(1, alert="green", fetched="2027-01-01T04:17:00Z") for _ in range(25)]
    recs += [gd(i) for i in range(2, 22)]
    groups = P.latest_records(runs(gdacs=recs))
    assert len(groups["gdacs/search"]) == 21


def test_names_in_cems_countries_give_the_table_verdict():
    rs = runs(cems_=[cems(f"C{i}", countries=("Philippines",)) for i in range(20)])
    agg = P.presence(rs)
    assert agg["cems"]["fields"]["countries"] == {"present": 1.0, "parses": 0.0}
    v = P.verdicts(agg)
    assert v["cems:countries"] == "names: CEMS table"
    assert v["cems:gdacsId"] == "wrong name"          # fixture leaves it None
    assert v["cems:activationTime"] == "reads"


def test_key_names_hold_no_values_or_codes():
    recs = [gd(i) for i in range(20)]
    for r in recs:
        r["properties"]["PHL"] = 1                    # code-like key: left out
        r["properties"]["x"] = 1                      # too short: left out
    names = P.presence(runs(gdacs=recs))["gdacs/search"]["key_names"]
    assert "properties.alertlevel" in names
    assert "properties.PHL" not in names and "properties.x" not in names
    blob = json.dumps(P.presence(runs(gdacs=recs)))
    assert "2027-01-01" not in blob                   # no dates or values leave


def test_source_gaps_from_manifest():
    lines = [{"run_id": "2027-01-01T041700Z", "sources": {s: {"error": None} for s in M.SOURCES}},
             {"run_id": "2027-01-03T041700Z",
              "sources": {**{s: {"error": None} for s in M.SOURCES},
                          "cems": {"error": "HTTPError"}}}]
    g = M.source_gaps(lines, dt.date(2027, 1, 4))
    assert g["gdacs"] == {dt.date(2027, 1, 2), dt.date(2027, 1, 4)}
    assert g["cems"] == {dt.date(2027, 1, 2), dt.date(2027, 1, 3), dt.date(2027, 1, 4)}


def test_build_cards_and_edge_counts():
    rs = runs(gdacs=[gd(1, glide="EQ-2027-000001-PHL")],
              usgs=[us("us1", 1798772400000, alert="orange")],
              cems_=[cems("EMSR1", gdacs_id=1)],
              go=[goev(5, glide="EQ-2027-000001-PHL"), goap(7, 5)])
    cards, edges = M.build_cards(rs, NOW, {})
    assert len(cards) >= 1
    cnt = M.edge_counts(edges)
    assert cnt["K1_gdacsId"] == 1 and cnt["K2_glide"] == 1 and cnt["K3_event_id"] == 1


def test_aggregates_end_to_end_holds_only_section_11(tmp_path, monkeypatch):
    monkeypatch.setenv(store.KEY_ENV, "synthetic-test-key")
    rs = runs(gdacs=[gd(1)], cems_=[cems("EMSR1", gdacs_id=1),
                                    cems("EMSR2", countries=("DEU",), cat="Flood")])
    store.write_run(tmp_path, {"run_id": "2027-01-02T041700Z"},
                    {k: {"records": v["records"], "error": None, "requests": []}
                     for k, v in rs[0]["sources"].items()})
    agg = M.aggregates(tmp_path, NOW)
    assert set(agg) == {"version", "built_at", "last_ingestion_run", "ingestion_runs_read",
                        "safe_aggregate", "edge_rule_counts", "source_days_lost",
                        "evidence_class", "note"}
    blob = json.dumps(agg)
    for leak in ("EMSR", "DEU", "PHL", "eventid"):
        assert leak not in blob
    assert agg["last_ingestion_run"] == "2027-01-02T041700Z"


def test_mirror_page_renders_counts_and_last_run(tmp_path, monkeypatch):
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_site", "scripts/build_site.py")
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    (tmp_path / "data/mirror").mkdir(parents=True)
    (tmp_path / "data/mirror/aggregates.json").write_text(json.dumps({
        "built_at": "2027-01-15T13:00:00+00:00", "last_ingestion_run": "2027-01-15T041700Z",
        "safe_aggregate": {"2027-01|EQ|stage3": 2, "2027-01|EQ|D=present": 2,
                           "2027-01|EQ|B=not yet": 2},
        "edge_rule_counts": {"K1_gdacsId": 1}, "source_days_lost": {"gdacs": 0}}))
    monkeypatch.setattr(bs, "ROOT", tmp_path)
    page = bs.mirror_page("<!doctype html><html><head><title>x</title><style></style>")
    assert "2027-01-15T13:00:00+00:00" in page and "<title>EMO mirror</title>" in page
    assert "No per-event card is published" in page and "K1_gdacsId" in page
    assert "<td>2</td>" in page
