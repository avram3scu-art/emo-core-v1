# EMO weekly run, 2026-10-26

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
- `rdl_v04_test` not run: needs the Oslo-Seattle / IRD component file (requested 20 Oct 2026, not received).

## Analyses

- `dac_ozone`: unchanged since 2026-10-23
- `dac_compare_ozone_climate`: changed since 2026-10-23

```diff
--- 2026-10-23
+++ 2026-10-26
@@ -4 +4 @@
-Climate                18.3       +8%      +29%      +48%       +58% (2024)
+Climate                18.4       +8%      +29%      +48%       +58% (2024)
@@ -7 +7,3 @@
-Climate: 50% cut from 1997 baseline not reached; emissions not yet past their peak.
+Climate: the highest emissions year is the latest year in the data; no peak yet observed.
+Scope: Montreal bound all parties; Kyoto bound only listed developed countries, while delivery
+here is world CO2. The two rows are the same arithmetic, not equally binding commitments.
```

- `organismality_plane`: unchanged since 2026-10-23
- `information_time_nhc`: changed since 2026-10-23

```diff
--- 2026-10-23
+++ 2026-10-26
@@ -8,0 +9,9 @@
+
+[robust] 95% CI from a moving-block bootstrap (block 5 years, 2000 resamples), which allows for autocorrelated years; same point estimates as above:
+  12h    2.33%/yr  [ 2.04,  2.62]  improvement still demonstrated: True
+  24h    3.05%/yr  [ 2.69,  3.41]  improvement still demonstrated: True
+  36h    3.95%/yr  [ 3.61,  4.31]  improvement still demonstrated: True
+  48h    3.63%/yr  [ 3.34,  3.91]  improvement still demonstrated: True
+  72h    3.71%/yr  [ 3.43,  3.99]  improvement still demonstrated: True
+  96h    3.65%/yr  [ 3.30,  4.11]  improvement still demonstrated: True
+ 120h    3.06%/yr  [ 2.68,  3.51]  improvement still demonstrated: True
```

- `score_forecast_ledger`: unchanged since 2026-10-23

## Tests

- pytest: 57 passed in 8.88s
