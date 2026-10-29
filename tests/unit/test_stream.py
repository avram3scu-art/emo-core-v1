"""Session 3.2: exclusions E1-E3, guarded HTTP, encrypted append-only store, counts.

All data here are synthetic; no stream record is opened.
"""
import datetime as dt
import json
import logging
import shutil
import subprocess

import pytest

from emo.stream import exclusions as ex
from emo.stream import fetchers, store
from emo.stream.counts import monthly_counts

# ---- E1 -------------------------------------------------------------------------------


def cems(cat="Flood", countries=("Italy",), event="2026-11-05T10:00:00",
         act="2026-11-06T08:00:00", sub=None, code="EMSR900"):
    return {"code": code, "category": cat, "subCategory": sub, "countries": list(countries),
            "eventTime": event, "activationTime": act}


@pytest.mark.parametrize("rec", [
    cems(),                                                    # EU flood in window
    cems(countries=("Spain", "Morocco")),                      # any EU27 country
    cems(event="2026-10-20T00:00:00", act="2026-10-30T09:00:00"),   # activation on day 1
    cems(event="2029-01-31T23:00:00", act="2029-02-03T00:00:00"),   # event on last day
    cems(cat="Storm", sub="Flash flood"),                      # flood as sub-category
    cems(cat="FLOOD", countries=("DE",)),                      # ISO2, upper case
    cems(countries=("NLD",)),                                  # ISO3
    cems(countries=[{"name": "Belgium"}]),                     # dict form
    cems(event=None, act=None),                                # undated: dropped
    cems(event="bad", act=""),                                 # unreadable dates: dropped
])
def test_e1_drops(rec):
    assert ex.e1_drops(rec)
    assert ex.apply_e1([rec]) == []


@pytest.mark.parametrize("rec", [
    cems(countries=("Pakistan",)),                             # flood outside EU27
    cems(cat="Wildfire"),                                      # EU, not flood
    cems(event="2026-10-01T00:00:00", act="2026-10-29T23:00:00"),   # before window
    cems(event="2029-02-01T00:00:00", act="2029-02-02T00:00:00"),   # after window
    cems(countries=("United Kingdom", "Norway")),              # Europe but not EU27
])
def test_e1_keeps(rec):
    assert not ex.e1_drops(rec)
    assert ex.apply_e1([rec]) == [rec]


def test_e1_is_silent(capsys, caplog):
    caplog.set_level(logging.DEBUG)
    kept = ex.apply_e1([cems(), cems(countries=("Chile",), code="EMSR901")])
    assert [r["code"] for r in kept] == ["EMSR901"]
    out = capsys.readouterr()
    assert out.out == "" and out.err == "" and caplog.records == []
    assert all(not any("drop" in k.lower() or "e1" in k.lower() for k in r) for r in kept)


class FakeResp:
    def __init__(self, payload, status=200, url="https://x", headers=None):
        self.payload, self.status_code, self.url = payload, status, url
        self.headers = headers or {}

    def json(self):
        return self.payload

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests
            raise requests.HTTPError(str(self.status_code))


class FakeSession:
    def __init__(self, pages):
        self.pages, self.headers, self.urls = list(pages), {}, []

    def get(self, url, params=None, timeout=None, allow_redirects=False):
        self.urls.append(url)
        return self.pages.pop(0)


def test_fetch_cems_applies_e1_before_return():
    sess = FakeSession([
        FakeResp({"results": [cems()], "next": fetchers.CEMS_URL + "?offset=100"}),
        FakeResp({"results": [cems(countries=("Peru",), code="EMSR902")], "next": None}),
    ])
    recs = fetchers.fetch_cems(fetchers.Http(sess, pause=0), dt.date(2026, 11, 7))
    assert [r["code"] for r in recs] == ["EMSR902"]
    assert "_emo_fetched_at" in recs[0]


# ---- E2, E3: host guard -----------------------------------------------------------------


