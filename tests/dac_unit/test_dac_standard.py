"""Tests for the DAC event-file standard (emo/dac_standard.py, docs/DAC_STANDARD.md).

All data here are synthetic; no real case is opened.
"""

from __future__ import annotations

import copy
import json
from numbers import Number
from pathlib import Path

import pytest

from emo import dac_standard as ds

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "docs" / "dac_event_file_example.json"
SCHEMA = ROOT / "docs" / "dac_event_file.schema.json"


@pytest.fixture()
def valid() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def _errors(data) -> list[str]:
    with pytest.raises(ds.DACStandardError) as exc:
        ds.validate_event_file(data)
    return exc.value.errors


def test_example_file_is_valid():
    ds.load_event_file(EXAMPLE)


def test_malformed_file_is_rejected(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"standard_version": "1.0", "case": {', encoding="utf-8")
    with pytest.raises(ds.DACStandardError):
        ds.load_event_file(bad)
    with pytest.raises(ds.DACStandardError):
        ds.compute_profile({"events": []})


@pytest.mark.parametrize(
    "mutate, expected",
    [
        (lambda d: d["events"][1].pop("source"), "'source' required"),
        (lambda d: d["events"][1].update(sublayer="vibes"), "sublayer 'vibes'"),
        (lambda d: d["events"][1].update(date_earliest="2020-02-30"), "not a valid"),
        (lambda d: d["events"][1].update(date_latest="2020-02-11"), "exact date needs"),
        (lambda d: d["events"][2].pop("source_wording"), "needs 'source_wording'"),
        (lambda d: d["events"][2].update(date_latest="2020-02-20"), "window needs"),
        (lambda d: d["events"][1].update(source_type="blog"), "source_type"),
        (lambda d: d["events"][1].update(extra=1), "unknown field 'extra'"),
        (lambda d: d["events"][5].pop("end_point"), "delivery needs 'end_point'"),
        (lambda d: d["events"][5].update(pairs_with="act"), "is not a firm_order"),
        (lambda d: d["events"][1].update(pairs_with="order2"), "only allowed on delivery"),
        (lambda d: d["events"][4].update(reading="A"), "distinct readings"),
        (lambda d: d["events"][3].update(sublayer="firm_order"), "share one sublayer"),
        (lambda d: d["case"].update(t0_event_id="nope"), "not found"),
        (lambda d: d["case"].update(t0_event_id="order1"), "t0 event must be"),
        (lambda d: d["case"]["inclusion_rules"].pop("binding_act"), "no rule for sublayer 'binding_act'"),
        (lambda d: d["case"]["coding"].update(coders=0), "'coders'"),
        (lambda d: d["case"].pop("start_rule"), "missing 'start_rule'"),
        (lambda d: d["events"][1].update(date_earliest="2020-07-02", date_latest="2020-07-02"),
         "outside the observation window"),
        (lambda d: d["events"].append(dict(d["events"][7], event_id="f2")), "coded missing/censored twice"),
        (lambda d: d["events"].append(dict(d["events"][1], event_id="f3", sublayer="dedicated_funding")),
         "both dated and missing"),
        (lambda d: d["events"][5].update(date_earliest="2020-02-01", date_latest="2020-02-01"),
         "ends before its order"),
        (lambda d: d["events"][7].update(reading="A"), "cannot carry a reading"),
        (lambda d: d.update(score=1.0), "unknown top-level field"),
    ],
)
def test_each_rule_rejects(valid, mutate, expected):
    data = copy.deepcopy(valid)
    mutate(data)
    errors = _errors(data)
    assert any(expected in e for e in errors), errors


def test_all_errors_are_collected(valid):
    data = copy.deepcopy(valid)
    data["events"][1].pop("source")
    data["events"][2].pop("source_wording")
    assert len(_errors(data)) >= 2


def test_profile_values_match_hand_computation(valid):
    prof = ds.compute_profile(valid)
    assert prof["missing"] == ["dedicated_funding"]
    assert prof["censored"] == ["counter_measure"]
    assert prof["contested_events"] == {"act": ["A", "B"]}
    by_reading = {p["reading"]["act"]: p for p in prof["profiles"]}
    assert set(by_reading) == {"A", "B"}
    for reading, act_lag in (("A", 45), ("B", 50)):
        p = by_reading[reading]
        s = p["sublayers"]
        assert s["firm_order"]["lag_from_t0"] == {"min_days": 11, "max_days": 11}
        assert s["firm_order"]["first_event_ids"] == ["order1"]
        assert s["binding_act"]["lag_from_t0"] == {"min_days": act_lag, "max_days": act_lag}
        assert s["delivery"]["lag_from_t0"] == {"min_days": 57, "max_days": 57}
        assert s["delivery"]["n_events"] == 1  # secondary end point excluded
        assert "dedicated_funding" not in s and "counter_measure" not in s
        assert p["paired_order_to_delivery"] == [{
            "order_id": "order1", "delivery_id": "del1",
            "end_point": "national distribution level",
            "interval": {"min_days": 46, "max_days": 46},
        }]
        assert p["unpaired_first_order_to_first_delivery"] == {"min_days": 46, "max_days": 46}
        assert p["secondary_end_points"] == {"provider level": {"min_days": 61, "max_days": None}}


def test_window_dates_give_ranges(valid):
    data = copy.deepcopy(valid)
    data["events"][1].update(date_status="window", date_earliest="2020-02-05",
                             date_latest="2020-02-12", source_wording="early February")
    data["events"][0].update(date_status="window", date_earliest="2020-01-28",
                             date_latest="2020-01-30", source_wording="end of January")
    p = ds.compute_profile(data)["profiles"][0]
    # order window 5-12 Feb, t0 window 28-30 Jan: 6 to 15 days
    assert p["sublayers"]["firm_order"]["lag_from_t0"] == {"min_days": 6, "max_days": 15}
    # paired: order 5-12 Feb to delivery 27 Mar: 44 to 51 days
    assert p["paired_order_to_delivery"][0]["interval"] == {"min_days": 44, "max_days": 51}


def _numbers(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _numbers(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _numbers(v, f"{path}[{i}]")
    elif isinstance(obj, Number) and not isinstance(obj, bool):
        yield path


def test_profile_is_never_a_scalar(valid):
    prof = ds.compute_profile(valid)
    assert isinstance(prof, dict)
    banned = ("score", "index", "total", "composite", "weight", "dac_value")
    for path in _numbers(prof):
        assert any(k in path for k in ("min_days", "max_days", "n_events")), path
        assert not any(b in path for b in banned), path


def test_schema_matches_validator_constants():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    ev = schema["properties"]["events"]["items"]
    assert ev["properties"]["sublayer"]["enum"] == list(ds.SUBLAYERS)
    assert ev["properties"]["date_status"]["enum"] == list(ds.DATE_STATUSES)
    assert ev["properties"]["source_type"]["enum"] == list(ds.SOURCE_TYPES)
    assert ev["required"] == list(ds.EVENT_REQUIRED)
    assert set(ev["properties"]) == set(ds.EVENT_REQUIRED) | set(ds.EVENT_OPTIONAL)
    assert schema["properties"]["case"]["required"] == list(ds.CASE_REQUIRED)
    assert schema["properties"]["standard_version"]["const"] == ds.STANDARD_VERSION


@pytest.mark.parametrize("name, exact", [("ozone", 4828), ("climate", 6712)])
def test_converted_case_files_reproduce_comparison_lag(name, exact):
    """docs/DAC_STANDARD.md §5: converted files validate and contain the script's lag."""
    prof = ds.compute_profile(ds.load_event_file(ROOT / "data" / f"dac_{name}_events.json"))
    lag = prof["profiles"][0]["sublayers"]["binding_act"]["lag_from_t0"]
    assert lag["min_days"] <= exact <= lag["max_days"]
