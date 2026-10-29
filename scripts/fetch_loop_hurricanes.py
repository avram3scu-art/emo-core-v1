"""Fetch the hurricane-loop sources (docs/LOOP_PROTOCOL.md §16 rule 1) except Wikimedia.

Steps (run in order from the repository root; each writes committed extracts under
data/loop_hurricanes/sources/ and records URL, access time and SHA-256 in
data/loop_hurricanes/MANIFEST.json; full downloads stay in .cache/loop_hurricanes/):

  python scripts/fetch_loop_hurricanes.py hurdat2   # HURDAT2 extract, seasons 2015-2025
  python scripts/fetch_loop_hurricanes.py census    # Census states; landfall_states.csv, events.csv
  python scripts/fetch_loop_hurricanes.py errors    # NHC error-file lines of the event storms
  python scripts/fetch_loop_hurricanes.py adeck     # ATCF a-deck OCD5 TAU-48 lines of the event storms
  python scripts/fetch_loop_hurricanes.py fema      # OpenFEMA v2 DR/EM records of a qualifying type
  python scripts/fetch_loop_hurricanes.py gis       # NHC GIS advisory watch/warning summary

Wikimedia (MediaWiki API, pageviews) is fetched by scripts/fetch_loop_wiki.py in the
`loop_wiki_fetch.yml` workflow (Claude's workspace is rate-limited by Wikimedia).
"""

from __future__ import annotations

import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from emo import loop_hurricanes as lh  # noqa: E402

OUT = ROOT / "data" / "loop_hurricanes"
SRC = OUT / "sources"
CACHE = ROOT / ".cache" / "loop_hurricanes"
MANIFEST = OUT / "MANIFEST.json"

HURDAT2_URL = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2025-092326.txt"
CENSUS_URL = "https://www2.census.gov/geo/tiger/GENZ2025/shp/cb_2025_us_state_500k.zip"
ERR_URL = "https://www.nhc.noaa.gov/verification/errors/1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt"
ADECK_URL = "https://ftp.nhc.noaa.gov/atcf/archive/{y}/aal{nn}{y}.dat.gz"
FEMA_URL = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
GIS_LIST = "https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=al{nn}&year={y}"
GIS_ZIP = "https://www.nhc.noaa.gov/gis/forecast/archive/{f}"
FEMA_FROM, FEMA_TO = "2015-01-01T00:00:00.000Z", "2026-01-10T23:59:59.999Z"


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def get(url: str, tries: int = 4) -> bytes:
    for k in range(tries):
        r = subprocess.run(["curl", "-sSfL", "-m", "300", url], capture_output=True)
        if r.returncode == 0:
            return r.stdout
        time.sleep(3 * (k + 1))
    raise RuntimeError(f"fetch failed: {url}: {r.stderr.decode()[:200]}")


def manifest_set(key: str, **kw: object) -> None:
    m = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    m[key] = kw
    MANIFEST.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")


def commit_file(rel: str, data: bytes, **kw: object) -> None:
    p = SRC / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    manifest_set(f"sources/{rel}", sha256=sha(data), bytes=len(data), **kw)


def write_lines_csv(rows: list[tuple[int, str]]) -> bytes:
    b = io.StringIO()
    w = csv.writer(b, lineterminator="\n")
    w.writerow(["line", "text"])
    w.writerows(rows)
    return b.getvalue().encode()


def read_lines_csv(path: Path) -> list[tuple[int, str]]:
    with open(path, newline="") as f:
        return [(int(r["line"]), r["text"]) for r in csv.DictReader(f)]


def events() -> list[dict[str, str]]:
    with open(SRC / "events.csv", newline="") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------ steps


def step_hurdat2() -> None:
    raw = get(HURDAT2_URL)
    acc = now()
    lines = raw.decode().splitlines()
    keep: list[tuple[int, str]] = []
    on = False
    for i, t in enumerate(lines, 1):
        if t[:2].isalpha():
            on = int(t[4:8]) in lh.SEASONS
        if on:
            keep.append((i, t))
    commit_file("hurdat2_2015_2025.csv", write_lines_csv(keep), source=HURDAT2_URL, accessed=acc,
                full_file_sha256=sha(raw), full_file_lines=len(lines),
                note="all header and data lines of storms with ATCF year 2015-2025; line = line number in the full file")


def load_census() -> list[tuple[str, list]]:
    z = CACHE / "cb_2025_us_state_500k.zip"
    if not z.exists():
        raise SystemExit("run the census step first (cache missing)")
    zf = zipfile.ZipFile(z)
    shp = zf.read("cb_2025_us_state_500k.shp")
    dbf = zf.read("cb_2025_us_state_500k.dbf")
    polys = lh.read_shapefile_polygons(shp, dbf)
    return [(a["STUSPS"], rings) for a, rings in polys if a["STUSPS"] not in lh.DROP_ENTITIES]


