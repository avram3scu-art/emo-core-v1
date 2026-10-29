"""Monthly counts of events and linked events, from the stream log only (infrastructure).

Reads only identifiers, dates, countries and explicit link keys. No outcome field
(alert level, losses, funding, lags) is read. CEMS activations in any EU27 country are left
out of every count, whatever their hazard, so that no count can reveal what E1 removed.

Linked event (docs/STREAM_DATA.md §4): a GDACS event with at least one decision record,
joined by explicit keys only (§3 rule 1-2; the fallback rule waits for the 3.3 protocol):
  CEMS gdacsId == GDACS eventid, or GLIDE equal between the GDACS event and an IFRC GO
  event that has at least one appeal (DREF or Emergency Appeal) in the log.
"""
from __future__ import annotations

import datetime as dt
from collections import Counter, defaultdict

from emo.stream.exclusions import _is_eu27


def _month(value) -> str | None:
    if isinstance(value, (int, float)):        # USGS: ms since epoch
        return dt.datetime.fromtimestamp(value / 1000, dt.UTC).strftime("%Y-%m")
    if isinstance(value, str) and len(value) >= 7 and value[4] == "-":
        return value[:7]
    return None


def _event_id(appeal: dict):
    e = appeal.get("event")
    return e.get("id") if isinstance(e, dict) else e


def monthly_counts(runs: list[dict]) -> dict:
    gdacs: dict = {}
    usgs: dict = {}
    cems: dict = {}
    go_events: dict = {}
    go_appeals: dict = {}
    for run in runs:
        src = run["sources"]
        for f in src.get("gdacs", {}).get("records", []):
            p = f.get("properties") or {}
            if p.get("eventid") is not None:
                gdacs[(p.get("eventtype"), str(p["eventid"]))] = p
        for f in src.get("usgs", {}).get("records", []):
            if f.get("_emo_feed") == "comcat" and f.get("id"):
                usgs[f["id"]] = (f.get("properties") or {}).get("time")
        for r in src.get("cems", {}).get("records", []):
            if r.get("code") and not _is_eu27(r.get("countries")):
                cems[r["code"]] = r
        for r in src.get("ifrc_go", {}).get("records", []):
            if r.get("_emo_feed") == "event" and r.get("id") is not None:
                go_events[r["id"]] = r
            elif str(r.get("_emo_feed", "")).startswith("appeal") and r.get("id") is not None:
                go_appeals[r["id"]] = r

    out: dict = defaultdict(Counter)
    for p in gdacs.values():
        out[_month(p.get("fromdate"))]["gdacs_events"] += 1
    for t in usgs.values():
        out[_month(t)]["usgs_m4_5_events"] += 1
    for r in cems.values():
        out[_month(r.get("activationTime"))]["cems_activations_non_eu27"] += 1
    for r in go_events.values():
        out[_month(r.get("disaster_start_date"))]["ifrc_go_events"] += 1
    for r in go_appeals.values():
        kind = {0: "dref", 1: "emergency_appeal"}.get(r.get("atype"), "other_appeal")
        out[_month(r.get("start_date"))][f"ifrc_{kind}"] += 1

    cems_gdacs = {str(r.get("gdacsId")) for r in cems.values() if r.get("gdacsId")}
    events_with_appeal = {_event_id(a) for a in go_appeals.values()}
    appeal_glides = {str(e.get("glide")).strip() for i, e in go_events.items()
                     if i in events_with_appeal and e.get("glide")}
    for (_, eid), p in gdacs.items():
        glide = str(p.get("glide") or "").strip()
        if eid in cems_gdacs or (glide and glide in appeal_glides):
            out[_month(p.get("fromdate"))]["linked_events_explicit_keys"] += 1
    return {m: dict(c) for m, c in sorted(out.items(), key=lambda kv: str(kv[0]))}
