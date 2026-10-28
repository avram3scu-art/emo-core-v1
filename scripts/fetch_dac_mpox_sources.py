"""Fetch the official records of the mpox case (docs/DAC_MPOX_CODING.md §4) and write their text.

Web pages: the visible text is written to data/sources/dac_mpox/<name>.txt (committed); pages carry
navigation that changes over time, so they have no stable sha256. PDFs: checked against the sha256
recorded below, text written with pdftotext. Files already in .cache/dac_mpox are reused.
Requires curl and pdftotext. Run from the repository root: python scripts/fetch_dac_mpox_sources.py
"""

from __future__ import annotations

import hashlib
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "dac_mpox"
OUT = ROOT / "data" / "sources" / "dac_mpox"
ACCESSED = "2026-10-28"

PAGES = {
    # WHO statement, 23 July 2022: second IHR Emergency Committee meeting; DG determines a PHEIC.
    "who_2022-07-23_pheic": "https://www.who.int/news/item/23-07-2022-second-meeting-of-the-international-health-regulations-(2005)-(ihr)-emergency-committee-regarding-the-multi-country-outbreak-of-monkeypox",
    # WHO statement, 11 May 2023: fifth meeting; event no longer a PHEIC.
    "who_2023-05-11_end": "https://www.who.int/news/item/11-05-2023-fifth-meeting-of-the-international-health-regulations-(2005)-(ihr)-emergency-committee-on-the-multi-country-outbreak-of-monkeypox-(mpox)",
    # European Commission press release, 14 June 2022 (Representation in Cyprus copy): HERA contract, 109 090 doses.
    "ec_2022-06-14_contract": "https://cyprus.representation.ec.europa.eu/news/hera-secures-vaccines-eu-member-states-response-monkeypox-outbreaks-2022-06-14_en",
    # European Commission press release, 28 June 2022: first delivery, 5,300 doses arriving in Spain.
    "ec_2022-06-28_delivery": "https://cyprus.representation.ec.europa.eu/news/european-health-union-start-delivery-vaccines-response-monkeypox-outbreak-2022-06-28_en",
    # European Commission news announcement, 18 July 2022: additional doses purchased.
    "ec_2022-07-18_additional": "https://cyprus.representation.ec.europa.eu/news/health-union-hera-secures-additional-vaccine-doses-response-ongoing-monkeypox-outbreak-2022-07-18_en",
    # European Commission press release, 7 September 2022 (Representation in Germany): over 170,000 further doses.
    "ec_2022-09-07_additional_de": "https://germany.representation.ec.europa.eu/news/eu-beschafft-mehr-impfstoff-gegen-affenpocken-2022-09-07_de",
    # European Commission press article, 17 November 2022 (Representation in Luxembourg): framework contract, up to 2 million doses.
    "ec_2022-11-17_framework_de": "https://luxembourg.representation.ec.europa.eu/actualites-et-evenements/actualites/europaische-gesundheitsunion-hera-sichert-bis-zu-2-millionen-dosen-des-affenpockenimpfstoffs-2022-11-17_de",
}

PDFS = {
    # Commission Implementing Decision C(2022) 5446 final of 22.7.2022 amending the Imvanex marketing
    # authorisation ("Smallpox and monkeypox vaccine"); Union Register, procedure 156674 (EMEA/H/C/002596/II/0076).
    "ec_C2022_5446_dec": ("https://ec.europa.eu/health/documents/community-register/2022/20220722156674/dec_156674_en.pdf",
                          "4c508e93d4a545c45c50c2be6f9903671362b2b4e07db789e1c620a507b95619"),
    # Annex I-III of that decision (SmPC with the monkeypox indication).
    "ec_C2022_5446_anx": ("https://ec.europa.eu/health/documents/community-register/2022/20220722156674/anx_156674_en.pdf",
                          "27661db32c82aa7a503e4ed8abd520b93b783fdaafa79b888c1eff75ac5e2eb6"),
}


def _fetch(url: str, path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        subprocess.run(["curl", "-sL", "--max-time", "60", "-o", str(path), url], check=True)


def page_text(raw: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, url in PAGES.items():
        p = CACHE / f"{name}.html"
        _fetch(url, p)
        text = page_text(p.read_text(encoding="utf-8", errors="replace"))
        if "Too Many Requests" in text[:300]:
            raise SystemExit(f"{name}: HTTP 429 page; delete {p} and retry later")
        (OUT / f"{name}.txt").write_text(f"Source: {url}\nAccessed: {ACCESSED}\nPage text (no stable sha256):\n\n{text}\n", encoding="utf-8")
        print(f"{name}: {len(text)} chars")
    for name, (url, sha) in PDFS.items():
        p = CACHE / f"{name}.pdf"
        _fetch(url, p)
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if got != sha:
            raise SystemExit(f"{name}: sha256 {got} != {sha}")
        txt = subprocess.run(["pdftotext", "-layout", str(p), "-"], check=True, capture_output=True, text=True).stdout
        (OUT / f"{name}.txt").write_text(f"Source: {url}\nAccessed: {ACCESSED}\nsha256: {sha}\n\n{txt}", encoding="utf-8")
        print(f"{name}: sha256 ok")


if __name__ == "__main__":
    main()
