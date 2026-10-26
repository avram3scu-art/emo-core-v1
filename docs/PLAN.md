<!-- Transcribed on 2026-10-23 from the Claude Doc "EMO: from prototype to planetary program" (https://claude.ai/artifact/GBsjLAgpASdmWzgx4UcWQA, rev 17). The roadmap diagram is rendered as text. -->

# EMO: from prototype to planetary program

2026-10-21 · Adrian

EMO can grow into an institutional instrument, but the route runs through credibility first: every pillar working on real data, every claim matching the code, and one outside institution using an EMO number, before investors or planetary scale.

## Where each pillar stands

DAC is the strongest pillar and UIA the weakest; none of the four runs on its own yet.

| Pillar | Works on real data today | Not yet working | Evidence |
|---|---|---|---|
| DAC (warning to delivered response) | Ozone vs climate lags (OWID); five-country PPE profiles from parliamentary inquiries | Only one coder; only Belgium has orders paired with deliveries | JCCM manuscript under review; dac_ozone_vs_climate.png |
| EMO metrics (OI, τ_I, synergy, GWI, SMF) | Organismality plane 1989–2025; τ_I from NHC hurricane track errors (3–4% a year); synergy, GWI and SMF pass noise controls (synthetic) | GDELT and Wikipedia attention streams never ingested; SMF and GWI not yet run on a real case | analysis/ scripts; 57 passing tests |

Starting state above as of 23 Oct 2026. Since then: GWI PASS (session 6), calibration FAIL (6c); SMF passes at short horizons (7); synergy FAIL on real streams (8). Current state: `README.md` and `docs/STATUS.md`.
| RDL (remedies) | Forecast ledger of 5 dated forecasts, public on Zenodo | v0.2 and v0.3 failed their held-out tests; v0.4 waits for Oslo–Seattle or IRD data | docs/RDL_*; DOI 10.5281/zenodo.23507467 |
| UIA (interface density) | Code exists (emo/uia_engine, about 450 lines) | All six weights set to 1.0; no term measured from real data; no test of what it predicts | emo/uia_engine/aggregate.py |
| Continuous running | Nothing | No scheduler deployed; Prefect and Airflow files exist but have never run | orchestration/ |

The Nov 2025 white paper describes a live observatory with DestinE overlays and a dashboard. The repository does not yet do that: ECMWF declined data access, and the dashboard and pipelines have not run.

## What must change before anyone outside sees EMO

An investor or institution will open the repository before the white paper; what they find there must match what we claim.

- **Claims match code.** Rewrite the white paper as "what runs today, what is next", with each statement linked to a script, a dataset or a test. Remove "live", "deployed" and "ready" until they are true.
- **Profiles, not one gauge.** The white paper sells a single UIA gauge; your DAC paper says no weighting is justified and components do not move together. EMO keeps one rule everywhere: report the profile, never a scalar with invented weights.
- **Fewer metrics, measured well.** "Measure everything that matters" is how indices lose credibility. Start with the metrics that pass noise controls on real data, and add one only when it survives the same test.
- **Every pillar must be able to fail.** Each test is pre-registered before its data are opened, as done for RDL. Failures stay on record; they are what make the passes believable.
- **Name what exists.** Policy coherence is already measured in parts: SDG indicator 17.14.1 (policy-coherence mechanisms), the World Bank Sovereign ESG Data Portal, the Worldwide Governance Indicators. EMO must say what it adds to them, after a search, not claim a blank field.

## The scientific spine

Your hypothesis from "The Measurement of Silence", He = f(I, C, F, E) − D, can tie the four pillars into one testable program, if each letter is a measured profile entry rather than a weighted sum.

| Term | Meaning | Measured by | Pillar |
|---|---|---|---|
| I | information integration | synergy (O-information), GWI ignition | EMO metrics |
| C | coordination | cooperation axis of the organismality plane; counter-measures between levels | EMO metrics, DAC |
| F | feedback and self-modelling | SMF (models steer outcomes?), τ_I (learning rate) | EMO metrics |
| E | resources | DAC budget sublayer; stocks at warning date | DAC |
| D | fragmentation, delay, contradiction | DAC lags, conflict axis, contradiction score | DAC |
| He | emergent capacity | what the system delivers: DAC delivery dates, realised RDL forecasts | DAC, RDL |

Proposal for UIA: redefine it as this profile at the human–Earth interface, replacing a_UIA's six weights set to 1.0. Then UIA is measured, and it can fail.

First pre-registered prediction, written before data: across DAC cases, systems with higher I, C, F and E, and lower D, at the warning date reach delivery sooner. The form of f is left open; only the direction is tested.

## Who benefits, and who would pay

The groups in your list are right; they differ in whether they would use EMO, fund it, or pay for it, and the plan follows that order.

| Group | What they would use | What they use now | Role for EMO |
|---|---|---|---|
| Earth System Governance Project, universities | DAC profiles, organismality plane, open data for papers | Case studies, regime databases | First partner: methods, validation, a host |
| Crisis and early-warning bodies (UNDRR, WMO, ECDC, national crisis centres) | Warning-to-delivery profiles, paired order–delivery lags | Coverage indicators, after-action reviews | User; possible funder of pilots |
| Ministries and central agencies | Where delay sits (decision or conversion), counter-measures between levels | Inquiries after the event | User; pays only through a pilot contract |
| OECD, IMF, World Bank, EBRD | Comparable country profiles of response and coherence | SDG 17.14.1, governance indicators, Sovereign ESG portal | Funder of methods if EMO adds what these lack |
| Institutional investors, rating agencies (ESG investing) | Coherence-adjusted country risk | Sovereign ESG scores from data vendors | Possible paying customer, later |
| Consultancies, risk advisory | Structured diagnostics for clients | Proprietary country-risk products | Possible licensee, later |
| Civil society, media, think tanks | Public mirror: are we responding to what we know? | Scattered dashboards | Audience; gives legitimacy, not money |
| Philanthropy (risk, climate, governance) | A neutral public-good instrument | Grants to existing indices | Main funder for the public layer |

Two kinds of EMO follow from this table: an open public mirror funded by grants and philanthropy, and, later, paid services built on it. Deciding whether the second exists is your decision for Phase 4; it must not compromise the openness of the first.

## Roadmap

Each phase opens only when the gate before it is met.

```text
Phase 1 · sessions 1–4: EMO runs by itself
  Weekly data refresh, public mirror page, truthful README, related-work search
  ◇ Gate A: two unattended weekly runs; README matches the code
Phase 2 · sessions 5–14: every pillar works or fails on the record
  UIA as the He profile; GWI, SMF and synergy on real data; DAC standard and a new domain; RDL v0.4
  ◇ Gate B: each pillar has a pre-registered result, pass or fail
Phase 3 · sessions 15–19: credibility
  Honest white paper, software paper, release 1.0 with a DOI, first annual report, one-page briefs
  ◇ Gate C: release 1.0 public, and checked by one outside reviewer
Phase 4 · sessions 20–24: partners and money
  First partner, legal home, first grant, consortium role, decision on a paid layer
  ◇ Gate D: one outside institution uses an EMO number
Then: more institutions, one at a time
  Planetary scale is the sum of these adoptions; each one depends on the gates above still holding
```

No phase starts on the calendar; each starts when the gate before it is met, so delays in one phase do not let weak work through to the next.

## Session by session

Twenty-four sessions in four phases; each ends with something in the repository and a test of whether it is done. Sessions 13, 20 and 22 depend on other people's replies and may move.

### Phase 1: EMO runs by itself (sessions 1–4)

| # | Session | Output | Done when |
|---|---|---|---|
| 1 | Move work to avram3scu-art; truthful README | Default branch set; README status table; CLAUDE.md with the standing rules | A real commit pushed; README matches the pillar table above |
| 2 | Weekly GitHub Action | Fetches OWID (CO₂, ozone, aid, conflict), OpenAlex counts, NHC; reruns analyses and tests; commits dated results | Two scheduled runs commit without you |
| 3 | Public mirror page | GitHub Pages site: organismality plane, τ_I, DAC ozone vs climate, forecast ledger; every number linked to its source | The page changes after a run, untouched |
| 4 | Related work | docs/RELATED_WORK.md: SDG 17.14.1, Sovereign ESG portal, WGI, regime-effectiveness studies, response trackers; what EMO adds | Every "gap" claim backed by a search |

### Phase 2: every pillar works or fails on the record (sessions 5–14)

| # | Session | Output | Done when |
|---|---|---|---|
| 5 | UIA audit | Each UIA term: measurable or not; UIA redefined as the He profile; pre-registration | Your decision recorded; a protocol committed before data |
| 6 | GWI on real attention | Wikipedia pageviews (fetched by the Action) around pre-registered events; noise control | Test run once; result recorded |
| 7 | SMF on a real case | Pledged or modelled emissions paths vs realised emissions | Same |
| 8 | Synergy on real streams | Science, media and policy series for one domain, with surrogate null | Same |
| 9 | DAC standard | Event-file schema and validator from the JCCM paper's Table 4 | Validator rejects a malformed file in a test |
| 10 | DAC new domain | One more warning-to-delivery case coded under rules fixed first (candidate: mpox 2022, vaccine orders to deliveries) | Profile computed from a public event file |
| 11 | Second coder | Double-coding protocol; first volunteer recruited | Agreement statistic on one case |
| 12 | He direction test | Pre-registered test across DAC cases | Result recorded, pass or fail |
| 13 | RDL v0.4 | Run on Oslo–Seattle or IRD data when it arrives | Verdict in the protocol |
| 14 | Forecast ledger v2 | IMO outcome recorded; ten new forecasts; new Zenodo version | Fingerprints match |

### Phase 3: credibility (sessions 15–19)

| # | Session | Output | Done when |
|---|---|---|---|
| 15 | White paper rewrite | "EMO: what runs today", every claim linked to code or data | Editor-style review passed |
| 16 | Software paper | Journal of Open Source Software submission, after checking its AI policy | Submitted, not on the same day as finished |
| 17 | Release 1.0 | Tagged release archived on Zenodo; CITATION.cff | DOI resolves |
| 18 | State of the Mirror 2027 | Short annual report from the live data, with failures included | Every figure reproducible from the repo |
| 19 | Briefs | One page each for research partners, crisis bodies, funders | Each claim traceable to the report |

### Phase 4: partners and money (sessions 20–24)

| # | Session | Output | Done when |
|---|---|---|---|
| 20 | First partner | Approach the Earth System Governance network with the honest status | A reply and a named contact |
| 21 | Legal home | Compare a Belgian non-profit (VZW/ASBL) with hosting at a partner | Decision made |
| 22 | First grant | Small open-source grant application, with full AI disclosure | Submitted |
| 23 | Consortium role | EMO as a work package in a partner's Horizon Europe bid | Partner agrees in writing |
| 24 | Paid layer, yes or no | Decision on a commercial service (coherence-adjusted country risk) and its rules | Decision recorded; investor material only if yes and users exist |

## How every session starts and ends

Every session is a new conversation with avram3scu-art/emo-core-v1 as its repository. Paste the opening block, then that session's prompt below. When the task is done, Claude gives a short review (more to do, changes, improvements; see CLAUDE.md) and waits for your answer; then paste the closing block, so the work is recorded in the repo, not only in the chat. (Blocks revised 26 Oct 2026; recording rule added 26 Oct 2026, session 9.)

**Opening block (paste first, every session):**

```text
EMO session [N]. Repository: avram3scu-art/emo-core-v1. Before anything else, read CLAUDE.md, docs/STATUS.md and the entry for session [N] in docs/PLAN.md, and follow them. One task only this session: the one below. Stop when its "done when" is met, or tell me plainly why it cannot be met. Everything you need must be in the repo: do not rely on past chats or on me remembering; if something is missing, say so first. Record every test, simulation, probe, run and failed attempt in the repo as you go (files committed, one row each in docs/RECORD.md). Pre-register any test before opening its data. Cite only sources you opened. Test or verify anything you can within the session before calling it open. When the task is done, give me the review from CLAUDE.md (more of this task now, changes or improvements, your own mistakes) and wait for my answer before closing. Keep replies short; I am on a limited weekly allowance.
```

**Closing block (paste at the end, every session):**

```text
Close the session. (0) Check the record: git status clean, every item of this session in docs/RECORD.md, nothing the next session needs outside the repo; report any gap. (1) Update docs/STATUS.md: date, session number, what was done, commits, results including failures, open questions each with its reason (scope, my decision, needs time, not attempted), the review's improvement points and my answer, and the next session. (2) Append one row to docs/SESSION_LOG.md: date | session | task | done when met (yes/no) | key commit | note. (3) If a rule changed, update CLAUDE.md. Commit and push. (4) Give me six lines: done; not done, each with its reason; result; could still do or improve; next session; anything I must do.
```

After each session, also fill one row of the Usage log tab in EMO_weekly_plan_and_tools.xlsx (allowance left before and after).

## Session prompts, Phase 1

### Session 1: move the work home

```text
Session 1 task: make avram3scu-art/emo-core-v1 the working home.
1. Check out branch emo-2026-10 (head 9428f24, all work from 19-21 Oct 2026; main is the old original upload). Confirm push access with a real commit.
2. Make emo-2026-10 the default branch if you can; if not, give me the exact GitHub steps. Do not delete main.
3. Create docs/PLAN.md from the plan doc "EMO: from prototype to planetary program" (https://claude.ai/artifact/GBsjLAgpASdmWzgx4UcWQA; read it with the Docs connector), including every session prompt.
4. Create docs/STATUS.md and docs/SESSION_LOG.md (empty table with header: date | session | task | done when met | key commit | note).
5. Create CLAUDE.md with the standing rules: pre-register tests before data; DAC, UIA and every multi-part measure reported as a profile, never a weighted scalar; cite only sources opened; no claim beyond what the code does; RDL is not a validated recommender; AI disclosure in Adrian's three-point form; one task per session; closing routine.
6. Rewrite README.md: a status table (works / not yet / evidence) per pillar, matching the plan; remove "live", "deployed" and "ready" wherever untrue.
Done when: the commit is on GitHub and the README table matches the plan's pillar table.
```

### Session 2: the weekly GitHub Action

```text
Session 2 task: EMO refreshes its own data every week.
Write .github/workflows/weekly_refresh.yml (schedule: once a week, plus manual run). It must: download the OWID series already in data/ (annual CO2, ozone-depleting substances, foreign aid share, armed-conflict deaths); fetch the OpenAlex counts as in data/README_cooperation.md (excluding CN and ID); rerun the analysis scripts in analysis/ and the unit tests; commit changed data and figures with a dated message only if tests pass. Keep each download in its own folder and record source URL and download date in a manifest. Run it once manually and fix failures.
Done when: two scheduled or manual runs have committed without my help (the second can be in a later session).
```

### Session 3: the public mirror page

```text
Session 3 task: a public page that updates itself.
Build a GitHub Pages site from the repo (static HTML, no server): organismality plane, tau_I from NHC track errors, DAC ozone vs climate, and the forecast ledger with its Zenodo DOI. Every number and figure links to its data file and source. State plainly what EMO does not yet measure. The weekly Action rebuilds the page after a successful run.
Done when: the page is live and changes after a run without manual edits.
```

### Session 4: related work

```text
Session 4 task: write docs/RELATED_WORK.md before EMO claims any gap.
Search and open: SDG indicator 17.14.1 (policy coherence), World Bank Sovereign ESG Data Portal, Worldwide Governance Indicators, regime-effectiveness work (Miles et al. 2002; Breitmeier, Young and Zurn 2006; Breitmeier, Underdal and Young 2011), COVID response trackers (OxCGRT), early-warning effectiveness reviews, the Earth System Governance Project's indicator work. For each: what it measures, how, coverage, and what EMO adds or duplicates. Flag anything you could not open. Mark unverified claims.
Done when: every "gap" sentence in README and the white paper is backed by an entry, or removed.
```

## Session prompts, Phase 2

### Session 5: UIA audit

```text
Session 5 task: decide what UIA is, by measurement.
Read emo/uia_engine and the UIA section of the white paper. For each term (informational curvature R, focusing B, coherence C, entropy rate, information rate, semantic efficiency M_E): can it be computed from real public data today, from which source, and with what noise control? Then draft docs/UIA_PROTOCOL.md proposing UIA as the profile He = f(I, C, F, E) - D at the human-Earth interface (no weighted sum), with one pre-registered prediction and its fail condition. Present the options to me; I decide. Commit only after my decision.
Done when: my decision and the protocol are committed before any UIA data is opened.
```

### Session 6: GWI on real attention data

```text
Session 6 task: test Global Workspace Ignition on real attention data.
Pre-register in docs/GWI_PROTOCOL.md: the events (dated hazards with official warnings, chosen before looking at attention data), the attention series (Wikipedia pageviews, fetched by the weekly Action), the ignition rule in emo/gwi.py, the control windows, and pass/fail. Commit, then add the fetch to the Action, run once, record the result whether it passes or fails.
Done when: the result is in the protocol file.
```

### Session 7: SMF on a real case

```text
Session 7 task: test Self-Model Fidelity on a real case.
Pre-register in docs/SMF_PROTOCOL.md: a published self-model (e.g. pledged or modelled emissions paths) and the realised series (OWID CO2), the dates, emo/smf.py with its circular-shift null, and pass/fail. Commit before computing. Run once; record the result.
Done when: the result is in the protocol file.
```

### Session 8: synergy on real streams

```text
Session 8 task: test synergy (Gaussian O-information) on real streams.
Pre-register in docs/SYNERGY_PROTOCOL.md: one domain, at least three real streams (science: OpenAlex counts; policy: dated acts; attention: pageviews), the window, the surrogate null and pass/fail. Commit, run once, record.
Done when: the result is in the protocol file.
```

### Fix sessions F1–F8 (between 9 and 10)

Prompts for Claude and tasks for Adrian: `docs/FIX_PLAN.md` (from `docs/AUDIT_2026-10-26b.md`). Session 10 starts only after they are closed.

### Session 9: DAC standard

```text
Session 9 task: turn the DAC method into a reusable standard.
From Table 4 (minimum reporting standard) of the DAC manuscript, write docs/DAC_STANDARD.md, a JSON or CSV schema for event files (date, window bounds, sublayer, description, source, source type, reading for contested dates, order-delivery pairing), and a validator in emo/ with unit tests. The validator must reject a malformed file and compute the profile (never a scalar) from a valid one.
Done when: tests pass, including one malformed-file rejection.
```

### Session 10: DAC new domain

```text
Session 10 task: code one new warning-to-delivery case.
Candidate: mpox, WHO emergency declared July 2022, to vaccine orders and deliveries in EU countries and at EU level. First write the coding rules and the source list (official records only) and commit them; then code the event file with the validator; compute the profile; record what could not be dated.
Done when: a validated event file and its profile are committed.
```

### Session 11: second coder

```text
Session 11 task: prepare independent double coding.
Write docs/DOUBLE_CODING.md: rules a second person can follow without me, a short training example, the agreement statistic, and how disagreements are resolved. Draft a short message inviting a volunteer (student or researcher) to code one case. I send it.
Done when: protocol committed and message ready; agreement is computed in a later session once someone codes.
```

### Session 12: the He direction test

Postponed (session 5 decision, Option C): runs only once DAC holds at least 8 coded cases with warning dates after pageview coverage starts. See docs/UIA_PROTOCOL.md §4.

```text
Session 12 task: first test of He = f(I, C, F, E) - D.
Using docs/UIA_PROTOCOL.md: score I, C, F, E and D at the warning date for every coded DAC case, using only data dated before the warning. Commit the scores. Then test the pre-registered direction (higher I, C, F, E and lower D reach delivery sooner) with the stated statistic. Report the result whatever it is; with few cases, say what it cannot show.
Done when: result recorded in the protocol.
```

### Session 13: RDL v0.4 (only when data arrives)

```text
Session 13 task: run RDL v0.4 per docs/RDL_V04_PROTOCOL.md.
I attach the Oslo-Seattle or IRD files. First, from the codebook only, fill and commit the category directions in analysis/rdl_v04_test.py (CODEBOOK confirmed = True). Then convert the data to the CSV the script expects and run it once. Record the verdict in the protocol; ozone and LRTAP are development cases and the verdict excludes them.
Done when: verdict recorded.
```

### Session 14: forecast ledger v2 (after 31 Dec 2026)

```text
Session 14 task: score and extend the forecast ledger.
Record the outcome of F001 (IMO Net-Zero Framework adopted by 31 Dec 2026?) with a source in data/rdl_forecast_outcomes.csv; run analysis/score_forecast_ledger.py. Register ten new forecasts on open negotiations, coded with the RDL v0.4 indicators and notes; never edit old rows. Update the SHA-256 file and prepare the files for a new Zenodo version of DOI 10.5281/zenodo.23507467.
Done when: new fingerprint committed and files ready for my upload.
```

## Session prompts, Phase 3

### Session 15: honest white paper

```text
Session 15 task: rewrite the white paper as "EMO: what runs today".
Start from WHITEPAPER_EMO_v1_Why_EMO_Must_Run_Continuously and the README status table. Keep the vision; every factual statement must link to a script, data file, test or protocol in the repo, or be marked as a plan. Remove the single-gauge a_UIA claim unless session 5 kept it; include the failures (RDL v0.2, v0.3 and any later). Author: Adrian N. Avramescu, Independent researcher, Antwerp. Then give me a hostile editor-style review of the draft before anything is shared.
Done when: draft committed and reviewed; nothing sent out the same day.
```

### Session 16: software paper

```text
Session 16 task: prepare a Journal of Open Source Software submission.
First open JOSS's current submission requirements and AI usage policy and check EMO against each, listing gaps. Fix small gaps; list large ones. Draft paper.md (summary, statement of need, related work from docs/RELATED_WORK.md, AI usage disclosure in Adrian's three-point form). Give an editor-style review with a realistic verdict.
Done when: checklist and draft committed; submission waits at least one day after the review.
```

### Session 17: release 1.0

```text
Session 17 task: tag and archive release 1.0.
Add CITATION.cff (Adrian N. Avramescu, ORCID 0009-0005-1393-5264), a CHANGELOG, and check that the Zenodo-GitHub integration is on for avram3scu-art/emo-core-v1. Make sure tests pass, then create the v1.0.0 release with notes stating what works and what does not.
Done when: the Zenodo DOI for the release resolves.
```

### Session 18: State of the Mirror 2027

```text
Session 18 task: first annual report from the live data.
Write reports/state_of_the_mirror_2027.md: what the measured pillars show (organismality plane, tau_I, DAC cases, forecast ledger score), what failed and why, and what EMO cannot yet see. Every figure produced by a script in the repo and reproducible from the release. Short: under 3,000 words.
Done when: every figure regenerates from the repo.
```

### Session 19: one-page briefs

```text
Session 19 task: three one-page briefs.
For (a) research partners, (b) crisis and early-warning bodies, (c) funders: what EMO measures today, one result each would care about, what we ask of them, what EMO does not claim. Every claim traceable to the report or repo. No Substack or Zenodo portfolio links.
Done when: three briefs committed in docs/briefs/.
```

## Session prompts, Phase 4

### Session 20: first partner

```text
Session 20 task: approach the first partner.
Draft a short email to the Earth System Governance Project network (Adrian was previously invited as a Fellow) with the honest status: what runs, the release DOI, the annual report, the failures, and one concrete ask (methods feedback, a co-author, or hosting). No exaggeration, no portfolio links. Give me two variants; I choose and send.
Done when: email sent by me; reply and contact recorded in STATUS when it arrives.
```

### Session 21: legal home

```text
Session 21 task: decide where EMO legally lives.
Compare, with sources opened: a Belgian non-profit (VZW/ASBL) founded by Adrian, versus hosting by a partner institution, versus staying an individual open-source project. For each: cost, time, who can receive grants, governance, and fit with EMO's openness. Recommend one; I decide.
Done when: decision recorded in docs/GOVERNANCE.md.
```

### Session 22: first grant

```text
Session 22 task: one small grant application.
Open the current NLnet calls (and up to two other open-source or public-good funders you find and verify). Check eligibility, deadline and AI policy (NLnet asks for prompts and logs from AI-assisted work). Draft the application for a concrete technical deliverable (e.g. the DAC event-file standard and validator, or the live pipeline), with full AI disclosure. Editor-style review before I submit; never same day.
Done when: application ready for my submission.
```

### Session 23: consortium role

```text
Session 23 task: EMO as a work package in a partner's bid.
With the partner from session 20: find a current Horizon Europe or comparable call that fits, open its text, and draft a one-page work-package description (objectives, deliverables, months, cost) for EMO's part. Only what EMO can do by then.
Done when: partner agrees in writing to include it.
```

### Session 24: paid layer, yes or no

```text
Session 24 task: decide whether EMO gets a paid service.
Set out, with evidence: possible users who would pay (e.g. coherence-adjusted country risk for investors), existing competitors, what it would cost to build, and the risk to EMO's open, non-oracular public layer. Give the case for and against; I decide. Investor material only if the answer is yes and at least one real user has asked for it.
Done when: decision and its rules recorded in docs/GOVERNANCE.md.
```

## Funding ladder

Money follows evidence: phases 1–3 need almost none, and each rung below becomes realistic only after the one before it.

| Rung | Source | Size | Needs first | Status of the fact |
|---|---|---|---|---|
| 0 | Your time; free public-repository tools | none | A laptop helps | Known |
| 1 | NLnet open calls (open-source technical work) | €5,000–50,000 first grant; individuals may apply | Clear technical deliverable; their generative-AI policy asks for disclosure and your prompts and logs, and does not want AI-generated projects | Verified on nlnet.nl; next deadline 3 Nov 2026 is too soon for us |
| 2 | Pilot contract with a crisis or early-warning body | to be found | A DAC profile they can use | Unverified |
| 3 | Philanthropy for public-good indicators | to be found | Release 1.0, report, a partner | Unverified; names to be searched in session 22 |
| 4 | Partner-hosted public research grants (e.g. Horizon Europe) | large, shared | A university or institute partner leading the bid | Unverified for EMO |
| 5 | Investors | depends | Paying users of a service; a legal entity | Only if session 24 says yes |

The NLnet AI policy matters beyond NLnet: EMO is built with AI, and funders will increasingly ask how. Keeping full disclosure, as in your three-point model, is safer than any wording that hides it.

## Where I push back, and the risks

- **"All institutions" is a direction, not a plan.** Indicators reach institutions one at a time, usually through a host that others trust. The plan aims at the first one; the rest follows only if that one finds EMO useful.
- **Investors come last.** A neutral public mirror is rarely an investment; a paid service built on it might be. Pitching investors before users exist would cost credibility that cannot be bought back.
- **The white paper is the largest risk today.** It describes a running system that does not exist yet. One expert reading it next to the repository would close the door.
- **Working alone, on a phone.** Sessions 1–3 remove the phone from the loop. Session 11 brings the first outside person in; a second coder is also the first check that EMO is not shaped by one mind.
- **Some pillars may fail.** UIA in particular may not survive measurement as written. A pillar that fails a fair test is rebuilt or dropped, and the record shows why; that is how EMO grows up.
- **Speed.** Twenty-four sessions is months of work, and replies from others set part of the pace. The plan holds if each session ends with its "done when" met.

## Sources

- [NLnet: how to propose](https://www.nlnet.nl/propose) (grant size, eligibility, AI policy, deadline)
- [Journal of Open Source Software documentation](https://joss.readthedocs.io/en/latest/) (no submission fees; AI usage disclosure required)
- [UNEP: SDG indicator 17.14.1](https://www.unep.org/en/what-we-do/indicator-17141)
- [World Bank: Sovereign ESG Data Portal relaunch](https://www.worldbank.org/en/news/feature/2022/12/12/world-bank-relaunches-sovereign-esg-data-portal)
- [EMO-RDL forecast ledger, Zenodo](https://doi.org/10.5281/zenodo.23507467)
- Repository state: avram3scu-art/emo-core-v1, branch emo-2026-10
- Your documents: "Why EMO Must Run Continuously" (Nov 2025), "The Measurement of Silence", the DAC manuscript for JCCM
