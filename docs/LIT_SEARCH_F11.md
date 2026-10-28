# Literature search for "Decision or Supply?" (fix session F11, 28 Oct 2026)

Task (review F10, point 4): test the manuscript's claim that no existing approach pairs each order with the delivery of that same order, and find records that could give a second paired case. Evidence class: exploratory (literature search; no test).

**Method.** Web search (built-in search tool, "standard" mode except where marked) on 28 Oct 2026, then the most relevant results were opened. Only sources opened are used in the conclusions. Snippets and titles are not used. PDFs too large or blocked for the fetch tool were downloaded with curl and read with pdftotext (sha256 given).

**Could not be searched:** Scopus, Web of Science and Google Scholar (no access from this session); paywalled journal full texts; ResearchGate (not opened); JCCM and Wiley pages (not reachable). The search is therefore broad for official audits and grey literature and thin for peer-reviewed operations-management work. A database search remains to be done.

## 1. Queries (all 28 Oct 2026)

| # | Query | Result used |
|---|---|---|
| 1 | PPE procurement lead time order to delivery COVID-19 empirical study purchase orders hospitals (extended mode) | Global Fund OIG report opened (2.3); others are models or reviews, not opened |
| 2 | National Audit Office PPE contracts order date delivery date data 2020 report investigation | NAO 2022 investigation opened (2.2) |
| 3 | Public Services and Procurement Canada PPE contracts delivered quantities by contract date House of Commons production of documents 2021 | one HESA production document opened (2.1) |
| 4 | GAO report Strategic National Stockpile PPE contracts awarded delivered timeliness 2020 2021 | GAO-21-551 and HHS-OIG A-04-20-02028 opened (2.4) |
| 5 | emergency procurement COVID-19 public administration "lead time" OR "delivery delay" masks government contracts analysis journal article | Spanish Tribunal de Cuentas summary opened (2.5) |
| 6 | process tracing crisis response timeline decision lag implementation lag procurement delivery COVID protective equipment article | nothing relevant opened (press and tender notices) |
| 7 | Auditor General of Canada 2021 Report 10 Securing Personal Protective Equipment and Medical Devices deliveries contracts received | **OAG Report 10 opened (2.1)** |
| 8 | UK Covid-19 Inquiry Module 5 procurement report PPE published findings delivery | Module 5 "In brief" opened (2.2) |
| 9 | Tribunal de Cuentas informe fiscalización contratos emergencia COVID-19 2020 ministerios mascarillas plazo entrega retrasos pdf | full report not opened (press only) |
| 10 | Algemene Rekenkamer Landelijk Consortium Hulpmiddelen inkoop beschermingsmiddelen leveringen onderzoek 2020 2021 | Kamerstuk 35 830 XVI nr. 7 opened (2.6) |
| 11 | "personal protective equipment" procurement COVID-19 systematic review lead times supply chain disruption delivery delays academic | Best & Williams 2021, Caggia et al. 2024, BC internal audit opened (2.3, 2.7) |
| 12 | Open Contracting COVID-19 emergency procurement data contract signature date delivery date implementation milestones masks dataset analysis | OCP European dataset note opened (2.4) |
| 13 | Commissario straordinario emergenza Covid contratti mascherine consegne date open data Corte dei conti … | nothing opened (press) |
| 14 | European Court of Auditors special report 2022 EU initial contribution public health response COVID-19 joint procurement PPE contracts deliveries delays | not opened (scope: EU vaccine reports dominate) |
| 15 | "order-to-delivery" OR "order to delivery" masks respirators government 2020 pandemic analysis contracts days delivered | ProPublica FPDS database page opened (2.4) |

## 2. What the opened sources contain

### 2.1 Canada: the only source found that pairs contracts with their own first delivery

- **Office of the Auditor General of Canada (2021), Report 10, *Securing Personal Protective Equipment and Medical Devices*.** PDF https://publications.gc.ca/collections/collection_2021/bvg-oag/FA1-27-2021-1-10-eng.pdf (accessed 28 Oct 2026, sha256 8720d449…).
  - The audit examined 39 of 85 federal contracts for selected equipment (Exhibit 10.5).
  - **Exhibit 10.7** gives, per equipment type, the "Average number of days from requisition to contract signature (Public Services and Procurement Canada's responsibility)" and the "Average number of days from original contract signature to first delivery … (Supplier's responsibility)": N95 masks 34 and 71 (total 105); medical gowns 28 and 57 (85); test swabs 8 and 16 (24); ventilators 22 and 132 (154).
  - Paragraph 10.96: "We also looked at the time it took from the approval of the original contract to the first delivery…".
  - The federal data "included quantities ordered, expected delivery dates, and quantities received".
  - **What it does and does not do:** it pairs each audited contract with that contract's own first delivery and splits the interval into an administrative part and a supplier part. It reports only averages per equipment type. It does not use variation in order dates to ask whether delivery was set by the decision or by supply.
