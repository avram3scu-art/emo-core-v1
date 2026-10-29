"""Hurricane loop event table (session 2.4; docs/LOOP_PROTOCOL.md §2-§3, §16).

Pure functions: parsers for the committed source extracts, the landfall-state geometry,
the FEMA matching rule, the forecast-skill aggregate, the attention and warning measures,
and the table assembly. Fetching lives in scripts/fetch_loop_*.py, the build in
scripts/build_loop_table.py, the check in scripts/validate_loop_table.py.

No H4 or H5 statistic is computed here (session 2.4 task).
"""

from __future__ import annotations

import csv
import datetime as dt
import math
import re
import struct
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SEASONS = range(2015, 2026)
US_ENTITIES = None  # all STUSPS kept except the Pacific ones below
DROP_ENTITIES = {"GU", "AS", "MP"}
NEAR_KM = 50.0
R_EARTH_KM = 6371.0088
R_EARTH_NMI = 3440.065
QUAL_STATUS_HUTS = {"HU", "TS"}

# Fixed list of exclusion reasons (LOOP_PROTOCOL §16 rule 8).
REASONS = {
    "no_candidate": "no FEMA DR/EM record of a qualifying type in state k within the date window",
    "ambiguous": "no title names the storm and another table storm has a landfall in k within ±10 days",
    "no_dr": "matched records include no major disaster (DR)",
    "dr_request_missing": "DR request date missing",
    "y_fed_negative": "DR declaration date before DR request date (data error)",
    "f_no_lines": "no error-file line with initial time < t0 and 48-h OFCL and OCD5 errors",
    "f_ess_lt2": "summed 48-h equivalent sample size < 2",
    "a_no_article": "no candidate title resolves to an article (T1, T2 non-disambiguation, T3)",
    "a_fetch_missing": "pageview fetch record missing",
    "w_no_ww": "no advisory with a TS/hurricane watch or warning before the fetch stopped",
    "w_no_gis": "no GIS advisory files listed for the storm",
}

WW_CODES = {"TWA", "TWR", "HWA", "HWR"}


# ---------------------------------------------------------------- HURDAT2


@dataclass
class BestRecord:
    line_no: int
    time: dt.datetime
    ident: str
    status: str
    lat: float
    lon: float
    wind: int
    pressure: int
    r64: tuple[int, int, int, int]


@dataclass
class Storm:
    atcf: str
    name: str
    header_line: int
    records: list[BestRecord] = field(default_factory=list)

    @property
    def year(self) -> int:
        return int(self.atcf[4:8])


def _latlon(s: str) -> float:
    s = s.strip()
    v = float(s[:-1])
    return -v if s[-1] in "SW" else v


def parse_hurdat2(lines: Iterable[tuple[int, str]]) -> dict[str, Storm]:
    """Parse (original line number, text) pairs of a HURDAT2 file or extract."""
    storms: dict[str, Storm] = {}
    cur: Storm | None = None
    for no, text in lines:
        p = [x.strip() for x in text.rstrip("\n").split(",")]
        if not p or not p[0]:
            continue
        if p[0][:2].isalpha():
            cur = Storm(p[0], p[1], no)
            storms[cur.atcf] = cur
            continue
        if cur is None:
            raise ValueError(f"data line {no} before any header")
        t = dt.datetime.strptime(p[0] + p[1].zfill(4), "%Y%m%d%H%M")
        r64 = tuple(int(x) for x in p[16:20])
        cur.records.append(BestRecord(no, t, p[2], p[3], _latlon(p[4]), _latlon(p[5]),
                                      int(p[6]), int(p[7]), r64))  # type: ignore[arg-type]
    return storms


def best_position(storm: Storm, t: dt.datetime) -> BestRecord | None:
    for r in storm.records:
        if r.time == t:
            return r
    return None


# ---------------------------------------------------------------- geometry


def gc_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (lat1, lon1, lat2, lon2))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(math.sqrt(min(1.0, h)))


