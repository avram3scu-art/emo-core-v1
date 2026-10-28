"""Every coded PPE case file (data/dac_ppe/<case>.json) validates and its committed profile is current."""

import json
from pathlib import Path

import pytest

from emo.dac_standard import compute_profile, load_event_file

D = Path(__file__).resolve().parents[2] / "data/dac_ppe"
CASES = sorted(D.glob("[A-Z][A-Z].json"))


@pytest.mark.parametrize("path", CASES, ids=[p.stem for p in CASES])
def test_case_file_valid_and_profile_current(path):
    prof = compute_profile(load_event_file(path))
    committed = json.loads((D / f"{path.stem}_profile.json").read_text(encoding="utf-8"))
    assert prof == committed, f"rerun scripts/dac_ppe_outputs.py for {path.stem}"


def test_belgian_file_is_coded():
    assert (D / "BE.json").exists() and (D / "BE_orders.csv").exists()


def _annex5_rows():
    """(PDF page, row number) of every entry in the committed Belgian Annex 5 text."""
    import re
    lines = (D.parent / "sources/dac_ppe/BE_annex5.txt").read_text(encoding="utf-8").split("\n")
    rows, page = set(), None
    for i, ln in enumerate(lines):
        m = re.search(r"===== PDF page (\d+)", ln)
        if m:
            page = int(m.group(1))
            continue
        m = re.match(r"^\s{40,}(\d{2})/(\d{2})/(\d{4})\s{2,}", ln)
        if m:
            j = i - 1
            while j > 0 and not lines[j].strip():
                j -= 1
            if lines[j].strip().isdigit():
                rows.add((page, lines[j].strip(), f"{m.group(3)}-{m.group(2)}-{m.group(1)}"))
    return rows


def test_belgian_citations_point_to_existing_rows():
    """Every 'PDF p. N, row R' cited in BE.json is an entry with row number R on page N of Annex 5."""
    import re
    rows = _annex5_rows()
    pages = {(r[0], r[1]) for r in rows}
    bad, n = [], 0
    for e in json.loads((D / "BE.json").read_text(encoding="utf-8"))["events"]:
        m = re.search(r"PDF p\. (\d+), row (\d+)", e["source"])
        if not m:
            continue
        n += 1
        key = (int(m.group(1)), m.group(2))
        if key not in pages:
            bad.append((e["event_id"], key, "row not on page"))
        # the row's own date must be the event's date, except deliveries (their date is stated in the order's row)
        elif e["sublayer"] != "delivery" and e.get("date_earliest") and (*key, e["date_earliest"]) not in rows:
            bad.append((e["event_id"], key, "row date differs"))
    assert n and not bad, bad


# F8.2: each French citation is checked by a verbatim phrase on its cited PDF page.
FRS = "FR_senat_r20-199-11.txt"
FR_PHRASES = {
    "who_pandemic": [("BE_annex5.txt", 363, "L'OMS déclare la pandémie")],
    "who_pheic": [(FRS, 30, "30/01 L’OMS déclare l’USSPI"), (FRS, 37, "l’USPPI est enfin déclarée le 30 janvier")],
    "stock_at_t0": [(FRS, 105, "33 millions de masques pédiatriques")],
    "order_30jan_mission": [(FRS, 114, "le 30 janvier 2020"), (FRS, 115, "équipes médicales qui se sont rendues à Wuhan")],
    "order_ffp2_28m": [(FRS, 115, "Le lendemain, Santé publique France est saisie"), (FRS, 146, "du 7 février (28,4 millions de FFP2)"),
                       (FRS, 123, "validée le 19 février")],
    "order_ffp2_170m": [(FRS, 116, "25 février (170 millions"), (FRS, 146, "25 février (170,5 millions")],
    "pharmacies_volunteer": [(FRS, 141, "volontaires dès le 18 février"), (FRS, 142, "dès le 18 février")],
    "channel_announced": [(FRS, 49, "le 2 mars 2020 que les professionnels de santé libéraux ont été informés")],
    "decree_requisition": [(FRS, 131, "Décret n° 2020-190 du 3 mars 2020")],
    "decree_requisition_13mar": [(FRS, 131, "Décret n° 2020-247 du 13 mars 2020")],
    "funding_spf_11mar": [(FRS, 352, "260 millions d’euros")],
    "del_pharmacies": [(FRS, 142, "pour une première livraison de masques aux officines"), (FRS, 141, "pendant la semaine du 17 mars")],
    "prefect_requisition": [(FRS, 134, "Le 5 avril 2020"), (FRS, 135, "préfet du Haut-Rhin")],
}


