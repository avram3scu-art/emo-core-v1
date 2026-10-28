"""F3 (28 Oct 2026): backfill docs/RECORD.md with sessions 0-8 and add the evidence-class column.

One-off script, kept for the record. Sources: git history (231 commits), the Actions run list
(REST API, 329 runs before 26 Oct 14:45 UTC), docs/STATUS.md, docs/SESSION_LOG.md and the
protocol files. Run once from the repository root; it refuses to run twice.
Classes: blind = pre-registered blind; known = pre-registered on known history;
exploratory; infra = infrastructure (code, CI, data plumbing, synthetic method checks, audits).
"""

from pathlib import Path

P = Path("docs/RECORD.md")
CLASS = {"blind": "pre-registered blind", "known": "pre-registered on known history",
         "exploratory": "exploratory", "infra": "infrastructure"}

# date | session | type | class | what | protocol | code | data | result | commit / run
ROWS = [
    # Before session 0
    ("2026-02-04..04-21", "pre-0", "CI runs", "infra", "228 CI runs on the old account (branches main, feature/dac-v0.1-*, feature/dac-mode-and-snapshot-query-params, docs/whitepaper-v1-1) before the transfer; not indexed one by one (before session 0)", "—", "`ci.yml` of that time", "—", "218 failure, 10 success; code they tested was later deleted (26 Oct)", "runs 21684587708 … 24738065110"),
    # Session 0: 19-21 Oct
    ("2026-10-19", "0", "clean-up", "infra", "Remove leftover ChatGPT citation tags", "—", "—", "—", "93 tags removed from 7 files", "e0d2957"),
    ("2026-10-19", "0", "control test", "infra", "Synergy: v1.0 proxy was identically zero; replaced by Gaussian O-information, synthetic controls", "—", "`emo/synergy.py`, tests", "synthetic", "v1.0 FAIL (always 0); new version passes controls", "d74fc4c"),
    ("2026-10-19", "0", "control test", "infra", "GWI, SMF, τ_I v1.0 scored noise; replaced by null-corrected versions with noise/signal controls", "—", "`emo/gwi.py`, `emo/smf.py`, `emo/info_time.py`, tests", "synthetic", "v1.0 FAIL on noise (SMF ≈ 0.57 for unrelated noise; GWI flagged ~5% of days; τ_I 26× higher on flat noise); new versions pass controls", "86ccd80"),
    ("2026-10-20", "0", "analysis", "exploratory", "τ_I on NHC Atlantic official track errors 1970–2025, with shuffled-years control", "—", "`analysis/information_time_nhc.py`", "`data/nhc_atlantic_official_track_errors_1970_2025.csv` (hand-transcribed)", "improvement 3–4% a year at every lead; restates NHC's known trend", "6238546"),
    ("2026-10-20", "0", "data", "infra", "OWID/UCDP conflict death rate; OpenAlex co-authorship, ODA, ODS added", "—", "fetch scripts", "`data/sources/owid_*`, `openalex_*`", "added", "0a93a63, 526048a"),
    ("2026-10-20", "0", "analysis", "exploratory", "Organismality plane: cooperation–conflict path 1989–2025", "—", "`analysis/organismality_plane.py`", "OWID, OpenAlex", "figure; descriptive", "b1c40bf"),
    ("2026-10-20", "0", "analysis", "exploratory", "Composition control: co-authorship excluding China and Indonesia; plane redrawn", "—", "same", "`openalex_*_excl_CN_ID`", "figure redrawn; descriptive", "86c7597"),
    ("2026-10-20", "0", "code fix", "infra", "Stale package exports and `smf_from_dataframe`; tests added", "—", "`emo/`", "—", "fixed", "ae89176"),
    ("2026-10-20", "0", "analysis", "exploratory", "DAC ozone calibration case (warning to Montreal Protocol)", "—", "`analysis/dac_ozone.py`", "`data/dac_ozone_events.csv` (Wikipedia/secondary sources)", "lag computed; descriptive", "be23dfc"),
    ("2026-10-20", "0", "analysis", "exploratory", "DAC contrast: climate vs ozone, same measurement", "—", "`analysis/dac_compare_ozone_climate.py`", "`data/dac_climate_events.csv`", "climate slower; n = 2, descriptive", "948953b"),
    ("2026-10-20", "0", "control test", "infra", "RDL v0.2: gap-bounded simulation, refusal without data, error on unknown domain", "—", "`emo/remedy/`, tests", "synthetic", "controls pass", "bc10c7d"),
    ("2026-10-20", "0", "pre-registration", "known", "RDL backtest protocol (ozone 1985, climate 1997/2015; held-out leaded petrol)", "`docs/RDL_BACKTEST_PROTOCOL.md`", "—", "—", "committed before engine and inputs", "1b84f12"),
    ("2026-10-20", "0", "code freeze", "known", "RDL backtest engine frozen (delivery-effect fix logged)", "same", "`emo/remedy/backtest.py`", "—", "frozen", "2c44071, 54e0993"),
    ("2026-10-20", "0", "inputs", "known", "RDL backtest inputs, rules and sources, before the first run", "same", "—", "`docs/RDL_BACKTEST_INPUTS.md`", "committed before run", "9b9422f"),
    ("2026-10-20", "0", "test", "known", "RDL v0.2 backtest, development cases", "same", "`analysis/rdl_backtest_run.py`", "inputs 9b9422f", "without structure inputs discrimination FAIL (0.224 = 0.224, as predicted); with them PASS (0.160 > 0.126); resemblance pass (weak criterion); ozone ahead in 144/162 sensitivity combinations", "236aa8a"),
    ("2026-10-20", "0", "test", "known", "RDL v0.2 held-out case: leaded petrol 2002 (inputs c5d8ad9 before the run)", "same", "`analysis/rdl_backtest_heldout.py`", "inputs c5d8ad9", "**FAIL**: 0.119 < climate 1997 0.126, in all 4 sensitivity settings (gain scales with remaining gap)", "c5d8ad9 → 468816c"),
    ("2026-10-20", "0", "pre-registration", "known", "RDL v0.3: separate gap and tractability; held-out sulphur 1985 vs chrysotile 2004", "`docs/RDL_V03_PROTOCOL.md`", "—", "—", "committed before code", "47ffbc3"),
    ("2026-10-20", "0", "test", "known", "RDL v0.3 development run 1", "same", "`emo/remedy/backtest.py` (`run_backtest_v03`)", "development cases", "FAIL: pledges check (held-out blocked)", "2dbca47"),
    ("2026-10-20", "0", "test", "known", "RDL v0.3 effect-floor rule (author's choice among three, logged); development run 2", "same", "same", "same", "all four checks PASS; engine frozen for held-out", "0749b78"),
    ("2026-10-20", "0", "test", "known", "RDL v0.3 held-out: sulphur 1985 vs chrysotile 2004 (inputs before the run)", "same", "`analysis/rdl_v03_heldout.py`", "inputs 46c15ca", "**FAIL**: sulphur > chrysotile fails in all 16 sensitivity settings", "46c15ca → b58c51d"),
    ("2026-10-20", "0", "pre-registration", "blind", "RDL v0.4 against independently coded regime data (Oslo–Seattle / IRD); script checked on synthetic data", "`docs/RDL_V04_PROTOCOL.md`", "`analysis/rdl_v04_test.py`", "synthetic", "FPR 0.037 over 300 null datasets (one of the first two passed by chance, p = 0.006); power 0.32 at 30 components; real data not received", "f75c993"),
    ("2026-10-20", "0", "forecasts", "blind", "RDL forecast ledger F001–F005, dated, with scoring script", "`docs/RDL_FORECAST_LEDGER.md`", "`analysis/score_forecast_ledger.py`", "`data/rdl_forecast_ledger.csv`", "registered; first resolution by 31 Dec 2026", "7f7fc9d"),
    ("2026-10-20", "0", "archive", "infra", "Forecast ledger deposited on Zenodo", "—", "—", "DOI 10.5281/zenodo.23507467", "done; sha256 recorded", "2a20df7"),
    ("2026-10-20", "0", "code change", "infra", "DAC profile reported without aggregation; gap scalar labelled convenience only", "—", "`emo/`", "—", "done", "9428f24"),
    ("2026-10-21", "0", "CI", "infra", "CI after project-URL update (transfer to avram3scu-art)", "—", "`ci.yml`", "—", "FAIL (cause not recorded)", "691d3fe / run 39570756183"),
    ("2026-10-21", "0", "run", "infra", "Weekly open-data refresh created; first run", "—", "weekly refresh workflow, `scripts/weekly_run.py`", "OWID, OpenAlex", "PASS; recorded run 2026-10-21", "bd0c68f / run 39571543132 → 9514569"),
    ("2026-10-21", "0", "CI", "infra", "CI on the refresh commit, then mypy annotation", "—", "`ci.yml`", "—", "FAIL on bd0c68f (run 39571542844; next commit fixed a mypy annotation), then PASS", "run 39571542844; 72b248e / run 39571879091"),
    # Session 1
    ("2026-10-23", "1", "check", "infra", "Push access to avram3scu-art/emo-core-v1", "—", "git", "—", "PASS", "d64b7d4"),
    ("2026-10-23", "1", "attempt", "infra", "Run tests in Claude's workspace", "—", "pip", "—", "error: PyPI unreachable", "—"),
    ("2026-10-23", "1", "attempt", "infra", "Change default branch from the session", "—", "GitHub API", "—", "error: HTTP 403; Adrian changed it by hand", "c2ee905"),
    ("2026-10-23", "1", "count", "infra", "Test functions defined vs recorded", "—", "grep", "`tests/`", "82 defined vs 57 recorded (resolved in session 2: 95 pass)", "4ef3aa6"),
    # Session 2
    ("2026-10-23", "2", "merge", "infra", "Unmerged 21 Oct weekly-refresh work from `main` merged; workflow adapted", "—", "`weekly_refresh.yml`", "—", "done", "91f0931, abb7bbd"),
    ("2026-10-23", "2", "run", "infra", "Weekly refresh, push-triggered", "—", "same", "—", "PASS", "run 39916341895 → 7a6afdf"),
    ("2026-10-23", "2", "run", "infra", "Weekly refresh, manual", "—", "same", "—", "FAIL: queued run checked out a stale commit, push conflicted; fixed in 00b02b0", "run 39916346571"),
    ("2026-10-23", "2", "run", "infra", "Two manual weekly runs after the fix", "—", "same", "—", "PASS both; 95 tests", "runs 39917084473 → ef78159, 39917096846 → 6b9fe0a"),
    ("2026-10-23", "3", "code", "infra", "Public page: build script, page test, pages job (deploys only if the refresh committed)", "—", "`scripts/build_site.py`, `tests/test_build_site.py`, `weekly_refresh.yml`", "—", "done", "36dae27"),
    # Session 3
    ("2026-10-23", "3", "run", "infra", "Public page job, first run", "—", "`weekly_refresh.yml` pages job, `scripts/build_site.py`", "—", "refresh PASS (9dc72e6); pages FAIL: 'Resource not accessible by integration'; Adrian enabled Pages by hand", "run 39918662082"),
    ("2026-10-23", "3", "run", "infra", "Page rebuilt without edits", "—", "same", "—", "PASS: page changed (e16d394 → 2419c6d), checked by fetching", "run 39920616723"),
    ("2026-10-23", "3", "run", "infra", "τ_I figure added to the page", "—", "`analysis/information_time_nhc.py`", "—", "PASS; 96 tests", "5562329 / run 39921357715 → 251395f"),
    # Session 4
    ("2026-10-23", "4", "review", "infra", "Related work: 9 entries; white-paper gap claims checked", "—", "—", "`docs/RELATED_WORK.md`", "10 gap claims removed or reworded, 1 backed; full texts of Miles 2002 and Breitmeier 2006/2011 not opened; no novelty claim", "2d31d9e, de2ebeb"),
    # Session 5
    ("2026-10-23", "5", "audit", "exploratory", "UIA audit: six a_UIA terms against public data", "`docs/UIA_PROTOCOL.md`", "`emo/uia_engine/` (deleted 26 Oct)", "—", "1 of 6 measurable, 1 conditional, 4 not; a_UIA retired (Adrian: Option C)", "ff9d692"),
    # Session 6
    ("2026-10-23", "6", "pre-registration", "blind", "GWI on hurricane landfalls in Wikipedia pageviews; event list fixed by rule (n = 21) before pageviews", "`docs/GWI_PROTOCOL.md`", "—", "HURDAT2", "committed before pageview fetch", "ae3b507, 08b99ab"),
    ("2026-10-23", "6", "code", "infra", "Weekly Action fetches Wikipedia daily pageviews for the GWI test (after the event list was fixed)", "`docs/GWI_PROTOCOL.md` §3", "`scripts/refresh_open_data.py`", "pageviews", "done", "31e7fa5"),
    ("2026-10-23", "6", "run", "infra", "Weekly runs with the GWI fetch", "same", "`weekly_refresh.yml`", "—", "FAIL twice: three refresh tests assumed only OWID/OpenAlex sources; fixed in 08b99ab", "runs 39930253098, 39930507770"),
    ("2026-10-23", "6", "test", "blind", "GWI on 21 landfalls vs 275 controls, placebo 'Photosynthesis'", "same", "`analysis/gwi_hurricanes.py`", "pageviews 12 editions", "**PASS**: 14/21 vs 9/275, Fisher p = 2.3e-13; placebo 2/21 vs 4/275, p = 0.061 (thin; audit S4); 97 tests", "run 39930743235 → 5e343fc; a93233f"),
    ("2026-10-23", "6b", "decision", "infra", "UIA consequences of the GWI pass", "`docs/UIA_PROTOCOL.md` §5", "—", "—", "C stays retired; GWI may score He's I only after a calibration test", "d98bedd"),
    ("2026-10-23", "6c", "pre-registration", "blind", "GWI calibration on unopened 2026 pageviews", "`docs/GWI_CALIBRATION_PROTOCOL.md`", "—", "—", "committed before fetch", "db843a4"),
    ("2026-10-23", "6c", "test", "blind", "GWI calibration: threshold on training, tested across articles and time", "same", "`analysis/gwi_calibration.py`, `emo/gwi.py`", "held-out pageviews", "**FAIL**: 'Prime number' ignited at 0.0134 > 0.010; held in time and kept discrimination (14/21 vs 12/275); 'Mitochondrion' dropped", "803d614 / run 39933057718 → 7fec9bd; 4420ddf"),
    ("2026-10-23", "6c", "diagnostics", "exploratory", "GWI calibration §8: Prime-number September cluster; session-6 PASS split by month; Mitochondrion streams", "same §8", "—", "opened pageviews", "50/53 Prime-number ignitions in September; session-6 PASS holds in both splits", "7d41576"),
    ("2026-10-23", "6c", "check", "infra", "Was en 'Mitochondrion' moved?", "same §8", "one-off wiki title check", "Wikipedia move log (metadata)", "first attempt unverified (178a2d8); then verified: moved to 'Mitochondria' 2026-06-29", "run 39934649530 → e899e03"),
    # Session 7
    ("2026-10-23", "7", "check", "infra", "SMF on annual OWID CO2: can the null reach p < 0.05?", "—", "`emo/smf.py` v1.1", "no data opened", "FAIL: n = 25 gives 6 distinct shifts; reported p overstated; session stopped before pre-registration", "8605b0b"),
    ("2026-10-23", "7a", "code fix", "infra", "SMF v1.2: each shift used once, honest p, n_null and p_min reported", "—", "`emo/smf.py`", "—", "PASS; 102 tests", "9dc38eb / run 39940150931"),
    ("2026-10-23", "7", "probe", "infra", "Layout-only probes (labels, never values): STEO/MER, electricity, SPF, industrial production", "—", "probe workflows (replaced 2a0a16a)", "—", "done; no values printed", "runs 39940687789, 39940799124, 39946118805, 39948050223, 39948495201"),
    ("2026-10-23", "7b", "test", "blind", "SMF §7: EIA STEO CO2, lead 12, vs persistence", "`docs/SMF_PROTOCOL.md` §7", "`analysis/smf_steo.py`", "`data/sources/eia_steo_co2`, `eia_mer_t11_01`", "PASS (r = 0.39, p = 0.010) but r = −0.01 without 2020–21", "14b06b2 → 1677108 → run 39941453995 → 7fc7696; 6183f58"),
    ("2026-10-23", "7c", "test", "blind", "SMF §8: CO2 leads 3/6/12 vs no change, without 2020–21", "same §8", "`analysis/smf_steo_leads.py`", "`eia_steo_co2_leads`", "PASS h = 3 (r = 0.53), PASS h = 6 (r = 0.52), FAIL h = 12 (2020–21 result known before; not blind for h = 12)", "6f95ad8 → 30a0a48 → run 39942987695 → c32cfa9; fc08493"),
    ("2026-10-23", "7d", "test", "blind", "SMF §9: CO2 lead 18", "same §9", "`analysis/smf_steo_h18.py`", "`eia_steo_co2_h18`", "FAIL: r = −0.21, p = 0.86, MSE 24% worse than no change", "f6519cd → b5ed83b → run 39944422318 → 9cb5ded; 20da6c5"),
    ("2026-10-23", "7", "search", "infra", "Second archived monthly CO2 forecaster", "—", "3 web queries", "—", "none found", "2cfc9f3"),
    ("2026-10-23", "7e", "test", "blind", "SMF §10: EIA electricity retail sales", "same §10", "`analysis/smf_steo_elec.py`", "`eia_steo_elec`", "PASS 3 and 6 months, FAIL 12", "950ad46 → 427966a → run 39946280348 → 7031a64; a88ab88"),
    ("2026-10-23", "7f", "test", "blind", "SMF §11: SPF unemployment (second forecaster)", "same §11", "`analysis/smf_spf.py`", "`spf_unemp`", "PASS at 1, 2, 4 quarters (r = 0.85/0.82/0.75)", "8fb4c79 → 8aa3234 → run 39948229129 → 8baf911; bda024b"),
    ("2026-10-23", "7g", "test", "blind", "SMF §12: industrial production, EIA and SPF", "same §12", "`analysis/smf_ip.py`", "`smf_ip`", "EIA PASS 3/6, FAIL 12; SPF PASS 1/2/4 q → 'forecaster effect'; exploratory checks (no weight) undo it", "834d39c → e3aef93 → run 39948712388 → 2c18760; 97d4ff4"),
    ("2026-10-23", "7 review", "rerun", "infra", "Rerun of sessions 1–7; six SMF analyses from committed data", "—", "weekly run", "committed", "PASS: outputs reproduce; 102 tests", "run 39951627726 → 387cd99; 261da1f"),
    ("2026-10-23", "7 fixes", "CI", "infra", "Review fixes: new test helper shadowed `_Resp`", "—", "`tests/`", "—", "FAIL: 3 refresh tests broke (CI 39952543332, weekly 39952555284 blocked); fixed 29d2205", "2a0a16a"),
    ("2026-10-23", "7 fixes", "run", "infra", "One-off workflow check (probe-spf)", "—", "`one_off.yml`", "—", "PASS", "run 39952550960"),
    ("2026-10-23", "7 fixes", "run", "infra", "Weekly run after the fix", "—", "weekly", "—", "PASS: 103 tests", "run 39952996639"),
    ("2026-10-23", "7 lint", "CI", "infra", "CI on default branch: ruff lint debt", "—", "`ci.yml`, `ruff-autofix.yml`", "—", "FAIL (runs 39952816621, 39953412815, 39956055595); autofix 39956062452 → aecfb77 (28 of 52); 24 by hand 8c80d6c; then PASS", "run 39956184040"),
    ("2026-10-23", "7 audit", "audit", "infra", "Partial logic re-audit of sessions 1–6 (GWI tests, weekly gate)", "—", "—", "—", "no logic error; GWI Fisher p optimistic (clustering); GWI outputs not frozen", "a169ee1"),
    # Session 8
    ("2026-10-26", "8", "pre-registration", "blind", "Synergy on three climate streams (science, policy, attention)", "`docs/SYNERGY_PROTOCOL.md`", "`analysis/synergy_climate.py` (b27400e, before data)", "—", "committed before data", "e4c160c, b27400e"),
    ("2026-10-26", "8", "fetch", "infra", "OpenAlex fetch for the synergy test", "same §9", "`scripts/fetch_synergy_climate.py`", "—", "FAIL twice: HTTP 429; nothing saved", "runs 40283263805, 40283537981 (213d3ef)"),
    ("2026-10-26", "8", "fetch", "infra", "Resumable fetch, amendment recorded before data", "same", "same", "cached unopened", "101/120 months cached", "0a6c697 / run 40286109947 → be7028b"),
    ("2026-10-26", "8", "test", "blind", "Synergy on real streams (fetch completed with OPENALEX_API_KEY)", "same §10", "`analysis/synergy_climate.py`", "`data/sources/synergy_climate`", "**FAIL**: S = +0.0012 bits, p_syn = 0.215; TC p = 0.59", "e4fb711 / run 40288775279 → 93fb72a; 5b1d894"),
    ("2026-10-26", "8", "audit", "infra", "First audit of sessions 1–8 and code", "—", "—", "—", "findings in `docs/AUDIT_2026-10-26.md`; my list wrongly called RDL backtest/bottlenecks unused (corrected a047f00)", "7be95c0"),
    ("2026-10-26", "8", "run", "infra", "Audit fixes 1–2 (DAC text computed; GWI frozen); weekly run", "—", "weekly", "—", "PASS: 103 tests, frozen runs reproduce", "48e75e0 / run 40289771653 → eb5eb71"),
    ("2026-10-26", "8", "deletion", "infra", "Never-run scaffolding deleted (API, dashboard, orchestration, ingestion, DestinE hooks)", "—", "—", "—", "89 files; CI PASS", "4507783 / run 40290629520"),
    ("2026-10-26", "8", "CI change", "infra", "README/plan: synergy is a synthetic-only pass; Tuesday backup trigger for the weekly run; idle `synergy_resume.yml` deleted", "—", "`weekly_refresh.yml`", "—", "done", "81caa80"),
    ("2026-10-26", "8", "analysis", "exploratory", "τ_I block-bootstrap interval on NHC", "—", "`emo/info_time.py`, `analysis/information_time_nhc.py`", "NHC", "improvement holds at every lead (48 h 3.63%/yr [3.34, 3.91]); CI first FAIL (F541 f-string, run 40292329460; also 40292367060, 40292580268), fixed f5e369f", "b6d5de6"),
    ("2026-10-26", "8", "check", "infra", "NHC table vs NHC's PDF", "—", "`one_off.yml` nhc-pdf, permanent test", "NHC PDF", "FAIL at apt-get (40292369127) and once more (40292580063), then PASS: 368/368 cells match", "run 40292776083 → 7d6803d; 0cd462f"),
    ("2026-10-26", "8", "run", "infra", "Weekly run after audit follow-up", "—", "weekly", "—", "PASS: 76 tests", "run 40293170796 → 51b060b"),
    ("2026-10-26", "8", "probe", "infra", "Why scheduled runs never fire: 5-minute schedule probes", "—", "probe workflows", "—", "0 runs in 46 min (diagnosis 'GitHub fires none' later corrected: late, not dead)", "d17ef03, f97c75f, b5cd080"),
    ("2026-10-26", "8", "attempt", "infra", "Claude scheduled task as weekly starter, two tests", "—", "—", "—", "FAIL: no run started; reported as a fix before testing (my mistake); disabled", "343d6ef"),
    ("2026-10-26", "8", "run", "infra", "Clean-up (59 files, deps 15 → 5); weekly run", "—", "weekly", "—", "PASS: 57 tests", "ee01bc6 / run 40308922444 → 6b85f75"),
    ("2026-10-26", "8", "run", "infra", "GitHub's Monday cron", "—", "weekly (schedule)", "—", "fired 6 h late; gate skipped it", "run 40313738746"),
    ("2026-10-26", "8", "run", "infra", "cron-job.org weekly starter tests", "—", "workflow-dispatch API", "—", "first 401 (token pasted wrongly), then PASS; token renewed (expires 26 Oct 2027), PASS", "runs 40329335301, 40330816177; 709b9da, 9bb7771"),
    ("2026-10-26", "8", "rules", "infra", "CLAUDE.md: pre-closing review, reason for every not-done item, start-of-session weekly-run check", "—", "`CLAUDE.md`", "—", "done (Adrian's request)", "2910790"),
]


