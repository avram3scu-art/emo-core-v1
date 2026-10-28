# DAC standard v1.1: event files, validator, profile

Turns the minimum reporting standard of the DAC manuscript into a machine-checked format.

- Schema: `docs/dac_event_file.schema.json` (structure; JSON Schema 2020-12)
- Validator and profile: `emo/dac_standard.py` (`validate_event_file`, `load_event_file`, `compute_profile`)
- Example (synthetic, not data): `docs/dac_event_file_example.json`
- Tests: `tests/dac_unit/test_dac_standard.py`

**Source of the fields.** v1.0 (26 Oct 2026) followed the reporting-standard table of an earlier manuscript version (`docs/sources/dac_manuscript_reporting_standard.md`). v1.1 (28 Oct 2026, fix session F7) follows Table S1 of the final manuscript "Decision or Supply?" (`docs/sources/dac_paper/Decision_or_Supply_supporting_information.docx`, supplied by Adrian in F1), which adds the **Identification** row, and fixes the validator gaps D1–D6 of `docs/AUDIT_2026-10-27.md`. v1.0 files are rejected; `scripts/convert_dac_csv.py` writes v1.1.

## 1. Table field → where it lives

| Manuscript field | In the event file | Checked by the validator |
|---|---|---|
| Validation (t0) | `case.t0_event_id`, `t0_institution`, `t0_rule`, `alternative_t0` | t0 event exists, is sublayer `validation`, every reading has an exact or window date |
| Response scale | `case.response_scale` | present |
| Start rule | `case.start_rule` | present |
| End point | `case.end_point`; `end_point` on every dated delivery; optional `end_point` (level) on a firm order, default the case's | present; deliveries and orders at other levels are reported as secondary end points; intervals compare orders and deliveries of the same level |
| Pairing | `pairs_with` on a delivery = `event_id` of the firm order it fulfils | target is a `firm_order`; delivery cannot end before its order can start; paired and unpaired intervals reported separately; a pair whose order or delivery date is missing is listed as undatable |
| Identification | `good` on firm orders and deliveries; `case.identification`: which explanations each test can eliminate | profile per good: number of paired orders, spread of their order dates, and whether separating decision-limited from supply-limited delay is possible (≥ 2 paired orders on different dates; Proposition 1 of the manuscript) |
| Inclusion rules | `case.inclusion_rules` {sublayer: rule} | every sublayer used (dated, missing or censored) has a rule |
| Event file | `events[]`: `event_id`, `sublayer`, `date_status`, dates, `description`, `source`, `source_type` | required, enumerated, no unknown fields (also none in `case` and its sub-objects); `standard_version` must be "1.1" |
| Imprecise and contested dates | `date_status` window / lower_bound / upper_bound with `source_wording`; contested dates as rows sharing `event_id` with distinct `reading` | wording required; window ordered; readings distinct, ≥ 2, same sublayer |
| Missing and censored | rows with `date_status` `missing` or `censored`, no dates | never imputed; keyed by sublayer **and end point** for orders and deliveries, so a dated EU-level delivery and a missing national delivery can coexist; a sublayer at one level cannot be both dated and missing/censored; an order or delivery named in a pair may be missing (event-level, listed as an undatable pair, not as a missing sublayer) |
| Source pool | `case.source_pool`: `searched`, `search_date`, `not_accessed`, `case_selection_reason` | present, date valid |
| Coding | `case.coding`: `coders`, `agreement`, `rules_fixed_before_coding` | coders ≥ 1; flag is boolean |
| Computation | `case.computation.code` | present |
| (Observation window) | `case.observation_window`: `start`, `end`, `reason` | every date inside it; later events must be coded `censored` |

The observation window comes from the older draft's table; kept because censoring cannot be defined without it.

## 2. Sublayers

`validation` (t0), `firm_order`, `binding_act`, `dedicated_funding`, `delivery`, `counter_measure`, `reversal`, `institutionalisation`, `persistence`, `context`. `context` rows (e.g. a tender that is not a firm order, acts of another level) are recorded and never enter the profile.

## 3. Profile (never a scalar)

`compute_profile` validates first, then returns, for each combination of readings of contested dates:

- per sublayer: lag from t0 to its first event as `{min_days, max_days}` over all dates consistent with windows and bounds (`null` = open end), the first event id(s), the number of events;
- per sublayer, orders and deliveries counted at the case's end point only;
- paired order-to-delivery intervals, one per paired delivery, with the order's and the delivery's level and the good;
- undatable pairs (order or delivery date missing or censored), with the reason;
- first order to first delivery at the case's end point, labelled unpaired;
- per secondary end point: lag to its first delivery and its own unpaired order-to-delivery interval;
- identification per good (see table).

