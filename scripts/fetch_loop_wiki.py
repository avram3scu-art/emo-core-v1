"""Fetch the attend link of the hurricane loop (docs/LOOP_PROTOCOL.md §3.3, §16 rule 6).

For every event in data/loop_hurricanes/sources/events.csv: one MediaWiki query on en.wikipedia
resolving the candidate titles T1-T3 (redirects, existence, disambiguation), the target's
earliest revision timestamp, and Wikimedia per-article daily user pageviews (all-access) of the
target and of every candidate title that redirects to it, for the three UTC days before date(t0).
Also saves the API's own help for the modules used (documentation, §17).

Runs in the `loop_wiki_fetch.yml` workflow (Wikimedia rate-limits Claude's workspace).
Writes data/loop_hurricanes/sources/wiki/<ATCF>.json and api_help.json; standard library only.
Run from the repository root: python scripts/fetch_loop_wiki.py
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from emo import loop_hurricanes as lh  # noqa: E402

OUT = ROOT / "data" / "loop_hurricanes" / "sources" / "wiki"
UA = "EMO-research/2.4 (https://github.com/avram3scu-art/emo-core-v1; avram3scu@gmail.com)"
API = "https://en.wikipedia.org/w/api.php"
PV = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/"
      "all-access/user/{title}/daily/{start}/{end}")


def get(url: str) -> tuple[int, bytes]:
    for k in range(6):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, e.read()
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(5 * (k + 1))
                continue
            raise
        except urllib.error.URLError:
            time.sleep(5 * (k + 1))
    raise RuntimeError(f"fetch failed after retries: {url}")


def api(params: dict[str, str]) -> tuple[str, dict]:
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    for k in range(8):
        st, b = get(url)
        time.sleep(1.0)
        if st == 200:
            try:
                return url, json.loads(b)
            except json.JSONDecodeError:
                print(f"non-JSON body (try {k + 1}): {b[:200]!r}", flush=True)
        else:
            print(f"HTTP {st} (try {k + 1})", flush=True)
        time.sleep(10 * (k + 1))
    raise RuntimeError(f"no JSON after retries: {url}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    try:  # documentation only: never blocks the data fetch
        url, helpj = api({"action": "help", "modules": "main|query|query+info|query+pageprops|query+revisions",
                          "helpformat": "wikitext", "wrap": "1"})
        (OUT / "api_help.json").write_text(json.dumps({"url": url, "accessed": now(), "response": helpj}, indent=1) + "\n")
    except RuntimeError as exc:
        print(f"API help not saved: {exc}", flush=True)
    with open(ROOT / "data" / "loop_hurricanes" / "sources" / "events.csv", newline="") as f:
        events = list(csv.DictReader(f))
    for e in events:
        titles = lh.candidate_titles(e["name"], int(e["year"]))
        qurl, q = api({"action": "query", "redirects": "1", "prop": "pageprops|info",
                       "titles": "|".join(titles.values())})
        target, rule, via = lh.resolve_target(q, titles)
        rec: dict = {"atcf": e["atcf"], "pulled_at": now(), "titles": titles,
                     "query": {"url": qurl, "response": q}, "target": target, "rule": rule, "via": via}
        if target:
            curl, c = api({"action": "query", "prop": "revisions", "rvdir": "newer", "rvlimit": "1",
                           "rvprop": "timestamp|ids", "titles": target})
            rec["creation"] = {"url": curl, "response": c}
            d0 = dt.date.fromisoformat(e["t0_utc"][:10])
            start = (d0 - dt.timedelta(days=3)).strftime("%Y%m%d")
            end = (d0 - dt.timedelta(days=1)).strftime("%Y%m%d")
            rec["pageviews"] = {}
            for t in [target, *via]:
                u = PV.format(title=urllib.parse.quote(t.replace(" ", "_"), safe=""), start=start, end=end)
                st, b = get(u)
                rec["pageviews"][t] = {"url": u, "status": st, "sha256": hashlib.sha256(b).hexdigest(),
                                       "response": json.loads(b) if b else {}}
                time.sleep(1.0)
        (OUT / f"{e['atcf']}.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
        print(e["atcf"], target, rule, via, flush=True)


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    main()
