# UIA protocol (session 5, 2026-10-23)

Status: audit done; Adrian chose Option C (§4). No UIA data was opened before this commit.
Files read: `emo/uia_engine/*.py` (450 lines), `api/routers/uia.py`, `tests/test_uia_engine_smoke.py`,
`WHITEPAPER_EMO_v1_1_funders.md` §3.1–3.2 and §4.3, `docs/PLAN.md` ("The scientific spine", sessions 5 and 12).
Header rows only of `data/dac_ozone_events.csv` (to read warning dates).

## 1. Audit: can each a_UIA term be computed from real public data today?

`aggregate.py` computes a_UIA = αR + βℓ²B + γτ_C dC + δ dS/S₀ + ε dI/I₀ + η M_E/M₀ with every
coefficient 1.0. That is a weighted sum with chosen weights, which `CLAUDE.md` forbids. The only test
(`test_uia_engine_smoke.py`) checks types and length on five synthetic points.

| Term | What the code actually does | Public data today? | Noise control | Verdict |
|---|---|---|---|---|
| R, informational curvature | "Gradient" is set to −θ; the skill metric is read but never used, so R depends only on the sampled parameters. log det(F)/dim is not the scalar curvature of a Fisher metric. | No. There is no defined parametric model of the human–Earth interface whose Fisher metric could be estimated. | None possible | **Not measurable. Drop.** |
| B, focusing | B̃ is hard-coded to 3.0; B = 3·mean(H)²; shear and vorticity arguments are ignored. "Expansion H" has no definition at this interface. | No observable defined. | None | **Not measurable. Drop.** |
| C, coherence | Rolling mean of GWI, clipped to [0,1]. | Only if GWI passes on real data (session 6: Wikipedia pageviews, public). Pageview coverage starts July 2015 (corrected in session 6 from "mid-2000s"; source: pageviews.wmcloud.org Langviews FAQ, opened in session 6). | Session 6's control windows (event-level only) | **Conditional on session 6.** Updated in §5: not usable as a level; stays retired with a_UIA. |
| S, entropy rate | Shannon entropy of normalised planetary-boundary indicators: measures how evenly the indicators are spread, not an entropy rate. Changes with the indicator set and normalisation. | Partly: some indicators (CO₂, ODS) in OWID. No public annual series for all boundaries found (not searched). | None that makes the quantity meaningful | **Computable but meaningless. Drop.** |
| I, information rate | Positive differences of a skill series. Clipping at zero makes pure noise look like gain (biased upward). | Yes, but via `emo/info_time.py` (τ_I), not this code: NHC track errors 1970–2025 and ECMWF headline scores are in `data/`. | τ_I has slope CIs and a year-shuffle control (`analysis/information_time_nhc.py`) | **Measurable today, as τ_I. Keep; move to F.** |
| M_E, semantic efficiency | Sum of risk reduction / sum of energy. | No. Neither risk reduction attributable to governance action nor the energy spent on it exists as a public series. | None | **Not measurable. Drop.** |

Result: 1 of 6 terms measurable today (and only through other code), 1 conditional, 4 not measurable.
a_UIA as written cannot be computed from real data, and the white paper's "single dimensionless
cognitive-health indicator" has no measured basis.

## 2. Proposal: UIA = the He profile at the human–Earth interface

UIA is redefined as the profile (I, C, F, E, D; He), reported side by side, never summed.

| Letter | Meaning | Candidate measure | Exists today? |
|---|---|---|---|
| I | information integration | synergy (session 8), GWI (session 6) | GWI: event detection passed for one hazard class (session 6); not yet usable to score I (§5). Synergy: untested |
| C | coordination | cooperation axis of the organismality plane | Yes (`analysis/organismality_plane.py`) |
| F | feedback, self-modelling | τ_I (yes); SMF (session 7) | Partly |
| E | resources | DAC budget sublayer at warning date | Partly |
| D | fragmentation, delay, contradiction | conflict axis; contradiction score | Partly |
| He | emergent capacity | DAC warning→delivery lag | Yes, 2 cases |

Rules fixed now:
- **No circularity.** D must not contain any DAC lag, because He is a DAC lag.
- **Dated before warning.** Every score uses only data dated before the case's warning date.
- **Failed metrics drop out.** If a metric fails its own pre-registered test (sessions 6–8), its letter is
  scored "not measured" and excluded; it is not replaced after the He data are seen.
- `a_UIA` in `emo/uia_engine/aggregate.py` and `/v1/uia/*` are marked deprecated; no new claim uses them.

## 3. The prediction: three options (Adrian decides)

Problems any option must face:
- **n.** Two DAC cases are coded (ozone, climate); a third comes in session 10. With n = 3 no rank
  statistic can reach p < 0.05 (smallest one-sided p for Spearman/Kendall is 1/6).
