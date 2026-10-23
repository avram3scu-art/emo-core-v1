# Organismality Index — cooperation axis data (downloaded 20 Oct 2026)

1. International scientific co-authorship (cognitive cooperation)
   - `openalex_articles_multicountry_by_year.json`: OpenAlex API,
     https://api.openalex.org/works?filter=type:article,countries_distinct_count:%3E1&group_by=publication_year
   - `openalex_articles_anycountry_by_year.json`: same with countries_distinct_count:>0 (denominator: articles with known country).
   - Share = multi-country / any-country. OpenAlex data CC0. group_by returns at most 200 groups (years before ~1826 omitted; irrelevant here).
   - Caveat: recent years may still be incompletely indexed; affiliation coverage varies over time.

2. Official development assistance (material cooperation)
   - `owid_foreign_aid_share_of_gni.csv`: Our World in Data, "Foreign aid given as a share of national income"
     (ODA by donor, % of GNI, official estimate; OECD DAC data). Series used: "DAC countries". CC BY 4.0.

3. Ozone-depleting substances (one global collective action; saturating)
   - `owid_ozone_depleting_substance_consumption.csv`: Our World in Data, consumption by gas, ODP tonnes; "World" = sum of gases.
     Source as given by OWID (UNEP Ozone Secretariat data). Years 1986–2021 for World.

## Composition control (added 20 Oct 2026)
- `openalex_single_country_2020_by_country.json`, `openalex_single_country_2025_by_country.json`: single-country articles by country.
  Of the +1.10 M growth in single-country articles 2020→2025, China contributed +456 k (41%) and Indonesia +366 k (33%; likely
  OpenAlex coverage expansion of Indonesian journals — inference, not verified).
- `openalex_articles_multicountry_by_year_excl_CN_ID.json`, `openalex_articles_anycountry_by_year_excl_CN_ID.json`: same series
  excluding any article with an author in China or Indonesia (filters authorships.countries:!CN and !ID).
- Result: with all countries the share falls 18.5% (2020) → 16.7% (2025); excluding CN & ID it is 17.9% → 18.2% (plateau since 2021).
  The apparent post-2020 decline is a composition/coverage effect. Use the excluded series for trend statements.

## Weekly refresh
These files are refreshed weekly by `.github/workflows/weekly_refresh.yml`; retrieval dates, hashes and changes are in `data/MANIFEST.json` and `results/weekly/`. Figures quoted in this README are from the 20 Oct 2026 download unless stated otherwise.

Location: each file is in its own folder, `data/sources/<file name without extension>/`; source URL and download date are in `data/MANIFEST.json`.