def step_census() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = get(CENSUS_URL)
    acc = now()
    (CACHE / "cb_2025_us_state_500k.zip").write_bytes(raw)
    prj = zipfile.ZipFile(io.BytesIO(raw)).read("cb_2025_us_state_500k.prj").decode()
    polys = load_census()
    manifest_set("cache/cb_2025_us_state_500k.zip", source=CENSUS_URL, accessed=acc, sha256=sha(raw),
                 bytes=len(raw), committed=False, prj=prj, entities=sorted(c for c, _ in polys))
    storms = lh.parse_hurdat2(read_lines_csv(SRC / "hurdat2_2015_2025.csv"))
    rows = []
    for s in storms.values():
        for r in s.records:
            if r.ident != "L":
                continue
            st, d = lh.assign_state(r.lon, r.lat, polys)
            rows.append([s.atcf, s.name, r.line_no, r.time.isoformat(), r.status, r.lat, r.lon, st, f"{d:.2f}"])
    b = io.StringIO()
    w = csv.writer(b, lineterminator="\n")
    w.writerow(["atcf", "name", "hurdat2_line", "time_utc", "status", "lat", "lon", "state", "dist_km"])
    w.writerows(rows)
    commit_file("landfall_states.csv", b.getvalue().encode(), derived_from=["sources/hurdat2_2015_2025.csv",
                "cache/cb_2025_us_state_500k.zip"], note="every HURDAT2 L record of 2015-2025; state '' = not within 50 km of a US entity")
    lfs = lh.read_landfalls(SRC / "landfall_states.csv")
    ev = []
    for s in storms.values():
        q = lh.qualifying_landfalls([x for x in lfs if x.atcf == s.atcf], lh.QUAL_STATUS_HUTS)
        if q:
            ev.append([s.atcf, s.name, s.year, q[0].time.isoformat(), q[0].state, q[0].line_no])
    ev.sort(key=lambda r: r[3])
    b = io.StringIO()
    w = csv.writer(b, lineterminator="\n")
    w.writerow(["atcf", "name", "year", "t0_utc", "state", "hurdat2_line"])
    w.writerows(ev)
    commit_file("events.csv", b.getvalue().encode(), derived_from=["sources/landfall_states.csv"],
                note="event set HU+TS (one row per storm), input of the other fetch steps")


def step_errors() -> None:
    raw = get(ERR_URL)
    acc = now()
    ids = {e["atcf"] for e in events()}
    lines = raw.decode().splitlines()
    keep = [(i, t) for i, t in enumerate(lines, 1) if i <= 12 or (len(t.split()) > 1 and t.split()[1] in ids)]
    commit_file("nhc_errors_events.csv", write_lines_csv(keep), source=ERR_URL, accessed=acc,
                full_file_sha256=sha(raw), full_file_lines=len(lines),
                note="header lines 1-12 and every line whose STMID is an event storm")


def step_adeck() -> None:
    rows: list[list[object]] = []
    files = {}
    for e in events():
        nn, y = e["atcf"][2:4], e["atcf"][4:8]
        url = ADECK_URL.format(nn=nn, y=y)
        raw = get(url)
        txt = gzip.decompress(raw).decode(errors="replace").splitlines()
        files[e["atcf"]] = {"source": url, "accessed": now(), "sha256": sha(raw), "lines": len(txt)}
        for i, t in enumerate(txt, 1):
            p = [x.strip() for x in t.split(",")]
            if len(p) > 5 and p[4] == lh.BASELINE_TECH and p[5] == "48":
                rows.append([e["atcf"], i, t])
        time.sleep(0.5)
    b = io.StringIO()
    w = csv.writer(b, lineterminator="\n")
    w.writerow(["atcf", "line", "text"])
    w.writerows(rows)
    commit_file("adeck_ocd5_tau48.csv", b.getvalue().encode(), files=files,
                note="every OCD5 TAU-48 line of the event storms' a-decks; line = line in the decompressed a-deck")


FEMA_FIELDS = ["id", "hash", "femaDeclarationString", "disasterNumber", "state", "declarationType",
               "declarationDate", "declarationRequestNumber", "declarationRequestDate", "incidentType",
               "designatedIncidentTypes", "declarationTitle", "incidentBeginDate", "incidentEndDate",
               "incidentId", "region", "fipsStateCode", "fipsCountyCode", "designatedArea", "lastRefresh"]


