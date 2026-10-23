# EMO weekly run, 2026-10-23

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

Not refreshed by design (manual or hand-coded): NHC track errors, DAC event dates, forecast ledger.

## Frozen records

- Forecast ledger sha256 matches the archived hash (677eaf342898…).
- `rdl_backtest_run` reproduces `analysis/rdl_backtest_run_output.txt`.
- `rdl_backtest_heldout` reproduces `analysis/rdl_backtest_heldout_output.txt`.
- `rdl_v03_development` reproduces `analysis/rdl_v03_development_output_run2.txt`.
- `rdl_v03_heldout` reproduces `analysis/rdl_v03_heldout_output.txt`.
- `rdl_v04_test` not run: needs the Oslo-Seattle / IRD component file (requested 20 Oct 2026, not received).

## Analyses

- `dac_ozone`: unchanged since 2026-10-21
- `dac_compare_ozone_climate`: unchanged since 2026-10-21
- `organismality_plane`: unchanged since 2026-10-21
- `information_time_nhc`: unchanged since 2026-10-21
  - figure `analysis/information_time_nhc.png` changed; copy kept in this folder
- `score_forecast_ledger`: unchanged since 2026-10-21

Note: the subtitle of `dac_ozone_vs_climate.png` states fixed percentages (ozone -99 % in 20 years, CO₂ +48 %). If `dac_compare_ozone_climate` changed, check that text.

## Tests

- pytest: 96 passed, 1 warning in 8.06s
