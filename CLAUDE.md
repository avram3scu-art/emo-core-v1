# CLAUDE.md — standing rules for every EMO session

These rules bind every session in this repository. If a session prompt conflicts with them, stop and say so.

## Start of every session

1. Read this file, `docs/STATUS.md`, and the entry for the current session in `docs/PLAN.md`.
2. Work on that session's task only. Stop when its "done when" is met, or say plainly why it cannot be met.
3. The weekly run is started every Monday 07:41 Brussels by an external scheduler (cron-job.org job "EMO weekly run", Adrian's account), which calls GitHub's workflow-dispatch API with a fine-grained token limited to Actions on this repo (set up and tested 26 Oct 2026, run 40329335301). GitHub's own cron also exists but is unreliable here (the 26 Oct Monday run fired six hours late; 5-minute probes never fired); its gate skips it when a run from the last 5 days exists. Check the latest weekly run (`gh run list -w weekly_refresh.yml -L 1`): if it is older than 7 days, start it (`gh workflow run weekly_refresh.yml --ref emo-2026-10`), report its result before the task, and tell Adrian the external starter may have failed (token expired?); if the last one failed, say so first.

## Before closing: review (every session)

When the task's "done when" is met, or cannot be met, and before the closing routine, give Adrian a short review and wait for his answer:

1. **More of this task now?** What could still be done on this session's task, and roughly what it costs.
2. **Change or improve?** Anything in the method, code, data, plan or these rules that should change, with the reason. Point out weaknesses in the session's own work, including Claude's own mistakes.
3. **Test before calling it open.** Anything that can be tested or verified within the session (a probe, a rerun, a check against the source) is done before it is listed as open, unless Adrian says otherwise.

Do not extend the task without Adrian's yes. If a review point changes these rules, update this file in the same session.

## "Not done" always gives its reason

Every item reported as not done or open names one reason:

- **Scope**: outside this session's task (rule: one task per session).
- **Adrian's decision**: irreversible, costly or his call (deleting, keys, accounts, money, method choices).
- **Needs time**: can only be verified later (e.g. a weekly schedule), with the date of the check.
- **Not attempted**: could have been done now but was not. Say so plainly; this is Claude's shortfall, not a limit.

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

1. Update `docs/STATUS.md`: date, session number, what was done, commits, results including failures, open questions (each with its reason), the review's improvement points and Adrian's answer, next session.
2. Append one row to `docs/SESSION_LOG.md`: date | session | task | done when met (yes/no) | key commit | note.
3. If a rule changed, update this file. Commit and push.
4. Report in six lines: done; not done (each with its reason); result; could still do or improve; next session; anything Adrian must do.

## Style

Keep replies short. Pushback over encouragement.
