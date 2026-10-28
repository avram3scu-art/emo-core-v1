# RDL backtest protocol (pre-registration)

**Evidence class (added 28 Oct 2026, fix session F6): pre-registered on known history, not blind.** The cases' outcomes were known to the author and Claude when the protocol, inputs and engine were written. "Held-out" below is the word used at the time; it means a reserved historical case kept out of development, not a blind test. The only blind RDL test is the forecast ledger (`docs/RDL_FORECAST_LEDGER.md`).

Status: written and committed **before** any backtest run. Changes after the first run must be logged below with the reason.

## Question
Given only what was known at the decision point, does RDL recommend interventions that resemble what later worked, and does it distinguish a case that succeeded from one that failed?

## The hindsight problem
The authors know the outcomes (Montreal worked; Kyoto and Paris have not delivered). Any domain-specific intervention list written now would encode that knowledge. Therefore:

1. **One generic intervention library for all domains.** The same instrument types, written once, with the same effectiveness labels, for ozone, climate and every later case:
   - binding regulation or ban with deadlines
   - price instrument (tax, levy, permit trading)
   - subsidy or public investment in substitutes
   - finance transfer to lower-income parties
   - trade measures against non-participants
   - voluntary targets or pledges
   - information, labelling and reporting
   - research and monitoring
2. **Labels are set from general policy-evaluation evidence, not from these cases.** Any label that cites ozone or climate evidence is excluded.
3. **Inputs come only from what was knowable at the decision date**, recorded with sources:
   - ozone: decision date 1985-06 (after Farman et al. 1985, before Montreal 1987)
   - climate: decision dates 1997-11 (before Kyoto) and 2015-11 (before Paris)
4. **The library, labels and scoring are frozen in a commit before the first run.** The commit hash is recorded here.
5. **Held-out case:** leaded petrol phase-out. It is not looked at while building anything above; it is run once, after the others.

## Problem-structure inputs (added before running)
RDL v0.2 sees only pipeline bottlenecks (validation, translation, budget, deployment, persistence, contradiction). At the decision dates, ozone and climate looked similar on these. What differed was the structure of the problem:
- number of major producers or emitters
- availability and cost of substitutes
- share of the economy affected

These are added as explicit inputs, valued from sources dated before each decision date.

## Pass and fail criteria (fixed now)
- **Pass (discrimination):** RDL's predicted gain for its recommended portfolio is higher for ozone-1985 than for climate-1997, and the ranking is driven by recorded inputs, not by domain name.
- **Pass (resemblance):** for ozone-1985, at least two of RDL's top three instruments are among binding regulation with deadlines, finance transfer, trade measures, and support for substitutes.
- **Fail:** RDL ranks voluntary pledges in its top three for either case while binding options are feasible on its own inputs, or it cannot distinguish the two cases.
- **Prediction made before running:** without the problem-structure inputs, RDL v0.2 is expected to **fail discrimination**, because the two cases' pipeline profiles are similar. If that happens, it is a finding about what RDL must model, not a defect to hide.

## Not claimed
Passing would show that RDL's rules are consistent with two historical cases and one held-out case. It would not show that RDL predicts the effect of new policies.

## Change log
- 2026-10-20, before any historical case was run. The engine first ranked instruments by ease and speed (capacity, time to effect, evidence). Synthetic controls exposed two flaws: voluntary pledges ranked first in every structure, and a hard problem got a higher predicted gain than an easy one. Fix: instruments are now rated by a separate **delivery effect** label (size of behaviour change: binding regulation and price instruments high; substitute support, finance transfer and trade measures medium; pledges, information and research low), and finance transfer's effect scales with substitute availability. Found with synthetic structures only; no ozone or climate input had been prepared.
- Labels: no domain-independent policy-evaluation source was verified for the delivery, capacity or structure rules. They are documented assumptions, identical for all domains, written by authors who know the ozone and climate outcomes. This weakens the test: a pass would show internal consistency with history, not independent validation.

Frozen at commit: 2c44071 (engine, generic library, labels and structure rules). Structure input values and bottleneck profiles: docs/RDL_BACKTEST_INPUTS.md, committed before the first run.

## Result of the first run (2026-10-20, inputs at commit 9b9422f, unchanged)
- Without structure inputs: discrimination **fails** (ozone 0.224 = climate-1997 0.224), as predicted.
- With structure inputs: discrimination **passes** (ozone 0.160 > climate-1997 0.126; climate-2015 0.147). Resemblance **passes** (ozone top 3: substitute support, finance transfer, binding regulation). Voluntary pledges are in no top 3.
- Swap test: ozone profile with climate-1997 structure gives 0.136; climate-1997 profile with ozone structure gives 0.159. The ranking follows the structure inputs, not the case.
- Sensitivity (done after the run, not a pre-registered criterion): across 162 combinations of the flagged values, ozone stays ahead in 144. All 18 reversals have ozone substitutes = 0.25 and climate substitutes = 0.5. The pass rests on the substitutes input, the least well-sourced one; actor count and economic share barely move the result because the top-ranked instruments do not use them.
- Resemblance passes with or without structure inputs, so it tests the delivery labels, not the inputs. It is a weak criterion.

## Held-out case result (2026-10-20, inputs at commit c5d8ad9, run once)
- Discrimination: **FAIL.** Leaded petrol 2002 predicted gain 0.119 < climate 1997 0.126. Fails in all four pre-stated sensitivity settings (0.108-0.121).
- Resemblance: pass (substitute support, finance transfer, price instrument). Pledges: not in top 3.
- Secondary measure (added before the run, cannot rescue the primary): portfolio quality 0.251 vs climate 0.183, so RDL rates the remedies for lead as more likely to work.
- Diagnosis: the gain scales with the remaining gap, and in 2002 lead had a smaller gap (0.475 vs 0.688). RDL's "predicted gain" measures how much is left to fix times remedy quality; it does not measure tractability. The ozone-vs-climate pass did not expose this because their gaps were almost equal.
- Second finding: binding regulation (national bans, which is how lead was in fact removed) is not in the top 3. The only dominant bottleneck was budget, so binding regulation got half relevance.
- Overall: RDL as frozen at 2c44071 passes the two development cases and **fails the held-out case.** Any change made now is a new model version and needs a new held-out case.
