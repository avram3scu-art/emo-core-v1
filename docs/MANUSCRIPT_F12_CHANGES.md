# Manuscript "Decision or Supply?": argument rewrite (fix session F12, 28 Oct 2026)

- **Base:** `docs/sources/dac_paper/Decision_or_Supply_manuscript_F9_revised.docx` with its F9 tracked changes accepted (in the XML: deletions removed, insertions kept). Checked: the accepted base gives the same text as pandoc's accepted view of the F9 file.
- **Output, with F12 tracked changes only (author "Claude"):** `docs/sources/dac_paper/Decision_or_Supply_manuscript_F12_revised.docx` (text copy `…_F12_revised.md`)
- **Made by:** `scripts/manuscript_f12_edits.py`
- **Validated:** against the accepted base; schema checks pass and every edit is tracked (+5 paragraphs: one reference and one table row of four cells).

Scope: review F10 points 2, 3, 4, 5 and 8, as set by Adrian's F12 prompt. No new numbers. The identification result (§2.2) and the numerical results of §4.2 (slopes, sums of squares) are unchanged.

Sources:

- **X:** `analysis/dac_ppe_crosscase_output.txt` §1 (case windows: BE 46, DE 41–50, NL 51–52, SE 47–61, hence days 41–61)
- **L:** `docs/LIT_SEARCH_F11.md`
- **OAG:** `data/sources/lit/OAG_Canada_2021_Report10.txt` (Exhibit 10.7; fetched by `scripts/fetch_lit_sources.py`, sha256 8720d449…)
- **S:** the search of the committed Belgian sources (Annex 5, hearings K022 and K040, report pp. 270–285) for a proposal of either rival, run in F12: no hit for administrative or procedural slowness, nor for waiting for EU joint procurement (patterns in the record row).

## Changes

| # | Where | Before | After | Reason | Source |
|---|---|---|---|---|---|
| 1 | §1, para. 4 (after the NAO sentence) | — | adds the Auditor General of Canada: 39 contracts paired with their first delivery; 34/28 days request to contract, 71/57 days contract to first delivery (N95/gowns); averages cannot show whether earlier ordering would have helped | novelty (point 4); a second country where the supplier part dominated | OAG Exhibit 10.7; L §2.1 |
| 2 | §2.3 | "None is designed to link each order to the delivery of that same order from records" | only an audit has linked contracts to their deliveries, as averages; none uses the spread of order dates across paired orders of one good | the claim is narrowed to the test | L §3 |
| 3 | Table 1 | — | new row: Auditor General of Canada (2021) | closest approach | OAG; L §2.1 |
| 4 | References | — | Auditor General of Canada (2021) | new citation | OAG |
| 5 | Abstract | first deliveries "within 5–11 days … orders 2–16 / 31–49 days apart" | every import-dependent first delivery between days 41 and 61, inside the export surge; unpaired dates cannot show whether supply set that timing | holds under every reading (point 3) | X §1 |
| 6 | §1, para. 5 | same claim as #5 | same as #5 | as #5 | X §1 |
| 7 | §4.3, para. 1 | deliveries "5–11 days apart, while … orders 2–16 … 35–49 days apart" | deliveries per case incl. Sweden; all between days 41 and 61, inside the surge (days 31–66) | as #5 | X §1; manuscript §3.1 (export surge) |
| 8 | §4.3, para. 1 | France's window "does not place it before Germany's or Belgium's" | removed (France 39–52, most plausibly from stock) | drop the "France first" framing | P (FR) |
| 9 | §5, para. 1 | "cross-case pattern … is what a common supply constraint would produce; under reading B …" | every first delivery between days 41 and 61, inside the surge (rest of the paragraph, unpaired, unchanged) | as #5 | X §1 |
| 10 | §5, para. 3 | France "delivered from day 39, although its window does not establish that it delivered first" | France "delivered from day 39" | as #8 | P (FR) |
| 11 | §8 | "first deliveries … within days of one another, and orders were more dispersed only under some readings" | every import-dependent first delivery between days 41 and 61, inside the surge; unpaired dates cannot test a supply constraint | as #5 | X §1 |
| 12 | Abstract | "rejects a delay common … also rejects waiting for European joint procurement" | bounds any common delay at five days; the first Belgian order preceded the end of the first joint call | M0 not shown proposed; EU rival not shown proposed (point 2) | S; Table 3 |
| 13 | §1, para. 5 | "rejects a delay common … rejects waiting for European joint procurement" | bounds any common delay at five days; the first order preceded the end of the joint call | as #12 | S |
| 14 | Table 4, row 1 verdict | "Rejected; any common component is at most 5 days" | "Bounded: any common component is at most 5 days" | as #12 | S |
| 15 | Table 4, row 9 verdict | "Rejected" | "Not supported: the pattern is absent, and the explanation was not found proposed in the sources" | as #12 | S |
| 16 | §4.2, verdict terms | "Verdicts use five terms:" | six terms, adding "bounded" | forced by #14 | — |
| 17 | §4.2, para. after Table 4 | "two are rejected, one is not supported … excludes a delay common … excludes waiting for joint procurement" | "one is bounded, two are not supported …"; bounds the common delay; the first order did not wait | forced by #14–15 (counts: bounded 1, not supported 2, consistent 2, unidentified 5, present 1) | Table 4 |
| 18 | §5, para. 2 | EU rival "is rejected for Belgium and the Netherlands … cannot be tested for Germany and Sweden" | not found proposed; pattern absent in Belgium, the Netherlands and Sweden (first orders before day 42), cannot be checked for Germany (window 29–50) | as #12; Sweden now dated to February | S; X §1 |
| 19 | §6.1 | "The delay was not a property of the purchasing service … not caused by waiting for the EU" | any service delay at most five days; the first order did not wait for the joint call | as #12 | S |
| 20 | §8 | "rejects a delay common … rejects waiting" | bounds the common delay at five days; the first order did not wait | as #12 | S |
| 21 | §7 Coding | "no human has yet recoded them" | the author's check of each coded date against its source is pending; no human has recoded them | point 4 of the prompt: Adrian's check not reported as complete | STATUS (F10) |
| 22 | §7 Explanations | "search covered the approaches in Table 1 …; a systematic search … was not made" | covered audits, reports, reviews and open procurement data by web search; Scopus, Web of Science and Google Scholar not searched | point 4 | L (method) |
| 23 | Table 3, order 1 | "34 (reading A: 1; option reading: 5)"; "23 (reading A: 56; option reading: 52)" | "34 (reading A: 1)"; "23 (reading A: 56)" | option reading moved to the note (point 8) | P (BE) |
| 24 | Table 3 note | — | option reading: order 1 on day 5, paired lag 52 | as #23 | P (BE) |
| 25 | Table 5, Belgium | cells with "option" values | "34 (A: 1)", "12 (A: 45)", "23 (A: 56); five orders 5–23" | as #23 | P (BE) |
| 26 | Table 5 note | "Option: the third reading …" | option reading: order day 5, unpaired 41, paired lag 52 | as #23 | P (BE) |

## Before submission (not changed here)

- **Declarations:** "All AI-assisted outputs, including every date, figure and reference, were verified by the author." This must be true before submission: Adrian's check of the coded dates is pending (§7 now says so). The wording follows Adrian's three-point form (CLAUDE.md) and is his to keep or change.
- **Figures 1–2:** to be redrawn (F13).
