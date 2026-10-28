# EMO status

Updated at the close of every session. Plan: `docs/PLAN.md`. History: `docs/SESSION_LOG.md`.

## Current state (28 Oct 2026)

- **Plan position:** fix sessions before session 10. Done: F1–F8 (PPE case recoded, gap-filled and compared with the manuscript: `docs/DAC_PPE_COMPARISON.md`). Next: session 10 (mpox, `docs/PLAN.md`). Session 10 (mpox) after them (`docs/FIX_PLAN.md`).
- **Runs:** weekly run every Monday 07:41 Brussels via cron-job.org (token expires 26 Oct 2027). CI: tests (115), mypy, ruff, claim-word check.
- **Results on record:** README table, each with its evidence class; every test and run in `docs/RECORD.md`; sessions 1–8 in `docs/STATUS_ARCHIVE.md`.
- **Open A items (audits 26b, 27 Oct):** PPE case: closed in F8 (six files in the repo, compared; one type-(c) error corrected, no manuscript error found, four manuscript sources unnamed). SMF deciding condition tested in F5 (6 of 12 passes survive).
- **Adrian must do:** nothing now.

## Fix session F8.8 (2026-10-28, 14:14–15:07) — PPE comparison with the manuscript

**Done when met: yes.** `docs/DAC_PPE_COMPARISON.md` and record rows committed (63ab805, 7847c9e); CI 40702495491.

**Done**
- Freeze: six files frozen at 8ebcf9e (115 tests, profiles current), new side written out first (`data/dac_ppe/frozen_summary.md`, 7edcb3d); then Tables 2–5 opened. Figures 1–2 not in the repo (legends only; no images in the .docx).
- Comparison per item (same / overlapping / different, kinds a–d). Same: BE first delivery 46, all five BE paired lags, gloves, Pan Scope exclusion, identification under shared readings; five of six binding acts; NL order; EU binding act and stockpile delivery. Overlapping: FR, NL, SE deliveries; SE and DE orders. Different: BE binding act 53 vs 43 (a, b), DE first delivery 41–50 vs 51–52 (a, b; added source, "Mitte" convention), BE national-producer delivery (censored), EU joint-procurement delivery (no source in new pool).
- **Claude's mistake (type c):** the BE national-producer order of 20 Mar (Annex 5 row 742) had been omitted; added with a censored delivery; no lag changes; listed before/after.
- Data statement: every item citable from the new files with the new value; rules and F8.7-added sources stated; the manuscript's §4.3 "within six days" sentence does not hold and must be recomputed.
- Supporting Information opened afterwards (Adrian): only Table S1; Ärzteblatt 27 Mar reread: undated; no classification changes; no type (d) found.

**Open (each with reason)**
- Manuscript sources unnamed for BE binding act (43), DE delivery (51–52), SE lower bound (41), EU joint procurement (≥ 62). Reason: the manuscript's original event files were not recovered (F1); not decidable.
- Defence fabric masks (5 May) and Justice filters (row 1026) not coded. Reason: scope; no first event changes, fabric masks may fall outside the PPE definition.
- BE reading B rests on an ambiguous "option sur/commande" row. Reason: rule choice (§5 Belgium b), kept and labelled (Adrian accepted the recommendation by closing).

**Review and Adrian's answer:** recommended opening the Supporting Information (Adrian: "Open", 15:04), then close; Adrian "Close" (15:07).

**Next:** session 10 (mpox) per `docs/PLAN.md`. The manuscript's revision (recomputed cross-case sentence, data statement) is a separate task when Adrian chooses it.

## Fix session F8.7 (2026-10-28, 13:26–14:13) — PPE gap-filling

**Done when met: yes.** Tightened test passes; four gaps filled or recorded; changed files revalidated, profiles recomputed, committed (d266318, 16da3cb, 34df56b, 411e43d, efd0522, fa9957d); CI 40694120554.

