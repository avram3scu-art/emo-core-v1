# SMF on a real case: pre-registration

Session 7 (`docs/PLAN.md`), redefined 2026-10-23 with Adrian's approval: the
realised series is EIA monthly CO2, not OWID annual CO2 (§1). Code:
`emo/smf.py` v1.2 (9dc38eb). This file is committed before any data value is
fetched or opened; §7 is filled in after the single run.

## 1. Why not OWID annual CO2

A circular-shift null on annual data needs at least 38 points to reach
p < 0.05 (`emo/smf.py` v1.2, `extra["p_min"]`), and no published annual
emissions path covers 38 realised years. Recorded in `docs/STATUS.md`
(session 7).

## 2. Hypothesis

H1: the forecasts of the US Energy Information Administration (EIA) for US
energy CO2 emissions track the realised emissions 12 months later better than
chance. Under the null, forecast and outcome are unrelated, apart from each
series' own autocorrelation.

Scope: this is EIA's model of the US energy system, built and checked by
the same agency. It is not the US's, nor humanity's, model of itself. A pass
says SMF detects fidelity in one agency forecaster; nothing wider.

## 3. Data

**Self-model (model).** EIA Short-Term Energy Outlook (STEO), monthly editions
January 2010 to June 2025, from
`https://www.eia.gov/outlooks/steo/archives/{mon}{yy}_base.xlsx`, falling back
to `.xls` when `.xlsx` is missing. Sheet `9atab`, total CO2 row: `TETCCO2` if
present, otherwise `FFTCCO2`. Each edition uses one code for both of its
values (§4), so the code change cancels.

**Realised.** EIA Monthly Energy Review, Table 11.1,
`https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T11.01`,
Description "Total Energy CO2 Emissions", monthly rows only (YYYYMM not ending
in 13). The vintage is the one fetched on the run date; EIA revises past
months, and the forecasts are judged against today's numbers, not those known
at the time.

**Layout checked beforehand, values never opened:** runs 39940687789 and
39940799124 (`scripts/probe_steo_layout.py`) printed only sheet names, row
codes and column names. Total CO2 is in table 9a in the January 2010, 2013 and
2026 editions; it is missing in January 2008 and 2009. The analyst knows the
broad history of US emissions (including the 2020 drop), not the paired
values used here.

## 4. Series

For each edition e, published in month P:

- target month T = P + 12 months;
- model(T) = ln F_e(T) − ln F_e(P), where F_e is edition e's value of the
  total CO2 row (F_e(P) is that edition's estimate for its own month);
- realised(T) = ln R(T) − ln R(P), where R is the MER total.

Both are 12-month log changes of the same two calendar months, so the shared
seasonal cycle and any constant level difference between STEO and MER
definitions cancel. Index: T from 2011-01 to 2026-06, about 186 points.

**Parsing rule.** The column for a month is located from the year and month
header rows of `9atab`. An edition that cannot be fetched or parsed is dropped
and listed in the output. If more than 10% of editions are dropped, the test
is not run; that is recorded, the parser may be fixed for layout only, and
the run repeated with every choice in this file unchanged.

## 5. Statistic

`compute_smf(model, realised, max_lag_days=0, n_surrogates=999, seed=0)`.
Lag fixed at 0, because the lead is fixed by design (§4).

## 6. Pass / fail

Persistence benchmark: naive(T) = ln R(P) − ln R(P − 12), the 12-month change
last observed at publication (current MER vintage). Errors are computed on the
months T where model, naive and realised all exist:
MSE_model = mean((model − realised)²), MSE_naive = mean((naive − realised)²).

**PASS** if all three hold:

1. p_value < 0.05 (one-sided, as computed by `compute_smf`);
2. smf_score > 0;
3. MSE_model < MSE_naive (STEO beats persistence; chosen by Adrian on
   2026-10-23 so that a pass cannot come from the autocorrelation of emissions
   growth alone).

Otherwise **FAIL**, and the file says which condition failed.

Reported either way: n, best_corr, null_corr_95, smf_score, p_value, n_null,
p_min, MSE_model, MSE_naive, SMF of naive vs realised, dropped editions.

**Secondary, reported, no weight on the verdict:** the same three numbers
(p, SMF, MSE ratio) with T from 2020-03 to 2021-12 removed. If the verdict
holds only with these months, this is said.

## 7. Result

Not yet run.
