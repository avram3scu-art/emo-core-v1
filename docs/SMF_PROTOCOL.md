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

**Result.** Single run 2026-10-23: Action 39944422318, code b5ed83b, data and
output 9cb5ded (`results/smf_steo_h18/result.txt`). 90 of 90 editions used.

**FAIL** on all three conditions. Primary (n = 78): corr −0.214, SMF 0,
p = 0.857 (p_min 0.024), MSE_model / MSE_zero = 1.239. Full sample (n = 90,
no weight): corr 0.026, p = 0.56, MSE ratio 1.093, also FAIL; at 18 months
even the pandemic swing is not foreseen.

**Profile across §8–§9 (primary samples):** lead 3 PASS, 6 PASS, 12 FAIL,
18 FAIL. At 18 months the forecasts are 24% worse than "no change".

## 10. Second STEO variable: electricity retail sales (pre-registration)

Registered 2026-10-23 after §9, at Adrian's request. Question: is the CO2
profile (§8: PASS at 3 and 6 months, FAIL at 12) specific to CO2, or does
EIA's model of US electricity use show the same horizon? Same forecaster, so
this does not answer whether the decay is general beyond EIA. Electricity is
not independent of CO2 (power plants are part of energy CO2).

**Layout checked beforehand, values never opened:** run 39946118805
(`scripts/probe_steo_elec_layout.py`). STEO table 7a, retail sales row:
`EXTCPUS` in billion kWh per day (January 2010), `ELTCTWH` in billion kWh
(January 2020, October 2026). MER Table 7.6
(`https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T07.06`),
Description "Electricity Sales to Ultimate Customers, Total", million kWh.

**Series.** As §8 with F_e = the 7atab retail-sales row: `ELTCTWH` if
present, otherwise `EXTCPUS` multiplied by the number of days in its month
(per-day → monthly total). realised = MER 7.6 total, monthly rows only.
Leads h ∈ {3, 6, 12}; editions January 2010 to P = June 2026 − h; an edition
lacking the row or a needed month is dropped for that lead; >10% dropped →
that lead not run.

**Sample, benchmark, statistic, pass / fail:** exactly §8 (without T in
2020-03..2021-12; "no change"; `compute_smf(..., max_lag_days=0,
n_surrogates=999, seed=0)`; PASS_h if p < 0.0167, SMF > 0 and
MSE_model < MSE_zero). Full sample reported, no weight.

**Comparison (stated before the run).** "Same horizon as CO2" if the
electricity profile is PASS at 3 and 6, FAIL at 12. Any other profile is
reported as "differs", with the leads that differ.

**Result.** Single run 2026-10-23: Action 39946280348, code 427966a, data and
output 7031a64 (`results/smf_steo_elec/result.txt`). No edition dropped
(EXTCPUS in 345 rows, ELTCTWH in 228).

| lead h | n | corr | SMF | p (p_min) | MSE_model / MSE_zero | verdict |
|---|---|---|---|---|---|---|
| 3 | 173 | 0.573 | 0.499 | 0.0112 (0.0112) | 0.638 | **PASS** |
| 6 | 170 | 0.535 | 0.461 | 0.0114 (0.0114) | 0.698 | **PASS** |
| 12 | 164 | 0.062 | 0.000 | 0.191 (0.0119) | 1.119 | **FAIL** (all three) |

Full sample, no weight: PASS at 3 and 6, FAIL at 12.

**Comparison: same horizon as CO2** by the rule stated above. EIA's forecasts
of US electricity sales track 12-month changes at 3 and 6 months and beat "no
change" (MSE −36% and −30%); at 12 months they are uncorrelated and 12%
worse than "no change". The decay within a year holds for two EIA variables;
whether it holds beyond EIA is untested (§8 note; no second forecaster found).

## 11. A forecaster other than EIA: Survey of Professional Forecasters (pre-registration)

Registered 2026-10-23 after §10, at Adrian's request. Question: is the loss
of fidelity within a year (§8–§10) specific to EIA? No second CO2 or energy
forecaster with archived machine-readable monthly editions was found
(`docs/STATUS.md`, session 7). The nearest candidate is a different forecaster
of a different US quantity: the median forecast of the US unemployment rate
in the Philadelphia Fed's Survey of Professional Forecasters (SPF), quarterly
since 1968. This changes both forecaster and variable; a difference from EIA
cannot be attributed to either alone.

