"""Synthetic checks of the H8 caller, ledger, index and scorer (session 3.6).

Every card, record, answer and outcome here is invented; the model is a stub. No stream
record and no network is used. Evidence class: infrastructure.
"""
import datetime as dt
import importlib.util
import json

import pytest

from emo.selfmodel import ledger as L
from emo.selfmodel import protocol as P
from emo.selfmodel import score as S
from emo.stream import store
from tests.unit.test_loop_cards import gd, goap, goev

UTC = dt.UTC
KEY = b"synthetic-test-key"
T0 = dt.datetime(2026, 11, 5, 8, 0, tzinfo=UTC)


def card(cid, onset="2026-11-03T00:00:00+00:00", d="not yet", b="not yet", t_dec=None,
         t_money=None, iso=("PHL",), hz="EQ", eu27=False, closed=False, stage=1):
    return {"card_id": cid, "hazard": hz, "iso3": list(iso), "eu27": eu27, "anchored": True,
            "onset": onset, "t_decision": t_dec, "t_money": t_money, "closed": closed,
            "rungs": {"W": "present", "R": "not yet", "D": d, "B": b},
            "stage": stage, "stage_label": "warned", "decision_systems": []}


def ex(*nodes, seen="2026-11-03T05:00:00+00:00"):
    return {"component": list(nodes), "first_seen": dt.datetime.fromisoformat(seen)}


def empty():
    return {"forecasts": [], "components": {}, "snapshots": [], "missed": [],
            "stream_runs": []}


def stub(p=0.3):
    calls = []

    def fn(system, user):
        calls.append(user)
        return {"kind": "answer", "model_returned": L.MODEL, "response_id": f"msg_{len(calls)}",
                "response_text": json.dumps({"p": p, "coherent_whole": "x"}), "error": None}
    fn.calls = calls
    return fn


def state(sid, t, cards):
    return {"stream_run_id": sid, "t": t, "cards": cards}


# --- caller rules ------------------------------------------------------------------------
def test_forecast_once_at_earliest_run_and_matched_by_shared_node():
    fn = stub()
    r1 = L.process([state("s1", T0, [(card("gdacs|EQ|1"), ex("gdacs|EQ|1"))])], empty(), T0,
                   fn, KEY, "h")
    assert [f["target"] for f in r1["forecasts"]] == ["D"] and r1["status"] == "forecasts"
    prior = L.merge([{**r1, "stream_runs": ["s1"]}])
    # next day the card has gained a node and a new id; still the same card for D
    t1 = T0 + dt.timedelta(days=1)
    r2 = L.process([state("s2", t1, [(card("usgs|u9"), ex("gdacs|EQ|1", "usgs|u9"))])],
                   prior, t1, fn, KEY, "h")
    assert r2["forecasts"] == [] and len(fn.calls) == 1


def test_no_key_records_missed_and_never_forecasts_it_later():
    r1 = L.process([state("s1", T0, [(card("c1"), ex("c1"))])], empty(), T0, None, KEY, "h")
    assert r1["forecasts"] == [] and r1["missed"][0]["reason"] == "no key"
    assert r1["status"] == "no key"
    t1 = T0 + dt.timedelta(days=1)
    r2 = L.process([state("s2", t1, [(card("c1"), ex("c1"))])], L.merge([r1]), t1, stub(),
                   KEY, "h")
    assert r2["forecasts"] == [] and r2["missed"] == []


def test_account_error_is_missed_other_failures_are_rows_scored_half():
    def acct(s, u):
        return {"kind": "account", "model_returned": None, "response_id": None,
                "response_text": None, "error": "HTTP 401"}

    cards = [(card(f"c{i}"), ex(f"c{i}")) for i in range(3)]
    r = L.process([state("s1", T0, cards)], empty(), T0, acct, KEY, "h")
    assert r["forecasts"] == [] and {m["reason"] for m in r["missed"]} == {"api_unavailable"}

    def failed(s, u):
        return {"kind": "failed", "model_returned": None, "response_id": None,
                "response_text": None, "error": "HTTP 529"}
    r = L.process([state("s1", T0, cards)], empty(), T0, failed, KEY, "h")
    assert len(r["forecasts"]) == 3 and all(f["p_ai"] is None for f in r["forecasts"])


