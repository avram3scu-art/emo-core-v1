# EMO weekly run, 2026-10-30

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
- `loop_power` reproduces `analysis/loop_power_output.txt`.
- `loop_power_amend1` reproduces `analysis/loop_power_amend1_output.txt`.
- `loop_power_amend2` reproduces `analysis/loop_power_amend2_output.txt`.
- `loop_power_amend3` reproduces `analysis/loop_power_amend3_output.txt`.
- `gwi_v2_development` reproduces `analysis/gwi_v2_development_output.txt`.
- `gwi_v2_synthetic_quick` reproduces `analysis/gwi_v2_synthetic_quick_output.txt`.
- `smf_v2_power` reproduces `analysis/smf_v2_power_output.txt`.
- `he_loop_test` reproduces `analysis/he_loop_test_output.txt`.
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

- `dac_ozone`: unchanged since 2026-10-29
- `dac_compare_ozone_climate`: unchanged since 2026-10-29
- `organismality_plane`: unchanged since 2026-10-29
- `information_time_nhc`: unchanged since 2026-10-29
- `score_forecast_ledger`: unchanged since 2026-10-29

## Tests

- pytest: 273 passed, 36 warnings in 15.21s