def step_fema() -> None:
    flt = (f"incidentBeginDate ge '{FEMA_FROM}' and incidentBeginDate le '{FEMA_TO}' and "
           "(declarationType eq 'DR' or declarationType eq 'EM')")
    allrec: list[dict] = []
    pages = []
    skip = 0
    acc = now()
    while True:
        q = {"$filter": flt, "$top": "10000", "$skip": str(skip), "$orderby": "id", "$inlinecount": "allpages"}
        url = FEMA_URL + "?" + "&".join(f"{k}={v}" for k, v in q.items()).replace(" ", "%20").replace("'", "%27")
        raw = get(url)
        d = json.loads(raw)
        recs = d["DisasterDeclarationsSummaries"]
        pages.append({"url": url, "sha256": sha(raw), "records": len(recs), "count": d["metadata"]["count"]})
        allrec += recs
        skip += len(recs)
        if not recs or skip >= d["metadata"]["count"]:
            break
    keep = [r for r in allrec if lh.type_route({k: (r.get(k) or "") for k in r}, hu_only=False)]
    b = io.StringIO()
    w = csv.DictWriter(b, FEMA_FIELDS, lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    for r in sorted(keep, key=lambda r: (r["disasterNumber"], r["id"])):
        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in FEMA_FIELDS})
    commit_file("fema_qualifying.csv", b.getvalue().encode(), source=FEMA_URL, accessed=acc, pages=pages,
                records_fetched=len(allrec), records_kept=len(keep),
                note="DR/EM records with incident begin 2015-01-01..2026-01-10 whose type qualifies for set HU+TS (amendment 5)")


def step_gis() -> None:
    rows: list[list[object]] = []
    for e in events():
        nn, y = e["atcf"][2:4].lower(), e["atcf"][4:8]
        html = get(GIS_LIST.format(nn=nn, y=y)).decode(errors="replace")
        files = list(dict.fromkeys(re.findall(rf"forecast/archive/(al{nn}{y}_5day_\d{{3}}A?\.zip)", html)))
        if not files:
            rows.append([e["atcf"], "", "", "", "", "", 0, "no_files_listed"])
            continue
        last = None
        found = False
        for f in files:
            url = GIS_ZIP.format(f=f)
            raw = get(url)
            zf = zipfile.ZipFile(io.BytesIO(raw))
            names = zf.namelist()
            ww = [n for n in names if n.endswith("_ww_wwlin.dbf")]
            pts = [n for n in names if n.endswith("_5day_pts.dbf")] or [n for n in names if n.endswith(".dbf")]
            codes: list[str] = []
            advdate = ""
            if ww:
                recs = _dbf(zf.read(ww[0]))
                codes = sorted({r.get("TCWW", "") for r in recs})
                advdate = recs[0].get("ADVDATE", "") if recs else ""
            if not advdate and pts:
                recs = _dbf(zf.read(pts[0]))
                advdate = recs[0].get("ADVDATE", "") if recs else ""
            t = lh.parse_advdate(advdate)
            if last and t and t < last:
                print(f"warning: {f} issued before the previous advisory", file=sys.stderr)
            last = t or last
            has = bool(set(codes) & lh.WW_CODES)
            rows.append([e["atcf"], f, url, sha(raw), advdate, ";".join(codes), int(has), ""])
            time.sleep(0.3)
            if has:
                found = True
                break
        if not found:
            rows[-1][-1] = "no_ww_in_listed_files"
    b = io.StringIO()
    w = csv.writer(b, lineterminator="\n")
    w.writerow(["atcf", "file", "url", "sha256", "advdate", "tcww_codes", "has_ts_hu_ww", "note"])
    w.writerows(rows)
    commit_file("gis_advisories.csv", b.getvalue().encode(), accessed=now(), source=GIS_LIST,
                note="advisory zips fetched in listing order until one with a TS/hurricane watch or warning (inclusive)")


def _dbf(b: bytes) -> list[dict[str, str]]:
    import struct
    n, hl, rl = struct.unpack("<xxxxIHH", b[:12])
    fs = []
    i = 32
    while b[i] != 0x0D:
        fs.append((b[i:i + 11].split(b"\0")[0].decode(), b[i + 16]))
        i += 32
    out = []
    for r in range(n):
        o = hl + r * rl
        if b[o:o + 1] == b"*":  # deleted record
            continue
        o += 1
        row = {}
        for name, ln in fs:
            row[name] = b[o:o + ln].decode("latin1").strip()
            o += ln
        out.append(row)
    return out


def step_wiki_manifest() -> None:
    """Record SHA-256 of the files written by the loop_wiki_fetch.yml run (argument: its run ID)."""
    run = sys.argv[sys.argv.index("wiki-manifest") + 1]
    for p in sorted((SRC / "wiki").glob("*.json")):
        b = p.read_bytes()
        d = json.loads(b)
        manifest_set(f"sources/wiki/{p.name}", sha256=sha(b), bytes=len(b), accessed=d.get("pulled_at") or d.get("accessed"),
                     source="scripts/fetch_loop_wiki.py in workflow loop_wiki_fetch.yml",
                     run=f"https://github.com/avram3scu-art/emo-core-v1/actions/runs/{run}")


STEPS = {"hurdat2": step_hurdat2, "census": step_census, "errors": step_errors, "adeck": step_adeck,
         "fema": step_fema, "gis": step_gis, "wiki-manifest": step_wiki_manifest}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a in STEPS] or [s for s in STEPS if s != "wiki-manifest"]
    for s in args:
        print("step", s, flush=True)
        STEPS[s]()
