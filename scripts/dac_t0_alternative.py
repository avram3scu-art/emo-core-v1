"""Profiles of the EU files under the early-warning t0 (docs/DAC_T0_EARLY_WARNING.md §4).

In memory only: t0_event_id -> "ecdc_first_ra", that row's sublayer -> validation, the PHEIC row
-> context, and the two swapped in alternative_t0. The committed event files keep the PHEIC t0.
Writes data/<dir>/EU_profile_t0_early.json. Run from the repository root.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from emo.dac_standard import compute_profile, load_event_file

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "data/dac_mpox/EU.json", ROOT / "data/dac_ppe/EU.json"]
NEW_T0 = "ecdc_first_ra"


def swap_t0(data: dict[str, Any], new_t0: str = NEW_T0) -> dict[str, Any]:
    d = copy.deepcopy(data)
    case = d["case"]
    old = case["t0_event_id"]
    for e in d["events"]:
        if e["event_id"] == new_t0:
            e["sublayer"] = "validation"
        elif e["event_id"] == old:
            e["sublayer"] = "context"
    case["t0_event_id"] = new_t0
    case["alternative_t0"] = [old if x == new_t0 else x for x in case["alternative_t0"]]
    case["t0_rule"] = "ECDC's first risk assessment for the hazard (docs/DAC_T0_EARLY_WARNING.md §1); alternative-t0 run"
    return d


def main() -> None:
    for f in FILES:
        prof = compute_profile(swap_t0(load_event_file(f)))
        out = f.with_name("EU_profile_t0_early.json")
        out.write_text(json.dumps(prof, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        s = prof["profiles"][0]["sublayers"]
        print(f.parent.name, {k: v["lag_from_t0"] for k, v in s.items()}, "missing:", prof["missing"])


if __name__ == "__main__":
    main()
