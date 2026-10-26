"""DAC event-file standard: validator and profile.

Implements `docs/DAC_STANDARD.md` (schema: `docs/dac_event_file.schema.json`).
`validate_event_file` rejects a malformed file with every error found;
`compute_profile` returns the DAC profile of a valid file: per-sublayer lag
ranges from t0, paired and unpaired order-to-delivery intervals, and missing and
censored sublayers listed separately. One profile is computed for each
combination of readings of contested dates. No weighted or composite scalar is
computed anywhere in this module.
"""

from __future__ import annotations

import itertools
import json
from datetime import date
from pathlib import Path
from typing import Any

STANDARD_VERSION = "1.0"

SUBLAYERS = (
    "validation",
    "firm_order",
    "binding_act",
    "dedicated_funding",
    "delivery",
    "counter_measure",
    "reversal",
    "institutionalisation",
    "persistence",
    "context",
)
# Sublayers that enter the profile (validation is t0; context is recorded only).
PROFILE_SUBLAYERS = SUBLAYERS[1:-1]

DATE_STATUSES = ("exact", "window", "lower_bound", "upper_bound", "missing", "censored")
SOURCE_TYPES = ("primary", "secondary")

CASE_REQUIRED = {
    "case_id": str,
    "t0_event_id": str,
    "t0_institution": str,
    "t0_rule": str,
    "alternative_t0": list,
    "response_scale": str,
    "start_rule": str,
    "end_point": str,
    "inclusion_rules": dict,
    "observation_window": dict,
    "source_pool": dict,
    "coding": dict,
    "computation": dict,
}
EVENT_REQUIRED = ("event_id", "sublayer", "date_status", "description", "source", "source_type")
EVENT_OPTIONAL = (
    "date_earliest",
    "date_latest",
    "source_wording",
    "reading",
    "pairs_with",
    "end_point",
)
TOP_KEYS = ("standard_version", "case", "events")


class DACStandardError(ValueError):
    """Raised when an event file does not meet the standard. `errors` lists every problem."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"{len(errors)} error(s): " + "; ".join(errors))


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def load_event_file(path: str | Path) -> dict[str, Any]:
    """Read and validate a JSON event file; raise DACStandardError if malformed."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DACStandardError([f"not valid JSON: {exc}"]) from exc
    validate_event_file(data)
    return data


def _check_case(case: dict[str, Any], errors: list[str]) -> tuple[date | None, date | None]:
    for key, typ in CASE_REQUIRED.items():
        if key not in case:
            errors.append(f"case: missing '{key}'")
        elif not isinstance(case[key], typ) or (typ is str and not _is_text(case[key])):
            errors.append(f"case: '{key}' must be a non-empty {typ.__name__}")
    win = case.get("observation_window", {})
    start = end = None
    if isinstance(win, dict):
        start, end = _parse_date(win.get("start")), _parse_date(win.get("end"))
        if start is None or end is None:
            errors.append("case.observation_window: 'start' and 'end' must be YYYY-MM-DD")
        elif start > end:
            errors.append("case.observation_window: start after end")
        if not _is_text(win.get("reason")):
            errors.append("case.observation_window: 'reason' required")
    pool = case.get("source_pool", {})
    if isinstance(pool, dict):
        for key in ("searched", "not_accessed"):
            if not isinstance(pool.get(key), list):
                errors.append(f"case.source_pool: '{key}' must be a list")
        if _parse_date(pool.get("search_date")) is None:
            errors.append("case.source_pool: 'search_date' must be YYYY-MM-DD")
        if not _is_text(pool.get("case_selection_reason")):
            errors.append("case.source_pool: 'case_selection_reason' required")
    coding = case.get("coding", {})
    if isinstance(coding, dict):
        coders = coding.get("coders")
        if not isinstance(coders, int) or isinstance(coders, bool) or coders < 1:
            errors.append("case.coding: 'coders' must be an integer >= 1")
        if not isinstance(coding.get("rules_fixed_before_coding"), bool):
            errors.append("case.coding: 'rules_fixed_before_coding' must be true or false")
        if "agreement" not in coding:
            errors.append("case.coding: 'agreement' required (null if one coder)")
    comp = case.get("computation", {})
    if isinstance(comp, dict) and not _is_text(comp.get("code")):
        errors.append("case.computation: 'code' required (repository or archive identifier)")
    return start, end


