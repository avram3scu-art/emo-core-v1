# EMO weekly run, 2026-10-28

**Result: all checks passed**

## Data refresh

| file | status | changed | rows |
|---|---|---|---|
| owid_annual_co2_emissions.csv | ok | no | 29384 |
| owid_ozone_depleting_substance_consumption.csv | ok | no | 5642 |
| owid_foreign_aid_share_of_gni.csv | ok | no | 2114 |
| owid_ucdp_death_rate_armed_conflicts.csv | ok | no | 7561 |
| openalex_articles_multicountry_by_year.json | ok | yes | 200 |
| openalex_articles_anycountry_by_year.json | ok | yes | 200 |
| openalex_articles_multicountry_by_year_excl_CN_ID.json | ok | yes | 200 |
| openalex_articles_anycountry_by_year_excl_CN_ID.json | ok | yes | 200 |
| openalex_single_country_2020_by_country.json | ok | yes | 200 |
| openalex_single_country_2025_by_country.json | ok | yes | 200 |
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
- `rdl_v04_test` not run: needs the Oslo-Seattle / IRD component file (requested 20 Oct 2026, not received).

## Analyses

- `dac_ozone`: unchanged since 2026-10-27
- `dac_compare_ozone_climate`: unchanged since 2026-10-27
- `organismality_plane`: unchanged since 2026-10-27
  - figure `analysis/organismality_plane.png` changed; copy kept in this folder
- `information_time_nhc`: unchanged since 2026-10-27
- `score_forecast_ledger`: unchanged since 2026-10-27

## Tests

- pytest: 91 passed in 15.08s
