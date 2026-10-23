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

Single run 2026-10-23: Action 39941453995, code 1677108, data and output
7fc7696 (`results/smf_steo/result.txt`). 186 of 186 editions parsed, none
dropped (FFTCCO2 in 67, TETCCO2 in 119). Values checked for plausibility
only (monthly totals 322–534 Mt).

**Verdict: PASS** by the pre-registered rule.

| | primary (n = 186) | without 2020-03..2021-12 (n = 164, no weight) |
|---|---|---|
| corr (model, realised) | 0.393 | −0.006 |
| null_corr_95 | 0.168 | 0.202 |
| SMF | 0.271 | 0.000 |
| p (n_null, p_min) | 0.0104 (95, 0.0104) | 0.345 (83, 0.0119) |
| MSE_model / MSE_naive | 0.345 | 0.417 |
| naive vs realised corr | −0.301 | −0.188 |
| verdict by §6 | PASS | FAIL (p, SMF) |

**What the pass rests on.** Outside the pandemic months the forecasts'
12-month changes are uncorrelated with what happened (r = −0.006). The whole
correlation comes from 2020–21: editions from spring 2020 forecast the 2021
rebound. The pass therefore shows that SMF detects one large, foreseen
swing, not that EIA tracks ordinary year-to-year variation.

**Benchmark weaker than intended.** Persistence is anti-correlated with the
outcome (12-month changes revert), so beating it on MSE (condition 3) was
easy in both samples. A "no change" forecast (naive = 0) would have been the
stronger benchmark; it was not pre-registered and was not computed.

**p at its floor.** p = 0.0104 equals p_min: with n = 186, `smf.py` admits
95 distinct shifts, and none reached the observed correlation.

## 8. Follow-up test: other leads and a "no change" benchmark (pre-registration)

Registered 2026-10-23 after §7, at Adrian's request. **Not blind:** the STEO
and MER values for lead 12 were opened in §7, and its result without
2020–21 (r = −0.006) is known. Leads 3 and 6 and the "no change" benchmark
have not been computed. Nothing in §2–§7 is changed.

**Question.** Outside the pandemic swing, do EIA's forecasts track realised
12-month changes better than chance and better than forecasting no change?

**Series.** For edition e (published month P) and lead h ∈ {3, 6, 12}:
target T = P + h; model_h(T) = ln F_e(T) − ln F_e(T − 12);
realised(T) = ln R(T) − ln R(T − 12); same sources and row rule as §3.
For h = 12 this is §4's series. Editions January 2010 to P = June 2026 − h
(so T ≤ 2026-06). An edition lacking a needed month is dropped for that lead;
more than 10% dropped for a lead → that lead is not run (§4 rule).

**Primary sample.** T outside 2020-03..2021-12.

**Benchmark.** No change: zero(T) = 0, MSE_zero = mean(realised²).

**Statistic.** `compute_smf(model_h, realised, max_lag_days=0, n_surrogates=999, seed=0)`.

**Pass / fail, per lead (three tests, Bonferroni α = 0.05/3 = 0.0167):**
PASS_h if p < 0.0167, SMF > 0 and MSE_model < MSE_zero. Reported as a profile
of three verdicts, never combined into one score. Also reported, no weight:
the full sample (with 2020–21) for each lead, and the §6 persistence MSE.

**Result.** Single run 2026-10-23: Action 39942987695, code 30a0a48, data and
output c32cfa9 (`results/smf_steo_leads/result.txt`). No edition dropped
for any lead. Lead 12 reproduces §7 exactly (parser cross-check).

| lead h | n | corr | SMF | p (p_min) | MSE_model / MSE_zero | verdict |
|---|---|---|---|---|---|---|
| 3 | 173 | 0.532 | 0.466 | 0.0112 (0.0112) | 0.758 | **PASS** |
| 6 | 170 | 0.518 | 0.450 | 0.0114 (0.0114) | 0.809 | **PASS** |
| 12 | 164 | −0.006 | 0.000 | 0.345 (0.0119) | 1.185 | **FAIL** (all three) |

Primary sample (without 2020-03..2021-12). Full sample, no weight: PASS at
all three leads (corr 0.64, 0.61, 0.39).

**Reading.** SMF detects real fidelity at 3 and 6 months: EIA's forecasts
track ordinary 12-month changes and beat "no change", by 24% and 19% in MSE.
At 12 months, outside the pandemic, the forecasts are worse than "no change"
(MSE 18% higher) and uncorrelated with the outcome. The §7 pass at lead 12
was the pandemic swing. Fidelity of this self-model decays to zero within a
year. p sits at p_min for leads 3 and 6: no shift reached the observed
correlation; with ~87 distinct shifts the p-value cannot go lower.

## 9. Lead 18 months (pre-registration)

Registered 2026-10-23 after §8, at Adrian's request. Not blind: lead 12
failed outside 2020–21 (§8), so a fail at 18 months is the expected outcome;
the test records it rather than assume it. Lead-18 values not yet computed.

**Editions.** Only January–June editions reach 18 months (a STEO forecasts to
December of the next year). Editions January–June of 2010–2024 (T ≤ 2026-06),
90 expected; >10% dropped → not run.

**Series, sample, benchmark, statistic:** as §8 with h = 18
(model(T) = ln F_e(T) − ln F_e(T − 12), T = P + 18, T − 12 = P + 6); primary
sample without T in 2020-03..2021-12; benchmark "no change";
`compute_smf(..., max_lag_days=0, n_surrogates=999, seed=0)`. The series holds
only July–December target months, taken in time order; the circular shift runs
over that order.

**Pass / fail.** One new test, α = 0.05: PASS if p < 0.05, SMF > 0 and
MSE_model < MSE_zero. Full sample reported, no weight. Expected p_min ≈ 0.024
(n ≈ 78).

**Result.** Not yet run.
