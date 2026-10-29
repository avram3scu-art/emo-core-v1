# Hurricane loop event table (session 2.4)

Protocol: `docs/LOOP_PROTOCOL.md` §2–§3, amendments 4–6 and build rules (§16), sources (§17). Hypothesis moved: H3 (decide-act measurability). Evidence class: **infrastructure** (data plumbing). No H3, H4 or H5 statistic is computed here; `summary.json` holds counts only.

## Files

| File | What | Made by |
|---|---|---|
| `loop_events.csv` | one row per event (set HU+TS), one column group per link | `scripts/build_loop_table.py` |
| `decide_records.csv` | every FEMA record matched to an event (`fema_id` = OpenFEMA `id`) | same |
| `predict_lines.csv` | every forecast used in F: error-file line, a-deck line, OFCL and OCD5 48-h errors | same |
| `exclusions.csv` | every missing value with its link and reason (§8.2) | same |
| `summary.json` | realized season sizes, non-missing counts per link, complete cases per H4 pair and season (for the §15 guard in 2.5) | same |
| `MANIFEST.json` | URL, access time and SHA-256 of every source file (committed extracts and the uncommitted full downloads) | fetch scripts |
| `sources/hurdat2_2015_2025.csv` | all lines of storms 2015–2025 from `hurdat2-1851-2025-092326.txt`, with their line numbers in the full file | `scripts/fetch_loop_hurricanes.py hurdat2` |
| `sources/landfall_states.csv` | every HURDAT2 `L` record 2015–2025 with its Census entity (50-km rule) | `... census` (needs the Census zip, not committed: 1:500k, SHA-256 in MANIFEST) |
| `sources/events.csv` | event list (input of the other fetch steps) | `... census` |
| `sources/nhc_errors_events.csv` | header and event-storm lines of the NHC error file, with line numbers | `... errors` |
| `sources/adeck_ocd5_tau48.csv` | every OCD5 TAU-48 line of the event storms' a-decks, with line numbers | `... adeck` |
| `sources/fema_qualifying.csv` | OpenFEMA v2 DR/EM records, incident begin 2015-01-01 to 2026-01-10, type qualifying for HU+TS (amendment 5) | `... fema` |
| `sources/gis_advisories.csv` | NHC GIS advisory zips fetched per storm in listing order up to and including the one with a TS/hurricane watch or warning; `ADVDATE`, `TCWW` codes, SHA-256 | `... gis` |
| `sources/wiki/*.json` | MediaWiki query, earliest revision and pageview responses per event; `api_help.json` | `scripts/fetch_loop_wiki.py` in workflow `loop_wiki_fetch.yml` |

## Columns

- **ev_** event: ATCF id, name, season, t0 (UTC), landfall entity k, HURDAT2 line of t0, status, V (kt), minimum pressure (mb; sensitivity only), R64 (n mi; −999 or TS → 0, flag), distance to the entity (km; 0 = inside), number of qualifying US landfalls, HU-only flag with its own t0 and entity (secondary set; its FEMA matching would use code H only: `dc_dr_type_hu_only`).
- **dc_** decide-act: match status and rule (title / window), chosen DR (number, dates, region), Y_state = request − date(t0), Y_fed = declaration − request (days), number of DRs matched, EM numbers and dates, EMpre, `incidentType` strings of the matched records, type route (code / fallback, amendment 5), DR/EM `incidentId` differ flag.
- **pr_** predict: F (track skill vs OCD5, amendments 4 and 6), intensity skill (for session 2.7; enters no test), lines used, summed 48-h equivalent sample size.
- **at_** attend: target article, its kind (storm / list / season; descriptive flag: §3.3 accepts a non-disambiguation list or season page as T2 target), rule (T1/T2/T3), candidate titles redirecting to it, creation time, views over the three UTC days before date(t0), A = log10(1 + views), wiki file.
- **wn_** warnings: advisory file, issuance (`ADVDATE`, UTC), `TCWW` codes, W = t0 − issuance (hours).
- **exclusions**: `link:reason` list; reasons below.

## Exclusion reasons

`no_candidate`, `ambiguous`, `no_dr`, `dr_request_missing`, `y_fed_negative` (decide); `f_no_lines`, `f_ess_lt2` (predict); `a_no_article`, `a_fetch_missing` (attend); `w_no_ww`, `w_no_gis` (warnings). Texts: `emo/loop_hurricanes.py` `REASONS`.

## Rebuild and check

```
python scripts/fetch_loop_hurricanes.py hurdat2 census errors adeck fema gis   # refetch (current vintages may differ)
python scripts/build_loop_table.py
python scripts/validate_loop_table.py   # SHA-256 of sources, byte-identical rebuild, every value traced to its source row
```

`tests/test_loop_hurricanes.py` runs the validator and checks that no H4/H5 output exists.
