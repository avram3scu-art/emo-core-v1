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

## 7. Amendment 1 (pre-registered 26 Oct 2026, before its run): fill the grid

Two gaps in §6: the T-D threshold lies somewhere in (20, 30], and power for a weaker link
(β = 0.3) was below 0.80 at every n tested. Same model, tests, criteria and code as §2–§4
(functions imported unchanged from `analysis/he_calibration.py`); new seed 20261030;
code `analysis/he_calibration_grid2.py`, output `analysis/he_calibration_grid2_output.txt`.

- Part A: n ∈ {22, 24, 26, 28}; β ∈ {0, 0.5}; λ ∈ {0, 0.5}; m ∈ {3, 5}.
  Reported: smallest n in {20 (from §6), 22, …, 30 (from §6)} at which T-D is usable (§4 criteria).
- Part B: n ∈ {40, 60}; β ∈ {0, 0.3}; λ ∈ {0, 0.5}; m ∈ {3, 5}.
  Reported: whether T-D reaches power ≥ 0.80 at β = 0.3 (both λ) with FPR ≤ 0.060.

Expectation written now: Part A threshold near 24–26 for m = 5 and 26–30 for m = 3 (driven by
λ = 0.5); Part B: n = 60 reaches 0.80 at β = 0.3 for λ = 0 but probably not for λ = 0.5.

## 8. Reproduction in CI

From 26 Oct 2026 `analysis/he_calibration.py` is a frozen run in `scripts/weekly_run.py`: the weekly
run must reproduce `analysis/he_calibration_output.txt` exactly, or the commit is blocked.

## 9. Result of amendment 1 (§7)

Run in Claude's workspace, 26 Oct 2026. **First run aborted** after 50 of 64 result lines (process
ended with no error message; cause unknown, likely the workspace stopping a long background job).
Rerun once, same code and seed, complete; its first 50 lines are byte-identical to the aborted
run's, so the abort did not change any result. Output `analysis/he_calibration_grid2_output.txt`.

**Part A (T-D usable, §4 criteria):** smallest n = **24** for both m = 3 and m = 5 (22: power
0.76–0.79 with a shared trend, just short). False positives 3.5–5.9% in every cell.

**Part B (β = 0.3, T-D):** FPR within limit everywhere. Power without a shared trend:
0.84–0.95 at n = 40, 0.94–0.99 at n = 60. With a shared trend (λ = 0.5): 0.60–0.64 at n = 40,
0.78–0.80 at n = 60, so **not reached even at 60** (m = 5: 0.799).

**Expectations (§7) vs result:** Part A threshold came lower than expected for m = 3 (24, not
26–30); for m = 5 as expected. Part B as expected: 60 cases reach 0.80 without a shared trend,
not with one.

**Consequence:** the shared trend among letters, not the number of letters, decides how many cases
a weak-link test needs. Measuring it (UIA §6 point 6) comes before choosing n.

## 10. He direction test on the hurricane loop, 2015–2025 (session 2.9, 29 Oct 2026; pre-registered on known history)

**Power statement (synthetic, §10.6; before the data were opened):** within-season FPR 0.037–0.049 (across-all null 0.665–0.779 under a season shock); power at β = 0.5: 0.54–0.75; **at β = 0.3 power is below 0.5 (0.26–0.41)**, so a non-significant result reads "not shown at this size" for any link weaker than β = 0.5.

**Evidence class: pre-registered on known history.** All 52 events of 2015–2025 entered the session 2.5 run (`docs/LOOP_PROTOCOL.md` §19), and their lag summaries (min/median/max) and counts are published there, so no unused loop event remains; 2026 is excluded (LOOP_PROTOCOL §1) and 2027 rows are reserved for session 2.12b and are not used. Why no prospective test now (CLAUDE.md "Prospective first"): the 2027 blind arm is registered (LOOP_PROTOCOL §20–§21) but cannot reach p < 0.05 for one season. Committed before any lag or link value was opened in session 2.9; inputs read before this commit: the table header and `summary.json` season counts.

### 10.1 What it tests, and what it cannot

