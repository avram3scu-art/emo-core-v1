# EMO 2.0: from prototype to a testable emergent mind

29 Oct 2026 · Adrian N. Avramescu, Independent researcher, Antwerp

**Read this before every session (Adrian and Claude).** It is the roadmap of record. Rules: `CLAUDE.md` 2.0. Where we are now: `docs/STATUS.md`. History: `docs/SESSION_LOG.md`. Written by Claude on Adrian's decisions of 29 Oct 2026 (04:33, 04:57). A reading copy for the phone, `docs/PLAN.docx`, is made from this file with `pandoc docs/PLAN.md -o docs/PLAN.docx` and is regenerated in every commit that changes this file; if they differ, this file wins. It keeps the structure of plan 1, "EMO: from prototype to planetary program" (21 Oct 2026; committed in `docs/sources/plan/`, text in `docs/archive/PLAN_1.md`). Basis: `docs/AUDIT_2026-10-29.md`; review: `docs/REVIEW_2_0_DRAFTS.md`.

EMO tests one idea: that humanity's response to a hazard behaves like a mind, a loop whose links are coupled and learn. The route runs through tests that can fail, in a domain that repeats every year, before reports, partners or money.

## 1. Where each pillar stands (29 Oct 2026)

| Pillar | Works on real data today | Not yet working | Evidence |
|---|---|---|---|
| DAC (decide-act link) | Ozone vs climate lags [exploratory]; PPE 5 countries + EU recoded from primary sources [known history]; mpox EU [known history] | Every file coded by Claude; no human recode yet | `data/dac_*`, `docs/DAC_*.md`, `docs/DOUBLE_CODING.md` |
| EMO metrics (predict, attend) | τ_I on NHC errors 2.3–4.0 %/yr [exploratory]; GWI event test PASS [blind]; SMF 6 of 12 [known history] | GWI calibration FAIL; synergy FAIL; GWI and SMF need repair (audit D2–D5) | `docs/GWI_*.md`, `docs/SMF_PROTOCOL.md`, `docs/SYNERGY_PROTOCOL.md` |
| RDL (choose link) | Forecast ledger, 5 forecasts on Zenodo [blind], unscored | v0.2, v0.3 FAIL [known history]; v0.4 waits for OSP/IRD data | `docs/RDL_*.md` |
| UIA (loop profile) | none scored | a_UIA retired; loop profile defined in this plan, not built | `docs/UIA_PROTOCOL.md` |
| Learn link | none | not built | this plan, H5 |
| Running | Weekly run every Monday (external scheduler); CI with claim-word check; 149 tests | no hook, no lock file (audit D8, D9) | `.github/workflows/` |

## 2. What must hold before anyone outside sees EMO

1. **Claims match code**, with one evidence class on every result.
2. **Profiles, not one gauge.**
3. **Every test can fail**, is pre-registered with its power, and failures stay on record and are repaired, replaced or retired.
4. **Prospective tests first**; a fix is never tested on data already seen.
5. **Name what exists** (`docs/RELATED_WORK.md`); no novelty without a search.

## 3. The idea, made testable

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

## 4. Hypotheses

