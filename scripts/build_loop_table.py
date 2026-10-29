"""Build the hurricane-loop event table from the committed source extracts (session 2.4).

docs/LOOP_PROTOCOL.md §2-§3 with amendments 4-6 and the build rules of §16. One row per event
(set HU+TS), one column group per link: ev_ (event, severity controls, HU-only flag),
dc_ (decide-act, FEMA), pr_ (predict, F), at_ (attend, A), wn_ (warnings, W).
Writes data/loop_hurricanes/{loop_events.csv, decide_records.csv, predict_lines.csv,
exclusions.csv, summary.json}. Computes no lag correlation, trend, link-to-link statistic,
H3, H4 or H5 statistic (§16 rule 9). Run from the repository root:
    python scripts/build_loop_table.py [--out DIR]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from emo import loop_hurricanes as lh  # noqa: E402

DATA = ROOT / "data" / "loop_hurricanes"
SRC = DATA / "sources"

COLUMNS = [
    # event
    "ev_atcf", "ev_name", "ev_season", "ev_t0_utc", "ev_state", "ev_hurdat2_line", "ev_status_t0",
    "ev_V_kt", "ev_pmin_mb", "ev_R64_nmi", "ev_R64_missing_replaced", "ev_landfall_dist_km",
    "ev_n_us_landfalls", "ev_hu_set", "ev_hu_t0_utc", "ev_hu_state",
    # decide-act
    "dc_status", "dc_name_rule", "dc_dr_number", "dc_dr_string", "dc_dr_declaration_date",
    "dc_dr_request_date", "dc_region", "dc_Y_state_days", "dc_Y_fed_days", "dc_n_dr_matched",
    "dc_em_numbers", "dc_em_declaration_date", "dc_em_request_date", "dc_EMpre", "dc_incident_types",
    "dc_type_routes", "dc_dr_type_hu_only", "dc_dr_em_incidentid_differ",
    # predict
    "pr_F", "pr_F_intensity", "pr_n_lines", "pr_ess48",
    # attend
    "at_target", "at_rule", "at_via", "at_created_utc", "at_views_3d", "at_A", "at_wiki_file",
    # warnings
    "wn_advisory_file", "wn_issued_utc", "wn_codes", "wn_W_hours",
    # exclusions
    "exclusions",
]


def fmt(x: object) -> str:
    if x is None:
        return ""
    if isinstance(x, float):
        return f"{x:.6g}"
    if isinstance(x, dt.datetime):
        return x.strftime("%Y-%m-%dT%H:%MZ")
    if isinstance(x, dt.date):
        return x.isoformat()
    return str(x)


def read_csv(p: Path) -> list[dict[str, str]]:
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def lines_csv(p: Path) -> list[tuple[int, str]]:
    return [(int(r["line"]), r["text"]) for r in read_csv(p)]


def build() -> dict[str, object]:
    storms = lh.parse_hurdat2(lines_csv(SRC / "hurdat2_2015_2025.csv"))
    lfs = lh.read_landfalls(SRC / "landfall_states.csv")
    events = read_csv(SRC / "events.csv")
    fema = read_csv(SRC / "fema_qualifying.csv")
    errs = lh.parse_error_lines(lines_csv(SRC / "nhc_errors_events.csv"))
    adeck: dict[str, list[tuple[int, str]]] = {}
    for r in read_csv(SRC / "adeck_ocd5_tau48.csv"):
        adeck.setdefault(r["atcf"], []).append((int(r["line"]), r["text"]))
    gis: dict[str, list[dict[str, str]]] = {}
    for r in read_csv(SRC / "gis_advisories.csv"):
        gis.setdefault(r["atcf"], []).append(r)
    ids = {e["atcf"] for e in events}
    qual = {s: lh.qualifying_landfalls([x for x in lfs if x.atcf == s], lh.QUAL_STATUS_HUTS) for s in ids}

    rows, drec, plines, excl = [], [], [], []
    for e in events:
        s = storms[e["atcf"]]
        q = qual[s.atcf]
        lf0 = q[0]
        rec0 = next(r for r in s.records if r.line_no == lf0.line_no)
        t0, k, d0 = lf0.time, lf0.state, lf0.time.date()
        hu = [x for x in q if x.status == "HU"]
        r64 = max(rec0.r64)
        r64_rep = int(r64 == -999 and rec0.status != "TS")
        if r64 < 0 or rec0.status == "TS":
            r64 = 0
        reasons: list[tuple[str, str]] = []
        row: dict[str, object] = {
            "ev_atcf": s.atcf, "ev_name": s.name, "ev_season": s.year, "ev_t0_utc": t0, "ev_state": k,
            "ev_hurdat2_line": lf0.line_no, "ev_status_t0": rec0.status, "ev_V_kt": rec0.wind,
            "ev_pmin_mb": rec0.pressure if rec0.pressure != -999 else None, "ev_R64_nmi": r64,
            "ev_R64_missing_replaced": r64_rep, "ev_landfall_dist_km": lf0.dist_km, "ev_n_us_landfalls": len(q),
            "ev_hu_set": int(bool(hu)), "ev_hu_t0_utc": hu[0].time if hu else None,
            "ev_hu_state": hu[0].state if hu else None,
        }
        # ---- decide-act
        others = [x.time.date() for o in ids if o != s.atcf for x in qual[o] if x.state == k]
        m = lh.match_fema(s.name, k, d0, fema, others)
        row["dc_status"] = m.status
        row["dc_name_rule"] = m.name_rule or None
        if m.status != "matched":
            reasons.append(("decide", m.reason))
        else:
            decl = lh.group_declarations(m.records)
            for r in m.records:
                drec.append([s.atcf, r["id"], r["disasterNumber"], r["declarationType"]])
            drs = sorted((x for x in decl if x.dtype == "DR"), key=lambda x: (x.decl_date, x.disaster_number))
            ems = sorted((x for x in decl if x.dtype == "EM"), key=lambda x: (x.decl_date, x.disaster_number))
            row["dc_n_dr_matched"] = len(drs)
            row["dc_incident_types"] = ";".join(sorted({t for x in decl for t in x.incident_types}))
            row["dc_type_routes"] = ";".join(sorted({t for x in decl for t in x.routes}))
            if ems:
                row["dc_em_numbers"] = ";".join(str(x.disaster_number) for x in ems)
                row["dc_em_declaration_date"] = ems[0].decl_date
                reqs = [x.request_date for x in ems if x.request_date]
                row["dc_em_request_date"] = min(reqs) if reqs else None
            row["dc_EMpre"] = int(any(x.decl_date <= d0 for x in ems))
            if not drs:
                reasons.append(("decide", "no_dr"))
            else:
                dr = drs[0]
                row["dc_dr_number"] = dr.disaster_number
                row["dc_dr_string"] = f"DR-{dr.disaster_number}-{k}"
                row["dc_dr_declaration_date"] = dr.decl_date
                row["dc_dr_request_date"] = dr.request_date
                row["dc_region"] = dr.region
                drrecs = [r for r in m.records if int(r["disasterNumber"]) == dr.disaster_number]
                row["dc_dr_type_hu_only"] = int(any(lh.type_route(r, hu_only=True) for r in drrecs))
                row["dc_dr_em_incidentid_differ"] = int(any(set(x.incident_ids) != set(dr.incident_ids) for x in ems))
                if dr.request_date is None:
                    reasons.append(("decide", "dr_request_missing"))
                else:
                    row["dc_Y_state_days"] = (dr.request_date - d0).days
                    yf = (dr.decl_date - dr.request_date).days
                    if yf < 0:
                        reasons.append(("decide", "y_fed_negative"))
                    else:
                        row["dc_Y_fed_days"] = yf
        # ---- predict
        base = lh.parse_adeck_base48(adeck.get(s.atcf, []))
        sk = lh.track_skill(s, t0, errs, base)
        row["pr_F"], row["pr_F_intensity"] = sk.f, sk.f_int
        row["pr_n_lines"], row["pr_ess48"] = sk.n_lines, round(sk.ess48, 4)
        for a, b, o, bb in sk.lines:
            plines.append([s.atcf, a, b, o, f"{bb:.3f}"])
        if sk.reason:
            reasons.append(("predict", sk.reason))
        # ---- attend
        wf = SRC / "wiki" / f"{s.atcf}.json"
        if not wf.exists():
            reasons.append(("attend", "a_fetch_missing"))
        else:
            w = json.loads(wf.read_text())
            titles = w["titles"]
            target, rule, via = lh.resolve_target(w["query"]["response"], titles)
            row["at_wiki_file"] = f"sources/wiki/{s.atcf}.json"
            if not target:
                reasons.append(("attend", "a_no_article"))
            else:
                pages = w["creation"]["response"]["query"]["pages"]
                revs = pages[0].get("revisions") or []
                row["at_target"], row["at_rule"], row["at_via"] = target, rule, ";".join(via) or None
                row["at_created_utc"] = revs[0]["timestamp"] if revs else None
                series = [lh.views_by_day(w["pageviews"][t]["response"]) for t in [target, *via]]
                a_val, tot = lh.attention(d0, series)
                row["at_views_3d"], row["at_A"] = tot, a_val
        # ---- warnings
        g = gis.get(s.atcf, [])
        hit = [r for r in g if r["has_ts_hu_ww"] == "1"]
        if not g or not g[0]["file"]:
            reasons.append(("warn", "w_no_gis"))
        elif not hit:
            reasons.append(("warn", "w_no_ww"))
        else:
            h = hit[0]
            ti = lh.parse_advdate(h["advdate"])
            row["wn_advisory_file"], row["wn_codes"] = h["file"], h["tcww_codes"]
            row["wn_issued_utc"] = ti
            if ti is not None:
                row["wn_W_hours"] = round((t0 - ti).total_seconds() / 3600, 2)
        row["exclusions"] = ";".join(f"{lk}:{r}" for lk, r in reasons) or None
        for lk, r in reasons:
            excl.append([s.atcf, lk, r, lh.REASONS[r]])
        rows.append(row)
    return {"rows": rows, "decide_records": drec, "predict_lines": plines, "exclusions": excl}


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Counts only (§16 rule 9): season sizes, non-missing counts per link, complete cases per H4 pair."""
    seasons = sorted({int(r["ev_season"]) for r in rows})  # type: ignore[call-overload]

    def has(r: dict[str, object], c: str) -> bool:
        return r.get(c) not in (None, "")

    links = {"Y_state": "dc_Y_state_days", "Y_fed": "dc_Y_fed_days", "F": "pr_F", "A": "at_A", "W": "wn_W_hours",
             "EMpre": "dc_EMpre", "region": "dc_region", "V": "ev_V_kt", "R64": "ev_R64_nmi"}
    per_season = {str(y): {"events": sum(int(r["ev_season"]) == y for r in rows)} for y in seasons}  # type: ignore[call-overload]
    for y in seasons:
        for nm, c in links.items():
            per_season[str(y)][nm] = sum(has(r, c) for r in rows if int(r["ev_season"]) == y)  # type: ignore[call-overload]
    ctrl = ["ev_V_kt", "ev_R64_nmi", "dc_region", "dc_EMpre"]
    pairs = {}
    for x in ("F", "W", "A"):
        for yv in ("Y_state", "Y_fed"):
            cc = [r for r in rows if all(has(r, c) for c in [links[x], links[yv], *ctrl])]
            pairs[f"{x}~{yv}"] = {str(y): sum(int(r["ev_season"]) == y for r in cc) for y in seasons}  # type: ignore[call-overload]
    return {
        "event_set": "HU+TS", "seasons": [int(s) for s in seasons], "events": len(rows),
        "hu_only_events": sum(int(r["ev_hu_set"]) for r in rows),  # type: ignore[call-overload]
        "non_missing": {nm: sum(has(r, c) for r in rows) for nm, c in links.items()},
        "both_lags": sum(has(r, "dc_Y_state_days") and has(r, "dc_Y_fed_days") for r in rows),
        "per_season": per_season,
        "complete_cases_by_season_per_pair": pairs,
        "note": "counts only; no lag correlation, trend, link-to-link, H3, H4 or H5 statistic",
    }


def write(out: Path, b: dict[str, object]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    rows = b["rows"]
    with open(out / "loop_events.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(COLUMNS)
        for r in rows:  # type: ignore[attr-defined]
            w.writerow([fmt(r.get(c)) for c in COLUMNS])
    for name, head in (("decide_records", ["atcf", "fema_id", "disasterNumber", "declarationType"]),
                       ("predict_lines", ["atcf", "error_file_line", "adeck_line", "ofcl48_nmi", "ocd5_48_nmi"]),
                       ("exclusions", ["atcf", "link", "reason", "text"])):
        with open(out / f"{name}.csv", "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(head)
            w.writerows(b[name])  # type: ignore[arg-type]
    (out / "summary.json").write_text(json.dumps(summary(rows), indent=1, sort_keys=True) + "\n")  # type: ignore[arg-type]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DATA))
    write(Path(ap.parse_args().out), build())
