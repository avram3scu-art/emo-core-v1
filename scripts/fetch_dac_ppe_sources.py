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
}
BE_ANNEX5_PAGES = (326, 549)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"


def fetch(name: str, url: str, sha: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / name
    if not out.exists() or hashlib.sha256(out.read_bytes()).hexdigest() != sha:
        # The Chamber's site rejects bare user agents and needs its cookie: browser UA + cookie jar.
        jar = CACHE / "cookies.txt"
        subprocess.run(["curl", "-sS", "-L", "-m", "300", "-A", UA, "-c", str(jar), "-b", str(jar),
                        "-o", str(out), url], check=True)
    got = hashlib.sha256(out.read_bytes()).hexdigest()
    if got != sha:
        raise SystemExit(f"{name}: sha256 {got} != expected {sha}")
    return out


def full_text(pdf: Path, out: str) -> None:
    """Whole document as text with page markers (PDF page numbers), for citation by page."""
    n = int(next(ln.split()[-1] for ln in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True,
                                                          check=True).stdout.splitlines() if ln.startswith("Pages:")))
    parts = []
    for p in range(1, n + 1):
        txt = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), str(pdf), "-"],
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
    print("wrote data/sources/dac_ppe/FR_senat_r20-199-11.txt")
