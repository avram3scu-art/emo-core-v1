# PPE case: comparison of the new event files with the manuscript (fix session F8.8)

Pre-registered in `docs/DAC_PPE_CODING.md` §4 (committed 28 Oct 2026, before any PPE event was coded). Evidence class of every new file: **pre-registered on known history** (§1, including breaches 1 and 2). Lags are days from t0 = 30 January 2020.

## 1. Procedure

1. **Freeze.** The six files were frozen at commit `8ebcf9e` (115 tests pass; regenerated profiles identical to the committed ones; file sha256 in `docs/RECORD.md`). The new side of every comparison was written out before anything was opened: `data/dac_ppe/frozen_summary.md` (commit `7edcb3d`).
2. **Opened afterwards:** the manuscript's §3.1–§4.3 with Tables 2–5 (`docs/sources/dac_paper/Decision_or_Supply_manuscript_anonymised.md`, lines 79–172).
3. **Figures 1–2 are not in the repository.** The Markdown holds only their legends (already seen in breach 2), and the .docx contains no image files (no `word/media`). The figures were therefore not compared. Their content is described by the legends as drawn from Tables 3 and 5.
4. **Kinds of difference** (§4): (a) different source; (b) different rule or reading; (c) coding error in the new file; (d) error in the manuscript.
5. **Agreement** per item: *same*, *overlapping* (the date ranges share at least one day) or *different*. No overall score.
6. Items marked **[F8.7]** rest, in the new file, on a source added in the gap-filling sitting (outside the manuscript's reference list; Adrian's decision of 28 Oct 13:24).

## 2. Correction after the tables were opened (type c)

| File | Before (frozen, sha256 28728862…) | After | Effect on the profile |
|---|---|---|---|
| `BE.json` | The order of surgical and FFP2 masks from a national producer on 20 March 2020 (Annex 5, row 742, PDF p. 373) was not coded | Order coded (exact, 20 Mar, day 50); its delivery ("premières livraisons … début août") coded `censored` (after the observation window) and paired | No lag or first event changes; one more undatable pair per reading; one more order-file row |

The manuscript's Table 3 lists this order (order 6). It brought the omission to light. Nothing else in the new files was changed after the tables were opened.

## 3. Comparison per case

### Belgium

| Item | Manuscript | New file | Agreement | Kind | Note |
|---|---|---|---|---|---|
| First firm order | 34 (reading A: 1) | readings A 1, B 5, C 34 | same for A and C | (b) | The new file counts every dated statement as a reading (§5 Belgium b): the 4 February "option sur/commande" (row 760) is reading B. The manuscript treats it as an option. The labels differ: the manuscript's reading B is the new reading C. [F8.7]: hearings K022/K040 added as sources; dates unchanged |
| First binding act | 43 | 53 | different | (a), (b) | The new file uses the PPE-specific arrêté ministériel of 23 March 2020 (Moniteur belge, supplied by Adrian) [F8.7]. The manuscript does not name its act. The only Belgian binding act dated 13 March (day 43) in Annex 5 is the ministerial decree triggering the federal phase (PDF p. 366), a general crisis act that the new rules exclude (§2: "concerning the PPE response"). Both texts state that binding acts are not compared across cases |
| First delivery (municipalities) | 46 | 46 | same | — | |
| Unpaired first order to first delivery | 12 (A: 45) | 12 (C), 45 (A), 41 (B) | same for shared readings | (b) | Extra reading B, as above |
| Paired lag, 3M FFP2 | 23 (A: 56) | 23 (C), 56 (A), 52 (B) | same for shared readings | (b) | Delivery day 57 in both |
| Paired lag, Life surgical | 5 (order 45, delivery 50) | 5 | same | — | |
| Paired lag, Ultrazonic FFP2 | 21 (46 → 67) | 21 | same | — | |
| Paired lag, Life FFP2 | 10 (53 → 63) | 10 | same | — | |
| Paired lag, XML surgical | 6 (61 → 67) | 6 | same | — | |
| Paired lag, gloves (Erard) | 5 (note) | 5 | same | — | |
| Pan Scope order (entry 723) | excluded (delivery recorded before order) | delivery coded `missing` (source flags it contradicted) | same | — | |
| National producer order | order 50, delivery 184–198, lag 134–148 | order 50; delivery censored | different | (c) corrected, then (b) | After correction, the remaining difference is the observation window (new file ends 30 June 2020). The manuscript's 184–198 reads "début août" as 1–15 August; the new month-part rule (§5 Germany e a) would give 184–193 |
| Identification, FFP2 | 3 orders, days 34, 46, 53 (A: 1, 46, 53) | 3 paired orders, spread 19 (C), 52 (A), 48 (B) | same for shared readings | (b) | |
| Identification, surgical masks | 2 orders, days 45 and 61 | 2 paired orders, spread 16 | same | — | |
| Identification, gloves | 1 order | 1 paired order, separation not possible | same | — | |
| Order file | 9 rows, 8 orders | 10 rows, 8 orders (after the correction in §2) | same orders | (b) | Extra row from reading B |