- **Prediction (UIA §2.0):** events whose predict, attend and warn links are stronger have higher He (faster landfall→DR declaration).
- **It does not test H4 as stated.** H4 is "coupling beyond procedure": it needs controls for severity, region and triggers (LOOP_PROTOCOL §4–§5), and on 2015–2025 those controls cannot be fitted (guard §15: 9–10 within-season degrees of freedom < 15). T-D has no controls. A PASS here shows only an **unconditional association** within seasons, which severity alone could produce (stronger storms draw more attention, longer warning leads and faster declarations); it never reads as coupling beyond procedure, and H4's status stays "cannot be tested at this size" in this domain on 2015–2025.

### 10.2 Data and cases

`data/loop_hurricanes/loop_events.csv` (checked first by `scripts/validate_loop_table.py`: 52 rows, 0 failures required), rows with `ev_season` in 2015–2025 (asserted). Cases: rows with `dc_Y_state_days`, `dc_Y_fed_days`, `pr_F`, `at_A`, `wn_W_hours` all present. Expected from the counts: 23 cases in 9 seasons, sizes 2016:2, 2017:3, 2018:2, 2019:1, 2020:5, 2021:1, 2022:3, 2023:1, 2024:5. Letters m = 3 (F, A, W), predicted sign + for all; He as UIA §2.0.

### 10.3 Statistic and null

- **T-D** (§3): mean over the three letters of Kendall τ-a between letter and He (sign of pairwise differences; ties count 0), as in `analysis/he_calibration.py`.
- **Null: He permuted within season** (letters kept together; seasons with one case stay fixed). Change from §3, where He is permuted across all cases: CLAUDE.md requires a null that respects clustering, and a shock shared by a season's lags and letters (a busy year, an administration) would make the across-all null over-reject (checked in §10.5). 9,999 permutations, seed 2026102990; one-sided p = (1 + #{T_perm ≥ T_obs − 1e-12}) / 10,000. **α = 0.05.**

### 10.4 Reading rules

- **PASS:** p < 0.05 → "He direction shown within seasons on known history (unconditional association; not coupling beyond procedure)".
- **Not significant:** "He direction not shown"; if §10.6 power at β = 0.5 is < 0.5, "not shown at this size". No "no effect" reading (no equivalence bound is fixed).
- **Descriptive, no weight in any verdict:** per-letter τ; the shared trend among letters (UIA §6 point 6): Kendall τ of each letter and of He with season year, and the mean pairwise τ among the letters; severity: τ of each letter and of He with V (`ev_V_kt`); the across-all-cases permutation p (the §3 null), to show what the season stratification does.
- No step here is changed after the data are opened.

### 10.5 Synthetic check (code `analysis/he_loop_power.py`, committed before its run; output `analysis/he_loop_power_output.txt`)

Model of §2 at the realized season sizes (§10.2), m = 3, plus a season shock Z_s ~ N(0, 1) added with weight κ to He and to every letter (κ ∈ {0, 1}). Grid β ∈ {0, 0.3, 0.5}, λ ∈ {0, 0.5}; 2,000 studies, 999 permutations, seed 2026102991. Reported: rejection rate of T-D with the within-season null and with the across-all null. Criterion: within-season FPR ≤ 0.060 at β = 0 in every (λ, κ) cell, else the test is not run and reads "cannot be tested". Expectation written now: within-season holds; across-all over-rejects at κ = 1; power at β = 0.5 below the 0.80 of §9 at n = 24, because the three singleton seasons carry no information and within-season pairs are few.

### 10.6 Result of the synthetic check (single run, 29 Oct 2026, Claude's workspace, 7 min; before the data were opened)

| β | λ | κ | within-season | across-all |
|---|---|---|---|---|
| 0 | 0 / 0.5 | 0 | 0.045 / 0.045 | 0.044 / 0.054 |
| 0 | 0 / 0.5 | 1 | 0.049 / 0.037 | **0.779 / 0.665** |
| 0.3 | 0 / 0.5 | 0 / 1 | 0.412, 0.374 / 0.277, 0.255 | — |
| 0.5 | 0 / 0.5 | 0 / 1 | 0.754, 0.733 / 0.574, 0.539 | — |

Criterion met (max within-season FPR 0.049 ≤ 0.060): the test is run. Expectations (§10.5): all three held; the across-all null of §3 is unusable here if seasons share a shock (FPR up to 0.78). Power at β = 0.5 is 0.54–0.75, below 0.80, so even a strong link is missed a quarter to nearly half the time.
