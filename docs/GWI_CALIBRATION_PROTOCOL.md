# GWI calibration protocol (2026-10-23, UIA follow-up)

Status: pre-registered. Written and committed before any data listed in §3 as "not yet opened"
was fetched. Result goes in §7 only; §1–6 are not edited after the commit.

Why: `docs/UIA_PROTOCOL.md` §5. GWI passed its event test (`docs/GWI_PROTOCOL.md` §7), but
`compute_gwi`'s binomial threshold assumes independent language streams; it expected 0.012 false
ignitions and found 95 (test) and 15 (placebo). GWI may score the He letter I only if a calibrated
threshold holds its stated false-ignition rate on data it was not tuned on.

## 1. Question

Does a threshold calibrated on the coincidence counts of one placebo article keep its target
false-ignition rate on other placebo articles and on later dates, while keeping the session-6
discrimination of hurricane landfalls?

## 2. Calibrated rule (fixed now)

Pre-processing as `docs/GWI_PROTOCOL.md` §4: y_t = log(1 + views_t); r_t = y_t − median of y over
t−56 … t−1; missing days = 0; a stream with more than 5 % zero days in its analysis period is
excluded.

Excursion: z_t = (r_t − m) / s per stream, with m = median and s = 1.4826 × MAD of that stream's r
over the **training period 2016-01-01 … 2025-12-31** (the same m, s are used for every later day).
A stream is in excursion when z_t > 2.0 (unchanged). Coincidence fraction g_t = (streams in
excursion) / (streams used).

Null: the empirical distribution of g_t of the **reference placebo** "Photosynthesis" (12 editions)
over the training period. This keeps whatever co-movement Wikipedia streams share on ordinary days,
which the binomial null ignores.

Target false-ignition rate per day: **q = 0.005** (about 1.8 days a year).

Calibrated threshold: f_cal = the smallest value of k / n (k = 1 … n, n = reference streams used)
such that the share of training days with g_t ≥ f_cal is ≤ q. An ignition day is g_t ≥ f_cal.
f_cal is computed once and then applied unchanged to every set and period below.

## 3. Data

Wikimedia per-article daily pageviews, `all-access`, agent `user`, editions en, es, fr, de, it, pt,
nl, pl, ru, ja, zh, ko; titles via English interlanguage links (as `docs/GWI_PROTOCOL.md` §3).

- Already opened (session 6): "Tropical cyclone" and "Photosynthesis", 2015-11-01 … 2025-12-31.
- **Not yet opened**, fetched by the weekly Action after this commit:
  - "Photosynthesis", 2025-11-01 … 2026-10-18 (time held out);
  - held-out placebo articles, 2015-11-01 … 2026-10-18: **"Mitochondrion"**, **"Pythagorean theorem"**,
    **"Prime number"** (chosen now as stable topics without news peaks).

End date fixed at 2026-10-18 (last full week). Stored in a new file; the session-6 file is untouched.

If a held-out article lacks an interlanguage link in some edition, that edition is dropped for that
article. An article with fewer than 8 usable streams is dropped. Fewer than 2 held-out articles left
→ **NOT TESTABLE**.

## 4. Periods

- Training: 2016-01-01 … 2025-12-31 (reference only).
- Held out in articles: each held-out article, 2016-01-01 … 2026-10-18.
- Held out in time: "Photosynthesis", 2026-01-01 … 2026-10-18.

## 5. Statistic and pass/fail

Rate = ignition days / analysis days, per article and period.

**PASS** only if all three hold:
1. **Other articles:** each held-out article has rate ≤ 2q = 0.010.
2. **Later dates:** "Photosynthesis" 2026-01-01 … 2026-10-18 has rate ≤ 2q (with 291 days: at most 2
   ignition days).
3. **Discrimination kept** (on session-6 data, already seen; the threshold uses no event information):
   rerunning `docs/GWI_PROTOCOL.md` §5–6 with the calibrated rule on "Tropical cyclone" gives H ≥ 0.5
   and Fisher p < 0.05 against the Jun–Nov control windows.

**FAIL** otherwise. Condition 1 or 2 failing means the calibration does not transfer; condition 3
failing means a calibrated GWI no longer detects landfalls. On FAIL, GWI does not score I
(`docs/UIA_PROTOCOL.md` §5).

Reported without weight: f_cal and the k it corresponds to; training rate; per-article rates for
2026 alone; the session-6 placebo test rerun with the calibrated rule; the binomial k_min for comparison.

## 6. Known limits, stated in advance

One reference article; three held-out articles; academic-calendar seasons may raise placebo rates in
some editions. 2026 hurricane events cannot be tested (HURDAT2 for 2026 is not yet published), so
discrimination is checked only on seen events. A PASS calibrates the false-ignition rate on ordinary
topics; it does not show that GWI measures "information integration" in the He sense.

## 7. Results

