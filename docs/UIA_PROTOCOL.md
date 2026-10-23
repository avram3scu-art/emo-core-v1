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
| C, coherence | Rolling mean of GWI, clipped to [0,1]. | Only if GWI passes on real data (session 6: Wikipedia pageviews, public). Pageview coverage starts July 2015 (corrected in session 6 from "mid-2000s"; source: pageviews.wmcloud.org Langviews FAQ, opened in session 6). | Session 6's control windows | **Conditional on session 6.** |
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
| I | information integration | synergy (session 8), GWI (session 6) | No (untested) |
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
- **No He prediction is pre-registered yet.** Trigger: DAC holds at least 8 coded cases whose warning dates
  fall after the start of pageview coverage. Then a new protocol section, committed before any scoring,
  states the prediction, statistic and fail condition.
- Session 12 (the He direction test) is postponed until that trigger is met.
