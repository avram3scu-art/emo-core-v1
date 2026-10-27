"""Audit 2026-10-27: probes of emo/dac_standard.py edge cases (no pytest needed).

Each probe mutates the committed synthetic example and prints whether the
validator accepts it and what the profile does. Expected behaviour is stated
per probe; "GAP" marks a result that departs from docs/DAC_STANDARD.md intent.
Run from the repository root: PYTHONPATH=. python analysis/audit_2026-10-27/probe_dac_standard.py
"""

import copy
import json

from emo.dac_standard import DACStandardError, compute_profile, validate_event_file

BASE = json.load(open("docs/dac_event_file_example.json"))


def check(name: str, data: dict, expect_valid: bool) -> dict | None:
    try:
        validate_event_file(data)
        ok = True
        err = ""
    except DACStandardError as exc:
        ok = False
        err = str(exc)[:160]
    flag = "ok " if ok == expect_valid else "GAP"
    print(f"[{flag}] {name}: valid={ok} (expected {expect_valid}) {err}")
    return compute_profile(data) if ok else None


# P1: standard_version explicitly null should be rejected.
d = copy.deepcopy(BASE)
d["standard_version"] = None
check("P1 standard_version null", d, expect_valid=False)

# P2: unknown key inside 'case' should be rejected (top-level and event keys are).
d = copy.deepcopy(BASE)
d["case"]["typo_feild"] = "x"
check("P2 unknown case key", d, expect_valid=False)

# P3: delivery dated at a secondary end point while delivery at the primary end
# point is missing. Multi-level cases (EU level vs national) need this.
d = copy.deepcopy(BASE)
d["events"] = [e for e in d["events"] if e["event_id"] != "del1"]
d["events"].append({"event_id": "del_nat", "sublayer": "delivery", "date_status": "missing",
                    "description": "No dated national delivery", "source": "s", "source_type": "primary"})
check("P3 primary-end-point delivery missing, secondary dated", d, expect_valid=True)

# P4: a delivery paired with an order whose date is missing: the pair should
# appear in the profile as undatable, not vanish.
d = copy.deepcopy(BASE)
d["events"] = [e for e in d["events"] if e["event_id"] not in ("order1", "order2")]
d["events"].append({"event_id": "order1", "sublayer": "firm_order", "date_status": "missing",
                    "description": "Order known, date not found", "source": "s", "source_type": "primary"})
d["case"]["inclusion_rules"]["firm_order"] = "First signed contract"
p = check("P4 paired order missing", d, expect_valid=True)
if p:
    pairs = p["profiles"][0]["paired_order_to_delivery"]
    print(f"      paired list = {pairs}  -> {'GAP: pair silently dropped' if not pairs else 'kept'}")

# P5: contested t0 whose second reading is a lower bound (validation checks only the first row).
d = copy.deepcopy(BASE)
w = d["events"][0]
w["reading"] = "A"
d["events"].append({"event_id": "warning", "sublayer": "validation", "date_status": "lower_bound",
                    "date_earliest": "2020-01-25", "source_wording": "after 25 Jan", "reading": "B",
                    "description": "alt", "source": "s", "source_type": "primary"})
p = check("P5 contested t0 with a lower-bound reading", d, expect_valid=False)
if p:
    print(f"      profile B binding_act lag = {p['profiles'][-1]['sublayers']['binding_act']['lag_from_t0']}")
