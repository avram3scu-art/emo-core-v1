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
