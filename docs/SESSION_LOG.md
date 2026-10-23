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
2026-10-23 | 7 | SMF on a real case | no | (this commit) | Stopped before pre-registration: smf.py null degenerate on annual data (n=25 → 6 distinct shifts; reported p overstated); no data opened
