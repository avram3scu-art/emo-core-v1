# Synergy on real streams — pre-registration (session 8)

Adrian N. Avramescu. Committed before any of the data below was fetched or opened.

## 1. Question

Does `emo/synergy.py` (Gaussian O-information, Ω; synergy index S = −Ω, in bits) find
higher-order structure among three real streams of one domain that a surrogate null,
which keeps each stream's own autocorrelation but breaks their alignment, does not?

Session-1 status claimed "synergy passes noise controls". That rests on synthetic tests
(`tests/unit/test_synergy_controls.py`). This is the first run on real streams.

## 2. Domain and streams

Domain: climate change. Window: monthly, January 2016 to December 2025 (T = 120 months;
pageview data start July 2015, so 2016 is the first full year).

| Stream | Column | Source and exact query | Count per month |
|---|---|---|---|
| Science | `science` | OpenAlex works API: `filter=title_and_abstract.search:"climate change",type:article,from_publication_date:<first day>,to_publication_date:<last day>`; `meta.count` | articles published that month |
| Policy | `policy` | Federal Register API `documents/facets/monthly`, `conditions[term]="climate change"`, `conditions[type][]` = RULE, PRORULE, PRESDOCU, publication dates 2016-01-01..2025-12-31 | dated US federal acts (rules, proposed rules, presidential documents) mentioning the phrase |
| Attention | `attention` | Wikimedia pageviews API, per-article, en.wikipedia, all-access, agent `user`, monthly; titles `Climate_change` + `Global_warming`, summed | English Wikipedia views |

The two titles are summed because "Global warming" was the main article until a page
move to "Climate change" in 2019 (from memory, not verified); views of a redirect title
are counted under that title, so the sum keeps one attention stream across the move.

Fetched by the GitHub Action (`one_off.yml`, job `synergy-climate`) into
`data/sources/synergy_climate/` with `SOURCES.json` (URL, download time, SHA-256).

## 3. Transform (fixed before data)

For each stream c_t: y_t = ln(c_t + 1); e_t = residual of an OLS fit of y_t on an
intercept, a linear time trend and 11 month-of-year dummies. The residuals e_t of the
three streams are the input. Reason: shared growth and shared seasonality (and the
OpenAlex habit of dating year-only records to 1 January) would otherwise make any three
counts look redundant.

## 4. Statistic and null

- Observed: S_obs = `compute_gaussian_synergy(E).synergy_index`, E = 120 × 3 residuals,
  columns (science, policy, attention), default ridge.
- Null: circular shifts of `policy` by s2 and `attention` by s3 months (`science` fixed),
  s2, s3 ∈ {12, …, 108}, with circular distance between s2 and s3 ≥ 12 (so no pair of
  streams keeps its alignment). Every admissible (s2, s3) pair used once; N_null reported.
- p_syn = (1 + #{S_null ≥ S_obs}) / (1 + N_null); p_red = (1 + #{S_null ≤ S_obs}) / (1 + N_null).

## 5. Verdict rule

- **PASS** (synergy on real streams): p_syn ≤ 0.025.
- **FAIL — redundancy-dominated**: p_red ≤ 0.025.
- **FAIL — no higher-order structure distinguishable from the null**: otherwise.

Two tails at 0.025 each, so either sign is a recorded outcome. Run once.

## 6. Reported without weight on the verdict

Total correlation (TC) against the same null (upper tail); the three pairwise residual
correlations; Ω and TC on the untransformed ln(c + 1) series (to show how much a raw
analysis would be driven by shared trend).

## 7. Failure modes fixed in advance

- A stream with a missing month, or any fetch error: test not run; recorded as such.
  Exception (added before data, with the code): a month absent from the Federal Register
  monthly facet means zero documents, not missing data; it is set to 0 and the number of
  such months is reported.
- A code fault that stops the run before S_obs is computed may be fixed once; the failed
  run and the fix are recorded. No change to §2–§5 after data are opened.

## 8. Known limits

- Gaussian, stationary approximation; residuals may keep slow drifts (e.g. changes of US
  administration in 2017, 2021, 2025 in `policy`). The circular-shift null keeps each
  stream's own drift, but with T = 120 shifts of a slow drift are not independent.
- Policy is US-only; science and attention are global/English. One domain, one window.
- OpenAlex counts for recent months are still being indexed (drift seen in session 2).
- A PASS shows structure beyond aligned noise in one domain, not that EMO's "emergent
  mind" reading of synergy is right.

Code: `scripts/fetch_synergy_climate.py`, `analysis/synergy_climate.py`; Action
`one_off.yml`, job `synergy-climate`, run with `commit` on. Checked before data on random
fake inputs only (no structure found, as expected).

## 9. Runs

- Run 40283263805 (code b27400e): FAILED at fetch. OpenAlex returned HTTP 429 (rate limit)
  at month 2024-05; nothing was saved, no value was seen, S_obs was not computed
  (record 6b3aa09). Fix used once under §7: one-second pacing between OpenAlex calls,
  polite-pool `mailto`, longer retries. No change to §2–§5.

- Run 40283537981 (code 213d3ef): FAILED at fetch, identically. HTTP 429 again at 2024-05
  (the 101st of 120 OpenAlex calls) after 8 retries over ~18 min; nothing saved, no value
  seen, S_obs not computed (record 6f20bdb). Stopping at the same call in both runs
  suggests a per-client cap on OpenAlex search queries, not a burst limit (inference,
  not verified).

## 10. Result

**Not run.** Under §7 the one allowed fix is used and the fetch still fails, so the test
was not run. No data of the three streams has been opened; §2–§5 remain valid and blind.

To run it, a further fetch fix needs Adrian's decision (it goes beyond §7): e.g. an
`OPENALEX_API_KEY` secret, or spreading the 120 calls over two days. The design (§2–§5)
would stay unchanged; the amendment would be recorded here before the new run.