def gc_nmi(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return gc_km(lat1, lon1, lat2, lon2) * R_EARTH_NMI / R_EARTH_KM


def read_shapefile_polygons(shp: bytes, dbf: bytes) -> list[tuple[dict[str, str], list[np.ndarray]]]:
    """Minimal ESRI shapefile reader for polygon records (type 5): [(attributes, rings)]."""
    # dbf
    n, hl, rl = struct.unpack("<xxxxIHH", dbf[:12])
    fields_ = []
    i = 32
    while dbf[i] != 0x0D:
        fields_.append((dbf[i:i + 11].split(b"\0")[0].decode(), dbf[i + 16]))
        i += 32
    attrs = []
    for r in range(n):
        o = hl + r * rl + 1
        row = {}
        for name, ln in fields_:
            row[name] = dbf[o:o + ln].decode("latin1").strip()
            o += ln
        attrs.append(row)
    # shp
    out = []
    pos = 100
    k = 0
    while pos < len(shp):
        _, clen = struct.unpack(">ii", shp[pos:pos + 8])
        body = shp[pos + 8:pos + 8 + 2 * clen]
        pos += 8 + 2 * clen
        stype = struct.unpack("<i", body[:4])[0]
        rings: list[np.ndarray] = []
        if stype == 5:
            nparts, npts = struct.unpack("<ii", body[36:44])
            parts = list(struct.unpack(f"<{nparts}i", body[44:44 + 4 * nparts])) + [npts]
            pts = np.frombuffer(body[44 + 4 * nparts:44 + 4 * nparts + 16 * npts], dtype="<f8").reshape(-1, 2)
            rings = [pts[parts[j]:parts[j + 1]] for j in range(nparts)]
        elif stype != 0:
            raise ValueError(f"unsupported shape type {stype}")
        out.append((attrs[k], rings))
        k += 1
    return out


def point_in_rings(lon: float, lat: float, rings: list[np.ndarray]) -> bool:
    """Even-odd rule over all rings (holes handled)."""
    inside = False
    for ring in rings:
        x, y = ring[:, 0], ring[:, 1]
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        cond = (y > lat) != (y2 > lat)
        with np.errstate(divide="ignore", invalid="ignore"):
            xint = x + (lat - y) * (x2 - x) / (y2 - y)
        inside ^= bool(np.count_nonzero(cond & (lon < xint)) % 2)
    return inside


def dist_to_rings_km(lon: float, lat: float, rings: list[np.ndarray]) -> float:
    """Minimum distance from the point to the rings' segments (local equirectangular, km)."""
    c = math.cos(math.radians(lat))
    k = math.radians(1) * R_EARTH_KM
    best = math.inf
    for ring in rings:
        px = (ring[:, 0] - lon) * c * k
        py = (ring[:, 1] - lat) * k
        ax, ay, bx, by = px[:-1], py[:-1], px[1:], py[1:]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        with np.errstate(divide="ignore", invalid="ignore"):
            tt = np.where(L2 > 0, -(ax * dx + ay * dy) / L2, 0.0)
        tt = np.clip(tt, 0, 1)
        d = np.hypot(ax + tt * dx, ay + tt * dy)
        if d.size:
            best = min(best, float(d.min()))
    return best


def assign_state(lon: float, lat: float, polys: list[tuple[str, list[np.ndarray]]]) -> tuple[str, float]:
    """Return (entity, distance km): inside → (STUSPS, 0); else nearest within NEAR_KM; else ('', d)."""
    for code, rings in polys:
        if point_in_rings(lon, lat, rings):
            return code, 0.0
    best_code, best_d = "", math.inf
    for code, rings in polys:
        # cheap bounding-box prefilter (1 degree is > 50 km)
        allp = np.concatenate(rings)
        if (lon < allp[:, 0].min() - 1.5 or lon > allp[:, 0].max() + 1.5
                or lat < allp[:, 1].min() - 1.5 or lat > allp[:, 1].max() + 1.5):
            continue
        d = dist_to_rings_km(lon, lat, rings)
        if d < best_d:
            best_code, best_d = code, d
    if best_d <= NEAR_KM:
        return best_code, best_d
    return "", best_d


# ---------------------------------------------------------------- events


@dataclass
class Landfall:
    atcf: str
    line_no: int
    time: dt.datetime
    status: str
    lat: float
    lon: float
    state: str
    dist_km: float


def qualifying_landfalls(landfalls: list[Landfall], statuses: set[str]) -> list[Landfall]:
    return sorted((x for x in landfalls if x.state and x.status in statuses), key=lambda x: (x.time, x.line_no))


def read_landfalls(path: Path) -> list[Landfall]:
    out = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            out.append(Landfall(r["atcf"], int(r["hurdat2_line"]), dt.datetime.fromisoformat(r["time_utc"]),
                                r["status"], float(r["lat"]), float(r["lon"]), r["state"],
                                float(r["dist_km"])))
    return out


# ---------------------------------------------------------------- FEMA


def _date(s: str | None) -> dt.date | None:
    if not s:
        return None
    return dt.date.fromisoformat(s[:10])


def type_route(rec: dict[str, str], hu_only: bool) -> str:
    """'code', 'fallback' or '' (amendment 5)."""
    dit = (rec.get("designatedIncidentTypes") or "").strip()
    codes = {"H"} if hu_only else {"H", "4"}
    if dit:
        toks = {t.strip() for t in dit.split(",")}
        return "code" if toks & codes else ""
    it = (rec.get("incidentType") or "").strip()
    names = {"Hurricane"} if hu_only else {"Hurricane", "Tropical Storm"}
    return "fallback" if it in names else ""


def whole_word(name: str, title: str) -> bool:
    return re.search(rf"\b{re.escape(name)}\b", title or "", re.I) is not None


@dataclass
class Decision:
    status: str  # matched / unmatched
    reason: str = ""
    name_rule: str = ""  # title / window
    records: list[dict[str, str]] = field(default_factory=list)


def match_fema(storm_name: str, state: str, t0_date: dt.date, records: list[dict[str, str]],
               other_landfall_dates_in_k: list[dt.date], hu_only: bool = False) -> Decision:
    lo, hi = t0_date - dt.timedelta(days=10), t0_date + dt.timedelta(days=3)
    cand = []
    for r in records:
        if r.get("state") != state or r.get("declarationType") not in ("DR", "EM"):
            continue
        if not type_route(r, hu_only):
            continue
        b = _date(r.get("incidentBeginDate"))
        if b is None or not (lo <= b <= hi):
            continue
        cand.append(r)
    if not cand:
        return Decision("unmatched", "no_candidate")
    named = [r for r in cand if whole_word(storm_name, r.get("declarationTitle", ""))]
    if named:
        return Decision("matched", "", "title", named)
    if any(abs((d - t0_date).days) <= 10 for d in other_landfall_dates_in_k):
        return Decision("unmatched", "ambiguous")
    return Decision("matched", "", "window", cand)


@dataclass
class Declaration:
    disaster_number: int
    dtype: str
    decl_date: dt.date
    request_date: dt.date | None
    incident_ids: tuple[str, ...]
    region: str
    incident_types: tuple[str, ...]
    routes: tuple[str, ...]
    ids: tuple[str, ...]


def group_declarations(records: list[dict[str, str]], hu_only: bool = False) -> list[Declaration]:
    by: dict[int, list[dict[str, str]]] = {}
    for r in records:
        by.setdefault(int(r["disasterNumber"]), []).append(r)
    out = []
    for num, rs in sorted(by.items()):
        decl = min(d for d in (_date(r["declarationDate"]) for r in rs) if d is not None)
        reqs = [d for d in (_date(r.get("declarationRequestDate")) for r in rs) if d is not None]
        out.append(Declaration(
            num, rs[0]["declarationType"], decl, min(reqs) if reqs else None,
            tuple(sorted({r.get("incidentId", "") for r in rs})),
            sorted({str(r.get("region", "")) for r in rs})[0],
            tuple(sorted({r.get("incidentType", "") for r in rs})),
            tuple(sorted({type_route(r, hu_only) for r in rs})),
            tuple(sorted(r["id"] for r in rs))))
    return out


# ---------------------------------------------------------------- predict


@dataclass
class ErrLine:
    line_no: int
    t: dt.datetime
    stmid: str
    f048: float
    ofcl48: float
    ofcl48_int: float


def parse_error_lines(lines: Iterable[tuple[int, str]]) -> list[ErrLine]:
    out = []
    for no, text in lines:
        p = text.split()
        if len(p) != 37 or not re.match(r"\d\d-\d\d-\d{4}/", p[0]):
            continue
        out.append(ErrLine(no, dt.datetime.strptime(p[0], "%d-%m-%Y/%H:%M:%S"), p[1],
                           float(p[5]), float(p[19]), float(p[30])))
    return out


@dataclass
class AdeckRec:
    line_no: int
    t: dt.datetime
    lat: float
    lon: float
    vmax: int | None


BASELINE_TECH = "OCD5"  # amendment 6 (LOOP_PROTOCOL §16)


def parse_adeck_base48(lines: Iterable[tuple[int, str]]) -> dict[dt.datetime, AdeckRec]:
    """Baseline (OCD5) TAU-48 line per DTG; the earliest-listed line wins."""
    out: dict[dt.datetime, AdeckRec] = {}
    for no, text in lines:
        p = [x.strip() for x in text.split(",")]
        if len(p) < 9 or p[4] != BASELINE_TECH or p[5] != "48":
            continue
        t = dt.datetime.strptime(p[2], "%Y%m%d%H")
        if t in out:
            continue
        lat = int(p[6][:-1]) / 10 * (-1 if p[6][-1] == "S" else 1)
        lon = int(p[7][:-1]) / 10 * (-1 if p[7][-1] == "W" else 1)
        v = int(p[8]) if p[8] not in ("", "0") else None
        out[t] = AdeckRec(no, t, lat, lon, v)
    return out


@dataclass
class Skill:
    f: float | None
    f_int: float | None
    n_lines: int
    ess48: float
    lines: list[tuple[int, int, float, float]]  # err line, adeck line, ofcl48, base_48
    reason: str


def track_skill(storm: Storm, t0: dt.datetime, errs: list[ErrLine], base: dict[dt.datetime, AdeckRec]) -> Skill:
    used = []
    so = sb = ess = 0.0
    io = ib = 0.0
    n_int = 0
    for e in errs:
        if e.stmid != storm.atcf or e.t >= t0 or e.ofcl48 == -9999:
            continue
        a = base.get(e.t)
        v = best_position(storm, e.t + dt.timedelta(hours=48))
        if a is None or v is None:
            continue
        eb = gc_nmi(a.lat, a.lon, v.lat, v.lon)
        used.append((e.line_no, a.line_no, e.ofcl48, eb))
        so += e.ofcl48
        sb += eb
        ess += e.f048
        if e.ofcl48_int != -9999 and a.vmax is not None:
            io += abs(e.ofcl48_int)
            ib += abs(a.vmax - v.wind)
            n_int += 1
    if not used:
        return Skill(None, None, 0, 0.0, [], "f_no_lines")
    if ess < 2:
        return Skill(None, None, len(used), ess, used, "f_ess_lt2")
    f = 1 - so / sb if sb > 0 else None
    fi = 1 - io / ib if n_int and ib > 0 else None
    return Skill(f, fi, len(used), ess, used, "")


# ---------------------------------------------------------------- attend


def candidate_titles(name: str, year: int, hu_ts: bool = True) -> dict[str, str]:
    n = name.strip().title()
    d = {"T1": f"Hurricane {n} ({year})", "T2": f"Hurricane {n}"}
    if hu_ts:
        d["T3"] = f"Tropical Storm {n} ({year})"
    return d


def resolve_target(query: dict, titles: dict[str, str]) -> tuple[str | None, str, list[str]]:
    """From a MediaWiki action=query response (formatversion 2, redirects=1, prop=pageprops|info):
    returns (target title, rule used, candidate titles that redirect to the target)."""
    q = query.get("query", {})
    norm = {x["from"]: x["to"] for x in q.get("normalized", [])}
    redir = {x["from"]: x["to"] for x in q.get("redirects", [])}
    pages = {p["title"]: p for p in q.get("pages", [])}

    def resolve(t: str) -> tuple[str | None, bool]:
        t = norm.get(t, t)
        seen = set()
        while t in redir and t not in seen:
            seen.add(t)
            t = redir[t]
        p = pages.get(t)
        if p is None or p.get("missing") or p.get("invalid"):
            return None, False
        return t, "disambiguation" in (p.get("pageprops") or {})

    target, rule = None, ""
    t1, _ = resolve(titles["T1"])
    if t1:
        target, rule = t1, "T1"
    else:
        t2, dis = resolve(titles["T2"])
        if t2 and not dis:
            target, rule = t2, "T2"
        elif "T3" in titles:
            t3, _ = resolve(titles["T3"])
            if t3:
                target, rule = t3, "T3"
    if target is None:
        return None, "", []
    via = []
    for t in titles.values():
        tn = norm.get(t, t)
        if tn != target and resolve(t)[0] == target and tn in redir:
            via.append(tn)
    return target, rule, sorted(set(via))


def views_by_day(pv_json: dict) -> dict[str, int]:
    return {it["timestamp"][:8]: int(it["views"]) for it in pv_json.get("items", [])}


def attention(t0_date: dt.date, series: list[dict[str, int]]) -> tuple[float, int]:
    days = [(t0_date - dt.timedelta(days=k)).strftime("%Y%m%d") for k in (1, 2, 3)]
    total = sum(s.get(d, 0) for s in series for d in days)
    return math.log10(1 + total), total


# ---------------------------------------------------------------- warnings


def parse_advdate(s: str) -> dt.datetime | None:
    try:
        return dt.datetime.strptime(s.strip(), "%y%m%d/%H%M")
    except ValueError:
        return None