@pytest.mark.parametrize("url", [
    "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries",      # E3
    "https://www.fema.gov/openfema",
    "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/x",    # E2
    "https://en.wikipedia.org/w/api.php",
    "https://dumps.wikimedia.org/other/pageviews/",
    "https://www.wikidata.org/w/api.php",
    "https://example.org/data",                                             # not allowlisted
    "http://earthquake.usgs.gov/fdsnws/event/1/query",                      # not https
    "https://earthquake.usgs.gov.evil.example/x",
])
def test_guard_refuses(url):
    with pytest.raises(ex.ExcludedSource):
        ex.check_url(url)


def test_guard_allows_stream_hosts():
    for u in (fetchers.GDACS_SEARCH, fetchers.GDACS_CACHE, fetchers.USGS_QUERY,
              fetchers.CEMS_URL, fetchers.GO_BASE + "appeal/"):
        assert ex.check_url(u) == u


def test_no_fetcher_targets_excluded_hosts():
    assert set(fetchers.FETCHERS) == {"gdacs", "usgs", "cems", "ifrc_go"}
    for suffix in ("fema.gov", "wikipedia.org", "wikimedia.org"):
        assert all(not h.endswith(suffix) for h in ex.ALLOWED_HOSTS)


def test_redirect_and_next_cannot_leave_allowlist():
    sess = FakeSession([FakeResp({}, status=302,
                                 headers={"Location": "https://www.fema.gov/x"})])
    with pytest.raises(ex.ExcludedSource):
        fetchers.Http(sess, pause=0).get_json(fetchers.GO_BASE + "event/")
    sess = FakeSession([FakeResp({"results": [], "next": "https://en.wikipedia.org/x"})])
    with pytest.raises(ex.ExcludedSource):
        fetchers._go_pages(fetchers.Http(sess, pause=0), "event", {})


def test_gdacs_pagination_and_empty_page():
    full = {"features": [{"properties": {"eventid": i}} for i in range(100)]}
    sess = FakeSession([FakeResp(full), FakeResp(None, status=204), FakeResp({"features": []})])
    recs = fetchers.fetch_gdacs(fetchers.Http(sess, pause=0), dt.date(2026, 11, 7))
    assert len(recs) == 100 and len(sess.urls) == 3


# ---- encrypted, append-only store ------------------------------------------------------

needs_openssl = pytest.mark.skipif(shutil.which("openssl") is None, reason="no openssl")


def test_write_refuses_without_key(tmp_path, monkeypatch):
    monkeypatch.delenv(store.KEY_ENV, raising=False)
    with pytest.raises(store.MissingKey):
        store.write_run(tmp_path, {"run_id": "r"}, {})
    assert not (tmp_path / "data").exists()


@needs_openssl
def test_roundtrip_and_no_plaintext(tmp_path, monkeypatch):
    monkeypatch.setenv(store.KEY_ENV, "synthetic-test-key")
    srcs = {"cems": {"records": [{"code": "EMSR777", "secret_marker": "zzqx"}],
                     "requests": [{"url": "u", "status": 200}], "error": None}}
    line = store.write_run(tmp_path, {"run_id": "2026-11-01T041700Z"}, srcs)
    blob = (tmp_path / line["file"]).read_bytes()
    assert b"zzqx" not in blob and b"EMSR777" not in blob
    assert store.read_run(tmp_path / line["file"])["sources"] == srcs
    man = (tmp_path / "data/stream/MANIFEST.jsonl").read_text()
    assert "EMSR777" not in man and "zzqx" not in man
    with pytest.raises(FileExistsError):
        store.write_run(tmp_path, {"run_id": "2026-11-01T041700Z"}, srcs)