Single run: Action run 39933057718 (2026-10-23), code at 803d614, results committed by the Action in
7fec9bd (`results/weekly/2026-10-23/gwi_calibration.txt`; data in
`data/sources/wikipedia_pageviews_gwi_calibration/`). 100 tests pass.

| | Streams | Ignition days / days | Rate | ≤ 2q = 0.010 |
|---|---|---|---|---|
| Reference "Photosynthesis", training 2016–2025 | 12 | 15 / 3,653 | 0.0041 | (target q = 0.005) |
| Reference, 2026 (time held out) | 12 | 1 / 291 | 0.0034 | yes |
| "Prime number", 2016-01-01 … 2026-10-18 | 12 | 53 / 3,944 | **0.0134** | **no** |
| "Pythagorean theorem", same period | 12 | 9 / 3,944 | 0.0023 | yes |
| "Mitochondrion" | 1 | dropped (< 8 streams) | — | — |

f_cal = 0.5 (k = 6 of 12). The binomial k_min on the reference was also 6, so calibration did not change the
threshold for this article; for "Tropical cyclone" it lowers k from 7 to 6.

Discrimination with the calibrated rule (session-6 events, seen data): 118 ignition days; events hit
14/21 = 0.667; Jun–Nov controls 12/275 = 0.044; Fisher p = 2.5e-12. Kept.
[no weight] Placebo rerun: 15 ignition days; events 2/21; controls 4/275; p = 0.061.
[no weight] 2026 only: "Prime number" 1/291, "Pythagorean theorem" 0/291.

**RESULT: FAIL** — condition 1 fails ("Prime number" 0.0134 > 0.010). Conditions 2 and 3 hold.

Read with these limits:
- The failure is in articles, not in time: the threshold held on 2026 for the reference and both
  held-out articles, but one ordinary topic ignites 2.7 times the target over 2016–2026. A threshold
  tuned on one article does not transfer to every other article.
- "Mitochondrion" contributed only one stream: its interlanguage links were not returned (cause not
  checked; possibly a redirect). Two held-out articles remained, so the test was testable by §3.
- Consequence (§5): GWI does not score the He letter I. The session-6 event result stands; it is a
  contrast with control windows and never relied on the threshold's nominal rate.

## 8. Exploratory diagnostics after the result (no weight; verdict in §7 unchanged)

Run 2026-10-23 in the session on the committed data; not pre-registered.

**"Mitochondrion" (one stream).** Only the English stream was written: the English interlanguage-link
query returned no links. English views of the title fall about 85 % between 10 and 12 July 2026
(monthly median ~900/day in June, ~150–170/day from July to October). That pattern fits the title
becoming a redirect after a page move, and the query (no `redirects=1`) returns no links for a
redirect. **Not verified:** the English article fetched in this session still showed the title
"Mitochondrion" (that fetch may be cached). Cause therefore open. Pre-2026 data are unaffected.
Verification attempt (same day): the page info, the interlanguage-link API and the pageviews API are
not reachable from the session; a fetch of `/wiki/Mitochondria` returned the same article, with
internal links naming it "Mitochondria", no "redirected from" note and no edit date. Evidence is
mixed and the fetch tool summarises pages rather than showing them raw, so the move is still
**not verified**. A decisive check is the English pageviews of "Mitochondria" from July 2026, which
only the Action can fetch.

**Verified** (one-off manual workflow `check_wiki_title.yml`, run 39934649530, English Wikipedia API
move log and page info): the English article "Mitochondrion" was moved to "Mitochondria" on
2026-06-29 14:26 UTC (round-robin swap, per a requested move opened 23 June 2026). "Mitochondrion"
is now an 89-byte redirect. The fetch asks for interlanguage links without following redirects, so it
got none: this is why only the English stream was written. The views of the old title fell gradually
from late June and stepped down on 10–12 July (likely search engines updating; not checked). The
daily-views step of that workflow printed nothing (a quoting error); not needed for the verdict.
A future fetch should follow redirects; it would not change this run.

**"Prime number" (53 ignition days).** Not scattered, not tied to news: 50 of 53 fall in September,
all on Monday–Friday, in 22 short runs, in 8 of the 11 years. This is the start of the academic year,
shared by most of the 12 editions; the 56-day rolling-median baseline lags a seasonal step-up, so it
reads as a coincident excursion. The calibration did not fail at random: it failed on a calendar driver
the protocol named as a known limit (§6). A redesign would need a seasonal baseline (same weeks of
earlier years), pre-registered and tested on articles and dates not yet opened.

**Check on the session-6 GWI pass (exploratory).** Because hurricanes also peak in September: with the
session-6 rule, September control windows were hit 5/34 vs 4/241 for other June–November controls,
so September is a weak spot. Split by month, the event contrast still holds: September events 6/6 vs
controls 5/34 (Fisher one-sided p = 1.2e-4); other months 8/15 vs 4/241 (p = 7.0e-9). The session-6
PASS is not explained by the calendar effect, but its September contrast is weaker than the pooled one.
