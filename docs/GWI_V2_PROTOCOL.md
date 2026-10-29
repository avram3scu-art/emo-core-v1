# GWI v2 protocol: prospective calibration and event tests (session 2.6, 2026-10-29)

**Status: pre-registered (evidence class on scoring: pre-registered blind).** Committed before any scored pageview or event exists: every scored day is 2026-11-01 or later; every event occurs 2026-11-01 or later. Power from synthetic data (§7): calibration 0.91 at the target rate; event test 0.70–0.96 at a 30 % event hit rate and ≥ 0.94 at 50 %, with 8–20 events; false-positive rate ≤ 0.017. **Scoring date: Monday 15 November 2027** (§8). §1–§9 are not edited after this commit; the result goes in §11 only. Hypothesis moved: **H2** (`docs/PLAN.md` §4): it fails if GWI v2 fails this calibration test or this event test.

## 1. Question

Does attention ignite across language communities on hazard events beyond calendar and seasonal drivers, with a threshold that transfers to articles and dates it was not set on?

## 2. What is repaired (audit `docs/AUDIT_2026-10-29.md` D2–D4; failures F4, F5)

GWI v1.1 (`emo/gwi.py`) and its results (`docs/GWI_PROTOCOL.md`, `docs/GWI_CALIBRATION_PROTOCOL.md`) stay unchanged on record. GWI v2 is `emo/gwi_v2.py`:

| Defect | v1.1 | v2 |
|---|---|---|
| D2 look-ahead | median/MAD from the whole sample (or a frozen training period) | every quantity for day t uses days before t only (tested: `tests/unit/test_gwi_v2.py::test_causal_no_lookahead`) |
| D4 calendar | 56-day rolling median; lagged behind the September step-up of "Prime number" | per-stream baseline: same-weekday level of the last 8 weeks + that baseline's seasonal miss at the same time in earlier years |
| D3 pooled rate | one pooled excursion rate, binomial | per-stream causal rates, Poisson-binomial tail |
| D4 serial correlation, F5 | Fisher tests; non-significant placebo used as evidence | event test on a joint block-permutation null, including the test-minus-placebo difference; no "no placebo effect" claim is made |
| new | — | common-mode filter: ignitions shared with ≥ 15 % of a placebo panel are discarded (§3.4, §4) |

## 3. Method (fixed)

### 3.1 Data

Wikimedia per-article daily pageviews, `all-access`, agent `user`; editions en, es, fr, de, it, pt, nl, pl, ru, ja, zh, ko; titles from the English article's interlanguage links **with redirects followed** (`scripts/refresh_open_data.py::_pageviews_csv`, `follow_redirects=True`; the 6c page move, `docs/GWI_CALIBRATION_PROTOCOL.md` §8). Fetched 2022-07-01 … 2027-11-02 by `scripts/fetch_gwi_v2.py`, which refuses to run before 2027-11-15. Days before 2026-11-01 are used only as baseline history, never scored. Missing days = 0; a stream with more than 5 % zero days over the fetched period is excluded; an article with fewer than 8 streams is dropped.

### 3.2 Articles

- Test: English "Earthquake" and its interlanguage links.
- Placebo panel (20, chosen now, before any data): Photosynthesis, Prime number, Pythagorean theorem, Mitochondrion (redirects to "Mitochondria" since 29 Jun 2026), Periodic table, Atom, Cell (biology), Fraction, Triangle, Water cycle, Leaf, Bird, Tree, River, Chess, Piano, Bread, Algebra, Circle, Fern. Photosynthesis, Prime number, Pythagorean theorem and Mitochondrion were used in development (§4) on days up to 2026-10-18; their days from 2026-11-01 are unseen. No day is removed by hand.

### 3.3 Ignition rule (per article)