# F8.3: each German citation is checked by a verbatim phrase on its cited page of the committed text.
DE_PHRASES = {
    "who_pheic": [("BE_annex5.txt", 342, "Urgence de santé publique de portée internationale")],
    "who_pandemic": [("BE_annex5.txt", 363, "L'OMS déclare la pandémie")],
    "no_federal_stock": [("DE_btd_19-19047.txt", 2, "Gleiches gilt für die Bevorratung von Schutzmaterialien im Pandemiefall")],
    "procurement_start": [("DE_btd_19-21798.txt", 2, "Seit 28. Februar 2020 wurde zunächst über die Beschaffungsämter")],
    "first_order_federal": [("DE_btd_19-21798.txt", 2, "Seit 28. Februar 2020"),
                            ("DE_brh_enquete_2025.txt", 13, "Das BMG begann am 9. März 2020"),
                            ("DE_brh_enquete_2025.txt", 13, "mit dem Abschluss eigener Kaufverträge über PSA"),
                            ("DE_bmg_beschaffungsstab_1.txt", 2, "durch das Ministerium selbst (seit Mitte März)"),
                            ("DE_brh_enquete_2025.txt", 13, "Mitte März 2020 begann die Auslieferung")],
    "export_ban": [("DE_tris_2020-0104-D.txt", 1, "Date received : 04/03/2020"),
                   ("DE_tris_2020-0104-D.txt", 1, "Ban on the export and shipment of goods"),
                   ("BE_annex5.txt", 358, "Interdiction d'exportation à partir de l'Allemagne")],
    "bmg_own_procurement": [("DE_btd_19-21798.txt", 2, "ab dem 9. März 2020 zur Intensivierung"),
                            ("DE_brh_enquete_2025.txt", 13, "Das BMG begann am 9. März 2020")],
    "budget_committee_4mar": [("DE_brh_enquete_2025.txt", 10, "In den einschlägigen Sitzungen vom 4. März und 22. April 2020"),
                              ("DE_brh_enquete_2025.txt", 10, "in überplanmäßige Ausgaben für die Pande")],
    "nrgs_concept": [("DE_brh_enquete_2025.txt", 16, "Am 3. Juni 2020 hatte das Bundeskabinett")],
    "logistics_concept": [("DE_btd_19-21798.txt", 14, "Logistikkonzepts am 24. und 25. März 2020")],
    "open_house_programme": [("DE_btd_19-21798.txt", 11, "seit dem 27. März 2020 beauftragten")],
    "del_laender_kv": [("DE_brh_enquete_2025.txt", 13, "Mitte März 2020 begann die Auslieferung erster vom Bund beschaffter Schutzausrüstung an Länder, KVen und Bundesbehörden"),
                       ("DE_btd_19-21798.txt", 2, "Kurze Zeit später begann die Auslieferung")],
}


def _pages(fname):
    import re
    text = (D.parent / "sources/dac_ppe" / fname).read_text(encoding="utf-8")
    parts = re.split(r"===== PDF page (\d+) =====\n", text)[1:]
    if not parts:  # a source without pages (rendered web page): the whole text is page 1
        return {1: re.sub(r"\s+", " ", text)}
    return {int(a): re.sub(r"\s+", " ", b).replace("- ", "") for a, b in zip(parts[::2], parts[1::2], strict=True)}


