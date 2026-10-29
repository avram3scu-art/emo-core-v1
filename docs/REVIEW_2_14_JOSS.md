# Editor-style review: EMO-Core for JOSS (session 2.14, 29 Oct 2026)

Reviewer stance: a skeptical JOSS editor doing the pre-review scope check, using the requirements opened today (`docs/JOSS_CHECKLIST.md`). Class: infrastructure.

## Verdict

**Not eligible now; do not submit.** If submitted today, a desk rejection at the scope check is close to certain (Claude's estimate: above 90%), on development history alone. Earliest sensible submission: **after 19 April 2027**, and only if the three conditions below are met. Realistic chance of acceptance then: about 25–40% (estimate, not computed), limited mainly by research impact and by how much of the package is reusable outside this one project.

## Blocking issues

1. **Development history.** JOSS asks for more than six months of public, sustained development and names concentrated bursts as disqualifying. The default branch starts on 19 Oct 2026 from a snapshot; about 450 commits fall in ten days; there were no commits May–Sep 2026. The earlier branch (Nov 2025–Apr 2026) helps only if the editor counts it and the repo was public then, which could not be checked.
2. **Human verification in the AI disclosure.** JOSS requires the authors to affirm that humans reviewed, modified and checked all AI-assisted output and made the design decisions. Today 344 of about 430 commits are by `claude`, disclosure point 2 is withheld, and the white paper states that no human has checked an AI-coded decide-act file. Writing point 2 before the check is done would be an inaccurate disclosure, which JOSS treats as an ethical breach. This is the most serious issue because it is about truth, not timing.
3. **Research impact.** The software is used only by its author, and most of its results are failures or exploratory. JOSS accepts developer use as a minimum but rejects "future use" as evidence. One outside use (the returned second-coder sheet, or another group coding a case in the DAC format) would change this more than any text.

## Major issues

4. **Is it one project's analysis code?** Of 3,349 lines in `emo/`, the hurricane loop, NHC, remedy backtest and much of SMF serve EMO's own registered tests. A reviewer will ask what another group would install it for. The defensible reusable core is the DAC event-file standard (format, schema, validator, contested-date profiles). **Recommendation:** submit (when eligible) a paper centred on the DAC standard, with the rest described as the project's applications; this also shortens the claim that must be verified (point 2).
5. **State of the field compares no software.** `docs/RELATED_WORK.md` compares datasets and studies (OxCGRT, regime-effectiveness work, WGI). JOSS asks for comparison with other tools and a build-versus-contribute reason. Without a search for comparable event-coding formats and tools, this section fails the checklist item.
6. **AI disclosure: early tools.** Resolved 29 Oct 17:04: Adrian states Claude was the only AI tool for all code; the draft says so and that the model versions before 19 Oct 2026 were not recorded. Since Claude wrote nearly all the code, issue 2 (human verification) carries more weight, not less.
7. **Editor conversation rule.** JOSS forbids AI use in conversation with editors and reviewers, except translation. Review replies would have to be written by Adrian.

## Minor issues (fixed this session)

- LICENSE was a summary (GitHub: NOASSERTION); now the full AGPL-3.0 text.
- No CONTRIBUTING or support statement; added.
- No usage example; added and run.
- Python version inconsistent (3.10 vs 3.11); aligned to 3.11, what CI tests.

## Minor issues (open)

- No tagged release, CHANGELOG or CITATION.cff (session 2.15).
- No API reference.
- Two of three references not re-opened today (`paper/paper.bib` header); WGI author given names missing.
- Superseded white papers, deck and grants at the repo root.

## Is the paper honest?

Yes, as drafted: it claims a narrow contribution, says the difference from regime-effectiveness work is form not question, reports the failures and the single-coder state, and withholds point 2. Honest is not the same as eligible: the blockers above are facts about the repository, not about the text.

## Submission timing

No submission before 30 Oct 2026 in any case (session rule: at least one day after the review). On this review, no submission before 19 Apr 2027.