@needs_openssl
def test_verify_append_only(tmp_path, monkeypatch):
    monkeypatch.setenv(store.KEY_ENV, "k")
    git = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True,  # noqa: E731
                                    capture_output=True)
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    empty = {"x": {"records": [], "requests": [], "error": None}}
    store.write_run(tmp_path, {"run_id": "a"}, empty)
    git("add", "-A")
    git("commit", "-qm", "1")
    store.write_run(tmp_path, {"run_id": "b"}, empty)
    git("add", "-A")
    assert store.verify_append_only(tmp_path) == []
    man = tmp_path / "data/stream/MANIFEST.jsonl"
    man.write_text(man.read_text().replace('"a"', '"z"'))
    (tmp_path / "data/stream/log/a.json.gz.enc").write_bytes(b"changed")
    git("add", "-A")
    probs = store.verify_append_only(tmp_path)
    assert len(probs) == 2


# ---- counts ---------------------------------------------------------------------------


def test_monthly_counts_explicit_links_and_eu27_left_out():
    run = {"sources": {
        "gdacs": {"records": [
            {"properties": {"eventid": 11, "eventtype": "EQ", "fromdate": "2026-11-02"}},
            {"properties": {"eventid": 12, "eventtype": "FL", "fromdate": "2026-11-03",
                            "glide": "FL-2026-000123-PAK"}},
            {"properties": {"eventid": 13, "eventtype": "TC", "fromdate": "2026-11-04"}}]},
        "cems": {"records": [
            {"code": "EMSR1", "countries": ["Chile"], "gdacsId": "11",
             "activationTime": "2026-11-03"},
            {"code": "EMSR2", "countries": ["Greece"], "gdacsId": "13",     # EU27: left out
             "activationTime": "2026-11-05", "category": "Wildfire"}]},
        "ifrc_go": {"records": [
            {"_emo_feed": "event", "id": 5, "glide": "FL-2026-000123-PAK",
             "disaster_start_date": "2026-11-03T00:00:00Z"},
            {"_emo_feed": "appeal_running", "id": 9, "event": 5, "atype": 0,
             "start_date": "2026-11-04"}]},
        "usgs": {"records": [{"_emo_feed": "comcat", "id": "us1",
                              "properties": {"time": 1793000000000}}]},
    }}
    c = monthly_counts([run, run])                     # duplicates across runs count once
    nov = c["2026-11"]
    assert nov["gdacs_events"] == 3
    assert nov["cems_activations_non_eu27"] == 1
    assert nov["ifrc_dref"] == 1 and nov["ifrc_go_events"] == 1
    assert nov["linked_events_explicit_keys"] == 2     # 11 via CEMS, 12 via GLIDE; 13 not
    assert sum(v.get("usgs_m4_5_events", 0) for v in c.values()) == 1


def test_counts_read_no_outcome_fields():
    import inspect

    from emo.stream import counts
    src = inspect.getsource(counts.monthly_counts)
    for field in ("amount_funded", "alertlevel", "fatalit", "losspager", "num_affected"):
        assert field not in src


def test_cli_ran_today(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("sd", "scripts/stream_daily.py")
    sd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sd)
    assert sd.ran_today(tmp_path) == 1
    d = tmp_path / "data/stream"
    d.mkdir(parents=True)
    today = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    (d / "MANIFEST.jsonl").write_text(json.dumps({"run_id": today + "T041700Z"}) + "\n")
    assert sd.ran_today(tmp_path) == 0


@needs_openssl
def test_empty_source_is_flagged(tmp_path, monkeypatch):
    import importlib.util
    spec = importlib.util.spec_from_file_location("sd2", "scripts/stream_daily.py")
    sd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sd)
    monkeypatch.setenv(store.KEY_ENV, "k")
    monkeypatch.setattr(sd, "FETCHERS", {"a": lambda h, d: [{"x": 1}], "b": lambda h, d: []})
    assert sd.run(tmp_path) == 2
    line = json.loads((tmp_path / "data/stream/MANIFEST.jsonl").read_text())
    assert line["sources"]["a"]["has_records"] and line["sources"]["a"]["error"] is None
    assert not line["sources"]["b"]["has_records"]
    assert line["sources"]["b"]["error"] == "EmptyResponse"
