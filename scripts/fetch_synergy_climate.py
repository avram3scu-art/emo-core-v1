"""Fetch the three climate streams for the synergy test (docs/SYNERGY_PROTOCOL.md §2).

Raw responses are stored as fetched; parsing happens in analysis/synergy_climate.py.
"""
import calendar
import datetime as dt
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "emo-core-v1 synergy test (github.com/avram3scu-art/emo-core-v1)"}
OUT = Path("data/sources/synergy_climate")
YEARS = range(2016, 2026)

OPENALEX = ("https://api.openalex.org/works?per_page=1&filter="
            'title_and_abstract.search:"climate change",type:article,'
            "from_publication_date:{a},to_publication_date:{b}")
FEDREG = ("https://www.federalregister.gov/api/v1/documents/facets/monthly?"
          + urllib.parse.urlencode([
              ("conditions[term]", '"climate change"'),
              ("conditions[type][]", "RULE"),
              ("conditions[type][]", "PRORULE"),
              ("conditions[type][]", "PRESDOCU"),
              ("conditions[publication_date][gte]", "2016-01-01"),
              ("conditions[publication_date][lte]", "2025-12-31"),
          ]))
PV = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/"
      "all-access/user/{title}/monthly/2016010100/2025123100")


def get(url: str, tries: int = 8) -> bytes:
    last = None
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(30 * (i + 1))
    raise RuntimeError(f"{url}: {last}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    src = {}

    def save(name: str, url: str, raw: bytes) -> None:
        (OUT / name).write_bytes(raw)
        src[name] = {"source_url": url, "downloaded_at": now, "sha256": hashlib.sha256(raw).hexdigest()}

    # Resumable (protocol §9 amendment): each month is saved as it arrives; a 429 stops the
    # run with the partial cache kept, and the next run fetches only the missing months.
    cache = OUT / "openalex_climate_change_monthly.json"
    science = json.loads(cache.read_text()) if cache.exists() else {}
    for y in YEARS:
        for m in range(1, 13):
            a = f"{y}-{m:02d}-01"
            if a[:7] in science:
                continue
            b = f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"
            url = OPENALEX.format(a=a, b=b).replace(" ", "%20").replace('"', "%22")
            url += "&mailto=avram3scu-art@users.noreply.github.com"
            key = os.environ.get("OPENALEX_API_KEY")
            time.sleep(1.0)
            try:
                got = get(url + (f"&api_key={key}" if key else ""), tries=3)  # key never stored
                science[a[:7]] = {"url": url, "count": json.loads(got)["meta"]["count"]}
            except RuntimeError:
                cache.write_text(json.dumps(science, indent=1, sort_keys=True) + "\n")
                print(f"partial: {len(science)} of 120 OpenAlex months cached; rerun later")
                return
    raw = (json.dumps(science, indent=1, sort_keys=True) + "\n").encode()
    save("openalex_climate_change_monthly.json", OPENALEX, raw)

    save("fedreg_climate_change_monthly.json", FEDREG, get(FEDREG))
    for t in ("Climate_change", "Global_warming"):
        url = PV.format(title=t)
        save(f"pageviews_en_{t}_monthly.json", url, get(url))

    (OUT / "SOURCES.json").write_text(json.dumps(src, indent=2) + "\n")
    print("fetched", list(src))


if __name__ == "__main__":
    main()
