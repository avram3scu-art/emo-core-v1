# Hurricane loop tests: pre-registration (session 2.3, 29 Oct 2026)

**Power statement (CLAUDE.md "Power before data"; synthetic, §14–§15, which supersede §10).** H4 with the amended statistic (§14), primary event set HU+TS at the planned ~54 storms: false-positive rate ≤ 0.006, also under strong season clustering; power 0.80 at r = 0.5 (0.76–0.79 under strong clustering) and 0.39 at r = 0.3. **H5 has power below 0.5** (0.12–0.41) and **the blind arm has power below 0.5** (2027 alone 0.08–0.24; five seasons of 4: 0.49): both are run as registered, and a non-significant result reads "not shown at this size". H4 is not run at all if the guard of §15 fails at the realized sizes. Planned sizes are unverified (§8.4).

Moves H3, H4, H5 (`docs/PLAN.md` §4). Evidence class of this file: **infrastructure** (protocol and synthetic method check). The tests it defines carry the class of their run: 2015–2025 = **pre-registered on known history**; 2027 season = **pre-registered blind**.

**No loop record was opened in writing this protocol.** No HURDAT2 data line, NHC error-file line, pageview count, FEMA declaration, NHC advisory or GIS file, or TCR was read in session 2.3. Inputs were documentation only: `docs/LOOP_DATA.md` (session 2.2), `docs/PLAN.md` §3–§5, `docs/HE_CALIBRATION_PROTOCOL.md`, `analysis/he_calibration.py`, `docs/FAILURES.md`, and the two format documents in `docs/sources/loop_data/`. The season sizes used to size the power simulation (§9) are a planning assumption from Claude's general knowledge of which hurricanes struck the US 2016–2024; they are **unverified**, were not taken from any loop record, and carry no weight in any verdict (the power is recomputed at the realized sizes, §8.4).

## 1. Split

- **Known history:** Atlantic seasons 2015–2025. Outcomes are public and partly known to Adrian and Claude, so no result on them is called blind or held-out.
- **Blind:** the 2027 season (events with landfall 1 Jun–30 Nov 2027), and later seasons pooled under §7.
- **Excluded:** the 2026 season (mostly before this commit; outcomes public).
- Why a historical arm at all (CLAUDE.md "Prospective first"): one blind season yields too few events for any test of adequate power (§10); the historical arm is the only way to size and check the method before 2027.

## 2. Events (HURDAT2)

- **File:** the HURDAT2 Atlantic file current when session 2.4 builds the table; its name and SHA-256 recorded there.
- **Storm:** a HURDAT2 system with ATCF id `ALnnYYYY`, YYYY in the split.
- **Landfall record:** a data line with record identifier `L`.
- **Event set HU (default):** the storm has at least one `L` record with status `HU` whose position lies in a US state, DC, Puerto Rico or the US Virgin Islands. Position → state: point-in-polygon against the US Census Bureau cartographic boundary file (version fixed and checksummed in 2.4; **unverified** source, not opened); a point outside every polygon but within 50 km of one is assigned to the nearest; beyond 50 km it is not a US landfall.
- **Event set HU+TS (alternative):** as HU, with status in {`HU`, `TS`}. Which set is the primary one is decided by the rule in §10, from synthetic power only, before any record is opened.
- **Event time t0:** the date and time (UTC) of the storm's earliest qualifying landfall record. **Landfall state k:** the state of that record. One row per storm (unit = storm; this removes within-storm clustering from the primary tests). A storm's later landfalls and its declarations in other states are reported descriptively only.
- **Severity at t0 (controls, named now):** V = maximum sustained wind (kt) of the t0 record; R64 = largest of the four 64-kt wind radii (n mi) of the t0 record (0 when absent or status TS). Sensitivity only: minimum pressure (mb) in place of V. The outcome link is not measured (LOOP_DATA §6): severity is a control, never a link.

## 3. Link measures and reading rules

### 3.1 Decide-act (OpenFEMA Disaster Declarations Summaries v2)

- **Candidate records:** `state` = k; `designatedIncidentTypes` contains `H` (set HU) or `H` or `4` (set HU+TS); `declarationType` major disaster (DR) or emergency (EM); `incidentBeginDate` within [date(t0) − 10 d, date(t0) + 3 d]. The `incidentType` string is not used for selection (unverified; recorded in 2.4).
- **Name rule:** keep candidates whose `declarationTitle` contains the storm name as a whole word (case-insensitive). If none does, keep the date-window candidates only if no other event in the table has a landfall in k within ±10 days of t0; otherwise the storm is **unmatched (ambiguous)** and listed.
- **Declaration level:** records are grouped by `disasterNumber`; per declaration, declaration date = earliest `declarationDate`, request date = earliest non-missing `declarationRequestDate`; `incidentId` recorded. A DR and an EM matched to the same storm with different `incidentId` are flagged and kept. If more than one DR matches, the earliest is used.
- **Lags (days, UTC calendar dates):** Y_state = date(DR request) − date(t0) (signed; a request before landfall is negative); Y_fed = date(DR declaration) − date(DR request) (≥ 0; a negative value is a data error, excluded and listed).
- **EMpre** = 1 if an EM matched to the storm in k has declaration date ≤ date(t0), else 0.
- **EM lags** are reported descriptively and enter no H4 or H5 test (§5).

