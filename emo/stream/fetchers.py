"""Daily fetchers for the global hazard stream (docs/STREAM_DATA.md §6, §9).

Every request passes the host guard of exclusions.check_url (E2, E3). Each fetcher returns
(records, requests_log): records are the raw source objects, unchanged except for an added
"_emo_fetched_at" (UTC ISO time the response arrived, for latency); requests_log holds,
per request, the URL, HTTP status and start/end times. Nothing here prints or logs record
content or record counts.

Windows are rolling (7 days back) so a missed day is recovered by the next run; the
duplicates this creates are removed at analysis time, never by editing the log.
"""
from __future__ import annotations

import datetime as dt
import time
from collections.abc import Callable

import requests

from emo.stream.exclusions import apply_e1, check_url

USER_AGENT = "EMO-stream/0.1 (+https://github.com/avram3scu-art/emo-core-v1)"
WINDOW_DAYS = 7
PAUSE_S = 0.5          # between requests to one host (Wikimedia-style politeness, §9)
MAX_PAGES = 200        # hard stop against a pagination loop


def _now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class Http:
    """Guarded GET with retries; records one log row per request."""

    def __init__(self, session: requests.Session | None = None, pause: float = PAUSE_S):
        self.s = session or requests.Session()
        self.s.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
        self.pause = pause
        self.log: list[dict] = []

    def get_json(self, url: str, params: dict | None = None, allow_empty: bool = False):
        check_url(url)
        last_err: Exception | None = None
        for attempt in range(3):
            start = _now()
            try:
                r = self.s.get(url, params=params, timeout=90, allow_redirects=False)
                end = _now()
                self.log.append({"url": r.url if hasattr(r, "url") else url,
                                 "status": r.status_code, "start": start, "end": end})
                if r.status_code in (301, 302, 303, 307, 308):
                    loc = r.headers.get("Location", "")
                    check_url(loc)          # a redirect may not leave the allowlist
                    url, params = loc, None
                    continue
                if allow_empty and r.status_code in (204, 404):
                    return None, end
                r.raise_for_status()
                time.sleep(self.pause)
                return r.json(), end
            except requests.RequestException as e:   # retry network/5xx errors
                last_err = e
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"request failed after retries: {url}") from last_err


def _stamp(records: list, fetched_at: str) -> list:
    out = []
    for r in records:
        if isinstance(r, dict):
            r = dict(r)
            r["_emo_fetched_at"] = fetched_at
        out.append(r)
    return out


# --- GDACS (API quick start v2, opened 29 Oct 2026) -------------------------------------
GDACS_SEARCH = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"
GDACS_CACHE = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/events4app"
GDACS_TYPES = "EQ;TC;FL;VO;DR;WF;TS"


def fetch_gdacs(http: Http, today: dt.date) -> list:
    recs: list = []
    params = {"eventlist": GDACS_TYPES, "alertlevel": "green;orange;red",
              "fromdate": str(today - dt.timedelta(days=WINDOW_DAYS)),
              "todate": str(today), "pagesize": 100}
    for page in range(1, MAX_PAGES + 1):
        data, at = http.get_json(GDACS_SEARCH, {**params, "pagenumber": page},
                                 allow_empty=True)
        feats = (data or {}).get("features") or []
        recs += [{"_emo_feed": "search", **f} for f in _stamp(feats, at)]
        if len(feats) < 100:
            break
    data, at = http.get_json(GDACS_CACHE, allow_empty=True)
    feats = (data or {}).get("features") or []
    recs += [{"_emo_feed": "events4app", **f} for f in _stamp(feats, at)]
    return recs


# --- USGS ComCat FDSN event service + PAGER (opened 29 Oct 2026) -------------------------
USGS_QUERY = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def fetch_usgs(http: Http, today: dt.date) -> list:
    start = today - dt.timedelta(days=WINDOW_DAYS)
    data, at = http.get_json(USGS_QUERY, {"format": "geojson", "starttime": str(start),
                                          "minmagnitude": 4.5, "orderby": "time-asc",
                                          "limit": 20000})
    feats = _stamp(data.get("features") or [], at)
    recs = [{"_emo_feed": "comcat", **f} for f in feats]
    # PAGER: the detail document (which carries the losspager product) for every event
    # with a PAGER alert level, whatever its value.
    for f in feats:
        props = f.get("properties") or {}
        if props.get("alert") and props.get("detail"):
            det, at2 = http.get_json(props["detail"])
            recs.append({"_emo_feed": "detail", **_stamp([det], at2)[0]})
    return recs


# --- CEMS Rapid Mapping (endpoint as scripts/fetch_cems_activations.py) ------------------
CEMS_URL = ("https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/"
            "public-activations-info/")


def fetch_cems(http: Http, today: dt.date) -> list:
    recs: list = []
    url: str = CEMS_URL
    params: dict | None = {"limit": 100}
    for _ in range(MAX_PAGES):
        data, at = http.get_json(url, params)
        recs += _stamp(data.get("results") or [], at)
        nxt = data.get("next")
        if not nxt:
            break
        url, params = nxt, None
    return apply_e1(recs)            # E1: dropped in memory, before anything is written


# --- IFRC GO (production API https://goadmin.ifrc.org/api/v2/, OpenAPI 3.0.3) -----------
GO_BASE = "https://goadmin.ifrc.org/api/v2/"


def _go_pages(http: Http, endpoint: str, params: dict) -> list:
    out: list = []
    url: str = GO_BASE + endpoint + "/"
    p: dict | None = {**params, "limit": 100, "format": "json"}
    for _ in range(MAX_PAGES):
        data, at = http.get_json(url, p)
        out += _stamp(data.get("results") or [], at)
        nxt = data.get("next")
        if not nxt:
            break
        url, p = nxt, None
    return out


def fetch_ifrc(http: Http, today: dt.date) -> list:
    since = str(today - dt.timedelta(days=WINDOW_DAYS))
    recs = [{"_emo_feed": "event", **r}
            for r in _go_pages(http, "event", {"updated_at__gte": since})]
    # Appeals (atype 0 DREF, 1 Emergency Appeal, ...): the daily amount_funded snapshot is
    # every appeal still running today plus every appeal whose data changed in the window.
    recs += [{"_emo_feed": "appeal_running", **r}
             for r in _go_pages(http, "appeal", {"end_date__gte": str(today)})]
    recs += [{"_emo_feed": "appeal_updated", **r}
             for r in _go_pages(http, "appeal", {"appeal__real_data_update__gte": since})]
    return recs


FETCHERS: dict[str, Callable[[Http, dt.date], list]] = {
    "gdacs": fetch_gdacs,
    "usgs": fetch_usgs,
    "cems": fetch_cems,
    "ifrc_go": fetch_ifrc,
}
