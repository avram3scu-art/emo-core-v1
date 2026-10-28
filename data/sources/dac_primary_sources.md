# Primary sources for the ozone and climate t0 and binding-act events (F7, 2026-10-28)

Opened 2026-10-28 by Claude (curl through the session proxy; rules in `docs/DAC_STANDARD.md` §6, fixed before opening). Pages are not committed (publisher and UN pages); sha256 of the HTML as fetched is given so the copy can be recognised.

| Event | Primary record (URL) | Accessed | What the record states (verbatim) | Coding |
|---|---|---|---|---|
| `molina_rowland_1974` (ozone t0) | Nature article page via https://doi.org/10.1038/249810a0 (resolves to https://www.nature.com/articles/249810a0); Crossref record https://api.crossref.org/works/10.1038/249810a0 | 2026-10-28 | "Stratospheric sink for chlorofluoromethanes: chlorine atom-catalysed destruction of ozone"; Nature, volume 249, issue 5460, pages 810–812; "Published: 28 June 1974" (Crossref: issued 1974-06) | date 1974-06-28 unchanged; precision year → **day** (the article page states the day) |
| `montreal_protocol` (ozone binding act) | UN Treaty Collection, Chapter XXVII 2.a: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XXVII-2-a&chapter=27&clang=_en | 2026-10-28 | "Montreal Protocol on Substances that Deplete the Ozone Layer Montreal, 16 September 1987 Entry into force : 1 January 1989" | date 1987-09-16 unchanged, day |
| `charney_1979` (climate t0) | National Academies Press record: https://nap.nationalacademies.org/catalog/12181/carbon-dioxide-and-climate-a-scientific-assessment (DOI https://doi.org/10.17226/12181) | 2026-10-28 | "Carbon Dioxide and Climate: A Scientific Assessment 1979 Consensus Study Report"; "National Research Council. 1979." | year only: window 1979 unchanged (the record gives no day or month; the PDF needs a login and was not opened) |
| `kyoto_adopted` (climate binding act) | UN Treaty Collection, Chapter XXVII 7.a: https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XXVII-7-a&chapter=27&clang=_en | 2026-10-28 | "Kyoto Protocol to the United Nations Framework Convention on Climate Change Kyoto, 11 December 1997 Entry into force : 16 February 2005" | date 1997-12-11 unchanged, day |

Failed attempts on record: nature.com article page and .ris returned HTTP 429 twice; Crossref returned 429 once, then 200; WebFetch refused all four URLs (not on its allowlist). The article page was then read through the DOI resolver.

sha256 of fetched pages: Nature d8eef3ed239f2e58…, Crossref JSON 2076b02158017fea…, NAP fe299ace4b1f3df6…, UNTC Montreal 6404f064615c9469…, UNTC Kyoto fb51c4f62a0c42b7…