### 3.2 Predict (NHC individual-forecast error file)

- **File:** `1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt` (TS+ storms); `STMID` = the HURDAT2 ATCF id.
- **F (track skill)** = 1 − Σ OFCL 48-h track error / Σ CLIPER5 48-h track error, over the storm's forecasts with initial time < t0 and both errors present (not −9999). The CLIPER5 column is identified from the file header in 2.4. Missing if the forecasts' summed 48-h equivalent sample size is < 2.
- **Dependence:** forecasts < 18 h apart are not independent (LOOP_DATA §3); F is a per-storm aggregate and the storm is the unit, so no forecast-level test is made.
- Intensity skill (vs SHIFOR5) is recorded for SMF v2 (session 2.7) and enters no test here.

### 3.3 Attend (Wikimedia pageviews, user agent, daily)

- **Article rule:** candidate titles on en.wikipedia: T1 "Hurricane {Name} ({YYYY})", T2 "Hurricane {Name}", and for set HU+TS T3 "Tropical Storm {Name} ({YYYY})". Each is resolved for redirects at pull time (session 2.4). Target = the article T1 resolves to; if T1 does not exist, T2's target if T2 is not a disambiguation page; else T3's target (HU+TS); else A is missing.
- **Views** = target user-agent daily views + views of every candidate title that redirects to the target at pull time. A day with no record counts 0 (an article created after naming has no views before creation; its creation date is recorded).
- **A (pre-landfall attention)** = log10(1 + Σ views over the three UTC days before date(t0)).
- The redirect-resolution API is a source not documented in session 2.2: **unverified**; 2.4 records its documentation or, if it cannot be opened, uses T1 only and says so.

### 3.4 Warnings (NHC GIS advisory watch/warning files, 2008+)

- **W (warning lead, hours)** = t0 − issuance time of the earliest advisory whose watch/warning file contains any tropical-storm or hurricane watch or warning for the storm. The issuance field is **unverified** (LOOP_DATA §7); fallback: the issuance time printed in the public advisory text of the same advisory number.

## 4. Controls and rule-based triggers

- **Control set C:** V, R64, FEMA region of the matched DR (`region`: 4, 6, other; two dummies), EMpre, season year (linear).
- **Rule-based triggers found in 2.2 and how each is handled:**
  1. FEMA 2006 pre-landfall policy (EM tied to an NWS threat projection plus evacuation orders): forecast→EM timing is procedure. EM lags are not tested; EMpre enters C, so any route forecast/warning → pre-landfall EM → faster DR request is removed. Because the control is the observed EM declaration, not the policy, the test reads the same whether or not the policy is still in force. Sensitivity: H4 rerun on storms with EMpre = 0 (descriptive only if fewer than 8).
  2. 44 CFR 206.35 deadlines (EM request within 5 days of need, ≤ 30 days after the incident) bound EM lags only; no DR test is affected.
  3. No automatic federal trigger exists (44 CFR 206.35): none to control.
- Rules not checked (state statutes, current FEMA policy text, 44 CFR 206.36 for DR requests) are a stated limit: a procedural link through them would read as coupling.

## 5. H4: coupling beyond procedure