**Done**
- Phrase tests: one per-document page check for all cases (probes: "p. 34"→"p. 340" and a swapped Annex page now fail).
- EU funding: amending budgets 1–2/2020 (17 Apr) add funds to a general civil-protection line whose remarks do not name PPE → context; funding stays missing (not fillable from legal acts).
- SE: SOU 2020:80 → first delivery to regions/municipalities 17–31 Mar (t0 + 47–61 d; was 31–61); order unchanged (Feb).
- DE: Bundesrechnungshof report to the Enquete-Kommission (12 Dec 2025) and BMG Beschaffungsstab report (4 Apr 2020) → first delivery to Länder/KVs 11–20 Mar (t0 + 41–50 d; was 29–88); first order two readings, A 28 Feb–9 Mar (t0 + 29–39), B 28 Feb–20 Mar (t0 + 29–50).
- BE: hearing records K022/K040 confirm 3M readings C and A, unresolved (sources added); first binding act = arrêté ministériel 23 Mar 2020 (Moniteur supplied by Adrian; t0 + 53 d; was missing).
- All added sources listed in `docs/DAC_PPE_CODING.md` §3/§5 with URL, access date, sha256 and reason (Adrian's decision of 28 Oct 13:24).
- **Claude's mistake:** commit 34df56b pushed with the claims check failing; CI run 40688904036 failed; fixed at once ("interim" added to the ordinal list), recorded.

**Open (each with reason)**
- An earlier Belgian federal PPE act is not excluded (only the Moniteur of 23 Mar ed. 2 opened; eJustice CAPTCHA). Reason: Adrian's decision whether to search further; low value (binding acts are recorded, not compared across cases).
- Conventions to state in the comparison: "Mitte" = days 11–20; the audit sentence read as naming the first recipients; German audit copy from the ULB Bonn legal deposit. Reason: method choices, recorded in §5.

**Review and Adrian's answer:** recommended close; Adrian supplied the Moniteur (14:09), then "Close" (14:13).

**Next:** F8.8 — the pre-registered comparison (§4): open the manuscript's Tables 2–5 and Figures 1–2 only after all profiles are confirmed current; report every difference by kind; then session 10.

## Fix session F8.6 (2026-10-28, 13:12–13:22) — PPE recoding, EU

**Done when met: yes.** `data/dac_ppe/EU.json` validated, profile computed, both committed (5aa9bfb); CI 40686814637.

**Done**
- Regulation (EU) 2020/402 and Decision (EU) 2020/414 fetched from the Publications Office by CELEX (EUR-Lex reference-list URLs return a bot challenge) with sha256; EP photo record P-043686 rendered with headless Chromium, text committed (no stable sha256).
- EU.json (11 events): firm order missing (joint-procurement tenders and rescEU host-state purchases are context); binding act 2020/402, 14 Mar (t0 + 44 d); counter-measure German export ban, 4 Mar (t0 + 34 d); first delivery to member states 25 Apr (t0 + 86 d; Sénat p. 400, EP photo record); funding and permanent body missing. Rules §5 EU a–g dated before the profile. Phrase test with probe.
- **Claude's mistake: blindness breach 2.** The reference-list cut included the manuscript's figure legends; a grep printed both (EU first tender "not a firm order"; Belgian 3M lags). Recorded verbatim in §1; EU file classed known history; cut now ends before "# Figure legends".

**Open (each with reason)**
- EU first funding undated: the rescEU budget amendment (Apr 2020) is not in the reference list. Reason: Adrian's decision (sources outside the reference list), at the gap-filling sitting.
- Phrase tests check "p. N" as a substring of the source field; a wrong page can pass in multi-page rows. Reason: not attempted; first item of the gap-filling sitting (~15 min).

**Review and Adrian's answer:** recommended no more now, no rule change, page-check fix first in the gap-filling sitting; Adrian "Close" (13:22).

**Decision (Adrian, 28 Oct 13:24):** sources outside the manuscript's reference list may be used in the gap-filling sitting, each recorded as an addition (source, URL, access date, reason) in `docs/DAC_PPE_CODING.md` §3 and `docs/RECORD.md`; the comparison reports which items rest on added sources.

**Next:** gap-filling sitting (page-check fix; BE, DE, SE; EU funding from added sources); then the pre-registered comparison (§4); then session 10.

## Fix session F8.5 (2026-10-28, 11:40–12:10) — PPE recoding, Sweden

**Done when met: yes.** `data/dac_ppe/SE.json` validated, profile computed, both committed (4fb2dc6, 6c4328d); CI 40677711065.

**Done**
- SOU 2021:89 volym 1 fetched from regeringen.se (URL from the manuscript's reference list only) with sha256 88646b7c…, identical to Adrian's copy; per-page text committed.
- SE.json (17 events): first firm order window Feb 2020, Socialstyrelsen's "smärre inköp" (t0 + 2–30 d); binding act förordning 2020:126, 16 Mar (t0 + 46 d); first delivery to regions and municipalities window Mar 2020 from Figure 8.2 (t0 + 31–61 d); dedicated funding and permanent body missing (state grants cover several cost types: context); no pairs. Rules §5 Sweden a–h dated before the profile. Phrase test with probe.
- March bar of Figure 8.2 decomposed from the PDF's vector data (`scripts/se_figure82_march.py`): about 1.07 million items, all PPE.

**Open (each with reason)**
- Order and delivery have month precision only; SOU 2020:80 (first interim report, cited for Feb–Mar detail) could narrow them. Reason: scope (one source this session); added to the gap-filling sitting.
- Chapter 8 pp. 320–340 read in full, the rest keyword-searched; the two "missing" rows rest on that search. Reason: scope; recheck in the gap-filling sitting.
- First order coded Feb 2020 while the manuscript (§3.1, known) calls it undated: an expected rule difference at the comparison. Reason: known history, recorded.

**Review and Adrian's answer:** recommended no more now and SE added to the gap-filling sitting; Adrian "Close" (12:10).

**Next:** F8.6 — EU; then gap-filling sitting (BE, DE, SE); then the comparison; then session 10.

## Fix session F8.4 (2026-10-28, 11:26–11:32) — PPE recoding, Netherlands

**Done when met: yes.** `data/dac_ppe/NL.json` validated, profile computed, both committed (a33a179); CI 40672653150.

**Done**
- VWS *Feitenreconstructie, tijdlijn: Persoonlijke beschermingsmiddelen* (2021) fetched with sha256 (title and URL taken from the manuscript's reference list only); text kept in reading order.
- NL.json (18 events): first national order 6–9 Mar (t0 + 36–39 d); first delivery to ROAZ 21–22 Mar (t0 + 51–52 d), paired with an undated order (undatable pair); redistribution to care providers 13–20 Mar (t0 + 43–50 d, secondary); binding act, funding and permanent body missing. Rules §5 Netherlands a–g dated before the profile.
- Grey-text check (oral sources) in the PDF: all order, delivery and decision passages used are documented; two context rows grey, marked. Phrase test with probe.

**Open**
- The Dutch delivery day matches a value seen in the F8.3 breach; it is not an independent confirmation. Reason: known history (recorded in §1).

**Review and Adrian's answer:** recommended close; Adrian "Close" (11:32).

**Next:** F8.5 — Sweden (SOU 2021:89); then EU; then a gap-filling sitting (BE, DE); then the comparison; then session 10.

## Fix session F8.3 (2026-10-28, 11:10–11:25) — PPE recoding, Germany

**Done when met: yes.** `data/dac_ppe/DE.json` validated, profile computed, both committed (dc7fdf7); CI 40670748732.

**Done**
- Bundestag Drucksachen 19/21798 and 19/19047 fetched with sha256; six further answers and the federal government's procurement page scanned (no dated delivery). DE.json (13 events): first order and first delivery to Länder/KVs both windows 28 Feb–27 Apr (t0 + 29–88 d; no order or delivery dated in public sources); binding act: export ban 4 Mar (t0 + 34 d); funding and institutionalisation missing; Ärzteblatt (27 Mar) secondary context only; Sudhof not used. Rules §5 Germany a–d dated before the profile. Phrase test with probe.
- Adrian supplied the TRIS record of notification 2020/0104/D; committed and now the primary source of the export ban (profile unchanged).
- **Claude's mistake: blindness breach.** A whole-file grep of the manuscript printed four Results/Discussion sentences (DE/NL first-delivery days, Sweden's window, first orders ≥ day 29, German export ban as binding act); recorded verbatim in `docs/DAC_PPE_CODING.md` §1; DE/NL/SE classed known history; method fixed (reference list only).

**Open (each with reason)**
- German first order and delivery are 60-day windows. Reason: needs a gap-filling sitting before the comparison (BMG procurement reports to the Bundestag; KBV's own announcement of the first federal delivery), with the Belgian gaps (Moniteur belge, hearings); ~1–1.5 h.
- German unpaired order-to-delivery interval −59…+59 d (overlapping windows): reported as is.

**Review and Adrian's answer:** recommended close, gap-filling before the comparison, NL next; Adrian sent the TRIS record (11:22).

**Next:** F8.4 — Netherlands (VWS factual reconstruction 2021); then SE, EU; then a gap-filling sitting (BE, DE); then the comparison; then session 10.

## Fix session F8.2 (2026-10-28, 11:01–11:10) — PPE recoding, France

**Done when met: yes.** `data/dac_ppe/FR.json` validated, profile computed, both committed (45438bc); CI 40669471376.

**Done**
- Sénat report no. 199 (2020-2021) tome I fetched (sha256 identical to Adrian's copy); full text with page markers committed.
- FR.json (15 events): first firm order 28.4 M FFP2, readings A 7 Feb (request) / B 19 Feb (first validated purchase); 25 Feb order 170.5 M FFP2; binding act décret 2020-190 (3 Mar); funding arrêté 11 Mar (EUR 260 M for strategic stocks); first pharmacy delivery window 9–22 Mar; 30 Jan order excluded (single mission); institutionalisation missing; no paired orders. Rules §5 France a–c dated before the profile.
- Profile: first order t0 + 8 / 20 d; binding act t0 + 33; funding t0 + 41; delivery t0 + 39–52 d; unpaired first order → first delivery 31–44 d (A) / 19–32 d (B).
- Test: every Sénat citation's verbatim phrase is on its cited page (planted wrong page fails). Claim-check ordinal list extended.
- Claude's mistake, fixed before the profile: an unsourced lower bound on a context row (airlift); row removed.

**Open**
- Tome II (hearings) and Légifrance texts not opened. Reason: scope; the report cites decrees by number and date.
- Pharmacy-delivery lower bound rests on a request ('sollicités … pour une première livraison'). Reason: source limit; window kept wide.

**Decision (2026-10-28, 11:10, Adrian "Close" on Claude's recommendation):** Germany is coded from public Bundestag papers only; the Sudhof report (marked "VS – Nur für den Dienstgebrauch") is not used.

**Next:** F8.3 — Germany (public Bundestag papers; EU notification of the export ban); then NL, SE, EU; then the comparison; then session 10.

## Fix session F8.1 (2026-10-28, 10:53–11:00) — PPE recoding, Belgium

**Done when met: yes.** Coding rules committed before coding (c72013b); Belgian event file and order file validated and committed; CI 40668404946.

**Done**
- `docs/DAC_PPE_CODING.md`: blindness statement (Belgium coded with its key result known → pre-registered on known history; FR/DE/SE first orders known from §3.1), rules per sublayer, sources, comparison protocol; three rules added during coding, dated, before any profile (§5).
- Belgian Chamber report DOC 55 1394/002 fetched (sha256 identical to Adrian's copy), `scripts/fetch_dac_ppe_sources.py`; Annex 5 text committed (`data/sources/dac_ppe/BE_annex5.txt`).
- `data/dac_ppe/BE.json` (30 events), `BE_orders.csv` (9 rows: 7 orders, 3M under 3 readings), `BE_profile.json`; `scripts/dac_ppe_outputs.py`; tests: files valid, profile current, every cited row exists on its page with the event's date.
- Profile: first firm order t0 + 1 / 5 / 34 d (3M readings A/B/C); first delivery to municipalities 16 Mar (t0 + 46 d); paired lags surgical 5–6 d, FFP2 10–56 d, gloves 5 d; Pan Scope pair undatable (date contradicted in source); binding act, funding, institutionalisation missing.
- Claude's mistakes, fixed: two wrong row citations (row 65 was a cross-reference, row 44 guessed); citation test added (cannot tell apart two same-day rows on one page).

**Open (each with reason)**
- Moniteur belge not searched for a binding PPE act. Reason: scope (one source per sitting); before the comparison (~30 min).
- Hearing records cited by Annex 5 (mainly CRIV K022) not opened. Reason: scope; before the comparison (~45 min).
- 16 Mar municipal delivery is from one province, federal and provincial goods mixed. Reason: Claude recommended keeping it, flagged for the comparison.

**Review and Adrian's answer:** recommended close, France next; Adrian "Close" (11:00).

**Next:** F8.2 — France (fetch Sénat report no. 199, code FR); then DE, NL, SE, EU; then the pre-registered comparison; then session 10.

## Fix session F7 (2026-10-28, 10:34–10:51) — DAC clean-up

**Done when met: yes.** Tests pass (100; CI 40666225661; weekly 40666382346); D1–D6 fixed with tests; every ozone/climate t0 and binding-act row has a primary source; Identification row in.

**Done**
- DAC standard v1.1 (197654b): D1 version check, D2 unknown case keys, D3 missing/censored by sublayer and level (multi-level cases valid), D4 undatable pairs listed, D5 every t0 reading exact/window, D6 orders carry a level and intervals compare like with like; Identification row from Table S1 of the final manuscript (`good`, `case.identification`, per-good paired orders, order-date spread, `minimum_for_separation_met` per Proposition 1). Audit probe 5/5 ok.
- Old DAC code retired (913748f): `analysis/dac_ozone.py` now reads the standard file and prints lag ranges; `emo/metrics/dac`, `emo/harmonize`, three `emo/models` files and 12 tests deleted; DAC_METRICS.md archived.
- Primary sources (rules d3dced2 before opening; result 7cda800): Nature article page (Molina & Rowland, "Published: 28 June 1974"), NAP record (Charney, 1979), UN Treaty Collection (Montreal 16 Sep 1987; Kyoto 11 Dec 1997); `data/sources/dac_primary_sources.md`. Ozone lag now exact 4,828 d (was 4,642–5,006); climate 6,555–6,919 d unchanged.
- Manuscript Markdown copies by `scripts/docx_to_md.py` with source sha256; staleness test.
- Claude's mistakes, fixed: CSV rewrite changed quoting (reverted before commit); identification field name overclaimed Proposition 1 → `minimum_for_separation_met` (401c937).

**Open**
- Context rows of the ozone/climate files still cite Wikipedia. Reason: scope (they enter no lag; ~20 min later).
- Charney report dated to the year only. Reason: Adrian's decision not needed; recommended to keep (the PDF needs a login; the width does not change the contrast).

**Review and Adrian's answer:** more of F7: recommended no; Adrian "Close" (10:51).

**Next:** F8 (recode the PPE case from primary sources, 2–4 sessions); session 10 (mpox) after it.

## Fix session F6 (2026-10-28, 10:11–10:30) — method labels and the evidence-class rule

**Done when met: yes.** Labels in place; rules in CLAUDE.md, approved by Adrian ("Yes", 10:13).

**Done**
- RDL backtest, v0.3 and v0.4 docs labelled "pre-registered on known history, not blind" ("held-out" explained as the word used at the time); forecast ledger named the only blind RDL test; README, PLAN and page wording (02912f9).
- `docs/GWI_PROTOCOL.md` §6 note: condition 3 used a non-significant placebo as evidence; Fisher p optimistic under clustering; future GWI tests: direct test-vs-placebo difference on a block-permutation null, equivalence bound for any "no effect" claim, H ≥ 0.5 descriptive only.
- CLAUDE.md Science rules: one evidence class on every result (known-outcome tests never called held-out or blind); a pass needs a significance test of its deciding condition, with a dependence-respecting null, no point comparisons, no "non-significant = no effect" (dc0c1c3). RDL rule wording updated.
- GWI hurricane PASS caveat in README and page (decided by its significance condition only); page rebuilt and checked (40662610551).

**Review and Adrian's answer**
- More of F6: recommended no (RDL development passes were point comparisons on known cases, superseded by their FAILs; frozen RDL script docstrings keep "held-out", explained in the protocols). Adrian: "Close".
- Weakness: GWI calibration FAIL decided by point thresholds; FAIL stands (2.7× over). Future design in the GWI protocol note.
- Claude's mistakes: none found this session.

**Next:** F7 (DAC clean-up incl. validator gaps D1–D6; blocks session 10), then F8; session 10 after them.

## Fix session F5 (2026-10-28, 09:43–10:05) — SMF significance re-analysis

**Done when met: yes.** Result in `docs/SMF_PROTOCOL.md` §13; README and page follow it; frozen check includes SMF and synergy; M1 guard and its tests pass.

**Done**
- §13 protocol: draft (f4a4745), registered on Adrian's "go" (3f40146) with lags 11/11/13 (EIA) and 1/2/4 (SPF) instead of the prompt's h − 1 (reason in §13); code and tests before the run (4e3988c).
- **Result (6d0f142), pre-registered on known history:** 6 of 12 earlier passes survive Diebold–Mariano/Holm: EIA CO2 3 m, EIA electricity 3 m, SPF unemployment 1/2/4 q, SPF IP 1/2 q. Withdrawn: EIA CO2 6 m, EIA electricity 6 m, EIA IP 3/6 m, SPF IP 4 q.
- M1 guard: KPSS (1%) in `compute_smf`, warning + metadata, docstring corrected; fires on 5 of 15 recorded EIA inputs incl. the surviving EIA CO2 3 m (caveat now in README and page, Adrian "yes"). Recorded outputs unchanged (37cf6b9).
- Weekly frozen check: SMF §7–§13 and synergy added; openpyxl declared; weekly run 40659742858 on GitHub: all 15 frozen runs reproduce.
- Claude's mistakes, fixed: protocol count 10 → 12 of 15 (erratum before the run); an unverified explanation drafted and removed before commit; session-0 SMF signal control built on a random walk → stationary AR(1) (cb06b8a); CLAUDE.md index spec lacked F3's class column.

**Open**
- For the 5 flagged EIA samples the circular-shift null is not valid; a persistence-robust null (e.g. block bootstrap) would fix it. Reason: scope (new method work; Claude recommended later).

**Next:** F6 (method labels and the evidence-class rule), then F7, F8; session 10 after them.

## Fix session F3 (2026-10-28, 09:33–09:45) — records backfill

**Done when met: yes.** Every protocol result and recorded run of sessions 0–8 has a row in `docs/RECORD.md` (checked by script against every run ID and commit cited in STATUS/SESSION_LOG); no SESSION_LOG row has a placeholder.

**Done**
- `docs/RECORD.md`: 85 rows for sessions 0–8 plus a class column on every row (pre-registered blind / known history / exploratory / infrastructure), via `scripts/f3_backfill_record.py` (c05876c). 228 CI runs of Feb–Apr 2026 (old account, deleted code) summarised in one row.
- `docs/STATUS.md` split: current state on top; sessions 1–8 moved verbatim to `docs/STATUS_ARCHIVE.md`.
- `docs/SESSION_LOG.md` rewritten, one row per session, real commits; old rows in `docs/SESSION_LOG_ARCHIVE.md`.
- Claude's mistake, fixed: the claim check skipped untracked files locally (21 hits missed until staged); now `git grep --untracked`, tested with a probe (1689124). CI was not affected.

**Review and Adrian's answers**
- More of F3: recommended no (old CI runs and data-only weekly commits not indexed one by one).
- Backfilled rows rest on STATUS and commit messages, not on rereading each run log; one cause "not recorded" (21 Oct CI). Recommended: accept.
- RECORD on a phone: Adrian "Fine" (09:41).

**Next:** F5 (SMF re-analysis; Adrian answers "go" to the protocol), then F6, F7, F8; session 10 after them.

## Fix session F2 (2026-10-28, 09:02–09:40) — truth pass on public files

**Done when met: yes.** Claim grep 0 unjustified; banners and README approved by Adrian ("Yes", 09:08).

**Done**
- README: every result labelled [blind] / [known history] / [exploratory]; DAC row says the PPE case is not in the repo and the manuscript was not submitted ("under review" removed); SMF caveat (audit S1–S2); test count 91 from CI 40653907266 (a158c65).
- Dated "superseded" banner on both funder white papers (.md), the .docx white paper, `deck/`, `grants/`, `README_EMO.md`, `EMOStakeholderBenefits.md`; 11 "first" claims marked [unverified], 3 false statements marked [false].
- `docs/RDL_V0_1.md` corrected (RDL v0.1 is not operational; FastAPI deleted). Public page carries the SMF caveat (rebuilt and fetched, run 40654830115). PLAN "live data" → "weekly-run data".
- Old DAC docs moved to `docs/archive/` with a note.
- `scripts/claims_grep.py` → `docs/F2_CLAIMS_GREP.md` (251 hits, 0 unjustified at approval); added to CI as a failing check, tested with a planted claim (CI 40657324769 green on the clean tree).
- Rules added to CLAUDE.md (Adrian, 09:29): every question carries Claude's recommendation; Claude's mistakes fixed in full (c176b7d).

**Review and Adrian's answers**
- Claim check in CI: recommended yes → Adrian "Yes" → done.
- Open: the [blind] label on SMF (sequential tests, S2) and GWI (expected spikes) may be generous. Reason: scope (F6 decides evidence classes).
- Open: the README SMF line changes again after F5. Reason: scope (F5).
- Claude's mistake: hit count reported before the record row added one more; corrected in the same session.
- `docs/F2_CLAIMS_GREP.md` is a snapshot; CI regenerates the check on every push (the file is not kept current).

**Next:** F3 (records backfill), then F5, F6, F7, F8; session 10 after them.

**Decision (2026-10-28, 09:29, Adrian):** new CLAUDE.md rules: every question to Adrian states Claude's recommended option first with a one-line reason; Claude's own mistakes are always fixed completely, regardless of time or weekly allowance. Reason (Adrian): "There is far too much information for me … I am not an AI; you are."

## Fix session F1 (2026-10-28, 08:34–09:05) — DAC paper facts and files

- Committed with origin and sha256 (`docs/sources/dac_paper/README.md`): Futures submission FUTURES-D-26-00488 (conceptual DAC paper; submitted 17 Apr 2026, desk-rejected 18 Apr 2026); final DAC manuscript "Decision or Supply?" and its Supporting Information (Table S1 with the "Identification" row); Diagnosticity manuscript (not DAC) under `docs/sources/other_papers/`. The earlier JCCM manuscript, attached again, is byte-identical to the committed one.
- **Submission facts (Adrian, 28 Oct: "1 - NO"):** the DAC/PPE manuscript was **not submitted** to JCCM. README's "JCCM manuscript under review" is false (F2 fixes it). No letter to an editor needed.
- Final version vs committed one: a rewrite (identification result §2.2, Tables 1, 3, 4 new; profiles become Table 5).
- Its data statement says the six event files, the Belgian order file and the scripts are public with a persistent identifier: not true today.
- **Missing (by name):** PPE event files BE, FR, DE, NL, SE, EU; Belgian order file; scripts for Tables 2–5 and Figures 1–2; Figures 1–2; title page of the final version; full manuscript of the later revision (only §1 RQ, §2.7 Identification/Proposition 1 and §2.8 Table 1 were supplied, committed as fragments).
- Also supplied: Boyer et al. 2024 (IPMJ) landing page, recorded as a source (abstract only, 7e9f4ef).

**Closed 2026-10-28, 09:05. Done when met: yes** (every attached file committed and indexed; facts recorded; missing list above). Commits 33b34b1, 0293074, ef76d5a, 7e9f4ef and this one.

**Review and Adrian's answer**
- More of F1: only the event files; Adrian (09:01): "I don't know where the files are. Let's move on." → **F8 is required** (recode the PPE case from primary sources, 2–4 sessions) before the DAC paper can be submitted with its data statement.
- Change: README's "JCCM manuscript under review" and the PPE "works on real data" line are false → F2. The final manuscript's data statement is not true today → must be made true (F8) or changed before any submission.
- Claude's mistake: asked for "every file card" without saying which files were already in the repo; one duplicate upload.
- Adrian: "We need to fix everything, or improve it, before session 10."

**Not done**
- Event files, order file, scripts. Reason: Adrian's decision/files (not found) → F8.

**Next:** F2 (truth pass on public files), then F3, F5, F6, F7, F8; session 10 after them.

## Third audit (2026-10-27/28, extra work at Adrian's request)

- `docs/AUDIT_2026-10-27.md` (8573410): every recorded RDL, GWI, SMF and synergy result reproduces from committed data; new gaps D1–D6 (DAC validator; D3 blocks the mpox multi-level case), M1 (SMF null invalid on trending input), K1 (unpinned dependencies), W1 (fix plan stalled while extra work grows; all audit-26b A items open).
- T1 resolved 28 Oct: Adrian set network access to "All domains"; tests, ruff and mypy now run in Claude's workspace (d0b236e). Claude's advice: keep it while the repo holds only public material.
- **Decision (28 Oct, 08:22, Adrian "Yes"):** D1–D6 added to F7, M1 to F5 in `docs/FIX_PLAN.md`.
- Session 10 opened 27 Oct and stopped at its start: F1–F7 gate not cleared (Adrian chose "keep order"). F1 waits for Adrian's files.

**Next:** F1 (Adrian's files); if not available, F2 can run first.

## F4 follow-up (2026-10-27, 05:48–06:30): Adrian's "YES" to the review points

- All GitHub actions now run on Node 24 (upload-artifact v7, upload-pages-artifact v5, configure-pages v6, deploy-pages v5; ruff-autofix checkout v5 / setup-python v6). `include-hidden-files: true` keeps `site/.nojekyll`.
- Runners pinned to `ubuntu-24.04` in every workflow, so the Ubuntu 26 move of `ubuntu-latest` cannot change frozen outputs silently. Moving to Ubuntu 26 later is a deliberate change, checked by a weekly run.
- Tested: blocked weekly run on `f4-probe` uploaded its artifact with v7 (40451857575); weekly runs on emo-2026-10 passed (40451922643, then 40452754211 with no Node 20 warning left); 91 tests; page deployed.
- My shortfall: the first change missed configure-pages and deploy-pages (caught by the warning in run 40451922643, fixed in c19567b).

**Decision (2026-10-27, 06:35):** Adrian asked for a combined DAC/EMO/UIA/RDL paper "ready for publication". Claude stopped (CLAUDE.md: conflicts with the one-task rule and the F1–F7 gate; audit R1, S1, S3 and the He trigger make a combined paper unsupportable today). Adrian chose **keep order**: F1 → F2, F3, F5, F6, F7 → combined version as session 15 ("EMO: what runs today"), with editor review and no same-day sending.

**Not done**
- ~~Delete branch `f4-probe`~~ **Done by Adrian, 27 Oct 2026 07:44** (confirmed by the branch list: emo-2026-10, main, original-upload).

## Fix session F4 (2026-10-26, 21:15–21:40): CI readability — done when met: yes, except deleting the probe branch

- pytest results now appear as annotations in CI and in the weekly run: one error annotation per failing test (with its first error line) and the summary line as a notice.
- Proved with a deliberate failure on branch `f4-probe`: CI run 40394061138 and weekly run 40394065117 both showed "1 failed, 91 passed" and the FAILED line through the annotations API; the weekly run correctly blocked its commit.
- Test count recorded: **91 passing** (README fixed; it had 57 and 102 in two places).

**Not done**
- Delete branch `f4-probe`. Reason: Adrian's decision/permission — the session's proxy refuses branch deletion (HTTP 403). Adrian: GitHub → Branches → delete `f4-probe`.

**Review points**
- `actions/upload-artifact@v4` runs on deprecated Node 20 (warning in run 40394065117); upgrading is a one-line change, not tested here (scope).
- `ubuntu-latest` moves to Ubuntu 26 from 19 Oct 2026 (runner notice); frozen outputs could change with new library builds — the weekly frozen check would catch it.

**Next:** F1 (Adrian brings the DAC paper files), then F2, F3, F5–F7.

## Extra work, 26 Oct 2026 (20:30–21:10): test the test

Outside the session plan, at Adrian's request ("It's all about EMO"; yes to commit; "Do it" for the He calibration). Does not replace F1–F8.

- `analysis/test_the_test/`: Science of Truth trial-design simulations from today's chat, with origin and checksums (7bddd2b). Exploratory, synthetic.
- He direction test calibration: protocol (1039b08) → code (65a4a36) → single run → result in `docs/HE_CALIBRATION_PROTOCOL.md` §6. **Result:** the UIA §3 Option A sign rule gives 41–52% false positives at any n (unusable); the mean-τ permutation test (T-D) holds 5%; at the current trigger of 8 cases its power for a β = 0.5 effect is 0.34–0.55; usable (≥ 0.80) only at n = 30 in the grid.

**Decision applied (20:49, Adrian: "Record and apply everything necessary to EMO"):** He statistic = T-D; Option A rule retired; trigger 8 → 24 coded cases; 8–23 cases = pilot (`docs/UIA_PROTOCOL.md` §6, 727c500).
**Follow-up (20:41–21:15):** He calibration made a frozen run in the weekly check and reproduced exactly on GitHub (run 40389674340); unit test for the exact Kendall null; amendment 1 (grid n 22–28 and 40–60) pre-registered (7457d89) and run: T-D usable from 24 cases; weak links (β = 0.3) with a shared trend need more than 60. First amendment run aborted (no message), rerun identical on its common part; both on record.

**Open**
- Measure the shared trend among He letters on real data before choosing n for a weak-link test. Reason: scope (needs coded cases; part of session 12's pre-registration).
- Reaching 24 coded DAC cases: currently 2 (ozone, climate). Reason: needs time (DAC coding, sessions 10–11 and the second coder).

## Session 9 (2026-10-26, 14:41–16:05; closed 2026-10-27 08:15) — DAC standard

**Done when met: yes.** Tests pass in CI including malformed-file and per-rule rejections (CI 40334445714 on 3494540; first readable count, 91 tests, came later from F4).

**Done**
- `docs/DAC_STANDARD.md`, `docs/dac_event_file.schema.json`, synthetic `docs/dac_event_file_example.json`, validator and profile `emo/dac_standard.py` (profile per reading of contested dates: lag ranges per sublayer, paired and unpaired order-to-delivery intervals, missing and censored listed apart; no scalar, enforced by a test), tests `tests/dac_unit/test_dac_standard.py` (a89d48b → 3494540).
- Adrian's "1 – yes": ozone/climate converted to the standard (`scripts/convert_dac_csv.py`, `data/dac_{ozone,climate}_events.json`); check pre-registered (a4de996) before conversion; **PASS** (c70276e): 4,828 d ∈ [4,642; 5,006], 6,712 d ∈ [6,555; 6,919]. The year-precise warning dates widen each lag by 364 days; every t0 and binding-act source is secondary.
- Rules (Adrian's request): repository is the only memory; every test, run and attempt recorded in `docs/RECORD.md`; closing step 0 checks the record; PLAN.md opening/closing blocks updated (1b7b81d).
- Sources: reporting-standard table copied to `docs/sources/` (1b7b81d); DAC manuscript supplied by Adrian committed (de47250); 15 attachments checksummed and identified, `docs/sources/SOURCES_SUPPLIED.md` (0a9af0d).
- Second audit of sessions 0–9 and the repo, `docs/AUDIT_2026-10-26b.md` (109c8a9); fix sessions F1–F8 with prompts for Claude and tasks for Adrian, `docs/FIX_PLAN.md` (6d77b36).
- CI: mypy and ruff errors as annotations (5a5ca46, 8bdde1a).

**Failures on record**
- Six red CI runs before green (40333436686 … 40334306373): two blind mypy guesses, then visible errors fixed. Cause: no package index in Claude's workspace, CI logs unreadable (403).
- Standard built from a non-final manuscript version (the final one, "Decision or Supply?", adds an "Identification" row).
- PPE event files not found: not in any repo, not on the web (two searches); they existed only in a past chat's workspace.
- I told Adrian the event files could be downloaded from the old chat before checking which file cards it holds.

**Open questions**
- PPE event files, Belgian order file and scripts absent; the manuscript's data statement may promise files that are not public. Reason: Adrian's decision and files (F1; F8 if nothing is recovered).
- "Identification" row missing from the standard. Reason: scope (F7), needs the final manuscript from F1.
- Seven supplied PDFs recorded by checksum only, not committed (~60 MB; Sudhof report marked "VS – Nur für den Dienstgebrauch"; journal papers' licences). Reason: Adrian's decision.
- Ozone/climate t0 and binding-act sources are secondary. Reason: scope (F7).
- Old DAC docs describe deleted code. Reason: scope (F2).
- `emo/metrics/dac/` duplicates part of the new module. Reason: scope (F7).

**Review points and Adrian's answers**
- More of the task (PPE + ozone/climate conversion): "1 – yes" → ozone/climate done; PPE blocked on files.
- Adrian: "I am not an AI … everything needs to be recorded by you … inside the repo" → recording rule.
- Event files: Adrian supplied the manuscript and 15 files, then chose "2" (look for the files) → past-chat search: no repository was created; final manuscript exists only in that chat.
- Adrian asked for an audit of sessions 1–9 and the repo, and prompts for each fix → audit and FIX_PLAN.

**Next session:** F1 (Adrian first brings the DAC paper's submission facts and every file card from the chat "Combining DAC EMO UIA RDL"), then F2, F3, F5–F7 (F4 done); session 10 after them.

## Earlier sessions

Sessions 1–8: `docs/STATUS_ARCHIVE.md` (moved verbatim, 28 Oct 2026).
