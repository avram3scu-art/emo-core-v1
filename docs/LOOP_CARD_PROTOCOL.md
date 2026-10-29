# Loop card protocol for the global hazard stream (session 3.3, 29 Oct 2026)

Serves **H3** (decide-act: action follows each event with an event-specific, measurable lag; fails if lags are not measurable from official records for most events; `docs/PLAN.md`). Evidence class of the rules and synthetic checks: **infrastructure**. Evidence class of the §9 test when scored: **pre-registered blind** (its events have not happened when this file is committed).

**Registered before any card is public and before any record of the stream log was opened.** Claude does not hold `EMO_STREAM_KEY` and opened no log record; nothing here was tuned on stream data. No card is published by this session. Code: `emo/stream/cards.py` (every constant is part of this protocol). Tests: `tests/unit/test_loop_cards.py` (synthetic only). Power: `analysis/loop_card_power.py`, output `analysis/loop_card_power_output.txt`.

**Field names are documentation-based** (`docs/STREAM_DATA.md` §2, §9; Monty source pages): they have not been checked against a record. §10 says how they may be corrected and until when.

## 1. Inputs

Decrypted runs of `data/stream/log/` (STREAM_DATA §10), read only inside a GitHub Action that holds the secret. A source-day counts as lost when the manifest has no run that day or the source's `error` is not null; lost days form `source_gaps`.

## 2. Nodes and cards

- **Node:** one source record, deduplicated over daily snapshots by its key: GDACS (`eventtype`, `eventid`), USGS ComCat `id`, CEMS `code`, IFRC GO event `id`, IFRC GO appeal `id`. Each node keeps all its snapshots in fetch order (`_emo_fetched_at`); the latest gives current values, the earliest gives "earliest seen". GDACS episodes exist only as these daily snapshots (no episode endpoint, STREAM_DATA §9).
- **CEMS activations naming any EU27 country never become nodes** (all hazards, all dates until the flood test is scored), so nothing built from nodes can reveal what E1 dropped.
- **Card population:** one card per joined component (§4) that has a GDACS orange/red alert in any snapshot, a PAGER `alert` yellow/orange/red, or a decision record (a CEMS activation, or a GO appeal whose own or event hazard class is natural, §3). GDACS green events with no decision get no card.

## 3. Hazard classes and parsing

- Classes EQ, TS, TC, FL, VO, DR, WF. GDACS `eventtype` gives the class directly; USGS is EQ; CEMS `category`/`subCategory` and GO `dtype` (name) by the matching keyword earliest in this order: tsunami TS, earthquake EQ, cyclone/hurricane/typhoon/tropical TC, flood FL, volcan VO, drought DR, fire WF; anything else (epidemics, conflict, cold waves, landslides) has no class and is not a natural-hazard decision here.
- Times: ISO strings (date-only → precision `day`), USGS ms since epoch; unparseable → none.
- ISO3: from 3-letter strings or dicts with `iso3`/`iso`; country **names are never converted** (no name table is registered; see §10).
- GLIDE compared as (type, year, number); the ISO3 suffix is ignored.

## 4. Join rule (frozen; no linking statistic has been computed before this commit)

Explicit keys come before any fallback; components are the union of all links (a component may hold several GDACS events; the card anchor is the one with the earliest onset).

| Order | Rule | Condition |
|---|---|---|
| K1 | CEMS `gdacsId` = GDACS `eventid` | if the id is shared by several GDACS types, the type must equal the CEMS hazard class; if that does not leave exactly one, no link (logged "tie") |
| K2 | GLIDE equal | GDACS `glide` and GO event `glide`, (type, year, number) equal |
| K3 | GO appeal `event` = GO event `id` | `event` as id or as dict with `id` |
| F1 | USGS ↔ GDACS earthquake | onset times differ ≤ 30 min (GDACS time precision required) and epicentres ≤ 100 km apart; closest in time; equal closest → no link (logged) |
| F2 | Fallback for GO events and CEMS activations **with no K1/K2 link** | ISO3 sets intersect, same hazard class, candidate onset date − GDACS `fromdate` date within the window below |

F2 windows (days, inclusive): EQ 0…+2; TS 0…+2; TC −3…+7; FL −7…+14; VO −7…+14; WF −7…+14; **DR: no fallback** (onsets too vague). Candidate onset: GO `disaster_start_date`, CEMS `eventTime`. **Tie rule:** smallest |Δ days|; then the GDACS event whose interval [`fromdate`, `todate`] contains the candidate onset; if still tied, **no link** (logged "tie"). No tie is broken by an alert level, a funding value or any other rung field. A record with no ISO3 (e.g. CEMS countries given as names) is not fallback-joinable.

## 5. Rungs, their times and windows

