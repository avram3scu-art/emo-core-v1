# EMO status

Updated at the close of every session. Plan: `docs/PLAN.md`. History: `docs/SESSION_LOG.md`.

## Current state (28 Oct 2026)

- **Plan position:** fix sessions before session 10. Done: F1, F2, F3, F4. Next: F5 (SMF re-analysis), F6 (method labels), F7 (DAC clean-up incl. validator gaps D1–D6), F8 (recode the PPE case: its event files were not recovered). Session 10 (mpox) after them (`docs/FIX_PLAN.md`).
- **Runs:** weekly run every Monday 07:41 Brussels via cron-job.org (token expires 26 Oct 2027). CI: tests (91), mypy, ruff, claim-word check.
- **Results on record:** README table, each with its evidence class; every test and run in `docs/RECORD.md`; sessions 1–8 in `docs/STATUS_ARCHIVE.md`.
- **Open A items (audits 26b, 27 Oct):** SMF deciding condition untested (F5). PPE case not in the repo (F8).
- **Adrian must do:** nothing now.

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
