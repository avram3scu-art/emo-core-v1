# PPE case: coding rules, sources and comparison protocol (fix session F8)

Rebuilds the six PPE event files of the DAC manuscript ("Decision or Supply?") from primary sources in DAC standard v1.1, because the original files were not recovered (F1, 28 Oct 2026). Committed 2026-10-28 **before any PPE event was coded**.

## 1. What was already known when coding started (blindness)

Blindness is partial and stated here once, per case:

- **Read before F8:** the final manuscript's abstract (F1), its revision fragments for §1, §2.7 and §2.8 (F1), and the text of its Sections 2–3 with tables removed (F8, to write these rules). The table note under Table 2 was read ("the order file holds the contested first order under two readings, hence nine rows"). Tables 2–5 and Figures 1–2 were **not** opened.
- **Belgium: key result known.** The abstract and §2.8 state it: surgical masks ordered 15 March arrived in 5 days, FFP2 respirators ordered 16 March in 21; a delay common to the purchasing service is rejected and bounded at five days. **The Belgian file is therefore "pre-registered on known history", not blind.**
- **France, Germany, Sweden: first-order coding known.** §3.1 states France's first firm order (7 February 2020, 28.4 million FFP2; the 30 January order excluded as single-mission), Germany's (window closing at its first delivery; federal procurement started 28 February) and Sweden's (undated; window opens at t0). Their first-order rows are "known history"; their other rows are coded without having seen the manuscript's values.
- **Netherlands, EU: no result values seen.**

Each later F8 session records whether it opened anything of the manuscript beyond this.

## 2. Coding rules (from the manuscript's §2.1 and §3.1 text and DAC standard v1.1)

