# Session log

| date | session | task | done when met | key commit | note |
|---|---|---|---|---|---|
| 2026-10-23 | 1 | Move work to avram3scu-art; truthful README | yes (default branch set by Adrian by hand; settings blocked from session) | d64b7d4 | head was 691d3fe; 82 test fns vs 57 recorded |
| 2026-10-23 | 2 | weekly GitHub Action (weekly_refresh.yml) | yes | 00b02b0 | merged unmerged 21 Oct work from main; manual runs ef78159, 6b9fe0a committed; 95 tests pass |
| 2026-10-23 | 3 | public page (GitHub Pages, rebuilt by weekly Action) | yes (Pages enabled by Adrian by hand) | 36dae27 | page changed after run 39920616723 without edits (e16d394 → 2419c6d) |
| 2026-10-23 | 4 | related work (docs/RELATED_WORK.md) | yes | 2d31d9e | 10 white-paper gap claims removed/reworded, 1 backed; key full texts not opened |
| 2026-10-23 | 5 | UIA audit (docs/UIA_PROTOCOL.md) | yes | ff9d692 | Option C: a_UIA retired, He profile defined, prediction deferred to ≥8 DAC cases; session 12 postponed |
| 2026-10-23 | 6 | GWI on real attention data (docs/GWI_PROTOCOL.md) | yes | 5e343fc | PASS: 14/21 event windows vs 9/275 controls, p=2.3e-13; placebo p=0.061 (thin); 2 runs blocked by stale tests first |
| 2026-10-23 | 6b | UIA follow-up: consequences of GWI pass (docs/UIA_PROTOCOL.md §5) | yes | d98bedd | a_UIA's C stays not usable (GWI level uncalibrated); GWI moves to He's I, usable only after a pre-registered calibration test on unopened 2026 pageviews |
| 2026-10-23 | 6c | GWI calibration test (docs/GWI_CALIBRATION_PROTOCOL.md) | yes | 7fec9bd | FAIL: threshold held in 2026 and kept discrimination, but "Prime number" ignited at 0.0134 > 0.010; GWI does not score He's I |
| 2026-10-23 | 6c close | GWI calibration: close-out and next step | yes | 4420ddf | advice: stop GWI-as-I work, optional clustering diagnostic, go to session 7 (SMF) |
| 2026-10-23 | 6c diag | GWI calibration exploratory diagnostics (protocol §8) | yes | (see STATUS) | Prime number ignitions = September academic-year effect; Mitochondrion likely a July-2026 redirect (unverified); session-6 PASS holds split by month |
| 2026-10-23 | 7 | SMF on a real case | no | 8605b0b | Stopped before pre-registration: smf.py null degenerate on annual data (n=25 → 6 distinct shifts; reported p overstated); no data opened |
| 2026-10-23 | 7a | smf.py null fix | yes | 9dc38eb | each shift once, honest p, p_min reported; 102 tests pass (run 39940150931) |
| 2026-10-23 | 7b | SMF on EIA STEO vs MER (redefined case) | yes | 7fc7696 | PASS (r=0.39, p=0.010, beats persistence) but r=-0.01 without 2020-21; carried by the pandemic swing |
| 2026-10-23 | 7c | SMF follow-up: leads 3/6/12 vs no change, without 2020-21 (§8) | yes | c32cfa9 | PASS h=3 (r=0.53), PASS h=6 (r=0.52), FAIL h=12 (r=-0.01, worse than no change) |
| 2026-10-23 | 7d | SMF lead 18 (§9) | yes | 9cb5ded | FAIL: r=-0.21, p=0.86, MSE 24% worse than no change; profile 3 PASS, 6 PASS, 12 FAIL, 18 FAIL |
| 2026-10-23 | 7 close | SMF on a real case (redefined: EIA STEO vs MER) | yes | 20da6c5 | smf.py v1.2 null fix; SMF PASS at leads 3 and 6, FAIL at 12 and 18 (lead-12 pass only via 2020-21) |
| 2026-10-23 | 7e | SMF on STEO electricity retail sales (§10) | yes | 7031a64 | same horizon as CO2: PASS 3 and 6 months, FAIL 12 |
| 2026-10-23 | 7f | SMF on SPF unemployment, second forecaster (§11) | yes | 8baf911 | PASS at 1, 2, 4 quarters (r=0.85/0.82/0.75): differs from EIA at 12 months; forecaster and variable both changed |
| 2026-10-23 | 7g | SMF forecaster vs variable: industrial production, EIA and SPF (§12) | yes | 2c18760 | pre-registered reading "forecaster effect", undone by exploratory checks: since 2010 SPF also worse than no change at a year; design flaw (period, definition) |
| 2026-10-23 | 7 close | SMF on a real case (EIA CO2, electricity, IP; SPF unemployment, IP) | yes | 97d4ff4 | short-horizon fidelity detected; since 2010 no energy/IP forecast beats no change at a year; §12 forecaster-effect reading not supported |
| 2026-10-23 | 7 review | Review and rerun of sessions 1-7 | yes | 387cd99 | all outputs reproduce; 102 tests pass; 5 improvements listed in STATUS (stale README/page claims, ci.yml, GWI redirects, workflows, SMF on page) |
| 2026-10-23 | 7 fixes | Review fixes (1)-(5) | yes | 2a0a16a | README/page corrected, SMF on page, CI on default branch (tests pass, ruff lint fails on old debt), redirects option, one manual workflow; 103 tests pass |
| 2026-10-23 | 7 lint | Clear ruff lint debt | yes | 8c80d6c | 52 issues (28 auto, 24 by hand, style only); CI green: tests, mypy, ruff |
| 2026-10-23 | 7 final close | SMF on a real case + review, fixes, lint | yes | c8cf591 | SMF fidelity at 3-6 months, none for energy/IP at 12 since 2010; README/page corrected; CI green; next: session 8 |
| 2026-10-23 | 7 audit | Logic re-audit of sessions 1-6 (partial: GWI tests and weekly gate) | partial | a169ee1 | no logic error found; GWI Fisher p optimistic (clustering); GWI recorded outputs not frozen-checked; tau_I, DAC, organismality, sessions 4-5 not audited |
| 2026-10-23 | 7 closed | Session 7 with review, fixes, lint, partial re-audit | yes | 29f89d7 | all work pushed; next: session 8; open: freeze GWI recorded outputs, audit tau_I/DAC/organismality/sessions 4-5 |
| 2026-10-26 | 8 | Synergy (Gaussian O-information) on real climate streams | no | e4c160c | Pre-registered and coded before data; OpenAlex fetch hit HTTP 429 twice (runs 40283263805, 40283537981); not run, data unseen |
| 2026-10-26 | 8 follow-up | Resumable fetch, daily resume job | no (pending fetch) | 0a6c697 | 101/120 OpenAlex months cached unopened; synergy_resume.yml finishes fetch and runs analysis once |
| 2026-10-26 | 8 completed | Synergy on real climate streams | yes | 93fb72a | FAIL: no structure beyond circular-shift null (p_syn 0.215); fetch finished with OPENALEX_API_KEY |
| 2026-10-26 | audit | Audit sessions 1-8 and code; fixes 1-2 | yes | 48e75e0 | DAC text computed, GWI frozen; weekly run eb5eb71 all checks passed |
| 2026-10-26 | 8 closed | Synergy on real streams; audit; fixes; deletion of never-run code | yes | 4507783 | Synergy FAIL (p_syn 0.215); DAC text fixed, GWI frozen; 89 files deleted; weekly eb5eb71 all checks passed |
| 2026-10-26 | 8 follow-up | Close remaining audit items | yes | 0cd462f | README/plan synergy fixed; weekly backup trigger; tau_I block CI (result holds); NHC 368/368 cells match PDF; analysis checks; weekly 51b060b all passed, 76 tests |
| 2026-10-26 | 8 follow-up | Diagnose weekly cron | yes | b5cd080 | GitHub fires no schedules for this repo (0 in 46 min, 2 probes); weekly run now started by a Claude scheduled task, Mondays 07:41 Brussels |
| 2026-10-26 | 8 closed (final) | Synergy, audit, fixes, deletion, scheduler fix, rules | yes | 2910790 | Synergy FAIL; GitHub fires no schedules here, weekly run now started by a Claude scheduled task; CLAUDE.md: pre-closing review and reasons for not done |
| 2026-10-26 | 8 follow-up | Clean-up, results.json, scheduler starter test | yes | ee01bc6 | 59 files deleted, deps 15->5, 57 tests green; results.json on page; Claude scheduled task failed as starter (disabled); sessions start the weekly run |
| 2026-10-26 | 8 follow-up | External weekly starter | yes | (this commit) | cron-job.org + fine-grained token; test run 40329335301 succeeded; GitHub cron fires late, not never (correction) |
| 2026-10-26 | 8 closed (final) | Session 8 incl. audit, clean-up, external weekly starter | yes | 9bb7771 | cron-job.org starts the weekly run (tested twice); token valid to 26 Oct 2027; 57 tests green |
| 2026-10-26 | extra | Test the test: Science of Truth simulations committed; He calibration | yes | (this commit) | Option A rule unusable (FPR ~50%); T-D usable at n = 30; trigger of 8 gives power 0.34–0.55 |
