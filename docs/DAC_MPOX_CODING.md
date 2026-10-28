# Mpox case: coding rules and source list (session 10)

First warning-to-delivery case outside the PPE domain, coded in DAC standard v1.1 (`docs/DAC_STANDARD.md`). Committed 2026-10-28 **before any mpox source was opened**. Event file: `data/dac_mpox/EU.json`; profile: `data/dac_mpox/EU_profile.json`.

## 1. What was known before coding (blindness)

No mpox source was opened in this repository before this file was committed. From Claude's general knowledge (not checked; may be wrong), the following was believed before coding: WHO declared the multi-country mpox outbreak a PHEIC on 23 July 2022; the Commission's HERA bought MVA-BN (Imvanex/Jynneos) doses from Bavarian Nordic for donation to member states in June 2022, i.e. **before** the PHEIC, with first deliveries in late June; some member states (e.g. Germany) bought doses on their own in May–June 2022; the EU authorisation of Imvanex was extended to mpox in July 2022. **Every row of this file is therefore "pre-registered on known history", not blind.** The profile is a description, not a test.

## 2. Coding rules

- **t0:** WHO Director-General's declaration that the multi-country monkeypox outbreak is a Public Health Emergency of International Concern (expected 23 July 2022; dated from WHO's own statement). **Alternative t0:** the first meeting of the IHR Emergency Committee on the outbreak (which did not declare a PHEIC), dated from WHO's own statement; coded `context` and listed in `alternative_t0`.
- **Observation window:** 2022-05-01 to 2023-05-11. Start: the month in which the outbreak outside endemic countries was first reported. End: WHO's declaration that the PHEIC is over (11 May 2023, to be confirmed from a WHO record; if not confirmed, the end stays 2023-05-11 and is labelled unconfirmed). Later events are `censored`.
- **Responses before t0 are kept.** An order, act or delivery that precedes t0 is coded in its own sublayer, not as `context`, and its lag is negative. (Differs from the PPE case, where no pre-t0 response existed; reason: a warning-to-delivery profile that drops responses earlier than the warning would misstate the case.) A window without a sourced lower bound opens at the observation-window start (2022-05-01), not at t0.
- **Response scale:** the EU institutions (Commission, incl. HERA). Acts and purchases of member states are `context`, except acts against the EU response (`counter_measure`).
- **End point:** member states (physical arrival of EU-procured doses in a member state). No secondary end point.
- **firm_order:** a purchase contract for mpox vaccine (MVA-BN / Imvanex / Jynneos) signed by the Commission (HERA) for supply to member states. Excluded: tenders, framework contracts without a purchase, announcements of intent. Purchases of antivirals (tecovirimat) or tests are `context` (task: vaccines). A joint-procurement contract signed by the Commission on behalf of member states is a firm order if the source says it was signed.
- **binding_act:** first legally binding EU act concerning the mpox vaccine response (e.g. a Commission decision on the marketing authorisation for mpox, a financing decision). Dated by adoption.
- **dedicated_funding:** first funding legally earmarked for mpox vaccines (a legal act or financing decision naming mpox). A press statement of the amount spent is `context`.
- **delivery:** first physical arrival of EU-procured mpox vaccine doses in a member state. Shipments announced but not stated as arrived are not deliveries.
- **institutionalisation:** first permanent body created for the hazard (expected missing: HERA predates the outbreak). **counter_measure:** a member-state act against the EU response.
- **Pairing:** a delivery carries `pairs_with` only if the source links it to the purchase it fulfils (e.g. "doses from the first purchase"). `good`: "MVA-BN vaccine".
- **Dates:** exact only if the source gives the day or says "today" in a dated release; "has signed" / "have arrived" without a day → upper bound at the release date with the source's wording. Two official sources giving different dates for the same event → one row per reading. Nothing imputed; an event known to exist but undated in any opened record → `missing`.
- **Coders:** one (Claude); `rules_fixed_before_coding: true`.

## 3. Source list (official records only)

Only records published by the institution concerned are coded; news reports, encyclopaedias and secondary literature are not used, not even as `context`. Each source opened is listed in §4 with URL, access date and sha256 of the fetched file (or "page text, no stable sha256").

1. **WHO:** Director-General's statements on the IHR Emergency Committee meetings on the multi-country monkeypox outbreak (first meeting; PHEIC declaration; end of PHEIC).
2. **European Commission:** press releases and daily news (Press Corner) and HERA news pages on the purchase, donation and delivery of mpox vaccines.
3. **EU legal acts:** Commission decisions on the Imvanex marketing authorisation (Union Register of medicinal products) and any financing decision, via EUR-Lex / Publications Office.
4. **EMA:** CHMP recommendation on extending Imvanex to monkeypox (context unless binding).
5. **Member-state ministries:** only for `context` rows (national purchases), if found in an official national record.

If a needed record cannot be opened (bot challenge, CAPTCHA, HTTP error), it is not bypassed; the gap is recorded in §4 and the event is coded from another official record or as `missing`.

## 4. Sources opened and rules added during coding

(Filled during coding; dated.)
