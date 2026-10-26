# He direction test: calibration of the test itself (pre-registered)

Committed before the code is written and before it is run. Synthetic data only: no EMO, DAC or
UIA data are opened. Method origin: `analysis/test_the_test/README.md`.

## 1. Why

`docs/UIA_PROTOCOL.md` §4 postpones the He direction test until DAC holds at least 8 coded cases,
and §3 Option A proposes a rule: per letter, the sign of Kendall τ between the letter and −lag;
fail if fewer than half the measured letters have the predicted sign. Neither the trigger (8 cases)
nor any candidate rule has been checked for its false-positive rate or its power. This protocol
checks them before any He prediction is pre-registered, so the eventual test is a fair one.

This calibrates a statistical procedure under assumed parameters. Part of the result is
arithmetic (e.g. a sign rule on random data passes about half the time); it is recorded because the
point is to rule such rules out before real data are scored.

## 2. Synthetic world

For each of n cases:
- latent capacity H ~ N(0, 1);
- observed He (from the coded warning→delivery lag) = H + 0.5·ε (coding error);
- m measured letters among I, C, F, E (predicted +) and D (predicted −). Letter k:
  L_k = s_k · [β·H + √(1−β²)·(√λ·G + √(1−λ)·U_k)],
  with s_k = +1 for I, C, F, E and −1 for D; G a factor shared by all letters and unrelated to H
  (e.g. a common calendar trend); U_k independent.

Grid: β ∈ {0 (null), 0.3, 0.5}; λ ∈ {0, 0.5}; m ∈ {3, 5} (m = 3 drops D and E);
n ∈ {3, 8, 12, 20, 30}. 2,000 simulated studies per cell; 499 permutations where used.
Seed 20261029. Sign flip for D is applied before every statistic, so "predicted direction" is
always positive.

## 3. Candidate tests (each one-sided, α = 0.05)

- **T-A (UIA §3 Option A rule):** pass if at least ⌈m/2⌉ letters have Kendall τ > 0.
- **T-B:** per letter, exact one-sided Kendall test; pass if any letter has p < 0.05 (no correction).
- **T-C:** as T-B with Holm correction across the m letters.
- **T-D:** mean Kendall τ over the m letters; one-sided permutation p (He permuted across cases,
  letters kept together, so their shared factor stays in the null); pass if p < 0.05.

## 4. Criteria, fixed now

A test is **usable** at a given n and m if both hold:
1. false-positive rate at β = 0 ≤ 0.060 for both λ (0.05 + 2 Monte Carlo SE at 2,000 runs);
2. power at β = 0.5 ≥ 0.80 for both λ.

Reported for each test: false-positive rate and power in every cell, and the smallest n in the grid
at which it is usable (or "none up to 30").

Expectations written before running (to be checked, not assumed): T-A is not usable at any n
(false positives near 50%); T-B over-rejects as m grows; T-D holds its rate; 8 cases are too few for
80% power at β = 0.5.

## 5. Consequence for UIA

If the result shows the Option A rule unusable, it is recorded against Option A. The smallest usable
n of the best test is a proposal for the §4 trigger; changing the trigger is Adrian's decision.

## 6. Result

Single run, 26 Oct 2026, ~3 min, in Claude's workspace (not CI). Code `analysis/he_calibration.py`
(committed 65a4a36 before the run), output `analysis/he_calibration_output.txt`. Evidence class:
pre-registered, synthetic.

**False-positive rate at β = 0** (range over n = 8–30, both λ, both m):

| Test | FPR | Verdict |
|---|---|---|
| T-A (Option A sign rule) | 0.41–0.52 | **fails at every n**: about one study in two "passes" when there is nothing to find |
| T-B (any letter, uncorrected) | 0.07–0.21 | fails; worse with more letters |
| T-C (Holm) | 0.03–0.05 | holds |
| T-D (mean τ, permutation) | 0.04–0.05 | holds |

At n = 3 no test except T-A can reject at all (T-B–T-D: 0.000), as `docs/UIA_PROTOCOL.md` §3 stated.

**Power at β = 0.5** (best calibrated test, T-D; m = 5):

| n | λ = 0 | λ = 0.5 |
|---|---|---|
| 8 | 0.55 | 0.34 |
| 12 | 0.78 | 0.51 |
| 20 | 0.96 | 0.75 |
| 30 | 1.00 | 0.92 |

With m = 3 power is lower (n = 30: 0.98 / 0.87). T-C is calibrated but has lower power than T-D in
every cell with β > 0; T-D is the better test.

**Usable (criteria §4):** T-A never; T-B never; T-C at n = 30 for m = 5 only; **T-D at n = 30**
(m = 3 and m = 5). Between 20 and 30 the grid has no point, so the true threshold for T-D lies in
(20, 30].

**Expectations (§4) vs result:** all four held: T-A unusable, T-B over-rejects and worsens with m,
T-D holds its rate, 8 cases too few (power 0.34–0.55 at β = 0.5).

**What this shows and does not show.** It rules out the Option A rule and uncorrected per-letter
tests for any He direction test, and shows that the current trigger (8 cases) gives a test that
would miss a real β = 0.5 effect about half the time or more. It does not show that β = 0.5 is
realistic: if letters relate to He more weakly, more than 30 cases are needed (β = 0.3, n = 30:
power 0.52–0.86). A shared factor among letters (λ = 0.5, e.g. a common calendar trend) costs
power; dating letters before the warning (UIA rule) does not remove such a factor.

**Proposal for Adrian's decision (not applied):** (1) pre-register T-D, not the Option A rule, as
the He statistic; (2) raise the §4 trigger from 8 to about 30 coded cases, or accept and state a
power of roughly 0.5 at 8 cases, labelling that run a pilot that cannot fail informatively.
