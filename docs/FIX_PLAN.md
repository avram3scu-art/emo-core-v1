# Fix sessions F1–F8 (before session 10)

From `docs/AUDIT_2026-10-26b.md` §2. Each fix is one session: paste the opening block from `docs/PLAN.md`, then the "Prompt for Claude" below (with N = F1, F2, …). "Adrian does" lists what only Adrian can do, before or during the session. Session 10 starts only after F1–F7 are closed (and F8 if F1 recovers no event files).

---

## F1 — DAC paper facts and files

**Adrian does (before the session, ~10–20 min):**
1. Look in your email / JCCM account: was "Decision or Supply?" (or another version) submitted? Note the date, journal, manuscript number and status.
2. Open the chat "Combining DAC EMO UIA RDL" on claude.ai and download every file card you find: final anonymised manuscript, title page, Supporting Information, figures, every `.csv` (event files, Belgian order file) and every `.py` script.
3. Attach all of them in the F1 session, with one line: submitted yes/no, date, status.

**Prompt for Claude:**
```text
Session F1 task: bring the DAC paper's facts and files into the repo (audit R1–R3).
Commit every file I attach to docs/sources/dac_paper/ with an origin note (what, from where, date) and sha256 in a README there. Identify the final manuscript version and say how it differs from docs/sources/DAC_JCCM_manuscript_anonymised.docx. Record the submission facts I give (journal, date, number, status) in docs/STATUS.md. List what is still missing (event files, order file, scripts) by name. If the data statement of the submitted version is not true today, draft a short letter to the editor for me (copy-paste block), but do not send anything.
Done when: every attached file is committed and indexed, the submission facts are recorded, and the missing list is in docs/STATUS.md.
```

---

## F2 — Truth pass on public files

**Adrian does:** read the banners and README changes Claude shows at the end and answer "yes" or say what to change. Decide: keep the white papers, deck and grant (with banners) or move them to `archive/`.

**Prompt for Claude:**
```text
Session F2 task: make every public file true today (audit P1–P4).
(1) README: DAC row states only what the repo holds (ozone/climate; PPE case not in the repo until F1/F8), test note fixed with the current count read from CI, every result labelled by evidence class (pre-registered blind / pre-registered on known history / exploratory). (2) A dated banner at the top of each WHITEPAPER_EMO_v1_*, deck/, grants/, README_EMO.md and EMOStakeholderBenefits.md: superseded, describes a system that does not exist, see README; every "first"/novelty claim removed or marked unverified. (3) Move DAC_ARCHITECTURE.md, DAC_V0_1_ISSUES.md, DAC_V0_1_ROADMAP.md to docs/archive/ with a note. (4) grep the whole repo for live / real-time / deployed / operational / validated / ready / first and list each remaining hit with its justification. Show me the banners and README diff before committing.
Done when: the grep list has no unjustified hit and I have approved the banners and README.
```

---

## F3 — Records backfill

**Adrian does:** nothing during the session; at the end, open `docs/RECORD.md` on GitHub and check that it reads clearly on your phone.

**Prompt for Claude:**
```text
Session F3 task: index every test, run, probe and failure of sessions 0–8 in docs/RECORD.md (audit R4, R6).
Source: git history (git fetch --depth=2000), docs/STATUS.md, docs/SESSION_LOG.md and the protocol files. One row per item with commit or run ID; failures included; evidence class column added (pre-registered blind / pre-registered on known history / exploratory / infrastructure). Then split docs/STATUS.md: current state on top, sessions 0–8 moved verbatim to docs/STATUS_ARCHIVE.md; rewrite docs/SESSION_LOG.md as one row per session with real commit IDs (no "(this commit)" or "(see STATUS)"), old rows kept in the archive.
Done when: every protocol result and every recorded run in sessions 0–8 has a row, and no SESSION_LOG row has a placeholder commit.
```

---

## F4 — CI readability

**Adrian does:** nothing.

**Prompt for Claude:**
```text
Session F4 task: make CI results readable from the session without log access (audit T1).
Change .github/workflows/ci.yml and weekly_refresh.yml so that the pytest summary line (passed/failed/skipped counts) and every failing test with its first error line appear as annotations, as mypy and ruff already do. Prove it: push a temporary failing test on a branch, read the failure through the annotations API, then remove it. Record the current test count in docs/RECORD.md and README.
Done when: a deliberate failure was read from annotations, the branch is deleted, and the test count is recorded.
```

---

## F5 — SMF re-analysis (pre-registered)

