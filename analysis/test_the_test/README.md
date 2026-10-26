# Test the test: Science of Truth trial design (origin of the method)

**Origin.** Adrian supplied `science_of_truth_test_design_original.txt` in a claude.ai chat on
26 Oct 2026 (20:13 Brussels). In that chat Claude ran its simulation, a robustness sweep, a
combined-departure sample-size run and a false-positive check, and revised the protocol.
Everything from that chat is committed here (CLAUDE.md rule 4: the repo is the only memory).

**Why it is in the EMO repo.** Adrian: "It's all about EMO." The transferable part is the method:
before trusting a measure or a test, simulate a world where nothing happens (does it raise false
alarms?) and a world with a known effect (does it detect it?), under realistic distortions.
`docs/HE_CALIBRATION_PROTOCOL.md` applies it to the planned He direction test.

**Evidence class:** exploratory, synthetic data only. No EMO data. These results describe
statistical procedures under assumed parameters, not any real curriculum or classroom.

| File | What | Seed | sha256 (first 12) |
|---|---|---|---|
| `science_of_truth_test_design_original.txt` | Adrian's draft protocol, as supplied | — | 6767400ed187 |
| `simulate_trial.py` | Section 7 script, unchanged | 20261026 | see git |
| `sweep_trial.py` | 22 single departures × 4 analyses, 2,000 trials/cell; `teacher_level` option added later (does not change sweep output: rerun 26 Oct gave an identical CSV) | 20261026 | 531025854f1d |
| `sweep_results.csv` | output of `sweep_trial.py` | — | 396dd613a3d5 |
| `combined_trial.py` | 3 planning profiles × 80–320 classrooms, 1,000 trials/cell | 20261027 | 3912a345e6cb |
| `combined_results.csv` | output of `combined_trial.py` | — | c8f73dc58981 |
| `fpr_check.py`, `fpr_check.log` | 10,000-trial false-positive check of the optimistic profile | 20261028 | 3899e06cb982 |
| `the_science_of_truth_test_design.txt` | revised protocol (name under title, Sections 4, 5, 6, 7, 8, 9, 12 revised) | — | b81eaeb4cfa7 |

Results reproduced in the chat: Section 7 script gives 4.53% / 80.50% / 98.73% exactly; the sweep
CSV reproduces byte for byte.

**Main findings (synthetic):** the cluster-means test holds 5% under most departures; 80
classrooms is underpowered except under optimistic assumptions; differential attrition creates
bias (+0.13 to +0.20 SD) that more classrooms cannot remove; student-level analysis that ignores
clustering gives 17–40% false positives.

**Sources opened in that chat (26 Oct 2026):**
- Hedges & Hedberg, IPR working paper WP-06-12, https://www.ipr.northwestern.edu/documents/working-papers/2006/IPR-WP-06-12.pdf
- Abrami et al. 2015 summary, https://www.clearinghouse.edu.tum.de/wp-content/uploads/2023/12/CHU_KR18_ENG_Abrami_2015.pdf
- Kraft 2023 abstract, https://www.matthewakraft.com/the-effect-size-benchmark-that-matters-most-education-interventions-often-fail
- Kraft 2020 abstract page, https://annenberg.brown.edu/publications/interpreting-effect-sizes-education-interventions
- Cheung & Slavin 2016 summary, https://bestevidence.org/2021/02/07/methods-methodological-features-and-effect-sizes/

**Editor-style verdict given in the chat:** not submittable; the curriculum and outcome measure
are unspecified; the methods are standard. Right home for now: this repo (or OSF/Zenodo).

Run: `python analysis/test_the_test/sweep_trial.py` etc. (numpy, scipy). Scripts write their
CSV into the current directory.
