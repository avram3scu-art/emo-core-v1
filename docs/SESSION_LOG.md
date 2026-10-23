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