- **Pairs (family of 6):** predictor X ∈ {F, W, A} × outcome Y ∈ {Y_state, Y_fed}. Predicted direction for all six: better forecasts, longer warning lead, more pre-landfall attention → shorter lag.
- **Statistic:** complete cases for the pair; X and Y each replaced by mid-rank / n; rX, rY = OLS residuals on C; r = corr(rX, rY); T = −r (positive = predicted direction).
- **Independent-agencies null (PLAN §3):** each link depends on severity, region, year and procedure (C) and on season-level conditions, but not on another link. Implemented as a permutation of rX **within season** (999 permutations; storms exchanged only with storms of the same season), so any shock shared by all links in a season (workload, administration, a busy year) stays paired and cannot produce a positive. Storm clustering is removed by the one-row-per-storm unit. One-sided p = (1 + #{T_perm ≥ T}) / 1000.
- **Holm** correction across the 6 pairs, α = 0.05 family-wise.
- **PASS** (coupling shown, known history): at least one pair with Holm-adjusted p < 0.05.
- **FAIL** (PLAN §4): no pair significant **and** power ≥ 0.8 at r = 0.5 for the realized sizes (§8.4); with power below 0.8 the reading is "not shown at this size", not a FAIL of H4.
- **"No effect" for a pair** only if the 90% interval for r lies inside (−0.3, 0.3): Fisher z with n_eff = Σ_seasons (n_s − 1) − 5 (the controls that vary within a season). Otherwise no "no effect" reading is made.
- **Sensitivity (no weight):** the same family with a naive null (permutation across all storms), and with EMpre removed from C, both to show what the controls do.

## 6. H5: learning

- **Statistic, per outcome Y ∈ {Y_state, Y_fed}:** complete cases; Y → mid-rank / n; residuals on C5 = {V, R64, region dummies, EMpre, F} (no year term), so severity mix and forecast gains are removed; season mean of the residuals for each season with at least one event; S = −Kendall τ(season year, season mean) (positive = lags shrink).
- **Null:** season means permuted across seasons (999 permutations): the season is the unit, so season clustering is respected and storms within a season never count as independent evidence of a trend.
- **Holm** across the 2 outcomes. PASS: an adjusted p < 0.05. Otherwise "not shown at this size" unless power at the realized number of seasons is ≥ 0.8 at Δ = 1 (§9), then FAIL.
- **No "no effect" reading for H5:** with about ten seasons no equivalence bound can be met; a non-significant H5 is never read as "no learning".
- **Limit (stated now):** H5 cannot tell loop learning from one agency improving on its own (e.g. FEMA processing); a PASS supports "lags shrink beyond severity mix and forecast gains", not coupling.

## 7. Blind arm (2027, then pooled)

- **One pair**, fixed in session 2.5 from the known-history result before 1 Jun 2027 (the pair with the smallest Holm-adjusted p; if none is significant, the smallest raw p), and registered in session 2.8.
- Rank transforms use the known-history empirical distribution (mid-rank); residuals use the regression coefficients fitted on 2015–2025, frozen.
- **Statistic:** S_b = −Σ rX·rY over blind events; null: permutation within each blind season (999). One-sided α = 0.05, no further correction (single pre-specified test).
- Later blind seasons are pooled into the same statistic; the pooled run is repeated each December until its power at r = 0.5 reaches 0.8 (§10 gives the size), and each run is reported with its power.

## 8. H3 and reading rules common to all

1. **H3 (decide-act measurable):** PASS if the share of events with both Y_state and Y_fed measured is > 0.5 (exact one-sided binomial, p < 0.05) and Y_state is not constant (interquartile range > 0 days). Unmatched, ambiguous and excluded events count as not measured.
2. Every exclusion (unmatched, missing link, data error) is listed with its reason in the 2.5 result.
3. No step of §2–§7 is changed after any record is opened; a change becomes an amendment tested on data not yet opened (CLAUDE.md "No retesting on seen data").
4. **Power at the realized sizes:** in 2.5, before the statistics are computed, `analysis/loop_power.py` is rerun with the realized season sizes (counts only, no lag or link values) and its power at r = 0.5 and Δ = 1 decides between FAIL and "not shown at this size".

## 9. Synthetic check (code `analysis/loop_power.py`, output `analysis/loop_power_output.txt`)

Committed before it is run. Synthetic data only; the module reads no file.

- **Season sizes (planning assumption, unverified):** HU = (2, 4, 2, 2, 6, 2, 3, 1, 5), 27 storms in 9 seasons with events; HU+TS = each size doubled (54). Variant "HU, 25% unmatched": each storm loses both lags with probability 0.25.
- **World:** severity V ~ N(0,1) with a trend in the severity mix; R64 correlated with V (0.5); three regions; season shocks of SD 0.7 with half their variance shared by every link and outcome in that season (the clustering a naive test would mistake for coupling); F with a forecast-gain trend and a storm predictability factor shared with W; A strongly severity-driven; quadratic severity terms not in C (misspecification); EMpre more likely for strong storms and long warning leads, and EMpre shortens Y_state (the procedural route); skewed (log-normal) lag noise rounded to whole days (ties); 10% of each predictor missing at random.
- **H4 effect:** coupling on the idiosyncratic part of A → Y_state with partial correlation r ∈ {0, 0.3, 0.5}. Reported: family-wise false-positive rate (any Holm rejection at r = 0) for the within-season null, the naive null, and with EMpre dropped; power = probability that the true pair is rejected after Holm; rate of a "no effect" reading at r = 0 and at r = 0.3.
- **H5 effect:** total residual decline Δ ∈ {0, 1, 2} (in noise SD) over the seasons, with severity-mix and forecast-gain trends present and lags depending on F, which C5 must absorb. Reported: false-positive rate and power.
- **Blind arm:** blind sizes (4), (6), (4, 4, 4), (4, 4, 4, 4, 4) after a known-history HU fit; r ∈ {0, 0.5}; assumes the true pair is the one selected (optimistic).
- **Runs:** 2,000 simulated studies per cell (Monte Carlo SE of a 5% rate 0.005), 999 permutations, seed 2026102923.
- **Criteria (fixed now):** a null is calibrated if its rate at r = 0 (or Δ = 0) is ≤ 0.060. A test is adequate if calibrated and its power at r = 0.5 (Δ = 1) is ≥ 0.80.
- **Expectations written now:** the naive null over-rejects (shared season shocks); dropping EMpre over-rejects for W pairs only weakly, since the effect runs through Y_state; within-season HU power at r = 0.5 is below 0.8 (about 18 within-season degrees of freedom) and HU+TS is near or above it; no "no effect" reading is reachable at HU size; H5 power at Δ = 1 is below 0.5 with nine seasons; the 2027-only blind arm has power below 0.5.

## 10. Result of the synthetic check and the event-set decision

**Decision rule (fixed now):** primary event set = HU if its H4 power at r = 0.5 is ≥ 0.80; otherwise HU+TS if HU+TS is calibrated and has higher power; otherwise HU, with the power stated in the first line of this file.

Single run, 29 Oct 2026, in Claude's workspace (not CI). Code `analysis/loop_power.py` (committed e4bb2ab before the run), output `analysis/loop_power_output.txt`. Evidence class: infrastructure (synthetic). Effect size r is the population partial rank correlation of the coupled pair given C (pooled), fixed by bisection on one large synthetic sample: raw coefficient 1.007 for r = 0.3, 1.885 for r = 0.5. (A 100-run smoke check with another seed, before the run, showed that a coefficient r/√(1−r²) gives a much smaller realized r; the calibration was added before the committed run.)

**H4 (6 pairs, Holm, within-season null):**

| Design | n | FPR (r = 0) | power r = 0.3 | power r = 0.5 | "no effect" read at r = 0 / r = 0.3 |
|---|---|---|---|---|---|
| HU | 27 | 0.022 | 0.27 | 0.60 | 0.000 / 0.000 |
| HU, 25% unmatched | ~20 | 0.026 | 0.14 | 0.32 | 0.000 / 0.000 |
| HU+TS | 54 | 0.004 | 0.79 | **0.99** | 0.035 / 0.015 |

Power counts rejections of the true pair; family-wise rejection is within 0.02 of it. Naive null: 0.024 (HU), 0.005 (HU+TS); EMpre dropped: 0.021, 0.007. All nulls are calibrated (≤ 0.060), and conservative (Holm over six correlated one-sided tests).

**Decision (rule above):** HU power 0.60 < 0.80, HU+TS calibrated with higher power → **primary event set = HU+TS** (§2: status HU or TS at a US landfall; `designatedIncidentTypes` containing H or 4). HU-only is reported as a secondary analysis with no weight.

**H5 (2 outcomes, Holm, 9 seasons):** FPR 0.033 (HU), 0.030 (HU+TS) with severity-mix and forecast-gain trends present (C5 absorbs them). Power at Δ = 1: 0.12 / 0.17; at Δ = 2: 0.26 / 0.41. **Not adequate at any size reachable before 2030**; registered and run, a non-significant result reads "not shown at this size".

**Blind arm (one pair, frozen fit):** FPR 0.016–0.030. Power at r = 0.5: one season of 4: 0.10; of 6: 0.32; three seasons of 4: 0.48; five seasons of 4: 0.68. 0.80 is not reached within five blind seasons of 4 (outside the grid; the pooled run's power is restated each December, §7).

**Expectations (§9) vs result:** held: HU power < 0.8 and HU+TS above it; no "no effect" reading at HU size; H5 < 0.5; 2027-only blind < 0.5. **Did not hold:** the naive null did **not** over-reject (0.024): in this synthetic world the shared season shock is too weak, after the year control and rank residuals, to create false coupling. So the run shows the within-season null is calibrated, but it does **not** show that it is needed; the clustering nuisance is under-stressed. Dropping EMpre also did not over-reject (expected only weakly). The "no effect" reading at the bound r = 0.3 occurs 1.5% of the time (≤ 0.05, as required).

**What this shows and does not show.** It shows the registered tests hold their false-positive rate in a world with severity confounding, nonlinearity, a procedural EM route, trends, skewed tied lags and missing links, and that only the HU+TS set gives H4 adequate power at r = 0.5. It does not show that r = 0.5 is realistic, that the planned sizes are right (unverified counts), or that the within-season null protects against stronger season clustering than simulated.

## 11. Sources

All opened in session 2.2 and listed with URLs and access dates in `docs/LOOP_DATA.md` §10; none opened in session 2.3. The Census Bureau boundary file (§2) and the MediaWiki redirect API (§3.3) are named here for 2.4 and are **unverified**.

## 12. Amendment 1 (pre-registered 29 Oct 2026, before its run): stressed season clustering

Why: §10 showed the within-season null calibrated but not needed (the naive null did not over-reject). This checks both under strong season clustering. Synthetic only; no change to §2–§8 or to `analysis/loop_power.py`; code `analysis/loop_power_amend1.py` imports its functions unchanged and sets the season-shock parameters; output `analysis/loop_power_amend1_output.txt`; seed 2026102924; 2,000 studies per cell, 999 permutations.

- Cells: KAPPA = 0.9 (shared share of the season shock); SIG_SEASON ∈ {1.5, 2.5}; designs HU and HU+TS; r = 0 (H4) and Δ = 0 (H5, with the §9 trends).
- Reported: H4 family-wise rate for the within-season and naive nulls; H5 rate.
- Criteria (as §9): calibrated if ≤ 0.060.
- Expectation written now: within-season ≤ 0.060 in every cell; naive > 0.10 at SIG_SEASON = 2.5 for both designs; H5 ≤ 0.060 (season is its unit).

## 13. Result of amendment 1, Claude's design error, and amendment 2 (pre-registered before its run)

**Amendment 1 result** (`analysis/loop_power_amend1_output.txt`, 2 min): H4 within-season 0.000–0.004, naive 0.000–0.001, H5 0.040–0.059. Expectation "naive > 0.10" did not hold.

**Diagnosis (Claude's error, in §9 and §12).** The shared season shock entered links and lags with the same sign, so it pushed r positive, opposite to the predicted (negative) direction; a one-sided test cannot be fooled by it. Neither run tested the clustering nuisance against the H4 test. The §10 false-positive rates stand as computed but say nothing about clustering in the predicted direction.

**Amendment 2.** Same as amendment 1, with the season shock entering the lags with sign −1 (a season with more attention, warning lead or skill also has shorter lags: the confound that mimics coupling). Implemented by a module constant `Y_SHOCK_SIGN` in `analysis/loop_power.py` (default 1 leaves the recorded run unchanged); code `analysis/loop_power_amend2.py`, output `analysis/loop_power_amend2_output.txt`, seed 2026102925. Cells: KAPPA 0.9; SIG_SEASON ∈ {0.7, 1.5, 2.5}; HU and HU+TS; H4 within-season and naive at r = 0; H4 within-season power at r = 0.5 (coefficient from §10, which was found with sign +1); H5 at Δ = 0.
Expectation written now: naive > 0.10 at SIG_SEASON ≥ 1.5; within-season ≤ 0.060 in every cell; H5 > 0.060 at large SIG_SEASON is possible (a season-mean trend test cannot separate a run of season shocks from a trend), which would be recorded as a limit of H5.

## 14. Result of amendment 2, diagnosis, and amendment 3 (pre-registered before its run)

**Amendment 2 result** (`analysis/loop_power_amend2_output.txt`): naive null 0.24–0.97 (expected). **Within-season null over-rejects under strong clustering**: 0.038 / 0.009 (HU / HU+TS) at SIG_SEASON 0.7, but 0.138 / 0.101 at 1.5 and 0.355 / 0.409 at 2.5 (criterion ≤ 0.060). Power at r = 0.5: 0.66–0.71 (HU), 0.99 (HU+TS). H5: 0.006–0.024, calibrated.

**Diagnosis.** §5's statistic takes mid-ranks over all storms and fits C pooled. With large season shocks, a season's storms sit in a tail of the pooled distribution where the rank transform compresses, so the severity slope differs by season; pooled linear controls leave severity confounding inside seasons, and since both a link and the lags depend on severity, r is biased in the predicted direction. The permutation is exact only if residuals are exchangeable within season, and this breaks it. The §5 statistic is therefore **not** calibrated under strong season clustering: it is replaced before any record is opened.

**Amendment 3 (replaces the §5 statistic; §5 nulls, Holm, PASS/FAIL rules unchanged).** rX, rY = OLS residuals of the **raw** X and Y on C without the year term **plus season fixed effects** (one dummy per season); r = corr(rX, rY); permutation within season as before. Equivalence n_eff unchanged (it already counts within-season degrees of freedom). Blind arm (§7): slopes of the known-history fit are frozen; blind residuals are demeaned within each blind season; statistic and null as §7. H5 (§6) unchanged (calibrated in amendment 2). Implemented as `STAT = "fe"` in `analysis/loop_power.py` (default `"rank"` reproduces the recorded run); the coupling coefficient is recalibrated for the new statistic.

Run: `analysis/loop_power_amend3.py`, output `analysis/loop_power_amend3_output.txt`, seed 2026102926, 2,000 studies per cell, 999 permutations. Cells: (a) the §9 world (Y_SHOCK_SIGN −1, KAPPA 0.5, SIG_SEASON 0.7): H4 designs HU, HU 25% unmatched, HU+TS at r ∈ {0, 0.3, 0.5}, and the blind-arm grid of §9; (b) stress: KAPPA 0.9, SIG_SEASON ∈ {1.5, 2.5}, HU and HU+TS at r = 0 and 0.5. Criteria as §9; the event-set rule of §10 is re-applied to (a).
Expectation written now: within-season ≤ 0.060 in every cell, stress included; power slightly below §10 (season dummies cost degrees of freedom); HU+TS still ≥ 0.8 at r = 0.5.

## 15. Result of amendment 3, the small-sample guard, and the final design

**Result** (`analysis/loop_power_amend3_output.txt`, 4.5 min). Coupling coefficient for the fe statistic: 0.709 (r = 0.3), 1.173 (r = 0.5).

| Cell | FPR (any, r = 0) | power r = 0.3 | power r = 0.5 |
|---|---|---|---|
| HU, §9 world | 0.051 | 0.18 | 0.40 |
| HU, 25% unmatched | **0.171** | 0.19 | 0.31 |
| HU+TS, §9 world | 0.006 | 0.39 | **0.80** |
| HU, stress (KAPPA 0.9, SIG 1.5 / 2.5) | 0.046 / 0.043 | — | 0.42 / 0.42 |
| HU+TS, stress | 0.004 / 0.005 | — | 0.79 / 0.76 |

"No effect" read on the true pair: HU never; HU+TS 0.045 at r = 0, 0.013 at r = 0.3 (≤ 0.05). Blind arm (frozen slopes, demeaned within blind season): FPR 0.013–0.026; power at r = 0.5: 0.08 (4), 0.24 (6), 0.38 (4,4,4), 0.49 (five seasons of 4).

**Expectations (§14) vs result:** stress now calibrated (held); power lower than §10 (held: season dummies cost degrees of freedom); HU+TS ≥ 0.8 at r = 0.5 held only just (0.804, MC SE 0.009; 0.76–0.79 under stress). **Did not hold:** within-season ≤ 0.060 in every cell: HU with 25% unmatched gives 0.171.

**Diagnosis (exploratory probe, 400 runs, seed 99, recorded in RECORD):** every pair over-rejects mildly (0.055–0.092 uncorrected); the within-season residual degrees of freedom (Σ (n_s − 1) − 5) have median 5 and are sometimes ≤ 0. With so few, residuals are not exchangeable within season.

**Guard (pre-registered now, decided from counts only).** In session 2.5, before any H4 statistic is computed: (1) for each pair, if Σ_s (n_s − 1) − 5 < 15 on its complete cases, that pair is not tested and reads "cannot be tested at this size"; (2) `analysis/loop_power.py` (STAT "fe", Y_SHOCK_SIGN −1) is rerun at the realized season sizes and missingness pattern (counts only); if its family-wise rate at r = 0 exceeds 0.060, H4 is not run and reads "cannot be tested at this size"; its power at r = 0.5 decides FAIL vs "not shown at this size" (§8.4).

**Final design (for 2.4 and 2.5):** event set **HU+TS** (§10 rule re-applied: HU 0.40 < 0.80; HU+TS 0.80); H4 statistic **§14**; nulls, Holm, equivalence, H5 (§6, calibrated in amendment 2: 0.006–0.024) and blind arm (§7 with §14 residuals) as registered; guard above.

**What this shows and does not show.** Shown: the final H4 test holds its rate, including under strong season clustering in the predicted direction, at the planned HU+TS size, and has power about 0.8 only for a strong coupling (r = 0.5). Not shown: that r = 0.5 is realistic (at r = 0.3, power 0.39); that the planned counts are right; robustness to confounds not simulated (state-level triggers, FEMA policy changes over time). §9's and §12's runs did not test clustering at all (Claude's sign error, §13); they stay on record.

## 16. Amendment 4 and the 2.4 build rules (session 2.4, 29 Oct 2026; committed before any 2015–2025 loop record was opened)

**Why.** Session 2.4 opened the header of the NHC individual-forecast error file before any data line of the split: header line 2 lists `OFCL` only, and every data line has 37 fields (one model: 11 track + 11 intensity errors). The verification page (`https://www.nhc.noaa.gov/verification/verify7.shtml`, opened 29 Oct 2026) says the files are *homogeneous with* best-track CLIPER5 and Decay-SHIFOR5, i.e. the sample is restricted, but the baseline errors are not tabulated. §3.2's F cannot be computed from this file. This is Claude's error in `docs/LOOP_DATA.md` §3 (session 2.2: "the baseline model's errors sit in the same lines", read from the format description without checking line 2), carried into §3.2. Decision (Adrian, 29 Oct 2026, 08:41, "BCD5 from ATCF", Claude's recommendation): amend §3.2 as below.

**Amendment 4 (replaces the baseline in §3.2; F's formula, sample rule and missing rule unchanged).**
- **Baseline source:** NHC ATCF archive a-decks, `https://ftp.nhc.noaa.gov/atcf/archive/YYYY/aalNNYYYY.dat.gz` (README of 8 Apr 2026 and the NRL a/b-deck format page opened 29 Oct 2026; §17 sources), technique `BCD5` (best-track CLIPER5/Decay-SHIFOR5, NHC's verification baseline). NHC's tech list describes BCD5 with the same wording as OCD5, which names forecast-time inputs rather than best-track ones; this conflict is recorded, not resolved.
- **BCD5 48-h track error** of the forecast with initial time t_i: great-circle distance (Earth radius 3440.065 n mi) between the a-deck `BCD5` record with DTG = t_i and TAU = 48 (first such line) and the HURDAT2 position at t_i + 48 h (exact time; missing if HURDAT2 has no record then).
- **F** = 1 − Σ OFCL 048hT01 / Σ BCD5 48-h error over the storm's error-file lines with initial time < t0, 048hT01 ≠ −9999 and a BCD5 error present; missing if the summed F048 of those lines is < 2 (as §3.2).
- **Intensity skill (recorded for 2.7, enters no test):** 1 − Σ |048hI01| / Σ |BCD5 VMAX − HURDAT2 wind at t_i + 48 h| on the same lines.
- **Method check before adoption (exploratory, outside the split):** for the eight 2014 a-decks AL01–AL08, the same code recomputed OFCL 48-h errors from the a-deck `OFCL` records and HURDAT2; on all 83 lines of the error file with 048hT01 present they match the file within 0.12 n mi (median difference 0.04), and a BCD5 48-h record existed for all 83. No 2015–2025 line was read.
- **Power:** F enters the synthetic world of §9 only as a generic per-storm predictor; the amendment changes no simulated quantity, so §15's power and false-positive rates stand.

**Amendment 5 (incident-type selection, §3.1; Adrian, 29 Oct 2026, 08:47, "Fallback on null", Claude's recommendation).** Found before any 2015–2025 record was opened, on records outside the split only: `designatedIncidentTypes` is null on 9,812 of 10,000 DR/EM records with incident begin 2000–2014 (all 753 records of Aug–Oct 2012, `incidentType` "Hurricane"), and filled on all 1,841 records of 2026, where it is a comma-separated code list (e.g. "2,F,T,W,Z"). `incidentType` values seen there include "Hurricane", "Tropical Storm", "Typhoon", "Coastal Storm". Rule: a record's type qualifies if `designatedIncidentTypes` is filled and one of its comma-separated codes is `H` (set HU) or `H`/`4` (HU+TS); or, if `designatedIncidentTypes` is null, `incidentType` is "Hurricane" (HU) or "Hurricane"/"Tropical Storm" (HU+TS). Where the field is filled, it decides as registered. The route used (code or fallback) is recorded per matched record and counted. This also settles the 2.2 open item: the hurricane `incidentType` string is "Hurricane" (seen outside the split; its use inside the split is recorded per event).

**Amendment 6 (baseline technique; Adrian, 29 Oct 2026, 08:55, answer "OCD5, all years" to Claude's recommended option).** Found after the a-decks of the event storms were fetched and before any F value or lag was computed or seen: `BCD5` TAU-48 lines exist for the 2015–2017 storms only (0 for every 2018–2025 storm); `OCD5` (CLIPER5/Decay-SHIFOR run on forecast-time inputs) is present in a-decks checked for 2016, 2017, 2018, 2019, 2020, 2022, 2024 and 2025. Claude's error: amendment 4 was checked on 2014 only. Rule: the baseline of amendment 4 is `OCD5` for every storm (one baseline across all seasons, so no step change in 2018 can mimic a trend); `BCD5` is not used. Everything else in amendment 4 is unchanged; its 2014 method check concerned the error computation, which is the same code.

**2.4 build rules (implementation of §2–§3 where they leave a choice; fixed now).**
1. **Files:** HURDAT2 `hurdat2-1851-2025-092326.txt` (the current file on 29 Oct 2026); error file `1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt`; a-decks of the event storms; Census `cb_2025_us_state_500k.zip` (latest vintage on 29 Oct 2026); OpenFEMA v2 records with `incidentBeginDate` 2015-01-01 to 2026-01-10; MediaWiki API on en.wikipedia; Wikimedia per-article pageviews (`all-access`, `user`, daily, as `scripts/refresh_open_data.py`); NHC GIS forecast-advisory zips (`al{NN}{YYYY}_5day_{adv}.zip`, intermediate advisories included). Each file's URL, access time and SHA-256 go in `data/loop_hurricanes/MANIFEST.json`.
2. **US entities:** Census `STUSPS` of the 50 states, DC, PR and VI (GU, AS, MP are not Atlantic and are dropped). Distance to a polygon = minimum great-circle distance to its boundary segments (local equirectangular approximation per segment). Census states these generalized files are not for precise area relationships: a stated limit, which the 50-km rule absorbs.
3. **Qualifying landfall record:** a HURDAT2 line with identifier `L`, status `HU` or `TS`, in a storm with ATCF year 2015–2025, assigned to a US entity. **t0** = earliest; **k** = its entity. **hu_set** = 1 if any qualifying record has status `HU`; **hu_t0**, **hu_state** recorded for the secondary analysis.
4. **R64:** maximum of the four 64-kt radii of the t0 line; −999 or status TS → 0 (as §2), with a flag when −999 was replaced.
5. **FEMA dates:** the calendar date of the ISO string (UTC). **Name rule:** HURDAT2 storm name, whole word, case-insensitive, in `declarationTitle`. **Ambiguity rule (§3.1):** "another event's landfall in k within ±10 days" = any qualifying landfall record (rule 3) of another table storm assigned to k whose date is within ±10 days of date(t0). **DR choice:** earliest declaration date, ties by lowest `disasterNumber`. A DR with no request date leaves Y_state and Y_fed missing (exclusion "DR request date missing"). `region` from the chosen DR. Every matched record's `incidentType` string is recorded.
6. **Attend:** titles T1–T3 built from the HURDAT2 name in title case; one MediaWiki query (`action=query`, `redirects=1`, `prop=pageprops|info`) per storm; a title exists if not `missing`; disambiguation = `pageprops.disambiguation` present; creation date = timestamp of the target's earliest revision. Days = the three UTC dates before date(t0).
7. **W:** advisories listed on the NHC GIS archive page of the storm; issuance = `ADVDATE` (yymmdd/hhmm, UTC; documented in the zip's FGDC metadata, and checked as UTC against the local-time label on a 2014 file); the earliest advisory by issuance whose `*_ww_wwlin` layer has a record with `TCWW` in {TWA, TWR, HWA, HWR}. If `ADVDATE` cannot be parsed, §3.4's fallback applies and the event lists it.
8. **Exclusions:** every missing value carries one reason from a fixed list in `data/loop_hurricanes/README.md`, per event and per link.
9. **Outputs allowed in 2.4:** the table, the exclusion list, realized season sizes and per-link non-missing counts. No lag correlation, trend, link-to-link statistic, H3 binomial test, H4 or H5 statistic.

## 17. Sources opened in session 2.4 (documentation, 29 Oct 2026)

- US Census Bureau, Cartographic Boundary Files – Shapefile: https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html ; technical description: https://www2.census.gov/geo/tiger/GENZ2025/description.pdf ; file-name definitions: https://www2.census.gov/geo/tiger/GENZ2025/2025_file_name_def.pdf
- MediaWiki API:Query (redirect resolution, `redirects`, `missing`), archived copy of 26 Dec 2016: https://webarchive.library.unt.edu/web/20161226084947/https://www.mediawiki.org/wiki/API:Query . The current page (mediawiki.org) and the en.wikipedia API help could not be opened from Claude's workspace (HTTP 429, Wikimedia rate limit); the current API help is saved by the 2.4 fetch job (`data/loop_hurricanes/sources/wiki/api_help.json`).
- NHC verification page: https://www.nhc.noaa.gov/verification/verify7.shtml ; error file header: https://www.nhc.noaa.gov/verification/errors/1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt (header lines only before this section was committed; 2014 lines for the method check).
- NHC ATCF archive README (8 Apr 2026): https://ftp.nhc.noaa.gov/atcf/archive/README ; tech list: https://ftp.nhc.noaa.gov/atcf/docs/nhc_techlist.dat ; NRL a/b-deck format: https://science.nrlmry.navy.mil/atcf/docs/database/new/abrdeck.html
- NHC GIS forecast archive: https://www.nhc.noaa.gov/gis/archive_forecast.php ; FGDC metadata inside `al012014_5day_001.zip` (2014, outside the split).
