"""Field-presence aggregate (docs/FIELD_PRESENCE_CHECK.md; LOOP_CARD_PROTOCOL §10).

Runs only inside the GitHub Action that holds EMO_STREAM_KEY. Returns shares (rounded down
to 0.05, groups of >= 20 records only) and schema key names; never values, identifiers,
dates, titles or record counts. CEMS records naming an EU27 country are skipped before any
other key is looked at.
"""

from __future__ import annotations

import math
import re

from emo.stream.cards import (
    HAZARDS,
    _coords,
    _f,
    glide_key,
    hazard_from_text,
    iso3_set,
    parse_time,
)
from emo.stream.exclusions import _is_eu27

PRESENCE_VERSION = "presence-0.1"
MIN_GROUP = 20
STEP = 0.05
KEY_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{2,40}$")
ALERTS = {"green", "yellow", "orange", "red"}


def _t(v) -> bool:
    return parse_time(v)[0] is not None


def _event_id(v) -> bool:
    e = v.get("id") if isinstance(v, dict) else v
    return e is not None and str(e).strip() != ""


CHECKS = {
    "time": _t,
    "iso3": lambda v: bool(iso3_set(v)),
    "glide": lambda v: glide_key(v) is not None,
    "hazard_text": lambda v: hazard_from_text(v) is not None,
    "hazard_code": lambda v: str(v) in HAZARDS,
    "alert": lambda v: str(v).lower() in ALERTS,
    "number": lambda v: _f(v) is not None,
    "atype": lambda v: v in (0, 1) and not isinstance(v, bool),
    "id": lambda v: str(v).strip() != "",
    "event_ref": _event_id,
    "text": lambda v: isinstance(v, str) and v.strip() != "",
}

# group -> [(field path, check)]; "p." = under `properties`; "coords" = geometry coordinates.
FIELDS = {
    "gdacs/search": [("p.eventid", "id"), ("p.eventtype", "hazard_code"), ("p.alertlevel", "alert"),
                     ("p.fromdate", "time"), ("p.todate", "time"), ("p.glide", "glide"),
                     ("p.iso3", "iso3"), ("p.affectedcountries", "iso3"), ("p.eventname", "text"),
                     ("p.country", "text"), ("coords", "coords")],
    "gdacs/events4app": [("p.eventid", "id"), ("p.eventtype", "hazard_code"),
                         ("p.alertlevel", "alert"), ("p.fromdate", "time"), ("p.todate", "time"),
                         ("p.glide", "glide"), ("p.iso3", "iso3"),
                         ("p.affectedcountries", "iso3"), ("coords", "coords")],
    "usgs/comcat": [("id", "id"), ("p.time", "time"), ("p.alert", "alert"), ("coords", "coords")],
    "usgs/detail": [("id", "id"), ("p.alert", "alert")],
    "cems": [("code", "id"), ("countries", "iso3"), ("gdacsId", "id"), ("category", "hazard_text"),
             ("subCategory", "hazard_text"), ("eventTime", "time"), ("activationTime", "time")],
    "ifrc_go/event": [("id", "id"), ("glide", "glide"), ("created_at", "time"),
                      ("disaster_start_date", "time"), ("dtype", "hazard_text"),
                      ("dtype_name", "hazard_text"), ("countries", "iso3")],
    "ifrc_go/appeal": [("id", "id"), ("event", "event_ref"), ("atype", "atype"),
                       ("start_date", "time"), ("end_date", "time"), ("created_at", "time"),
                       ("amount_funded", "number"), ("amount_requested", "number"),
                       ("country", "iso3"), ("dtype", "hazard_text"), ("dtype_name", "hazard_text")],
}


def _get(rec: dict, path: str):
    if path == "coords":
        return _coords(rec)
    if path.startswith("p."):
        return (rec.get("properties") or {}).get(path[2:])
    return rec.get(path)


def _has(v) -> bool:
    return v not in (None, "", [], {})