### France

| Item | Manuscript | New file | Agreement | Kind | Note |
|---|---|---|---|---|---|
| First firm order | 8 (alt. 0) | readings A 8, B 20 | same for 8 | (b) | The manuscript's "alt. 0" is the looser first-action rule (30 January single-mission order); the new file codes that order as context. New reading B (validation of the first purchase on 19 February, §5 France a) is not in the manuscript |
| First binding act | 33 | 33 | same | — | Requisition decree of 3 March |
| Unpaired first order to first delivery | n.c. (stock) | A 31–44, B 19–32 | — | (b) | The manuscript does not compare it because the first French deliveries most plausibly came from the stock; the new file computes it mechanically |
| First delivery (pharmacies) | 39–45 | 39–52 | overlapping | (b) | The new file reads "sollicités … pour une première livraison" (week before 17 March) as a request, so it closes the window at the end of the week of 17 March. The manuscript closes it at the end of the week before |

### Germany

| Item | Manuscript | New file | Agreement | Kind | Note |
|---|---|---|---|---|---|
| First firm order | 29–51 | reading A 29–39, B 29–50 | overlapping | (a), (b) | [F8.7] The new file narrows the window with the Bundesrechnungshof report of 2025 (BMG's own purchase contracts from 9 March) and the BMG report of 4 April ("seit Mitte März"). Both texts close the window at the first delivery when no order is dated |
| First binding act | 34 | 34 | same | — | Export ban, 4 March |
| First delivery (Länder, KVs) | 51–52 | 41–50 | different (adjacent) | (a), (b) | [F8.7] The new file rests on the Bundesrechnungshof, "Mitte März 2020 begann die Auslieferung … an Länder, KVen und Bundesbehörden" (p. 13), with the convention "Mitte" = days 11–20. The manuscript's source for 21–22 March is not named in Table 5 (its §3.1 lists the Bundestag answers, the TRIS notification and one press report). A wider reading of "Mitte März" (to 24 March) would overlap. Not decidable as (c) or (d) without the manuscript's German event file, which was not recovered |
| Unpaired first order to first delivery | 0–23 | A 2–21, B −9–21 | overlapping | (a), (b) | Follows from the two rows above |

### Netherlands

| Item | Manuscript | New file | Agreement | Kind | Note |
|---|---|---|---|---|---|
| First firm order | 36–39 | 36–39 | same | — | |
| First binding act | none found | missing | same | — | |
| First delivery (ROAZ) | 51 | 51–52 | overlapping | (b) | The new file keeps 22 March in the window (the distribution "onder alle ROAZ-regio's" is not dated to 21 March; §5 Netherlands b) |
| Unpaired first order to first delivery | 12–15 | 12–16 | overlapping | (b) | Follows from the delivery window |

### Sweden

| Item | Manuscript | New file | Agreement | Kind | Note |
|---|---|---|---|---|---|
| First firm order | 0–61 (undated) | 2–30 (February) | overlapping | (b) | The new file counts Socialstyrelsen's "smärre inköp i februari" as the first firm order (§5 Sweden a). The manuscript treats the order as undated |
| First binding act | 46 | 46 | same | — | Ordinance 2020:126, 16 March |
| First delivery (regions, municipalities) | 41–61 | 47–61 | overlapping | (a) | [F8.7] New lower bound: first recorded delivery from Socialstyrelsen, 17 March (SOU 2020:80, p. 206). The manuscript's lower bound, 11 March, matches the meeting at which regions were told Socialstyrelsen was active on the market (SOU 2021:89, p. 325); its source is not named in Table 5. Upper bound (end of March, Figure 8.2) the same |
| Unpaired first order to first delivery | 0–61 | 17–59 | overlapping | (b) | Follows from the rows above |

### EU level

| Item | Manuscript | New file | Agreement | Kind | Note |
|---|---|---|---|---|---|
| First firm order | none; tender on day 29 | missing; first tender 27–28 February (days 28–29, context) | same coding; dates overlapping | (b) for the dates | The new file keeps the two Belgian chronology dates (rows 360 and 44) as a window. The tender rule was known from breach 2 |
| First binding act | 44 | 44 | same | — | Regulation 2020/402 |
| First delivery (member states) | 86 (stockpile); joint procurement ≥ 62 | 86 | same for the stockpile | (a) for joint procurement | No source in the new pool dates deliveries under joint procurement. The manuscript's source for "≥ 62" is not named in Table 5 |
| Counter-measure | (not in Table 5) | German export ban, 34 | — | — | |
| Dedicated funding | (not in Table 5) | missing [F8.7] | — | — | Amending budgets 1–2/2020 not earmarked for PPE |

### Table 2 (counts of entries)

Every case differs in its number of entries: the manuscript has 18 / 12 / 14 / 14 / 12 / 21; the new files have 33 / 15 / 16 / 18 / 20 / 13 (BE / FR / DE / NL / SE / EU). This is kind (b): the new files code more context rows and readings as separate rows; the EU file codes no vaccine events. Counts are not comparable item by item and carry no weight.

## 4. Summary profile (not a score)

| Case | Same | Overlapping | Different |
|---|---|---|---|
| Belgium | first delivery; unpaired interval and 3M lag under shared readings; five paired lags; gloves; Pan Scope exclusion; identification under shared readings | — | binding act (a, b); national-producer delivery (b, after a type-c correction) |
| France | binding act; first order under reading A | first delivery (b) | — |
| Germany | binding act | first order (a, b); unpaired interval (a, b) | first delivery (a, b) |
| Netherlands | first order; binding act (none) | first delivery (b); unpaired interval (b) | — |
| Sweden | binding act | first order (b); first delivery (a); unpaired interval (b) | — |
| EU | binding act; stockpile delivery; no firm order | tender date (b) | joint-procurement delivery (a) |

Errors found: one type (c) in the new files (corrected, §2); no type (d) error in the manuscript was found. The arithmetic of every interval in Tables 3 and 5 was checked against the table's own order and delivery days. Where the manuscript's source for an item is not named in its tables, the difference is classified (a) or (b), not (d).

## 5. Data statement (which items the paper may cite from the new files)

Per §4.6 the paper may cite the new files for items that agree or whose differences are explained. Every difference above is explained, so every item may be cited **from the new files, with the new value**, on these conditions:

1. **Cite as now**, with the reading named: Belgian paired lags and first delivery; first delivery in France, the Netherlands and Sweden (as windows); every first binding act except Belgium's; first orders in France, the Netherlands and Belgium (under readings A and C).
2. **Cite with the new value and the rule stated:**
   - Belgium's first binding act is day 53, not 43, and is PPE-specific.
   - Sweden's first order is February (days 2–30), not undated.
   - Belgium's 4 February option is a third reading.
3. **Cite with the new value and the added source named [F8.7]:**
   - Germany: first delivery days 41–50 (not 51–52); first order in two readings, days 29–39 or 29–50. The convention "Mitte" = days 11–20 must be stated.
   - Sweden: first delivery days 47–61.
4. **Do not cite** the manuscript's "joint procurement ≥ 62" or the national producer's delivery days (184–198) from the new files: the new files contain no dated value for them.
5. The cross-case statements of the manuscript's §4.3 that depend on Germany's delivery ("within six days of one another", days 46, 51–52 and 51) do not hold with the new files: the first deliveries now fall on day 46 (BE), 41–50 (DE), 51–52 (NL) and 47–61 (SE). Any such sentence must be recomputed from the new profiles before it is used.
