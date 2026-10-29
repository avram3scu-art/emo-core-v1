# Independent double coding: protocol (session 11)

Committed 2026-10-29, **before any second coder was contacted and before any second coding exists.** This file pre-registers how a second person codes one DAC case without help, how agreement with Claude's coding is computed, and how disagreements are resolved. Agreement is computed in a later session, once a coded sheet is returned.

## 1. Why, and which case

Every DAC event file in this repository was coded by one coder, an AI model (Claude). No human has recoded any of them (`docs/REVIEW_F10_DECISION_OR_SUPPLY.md`). A second, human coder working from the same written rules and the same sources is the check that the files are not shaped by one coder.

**Case for this round of double coding: EU mpox vaccines, 2022** (`data/dac_mpox/EU.json`, coded in session 10). Reasons: nine short official sources, all already in the repository; seven in English, two short Commission pages in German; about 3–4 hours of work. A later round may use the Belgian PPE case (`data/dac_ppe/BE.json`, the manuscript's key case), which needs French and Dutch and a 500-row annex.

**Evidence class of the agreement result.** Pre-registered blind if the second coder declares (§5) that they did not open Claude's file, its profile, the mpox coding notes or any EMO result before returning the sheet; otherwise pre-registered on known history. Claude's own coding stays pre-registered on known history (`docs/DAC_MPOX_CODING.md` §1).

## 2. What the second coder receives, and what they must not open

**Packet** (`docs/double_coding/DAC_double_coding_packet_mpox.zip`, built by `scripts/build_double_coding_packet.py`):

- this file;
- `coding_sheet.csv` (empty sheet, §5) and `training_answer.csv` (§4);
- the nine source texts of `data/sources/dac_mpox/`, unchanged.

**Do not open** before returning the sheet: `data/dac_mpox/` (Claude's file and profiles), `docs/DAC_MPOX_CODING.md`, `docs/DAC_T0_EARLY_WARNING.md`, `tests/dac_unit/test_dac_mpox_file.py`, the README, the EMO page, `docs/STATUS.md`, `docs/RECORD.md`. The message (§10) does not link the repository.

**No AI tools for coding.** The sheet is your own reading. A machine translation of the two German pages is allowed for understanding; quote the original German in the sheet and say in `notes` that you used a translation.

## 3. Coding rules (follow these alone; no other guidance is needed)

### 3.1 The idea

DAC measures how long institutions take to move from a **warning** to a **delivered response**. You read official records and write down, for each kind of step, the earliest step the records show, with its date as precisely as the record allows. You never guess a date.

### 3.2 This case

- **Warning (t0):** the World Health Organization Director-General's declaration that the multi-country monkeypox outbreak is a Public Health Emergency of International Concern (PHEIC). Code it as sublayer `validation`. If the records mention an earlier WHO Emergency Committee meeting that did not declare an emergency, code it as `context`.
- **Who responds:** the EU institutions (European Commission, including HERA and HaDEA). Purchases or acts of individual member states are `context`, except an act of a member state against the EU response (`counter_measure`).
- **End point:** member states, i.e. the physical arrival of EU-procured doses in a member state.
- **Good:** MVA-BN mpox vaccine (also called Imvanex or Jynneos). Write `MVA-BN vaccine` in `good` on every order and delivery.
- **Observation window:** 1 May 2022 to 11 May 2023 (the WHO declaration that the emergency is over). An event after 11 May 2023 is coded `censored`, without a date.
- **Responses before t0 are kept** in their own sublayer (not as context), even though they come before the warning.

### 3.3 Sublayers (one per row)

| Sublayer | Code a row when the record shows … | Not this sublayer |
|---|---|---|
| `validation` | the WHO PHEIC declaration (t0) | earlier meetings (→ `context`) |
| `firm_order` | a purchase contract for the vaccine signed by the Commission (HERA/HaDEA) for supply to member states | tenders, framework contracts without a purchase, announcements of intent, antivirals or tests (→ `context`) |
| `binding_act` | a legally binding EU act on the mpox vaccine response (e.g. a Commission decision on the marketing authorisation, a financing decision), dated by its adoption | a recommendation or opinion that binds no one (→ `context`) |
| `dedicated_funding` | funding legally earmarked for mpox vaccines (a legal act or financing decision naming mpox) | a press statement of an amount spent (→ `context`) |
| `delivery` | physical arrival of EU-procured doses in a member state | shipments announced but not stated as arrived (→ `context`); totals delivered so far (→ `context`) |
| `institutionalisation` | a permanent body created for this hazard | a body that existed before the outbreak |
| `counter_measure` | a member-state act against the EU response | — |
| `context` | anything relevant that is none of the above | — |

If the records show no event for a sublayer, write one row with `date_status` = `missing` and no dates (for `firm_order`, `binding_act`, `dedicated_funding`, `delivery`, `institutionalisation`, `counter_measure`). Never fill a gap from memory or from a non-official source.

### 3.4 Dates

- `exact`: the record gives the day, or says "today" in a release that carries a date. `date_earliest` = `date_latest` = that day.
- `upper_bound`: the record says something "has" happened ("has signed", "have arrived") without a day. `date_latest` = the record's date; leave `date_earliest` empty; copy the record's words into `source_wording`.
- `lower_bound`: the record says something will happen or happened after a known day, without its own day. `date_earliest` = that day; leave `date_latest` empty; `source_wording` required.
- `window`: both bounds known, e.g. a month ("in July 2022" → 2022-07-01 to 2022-07-31); `source_wording` required.
- **Additional purchases.** A purchase that the record calls additional or further ("additional", "further", "weitere") to purchases already made gets a lower bound: the date of the earliest dated purchase contract in your sheet. Code it as `window` if it also has an upper bound.
- **Size unknown.** A record that says doses "have been purchased" without saying how many in this purchase is still one purchase (one row).
- **Two records, two dates for one event:** write two rows with the same `row_id` and `reading` A and B.
- Dates as YYYY-MM-DD.

### 3.5 Pairing

On a delivery row, `pairs_with` = the `row_id` of the order it fulfils, **only if the record itself links them** (e.g. "doses from the contract signed on [date]"). Otherwise leave it empty.

### 3.6 Every row

Give the source file name and a verbatim quote (the shortest phrase that shows the event and its date). Use `notes` for anything uncertain; uncertainty is useful information, not a fault.

## 4. Training example (synthetic, not part of any case)

Read this invented release, code it, then compare with `training_answer.csv`.

> *European Commission, press release, Brussels, 3 March 2031.* "The Commission has today signed a contract with Fictipharm for 200,000 courses of the antiviral Zanovir for member states, following WHO's declaration of an emergency on 20 February 2031. This comes in addition to the 50,000 courses purchased under the earlier contract. An initial 20,000 courses of the earlier contract have arrived in Portugal. Delivery of the new courses will start in April. The Commission also proposes a regulation creating a permanent stockpile agency."

Answer (also in `training_answer.csv`), with t0 = WHO declaration 20 Feb 2031 and the good "Zanovir":

| row_id | sublayer | date_status | date_earliest | date_latest | why |
|---|---|---|---|---|---|
| t0 | validation | exact | 2031-02-20 | 2031-02-20 | day stated |
| order_new | firm_order | exact | 2031-03-03 | 2031-03-03 | "has today signed" in a dated release |
| order_earlier | firm_order | upper_bound | | 2031-03-03 | "purchased" before; no day; it is *earlier*, so no lower bound from the additional-purchase rule |
| delivery_pt | delivery | upper_bound | | 2031-03-03 | "have arrived"; pairs_with = order_earlier (the release links them) |
| delivery_new | context | | | | announced, not arrived |
| agency_proposal | context | | | | a proposal is not a binding act; the agency does not exist yet |
| funding | dedicated_funding | missing | | | no earmarked funding shown |

Two lessons: the earliest order may be the one with the vaguest date; and "will start in April" is never a delivery.

## 5. Return sheet

Fill `coding_sheet.csv` (one row per event; columns: `row_id, sublayer, reading, date_status, date_earliest, date_latest, source_wording, good, end_point, pairs_with, source_file, quote, description, notes`). Then add, at the end of the file or in your reply e-mail:

1. Hours spent.
2. "Before returning this sheet I did not open Claude's mpox file, its profile, the mpox coding notes or any EMO result, and I used no AI tool for coding": **yes / no** (if no, say what you saw).
3. Rules you found unclear, with the source passage.
4. How you want to be named (full name in the data file and acknowledgements, or anonymous).

Adrian forwards the sheet unchanged; it is committed as received before it is compared.

## 6. Agreement statistic (pre-registered)

**Conversion.** Claude converts the returned sheet to a DAC v1.1 event file (`data/dac_mpox/EU_coder2.json`) by a script that maps columns one to one and invents nothing; any row the validator rejects is listed with the reason and kept out, never repaired by guess. The conversion script, the sheet and the file are committed before the comparison is run. Both files are then frozen (commit ID recorded).

**Scored items (9), fixed now.** For the case's end point (member states):

1. t0 date; 2. earliest `firm_order`; 3. earliest `delivery`; 4. earliest `binding_act`; 5. `dedicated_funding`; 6. `institutionalisation`; 7. `counter_measure` — each as status (dated / missing / censored) and, if dated, the interval [earliest possible, latest possible] of the earliest event, over all readings (union);
8. pairing of the earliest delivery (which order it pairs with, matched by that order's date interval and description, or unpaired);
9. number of firm orders.

`context` rows are listed side by side but not scored.

**Per item:** *same* (same status and, if dated, identical interval; for 8 the same order or both unpaired; for 9 equal counts); *overlapping* (both dated, intervals intersect, not identical); *different* (anything else). For items 2–4 also the two profile lags from t0 (computed by `emo/dac_standard.py`) and their difference in days.

**Reported:** the 9 items with their class; counts of same / overlapping / different; lag differences. **No pass/fail and no significance test:** 9 items from one case cannot support either (CLAUDE.md, science rules); the result is a description. No kappa or alpha is computed for one case: with 9 dependent items it would look like a measure of reliability without being one. A chance-corrected statistic (Krippendorff's alpha, interval metric, on lags) is for a later protocol once several cases are double coded; it is not pre-registered here.

**Pre-set consequence.** Any item not *same* goes to §7. Claude's file is never changed to match before the comparison is recorded.

## 7. Disagreement resolution

1. **Record first.** The comparison of §6 on the frozen files is written to this file (§8) and `docs/RECORD.md` before any discussion. It is never revised.
2. **Classify each non-same item** by cause: (a) rule unclear or silent; (b) same source read differently; (c) a coder's error (either coder, Claude included); (d) a source one coder did not use or could not read.
3. **Resolve in writing.** Claude prepares, for each item, both rows with the source passages side by side. The second coder and Adrian answer item by item; Claude's coding gets no extra weight. Agreed corrections go into a separate resolved file (`data/dac_mpox/EU_resolved.json`) with a change log (item, before, after, cause, who agreed, date). Both original files stay unchanged.
4. **Unresolved:** both values are kept as two readings of the same event (`reading` A and B), which the DAC standard already supports; the profile then reports both. No one has a casting vote.
5. **Rules.** A cause (a) leads to a dated rule change in this file for future cases; the current case is recoded under a new rule only if both coders agree, and that change is labelled as made after the comparison.
6. Claude's own errors found here are fixed and recorded (CLAUDE.md).

`case.coding` in the resolved file becomes: `coders: 2` (one AI model, one human), `agreement`: the §6 counts as text.

## 8. Result

Not yet: no second coding exists (29 Oct 2026).

## 9. Limits (stated before any coding)

- One case and 9 items: the result can show disagreements, not establish reliability.
- The second coder reads the source texts as extracted (page navigation included), not the original pages; the URLs are in each file's first line if they want to check.
- The additional-purchase rule (§3.4) was added to Claude's rules during coding, after Claude had seen its first profile (`docs/DAC_MPOX_CODING.md` §4). The second coder applies it from the start; agreement on items 2 and 9 therefore tests the rule as written, not Claude's first reading.
- Blindness rests on the second coder's declaration; the repository is public.
- The second coder works from the source pool Claude chose; agreement does not test whether that pool is complete.

## 10. Invitation message (Adrian sends it)

Kept in `docs/double_coding/invitation.md`.