def _check_event(i: int, ev: Any, errors: list[str], win: tuple[date | None, date | None]) -> None:
    where = f"events[{i}]"
    if not isinstance(ev, dict):
        errors.append(f"{where}: must be an object")
        return
    for key in EVENT_REQUIRED:
        if not _is_text(ev.get(key)):
            errors.append(f"{where}: '{key}' required")
    for key in ev:
        if key not in EVENT_REQUIRED and key not in EVENT_OPTIONAL:
            errors.append(f"{where}: unknown field '{key}'")
    sub, status = ev.get("sublayer"), ev.get("date_status")
    if sub is not None and sub not in SUBLAYERS:
        errors.append(f"{where}: sublayer '{sub}' not in {SUBLAYERS}")
    if ev.get("source_type") is not None and ev.get("source_type") not in SOURCE_TYPES:
        errors.append(f"{where}: source_type must be one of {SOURCE_TYPES}")
    if status is not None and status not in DATE_STATUSES:
        errors.append(f"{where}: date_status '{status}' not in {DATE_STATUSES}")
        return
    raw_e, raw_l = ev.get("date_earliest"), ev.get("date_latest")
    e, l_ = _parse_date(raw_e), _parse_date(raw_l)
    if raw_e is not None and e is None:
        errors.append(f"{where}: date_earliest '{raw_e}' is not a valid YYYY-MM-DD date")
    if raw_l is not None and l_ is None:
        errors.append(f"{where}: date_latest '{raw_l}' is not a valid YYYY-MM-DD date")
    need = {
        "exact": (True, True),
        "window": (True, True),
        "lower_bound": (True, False),
        "upper_bound": (False, True),
        "missing": (False, False),
        "censored": (False, False),
    }.get(status)
    if need is not None:
        if need[0] != (raw_e is not None) or need[1] != (raw_l is not None):
            errors.append(
                f"{where}: date_status '{status}' requires date_earliest "
                f"{'present' if need[0] else 'absent'} and date_latest "
                f"{'present' if need[1] else 'absent'}"
            )
    if status == "exact" and e and l_ and e != l_:
        errors.append(f"{where}: exact date needs date_earliest == date_latest")
    if status == "window" and e and l_ and e >= l_:
        errors.append(f"{where}: window needs date_earliest < date_latest")
    if status in ("window", "lower_bound", "upper_bound") and not _is_text(ev.get("source_wording")):
        errors.append(f"{where}: imprecise date needs 'source_wording'")
    if status in ("missing", "censored"):
        if sub in ("validation", "context"):
            errors.append(f"{where}: sublayer '{sub}' cannot be {status}")
        if ev.get("reading") is not None:
            errors.append(f"{where}: {status} rows cannot carry a reading")
    start, end = win
    if start and end:
        if (e and e > end) or (l_ and l_ < start):
            errors.append(f"{where}: date outside the observation window (code as censored instead)")
    if sub == "delivery" and status not in ("missing", "censored") and not _is_text(ev.get("end_point")):
        errors.append(f"{where}: delivery needs 'end_point'")
    if ev.get("pairs_with") is not None and sub != "delivery":
        errors.append(f"{where}: 'pairs_with' only allowed on delivery")


def _bounds(ev: dict[str, Any], win_start: date) -> tuple[date, date | None]:
    """Earliest and latest consistent date; an upper bound is floored at the window start,
    a lower bound has an open latest end (None)."""
    e = _parse_date(ev.get("date_earliest")) or win_start
    return e, _parse_date(ev.get("date_latest"))