y = log(1 + views). For stream i and day t:
- L_t = median of y over t−7k, k = 1…8 (all 8 required);
- S_t = median over earlier years j = 1…3 (at least 2) of the median of (y − L) over days t−364j−3 … t−364j+3;
- r_t = y_t − L_t − S_t; z_t = (r_t − m_t)/s_t, with m_t and s_t = median and 1.4826 × MAD of r over t−365 … t−1 (at least 180 days);
- excursion: z_t > 2.0; causal rate p_i,t = (excursions + 0.5)/(scored days + 1) over t−365 … t−1 (at least 180 days).
- K_t = streams in excursion; P_t = P(PoissonBinomial(p_·,t) ≥ K_t). A day is scored if at least 8 streams have z and a rate. **Ignition: P_t < α_day = 3 × 10⁻⁴** (fixed in §4).

### 3.4 Common-mode filter

An ignition of article a on day t is discarded when at least 15 % of the other panel articles (placebo panel without a; scored that day) ignite within t−1 … t+1. For the test article the panel is all 20 placebos. Reason: global shocks move every topic (§4); they are not attention to a specific hazard.

## 4. Development on seen data (exploratory; no weight)

`analysis/gwi_v2_development.py`, output `analysis/gwi_v2_development_output.txt`; data already opened in sessions 6 and 6c (Photosynthesis, Prime number, Pythagorean theorem; scored days 2018-01-01 … 2026-10-18). Rule fixed before the first run (commit 4a1c3b7): α_day = the largest value in {10⁻², 3·10⁻³, …, 10⁻⁵} with false-ignition rate ≤ q = 0.005 on every development article.

- **Rule 1 (no filter): no value qualified.** At 10⁻⁵ Photosynthesis still had 0.0059. The September step was absorbed (Prime number September ignitions 1–4 at every α, against 50 of 53 in v1.1), but excess ignitions were shared across all three articles: March–April 2020 (school closures) and late December.
- **Rule 2 (after that diagnosis): same rule with the common-mode filter (leave-one-out over the other two articles): α_day = 3 × 10⁻⁴** (Photosynthesis 13/2864 = 0.0045, Prime number 1/2864, Pythagorean theorem 2/2864).
- No weight: the session-6 hurricane events with v2 (unfiltered, "Tropical cyclone"): 10 of 16 event windows ignite against 5 of 410 June–November control windows.

With only two other articles, the development filter fires on any shared ignition; with 19 it needs 3. Whether the filter transfers is part of what §5 tests.

## 5. Calibration test (threshold transfer)

Window W = 2026-11-01 … 2027-10-31 (365 days; includes a September and a December). For each placebo article a, the filtered ignition series on its scored days in W.

- Pooled false-ignition rate R = filtered ignition days / scored article-days. Upper bound U = 97.5 % one-sided block-bootstrap bound (blocks of 14 consecutive days within an article, 4000 resamples, seed 0).
- Per article: one-sided exact binomial p of its count against rate 2q; Holm over articles at 0.05.

**PASS** only if U ≤ 2q = 0.010 and no article is Holm-significant above 2q. **FAIL** otherwise. **NOT TESTABLE** if fewer than 15 placebo articles have ≥ 8 streams. The PASS claim rests on the bound U (an equivalence-type condition); the per-article check can only turn a PASS into a FAIL.

## 6. Event test

Events: every earthquake in the USGS ComCat catalogue with magnitude ≥ 7.0 and origin time 2026-11-01T00:00 … 2027-10-31T23:59 UTC, as returned on the scoring date by `scripts/fetch_gwi_v2.py` (query in that file). Event day = UTC date; an event within 3 days of the previous kept event is merged into it. Window: event day … +2 days. Expected count: about 18 a year before merging (USGS, §10). **NOT TESTABLE** if fewer than 8 events.

Statistics on filtered ignitions:
- H = share of event windows with a test-article ignition;
- D = H − mean over placebo articles of their share of event windows with an ignition.

