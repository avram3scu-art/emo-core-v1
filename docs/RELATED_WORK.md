# Related work

Session 4, 23 Oct 2026. Purpose: before EMO claims any gap, record what existing work already measures.

Rules used here:
- Every entry says what was **opened** in this session. Anything not opened is marked **[unverified]**.
- "What EMO adds" points only at code that runs today (see `README.md`, `results/weekly/`). Metrics that have not run on real data (UIA, SΦ, GWI, SMF, M_E) add nothing yet and are not counted.
- This is not a full literature search. Only the sources named in the session 4 prompt were searched, through a general web search engine. No full-text databases (Scopus, Web of Science, Google Scholar) were searched. No novelty claim follows from this file.

## Summary

Existing work already measures: the presence of policy-coherence mechanisms (SDG 17.14.1), perceived governance quality (WGI), sovereign ESG performance (Sovereign ESG portal), the effectiveness of international environmental regimes (Oslo-Seattle, IRD), the timing and stringency of government responses (OxCGRT), and early-warning coverage and its association with mortality (Global Status of MHEWS). So "no instrument measures how well humanity responds" is false and has been removed from the white papers.

The narrow thing EMO does today that none of the opened sources does: publish, as an open series re-run weekly from public data, the dated lags from a scientific warning to a policy instrument to measured physical delivery (DAC; ozone case, compared with climate). Even this overlaps closely with the regime-effectiveness literature, which studied the same ozone regime; EMO's difference is form (dated lags, open code, scheduled re-run), not question.

## Entries

### E1. SDG indicator 17.14.1: mechanisms in place to enhance policy coherence for sustainable development

- **Opened:** SDG metadata page, World Bank mirror of the UN metadata (last updated 2023-01-24): https://worldbank.github.io/sdg-metadata/metadata/en/17-14-1
- **What it measures:** whether a country has mechanisms for policy coherence across the dimensions of sustainable development. It measures institutions in place, not outcomes.
- **How:** composite of 8 domains (political commitment, long-term considerations, inter-ministerial coordination, participation, integration of the three dimensions, coordination across government levels, monitoring and reporting, financial resources and tools), each scored 0–10, total 80, reported as a percentage. Self-scored by national governments via a UNEP questionnaire; custodian UNEP.
- **Coverage:** countries that return the questionnaire; first collection 2020, biennial. Number of reporting countries not stated on the page **[unverified]**.
- **EMO overlap:** EMO's "alignment" and "consistency" dimensions, if read as policy coherence, duplicate this concept. EMO computes nothing equivalent today.
- **What EMO adds:** nothing on mechanisms. DAC measures something different: whether a warning was followed by delivery, from outcome data rather than self-report. 17.14.1 adds domain points into one percentage; EMO's profile rule (CLAUDE.md) would report the 8 domains separately.

### E2. World Bank Sovereign ESG Data Portal

- **Opened:** World Bank feature story on the relaunch, 12 Dec 2022: https://www.worldbank.org/en/news/feature/2022/12/12/world-bank-relaunches-sovereign-esg-data-portal. The portal itself (esgdata.worldbank.org) was **not opened**; current indicator counts **[unverified]**.
- **What it measures:** country environmental, social and governance performance for investors.
- **How:** 71 indicators in the Sovereign ESG Data Framework plus 40 more, mostly World Bank data, land cover from ESA satellite data. Includes a score builder where the user picks indicators and aggregation.
- **Coverage:** 217 economies, up to 60 years (as of Dec 2022).
- **EMO overlap:** EMO's weekly data refresh draws on similar public series (OWID CO₂, ODS consumption, aid share of GNI, conflict deaths). As a data source, the portal is broader than EMO's.
- **What EMO adds:** nothing as a data portal. EMO's analyses (lags, organismality plane, τ_I) are computations on series, which the portal does not provide.

### E3. Worldwide Governance Indicators (WGI)

