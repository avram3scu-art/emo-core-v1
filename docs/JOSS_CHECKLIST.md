# JOSS submission checklist — EMO-Core (session 2.14, 29 Oct 2026)

Class: infrastructure. Nothing submitted. Draft paper: `paper/paper.md`, `paper/paper.bib`. Review: `docs/REVIEW_2_14_JOSS.md`.

## Sources opened (29 Oct 2026)

- JOSS, Submitting a paper: https://joss.readthedocs.io/en/latest/submitting.html
- JOSS, Policies (AI usage): https://joss.readthedocs.io/en/latest/policies.html
- JOSS, Paper format: https://joss.readthedocs.io/en/latest/paper.html
- JOSS, Review checklist: https://joss.readthedocs.io/en/latest/review_checklist.html
- Seen in search results, not opened: a `pre-2026-submission` version of the docs (requirements changed in 2026) and the JOSS blog post "Preparing JOSS for a generative AI future" (Jan 2026). The `latest` pages above were used.
- Repository facts from the GitHub REST API (29 Oct 2026): created 2025-11-30; issues enabled; 0 stars, 0 forks; contributors by commit: `claude` 344, `avram3scu-art` 48, `github-actions[bot]` 41; 5 issues, all opened by `avradri`; branch `original-upload`: 68 commits Nov 2025, 46 Dec 2025, 4 Feb 2026, 288 Apr 2026; branch `emo-2026-10` (default): 449 commits, all from 19 Oct 2026, root commit "snapshot original upload" (history not connected to `original-upload`); no tags, no releases.
- Licence text: SPDX `AGPL-3.0.txt` from the `spdx` 2.5.1 wheel on PyPI (sha256 abbd50a363f1dc55faa9e15293c39294e65786f6a572b4345384c9994371e932).

## Requirement by requirement

| # | JOSS requirement | EMO today | Gap | Action |
|---|---|---|---|---|
| 1 | OSI-approved licence, plain-text LICENSE | LICENSE held an 8-line summary; GitHub reported NOASSERTION | small | **Fixed:** full AGPL-3.0 text in `LICENSE`; dual-licence note stays in README and `LICENSE-COMMERCIAL` |
| 2 | Code, files and issue tracker open without registration; anyone can open issues | public repo, issues enabled | none | — |
| 3 | Obvious research application | measurement of warning → decision → delivery lags; registered tests | none | — |
| 4 | Submitting author is a major contributor | 48 of ~430 commits by Adrian's account; 344 by `claude` | **large** | JOSS allows AI use with disclosure; a reviewer will still ask what the human contribution was. The contributions line answers it only once point 2 (verification) is true. Adrian's decision |
| 5 | Public for > 6 months with active development across the period; no concentrated burst | repo created Nov 2025, but no commits May–Sep 2026 and ~450 commits in 10 days of Oct 2026; default branch history starts 19 Oct 2026 | **large** | Needs time: steady public development to at least 19 Apr 2027 (6 months from the default branch's root); state the `original-upload` history in the submission. Whether the repo was public before Oct 2026 could not be checked (GitHub does not show visibility history) |
| 6 | Evidence of research impact (use at least by the developers; ideally by others); future use not enough | used by the author only; no external user, no citations searched | **large** | Needs time / outside use: e.g. the second coder's returned DAC sheet, or another group coding a case in the DAC format |
| 7 | Single-author open-practice indicators: public history, tagged releases or changelog, tests and CI, documentation, CONTRIBUTING, support/governance | history, tests, CI yes; no release, no changelog; no CONTRIBUTING | small + scope | **Fixed:** `CONTRIBUTING.md` (issues, support, governance). Release, CHANGELOG and CITATION.cff: session 2.15 (scope) |
| 8 | Feature-complete, packaged to community standards, designed for extension, automated tests | `pyproject.toml`, installs with pip; 200 tests pass (29 Oct, local); much code is single-project (hurricane loop, NHC, remedy backtest) | medium | Packaging fine; "designed for extension" is credible only for the DAC standard. Reframe or split (see review) |
| 9 | Installation documented with dependencies | README "Run it locally"; Python version stated 3.11+ in README, >=3.10 in pyproject, CI tests 3.11 | small | **Fixed:** `requires-python = ">=3.11"` (what CI tests) |
| 10 | Example usage, ideally real-world | README had none | small | **Fixed:** DAC validate/profile example in README, run verbatim on 29 Oct (output `SYNTHETIC-EXAMPLE ['dedicated_funding'] ['counter_measure']`). A real-data example (ozone case) would be stronger |
| 11 | Core functionality documented (API) | docstrings; protocols in `docs/`; no API reference | medium | Not attempted (scope: one task; listed for 2.15 or later) |
| 12 | Paper: 750–1,750 words; Summary, Statement of need, State of the field, Software design, Research impact statement, AI usage disclosure, Acknowledgements, References; `paper.bib` | none before | — | **Drafted:** `paper/paper.md`, 1,064 words, all sections |
| 13 | State of the field compares with other *software* and justifies build vs contribute | `docs/RELATED_WORK.md` covers datasets and studies only; no software search | **large** | A search for comparable software (policy-response coding tools, event-coding formats) is needed. Not attempted (scope) |
| 14 | AI disclosure: tools and versions, where used, nature and scope, human review/validation and human design decisions | three-point form has no tool/version; point 2 withheld (2.13); white paper records that every decide-act file was coded by one AI model and no human has checked one | **large** | Draft adds tool and version (Claude Opus 5.5; 320 commits with its co-author line) and keeps point 2 withheld. Adrian must (a) state which tools, if any, he used for the Nov 2025–Apr 2026 commits, (b) do and record the verification before point 2 can be written. JOSS treats an inaccurate disclosure as an ethical breach |
| 15 | No AI for conversation with editors or reviewers (translation only) | Adrian works with AI as his writing partner | **large** (practice) | Adrian's decision: replies in the review thread must be written by him |
| 16 | Disclose related publications | DAC manuscript ("Decision or Supply?") not submitted; white paper draft | small | To be listed in the submission form at the time |
| 17 | Fees | none | none | — |
| 18 | After acceptance: tagged release + archive DOI | no release; Zenodo–GitHub integration not checked this session | scope | Session 2.15 |

## Other points a reviewer will notice (not JOSS rules)

- Root of the repo still holds superseded funder white papers, a deck, grant drafts and `BRAND & TRADEMARKS.md`; they carry "superseded" banners but crowd the top level. Adrian's decision whether to move them to `docs/archive/`.
- `LICENSE-COMMERCIAL` with AGPL: allowed, but outside contributions cannot be relicensed commercially without an agreement (`CONTRIBUTING.md` says this is undecided). Adrian's decision.
