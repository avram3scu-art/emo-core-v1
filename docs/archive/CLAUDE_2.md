# CLAUDE.md 2.0 — standing rules for every EMO session

In force from 29 Oct 2026 (session 2.0-design, Adrian's yes, 04:57). It keeps every rule of CLAUDE.md 1.x word for word (archived in `docs/archive/CLAUDE_1.md`) and adds the rules marked **[2.0]**.

**[2.0] Purpose.** EMO tests one idea: that humanity's response to what it knows behaves like a mind, a loop of predicting, attending, deciding and acting, choosing remedies, and learning, whose links are coupled and improve with experience. The hypotheses H1–H7 in `docs/PLAN.md` state this so it can fail. Every session serves one of them.

These rules bind every session in this repository. If a session prompt conflicts with them, stop and say so.

## Start of every session

1. Read this file, `docs/STATUS.md`, and the entry for the current session in `docs/PLAN.md`.
2. Work on that session's task only. Stop when its "done when" is met, or say plainly why it cannot be met.
3. The weekly run is started every Monday 07:41 Brussels by an external scheduler (cron-job.org job "EMO weekly run", Adrian's account), which calls GitHub's workflow-dispatch API with a fine-grained token limited to Actions on this repo (set up and tested 26 Oct 2026, run 40329335301). GitHub's own cron also exists but is unreliable here (the 26 Oct Monday run fired six hours late; 5-minute probes never fired); its gate skips it when a run from the last 5 days exists. Check the latest weekly run (`gh run list -w weekly_refresh.yml -L 1`): if it is older than 7 days, start it (`gh workflow run weekly_refresh.yml --ref emo-2026-10`), report its result before the task, and tell Adrian the external starter may have failed (token expired?); if the last one failed, say so first. The token expires **26 Oct 2027**: from 19 Oct 2027, remind Adrian at session start to renew it.
4. **The repository is the only memory.** Everything a session needs (data, event files, manuscripts, protocols, earlier results, decisions) must be found in this repo. Do not rely on past chats, Claude's memory or Adrian's recollection. If something needed is not in the repo, say so first, name it, and record the gap in `docs/STATUS.md`. A past chat may be used only to locate an item; the item is then committed to the repo before it is used, with its origin noted.
5. **[2.0] Hooks on** (from session 2.1, which builds `scripts/hooks/pre-push`). Run `git config core.hooksPath scripts/hooks` once per clone, so the pre-push hook runs the claim-word check, ruff and the fast tests and refuses the push on any failure. A push with `--no-verify` is not allowed. **[2.0]** Also once per clone, install the locked tools the hook needs: `pip install --break-system-packages -r requirements-lock.txt` (added 29 Oct 2026, session 2.9: ruff was missing in three sessions).
6. **[2.0] Name the hypothesis.** Say at the start which hypothesis (H1–H7, `docs/PLAN.md`) the session moves, and how. A session that moves none (infrastructure) says so.

## Before closing: review (every session)

When the task's "done when" is met, or cannot be met, and before the closing routine, give Adrian a short review and wait for his answer:

1. **More of this task now?** What could still be done on this session's task, and roughly what it costs.
2. **Change or improve?** Anything in the method, code, data, plan or these rules that should change, with the reason. Point out weaknesses in the session's own work, including Claude's own mistakes.
3. **Test before calling it open.** Anything that can be tested or verified within the session (a probe, a rerun, a check against the source) is done before it is listed as open, unless Adrian says otherwise.

4. **[2.0] Improve before closing.** If the session's own findings show an improvement to the session's own work (a better method, a found defect, a clearer text) that can be made and checked within the session in about 15 minutes, propose it with Claude's recommendation and, on Adrian's yes, do it before closing; the session closes only when no such improvement is left or Adrian declines it. An improvement that would change a pre-registered test, use data already seen, or start a different task is not made in place: it becomes the next session's prompt; so does a larger improvement, unless Adrian says otherwise.

Do not extend the task without Adrian's yes. If a review point changes these rules, update this file in the same session.

**Every question to Adrian carries Claude's recommendation** (rule added 28 Oct 2026 at Adrian's request). Any question or choice put to him (yes/no, "more of this task?", "change or improve?", options) states the option Claude recommends first, with a one-line reason, so he can answer with one word. He is not expected to weigh the details himself.

**Claude's own mistakes are always fixed completely** (same date). When Claude finds or is shown a mistake of its own, it does everything needed to fix it in that session and records it; time and Adrian's weekly allowance are not reasons to leave it unfixed.

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
- **RDL is not a validated recommender.** RDL v0.2 and v0.3 failed their tests on reserved historical cases (known outcomes, not blind). Never present RDL output as a recommendation, only as a tested-and-failed or untested hypothesis.
- **One evidence class on every result** (rule added 28 Oct 2026, fix session F6, approved by Adrian). Every result in the README, the public page, a protocol, a paper or a report carries exactly one class: pre-registered blind (protocol committed before the data were opened, and the outcome unknown to Adrian and Claude); pre-registered on known history (protocol first, but the outcome of the cases was known); exploratory (no pre-registration); infrastructure (code, CI, data plumbing, synthetic method checks). A test on cases whose outcome is known to Adrian or Claude is never called held-out or blind.
- **A pass needs a significance test of the condition that decides it** (same date). Every condition that can turn a FAIL into a PASS is tested for significance, with correction for multiple or sequential tests, and with a null that respects the data's dependence (overlap, clustering, trend). It is never decided by a point comparison. A non-significant result is never used as evidence of no effect; a "no effect" condition needs an equivalence bound fixed in advance.
- **[2.0] Repair, don't drop.** A component that fails its test is neither hidden nor quietly abandoned. In the session of the failure it gets a written diagnosis (what failed, why, evidence) in its protocol and a row in `docs/FAILURES.md`; at that session's review Adrian chooses, on Claude's recommendation, one of three outcomes: **repair** (a new version with a new pre-registered test), **replace** (a different tool for the same loop link), or **retire** (with the reason). The failed version and its result stay on record unchanged.
- **[2.0] No retesting on seen data.** A repaired or new version is never tested on the data that exposed the failure or that were used to build it. Its test uses data not yet opened, preferably data that do not exist yet when the protocol is committed. A rerun on seen data is labelled exploratory and carries no weight in a verdict.
- **[2.0] Prospective first.** When a choice exists, prefer a test whose outcomes occur after the protocol is committed (a coming season, a dated forecast) over a test on history. Every historical test states why no prospective test was possible.
- **[2.0] Power before data.** Every protocol states, from synthetic data, the false-positive rate and the power of its test at the expected sample size before its data are opened. A test with power below 0.5 is run only if the protocol says so in its first line, and a FAIL then reads "not shown at this size".
- **Cite only sources opened.** Cite only what was opened in the session (fetched page, file, dataset) or supplied by Adrian. Anything else is marked unverified. Never claim novelty without a search, and say what could not be searched.

## AI disclosure (Adrian's three-point form)

Use this wording in papers, grant applications and releases:

1. All inputs were the author's own manuscript text, code and publicly available reference literature and data (plus synthetic simulation parameters where applicable).
2. All AI-assisted outputs were verified by the author.
3. All scientific claims and interpretations are the author's own.

Do not add "no AI tool is listed as an author". Manuscripts carry "Adrian N. Avramescu" under the title.

**[2.0] Contributions line** (Adrian's yes, 29 Oct 2026 05:15). Claude is credited by name for its role, not as an author. Next to the disclosure, in the README, release notes, papers and grant applications:

> Contributions: Adrian N. Avramescu (concept, decisions, verification). Claude (Anthropic) contributed code, data coding, analysis and drafting under the author's direction.

## Recording (every session, as the work happens)

Adrian does not keep records; Claude does. Every test, simulation, probe, run, conversion, fetch and failed attempt is recorded in the repo in the same session, never only in the chat or Claude's workspace:

- **Index:** one row per item in `docs/RECORD.md`: date | session | type | class (pre-registered blind / pre-registered on known history / exploratory / infrastructure) | what | protocol | code | data | result (PASS/FAIL/error) | commit or run ID.
- **Files:** protocol, code, input data (or a fetch script plus checksum when the data cannot be committed), outputs and figures are committed; a GitHub run ID alone is not a record.
- **Sources:** every external source opened is listed with URL and access date in the file that uses it; a source supplied by Adrian is committed (or, if it cannot be, its absence is recorded).
- **Decisions:** Adrian's choices and their reasons go in `docs/STATUS.md` when made.

**Run the claim-word check before every push** (rule added 28 Oct 2026, session 10b, at Adrian's request): `python scripts/claims_grep.py` must report `unjustified=0` locally before `git push`; a hit is fixed by rewording, or, in a pre-registered file that must not change, by a justification entry in the script.

## Closing routine (every session)

0. Check the record: `git status` is clean (nothing created or used is left uncommitted); every item of the session has a row in `docs/RECORD.md`; nothing the next session needs exists only outside the repo. Report any gap.
1. Update `docs/STATUS.md`: date, session number, what was done, commits, results including failures, open questions (each with its reason), the review's improvement points and Adrian's answer, next session.
2. Append one row to `docs/SESSION_LOG.md`: date | session | task | done when met (yes/no) | key commit | note.
3. If a rule changed, update this file. Commit and push.
4. Report in seven lines: done; not done (each with its reason); result; hypothesis moved [2.0]; could still do or improve; next session; anything Adrian must do.
5. **Write the next session's prompt** (rule added 29 Oct 2026 at Adrian's request). After the close, write the complete opening prompt for the next session, ready to paste: session number and name, the instruction to read CLAUDE.md, `docs/STATUS.md` and its `docs/PLAN.md` entry, the task, its inputs, any decision or finding from this session it must use, and its "done when". Put it in `docs/PLAN.md` (new or updated entry, committed with the close) and give it to Adrian in one monospace block.

## Style

Keep replies short (except when fixing Claude's own mistakes). **[2.0]** Copy-paste text (prompts, emails, sentences for Adrian) goes in one monospace block. Pushback over encouragement. Every question comes with Claude's recommended answer.