- **t0:** WHO declaration of a Public Health Emergency of International Concern, 30 January 2020 (exact). **Alternative t0** (rule chosen here; the manuscript's §4.3 alternative was not read): WHO's characterisation of COVID-19 as a pandemic, 11 March 2020.
- **Observation window:** 2020-01-01 to 2020-06-30 (first wave; opened at 2020-01-01 on 28 Oct, see §5). Events after it are `censored`.
- **Response scale:** one national government (federal level for BE and DE), or the EU institutions for the EU file. Acts of other levels are `context`; an act of one level against another's response is a `counter_measure` in the file of the level it targets.
- **firm_order:** first purchase order or contract for PPE (masks, respirators, gowns, gloves, goggles) intended for general supply. Excluded: inquiries, options, framework calls without a purchase, purchases documented for a single mission. An EU joint-procurement tender is `context` in national files and a firm order in the EU file only when a contract is signed.
- **binding_act:** first legally binding act concerning the PPE response (requisition, export ban, price cap, procurement derogation). Recorded, not compared across cases.
- **dedicated_funding:** first funding legally earmarked for the PPE response.
- **delivery:** first physical delivery to the first distribution level below the responding authority. Primary end points: BE municipalities; FR pharmacies supplying health professionals; DE the Länder and associations of statutory-health-insurance physicians; NL regional acute-care networks; SE regions and municipalities; EU member states. Delivery to providers (hospitals, care homes) is a secondary end point. Offers, contracts and announced arrivals are not deliveries.
- **institutionalisation:** first permanent body created for the hazard. **counter_measure:** as above, in either direction.
- **Pairing:** a delivery carries `pairs_with` only if the source links it to the order it fulfils. Each paired order and delivery carries `good` (e.g. "surgical masks", "FFP2 respirators"). The **order file** of the manuscript is, in standard v1.1, the set of paired `firm_order`/`delivery` rows of the Belgian event file.
- **Dates:** exact only if the source gives the day; otherwise a window or bound with the source's wording; a window without a sourced lower bound opens at t0. Contested dates: one row per reading, each with the source that supports it. Nothing imputed.
- **Sources:** primary only (parliamentary reports and their annexes, hearing records, official acts, ministry replies, official statistics), cited with document, page and, for the Belgian chronology, the annex row's date. Secondary sources may only be `context`.
- **Coders:** one (Claude), rules fixed before coding (`rules_fixed_before_coding: true` for every F8 file).

## 3. Sources per case and repository status

| Case | Primary source | In the repo |
|---|---|---|
| BE | Chamber of Representatives, special committee COVID-19, report DOC 55 1394/002 (13 Sep 2021), Annex 5 (chronology) | fetch script `scripts/fetch_dac_ppe_sources.py` with sha256 (identical to Adrian's copy of 26 Oct); Annex 5 text extracted to `data/sources/dac_ppe/BE_annex5.txt` |
| FR | Sénat, report no. 199 (2020–2021) | Adrian's copy identified by sha256 only (`docs/sources/SOURCES_SUPPLIED.md`); to be fetched in its F8 session |
| DE | Bundestag printed papers (answers to parliamentary questions) 2020; EU notification of the German export ban; Sudhof report (Jan 2025, marked "VS – Nur für den Dienstgebrauch": not committed, use limited to Adrian's decision) | not yet |
| NL | Ministerie van VWS (2021), factual reconstruction | not yet (Adrian to supply if not fetchable) |
| SE | SOU 2021:89 | Adrian's copy identified by sha256 only; to be fetched |
| EU | Official Journal acts, Commission records | not yet |

## 4. Comparison protocol (fixed now; run only after all six files are coded and validated)

1. Compute each file's profile with `emo/dac_standard.py` (all readings).
2. Then, and only then, open the manuscript's Tables 2–5 and Figures 1–2.
3. For each case compare: first firm order, first binding act, first verified delivery (date or window, and lag from t0), and for Belgium every paired order-to-delivery lag and the identification profile per good.
4. Report **every** difference with its kind: (a) different source, (b) different rule or reading, (c) coding error in the new file, (d) error in the manuscript. A new file is not changed after the tables are opened, except to correct a type-(c) error, which is then listed with before and after.
5. Agreement is reported per item as a profile (same / overlapping windows / different), never as one score.
6. The result decides the data statement: the paper may cite these files only for items that agree or whose differences are explained.

## 5. Rules added during coding (dated; before any profile was computed)

- **2026-10-28, Belgium.** (a) A date that the source itself flags as contradicted, with no alternative date given (Annex 5 "Contrad. dat."), is coded `missing`; the recorded value goes in the description. Applies to the Pan Scope delivery ("livraison le 19 mars 2020" for an order of 23 March, row 723). (b) Every dated statement in the chronology about the same order is a reading, including statements by members of the committee recorded in a hearing: the 3M order of 500,000 FFP2 has three readings (31 Jan, row 1052; 4 Feb "option sur/commande", row 760; 4 Mar "première commande", row 716; rows 760 and 716 are cross-flagged "Contradict."). (c) Annex 5 cites its source per row (hearing record CRIV K0xx or written answers); the coded `source` gives the report, PDF page, row number and that cited source. Hearing records themselves were not opened (scope: one source per sitting).
- **2026-10-28, all cases.** Observation window opens 2020-01-01 instead of at t0, so that events before t0 (e.g. the 29 January inquiry to 3M) can be recorded as `context`. It does not change any lag: windows without a sourced lower bound still open at t0 (set explicitly as `date_earliest` = 2020-01-30), and no pre-t0 event enters the profile. Found when the Belgian file failed validation; changed before any profile was computed.
- **2026-10-28, France (F8.2).** (a) Where the source dates both the request to the purchasing agency (DGS "saisine" of Santé publique France) and, separately, the validation of the first resulting purchase, both are readings of the first firm order: reading A 7 Feb 2020 (request; called a "commande … adressée aux quatre fabricants" on PDF p. 146), reading B 19 Feb 2020 ("l'une des deux premières commandes d'ampleur, validée le 19 février", p. 123). (b) A WHO event absent from a country's source is cited from the Belgian Annex 5 (an official record of the same event). (c) The Sénat report gives no dated verified delivery of any national order, so the French file has no paired orders.
