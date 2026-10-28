# GWI protocol (session 6, 2026-10-23)

Status: pre-registered, then run once; result in §7. Protocol committed in ae3b507 and the event
list in 08b99ab, both before any pageview data was fetched (fetch added in 31e7fa5). Section 7 is
never edited afterwards except to add later weekly re-runs that differ.

## 1. Question

Does Global Workspace Ignition (`emo/gwi.py`, `compute_gwi`) detect coincident attention across
independent language communities at dated hazards with official warnings, more often than in
control windows, and not for an unrelated topic?

Hypothesis H1: event windows contain at least one GWI ignition more often than control windows.

## 2. Events (chosen before any attention data)

Hazard class: Atlantic hurricanes making landfall at major-hurricane intensity. The U.S. National
Hurricane Center (NHC) is the official warning centre for this basin.

Source: NHC HURDAT2 Atlantic best-track file `hurdat2-1851-2025-092326.txt`, listed (last
modified 2026-09-30) at https://www.nhc.noaa.gov/data/hurdat/ (directory listing opened this
session). The file itself is fetched by the weekly Action into `data/sources/hurdat2_atlantic/`.

Rule, applied to the file, nothing chosen by hand:
- every storm with a landfall record (record identifier `L`) dated 2016-01-01 to 2025-12-31 with
  maximum sustained wind ≥ 96 kt (Saffir–Simpson category 3 or higher);
- one event per storm: the UTC date of its first such record;
- if two event windows (§5) overlap, they are merged into one event dated by the earlier storm.

Not verified here: the date of the official NHC warning for each event. HURDAT2 records the
hazard, not the warning; NHC issues watches and warnings for landfalling hurricanes in its area,
but per-event warning times are not used in this test.

The event list is produced by `analysis/gwi_hurricanes.py` in a first Action run that fetches
HURDAT2 only, and copied into §2.1 and committed before the pageview fetch is added.

### 2.1 Event list

Derived by `analysis/gwi_hurricanes.py` in Action run 39930507770 (2026-10-23, from commit ff9bb04;
HURDAT2 fetched by that run). No pageviews had been fetched. n = 21, no merges:

| Date (UTC) | Storm | | Date (UTC) | Storm |
|---|---|---|---|---|
| 2016-10-04 | Matthew (AL142016) | | 2021-08-21 | Grace (AL072021) |
| 2016-11-24 | Otto (AL162016) | | 2021-08-29 | Ida (AL092021) |
| 2017-08-26 | Harvey (AL092017) | | 2022-09-20 | Fiona (AL072022) |
| 2017-09-06 | Irma (AL112017) | | 2022-09-27 | Ian (AL092022) |
| 2017-09-19 | Maria (AL152017) | | 2023-08-30 | Idalia (AL102023) |
| 2018-10-10 | Michael (AL142018) | | 2024-07-01 | Beryl (AL022024) |
| 2019-09-01 | Dorian (AL052019) | | 2024-09-27 | Helene (AL092024) |
| 2020-08-27 | Laura (AL132020) | | 2024-10-10 | Milton (AL142024) |
| 2020-10-28 | Zeta (AL282020) | | 2024-11-06 | Rafael (AL182024) |
| 2020-11-03 | Eta (AL292020) | | 2025-10-28 | Melissa (AL132025) |
| 2020-11-17 | Iota (AL312020) | | | |

That run did not commit (three unrelated refresh tests assumed only OWID/OpenAlex sources; fixed
in the commit that adds this list).

Testability condition: fewer than 8 events → the test is recorded as **not testable** (no pass, no fail).

## 3. Attention series

Wikimedia per-article pageviews, daily, `all-access`, agent `user`, fetched by the weekly Action
(`scripts/refresh_open_data.py`) into `data/sources/wikipedia_pageviews_gwi/`. Data range
2015-11-01 to 2025-12-31 (fixed end, so weekly re-runs are reproducible). Coverage of the
pageviews API begins July 2015 (pageviews.wmcloud.org Langviews FAQ, opened this session); the
mid-2000s figure in `docs/UIA_PROTOCOL.md` was wrong.

Streams: one article per language edition, 12 editions: en, es, fr, de, it, pt, nl, pl, ru, ja,
zh, ko.
- Test set: English article "Tropical cyclone" and its interlanguage links to the 11 other editions.
- Placebo set: English article "Photosynthesis" and its interlanguage links (same editions).

Titles are resolved by the Action from the English Wikipedia langlinks API (metadata only, no
pageviews) and recorded with the data. Wikidata could not be reached from this session.

Missing days (the API omits days with zero views) are set to 0. A stream is excluded if more than
5 % of analysis days have 0 views. If fewer than 8 streams remain in either set → not testable.

## 4. Ignition rule

`emo/gwi.py`, `compute_gwi(streams, z_threshold=2.0, alpha=0.05)`, unchanged
(definition `coincident_excursions_binomial_v1.1`): robust z per stream; an ignition day needs k
streams in excursion together with P(Binomial(n, p) ≥ k) < alpha / T.

