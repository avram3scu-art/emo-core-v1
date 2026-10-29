"""Loop cards for the global hazard stream: joins, rungs, stages, the H3 stream test.

Registered rules: docs/LOOP_CARD_PROTOCOL.md (session 3.3). Every constant below is part of
the registered protocol; a change is an amendment there, never a silent edit.

This module only computes. It never fetches and never reads the log by itself: the caller
(a GitHub Action holding EMO_STREAM_KEY, session 3.4) passes decrypted runs in memory and may
commit only the aggregates of `safe_aggregate` and `h3_score` (protocol §8).
"""
from __future__ import annotations

import datetime as dt
import math
import re
from collections import defaultdict
from typing import Any

from emo.stream.exclusions import EU27_ISO3, _is_eu27

UTC = dt.UTC

# --- §3 hazard crosswalk -----------------------------------------------------------------
HAZARDS = ("EQ", "TS", "TC", "FL", "VO", "DR", "WF")
_KEYWORDS = (                                     # checked in this order
    ("tsunami", "TS"), ("earthquake", "EQ"), ("cyclone", "TC"), ("hurricane", "TC"),
    ("typhoon", "TC"), ("tropical", "TC"), ("flood", "FL"), ("volcan", "VO"),
    ("drought", "DR"), ("fire", "WF"),
)


def hazard_from_text(*texts) -> str | None:
    blob = " ".join(_flat(t) for t in texts).lower()
    for kw, h in _KEYWORDS:
        if kw in blob:
            return h
    return None


def _flat(v) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return " ".join(_flat(x) for x in v.values())
    if isinstance(v, (list, tuple)):
        return " ".join(_flat(x) for x in v)
    return str(v)


# --- §3 parsing --------------------------------------------------------------------------
def parse_time(v) -> tuple[dt.datetime | None, str]:
    """(UTC datetime, precision) with precision 'time', 'day' or 'none'."""
    if isinstance(v, bool) or v is None:
        return None, "none"
    if isinstance(v, (int, float)):               # USGS: ms since epoch
        return dt.datetime.fromtimestamp(v / 1000, UTC), "time"
    if not isinstance(v, str) or len(v) < 10:
        return None, "none"
    s = v.strip().replace("Z", "+00:00")
    try:
        if len(s) == 10:
            d = dt.date.fromisoformat(s)
            return dt.datetime(d.year, d.month, d.day, tzinfo=UTC), "day"
        t = dt.datetime.fromisoformat(s)
    except ValueError:
        return None, "none"
    if t.tzinfo is None:
        t = t.replace(tzinfo=UTC)
    return t.astimezone(UTC), "time"


_GLIDE = re.compile(r"^([A-Z]{2})-?(\d{4})-?(\d{6})(?:-?([A-Z]{3}))?$")


def glide_key(v) -> tuple[str, str, str] | None:
    """GLIDE as (type, year, number); the ISO3 suffix is ignored (one number, many countries)."""
    if not isinstance(v, str):
        return None
    m = _GLIDE.match(re.sub(r"\s+", "", v).upper())
    return (m[1], m[2], m[3]) if m else None


def iso3_set(*values) -> set[str]:
    """ISO3 codes from strings ('PHL', 'PHL,VNM') or dicts with an iso3/iso key. Names: none."""
    out: set[str] = set()
    for v in values:
        if v is None:
            continue
        if isinstance(v, str):
            for tok in re.split(r"[,;\s]+", v.strip()):
                if re.fullmatch(r"[A-Za-z]{3}", tok):
                    out.add(tok.upper())
        elif isinstance(v, dict):
            for k in ("iso3", "ISO3", "iso"):
                if isinstance(v.get(k), str) and re.fullmatch(r"[A-Za-z]{3}", v[k]):
                    out.add(v[k].upper())
            for k in ("countries", "country", "affectedcountries"):
                if k in v:
                    out |= iso3_set(v[k])
        elif isinstance(v, (list, tuple)):
            for x in v:
                out |= iso3_set(x)
    return out


def _haversine_km(a, b) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 6371.0 * math.asin(math.sqrt(h))


# --- §2 nodes: one per source record, deduplicated over snapshots ------------------------
def _go_dtype(r) -> str | None:
    return hazard_from_text(r.get("dtype"), r.get("dtype_name"))


