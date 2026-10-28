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

All accessed 2026-10-28; fetched and converted by `scripts/fetch_dac_mpox_sources.py`; text in `data/sources/dac_mpox/` (web pages: no stable sha256; PDFs: sha256 in the script). Phrases and dates tested by `tests/dac_unit/test_dac_mpox_file.py`.

| Record | URL | Used for |
|---|---|---|
| WHO statement, 23 July 2022 (second IHR EC meeting) | https://www.who.int/news/item/23-07-2022-second-meeting-of-the-international-health-regulations-(2005)-(ihr)-emergency-committee-regarding-the-multi-country-outbreak-of-monkeypox | t0 (23 Jul 2022); alternative t0 (first meeting 23 Jun 2022, as stated there) |
| WHO statement, 11 May 2023 (fifth meeting) | https://www.who.int/news/item/11-05-2023-fifth-meeting-of-the-international-health-regulations-(2005)-(ihr)-emergency-committee-on-the-multi-country-outbreak-of-monkeypox-(mpox) | window end confirmed |
| Commission press release, 14 Jun 2022 (Representation in Cyprus copy) | https://cyprus.representation.ec.europa.eu/news/hera-secures-vaccines-eu-member-states-response-monkeypox-outbreaks-2022-06-14_en | first firm order (exact) |
| Commission press release, 28 Jun 2022 (same) | https://cyprus.representation.ec.europa.eu/news/european-health-union-start-delivery-vaccines-response-monkeypox-outbreak-2022-06-28_en | first delivery (exact), paired; HERA founding date |
| Commission news, 18 Jul 2022 (same) | https://cyprus.representation.ec.europa.eu/news/health-union-hera-secures-additional-vaccine-doses-response-ongoing-monkeypox-outbreak-2022-07-18_en | second purchase (window); deliveries to 6 member states (context) |
| Commission press release, 7 Sep 2022 (Representation in Germany) | https://germany.representation.ec.europa.eu/news/eu-beschafft-mehr-impfstoff-gegen-affenpocken-2022-09-07_de | third purchase (window) |
| Commission press article, 17 Nov 2022 (Representation in Luxembourg) | https://luxembourg.representation.ec.europa.eu/actualites-et-evenements/actualites/europaische-gesundheitsunion-hera-sichert-bis-zu-2-millionen-dosen-des-affenpockenimpfstoffs-2022-11-17_de | framework contract (context) |
| Commission Implementing Decision C(2022) 5446 and annex (Union Register, procedure 156674) | https://ec.europa.eu/health/documents/community-register/2022/20220722156674/dec_156674_en.pdf (and anx_156674_en.pdf) | binding act (22 Jul 2022) |

**Not opened (gaps, not bypassed):** WHO's own statement of the 23 June EC meeting (HTTP 404 at the URL tried); Commission Implementing Decision C(2022) 5436 of 25.7.2022 amending the EU4Health work programmes (page opened; PDFs answered HTTP 429 with a JavaScript challenge, WebFetch returned binary), so whether it earmarks mpox funding is unknown; Commission Press Corner originals (API returned nothing; Representation copies of the same releases used); HaDEA contract records and national purchase records (not attempted). The Representation in Germany page also answered 429 once, then 200.

**Rules added during coding (dated):**

- **2026-10-28, after the first profile run (recorded because the profile had been seen).** A purchase that the source calls additional or further ("additional", "weitere") to purchases already made has a sourced lower bound: the first dated contract (14 June 2022). Applies to `hera_purchase_2` and `hera_purchase_3`, which were first coded as upper bounds floored at the window start (1 May). Reason: the floor made the two later purchases possible first orders (first-order lag −83 to −39 d; unpaired first order to first delivery 14–58 d), which the sources contradict. After the fix: first-order lag −39 d; unpaired interval 14 d. No other row changed.
- **2026-10-28.** The 18 July release ("has purchased"; "secured over 160,000 doses") does not give the size of the second purchase; it is coded as one additional purchase. Whether it restates part of the 14 June purchase is not excluded by the text.

## 5. Result: profile (description, pre-registered on known history)

`data/dac_mpox/EU_profile.json` (computed by `emo/dac_standard.py`). Lags from t0 (WHO PHEIC, 23 July 2022):

| Sublayer | First event | Lag from t0 |
|---|---|---|
| firm_order | HERA contract, 109 090 doses (14 Jun 2022); 3 orders | −39 d |
| delivery (member states) | 5,300 doses arrive in Spain (28 Jun 2022) | −25 d |
| binding_act | Imvanex authorisation extended to monkeypox, C(2022) 5446 (22 Jul 2022) | −1 d |
| paired order → delivery | 14 Jun → 28 Jun 2022 | 14 d |

**Missing (could not be dated):** dedicated funding (no legal earmark found; C(2022) 5436 unreadable); institutionalisation (none in window; HERA predates it); counter-measure (none found; no dedicated search). Identification: one paired order, minimum for separating decision-limited from supply-limited delay not met.

**Reading.** Every EU response in the file precedes the WHO declaration: the EU ordered 39 days and delivered 25 days before t0, and the binding act came one day before. Under a WHO-PHEIC t0, warning-to-delivery lag is negative for this case, so t0 here does not mark the warning the EU responded to. The alternative t0 (first EC meeting, 23 June) also follows the first order (−9 d to the order; the profile is computed only for the main t0). The earlier warning the EU did respond to (e.g. first case reports in May 2022, ECDC risk assessments) is not coded: no rule fixed it before coding.
