"""Exclusions E1-E3 of docs/STREAM_DATA.md §5, enforced in code.

E1  CEMS Rapid Mapping activations with a flood category (category or subCategory) and any
    EU27 country, whose event or activation date lies in 30 Oct 2026 - 31 Jan 2029, are
    dropped in memory before anything is written. Nothing reports them: no count, no log
    line, no flag. Records whose dates cannot be read are dropped too (conservative).
    Protects docs/FLOOD_LOOP_PROTOCOL.md §3, §10, §11.
E2  (a-d) No pageviews and no Wikimedia request of any kind in this version: every
    Wikimedia/Wikipedia host is refused by the HTTP guard. Pageviews need the 3.3 matching
    rule and per-article E2a-E2d filters first. Protects GWI v2, the flood test, the 2027
    hurricane arm.
E3  OpenFEMA never enters the stream: fema.gov hosts are refused. Protects the 2027
    hurricane registry (docs/LOOP_PROTOCOL.md §7).
"""
from __future__ import annotations

import datetime as dt
from collections.abc import Iterable
from urllib.parse import urlsplit

E1_START = dt.date(2026, 10, 30)
E1_END = dt.date(2029, 1, 31)

EU27_NAMES = {
    "austria", "belgium", "bulgaria", "croatia", "cyprus", "czechia", "czech republic",
    "denmark", "estonia", "finland", "france", "germany", "greece", "hungary", "ireland",
    "italy", "latvia", "lithuania", "luxembourg", "malta", "netherlands",
    "the netherlands", "poland", "portugal", "romania", "slovakia", "slovenia", "spain",
    "sweden",
}
EU27_ISO2 = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "EL", "HU",
    "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
}
EU27_ISO3 = {
    "AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC",
    "HUN", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK",
    "SVN", "ESP", "SWE",
}

# Only these hosts may be contacted by the stream (E2, E3 by construction).
ALLOWED_HOSTS = {
    "www.gdacs.org",
    "gdacs.org",
    "earthquake.usgs.gov",
    "rapidmapping.emergency.copernicus.eu",
    "goadmin.ifrc.org",
}
# Named refusals, checked before the allowlist so a later edit of ALLOWED_HOSTS cannot let them in.
FORBIDDEN_SUFFIXES = (
    "fema.gov",            # E3
    "wikipedia.org",       # E2a-E2d
    "wikimedia.org",       # E2a-E2d (pageviews API, dumps)
    "wikidata.org",        # E2: no article matching in this version
    "mediawiki.org",
)


class ExcludedSource(RuntimeError):
    """A request to a host the stream must never contact."""


def check_url(url: str) -> str:
    """Return url if the stream may fetch it; raise ExcludedSource otherwise."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    if parts.scheme != "https":
        raise ExcludedSource(f"not https: {url}")
    for suffix in FORBIDDEN_SUFFIXES:
        if host == suffix or host.endswith("." + suffix):
            raise ExcludedSource(f"excluded host (E2/E3): {host}")
    if host not in ALLOWED_HOSTS:
        raise ExcludedSource(f"host not in stream allowlist: {host}")
    return url


def _strings(value) -> Iterable[str]:
    if value is None:
        return
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _strings(v)
    elif isinstance(value, (list, tuple, set)):
        for v in value:
            yield from _strings(v)


def _is_eu27(countries) -> bool:
    for s in _strings(countries):
        t = s.strip()
        if t.lower() in EU27_NAMES or t.upper() in EU27_ISO2 or t.upper() in EU27_ISO3:
            return True
    return False


def _is_flood(rec: dict) -> bool:
    return any("flood" in s.lower()
               for key in ("category", "subCategory", "sub_category", "hazard")
               for s in _strings(rec.get(key)))


def _date(value) -> dt.date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    try:
        return dt.date.fromisoformat(value[:10])
    except ValueError:
        return None


def e1_drops(rec: dict) -> bool:
    """True if a CEMS activation falls under E1 (must not be written)."""
    if not (_is_flood(rec) and _is_eu27(rec.get("countries"))):
        return False
    dates = [d for d in (_date(rec.get("eventTime")), _date(rec.get("activationTime")))
             if d is not None]
    if not dates:
        return True
    return any(E1_START <= d <= E1_END for d in dates)


def apply_e1(records: list[dict]) -> list[dict]:
    """Keep the CEMS records E1 allows. Silent by design: returns only the kept list."""
    return [r for r in records if not e1_drops(r)]
