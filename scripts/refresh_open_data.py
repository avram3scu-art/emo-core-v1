"""Refresh the open data files in data/ from their public sources.

Sources (all open licences, see data/README_*.md):
  - Our World in Data grapher CSVs: CO2 emissions, ozone-depleting substances,
    ODA as share of GNI, UCDP conflict death rate (CC BY 4.0)
  - OpenAlex group_by counts used for the co-authorship share (CC0)

Safety rules, in order:
  1. A downloaded file replaces the committed one only if it passes validation:
     identical column header (OWID) or a non-empty year/country grouping
     (OpenAlex), and it keeps at least 95 % of the committed (Entity, Year)
     rows or group keys. A source that fails keeps its committed file and is
     reported as failed; it never silently changes a series' definition.
  2. Files are rewritten only when their content changed.
  3. Manually transcribed or hand-coded files (NHC, DAC events, the RDL
     forecast ledger) are never touched here.

Each series lives in its own folder, data/sources/<name>/<name>.<ext>.
Writes data/MANIFEST.json (folder path, source URL, download date, sha256, row
count, changed flag, status) and prints one JSON status line for the weekly runner.

Optional environment: OPENALEX_API_KEY, OPENALEX_MAILTO.
Run from the repository root: python scripts/refresh_open_data.py
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
UA = "emo-core-v1 weekly open-data refresh (+https://github.com/avram3scu-art/emo-core-v1)"
MIN_RETAINED = 0.95

OWID = {
    "owid_annual_co2_emissions.csv": "annual-co2-emissions-per-country",
    "owid_ozone_depleting_substance_consumption.csv": "ozone-depleting-substance-consumption",
    "owid_foreign_aid_share_of_gni.csv": "foreign-aid-given-as-a-share-of-national-income",
    "owid_ucdp_death_rate_armed_conflicts.csv": "death-rate-in-armed-conflicts",
}
OWID_URL = "https://ourworldindata.org/grapher/{slug}.csv?v=1&csvType=full&useColumnShortNames=false"

_EXCL = "authorships.countries:!CN,authorships.countries:!ID,"
OPENALEX = {
    "openalex_articles_multicountry_by_year.json":
        "filter=countries_distinct_count:>1,type:article&group_by=publication_year",
    "openalex_articles_anycountry_by_year.json":
        "filter=countries_distinct_count:>0,type:article&group_by=publication_year",
    "openalex_articles_multicountry_by_year_excl_CN_ID.json":
        f"filter={_EXCL}countries_distinct_count:>1,type:article&group_by=publication_year",
    "openalex_articles_anycountry_by_year_excl_CN_ID.json":
        f"filter={_EXCL}countries_distinct_count:>0,type:article&group_by=publication_year",
    "openalex_single_country_2020_by_country.json":
        "filter=countries_distinct_count:1,publication_year:2020,type:article&group_by=authorships.countries",
    "openalex_single_country_2025_by_country.json":
        "filter=countries_distinct_count:1,publication_year:2025,type:article&group_by=authorships.countries",
}
OPENALEX_URL = "https://api.openalex.org/works?{query}"

# NHC HURDAT2 Atlantic best track, pinned file (GWI test events, docs/GWI_PROTOCOL.md §2)
HURDAT2 = {"hurdat2_atlantic.txt": "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2025-092326.txt"}


def path_for(fname: str) -> Path:
    """Each download keeps its own folder: data/sources/<stem>/<fname>."""
    return DATA / "sources" / Path(fname).stem / fname


def _get(url: str, tries: int = 4) -> requests.Response:
    last: Exception | None = None
    for i in range(tries):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=120)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {r.status_code}", response=r)
            r.raise_for_status()
            return r
        except requests.RequestException as exc:
            last = exc
            time.sleep(float(os.environ.get("EMO_RETRY_WAIT", 10)) * (i + 1))
    raise RuntimeError(f"{url}: {last}")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _owid_check(old: bytes, new: bytes) -> tuple[int, str | None]:
    o = list(csv.reader(io.StringIO(old.decode("utf-8-sig"))))
    n = list(csv.reader(io.StringIO(new.decode("utf-8-sig"))))
    if not n or n[0] != o[0]:
        return len(n) - 1, f"header changed: {n[0] if n else None} != {o[0]}"
    ko = {(r[0], r[2]) for r in o[1:] if len(r) > 2}
    kn = {(r[0], r[2]) for r in n[1:] if len(r) > 2}
    kept = len(ko & kn) / max(len(ko), 1)
    if kept < MIN_RETAINED:
        return len(kn), f"only {kept:.1%} of committed (Entity, Year) rows retained"
    return len(kn), None


def _groups(payload: dict) -> dict[str, int]:
    return {str(g["key"]): int(g["count"]) for g in payload.get("group_by", [])}


def _openalex_check(old: dict, new: dict) -> tuple[int, str | None]:
    go, gn = _groups(old), _groups(new)
    if not gn:
        return 0, "no group_by results"
    kept = len(set(go) & set(gn)) / max(len(go), 1)
    if kept < MIN_RETAINED:
        return len(gn), f"only {kept:.1%} of committed group keys retained"
    return len(gn), None


# Wikipedia pageviews for the GWI test (docs/GWI_PROTOCOL.md §3). Fixed range for reproducibility.
PV_LANGS = ["en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "ja", "zh", "ko"]
PV_SETS = {"test": "Tropical cyclone", "placebo": "Photosynthesis"}
PV_FILE = "wikipedia_pageviews_gwi.csv"
PV_RANGE = ("20151101", "20251231")
LANGLINKS_URL = ("https://en.wikipedia.org/w/api.php?action=query&prop=langlinks&lllimit=500"
                 "&format=json&formatversion=2&titles={title}")
PV_URL = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{lang}.wikipedia/"
          "all-access/user/{title}/daily/{start}/{end}")


def _pageviews_csv() -> tuple[bytes, int]:
    from urllib.parse import quote

    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["set", "lang", "title", "date", "views"])
    rows = 0
    for which, en_title in PV_SETS.items():
        page = _get(LANGLINKS_URL.format(title=quote(en_title))).json()["query"]["pages"][0]
        titles = {"en": en_title} | {ll["lang"]: ll["title"] for ll in page.get("langlinks", [])}
        missing = [lg for lg in PV_LANGS if lg not in titles]
        if missing:
            raise RuntimeError(f"{which}: no interlanguage link for {missing}")
        for lg in PV_LANGS:
            t = titles[lg].replace(" ", "_")
            url = PV_URL.format(lang=lg, title=quote(t, safe=""), start=PV_RANGE[0], end=PV_RANGE[1])
            items = _get(url).json().get("items", [])
            if not items:
                raise RuntimeError(f"{which}/{lg}: no pageview items")
            for it in items:
                d = str(it["timestamp"])[:8]
                w.writerow([which, lg, titles[lg], f"{d[:4]}-{d[4:6]}-{d[6:]}", int(it["views"])])
                rows += 1
    return out.getvalue().encode(), rows


def _hurdat_check(new: bytes) -> tuple[int, str | None]:
    lines = new.decode("utf-8", "replace").splitlines()
    storms = [ln for ln in lines if ln.startswith("AL") and len(ln.split(",")[0].strip()) == 8]
    if not storms or not any(s.split(",")[0].strip().endswith("2025") for s in storms):
        return len(storms), "no storm headers, or no 2025 storms"
    return len(storms), None


def refresh() -> dict:
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    man_path = DATA / "MANIFEST.json"
    manifest = json.loads(man_path.read_text()) if man_path.exists() else {}
    report = []

    for fname, slug in OWID.items():
        url = OWID_URL.format(slug=slug)
        path = path_for(fname)
        entry = {"file": fname, "path": str(path.relative_to(DATA.parent)), "source": url, "kind": "owid"}
        try:
            new = _get(url).content
            old = path.read_bytes()
            rows, problem = _owid_check(old, new)
            if problem:
                entry.update(status="failed", detail=problem, changed=False)
            else:
                changed = new != old
                if changed:
                    path.write_bytes(new)
                entry.update(status="ok", changed=changed, rows=rows, sha256=_sha(new))
        except Exception as exc:  # network, parse
            entry.update(status="failed", detail=str(exc)[:300], changed=False)
        report.append(entry)

    key, mailto = os.environ.get("OPENALEX_API_KEY"), os.environ.get("OPENALEX_MAILTO")
    for fname, query in OPENALEX.items():
        q = query + (f"&api_key={key}" if key else "") + (f"&mailto={mailto}" if mailto else "")
        path = path_for(fname)
        entry = {"file": fname, "path": str(path.relative_to(DATA.parent)), "source": OPENALEX_URL.format(query=query), "kind": "openalex"}
        try:
            payload = _get(OPENALEX_URL.format(query=q)).json()
            payload.get("meta", {}).pop("notice", None)  # per-request text, not data
            old = json.loads(path.read_text())
            rows, problem = _openalex_check(old, payload)
            if problem:
                entry.update(status="failed", detail=problem, changed=False)
            else:
                changed = _groups(payload) != _groups(old)
                if changed:
                    path.write_text(json.dumps(payload))
                blob = json.dumps(sorted(_groups(payload).items())).encode()
                entry.update(status="ok", changed=changed, rows=rows, sha256=_sha(blob))
        except Exception as exc:
            detail = str(exc)
            for secret in (key, mailto):
                if secret:
                    detail = detail.replace(secret, "***")
            entry.update(status="failed", detail=detail[:300], changed=False)
        report.append(entry)

    for fname, url in HURDAT2.items():
        path = path_for(fname)
        entry = {"file": fname, "path": str(path.relative_to(DATA.parent)), "source": url, "kind": "hurdat2"}
        try:
            new = _get(url).content
            rows, problem = _hurdat_check(new)
            old = path.read_bytes() if path.exists() else None
            if problem:
                entry.update(status="failed", detail=problem, changed=False)
            else:
                changed = new != old
                if changed:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(new)
                entry.update(status="ok", changed=changed, rows=rows, sha256=_sha(new))
        except Exception as exc:
            entry.update(status="failed", detail=str(exc)[:300], changed=False)
        report.append(entry)

    path = path_for(PV_FILE)
    entry = {"file": PV_FILE, "path": str(path.relative_to(DATA.parent)),
             "source": PV_URL.format(lang="<lang>", title="<title>", start=PV_RANGE[0], end=PV_RANGE[1])
             + " ; titles via " + LANGLINKS_URL.format(title="<en title>"), "kind": "wikipedia_pageviews"}
    try:
        new, rows = _pageviews_csv()
        old = path.read_bytes() if path.exists() else None
        changed = new != old
        if changed:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(new)
        entry.update(status="ok", changed=changed, rows=rows, sha256=_sha(new))
    except Exception as exc:
        entry.update(status="failed", detail=str(exc)[:300], changed=False)
    report.append(entry)

    for e in report:
        prev = manifest.get(e["file"], {})
        if e["status"] == "ok":
            e["downloaded_at"] = now
            e["last_changed_at"] = now if e["changed"] else prev.get("last_changed_at", "2026-10-20 (initial download)")
        else:
            e["downloaded_at"] = prev.get("downloaded_at", prev.get("retrieved_at", "2026-10-20 (initial download)"))
            e["last_changed_at"] = prev.get("last_changed_at", "2026-10-20 (initial download)")
            e["last_attempt_at"] = now
        manifest[e["file"]] = {k: v for k, v in e.items() if k != "file"}
    man_path.write_text(json.dumps(dict(sorted(manifest.items())), indent=2) + "\n")
    return {"run_at": now, "sources": report}


if __name__ == "__main__":
    result = refresh()
    print(json.dumps(result))
    sys.exit(0)
