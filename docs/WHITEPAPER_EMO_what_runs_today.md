# EMO: what runs today

Adrian N. Avramescu
Independent researcher, Antwerp

Draft, 29 October 2026. Not for distribution until reviewed (see `docs/REVIEW_S15_WHITEPAPER.md`). It replaces `WHITEPAPER_EMO_v1_Why_EMO_Must_Run_Continuously.md.docx`, which described a system that never existed.

**How to read this paper.** Every factual statement links to a file in this repository (script, data file, test or protocol). Anything that is an aim and not yet built is marked **[plan]**. Every result carries one evidence class, as defined in [`CLAUDE.md`](../CLAUDE.md): **[blind]** (protocol committed before the data were opened, outcome unknown); **[known history]** (protocol first, but the outcome of the cases was known to the author or to Claude); **[exploratory]** (no pre-registration); **[infrastructure]** (code, CI, data plumbing, synthetic checks of a method). Claims of "first" or "only" are not made: no full-text literature database was searched ([`docs/RELATED_WORK.md`](RELATED_WORK.md), [`docs/LIT_SEARCH_F11.md`](LIT_SEARCH_F11.md)).

---

## 1. The vision, stated as a plan

EMO (Emergent Mind Observatory) starts from one idea: humanity, with its institutions and infrastructures, can be studied as a system that senses, remembers, predicts and acts, and its response to what it knows can be measured. The questions are simple to state:

- When a warning is issued, how long until something is actually delivered? (DAC)
- Is our collective prediction getting better, and how fast? (τ_I, SMF)
- Does attention converge on a risk when it should? (GWI)
- Do media, science and policy streams carry information jointly that none carries alone? (synergy)
- Can proposed remedies be tested before they are adopted? (RDL)
- Can these be read together as a profile of how the human–Earth interface is working? (UIA)

**[plan]** In the long run EMO should be an open, continuously re-run instrument whose outputs sit beside Earth-system models, early-warning systems and planetary dashboards, as inputs to deliberation, never as scores that decide. That is the vision of the earlier white paper and it is kept. What changed is the status: almost none of it exists yet, several parts were tested and failed, and the rest of this paper says exactly which.

Other instruments already measure parts of the response: policy-coherence mechanisms (SDG 17.14.1), governance quality, regime effectiveness (Oslo–Seattle, IRD), response stringency (OxCGRT) and early-warning coverage ([`docs/RELATED_WORK.md`](RELATED_WORK.md), entries opened in session 4). The narrow thing EMO adds today is form, not a new question: dated warning-to-delivery lags from primary records, open code, a scheduled re-run, and every test with its protocol on record (same file, Summary).

## 2. What runs

| Component | What it does today | Evidence |
|---|---|---|
| Weekly run | A GitHub Action, started every Monday by an external scheduler, refreshes open data, re-runs the analyses, runs the tests, commits only if they pass, and rebuilds a public page. Running since 23 Oct 2026. **[infrastructure]** | [`.github/workflows/weekly_refresh.yml`](../.github/workflows/weekly_refresh.yml), [`scripts/weekly_run.py`](../scripts/weekly_run.py), [`scripts/build_site.py`](../scripts/build_site.py); start-up in [`CLAUDE.md`](../CLAUDE.md) §Start; latest run 40666382346 |
| Frozen check | The weekly run re-runs recorded analyses and fails if any recorded output changes. **[infrastructure]** | [`docs/STATUS.md`](STATUS.md) (F5: all 15 frozen runs reproduce, weekly run 40659742858) |
| Tests and checks | CI runs unit and integration tests, mypy, ruff, and a claim-word check that fails on unjustified status or priority words (word list in the script). 149 tests at the last recorded CI run. **[infrastructure]** | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml), [`tests/`](../tests/), [`scripts/claims_grep.py`](../scripts/claims_grep.py); count from [`docs/STATUS.md`](STATUS.md), session 11 (CI 40807395513) |
| DAC standard | A JSON schema, validator and profile function for warning-to-delivery event files. **[infrastructure]** | [`emo/dac_standard.py`](../emo/dac_standard.py), [`docs/DAC_STANDARD.md`](DAC_STANDARD.md), [`docs/dac_event_file.schema.json`](dac_event_file.schema.json), [`tests/dac_unit/`](../tests/dac_unit/) |
| Metric functions | Synergy, GWI, SMF and τ_I as tested Python functions. **[infrastructure]** | [`emo/synergy.py`](../emo/synergy.py), [`emo/gwi.py`](../emo/gwi.py), [`emo/smf.py`](../emo/smf.py), [`emo/info_time.py`](../emo/info_time.py) |
| Record | One row per test, run, fetch and failed attempt. | [`docs/RECORD.md`](RECORD.md) |

