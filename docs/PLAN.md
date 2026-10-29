# EMO plan 2.0

Adrian N. Avramescu, Independent researcher, Antwerp. In force from 29 Oct 2026 (session 2.0-design, Adrian's yes, 04:57); written by Claude on Adrian's decision of 29 Oct 04:33 (`docs/STATUS.md`, session 15). Plan 1 is archived in `docs/archive/PLAN_1.md`. Basis: `docs/AUDIT_2026-10-29.md`; review: `docs/REVIEW_2_0_DRAFTS.md`.

## 1. The idea, made testable

Version 1 tried to measure a "mind" with quantities defined from the top down (a_UIA, synergy, organismality). Those failed or could not be computed (`docs/UIA_PROTOCOL.md`, `docs/SYNERGY_PROTOCOL.md`). The parts that worked are close to dated, concrete events: forecast skill, attention spikes, warning-to-delivery lags.

Plan 2.0 rebuilds the vision from what works. **The emergent mind is defined as a response loop** that a society runs when it faces a hazard:

| Link | Question | EMO tool | State today |
|---|---|---|---|
| Predict | Does it see the hazard coming, and better over time? | τ_I, SMF v2 | τ_I on NHC errors [exploratory]; SMF 6 of 12 [known history] |
| Attend | Does attention converge on it when it should? | GWI v2 | event test PASS [blind]; calibration FAIL [blind] |
| Decide and act | How fast do decisions and deliveries follow? | DAC | profiles [exploratory / known history] |
| Choose | Are its remedy choices better than naive ones? | RDL 2.0 (forecast registry) | 2 FAILs [known history]; ledger unscored [blind] |
| Learn | Does the loop get faster or better with experience? | loop-learning test (new) | not built |

**UIA 2.0** is the profile of these five links for one event or one season, never a weighted sum. **EMO** is the observatory that runs the loop measurements on a schedule. A loop with independent links is a set of agencies; a loop whose links are coupled and improve together is what the vision calls a mind. That is the claim that can now fail.

**Null model: independent agencies.** Each link responds to the hazard's severity on its own, with no influence from the other links beyond formal procedure (rule-based triggers, such as a warning that by rule starts a declaration). The mind reading is supported only where the loop beats this null: H4 and H5 must show coupling or learning that severity and formal procedure do not explain.

## 2. Hypotheses

| # | Hypothesis | Fails if | Status |
|---|---|---|---|
| H1 | Predict: forecast skill improves over time (supports the predict link only; carries no weight on the mind claim) | τ_I = 0 on the domain's forecasts | NHC 2.3–4.0%/yr [exploratory] |
| H2 | Attend: attention ignites on hazard events beyond calendar and seasonal drivers, with a threshold that transfers | GWI v2 fails its prospective calibration or event test | partial |
| H3 | Decide-act: action follows each event with an event-specific, measurable lag | lags not measurable from official records for most events | ozone/climate, PPE, mpox profiles |
| H4 | **Coupling beyond procedure**: events with earlier attention or better forecasts get faster action, after controlling for severity, region and every rule-based trigger, and beating the independent-agencies null | no significant association at power ≥ 0.8, or an equivalence bound excludes it | not tested |
| H5 | **Learning**: action lags shrink across seasons more than intensity mix and forecast gains explain | no significant trend in residual lags at adequate power | not tested |
| H6 | Generality: H4–H5 hold in a second hazard or region | they fail there | not tested |
| H7 | Choose: registered forecasts of response outcomes beat a naive baseline (Brier score) | no better than baseline after ≥ 20 resolved forecasts | 5 forecasts, unscored |

**Falsification, stated now.** If H4 and H5 both fail at adequate power in the hurricane domain, EMO reports publicly that the links are not shown to be coupled or learning there, and that the "mind" reading is unsupported for that domain. EMO then remains a set of response measurements, which is still useful, but the claim is withdrawn for that domain.

## 3. The engine domain: Atlantic hurricanes

Why: the loop repeats several times a season, so n grows every year and a coming season gives true blind tests. Two links are already in the repository. Data (from `docs/AUDIT_2026-10-29.md` §6; documentation only, no records opened):

- events: HURDAT2, refreshed weekly;
- predict: NHC official track errors (annual in the repo; per-storm verification **unverified**);
- attend: Wikipedia pageviews (from July 2015);
- decide-act: FEMA OpenFEMA Disaster Declarations Summaries (declaration and incident dates, from 1953; whether hurricanes are a listed incident type is **unverified**);
- outcome: NHC Tropical Cyclone Reports (**unverified**).

Limits: US only; a declaration is a decision, not a delivery; full four-link coverage starts in 2015 (about ten seasons). Every past season is **known history** (Claude's training and public knowledge); only seasons after a protocol's commit date are blind. The 2027 season (June–November) is the first blind loop test.

## 4. The four pillars, rebuilt

- **EMO** (observatory): the weekly run gains the loop event table and writes JSON results; a seasonal run scores the registry.
- **UIA 2.0**: the loop profile (predict, attend, act, choose, learn), per event and per season; the He direction test runs on loop events (24 needed, about ten seasons provide them).
- **DAC**: keeps its standard and pandemic files as deep case studies (double coding pending); the hurricane loop uses machine-readable records, so no hand coding is needed for the engine domain.
- **RDL 2.0**: v0.2/v0.3 code frozen as a record of two failures. Remedy work becomes a prospective registry of dated forecasts scored by Brier (H7), plus v0.4 calibration when OSP/IRD data arrive.

Repairs: GWI v2 (causal per-article seasonal baseline, Poisson-binomial, block-permutation null), SMF v2 (skill vs persistence as the definition), τ_I time-index fix; synergy parked unless a loop test needs it (`docs/AUDIT_2026-10-29.md` §3).

## 5. How every session runs

Rules: `CLAUDE.md` (2.0 after Adrian's yes). Every session has one task, names its hypothesis, pre-registers any test, records everything, runs the review (including improve-before-close), and ends with the next session's prompt.

**Opening prompt (template)**

```text
EMO session <N>: <name>. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session <N> in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: <H#>. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session <N> task: <task>
Inputs: <files, decisions>
Done when: <condition>
```

**Closing prompt (template)**

```text
Close session <N>. Run the review (more now, change or improve, improve before close) with your recommendation on each point; then the closing routine of CLAUDE.md, the seven-line report, and the full prompt for the next session in one block.
```

## 6. Sessions

Old sessions 12–14 and 16–24 (`docs/archive/PLAN_1.md`) are kept, re-sequenced below. Times are rough.

### 2.1 Clean ground (infrastructure; ~1 h)

```text
EMO session 2.1: clean ground. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.1 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (infrastructure). Stop when its "done when" is met, or tell me plainly why it cannot be met. Keep replies short.
Session 2.1 task: fix the defects that block 2.0 work (docs/AUDIT_2026-10-29.md D1, D8, D9, D10).
(1) README: correct the PPE line, test count and τ_I range from the repo files. (2) scripts/hooks/pre-push running claims_grep, ruff and the fast tests; document the install line. (3) A pinned lock file used by CI and the weekly run; check the frozen outputs still reproduce. (4) τ_I fitted on the time index, with a gapped-series test; recorded results must not change (probe in the audit). (5) docs/FAILURES.md: one row per recorded failure with its diagnosis and a recommended outcome (repair/replace/retire) for me to choose.
Done when: all five committed, CI and one weekly run green, my choices on FAILURES.md recorded.
```

### 2.2 Hurricane loop: data check (H3–H5; ~1 h)

```text
EMO session 2.2: hurricane loop data check. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.2 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3–H5 (feasibility). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.2 task: for each loop link (events, predict, attend, decide-act, outcome, warning times), open the source's documentation only, not its records, and record: fields, coverage, licence, update frequency, access method, caveats, and whether per-event values exist. Confirm whether FEMA lists hurricanes as an incident type, whether per-storm NHC verification and Tropical Cyclone Reports are machine-readable, and when watches/warnings were issued, and which rule-based triggers link warnings to declarations (legal basis, with sources). Write docs/LOOP_DATA.md with a feasible/infeasible verdict per link and a fallback for each infeasible one.
Done when: LOOP_DATA.md committed; no data record opened (stated in the file).
```

### 2.3 Hurricane loop: pre-registration (H3–H5; ~1.5 h)

```text
EMO session 2.3: loop protocol. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.3 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3, H4, H5. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.3 task: pre-register the loop tests in docs/LOOP_PROTOCOL.md before any loop record is opened: event definition from HURDAT2 (e.g. US landfall at hurricane strength), each link's measure and its reading rules, the H4 coupling statistic and the H5 learning statistic, controls (severity measures named in advance, region, year, every rule-based trigger found in 2.2), the independent-agencies null model (PLAN §1) that H4 and H5 must beat, a null that respects clustering by season, Holm correction, equivalence bounds for any "no effect" reading, and power and false-positive rate from synthetic data (code in analysis/, tests). Split: 2015–2025 = known history; the 2027 season = blind.
Done when: protocol, synthetic power code and tests committed; power stated; nothing opened.
```

### 2.4 Hurricane loop: event table (H3; ~1.5 h)

```text
EMO session 2.4: loop event table. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.4 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.4 task: build data/loop_hurricanes/ from the sources approved in LOOP_DATA.md with fetch scripts, sha256 and tests, following LOOP_PROTOCOL.md exactly; one row per event, one column group per link; validator and test that every value traces to its source row. Do not compute any H4 or H5 statistic.
Done when: table, fetch scripts and tests committed; CI green; no H4/H5 output exists.
```

### 2.5 Hurricane loop: first test (H4, H5; known history; ~1 h)

```text
EMO session 2.5: loop test on 2015–2025. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.5 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H4, H5. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.5 task: run the pre-registered H4 and H5 tests once on the 2015–2025 table (class: known history); report every condition with its significance test; diagnose any FAIL under the repair-don't-drop rule.
Done when: result committed in LOOP_PROTOCOL.md §results and RECORD; README and page updated with the evidence class.
```

### 2.6 GWI v2 (H2; ~1.5 h)

```text
EMO session 2.6: GWI v2. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.6 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H2. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.6 task: repair GWI (audit D2–D4): causal rolling baseline, per-article seasonal model, Poisson-binomial, block-permutation null. Pre-register its calibration and event tests on pageview data dated after the protocol commit only; synthetic false-positive rate and power first. Old GWI results stay unchanged.
Done when: protocol, code, tests and synthetic checks committed; the prospective test's first scoring date stated.
```

### 2.7 SMF v2 on the predict link (H1; ~1 h)

```text
EMO session 2.7: SMF v2. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.7 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H1. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.7 task: make skill vs persistence (Diebold–Mariano, Holm) the SMF definition in emo/ (audit D5); keep the correlation as a descriptive extra; pre-register its use on per-storm NHC forecasts if LOOP_DATA.md found them machine-readable, otherwise state why not.
Done when: code, tests and protocol committed; earlier SMF records unchanged.
```

### 2.8 Blind registry for the 2027 season (H4, H5, H7; before 1 June 2027)

```text
EMO session 2.8: 2027 season registry. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.8 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H4, H5, H7. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.8 task: register dated, scored predictions for the 2027 Atlantic season (e.g. the distribution of decide-act lags conditional on intensity, from the 2015–2025 model) in the forecast ledger, with sha256 and a Zenodo version; scoring rule fixed now.
Done when: ledger entries committed and deposited before 1 June 2027.
```

### 2.9 UIA 2.0 and the He test (H4; after 2.5; ~1.5 h)

```text
EMO session 2.9: UIA 2.0 loop profile and He direction test. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.9 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H4. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.9 task: define UIA 2.0 as the per-event profile of the loop links (docs/UIA_PROTOCOL.md §2.0, never a weighted sum); pre-register the He direction test (permutation test T-D, docs/HE_CALIBRATION_PROTOCOL.md) on loop events not yet used in 2.5 if any remain, else label known history; run once.
Done when: protocol, result and evidence class committed.
```

### 2.10 RDL 2.0 and the ledger (H7; after 31 Dec 2026; was session 14)

```text
EMO session 2.10: forecast ledger scoring. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.10 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H7. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.10 task: score every resolved ledger forecast with analysis/score_forecast_ledger.py (Brier vs 0.5 baseline), record outcomes with sources opened, add a new Zenodo version; mark RDL v0.2/v0.3 code frozen in its docstrings. RDL v0.4 runs only when OSP/IRD data arrive (was session 13).
Done when: scores committed and deposited.
```

### 2.11 DAC: second coder and a second hazard (H3, H6)

```text
EMO session 2.11: DAC agreement and second-hazard feasibility. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.11 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3, H6. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.11 task: when a coder's sheet returns, compute the pre-registered agreement (docs/DOUBLE_CODING.md); separately, check documentation only for a second loop domain with dated public records (e.g. EU floods or heatwaves), with a feasible/infeasible verdict.
Done when: agreement result (if a sheet exists) and feasibility note committed.
```

### 2.12 2027 season blind scoring (H4, H5, H7; December 2027)

```text
EMO session 2.12: score the 2027 season. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.12 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H4, H5, H7. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.12 task: build the 2027 rows exactly as in 2.4, score the registered predictions and the H4/H5 tests on 2027 only (class: blind), report every condition, and apply repair-don't-drop to any FAIL.
Done when: results committed; README, page and STATUS updated.
```

### 2.13 onward: credibility, partners, money (old sessions 15–24, after 2.5)

The white paper is revised from the session 15 review once loop results exist; then the software paper (old 16), release 1.0 (old 17), State of the Mirror (old 18), briefs (old 19), first partner (old 20), legal home (old 21), first grant (old 22), consortium role (old 23), paid layer (old 24). Their prompts in `docs/archive/PLAN_1.md` are kept unchanged, with "Hypothesis moved" added.

## 7. Where Claude pushes back

- The hurricane loop is US-specific and decision-based; it can support the "mind" reading only for one hazard in one country. H6 is required before any general claim.
- Ten seasons is a small n for coupling with controls; power may stay below 0.8 until several blind seasons accumulate. The plan is slow by design.
- Attention and action share a driver (storm severity); H4 can be confounded even with controls. The protocol must say what result would count as coupling beyond severity.
- None of this needs new grand theory. If a new tool is needed, it is built only when a pre-registered test shows the old one cannot answer the question.