- **Outcome already known.** Ozone delivered faster than climate; scoring after knowing this is open to bias.
- **Coverage.** Ozone warning dates are 1974 and 1985. Pageviews, and so GWI and pageview-based synergy,
  cannot be measured then; UCDP conflict data also starts later (start year unverified). I and part of D
  are unmeasurable for the ozone case.

**Option A — pilot on DAC cases, as the plan says.**
Prediction: ranking cases by delivery lag (shorter = higher He), each measured letter I, C, F, E ranks
cases the same way and D the opposite way.
Statistic: per letter, sign of Kendall τ between letter and −lag. Fail if fewer than half the measured
letters have the predicted sign, or if fewer than 3 letters are measurable for every case.
Honest label: a pilot; it cannot pass in any statistical sense, and with the coverage problem it will
probably fail on "fewer than 3 letters measurable". Cheap; keeps sessions 10 and 12 as planned.

**Option B — change the unit to many cases.**
Countries under one treaty (e.g. Montreal Protocol phase-out timing per country from OWID ODS
consumption) give dozens of cases and a real statistic. But per-country I and F do not exist, and the
treaty itself gave developing countries a later deadline (Article 5; from memory, unverified), so E is
confounded by design. Needs its own data audit before it can be pre-registered: one extra session.

**Option C — retire a_UIA now, defer the He test.**
Commit the audit and the profile definition; pre-register no He prediction until DAC has at least 8
coded cases with warning dates after the start of pageview coverage. Session 12 is postponed. Honest,
but UIA has no test for a long time.

**Recommendation:** C for the prediction, plus the retirement of a_UIA (needed under every option).
A spends a session on a result fixed in advance by coverage and n; B is worth considering only if a
per-country I and F can be found.

## 4. Decision

Adrian's decision (2026-10-23, 11:04 Brussels): **Option C.**

- a_UIA is retired: `emo/uia_engine/aggregate.py` and `/v1/uia/*` are deprecated; no claim may rest on them.
- UIA is defined as the He profile of §2, with the rules fixed there (no circularity, data dated before
  warning, failed metrics drop out).
- **No He prediction is pre-registered yet.** Trigger (raised to 24 on 2026-10-26, see §6): DAC holds at least 8 coded cases whose warning dates
  fall after the start of pageview coverage. Then a new protocol section, committed before any scoring,
  states the prediction, statistic and fail condition.
- Session 12 (the He direction test) is postponed until that trigger is met.

## 5. Update after session 6 (2026-10-23, UIA follow-up)

GWI passed its pre-registered event test (`docs/GWI_PROTOCOL.md` §7: 14/21 event windows vs 9/275
controls, Fisher p = 2.3e-13; placebo p = 0.061). Decision recorded here, since a pass does not by
itself make GWI usable for UIA.

**What the pass shows.** Ignition days fall in hurricane-landfall windows far more often than in
control windows. Both sets use the same threshold, so the result holds even though the threshold is
miscalibrated. It is a statement about *timing relative to controls*, for one hazard class and one article.

**What it does not show.** `compute_gwi` expected 0.012 false ignitions under independent streams and
found 95 (test) and 15 (placebo). The binomial threshold is not a calibrated false-alarm rate on real
streams. Any use of GWI as a *level* (how much ignition, or how coherent attention is, at a given
date) inherits that miscalibration: the level mixes real ignition with shared cross-language news-cycle
co-movement.

**Decisions.**
1. *a_UIA's C (coherence = rolling mean of GWI):* **not usable**. It is a level, so the session-6 pass
   does not support it. It stays retired with a_UIA.
2. *Naming:* a_UIA's C (coherence) is not the He profile's C (coordination). GWI belongs to He's **I**
   (information integration), not to C. The He C remains the organismality cooperation axis.
3. *GWI in He's I:* **not yet usable for scoring.** Scoring I at a warning date needs a level, which needs
   calibration first. GWI may score I only after a separate pre-registered calibration test passes, with:
   - a null that keeps the streams' shared co-movement (e.g. per-stream circular-shift surrogates, or the
     placebo article's ignition rate as the baseline), fixed before data;
   - calibration chosen on data already opened (pageviews to 2025-12-31) and tested only on pageviews
     not yet opened (2026-01-01 onward);
   - pass: false-ignition rate on held-out control windows within the nominal rate stated in advance.
4. *Coverage still binds:* pageviews start July 2015, so GWI cannot score I for either coded DAC case
   (ozone 1974/1985; climate pre-2015). This leaves the §4 trigger unchanged.

No UIA or GWI data were opened for this update; it uses only the committed session-6 result.

