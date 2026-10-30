"""H8 self-model protocol code (docs/SELF_MODEL_PROTOCOL.md). Synthetic cards only."""
import datetime as dt

import numpy as np
import pytest

import emo.selfmodel.protocol as P

UTC = dt.UTC
NOW = dt.datetime(2026, 11, 10, 12, tzinfo=UTC)


def card(**kw):
    c = {"eu27": False, "closed": False, "anchored": True, "hazard": "EQ", "iso3": ["NPL"],
         "onset": "2026-11-08T00:00:00+00:00", "t_decision": None, "t_money": None,
         "stage_label": "warning not recognised", "decision_systems": [],
         "card_id": "gdacs|EQ|123",
         "rungs": {"W": "present", "R": "not yet", "D": "not yet", "B": "not yet"}}
    c.update(kw)
    return c


def test_eligibility_rules():
    seen = dt.datetime(2026, 11, 8, 6, tzinfo=UTC)
    assert P.eligible_targets(card(), NOW, seen) == ["D"]
    assert P.eligible_targets(card(eu27=True), NOW, seen) == []
    assert P.eligible_targets(card(onset="2026-10-29T00:00:00+00:00"), NOW, seen) == []
    early = dt.datetime(2026, 10, 30, tzinfo=UTC)
    assert P.eligible_targets(card(), NOW, early) == []          # seen before the cutoff
    assert P.eligible_targets(card(anchored=False), NOW, seen) == []
    assert P.eligible_targets(card(), NOW, seen, n_so_far=P.N_TARGET) == []
    b = card(t_decision="2026-11-09T00:00:00+00:00",
             rungs={"W": "present", "R": "present", "D": "present", "B": "not yet"})
    assert P.eligible_targets(b, NOW, seen) == ["B"]
    late = NOW + dt.timedelta(days=70)                           # D window closed
    assert P.eligible_targets(card(), late, seen) == []


def test_payload_has_no_identifier_title_or_date():
    c = card(attention_title="2026 Nepal earthquake", t_warning="2026-11-08T01:00:00+00:00")
    p = P.payload(c, "D", NOW)
    text = P.canonical(p)
    assert "2026" not in text and "gdacs" not in text and "Nepal" not in text
    assert set(p) == {"hazard", "countries_iso3", "stage_so_far", "rungs", "decision_systems",
                      "days_since_reference", "reference", "days_left"}
    assert p["days_left"] == pytest.approx(60 - 2.5, abs=0.1)
    s, u = P.prompt(c, "D", NOW)
    assert "within 57 days" in u and "recommend" in s


def test_parse_probability():
    assert P.parse_probability('{"p": 0.3, "coherent_whole": "x"}') == 0.3
    assert P.parse_probability('```json\n{"p": 1}\n```') == 1.0
    assert P.parse_probability('Sure. "p": 0.42 is my answer') == 0.42
    for bad in (None, "", '{"p": 1.2}', '{"p": "high"}', '"p": 0.1 or "p": 0.2', '{"p": true}'):
        assert P.parse_probability(bad) is None


def _row(**over):
    kw = {k: None for k in P.LEDGER_FIELDS}
    kw.update(forecast_id="a", target="D", p_ai=0.2, p_base=0.4, p_logit=0.3)
    kw.update(over)
    return P.ledger_row(**kw)


def test_ledger_hash_and_digest():
    r1, r2 = _row(), _row(forecast_id="b")
    assert P.run_digest([r1, r2]) == P.run_digest([r2, r1])
    r1["p_ai"] = 0.9                                             # tampering is detected
    with pytest.raises(ValueError):
        P.run_digest([r1, r2])
    with pytest.raises(ValueError):
        P.ledger_row(forecast_id="x")
    k = b"k" * 32
    assert P.forecast_id("c", "D", k) != P.forecast_id("c", "B", k)
    assert P.forecast_id("c", "D", k) != P.forecast_id("c", "D", b"j" * 32)
    assert len(P.prompt_sha256()) == 64


def test_outcome_from_records_only():
    f = NOW
    d = card(t_decision="2026-11-20T00:00:00+00:00",
             rungs={"D": "present", "B": "not yet"})
    assert P.outcome(d, "D", f) == 1
    assert P.outcome(card(t_decision="2026-11-09T00:00:00+00:00",
                          rungs={"D": "present"}), "D", f) is None   # before the forecast
    assert P.outcome(card(rungs={"D": "absent"}), "D", f) == 0
    for st in ("not yet", "missing", "withheld", "no source"):
        assert P.outcome(card(rungs={"D": st}), "D", f) is None
    assert P.outcome(card(eu27=True, rungs={"D": "absent"}), "D", f) is None
    m = card(t_decision="2026-11-12T00:00:00+00:00", t_money="2027-01-20T00:00:00+00:00",
             rungs={"D": "present", "B": "present"})
    assert P.outcome(m, "B", f) == 0                             # money after its window


def test_baselines():
    assert P.base_rate([]) == 0.5
    small = P.fit_logistic([{"hazard": "EQ", "stage": 1, "days": 1, "y": 1}] * 5)
    assert small["kind"] == "base"
    rng = np.random.default_rng(0)
    train = []
    for _ in range(400):
        h = rng.choice(["EQ", "FL", "VO"])
        p = {"EQ": .7, "FL": .4, "VO": .1}[h]
        train.append({"hazard": h, "stage": 1, "days": 1.0, "y": int(rng.random() < p)})
    m = P.fit_logistic(train)
    assert m["kind"] == "logit"
    pe = P.predict(m, {"hazard": "EQ", "stage": 1, "days": 1.0})
    pv = P.predict(m, {"hazard": "VO", "stage": 1, "days": 1.0})
    assert 0.6 < pe < 0.8 and 0.03 < pv < 0.2


def _scored(n, gain, rng, clusters=None):
    rows = []
    for i in range(n):
        y = int(rng.random() < .4)
        rows.append({"y": y, "p_base": .4, "p_logit": .4,
                     "p_ai": float(np.clip(.4 + (gain if y else -gain), 0, 1)),
                     "cluster": i if clusters is None else i % clusters})
    return rows


def test_h8_score_decisions():
    rng = np.random.default_rng(1)
    assert P.h8_score(_scored(20, .3, rng))["verdict"] == "not testable at this size"
    assert P.h8_score(_scored(60, .3, rng, clusters=10))["verdict"] == \
        "not testable at this size"
    assert P.h8_score(_scored(80, .3, rng))["verdict"] == "PASS"
    worse = P.h8_score(_scored(200, -.2, rng))
    assert worse["verdict"] == "FAIL" and worse["gain_logit"] < 0
    rows = _scored(80, .3, rng)
    for r in rows:
        r["p_ai"] = None                                         # unusable → 0.5, no drop
    s = P.h8_score(rows)
    assert s["ai_unusable"] == 80 and s["n"] == 80 and s["verdict"] != "PASS"


def test_may_score():
    ends = [dt.datetime(2027, 3, 1, tzinfo=UTC)]
    assert not P.may_score(dt.date(2027, 3, 5), ends, P.N_TARGET)
    assert P.may_score(dt.date(2027, 3, 8), ends, P.N_TARGET)
    assert not P.may_score(dt.date(2027, 3, 8), ends, 50)
    assert P.may_score(P.SCORE_LATEST, ends, 50)
    assert not P.may_score(P.SCORE_LATEST, [], 0)