**Adrian does:** read the protocol summary Claude shows before running and answer "go" (or change it). Nothing else.

**Prompt for Claude:**
```text
Session F5 task: test the condition that decides every SMF pass (audit S1, S2, S5).
First commit a protocol in docs/SMF_PROTOCOL.md (new section, before any computation): Diebold–Mariano test of model vs "no change" (squared error, HAC variance with h−1 lags, Harvey small-sample correction), on the committed primary samples of §8, §10, §11 and §12; Holm correction across all of them; pass = model better at Holm-adjusted p < 0.05. State in advance how each README sentence will be rewritten for each outcome. Show me the protocol, wait for "go", commit, then run once on committed data (no refetch), record, and rewrite the README/page SMF lines from the result. Add the SMF and synergy recorded runs to the weekly frozen-output check using committed data.
Done when: the result is in the protocol file, README/page follow it, and the frozen check includes SMF and synergy.
```

---

## F6 — Method labels and the evidence-class rule

**Adrian does:** approve the new CLAUDE.md rule text Claude shows (yes / change).

**Prompt for Claude:**
```text
Session F6 task: label every method result by what its test can support (audit S3, S4).
(1) RDL docs and README: backtest and v0.3 held-out tests labelled "pre-registered on known history (not blind)"; the forecast ledger named as the only blind RDL test. (2) docs/GWI_PROTOCOL.md: note that criterion 3 treated a non-significant placebo as evidence, and how any future GWI test will avoid this. (3) Add to CLAUDE.md, Science rules: every result is labelled with one evidence class; a test on cases whose outcome is known to the author or Claude is never called held-out or blind; a pass needs a significance test of the condition that decides it. Show me the rule text before committing.
Done when: the labels are in place, the rule is in CLAUDE.md and I have approved it.
```

---

## F7 — DAC clean-up

**Adrian does:** nothing, unless Claude asks you to open a page it cannot reach (it will name the page).

**Prompt for Claude:**
```text
Session F7 task: finish the DAC standard and clean the DAC code (audit R3, T2, T3, ozone/climate sources).
(1) If F1 brought the final manuscript: add the "Identification" row of its Table S1 to docs/DAC_STANDARD.md, the schema and the validator (per good: number of paired orders and spread of order dates), with tests. (2) Retire emo/metrics/dac/ and emo/models/{diagnostic_event,policy_instrument,delivery_trace}.py if unused, or route them through emo/dac_standard.py; tests stay green. (3) Replace the Wikipedia sources of the ozone and climate t0 and binding-act events with primary records (Molina & Rowland 1974 in Nature; Charney report 1979; Montreal Protocol and Kyoto Protocol texts), opened and cited with URL and date; rerun scripts/convert_dac_csv.py and record. (4) Regenerate the pandoc .md of any manuscript in docs/sources by a script, not by hand.
Done when: tests pass, every ozone/climate t0 and binding-act row has a primary source, and the Identification row is in (or recorded as waiting for F1).
```

---

## F8 — Recode the PPE event files (only if F1 recovers none; 2–4 sessions)

Limit, stated now: the manuscript (with Tables 2–3) is in the repo and was read in session 9, so blindness rests on each F8 session not opening those tables; each session records whether it did.

**Adrian does:** (1) supply or open the sources Claude cannot fetch: the Dutch NSOB/VWS reconstruction, the Bundestag papers, any EU act Claude names; (2) decide whether the seven PDFs you sent (~60 MB) may be committed (Sudhof report is marked "VS – Nur für den Dienstgebrauch"); (3) at the end, decide what to tell JCCM.

**Prompt for Claude (first of the F8 sessions):**
```text
Session F8 task: rebuild the PPE event files in the DAC standard from primary sources, blind to the manuscript's results.
First commit docs/DAC_PPE_CODING.md: coding rules per sublayer (from the manuscript's Sections 2–3 only, not its tables), the source list per country with what is in the repo, and the comparison protocol: after all six files are coded and validated, compare their profiles with manuscript Tables 2–3, every difference reported, none adjusted after seeing the tables. Then code one case per sitting (Belgium first, including the order file and both readings of the contested first order) into data/dac_ppe/<case>.json, validated by emo/dac_standard.py, each source cited with page. Do not open Tables 2–3 or Figures 1–2 of the manuscript until the comparison step.
Done when (this session): coding rules committed and the Belgian file plus order file validated and committed. Later F8 sessions: one or two cases each; the last one runs the pre-registered comparison.
```