def test_eligibility_rules_eu27_cutoff_first_seen_closed():
    cs = [(card("eu", eu27=True), ex("eu")),
          (card("old", onset="2026-10-30T00:00:00+00:00"), ex("old")),
          (card("seen", ), ex("seen", seen="2026-10-30T23:00:00+00:00")),
          (card("closed", closed=True), ex("closed")),
          (card("ok"), ex("ok"))]
    r = L.process([state("s1", T0, cs)], empty(), T0, stub(), KEY, "h")
    assert [f["card_id"] for f in r["forecasts"]] == ["ok"]
    # training snapshots ignore the onset/earliest-seen dates but still drop EU27 and closed
    assert {tuple(s["component"]) for s in r["snapshots"]} == {("old",), ("seen",), ("ok",)}


def test_replayed_earlier_run_never_forecasts():
    t_old = T0 - dt.timedelta(hours=20)
    r = L.process([state("s0", t_old, [(card("c1"), ex("c1"))]),
                   state("s1", T0, [(card("c1"), ex("c1"))])], empty(), T0, stub(), KEY, "h")
    assert r["forecasts"] == [] and r["missed"][0]["reason"] == "no caller run"


def test_cap_at_n_target(monkeypatch):
    monkeypatch.setattr(P, "N_TARGET", 2)
    cs = [(card(f"c{i}"), ex(f"c{i}")) for i in range(5)]
    r = L.process([state("s1", T0, cs)], empty(), T0, stub(), KEY, "h")
    assert len(r["forecasts"]) == 2 and r["forecasts_total"] == 2


def test_row_fields_hash_payload_and_b_target():
    c = card("c1", d="present", t_dec="2026-11-04T00:00:00+00:00")
    r = L.process([state("s1", T0, [(c, ex("c1"))])], empty(), T0, stub(0.7), KEY, "h")
    (f,) = r["forecasts"]
    assert f["target"] == "B" and f["p_ai"] == 0.7 and f["coherent_whole"] == "x"
    assert f["window_end_utc"].startswith("2027-01-03")
    assert f["prompt_sha256"] == P.prompt_sha256() and f["model_requested"] == L.MODEL
    assert f["forecast_id"] == P.forecast_id("c1", "B", KEY)
    assert P.run_digest(r["forecasts"])               # hashes verify
    assert "c1" not in json.dumps(f["payload"]) and "2026" not in json.dumps(f["payload"])


def test_training_rows_only_known_outcomes_before_forecast():
    snaps = [{"component": ["a"], "target": "D", "t": "2026-10-01T00:00:00+00:00",
              "hazard": "EQ", "stage": 1, "days": 1.0},
             {"component": ["b"], "target": "D", "t": "2026-10-01T00:00:00+00:00",
              "hazard": "EQ", "stage": 1, "days": 1.0},
             {"component": ["c"], "target": "D", "t": "2026-10-01T00:00:00+00:00",
              "hazard": "FL", "stage": 1, "days": 2.0}]
    cur = [(card("a", onset="2026-09-30T00:00:00+00:00", d="present",
                 t_dec="2026-10-05T00:00:00+00:00"), ex("a")),       # y = 1
           (card("b", onset="2026-08-01T00:00:00+00:00", d="absent"), ex("b")),  # y = 0
           (card("c", onset="2026-09-30T00:00:00+00:00"), ex("c"))]  # not yet: excluded
    rows = L.training_rows("D", T0, snaps, cur)
    assert sorted(r["y"] for r in rows) == [0, 1]
    assert L.training_rows("D", dt.datetime(2026, 10, 1, tzinfo=UTC), snaps, cur) == []


