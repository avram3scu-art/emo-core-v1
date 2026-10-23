# EMO status

Updated at the close of every session. Plan: `docs/PLAN.md`. History: `docs/SESSION_LOG.md`.

## Last session: 6 (2026-10-23) — GWI on real attention data

**Done when met: yes.** Result in `docs/GWI_PROTOCOL.md` §7: **PASS**.

**Checked first:** Monday 26 Oct's scheduled run cannot be checked yet (today is Fri 23 Oct). Carried to session 7.

**Done**
- Protocol committed before data (ae3b507); event list fixed from NHC HURDAT2 by rule, n = 21 Atlantic major-hurricane landfalls 2016–2025 (08b99ab); then pageview fetch added (31e7fa5).
- Weekly Action now fetches HURDAT2 (pinned file) and Wikipedia daily pageviews (12 editions, "Tropical cyclone" + placebo "Photosynthesis", fixed range 2015-11-01..2025-12-31); `analysis/gwi_hurricanes.py` runs weekly. Action now writes status, pytest and GWI lines as annotations (logs and artifacts are not readable from the session).
- Run 39930743235 → 5e343fc ("all checks passed"), 97 tests pass, page redeployed.

**Results**
- Test: 14/21 event windows hit vs 9/275 Jun–Nov controls, Fisher p = 2.3e-13. Placebo: 2/21 vs 4/275, p = 0.061. PASS by the pre-registered rule.
- Weak points: placebo margin thin (0.061 vs 0.05); 95 ignitions vs 0.012 expected under independence, so `compute_gwi`'s binomial threshold is not calibrated on real streams; misses cluster on Central American landfalls.
- Failure on record: run 39930253098 / 39930507770 did not commit (three refresh tests assumed only OWID/OpenAlex sources); fixed in 08b99ab.
- Pageview coverage starts July 2015 (pageviews.wmcloud.org FAQ, opened); `docs/UIA_PROTOCOL.md` said mid-2000s; corrected after close.

**Open questions**
- Does GWI pass for a second hazard class (earthquakes/tsunamis), and with per-language baselines that model the shared news cycle?
- UCDP start year still unverified. (Pageview start: July 2015, verified.) `ci.yml` still does not run on `emo-2026-10`.

**Adrian must do**
- Nothing.

## Next session
Session 7 (`docs/PLAN.md`). First check that Monday 26 Oct's scheduled run committed and redeployed the page.

## Previous session: 5 (2026-10-23) — UIA audit

**Done when met: yes.** Adrian chose Option C; decision and `docs/UIA_PROTOCOL.md` committed (ff9d692) before any UIA data was opened.

**Checked first:** Monday 26 Oct's scheduled run cannot be checked yet (today is Fri 23 Oct). Carried to session 6.

**Done** (ff9d692)
- Audit of the six a_UIA terms against real public data: R and B not measurable (code ignores the skill metric; B̃ hard-coded 3.0); S computable but meaningless (evenness of indicators, not an entropy rate); M_E not measurable; C conditional on GWI (session 6); I measurable only as τ_I (`emo/info_time.py`), the UIA version is biased upward by clipping.
- a_UIA retired: deprecation notes in `emo/uia_engine/aggregate.py` and `api/routers/uia.py`. UIA redefined as the He profile (I, C, F, E, D; He), never summed. D may not contain DAC lags (He is a DAC lag).
- No He prediction pre-registered: trigger is ≥8 DAC cases with warning dates after pageview coverage starts. Session 12 postponed (note in `docs/PLAN.md`).

**Results**
- 1 of 6 a_UIA terms measurable today, 1 conditional, 4 not. The white paper's single UIA gauge has no measured basis.
- The planned He test was blocked by n = 2–3 (no rank test can reach p < 0.05), a known outcome (ozone faster than climate), and ozone warnings (1974, 1985) predating pageview data.

**Open questions**
- Start years of Wikipedia pageview coverage and UCDP data: from memory, unverified; check in session 6.
- Could a per-country I and F make Option B (Montreal Protocol countries) testable?
- `ci.yml` still does not run on `emo-2026-10` (carried over).

**Adrian must do**
- Nothing.

