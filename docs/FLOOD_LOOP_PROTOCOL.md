# Flood loop (EU): data definitions registered; test statistic not yet registrable

**First line (power and validity rule):** two tests are registered here, both with power below 0.5 at the expected size, so a FAIL reads "not shown at this size": (1) §10, news pressure → activation (H4 in floods, replaces the retired attention arm; error rate 0.034–0.052, power 0.06–0.34 at N 20–45); (2) §11, lag measurability (H3 in floods; wrong-pass rate ≤ 0.033, power 0.47–0.91 at N 20–45 if 90% of lags are measurable, 0.25–0.65 if 80%). The attention-residual tests (§4, §8, §9) failed their synthetic checks and the attention arm A → Y is retired (Adrian, 29 Oct 2026 15:15; `docs/FAILURES.md` F13). Both registered tests are scored once, after 31 Jan 2029.

Session 2.11b, 29 Oct 2026. Hypotheses: H6 (H4 in a second domain), H4 power by pooling. Class: infrastructure (definitions and synthetic checks). Feasibility: `docs/SECOND_DOMAIN_FEASIBILITY.md` §2b (C1 pass for prospective use).

## 1. Why prospective

EFAS notification criteria changed (catchment > 4000 km² in 2016, > 2000 km² now; feasibility §2b), so a 10-year historical series is not homogeneous. CEMS activations 2023–2026 were counted in session 2.11 (counts only, no lag). The period below starts after this commit, so no event in it exists yet.

## 2. Period

Formal notifications **issued from 30 Oct 2026 to 31 Dec 2028** inclusive. Activations are followed to 31 Jan 2029. Scored once, after the EFAS bulletin covering Dec 2028 is published, no interim look.

## 3. Data definitions (fixed now)

- **Notification:** a row of type "Formal" in Table 1 of an EFAS bimonthly bulletin (the table, not the text total, is the source; any mismatch is recorded), with country one of the 27 EU member states. Fields kept: issue date, forecast date, lead time, river, country.
- **Episode (event unit):** all formal notifications for one country, chained while consecutive issue dates are at most 10 days apart. d0 = issue date of the episode's earliest notification. Size n = number of notifications.
- **Decide-act Y:** Y = 1 if a CEMS Rapid Mapping activation with hazard flood names the episode's country and its activation date falls in [d0 + 2, d0 + 30]; else Y = 0 ("no activation" is a valid outcome). If one activation fits two episodes, it goes to the episode with the latest d0 not after its event date. Activations dated d0 or d0 + 1 are counted and reported, and the episode is left out of any attention test (the decision could drive the attention). Requester: counted unless the API states the request came from outside that country's authorities; if no such field exists, all are counted and that is recorded. Source: the CEMS public API (`scripts/fetch_cems_activations.py`), fetched after 31 Jan 2029.
- **Attend A:** for each river in the episode, the article on the Wikipedia of the country's language (AT de, BE nl, BG bg, HR hr, CY el, CZ cs, DK da, EE et, FI fi, FR fr, DE de, GR el, HU hu, IE en, IT it, LV lv, LT lt, LU fr, MT en, NL nl, PL pl, PT pt, RO ro, SK sk, SI sl, ES es, SE sv). A river is matched to its article by exact title, written to a matching sheet and committed before any pageview is fetched; no or ambiguous match → missing. A = ln(mean daily views on d0, d0+1 + 1) − ln(median daily views d0−29…d0−2 + 1); episode A = maximum over its rivers.

## 4. Candidate statistic (tested here, not registered)

Within strata of n (1, 2–3, ≥ 4), the centred rank of A; T = sum over activated episodes; one-sided permutation p (Y shuffled within strata), α 0.05.

## 5. Synthetic checks (code `analysis/flood_loop_power.py`, committed before each run: c6fccc1, 8f1b619; output `analysis/flood_loop_power_output.txt`)

1000 replications, 999 permutations, 20% of A missing, base activation 0.3, storm clusters of mean size 1.5.

| scenario (β = 0) | N 20 | N 30 | N 40 | N 100 |
|---|---|---|---|---|
| A unrelated to severity | 0.040 | 0.034 | 0.038 | 0.049 |
| A and Y both rise with severity, strata by n | 0.077 | 0.135 | 0.167 | 0.311 |
| strong confounding, strata by n | 0.124 | 0.258 | 0.390 | 0.751 |
| storm shock on A, strata by n | 0.111 | 0.170 | 0.219 | 0.454 |
| strata by tertiles of measured severity (error 0.3 SD) | 0.048 | 0.074 | 0.096 | 0.123 |
| same, strong confounding | 0.055 | 0.131 | 0.159 | 0.321 |