def build_nodes(runs: list[dict]) -> dict:
    """key -> {'src','snaps':[(fetched_at, rec)] sorted,'latest','earliest_seen'}."""
    snaps: dict = defaultdict(list)
    for run in runs:
        src = run.get("sources", {})
        for f in src.get("gdacs", {}).get("records", []):
            p = f.get("properties") or {}
            if p.get("eventid") is not None and p.get("eventtype"):
                snaps[("gdacs", str(p["eventtype"]), str(p["eventid"]))].append(f)
        for f in src.get("usgs", {}).get("records", []):
            if f.get("_emo_feed") == "comcat" and f.get("id"):
                snaps[("usgs", str(f["id"]))].append(f)
        for r in src.get("cems", {}).get("records", []):
            if r.get("code") and not _is_eu27(r.get("countries")):   # §8: EU27 CEMS never used
                snaps[("cems", str(r["code"]))].append(r)
        for r in src.get("ifrc_go", {}).get("records", []):
            feed = str(r.get("_emo_feed", ""))
            if r.get("id") is None:
                continue
            if feed == "event":
                snaps[("go_event", str(r["id"]))].append(r)
            elif feed.startswith("appeal"):
                snaps[("go_appeal", str(r["id"]))].append(r)
    nodes = {}
    for k, lst in snaps.items():
        lst = sorted(lst, key=lambda r: str(r.get("_emo_fetched_at", "")))
        nodes[k] = {"src": k[0], "snaps": lst, "latest": lst[-1],
                    "earliest_seen": parse_time(lst[0].get("_emo_fetched_at"))[0]}
    return nodes


def node_hazard(k, n) -> str | None:
    r = n["latest"]
    if k[0] == "gdacs":
        return k[1] if k[1] in HAZARDS else None
    if k[0] == "usgs":
        return "EQ"
    if k[0] == "cems":
        return hazard_from_text(r.get("category"), r.get("subCategory"))
    return _go_dtype(r)


def node_onset(k, n) -> tuple[dt.datetime | None, str]:
    r = n["latest"]
    if k[0] == "gdacs":
        return parse_time((r.get("properties") or {}).get("fromdate"))
    if k[0] == "usgs":
        return parse_time((r.get("properties") or {}).get("time"))
    if k[0] == "cems":
        return parse_time(r.get("eventTime"))
    if k[0] == "go_event":
        return parse_time(r.get("disaster_start_date"))
    return parse_time(r.get("start_date"))


def node_iso3(k, n) -> set[str]:
    r = n["latest"]
    if k[0] == "gdacs":
        p = r.get("properties") or {}
        return iso3_set(p.get("iso3"), p.get("affectedcountries"))
    if k[0] == "usgs":
        return set()
    if k[0] == "cems":
        return iso3_set(r.get("countries"))
    if k[0] == "go_event":
        return iso3_set(r.get("countries"))
    return iso3_set(r.get("country"))


def _coords(r):
    g = (r.get("geometry") or {}).get("coordinates")
    if isinstance(g, (list, tuple)) and len(g) >= 2 and all(
            isinstance(x, (int, float)) for x in g[:2]):
        return g[0], g[1]
    return None


# --- §4 join rule (frozen before any linking statistic) ----------------------------------
FALLBACK_WINDOW_DAYS = {          # candidate onset minus GDACS fromdate, inclusive
    "EQ": (0, 2), "TS": (0, 2), "TC": (-3, 7), "FL": (-7, 14), "VO": (-7, 14),
    "WF": (-7, 14),               # DR: no fallback (explicit keys only)
}
EQ_USGS_MAX_MIN = 30              # USGS <-> GDACS earthquake: |dt| <= 30 min ...
EQ_USGS_MAX_KM = 100.0            # ... and epicentres <= 100 km apart


