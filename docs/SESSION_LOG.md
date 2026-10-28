# Session log

One row per session, with real commit IDs (rewritten 28 Oct 2026, fix session F3). Rows as first written, several per session: `docs/SESSION_LOG_ARCHIVE.md`. Every item: `docs/RECORD.md`.

| date | session | task | done when met | key commits | note |
|---|---|---|---|---|---|
| 2026-10-19/21 | 0 | Work before the plan: metric fixes, first real-data cases, RDL v0.2/v0.3 tests, forecast ledger, weekly refresh | — (no plan yet) | 86ccd80, 6238546, 948953b, 236aa8a, 468816c, b58c51d, 7f7fc9d, bd0c68f | v1.0 metrics scored noise, replaced; RDL v0.2 and v0.3 FAIL held-out [known history]; ledger F001–F005 on Zenodo |
| 2026-10-23 | 1 | Move work to avram3scu-art; truthful README | yes | d64b7d4 | default branch set by Adrian by hand (settings 403) |
| 2026-10-23 | 2 | Weekly GitHub Action | yes | abb7bbd, 00b02b0 | one failed manual run (stale checkout), fixed; 95 tests |
| 2026-10-23 | 3 | Public page | yes | 36dae27, 5562329 | Pages enabled by Adrian; page rebuilt without edits (run 39920616723) |
| 2026-10-23 | 4 | Related work | yes | 2d31d9e | 10 gap claims removed or reworded, 1 backed; no novelty claim |
| 2026-10-23 | 5 | UIA audit | yes | ff9d692 | a_UIA retired (Option C); 1 of 6 terms measurable |
| 2026-10-23 | 6 | GWI on real attention data (+ 6b UIA follow-up, 6c calibration) | yes | a93233f, d98bedd, 4420ddf, e899e03 | GWI PASS [blind] (p 2.3e-13; placebo thin); calibration FAIL [blind] |
| 2026-10-23 | 7 | SMF on a real case (+ smf.py fix, §7–§12, review, lint, partial re-audit) | yes (case redefined by Adrian) | 9dc38eb, 97d4ff4, 2a0a16a, 8c80d6c, a169ee1 | fidelity at 3–6 months, none for energy/IP at 12 since 2010; deciding condition untested (audit S1) |
| 2026-10-26 | 8 | Synergy on real streams (+ first audit, deletions, scheduler fix, rules) | yes | 5b1d894, 7be95c0, 4507783, ee01bc6, 9bb7771, 2910790 | synergy FAIL [blind]; cron-job.org starts the weekly run |
| 2026-10-26 | extra | Test the test; He calibration and amendment | yes | 5c50e32, 727c500, e100c80 | Option A rule unusable; T-D usable from 24 cases; trigger 8 → 24 |
| 2026-10-26/27 | 9 | DAC standard (+ ozone/climate conversion, recording rule, second audit, fix plan) | yes | 3494540, c70276e, 109c8a9, 6d77b36 | tests incl. malformed-file rejection; PPE files not in any repo |
| 2026-10-26/27 | F4 | CI readability (+ Node 24, pinned runners) | yes | 6df6a83, 37f58f4 | failures readable as annotations; 91 tests |
| 2026-10-27 | 10 (attempt) | DAC new domain (mpox) | no: stopped at start | eac2017 | F1–F7 gate not cleared; Adrian chose to keep order |
| 2026-10-27/28 | audit | Third audit: code and work since the second | yes | 8573410, d0b236e, eac2017 | all recorded results reproduce; validator gaps D1–D6, SMF null M1 → fix plan |
| 2026-10-28 | F1 | DAC paper facts and files | yes | 33b34b1, 0293074, 6130d1e | JCCM not submitted; final manuscript committed; event files not found → F8 |
| 2026-10-28 | F2 | Truth pass on public files | yes | a158c65, c176b7d | banners, evidence classes, claim check in CI; new rules (recommendation with every question; own mistakes fixed in full) |
| 2026-10-28 | F3 | Records backfill | yes | c05876c | sessions 0–8 indexed (85 rows), class column on every row; STATUS split, archive verbatim; session log one row per session, no placeholders |
| 2026-10-28 | F5 | SMF significance re-analysis (+ M1 guard, frozen SMF/synergy) | yes | 6d0f142 | 6 of 12 passes survive DM/Holm; guard flags 5 EIA inputs (caveat on EIA CO2 3m); weekly 40659742858 reproduces all 15 frozen runs |
| 2026-10-28 | F6 | Method labels and the evidence-class rule | yes | dc0c1c3 | RDL tests labelled known history (ledger the only blind RDL test); GWI placebo note and caveat; two new Science rules approved |
| 2026-10-28 | F7 | DAC clean-up: standard v1.1, old code retired, primary sources, manuscript copies by script | yes | 197654b | D1–D6 fixed; Identification row; ozone lag exact 4,828 d; 100 tests; weekly 40666382346 |
| 2026-10-28 | F8.1 | PPE recoding: rules + Belgium | yes | c72013b | BE.json and order file validated from Chamber Annex 5; known-history class; two citation errors fixed with a test |
| 2026-10-28 | F8.2 | PPE recoding: France | yes | 45438bc | FR.json from the Sénat report; two readings of the first order; no paired orders; citation-phrase test; Sudhof report not to be used for DE (Adrian) |
| 2026-10-28 | F8.3 | PPE recoding: Germany | yes | dc7fdf7 | DE.json from public Bundestag answers + TRIS record (Adrian); order and delivery are 60-day windows; blindness breach recorded (my mistake) |
| 2026-10-28 | F8.4 | PPE recoding: Netherlands | yes | a33a179 | NL.json from the VWS fact reconstruction; order 6–9 Mar, ROAZ delivery 21–22 Mar; grey-text check |
| 2026-10-28 | F8.5 | PPE recoding: Sweden | yes | 4fb2dc6 | SE.json from SOU 2021:89; order Feb, binding act 16 Mar, delivery Mar (Fig. 8.2 decomposed: all PPE); month precision |
| 2026-10-28 | F8.6 | PPE recoding: EU | yes | 5aa9bfb | EU.json from OJ acts, Sénat p. 400, EP photo record; binding act 14 Mar, German ban 4 Mar, rescEU delivery 25 Apr; firm order missing; breach 2 recorded (my mistake) |
| 2026-10-28 | F8.7 | PPE gap-filling | yes | fa9957d | strict page test; EU funding not fillable; SE delivery 17–31 Mar; DE delivery 11–20 Mar, order 2 readings; BE binding act 23 Mar (Moniteur from Adrian); one push with failing claims check (my mistake, fixed) |
| 2026-10-28 | F8.8 | PPE comparison with the manuscript | yes | 63ab805 | frozen then compared; 1 type-(c) error of mine corrected (BE row 742); 0 type-(d); BE binding act and DE delivery differ (explained); SI holds no sources; F8 complete |
| 2026-10-28 | F9 | Manuscript data-only revision | yes | afdc3e7 | 29 tracked changes; cross-case stats recomputed (exploratory); 3 argument-level consequences flagged for Adrian |
| 2026-10-28 | F10 | Editor-style review of the manuscript | yes | 3907fd5 | not ready for JCCM; 5 blockers; F9 coder sentence corrected (my mistake); Adrian checks the coded dates himself |
| 2026-10-28 | F11 | Literature and records search | yes | 7e1165f | novelty claim must narrow to the test (Canada OAG pairs contracts with first delivery); second-case candidates listed |
| 2026-10-28 | F12 | Manuscript argument rewrite | yes | 93558a2 | 26 tracked changes; novelty narrowed (Canada OAG); cross-case days 41–61; rivals bounded; closed at start of F13 |
| 2026-10-28 | F13 | Manuscript figures | yes | c200d01 | Figures 1–2 redrawn from event files; China sources committed; inserted with tracked changes |
| 2026-10-28 | F14 | Final editor-style review | yes | 118221d | not ready, do not submit yet; ChatGPT not used (Adrian) — declaration to correct; Adrian's three steps pending |
| 2026-10-28 | 10 | Code one new warning-to-delivery case (mpox, EU) | yes | 65054ae | all EU responses precede the WHO PHEIC (order −39 d, delivery −25 d); next 10b: earlier-warning t0 |
