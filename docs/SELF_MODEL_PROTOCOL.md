# Self-model protocol: H8 (session 3.5, 30 Oct 2026)

**Power below 0.5 is possible and this test runs anyway:** if the AI captures only half of what hazard, stage and time do not explain, power is 0.31 at 60 forecasts and 0.56 at the target of 120 (§7). Then a non-PASS reads "not shown at this size", never "no effect".

Serves **H8** (`docs/PLAN.md` §0.2): AI forecasts of response outcomes, committed before the outcome, beat both a naive base rate and a simple statistical model (Brier score). Evidence class of the rules, code and synthetic power: **infrastructure**. Evidence class of the §6 test when scored: **pre-registered blind** (no forecast exists and no eligible event has happened when this file is committed). Rules: CLAUDE.md 3.0, self-model rules (a)–(e). Decision of 30 Oct 2026, 07:57 (`docs/STATUS.md`): EMO calls the model; the paid-service choice is Adrian's in session 3.6.

**Registered before any forecast and before any stream record or aggregate was opened.** Claude does not hold `EMO_STREAM_KEY`; this session opened no record of `data/stream/` and did not open `data/mirror/aggregates.json`. Code: `emo/selfmodel/protocol.py` (every constant is part of this protocol). Tests: `tests/unit/test_selfmodel.py` (synthetic). Power: `analysis/selfmodel_power.py`, output `analysis/selfmodel_power_output.txt`. Card rules, statuses and windows: `docs/LOOP_CARD_PROTOCOL.md` §2–§7, unchanged.

## 1. What the self-model is, and is not

Two outputs per forecast (STRATEGY_3_0 §3, pillar 5):

- **(a) What humanity will do:** a probability that a response rung is reached within its window. Only (a) is scored.
- **(b) What a coherent whole that knows what humanity knows would do:** one sentence. Never scored. Wherever shown, it carries the label "a normative model: one AI model's view, not a measurement and not a recommendation" (rule (e)). It is stored with the ledger and is not shown before cards are public under the reuse terms (STREAM_DATA §11).

No output is presented as humanity's decision, as a recommendation to act, or as a substitute for human judgment (rule (a)).

## 2. What is forecast, and when

Per open card (LOOP_CARD_PROTOCOL §2), at most once per (card, target), at the earliest daily run where the target is eligible:

| Target | Eligible when | Outcome = 1 if | Window |
|---|---|---|---|
| **D** decision | rung D "not yet" | a CEMS activation (non-EU27) or an IFRC GO appeal (DREF or Emergency Appeal) is recorded, its rung time after the forecast and within the window | onset + 60 days |
| **B** money | rung D present, rung B "not yet" | a DREF or `amount_funded` > 0 is recorded, its rung time after the forecast and within the window | earliest decision + 60 days |

A card is eligible only if: not EU27 (E1); anchored by a hazard record; onset ≥ **31 Oct 2026 00:00 UTC** and < **1 Dec 2027**; earliest seen by EMO on or after 31 Oct 2026; not closed; window not yet ended. Forecasting stops at the **120th** forecast (`N_TARGET`) or after onsets of 30 Nov 2027, whichever comes earliest. No other selection: every eligible (card, target) is forecast; none may be skipped by hand.

## 3. What is sent to the model (the only data that leave the Action for this test)

Exactly the `payload()` fields: hazard class; ISO3 country codes; stage so far (label); statuses of rungs W, R, D, B; decision systems present (CEMS, IFRC); days since the reference (onset for D, earliest decision for B); days left in the window. **No** identifier, title, name, date, alert value, amount, coordinate or source record (test `test_payload_has_no_identifier_title_or_date`). The prompt is fixed (`SYSTEM_PROMPT`, `USER_TEMPLATE`, `QUESTIONS`, version `h8-v1`, hash `prompt_sha256()`); no tools, no web access, no earlier forecast or outcome in the prompt (each call is stateless). Temperature 0 where the API accepts it; the setting used is recorded.

