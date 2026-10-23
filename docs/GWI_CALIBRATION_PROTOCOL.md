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

(Empty until the single run.)