class _UF:
    def __init__(self, keys):
        self.p = {k: k for k in keys}

    def find(self, k):
        while self.p[k] != k:
            self.p[k] = self.p[self.p[k]]
            k = self.p[k]
        return k

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def join(nodes: dict) -> tuple[list[set], list[dict]]:
    """Components (sets of node keys) and the edge log [{a, b, rule, note}]."""
    uf, edges = _UF(nodes), []
    gdacs = {k: n for k, n in nodes.items() if k[0] == "gdacs"}

    def link(a, b, rule, note=""):
        uf.union(a, b)
        edges.append({"a": a, "b": b, "rule": rule, "note": note})

    by_eventid = defaultdict(list)
    for k in gdacs:
        by_eventid[k[2]].append(k)
    explicit_anchor: set = set()
    # K1 CEMS gdacsId -> GDACS eventid (hazard must agree when the id is shared by types)
    for k, n in nodes.items():
        if k[0] != "cems" or not n["latest"].get("gdacsId"):
            continue
        raw = by_eventid.get(str(n["latest"]["gdacsId"]).strip(), [])
        cands = [c for c in raw if c[1] == node_hazard(k, n)] if len(raw) > 1 else raw
        if len(cands) == 1:
            link(k, cands[0], "K1_gdacsId")
            explicit_anchor.add(k)
        elif raw:                                # shared id, hazard does not decide
            edges.append({"a": k, "b": None, "rule": "K1_gdacsId", "note": "tie"})
    # K2 GLIDE equal (type, year, number) between GDACS and GO events
    g_by_glide = defaultdict(list)
    for k, n in gdacs.items():
        g = glide_key((n["latest"].get("properties") or {}).get("glide"))
        if g:
            g_by_glide[g].append(k)
    for k, n in nodes.items():
        if k[0] != "go_event":
            continue
        g = glide_key(n["latest"].get("glide"))
        for c in g_by_glide.get(g, []) if g else []:
            link(k, c, "K2_glide")
            explicit_anchor.add(k)
    # K3 GO appeal.event -> GO event
    for k, n in nodes.items():
        if k[0] != "go_appeal":
            continue
        e = n["latest"].get("event")
        eid = e.get("id") if isinstance(e, dict) else e
        if eid is not None and ("go_event", str(eid)) in nodes:
            link(k, ("go_event", str(eid)), "K3_event_id")
    # F1 USGS <-> GDACS earthquake by time and distance (no documented shared id)
    for k, n in nodes.items():
        if k[0] != "usgs":
            continue
        t, _ = node_onset(k, n)
        c1 = _coords(n["latest"])
        best = []
        for g, gn in gdacs.items():
            if g[1] != "EQ":
                continue
            tg, prec = node_onset(g, gn)
            c2 = _coords(gn["latest"])
            if t is None or tg is None or prec != "time" or c1 is None or c2 is None:
                continue
            dmin = abs((tg - t).total_seconds()) / 60
            if dmin <= EQ_USGS_MAX_MIN and _haversine_km(c1, c2) <= EQ_USGS_MAX_KM:
                best.append((dmin, g))
        best.sort()
        if len(best) == 1 or (len(best) > 1 and best[0][0] < best[1][0]):
            link(k, best[0][1], "F1_eq_time_distance")
        elif best:
            edges.append({"a": k, "b": None, "rule": "F1_eq_time_distance", "note": "tie"})
    # F2 fallback: GO events and CEMS activations with no explicit hazard anchor
    for k, n in nodes.items():
        if k[0] not in ("go_event", "cems") or k in explicit_anchor:
            continue
        h, (t, _), iso = node_hazard(k, n), node_onset(k, n), node_iso3(k, n)
        if h not in FALLBACK_WINDOW_DAYS or t is None or not iso:
            continue
        lo, hi = FALLBACK_WINDOW_DAYS[h]
        cands = []
        for g, gn in gdacs.items():
            if g[1] != h or not (iso & node_iso3(g, gn)):
                continue
            tg, _ = node_onset(g, gn)
            if tg is None:
                continue
            d = (t.date() - tg.date()).days
            if lo <= d <= hi:
                te, _ = parse_time((gn["latest"].get("properties") or {}).get("todate"))
                inside = tg.date() <= t.date() <= (te or tg).date()
                cands.append((abs(d), 0 if inside else 1, g))
        cands.sort(key=lambda c: (c[0], c[1]))
        if len(cands) == 1 or (len(cands) > 1 and cands[0][:2] < cands[1][:2]):
            link(k, cands[0][2], "F2_iso3_hazard_window")
        elif cands:
            edges.append({"a": k, "b": None, "rule": "F2_iso3_hazard_window", "note": "tie"})
    comps = defaultdict(set)
    for k in nodes:
        comps[uf.find(k)].add(k)
    return list(comps.values()), edges


