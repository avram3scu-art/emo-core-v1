"""Fetch the primary sources of the PPE case (docs/DAC_PPE_CODING.md §3) and check their sha256.

PDFs are not committed (size); this script and the checksums are the record. For Belgium it also
writes the text of Annex 5 (chronology, PDF pages 326-549) with page markers to
data/sources/dac_ppe/BE_annex5.txt, which is committed and cited by page.
Requires curl and pdftotext. Run from the repository root: python scripts/fetch_dac_ppe_sources.py
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "dac_ppe"
SOURCES = {
    # Chamber of Representatives, special committee COVID-19, DOC 55 1394/002, 13 Sep 2021 (581 pages).
    # Same sha256 as the copy Adrian supplied on 26 Oct 2026 (docs/sources/SOURCES_SUPPLIED.md).
    "BE_55K1394002.pdf": ("https://www.dekamer.be/FLWB/PDF/55/1394/55K1394002.pdf",
                          "3a71e63dcb23f322740fbb72d39f54ffffe87ddaca87960b5b95cdc714f2323c"),
    # Sénat, commission d'enquête COVID-19, rapport no. 199 (2020-2021), tome I, 8 Dec 2020 (486 pages).
    # Same sha256 as the copy Adrian supplied on 26 Oct 2026.
    "FR_r20-199-11.pdf": ("https://www.senat.fr/rap/r20-199-1/r20-199-11.pdf",
                          "27bfb9b14b419f14878f6193029395906aba9cfbe40d20aa5a51490279bc6d77"),
    # Deutscher Bundestag, Antwort der Bundesregierung, Drucksache 19/21798 (21 Aug 2020), 68 pages.
    "DE_1921798.pdf": ("https://dserver.bundestag.de/btd/19/217/1921798.pdf",
                       "361bc1853bf4966fe86f38120015ebef806997eef1c56511fa0a369fe814ba78"),
    # Deutscher Bundestag, Antwort der Bundesregierung, Drucksache 19/19047 (7 May 2020), 8 pages.
    "DE_1919047.pdf": ("https://dserver.bundestag.de/btd/19/190/1919047.pdf",
                       "ff185159c6f0ff16f5bbe12c631450eadaeec5135aa416f57d405b82542f59fb"),
    # Ministerie van VWS (2021), Feitenreconstructie, tijdlijn: Persoonlijke beschermingsmiddelen,
    # januari-juli 2020 (Programmadirectie Nafase COVID-19 with NSOB; adopted 9 Apr 2021), 39 pages,
    # as published by the Eerste Kamer.
    "NL_vws_tijdlijn_pbm.pdf": ("https://www.eerstekamer.nl/overig/20230914/interactieve_tijdlijn_persoonlijke/document",
                                "237fcdb5a0288e670fed9d1d5d24bd3b0afe03179d9d3b5c6f6f887630bc125f"),
    # SOU 2021:89, Sverige under pandemin, volym 1 (Coronakommissionen, interim report), 403 pages.
    # Same sha256 as the copy Adrian supplied on 26 Oct 2026.
    "SE_sou_2021_89.pdf": ("https://regeringen.se/contentassets/e1c4a1033b9042fe96c0b2a3f453ff1d/sverige-under-pandemin-volym-1_webb-1.pdf",
                           "88646b7c4f9f58c3b33e00efac8f843cd3edf591efa342e7976a439d27b9a71b"),
    # Commission Implementing Regulation (EU) 2020/402 of 14 March 2020 (export authorisation), OJ L 77 I,
    # 15.3.2020, 7 pages. Reference-list URL https://eur-lex.europa.eu/eli/reg_impl/2020/402/oj answers with a
    # bot challenge (HTTP 202); the same act is fetched from the Publications Office repository by CELEX number.
    "EU_32020R0402.pdf": ("cellar:32020R0402",
                          "d7330ff2a6f7db3c0702bfe5d8e28b223eab38c0fdf5a7a90ccd6288aa09b2ff"),
    # Commission Implementing Decision (EU) 2020/414 of 19 March 2020 (rescEU medical stockpiling), OJ L 82 I,
    # 19.3.2020, 5 pages. Same route as above (reference-list URL https://eur-lex.europa.eu/eli/dec_impl/2020/414/oj).
    "EU_32020D0414.pdf": ("cellar:32020D0414",
                          "72b65e271343fd18b1ab21d3f6f05da05d2cff4c073974264c16619298d0aa97"),
    # F8.7 additions (outside the manuscript's reference list; allowed by Adrian 28 Oct 2026):
    # Definitive adoption (EU, Euratom) 2020/536 and 2020/537 of Amending budgets No 1 and No 2/2020, OJ L 126, 21.4.2020.
    "EU_32020B0536.pdf": ("cellar:32020B0536",
                          "64219372fe00a69d04653b7454e21299f8b69661574b870f28ae4a6c37d56d71"),
    "EU_32020B0537.pdf": ("cellar:32020B0537",
                          "d0ff837064ff768c7b30d5904cecee0a0a86fb58cb9bd888d6eb94a8a86ed5d4"),
    # SOU 2020:80, Äldreomsorgen under pandemin (Coronakommissionen, first interim report, Dec 2020), 318 pages.
    "SE_sou_2020_80.pdf": ("https://regeringen.se/contentassets/a8e708fff5e84279bf11adbd0f78fcc1/sou_2020_80_aldreomsorgen-under-pandemin.pdf",
                           "4b6bc9600443e39b4bbf2a6121b7e4ea793ec9606de60b5b29aa542b8147b16a"),
    # Bundesrechnungshof, Bericht nach § 88 Abs. 2 BHO an die Enquete-Kommission (Beschaffung, Versorgungssicherheit),
    # 12 Dec 2025, 19 pages; legal-deposit copy (ULB Bonn) of the report published on bundesrechnungshof.de.
    "DE_brh_enquete_2025.pdf": ("https://epflicht.ulb.uni-bonn.de/download/pdf/811470",
                                "cf4f6a028255f037091f952b656ab26856aa6312c9ef1a4f7c08ce213db8e1f0"),
    # BMG, Beschaffungsstab Corona, 1. Bericht über den Stand der Beschaffung von PSA, Stand 4 April 2020, 3 pages.
    "DE_bmg_beschaffungsstab_1.pdf": ("https://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/C/Coronavirus/Beschaffungsstab/1._Bericht_Beschaffungsstab_040420.pdf",
                                      "f5eb3d498af62e9c7cbbd225c955e9d67ba26244861769212a943e94fbb94f87"),
}
# European Parliament Multimedia Centre, photo record P-043686 (25 Apr 2020), URL from the manuscript's
# reference list. The page is dynamic and behind a bot challenge, so it is rendered with headless Chromium
# (Playwright) and its visible text is committed; no stable sha256 of the page exists.
EP_PHOTO_URL = ("https://multimedia.europarl.europa.eu/en/photo/coronavirus-delivery-of-medical-equipment-from-"
                "resceu-reserve-in-italyon-25-april-2020-ffp2-protecti_20200425_P043686-850895")
BE_ANNEX5_PAGES = (326, 549)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"


def fetch(name: str, url: str, sha: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / name
    if not out.exists() or hashlib.sha256(out.read_bytes()).hexdigest() != sha:
        if url.startswith("cellar:"):
            url = cellar_pdf_url(url.removeprefix("cellar:"))
        # The Chamber's site rejects bare user agents and needs its cookie: browser UA + cookie jar.
        jar = CACHE / "cookies.txt"
        subprocess.run(["curl", "-sS", "-L", "-m", "300", "-A", UA, "-c", str(jar), "-b", str(jar),
                        "-o", str(out), url], check=True)
    got = hashlib.sha256(out.read_bytes()).hexdigest()
    if got != sha:
        raise SystemExit(f"{name}: sha256 {got} != expected {sha}")
    return out


def cellar_pdf_url(celex: str) -> str:
    """English PDF of an act in the Publications Office repository. Its redirects point to http://, which this
    environment cannot resolve, so they are followed by hand over https."""
    url = f"https://publications.europa.eu/resource/celex/{celex}"
    for _ in range(5):
        head = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-D", "-", "-H", "Accept: application/pdf",
                               "-H", "Accept-Language: eng", url], capture_output=True, text=True, check=True).stdout
        loc = [ln.split(" ", 1)[1].strip() for ln in head.splitlines() if ln.lower().startswith("location:")]
        if not loc:
            return url
        url = loc[0].replace("http://", "https://", 1)
    raise SystemExit(f"{celex}: too many redirects")


def ep_photo_text(out: str) -> None:
    """Visible text of the EP photo record (title and Info block), rendered with Playwright."""
    js = (
        "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
        f"await p.goto('{EP_PHOTO_URL}',{{waitUntil:'networkidle',timeout:60000}});await p.waitForTimeout(5000);"
        "console.log('TITLE: '+await p.title());console.log(await p.innerText('body'));await b.close();})();"
    )
    body = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    lines = body.splitlines()
    title = lines[0]
    info = lines[lines.index("Info"):lines.index("Places") + 2] if "Info" in lines else []
    text = "\n".join([f"Source: {EP_PHOTO_URL}", title, *info]) + "\n"
    (ROOT / out).write_text(text, encoding="utf-8")


def full_text(pdf: Path, out: str, layout: bool = True) -> None:
    """Whole document as text with page markers (PDF page numbers), for citation by page.

    layout=False keeps reading order for two-column documents (phrases are not split across columns).
    """
    n = int(next(ln.split()[-1] for ln in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True,
                                                          check=True).stdout.splitlines() if ln.startswith("Pages:")))
    parts = []
    for p in range(1, n + 1):
        opts = ["-layout"] if layout else []
        txt = subprocess.run(["pdftotext", *opts, "-f", str(p), "-l", str(p), str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        parts.append(f"===== PDF page {p} =====\n{txt}")
    (ROOT / out).write_text("".join(parts), encoding="utf-8")


def be_annex5(pdf: Path) -> None:
    lines = []
    for p in range(BE_ANNEX5_PAGES[0], BE_ANNEX5_PAGES[1] + 1):
        txt = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
        lines.append(f"===== PDF page {p} =====\n{txt}")
    (ROOT / "data/sources/dac_ppe/BE_annex5.txt").write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    for name, (url, sha) in SOURCES.items():
        path = fetch(name, url, sha)
        print(f"{name}: sha256 ok")
    be_annex5(CACHE / "BE_55K1394002.pdf")
    print("wrote data/sources/dac_ppe/BE_annex5.txt")
    full_text(CACHE / "FR_r20-199-11.pdf", "data/sources/dac_ppe/FR_senat_r20-199-11.txt")
    full_text(CACHE / "DE_1921798.pdf", "data/sources/dac_ppe/DE_btd_19-21798.txt")
    full_text(CACHE / "DE_1919047.pdf", "data/sources/dac_ppe/DE_btd_19-19047.txt")
    full_text(CACHE / "NL_vws_tijdlijn_pbm.pdf", "data/sources/dac_ppe/NL_vws_tijdlijn_pbm.txt", layout=False)
    full_text(CACHE / "SE_sou_2021_89.pdf", "data/sources/dac_ppe/SE_sou_2021_89.txt", layout=False)
    full_text(CACHE / "EU_32020R0402.pdf", "data/sources/dac_ppe/EU_32020R0402.txt")
    full_text(CACHE / "EU_32020D0414.pdf", "data/sources/dac_ppe/EU_32020D0414.txt")
    full_text(CACHE / "EU_32020B0536.pdf", "data/sources/dac_ppe/EU_32020B0536.txt", layout=False)
    full_text(CACHE / "EU_32020B0537.pdf", "data/sources/dac_ppe/EU_32020B0537.txt", layout=False)
    full_text(CACHE / "SE_sou_2020_80.pdf", "data/sources/dac_ppe/SE_sou_2020_80.txt", layout=False)
    full_text(CACHE / "DE_brh_enquete_2025.pdf", "data/sources/dac_ppe/DE_brh_enquete_2025.txt", layout=False)
    full_text(CACHE / "DE_bmg_beschaffungsstab_1.pdf", "data/sources/dac_ppe/DE_bmg_beschaffungsstab_1.txt", layout=False)
    ep_photo_text("data/sources/dac_ppe/EU_ep_photo_P043686.txt")
    print("wrote data/sources/dac_ppe/*.txt")
