"""The mpox event file (data/dac_mpox/EU.json) validates, its profile is current, and every coded
date rests on a phrase that is in the committed source text (docs/DAC_MPOX_CODING.md)."""

import json
import re
from pathlib import Path

import pytest

from emo.dac_standard import compute_profile, load_event_file

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data/dac_mpox"
S = ROOT / "data/sources/dac_mpox"


def _text(name: str) -> str:
    return re.sub(r"\s+", " ", (S / f"{name}.txt").read_text(encoding="utf-8"))


def test_file_valid_and_profile_current():
    prof = compute_profile(load_event_file(D / "EU.json"))
    committed = json.loads((D / "EU_profile.json").read_text(encoding="utf-8"))
    assert prof == committed, "recompute data/dac_mpox/EU_profile.json"


PHRASES = [
    ("who_2022-07-23_pheic", "23 July 2022 Statement"),
    ("who_2022-07-23_pheic", "the Director-General has determined that the multi-country outbreak of monkeypox constitutes a Public Health Emergency of International Concern"),
    ("who_2022-07-23_pheic", "the first meeting of the Committee on 23 June 2022"),
    ("who_2023-05-11_end", "11 May 2023 Statement"),
    ("who_2023-05-11_end", "the event no longer constitutes a PHEIC"),
    ("ec_2022-06-14_contract", "Today, HERA, the European Commission's Health Preparedness and Response Authority, concluded a contract with the company Bavarian Nordic to purchase 109 090 doses"),
    ("ec_2022-06-14_contract", "Press release 14 June 2022"),
    ("ec_2022-06-28_delivery", "with an initial 5,300 doses arriving in Spain, out of the total 109,090 doses procured"),
    ("ec_2022-06-28_delivery", "Press release 28 June 2022"),
    ("ec_2022-06-28_delivery", "HERA was established in October 2021"),
    ("ec_2022-07-18_additional", "News announcement 18 July 2022"),
    ("ec_2022-07-18_additional", "has purchased the third-generation vaccine"),
    ("ec_2022-07-18_additional", "already delivered around 25 000 doses to 6 Member States"),
    ("ec_2022-09-07_additional_de", "Pressemitteilung 7. September 2022"),
    ("ec_2022-09-07_additional_de", "über 170.000 weitere Dosen"),
    ("ec_2022-11-17_framework_de", "17. November 2022"),
    ("ec_2022-11-17_framework_de", "Rahmenvertrag über die gemeinsame Beschaffung von bis zu 2 Millionen Dosen"),
    ("ec_C2022_5446_dec", "Done at Brussels, 22.7.2022"),
    ("ec_C2022_5446_dec", "formulated on 21 July 2022"),
    ("ec_C2022_5446_anx", "Active immunisation against smallpox, monkeypox and disease caused by vaccinia virus in adults"),
]


@pytest.mark.parametrize("name,phrase", PHRASES)
def test_phrase_in_source(name, phrase):
    assert phrase in _text(name)


def test_pre_t0_responses_kept_with_negative_lags():
    p = json.loads((D / "EU_profile.json").read_text(encoding="utf-8"))["profiles"][0]["sublayers"]
    assert p["firm_order"]["lag_from_t0"] == {"min_days": -39, "max_days": -39}
    assert p["delivery"]["lag_from_t0"] == {"min_days": -25, "max_days": -25}
    assert p["binding_act"]["lag_from_t0"] == {"min_days": -1, "max_days": -1}