# --- §5-§6 rungs, statuses, stages ------------------------------------------------------
GDACS_WARN = {"orange", "red"}
PAGER_WARN = {"yellow", "orange", "red"}
WINDOW_DAYS = {"W": 7, "R": 30, "D": 60, "B_after_D": 60}
CARD_CLOSE_DAYS = 180
GAP_DAYS = 7                       # >= 7 consecutive source-days lost: rung "missing"
COVERAGE_COLLAPSE = 0.5
ATTENTION_MIN_VIEWS = 1000
STAGE_LABELS = {
    0: "no warning or response record",
    1: "warning not recognised",
    2: "recognised, not transmitted",
    3: "reached decision-makers, no budget",
    4: "funded, fragmented",
    5: "coordinated",
    6: "learned (faster than last time)",
}
STATUSES = ("present", "not yet", "absent", "missing", "no source", "withheld")


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _gap(source_gaps: dict, sources, start: dt.date, end: dt.date) -> bool:
    """True if any listed source lost >= GAP_DAYS consecutive days overlapping [start, end]."""
    for s in sources:
        days = sorted(d for d in source_gaps.get(s, set())
                      if start - dt.timedelta(days=GAP_DAYS) <= d <= end)
        run, prev = 0, None
        for d in days:
            run = run + 1 if prev and (d - prev).days == 1 else 1
            prev = d
            if run >= GAP_DAYS and d >= start:   # a lost stretch reaching into the window
                return True
    return False


def _status(t, window_end, now, gap):
    if t is not None:
        return "present"
    if now < window_end:
        return "not yet"
    return "missing" if gap else "absent"


