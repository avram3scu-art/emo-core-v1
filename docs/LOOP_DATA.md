# Hurricane loop: data check (session 2.2, 29 Oct 2026)

Moves H3–H5 (feasibility only; no test). Evidence class of this file: **infrastructure**.

**No data record was opened in this session.** Only documentation pages, format descriptions, dataset index pages and the OpenFEMA dataset-metadata endpoint (which lists datasets, not declarations) were read. No HURDAT2, error-file, pageview, declaration, advisory, GIS or TCR content was opened. The repo's existing HURDAT2 file and pageview code were not read as data; only `scripts/refresh_open_data.py` was read for its URLs.

All pages below were accessed 29 Oct 2026. Pages that could not be opened are listed in §9; what depends on them is marked **unverified**.

## 1. Verdicts

| Link | Source | Per-event values | Verdict | Fallback |
|---|---|---|---|---|
| Events | HURDAT2 Atlantic (NHC) | yes (six-hourly; landfall flag `L`) | **Feasible** | — |
| Predict | NHC official forecast error database, individual forecasts (text) | yes (per forecast; aggregate per storm) | **Feasible** (column layout unverified) | annual errors already in repo (`data/nhc_atlantic_official_track_errors_1970_2025.csv`), season-level only |
| Attend | Wikimedia pageviews API, per article per day | yes, once a storm→article rule is fixed | **Feasible** from 2015 | — |
| Decide-act | OpenFEMA Disaster Declarations Summaries v2 | yes (per declaration and designated area) | **Feasible with caveats** (§5) | FEMA Web Disaster Declarations v1 (hurricane code documented) |
| Outcome | NHC Tropical Cyclone Reports | yes, but in PDF prose/tables | **Infeasible as machine-readable** | (a) HURDAT2 landfall intensity as the severity/outcome proxy; (b) PDF extraction under pre-registered rules with a second check (D11 risk) |
| Warning times | NHC GIS advisory watches/warnings, per advisory | yes, per advisory | **Feasible** from 2008 (fields unverified) | advisory text archive 1999–2025 (issuance times in text) |
| Rule-based triggers | 44 CFR 206.35; FEMA pre-landfall policy (2006) | — | **Found**: no automatic federal trigger; one procedural link (§7) | — |

Full four-link coverage (events, predict, attend, decide-act, warnings) is 2015–2025 for known history, as PLAN §5 assumed. Outcome needs a fallback.

## 2. Events — HURDAT2

- **Fields:** header (basin, ATCF number, year, name, line count); data lines: date, time (UTC), record identifier, status, lat, lon, max sustained wind (kt), min pressure (mb), 34/50/64-kt wind radii by quadrant (n mi).
- **Identifiers:** L = landfall, C = closest approach without landfall, G, I, P, R, S, T, W. **Status:** TD, TS, HU (≥ 64 kt), SD, SS, EX, LO, WV, DB.
- **Coverage:** 1851–2025; current file `hurdat2-1851-2025-092326.txt`, updated 23 Sep 2026 (1971–1975 revised). Same file the repo pins.
- **Update:** reanalysis revisions issued irregularly (latest above); a new season is added after post-analysis.
- **Access:** comma-delimited text download.
- **Licence:** no licence text on the data page; NOAA disclaimer page linked, not opened (**unverified**).
- **Caveats:** landfall marking rules vary by era and country (international landfalls only 1951–1965 and 1991 on); pressure complete from 1979; radii from 2004; non-synoptic records at analyst discretion; −999 missing.

## 3. Predict — NHC official forecast error database

- **Files:** `1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt` (Atlantic track and intensity, 1970–2025, no depressions); `1989-present_..._ATL_TI_errors.txt` (with depressions); along/cross-track versions; `.zip` copies.
- **Per event:** yes; files tabulate individual forecasts ("ind").
- **Computation:** homogeneous with best-track CLIPER5 and Decay-SHIFOR5, subtropical systems included (so forecasts without a CLIPER/SHIFOR pair are excluded).
- **Fields:** in `Error_Tabulation_File_Format.pdf`, which could not be opened (§9): column layout **unverified**.
- **Update:** coverage ends 2025; annual addition implied, not stated (**unverified**).
- **Licence:** none stated (as §2).

## 4. Attend — Wikimedia pageviews