**Calibration test result (2026-10-23): FAIL** (`docs/GWI_CALIBRATION_PROTOCOL.md` §7). The calibrated
threshold held in time but not across articles ("Prime number" 0.0134 vs ≤ 0.010). GWI therefore does
**not** score I. A new calibration design would need its own pre-registration; it is not proposed here.

## 6. Update after the He calibration (2026-10-26)

Source: `docs/HE_CALIBRATION_PROTOCOL.md` §6–§7 (synthetic, pre-registered; reproduced in CI by the
weekly run 40389674340). Adrian's decision (26 Oct 2026, 20:49 Brussels: "Record and apply
everything necessary to EMO") applies the calibration's proposal:

1. **Statistic for the He direction test: T-D.** Mean Kendall τ between each measured letter and
   −lag (D sign-flipped), one-sided permutation test over cases (letters permuted together),
   α = 0.05. It held 3.5–5.9% false positives in every cell tested.
2. **The §3 Option A rule is retired.** "At least half the measured letters with the predicted
   sign" passes 41–52% of the time when nothing is there, at every n. Uncorrected per-letter tests
   (7–23%) are also excluded.
3. **Trigger raised from 8 to 24 coded cases** (warning dates after pageview coverage, unchanged).
   At 24 cases T-D reaches ≥ 0.80 power for β = 0.5 with 3 or 5 letters, including a shared trend
   among letters (λ = 0.5). At 8 cases power was 0.34–0.55.
4. **Runs with 8–23 cases are pilots.** They may be run, but are labelled pilot in advance: a
   non-significant result there cannot count as evidence against He.
5. **Stated limit of the trigger.** 24 cases is enough only for a strong link (β = 0.5). For a
   weaker link (β = 0.3) with a shared trend among letters, power is 0.60–0.64 at 40 cases and
   0.78–0.80 at 60 (`docs/HE_CALIBRATION_PROTOCOL.md` §9), so 60 cases still fall short. The
   pre-registration for session 12 must state the effect size it is powered for.
6. **New requirement for the pre-registration:** measure and report the shared trend among letters
   (e.g. correlation of each letter with the case's warning year), because it is the factor that
   costs most power.

## 2.0 UIA 2.0: the per-event profile of the loop links (session 2.9, 29 Oct 2026)

Evidence class of this section: **infrastructure** (a definition). Committed before any lag or link value of `data/loop_hurricanes/loop_events.csv` was opened in session 2.9 (only its header and the season counts in `summary.json`, already reported in `docs/LOOP_PROTOCOL.md` §19, were read). Moves H4 (`docs/PLAN.md` §4) by fixing the measure the He direction test uses.

**Definition.** For each event e of a loop domain, UIA 2.0 is the profile of its measured links, reported side by side, one column per link, **never summed, weighted or averaged into a score**:

| Link (PLAN §3) | Hurricane measure (LOOP_PROTOCOL §3) | Column | Predicted sign vs He |
|---|---|---|---|
| Predict | F, 48-h track skill vs CLIPER5/OCD5 before t0 | `pr_F` | + |
| Attend | A, log10 pre-landfall views (3 days before t0) | `at_A` | + |
| Warn (part of decide-act, before t0) | W, earliest watch/warning lead (h) | `wn_W_hours` | + |
| Decide-act (state) | Y_state, DR request − t0 (days) | `dc_Y_state_days` | (outcome) |
| Decide-act (federal) | Y_fed, DR declaration − request (days) | `dc_Y_fed_days` | (outcome) |
| Choose | registered forecasts (LOOP_PROTOCOL §21) | ledger, per season | not per event |
| Learn | season trend of residual lags (H5) | per season | not per event |

**He (emergent capacity) of an event** = −(Y_state + Y_fed) = −(date of the DR declaration − date(t0)), in days: the landfall→federal-declaration lag, sign-flipped so that higher He = faster response. It is the hurricane analogue of the DAC warning→delivery lag (§2). Missing if either lag is missing.

**Rules (§2 kept):** no circularity (no letter contains a lag); every letter dated before t0 (F: forecasts with initial time < t0; A: the three days before t0; W: lead before t0); a letter not measured for an event is "not measured", never imputed; the §2 letters I (synergy), C, E and D have no per-event hurricane measure and are "not measured" in this domain. Code: `emo/uia2.py` builds the profile table (column selection plus He); output `data/uia2_hurricanes_profile.csv`. a_UIA stays retired (§4).

**Use in session 2.9 (29 Oct 2026):** He direction test, `docs/HE_CALIBRATION_PROTOCOL.md` §10.7: PASS on known history (T-D +0.220, within-season p = 0.0116), unconditional association led by attention; severity not controlled, so not evidence of coupling beyond procedure.