def build_card(comp: set, nodes: dict, now: dt.datetime, source_gaps: dict | None = None,
               attention: dict | None = None, prior_lags: dict | None = None) -> dict:
    """One card. `attention`: {'status', 't', 'title'} from the §7 rule, or None (no source)."""
    gaps = source_gaps or {}
    keys = sorted(comp, key=str)
    hazard_keys = [k for k in keys if k[0] in ("gdacs", "usgs")]
    hz = {node_hazard(k, nodes[k]) for k in keys} - {None}
    iso = set().union(*(node_iso3(k, nodes[k]) for k in keys))
    eu27 = bool(iso & EU27_ISO3)
    # onset: earliest hazard-record onset; else earliest decision-record onset
    on: list[Any] = sorted((node_onset(k, nodes[k]) + (k,) for k in hazard_keys
                 if node_onset(k, nodes[k])[0] is not None), key=lambda x: x[0])
    anchored = bool(on)
    if not on:
        on = sorted((node_onset(k, nodes[k]) + (k,) for k in keys
                     if node_onset(k, nodes[k])[0] is not None), key=lambda x: x[0])
    t_on, p_on = (on[0][0], on[0][1]) if on else (None, "none")
    hazard = (node_hazard(on[0][2], nodes[on[0][2]]) if on else None) or (
        sorted(str(x) for x in hz)[0] if hz else None)

    # W warning
    w: list[Any] = []
    for k in hazard_keys:
        n = nodes[k]
        if k[0] == "gdacs" and k[1] != "FL":
            for i, s in enumerate(n["snaps"]):
                if str((s.get("properties") or {}).get("alertlevel", "")).lower() in GDACS_WARN:
                    ts, _ = parse_time(s.get("_emo_fetched_at"))
                    o, op = node_onset(k, n)
                    if (i == 0 and k[1] == "EQ" and o is not None and op == "time"
                            and ts is not None and ts - o <= dt.timedelta(days=1)):
                        w.append((o, "onset-proxy"))
                    elif ts is not None:
                        w.append((ts, "snapshot"))
                    break
        if k[0] == "usgs":
            if str((n["latest"].get("properties") or {}).get("alert", "")).lower() in PAGER_WARN:
                o, _ = node_onset(k, n)
                if o is not None:
                    w.append((o, "onset-proxy"))
    w.sort(key=lambda x: x[0])
    no_warn_source = hazard == "FL" or not hazard_keys

    # R recognition: GO event, GLIDE, attention
    r: list[Any] = []
    for k in keys:
        n = nodes[k]
        if k[0] == "go_event":
            t, p = parse_time(n["latest"].get("created_at"))
            r.append((t, p) if t else (n["earliest_seen"], "snapshot"))
        if k[0] in ("go_event", "gdacs"):
            for s in n["snaps"]:
                g = s.get("glide") if k[0] == "go_event" else (s.get("properties") or {}).get("glide")
                if glide_key(g):
                    r.append((parse_time(s.get("_emo_fetched_at"))[0], "snapshot"))
                    break
    if attention and attention.get("status") == "present" and attention.get("t"):
        r.append((attention["t"], "day"))
    r = sorted((x for x in r if x[0] is not None), key=lambda x: x[0])

    # D decision: CEMS activation (non-EU27 only), GO appeal
    d: list[Any] = []
    systems: set[str] = set()
    for k in keys:
        n = nodes[k]
        if k[0] == "cems":
            t, p = parse_time(n["latest"].get("activationTime"))
            systems.add("CEMS")
            d.append((t, p) if t else (n["earliest_seen"], "snapshot"))
        if k[0] == "go_appeal":
            a = n["latest"]
            t, p = parse_time(a.get("created_at"))
            if t is None:
                t, p = parse_time(a.get("start_date"))
            systems.add("IFRC")
            d.append((t, p) if t else (n["earliest_seen"], "snapshot"))
    d = sorted((x for x in d if x[0] is not None), key=lambda x: x[0])

    # B money: DREF record, or amount_funded > 0 (earliest snapshot showing it)
    b: list[Any] = []
    req, fund, open_appeal = 0.0, 0.0, False
    for k in keys:
        if k[0] != "go_appeal":
            continue
        n = nodes[k]
        a = n["latest"]
        if a.get("atype") == 0:
            b.append(parse_time(a.get("start_date")) if a.get("start_date") else
                     (n["earliest_seen"], "snapshot"))
        for s in n["snaps"]:
            if (_f(s.get("amount_funded")) or 0) > 0:
                b.append((parse_time(s.get("_emo_fetched_at"))[0], "snapshot"))
                break
        if a.get("atype") == 1 and _f(a.get("amount_requested")):
            req += _f(a.get("amount_requested")) or 0
            fund += _f(a.get("amount_funded")) or 0
        te, _ = parse_time(a.get("end_date"))
        if te is None or te > now:
            open_appeal = True
    b = sorted((x for x in b if x and x[0] is not None), key=lambda x: x[0])
    coverage = fund / req if req > 0 else None

    # C coordination: both decision systems and money
    c_present = b and {"CEMS", "IFRC"} <= systems

    # statuses
    base = t_on or (d[0][0] if d else now)
    w_end = base + dt.timedelta(days=WINDOW_DAYS["W"])
    r_end = base + dt.timedelta(days=WINDOW_DAYS["R"])
    d_end = base + dt.timedelta(days=WINDOW_DAYS["D"])
    close = base + dt.timedelta(days=CARD_CLOSE_DAYS)
    b_end = (d[0][0] + dt.timedelta(days=WINDOW_DAYS["B_after_D"])) if d else d_end
    sd = base.date()
    st = {
        "W": "no source" if no_warn_source and not w else _status(
            w[0][0] if w else None, w_end, now, _gap(gaps, ["gdacs", "usgs"], sd, w_end.date())),
        "R": _status(r[0][0] if r else None, r_end, now,
                     _gap(gaps, ["ifrc_go", "gdacs"], sd, r_end.date())),
        "D": _status(d[0][0] if d else None, d_end, now,
                     _gap(gaps, ["ifrc_go", "cems"], sd, d_end.date())),
        "B": _status(b[0][0] if b else None, b_end, now,
                     _gap(gaps, ["ifrc_go"], sd, b_end.date())),
        "C": "present" if c_present else ("not yet" if now < close else "absent"),
        "A": ("no source" if attention is None else attention.get("status", "missing")),
    }
    if eu27:
        st["CEMS"] = "withheld"                    # E1: never shown for EU27 events
        if not c_present:
            st["C"] = "withheld"
    order = ["W", "R", "D", "B", "C"]
    furthest = max([i + 1 for i, x in enumerate(order) if st[x] == "present"], default=0)
    closed = now >= close
    collapsed = None
    if furthest == 5 and closed:
        collapsed = (coverage < COVERAGE_COLLAPSE) if coverage is not None else None
    lag_od = ((d[0][0] - t_on).total_seconds() / 86400) if (d and t_on) else None
    lag_wd = ((d[0][0] - w[0][0]).total_seconds() / 86400) if (d and w) else None
    learned = None
    if prior_lags is not None and lag_od is not None and hazard and iso:
        prev = [prior_lags[(c, hazard)] for c in sorted(iso) if (c, hazard) in prior_lags]
        learned = (lag_od < min(prev)) if prev else None
    stage = furthest
    if furthest == 5 and collapsed is False and learned:
        stage = 6
    label = STAGE_LABELS[stage]
    if furthest == 5 and collapsed:
        label = "coordinated, then collapsed"
    return {
        "card_id": "|".join(map(str, keys[0])) if not hazard_keys else "|".join(
            map(str, sorted(hazard_keys, key=str)[0])),
        "hazard": hazard, "iso3": sorted(iso), "eu27": eu27, "anchored": anchored,
        "onset": t_on.isoformat() if t_on else None, "onset_precision": p_on,
        "t_warning": w[0][0].isoformat() if w else None,
        "warning_precision": w[0][1] if w else None,
        "t_recognition": r[0][0].isoformat() if r else None,
        "t_decision": d[0][0].isoformat() if d else None,
        "decision_precision": d[0][1] if d else None,
        "decision_systems": sorted(systems), "t_money": b[0][0].isoformat() if b else None,
        "coverage": coverage, "appeal_open": open_appeal,
        "lag_onset_decision_days": lag_od, "lag_warning_decision_days": lag_wd,
        "lag_so_far_days": _days_since(now, w[0][0] if w else t_on) if not d else None,
        "rungs": st, "furthest_rung": furthest, "stage": stage, "stage_label": label,
        "closed": closed, "collapsed": collapsed, "learned": learned,
        "attention_title": (attention or {}).get("title"),
    }