**Layout checked beforehand, values never opened:** run 39948050223
(`scripts/probe_spf_layout.py`). `medianLevel.xlsx`
(`https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/historical-data/medianLevel.xlsx?sc_lang=en&hash=E52F5DEF4551C3EBD24031A04CE6E98A`),
sheet UNEMP: YEAR, QUARTER, UNEMP1..UNEMP6, surveys 1968Q4 to 2026Q3, 232
rows (UNEMP6 missing in 5). Realised: FRED UNRATE
(`https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE`), monthly
1948-01 to 2026-09. Prior expectation (from general knowledge, unverified):
short-horizon unemployment forecasts are usually skilful.

**Series.** Survey in quarter q. UNEMP1 is the forecasters' value for q − 1
(last observed), UNEMP3, UNEMP4, UNEMP6 the forecasts for q + 1, q + 2,
q + 4. R = quarterly mean of monthly UNRATE (current vintage). For
h ∈ {1, 2, 4} quarters (≈ 3, 6, 12 months), target T = q + h:
model_h(T) = UNEMP(h+2) − UNEMP1; realised(T) = R(T) − R(q − 1). Changes in
percentage points; the rate is seasonally adjusted, so no seasonal step.
Surveys 1968Q4 onward with T ≤ 2026Q3; a survey missing a needed value is
dropped for that horizon (>10% dropped → not run).

**Sample, benchmark, statistic, pass / fail:** as §8. Primary sample without
T in 2020Q1..2021Q4; benchmark "no change" (MSE_zero = mean(realised²));
`compute_smf(model, realised, max_lag_days=0, n_surrogates=999, seed=0)`;
PASS_h if p < 0.0167, SMF > 0 and MSE_model < MSE_zero. Reported, no weight:
full sample; surveys 2010Q1 onward only (EIA's period; expected too short to
reach p < 0.0167).

**Comparison (stated before the run).** "Same horizon as EIA" if PASS at 1
and 2 quarters and FAIL at 4. Any other profile is reported as "differs",
with the horizons that differ.

**Result.** Single run 2026-10-23: Action 39948229129, code 8aa3234, data and
output 8baf911 (`results/smf_spf/result.txt`). Dropped: 0, 0, 5 surveys
(the 5 early surveys without UNEMP6; 2% < 10%).

| horizon | n | corr | SMF | p (p_min) | MSE_model / MSE_zero | verdict |
|---|---|---|---|---|---|---|
| 1 quarter | 223 | 0.853 | 0.801 | 0.0087 (0.0087) | 0.309 | **PASS** |
| 2 quarters | 222 | 0.815 | 0.748 | 0.0088 (0.0088) | 0.377 | **PASS** |
| 4 quarters | 215 | 0.753 | 0.678 | 0.0090 (0.0090) | 0.490 | **PASS** |

Primary sample (without 2020Q1..2021Q4). Full sample, no weight: PASS at all
three (corr 0.66, 0.64, 0.68). Surveys from 2010Q1 only, no weight: corr
0.82, 0.88, 0.92, MSE ratio 0.29, 0.24, 0.21, but p = 0.031–0.032 = p_min
(n ≈ 56), so FAIL on the p condition, as expected.

**Comparison: differs** by the rule stated above, at 4 quarters: the SPF
keeps fidelity at about 12 months (r = 0.75, MSE 51% below "no change"),
where EIA's CO2 and electricity forecasts had none. The decay within a year
is therefore not a general property of forecasters; it holds for EIA's two
energy variables. Because forecaster and variable both changed, this run
cannot say whether the difference comes from the forecaster or from
unemployment being easier to forecast a year ahead (its changes are
persistent, while energy use swings with weather and prices). "No change" is
also a weaker benchmark for a persistent series.

## 12. Separating forecaster from variable: industrial production (pre-registration)

Registered 2026-10-23 after §11, at Adrian's request. §11 changed forecaster
and variable at once. Here both forecasters forecast the same variable, US
total industrial production (IP):

| | energy (CO2, electricity) | unemployment | industrial production |
|---|---|---|---|
| EIA STEO | §8, §10: fidelity lost by 12 months | – | **this test** |
| SPF | – | §11: kept at 4 quarters | **this test** |

**Layout checked beforehand, values never opened:** run 39948495201
(`scripts/probe_ip_layout.py`): STEO sheet 9atab row `ZOTOIUS` "Total
Industrial Production" in January 2010, 2015, 2020 and October 2026 (index
base year changes between editions). The SPF and FRED lines of that probe were
cut off in the annotation; the SPF sheet `INDPROD` is assumed to follow the
UNEMP layout (INDPROD1..INDPROD6); if it does not, that forecaster is not run
and this is recorded. Realised: FRED INDPRO
(`https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDPRO`), monthly, current
vintage. Caveat: STEO's macro forecasts are built on an outside macroeconomic
model (S&P Global, per STEO documentation; unverified this session), so
"EIA" here means the forecast EIA publishes, not necessarily EIA's own model.