- **Opened:** WGI FAQ page, World Bank: https://www.worldbank.org/en/publication/worldwide-governance-indicators/frequently-asked-questions; and *The Worldwide Governance Indicators: Revised Methodology for Measuring Governance Using Perception Data* (World Bank DECIG, December 2025; Jiang, Jain, Romano, Boyce), PDF supplied by Adrian, 23 Oct 2026: https://www.worldbank.org/content/dam/sites/govindicators/doc/The%20Worldwide%20Governance%20Indicators%202025%20Methodology%20Revision.pdf
- **What it measures:** six perception-based dimensions: Voice and Accountability, Political Stability, Government Effectiveness, Regulatory Quality, Rule of Law, Control of Corruption.
- **How:** 35 sources (surveys and expert assessments), 400+ individual indicators rescaled to 0–1 and averaged within source and dimension, then combined by an Unobserved Components Model whose weights reflect each source's estimated precision; 90% confidence intervals. The 2025 revision lets the global average vary over time and maps estimates onto an absolute 0–100 scale anchored by two hypothetical benchmark countries (all representative sources at 1, or all at 0). The six dimensions are not combined into one index (paper: too broad to interpret meaningfully). Historical estimates recalculated back to 1996.
- **Coverage:** 200+ economies, annually 1996–2024 (2025 paper); the FAQ says the 2026 edition covers data through 2025.
- **EMO overlap:** none in substance. WGI is national and perception-based; EMO's running analyses are global and outcome-based.
- **What EMO adds:** not comparable. WGI already follows the rule EMO adopted (dimensions reported separately, with uncertainty), and since 2025 it can show global trends over time. EMO should cite it as precedent, not as a gap.

### E4. Regime effectiveness: Miles et al. (2002), the Oslo-Seattle project

- **Opened:** library catalogue record with full table of contents: https://bdu3.siu.edu.ar/bdu/Record/B-35-990000674870204151/TOC. Full text **not opened**.
- **Citation (from the record):** Miles, E. L., Underdal, A., Andresen, S., Wettestad, J., Skjærseth, J. B., Carlin, E. M. (2002). *Environmental Regime Effectiveness: Confronting Theory with Evidence*. MIT Press. (Author list beyond Miles taken from chapter authorship in the TOC.)
- **What it measures:** whether international environmental regimes changed behaviour and solved problems.
- **How:** case studies with a common method (ch. 2, Underdal). The measurement scale (no-regime counterfactual, distance to collective optimum) is how this project is usually described **[unverified: not read in the opened source]**.
- **Coverage:** 14 regimes, including the Vienna Convention / Montreal Protocol (ch. 6, Wettestad), LRTAP, North Sea, IWC, CITES, CCAMLR, nuclear non-proliferation.
- **EMO overlap: high.** DAC's calibration case is the ozone regime, which this book already assesses. RDL v0.4 is waiting for this project's component data (`docs/RDL_V04_PROTOCOL.md`).
- **What EMO adds:** dated warning→policy→delivery lags computed from open data by open code and re-run weekly (`analysis/dac_ozone.py`, `analysis/dac_compare_ozone_climate.py`). Not a new question. Whether the book already reports comparable lags is **[unverified]**.

### E5. Breitmeier, Young and Zürn (2006): the International Regimes Database (IRD)

- **Opened:** library catalogue record only: https://library.usi.edu/record/411969. No abstract, no full text.
- **Citation (from the record):** Breitmeier, H., Young, O. R., Zürn, M. (2006). *Analyzing International Environmental Regimes: From Case Study to Database*. MIT Press.
- **What it measures, how, coverage:** **[unverified]**. The title states that case-study knowledge was coded into a database. Number of regimes and variables not seen.
- **EMO overlap:** likely high, as for E4. RDL v0.4 waits on IRD data too.
- **What EMO adds:** same as E4, if at all.

### E6. Breitmeier, Underdal and Young (2011)

- **Opened:** article page with abstract: https://academic.oup.com/isr/article/13/4/579/1798366
- **Citation:** Breitmeier, H., Underdal, A., Young, O. R. (2011). The effectiveness of international environmental regimes: comparing and contrasting findings from quantitative research. *International Studies Review* 13(4): 579–605. doi:10.1111/j.1468-2486.2011.01045.x
- **What it measures:** compares findings on regime effectiveness from the Oslo-Seattle and IRD datasets; examines power distribution, pushers and laggards, decision rules, depth and density of rules, problem knowledge. Uses statistics and QCA. Concludes that regimes do make a difference.
- **How effectiveness is operationalised:** not in the abstract **[unverified]**.
- **EMO overlap:** high. This is quantitative work on the same question DAC asks ("did the regime deliver?"), with a larger sample than EMO's two cases.
- **What EMO adds:** as E4. EMO has 2 coded cases (ozone, climate); these datasets have more. EMO should use them, not claim a gap.