## Next session
Session 6 (`docs/PLAN.md`). First check that Monday 26 Oct's scheduled run committed and redeployed the page.

## Previous session: 4 (2026-10-23) — related work

**Done when met: yes.** Every gap sentence in README and the three white papers is now backed by an entry in `docs/RELATED_WORK.md` or removed (register G1–G12 in that file). README had none.

**Checked first:** Monday 26 Oct's scheduled run cannot be checked yet (today is Fri 23 Oct). Carried to session 5.

**Done** (2d31d9e)
- `docs/RELATED_WORK.md`: nine entries (SDG 17.14.1; Sovereign ESG portal; WGI; Miles et al. 2002; Breitmeier, Young, Zürn 2006; Breitmeier, Underdal, Young 2011; OxCGRT; early-warning effectiveness; ESG Project). Each: what was opened, measures, method, coverage, overlap, what EMO adds. Unopened items marked unverified.
- White papers (v1.0, v1.1 md, docx): 10 gap claims removed or reworded, 1 kept and backed (behaviour after warnings, E8), "Uniqueness" section replaced. Full rewrite still session 15.
- No pre-registration: no hypothesis tested.

**Results**
- "No instrument measures how humanity responds" is false: policy coherence, governance quality, regime effectiveness and response timing are all measured elsewhere.
- What EMO does that none of the opened sources does: an open, weekly re-run series of dated warning→policy→delivery lags (DAC). Same question as the regime-effectiveness literature, different form; overlap with Miles 2002 (ozone, ch. 6) is high.
- Not opened: full texts of Miles 2002, Breitmeier 2006/2011; Sovereign ESG portal itself; Global Status of MHEWS 2025 report; Pattberg et al. 2014. No full-text database searched; no novelty claim made.

**Open questions**
- Do Miles 2002 or the IRD already report dated lags? Needs the full texts (library access).
- `ci.yml` still does not run on `emo-2026-10` (carried over).

**Adrian must do**
- Nothing required. Optional: library access to Miles 2002 and Breitmeier et al. 2006 would let entries E4–E6 be completed.

## Next session
Session 5 (`docs/PLAN.md`). First check that Monday 26 Oct's scheduled run committed and redeployed the page.

## Previous session: 3 (2026-10-23) — the public page

**Done when met: yes.** Live at https://avram3scu-art.github.io/emo-core-v1/ after Adrian enabled Pages (Source: GitHub Actions) by hand. Re-run of 39918662082 deployed the page built from e16d394 (07:50 UTC); run 39920616723, with no edits, rebuilt it from 2419c6d (07:53 UTC). Both checked by fetching the page.

**Checked first:** Monday 26 Oct's scheduled run has not happened (session held Fri 23 Oct). Latest run instead: 9dc72e6 ("Weekly run 2026-10-23: all checks passed").

**Done** (36dae27)
- `scripts/build_site.py`: static `site/index.html` from the newest `results/weekly/<date>/`, `data/MANIFEST.json`, the forecast ledger and the two figures. Computes nothing; copies numbers. Sections: what EMO does not yet measure; organismality plane; τ_I from NHC track errors; DAC ozone vs climate; forecast ledger with DOI 10.5281/zenodo.23507467 and its SHA-256. Each block links to its output file, script, input data (retrieval date, hash) and upstream source.
- `tests/test_build_site.py`: sections present, every repository link resolves to a real file.
- `weekly_refresh.yml`: new `pages` job, runs only if the refresh job succeeded and committed (`commit_allowed`); builds and deploys with actions/deploy-pages. `site/` is not committed.
- No pre-registration: no hypothesis tested.

**Results**
- Run 39918662082: refresh succeeded and committed (9dc72e6); `pages` failed at Configure Pages: "Resource not accessible by integration" (the token may not create a Pages site). Session API also refused (403).
- τ_I figure added after close (5562329): `analysis/information_time_nhc.py` also saves `information_time_nhc.png` (data and per-lead τ_I with 95% CI, same numbers as its table; text output unchanged). Run 39921357715 rebuilt it and the page (251395f).
- New page test passes on GitHub: pytest 96 passed (95 + `test_build_site`).

