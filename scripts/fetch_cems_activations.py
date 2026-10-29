"""Fetch the CEMS Rapid Mapping public activation list (session 2.11, feasibility count only).

Writes data/second_domain/cems_activations_<date>.json and prints counts of flood
activations in EU member states by activation year. No lag (eventTime -> activationTime)
is computed here: lags are reserved for a future pre-registered protocol.
Endpoint documented at https://mapping.emergency.copernicus.eu/about/how-to-harvest-cems-mapping-data/emergency-response-data/
"""
import collections
import datetime
import hashlib
import json
import sys
import urllib.request

URL = "https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations-info/?limit=100"
EU27 = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Czech Republic", "Denmark",
        "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia",
        "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
        "Slovenia", "Spain", "Sweden"}


def fetch() -> list:
    out, url = [], URL
    while url:
        with urllib.request.urlopen(url, timeout=60) as r:
            page = json.load(r)
        out += page["results"]
        url = page["next"]
    return out


def main() -> None:
    if len(sys.argv) > 1:
        rows = json.load(open(sys.argv[1]))
    else:
        rows = fetch()
        path = f"data/second_domain/cems_activations_{datetime.date.today()}.json"
        blob = json.dumps(rows, indent=1, sort_keys=True).encode()
        open(path, "wb").write(blob)
        print(path, hashlib.sha256(blob).hexdigest())
    years = sorted({r["activationTime"][:4] for r in rows if r.get("activationTime")})
    print(f"activations: {len(rows)}; activation years {years[0]}-{years[-1]}")
    cats = collections.Counter(r.get("category") for r in rows)
    print("categories:", dict(cats))
    eu_flood = collections.Counter(
        r["activationTime"][:4] for r in rows
        if "flood" in str(r.get("category", "")).lower() and EU27 & set(r.get("countries") or []))
    print("EU flood activations by activation year:", dict(sorted(eu_flood.items())))


if __name__ == "__main__":
    main()
