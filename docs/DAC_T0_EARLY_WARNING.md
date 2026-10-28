# Earlier-warning t0 for the EU files (session 10b)

Applies one alternative t0 rule, unchanged, to `data/dac_mpox/EU.json` and `data/dac_ppe/EU.json`. Committed 2026-10-28 **before any new source was opened**. Reason (session 10): every EU mpox response precedes the WHO PHEIC, so the PHEIC is not the warning the EU answered.

## 1. Rule (both cases, unchanged)

- **Early-warning t0:** the first risk assessment for the hazard published by ECDC: the earliest ECDC publication on the hazard whose own page or document calls it a rapid risk assessment or a threat assessment brief. Epidemiological updates, news items and the Communicable Disease Threats Report are not risk assessments.
- **Fallback** (only if no such ECDC publication can be opened or dated from an ECDC record): WHO's first Disease Outbreak News item on the hazard, from WHO's own page.
- **Date:** the publication date stated on ECDC's (or WHO's) own record. Exact if the record gives the day; otherwise window over the stated period with the wording. If the page date and the document date differ, both are readings.
- **Tie:** two qualifying publications on the same day → one event, both cited.
- **Coding:** one `context` row per file, listed in `case.alternative_t0`; primary source only (URL, access date, sha256 or page text); dating phrase tested.

## 2. Not chosen to fit the result

The rule is fixed before the dates are checked and is applied to PPE as well. If under it the mpox order or delivery lag is still negative (or the PPE lags change in any direction), that is reported as is: no second, earlier t0 is searched for in this session, and the conclusion would be that the EU responded to a signal earlier than ECDC's first risk assessment.

## 3. What Claude knows before opening the sources (both cases are known history)

From general knowledge, not checked: for mpox, WHO's first Disease Outbreak News on the UK cases was in mid-May 2022 and ECDC published a rapid risk assessment around 23 May 2022 (an epidemiological update a few days earlier), which would make the first EU order (14 June) and delivery (28 June) positive by roughly 3–6 weeks. For COVID-19, WHO's first Disease Outbreak News was 5 January 2020 and ECDC published a threat assessment brief or risk assessment in early-to-mid January 2020, i.e. a few weeks before the PHEIC (30 January). **Every result here is "pre-registered on known history".**

## 4. Computation and what is reported

- `scripts/dac_t0_alternative.py`: loads a committed file, in memory sets `case.t0_event_id` to the early-warning row, relabels that row `validation` and the PHEIC row `context` (and swaps them in `alternative_t0`), validates, computes the profile with `emo/dac_standard.py`, writes `data/<case dir>/EU_profile_t0_early.json`. The committed event files and main profiles are not changed (their tests must still pass).
- Reported per case as a profile: lag from the early-warning t0 to the first firm order, binding act and delivery (`{min_days, max_days}`), plus the paired and unpaired intervals the profile already gives (unchanged by t0). No pass/fail, no scalar, no cross-case score.
- **Known limit, flagged in the report:** windows in the PPE files whose lower bound was set at the PHEIC by an earlier rule (`date_earliest` = 2020-01-30 without a source) are kept as coded; any such row affecting an EU first event is named.
- What could not be dated or opened is listed here in §5.

## 5. Sources opened and result

(Filled after coding; dated.)