- **Access:** REST endpoint already used by the repo, `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{lang}.wikipedia/...` (`scripts/refresh_open_data.py`).
- **Definition:** a view is a 200/304 HTML (or app JSON) request; agents split into user, spider (self-identified bots) and automated (heuristic); redirects are not counted for the target article.
- **Coverage:** current pageview definition since May 2015 (dumps readme); per-article API from July 2015 per `docs/UIA_PROTOCOL.md` (API start date not confirmed on a page opened this session).
- **Licence:** CC0 (all Analytics datasets).
- **Per event:** yes, daily per article; requires a fixed storm→article mapping rule (session 2.3), since articles are created after naming and redirects split views.
- **Update latency, rate limits:** not stated on pages opened (**unverified**).

## 5. Decide-act — OpenFEMA declarations

- **Dataset:** Disaster Declarations Summaries **v2** (v1 is no longer updated; last update 1 May 2025). API `https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries`; CSV/JSON downloads.
- **Metadata (OpenFEMA dataset index):** 70,596 records; refresh every 20 minutes; licence field null; citation rules on the OpenFEMA Terms and Conditions page (not opened, **unverified**). data.gov lists the US government-works licence.
- **Fields (from the v1 page opened in session 2.0, AUDIT §6):** `declarationDate`, `incidentBeginDate`, `incidentEndDate`, `incidentType`, programmes declared; coverage from 1953, county data from 1964. The v2 field list could not be opened (§9): **unverified** that v2 keeps these names.
- **Hurricane as an incident type:** **partly confirmed.** The FEMA Web Disaster Declarations v1 page lists incident-type codes in `designatedIncidentTypes` with **H = Hurricane**; `incidentType` itself has no enumerated value list on any page opened ("such as fire or flood"). Confirm the exact `incidentType` string when the data are opened (session 2.4, after the protocol).
- **Per event:** one record per declaration and designated area; declaration type distinguishes major disaster (DR) and emergency (EM) (codes stated in v1 docs, AUDIT §6).
- **Caveats:** raw NEMIS data with some human error; historical records entered manually after 1998; a declaration is a decision, not a delivery; US only; storm→declaration matching must use state, dates and (if present) title (**unverified** field). The Web Declarations v1 page states its last refresh as 10 Oct 2024, while the index shows 29 Oct 2026: conflicting, unresolved.

## 6. Outcome — Tropical Cyclone Reports

- **Format:** one PDF per storm (`https://www.nhc.noaa.gov/data/tcr/ALNNYYYY_Name.pdf`); Atlantic 1995–2025 as text PDFs, older as scanned images; an XML index of reports; best track as KMZ/shapefile.
- **Content:** synoptic history, meteorological statistics, casualties and damages, best track; comprehensive reports for storms with coastal watches or warnings, direct deaths, or wide interest.
- **Machine-readable outcome table:** **none**; deaths and damage sit in the PDF. Hence infeasible as a machine-readable link.
- **Fallback:** (a) use HURDAT2 landfall intensity (wind, pressure) as the severity control and drop "outcome" as a measured link, or (b) extract deaths/damage from the TCR PDFs under extraction rules fixed in the protocol, with an independent check, accepting the D11 hand-coding risk. Other outcome databases (e.g. NCEI) were not opened (**unverified**). Recommendation for 2.3: (a) for H4–H5, which need severity but not outcome.

## 7. Warning times and rule-based triggers

**Warning times.** NHC GIS archive: "Advisory forecast track, cone and watches/warnings", shapefile and KMZ, **2008–2026**, one file per advisory (advisory number in the file name, e.g. `AL112017_020adv_WW.kmz`). Attribute fields (issuance time) are not described on the page opened (**unverified**). Storm-surge watches/warnings archived 2017–2026. The breakpoint product has **no archive** (current season only). Advisory text archive 1999–2025 carries issuance times in the text. Per event: the earliest hurricane watch/warning time for a storm is derivable per advisory.