# F8.4: each Dutch citation is checked by a verbatim phrase on its cited page (text kept in reading order).
NL_PHRASES = {
    "who_pheic": [("BE_annex5.txt", 342, "Urgence de santé publique de portée internationale")],
    "who_pandemic": [("BE_annex5.txt", 363, "L'OMS déclare la pandémie")],
    "inventory_start": [("NL_vws_tijdlijn_pbm.txt", 6, "start VWS op 30 januari met een inventarisatie")],
    "bao_central_distribution": [("NL_vws_tijdlijn_pbm.txt", 8, "Op 28 februari adviseert het BAO"),
                                 ("NL_vws_tijdlijn_pbm.txt", 20, "Op 28 februari adviseert het Bestuurlijk Afstemmingsoverleg")],
    "eu_jpa_registration": [("NL_vws_tijdlijn_pbm.txt", 8, "inschrijving van de eerste Europese aanbesteding")],
    "roaz_three_hours": [("NL_vws_tijdlijn_pbm.txt", 9, "binnen drie uur beschermingsmiddelen geleverd krijgen")],
    "first_order_national": [("NL_vws_tijdlijn_pbm.txt", 9, "VWS helpt de NFU vanaf 6 maart actief met de inkoop"),
                             ("NL_vws_tijdlijn_pbm.txt", 9, "De directie heeft op dit moment 500.000 mondmaskers gekocht")],
    "minister_letter_10mar": [("NL_vws_tijdlijn_pbm.txt", 9, "start is gemaakt met de aankoop en distributie van mondmaskers door de ROAZ")],
    "announced_500k": [("NL_vws_tijdlijn_pbm.txt", 9, "morgen de eerste 500.000 mondmaskers aankomen")],
    "redistribution_providers": [("NL_vws_tijdlijn_pbm.txt", 10, "rond de 200.000 verschillende typen mondmaskers kunnen herverdelen")],
    "no_requisition": [("NL_vws_tijdlijn_pbm.txt", 10, "geen vorderingsbesluit ten behoeve van persoonlijke beschermingsmiddelen")],
    "order_china_690k": [("NL_vws_tijdlijn_pbm.txt", 11, "door VWS zijn besteld via een tussenleverancier")],
    "del_china_690k_roaz": [("NL_vws_tijdlijn_pbm.txt", 11, "690.000 mondmaskers is net binnen"),
                            ("NL_vws_tijdlijn_pbm.txt", 11, "verdeeld onder alle ROAZ-regio"),
                            ("NL_vws_tijdlijn_pbm.txt", 18, "Een deel van deze zending was reeds uitgeleverd aan zorgaanbieders")],
    "lch_start": [("NL_vws_tijdlijn_pbm.txt", 14, "Op 23 maart gaat het LCH van start")],
    "vat_zero_masks": [("NL_vws_tijdlijn_pbm.txt", 32, "Het nultarief zal worden toegepast met ingang van 25 mei")],
}


