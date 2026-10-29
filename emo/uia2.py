"""UIA 2.0: the per-event profile of the loop links (docs/UIA_PROTOCOL.md §2.0).

A profile is reported column by column; it is never summed, weighted or averaged.
"""
from __future__ import annotations

import csv
from pathlib import Path

LETTERS = ("F", "A", "W")
SOURCE = {"F": "pr_F", "A": "at_A", "W": "wn_W_hours"}
PROFILE_COLUMNS = ("atcf", "name", "season", "V_kt", "F", "A", "W", "Y_state", "Y_fed", "He")


def _num(v: str) -> float | None:
    v = (v or "").strip()
    return float(v) if v else None


def he_value(y_state: float | None, y_fed: float | None) -> float | None:
    """He = -(Y_state + Y_fed): landfall -> DR declaration lag in days, sign-flipped."""
    if y_state is None or y_fed is None:
        return None
    return -(y_state + y_fed)


def profile_rows(events_csv: Path, max_season: int = 2025) -> list[dict]:
    rows = []
    with open(events_csv, newline="") as f:
        for r in csv.DictReader(f):
            season = int(r["ev_season"])
            if season > max_season:
                continue
            ys, yf = _num(r["dc_Y_state_days"]), _num(r["dc_Y_fed_days"])
            row = {
                "atcf": r["ev_atcf"], "name": r["ev_name"], "season": season,
                "V_kt": _num(r["ev_V_kt"]),
                "Y_state": ys, "Y_fed": yf, "He": he_value(ys, yf),
            }
            for k in LETTERS:
                row[k] = _num(r[SOURCE[k]])
            rows.append(row)
    return rows


def write_profile(rows: list[dict], out_csv: Path) -> None:
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PROFILE_COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r[k] is None else r[k]) for k in PROFILE_COLUMNS})
