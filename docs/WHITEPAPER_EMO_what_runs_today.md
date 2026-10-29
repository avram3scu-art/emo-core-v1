# EMO: what runs today, and what it has not shown

Adrian N. Avramescu
Independent researcher, Antwerp

Draft of 29 October 2026 (revision of the session 15 draft). **Not for distribution** until the author's verification is recorded in [`docs/STATUS.md`](STATUS.md) (see AI disclosure, point 2) and the review [`docs/REVIEW_2_13_WHITEPAPER.md`](REVIEW_2_13_WHITEPAPER.md) is answered. It replaces `WHITEPAPER_EMO_v1_Why_EMO_Must_Run_Continuously.md.docx`, which described a system that never existed ([`docs/FAILURES.md`](FAILURES.md) F9).

**Who this is for, and the one ask.** This is a status paper for researchers who evaluate disaster response or early-warning systems. It asks one thing: **one person willing to recode one case (EU mpox vaccines, 2022; nine short official records, about 3–4 hours) as an independent second coder**, under a protocol already committed ([`docs/DOUBLE_CODING.md`](DOUBLE_CODING.md)). Every decide-act file in EMO was coded by one AI model and no human has checked one ([§3.3](#33-decide-and-act-h3)). To keep that recode blind, this paper gives no mpox result, and a volunteer should not open the files listed in `docs/DOUBLE_CODING.md` ("Do not open") before returning the sheet. Contact: the author via ORCID https://orcid.org/0009-0005-1393-5264. It is not a funding request.

**How to read it.** Every factual statement links to a file in this repository; anything not yet built or not yet scored is marked **[plan]**. Every result carries one evidence class ([`CLAUDE.md`](../CLAUDE.md), Science rules): **[blind]** protocol committed before the data were opened, outcome unknown; **[known history]** protocol first, outcome of the cases known to the author or to Claude; **[exploratory]** no pre-registration; **[infrastructure]** code, CI, data plumbing, synthetic checks of a method. A test that is registered but not yet scored is marked **[blind, registered]**: it is a commitment, not a result. No claim of "first" or "only" is made: no full-text literature database was searched ([`docs/RELATED_WORK.md`](RELATED_WORK.md), [`docs/LIT_SEARCH_F11.md`](LIT_SEARCH_F11.md)). Links are relative to branch `emo-2026-10`; a shared copy will point to a tagged release [plan, session 2.15, [`docs/PLAN.md`](PLAN.md)].

---

## 1. The hypothesis, and how it can fail

EMO tests one idea: that a society's response to a hazard behaves like a mind, a loop of predicting, attending, deciding and acting, choosing remedies and learning, whose links are **coupled** and **improve with experience** ([`CLAUDE.md`](../CLAUDE.md), Purpose; [`docs/PLAN.md`](PLAN.md) §3). A loop with independent links is a set of agencies; only coupling and learning beyond what severity and formal procedure explain would support the "mind" reading. That null, **independent agencies**, is stated before any test ([`docs/PLAN.md`](PLAN.md) §3).

The idea is split into seven hypotheses ([`docs/PLAN.md`](PLAN.md) §4). Only H4 and H5 bear on the "mind" reading; H1–H3 and H7 test single links; H6 tests generality.

| # | Hypothesis | Fails if | Where it stands (29 Oct 2026) |
|---|---|---|---|
| H1 | Predict: forecast skill improves over time | τ_I = 0 on the domain's forecasts | NHC track errors fall 2.3–4.0 %/yr **[exploratory]**; SMF v2 test on 2026 storms **[blind, registered]**, scored from May 2027 ([§3.1](#31-predict-h1)) |
| H2 | Attend: attention ignites on hazard events, with a threshold that transfers | GWI v2 fails its prospective calibration or event test | v1 event test PASS **[blind]**; v1 calibration FAIL **[blind]**; GWI v2 **[blind, registered]**, scored 15 Nov 2027 ([§3.2](#32-attend-h2)) |
| H3 | Decide-act: action follows each event with a measurable lag | lags not measurable from official records for most events | hurricanes 2015–2025 **FAIL** **[known history]**; repaired for 2027+ and for floods **[blind, registered]** ([§3.3](#33-decide-and-act-h3)) |
| H4 | Coupling beyond procedure | no significant association at power ≥ 0.8, or an equivalence bound excludes it | **not tested**: cannot be tested on 2015–2025 hurricanes; registered tests have power < 0.5 ([§3.4](#34-coupling-beyond-procedure-h4)) |
| H5 | Learning: lags shrink across seasons beyond intensity mix and forecast gains | no significant trend at adequate power | **not shown at this size** (power 0.06) **[known history]** ([§3.5](#35-learning-h5)) |
| H6 | Generality: H4–H5 hold in a second hazard or region | they fail there | EU floods: two tests **[blind, registered]**, scored after 31 Jan 2029 ([§3.6](#36-a-second-domain-eu-floods-h6)) |
| H7 | Choose: registered forecasts beat a naive baseline (Brier) | no better than baseline after ≥ 20 resolved forecasts | 15 forecasts registered, none resolved ([§3.7](#37-choose-h7-and-rdl)) |

**What this means today.** No result supports the "mind" reading. The two hypotheses that bear on it have not been tested at adequate power, and in the hurricane domain H4 cannot be decided before about 2036 at the expected sample size ([`docs/PLAN.md`](PLAN.md) §4, H4 note). If H4 and H5 both fail at adequate power in a domain, the claim is withdrawn for that domain and EMO remains a set of response measurements ([`docs/PLAN.md`](PLAN.md) §4, "Falsification, stated now"). The framing is a hypothesis under test, not a finding.

**Related work.** Policy-coherence indicators (SDG 17.14.1), governance quality, regime effectiveness (Oslo–Seattle, IRD), response stringency (OxCGRT) and early-warning coverage already measure parts of the response ([`docs/RELATED_WORK.md`](RELATED_WORK.md), entries opened in session 4). What EMO adds today is form, not a new question: dated lags from primary records, open code, a scheduled re-run, pre-registered tests with their power stated, and every failure on record (same file, Summary). Regime-effectiveness work may cover more of this ground than the named-source search found (same file).

## 2. What runs

| Component | What it does today | Evidence |
|---|---|---|
| Weekly run | A GitHub Action, started each Monday 07:41 Brussels by an external scheduler, refreshes open data, re-runs analyses and tests, commits only if they pass, rebuilds a public page. Running since 23 Oct 2026; latest run 40843970838 (29 Oct 2026), green. **[infrastructure]** | [`.github/workflows/weekly_refresh.yml`](../.github/workflows/weekly_refresh.yml), [`scripts/weekly_run.py`](../scripts/weekly_run.py), [`scripts/build_site.py`](../scripts/build_site.py); [`CLAUDE.md`](../CLAUDE.md) §Start, step 3 |
| Frozen check | The weekly run re-runs recorded analyses and fails if any recorded output changes; 19 reproduced on 29 Oct 2026, RDL v0.4 not run (no data). **[infrastructure]** | [`results/weekly/2026-10-29/SUMMARY.md`](../results/weekly/2026-10-29/SUMMARY.md) |
| Tests and checks | CI: 200 tests pass (run 40895686707, 29 Oct 2026), mypy, ruff, and a claim-word check that fails on unjustified status or priority words; a pre-push hook runs the same checks; exact tool versions locked. **[infrastructure]** | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml), [`tests/`](../tests/), [`scripts/claims_grep.py`](../scripts/claims_grep.py), [`scripts/hooks/pre-push`](../scripts/hooks/pre-push), [`requirements-lock.txt`](../requirements-lock.txt) |
| Hurricane loop table | 52 Atlantic landfalls 2015–2025, one row per storm with predict, attend, warning and decide-act fields from machine-readable records, checked by script. **[infrastructure]** | [`data/loop_hurricanes/`](../data/loop_hurricanes/), [`scripts/validate_loop_table.py`](../scripts/validate_loop_table.py), [`docs/LOOP_PROTOCOL.md`](LOOP_PROTOCOL.md) §16 |
| DAC standard | JSON schema, validator and profile function for warning-to-delivery event files. **[infrastructure]** | [`emo/dac_standard.py`](../emo/dac_standard.py), [`docs/DAC_STANDARD.md`](DAC_STANDARD.md), [`tests/dac_unit/`](../tests/dac_unit/) |
| Metric functions | τ_I, SMF v2, GWI v2 and the UIA 2.0 loop profile as tested Python functions. **[infrastructure]** | [`emo/info_time.py`](../emo/info_time.py), [`emo/smf.py`](../emo/smf.py), [`emo/gwi_v2.py`](../emo/gwi_v2.py), [`emo/uia2.py`](../emo/uia2.py) |
| Records | One row per test, run, fetch and failed attempt; one row per failure with its diagnosis and the author's choice. | [`docs/RECORD.md`](RECORD.md), [`docs/FAILURES.md`](FAILURES.md) |

What does **not** run: no dashboard, no API, no streaming or daily ingestion, no digital-twin link. The scaffolding the earlier white paper described never ran and was deleted on 26 Oct 2026 ([`docs/AUDIT_2026-10-26.md`](AUDIT_2026-10-26.md)). ECMWF declined to distribute the numerical data behind its headline-score charts ([`docs/sources/ecmwf/SD-131630_reply.md`](sources/ecmwf/SD-131630_reply.md)).

## 3. Results, link by link

The engine domain is Atlantic hurricanes, chosen because the loop repeats several times a season; every season up to 2026 is known history, so only 2027 onward gives blind tests ([`docs/PLAN.md`](PLAN.md) §5).

### 3.1 Predict (H1)

- **τ_I** on NHC Atlantic track errors 1970–2025: error falls 2.33 %/yr at 12 h and 3.05–3.95 %/yr at 24–120 h, block-bootstrap intervals excluding zero at every lead. This restates NHC's known trend. **[exploratory]** ([`results/weekly/2026-10-29/information_time_nhc.txt`](../results/weekly/2026-10-29/information_time_nhc.txt), [`analysis/information_time_nhc.py`](../analysis/information_time_nhc.py)).
- **SMF v1** (do official forecasts beat "no change"?): after Diebold–Mariano with Holm correction, 6 of 12 earlier passes survive (EIA CO2 and electricity at 3 months; SPF unemployment at 1, 2, 4 quarters; SPF industrial production at 1–2 quarters). The EIA CO2 input fails a stationarity check. **[known history]** ([`docs/SMF_PROTOCOL.md`](SMF_PROTOCOL.md) §13, [`results/smf_dm/result.txt`](../results/smf_dm/result.txt)).
- **SMF v2** (skill against persistence as the definition): NHC official forecasts vs the OCD5 benchmark on 2026 storms, track and intensity at 24/48/72 h, Holm over the family. Synthetic family false-positive rate 0.027–0.045 (0.066 under strong between-storm dependence, a stated limit); power 0.51–0.64 at 12–15 storms for a one-SD advantage. **[blind, registered]**, data from 1 May 2027 ([`docs/SMF_PROTOCOL.md`](SMF_PROTOCOL.md) §14–§15, [`analysis/smf_v2_power_output.txt`](../analysis/smf_v2_power_output.txt)).

### 3.2 Attend (H2)

- **GWI v1** on Wikipedia pageviews: ignition days fall in hurricane-landfall windows in 14 of 21 event windows vs 9 of 275 controls (Fisher p = 2.3e-13). **PASS [blind]**, on that condition only: its placebo condition used a non-significant result as evidence and is invalid; Fisher ignores clustering ([`docs/GWI_PROTOCOL.md`](GWI_PROTOCOL.md) §6 note; [`docs/FAILURES.md`](FAILURES.md) F5).
- **GWI v1 calibration**: the threshold does not transfer across articles, so a GWI level is not a measurement. **FAIL [blind]** ([`docs/GWI_CALIBRATION_PROTOCOL.md`](GWI_CALIBRATION_PROTOCOL.md) §7; F4).
- **GWI v2** (causal per-article seasonal baseline, Poisson-binomial tail, common-mode filter, block-permutation null): 20-placebo calibration and an M ≥ 7 earthquake event test on 1 Nov 2026–31 Oct 2027. Its filter and threshold were tuned on three seen articles (exploratory development, stated). Synthetic event-test false-positive rate ≤ 0.017, power 0.70–0.96 at hit rate 0.3. **[blind, registered]**, scored once on 15 Nov 2027 ([`docs/GWI_V2_PROTOCOL.md`](GWI_V2_PROTOCOL.md), [`analysis/gwi_v2_synthetic_output.txt`](../analysis/gwi_v2_synthetic_output.txt)).

### 3.3 Decide and act (H3)

- **Hurricane loop 2015–2025, 52 storms**: both lags measurable for 24 of 52 (binomial p = 0.756). **H3 FAIL [known history]**. Diagnosis: the unmeasured are almost all weak tropical storms with no qualifying federal major-disaster declaration, so there is no lag to measure; hurricanes alone had both lags in 23 of 27 (exploratory, seen data, no weight) ([`docs/LOOP_PROTOCOL.md`](LOOP_PROTOCOL.md) §19, [`analysis/loop_test_2015_2025_output.txt`](../analysis/loop_test_2015_2025_output.txt); F12). Repaired for 2027+ only: H3 on storms with a disaster-declaration request, plus a separate declaration-rate measure. **[blind, registered]** ([`docs/LOOP_PROTOCOL.md`](LOOP_PROTOCOL.md) §20.1).
- **DAC case files (hand-coded from primary records):**
  - Ozone vs climate: warning-to-binding-act lag 4,828 days (ozone) and 6,555–6,919 days (climate; the Charney report is dated to the year only); n = 2, descriptive. **[exploratory]** ([`data/dac_ozone_events.json`](../data/dac_ozone_events.json), [`data/dac_climate_events.json`](../data/dac_climate_events.json), [`data/sources/dac_primary_sources.md`](../data/sources/dac_primary_sources.md)).
  - COVID-19 PPE, five countries and the EU, recoded after the original files were lost; e.g. Belgium's first delivery to municipalities at t0 + 46 days. **[known history]** (coded with an earlier manuscript's key results known; two blindness breaches recorded) ([`docs/DAC_PPE_CODING.md`](DAC_PPE_CODING.md) §1, [`data/dac_ppe/BE_profile.json`](../data/dac_ppe/BE_profile.json), [`docs/DAC_PPE_COMPARISON.md`](DAC_PPE_COMPARISON.md)).
  - EU mpox 2022: coded **[known history]**; results withheld here so that the second-coder recode can stay blind (see the ask above) ([`docs/DOUBLE_CODING.md`](DOUBLE_CODING.md)).
  - **Limit:** every DAC file was coded by Claude; no human recode exists; no agreement result exists ([`docs/double_coding/coding_sheet.csv`](double_coding/coding_sheet.csv), header only).
- **EU floods**: a lag-measurability test (formal EFAS notification → CEMS activation) is **[blind, registered]**; see §3.6.

### 3.4 Coupling beyond procedure (H4)

- **Hurricanes 2015–2025: cannot be tested at this size.** The guard failed for all six link pairs (9–10 usable within-season comparisons, 15 needed) **[known history]** ([`docs/LOOP_PROTOCOL.md`](LOOP_PROTOCOL.md) §19).
- **He direction test** on the UIA 2.0 loop profile, 23 storms: **PASS**, mean Kendall τ +0.22, within-season permutation p = 0.012 **[known history]**, led by attention (τ +0.46) and warning lead (+0.20), not forecast skill (+0.00). Attention and response speed both rise with storm intensity, which was not controlled: this is an association, **not** evidence of coupling beyond procedure ([`docs/HE_CALIBRATION_PROTOCOL.md`](HE_CALIBRATION_PROTOCOL.md) §10, [`analysis/he_loop_test_output.txt`](../analysis/he_loop_test_output.txt)). A severity-adjusted version is to be registered before any 2027 row is built [plan, session 2.12b].
- **Hurricane blind arm** (attention → state lag, 2027+): power 0.15 after 5 blind seasons and 0.38 after 10 at about two measured storms per season. **[infrastructure]** synthetic ([`docs/LOOP_PROTOCOL.md`](LOOP_PROTOCOL.md) §20.5).
- **Flood attention arm: retired** after three synthetic failures, before any data of the period existed. A within-strata rank test rejected on severity alone (false-positive rate 0.08–0.75); a severity-adjusted Freedman–Lane test reached 0.06–0.09 at 20–45 episodes when severity is measured with 0.3 SD error; a sensitivity-analysis repair was liberal at 20–30 episodes (0.015–0.135) with power 0.21–0.38. Diagnosis: with one attention value and one binary decision per episode, and severity measured only through hazard (discharge), no observational adjustment controls the false-positive rate at this size. **[infrastructure]** ([`docs/FLOOD_LOOP_PROTOCOL.md`](FLOOD_LOOP_PROTOCOL.md) §5, §8, §9; F13).
- **Replacement: news pressure → activation** (competing news on the day of the earliest notification cannot follow flood severity). Error rate 0.034–0.052 under every scenario, **power 0.06–0.34** at 20–45 episodes. **[blind, registered]**, scored once after 31 Jan 2029; a FAIL will read "not shown at this size". A PASS would show that decisions respond to the news environment, not that attention to a flood caused its activation ([`docs/FLOOD_LOOP_PROTOCOL.md`](FLOOD_LOOP_PROTOCOL.md) §10, [`analysis/flood_loop_newspressure_power_output.txt`](../analysis/flood_loop_newspressure_power_output.txt)).

Every H4 route registered today has power below 0.5. H4 can be decided only by pooling across domains or by a design not yet found [plan].

### 3.5 Learning (H5)

Hurricanes 2015–2025, 9 seasons, 23 storms: season-mean trend of residual lags, Holm p 0.223 (state) and 0.126 (federal); power 0.064. **Not shown at this size [known history]** ([`docs/LOOP_PROTOCOL.md`](LOOP_PROTOCOL.md) §19). Adequate power is not reachable before about 2030 ([`docs/PLAN.md`](PLAN.md) §4, H5 note).

### 3.6 A second domain: EU floods (H6)

Data definitions are fixed for EFAS formal notifications issued 30 Oct 2026–31 Dec 2028, with CEMS Rapid Mapping activations followed to 31 Jan 2029; "no activation" is a valid outcome ([`docs/FLOOD_LOOP_PROTOCOL.md`](FLOOD_LOOP_PROTOCOL.md) §2–§3; feasibility [`docs/SECOND_DOMAIN_FEASIBILITY.md`](SECOND_DOMAIN_FEASIBILITY.md)). Two tests are registered, both scored once after 31 Jan 2029, no interim look:

- news pressure → activation (H4 in floods; §3.4 above), power 0.06–0.34; **[blind, registered]**
- lag measurability (H3 in floods): PASS iff at least 5 activations and the 95 % lower bound of the measurable share exceeds 0.5; wrong-pass rate ≤ 0.033, power 0.47–0.91 at 20–45 episodes if 90 % of lags are measurable. A PASS shows only that the lag can be measured, not that it is short or improving. **[blind, registered]** ([`docs/FLOOD_LOOP_PROTOCOL.md`](FLOOD_LOOP_PROTOCOL.md) §11, [`analysis/flood_lag_power_output.txt`](../analysis/flood_lag_power_output.txt)).

### 3.7 Choose (H7) and RDL

- **RDL v0.2 and v0.3** both FAIL on reserved historical cases **[known history]**; RDL has passed no test of its recommendations ([§4](#4-what-failed)).
- **RDL forecast ledger**: 5 dated forecasts, deposited on Zenodo 20 Oct 2026 (DOI 10.5281/zenodo.23507467), first resolution 31 Dec 2026, not scored. **[blind, registered]** ([`docs/RDL_FORECAST_LEDGER.md`](RDL_FORECAST_LEDGER.md), [`data/rdl_forecast_ledger.csv`](../data/rdl_forecast_ledger.csv)).
- **Hurricane loop ledger**: 10 forecasts for the 2027 season (declaration by storm class; lag thresholds by intensity), Brier score against a pooled baseline; one-season power 0.234. **[blind, registered]**, scored about May 2028 ([`docs/LOOP_PROTOCOL.md`](LOOP_PROTOCOL.md) §21, [`data/loop_forecast_ledger.csv`](../data/loop_forecast_ledger.csv)). Its public deposit (a new Zenodo version) is not yet made [plan, before 1 June 2027].

H7 needs at least 20 resolved forecasts; 15 are registered and none has resolved.

## 4. What failed

Failures stay on record. Each has a diagnosis and a recorded choice (repair, replace or retire) in [`docs/FAILURES.md`](FAILURES.md).

| # | What | Result and class | Choice |
|---|---|---|---|
| F1 | RDL v0.2 | FAIL on the reserved case in all 4 settings; gain scales with the remaining gap, not tractability **[known history]** | retire |
| F2 | RDL v0.3 | FAIL on the reserved case in all 16 settings; no veto structure **[known history]** | replace by the forecast registry (H7) |
| F3 | Synergy on three climate streams | FAIL: no higher-order structure beyond the null **[blind]** | retire |
| F4 | GWI v1 calibration | FAIL: threshold does not transfer **[blind]** | repair as GWI v2 |
| F5 | GWI v1 placebo condition | invalid (non-significant result used as evidence) | repair inside GWI v2 |
| F6 | SMF v1 | 6 of 12 passes withdrawn after a significance test **[known history]** | replace by SMF v2 |
| F7 | a_UIA scalar | retired: 4 of 6 terms not measurable | replace by the UIA 2.0 profile |
| F8 | He direction rule (Option A) | 41–52 % false positives on synthetic data **[infrastructure]** | replace by a permutation test |
| F9 | Earlier white papers, deck, grants | described an observatory that never ran; "first" claims unchecked | replace by this paper |
| F10 | Lost DAC files | original PPE files lost; recoded **[known history]** | repair; second coder pending |
| F11 | Conceptual DAC paper | desk-rejected by *Futures*, 18 Apr 2026 ([`docs/sources/dac_paper/README.md`](sources/dac_paper/README.md)) | retire |
| F12 | Hurricane loop H3, 2015–2025 | FAIL, 24/52 measurable **[known history]** | repair for 2027+ |
| F13 | Flood attention arm | three designs fail synthetic checks before any data **[infrastructure]** | retire, then replace by news pressure |

## 5. How EMO keeps itself honest

Working rules in [`CLAUDE.md`](../CLAUDE.md), enforced by code where possible:

1. Every test is pre-registered (hypothesis, data, statistic, threshold) and committed before its data are opened.
2. Every protocol states its false-positive rate and power from synthetic data before its data are opened; a test with power below 0.5 says so in its first line, and its FAIL reads "not shown at this size".
3. A pass needs a significance test of the condition that decides it, with a null that respects dependence; a non-significant result is never evidence of no effect.
4. Prospective tests are preferred; a repaired version is never tested on the data that exposed the failure.
5. Repair, don't drop: every failure gets a diagnosis and a recorded choice.
6. Multi-part measures are profiles, never weighted scores.
7. No status or priority word without evidence, checked before every push and in CI ([`scripts/claims_grep.py`](../scripts/claims_grep.py)).

## 6. Scoring calendar [plan]

All from [`docs/PLAN.md`](PLAN.md); none has happened yet.

| When | What | Hypothesis |
|---|---|---|
| from 1 Jan 2027 | RDL ledger, first forecast (session 2.10) | H7 |
| from 1 May 2027 | SMF v2 on 2026 NHC forecasts | H1 |
| 15 Nov 2027 | GWI v2 calibration and earthquake event test (session 2.12) | H2 |
| about May 2028 | 2027 hurricane season: H3 repair, declaration rate, blind H4 pair, 10 forecasts, severity-adjusted He test (session 2.12b) | H3, H4, H7 |
| after 31 Jan 2029 | EU floods: news pressure → activation, lag measurability | H4, H3 in H6 |
| open | second coder for the mpox file | DAC data quality |

What EMO cannot see today: any hazard outside Atlantic hurricanes and EU floods; any causal claim; coupling or learning at adequate power. What would change the picture most: an independent second coder, and the earliest blind scores above.

## Data and code availability

Everything cited is in the public repository `avram3scu-art/emo-core-v1`, branch `emo-2026-10`, licensed AGPL-3.0 ([`LICENSE`](../LICENSE)).

## AI disclosure

1. All inputs were the author's own manuscript text, code and publicly available reference literature and data (plus synthetic simulation parameters where applicable).
2. *[Withheld until the author's verification of this draft is recorded in [`docs/STATUS.md`](STATUS.md); not true today.]*
3. All scientific claims and interpretations are the author's own.

Contributions: Adrian N. Avramescu (concept, decisions, verification). Claude (Anthropic) contributed code, data coding, analysis and drafting under the author's direction.