Each card has five rungs, each with one status (§6). Times use the earliest qualifying record; each time carries its precision (`time`, `day`, `snapshot` = EMO fetch time, an upper bound; `onset-proxy`).

| Rung | Record | Time | Window (from onset) |
|---|---|---|---|
| W warning | GDACS alert orange/red (not FL: GDACS flood alerts follow impact, STREAM_DATA §2.2); PAGER `alert` yellow/orange/red | GDACS: fetch time of the earliest snapshot showing orange/red; if that is the event's earliest snapshot, it is an EQ and onset is ≤ 1 day earlier, the onset (`onset-proxy`). PAGER: origin time (`onset-proxy`; PAGER release time unverified) | 7 days |
| R recognition | a GO event linked; a GLIDE number on a linked GDACS or GO record; English attention (§7) when pageviews exist | GO `created_at`, else earliest seen; GLIDE: earliest snapshot showing it; attention: earliest day ≥ 1,000 views | 30 days |
| D decision | CEMS activation (non-EU27); GO appeal (DREF or Emergency Appeal) | CEMS `activationTime`; GO `created_at`, else `start_date`; else earliest seen | 60 days |
| B money | a DREF record (`atype` 0), or `amount_funded` > 0 in any snapshot | DREF `start_date`; else the earliest snapshot with funding | 60 days after the earliest decision |
| C coordination | B present and decision records from **both** systems (CEMS and IFRC) | — | until the card closes (180 days) |

Onset: the earliest hazard-record onset (GDACS `fromdate`, USGS `time`); a card with no hazard record is **unanchored** and uses the earliest decision-record onset. Coverage = Σ `amount_funded` / Σ `amount_requested` over linked Emergency Appeals (latest snapshot); undefined without one. The card closes 180 days after onset.

## 6. Statuses: "not yet" versus "missing"

| Status | Meaning |
|---|---|
| present | the record exists |
| **not yet** | no record, and the rung's window is still open: the loop may still reach it |
| absent | no record, the window has closed, and the sources were complete: a real stop of the loop |
| **missing** | no record, the window has closed, and a source that would carry it lost ≥ 7 consecutive days overlapping the window (the rolling 7-day fetch recovers shorter gaps): EMO cannot tell |
| no source | no source can carry this rung for this event (W for floods; attention before pageviews are added; W for unanchored cards) |
| withheld | E1: CEMS for every card with an EU27 country, and C for those cards unless present without CEMS |

"Not yet" is never counted as a stop; "missing" is never counted as absent.

## 7. Stages (STRATEGY_3_0 §3, Adrian's six)

The furthest present rung, in the order W, R, D, B, C, gives the stage; lower rungs are implied by a later record (a decision implies recognition) and keep their own status.

| Stage | Furthest rung | Label |
|---|---|---|
| 0 | none | no warning or response record |
| 1 | W | warning not recognised |
| 2 | R | recognised, not transmitted |
| 3 | D | reached decision-makers, no budget |
| 4 | B | funded, fragmented (one decision system) |
| 5 | C | coordinated; at close with coverage < 0.5: **coordinated, then collapsed** |
| 6 | C, not collapsed, and learned | learned (faster than last time) |

While a card is open its stage reads "so far"; when closed, "stopped at". **Learned** is one comparison, not a measure of learning: the onset → decision lag is shorter than the shortest lag of an earlier closed card of the same ISO3 and hazard in the stream; with no earlier card it is unknown. The stage is a card label (a profile field); no stage is summed or weighted into a score.

## 8. English pageview matching rule and per-article E2 filters (for a later session)

Pageviews are **not** fetched now; the host guard (STREAM_DATA §10) still refuses every Wikimedia host. A later session may add them only with this rule, unchanged:

1. **Before any Wikimedia request** (matching or pageviews), the event passes `e2_refusal`; after redirect resolution the resolved title passes it again.
   - **E2a** (GWI v2): refused if EQ with onset 25 Oct 2026 – 7 Nov 2027 and any magnitude ≥ 6.8 or unknown, or an EQ without onset; refused if the title is one of the 20 GWI v2 placebos (and "Mitochondria"); until GWI v2 is scored and the date is ≥ 16 Nov 2027.
   - **E2b** (flood test top lists): only English per-article daily URLs are ever built; a URL containing `/top/` is refused.
   - **E2c** (flood test): refused if the title names a river; or if the event is a flood, or the title is flood-like, and the event has no ISO3, an EU27 ISO3, or the title names an EU27 country, a nationality or Europe; until the flood test is scored and the date is ≥ 1 Feb 2029.
   - **E2d** (2027 hurricane arm): refused if TC with onset ≥ 1 Jan 2027 (or no onset) and the event touches USA/PRI/VIR or lies in the box lat 0…70, lon −110…0 (or has no position), until that season is in `HURRICANE_SEASONS_SCORED`.
   - The three flags in `cards.py` are set only by the session that scores each protected test, recorded in `docs/RECORD.md`.