Pre-processing, fixed here: for each stream, y_t = log(1 + views_t); input r_t = y_t − median of
y over the 56 preceding days (t−56 … t−1). This removes slow trends (Wikipedia's long decline,
the 2020 change in bot classification) which otherwise make all streams "co-excursive" in the
early years. Analysis days: 2016-01-01 to 2025-12-31 (T ≈ 3,653).

## 5. Windows

- Event window: event date d, days d−2 … d+2 (5 days).
- Control windows: the analysis period cut into consecutive 5-day blocks from 2016-01-01; a block
  is a control if all its days fall in June–November (season match) and none is within 10 days of
  any event date.
- A window is "hit" if it contains at least one GWI ignition day.

## 6. Statistic and pass/fail

H = hit share of event windows; F = hit share of control windows; one-sided Fisher exact test
(event windows hit more often than controls). Same for the placebo set: H_p, F_p, p_placebo.

**PASS** only if all three hold:
1. H ≥ 0.5;
2. Fisher p < 0.05 (test set);
3. placebo not enriched: p_placebo ≥ 0.05.

**FAIL** otherwise (including no ignitions at all). Condition 3 failing means the ignitions track
something Wikipedia-wide, not the hazard.

**Note added 28 Oct 2026 (fix session F6; audit 2026-10-26b S4; no change to the recorded verdict).** Condition 3 treated a non-significant placebo result (p_placebo = 0.061, §7) as evidence that the placebo is not enriched. That inference is invalid: failing to reject is not evidence of no effect, and with 21 events the placebo test had little power to detect enrichment. The Fisher tests also treat windows as independent although ignitions cluster in time (audit 2026-10-26, #5), so all three p-values are optimistic. The PASS therefore rests on condition 2 (p = 2.3e-13, large enough that clustering does not change it), not on condition 3. **Any future GWI test will:** (a) test the difference directly: the test set must be enriched significantly more than the placebo set (one-sided test of H_test − H_placebo against a block-permutation null), instead of asking the placebo test to be non-significant; (b) if a "no placebo effect" claim is wanted, state an equivalence bound in advance (e.g. placebo hit share within 0.05 of its control rate) and test it; (c) compute p-values from a null that keeps the clustering in time (block permutation of windows), not from Fisher's independence assumption; (d) treat the H ≥ 0.5 threshold as a descriptive floor, with the decision carried by (a). **Not testable** only under the conditions in §2.1 and §3.

Reported without weight in the verdict: H and F for all-year controls; the number of ignition
days; k_min and the expected number of false ignitions from `compute_gwi`.

Known limits, stated in advance: concept articles respond less than storm articles (which cannot be
pre-registered, as they are created after each storm), so a FAIL may reflect the proxy; streams are
not independent (shared news cycle), which `compute_gwi` does not model; one hazard class only.

## 7. Results

Single run: Action run 39930743235 (2026-10-23), code at 31e7fa5, results committed by the
Action in 5e343fc (`results/weekly/2026-10-23/gwi_hurricanes.txt`; pageviews in
`data/sources/wikipedia_pageviews_gwi/`, sha256 cb40fda4dcb17842…). All 12 streams kept in both sets.

| | Test ("Tropical cyclone") | Placebo ("Photosynthesis") |
|---|---|---|
| Ignition days (of 3,653) | 95 | 15 |
| k_min (of 12 streams) | 7 | 6 |
| Event windows hit, H | 14/21 = 0.667 | 2/21 = 0.095 |
| Control windows hit, Jun–Nov, F | 9/275 = 0.033 | 4/275 = 0.015 |
| Fisher one-sided p | 2.3e-13 | 0.061 |
| [no weight] all-year controls hit | 10/644 = 0.016 | 4/644 = 0.006 |

Events not hit (7): Otto 2016, Michael 2018, Zeta 2020, Eta 2020, Iota 2020, Grace 2021, Rafael 2024.
Placebo hits: Maria 2017, Helene 2024.

**RESULT: PASS** (H ≥ 0.5; p < 0.05; placebo p ≥ 0.05).

Read with these limits:
- The placebo margin is thin (p = 0.061 against the 0.05 line). Two placebo hits inside event
  windows suggest some Wikipedia-wide co-movement; the pass is by the pre-registered rule, not by a wide margin.
- `compute_gwi` expected 0.012 false ignitions under independence but found 95 (test) and 15
  (placebo): the language streams are not independent. Its binomial threshold is therefore not a
  calibrated false-alarm rate on real data; only the comparison with control windows carries the result.
- Misses concentrate on Central American landfalls (Otto, Eta, Iota, Rafael, Grace) and late
  seasons; hits concentrate on U.S. and large Caribbean landfalls. GWI here measures where
  multilingual Wikipedia attention goes, which is not uniform across affected populations.
- One hazard class, one concept article; not a test of GWI as a general measure of "global
  workspace". Weekly re-runs will reproduce this (fixed data range) and are listed below if they differ.