# F8.5: each Swedish citation is checked by a verbatim phrase on its cited PDF page of SOU 2021:89.
# The delivery's March bar is read from the rendered Figure 8.2; the test checks the caption and the month label only.
SE = "SE_sou_2021_89.txt"
SE_PHRASES = {
    "who_pheic": [("BE_annex5.txt", 342, "Urgence de santé publique de portée internationale")],
    "who_pandemic": [("BE_annex5.txt", 363, "L'OMS déclare la pandémie")],
    "sos_alerts_msb": [(SE, 322, "Socialstyrelsen hade den 4 februari uppmärksammat MSB på att en möjlig brist på skyddsutrustning förelåg")],
    "msb_urges_regions": [(SE, 322, "MSB publicerade den 6 februari en nationell lägesbild"),
                          (SE, 322, "Regionerna bör uppmanas att säkerställa inköp och distribution")],
    "first_order_sos": [(SE, 371, "gjorde smärre inköp av skyddsutrustning i februari"),
                        (SE, 336, "gjordes inköp av skyddsutrustning redan från februari 2020"),
                        (SE, 34, "Socialstyrelsen gjorde i februari visserligen mindre inköp")],
    "regions_assured": [(SE, 325, "Redan den 11 mars 2020 tillförsäkrades samtliga regioner")],
    "regions_petition": [(SE, 324, "Den 13 mars 2020 lämnade Region Stockholm, Västra Götalandsregionen och Region Skåne in en hemställan")],
    "sos_assignment": [(SE, 325, "Den 16 mars 2020 fick Socialstyrelsen i uppdrag av regeringen att säkerställa tillgången till skyddsutrustning")],
    "ordinance_2020_126": [(SE, 326, "den 16 mars, fattade regeringen beslut om förordningen (2020:126)")],
    "sos_purchasing_reported": [("SE_sou_2020_80.txt", 154, "påbörjat arbetet med inköp av skyddsutrustning och materiel för provtagning genom EU samt på egen hand")],
    "first_noted_delivery_sos": [("SE_sou_2020_80.txt", 206, "Den första noterade leveransen från Socialstyrelsen sker den 17 mars")],
    "delivery_lansstyrelse_sthlm": [("SE_sou_2020_80.txt", 206, "Länsstyrelsen i Stockholms län som den 21 mars fick 4 800 munskydd")],
    "first_delivery_regions": [("SE_sou_2020_80.txt", 206, "Den första noterade leveransen från Socialstyrelsen sker den 17 mars"),
                               (SE, 338, "Fördelad skyddsutrustning och provtagningsutrustning per månad, som komplement i regioner och kommuner, mars 2020 till mars 2021"),
                               (SE, 338, "2020-mar")],
    "crisis_office_distribution": [(SE, 334, "Det material som Socialstyrelsen får in distribueras till verksamheter"),
                                   (SE, 334, "den 3 april 2020")],
    "ce_waiver": [(SE, 329, "Den 7 april beslutade regeringen att tillfälligt slopa kravet på CEmärkning")],
    "adda_mandate": [(SE, 329, "Den 8 april fick SKR:s inköpscentral Adda")],
    "adda_webshop": [(SE, 330, "Den 27 maj började Adda genom sin webbutik leverera materiel till kommunerna")],
    "statsbidrag": [(SE, 334, "Riksdagen beslutade under 2020 att fördela statsbidrag"),
                    (SE, 334, "förordningen (2020:193)")],
}


# F8.6: each EU citation is checked by a verbatim phrase on its cited page (the EP photo record has no pages: p. 1).
R402, D414, SEN, EPF = "EU_32020R0402.txt", "EU_32020D0414.txt", "FR_senat_r20-199-11.txt", "EU_ep_photo_P043686.txt"
EU_PHRASES = {
    "who_pheic": [("BE_annex5.txt", 342, "Urgence de santé publique de portée internationale")],
    "who_pandemic": [("BE_annex5.txt", 363, "L'OMS déclare la pandémie")],
    "jpa_start_communicated": [("BE_annex5.txt", 346, "Communication du début du Joint Procurement")],
    "jpa_first_tender": [("BE_annex5.txt", 353, "Masques buccaux et autres équipements de protection : la Belgique participe à"),
                         ("BE_annex5.txt", 354, "Premier joint procurement EPI"),
                         (R402, 1, "a procurement procedure for personal protective equipment has been launched under the Joint Procurement Agreement")],
    "de_export_ban": [("DE_tris_2020-0104-D.txt", 1, "Date received : 04/03/2020"),
                      ("DE_tris_2020-0104-D.txt", 1, "Ban on the export and shipment of goods"),
                      ("BE_annex5.txt", 358, "Interdiction d'exportation à partir de l'Allemagne")],
    "reg_2020_402": [(R402, 2, "Without the production of such export authorisation, the exportation is prohibited"),
                     (R402, 3, "Done at Brussels, 14 March 2020"),
                     (R402, 3, "shall enter into force on the day of its publication")],
    "dec_2020_414": [(D414, 1, "of 19 March 2020"),
                     (D414, 2, "personal protective equipment aimed at combating serious cross-border threats to health should be included in the capacities of rescEU"),
                     (D414, 3, "Total estimated costs of medical stockpiling rescEU capacities")],
    "amending_budget_1": [("EU_32020B0536.txt", 1, "Done at Brussels, 17 April 2020"),
                          ("EU_32020B0536.txt", 49, "Commitments 70 000 000 Payments 40 000 000"),
                          ("EU_32020B0536.txt", 49, "This appropriation is intended to cover expenditure on actions in the field of civil protection")],
    "amending_budget_2": [("EU_32020B0537.txt", 1, "Done at Brussels, 17 April 2020"),
                          ("EU_32020B0537.txt", 28, "Commitments 300 000 000 Payments 150 000 000"),
                          ("EU_32020B0537.txt", 28, "This appropriation is intended to cover expenditure on actions in the field of civil protection")],
    "first_resceu_delivery": [(SEN, 400, "La première livraison de masques issue de cette réserve est intervenue le 25 avril 2020"),
                              (SEN, 400, "à destination de l’Italie, de l’Espagne et de la Croatie"),
                              (EPF, 1, "On 25 April 2020, FFP2 protective masks from the RescEU Reserve were delivered to Milan, Italy")],
}