Power, strata by n, odds ratio per SD of A: OR 1.5: 0.17 / 0.30 / 0.36 / 0.70; OR 2: 0.22 / 0.35 / 0.53 / 0.89; OR 3: 0.29 / 0.51 / 0.67 / 0.97 (N 20 / 30 / 40 / 100). At 10–20 episodes a year over 26 months, N is about 20–45.

**Diagnosis:** notification count is a weak severity proxy; whenever attention and activation both rise with severity (as attention did with intensity in hurricanes, τ(A, V) +0.37, `docs/STATUS.md` 2.9), the test rejects on severity alone. Coarse strata of even a well-measured severity still leak. A PASS would show association, not coupling beyond procedure, and the false-positive rate is not controlled, so the candidate is rejected before any data exist.

## 6. What a registrable test needs (next session)

1. A severity measure independent of attention and decision, available for each episode after the fact (candidate, unverified: EFAS or GloFAS discharge reanalysis return period at the notified river; access and licence not checked).
2. A test that adjusts for it continuously (e.g. permutation of A residuals on severity, or a logistic model with a permutation null within storm clusters), with synthetic FPR ≤ 0.05 under the scenarios of §5 and stated power at N 20–45.
3. Registration before 31 Dec 2028 and before any data of the period are opened; the §3 definitions stay as fixed here.

## 7. Severity source: verdict (session 2.11c, 29 Oct 2026; documentation only, no data downloaded)

**Verdict: available, with conditions.** A per-episode severity measure that neither attention nor decision can affect exists after the fact: simulated river discharge from the CEMS-Flood historical runs, scored against the published Gumbel flood thresholds.

| item | EFAS historical (primary) | GloFAS historical (fallback) |
|---|---|---|
| what | LISFLOOD discharge forced with gridded observed precipitation and temperature | LISFLOOD discharge forced with ERA5 reanalysis |
| coverage | 1 Jan 1992 to near real time (v5.0) | 1 Jan 1979 to near real time (v4.0, v5.0) |
| latency | page states both "6 day delay" and "minimum of 1 month lag" (conflict recorded; irrelevant, scoring is after 31 Jan 2029) | intermediate (ERA5T) daily, consolidated monthly; delay in days not stated |
| grid | 1 arcminute (about 1.5 km) | 0.05° |
| thresholds | EFAS v5.1 threshold files: return periods 1.5–500 years plus Gumbel μ, σ (L-moments), NetCDF, direct links | GloFAS v4.0 files, same set, fitted to 1979–2022 annual maxima |
| licence | CEMS-FLOODS datasets licence: free access; reproduction, modification, publication allowed with the notice "Generated using (or Contains modified) Copernicus Emergency Management Service information [year]"; information only, not a warning | same |
| account | yes: EWDS registration, personal access token, and manual acceptance of the dataset's terms of use on its page | same |

Independence: the discharge is a model run from meteorological inputs; Wikipedia views and CEMS activations do not enter it. The current EFAS forecasts (which trigger notifications) are partner-only; the historical runs are not.