This extends LOOP_CARD_PROTOCOL §11 for H8 only: the payload goes to the model provider and nowhere else; ISO3 codes are included because they are the only information the model can know beyond the statistical baseline (without them H8 would compare one model's prior against a fit on the same three features). **This choice is open to Adrian until any forecast is committed** (§9).

## 4. Forecast ledger (committed before the outcome)

Written inside the Action by the 3.6 caller, one row per forecast, `ledger_row()` with fields: `forecast_id` (keyed hash of card and target, not reversible without the key), `card_id`, `target`, `forecast_utc`, `window_end_utc`, `cluster`, `payload`, `prompt_version`, `prompt_sha256`, `model_requested` (the model string sent), `model_returned` (the model string in the API response), `response_id`, `response_text`, `p_ai`, `coherent_whole`, `p_base`, `p_logit`, `baseline_train_n`, `protocol_sha256` (SHA-256 of this file at run time), and `row_sha256` over all of them.

- **Encrypted file** per run (same key and method as the stream log, `emo/stream/store.py`), committed under `data/selfmodel/ledger/`.
- **Public index** `data/selfmodel/ledger_index.csv`, one line per run: run time, number of forecasts, `run_digest()` (hash of the sorted row hashes), SHA-256 of the encrypted file, model requested and returned, prompt hash, protocol hash. No per-forecast line (§11 of the card protocol: no date of a single event leaves).
- The git commit of the run, before any outcome can be known, is the timestamp. Baseline forecasts are written in the same row, so they are pre-committed too.
- An unparseable, refused, or failed AI answer is kept in the ledger with `p_ai` empty and **scored as 0.5**; it is never dropped or retried after the run.

Model name and version: chosen in 3.6 (Adrian's decision). The same model string is used for every forecast; a change of model (e.g. a retired version) is recorded with its date, and the test is then reported per model as well as pooled.

## 5. Baselines (rule (d))

Both are fitted inside the Action at forecast time, separately for D and B, on **training rows**: earlier cards of the stream (any onset since the stream began, non-EU27, anchored) whose target was eligible at their earliest daily run and whose outcome (§6 rule) was known before the forecast time. Features of a training row are taken at its own earliest eligible run.

1. **Naive base rate:** (k + 0.5) / (n + 1) over the training rows; 0.5 with none.
2. **Statistical model:** logistic regression with an intercept, hazard indicators (hazards with < 5 training rows pooled with the reference), stage so far ≥ 2, and log(1 + days since the reference); ridge penalty 1.0 on all but the intercept; Newton's method (`fit_logistic`). With < 20 training rows or < 5 of either outcome, it falls back to the base rate.

## 6. Outcome and score (rules (b), (c))

- **Outcome by code only**, from IFRC GO and CEMS records through `emo/stream/cards.py` at the scoring date (`outcome()`): 1, 0, or excluded. Excluded for all three forecasters alike: rung "missing", "withheld" or "no source"; still "not yet"; rung time at or before the forecast time (the outcome existed but was not yet in the stream). The AI's text, files coded by an AI, and the coherent-whole sentence are never read by the scorer. The AI never scores itself.
- **Brier score** (p − y)² per forecast; AI unusable answers at 0.5.
- **Statistic:** gain over a baseline = its Brier − the AI's Brier, per forecast. Dependence: forecasts are grouped in clusters (ISO3 set, hazard, onset month; LOOP_CARD_PROTOCOL §9), and both targets of one card share its cluster.
- **Tests:** for each baseline, a one-sided sign-flip test on the cluster sums of the gain (exact up to 15 clusters, else 10,000 random flips). **PASS** if both p < 0.05 (both must hold, so no correction is needed: intersection–union). **FAIL** if the one-sided 95 % cluster-bootstrap upper bound of the mean gain over the statistical model is below **0.01** Brier (fixed equivalence margin: the AI adds less than 0.01). Otherwise **"not shown at this size"**. **"Not testable at this size"** if < 30 scored forecasts or < 20 clusters. Both conditions that can make a PASS are significance tests; no point comparison decides.
- **Once only:** `may_score()` allows scoring when every window has closed (+7 days for late records) and either 120 forecasts exist or the date is ≥ 1 Apr 2028. Before that, the Action commits only the ledger index; no interim Brier is computed or committed.
- **What leaves the Action at scoring:** n, clusters, the three mean Brier scores, the two gains, p-values, the upper bound, the number of unusable AI answers, and the verdict; per model if the model changed. No outcome of a single event.

## 7. Power (synthetic; `analysis/selfmodel_power_output.txt`)

Model: true logit = hazard + stage + time terms + u, where u (sd 1, 30 % shared within a cluster) is what those features do not explain; clusters of 1 + Poisson(0.25); baselines fitted on 150 earlier forecasts; 600 replications per cell (2,000 flips and bootstraps for speed; the scorer uses 10,000).

| AI scenario | n = 30 | 45 | 60 | 90 | **120** |
|---|---|---|---|---|---|
| null: exchangeable with the statistical model (false PASS) | 0.025 | 0.018 | 0.032 | 0.020 | **0.030** |
| knows the structure, none of u (false PASS) | 0.040 | 0.033 | 0.037 | 0.025 | **0.037** |
| knows half of u (PASS) | 0.21 | 0.27 | 0.31 | 0.48 | **0.56** |
| knows 0.8 of u (PASS) | 0.32 | 0.45 | 0.52 | 0.71 | **0.79** |

FAIL under the null: 0.11–0.24 (it rises with n); FAIL when the AI knows half of u: ≤ 0.005. **Expected size:** STREAM_DATA §4 estimates 8–15 linked events a month before EU27 removal; D and B forecasts arise only on warned cards without a decision and on decided cards without money, so about 4–10 forecasts a month are expected (an estimate, not a count). Over the 13 months to the onset limit that gives about 50–130: the target of 120 is reached only near the upper rate; otherwise the test runs at the size reached (at 50, power is about 0.3 in the half-of-u case). These numbers depend on the assumed size of u, which no one knows; that is why the earliest line states the low-power case.

## 8. Contamination and circularity rules

1. No EU27 card is forecast, sent, trained on or scored (E1). The payload is the §3 list and nothing else.
2. Only cards with onset on or after 31 Oct 2026 and seen by EMO only from that date count (rule (b)); training rows may be older because they are fitted by code and never shown.
3. The AI never scores itself; outcomes come from IFRC/CEMS records by code (rule (c)).
4. No forecast is written by hand or in a chat session: in-session forecasting would show Claude per-event card state, which the stream rules forbid (Claude holds no key). Forecasts come only from the Action.
5. Prompts are stateless: no earlier forecast, outcome or score is sent to the model. Model knowledge cutoffs precede the events, and forecasts precede outcomes, so training data cannot hold the outcome.
6. No interim look: no Brier, calibration or hit count is computed on scored-so-far forecasts before `may_score()` is true.
7. The mirror page shows counts only (number of forecasts committed, last ledger run); no forecast value is public before scoring.

## 9. Allowed amendments

Before any forecast is committed (session 3.6), a dated section here may change the §3 payload (e.g. drop ISO3) or the prompt wording, with the power unchanged or rerun. After any forecast: none, except recording a forced model change (§4).

## Sources

No external source was opened in this session. Repository files used: `CLAUDE.md` 3.0, `docs/STATUS.md` (decision 30 Oct 07:57; session 3.4), `docs/STRATEGY_3_0.md` §3–§5, `docs/LOOP_CARD_PROTOCOL.md`, `docs/STREAM_DATA.md` §4, `docs/PLAN.md` (H8, 3.5), `emo/stream/cards.py`.
