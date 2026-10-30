# Field-presence check for the loop card protocol (session 3.4, 30 Oct 2026)

Serves `docs/LOOP_CARD_PROTOCOL.md` §10 (one amendment of field names before 30 Nov 2026). Evidence class: **infrastructure**. **Registered before the check ran and before any log record was opened.** Claude does not hold `EMO_STREAM_KEY` and opens no record; the check runs only inside the GitHub Action `field_presence.yml`, which commits one file, `data/stream/field_presence.json`, and prints nothing about records to the (public) Action log.

## 1. Records

All runs in `data/stream/log/` at the time of the check, decrypted in memory inside the Action. Per source, **one record per node key** (the latest snapshot, as `build_nodes` keys them: GDACS (`eventtype`, `eventid`) per feed, USGS by `id` per feed, CEMS `code`, GO event `id`, GO appeal `id`), so a long-running event counts once. CEMS records with any EU27 country (`exclusions._is_eu27` on `countries`, the same filter as `build_nodes`) are skipped before any other key is looked at: **EU27 CEMS never read**. Groups: `gdacs/search`, `gdacs/events4app`, `usgs/comcat`, `usgs/detail`, `cems`, `ifrc_go/event`, `ifrc_go/appeal` (running and updated feeds together).

## 2. What is computed (and nothing else)

For each group and each field the protocol reads (list in `emo/stream/presence.py`, `FIELDS`, copied from `emo/stream/cards.py` §2–§5 and §8):

- **present**: share of records where the key exists and its value is not null or empty;
- **parses**: share of records where the value is usable by the code that reads it (`parse_time` gives a time; `iso3_set` gives at least one code; `glide_key` parses; `hazard_from_text` gives a class; coordinates are two numbers; alert in the protocol's level names; number for amounts; `atype` 0/1). It is needed to decide the one allowed table (CEMS country names → ISO3), because a key can be present and still hold names;
- **key names** per group whose presence share is ≥ 0.05 (schema names only, at the top level and under `properties`; names that look like codes or values are left out: not matching `^[A-Za-z_][A-Za-z0-9_]{2,40}$`, or all upper-case of length ≤ 3). They show the right name when a documented one is absent.

Shares are rounded **down to the nearest 0.05** (so no share reveals a record count) and given only for groups with ≥ 20 records; a smaller group shows `"n<20"`. No values, identifiers, dates, titles or record counts are written. The output also carries the run IDs read (already public in the manifest) and the code version.

## 3. Decision rule (fixed now)

- A field **reads correctly** if its `parses` share ≥ 0.50 in the group the code reads it from.
- A field is **wrong** if `present` = 0 in a group of ≥ 20 records. Then one amendment (LOOP_CARD_PROTOCOL §10) may rename it to a key from the key list that the API documentation (`docs/STREAM_DATA.md` §9) names for the same content; if none fits, the field stays and its rung reads "missing" or "no source" as the protocol already says.
- **CEMS countries**: if `present` ≥ 0.50 and `parses` < 0.50, CEMS gives names, and the amendment adds a country-name → ISO3 table (fixed, from ISO 3166 English short names; built and committed before it is applied, without opening a record).
- A field with 0 < `parses` < 0.50 that is not one of the above is **recorded, not changed** (the protocol allows only names and the CEMS table).
- No window, threshold, tie rule, stage, population or decision rule changes. The amendment, if any, is one dated section in LOOP_CARD_PROTOCOL §10 committed with this aggregate, before 30 Nov 2026, i.e. before the §9 window opens (1 Dec 2026).

## 4. Why this cannot bias H3

The aggregate holds no event, no link and no count of cards; H3's population opens 1 Dec 2026, after the deadline. Only names and the CEMS table may change, as §10 registered on 29 Oct.