**Conditions and limits (recorded before any design):**
1. **Account (Adrian's decision):** an EWDS account and token are needed; Claude cannot create them. The fetch will run in GitHub Actions with the token as a secret, after 31 Jan 2029.
2. **Hazard, not impact:** discharge return period measures the hydrological hazard. Attention and activation respond to impacts (people, damage), which discharge only partly predicts. Any adjustment for it leaves the impact part unadjusted; this is the main validity threat and is simulated as severity measurement error in §8.
3. **Version drift:** thresholds are published for the current versions only (EFAS v5.1, GloFAS v4.0). The version used must be the one whose threshold files exist when scored; the version string is recorded then.
4. **Not checked:** whether EWDS allows spatial subsetting of `efas-historical` (data volume); the EFAS FAQ page names historical data among partner downloads, while the licence and dataset page grant free access under registration; that tension is recorded, and the GloFAS fallback is used if EFAS historical proves restricted.

Sources (opened 29 Oct 2026):
- [EWDS: efas-historical](https://ewds.climate.copernicus.eu/datasets/efas-historical)
- [EWDS: cems-glofas-historical](https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical)
- [CEMS Confluence: Auxiliary Data (flood thresholds)](https://confluence.ecmwf.int/display/CEMS/Auxiliary+Data)
- [CEMS Confluence: FAQ in EFAS](https://confluence.ecmwf.int/spaces/CEMS/pages/293701841/7+FAQ+in+EFAS)
- [CEMS-FLOODS datasets licence (rev. 1)](https://ewds.climate.copernicus.eu/licences/cems-floods)
- [EWDS: CDSAPI setup](https://ewds.climate.copernicus.eu/how-to-api)
- Not usable: https://european-flood.emergency.copernicus.eu/en/node/260 (page body did not render).

## 8. Severity-adjusted candidate: synthetic check (session 2.11c) — rejected, not registered

Code `analysis/flood_loop_severity_test.py` (committed before its run: 66a89f0, 60c0e89); outputs `analysis/flood_loop_severity_test_output.txt`, `..._output_with_n.txt`. Same data model as §5, plus measured severity M = true severity + error (M stands for the Gumbel reduced variate of discharge, §7). Statistic: Freedman–Lane covariance of A residualised on [1, M, M²] with Y − p̂(M) (logistic), one-sided, 999 permutations; variant also adjusts for ln n. 2000 replications (Monte Carlo SE about 0.005 at 0.05).

| FPR, β = 0, adjust M, M² | N 20 | N 30 | N 40 | N 45 | N 100 |
|---|---|---|---|---|---|
| error 0: four §5 scenarios (range) | 0.053–0.064 | 0.046–0.058 | 0.048–0.057 | 0.048–0.054 | 0.044–0.056 |
| error 0.3 SD: A unrelated | 0.064 | 0.058 | 0.068 | 0.044 | 0.058 |
| error 0.3: both rise with severity | 0.062 | 0.065 | 0.053 | 0.073 | 0.072 |
| error 0.3: strong confounding | 0.070 | 0.086 | 0.084 | 0.094 | 0.115 |
| error 0.3: storm shock | 0.072 | 0.070 | 0.071 | 0.064 | 0.077 |
| error 0.6: range | 0.052–0.115 | 0.057–0.160 | 0.062–0.172 | 0.047–0.194 | 0.050–0.311 |

Adding ln n changes nothing material (error 0.3: 0.049–0.100 at N 20–45). Power (error 0.3, OR per SD of A 1.5 / 2 / 3): N 20 0.13 / 0.23 / 0.32; N 45 0.22 / 0.40 / 0.57; N 100 0.36 / 0.64 / 0.86.

**Diagnosis.**
1. Even with severity measured without error, FPR is 0.05–0.06 at N 20–30: the plug-in logistic fit makes the permutation null slightly liberal at these sizes.
2. With error 0.3 SD, residual confounding pushes FPR to 0.06–0.09 at N 20–45 and grows with N (0.115 at N 100). This is not a defect of this statistic: no adjustment for a confounder measured with unknown error controls FPR when attention and activation both depend on the true value. Discharge measures hazard, not impact (§7 condition 2), so the realistic error is likely at least 0.3 SD.
3. Power is below 0.5 at OR ≤ 2 for every N ≤ 45.

**Consequence:** the requirement of §6 (FPR ≤ 0.05 under every §5 scenario, at N 20–45) cannot be met by an observational adjustment at this sample size with this severity measure. No test is registered. The §3 definitions are unchanged; the period's data stay unopened; the registration deadline (31 Dec 2028) still stands for any repaired design.

## 9. F13 repair by a new estimand: sensitivity analysis (session 2.11d) — failed, not registered

Code `analysis/flood_loop_sensitivity_test.py` (committed before its run: e6fad52); output `analysis/flood_loop_sensitivity_test_output.txt`. Same data model as §5 and §8. Class: infrastructure.

**Estimand.** Not "is A associated with Y beyond measured severity M?" but "how large would the unmeasured part of severity (error e, in SD of severity, as in §8) have to be to explain the A–Y association?" Statistic T = partial covariance of A and Y after OLS on [1, M, M²]. Null at a given e: parametric bootstrap with s | M ~ N(R·M, R(1−R)), R = 1/(1+e²); severity's loadings on A (OLS) and Y (probit) are estimated from the data and de-attenuated for R; 499 null draws. Reported e* = largest e on 0, 0.1, …, 2.0 with p(e) ≤ 0.05. Decision fixed in the code before the run: PASS iff p(0.6) ≤ 0.05. 2000 replications (power 1000).

| error rate at the fixed threshold e0 = 0.6, β = 0 | N 20 | N 30 | N 40 | N 45 | N 100 |
|---|---|---|---|---|---|
| true error 0, four scenarios (range) | 0.053–0.102 | 0.025–0.066 | 0.018–0.062 | 0.015–0.059 | 0.004–0.050 |
| true error 0.3 (range) | 0.067–0.102 | 0.043–0.076 | 0.025–0.068 | 0.028–0.061 | 0.010–0.059 |
| true error 0.6 (range) | 0.074–0.135 | 0.066–0.103 | 0.065–0.090 | 0.061–0.092 | 0.051–0.061 |

Power (true error 0.3, λ 0.6, g 1), OR per SD of A 1.5 / 2 / 3: N 20 0.13 / 0.23 / 0.27; N 30 0.12 / 0.22 / 0.32; N 45 0.11 / 0.21 / 0.38; N 100 0.15 / 0.32 / 0.56.

Information only (e0 = 0.3, not a registered decision): error rate 0.038–0.120 at N 20–45 when true error ≤ 0.3, 0.055–0.168 when true error 0.6; power OR 3 0.33–0.52 at N 20–45.

**Diagnosis.**
1. The plug-in bootstrap null is liberal at N 20–30 even with no confounding (A independent of severity: 0.10 at N 20, 0.07 at N 30): the null ignores the sampling error of the estimated loadings and probit fit. A double bootstrap might fix this; not attempted (it cannot fix point 2).
2. Even where the error rate is near 0.05, power is 0.21–0.38 at OR 2–3 for N 20–45: assuming a hidden error of 0.6 SD absorbs most of what 20–45 binary outcomes can show. At e0 = 0.3 (power up to 0.52) the claim is no longer robust to the error §7 calls realistic.
3. The sensitivity parameter assumes the hidden part of severity loads on A and Y as discharge does (proportional loadings). Impact may drive attention more than hazard does; then even e* understates the confounding. This limit holds for any one-parameter sensitivity analysis here.
4. Option (b) (an estimand the decision cannot follow from severity alone): none is defined by the §3 data, which give one attention value and one binary decision per episode, with no ordering of attention and decision inside an episode beyond the d0/d0+1 exclusion. No external documentation was searched for one (not attempted; scope).

**Consequence:** no repaired test meets the requirement (error rate ≤ 0.05 at the fixed threshold under every §5/§8 scenario, useful power at N 20–45). Claude recommends **retire** of the flood attention arm (H4 in floods); floods may still serve H3-type lag description (d0 → activation), which needs no attention test. §3 unchanged; no data of the period opened; no lag computed.

## 10. Option (b): news pressure → activation (session 2.11d-ext) — registered

Class when scored: pre-registered blind. Hypothesis: H4 in floods (H6). Code `analysis/flood_loop_newspressure_power.py` (committed before its run: 8250325); output `analysis/flood_loop_newspressure_power_output.txt`.

**Why this estimand.** Competing news is set by other events, so flood severity cannot cause it, and a news-pressure → activation association needs no severity measure. The route is documented: disasters that coincide with other newsworthy events (e.g. the Olympic Games) get less coverage and less relief ([News Droughts, News Floods, and U.S. Disaster Relief](https://hats.arizona.edu/node/301), abstract page opened 29 Oct 2026; the page names no authors; attribution to Eisensee and Strömberg, QJE 2007, is unverified).

**Data (fixed now; fetched after 31 Jan 2029, with the pageviews of §3).**
- Daily top-articles list of the country's language Wikipedia (the §3 language map), all access, from the Wikimedia pageviews "top" endpoint (documented as `top_articles(project, platform, start)` in [pageviews R client manual](https://ironholds.r-universe.dev/pageviews/doc/manual.html), opened 29 Oct 2026; the endpoint URL and list length are unverified and are recorded at fetch time).
- Exclusions: the Main Page; any title with a namespace prefix (text before ":" that is a namespace of that wiki) or starting with "Special"; any title on the episode matching sheet (§3); any title containing, case-insensitive, a flood stem of its language: de hochwasser, überschwemm, flut; nl overstrom, hoogwater; fr inondation, crue; it alluvion, inondazion, esondazion; es inundaci, riada; pt inunda, cheia; pl powód, powodz; cs, sk povod; sl, hr poplav; hu árvíz; ro inunda; bg наводн; el πλημμ; sv översvämn; da oversvømm; fi tulva; et üleujut; lv plūd; lt potvyn; en (IE, MT) flood.
- NP_day = sum of views of the 10 highest-ranked remaining titles. Episode NP = ln(mean NP_day on d0, d0 + 1) − ln(median NP_day over d0 − 29 … d0 − 2).
- Season of d0: DJF, MAM, JJA, SON. Cluster: episodes (any country) chained while their d0 are at most 3 days apart.
- Episodes are the §3 episodes with Y defined; episodes with an activation on d0 or d0 + 1 are left out (as in §3). Y as §3.

**Statistic and decision.** x_c = mean NP of cluster c, centred within season; r_c = sum over c of (Y − season mean of Y); T = −Σ x_c r_c. One-sided p from 9999 permutations of x across clusters within season (synthetic checks used 999). PASS iff p ≤ 0.05 ("activation falls with competing news pressure"); otherwise "not shown at this size". A remaining flood title in the top 10 would raise NP with severity and push T the other way, so the leak makes the test conservative.

**Synthetic (2000 replications; power 1000).** Error rate, no news effect, under every §5/§8 scenario plus seasonal confounding (severity error does not enter: no severity measure is used): N 20 0.034–0.047; N 30 0.039–0.052; N 40 0.044–0.048; N 45 0.041–0.048; N 100 0.041–0.048. Power (N 20 / 30 / 40 / 45 / 100): via attention, OR 3 per SD of A and news lowering A by 0.6: 0.10 / 0.12 / 0.14 / 0.17 / 0.27; OR 2, by 0.3: 0.06 / 0.06 / 0.08 / 0.09 / 0.11; direct news effect OR 0.5 per SD of NP: 0.15 / 0.26 / 0.28 / 0.34 / 0.65. Episode-level variant (information only, not registered): error rate up to 0.065 at N 45, power slightly higher.

**Limits.** Very low power: at N 20–45 only a large direct effect has a chance. A PASS shows that decisions respond to the news environment, not that attention to this flood caused the activation (news pressure could also act through officials' workload). The test pools naturally with other domains for H4.

## 11. Lag description and measurability (H3 in floods; session 2.11d-ext) — registered

Class when scored: pre-registered blind. Code `analysis/flood_lag_power.py` (committed 53fe445; a first run happened before its commit, by a command-chain error; the script reads no data, is exact, and the rerun after the commit gave identical output); output `analysis/flood_lag_power_output.txt`.

**Data (fixed now).** §3 episodes and activations, from the CEMS public API fields `activationTime`, `eventTime`, `category`, `countries` (field names from `scripts/fetch_cems_activations.py`; no record of the period read). K = episodes with an activation assigned in [d0, d0 + 30] (d0 and d0 + 1 included here). A lag is **measurable** when `activationTime` and `eventTime` are both present and the `eventTime` date lies in [d0 − 3, d0 + 30] (the activation answers this flood, not an earlier one). Lag L = activation date − d0, in days.

**Decision.** M = measurable lags. PASS iff K ≥ 5 and the exact one-sided 95% Clopper–Pearson lower bound of M/K > 0.5; FAIL iff K ≥ 5 and the one-sided 95% upper bound < 0.5; otherwise "not shown at this size".

**Description (no decision).** Activation share K / episodes with Clopper–Pearson 95%; L median, interquartile range and exact 95% CI of the median (order statistics); the same for `eventTime` → `activationTime`; count of activations on d0 or d0 + 1; by country where K ≥ 3.

**Exact error rate and power (no simulation).** At a true measurable share of 0.5, wrong PASS 0.016–0.029 (activation share 0.3) and 0.023–0.033 (share 0.5) at N 20–45. Power at activation share 0.3 (N 20 / 30 / 40 / 45): q 0.8 0.25 / 0.43 / 0.59 / 0.65; q 0.9 0.47 / 0.73 / 0.87 / 0.91; q 1.0 0.76 / 0.97 / 1.00 / 1.00. At share 0.5, q 0.8 0.49 / 0.71 / 0.84 / 0.88.

**Limit.** The pass condition is weak: an activation after a formal notification will usually answer that flood, so a PASS shows only that the lag is measurable from official records (H3's falsifier), not that it is short or improving (H5, which needs several seasons).
