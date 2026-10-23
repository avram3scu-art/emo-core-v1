# EMO status

Updated at the close of every session. Plan: `docs/PLAN.md`. History: `docs/SESSION_LOG.md`.

## Last session: 2 (2026-10-23) — the weekly GitHub Action

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
