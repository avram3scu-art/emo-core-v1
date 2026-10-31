# Benefit feasibility (H9) — session 3.7, 31 Oct 2026

Serves **H9** (`docs/PLAN.md` §0; `docs/STRATEGY_3_0.md` §3, §5): *events whose loop runs faster (shorter warning → decision lag) have smaller losses than severity explains*; "cannot be tested" (not FAIL) if no usable loss data. Evidence class of this file: **infrastructure** (documentation review). Nothing here is a result.

**No record was opened.** Only documentation, terms, schema and news pages were read. No stream record, loss record, aggregate, appeal, field report or EM-DAT row was fetched or opened. Several pages could not be fetched (session allowlist, §6); what depends on them is marked **unverified**.

**Simulation of benefit:** none was attached in this session, so nothing was committed (CLAUDE.md, *Benefit is earned*). If Adrian supplies it later, it is committed unchanged, labelled exploratory, with its origin.

## 1. What H9 needs from a loss source

1. **Per-event** losses (deaths, affected, displaced, or money), not yearly totals.
2. **Joinable** to a loop card (`docs/LOOP_CARD_PROTOCOL.md` §4: GLIDE or other explicit key, else ISO3 + hazard class + onset window).
3. **Coverage** of the card population: natural hazards, worldwide, **no EU27** (E1), cards with a GO appeal or CEMS activation.
4. **Delay** short enough to score cards from a prospective window within about 18 months.
5. **Licence** allowing EMO to compute and publish a statistic (not the records).
6. **Independence**: the loss figure must not be produced by the response it judges, and the source's inclusion rule must not depend on the decision rung. Otherwise "faster decision ↔ smaller loss" is partly built in.

## 2. Sources, one verdict each

| Source | Verdict for H9 outcome | Main reason |
|---|---|---|
| EM-DAT (offline) | **use with conditions** (the only candidate) | global, per event, deaths/affected; but access terms for an unaffiliated individual, no redistribution, and an inclusion rule that partly depends on the response |
| DesInventar / DesInventar Sendai | **reject** | data licence not found; per-country, update dates not shown; being succeeded by DLDT (no launch date) |
| IFRC GO field reports | **reject as outcome; record as secondary only** | figures entered by the same system whose appeal is the decision rung (not independent) |
| IFRC appeal documents (EPoA, operation updates, final reports) | **reject** | written by the responder; PDFs, no stable field; timing unverified |
| USGS PAGER (modelled losses) | **use as severity covariate, never as outcome** | computed from shaking, population and vulnerability within ~30 min, before any response |
| IDMC displacement (IDU/GIDD) | **not usable now** (licence unverified) | per event, disaster-only; licence "none stated"; terms page not reachable |
| National loss databases (NCEI Storm Events; billion-dollar list, now Climate Central) | **reject** | US only; US events rarely carry an IFRC appeal or a non-EU CEMS activation, so almost no overlap with cards |
| Sendai Framework Monitor | **reject** | national official reporting; event-level data sit in national databases, not in the Monitor; delay and per-event access not documented on pages opened |
| Insured-loss sources (PERILS; Munich Re NatCatSERVICE; Swiss Re sigma; Aon) | **reject** | PERILS covers mostly high-income countries outside the card population and sells per transaction; Munich Re page not reachable; reinsurer reports give selected events only |
| OCHA FTS | **reject as loss source** | it records money flows (a response rung), not losses (`docs/STREAM_DATA.md` §2.6) |

### 2.1 EM-DAT (CRED, UCLouvain), offline

