# Hostile editor-style review: "EMO: what runs today, and what it has not shown" (session 2.13)

Reviewer: Claude, 29 Oct 2026, of `docs/WHITEPAPER_EMO_what_runs_today.md` as revised in session 2.13. Read as a skeptical editor and as a skeptical researcher in disaster-response evaluation (the paper's stated audience). Evidence class of this file: infrastructure (review of committed files; no data opened).

## Verdict

**Not fit to share yet; fit to stand in the repository as the status paper.** It is accurate and traceable, but its central claim cannot be judged by any result it reports, and one blocker (disclosure point 2) is the author's to remove. Do not send it anywhere today.

## How the session 15 review points were handled

| S15 point | Handling in this draft | State |
|---|---|---|
| 1 Disclosure point 2 untrue | Point 2 withheld, marked "not true today", until the author's verification is recorded in `docs/STATUS.md` | **open: Adrian's decision/action** |
| 2 Vision not tied to results | §1 replaced by the hypothesis, the independent-agencies null and the H1–H7 table; states that no result supports the "mind" reading; §3 is organised by loop link and hypothesis | fixed |
| 3 README contradicts paper | PPE and τ_I lines were already fixed; test count updated (154 → 200, CI run 40895686707); the paper no longer cites README for any fact | fixed |
| 4 Thin evidence; "white paper" overstates | Retitled to say what it has not shown; called a status paper | fixed in framing; evidence still thin (point 2 below) |
| 5 No audience, no ask | One audience (researchers evaluating disaster response or early warning), one ask (a second coder for the mpox file), funding language removed | fixed, with a new risk (point 3 below) |
| 6 Facts resting on STATUS | Test count from the CI run, frozen check from `results/weekly/2026-10-29/SUMMARY.md`, ECMWF from the committed reply `docs/sources/ecmwf/SD-131630_reply.md` | fixed |
| 7 Relative, branch-bound links | Stated; pinned to a tagged release at session 2.15 [plan] | open: needs time (session 2.15) |
| 8 Related work | Kept; no new search | unchanged (no search this session; scope) |

## Points, most serious first

1. **Blocker: disclosure point 2, and the contributions line.** Point 2 is withheld, correctly. But the contributions line credits the author with "verification", which is the same claim. Until the verification is recorded, either withhold that word too or keep the paper unshared. Recommendation: keep the line as decided and do not share before the verification is recorded.
2. **The central claim has no evidence and cannot get any soon.** H4 and H5 are the only hypotheses that bear on the "mind" reading. H4: untestable on 2015–2025; every registered route has power < 0.5 (hurricane blind arm 0.15–0.38 after 5–10 seasons; flood news pressure 0.06–0.34); not decidable in hurricanes before about 2036. H5: power 0.06. An editor will ask why a reader should care now. The honest answer, which the paper gives, is the form (registered, power-stated, failure-recorded tests), not a finding. That is a narrower contribution than the title's subject suggests.
3. **The ask conflicts with its own blindness rule.** `docs/DOUBLE_CODING.md` (§2, and the invitation) says the invitation must not link the repository. This paper links it throughout. Mpox results are withheld here, but a reader recruited through the paper is one click from Claude's file and would likely end as "known history" for the agreement result. Recommendation: send candidate coders the invitation and packet only, not this paper; keep the ask in the paper but route it to the invitation.
4. **Positive evidence remains thin and partly confounded.** The only blind PASS is GWI v1's event test, on one condition, with its calibration failed. The He PASS is known history and confounded by intensity (stated). SMF v1 survivors are known history. Everything else is FAIL, "cannot be tested", "not shown" or registered-not-scored.
5. **A fifth label.** "[blind, registered]" is not one of the four classes in `CLAUDE.md`. It marks commitments, not results, and is defined in the paper, so no result carries two classes; but a strict reader may object. Option: write "class on scoring: pre-registered blind", as the protocols do.
6. **Phase gate.** `docs/PLAN.md` §8 opens Phase C (where 2.13 sits) only after the 2027 registry is deposited (Zenodo version 2, pending, Adrian's action, before 1 June 2027). This session ran before that gate. Harmless for a draft that is not shared; it should not be shared before the deposit either, since §3.7 calls the deposit [plan].
7. **Mixed engine.** GWI v2's event test uses earthquakes, not the hurricane loop, and its threshold was tuned on seen articles (stated). It tests H2 in general, not the attend link of the engine domain.
8. **Density.** Tables of numbers with many caveats; on a phone the H1–H7 table and §3.4 are hard going. Minor.

## Checks done in this session

- Every relative link in the draft resolves (script check, 29 Oct 2026; this file created in the same commit).
- Claim-word check: `unjustified=0` after five rewordings (validated → checked; first → earliest ×2; "not a validated recommender" → "has passed no test"; "Prospective tests first" → "are preferred").
- Numbers checked against their files: τ_I (`results/weekly/2026-10-29/information_time_nhc.txt`); hurricane H3/H4/H5 (`docs/LOOP_PROTOCOL.md` §19); He test p = 0.0116 (`analysis/he_loop_test_output.txt`); 2027 ledger power 0.234 (§21.1); blind-arm power 0.15/0.38 (§20.5); SMF v2 (`docs/SMF_PROTOCOL.md` §15.6); GWI v2 (`analysis/gwi_v2_synthetic_output.txt`, protocol §7); flood §5, §8–§11 and F13; CI 200 passed (run 40895686707 log); 19 frozen reproductions (`results/weekly/2026-10-29/SUMMARY.md`).
- Not checked against a primary file: the Zenodo deposit date 20 Oct 2026 (carried from the session 15 draft and `docs/RDL_FORECAST_LEDGER.md`; the DOI was not opened this session).

## Venue and chance

No journal fits. Realistic use: the repository's status paper and later the public page or a release note. Sent to a research group in its present form: low chance of engagement beyond the coder ask (judgement). Earliest sharing: after the author's recorded verification, the Zenodo version 2 deposit, and not the same day as this review.