### E7. COVID-19 response trackers: OxCGRT

- **Opened:** Hale et al. (2021), full PDF: https://www.nature.com/articles/s41562-021-01079-8.pdf
- **Citation:** Hale, T., Angrist, N., Goldszmidt, R., Kira, B., Petherick, A., Phillips, T., Webster, S., Cameron-Blake, E., Hallas, L., Majumdar, S., Tatlow, H. (2021). A global panel database of pandemic policies (Oxford COVID-19 Government Response Tracker). *Nature Human Behaviour* 5: 529–538. doi:10.1038/s41562-021-01079-8
- **What it measures:** 19 daily policy indicators (containment, economic, health), and four indices (e.g. Stringency) as unweighted averages of rescaled indicators, 0–100.
- **How:** ~400 volunteer coders, 88 languages, public sources, every data point checked by a second coder.
- **Coverage:** 180+ countries, subnational for several, from 1 Jan 2020.
- **Stated limits:** does not measure implementation, compliance or effects.
- **EMO overlap:** OxCGRT records the timing of policy after a warning, which is DAC's "warning→policy" leg, for one hazard, at far greater scale. Its double-coding protocol is the model for EMO's planned second coder (session 11).
- **What EMO adds:** the "policy→delivery" leg (a physical outcome series), which OxCGRT explicitly does not measure. EMO has not done this for COVID.

### E8. Early-warning effectiveness reviews

- **Opened:**
  - WMO press release on the *Global Status of Multi-Hazard Early Warning Systems 2025*, 12 Nov 2025: https://wmo.int/node/37886. The report itself was **not opened**.
  - Lloyd's Register Foundation, Kumah (7 Jan 2026), on its systematic review in progress: https://www.lrfoundation.org.uk/news/building-the-evidence-on-effective-early-warning-systems
  - Yore, R., Faure Walker, J., *Early Warning Systems and Evacuation: Rare and Extreme vs Frequent and Small-Scale Tropical Cyclones in the Philippines and Dominica*, doi:10.1111/disa.12434 (journal and year not shown on the opened PDF; *Disasters* is inferred from the DOI **[unverified]**): https://discovery-pp.ucl.ac.uk/10094019/1/EWS%20Paper.pdf
- **What they measure:** Global Status: countries reporting MHEWS (119, 60%), comprehensiveness scores across four pillars, tracked against Sendai Target G; reports mortality nearly six times lower where systems are more comprehensive, and a rise in evacuees. Lloyd's: states that no systematic review yet synthesises the evidence on effectiveness; its own (PRISMA, OSF-registered) has no results yet. Yore & Faure Walker: nearly all residents received warnings, most did not take the safest action (survey, 315 and 177 households).
- **EMO overlap:** the warning-to-action question is studied, but mostly by surveys and cross-country association.
- **What EMO adds:** τ_I from NHC track errors (`analysis/information_time_nhc.py`) measures forecast skill over time, which forecast verification already does routinely **[unverified: verification literature not searched]**. EMO adds nothing on warning-to-action yet (GWI untested; session 6).
- **Gap status:** the claim "early-warning communities only patchily track how warnings change behaviour" is supported by the Lloyd's statement and by the Global Status press release, which reports coverage and mortality association, not behaviour.

### E9. Earth System Governance Project: indicator work

- **Opened:**
  - Science and Implementation Plan (Biermann et al. 2009, ESG Report 1 / IHDP Report 20), page: https://www.earthsystemgovernance.org/publication/earth-system-governance-people-places-and-the-planet-science-and-implementation-plan-of-the-earth-system-governance-project/
  - Biermann, van Driel, Vijge, Peek (2020), "Governance Fragmentation", ch. 8 in Biermann & Kim (eds.), *Architectures of Earth System Governance*, Cambridge UP; abstract only: https://www.cambridge.org/core/books/abs/architectures-of-earth-system-governance/governance-fragmentation/E75F6E9F162E2F79FA9506097A34D9A5
