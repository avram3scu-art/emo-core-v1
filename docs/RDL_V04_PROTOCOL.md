# RDL v0.4 protocol (pre-registration, before any data is received)

Status: written 2026-10-20, after requesting the Oslo-Seattle (OSP) and International Regimes Database (IRD) data, before receiving or seeing any coded value. Variable names and recodes are taken from the OSP replication variable list (ISR.Replic-file.var-OSP.pdf, Underdal's former UiO page), which documents the data used in Breitmeier, Underdal & Young (2011), *International Studies Review* 13(4):579-605.

## Why v0.4
RDL v0.2 and v0.3 failed their held-out tests (RDL_BACKTEST_PROTOCOL.md, RDL_V03_PROTOCOL.md). The missing ingredients (decision rules, veto power, malignancy of the problem) are the core variables of the regime-effectiveness literature (Miles et al. 2002; Breitmeier, Young & Zürn 2006). v0.4 takes its variables from that literature and its inputs from coders independent of the EMO authors.

## What is not new
Testing problem malignancy and institutional capacity against regime effectiveness is what Miles et al. (2002) and Breitmeier, Underdal & Young (2011) did. This test checks whether EMO's tractability score reproduces their kind of result. It is a calibration of EMO's tool, not a new finding about regimes.

## Unit and outcome
- Unit: the regime component, as coded in the OSP SPSS file.
- Primary outcome: behavioural change (OSP Var63), recoded as in the OSP file: 0-2 -> 1 (low), 3-4 -> 2 (high).
- Secondary outcome: problem-solving (OSP Var66, distance to collective optimum), recoded 1 -> 1, 2-4 -> 2. The direction (whether 1 means close to or far from the optimum) is read from the codebook before the data file is opened, and recorded below.

## RDL v0.4 tractability score (fixed now; no fitting)
Four binary indicators, each 1 = favourable, using the OSP recodes:
1. **Benign problem**: malignancy aggregate (Var15 with Var18 and Var28 as in the OSP file) = the benign category.
2. **No veto**: decision rule (IRD Var40a) is not unanimity or consensus.
3. **Capacity**: secretariat role (Var44), conference chair role (Var45) and fast-track options (Var43), each recoded as in the OSP file; favourable if at least two of three are in the higher category. Var40a is left out of capacity here to avoid counting the decision rule twice.
4. **Low uncertainty**: IRD Var58 recoded 1-2 (low).

Tractability T = mean of the four indicators (0, 0.25, 0.5, 0.75, 1). Missing indicator: T is the mean of those available if at least three are present; otherwise the component is excluded.

Equal weights are used because no weight can be justified without fitting. Power skew (Var72) is recorded but not in T, because its direction for effectiveness is contested in the literature.

The direction of each category (which code means "benign", "consensus", "low") is read from the codebook only, before opening the data file, and recorded in the change log in a separate commit.

## Hypotheses and criteria
- **H1 (primary):** Spearman correlation between T and behavioural change > 0, one-sided permutation p < 0.05 (10,000 permutations, seed 0).
- **H2:** the same for problem-solving.
- **H3 (does RDL add anything):** T's correlation with behavioural change is higher than that of the benign-problem indicator alone. If not, RDL v0.4 adds nothing over Underdal's single variable at this sample size.
- **H4 (the asbestos lesson):** components with a veto rule have lower mean behavioural change than components without, one-sided permutation p < 0.05.
- **Development cases:** components from the ozone regime and from LRTAP were used to build RDL v0.2/v0.3. All results are reported with and without them; the verdict uses the "without" result.
- **Verdict:** pass if H1 holds without the development cases. H2-H4 are reported whatever the outcome.

## Small-sample warning
Miles et al. (2002) cover 14 regimes; the number of components in the file is not yet known. With roughly 30-45 units and a four-level score, a true moderate correlation can easily miss p < 0.05. A fail would mean "not shown at this size", not "no relation".

## If the IRD arrives instead
The same four concepts are mapped from the IRD codebook to IRD variables, written down and committed before the IRD data file is opened. Outcome: the IRD effectiveness variable closest to behavioural change, chosen from the codebook alone.

## Code
`analysis/rdl_v04_test.py`, written and tested on synthetic data before any real data is received. It takes a CSV with one row per component and columns: component_id, regime, var15, var18, var28, var40a, var43, var44, var45, var58, var63, var66.

## Checks of the test itself (synthetic data only, before any real data)
- False-positive rate under no relation: 0.037 over 300 simulated datasets of 30 components (target 0.05). One of the two first synthetic null files passed by chance (p = 0.006), which is what a 5% test does about once in twenty.
- Power for a moderate simulated relation at 30 components: 0.32. **A fail is the likely outcome even if RDL's variables matter.** The verdict must be read with this in mind.
- The script refuses to open real data until the codebook directions are confirmed and committed.

## Change log
(empty)