| # | Hypothesis | Fails if | Status |
|---|---|---|---|
| H1 | Predict: forecast skill improves over time (supports the predict link only; carries no weight on the mind claim) | τ_I = 0 on the domain's forecasts | NHC 2.3–4.0%/yr [exploratory] *Note 29 Oct 2026 (session 2.7):* SMF v2 (skill vs persistence, DM, Holm) is the SMF definition; one-season test of OFCL vs OCD5 on 2026 storms pre-registered (`docs/SMF_PROTOCOL.md` §15), scored after 1 May 2027 |
| H2 | Attend: attention ignites on hazard events beyond calendar and seasonal drivers, with a threshold that transfers | GWI v2 fails its prospective calibration or event test | partial. *Note 29 Oct 2026 (session 2.6):* GWI v2 pre-registered (`docs/GWI_V2_PROTOCOL.md`): 20-placebo calibration and M ≥ 7 earthquake event test on 1 Nov 2026 – 31 Oct 2027, scored 15 Nov 2027 |
| H3 | Decide-act: action follows each event with an event-specific, measurable lag | lags not measurable from official records for most events | ozone/climate, PPE, mpox profiles |
| H4 | **Coupling beyond procedure**: events with earlier attention or better forecasts get faster action, after controlling for severity, region and every rule-based trigger, and beating the independent-agencies null | no significant association at power ≥ 0.8, or an equivalence bound excludes it | not tested. *Note 29 Oct 2026 (session 2.8):* 2015–2025 cannot test it (guard §15); the hurricane blind arm (A → Y_state, `docs/LOOP_PROTOCOL.md` §20.5) has power 0.15 after 5 blind seasons and 0.38 after 10 at about 2 measured storms per season, and cannot reject at all before about 5 seasons; H4 cannot be decided in this domain before about 2036, so a second domain (H6) or pooling across domains is the only route to adequate power. *Note 29 Oct 2026 (session 2.9):* uncontrolled He direction test (T-D, within-season null) PASS on known history, p = 0.012, led by attention, which rises with intensity; not evidence of coupling beyond procedure (`docs/HE_CALIBRATION_PROTOCOL.md` §10.7) |
| H5 | **Learning**: action lags shrink across seasons more than intensity mix and forecast gains explain | no significant trend in residual lags at adequate power | not tested. *Note 29 Oct 2026 (session 2.3):* synthetic power 0.12–0.41 with ~9 seasons (`docs/LOOP_PROTOCOL.md` §10); adequate power is not reachable before about 2030, so a non-significant H5 reads "not shown at this size", never FAIL |
| H6 | Generality: H4–H5 hold in a second hazard or region | they fail there | not tested |
| H7 | Choose: registered forecasts of response outcomes beat a naive baseline (Brier score) | no better than baseline after ≥ 20 resolved forecasts | 5 forecasts, unscored. *Note 29 Oct 2026 (session 2.8):* 10 hurricane-loop forecasts for 2027 registered (`docs/LOOP_PROTOCOL.md` §21), scored in 2.12b |

**Falsification, stated now.** If H4 and H5 both fail at adequate power in the hurricane domain, EMO reports publicly that the links are not shown to be coupled or learning there, and that the "mind" reading is unsupported for that domain. EMO then remains a set of response measurements, which is still useful, but the claim is withdrawn for that domain.

## 5. The engine domain: Atlantic hurricanes

Why: the loop repeats several times a season, so n grows every year and a coming season gives true blind tests. Two links are already in the repository. Data (from `docs/AUDIT_2026-10-29.md` §6; documentation only, no records opened):

- events: HURDAT2, refreshed weekly;
- predict: NHC official track errors (annual in the repo; per-storm verification **unverified**);
- attend: Wikipedia pageviews (from July 2015);
- decide-act: FEMA OpenFEMA Disaster Declarations Summaries (declaration and incident dates, from 1953; whether hurricanes are a listed incident type is **unverified**);
- outcome: NHC Tropical Cyclone Reports (**unverified**).

