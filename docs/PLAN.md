# EMO 3.0: build the mirror, let it earn its claims

29 Oct 2026 · Adrian N. Avramescu, Independent researcher, Antwerp

**Plan 3.0 (Adrian's yes, 29 Oct 2026 18:26).** Strategy and reasons: `docs/STRATEGY_3_0.md`; vision sources: `docs/sources/vision/`. Plan 3.0 adds §0 (pillars, H8, H9, phases C–H, sessions 3.1–3.10) and keeps the 2.0 text below, which stays in force where §0 does not change it. Old phases C and D become F and G.

**Read this before every session (Adrian and Claude).** It is the roadmap of record. Rules: `CLAUDE.md` 3.0. Where we are now: `docs/STATUS.md`. History: `docs/SESSION_LOG.md`. Written by Claude on Adrian's decisions of 29 Oct 2026 (04:33, 04:57). A reading copy for the phone, `docs/PLAN.docx`, is made from this file with `pandoc docs/PLAN.md -o docs/PLAN.docx` and is regenerated in every commit that changes this file; if they differ, this file wins. It keeps the structure of plan 1, "EMO: from prototype to planetary program" (21 Oct 2026; committed in `docs/sources/plan/`, text in `docs/archive/PLAN_1.md`). Basis: `docs/AUDIT_2026-10-29.md`; review: `docs/REVIEW_2_0_DRAFTS.md`.

EMO tests one idea: that humanity's response to a hazard behaves like a mind, a loop whose links are coupled and learn. The route runs through tests that can fail, in a domain that repeats every year, before reports, partners or money.

## 0. Plan 3.0 (29 Oct 2026)

### 0.1 The five pillars, each tied to something that can run and something that can fail

| Pillar (Adrian's document) | What it becomes in code | What can fail | Hypothesis |
|---|---|---|---|
| 1. Credibility (plan 1) | Every claim on the public page points to a file; release DOI; failure register | claims drift from code | rules, not a test |
| 2. Mirror (*Why Humanity Needs a Mirror*) | One public loop card per hazard event: warning, attention, decision, delivery, lag so far, and the knowing→doing stage | stages not measurable from records | H3 (extended) |
| 3. Continuous running (*Why EMO Must Run Continuously*) | Daily jobs append events and update cards; the page shows last successful run | jobs fail or need hands | rules: the word "continuous" is earned by unattended running (CLAUDE 3.0) |
| 4. Benefit (*Who may benefit*) | Registered test: do faster loops go with smaller losses, beyond severity? First user pilot | no association, or no loss data | **H9 (new)** |
| 5. AI (*What if humanity is already a mind*): teacher, not a control system (Adrian, 18:35) | The **species self-model**: before each outcome, an AI writes (a) what humanity will do and (b) what a coherent whole that knows what humanity knows would do; (a) is scored, (b) is shown beside reality | (a) no better than a non-AI baseline | **H8 (new)** |

Adrian's mirror essay already maps onto the loop: latency = DAC lags; learning = H5; alignment (promise vs budget) = SMF; consistency (parts reinforcing or opposing) = counter-measures between levels in DAC. The six stages of *What if humanity is already a mind* (warning not recognised; recognised, not transmitted; reached decision-makers, no budget; funded, fragmented; coordinated, then collapsed; learned) become the stage field of each loop card.

**Pillar 5 (Adrian, 29 Oct 2026):** EMO is "our teacher, not a control system" (18:35). Reason, in Adrian's words (29 Oct 2026, 18:38): "You can become a mass destruction weapon. Trust humanity, as I trust." People decide; EMO only makes it harder to pretend not to know. Rules: CLAUDE.md 3.0, self-model rules.

### 0.2 Hypotheses added (H1–H7 unchanged)

| # | Hypothesis | Fails if | Status |
|---|---|---|---|
| H8 | Self-model: AI forecasts of response outcomes, committed before the outcome, beat both a naive base rate and a simple statistical model (Brier score) | not better than the statistical model after the pre-registered number of resolved events | protocol and power registered 30 Oct 2026 (3.5, `docs/SELF_MODEL_PROTOCOL.md`); ledger in 3.6 |
| H9 | Benefit: events whose loop runs faster (shorter warning → decision lag) have smaller losses than severity explains | no association at adequate power, or no usable loss data (then "cannot be tested", not FAIL) | not built; feasibility in 3.7 |

### 0.3 Roadmap 3.0

No phase starts on the calendar; each starts when its gate is met. Dated sessions of plan 2.0 keep their dates.

| Phase | Sessions | Gate to the next |
|---|---|---|
| A, B (plan 2.0) | 2.1–2.12b | unchanged; dated sessions run on their dates |
| **C. The mirror runs** | 3.1–3.4 | daily jobs have run unattended for 14 days; cards public |
| **D. The self-model** | 3.5–3.6 | H8 protocol registered; ≥ 10 AI forecasts committed before outcomes |
| **E. Benefit and reach** | 3.7–3.8 | H9 verdict on feasibility; one country coherence profile feasibility note |
| **F. Credibility, as by-products** | 3.9 release, 2.16 report, 2.17 briefs, JOSS (≥ 19 Apr 2027), white paper share | release DOI resolves |
| **G. Partners and money** | 2.18–2.22 | a partner's written reply |
| **H. First user pilot** | 3.10 | one institution uses one card or profile, in writing |

| # | Session | Hypothesis | Done when |
|---|---|---|---|
| 3.1 | Global event stream: data check (documentation only: alerts, attention, activations, losses; licences, latency, coverage) | H3, H6, H8 | `docs/STREAM_DATA.md` with a verdict per source; no records opened |
| 3.2 | Daily ingestion: append-only event log from the chosen sources, daily Action, manifest with checksums | infrastructure | three consecutive daily runs commit without help |
| 3.3 | Loop card protocol: fields, the six knowing→doing stages defined from records, "not yet" vs "missing", synthetic checks; registered before any card is public | H3 | protocol and tests committed; no card published |
| 3.4 | Mirror page: one card per event, stage, lag so far, last run; rebuilt daily | infrastructure | page updates on its own for 14 days (checked in a later session) |
| 3.5 | Self-model protocol (pillar 5): the two outputs, ledger format, baselines (base rate, logistic), Brier scoring, contamination and circularity rules, power from synthetic data | H8 | protocol and power committed before any forecast |
| 3.6 | Self-model ledger: first AI forecasts committed with hashes before outcomes; Adrian decides in-session vs scheduled (API cost) | H8 | ≥ 10 forecasts committed; scoring script tested on synthetic outcomes |
| 3.7 | Benefit feasibility: loss data per event (documentation only); Adrian's earlier simulation committed as exploratory if supplied | H9 | protocol registered, or the reason it cannot be tested |
| 3.8 | Coherence profile pilot design (*Who may benefit*): one country, the four mirror dimensions as a profile from public records | H3, H6 | feasibility note and coding rules, or reason |
| 3.9 | Release 1.0 (was 2.15), now including the mirror | infrastructure | release DOI resolves |
| 3.10 | First user pilot: one crisis or early-warning body, one card or profile they use | H9 | a written reply |

Plan 2.0 sessions 2.13 (white paper, shared only after Adrian's verification), 2.14 (JOSS, resubmit check after 19 Apr 2027), 2.16, 2.17 and 2.18–2.22 stay, moved behind the mirror. The dated sessions 2.8 (2027 registry, before 1 June 2027), 2.10 (after 31 Dec 2026), 2.12 (15 Nov 2027) and 2.12b (about May 2028) keep priority on their dates.

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
| 2.11b | Flood loop: C1 and protocol | H6, H4 | C1 verdict; protocol or reason (done: definitions registered, statistic rejected) |
| 2.11c | Flood loop: severity measure, test registration | H6, H4 | severity-source verdict; registered test with synthetic FPR and power, or reason (done: source available with conditions; test rejected, F13)|
| 2.11d | Flood loop: repair F13 (new estimand) | H6, H4 | registered repaired test with synthetic error rates and power, or reason and retire recommendation (done: sensitivity repair failed; attention arm retired, replaced by news-pressure test §10; lag test §11) |
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

### 2.11c Flood loop: severity measure and test registration (H6, H4; from 2.11b)

*From the 2.11b review (Adrian 13:03, "2a - yes").*

```text
EMO session 2.11c: flood loop, severity measure and test registration. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.11c in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H6 (and H4 power by pooling). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.11c task: using docs/FLOOD_LOOP_PROTOCOL.md (data definitions fixed in 2.11b for notifications issued 30 Oct 2026 to 31 Dec 2028; the candidate rank test was rejected, synthetic FPR 0.08-0.75 under severity confounding, §5), (1) check from documentation whether a severity measure independent of attention and decision is available per episode after the fact (candidate: EFAS or GloFAS discharge reanalysis return period at the notified river; access, licence, latency and whether an account is needed); (2) if yes, design a test that adjusts for it continuously (e.g. permutation of A residuals on severity, or a logistic model with a permutation null within storm clusters), commit its code before running it, and show from synthetic data FPR <= 0.05 under every §5 scenario plus power at N 20-45; then register it in the protocol. Do not open any EFAS notification, pageview or CEMS activation of the period, and compute no lag from data/second_domain/cems_activations_2026-10-29.json. The §3 definitions stay unchanged.
Done when: severity-source verdict committed, and either the registered test with its synthetic FPR and power is committed or the reason it cannot be is recorded.
```

### 2.11d Flood loop: repair F13 by changing the estimand (H6, H4; from 2.11c)

*From the 2.11c review (Adrian 13:31, "2 repair").*

```text
EMO session 2.11d: flood loop, repair F13 by changing the estimand. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.11d in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H6 (and H4 power by pooling). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.11d task: using docs/FLOOD_LOOP_PROTOCOL.md (§3 definitions fixed for notifications issued 30 Oct 2026 to 31 Dec 2028; severity source verdict §7: EFAS/GloFAS historical discharge with Gumbel thresholds, EWDS account needed; both candidate tests rejected on synthetic FPR, §5 and §8; F13 repair chosen by Adrian 29 Oct 13:31), design a repaired test whose claim does not need FPR control under unmeasured impact confounding: (a) a pre-registered sensitivity analysis that reports how large a hidden confounder (in SD of severity error, as in §8) would have to be to explain an observed association, with the decision threshold fixed now, or (b) another estimand that the decision cannot follow from severity alone, if documentation shows one. Commit code before running it; show from synthetic data its FPR (or its error rate at the fixed threshold) under every §5 and §8 scenario and its power at N 20-45; if the power is below 0.5, say so in the protocol's first line. Register it in the protocol, or record why no repair is possible and recommend retire. Do not open any EFAS notification, pageview, discharge or CEMS activation of the period, and compute no lag from data/second_domain/cems_activations_2026-10-29.json. The §3 definitions stay unchanged.
Done when: a repaired test with its synthetic error rates and power is registered and committed, or the reason no repair is possible is recorded with a retire recommendation in docs/FAILURES.md F13.
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

### Phase C (3.0): the mirror runs

### 3.1 Global event stream: data check (H3, H6, H8; documentation only)

```text
EMO session 3.1: global event stream, data check. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md, docs/STRATEGY_3_0.md and the entry for session 3.1 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none directly (data check for H3, H6, H8). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 3.1 task: choose the high-frequency global hazard stream for the mirror and the self-model. From documentation only (no event records opened), check for each candidate link: warning or alert (e.g. USGS earthquake feeds and PAGER, GDACS alerts), attention (Wikipedia pageviews), decision (Copernicus EMS rapid mapping activations, IFRC GO emergency appeals and DREF), delivery or money (OCHA FTS, IFRC appeal funding), losses (EM-DAT or others): what it records, licence and terms, access (account, key, cost), update latency, coverage, and how events can be linked across sources. Every candidate named here is unverified until opened. Keep the registered flood test (docs/FLOOD_LOOP_PROTOCOL.md §3, §10, §11) and the 2027 hurricane registry unchanged; say whether any chosen source overlaps them.
Done when: docs/STREAM_DATA.md gives a verdict per source (use, use with conditions, reject), the expected number of linked events per month, and a recommended stream; no event record opened; record, STATUS and next prompt committed.
```

### 3.2 Daily ingestion (infrastructure)

```text
EMO session 3.2: daily ingestion of the global hazard stream. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md, docs/STRATEGY_3_0.md, docs/STREAM_DATA.md and the entry for session 3.2 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (infrastructure). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 3.2 task: build an append-only daily event log from the stream recommended in docs/STREAM_DATA.md §6: GDACS events and episodes, USGS ComCat/PAGER, CEMS Rapid Mapping, IFRC GO events, DREF and appeals (with a daily amount_funded snapshot), and Wikimedia pageviews for English event articles only after a matching rule exists (so pageviews are not fetched in this session). First open the API documentation each fetcher uses (GDACS API reference, USGS feed policy, IFRC GO production API, Wikimedia rate and User-Agent policy) and record it in STREAM_DATA. Before writing EMO's own joins, check whether a public IFRC Monty endpoint exists and can serve these sources (STREAM_DATA §3); recommend reuse or not. Exclusions E1–E3 (STREAM_DATA §5) are enforced in code and covered by unit tests: E1 CEMS EU27 flood activations 30 Oct 2026 – 31 Jan 2029 are dropped in memory before writing, with no count or log line; E3 no OpenFEMA; E2a–E2d no pageviews. Daily GitHub Action, manifest with checksums, fetch timestamps (to measure latency), and the log is not published or shown on any page (3.3 protocol first). Monthly counts of events and linked events are infrastructure, counted only from the log, and no outcome field is analysed.
Done when: fetchers, exclusion tests and the daily Action committed; three consecutive daily runs commit without help (checked in a later session if needed); record, STATUS and next prompt committed.
```

### 3.3 Loop card protocol (H3)

```text
EMO session 3.3: loop card protocol. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md, docs/STRATEGY_3_0.md, docs/STREAM_DATA.md (§3, §3a, §5, §9, §10) and the entry for session 3.3 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: H3 (protocol only; no card published). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
First, close session 3.2: check that Stream daily committed one run without help on each of 30 Oct, 31 Oct and 1 Nov 2026, started by any of its three starters (GitHub cron 04:17 UTC, cron-job.org "EMO stream daily" 07:13 Brussels, GitHub backup 11:47 UTC); use gh run list -w stream_daily.yml and data/stream/MANIFEST.jsonl (every source has_records true, error null). Record the result in docs/RECORD.md and STATUS; if any day is missing, say which starter failed and propose the fix.
Session 3.3 task: write and register the loop card protocol for the stream: card fields per event; the six knowing→doing stages (STRATEGY_3_0 §3) defined only from machine-readable records; "not yet" vs "missing"; the join rule frozen before any linking statistic (explicit keys first: CEMS gdacsId, GLIDE, GO event_id; then the ISO3 + hazard + onset-window fallback with its window and tie rules); the English pageview matching rule with the per-article E2a–E2d filters (so a later session may add pageviews); synthetic checks of every rule. Use these 3.2 findings: Monty has no public endpoint (HTTP 401) and no CEMS or appeal collections, so EMO writes its own joins; the log is encrypted with EMO_STREAM_KEY, which Claude never holds, so any step that reads the log (counts, cards) runs inside a GitHub Action with the secret and commits only aggregates that cannot reveal E1-dropped records (CEMS EU27 left out of all counts); GDACS episodes exist only through daily snapshots; one run is about 340 KB, so decide whether to trim the stored fields (storage about 125 MB a year). No record of the log is opened in this session; no card is published.
Done when: protocol and synthetic tests committed, registered before any card is public; 3.2 run check recorded; record, STATUS and next prompt committed.
```

### 3.4 Mirror page (infrastructure)

```text
EMO session 3.4: field check and mirror page. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md, docs/LOOP_CARD_PROTOCOL.md, docs/STREAM_DATA.md (§5, §10) and the entry for session 3.4 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (infrastructure; protects the registered H3 stream test). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
First, fix the pre-push hook so it never leaves docs/F2_CLAIMS_GREP.md modified (three pushes were refused by it on 29–30 Oct); test it with one push. The 3.2 three-day check (31 Oct, 1 Nov, 2 Nov) is done at the start of the first session on or after 3 Nov 2026, whichever it is.
Session 3.4 task: (1) Field-presence check (LOOP_CARD_PROTOCOL §10, deadline 30 Nov 2026): a workflow, run inside GitHub Actions with EMO_STREAM_KEY, that commits only, per source and per field the protocol reads, the share of records where the key is present (no values, no record counts, EU27 CEMS never read). If a name is wrong, write one dated amendment in §10 (field names, or a country-name → ISO3 table for CEMS only); nothing else in the protocol changes. (2) Card job: a daily workflow that builds cards with emo/stream/cards.py and commits only the §11 aggregates (safe_aggregate, edge-rule counts, last run time). (3) Mirror page skeleton showing those aggregates and the time of the last successful run; per-event cards stay unpublished until written reuse terms from GDACS (EC legal notice) and IFRC GO are recorded. Claude never holds the key and opens no record. Do not call any job continuous before 14 unattended days.
Done when: hook fixed; field-presence aggregate committed and any amendment registered before 30 Nov 2026; card job and page committed and run once by the Action; record, STATUS and next prompt committed.
```

### 3.4b Field-name amendment (infrastructure; dated: on or after 16 Nov 2026, before 30 Nov 2026)

```text
EMO session 3.4b: field-name amendment. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md (session 3.4), docs/FIELD_PRESENCE_CHECK.md, docs/LOOP_CARD_PROTOCOL.md (§3, §10, §11) and this entry in docs/PLAN.md, and follow them. One task only. Hypothesis moved: none (infrastructure; protects the registered H3 stream test). Run only on or after 16 Nov 2026 and finish before 30 Nov 2026. Claude never holds EMO_STREAM_KEY and opens no record. Keep replies short; I am on a limited weekly allowance.
First, check whether GDACS and IFRC GO have replied to the reuse requests sent 30 Oct (ask me); if not, give me a one-line reminder text for each. Task: (1) Build a country-name → ISO3 table for CEMS (ISO 3166 English short names, from a source opened in the session and cited), committed before it is applied, without opening a record; add a "parses with the table" share for CEMS countries to emo/stream/presence.py (register this addition in FIELD_PRESENCE_CHECK.md first). (2) Re-run .github/workflows/field_presence.yml; read the committed aggregate by the §3 rule of FIELD_PRESENCE_CHECK.md (3.4 found: CEMS countries are names; CEMS subCategory, GO appeal dtype_name absent and GDACS glide empty, no replacement key; GDACS search and GO events had < 20 records). (3) Write the single dated amendment in LOOP_CARD_PROTOCOL §10 (the CEMS table plus any rename the rule calls for; nothing else changes) and apply it in emo/stream/cards.py with synthetic tests. If GDACS search or GO events are still < 20, say so in the amendment and leave their names as documented. (4) Mirror page: label that cards with onsets before the stream began (Oct 2026) come from running appeals; README: replace "no daily ingestion" with what runs now (no "continuous" before 14 unattended days).
Done when: table, aggregate and amendment committed before 30 Nov 2026; mirror job green after the change; page label and README fixed; record, STATUS and next prompt committed.
```

### 3.5 Self-model protocol and power (H8)

```text
EMO session 3.5: self-model protocol and power. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md (decision 30 Oct 07:57 on the AI layer; session 3.4), docs/STRATEGY_3_0.md (§3, §4.1, §5), docs/LOOP_CARD_PROTOCOL.md and the entry for session 3.5 in docs/PLAN.md, and follow them. One task only. Hypothesis moved: H8 (protocol and power registered; no forecast made). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register before any data are opened. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
First, if today is on or after 3 Nov 2026: check that Stream daily ran unattended on 31 Oct, 1 Nov and 2 Nov (gh run list -w stream_daily.yml; event and starter per run; no manual start) and that Mirror daily followed each; report it, then record it as the 3.2 done-when check. If before 3 Nov, say it waits.
Task: write docs/SELF_MODEL_PROTOCOL.md: what the AI forecasts (per open card, from the §11-permitted card state only: e.g. whether a decision or money rung is reached within its window), the forecast ledger format (hash, model name and version, commit before the outcome), the two baselines (naive base rate; a simple statistical model such as logistic on hazard and stage so far), Brier scoring by code against IFRC/CEMS records only, contamination and circularity rules (no E1-protected record sent; the AI never scores itself; only events after the protocol commit count), and power from synthetic data at the expected number of forecasts. Constraints from 30 Oct: EMO calls the model; paid-service choice stays mine in 3.6. The mirror page shows counts only; 3.4b (field amendment) runs separately on or after 16 Nov.
Done when: protocol, synthetic power and tests committed before any forecast; record, STATUS and next prompt committed.
```

### 3.6 Self-model ledger (H8)

```text
EMO session 3.6: self-model ledger. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md (session 3.5; decision 30 Oct 07:57 on the AI layer), docs/SELF_MODEL_PROTOCOL.md (all of it; registered d306482) and the entry for session 3.6 in docs/PLAN.md, and follow them. One task only. Hypothesis moved: H8 (forecasts committed before outcomes; nothing scored). Stop when its "done when" is met, or tell me plainly why it cannot be met. Do not change the registered protocol except by a dated §9 amendment made before any forecast. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
First, if today is on or after 3 Nov 2026 and the 3.2 check is not yet recorded: check that Stream daily ran unattended on 31 Oct, 1 Nov and 2 Nov (gh run list -w stream_daily.yml; event and starter per run; no manual start) and that Mirror daily followed each; report it and record it as the 3.2 done-when check.
Then ask me the paid-service decision, with your recommendation: in-session forecasting is not compliant (3.5 finding: you would see per-event card state and hold no key), so the choice is the Anthropic API called inside the Action (recommended earlier: Haiku 5.5, $5 monthly cap; check current model names and prices on Anthropic's own pages before recommending) or no H8 forecasts. I add the API key as a repository secret myself; you never see it.
Task (on my yes): build the forecast caller as a daily Action after Mirror daily, using only emo/selfmodel/protocol.py: training-row replay (each earlier non-EU27 card as at its own earliest eligible run, outcome known before the forecast time), baselines, payload and fixed prompt h8-v1, one call per eligible (card, target), encrypted ledger per run under data/selfmodel/ledger/ (emo/stream/store.py), public run-level data/selfmodel/ledger_index.csv, forecast count and last ledger run on the mirror page (counts only); a scoring script that refuses before may_score() is true, tested end to end on synthetic cards and outcomes; a dry run with a stub model on synthetic cards. Decide nothing about ISO3 unless I ask (kept in 3.5).
Done when: caller, ledger, index and scoring script committed with synthetic tests; first real run green; ≥ 10 forecasts committed before their outcomes (if fewer eligible cards exist yet, say so, and the count is checked in a later session: needs time); record, STATUS and next prompt committed.
```

### 3.6b Self-model ledger: first run with the API key (H8)

```text
EMO session 3.6b: self-model ledger, first run with the API key. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md (session 3.6), docs/SELF_MODEL_PROTOCOL.md and the entry for session 3.6b in docs/PLAN.md, and follow them. One task only. Hypothesis moved: H8 (forecasts committed before outcomes; nothing scored). Keep replies short; I am on a limited weekly allowance.
First (today is on or after 3 Nov 2026): check that Stream daily ran unattended on 31 Oct, 1 Nov and 2 Nov (gh run list -w stream_daily.yml; event and starter per run; no manual start) and that Mirror daily and Self-model daily followed each; report it and record it as the 3.2 done-when check.
Then guide me, one step at a time on "Next", through the key steps left from 3.6: (3) set a $5 monthly spend limit in the Console (the default tier limit is $500); (4) buy $5 of credits (I pay; not before then); (5) create the key "EMO H8" and add it as repository secret ANTHROPIC_API_KEY. You never see the key.
Task: start Self-model daily once by hand only after the key is in (gh workflow run selfmodel_daily.yml --ref emo-2026-10; it writes nothing if no new stream run exists, so start it after a Stream daily run of the day). Check from the public index only (never the encrypted ledger): status, n_forecasts, n_ai_unusable, n_missed, model_returned = claude-haiku-5-5, digest verified. Report how many eligible cards were recorded as missed ("no key") between 31 Oct and the key (lost for H8, by the 3.6 rule). If n_ai_unusable > 0 on the first keyed run, diagnose from the Action log (error class only) before the next run.
Done when: one keyed run green with model_returned recorded and no account error, or the reason it cannot be stated; ≥ 10 forecasts committed before their outcomes, or the count so far and the date of the next check (needs time); record, STATUS and next prompt committed.
```

### 3.7 Benefit feasibility (H9)

```text
EMO session 3.7: benefit feasibility. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md (session 3.6), docs/STRATEGY_3_0.md (pillar 4 and H9), docs/STREAM_DATA.md (EM-DAT and OCHA FTS verdicts) and the entries for H9 and session 3.7 in docs/PLAN.md, and follow them. One task only. Hypothesis moved: H9 (feasibility only; no test data opened). Keep replies short; I am on a limited weekly allowance.
Task: write docs/BENEFIT_FEASIBILITY.md: which public sources give losses or harm per event that could later be linked to loop cards (e.g. EM-DAT offline, DesInventar, IFRC GO field reports and appeal documents, national loss databases, insured-loss reports): documentation pages only, no records; per source: coverage, delay, licence (redistribution, derivatives), how it would join a card, and its independence from the response it would judge. Then a verdict: can H9 ("EMO reduces losses or helps an institution") be tested prospectively, and how (registered result or a user's written statement), or why not. If I attach an earlier simulation of benefit, commit it unchanged as exploratory with its origin. Do not open any stream record, aggregate, or loss record. 3.6b (API key) runs separately on or after 3 Nov.
Done when: docs/BENEFIT_FEASIBILITY.md with a verdict per source and an overall verdict (protocol to register in 3.7b, or the reason H9 cannot be tested), every source opened listed with URL and date; record, STATUS and next prompt committed.
```

### 3.7b Benefit protocol or "cannot be tested" (H9)

```text
EMO session 3.7b: benefit protocol (H9). Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md (session 3.7), docs/BENEFIT_FEASIBILITY.md (§2.1 conditions C1–C4, §3 draft) and the entry for session 3.7b in docs/PLAN.md, and follow them. One task only. Hypothesis moved: H9 (protocol and power, or the reason it cannot be tested; no loss record opened). Keep replies short; I am on a limited weekly allowance.
Step 1: draft, in one monospace block, my written message to CRED (EM-DAT) asking: (C1) may an unaffiliated individual researcher use the free non-commercial access for research; (C2) may results be published as aggregate statistics only (a coefficient, its interval, n, counts by stratum; never a per-event value), with citation. No repository link. I send it; wait for my "sent". If CRED's reply is already in hand, commit it unchanged first.
Step 2 (only if C1 and C2 are answered yes in writing, committed unchanged): write and commit docs/BENEFIT_PROTOCOL.md from the §3 draft: population (closed TC and FL cards, non-EU27, anchored, with a decision record, onset after this commit to 31 Dec 2027), exposure (warning → decision lag, else onset → decision), outcomes (EM-DAT deaths; affected as second outcome, corrected), severity covariates chosen from documented GDACS fields only, the EM-DAT ↔ card join rule (GLIDE, else F2), statistic, clustered null, equivalence bound, score date (on or after 1 Apr 2028), what may leave, the stated bias against H9; with false-positive rate and power from synthetic data at the expected n (first line says so if power < 0.5) and tests. No EM-DAT file is downloaded in this session.
If no answer by the end of the session: record H9 as "waiting for CRED" with the date of the next check; if CRED says no to C1 or C2: record "H9 cannot be tested (no usable loss data)" with the reason in docs/BENEFIT_FEASIBILITY.md and FAILURES only if a test had been registered (none is).
Done when: message to CRED drafted and sent (or reply committed); and either the protocol with power and tests committed, or the reason it cannot be registered yet, with the next check date; record, STATUS and next prompt committed.
```

Prompts for 3.7–3.10 are written at the close of the session before each, from §0.3.

### Phase F (was C): credibility, as by-products

### 2.13 White paper 2.0 (credibility; after 2.5)

```text
EMO session 2.13: white paper 2.0. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session 2.13 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none (reports H1–H7). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 2.13 task: revise docs/WHITEPAPER_EMO_what_runs_today.md with the loop results to date (including the flood loop: attention arm retired after three synthetic failures and replaced by a registered news-pressure → activation test with power < 0.5, plus a registered lag-measurability test, both scored after 31 Jan 2029; docs/FLOOD_LOOP_PROTOCOL.md §5, §8–§11, docs/FAILURES.md F13), fixing every point of docs/REVIEW_S15_WHITEPAPER.md (disclosure point 2 only after my recorded verification; vision tied to H1–H7; one audience and one ask). Every factual statement links to a repo file or is marked [plan]; evidence class on every result. Then a hostile editor-style review.
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
Session 2.15 task: tag and archive release 1.0. Add CITATION.cff (Adrian N. Avramescu, ORCID 0009-0005-1393-5264), a CHANGELOG (from git history; state that the default branch starts from a snapshot on 19 Oct 2026 and that earlier work is on branch original-upload, Nov 2025–Apr 2026), and check that the Zenodo-GitHub integration is on for avram3scu-art/emo-core-v1. Make sure tests pass, then create the v1.0.0 release with notes stating what works and what does not, carrying the AI disclosure exactly as in paper/paper.md (point 2 withheld unless my verification is recorded in docs/STATUS.md) and the contributions line. LICENSE (full AGPL-3.0) and CONTRIBUTING.md already exist (session 2.14, docs/JOSS_CHECKLIST.md).
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

### Phase G (was D): partners and money

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
