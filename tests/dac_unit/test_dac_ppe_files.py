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
FR_PHRASES = {
    "who_pheic": [(30, "30/01 L’OMS déclare l’USSPI"), (37, "l’USPPI est enfin déclarée le 30 janvier")],
    "stock_at_t0": [(105, "33 millions de masques pédiatriques")],
    "order_30jan_mission": [(114, "le 30 janvier 2020"), (115, "équipes médicales qui se sont rendues à Wuhan")],
    "order_ffp2_28m": [(115, "Le lendemain, Santé publique France est saisie"), (146, "du 7 février (28,4 millions de FFP2)"),
                       (123, "validée le 19 février")],
    "order_ffp2_170m": [(116, "25 février (170 millions"), (146, "25 février (170,5 millions")],
    "pharmacies_volunteer": [(141, "volontaires dès le 18 février"), (142, "dès le 18 février")],
    "channel_announced": [(49, "le 2 mars 2020 que les professionnels de santé libéraux ont été informés")],
    "decree_requisition": [(131, "Décret n° 2020-190 du 3 mars 2020")],
    "decree_requisition_13mar": [(131, "Décret n° 2020-247 du 13 mars 2020")],
    "funding_spf_11mar": [(352, "260 millions d’euros")],
    "del_pharmacies": [(142, "pour une première livraison de masques aux officines"), (141, "pendant la semaine du 17 mars")],
    "prefect_requisition": [(134, "Le 5 avril 2020"), (135, "préfet du Haut-Rhin")],
}


def test_french_citations_match_their_pages():
    import re
    text = (D.parent / "sources/dac_ppe/FR_senat_r20-199-11.txt").read_text(encoding="utf-8")
    parts = re.split(r"===== PDF page (\d+) =====\n", text)[1:]
    pages = {int(a): re.sub(r"\s+", " ", b) for a, b in zip(parts[::2], parts[1::2], strict=True)}
    rows = json.loads((D / "FR.json").read_text(encoding="utf-8"))["events"]
    sen = {e["event_id"] for e in rows if e["source"].startswith("Sénat") and e["date_status"] != "missing"}
    sources: dict[str, str] = {}
    for e in rows:  # readings share an event_id: combine their sources
        sources[e["event_id"]] = sources.get(e["event_id"], "") + " " + e["source"].split("tome I,")[-1]
    assert set(sen) == set(FR_PHRASES), set(sen) ^ set(FR_PHRASES)
    def cited(src: str) -> set[int]:
        nums: set[int] = set()
        for a, b in re.findall(r"(\d+)(?:-(\d+))?", src):
            nums.update(range(int(a), int(b or a) + 1))
        return nums
    bad = [(k, p, s) for k, v in FR_PHRASES.items() for p, s in v
           if s not in pages[p] or p not in cited(sources[k])]
    assert not bad, bad


# F8.3: each German citation is checked by a verbatim phrase on its cited page of the committed text.
DE_PHRASES = {
    "who_pheic": [("BE_annex5.txt", 342, "Urgence de santé publique de portée internationale")],
    "who_pandemic": [("BE_annex5.txt", 363, "L'OMS déclare la pandémie")],
    "no_federal_stock": [("DE_btd_19-19047.txt", 2, "Gleiches gilt für die Bevorratung von Schutzmaterialien im Pandemiefall")],
    "procurement_start": [("DE_btd_19-21798.txt", 2, "Seit 28. Februar 2020 wurde zunächst über die Beschaffungsämter")],
    "first_order_federal": [("DE_btd_19-21798.txt", 2, "Seit 28. Februar 2020"), ("DE_btd_19-21798.txt", 8, "I. 27. April 2020")],
    "export_ban": [("DE_tris_2020-0104-D.txt", 1, "Date received : 04/03/2020"),
                   ("DE_tris_2020-0104-D.txt", 1, "Ban on the export and shipment of goods"),
                   ("BE_annex5.txt", 358, "Interdiction d'exportation à partir de l'Allemagne")],
    "bmg_own_procurement": [("DE_btd_19-21798.txt", 2, "ab dem 9. März 2020 zur Intensivierung")],
    "logistics_concept": [("DE_btd_19-21798.txt", 14, "Logistikkonzepts am 24. und 25. März 2020")],
    "open_house_programme": [("DE_btd_19-21798.txt", 11, "seit dem 27. März 2020 beauftragten")],
    "del_laender_kv": [("DE_btd_19-21798.txt", 2, "Kurze Zeit später begann die Auslieferung"),
                       ("DE_btd_19-21798.txt", 8, "Häufig waren diese Waren noch in den Lagern der Empfänger")],
}