def _days_since(now: dt.datetime, t: dt.datetime | None) -> float | None:
    return (now - t).total_seconds() / 86400 if t is not None else None


def card_population(comps: list[set], nodes: dict) -> list[set]:
    """§2: a card for every component with a GDACS orange/red or PAGER yellow+ record, or any
    decision record (CEMS, or a GO appeal whose hazard class is natural)."""
    out = []
    for c in comps:
        warn = any(
            (k[0] == "gdacs" and any(str((s.get("properties") or {}).get("alertlevel", "")
                                         ).lower() in GDACS_WARN for s in nodes[k]["snaps"]))
            or (k[0] == "usgs" and str((nodes[k]["latest"].get("properties") or {})
                                       .get("alert", "")).lower() in PAGER_WARN)
            for k in c)
        dec = any(k[0] == "cems" or (k[0] == "go_appeal" and (
            node_hazard(k, nodes[k]) in HAZARDS or any(
                j[0] == "go_event" and node_hazard(j, nodes[j]) in HAZARDS for j in c)))
            for k in c)
        if warn or dec:
            out.append(c)
    return out


# --- §7 English pageview matching rule and per-article E2a-E2d filters --------------------
E2A_ONSET = (dt.date(2026, 10, 25), dt.date(2027, 11, 7))   # GWI v2 window with margin
E2A_MAG = 6.8                                               # margin below M 7.0
E2A_UNTIL = dt.date(2027, 11, 16)
GWI_V2_PLACEBOS = {
    "Photosynthesis", "Prime number", "Pythagorean theorem", "Mitochondrion", "Mitochondria",
    "Periodic table", "Atom", "Cell (biology)", "Fraction", "Triangle", "Water cycle", "Leaf",
    "Bird", "Tree", "River", "Chess", "Piano", "Bread", "Algebra", "Circle", "Fern",
}
E2C_UNTIL = dt.date(2029, 2, 1)
E2D_FROM = dt.date(2027, 1, 1)
US_ATLANTIC_ISO3 = {"USA", "PRI", "VIR"}
# Flags set only by the session that scores each protected test (recorded in RECORD.md).
GWI_V2_SCORED = False
FLOOD_TEST_SCORED = False
HURRICANE_SEASONS_SCORED: set[int] = set()
_FLOOD_TITLE = re.compile(r"\b(river|rivers|flood|floods|flooding|floodplain)\b", re.I)
EU27_EN_NAMES = (
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech", "Denmark", "Estonia",
    "Finland", "France", "German", "Greece", "Greek", "Hungar", "Ireland", "Irish", "Ital",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Dutch", "Poland", "Polish",
    "Portug", "Romania", "Slovak", "Sloven", "Spain", "Spanish", "Sweden", "Swedish",
    "Europe", "French", "Belgian", "Austrian", "Danish", "Finnish",
)
PAGEVIEW_DAYS = (-7, 30)