What does **not** run: no dashboard, no API, no streaming or daily ingestion, no DestinE or other digital-twin link. The API, dashboard and pipeline scaffolding described in the earlier white paper never ran and was deleted on 26 Oct 2026; ECMWF declined data access ([`README.md`](../README.md), Superseded documents; [`docs/AUDIT_2026-10-26.md`](AUDIT_2026-10-26.md)). GDELT has never been ingested ([`README.md`](../README.md), status table).

## 3. Results, pillar by pillar

### 3.1 DAC: from warning to delivered response

DAC records, for one hazard, dated events by sublayer (warning t0, first order, first delivery, binding act, funding, institutionalisation, counter-measure) and reports them as a profile, never as a weighted score ([`docs/DAC_STANDARD.md`](DAC_STANDARD.md)).

- **Ozone vs climate.** Warning-to-binding-act lag 4,828 days for ozone (exact) and 6,555–6,919 days for climate (the Charney report is dated to the year only); n = 2, t0 and binding acts from primary records. **[exploratory]** ([`data/dac_ozone_events.json`](../data/dac_ozone_events.json), [`data/dac_climate_events.json`](../data/dac_climate_events.json), [`data/sources/dac_primary_sources.md`](../data/sources/dac_primary_sources.md), [`analysis/dac_ozone.py`](../analysis/dac_ozone.py)). Two cases describe; they do not test anything.
- **COVID-19 PPE, five countries and the EU.** Recoded from primary sources in October 2026 after the original files were lost: six event files (Belgium, France, Germany, the Netherlands, Sweden, EU), with sources, sha256 checksums and phrase tests. **[known history]**: coded with the key results of an earlier manuscript known ([`docs/DAC_PPE_CODING.md`](DAC_PPE_CODING.md) §1, which records two blindness breaches verbatim). Example result: Belgium's first delivery to municipalities at t0 + 46 days; paired order-to-delivery lags, measured to the federal stock (a secondary end point), 5–6 days (surgical masks), 10–56 days (FFP2, across three readings of one contested order), 5 days (gloves) ([`data/dac_ppe/BE_profile.json`](../data/dac_ppe/BE_profile.json)). The recoded files were compared item by item with the manuscript: most items the same or overlapping, a few different, one Claude omission corrected ([`docs/DAC_PPE_COMPARISON.md`](DAC_PPE_COMPARISON.md)). Cross-case summary script: [`analysis/dac_ppe_crosscase.py`](../analysis/dac_ppe_crosscase.py) **[exploratory]**.
- **Mpox 2022, EU.** From the WHO emergency declaration, first EU order −39 days, first delivery −25 days, binding act −1 day; one paired order (14 days). **[known history]** ([`docs/DAC_MPOX_CODING.md`](DAC_MPOX_CODING.md), [`data/dac_mpox/EU_profile.json`](../data/dac_mpox/EU_profile.json)). With an earlier-warning t0 (ECDC's first risk assessment, rule fixed before sources were opened) the order lag is +22 days ([`docs/DAC_T0_EARLY_WARNING.md`](DAC_T0_EARLY_WARNING.md), [`data/dac_mpox/EU_profile_t0_early.json`](../data/dac_mpox/EU_profile_t0_early.json)). The sign of a lag depends on the choice of t0; that is itself a finding about the method.
- **Limits.** Every DAC file was coded by an AI model (Claude) and no human has yet recoded any of them. A double-coding protocol and packet are committed; no agreement result exists ([`docs/DOUBLE_CODING.md`](DOUBLE_CODING.md)). The DAC manuscript ("Decision or Supply?") has not been submitted ([`docs/STATUS.md`](STATUS.md), F1, F14).

### 3.2 EMO metrics

- **τ_I (information-time)** on NHC Atlantic hurricane track errors 1970–2025: track error falls 2.3% a year at 12 h lead time and 3.0–4.0% a year at 24–120 h, which restates NHC's known trend. **[exploratory]** ([`results/weekly/2026-10-28/information_time_nhc.txt`](../results/weekly/2026-10-28/information_time_nhc.txt), [`analysis/information_time_nhc.py`](../analysis/information_time_nhc.py), [`data/nhc_atlantic_official_track_errors_1970_2025.csv`](../data/nhc_atlantic_official_track_errors_1970_2025.csv)).
- **Organismality plane** 1989–2025: international co-authorship share against conflict death rate, drawn as a path. **[exploratory]**, descriptive only ([`analysis/organismality_plane.py`](../analysis/organismality_plane.py), [`analysis/organismality_plane.png`](../analysis/organismality_plane.png)).
- **GWI (global workspace ignition)** on Wikipedia pageviews: ignition days fall in Atlantic hurricane-landfall windows far more often than in control windows (14 of 21 event windows vs 9 of 275 controls, Fisher p = 2.3e-13). **PASS [blind]**, decided by that significance condition only. Its placebo condition used a non-significant result as evidence and is invalid; its H ≥ 0.5 condition is a point threshold ([`docs/GWI_PROTOCOL.md`](GWI_PROTOCOL.md) §7 and §6 note; [`analysis/gwi_hurricanes.py`](../analysis/gwi_hurricanes.py)).
- **SMF (self-model fidelity)**: do official forecasts beat "no change"? Re-tested with Diebold–Mariano and Holm correction, **[known history]**: 6 of 12 earlier passes survive (EIA CO2 and electricity at 3 months; SPF unemployment at 1, 2, 4 quarters; SPF industrial production at 1–2 quarters); 6 are withdrawn. The EIA CO2 input fails a stationarity check, so its p-value may be optimistic ([`docs/SMF_PROTOCOL.md`](SMF_PROTOCOL.md) §13, [`results/smf_dm/result.txt`](../results/smf_dm/result.txt), [`analysis/smf_dm.py`](../analysis/smf_dm.py)).

### 3.3 UIA

The earlier white paper presented a_UIA, a weighted sum of six terms, as "a single, interpretable gauge". The session 5 audit found 1 of the 6 terms measurable from public data today (I, as τ_I), 1 conditional, 4 not measurable; a_UIA was **retired** and no claim may rest on it ([`docs/UIA_PROTOCOL.md`](UIA_PROTOCOL.md) §1, §4). UIA is now defined as the profile (I, C, F, E, D), reported component by component; **none of it is scored**. The direction test on that profile needs 24 coded cases; DAC case files exist for ozone, climate, mpox and the six PPE files, but none is coded on the profile ([`docs/PLAN.md`](PLAN.md), session 12). **[plan]**

### 3.4 RDL: remedies

RDL has passed no test of its recommendations ([`CLAUDE.md`](../CLAUDE.md), Science rules). See §4 for its failures. The only blind RDL test is a ledger of five dated forecasts, deposited on Zenodo on 20 Oct 2026 (DOI 10.5281/zenodo.23507467), first resolution by 31 Dec 2026, not yet scored. **[blind]** Five forecasts, three with the same score, cannot validate anything ([`docs/RDL_FORECAST_LEDGER.md`](RDL_FORECAST_LEDGER.md), [`data/rdl_forecast_ledger.csv`](../data/rdl_forecast_ledger.csv), [`analysis/score_forecast_ledger.py`](../analysis/score_forecast_ledger.py)).

## 4. What failed

Failures stay on record. This list is the most important part of the paper.

| What | Result | Source |
|---|---|---|
| RDL v0.2 | Passed its two development cases; **FAIL** on the reserved leaded-petrol case in all four sensitivity settings. Cause: "predicted gain" scales with the remaining gap, not with tractability. **[known history]** | [`docs/RDL_BACKTEST_PROTOCOL.md`](RDL_BACKTEST_PROTOCOL.md), [`analysis/rdl_backtest_heldout.py`](../analysis/rdl_backtest_heldout.py) |
| RDL v0.3 | **FAIL** on the reserved case: sulphur 1985 not above chrysotile 2004, in all 16 settings. Cause: no veto structure. A development check passed only by construction after a rule change. **[known history]** | [`docs/RDL_V03_PROTOCOL.md`](RDL_V03_PROTOCOL.md), [`analysis/rdl_v03_heldout.py`](../analysis/rdl_v03_heldout.py) |
| RDL v0.4 | Not run: the Oslo–Seattle / IRD data have not arrived. Synthetic checks show power 0.32, so a fail is likely even if its variables matter. **[infrastructure]** | [`docs/RDL_V04_PROTOCOL.md`](RDL_V04_PROTOCOL.md), [`analysis/rdl_v04_test.py`](../analysis/rdl_v04_test.py) |
| Synergy on three climate streams | **FAIL**: no higher-order structure distinguishable from the null. Earlier "passes noise controls" held for synthetic data only. Two earlier runs failed at fetch (OpenAlex HTTP 429). **[blind]** | [`docs/SYNERGY_PROTOCOL.md`](SYNERGY_PROTOCOL.md) §8–§10, [`analysis/synergy_climate.py`](../analysis/synergy_climate.py) |
| GWI cross-article calibration | **FAIL**: the threshold does not transfer across articles ("Prime number" false-ignition rate 0.0134 > 0.010), so a GWI level is not a measurement and GWI cannot score UIA's I. **[blind]** | [`docs/GWI_CALIBRATION_PROTOCOL.md`](GWI_CALIBRATION_PROTOCOL.md) §7, [`analysis/gwi_calibration.py`](../analysis/gwi_calibration.py) |
| SMF | 6 of 12 earlier passes withdrawn after a proper significance test. **[known history]** | [`docs/SMF_PROTOCOL.md`](SMF_PROTOCOL.md) §13 |
| a_UIA | Retired: 4 of 6 terms not measurable. | [`docs/UIA_PROTOCOL.md`](UIA_PROTOCOL.md) |
| UIA direction rule (Option A) | 41–52% false positives on synthetic data at every sample size: unusable. The replacement permutation test holds 5% but has power 0.34–0.55 at 8 cases. **[infrastructure]** | [`docs/HE_CALIBRATION_PROTOCOL.md`](HE_CALIBRATION_PROTOCOL.md) §6, [`analysis/he_calibration.py`](../analysis/he_calibration.py) |
| Earlier white paper, deck, grants | Described a continuously running observatory, DestinE overlays, dashboards and pipelines that never ran; "first" claims unchecked. Marked superseded. | [`README.md`](../README.md); [`docs/F2_CLAIMS_GREP.md`](F2_CLAIMS_GREP.md) |
| DAC records | The original PPE event files were lost; a README line called an unsubmitted manuscript "under review"; the manuscript's data statement was not true. All corrected or recoded. | [`docs/STATUS.md`](STATUS.md), F1, F2, F8 |
| Conceptual DAC paper | Desk-rejected by *Futures* (submitted 17 Apr, rejected 18 Apr 2026). | [`docs/sources/dac_paper/README.md`](sources/dac_paper/README.md) |

## 5. How EMO keeps itself honest

These are working rules, written into [`CLAUDE.md`](../CLAUDE.md) and enforced where code can enforce them:

1. Every test is pre-registered (hypothesis, data, statistic, threshold) and committed before its data are opened.
2. Every result carries one evidence class; a test on known cases is never called blind.
3. A pass needs a significance test of the condition that decides it, with a null that respects dependence; a non-significant result is never evidence of no effect.
4. Multi-part measures are profiles, never weighted scores.
5. No status or priority word without evidence: checked in CI ([`scripts/claims_grep.py`](../scripts/claims_grep.py)).
6. Every run, fetch and failure gets a row in [`docs/RECORD.md`](RECORD.md).

## 6. What comes next [plan]

All items below are plans from [`docs/PLAN.md`](PLAN.md), none started unless stated.

- An independent human coder for the mpox case (protocol and packet committed; waiting for a volunteer) ([`docs/DOUBLE_CODING.md`](DOUBLE_CODING.md)).
- The UIA direction test, once 24 cases are coded (session 12).
- RDL v0.4, only when the Oslo–Seattle or IRD data arrive (session 13).
- Scoring the forecast ledger after 31 Dec 2026 (session 14).
- A software paper, a versioned release with a DOI, an annual report from the weekly-run data, then partners and funding (sessions 16–24).

What EMO cannot see today: anything outside the few domains above; any national or regional profile beyond the PPE and mpox files; any causal claim. What would change the picture most: a second human coder, the regime-effectiveness data, and the earliest scored blind forecasts.

## Data and code availability

Everything cited is in the public repository `avram3scu-art/emo-core-v1` (branch `emo-2026-10`), licensed AGPL-3.0 ([`LICENSE`](../LICENSE)).

## AI disclosure

1. All inputs were the author's own manuscript text, code and publicly available reference literature and data (plus synthetic simulation parameters where applicable).
2. All AI-assisted outputs were verified by the author.
3. All scientific claims and interpretations are the author's own.