# F8.7: one check for every case. A phrase must stand on its cited page, and that page must be cited in the
# part of the source field that names the same document (not "p. N" anywhere in the field).
DOC_KEYS = {
    "BE_annex5.txt": "Annexe 5",
    "FR_senat_r20-199-11.txt": "Sénat",
    "DE_btd_19-21798.txt": "Drucksache 19/21798",
    "DE_btd_19-19047.txt": "Drucksache 19/19047",
    "DE_tris_2020-0104-D.txt": "TRIS",
    "DE_brh_enquete_2025.txt": "Bundesrechnungshof",
    "DE_bmg_beschaffungsstab_1.txt": "Beschaffungsstab",
    "NL_vws_tijdlijn_pbm.txt": "Feitenreconstructie",
    "SE_sou_2021_89.txt": "SOU 2021:89",
    "SE_sou_2020_80.txt": "SOU 2020:80",
    "EU_32020R0402.txt": "2020/402",
    "EU_32020D0414.txt": "2020/414",
    "EU_ep_photo_P043686.txt": "photo record",
    "EU_32020B0536.txt": "2020/536",
    "EU_32020B0537.txt": "2020/537",
}
CASE_PHRASES = {"FR": FR_PHRASES, "DE": DE_PHRASES, "NL": NL_PHRASES, "SE": SE_PHRASES, "EU": EU_PHRASES}


def cited_pages(source: str, key: str) -> set[int]:
    """Pages cited for the document named by `key`: the source text from each mention of `key`
    to the next mention of another document."""
    import re
    others = [k for k in DOC_KEYS.values() if k != key]
    pages: set[int] = set()
    for m in re.finditer(re.escape(key), source):
        seg = source[m.end():]
        cut = [seg.find(o) for o in others if seg.find(o) >= 0]
        seg = seg[:min(cut)] if cut else seg
        for a, b in re.findall(r"\bpp?\.\s*(\d+)(?:\s*-\s*(\d+))?(?:\s*and\s*p\.\s*\d+)?", seg):
            pages.update(range(int(a), int(b or a) + 1))
        pages.update(int(x) for x in re.findall(r"\band\s+(?:PDF\s+)?p\.\s*(\d+)", seg))
    return pages


@pytest.mark.parametrize("case", sorted(CASE_PHRASES))
def test_citations_match_their_pages(case):
    phrases = CASE_PHRASES[case]
    rows = json.loads((D / f"{case}.json").read_text(encoding="utf-8"))["events"]
    sources: dict[str, str] = {}
    for e in rows:  # readings share an event_id: combine their sources
        if e["source_type"] == "primary" and "searched" not in e["source"]:
            sources[e["event_id"]] = sources.get(e["event_id"], "") + " ; " + e["source"]
    assert set(sources) == set(phrases), set(sources) ^ set(phrases)
    cache: dict[str, dict[int, str]] = {}
    bad = []
    for k, items in phrases.items():
        for fname, page, phrase in items:
            pages = cache.setdefault(fname, _pages(fname))
            if phrase not in pages.get(page, "") or page not in cited_pages(sources[k], DOC_KEYS[fname]):
                bad.append((k, fname, page, phrase))
    assert not bad, bad


