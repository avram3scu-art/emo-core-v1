# Manuscript "Decision or Supply?": data-only revision (fix session F9, 28 Oct 2026)

- **Original (unchanged):** `docs/sources/dac_paper/Decision_or_Supply_manuscript_anonymised.docx`
- **Revised, with tracked changes by "Claude":** `docs/sources/dac_paper/Decision_or_Supply_manuscript_F9_revised.docx` (text copy with changes accepted: `…_F9_revised.md`)
- **Made by:** `scripts/manuscript_f9_edits.py`, which holds every change. The edit stays in that one reproducible script, so no change exists only in the .docx.

Scope (Adrian's prompt for F9): every number and data claim must match the six event files in `data/dac_ppe/` and the data statement in `docs/DAC_PPE_COMPARISON.md` §5. The argument, Table 4 and the target journal are not changed. Sources of values:

- **P:** the profiles `data/dac_ppe/<case>_profile.json`
- **X:** `analysis/dac_ppe_crosscase_output.txt` (sections 1–7), written by `analysis/dac_ppe_crosscase.py` (exploratory; its search is checked against brute force in `tests/test_dac_ppe_crosscase.py`)
- **C:** `docs/DAC_PPE_COMPARISON.md`
- **R:** `docs/DAC_PPE_CODING.md` §5 (rules and added sources)

## Changes

| # | Where | Before | After | Reason | Source |
|---|---|---|---|---|---|
| 1 | Abstract | first deliveries "within six days of one another although first orders were weeks apart" | BE/DE/NL deliveries within 5–11 days; orders 2–16 days apart (reading B) and 31–49 (other readings) | DE delivery now 41–50, NL 51–52; order spread recomputed | X §2, §3 |
| 2 | §1, para. 5 | same claim as #1 | same as #1 | as #1 | X §2, §3 |
| 3 | §3.1 Belgium sources | Annex 5 and hearings | adds the Moniteur belge for the first binding act | binding act now from the decree of 23 Mar 2020 | R (Belgium e); C §3 |
| 4 | §3.1 Sweden sources | SOU 2021:89 | adds SOU 2020:80 for first deliveries | delivery lower bound from SOU 2020:80 p. 206 | R (Sweden i) |
| 5 | §3.1 Germany sources | Bundestag answers, TRIS, one press report | adds the BMG report (4 Apr 2020) and the Bundesrechnungshof report (2025); press report "for context only" | new sources narrow order and delivery; the press report is secondary | R (Germany e); DE.json |
| 6 | §3.1 first-order rules | Germany: window closing at first delivery; Sweden: undated, window opens at t0 | Germany: window under two readings (9 Mar per audit; mid-March per ministry); Sweden: February ("minor purchases"); month-part convention stated | new coding | R (Germany e c, Sweden a, Germany e a) |
| 7 | §3.1 end | — | coder (an AI model, Claude), automatic phrase checks, evidence class: coded dates and lags are a test on known history; cross-case statistics are exploratory | CLAUDE.md evidence-class rule | `docs/DAC_PPE_CODING.md` §1 |
| 8 | §3.2 | "both an order date and a first-delivery date" | "both an order date and a first delivery"; the national producer's delivery is coded censored | delivery after the observation window | BE.json (row 742); C §2 |
| 9 | Table 2 | counts 18/12/14/14/12/21 (total 91), etc.; source column for BE, DE, SE | new counts per file (total 115 / 114 / 1 / 16 / 87); sources updated; order file 10 rows (8 orders), 2 undated, 6 paired with a dated delivery | new event files | X §7; BE_orders.csv |
| 10 | Table 2 note | exclusion rule of the old files; "two readings, hence nine rows" | new definitions; "three readings … ten rows" | new files | X §7 |
| 11 | §4.1 | readings A and B only | adds the 4 February "option sur/commande" as the option reading (day 5) | the event file keeps it as a reading (§5 Belgium b) | BE.json; C §3, §6 |
| 12 | Table 3, order 1 | 34 (A: 1); lag 23 (A: 56) | adds option reading: order 5, lag 52 | as #11 | P (BE) |
| 13 | Table 3, order 6 | delivery 184–198, lag 134–148 | delivery "after 152 (early August; censored)", lag "more than 102" | the new file codes the delivery as censored (observation window ends 30 June = day 152); the data statement excludes 184–198 | C §5.4; BE.json |
| 14 | Table 3 note | — | sentence on order 6 being censored | as #13 | BE.json |
| 15 | §4.2 | slope and fit under readings B and A | adds the option reading: slope 0.17, supply-limited fits better with any one order left out | every result reported under each reading | X §6 (B: 0.37, 98.0 vs 50.7, reversal without the Life order; A: 0.15; surgical 1.06, all unchanged) |
| 16 | §4.3, para. 1 | orders of import-dependent countries ≥ day 29; Sweden undated; France day 8 | BE/DE/NL ≥ day 29; Sweden February (2–30); France 8 (20 under its validation reading) | new coding | P (FR, SE) |
| 17 | §4.3, para. 1 | deliveries day 46 / 51–52 / 51 "within six days"; orders 2–17 (B) and 35–50 (A) days apart | deliveries 46 / 41–50 / 51–52, 5–11 days apart; orders 2–16 (B) and 35–49 (A) | new DE and NL deliveries; spreads recomputed | P; X §2, §3 |
| 18 | §4.3, para. 1 | "France delivered first (days 39–45)" | France's first delivery 39–52, a window that does not place it before Germany's or Belgium's | FR window 39–52 overlaps DE 41–50 and BE 46 | P (FR); C §3 |
| 19 | Table 5 | old values | FR order 8 (validation 20; looser rule 0), delivery 39–52; BE order 34 (A 1; option 5), binding act 53†, unpaired 12 (A 45; option 41), paired 23 (A 56; option 52); DE order 29–39 (ministry 29–50)†, delivery 41–50†, unpaired 2–21 (ministry −9 to 21); NL delivery 51–52, unpaired 12–16; SE order 2–30, delivery 47–61†, unpaired 17–59; EU tender 28–29, delivery 86 (stockpile) ("joint procurement ≥ 62" removed) | new files; data statement | P; X §1; C §5 |
| 20 | Table 5 note | — | explains the option reading, the two German readings, negative intervals, † (values resting on sources added to the record) and the evidence class | transparency | R; C |
| 21 | §4.3, para. 2 | Spearman "+1.00 in every combination … lower end −0.80 to +0.60" | BE/DE/NL/SE: lower end −0.80 to −0.40, upper +0.80 to +1.00; with France −0.90 to −0.50 and +0.90 to +1.00; labelled exploratory | recomputed over all dates and readings | X §5 |
| 22 | §5, para. 1 | "orders spread over weeks and deliveries within six days" is what a supply constraint would produce | holds under the earlier readings (orders 31–49 days apart); under reading B orders (2–16) were not more dispersed than deliveries (5–11) | recomputed spreads | X §2, §3 |
| 23 | §5, para. 1 | "No dated import-dependent first delivery precedes day 46 (Sweden's window opens on day 41)" | no import-dependent first delivery can fall before day 41 (Germany's window); all within days 31–66 | DE window opens on day 41; SE now 47 | P |
| 24 | §5, para. 3 | France "delivered first" | France delivered from day 39; its window does not establish that it delivered first | as #18 | P (FR) |
| 25 | §6.2 | the stocked case "delivered first" | "delivered early" | as #18 | P (FR) |
| 26 | §7 Coding | "All files were coded by one person, and the firm-order rule was fixed after a first round of coding" | coded by an AI model (Claude) under rules fixed before coding, phrases checked automatically, no human recoding yet, known history, not a blind test | describes the new files (corrected in F10: the F9 wording "one person" was false) | `docs/DAC_PPE_CODING.md` §1–2 |
| 27 | §8 | "deliveries converged while orders diverged, as a supply constraint would predict" | deliveries in the import-dependent countries within days of one another; orders more dispersed only under some readings | as #22 | X §2, §3 |
| 28 | Data availability | scripts "that draw Figures 1 and 2", "archived with a persistent identifier" | scripts for Tables 2, 3, 5 and Sections 4–5; to be archived with a persistent identifier; figures to be redrawn | no figure files or scripts exist in the repository; no persistent identifier has been issued | C §1.3 |
| 29 | References | — | added: Bundesministerium für Gesundheit (2020), Bundesrechnungshof (2025), Service public fédéral Economie (2020), SOU 2020:80 | new citations in §3.1 | R (additions 3–8) |

## Not changed, and why

- **§4.2 values** (slopes, sums of squared errors, leave-one-out results): reproduced exactly from the event files (X §6), so they are kept.
- **Table 4:** every row rests on the Belgian paired lags and first delivery, which are unchanged. Row 9 ("first firm order on day 34") still holds under reading B. Rows 7 and 8 are unchanged.
- **Figure legends:** the figures are not in the repository and must be redrawn from the new files (Data availability). Their legends are kept until then.
- **Practitioner points, §2, §6.1:** they contain no value that changed.

## Points where the revision touches the argument (for Adrian's decision)

These sentences were changed only as far as the new values force. Whether the argument should be rewritten around them is outside the data-only scope:

1. **§5 and §8, the cross-case pattern.** "Orders diverged while deliveries converged" now holds only under the earlier readings of the Belgian first order. Under reading B, which the paper takes as primary, orders (2–16 days apart) were not more dispersed than deliveries (5–11).
2. **France's position.** France's delivery window (days 39–52) no longer shows that it delivered first. §5 and §6.2 use that fact to contrast stock with no stock.
3. **The Spearman range** no longer reaches +1.00 under reading B (upper end +0.80; +0.90 with France).
