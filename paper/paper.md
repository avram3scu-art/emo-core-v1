---
title: 'EMO-Core: open, pre-registered measurement of how societies respond to warnings'
tags:
  - Python
  - disaster response
  - early warning
  - policy lags
  - pre-registration
  - research software
authors:
  - name: Adrian N. Avramescu
    orcid: 0009-0005-1393-5264
    affiliation: 1
affiliations:
  - name: Independent researcher, Antwerp, Belgium
    index: 1
date: 29 October 2026
bibliography: paper.bib
---

<!-- DRAFT, session 2.14 (29 Oct 2026). Not submitted. See docs/JOSS_CHECKLIST.md and docs/REVIEW_2_14_JOSS.md before any use. -->

Adrian N. Avramescu

# Summary

EMO-Core is a Python package and a set of scripts for measuring, from public records, how quickly a society turns a warning into a decision and the decision into delivered action. Its central component is the DAC event-file standard: a JSON format, a schema and a validator for dated events (a warning, a firm order, a binding act, physical delivery) in one case, together with a function that returns the case's lag profile. The package also contains time-series metrics used in the project's tests (forecast-skill trend from published forecast errors, an attention-ignition statistic on public pageview series, a forecast-advantage test against a "no change" forecast), an event table builder for Atlantic hurricane landfalls linked to US federal disaster declarations, and a backtest harness for candidate remedy rules. Every test the project runs is pre-registered in the repository before its data are opened, and every reported result carries one evidence class.

# Statement of need

Researchers who evaluate disaster response and early-warning systems often need the interval from a warning to a decision and from a decision to delivery, and they need those intervals to be reproducible from the primary records. In practice such lags are assembled by hand for one study, with undocumented choices about which document counts as the warning and how to treat dates known only to the month or year.

EMO-Core makes those choices explicit and machine-checkable. `emo.dac_standard.validate_event_file` rejects a malformed file and lists every error found. `emo.dac_standard.compute_profile` returns per-sublayer lags from the warning date, paired and unpaired order-to-delivery intervals, and missing and censored sublayers listed separately. A date that the records allow to be read in more than one way is kept as a contested date, and one profile is computed for each combination of readings, instead of choosing one silently. No weighted or composite score is computed: a case is reported as a profile of its components.

The target users are researchers coding policy-response cases who want a shared, testable format for those cases, and reviewers who want to rerun a published lag from the coded file.

# State of the field

Existing work already measures much of what a response observatory might claim to add. The Oxford COVID-19 Government Response Tracker records the daily timing and stringency of government policies across more than 180 countries, with every data point checked by a second coder, and states that it does not measure implementation, compliance or effects [@hale2021]. Quantitative research on international environmental regimes, including the ozone regime that EMO-Core uses as its calibration case, compares regime effectiveness across larger samples than EMO-Core has coded [@breitmeier2011]. Perception-based governance indicators report their dimensions separately with uncertainty, a practice EMO-Core follows [@wgi2025].

What EMO-Core adds is narrow: the delivery leg (an order or act followed to a physical outcome series), a standard file format for it, and open code that recomputes the lags. The difference from the regime-effectiveness literature is one of form (dated lags, open code, scheduled re-runs), not of question. The project's comparison of related work (`docs/RELATED_WORK.md`) covers datasets and studies; it did not search for software packages with a similar purpose, so no build-versus-contribute comparison with existing software can yet be given.

# Software design

The package (`emo/`) separates three kinds of code. (1) The DAC standard (`emo/dac_standard.py`, schema `docs/dac_event_file.schema.json`, specification `docs/DAC_STANDARD.md`) depends only on the Python standard library, so that a coded case can be checked without the rest of the package. (2) Metric functions (`emo/info_time.py`, `emo/gwi.py`, `emo/gwi_v2.py`, `emo/smf.py`, `emo/synergy.py`) take plain arrays or data frames and return statistics with their significance tests. (3) Domain code (`emo/loop_hurricanes.py`, `emo/smf_nhc.py`, `emo/remedy/`) builds event tables from named public sources and runs the project's registered tests.

Three design choices trade convenience for checkability. First, results are profiles, never weighted sums, so a user cannot read a single "response score" from the package. Second, the analysis scripts in `analysis/` are kept only if a registered test or the weekly run uses them; unused modules were removed. Third, the repository itself is part of the method: a protocol (hypothesis, data, statistic, threshold, and the false-positive rate and power from synthetic data) is committed before the data are opened, a pre-push hook runs a claim-word check, `ruff` and the tests, and a scheduled GitHub Action refreshes the public data series, reruns the analyses and tests, and commits only if the tests pass. Exact dependency versions are pinned in `requirements-lock.txt`, which CI and the weekly run install. The test suite has 200 tests.

# Research impact statement

The software has been used only by its author so far. It has produced the results listed with their evidence classes in the repository README, most of which are failures or exploratory: for Atlantic hurricane landfalls 2015–2025 (52 storms), the test that response lags are measurable for most events failed, and the tests of coupling and learning could not be decided at this sample size (pre-registered on known history). Two remedy-rule versions failed on reserved historical cases. Dated forecasts for 2027 and a 2027 hurricane-season test are registered and will be scored blind after their outcomes occur. The DAC event files have been coded by one coder; an independent second coding has been prepared but not yet returned. No outside user is recorded in the repository, and no citation search has been made.

# AI usage disclosure

Generative AI was used in this project. Tool: Claude Opus 5.5 (Anthropic), used through Claude Code from 19 October 2026 for code, tests, documentation, coding of DAC event files, analysis scripts and the drafting of this paper; 320 commits carry its co-author line. [Tools used for the commits of November 2025 to April 2026: to be stated by the author.]

1. All inputs were the author's own manuscript text, code and publicly available reference literature and data (plus synthetic simulation parameters where applicable).
2. [Withheld until the author's verification is recorded in `docs/STATUS.md`.]
3. All scientific claims and interpretations are the author's own.

Contributions: Adrian N. Avramescu (concept, decisions, verification). Claude (Anthropic) contributed code, data coding, analysis and drafting under the author's direction.

# Acknowledgements

[To be confirmed by the author: no financial support was received.]

# References