def _pages(fname):
    import re
    text = (D.parent / "sources/dac_ppe" / fname).read_text(encoding="utf-8")
    parts = re.split(r"===== PDF page (\d+) =====\n", text)[1:]
    return {int(a): re.sub(r"\s+", " ", b).replace("- ", "") for a, b in zip(parts[::2], parts[1::2], strict=True)}


def test_german_citations_match_their_pages():
    rows = json.loads((D / "DE.json").read_text(encoding="utf-8"))["events"]
    cited = {e["event_id"] for e in rows if e["date_status"] != "missing" and e["source_type"] == "primary"}
    assert cited == set(DE_PHRASES), cited ^ set(DE_PHRASES)
    src = {e["event_id"]: e["source"] for e in rows}
    cache: dict[str, dict[int, str]] = {}
    bad = []
    for k, items in DE_PHRASES.items():
        for fname, page, phrase in items:
            pages = cache.setdefault(fname, _pages(fname))
            if phrase not in pages[page] or f"p. {page}" not in src[k]:
                bad.append((k, fname, page, phrase))
    assert not bad, bad


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


def test_dutch_citations_match_their_pages():
    rows = json.loads((D / "NL.json").read_text(encoding="utf-8"))["events"]
    cited = {e["event_id"] for e in rows if e["source_type"] == "primary" and "searched in full" not in e["source"]}
    assert cited == set(NL_PHRASES), cited ^ set(NL_PHRASES)
    src = {e["event_id"]: e["source"] for e in rows}
    cache: dict[str, dict[int, str]] = {}
    bad = []
    for k, items in NL_PHRASES.items():
        for fname, page, phrase in items:
            pages = cache.setdefault(fname, _pages(fname))
            if phrase not in pages[page] or f"p. {page}" not in src[k]:
                bad.append((k, fname, page, phrase))
    assert not bad, bad


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
    "first_delivery_regions": [(SE, 338, "Fördelad skyddsutrustning och provtagningsutrustning per månad, som komplement i regioner och kommuner, mars 2020 till mars 2021"),
                               (SE, 338, "2020-mar")],
    "crisis_office_distribution": [(SE, 334, "Det material som Socialstyrelsen får in distribueras till verksamheter"),
                                   (SE, 334, "den 3 april 2020")],
    "ce_waiver": [(SE, 329, "Den 7 april beslutade regeringen att tillfälligt slopa kravet på CEmärkning")],
    "adda_mandate": [(SE, 329, "Den 8 april fick SKR:s inköpscentral Adda")],
    "adda_webshop": [(SE, 330, "Den 27 maj började Adda genom sin webbutik leverera materiel till kommunerna")],
    "statsbidrag": [(SE, 334, "Riksdagen beslutade under 2020 att fördela statsbidrag"),
                    (SE, 334, "förordningen (2020:193)")],
}


def test_swedish_citations_match_their_pages():
    rows = json.loads((D / "SE.json").read_text(encoding="utf-8"))["events"]
    cited = {e["event_id"] for e in rows if e["source_type"] == "primary" and "searched in full" not in e["source"]}
    assert cited == set(SE_PHRASES), cited ^ set(SE_PHRASES)
    src = {e["event_id"]: e["source"] for e in rows}
    cache: dict[str, dict[int, str]] = {}
    bad = []
    for k, items in SE_PHRASES.items():
        for fname, page, phrase in items:
            pages = cache.setdefault(fname, _pages(fname))
            if phrase not in pages[page] or f"p. {page}" not in src[k]:
                bad.append((k, fname, page, phrase))
    assert not bad, bad
