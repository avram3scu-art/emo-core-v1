# RDL backtest protocol (pre-registration)

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