**Open questions**
- `actions/configure-pages@v5` targets Node 20 (deprecation warning in run 39918662082); upgrade when a newer major is available.
- `ci.yml` still does not run on `emo-2026-10` (carried over from session 2).

**Adrian must do**
- Nothing. (Leave Actions log retention at its current value; do not set it to 7 days.)

## Next session
Session 4 (`docs/PLAN.md`). First check that Monday 26 Oct's scheduled run committed and redeployed the page.

## Previous session: 2 (2026-10-23) — the weekly GitHub Action

**Done when met: yes.** Two manual runs committed without help: runs 39917084473 → ef78159 and 39917096846 → 6b9fe0a ("Weekly run 2026-10-23: all checks passed").

**Done**
- Found that `main` already held a weekly refresh workflow, its scripts and tests and one recorded run (21 Oct), never merged into `emo-2026-10`. Merged (91f0931), then adapted to the task (abb7bbd, 00b02b0):
  - `.github/workflows/weekly_refresh.yml`: Mondays 05:23 UTC plus manual run; starts from the branch head.
  - Each series in its own folder, `data/sources/<name>/`; `data/MANIFEST.json` records path, source URL, `downloaded_at`, sha256.
  - Commits only if `commit_allowed`: tests pass, ledger hash and frozen RDL outputs hold, every analysis ran. Otherwise results kept as a run artifact and the run fails.
- Analysis scripts changed in input paths only; text outputs identical to the 21 Oct record.
- No pre-registration: this task tests no hypothesis.

**Results**
- 95 tests pass on GitHub. Closes the session-1 question (82 defined vs 57): 95 now, including the refresh tests from `main`.
- OWID series unchanged since 20 Oct; OpenAlex counts drifted (recent years still being indexed). No conclusion drawn.
- One failure on record: run 39916346571 (queued run checked out a stale commit, push conflicted). Fixed in 00b02b0.

**Open questions**
- `ci.yml` triggers on pushes to `main`/`master` only, not `emo-2026-10`; CI does not run on the default branch. Not this session's task.
- `main` still carries the old `weekly-refresh.yml`; harmless (schedules fire only on the default branch).

**Adrian must do**
- Nothing. Optional: set an `OPENALEX_API_KEY` secret / `OPENALEX_MAILTO` variable.

## Next session
Session 3: the public mirror page (`docs/PLAN.md`). First check that Monday 26 Oct's scheduled run committed.

## Previous session: 1 (2026-10-23) — move the work home

**Done**
- Push access confirmed: commit d64b7d4 pushed to `emo-2026-10` on avram3scu-art/emo-core-v1.
- `docs/PLAN.md` transcribed from the plan doc (rev 17), with all 24 session prompts and the opening and closing blocks; roadmap diagram rendered as text.
- `CLAUDE.md` with the standing rules and closing routine.
- `README.md` rewritten: pillar status table identical to the plan's; "live", "deployed" and "ready" kept only where negated.
- `docs/STATUS.md` and `docs/SESSION_LOG.md` created.

**Not done**
- Nothing outstanding. The default branch could not be changed from the session (settings writes blocked, HTTP 403); Adrian changed it by hand, and `emo-2026-10` was confirmed as the default branch at close (09:05, 23 Oct). `main` kept.

**Found**
- `emo-2026-10` head was 691d3fe, not 9428f24: one extra commit (21 Oct) updating project URLs in pyproject.toml after the transfer. Harmless.
- `tests/` defines 82 test functions; the plan records 57 passing. The suite could not be re-run here (PyPI unreachable from this environment). To be reconciled in session 2, when the Action runs the tests.
- Other documents still claim a live system: `WHITEPAPER_EMO_v1_*`, `LIVE_PIPELINES.md`, `DESTINE_INTEGRATION.md`, `deck/`, `docs/DAC_V0_1_ISSUES.md`. README flags them; rewrite is session 15.

**Adrian must do**
- Nothing for session 1.

## Open questions
- 82 defined vs 57 passing tests: are 25 failing, skipped, or was 57 counted before tests were added?

## Next session
Session 2: the weekly GitHub Action (`docs/PLAN.md`).