- **Coverage and fields:** natural and technological disasters worldwide. Entry if any one of: ≥ 10 deaths (dead and missing), ≥ 100 affected/injured/homeless, **or a call for international assistance or an emergency declaration, which alone is enough** ([entry criteria](https://doc.emdat.be/docs/protocols/entry-criteria/)). Economic fields: total damage, insured damage (usually from reinsurer reports such as Munich Re, Swiss Re, Aon), reconstruction costs; economic losses are largely under-reported and mostly available for high-impact events in insured countries ([economic impact variables](https://doc.emdat.be/docs/data-structure-and-content/impact-variables/economic/)). So for H9 only deaths and affected are usable; damage is too sparse in the card population.
- **Delay:** events are encoded daily but published only after an entry criterion is met and two sources confirm; public changes appear in the weekly update; each year's events are reviewed again at the start of the following year, and figures may change ([protocols](https://doc.emdat.be/docs/protocols/_print)). Public data updated weekly as `.xlsx` after login; no API on the page ([data accessibility](https://doc.emdat.be/docs/data-accessibility/)). **Consequence:** score only after the annual review of the window's last year (events of 2027 → early 2028).
- **Licence:** no copying or distribution of the database or a substantial part; no derivative or substitute databases; proper citation required; free only for academic organisations, universities, non-profit research institutions, international public organisations, national governments and media; **any other entity is treated as commercial use** (paid licence) ([terms of use](https://doc.emdat.be/docs/legal/terms-of-use/)). Publishing aggregate statistics is not addressed. The 2026 roadmap keeps free non-commercial access and adds a premium tier ([roadmap 2026](https://www.emdat.be/news/2026/01/roadmap-2026/)).
- **Join to a card:** GLIDE where present (EM-DAT raised GLIDE-linked events in 2025, `docs/STREAM_DATA.md` §3), else the frozen fallback F2 (ISO3 + hazard class + onset window). A new edge rule would be a 3.7b protocol item, frozen before any join.
- **Independence:** **partial.** EM-DAT is compiled by a third party (CRED) from OCHA, governments, research institutes, NGOs, press and reinsurers ([protocols](https://doc.emdat.be/docs/protocols/_print)); it does not run the response. But (a) an appeal alone can admit an event, so the decision rung partly selects the sample; (b) some human-impact figures come from responder reports. Remedy in 3.7b: restrict to events with deaths ≥ 10 or affected ≥ 100 (so the appeal criterion is not needed), and state (b) as a limit.
- **Continuity risk:** USAID funded about 90 %; the grant ended in 2025; new funders "nothing on paper yet" in June 2026 ([Resilience/Carbon Brief, 2 Jun 2026](https://www.resilience.org/stories/2026-06-02/trump-aid-cuts-could-close-database-storing-worlds-memory-of-disasters/)). A 2028 scoring date depends on EM-DAT still existing.
- **Verdict: use with conditions** — C1 written confirmation from CRED that Adrian, an unaffiliated individual doing non-commercial research, may use the free access (his status is not one of the listed free categories); C2 written confirmation that publishing aggregate statistics (a coefficient, n, counts by stratum, never per-event values) is allowed; C3 EM-DAT still running at scoring; C4 Adrian's account and download done by him (his decision).

### 2.2 DesInventar / DesInventar Sendai (UNDRR)

- **Coverage and fields:** national disaster loss databases; per-record deaths, injured, missing, affected, houses destroyed/damaged, evacuated, relocated, losses in USD and local currency, crops, cattle, roads; a `glide` field "if available"; downloaded per country ([Monty DesInventar](https://ifrcgo.org/monty-stac-extension/model/sources/DesInventar/)). The UNDRR server page cites 65 datasets for 82 countries and 3 states for GAR 2015, with no update dates; the software is Apache-2, **no data licence stated** ([desinventar-api.undrr.org](https://desinventar-api.undrr.org/)).
- **Delay:** not documented; national update cycles vary (unverified).
- **Successor:** UNDRR, UNDP and WMO develop **DLDT**, intended to succeed DesInventar, aligned with WMO's hazardous-event catalogue; no launch date, no data terms ([UNDRR DLDT](https://undrr.org//node/76608)).
- **Join:** country serial; GLIDE sometimes; else F2.
- **Independence:** national authorities record losses; they are also often the decision-maker (unverified per country).
- **Verdict: reject now.** Revisit when DLDT publishes terms and event IDs.

### 2.3 IFRC GO field reports

- **Fields:** `num_dead`, `num_injured`, `num_missing`, `num_affected`, `num_displaced`, `num_assisted`, each also as `gov_` and `other_` variants; `report_date`, `start_date`, `created_at`, `event_id`, `status`, `visibility` ([GO table api_fieldreport](https://ifrcgo.org/database-diagram/tables/api_fieldreport.html)). Who fills the form and when: the GO wiki page did not render (unverified).
- **Licence:** none stated; written reuse request sent 30 Oct 2026 (`docs/STATUS.md`).
- **Join:** `event_id` — the same key as the card's GO appeal (K-link, no fallback needed).
- **Independence:** **none.** Reports are entered in the system whose appeal is the decision rung, and reporting effort itself follows the response. A faster appeal may also produce earlier, lower initial counts.
- **Verdict: reject as the outcome.** Usable only as a secondary, labelled "responder-reported", and only the `gov_` figures.

### 2.4 IFRC appeal documents

Emergency Plans of Action, operation updates and final reports are written by the responder and published as PDFs; no field-level documentation was opened and their timing is **unverified**. **Verdict: reject** (not independent, not machine-readable).

### 2.5 USGS PAGER

Results generally within 30 minutes; estimates shaking, exposed population and ranges of fatalities and economic loss from ShakeMap, LandScan and country loss models; the alert level is an *output* that suggests a response level; estimates are revised as data arrive ([PAGER background](https://earthquake.usgs.gov/data/pager/background.php)). Licence not stated on that page (unverified). Already ingested (`docs/STREAM_DATA.md` §2.1).
**Verdict: severity covariate for EQ cards only, never the outcome.** Earthquake deaths happen within minutes of onset, before any decision; so H9 cannot apply to EQ deaths at all (§4).

### 2.6 IDMC displacement (IDU, GIDD)

Per event: name, dates, ISO3, hazard codes, figures by type (displaced, evacuated, deaths, …); disaster events only; source event ID, no GLIDE as event ID; **licence "none stated by the source (checked 2026-07)"** ([Monty IDU](https://ifrcgo.org/monty-stac-extension/model/sources/IDU/)). IDMC's own terms page was not reachable (§6). **Verdict: not usable now.** If IDMC's terms allow it, displacement could be a second outcome in a later protocol.

### 2.7 National loss databases

- NOAA NCEI Storm Events Database: the FAQ page opened gave no delay, licence or scope ([FAQ](https://www.ncei.noaa.gov/stormevents/faq.jsp)); US scope from the database name and NWS origin.
- US billion-dollar disasters: retired by NOAA in May 2025, revived by Climate Central (US only, ≥ $1 bn) ([WRKF, 6 Nov 2025](https://www.wrkf.org/2025-11-06/a-tool-tracking-billion-dollar-disasters-is-active-again-after-being-retired-by-trump-administration)).
- **Verdict: reject.** The card population needs a GO appeal or a non-EU CEMS activation; US events almost never have either, so overlap is near zero. Other national databases: not searched one by one (Scope; DesInventar covers the national-database route).

### 2.8 Sendai Framework Monitor

UNDRR's GAR states national loss databases should be disaggregated "by event, hazard and geographic area" as a minimum; Monitor reporting relies on officially endorsed national data; no reporting delay or per-event access is stated ([GAR 2019 ch. 9](https://gar.undrr.org/chapters/chapter-9-review-efforts-made-member-states-implement-sendai-framework.html)). **Verdict: reject** (the per-event layer is the national databases, §2.2).

### 2.9 Insured-loss sources

- **PERILS:** industry loss index for bushfire, earthquake, windstorm, flood, hail, tropical cyclone, volcano in Australia, Canada, Western Europe, Italy, Japan, New Zealand, Turkey; first report six weeks after the event, updates at 3, 6, 12 months, closing by 36 months; per-transaction licence ([PERILS ILIS](https://www.perils.org/products/industry-loss-index-service)). Almost no overlap with non-EU27 cards with an appeal; paid.
- **Munich Re NatCatSERVICE:** page not reachable (§6); terms unverified.
- **Swiss Re sigma, Aon:** not opened; EM-DAT names them as its insured-damage sources (§2.1).
- **Verdict: reject.** Insured losses exist mainly where insurance is common, which is the opposite of the card population.

## 3. Overall verdict

**Two different claims hide in "EMO reduces losses or helps an institution". They have different answers.**

**(A) H9 as registered — association: faster loops go with smaller losses beyond severity.** **Can be registered as a prospective test, with conditions.** Only EM-DAT supplies independent-enough, per-event, global losses for the card population. Proposal for the 3.7b protocol (not registered here; every number below is a draft):

- **Population:** closed loop cards (180 days), onset after the 3.7b commit until 31 Dec 2027, hazard **TC or FL only** (the only classes where a decision can come before most harm; EQ and TS deaths precede any decision, DR has no fallback join), non-EU27, anchored, with a decision record.
- **Exposure:** lag warning → decision, else onset → decision (as the card defines it), in days.
- **Outcome:** EM-DAT total deaths, and total affected as a second outcome (two tests, corrected), restricted to events admitted by deaths or affected thresholds.
- **Severity:** for TC, GDACS alert and exposed-population fields at the earliest snapshot; for FL, GDACS fields only if available before the decision (field choice from the 3.4b schema check; no values seen).
- **Statistic:** one pre-specified model (e.g. negative-binomial regression of deaths on log lag with log exposed population and hazard), one-sided, clustered by country, permutation or cluster-robust null; equivalence bound for any "no effect" reading.
- **Score date:** after EM-DAT's annual review of 2027 events (expected early 2028; set to on or after 1 Apr 2028).
- **What leaves:** the coefficient, its interval, n and counts by stratum; never an EM-DAT value per event (terms, §2.1).
- **Power:** from synthetic data in 3.7b. Rough size: the stream estimate is 8–15 linked events a month for all hazards (`docs/STREAM_DATA.md`); TC + FL non-EU27 cards with an EM-DAT match over ~13 months may be roughly 40–100 (a guess, unverified). Power may be below 0.5; then the protocol says so in its first line.
- **Known bias, stated in advance:** worse events tend to get faster appeals (severity drives speed), and severity is only partly measured. This pushes the association *against* H9. A null result is therefore weak evidence; a positive result survives this bias but is still not causal.
- **Gates before registration (C1–C4, §2.1):** CRED's written answers on individual access and on publishing aggregates are needed before 3.7b can register; without them H9 reads **"cannot be tested (no usable loss data)"**.

**(B) "EMO reduces losses or helps an institution."** **Cannot be tested from loss data.** EMO is in no response loop today: no body receives or acts on a card, so no loss can be caused by EMO, and (A) says nothing about EMO itself. A causal test would need some bodies to use cards and comparable ones not to, over many events; that is not feasible for this project in the coming years. The only honest route is the one already planned: **a user's written statement** (session 3.10) that a named body used a card or profile and what it did with it. That earns "helps an institution" (reported use), never "reduces losses" (CLAUDE.md, *Benefit is earned*).

## 4. Limits of this review

- Earthquake and tsunami deaths occur before any decision; for these hazards H9 has no mechanism and is excluded, not tested.
- Losses are counted, revised and partly reported by responders everywhere; no source is fully independent of response.
- Card public status: once the mirror shows cards, their data count as opened (CLAUDE.md 3.0); 3.7b must register before the window opens and use only events after its commit.
- Coverage of the source list: insurer reports (Swiss Re, Aon), national databases other than the US, and IFRC appeal-document schemas were not opened (§6).

## 5. Next step

Session 3.7b: (1) Adrian sends two written questions to CRED (individual non-commercial access; publishing aggregate statistics only) — texts drafted by Claude; (2) after the answers, register the (A) protocol with synthetic power, or record "H9 cannot be tested" with the reason. No EM-DAT file is downloaded before the protocol commit.

## 6. Sources opened (all on 31 Oct 2026)

| Source | URL | Used for |
|---|---|---|
| EM-DAT entry criteria | https://doc.emdat.be/docs/protocols/entry-criteria/ | inclusion rule (appeal alone qualifies) |
| EM-DAT terms of use | https://doc.emdat.be/docs/legal/terms-of-use/ | licence, free categories |
| EM-DAT data accessibility | https://doc.emdat.be/docs/data-accessibility/ | weekly update, xlsx, no API |
| EM-DAT protocols (print) | https://doc.emdat.be/docs/protocols/_print | sources, timing, annual review, revisions |
| EM-DAT economic impact variables | https://doc.emdat.be/docs/data-structure-and-content/impact-variables/economic/ | damage fields, under-reporting |
| EM-DAT roadmap 2026 | https://www.emdat.be/news/2026/01/roadmap-2026/ | funding end, access tiers |
| Resilience (Carbon Brief), 2 Jun 2026 | https://www.resilience.org/stories/2026-06-02/trump-aid-cuts-could-close-database-storing-worlds-memory-of-disasters/ | continuity risk |
| Monty DesInventar model | https://ifrcgo.org/monty-stac-extension/model/sources/DesInventar/ | DesInventar fields, GLIDE field |
| UNDRR DesInventar server | https://desinventar-api.undrr.org/ | coverage note, software licence |
| UNDRR DLDT | https://undrr.org//node/76608 | successor system |
| IFRC GO field report table | https://ifrcgo.org/database-diagram/tables/api_fieldreport.html | field names |
| GO wiki field report form | https://go-wiki.ifrc.org/en/user_guide/Field_report_form | did not render (metadata only) |
| USGS PAGER background | https://earthquake.usgs.gov/data/pager/background.php | timing, inputs |
| Monty IDMC IDU model | https://ifrcgo.org/monty-stac-extension/model/sources/IDU/ | IDU fields, licence none stated |
| IDMC GIDD about | https://internal-displacement.org/database | no terms on page |
| NCEI Storm Events FAQ | https://www.ncei.noaa.gov/stormevents/faq.jsp | no delay/licence stated |
| WRKF, 6 Nov 2025 | https://www.wrkf.org/2025-11-06/a-tool-tracking-billion-dollar-disasters-is-active-again-after-being-retired-by-trump-administration | billion-dollar list status |
| UNDRR GAR 2019 ch. 9 | https://gar.undrr.org/chapters/chapter-9-review-efforts-made-member-states-implement-sendai-framework.html | Sendai Monitor, event disaggregation |
| PERILS ILIS | https://www.perils.org/products/industry-loss-index-service | coverage, timing, licence model |

**Not reachable (session allowlist):** EM-DAT public table columns (https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/, first attempt; field names therefore unverified), IDMC terms (https://internal-displacement.org/terms-of-use/), Munich Re NatCatSERVICE (https://www.munichre.com/en/solutions/for-industry-clients/natcatservice.html). Earlier-session sources used by reference: `docs/STREAM_DATA.md` (EM-DAT GLIDE update, OCHA FTS, stream volume estimate), `docs/LOOP_CARD_PROTOCOL.md`.
