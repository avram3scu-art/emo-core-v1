"""SMF v2 on per-storm NHC forecasts (docs/SMF_PROTOCOL.md §15).

Forecaster: NHC official forecast (OFCL), errors from the individual-forecast error file.
Persistence benchmark: OCD5 (CLIPER5 track / Decay-SHIFOR5 intensity, climatology and
persistence), from the ATCF a-decks, verified against HURDAT2 as in docs/LOOP_PROTOCOL.md §16
(amendments 4 and 6). Unit: the storm (mean differential per storm, storms in order of first
forecast). Family: track and intensity at 24, 48 and 72 h.
"""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

from emo.loop_hurricanes import Storm, best_position, gc_nmi
from emo.smf import SMFSkill, smf_family, smf_skill

LEADS = (24, 48, 72)
BASELINE_TECH = "OCD5"
ALPHA = 0.025  # family-wise, Holm (§15.6: keeps the family false-positive rate near 0.05 when storms correlate)
MIN_STORMS = 8  # §15: fewer storms with a pair at a lead -> "cannot be tested at this size"
DM_LAGS = 2  # storms in order of first forecast; neighbouring storms may share a pattern (§15.6: lag 2 limits
#              the false-positive rate best when consecutive storms are correlated)

# Column positions in a 37-field data line, from the file's header line 11 (checked 29 Oct 2026):
# Date/Time STMID F012 F024 F036 F048 F060 F072 F096 F120 F144 F168 Lat Lon WS
# 000hT01 012hT01 024hT01 036hT01 048hT01 060hT01 072hT01 ... 000hI01 ... 048hI01 060hI01 072hI01 ...
_ESS = {24: 3, 48: 5, 72: 7}
_TRK = {24: 17, 48: 19, 72: 21}
_INT = {24: 28, 48: 30, 72: 32}


@dataclass
class OfclLine:
    line_no: int
    t: dt.datetime
    stmid: str
    ess: dict[int, float]
    trk: dict[int, float]
    inten: dict[int, float]


def parse_error_file(lines: Iterable[tuple[int, str]]) -> list[OfclLine]:
    out = []
    for no, text in lines:
        p = text.split()
        if len(p) != 37 or not re.match(r"\d\d-\d\d-\d{4}/", p[0]):
            continue
        out.append(OfclLine(no, dt.datetime.strptime(p[0], "%d-%m-%Y/%H:%M:%S"), p[1],
                            {h: float(p[i]) for h, i in _ESS.items()},
                            {h: float(p[i]) for h, i in _TRK.items()},
                            {h: float(p[i]) for h, i in _INT.items()}))
    return out


@dataclass
class BaseRec:
    line_no: int
    lat: float
    lon: float
    vmax: int | None


def parse_adeck_base(lines: Iterable[tuple[int, str]]) -> dict[tuple[dt.datetime, int], BaseRec]:
    """OCD5 lines at TAU 24/48/72 keyed by (DTG, TAU); the earliest-listed line wins."""
    out: dict[tuple[dt.datetime, int], BaseRec] = {}
    for no, text in lines:
        p = [x.strip() for x in text.split(",")]
        if len(p) < 9 or p[4] != BASELINE_TECH or not p[5].isdigit() or int(p[5]) not in LEADS:
            continue
        key = (dt.datetime.strptime(p[2], "%Y%m%d%H"), int(p[5]))
        if key in out:
            continue
        lat = int(p[6][:-1]) / 10 * (-1 if p[6][-1] == "S" else 1)
        lon = int(p[7][:-1]) / 10 * (-1 if p[7][-1] == "W" else 1)
        v = int(p[8]) if p[8] not in ("", "0") else None
        out[key] = BaseRec(no, lat, lon, v)
    return out


@dataclass
class Pair:
    stmid: str
    t: dt.datetime
    lead: int
    var: str  # "track" (n mi) or "intensity" (kt, absolute)
    ofcl: float
    base: float
    err_line: int
    adeck_line: int


def build_pairs(errs: list[OfclLine], storms: dict[str, Storm],
                bases: dict[str, dict[tuple[dt.datetime, int], BaseRec]], season: int) -> list[Pair]:
    """Homogeneous OFCL/OCD5 error pairs of the season's storms (§15 rules 2-4)."""
    out: list[Pair] = []
    for e in sorted(errs, key=lambda x: (x.t, x.stmid)):
        if not e.stmid.endswith(str(season)) or e.stmid not in storms:
            continue
        b = bases.get(e.stmid, {})
        for h in LEADS:
            a = b.get((e.t, h))
            v = best_position(storms[e.stmid], e.t + dt.timedelta(hours=h))
            if a is None or v is None:
                continue
            if e.trk[h] != -9999:
                out.append(Pair(e.stmid, e.t, h, "track", e.trk[h], gc_nmi(a.lat, a.lon, v.lat, v.lon),
                                e.line_no, a.line_no))
            if e.inten[h] != -9999 and a.vmax is not None:
                out.append(Pair(e.stmid, e.t, h, "intensity", abs(e.inten[h]), abs(a.vmax - v.wind),
                                e.line_no, a.line_no))
    return out


def score(pairs: list[Pair], alpha: float = ALPHA) -> list[SMFSkill]:
    tests = []
    for var in ("track", "intensity"):
        for h in LEADS:
            q = [x for x in pairs if x.var == var and x.lead == h]
            tests.append(smf_skill(f"{var} {h} h", np.array([x.ofcl for x in q]), np.array([x.base for x in q]),
                                   DM_LAGS, clusters=np.array([x.stmid for x in q])))
    return smf_family(tests, alpha=alpha, min_units=MIN_STORMS)