def validate_event_file(data: Any) -> None:
    """Raise DACStandardError listing every violation of the standard; return None if valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        raise DACStandardError(["file must be a JSON object"])
    for key in TOP_KEYS:
        if key not in data:
            errors.append(f"missing top-level '{key}'")
    for key in data:
        if key not in TOP_KEYS:
            errors.append(f"unknown top-level field '{key}'")
    if data.get("standard_version") not in (None, STANDARD_VERSION):
        errors.append(f"standard_version must be '{STANDARD_VERSION}'")
    case, events = data.get("case"), data.get("events")
    if not isinstance(case, dict) or not isinstance(events, list) or not events:
        errors.append("'case' must be an object and 'events' a non-empty list")
        raise DACStandardError(errors)
    win = _check_case(case, errors)
    for i, ev in enumerate(events):
        _check_event(i, ev, errors, win)
    if errors:
        raise DACStandardError(errors)

    # Cross-event rules (all rows are well formed from here on).
    by_id: dict[str, list[dict[str, Any]]] = {}
    for ev in events:
        by_id.setdefault(ev["event_id"], []).append(ev)
    for eid, rows in by_id.items():
        readings = [r.get("reading") for r in rows]
        if len(rows) == 1:
            if readings[0] is not None:
                errors.append(f"event '{eid}': a reading needs at least two alternative rows")
            continue
        if any(not _is_text(r) for r in readings) or len(set(readings)) != len(readings):
            errors.append(f"event '{eid}': repeated id; contested rows need distinct readings")
        if len({r["sublayer"] for r in rows}) != 1:
            errors.append(f"event '{eid}': readings must share one sublayer")
    t0_rows = by_id.get(case["t0_event_id"])
    if not t0_rows:
        errors.append(f"t0_event_id '{case['t0_event_id']}' not found in events")
    elif t0_rows[0]["sublayer"] != "validation" or t0_rows[0]["date_status"] not in ("exact", "window"):
        errors.append("t0 event must be sublayer 'validation' with an exact or window date")
    dated: set[str] = set()
    undated: dict[str, str] = {}
    for ev in events:
        if ev["date_status"] in ("missing", "censored"):
            if ev["sublayer"] in undated:
                errors.append(f"sublayer '{ev['sublayer']}' coded missing/censored twice")
            undated[ev["sublayer"]] = ev["date_status"]
        else:
            dated.add(ev["sublayer"])
    for sub in dated & set(undated):
        errors.append(f"sublayer '{sub}' is both dated and {undated[sub]}")
    rules = case["inclusion_rules"]
    for sub in (dated | set(undated)) & set(PROFILE_SUBLAYERS):
        if not _is_text(rules.get(sub)):
            errors.append(f"case.inclusion_rules: no rule for sublayer '{sub}'")
    win_start = win[0] or date.min
    for ev in events:
        target = ev.get("pairs_with")
        if target is None:
            continue
        orders = by_id.get(target)
        if not orders or orders[0]["sublayer"] != "firm_order":
            errors.append(f"delivery '{ev['event_id']}': pairs_with '{target}' is not a firm_order")
            continue
        _, d_latest = _bounds(ev, win_start)
        o_earliest = min(_bounds(o, win_start)[0] for o in orders if o["date_status"] not in ("missing", "censored")) \
            if any(o["date_status"] not in ("missing", "censored") for o in orders) else None
        if d_latest is not None and o_earliest is not None and d_latest < o_earliest:
            errors.append(f"delivery '{ev['event_id']}' ends before its order '{target}' can start")
    if errors:
        raise DACStandardError(errors)


def _lag_range(
    a: tuple[date, date | None], b: tuple[date, date | None]
) -> dict[str, int | None]:
    """Days from interval a to interval b over all consistent dates; None = open end."""
    lo = (b[0] - a[1]).days if a[1] is not None else None
    hi = (b[1] - a[0]).days if b[1] is not None else None
    return {"min_days": lo, "max_days": hi}


def _first(rows: list[dict[str, Any]], win_start: date) -> tuple[date, date | None]:
    """Range of the date of the first event among rows."""
    bounds = [_bounds(r, win_start) for r in rows]
    earliest = min(b[0] for b in bounds)
    latests = [b[1] for b in bounds if b[1] is not None]
    return earliest, (min(latests) if latests else None)


def compute_profile(data: dict[str, Any]) -> dict[str, Any]:
    """Validate, then return the DAC profile. Never returns a scalar summary."""
    validate_event_file(data)
    case, events = data["case"], data["events"]
    win_start = _parse_date(case["observation_window"]["start"])
    assert win_start is not None  # guaranteed by validation
    contested: dict[str, list[str]] = {}
    for ev in events:
        if ev.get("reading") is not None:
            contested.setdefault(ev["event_id"], []).append(ev["reading"])
    ids = sorted(contested)
    combos = [dict(zip(ids, c)) for c in itertools.product(*(sorted(contested[i]) for i in ids))] or [{}]

    profiles: list[dict[str, Any]] = []
    for combo in combos:
        chosen = [
            ev for ev in events
            if ev.get("reading") is None or combo.get(ev["event_id"]) == ev["reading"]
        ]
        dated = [ev for ev in chosen if ev["date_status"] not in ("missing", "censored")]
        t0 = _bounds(next(ev for ev in dated if ev["event_id"] == case["t0_event_id"]), win_start)
        sublayers: dict[str, Any] = {}
        for sub in PROFILE_SUBLAYERS:
            rows = [ev for ev in dated if ev["sublayer"] == sub]
            if sub == "delivery":
                rows = [ev for ev in rows if ev["end_point"] == case["end_point"]]
            if rows:
                first = _first(rows, win_start)
                sublayers[sub] = {
                    "lag_from_t0": _lag_range(t0, first),
                    "first_event_ids": sorted({ev["event_id"] for ev in rows
                                               if _bounds(ev, win_start)[0] == first[0]}),
                    "n_events": len(rows),
                }
        orders = {ev["event_id"]: ev for ev in dated if ev["sublayer"] == "firm_order"}
        deliveries = [ev for ev in dated if ev["sublayer"] == "delivery"]
        paired = [
            {
                "order_id": d["pairs_with"],
                "delivery_id": d["event_id"],
                "end_point": d["end_point"],
                "interval": _lag_range(_bounds(orders[d["pairs_with"]], win_start), _bounds(d, win_start)),
            }
            for d in deliveries if d.get("pairs_with") in orders
        ]
        primary = [d for d in deliveries if d["end_point"] == case["end_point"]]
        unpaired: dict[str, int | None] | None = None
        if orders and primary:
            unpaired = _lag_range(_first(list(orders.values()), win_start), _first(primary, win_start))
        secondary = sorted({d["end_point"] for d in deliveries} - {case["end_point"]})
        profiles.append({
            "reading": combo,
            "sublayers": sublayers,
            "paired_order_to_delivery": paired,
            "unpaired_first_order_to_first_delivery": unpaired,
            "secondary_end_points": {
                ep: _lag_range(t0, _first([d for d in deliveries if d["end_point"] == ep], win_start))
                for ep in secondary
            },
        })
    return {
        "standard_version": STANDARD_VERSION,
        "case_id": case["case_id"],
        "t0_event_id": case["t0_event_id"],
        "end_point": case["end_point"],
        "missing": sorted(ev["sublayer"] for ev in events if ev["date_status"] == "missing"),
        "censored": sorted(ev["sublayer"] for ev in events if ev["date_status"] == "censored"),
        "contested_events": {k: sorted(v) for k, v in contested.items()},
        "profiles": profiles,
    }