def main() -> None:
    text = P.read_text()
    if "| Class |" in text:
        raise SystemExit("already backfilled")
    lines = text.splitlines()
    out = []
    for ln in lines:
        if ln.startswith("| Date | Session | Type |"):
            out.append("| Date | Session | Type | Class | What | Protocol | Code | Data | Result | Commit / run |")
        elif ln.startswith("|---|"):
            out.append("|---|---|---|---|---|---|---|---|---|---|")
            for r in ROWS:
                out.append("| " + " | ".join([r[0], r[1], r[2], CLASS[r[3]], *r[4:]]) + " |")
        elif ln.startswith("| 20"):
            cells = ln.split(" | ")
            typ = cells[2].strip().lower()
            if typ in ("simulation", "code check") and "test the test" in cells[1]:
                cls = "pre-registered blind (synthetic)" if "He calibration" in ln else "exploratory"
            elif typ in ("probe",) and "audit" in cells[1]:
                cls = "exploratory"
            elif typ == "reproduction check":
                cls = "pre-registered on known history"
            else:
                cls = "infrastructure"
            cells.insert(3, cls)
            out.append(" | ".join(cells))
        else:
            out.append(ln)
    text = "\n".join(out) + "\n"
    text = text.replace(
        "Rows start at session 9 (26 Oct 2026). Sessions 1–8 are recorded in `docs/STATUS.md`, `docs/SESSION_LOG.md` and the protocol files (`docs/SMF_PROTOCOL.md`, `docs/SYNERGY_PROTOCOL.md`, `docs/RDL_*`); they have not yet been indexed here.",
        "Sessions 0–8 (19–26 Oct 2026) were backfilled on 28 Oct 2026 (fix session F3, `scripts/f3_backfill_record.py`) from git history, the Actions run list, `docs/STATUS_ARCHIVE.md` and the protocol files; rows from session 9 on were written as the work happened. "
        "**Class:** pre-registered blind (protocol committed before the data were opened, outcome unknown) / pre-registered on known history (protocol first, but on cases whose outcome the author and Claude knew) / exploratory (no pre-registration) / infrastructure (code, CI, data plumbing, synthetic method checks, audits). "
        "Weekly-run commits that only refresh data ('Weekly run …: all checks passed') are not listed one by one unless a session used them.")
    P.write_text(text)


if __name__ == "__main__":
    main()