- **Canada, PSPC briefing for the Government Operations committee, 9 June 2020** (https://www.canada.ca/en/public-services-procurement/corporate/transparency/briefing-materials/standing-committee-government-operations-estimates/2020-06-09/overview-public-services-procurement-canada-purchases-expected-delivery-critical-items.html, accessed 28 Oct 2026): aggregate confirmed orders and items received per item as of 3 June 2020 (e.g. N95: 121,861,800 ordered, 12,221,990 received). Not paired.
- **House of Commons, production of PSPC documents under the motion of 26 Oct 2020**, document HESA_PSPC-M-SPAC-M_0004634_E (https://ourcommons.azureedge.net/data/Motion2020-10-26/2021-02-26-SPDP-8550-432-1-05/HESA_PSPC-M-SPAC-M_0004634_E.pdf, accessed 28 Oct 2026): an email of 26 June 2020 with aggregate figures and one contract "with a set monthly delivery schedule". Not paired. The production runs to many thousands of pages; only this one was opened.

### 2.2 United Kingdom

- **NAO (2020), *The supply of personal protective equipment (PPE) during the COVID-19 pandemic*** (https://www.nao.org.uk/wp-content/uploads/2020/11/The-supply-of-personal-protective-equipment-PPE-during-the-COVID-19-pandemic.pdf, accessed 28 Oct 2026, sha256 4df909e7…). Para. 2.22: "Much of the PPE procured from new suppliers took a long time to be delivered". Figure 12 gives items received per month by delivery method. Not paired. This confirms the manuscript's description (§1).
- **NAO (2022), *Investigation into the management of PPE contracts*** (https://www.nao.org.uk/wp-content/uploads/2022/03/Investigation-into-the-management-of-PPE-contracts_with-CS-Summary.pdf, accessed 28 Oct 2026): disputes over "the timeliness of deliveries" (para. 18) and non-delivery (para. 22). Contract dates are aggregated, there is no per-contract delivery timing, and the NAO "has not reported on specific contracts" (para. 7).
- **UK Covid-19 Inquiry, Module 5 "In brief"** (https://covid19.public-inquiry.uk/reports/module-5-in-brief-summary-procurement/, accessed 28 Oct 2026): no order-to-delivery analysis; "procurement and distribution data were not easily available to procurement teams".

### 2.3 Operations management and reviews

- **Best & Williams (2021),** *Frontiers in Public Health*, scoping review of 30 articles (https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2021.765501/pdf, accessed 28 Oct 2026): no order-level lead times.
- **Caggia, Fondrevelle & Cagliano (2024),** *IFAC-PapersOnLine* 58(19) (https://iris.polito.it/bitstream/11583/2995644/1/Caggia%20et%20al%202024_FINAL%20VERSION.pdf, accessed 28 Oct 2026): literature review of 64 papers plus a Likert survey of PPE firms; delivery time is perceived, not measured.
- **Global Fund OIG (2021), GF-OIG-21-016** (https://www.theglobalfund.org/media/11590/oig_gf-oig-21-016_report_en.pdf, accessed 28 Oct 2026): average procurement lead times (standard orders eight months, p. 7; urgent orders seven to eight, p. 8). Not for PPE, and not order by order.

### 2.4 United States

- **GAO-21-551** (July 2021) (https://www.gao.gov/assets/720/716067.pdf, accessed 28 Oct 2026): aggregated obligations; no per-contract delivery timing.
- **HHS-OIG A-04-20-02028** (Oct 2023) (https://www.oversight.gov/sites/default/files/documents/reports/2023-11/42002028.pdf, accessed 28 Oct 2026): about stockpile deployment ("90 percent … in three shipments between March 11, 2020, and March 24, 2020", p. 8); no review of vendor contracts.
- **ProPublica "Coronavirus contracts"** (https://projects.propublica.org/coronavirus-contracts/vendors/3m-company, accessed 28 Oct 2026): FPDS contract actions with signing date and amount; no delivery dates shown.
- **Open Contracting Partnership, European COVID-19 tenders** (https://www.open-contracting.org/2021/02/04/unmasking-emergency-procurement-how-we-published-37000-european-covid-19-related-tenders/, accessed 28 Oct 2026): about 38,000 tenders and unit prices; no delivery dates; Belgium, the Netherlands and Denmark published none.

### 2.5 Spain

- **Tribunal de Cuentas, audit of 2020 emergency contracts of national ministries** (ECA summary page, https://eca.europa.eu/sites/CC/en/Documents/Covid_19/SAI-reports/SAI_ES_emergencycontracts_2020_EN.pdf, accessed 28 Oct 2026): 133 contracts; the implementation timeframe was imprecise "for 22 % of the contracts"; "delays in implementation (causing deadline extensions and further delays…)". The Spanish full report was **not opened**, so it may hold contract-level award and delivery dates; unverified.

### 2.6 Netherlands

- **Tweede Kamer 35 830 XVI nr. 7 (2021),** questions and answers on the audit office's report on VWS 2020 (https://zoek.officielebekendmakingen.nl/kst-35830-XVI-7.pdf, accessed 28 Oct 2026): deliveries to the LCH "niet konden wachten op administratieve verwerking"; missing receipts; Mediq placed the orders (p. 10). No per-order dates.

### 2.7 Other

- **British Columbia, Internal Audit & Advisory Services (2022), PPE procurement phase 1** (https://www2.gov.bc.ca/assets/gov/british-columbians-our-governments/services-policies-for-government/internal-corporate-services/internal-audits/procurement-ppe-phase-1-review.pdf, accessed 28 Oct 2026): no order-level timing.

## 3. Conclusion (a): does the manuscript's claim survive?

**Not in its present form.** The manuscript (Table 1 and §2.3) says no approach "is designed to link each order to the delivery of that same order from records". The Auditor General of Canada did exactly that for 39 federal contracts in 2021. It measured, for each, the days from contract signature to that contract's first delivery, and separated an administrative part (requisition to contract) from a supplier part (contract to first delivery), reported as averages per equipment type (Exhibit 10.7).

**What survives, in the sources searched:** no source found uses the variation in order dates across paired orders of the same good to test whether delivery was set by the decision or by supply (Proposition 1 and the slope test). Audits report averages and attribute the parts to responsibilities (agency or supplier), not to mechanisms.

**Consequence for F12:**
- Add the Canadian audit to Table 1 as the closest approach (an audit with contract-level pairing, averaged).
- Reword the novelty claim to the test, not the pairing.
- Cite Exhibit 10.7 as a second country in which the supplier part dominated: N95 71 of 105 days, gowns 57 of 85. This is unpaired across countries but comparable in kind.
- State that operations-management databases (Scopus, Web of Science) were not searched.

## 4. Conclusion (b): records that could give a second paired case

| Candidate | What it would give | Access route | Effort | Status |
|---|---|---|---|---|
| **Canada, federal N95 and gown contracts** (39 audited contracts) | contract signature and first-delivery dates per contract, several contracts per good on different dates: the Proposition 1 test | request to Public Services and Procurement Canada under the Access to Information Act (eligibility of a requester outside Canada not checked), or a search of the House of Commons production (many thousands of pages, partly scanned) | high (weeks; uncertain) | the most promising: the data exist (OAG Exhibit 10.7; PHAC tracked "expected delivery dates, and quantities received") |
| **United States, federal PPE contract actions** (FPDS / USAspending) | signing dates per contract; possibly promised completion dates (the period-of-performance fields, not opened here), which are the "promised delivery dates" the manuscript names as the record that would separate M1 from M2 | public API and bulk download | medium (one session to check the fields and pull March–June 2020 respirator contracts) | field availability unverified; actual deliveries not in FPDS |
| **Spain, Tribunal de Cuentas full report** (133 emergency contracts, 2020) | possibly award and delivery dates per contract, with delays | public report (Spanish) | low to medium (one session) | not opened; unverified |
| **Germany, Bundesrechnungshof reports of 16 Jun 2021 and 28 Mar 2024** (cited in its 2025 report) | procurement-channel timelines for the German case | Bundestag committee documents or the audit office's website | low to medium | not opened |
| **UK Covid Inquiry Module 5 evidence** | possible DHSC contract and delivery data | inquiry document library | high | not checked |

**Recommendation:**
1. **One session first:** check the Spanish full report and the US FPDS fields. These are the two cheap checks, and either could yield paired or promised dates.
2. **The Canadian request** gives the strongest second case but takes weeks and its eligibility is unchecked, so start it in parallel only if Adrian decides to.
3. **For F12, a second case is not needed** to fix the novelty claim; the rewording and the Canadian citation suffice.
