# Second loop domain: feasibility check (session 2.11, H6)

Class: infrastructure (documentation check only; no event, forecast, attention or decision record is opened or counted). Criteria committed 29 Oct 2026, before any source was searched.

## 1. Criteria (fixed before searching)

A candidate domain is **feasible** only if public documentation shows all of C1, C2, C4 and C5; C3 is checked but expected to pass.

- **C1 Events:** an open, dated catalogue of events (start date, area), at least 10 years, refreshed at least yearly.
- **C2 Predict:** archived, dated official forecasts or warnings per event, so that a forecast before the event can be matched to it.
- **C3 Attend:** Wikipedia pageviews (from July 2015) on per-event or per-topic articles.
- **C4 Decide-act:** an official, dated, public record of a decision taken in response to each event (declaration, activation, application), with the event it answers named, so that a lag (event date → decision date) can be measured.
- **C5 Size:** the documentation implies at least 5 events per year with a C4 record, so that pooling with hurricanes (about 2 measured storms per season, `docs/LOOP_PROTOCOL.md` §20.5) can raise H4 power.

Each criterion is marked pass / fail / unverified, with the source opened. Unverified counts as not shown. Verdict: feasible / infeasible / feasible pending (named unverified items).

Candidates, in this order: (A) floods in the EU; (B) heatwaves in the EU.

## 2. Sources opened and findings

All sources were opened 29 Oct 2026 (WebFetch), documentation only. No record was counted.

### (A) Floods in the EU — verdict: **feasible pending** (C1, C5 unverified; one design risk)

- **C1 Events: unverified.** CEMS Rapid Mapping activations carry an event onset (`eventTime`, distinct from `activationTime`), country and hazard, from 2012, through a public JSON API with no authentication [S1]. That covers only events that someone activated, so it cannot be the event set (see risk). No independent dated flood catalogue was opened (EM-DAT not opened: unverified).
- **C2 Predict: pass.** EFAS bulletins list each notification with type (formal/informal/flash flood), forecast date, issue date, lead time, river or region, and country. Feb–Mar 2019 had 9 flood and 185 flash-flood notifications [S2]. The web notification archive did not render for the fetch tool [S3]; the bulletins are the usable archive.
- **C3 Attend: expected pass, not checked** (pageviews exist for any article from July 2015; per-flood articles not counted).
- **C4 Decide-act: pass for one record type.** CEMS activations are requested by national authorities and dated, e.g. France 1 June, Germany and Belgium 2 June 2016, for floods from about 31 May [S4]. There is no per-activation public list of EU Civil Protection Mechanism activations: the 2023 summary gives 66 activations (+50 Ukraine) across 14 categories, with no dates or per-hazard counts [S5]. EUSF: 126 applications 2002–2016 (75 approved), with an online list of interventions referenced but not opened [S6]; flood applications are dated by the Commission's proposals [S7]. Their lags run to months or years, a different loop speed.
- **C5 Size: unverified.** More than 1,000 CEMS activations since 2012 (rapid plus risk mapping, worldwide) [S8]; no split by year, hazard or EU was shown.
- **Design risk:** if events are taken from CEMS activations, every event has a decision by construction, and the lag is measured only on events that got one (selection on the outcome). An independent event list (EFAS formal notifications, or a flood catalogue) must define events, and CEMS activation is then the decide-act record, with "no activation" as a valid outcome.

### (B) Heatwaves in the EU — verdict: **infeasible** on the documentation found

- **C1 Events: fail (not shown).** No official dated EU heatwave catalogue was found. A dataset of annual heatwave summaries (Excess Heat Factor) appeared in search but was not opened, and annual summaries would not date events.
- **C2 Predict: not shown.** Heat-health warnings are national or subnational, run by national meteorological services [S9]. No cross-country archive was found.
- **C4 Decide-act: fail.** No public dated archive of heat-health action plan activations, national or cross-country, is named; the evidence base is surveys (WHO Europe 2019, HEAT-SHIELD 2019, SCORCH) [S9].

### Overall

EU floods are the only candidate. Two items must be checked before any loop protocol for floods: (1) the yearly count of EU flood CEMS activations (C5), and (2) an independent dated event list (C1). This check does not move H6 itself; it only says whether H6 can be tested in floods.

## 3. Sources (opened 29 Oct 2026)

- [S1] IFRC Monty STAC extension, CEMS Rapid Mapping source: https://ifrcgo.org/monty-stac-extension/model/sources/CEMS/ (reports "224 activations as of 2026-07" for its own ingest; this does not match [S8] and is not used as a count)
- [S2] EFAS Bimonthly Bulletin Feb–Mar 2019: https://european-flood.emergency.copernicus.eu/sites/default/files/bulletins-documents/2019/EFAS_Bimonthly_Bulletin_Feb_Mar2019.pdf
- [S3] EFAS notifications pages (did not render): https://european-flood.emergency.copernicus.eu/en/notifications?page=22 ; https://european-flood.emergency.copernicus.eu/en/node/1145
- [S4] CEMS news, 3 June 2016: https://mapping.emergency.copernicus.eu/news/copernicus-ems-rapid-mapping-activated-for-floods-in-france-germany-and-belgium/
- [S5] UCPM activations 2023: https://civil-protection-knowledge-network.europa.eu/news/world-eu-civil-protection-mechanism-activations-2023
- [S6] EUSF 2002–2016 evaluation terms of reference: https://ec.europa.eu/regional_policy/sources/evaluation/eusf_2002_2016/eusf_2002_2016_tor.pdf
- [S7] Commission newsroom, 27 Aug 2024 (six 2023 flood cases): https://ec.europa.eu/regional_policy/whats-new/newsroom/27-08-2024-commission-proposes-to-deliver-over-eur1-billion-to-help-italy-slovenia-austria-greece-and-france-recover-from-natural-disasters_en
- [S8] CEMS mapping statistics page: https://mapping.emergency.copernicus.eu/stats/
- [S9] Climate-ADAPT, heat-health warning systems: https://climate-adapt.eea.europa.eu/en/observatory/policy/national-policies/heat-health-action-plans/national-and-sub-national-warning-systems/
- Not opened (blocked by the allowlist): the EUSF interventions list PDF on ec.europa.eu.