# --- files, index, end-to-end dry run with a stub model --------------------------------
def _site():
    spec = importlib.util.spec_from_file_location("sd", "scripts/selfmodel_daily.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _stream(tmp_path, rid, recs):
    store.write_run(tmp_path, {"run_id": rid, "ended": rid[:10] + "T07:00:00+00:00"},
                    {"gdacs": {"records": [r for r in recs if "properties" in r],
                               "error": None, "requests": []},
                     "usgs": {"records": [], "error": None, "requests": []},
                     "cems": {"records": [], "error": None, "requests": []},
                     "ifrc_go": {"records": [r for r in recs if "properties" not in r],
                                 "error": None, "requests": []}})


def test_dry_run_end_to_end_with_stub_model(tmp_path, monkeypatch):
    monkeypatch.setenv(store.KEY_ENV, KEY.decode())
    (tmp_path / "docs").mkdir()
    (tmp_path / L.PROTOCOL_FILE).write_text("synthetic protocol")
    sd = _site()
    f1 = "2026-11-02T04:17:00Z"
    _stream(tmp_path, "2026-11-02T041700Z",
            [gd(1, iso="PHL", frm="2026-11-01T03:00:00Z", fetched=f1),
             gd(2, typ="TC", iso="VNM", frm="2026-11-01T06:00:00Z", fetched=f1, lon=106,
                lat=16)])
    now = dt.datetime(2026, 11, 2, 9, 0, tzinfo=UTC)
    fn = stub(0.4)
    line = sd.run(tmp_path, now, fn)
    assert line["n_forecasts"] == 2 and line["status"] == "forecasts"
    assert sd.run(tmp_path, now + dt.timedelta(hours=2), fn) is None    # no new stream run
    # day 2: an appeal decides event 1 (D present) -> B becomes eligible for it only
    f2 = "2026-11-03T04:17:00Z"
    _stream(tmp_path, "2026-11-03T041700Z",
            [gd(1, iso="PHL", frm="2026-11-01T03:00:00Z", fetched=f2,
                glide="EQ-2026-000001-PHL"),
             gd(2, typ="TC", iso="VNM", frm="2026-11-01T06:00:00Z", fetched=f2, lon=106,
                lat=16),
             goev(5, iso="PHL", start="2026-11-01", glide="EQ-2026-000001-PHL",
                  created="2026-11-02T12:00:00Z", fetched=f2),
             goap(7, 5, atype=1, start="2026-11-02", created="2026-11-02T20:00:00Z",
                  fetched=f2)])
    line2 = sd.run(tmp_path, now + dt.timedelta(days=1), fn)
    assert line2["forecasts_total"] == 3 and line2["n_forecasts"] == 1  # B for event 1
    idx = L.read_index(tmp_path)
    assert len(idx) == 2 and L.verify_index(tmp_path) == []
    blob = (tmp_path / L.INDEX).read_text()
    for leak in ("PHL", "VNM", "gdacs", "0.4"):
        assert leak not in blob
    # encrypted file is not readable without the key
    raw = (tmp_path / L.LEDGER_DIR / f"{idx[0]['ledger_run_id']}.json.gz.enc").read_bytes()
    assert b"PHL" not in raw and raw.startswith(b"Salted__")
    lg = L.read_ledger(tmp_path / L.LEDGER_DIR / f"{idx[0]['ledger_run_id']}.json.gz.enc")
    assert all(f["p_ai"] == 0.4 for f in lg["forecasts"])


def test_no_key_dry_run_writes_ledger_without_forecast(tmp_path, monkeypatch):
    monkeypatch.setenv(store.KEY_ENV, KEY.decode())
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    (tmp_path / "docs").mkdir()
    (tmp_path / L.PROTOCOL_FILE).write_text("synthetic protocol")
    _stream(tmp_path, "2026-11-02T041700Z",
            [gd(1, frm="2026-11-01T03:00:00Z", fetched="2026-11-02T04:17:00Z")])
    line = _site().run(tmp_path, dt.datetime(2026, 11, 2, 9, tzinfo=UTC))
    assert line["status"] == "no key" and line["n_forecasts"] == 0 and line["n_missed"] == 1


# --- scorer ------------------------------------------------------------------------------
class Trap(dict):
    """A forecast row whose AI text must never be read by the scorer."""

    def __getitem__(self, k):
        assert k not in ("response_text", "coherent_whole"), "scorer read the AI's text"
        return super().__getitem__(k)


def _synthetic_ledger(n, seed=1, ai_skill=0.8):
    import numpy as np
    rng = np.random.default_rng(seed)
    fc, comps, cur = [], {}, []
    for i in range(n):
        y = int(rng.random() < 0.5)
        fid = f"f{i}"
        noise = rng.normal(0, 0.15)
        p_ai = float(np.clip(0.5 + (y - 0.5) * ai_skill + noise, 0.01, 0.99))
        fc.append(Trap(forecast_id=fid, target="D", forecast_utc="2026-11-05T08:00:00+00:00",
                       window_end_utc="2027-01-02T00:00:00+00:00", cluster=f"k{i % 25}",
                       model_returned=L.MODEL, model_requested=L.MODEL,
                       p_ai=p_ai if i % 10 else None, p_base=0.5, p_logit=0.5,
                       response_text="TRAP", coherent_whole="TRAP"))
        comps[fid] = [f"n{i}"]
        c = card(f"n{i}", d="present" if y else "absent",
                 t_dec="2026-11-20T00:00:00+00:00" if y else None)
        cur.append((c, ex(f"n{i}")))
    return {"forecasts": fc, "components": comps, "snapshots": [], "missed": [],
            "stream_runs": []}, cur


def test_scorer_refuses_before_may_score():
    lg, cur = _synthetic_ledger(40)
    with pytest.raises(S.ScoringRefused):
        S.score(lg, cur, dt.date(2027, 6, 1))      # windows closed, but < 120 and < Apr 2028


def test_scorer_end_to_end_on_synthetic_outcomes():
    lg, cur = _synthetic_ledger(60)
    res = S.score(lg, cur, dt.date(2028, 4, 1))
    p = res["pooled"]
    assert p["n"] == 60 and p["clusters"] == 25 and p["ai_unusable"] == 6
    assert p["verdict"] == "PASS" and p["brier_ai"] < p["brier_base"]
    lg2, cur2 = _synthetic_ledger(60, ai_skill=0.0)
    assert S.score(lg2, cur2, dt.date(2028, 4, 1))["pooled"]["verdict"] != "PASS"
    small, curs = _synthetic_ledger(20)
    assert S.score(small, curs, dt.date(2028, 4, 1))["pooled"]["verdict"] == \
        "not testable at this size"


def test_score_script_refuses_and_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setenv(store.KEY_ENV, KEY.decode())
    spec = importlib.util.spec_from_file_location("ss", "scripts/selfmodel_score.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert m.main(tmp_path, dt.datetime(2026, 12, 1, tzinfo=UTC)) == 2
    assert not (tmp_path / m.OUT).exists()


def test_mirror_page_shows_counts_only(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("build_site", "scripts/build_site.py")
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    monkeypatch.setattr(bs, "ROOT", tmp_path)
    assert "No ledger run yet" in bs.selfmodel_section()
    (tmp_path / "data/selfmodel").mkdir(parents=True)
    (tmp_path / L.INDEX).write_text(",".join(L.INDEX_FIELDS) + "\n" + ",".join(
        {"ledger_run_id": "r", "run_utc": "2026-11-02T09:00:00+00:00", "status": "forecasts",
         "forecasts_total": "7"}.get(k, "") for k in L.INDEX_FIELDS) + "\n")
    html = bs.selfmodel_section()
    assert "<b>7</b>" in html and "2026-11-02T09:00:00+00:00" in html


def test_call_model_classifies_account_errors_without_network(monkeypatch):
    import io
    import urllib.error

    def raise_(code, body):
        def f(req, timeout=0):
            raise urllib.error.HTTPError(L.API_URL, code, "x", {}, io.BytesIO(body))
        return f
    monkeypatch.setattr(L.time, "sleep", lambda s: None)
    low = json.dumps({"type": "error", "error": {"type": "invalid_request_error",
                      "message": "Your credit balance is too low"}}).encode()
    monkeypatch.setattr(L.urllib.request, "urlopen", raise_(400, low))
    assert L.call_model("s", "u", "k")["kind"] == "account"
    monkeypatch.setattr(L.urllib.request, "urlopen", raise_(401, b"{}"))
    assert L.call_model("s", "u", "k")["kind"] == "account"
    other = json.dumps({"error": {"type": "overloaded_error", "message": "busy"}}).encode()
    monkeypatch.setattr(L.urllib.request, "urlopen", raise_(529, other))
    assert L.call_model("s", "u", "k")["kind"] == "failed"