Null: the days × articles matrix (test + 20 placebos, W plus 2 days) is cut into 14-day blocks and the blocks are shuffled jointly, event dates fixed (9999 permutations, seed 0); p = (1 + #null ≥ observed)/(1 + 9999). This keeps each series' serial dependence and the cross-article dependence. **PASS** only if both H and D are rejected by Holm at 0.05 (one-sided). **FAIL** otherwise.

**H2 verdict:** supported at this test if §5 and §6 both PASS; fails (PLAN §4) if either FAILS; not testable otherwise.

## 7. Synthetic checks (before any data)

`analysis/gwi_v2_synthetic.py`, output `analysis/gwi_v2_synthetic_output.txt` (seed 20261029).

A. Pipeline, 20 synthetic articles × 12 streams, weekday, annual, September-step and December-dip seasonality, AR noise, article and global shared factors; scored year 365 days: v2 unfiltered rate 0.0084, **filtered 0.0041** (September 0.0050); target q = 0.005. Synthetic only: §4 showed real data have shared shocks the synthetic model lacks.

B. Calibration rule (§5), 20 articles × 365 days, clustered ignitions (mean run 1.5 days), 500 replications. P(PASS): all at 0.5q 0.996; **all at q 0.908**; 1.5q 0.446; **all at 2q 0.048** (false pass ≤ 0.05); one article at 5q and 19 at q 0.560; heterogeneous rates with mean q 0.880. Before this run, a 95 % bound gave false pass 0.083–0.10 at 2q; replaced by the 97.5 % bound (exploration in session, recorded in `docs/RECORD.md`).

C. Event test (§6), test + 20 placebos at base rate q, 300 replications, 999 permutations. P(PASS) by number of events n and event hit probability h1:

| n events | h1 = 0 (false positive) | 0.3 | 0.5 | 0.7 |
|---|---|---|---|---|
| 8 | 0.010 | 0.700 | 0.943 | 1.000 |
| 12 | 0.000 | 0.863 | 0.993 | 1.000 |
| 15 | 0.017 | 0.873 | 0.997 | 1.000 |
| 20 | 0.003 | 0.960 | 0.997 | 1.000 |

False-positive rate ≤ 0.017 at every n (nominal 0.05; conservative because both conditions must reject). Event hit rate is an assumption: v2 on the seen hurricane article hit 10/16 = 0.63 (§4, no weight); a generic "Earthquake" article may respond less.

## 8. Scoring

- **Scoring date (one scoring only): Monday 15 November 2027.** On or after that date, run the manual workflow `.github/workflows/gwi_v2_fetch.yml` (fetch, then `analysis/gwi_v2_prospective.py`; outputs committed to `data/sources/gwi_v2/` and `results/gwi_v2/`). Session 2.12 (December 2027) or any earlier session after that date records the result in §11, README and `docs/RECORD.md`.
- One scoring only: no interim look at W. A fetch before the scoring date is refused by the script; a scored day opened earlier by any route voids the blind label (then: pre-registered on known data).

## 9. Known limits, stated in advance

- One-year wait; one test article; a generic article ("Earthquake"), not event articles.
- The per-article check detects only gross single-article excess (one article at 5q fails 44 % of the time, §7B); the test is mainly of the panel-wide rate. v1.1's failure (one article at 2.7q) would usually not be caught by the per-article check alone.
- The common-mode filter discards hazards that move every topic; for M ≥ 7 earthquakes placebos are not expected to move.
- Synthetic placebos are independent; real articles share shocks (§4).
- USGS magnitudes are taken as returned on the scoring date.
- A PASS shows a transferable threshold and event-specific ignition for one hazard; it is not evidence of "information integration" in the He sense.

## 10. Sources (opened 2026-10-29)

- USGS, "Global earthquake numbers on par for 2015", https://www.usgs.gov/news/global-earthquake-numbers-par-2015 (about 18 M ≥ 7.0 a year since about 1900; 19 in 2015).
- ComCat query form (`/fdsnws/event/1/query`, parameters starttime, endtime, minmagnitude, format=csv): from https://dev.to/ronin13/earthquake-data-has-a-free-json-api-every-quake-on-earth-no-key-required-hch; the official page https://earthquake.usgs.gov/fdsnws/event/1/ could not be fetched here, so `eventtype`, `orderby=time-asc` and the CSV columns `time`, `mag` are **unverified** until the scoring run (it fails loudly if they differ).
- Wikimedia pageviews and langlinks APIs: as `docs/GWI_PROTOCOL.md` §3.

## 11. Results

(empty until the scoring run)