**Rule-based triggers (federal).**
- **44 CFR 206.35** (eCFR, current): an emergency declaration needs a Governor's request through the Regional Administrator, within five days of the need becoming apparent and no later than thirty days after the incident; incidents that "threaten to occur" qualify, so pre-landfall requests are allowed. Nothing is triggered automatically by a weather warning. Exception: emergencies where the federal government has primary responsibility.
- **FEMA Hurricane/Typhoon Pre-Landfall Policy** (DHS fact sheet, 16 Jun 2006, interim guidance of 9 Jun 2006; archived copy): a pre-landfall emergency declaration is considered when an **NWS projection** shows a major-hurricane threat **and** either mandatory evacuation of ≥ 3 counties or > 100,000 residents, or federal pre-positioning beyond state capacity; assistance limited to Public Assistance Category B. **Whether this policy is still in force is unverified.**
- **Consequence for H4 (independent-agencies null, PLAN §3):** pre-landfall EM declarations are procedurally tied to forecasts and evacuation orders, so forecast→EM timing is formal procedure, not coupling. Session 2.3 must treat EM pre-landfall declarations as procedure (control or exclude) and test coupling on lags not covered by this rule (e.g. landfall→DR major disaster declaration).
- **Not checked:** state statutes and state emergency triggers (each state differs; reason: needs time), current FEMA policy text, Stafford Act sections themselves (only cited via 44 CFR).

## 8. What session 2.3 must use

1. Event: US landfall (`L`) at `HU` status, 2015–2025 known history; 2027 blind.
2. Predict: per-storm errors from the individual-forecast file; layout to be confirmed from the format PDF (Adrian can supply it if it stays unreachable).
3. Attend: per-article daily user-agent views; storm→article rule fixed in advance.
4. Decide-act: DR vs EM split; pre-landfall EM treated as procedure.
5. Warnings: earliest watch/warning per storm from the 2008+ GIS advisory files.
6. Outcome: drop as a link; HURDAT2 intensity as severity control (recommended fallback (a)).

## 9. Pages that could not be opened (this session)

- `https://www.fema.gov/about/openfema/disaster-declarations-summaries` (opened in 2.0; not on this session's allowlist).
- `https://www.fema.gov/openfema-dataset-disaster-declarations-summaries-v2` (allowlist); `https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2` and `https://www.fema.gov/about/openfema/Datasets-disaster-declaration-summaries` (site error).
- `https://www.nhc.noaa.gov/verification/pdfs/Error_Tabulation_File_Format.pdf` (allowlist).
- Wikimedia API documentation pages opened did not state start date, latency or rate limits.

## 10. Sources (opened 29 Oct 2026)

- NHC, HURDAT2 format (Nov 2019): https://www.nhc.noaa.gov/data/hurdat/hurdat2-format-nov2019.pdf
- NHC Data Archive: https://nhc.noaa.gov/data
- NHC forecast error database: https://nhc.noaa.gov/verification/verify7.shtml
- NHC 2015 Atlantic TCR index: https://www.nhc.noaa.gov/data/tcr/index.php?season=2015
- NHC GIS data page: https://www.nhc.noaa.gov/gis/
- NHC GIS watch/warning breakpoints archive: https://www.nhc.noaa.gov/gis/archive_breakpoints.php
- eCFR, 44 CFR 206.35: https://www.ecfr.gov/current/title-44/chapter-I/subchapter-D/part-206/subpart-B/section-206.35
- DHS/FEMA, Hurricane/Typhoon Pre-Landfall Policy fact sheet (2006, archived): https://webarchive.library.unt.edu/web/20090114022621/http://www.fema.gov/pdf/media/2006/pre-landfall.pdf
- CRS Insight IN10978, Hurricane Michael (2018; pre-landfall EM example, no automatic trigger): https://www.everycrsreport.com/files/20181011_IN10978_8bd7d2a7a8ee492b592db553346cf89b311c635a.pdf
- data.gov, Disaster Declarations Summaries: https://catalog.data.gov/dataset/disaster-declarations-summaries
- OpenFEMA dataset index (metadata only): https://www.fema.gov/api/open/v1/OpenFemaDataSets
- FEMA Web Disaster Declarations v1: https://fema.gov/openfema-data-page/fema-web-disaster-declarations-v1
- Wikimedia, page views concept: https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/concepts/page-views.html
- Wikimedia, Analytics API: https://doc.wikimedia.org/analytics-api and https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/
- Wikitech, AQS: https://wikitech.wikimedia.org/wiki/Data_Platform/AQS
- Wikimedia pageview dumps readme: https://dumps.wikimedia.org/other/pageviews/readme.html
- Repo: `docs/AUDIT_2026-10-29.md` §6, `docs/UIA_PROTOCOL.md`, `scripts/refresh_open_data.py`.
