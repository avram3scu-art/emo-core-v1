# Global hazard event stream: data check (session 3.1, 29 Oct 2026)

Serves H3, H6, H8 (feasibility only; no test). Evidence class of this file: **infrastructure**.

**No event record was opened in this session.** Only documentation pages, terms pages, schema pages and aggregate reports (yearly or half-yearly totals, no per-event rows) were read. No feed, API list, activation, appeal, alert, pageview or EM-DAT row was fetched. Several official pages could not be fetched (session allowlist, §8); what depends on them is marked **unverified**.

## 1. Verdicts

| Link | Source | Verdict | Main condition |
|---|---|---|---|
| Warning / alert | **USGS earthquake feeds (ComCat) with PAGER** | **use** | exclusion E2a (GWI v2); feed latency and PAGER timing unverified |
| Warning / alert | **GDACS** (EQ, TC, FL, VO, DR, WF, TS) | **use with conditions** | licence unstated (EC legal notice, not opened); flood "alerts" are post-impact (§2.2), not warnings; API reference not opened |
| Attention | **Wikimedia pageviews (per article, daily)** | **use with conditions** | exclusions E2a–E2d protect three registered tests; latency not documented |
| Decision | **Copernicus EMS Rapid Mapping activations** | **use with conditions** | exclusion E1 (flood test); history coverage of the public API unclear (§2.4) |
| Decision | **IFRC GO: DREF and Emergency Appeals** | **use with conditions** | licence unstated; production API URL unverified; non-hazard types filtered by `dtype` |
| Delivery / money | **IFRC GO `amount_funded`** (appeal coverage) | **use with conditions** | a running total, not dated flows: only daily snapshots taken by EMO give a time series (no back-fill) |
| Delivery / money | **OCHA FTS** | **reject for the daily stream** (revisit for H9 in 3.7) | self-reported, curation latency "varies"; licence and GLIDE link not found |
| Losses | **EM-DAT** | **reject for the stream**; usable offline in 3.7 under its terms | account; no redistribution; no derivative databases; not published promptly |
| Losses (modelled) | **USGS PAGER** fatality and economic estimates | **use with conditions** | labelled *modelled*, never as observed losses; economic bins in million USD (§2.1) |
| Losses (reported) | **IFRC GO field reports** (deaths, affected, displaced) | **use with conditions** | as IFRC GO licence |
| Linking | **GLIDE** | **use with conditions** (join key, not a source) | licence unstated; coverage incomplete (§3) |
| Linking | **IFRC Monty STAC extension** | **check in 3.2** | already maps USGS, GDACS, CEMS, DREF, GLIDE; its correlation pages and any public endpoint not opened |

## 2. Per source

### 2.1 USGS earthquake feeds, ComCat, PAGER

