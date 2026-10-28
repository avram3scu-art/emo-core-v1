# EMO weekly run, 2026-10-28

**Result: all checks passed**

## Data refresh

| file | status | changed | rows |
|---|---|---|---|
| owid_annual_co2_emissions.csv | ok | no | 29384 |
| owid_ozone_depleting_substance_consumption.csv | ok | no | 5642 |
| owid_foreign_aid_share_of_gni.csv | ok | no | 2114 |
| owid_ucdp_death_rate_armed_conflicts.csv | ok | no | 7561 |
| openalex_articles_multicountry_by_year.json | ok | no | 200 |
| openalex_articles_anycountry_by_year.json | ok | no | 200 |
| openalex_articles_multicountry_by_year_excl_CN_ID.json | ok | no | 200 |
| openalex_articles_anycountry_by_year_excl_CN_ID.json | ok | no | 200 |
| openalex_single_country_2020_by_country.json | ok | no | 200 |
| openalex_single_country_2025_by_country.json | ok | no | 200 |
| hurdat2_atlantic.txt | ok | no | 1988 |
| wikipedia_pageviews_gwi.csv | ok | no | 89136 |
| wikipedia_pageviews_gwi_calibration.csv | ok | no | 104289 |

Not refreshed by design (manual or hand-coded): NHC track errors, DAC event dates, forecast ledger.

## Frozen records

- Forecast ledger sha256 matches the archived hash (677eaf342898…).
- `rdl_backtest_run` reproduces `analysis/rdl_backtest_run_output.txt`.
- `rdl_backtest_heldout` reproduces `analysis/rdl_backtest_heldout_output.txt`.
- `rdl_v03_development` reproduces `analysis/rdl_v03_development_output_run2.txt`.
- `rdl_v03_heldout` reproduces `analysis/rdl_v03_heldout_output.txt`.
- `gwi_hurricanes` reproduces `analysis/gwi_hurricanes_output.txt`.
- `gwi_calibration` reproduces `analysis/gwi_calibration_output.txt`.
- `he_calibration` reproduces `analysis/he_calibration_output.txt`.
- `smf_steo` reproduces `results/smf_steo/result.txt`.
- `smf_steo_leads` reproduces `results/smf_steo_leads/result.txt`.
- `smf_steo_h18` reproduces `results/smf_steo_h18/result.txt`.
- `smf_steo_elec` reproduces `results/smf_steo_elec/result.txt`.
- `smf_spf` reproduces `results/smf_spf/result.txt`.
- `smf_ip` reproduces `results/smf_ip/result.txt`.
- `smf_dm` reproduces `results/smf_dm/result.txt`.
- `synergy_climate` reproduces `results/synergy_climate/result.txt`.
- `rdl_v04_test` not run: needs the Oslo-Seattle / IRD component file (requested 20 Oct 2026, not received).

## Analyses

- `dac_ozone`: changed since 2026-10-27

```diff
--- 2026-10-27
+++ 2026-10-28
@@ -1,3 +1,3 @@
-Warning -> binding policy (Montreal Protocol, 1987-09-16):
-  molina_rowland_1974     13.2 years  (year_verified)
-  farman_1985              2.4 years  (month_verified)
+Warning -> binding policy (montreal_protocol, 1987-09-16), days (min-max over consistent dates):
+  molina_rowland_1974     4828- 4828 d  (13.2-13.2 y; t0 known 1974-06-28..1974-06-28)
+  farman_1985              838-  868 d  (2.3-2.4 y; t0 known 1985-05-01..1985-05-31)
@@ -5,4 +5,4 @@
-Delivery: world CFC + halon consumption, 1986 baseline 1,302,532 ODP t
-  50% reduction reached in 1993: 6 yr after policy, 19 yr after first warning
-  90% reduction reached in 2001: 14 yr after policy, 27 yr after first warning
-  99% reduction reached in 2008: 21 yr after policy, 34 yr after first warning
+Delivery: world CFC + halon consumption, 1986 baseline 1,302,532 ODP t (year precision)
+  50% reduction reached in 1993: 6 yr after policy year, 19 yr after first-warning year
+  90% reduction reached in 2001: 14 yr after policy year, 27 yr after first-warning year
+  99% reduction reached in 2008: 21 yr after policy year, 34 yr after first-warning year
```

- `dac_compare_ozone_climate`: unchanged since 2026-10-27
- `organismality_plane`: unchanged since 2026-10-27
- `information_time_nhc`: unchanged since 2026-10-27
- `score_forecast_ledger`: unchanged since 2026-10-27

## Tests

- pytest: 100 passed in 11.04s