- **What they measure:** the plan sets research questions (architecture, agency, adaptiveness, accountability, allocation) and, as opened, defines no quantitative indicators. The fragmentation chapter treats fragmentation as a variable for comparative research; its abstract names no index.
- **Not opened:** Pattberg et al. (2014) on measuring fragmentation and Kim (2013) on network structure, cited by the chapter **[unverified]**. Any later ESG indicator set: **not found** in one search; this does not show none exists.
- **EMO overlap:** EMO's "organismal vs fragmented" framing is close to the fragmentation concept, which ESG research already defines and studies.
- **What EMO adds:** the organismality plane (`analysis/organismality_plane.py`) uses two global outcome series (co-authorship share, conflict deaths), not institutional structure. Whether that measures fragmentation in the ESG sense is untested.

## Not opened / flags

- Full texts of Miles et al. 2002, Breitmeier et al. 2006 and 2011 (catalogue records and abstract only). Adrian has no access; the 2006 book costs about €74. Not bought: the white papers no longer claim a gap that depends on them.
- Sovereign ESG portal itself; Global Status of MHEWS 2025 report. (WGI 2025 methodology: opened 23 Oct, supplied by Adrian.)
- Pattberg et al. 2014; Kim 2013; any ESG Project indicator set beyond the two items above.
- Forecast-verification literature (relevant to τ_I) and science-of-science work (relevant to a white-paper claim): not in this session's list, not searched.

## Gap register: white papers and README

Each "gap" sentence found by search (`gap|missing|lack|only project|uniqueness|do not answer`) and what was done. Files: `WHITEPAPER_EMO_v1_funders.md` (v1.0), `WHITEPAPER_EMO_v1_1_funders.md` (v1.1), `WHITEPAPER_EMO_v1_Why_EMO_Must_Run_Continuously.md.docx` (docx).

| # | Claim (where) | Backed by | Action |
|---|---|---|---|
| G1 | No instrument tells how well the species thinks and acts in response; EMO is "that missing instrument" (v1.0, v1.1 §1; docx ¶14–16) | Contradicted by E1, E3, E4–E7 | Removed; replaced with a pointer to this file |
| G2 | Section "2. The gap: …" heading (all three) | — | Retitled "2. Context" |
| G3 | Existing systems "do not answer" OI, SΦ, GWI, SMF, τ_I, M_E (v1.0, v1.1 §2; docx ¶37) | Partly: physical-risk systems are not built for these; but E4–E7 address response; most EMO metrics are untested | Reworded as questions EMO asks, with pointer to this file and README |
| G4 | "Without a species-mind diagnostic, we are flying blind… EMO exists to close that gap" (v1.0, v1.1 §2) | No entry | Removed |
| G5 | "Each major initiative builds its own partial cognitive indicators"; DestinE tracks only its own skill and uptake (docx ¶43–44) | No entry (DestinE not searched) | Removed |
| G6 | Early-warning communities track behaviour change only patchily (docx ¶45) | E8 | Kept, cited to this file |
| G7 | Science-of-science does not couple to planetary risk (docx ¶46) | No entry | Removed |
| G8 | "No one is responsible for the top layer… EMO is that missing layer" (docx ¶47) | No entry | Removed |
| G9 | Semantic-efficiency view "currently missing from major dashboards" (v1.0, v1.1 §4.3) | No entry; M_E not run on real data | Removed |
| G10 | §7.3 Uniqueness: "the only project that…" (v1.0, v1.1) | No full search; E9 shows related framing | Removed; replaced with pointer |
| G11 | "The missing piece is a continuous instrument…" (v1.0, v1.1 §9) | No entry | Reworded without gap claim |
| G12 | Cognitive layer that twins and dashboards "have been missing" (docx ¶228) | No entry | Reworded |
| — | EW4All "critical gaps remain" in coverage (v1.0, v1.1 §1, §4.2; docx ¶13, 36, 153) | E8 (WMO release reports critical gaps) | Kept: an external fact about coverage, not an EMO gap claim |
| — | "reconstructs … and quantifies the gaps" (v1.0, v1.1 §4.2) | n/a | Kept: describes a feature (lags), not a literature gap |
| — | README | No gap sentences found | None |

The white papers remain scheduled for full rewrite (session 15); this session only removed or backed gap sentences.