**EIA series:** as §8, with F_e = row `ZOTOIUS` and R = FRED INDPRO:
model(T) = ln F_e(T) − ln F_e(T − 12), realised(T) = ln R(T) − ln R(T − 12),
leads 3, 6, 12 months, editions January 2010 to P = June 2026 − h. Log
changes within one edition cancel its base year.

**SPF series:** as §11, in logs: model = ln INDPROD(h+2) − ln INDPROD1,
realised = ln R(T) − ln R(q − 1), R = quarterly mean of INDPRO (complete
quarters), horizons 1, 2, 4 quarters, surveys 1968Q4 onward, T ≤ 2026Q3.

**Sample, benchmark, statistic, pass / fail:** as §8 and §11, for each
forecaster separately: without T in 2020-03..2021-12 (EIA) or 2020Q1..2021Q4
(SPF); "no change"; `compute_smf(..., max_lag_days=0, n_surrogates=999,
seed=0)`; PASS_h if p < 0.0167, SMF > 0, MSE_model < MSE_zero; >10% dropped
→ not run. Full samples reported, no weight.

**Reading rule (stated before the run), on the 12-month / 4-quarter verdict:**
- EIA FAIL, SPF PASS → forecaster effect: on the same variable, EIA's
  published forecast loses fidelity within a year and the SPF does not.
- both FAIL → variable effect: IP, like energy, has no 12-month fidelity in
  either forecaster; the §11 difference came from unemployment.
- both PASS → EIA's energy failure is specific to energy variables.
- EIA PASS, SPF FAIL → reported as found, no reading.
Shorter leads are reported as profiles alongside.

**Result.** Single run 2026-10-23: Action 39948712388, code e3aef93, data and
output 2c18760 (`results/smf_ip/result.txt`). SPF sheet INDPROD matched the
assumed layout. Dropped: EIA 0; SPF 0, 0, 5.

| forecaster, lead | n | corr | SMF | p (p_min) | MSE_model / MSE_zero | verdict |
|---|---|---|---|---|---|---|
| EIA 3 months | 173 | 0.715 | 0.641 | 0.0112 (0.0112) | 0.496 | PASS |
| EIA 6 months | 170 | 0.562 | 0.420 | 0.0114 (0.0114) | 0.760 | PASS |
| EIA 12 months | 164 | 0.201 | 0.000 | 0.262 (0.0119) | 1.387 | **FAIL** |
| SPF 1 quarter | 223 | 0.682 | 0.605 | 0.0087 (0.0087) | 0.495 | PASS |
| SPF 2 quarters | 222 | 0.635 | 0.516 | 0.0088 (0.0088) | 0.560 | PASS |
| SPF 4 quarters | 215 | 0.588 | 0.510 | 0.0090 (0.0090) | 0.604 | **PASS** |

Primary samples (without 2020–21). **By the pre-registered rule: forecaster
effect** (EIA FAIL at 12 months, SPF PASS at 4 quarters, same variable).

**Exploratory checks, computed after the run, no weight** (not
pre-registered; the data were already open):

| SPF 4 quarters, without 2020–21 | n | corr | p (p_min) | MSE_model / MSE_zero |
|---|---|---|---|---|
| (i) §12 definition, surveys 2010Q1+ (EIA's period) | 55 | 0.418 | 0.032 (0.032) | 1.092 |
| (ii) change from the current quarter (ln INDPROD6 − ln INDPROD2), all surveys | 215 | 0.459 | 0.0090 (0.0090) | 0.742 |
| (iii) (ii), surveys 2010Q1+ | 55 | 0.335 | 0.032 (0.032) | 1.245 |

They weaken the reading. In EIA's period (i) the SPF also forecasts IP worse
than "no change" a year ahead, as EIA does; its 4-quarter pass rests on
1969–2009. And part of the SPF's skill comes from the quarter it partly
observes when surveyed: without it (ii) the margin over "no change" shrinks
from 40% to 26%. The two forecasters were not compared over the same period
with the same change definition, and that is the design flaw of §12. What
survives: on IP since 2010, neither forecaster beats "no change" at a year
(EIA pre-registered, SPF exploratory). A forecaster effect is not shown.