def e2_refusal(ev: dict, today: dt.date, title: str | None = None) -> str | None:
    """Reason a pageview (or matching) request must not be made, or None.

    ev: hazard, onset (date), iso3 (set), magnitudes (list, None = unknown), lat, lon.
    Checked on the event before any Wikimedia request and again on the resolved title.
    """
    h, on, iso = ev.get("hazard"), ev.get("onset"), set(ev.get("iso3") or ())
    gwi_closed = GWI_V2_SCORED and today >= E2A_UNTIL
    if h == "EQ" and on is None and not gwi_closed:
        return "E2a: earthquake without onset"
    if h == "EQ" and on is not None and E2A_ONSET[0] <= on <= E2A_ONSET[1] and not gwi_closed:
        mags = ev.get("magnitudes") or [None]
        if any(m is None or m >= E2A_MAG for m in mags):
            return "E2a: earthquake M>=6.8 (or unknown) in GWI v2 window"
    if title is not None and title.strip() in GWI_V2_PLACEBOS and not gwi_closed:
        return "E2a: GWI v2 placebo article"
    flood_closed = FLOOD_TEST_SCORED and today >= E2C_UNTIL
    if not flood_closed:
        if title is not None and re.search(r"\b(river|rivers)\b", title, re.I):
            return "E2c: river article"
        floodish = h == "FL" or (title is not None and _FLOOD_TITLE.search(title))
        if floodish and (not iso or iso & EU27_ISO3 or (title and any(
                n.lower() in title.lower() for n in EU27_EN_NAMES))):
            return "E2c: flood article that is or may be EU27"
    if h == "TC" and (on is None or on >= E2D_FROM):
        season = on.year if on else None
        lat, lon = ev.get("lat"), ev.get("lon")
        atlantic = (lat is None or lon is None) or (0 <= lat <= 70 and -110 <= lon <= 0)
        if (iso & US_ATLANTIC_ISO3 or atlantic) and season not in HURRICANE_SEASONS_SCORED:
            return "E2d: possible US-landfalling Atlantic storm, season not scored"
    return None


def candidate_titles(hazard: str | None, year: int, country: str | None,
                     name: str | None) -> list[str]:
    """§7 templates. TC name from GDACS eventname ('MELISSA-25' -> 'Melissa')."""
    out: list[str] = []
    if hazard == "TC" and name:
        n = re.sub(r"-\d{2}$", "", name.strip()).title()
        if re.fullmatch(r"[A-Za-z][A-Za-z' -]+", n):
            for p in ("Hurricane", "Typhoon", "Cyclone", "Tropical Storm",
                      "Severe Tropical Storm", "Severe Cyclonic Storm"):
                out += [f"{p} {n}", f"{p} {n} ({year})"]
    elif hazard == "EQ" and country:
        out = [f"{year} {country} earthquake", f"{year} {country} earthquakes"]
    elif hazard == "FL" and country:
        out = [f"{year} {country} floods", f"{year} {country} flood"]
    return out


def match_article(resolved: list[dict], onset: dt.date) -> tuple[str, str | None]:
    """resolved: one dict per candidate after redirect resolution:
    {'title', 'exists', 'ns', 'disambiguation', 'section_redirect', 'created' (date)}.
    Returns ('present', title) for exactly one valid distinct target, ('ambiguous', None),
    or ('none', None)."""
    ok = set()
    for r in resolved:
        t = r.get("title") or ""
        created = r.get("created")
        if not r.get("exists") or r.get("ns", 0) != 0 or r.get("disambiguation"):
            continue
        if r.get("section_redirect") or t.startswith("List of") or re.search(
                r"\bseason\b", t, re.I):
            continue
        if not isinstance(created, dt.date) or created < onset - dt.timedelta(days=2):
            continue
        ok.add(t)
    if len(ok) == 1:
        return "present", ok.pop()
    return ("ambiguous", None) if ok else ("none", None)