def test_cited_pages_reads_each_document_separately():
    src = "Chambre, Annexe 5, PDF p. 353, row 360 and PDF p. 354, row 44; Regulation (EU) 2020/402, PDF p. 1, recital 3"
    assert cited_pages(src, "Annexe 5") == {353, 354}
    assert cited_pages(src, "2020/402") == {1}
    assert cited_pages("Sénat, tome I, PDF pp. 141-142", "Sénat") == {141, 142}
    assert cited_pages("SOU 2021:89, PDF p. 371, p. 336 and p. 34", "SOU 2021:89") == {371, 336, 34}


# F8.7: Belgian citations added from the hearing records and the report's main text (Annex 5 rows are checked above).
DOC_KEYS.update({"BE_criv_K022.txt": "CRIV 55 K022", "BE_criv_K040.txt": "CRIV 55 K040",
                 "BE_report_pp270-285.txt": "main report", "BE_mb_2020-03-23_ed2.txt": "Moniteur belge"})
BE_ADDED = {
    "order_3M_ffp2": [("BE_criv_K040.txt", 12, "Daarnaast ging er diezelfde dag een order buiten van 500.000 FFP2-maskers"),
                      ("BE_criv_K040.txt", 16, "FFP2-maskers die besteld werden op 31 januari"),
                      ("BE_criv_K022.txt", 4, "op 4 maart bij de firma 3M de eerste bestellingen werden geplaatst voor FFP2-maskers")],
    "del_3M_ffp2": [("BE_criv_K022.txt", 4, "pas worden geleverd vanaf 27 maart")],
    "am_23mar_sale": [("BE_mb_2020-03-23_ed2.txt", 11, "[C − 2020/40774]"),
                      ("BE_mb_2020-03-23_ed2.txt", 13, "La vente au détail des équipements de protection individuelle et des biocides suivants est uniquement autorisée aux officines agréées"),
                      ("BE_mb_2020-03-23_ed2.txt", 13, "1° masques FFP2"),
                      ("BE_mb_2020-03-23_ed2.txt", 13, "Bruxelles, le 23 mars 2020. N. MUYLLE")],
    "ar_30apr_information": [("BE_report_pp270-285.txt", 274, "l’arrêté royal du 30 avril 2020"),
                             ("BE_report_pp270-285.txt", 274, "stocks de matériel de protection individuelle"),
                             ("BE_report_pp270-285.txt", 281, "(M.B. 06.05.2020)")],
}


def test_belgian_added_citations_match_their_pages():
    rows = json.loads((D / "BE.json").read_text(encoding="utf-8"))["events"]
    sources: dict[str, str] = {}
    for e in rows:
        sources[e["event_id"]] = sources.get(e["event_id"], "") + " ; " + e["source"]
    bad = []
    for k, items in BE_ADDED.items():
        for fname, page, phrase in items:
            if phrase not in _pages(fname).get(page, "") or page not in cited_pages(sources[k], DOC_KEYS[fname]):
                bad.append((k, fname, page, phrase))
    assert not bad, bad


# Session 10b: ECDC's first risk assessment, added as an early-warning alternative t0 (docs/DAC_T0_EARLY_WARNING.md).
DOC_KEYS.update({"../dac_t0/ecdc_2020-01-09_tab_ncov.txt": "Threat Assessment Brief"})
EU_PHRASES["ecdc_first_ra"] = [("../dac_t0/ecdc_2020-01-09_tab_ncov.txt", 1, "THREAT ASSESSMENT BRIEF Pneumonia cases possibly associated with a novel coronavirus in Wuhan, China 9 January 2020")]
