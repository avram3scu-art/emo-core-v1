"""Session 10b: the early-warning t0 rows rest on ECDC's own records, the committed event files keep
the PHEIC t0, and the alternative-t0 profiles are current (docs/DAC_T0_EARLY_WARNING.md)."""

import json
import re
import sys
from pathlib import Path

import pytest

from emo.dac_standard import compute_profile, load_event_file

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from dac_t0_alternative import FILES, swap_t0  # noqa: E402


def _text(name: str) -> str:
    return re.sub(r"\s+", " ", (ROOT / "data/sources/dac_t0" / f"{name}.txt").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name,phrase", [
    ("ecdc_2020-01-09_tab_ncov", "THREAT ASSESSMENT BRIEF Pneumonia cases possibly associated with a novel coronavirus in Wuhan, China 9 January 2020"),
    ("ecdc_2022-05-23_rra_mpox", "RAPID RISK ASSESSMENT Monkeypox multi-country outbreak 23 May 2022"),
])
def test_phrase_in_source(name, phrase):
    assert phrase in _text(name)


@pytest.mark.parametrize("path", FILES, ids=[p.parent.name for p in FILES])
def test_committed_file_keeps_pheic_t0(path):
    case = load_event_file(path)["case"]
    assert case["t0_event_id"] == "who_pheic" and "ecdc_first_ra" in case["alternative_t0"]


@pytest.mark.parametrize("path", FILES, ids=[p.parent.name for p in FILES])
def test_alternative_profile_current(path):
    prof = compute_profile(swap_t0(load_event_file(path)))
    committed = json.loads(path.with_name("EU_profile_t0_early.json").read_text(encoding="utf-8"))
    assert prof == committed, "rerun scripts/dac_t0_alternative.py"


def test_alternative_lags():
    lags = {p.parent.name: {k: v["lag_from_t0"]["min_days"] for k, v in
                            json.loads(p.with_name("EU_profile_t0_early.json").read_text())["profiles"][0]["sublayers"].items()}
            for p in FILES}
    assert lags["dac_mpox"] == {"firm_order": 22, "binding_act": 60, "delivery": 36}
    assert lags["dac_ppe"] == {"binding_act": 65, "delivery": 107, "counter_measure": 55}