2. **Candidates** from templates only: TC "{Hurricane|Typhoon|Cyclone|Tropical Storm|Severe Tropical Storm|Severe Cyclonic Storm} {Name}" and the same with " ({year})", Name from GDACS `eventname` without its "-YY" suffix; EQ "{year} {country} earthquake(s)"; FL "{year} {country} flood(s)", country from the GDACS English country field. No template for VO, DR, WF, TS: attention "no source".
3. **Valid target** (after redirects, English Wikipedia): exists, main namespace, not a disambiguation page, not a redirect to a section, not "List of…", no word "season", and created no earlier than 2 days before onset. Exactly one distinct valid target → matched; two or more → ambiguous (attention "missing"); none → "not yet" within 30 days of onset, then "absent".
4. **Attention:** user-agent daily views, onset − 7 … onset + 30; present on the earliest day in onset … onset + 30 with ≥ 1,000 views. It is also a recognition record (§5).

## 9. H3 stream test (registered now; scored on or after 1 Aug 2027)

- **Population:** cards with a decision record, a natural hazard class, **no EU27 country** (E1 makes their decision rung incomplete), and onset (or, if unanchored, decision-record onset) 1 Dec 2026 – 31 May 2027.
- **Measurable:** the card is anchored by a hazard record (K1–K3, F1, F2; a GO or CEMS record left unjoined counts as **not** measurable), onset and decision times parse, and −3 ≤ lag(onset → decision) ≤ 60 days.
- **Statistic:** share measurable, k/n. Dependence: the same rule on one unit per cluster (ISO3 set, hazard, onset month), the earliest listed.
- **Decision:** PASS if the one-sided 95 % Clopper–Pearson lower bound exceeds 0.5 for both the units and the clusters; FAIL if the units' upper bound is below 0.5; otherwise "not decided at this size". "Not testable at this size" if n < 20 or clusters < 20. Both conditions that can make a PASS are significance conditions; no point comparison decides.
- **Power** (synthetic, `analysis/loop_card_power_output.txt`; clusters of 1 + Poisson(0.25), intra-cluster correlation 0.2, 4,000 reps): false PASS at p = 0.5: 0.015–0.027; PASS at p = 0.7: 0.46 (n ≈ 30), 0.72 (45), 0.84 (60), 0.95 (90); at p = 0.6 below 0.5 for every n tried. Expected n from STREAM_DATA §4 (8–15 linked events a month, before EU27 removal): about 45–90. **Power below 0.5 holds if the true share is only 0.6 or n is near 30**; then a FAIL or undecided reads "not shown at this size".
- **Who runs it:** a GitHub Action with the secret, after 1 Aug 2027; it commits only the §11 aggregates.

## 10. Allowed amendments (before 30 Nov 2026 only)

Field names (§3–§5) may be corrected once, before the §9 window opens, from a **schema-presence aggregate** made inside the Action: for each source and documented field, the share of records where the key is present (no values, no counts of records). Allowed changes: a field's name or path, and adding a country-name → ISO3 table if CEMS gives names only. No window, threshold, tie rule, stage or decision rule may change. Each amendment is a dated section here with its aggregate committed.

## 11. What may leave the Action

Only: `safe_aggregate` (counts by onset month × hazard × stage and × rung status), the schema-presence shares (§10), the H3 counts and verdict (§9), and edge-rule counts by rule (K1…F2, ties). Never: a record, an identifier, a title, a date of a single event, or any count of CEMS records with an EU27 country (they are not nodes). Cards go public only in session 3.4 or later, after the reuse terms of STREAM_DATA §6.

## 12. Storage decision

One run is 348,928 bytes (both logged runs, `data/stream/log/`), about 127 MB a year. **Decision: keep raw records untrimmed.** Reasons: later protocols (3.5 self-model, 3.7 losses) may need fields no one chose now; a trim cannot be undone; at this rate the repository stays under 1 GB until about 2034. Review trigger: when `data/stream/` exceeds 400 MB, a session proposes a trim (likely: USGS detail documents reduced to the `losspager` product), registered before it is applied, never removing a field a registered test reads.

## Sources

No external source was opened in this session. Repository files used: `docs/STREAM_DATA.md` (§2–§5, §9, §10, §3a), `docs/STRATEGY_3_0.md` §3, `docs/PLAN.md` (H3), `docs/GWI_V2_PROTOCOL.md` (placebo list, window), `emo/stream/*.py`.