- **Records:** every located earthquake; GeoJSON properties include `alert` (PAGER level), `sig`, `tsunami`, `mmi`, `cdi`, `felt`, `status`, `updated`, and `ids`/`sources`/`code` for linking ([event fields](https://earthquake.usgs.gov/data/comcat/event-fields.php)). The page gives types only, not value lists.
- **PAGER:** `losspager` product with modelled fatalities (`empirical_fatality.total_fatalities`) and economic loss (`empirical_economic.total_dollars`); `alerts.json` bins are in million USD although labelled USD ([Monty USGS model](https://ifrcgo.org/monty-stac-extension/model/sources/USGS/)).
- **Licence:** public domain (Monty USGS page, linking USGS copyright guidance; the USGS page itself could not be fetched: **unverified at source**).
- **Access:** no key; HTTP GET only; default cache 1 day for static resources ([feed changelog](https://earthquake.usgs.gov/earthquakes/feed/v1.0/changelog.php)); a 2025 ComCat query already ran in this repo (`docs/GWI_V2_PROTOCOL.md` §11, run 40848154988).
- **Latency:** feed update frequency not stated on the opened pages (Feed Life Cycle Policy not opened): **unverified**. PAGER release time: page not reachable, **unverified**.
- **Coverage:** global, earthquakes only. Volume of M ≥ 7: about 18 a year (`docs/GWI_V2_PROTOCOL.md` §10, citing USGS; not re-opened today).

### 2.2 GDACS

- **Records:** events and episodes (`eventid` + `episodeid`), `alertlevel`, `iso3` and affected countries, dates, GLIDE when present, links to other sources (e.g. GloFAS) ([Monty GDACS model](https://ifrcgo.org/monty-stac-extension/model/sources/GDACS/)). Coverage by hazard: earthquakes since 2004, floods since 2004 (red only), tropical cyclones since 2011, volcanoes since 2011, droughts since 2017, forest fires since 2021 ([GDACS poster 2024](https://www.gdacs.org/documents/GDACS_poster_2024_p01.pdf)).
- **How alert levels are set:** earthquakes from magnitude, depth, population within 100 km and country vulnerability; cyclones from population under storm-force winds and vulnerability; **floods from reported deaths or displacement**, so a GDACS flood alert follows impact and cannot serve as the warning link for floods ([GDACS Guidelines 2014](https://un-spider.org/sites/default/files/GDACS%20Guidelines%202014_-_FINAL.PDF)).
- **Latency:** earthquake messages a few minutes after the event (preliminary, revised later); cyclone bulletins every 6 h (Guidelines 2014).
- **Licence and terms:** no licence text; data "as is", automated alerts without expert review, not to be used for decisions without confirmation ([terms PDF Mar 2025](https://www.gdacs.org/documents/2025/GDACS_Terms_of_use_Mar_25.pdf); [terms page](https://gdacs.org/About/termofuse.aspx), which points to the EC legal notice for copyright, not opened). Monty lists the GDACS collection as MIT, which is Monty's own licence, not evidence about GDACS data.
- **Access:** API exists; the quickstart PDF could not be fetched: endpoints, key needs and rate limits **unverified**.

### 2.3 Wikimedia pageviews

- **Records:** daily views per article, per project; also a daily top-articles list per project.
- **Licence:** CC0 for all Analytics datasets ([pageviews readme, mirror](https://tutankhamon.acc.umu.se/mirror/wikimedia.org/other/pageviews/readme.html)).
- **Access:** open, no key ([Analytics API](https://doc.wikimedia.org/analytics-api); [getting started](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/getting-started.html)); rate-limit and User-Agent policy pages not opened. The repo already fetches it (`scripts/refresh_open_data.py`).
- **Latency:** not documented on any page opened; one 2015 user remark only ([talk page](https://Www.Wikipedia.org/wiki/Wikipedia_talk:Pageview_statistics)). **Unverified**; 3.2 measures it from fetch timestamps (infrastructure).
- **Linking:** needs an event → article rule (title, langlinks, redirects). That rule is a protocol item for 3.3, written before any matching.

### 2.4 Copernicus EMS Rapid Mapping

- **Records:** activation `code` (EMSR…), `eventTime` (onset), `activationTime` (tasking), `countries`, `category`/`subCategory`, `reason`, and link fields `gdacsId`, `charterNumber`, `relatedevents`; no GLIDE field ([Monty CEMS model](https://ifrcgo.org/monty-stac-extension/model/sources/CEMS/)).
- **Who decides:** inside the EU only the member state's national focal point may activate for its territory; outside the EU, EU services (ERCC, DGs, EEAS) may; every request is authorised by DG ECHO/ERCC. Initial products are due 3–12 h after imagery acceptance ([Manual of Procedures v1.3](https://emergency.copernicus.eu/mapping/sites/default/files/files/EMS_Mapping_Manual_of_Procedures_v1_3_final.pdf), characters 0–100,000 read). So outside Europe an activation is a European decision about another country.
- **Licence:** free and open, attribution "© European Union, Copernicus Emergency Management Service" (Monty CEMS page).
- **Access:** public API, no authentication; no "updated since" filter, so change detection is client-side (Monty CEMS page). Same endpoint as `scripts/fetch_cems_activations.py`.
- **Volume:** 572 activations 2012 – Apr 2022; 5–6 a month in the years before 2021 ([Copernicus Observer, Apr 2022](https://www.copernicus.eu/en/node/11552)). Monty's note that `limit=300` returns "the full set of 224" conflicts with 572: the Rapid Mapping endpoint may hold only recent activations. **History coverage unverified**; irrelevant for a prospective stream.

### 2.5 IFRC GO: DREF, Emergency Appeals, funding, field reports

- **Records:** appeal table columns include `code`, `atype` (0 DREF, 1 Emergency Appeal), `status`, `amount_requested`, `amount_funded`, `start_date`, `end_date`, `created_at`, `modified_at`, `event_id`, `dtype_id`, `country_id`, `triggering_amount` ([GO database diagram](https://ifrcgo.org/database-diagram/tables/api_appeal.html)). Events carry `disaster_start_date` and `dtype`; field reports carry deaths, injured, displaced, missing, affected, assisted (government / IFRC / other) ([Monty IFRC-DREF model](https://ifrcgo.org/monty-stac-extension/model/sources/IFRC-DREF/)). Whether GO events carry GLIDE: not on the pages opened, **unverified**.
- **Licence:** none stated (Monty, checked 2026-07); GO says all its information is open to the public ([IFRC GO](https://www.ifrc.org/ifrc-go)). **Condition:** written terms from IFRC information management before cards are public (3.4).
- **Access:** REST API v2; the documented host is a staging host; production URL **unverified**.
- **Volume:** 115 DREF allocations in H1 2026 (97 in H1 2025); by value floods ~33 %, epidemics ~17 %, complex emergencies ~13 %, population movement ~7 %, earthquakes ~7 % ([DREF Mid-Year Report 2026](https://www.ifrc.org/sites/default/files/2026-09/IFRC-DREF%20Mid-Year%20Report%202026.pdf)).
- **Delivery caveat:** `amount_funded` is a current total. A funding curve exists only from EMO's own daily snapshots, from the first run on; it cannot be rebuilt for the past.

### 2.6 OCHA FTS

- **Records:** humanitarian funding flows (`/v1/public/fts/flow`, query by year, project); public, 1 request/s without login ([UNICEF PRP note](https://unicef.gitbook.io/prp/technical-documentation/ocha-integration-research-summary)). Flows are reported by donors and recipients by template, then curated; processing time varies ([FTS IM toolbox page](https://humanitarian.atlassian.net/wiki/spaces/imtoolbox/pages/2359263233)). HDX describes FTS data as continuously updated, licence not shown on the page opened ([HDX FTS](https://data.humdata.org/organization/ocha-fts?page=12)).
- **Why rejected for the stream:** self-reported with unknown, variable delay, so "no money yet" cannot be told from "not yet reported"; event-level link (emergency ID, GLIDE) not documented on pages opened. Reconsider in 3.7 (H9) as a slow, end-of-event delivery measure.

### 2.7 EM-DAT

- **Terms:** registration; free only for non-commercial research, teaching, information; no copying or distribution of the database or a substantial part, no derivative or substitute databases ([terms of use](https://doc.emdat.be/docs/legal/terms-of-use/)). Public data updated weekly, `.xlsx` download, no API on the page opened ([data accessibility](https://doc.emdat.be/docs/data-accessibility/)); records "not published in real time" ([GLIDE update, Aug 2025](https://www.emdat.be/news/2025/08/major-glide-number-update/)).
- **Why rejected for the stream:** a public mirror republishing per-event losses would be a derivative database. Usable offline for H9 (3.7), losses reported only as aggregates, with Adrian's account (his decision).

## 3. Linking events across sources

Rule order for 3.2 (a proposal; frozen in the 3.3 protocol before any linking statistic is computed):

1. **Explicit keys:** CEMS `gdacsId` → GDACS event; GDACS GLIDE → GLIDE; USGS event ID ↔ GDACS earthquake (whether GDACS stores the USGS ID: **unverified**); IFRC GO `event_id` groups DREF and appeals for one emergency.
2. **GLIDE** ([about](https://glidenumber.net/glide/public/about.jsp): type-year-number-ISO3, issued by ADRC since 2004, on request, also at early-warning stage; used by OCHA, IFRC, EC, CRED). Coverage is incomplete: EM-DAT had to raise GLIDE-linked events by about 74 % in 2025 by back-matching. API `jsonglideset.jsp` by filters, not by ID; no licence stated ([Monty GLIDE model](https://ifrcgo.org/monty-stac-extension/model/sources/GLIDE/)).
3. **Fallback:** ISO3 + hazard class (crosswalk GDACS/EM-DAT/GLIDE codes, Monty GDACS page) + onset date within a fixed window. Window and tie rules are 3.3 protocol items.

**Monty:** IFRC's Monty STAC extension already maps these five sources to one schema with "correlation algorithms". If a public Monty endpoint exists, 3.2 should test it before EMO writes its own joins (cheaper, and a join EMO did not tune cannot be tuned on outcomes). Not opened: its correlation pages and any endpoint.

## 4. Expected linked events per month (estimate, not measured)

Definition used here: a natural-hazard event with an alert or onset record **and** at least one decision record (DREF, Emergency Appeal, or CEMS activation).

| Input (opened) | Per month |
|---|---|
| IFRC DREF allocations, H1 2026 | 19 |
| of which natural hazards (by value ~50–65 %; count share **unverified**) | ~10–12 |
| CEMS activations (pre-2021 rate) | 5–6 |
| USGS M ≥ 7 earthquakes | ~1.5 |
| GDACS orange/red alerts | **not found** |

**Estimate: about 8–15 linked events a month; about 2–4 a month with two decision sources** (IFRC and CEMS overlap unknown). Hurricanes give about 2 measured storms a season (STRATEGY_3_0 §1.4), roughly 0.2–0.3 a month, so the stream would raise n by a factor of about 30–50. Exclusions E1–E2 lower the attention-linked count (all M ≥ 7 earthquakes lose attention until 15 Nov 2027; EU floods lose CEMS until 2029). The real figure is a count, taken by 3.2 from its own log (infrastructure); it is a size, not an outcome of any test.

## 5. Overlap with registered tests (unchanged; exclusions protect them)

| Registered test | What it reads | Overlap with this stream | Exclusion |
|---|---|---|---|
| Flood loop `docs/FLOOD_LOOP_PROTOCOL.md` §3, §10, §11 (period 30 Oct 2026 – 31 Dec 2028, followed to 31 Jan 2029) | CEMS flood activations in EU27 (Y, lags); pageviews of river articles and daily top lists of the 27 EU-language wikis (incl. en for IE, MT) | **yes**: CEMS and pageviews | **E1**: CEMS activations with a flood category and any EU27 country, event or activation date 30 Oct 2026 – 31 Jan 2029, are dropped in memory before writing; no count or log line, until the flood test is scored. **E2b**: no top-articles list of those 27 wikis for dates 1 Oct 2026 – 31 Jan 2029 (baseline days included) until then. **E2c**: no pageviews of rivers or of floods in EU27 countries until then |
| GWI v2 `docs/GWI_V2_PROTOCOL.md` (scored 15 Nov 2027) | pageviews, 12 editions, of articles on M ≥ 7 earthquakes 2026-11-01 – 2027-10-31, and 20 placebo articles; ComCat events | **yes**: pageviews (a scored day opened earlier voids the blind label, §9) | **E2a**: no pageviews of any article about an M ≥ 7 earthquake in that window, nor of the 20 placebos, in any edition, before 15 Nov 2027. USGS alert and event records are not excluded: event identity is not the unknown there |
| 2027 hurricane registry and blind arm `docs/LOOP_PROTOCOL.md` §7, §20, §21 | HURDAT2, OpenFEMA declarations (outcomes), pageviews of US-landfalling Atlantic storms | **yes**: pageviews; no OpenFEMA in the stream | **E2d**: no pageviews of US-landfalling Atlantic storms from 2027 on until that season's §7 run. **E3**: OpenFEMA never enters the stream |

No registered file is changed by this session.

## 6. Recommended stream

**Core (3.2 ingests daily, append-only):** GDACS events and episodes (all hazards; flood alerts flagged as post-impact) + USGS ComCat/PAGER (earthquakes) + CEMS Rapid Mapping (with E1) + IFRC GO events, DREF and appeals with daily `amount_funded` snapshots + Wikimedia pageviews for English event articles (with E2a–E2d; other editions only after a 3.3 rule). Join by §3. Deferred: FTS (3.7), EM-DAT (offline, 3.7).

**Conditions before any card is public (3.4):** written reuse terms for GDACS (EC legal notice) and IFRC GO; attribution lines for CEMS and USGS; the 3.3 protocol registered first ([3.0] rule "published data count as opened"); the H8 protocol (3.5) registered before its forecasts.

**Honest limit:** the decision link is humanitarian and international (IFRC, EU). National government decisions (declarations, budgets) are mostly absent outside the US and EU; the mirror shows the international response loop, not "humanity's" whole response.

## 7. Open (each with reason)

- GDACS API reference and licence; USGS feed policy and PAGER timing; Wikimedia rate and User-Agent policy; IFRC GO production URL and terms. Reason: **needs time / not reachable here** (allowlist); 3.2 opens the API documentation pages it uses, and the licence questions go to 3.4.
- GDACS orange/red counts per month. Reason: **not attempted** beyond two searches; 3.2 counts from its log.
- Monty correlation and endpoint. Reason: **scope** (3.2).

## 8. Sources

All accessed 29 Oct 2026. Opened: the pages linked above. Could not be fetched (allowlist or site error): `earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php`, `earthquake.usgs.gov/data/pager/`, `usgs.gov/information-policies-and-instructions/copyrights-and-credits`, `www.gdacs.org/` (home), `data.gdacs.org/.../GDACS_API_quickstart_v1.pdf`; GO wiki Appeals page returned no body. Repository files used: `docs/FLOOD_LOOP_PROTOCOL.md`, `docs/GWI_V2_PROTOCOL.md`, `docs/LOOP_PROTOCOL.md`, `scripts/fetch_cems_activations.py`, `docs/STRATEGY_3_0.md`.
