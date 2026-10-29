"""Validate the hurricane-loop event table (session 2.4).

1. Every committed source extract matches the SHA-256 recorded in data/loop_hurricanes/MANIFEST.json.
2. Rebuilding the table from the committed extracts reproduces every output file byte for byte.
3. Every value traces to its source row: each row's event, decide, predict, attend and warning
   values are re-read from the cited source lines/records and compared.
Exit status 0 when all checks pass. Run from the repository root:
    python scripts/validate_loop_table.py
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import build_loop_table as blt  # noqa: E402

from emo import loop_hurricanes as lh  # noqa: E402

DATA = ROOT / "data" / "loop_hurricanes"
OUTPUTS = ["loop_events.csv", "decide_records.csv", "predict_lines.csv", "exclusions.csv", "summary.json"]


def check_manifest() -> list[str]:
    errs = []
    m = json.loads((DATA / "MANIFEST.json").read_text())
    for key, v in m.items():
        if not key.startswith("sources/"):
            continue
        p = DATA / key
        if not p.exists():
            errs.append(f"missing source {key}")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != v["sha256"]:
            errs.append(f"sha256 mismatch {key}")
    listed = {k for k in m if k.startswith("sources/")}
    for p in sorted((DATA / "sources").rglob("*")):
        if p.is_file() and f"sources/{p.relative_to(DATA / 'sources').as_posix()}" not in listed:
            errs.append(f"source file not in MANIFEST: {p.relative_to(DATA)}")
    return errs


def check_rebuild() -> list[str]:
    errs = []
    with tempfile.TemporaryDirectory() as td:
        blt.write(Path(td), blt.build())
        for f in OUTPUTS:
            if (Path(td) / f).read_bytes() != (DATA / f).read_bytes():
                errs.append(f"rebuild differs: {f}")
    return errs


def _close(a: str, b: float) -> bool:
    return a != "" and math.isclose(float(a), b, rel_tol=1e-5, abs_tol=1e-9)


def check_trace() -> list[str]:
    errs: list[str] = []
    src = DATA / "sources"
    h2 = dict(blt.lines_csv(src / "hurdat2_2015_2025.csv"))
    lfs = {int(r["hurdat2_line"]): r for r in blt.read_csv(src / "landfall_states.csv")}
    fema = {r["id"]: r for r in blt.read_csv(src / "fema_qualifying.csv")}
    errl = dict(blt.lines_csv(src / "nhc_errors_events.csv"))
    adk = {(r["atcf"], int(r["line"])): r["text"] for r in blt.read_csv(src / "adeck_ocd5_tau48.csv")}
    gis = blt.read_csv(src / "gis_advisories.csv")
    drec = blt.read_csv(DATA / "decide_records.csv")
    pl = blt.read_csv(DATA / "predict_lines.csv")
    storms = lh.parse_hurdat2(blt.lines_csv(src / "hurdat2_2015_2025.csv"))
    for r in blt.read_csv(DATA / "loop_events.csv"):
        a = r["ev_atcf"]
        # event
        ln = int(r["ev_hurdat2_line"])
        p = [x.strip() for x in h2[ln].split(",")]
        t = dt.datetime.strptime(p[0] + p[1], "%Y%m%d%H%M").strftime("%Y-%m-%dT%H:%MZ")
        if p[2] != "L" or t != r["ev_t0_utc"] or p[6] != r["ev_V_kt"] or p[3] != r["ev_status_t0"]:
            errs.append(f"{a}: event values do not match HURDAT2 line {ln}")
        if lfs[ln]["state"] != r["ev_state"] or lfs[ln]["atcf"] != a:
            errs.append(f"{a}: state does not match landfall_states line {ln}")
        # decide
        if r["dc_dr_number"]:
            recs = [fema[d["fema_id"]] for d in drec if d["atcf"] == a and d["disasterNumber"] == r["dc_dr_number"]]
            if not recs or any(x["state"] != r["ev_state"] or x["declarationType"] != "DR" for x in recs):
                errs.append(f"{a}: DR records missing or inconsistent")
            elif min(x["declarationDate"][:10] for x in recs) != r["dc_dr_declaration_date"]:
                errs.append(f"{a}: DR declaration date does not trace")
            else:
                req = [x["declarationRequestDate"][:10] for x in recs if x["declarationRequestDate"]]
                if (min(req) if req else "") != r["dc_dr_request_date"]:
                    errs.append(f"{a}: DR request date does not trace")
        # predict
        mine = [x for x in pl if x["atcf"] == a]
        so = sb = 0.0
        for x in mine:
            ep = errl[int(x["error_file_line"])].split()
            ap = [y.strip() for y in adk[(a, int(x["adeck_line"]))].split(",")]
            if ep[1] != a or float(ep[19]) != float(x["ofcl48_nmi"]) or ap[4] != lh.BASELINE_TECH or ap[5] != "48":
                errs.append(f"{a}: predict line {x['error_file_line']} does not trace")
            v = lh.best_position(storms[a], dt.datetime.strptime(ap[2], "%Y%m%d%H") + dt.timedelta(hours=48))
            lat = int(ap[6][:-1]) / 10 * (-1 if ap[6][-1] == "S" else 1)
            lon = int(ap[7][:-1]) / 10 * (-1 if ap[7][-1] == "W" else 1)
            if v is None or abs(lh.gc_nmi(lat, lon, v.lat, v.lon) - float(x["ocd5_48_nmi"])) > 0.001:
                errs.append(f"{a}: OCD5 error at a-deck line {x['adeck_line']} does not trace")
            so += float(x["ofcl48_nmi"])
            sb += float(x["ocd5_48_nmi"])
        if r["pr_F"] and not _close(r["pr_F"], 1 - so / sb):
            errs.append(f"{a}: F does not trace to its lines")
        # attend
        if r["at_A"]:
            w = json.loads((DATA / r["at_wiki_file"]).read_text())
            tot = sum(lh.views_by_day(w["pageviews"][t]["response"]).get(d, 0)
                      for t in [r["at_target"], *filter(None, r["at_via"].split(";"))]
                      for d in [(dt.date.fromisoformat(r["ev_t0_utc"][:10]) - dt.timedelta(days=k)).strftime("%Y%m%d")
                                for k in (1, 2, 3)])
            if str(tot) != r["at_views_3d"] or not _close(r["at_A"], math.log10(1 + tot)):
                errs.append(f"{a}: attention does not trace to its pageview records")
        # warnings
        if r["wn_advisory_file"]:
            g = [x for x in gis if x["atcf"] == a and x["file"] == r["wn_advisory_file"]]
            if not g or g[0]["has_ts_hu_ww"] != "1":
                errs.append(f"{a}: warning advisory does not trace")
            elif r["wn_issued_utc"] and lh.parse_advdate(g[0]["advdate"]).strftime("%Y-%m-%dT%H:%MZ") != r["wn_issued_utc"]:  # type: ignore[union-attr]
                errs.append(f"{a}: issuance time does not trace")
    return errs


def main() -> int:
    errs = check_manifest() + check_rebuild() + check_trace()
    for e in errs:
        print("FAIL", e)
    n = len(blt.read_csv(DATA / "loop_events.csv"))
    print(f"validate_loop_table: rows={n} failures={len(errs)}")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