def pageview_url(title: str, start: dt.date, end: dt.date) -> str:
    """Per-article daily, English Wikipedia, user agent only (E2b: never a top list)."""
    from urllib.parse import quote
    t = quote(title.replace(" ", "_"), safe="")
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/"
           f"all-access/user/{t}/daily/{start:%Y%m%d}/{end:%Y%m%d}")
    if "/top/" in url or "/per-article/en.wikipedia/" not in url:
        raise ValueError("E2b: only English per-article pageviews")
    return url


def attention_from_views(daily: dict, onset: dt.date) -> tuple[str, dt.date | None]:
    """'present' with the earliest day in [onset, onset+30] with views >= 1000, else 'absent'."""
    for k in range(0, PAGEVIEW_DAYS[1] + 1):
        day = onset + dt.timedelta(days=k)
        if (daily.get(day) or 0) >= ATTENTION_MIN_VIEWS:
            return "present", day
    return "absent", None


# --- §8 aggregates that may be committed -------------------------------------------------
def safe_aggregate(cards: list[dict]) -> dict:
    """Counts by month x hazard x stage x rung status. EU27 CEMS records never enter cards
    (build_nodes), and EU27 cards show CEMS 'withheld', so no count can reveal E1 drops."""
    out: dict = defaultdict(int)
    for c in cards:
        m = (c["onset"] or "none")[:7]
        out[f"{m}|{c['hazard']}|stage{c['stage']}"] += 1
        for rung, s in c["rungs"].items():
            out[f"{m}|{c['hazard']}|{rung}={s}"] += 1
    return dict(sorted(out.items()))


# --- §9 H3 stream test (registered; scored on or after 2027-08-01) ------------------------
H3_ONSET = (dt.date(2026, 12, 1), dt.date(2027, 5, 31))
H3_MIN_N = 20
H3_ALPHA = 0.05


def h3_unit(card: dict) -> dict | None:
    """Population member (or None) with its measurability flag. Population: natural-hazard
    components with a decision record, onset in the window, no EU27 country."""
    if card["eu27"] or card["t_decision"] is None or card["hazard"] not in HAZARDS:
        return None
    on = card["onset"]
    if on is None:
        on = card["t_decision"]
    day = dt.date.fromisoformat(on[:10])
    if not (H3_ONSET[0] <= day <= H3_ONSET[1]):
        return None
    lag = card["lag_onset_decision_days"]
    measurable = bool(card["anchored"] and lag is not None and -3 <= lag <= WINDOW_DAYS["D"])
    return {"measurable": measurable, "cluster": (tuple(card["iso3"]), card["hazard"],
                                                    day.strftime("%Y-%m"))}


def cp_bounds(k: int, n: int, alpha: float = H3_ALPHA) -> tuple[float, float]:
    """One-sided Clopper-Pearson lower and upper bounds at level 1 - alpha."""
    from scipy.stats import beta
    lo = 0.0 if k == 0 else float(beta.ppf(alpha, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha, k + 1, n - k))
    return lo, hi


def h3_score(units: list[dict]) -> dict:
    n = len(units)
    k = sum(u["measurable"] for u in units)
    first_of: dict = {}
    for u in units:                                  # one unit per cluster, earliest listed
        first_of.setdefault(u["cluster"], u)
    nc, kc = len(first_of), sum(u["measurable"] for u in first_of.values())
    if n < H3_MIN_N or nc < H3_MIN_N:
        verdict = "not testable at this size"
        lo = hi = loc = None
    else:
        lo, hi = cp_bounds(k, n)
        loc, _ = cp_bounds(kc, nc)
        if lo > 0.5 and loc > 0.5:
            verdict = "PASS"
        elif hi < 0.5:
            verdict = "FAIL"
        else:
            verdict = "not decided at this size"
    return {"n": n, "k": k, "n_clusters": nc, "k_clusters": kc, "lower": lo, "upper": hi,
            "lower_clusters": loc, "verdict": verdict}
