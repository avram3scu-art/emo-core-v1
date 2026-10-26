# DAC standard v1.0: event files, validator, profile

Turns the minimum reporting standard of the DAC manuscript into a machine-checked format.

- Schema: `docs/dac_event_file.schema.json` (structure; JSON Schema 2020-12)
- Validator and profile: `emo/dac_standard.py` (`validate_event_file`, `load_event_file`, `compute_profile`)
- Example (synthetic, not data): `docs/dac_event_file_example.json`
- Tests: `tests/dac_unit/test_dac_standard.py`

**Source of the fields.** The reporting-standard table of the DAC manuscript as last revised on 20 Oct 2026 (`manuscript_v2_anon.md`, where it is numbered Table 3; an earlier draft numbered it Table 4 and lacked the end-point and pairing rows). Read from the session record of that revision, not from a file in this repository; the manuscript is not in the repo.

## 1. Table field → where it lives

| Manuscript field | In the event file | Checked by the validator |
|---|---|---|
| Validation (t0) | `case.t0_event_id`, `t0_institution`, `t0_rule`, `alternative_t0` | t0 event exists, is sublayer `validation`, has an exact or window date |
| Response scale | `case.response_scale` | present |
| Start rule | `case.start_rule` | present |
| End point | `case.end_point`; `end_point` on every dated delivery | present; deliveries at other levels are reported as secondary end points |
| Pairing | `pairs_with` on a delivery = `event_id` of the firm order it fulfils | target is a `firm_order`; delivery cannot end before its order can start; paired and unpaired intervals reported separately |
| Inclusion rules | `case.inclusion_rules` {sublayer: rule} | every sublayer used (dated, missing or censored) has a rule |
| Event file | `events[]`: `event_id`, `sublayer`, `date_status`, dates, `description`, `source`, `source_type` | required, enumerated, no unknown fields |
| Imprecise and contested dates | `date_status` window / lower_bound / upper_bound with `source_wording`; contested dates as rows sharing `event_id` with distinct `reading` | wording required; window ordered; readings distinct, ≥ 2, same sublayer |
| Missing and censored | rows with `date_status` `missing` or `censored`, no dates | never imputed; a sublayer cannot be both dated and missing/censored |
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
- paired order-to-delivery intervals, one per paired delivery;
- first order to first delivery, labelled unpaired;
- lags to deliveries at secondary end points.

Missing and censored sublayers are listed separately at the top level. No weighted sum, index or composite is computed; a test fails if any numeric field other than `min_days`, `max_days` or `n_events` appears.

**Range rule.** For a first event with bounds [e, l] and t0 with bounds [a, b]: lag ∈ [e − b, l − a]. An upper-bound-only date is floored at the window start; a lower-bound-only date has an open maximum.

## 4. Not covered (reasons)

- Agreement between coders is stored as text, not computed. Reason: scope (session 11).
- Existing `data/dac_ozone_events.csv` and `data/dac_climate_events.csv` are not in this format. Reason: scope (one task per session).
- Counter-measure direction (restricting or easing) is in `description`, not a field. Reason: not attempted; add a field if a case needs it.
- The JSON Schema cannot express the cross-field rules; only the validator enforces them. A test keeps the schema's enums and required lists equal to the validator's.