def _group(source: str, rec: dict) -> str | None:
    feed = str(rec.get("_emo_feed", ""))
    if source == "gdacs":
        return f"gdacs/{feed}" if feed in ("search", "events4app") else None
    if source == "usgs":
        return f"usgs/{feed}" if feed in ("comcat", "detail") else None
    if source == "cems":
        return "cems"
    if source == "ifrc_go":
        if feed == "event":
            return "ifrc_go/event"
        return "ifrc_go/appeal" if feed.startswith("appeal") else None
    return None


def _node_key(group: str, rec: dict, i: int) -> str:
    p = rec.get("properties") or {}
    if group.startswith("gdacs"):
        t, e = p.get("eventtype"), p.get("eventid")
        return f"{t}|{e}" if t is not None and e is not None else f"row|{i}"
    k = rec.get("code") if group == "cems" else rec.get("id")
    return str(k) if k is not None else f"row|{i}"


def latest_records(runs: list[dict]) -> dict[str, list[dict]]:
    """group -> latest snapshot per node key. EU27 CEMS dropped before anything else."""
    latest: dict[tuple[str, str], dict] = {}
    i = 0
    for run in runs:
        for source, s in (run.get("sources") or {}).items():
            for rec in s.get("records") or []:
                i += 1
                if not isinstance(rec, dict):
                    continue
                if source == "cems" and _is_eu27(rec.get("countries")):
                    continue                              # E1 / §2: never read further
                g = _group(source, rec)
                if g is None:
                    continue
                key = (g, _node_key(g, rec, i))
                old = latest.get(key)
                if old is None or str(rec.get("_emo_fetched_at", "")) >= str(
                        old.get("_emo_fetched_at", "")):
                    latest[key] = rec
    out: dict[str, list[dict]] = {g: [] for g in FIELDS}
    for (g, _), rec in latest.items():
        out[g].append(rec)
    return out


def _floor(x: float) -> float:
    return round(math.floor(x / STEP + 1e-9) * STEP, 2)


def _key_names(recs: list[dict]) -> dict[str, float]:
    names: dict[str, int] = {}
    for r in recs:
        keys = {k for k in r if not k.startswith("_emo")}
        keys |= {f"properties.{k}" for k in (r.get("properties") or {})} if isinstance(
            r.get("properties"), dict) else set()
        for k in keys:
            leaf = k.split(".")[-1]
            if not KEY_NAME.match(leaf) or (leaf.isupper() and len(leaf) <= 3):
                continue
            names[k] = names.get(k, 0) + 1
    return {k: _floor(c / len(recs)) for k, c in sorted(names.items())
            if _floor(c / len(recs)) >= STEP}


def presence(runs: list[dict]) -> dict:
    groups = latest_records(runs)
    out: dict = {}
    for g, fields in FIELDS.items():
        recs = groups.get(g, [])
        if len(recs) < MIN_GROUP:
            out[g] = "n<20"
            continue
        res = {}
        for path, check in fields:
            vals = [_get(r, path) for r in recs]
            pres = sum(_has(v) for v in vals)
            if check == "coords":
                ok = pres
            else:
                ok = 0
                for v in vals:
                    try:
                        ok += bool(_has(v) and CHECKS[check](v))
                    except Exception:  # noqa: BLE001 - unparseable counts as not parsing
                        pass
            res[path] = {"present": _floor(pres / len(recs)), "parses": _floor(ok / len(recs))}
        out[g] = {"fields": res, "key_names": _key_names(recs)}
    return out


def verdicts(agg: dict) -> dict:
    """§3 decision rule of FIELD_PRESENCE_CHECK.md, per group and field."""
    out: dict = {}
    for g, v in agg.items():
        if not isinstance(v, dict):
            continue
        for path, s in v["fields"].items():
            if s["parses"] >= 0.5:
                verdict = "reads"
            elif s["present"] == 0:
                verdict = "wrong name"
            elif g == "cems" and path == "countries" and s["present"] >= 0.5:
                verdict = "names: CEMS table"
            else:
                verdict = "recorded, not changed"
            out[f"{g}:{path}"] = verdict
    return out
