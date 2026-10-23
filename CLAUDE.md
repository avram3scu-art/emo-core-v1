# CLAUDE.md — standing rules for every EMO session

These rules bind every session in this repository. If a session prompt conflicts with them, stop and say so.

## Start of every session

1. Read this file, `docs/STATUS.md`, and the entry for the current session in `docs/PLAN.md`.
2. Work on that session's task only. Stop when its "done when" is met, or say plainly why it cannot be met.

## Science rules

- **Pre-register every test before opening its data.** Commit the protocol (hypothesis, data, statistic, pass/fail threshold) first; only then fetch or open the data. Failures stay on record.
- **Profiles, never a weighted scalar.** DAC, UIA and every other multi-part measure are reported as a profile of their components. No weighted sum or composite score with chosen weights. A scalar may appear only if labelled a convenience summary that carries no weight in any conclusion.
- **No claim beyond what the code does.** Every statement in a README, paper or report must point to a script, dataset or test that does it today. Do not write "live", "deployed", "ready" or "validated" unless it is true and evidenced.
- **RDL is not a validated recommender.** RDL v0.2 and v0.3 failed their held-out tests. Never present RDL output as a recommendation, only as a tested-and-failed or untested hypothesis.
- **Cite only sources opened.** Cite only what was opened in the session (fetched page, file, dataset) or supplied by Adrian. Anything else is marked unverified. Never claim novelty without a search, and say what could not be searched.

## AI disclosure (Adrian's three-point form)

Use this wording in papers, grant applications and releases:

1. All inputs were the author's own manuscript text, code and publicly available reference literature and data (plus synthetic simulation parameters where applicable).
2. All AI-assisted outputs were verified by the author.
3. All scientific claims and interpretations are the author's own.

Do not add "no AI tool is listed as an author". Manuscripts carry "Adrian N. Avramescu" under the title.

## Closing routine (every session)

1. Update `docs/STATUS.md`: date, session number, what was done, commits, results including failures, open questions, next session.
2. Append one row to `docs/SESSION_LOG.md`: date | session | task | done when met (yes/no) | key commit | note.
3. Commit and push.
4. Report in five lines: done, not done, result, next session, anything Adrian must do.

## Style

Keep replies short. Pushback over encouragement.