Limits: US only; a declaration is a decision, not a delivery; full four-link coverage starts in 2015 (about ten seasons). Every past season is **known history** (Claude's training and public knowledge); only seasons after a protocol's commit date are blind. The 2027 season (June–November) is the first blind loop test.

## 6. The four pillars, rebuilt

- **EMO** (observatory): the weekly run gains the loop event table and writes JSON results; a seasonal run scores the registry.
- **UIA 2.0**: the loop profile (predict, attend, act, choose, learn), per event and per season; the He direction test runs on loop events (24 needed, about ten seasons provide them).
- **DAC**: keeps its standard and pandemic files as deep case studies (double coding pending); the hurricane loop uses machine-readable records, so no hand coding is needed for the engine domain.
- **RDL 2.0**: v0.2/v0.3 code frozen as a record of two failures. Remedy work becomes a prospective registry of dated forecasts scored by Brier (H7), plus v0.4 calibration when OSP/IRD data arrive.

Repairs: GWI v2 (causal per-article seasonal baseline, Poisson-binomial, block-permutation null), SMF v2 (skill vs persistence as the definition), τ_I time-index fix; synergy parked unless a loop test needs it (`docs/AUDIT_2026-10-29.md` §3).

## 7. Who benefits, and who would pay

Carried from plan 1 unchanged in substance; no new sources opened. Order of use: research partners (methods, validation, a host, a second coder), crisis and early-warning bodies (loop profiles per event; possible pilots), ministries (where delay sits; pilot contracts only), multilaterals (funders of methods if EMO adds what existing indicators lack), investors and rating agencies (later, only if a paid layer is decided), civil society and media (the public mirror; legitimacy, not money), philanthropy (main funder of the public layer). Two kinds of EMO follow: an open public mirror, and possibly, later, paid services that must not compromise it (decision in 2.22).

## 8. Roadmap: four phases, four gates

No phase starts on the calendar; each starts when its gate is met.

| Phase | Sessions | Gate to enter the next phase |
|---|---|---|
| A. Clean ground, loop design | 2.1–2.4 | loop event table built under a committed protocol; README true |
| B. The loop on the record | 2.5–2.12b | at least one H4/H5 result recorded (pass or fail) and GWI v2 pre-registered; 2027 registry deposited before 1 June 2027 |
| C. Credibility | 2.13–2.17 | release DOI resolves; report reproducible |
| D. Partners and money | 2.18–2.22 | a partner's written reply |

Sessions 2.8, 2.10, 2.12 and 2.12b have fixed dates (2.12b: when the HURDAT2 file covering 2027 exists, about May 2028); 2.11, 2.18 and 2.21 depend on other people's replies.

## 9. Session by session

**Phase A: clean ground, loop design**

| # | Session | Hypothesis | Done when |
|---|---|---|---|
| 2.1 | Clean ground | infrastructure | README, hook, lock file, τ_I fix, FAILURES.md committed; CI and weekly run green |
| 2.2 | Loop data check | H3–H5 | `docs/LOOP_DATA.md` with a verdict per link; no record opened |
| 2.3 | Loop protocol | H3–H5 | protocol, power code, tests committed; nothing opened |
| 2.4 | Loop event table | H3 | table, fetch scripts, tests; no H4/H5 output |

**Phase B: the loop on the record**

| # | Session | Hypothesis | Done when |
|---|---|---|---|
| 2.5 | Loop test 2015–2025 | H3, H4, H5 | result recorded [known history] |
| 2.6 | GWI v2 | H2 | protocol, code, synthetic checks; prospective scoring date |
| 2.7 | SMF v2 | H1 | code, tests, protocol |
| 2.8 | 2027 registry | H4, H5, H7 | deposited before 1 June 2027 |
| 2.9 | UIA 2.0, He test | H4 | result recorded |
| 2.10 | Ledger scoring (after 31 Dec 2026) | H7 | scores deposited |
| 2.11 | DAC agreement, second hazard | H3, H6 | agreement (if a sheet returned) and feasibility note |
| 2.12 | GWI v2 scoring (15 Nov 2027) | H2 | blind result recorded |
| 2.12b | Score the 2027 hurricane season (after HURDAT2 2027, ~May 2028) | H3, H4, H7 | blind results recorded |

**Phase C: credibility**: 2.13 white paper 2.0; 2.14 software paper; 2.15 release 1.0; 2.16 State of the Mirror 2027 (after 2.12b); 2.17 briefs.

**Phase D: partners and money**: 2.18 first partner; 2.19 legal home; 2.20 first grant; 2.21 consortium role; 2.22 paid layer, yes or no.

## 10. How every session starts and ends

Every session is a new conversation with avram3scu-art/emo-core-v1 as its repository. Paste the session's prompt (§11, or the one Claude gave at the last close); at the end paste the closing block, so the work is recorded in the repo, not only in the chat.

**Opening block (template; each prompt in §11 is already complete):**

```text
EMO session <N>: <name>. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session <N> in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: <H#>. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session <N> task: <task>
Inputs: <files, decisions>
Done when: <condition>
```

**Closing block (paste at the end, every session):**

```text
Close the session. Run the review (more now, change or improve, improve before close) with your recommendation on each point and wait for my answer. Then the closing routine of CLAUDE.md: record check, STATUS, SESSION_LOG, commit and push; the seven-line report (done, not done with reasons, result, hypothesis moved, could still do or improve, next session, anything I must do); and the full prompt for the next session in one block, also committed in docs/PLAN.md.
```

## 11. Session prompts

### Phase A and B

### 2.1 Clean ground (infrastructure; ~1–1.5 h)

```text
EMO session 2.1: clean ground. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (2.0), docs/STATUS.md and the entry for session 2.1 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (infrastructure). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.1 task: fix the defects that block 2.0 work (docs/AUDIT_2026-10-29.md D1, D8, D9, D10) and start the failure register.
(1) README.md: correct every stale line from the repo files (PPE case now in data/dac_ppe/, test count from the latest CI run, τ_I 2.3% at 12 h and 3.0–4.0% at 24–120 h from results/weekly/), point to docs/PLAN.md 2.0 and the white-paper draft, and add the contributions line from CLAUDE.md under the AI disclosure. Then run claims_grep.
(2) scripts/hooks/pre-push: runs claims_grep (must be unjustified=0), ruff and the fast tests, and refuses the push on any failure; install it in this clone (git config core.hooksPath scripts/hooks) and prove it with a planted failing claim that it blocks, then remove the plant.
(3) A pinned lock file (exact versions) used by CI and the weekly run; then start one weekly run and check that every frozen output still reproduces.
(4) emo/info_time.py: fit the slope on the series' time index (numeric or datetime), with a test on a gapped series; the recorded τ_I results must not change beyond the audit's probe (72 h: 3.715 → 3.713 %/yr).
(5) docs/FAILURES.md: one row per recorded failure (RDL v0.2, RDL v0.3, synergy, GWI calibration, GWI placebo condition, SMF withdrawn passes, a_UIA, He Option A rule, superseded documents, lost DAC files, Futures desk rejection), each with its diagnosis, evidence file and Claude's recommended outcome (repair / replace / retire, one-line reason). Ask me to choose; record my choices.
Inputs: docs/AUDIT_2026-10-29.md; docs/REVIEW_S15_WHITEPAPER.md (README points 3, 6); contributions line in CLAUDE.md (my decision, 29 Oct 05:15); docs/PLAN.md §4–§6 (loop links for "replace").
Done when: all five committed; the hook blocks a planted failure; CI and one weekly run green with frozen outputs reproduced; my choices on FAILURES.md recorded.
```

### 2.2 Hurricane loop: data check (H3–H5; ~1 h)

```text
EMO session 2.2: hurricane loop data check. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.2 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3–H5 (feasibility). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.2 task: for each loop link (events, predict, attend, decide-act, outcome, warning times), open the source's documentation only, not its records, and record: fields, coverage, licence, update frequency, access method, caveats, and whether per-event values exist. Confirm whether FEMA lists hurricanes as an incident type, whether per-storm NHC verification and Tropical Cyclone Reports are machine-readable, and when watches/warnings were issued, and which rule-based triggers link warnings to declarations (legal basis, with sources). Write docs/LOOP_DATA.md with a feasible/infeasible verdict per link and a fallback for each infeasible one.
Inputs: docs/AUDIT_2026-10-29.md §6 (documentation already opened: FEMA OpenFEMA Disaster Declarations Summaries page); docs/PLAN.md §5; docs/FAILURES.md (Adrian's outcomes, 29 Oct 05:29). From session 2.1: in a new clone run git config core.hooksPath scripts/hooks before the first push (the pre-push hook runs claims_grep, ruff and the tests) and install from requirements-lock.txt (pip install -r requirements-lock.txt, then pip install --no-deps -e ".[dev]").
Done when: LOOP_DATA.md committed; no data record opened (stated in the file); CI green.
```

### 2.3 Hurricane loop: pre-registration (H3–H5; ~1.5 h)

```text
EMO session 2.3: loop protocol. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.3 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3, H4, H5. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.3 task: pre-register the loop tests in docs/LOOP_PROTOCOL.md before any loop record is opened: event definition from HURDAT2 (e.g. US landfall, record identifier L, at HU status), each link's measure and its reading rules, the H4 coupling statistic and the H5 learning statistic, controls (severity measures named in advance, region, year, every rule-based trigger found in 2.2), the independent-agencies null model (PLAN §3) that H4 and H5 must beat, a null that respects clustering by season and by storm, Holm correction, equivalence bounds for any "no effect" reading, and power and false-positive rate from synthetic data (code in analysis/, tests). Split: 2015–2025 = known history; the 2027 season = blind.
Use these 2.2 findings (docs/LOOP_DATA.md): (1) decide-act: select declarations on designatedIncidentTypes containing H (the incidentType string is unverified); split major disaster (DR) and emergency (EM); measure two lags, landfall→declarationRequestDate (state) and request→declarationDate (federal); fix the storm→declaration matching rule (state, dates, declarationTitle, incidentId). (2) Exclude or control pre-landfall EM declarations: FEMA's 2006 pre-landfall policy ties them to an NWS threat projection plus evacuation orders, so they are procedure, not coupling; the test must hold whether or not that policy is still in force. (3) Predict: per-storm OFCL skill vs CLIPER5/SHIFOR5 from the individual-forecast file (STMID); forecasts < 18 h apart are not independent (use the file's equivalent sample size or a cluster-by-storm null). (4) Attend: per-article daily user-agent pageviews from July 2015; fix the storm→article rule in advance (redirects, articles created after naming). (5) Warnings: earliest watch/warning per storm from the NHC GIS advisory files (2008+). (6) Outcome: not machine-readable; use HURDAT2 landfall intensity as the severity control, not as a measured link.
Inputs: docs/LOOP_DATA.md; docs/PLAN.md §3–§5; docs/HE_CALIBRATION_PROTOCOL.md and analysis/he_calibration.py (power-simulation pattern); docs/FAILURES.md. In a new clone: git config core.hooksPath scripts/hooks; pip install -r requirements-lock.txt, then pip install --no-deps -e ".[dev]".
Done when: protocol, synthetic power code and tests committed; power and false-positive rate stated; no loop record opened (stated in the file); CI green.
```

### 2.4 Hurricane loop: event table (H3; ~1.5 h)

```text
EMO session 2.4: loop event table. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.4 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.4 task: build data/loop_hurricanes/ from the sources approved in LOOP_DATA.md with fetch scripts, sha256 and tests, following LOOP_PROTOCOL.md exactly; one row per event, one column group per link; validator and test that every value traces to its source row. Do not compute any H4 or H5 statistic.
Use these 2.3 decisions (docs/LOOP_PROTOCOL.md §14–§15): (1) primary event set HU+TS: US landfall (L) at status HU or TS, seasons 2015–2025; designatedIncidentTypes containing H or 4; HU-only flagged as a secondary column. (2) Two sources new in 2.3 and unverified: the US Census Bureau cartographic boundary file (landfall state, 50 km rule) and the MediaWiki redirect resolution for the article rule (§3.3); open and record their documentation first; if either cannot be opened, use the protocol's fallback and say so. (3) Record the incidentType string for matched hurricanes (open item from 2.2). (4) Record, per event, every exclusion with its reason (§8.2). (5) Output also the realized season sizes and per-link missingness (counts only), which 2.5 needs for the §15 guard; compute no lag correlation, no trend and no link-to-link statistic.
Done when: table, fetch scripts and tests committed; CI green; no H4/H5 output exists.
```

### 2.5 Hurricane loop: first test (H3, H4, H5; known history; ~1 h)

```text
EMO session 2.5: loop test on 2015–2025. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.5 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3, H4, H5. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.5 task: run the pre-registered tests once on the 2015–2025 table data/loop_hurricanes/loop_events.csv (class: known history), exactly as docs/LOOP_PROTOCOL.md §5–§8 with §14–§16 (amendments 3–6): first run scripts/validate_loop_table.py; then H3 (§8.1); then the §15 guard from data/loop_hurricanes/summary.json counts only (per-pair Σ(n_s−1)−5 ≥ 15; analysis/loop_power.py rerun with STAT "fe", Y_SHOCK_SIGN −1 at the realized season sizes and missingness) before any H4 statistic; then H4 and H5 only where the guard allows; report every condition with its significance test; list every exclusion from data/loop_hurricanes/exclusions.csv; diagnose any FAIL under the repair-don't-drop rule.
Use these 2.4 findings: (1) 52 events (27 HU), both lags measured for only 24, so the guard will likely bind; report "cannot be tested at this size" where it does. (2) 14 of 52 attention targets are list or season pages (column at_target_kind): A stays as registered; add one sensitivity without them, labelled no weight. (3) 22 storms have no FEMA candidate of a qualifying type (some storms' declarations are typed "Severe Storm"/"Flood"): list them descriptively, no rule change. (4) F uses OCD5 as baseline (amendment 6); W parses the local ADVDATE format from 2017 (§16 rule 7 note). (5) Any rule change found needed becomes an amendment for the blind arm (session 2.8), never applied to 2015–2025.
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
Session 2.8 task: register dated, scored predictions for the 2027 Atlantic season (e.g. the distribution of decide-act lags conditional on intensity, from the 2015–2025 model) in the forecast ledger, with sha256 and a Zenodo version; scoring rule fixed now. Also register, as amendments in docs/LOOP_PROTOCOL.md for the 2027+ blind arm only (never applied to 2015–2025), the three changes Adrian approved in the 2.5 review (29 Oct 2026, 09:53): (a) H3 repair (FAILURES F12): H3 defined on storms with a qualifying DR request, and the share of landfalling storms with any federal declaration reported as a separate declaration-rate measure; state the event set (HU+TS or HU) and its power (§15 HU-only 0.40 at r = 0.5); (b) the blind-arm pair (§7): 2.5 gave no H4 p-value (guard §15 bound all six pairs), so fix the pair by a stated rule that uses no 2015–2025 lag value; (c) the attention target rule (§3.3): list or season pages (at_target_kind) no longer accepted as target. Each amendment gets its synthetic false-positive rate and power before 2027 data exist. Inputs: docs/LOOP_PROTOCOL.md §18–§19, docs/FAILURES.md F12, analysis/loop_power_realized_output.txt.
Session-start check (not part of the task; added in session 2.7, Adrian 10:48): SMF v2 NHC test (docs/SMF_PROTOCOL.md §15 rule 8). If today is on or after 1 May 2027, run `python scripts/fetch_smf_v2_nhc.py HURDAT2_URL` once a HURDAT2 file covering 2026 exists; it prints counts only. If the 2026 lines exist, tell me and propose the scoring session (analysis/smf_v2_nhc2026.py, run once). If today is before 1 May 2027, say so and do nothing. If none by 1 Oct 2027, record "not available" per §15.
Done when: ledger entries committed and deposited before 1 June 2027.
```

### 2.9 UIA 2.0 and the He test (H4; after 2.5; ~1.5 h)

```text
EMO session 2.9: UIA 2.0 loop profile and He direction test. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.9 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H4. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.9 task: define UIA 2.0 as the per-event profile of the loop links (docs/UIA_PROTOCOL.md §2.0, never a weighted sum); pre-register the He direction test (permutation test T-D, docs/HE_CALIBRATION_PROTOCOL.md) on loop events not yet used in 2.5 if any remain, else label known history; run once. Use this 2.8 finding: all 52 events of 2015–2025 entered the 2.5 run (docs/LOOP_PROTOCOL.md §19), so none remains unused and the He test is labelled pre-registered on known history; 2027 rows are reserved for 2.12b and must not be used.
Done when: protocol, result and evidence class committed.
```

### 2.10 RDL 2.0 and the ledger (H7; after 31 Dec 2026; was session 14)

**Do not paste before 1 Jan 2027.** Started early on 29 Oct 2026 and stopped: no forecast had resolved (record in `docs/STATUS.md`, session 2.10 early attempt). Earliest resolve_by: F001, 31 Dec 2026.

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

### 2.11b Flood loop: data check and prospective protocol (H6, H4; from 2.11)

```text
EMO session 2.11b: flood loop, data check and prospective protocol. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.11b in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H6 (and H4 power by pooling). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.11b task: using docs/SECOND_DOMAIN_FEASIBILITY.md (EU floods feasible pending; C1 open), (1) settle C1 from documentation: does the EFAS formal-notification archive reach back 10 years with day-level dates per river and country; (2) if yes, write and commit a prospective flood-loop protocol for events after its commit date: events = EFAS formal notifications in EU states, decide-act = CEMS Rapid Mapping activation by a national authority (no activation is a valid outcome), attend = Wikipedia pageviews, with statistic, pass/fail rule, and synthetic false-positive rate and power at about 10–20 events a year, before any flood lag is computed. Do not compute any lag from data/second_domain/cems_activations_2026-10-29.json (only counts were seen in 2.11).
Done when: C1 verdict committed, and either the protocol with its synthetic power is committed or the reason it cannot be is recorded.
```

### 2.12 GWI v2 scoring (H2; on or after Mon 15 Nov 2027)

*Split in session 2.8 (Adrian 11:11, "2 - yes"): the 2027 hurricane rows need the HURDAT2 file covering 2027 (about May 2028), so the loop scoring moved to 2.12b.*

```text
EMO session 2.12: GWI v2 prospective scoring. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.12 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H2. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.12 task: if not done since 15 Nov 2027, run .github/workflows/gwi_v2_fetch.yml once, score as docs/GWI_V2_PROTOCOL.md registers (one scoring, no interim look), record the result in §11, README and RECORD (class: pre-registered blind), and apply repair-don't-drop to any FAIL. Session-start reminder: the cron-job.org token expires 26 Oct 2027; if not yet renewed, say so first.
Done when: result committed; README, page and STATUS updated.
```

### 2.12b Score the 2027 hurricane season (H3, H4, H7; when the HURDAT2 file covering 2027 exists, about May 2028)

```text
EMO session 2.12b: score the 2027 hurricane season. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.12b in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3, H4, H7. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.12b task: if a HURDAT2 file covering 2027 exists (if none by 1 Oct 2028, record the 2027 forecasts as void per docs/LOOP_PROTOCOL.md §21 rule 6 and stop), first, before building any 2027 row, pre-register a severity-adjusted He direction test (session 2.9 review, Adrian 11:58: T-D on F, A, W vs He = −(Y_state + Y_fed), permuted within season × V-tertile strata, tertile cuts frozen from 2015–2025; synthetic FPR and power at the expected 2027 size, power below 0.5 stated in its first line; run it on the 2027 rows as item 5, class pre-registered blind); then build the 2027 rows exactly as in 2.4 (§16) with amendments 7–9 (§20; amendment 9 rejects list/season attention targets), OpenFEMA pulled the same day. Then, class pre-registered blind, report: (1) the declaration-rate measure (§20.1, Clopper-Pearson); (2) H3r only if the pooled 2027+ DR-candidate count D ≥ 12, else "H3r not yet run (D = n)"; (3) the blind H4 pair A → Y_state (§20.2, §7 with §14 residuals): if the blind seasons give fewer than 20 within-season arrangements of the complete cases, "cannot be tested at this size" (§20.5), else the one-sided permutation p with its §20.5 power; (4) score the ten ledger forecasts L2027-01…10 (data/loop_forecast_ledger.csv; check its SHA-256 against data/loop_forecast_ledger.sha256 and the Zenodo version first) by §21 rule 5 (Brier vs the pooled baseline, sign-flip test; power 0.23, so non-significant reads "not shown at this size"), outcomes with sources opened, and add a Zenodo version; (5) the severity-adjusted He direction test registered at the start. Apply repair-don't-drop to any FAIL.
Done when: results committed; README, page and STATUS updated; ledger outcomes deposited.
```

### Phase C: credibility

### 2.13 White paper 2.0 (credibility; after 2.5)

```text
EMO session 2.13: white paper 2.0. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.13 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (reports H1–H7). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.13 task: revise docs/WHITEPAPER_EMO_what_runs_today.md with the loop results to date, fixing every point of docs/REVIEW_S15_WHITEPAPER.md (disclosure point 2 only after my recorded verification; vision tied to H1–H7; one audience and one ask). Every factual statement links to a repo file or is marked [plan]; evidence class on every result. Then a hostile editor-style review.
Done when: draft committed and reviewed; nothing sent out the same day.
```

### 2.14 Software paper (credibility)

```text
EMO session 2.14: software paper. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.14 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (infrastructure). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.14 task: prepare a Journal of Open Source Software submission. First open JOSS's current submission requirements and AI usage policy and check EMO against each, listing gaps. Fix small gaps; list large ones. Draft paper.md (summary, statement of need, related work from docs/RELATED_WORK.md, AI usage disclosure in my three-point form, contributions line as decided in STATUS). Give an editor-style review with a realistic verdict.
Done when: checklist and draft committed; submission waits at least one day after the review.
```

### 2.15 Release 1.0 (credibility)

```text
EMO session 2.15: release 1.0. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.15 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (infrastructure). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.15 task: tag and archive release 1.0. Add CITATION.cff (Adrian N. Avramescu, ORCID 0009-0005-1393-5264), a CHANGELOG, and check that the Zenodo-GitHub integration is on for avram3scu-art/emo-core-v1. Make sure tests pass, then create the v1.0.0 release with notes stating what works and what does not.
Done when: the Zenodo DOI for the release resolves.
```

### 2.16 State of the Mirror 2027 (credibility; after 2.12)

```text
EMO session 2.16: state of the mirror 2027. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.16 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H1–H7 (report). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.16 task: write reports/state_of_the_mirror_2027.md from the weekly-run data and the 2027 season: what each loop link shows, H1–H7 status with evidence classes, what failed and why, what EMO cannot yet see. Every figure produced by a script in the repo and reproducible from the release. Under 3,000 words.
Done when: every figure regenerates from the repo.
```

### 2.17 One-page briefs (credibility)

```text
EMO session 2.17: one-page briefs. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.17 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.17 task: three one-page briefs for (a) research partners, (b) crisis and early-warning bodies, (c) funders: what EMO measures today, one result each would care about, what we ask of them, what EMO does not claim. Every claim traceable to the report or repo. No Substack or Zenodo portfolio links.
Done when: three briefs committed in docs/briefs/.
```

### Phase D: partners and money

### 2.18 First partner (partners)

```text
EMO session 2.18: first partner. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.18 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.18 task: approach the first partner. Draft a short email to the Earth System Governance Project network (I was previously invited as a Fellow) with the honest status: what runs, the release DOI, the annual report, the failures, and one concrete ask (methods feedback, a co-author, a second coder, or hosting). No exaggeration, no portfolio links. Give me two variants; I choose and send.
Done when: email sent by me; reply and contact recorded in STATUS when it arrives.
```

### 2.19 Legal home (partners)

```text
EMO session 2.19: legal home. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.19 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.19 task: decide where EMO legally lives. Compare, with sources opened: a Belgian non-profit (VZW/ASBL) founded by me, hosting by a partner institution, or staying an individual open-source project. For each: cost, time, who can receive grants, governance, fit with EMO's openness. Recommend one; I decide.
Done when: decision recorded in docs/GOVERNANCE.md.
```

### 2.20 First grant (money)

```text
EMO session 2.20: first grant. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.20 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.20 task: one small grant application. Open the current NLnet calls (and up to two other open-source or public-good funders you find and verify). Check eligibility, deadline and AI policy (NLnet asked for prompts and logs from AI-assisted work as of 21 Oct 2026; recheck). Draft the application for a concrete technical deliverable (e.g. the loop event table and its weekly run, or the DAC standard and validator), with full AI disclosure. Editor-style review before I submit; never the same day.
Done when: application ready for my submission.
```

### 2.21 Consortium role (partners; needs 2.18)

```text
EMO session 2.21: consortium role. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.21 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.21 task: EMO as a work package in a partner's bid. With the partner from 2.18: find a current Horizon Europe or comparable call that fits, open its text, draft a one-page work-package description (objectives, deliverables, months, cost) for EMO's part. Only what EMO can do by then.
Done when: partner agrees in writing to include it.
```

### 2.22 Paid layer, yes or no (money)

```text
EMO session 2.22: paid layer, yes or no. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.22 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none. Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.22 task: decide whether EMO gets a paid service. Set out, with evidence: possible paying users, existing competitors, cost to build, and the risk to EMO's open, non-oracular public layer. Case for and against; I decide. Investor material only if the answer is yes and at least one real user has asked for it.
Done when: decision and its rules recorded in docs/GOVERNANCE.md.
```

## 12. Funding ladder

Carried from plan 1 (facts as checked on 21 Oct 2026; not reopened). Money follows evidence.

| Rung | Source | Size | Needs first | Status of the fact |
|---|---|---|---|---|
| 0 | Our time; free public-repository tools | none | — | Known |
| 1 | NLnet open calls | €5,000–50,000 first grant; individuals may apply | clear technical deliverable; AI disclosure with prompts and logs | Verified on nlnet.nl on 21 Oct 2026; recheck in 2.20 |
| 2 | Pilot with a crisis or early-warning body | to be found | a loop profile they can use | Unverified |
| 3 | Philanthropy for public-good indicators | to be found | release, report, partner | Unverified |
| 4 | Partner-hosted research grants (e.g. Horizon Europe) | large, shared | a partner leading the bid | Unverified for EMO |
| 5 | Investors | depends | paying users, a legal entity | Only if 2.22 says yes |

## 13. Where Claude pushes back, and the risks

- The hurricane loop is US-specific and decision-based; it can support the "mind" reading only for one hazard in one country. H6 is required before any general claim.
- Ten seasons is a small n for coupling with controls; power may stay below 0.8 until several blind seasons accumulate. The plan is slow by design.
- Attention and action share a driver (storm severity); H4 can be confounded even with controls. The protocol must say what result would count as coupling beyond severity.
- None of this needs new grand theory. If a new tool is needed, it is built only when a pre-registered test shows the old one cannot answer the question.
- **Investors come last**, and "all institutions" is a direction, not a plan: indicators reach institutions one at a time, through a host others trust (plan 1).
- **One mind.** Every coded file so far is Claude's; the second coder (2.11) and machine-readable records (2.4) are the checks that EMO is not shaped by one mind, human or AI.
- **Speed.** The blind test needs the 2027 season; the plan is slow by design and holds only if each session meets its "done when".

## 14. Sources

- FEMA, OpenFEMA Disaster Declarations Summaries (documentation page), https://www.fema.gov/about/openfema/disaster-declarations-summaries , opened 29 Oct 2026 (session 2.0-design).
- Plan 1 sources (NLnet, JOSS, UNEP SDG 17.14.1, World Bank Sovereign ESG portal, Zenodo ledger DOI 10.5281/zenodo.23507467): opened for plan 1 on or before 21 Oct 2026; not reopened in this session.
- Repository: avram3scu-art/emo-core-v1, branch emo-2026-10.
