# RDL v0.3 protocol (pre-registration)

Status: written and committed before any v0.3 code exists. RDL v0.2 (engine frozen at 2c44071) passed its two development cases and failed its held-out case (see RDL_BACKTEST_PROTOCOL.md). v0.3 is a new model and needs new held-out cases.

## What changes, and why
1. **Two outputs instead of one.** v0.2 reported predicted gain = gap x remedy quality, which mixes "how much is left to fix" with "whether it can be fixed". v0.3 reports them separately:
   - **remaining_gap** (0-1): unchanged from v0.2 (`measured_gap`).
   - **tractability** (0-1): mean feasibility x effect of the top 3 instruments.
   - predicted gain is still computed, for continuity, but is not used in any criterion.
2. **Instruments are not tied to pipeline stages for ranking.** v0.2 halved the score of an instrument that did not target a "dominant" stage, which pushed national bans out of lead's top 3. v0.3 ranks instruments by feasibility x effect only. The stage link is kept for explanation (which stage an instrument repairs), not for ranking.
3. Nothing else changes: same generic library, same delivery and capacity labels, same structure rules, same input rules (RDL_BACKTEST_INPUTS.md).

## Development cases (already seen; may be used to check the code)
Ozone 1985, climate 1997, climate 2015, leaded petrol 2002, with the inputs already committed. Changes to v0.3 are allowed while running these, and every change is logged below.

## Held-out cases (chosen now, inputs not yet prepared)
A pair, so that discrimination can be tested on held-out cases alone:
- **Expected tractable: European sulphur emissions.** Decision date 1985-07 (Helsinki Protocol to the 1979 LRTAP Convention, 30% cut).
- **Expected intractable: chrysotile asbestos, global.** Decision date 2004-09 (first proposal to list chrysotile under the Rotterdam Convention).

The authors know both outcomes (sulphur fell steeply; chrysotile is still produced and the listing is still blocked). Asbestos is a hard test on purpose: substitutes exist and the economic share is small, so if RDL rates it tractable, the reason will be visible (a few producer states blocking consensus, which RDL does not model).

## Pass and fail criteria (fixed now)
- **Development check (all must hold before the held-out run):** tractability of ozone 1985 and of leaded petrol 2002 > climate 1997; no voluntary pledges in any top 3 while binding regulation is feasible; binding regulation in the top 3 for leaded petrol.
- **Held-out pass:** tractability of sulphur 1985 > chrysotile 2004, and sulphur 1985 > climate 1997.
- **Held-out fail:** either comparison reversed, or voluntary pledges in a top 3.
- One run of the held-out pair, after the code and inputs are committed.

## Not claimed
Passing would show consistency with five historical cases, three of them used in development. It would not show that RDL predicts the effect of new policies.

## Change log
(empty)