Missing and censored sublayers are listed separately at the top level (`sublayer @ level` when the level is not the case's). No weighted sum, index or composite is computed; a test fails if any numeric field other than `min_days`, `max_days`, `n_events` or `n_paired_orders` appears.

**Range rule.** For a first event with bounds [e, l] and t0 with bounds [a, b]: lag ∈ [e − b, l − a]. An upper-bound-only date is floored at the window start; a lower-bound-only date has an open maximum.

## 4. Not covered (reasons)

- Agreement between coders is stored as text, not computed. Reason: scope (session 11).
- Counter-measure direction (restricting or easing) is in `description`, not a field. Reason: not attempted; add a field if a case needs it.
- The JSON Schema cannot express the cross-field rules; only the validator enforces them. A test keeps the schema's enums and required lists equal to the validator's.

## 5. Conversion check: ozone and climate (pre-registered 2026-10-26, before conversion)

**Purpose.** Show that the existing event files can be expressed in this standard and that the profile reproduces the warning-to-binding lag used by `analysis/dac_compare_ozone_climate.py`. This is a reproduction check, not a scientific test: the CSVs are already open and their values are on record.

**Data.** `data/dac_ozone_events.csv`, `data/dac_climate_events.csv` (unchanged). Converted by `scripts/convert_dac_csv.py` to `data/dac_ozone_events.json`, `data/dac_climate_events.json`.

**Mapping rules (fixed now).**
- t0: the first diagnostic event in the file (ozone `molina_rowland_1974`, climate `charney_1979`); other diagnostic events → `context`, listed in `alternative_t0`.
- `binding_act`: the treaty adoption with binding cuts named in the comparison script (`montreal_protocol`, `kyoto_adopted`). All other policy rows (frameworks without binding cuts, entry into force, phase-out deadlines, Paris) → `context`. No delivery is coded: the files contain no dated delivery events.
- Dates: `day_verified` → exact; `month_verified` → window over that calendar month; `year_verified` and `year_unverified` → window over that calendar year. `source_wording` records the original precision label.
- `source_type`: `primary` only if the source is the original document or official record; encyclopaedia and educational pages → `secondary`; empty source → row kept, source text "no source given", `secondary`.
- Coding: 1 coder; `rules_fixed_before_coding: false` (the CSVs were coded in earlier sessions). Window: 1 Jan of the t0 year to 26 Oct 2026.

**Statistic.** The binding_act `lag_from_t0` range; the exact-day lag implied by the CSV dates.

**Pass if** both converted files validate **and** each case's range contains the exact-day lag the comparison script uses. **Reported either way:** the range width, i.e. how much the "year-verified" precision of the warning dates widens the lag.

**Result (run 2026-10-26, after a4de996): PASS.**

| Case | Exact-day lag used by the comparison script | binding_act lag range (standard) |
|---|---|---|
| Ozone (Molina–Rowland → Montreal) | 4,828 d (13.2 y) | 4,642 – 5,006 d |
| Climate (Charney → Kyoto) | 6,712 d (18.4 y) | 6,555 – 6,919 d |

Both files validate. The year-level precision of both warning dates widens each lag by 364 days (about ±0.5 y); the comparison script's single values hide this. Every t0 and binding-act source in both files is secondary (encyclopaedia or educational pages); one context row (IPCC FAR) has no source. Neither weakens the ~5-year difference between the cases, but both would have to be fixed before the files met the standard's spirit, not only its format.

## 6. Primary sources for the ozone and climate t0 and binding acts (rules fixed 2026-10-28, F7, before any source was opened)

**Rows:** ozone `molina_rowland_1974` (t0), `montreal_protocol` (binding act); climate `charney_1979` (t0), `kyoto_adopted` (binding act). Other rows keep their sources (out of the F7 prompt's scope).

**Source rule.** Each row's `source` becomes a primary record opened in this session, cited with URL and access date in `data/sources/dac_primary_sources.md`: the journal's own article page (DOI) for Molina & Rowland; the National Academies record of the Charney report; the treaty text or the depositary's (UN Treaty Collection) or secretariat's record for the Montreal and Kyoto Protocols. `source_type` becomes `primary` only if such a record was opened; otherwise the row keeps its old source, stays `secondary`, and the failure is recorded.

**Date rule.** The date is the one the primary record states: for the article, its publication date in the journal issue; for the report, the date printed on or recorded for it; for a treaty, its adoption (conclusion) date. Precision follows the record: day if the record states the day, month or year otherwise (same window rule as §5). A date is changed in the CSV only if the record contradicts it or makes it more precise; every change is listed in that file.

**Reported either way (not a test).** The new binding_act lag ranges for both cases and whether the §5 exact-day lags (4,828 d; 6,712 d) still lie inside them. Since precision may rise, ranges may narrow; this is a correction of coding, not a result.
