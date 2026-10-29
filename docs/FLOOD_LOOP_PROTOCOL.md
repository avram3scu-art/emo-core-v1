# Flood loop (EU): data definitions registered; test statistic not yet registrable

**First line (power and validity rule):** no pass/fail test is registered in this file. The candidate test below failed its synthetic false-positive check (§5), so it must not be run. A test is registered only in a later commit, before any flood notification, pageview or activation of the period is opened.

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
