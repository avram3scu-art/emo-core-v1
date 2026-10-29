# Hostile editor-style review: "EMO: what runs today" (session 15)

Reviewer: Claude, 29 Oct 2026, of `docs/WHITEPAPER_EMO_what_runs_today.md` as committed in session 15. Read as a skeptical editor of a policy/infrastructure white paper (funder audience) and as a skeptical reader of a project status report.

## Verdict

**Not fit to share yet.** Fit to stand in the repository as an honest status document once points 1–3 are fixed. As a white paper meant to persuade a funder or partner, it would very likely fail (judgement, not data): it proves the project is honest, not that it is worth funding.

## Checks done in the session

- Every relative link in the draft resolves to a file in the repo (script check, 29 Oct).
- Claim-word check: `unjustified=0` after seven rewordings.
- Numbers checked against their files: mpox lags (−39, −25, −1; +22, +36, +60 with early t0), Belgian delivery t0 + 46 and FFP2 56 d (reading A), GWI 14/21 vs 9/275 and p = 2.3e-13, RDL v0.2/v0.3 held-out results, synergy and GWI-calibration FAILs, He false-positive rates, a_UIA audit.
- **Error found and fixed in the draft:** τ_I was initially written "3–4% a year", copied from README; the weekly output gives 2.3% at 12 h and 3.0–4.0% at 24–120 h. README carries the same error (point 3).

## Points, most serious first

1. **The AI disclosure's point 2 is not true today.** "All AI-assisted outputs were verified by the author": Claude drafted this paper and coded every DAC file; no record shows Adrian has verified either (F14 found the same problem in the manuscript). Before sharing, either Adrian verifies the draft and that is recorded, or point 2 is reworded to what is true. Blocker.
2. **The vision does not connect to the demonstration.** §1 frames humanity as an "emergent mind"; nothing in §2–§4 tests or even uses that framing. What runs is a weekly cron job, unit tests, two exploratory DAC cases, three known-history DAC files, one τ_I trend that restates NHC, one GWI pass with an invalid placebo condition, half-surviving SMF results, and a stack of FAILs. A skeptical reader will ask why this is called an observatory of a mind rather than a set of response-lag and forecast-skill measurements. Either cut §1 to the measurement questions, or add one honest sentence that the framing is a motivating hypothesis no result supports.
3. **README contradicts the paper.** README still says the PPE case is "not in this repository", gives 91 tests (now 149), and has the wrong τ_I range. The paper points to README as a source in two places. Fix README before anyone sees either.
4. **Thin positive evidence.** The only positive blind result is GWI on one hazard class, decided by one condition, with its threshold failing calibration. Every DAC result is exploratory or known history, coded by an AI with no second coder. That is not a white-paper case; it is a status report. Retitling or reframing it as "status report" would be more accurate than "white paper".
5. **No audience and no ask.** The old paper named funders; this one names none and asks nothing. If it is for funders, it needs one concrete ask; if it is a status note, say so and drop the funder language from §1.
6. **Several facts rest on STATUS.md, not on primary files:** the test count (149), the frozen-check result, the Futures desk rejection dates (backed by a committed PDF, acceptable), "ECMWF declined data access" (README only; no letter in the repo). Mark the ECMWF line unverified or commit the evidence.
7. **Links are relative and branch-bound.** Shared as a PDF they break; at release (session 17) they should point to a tagged commit.
8. **Novelty and related work.** No novelty claim is made, correctly. But §1's "the narrow thing EMO adds today is form" leans on a session-4 search of named sources only; a reviewer may still find the regime-effectiveness literature covers the same ground (RELATED_WORK says so). Keep it, it is honest.

## Venue and chance

No journal fits this document. Realistic use: a page in the repository, later the public page or a release note. If sent to a funder in its present form: low chance of interest (judgement). Do not share the same day; earliest after points 1–3 and Adrian's own read.
