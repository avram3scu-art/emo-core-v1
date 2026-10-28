"""Fetch ECDC's first risk assessments used as the early-warning t0 (docs/DAC_T0_EARLY_WARNING.md).

PDFs are checked against sha256 and their text written to data/sources/dac_t0/ (committed).
Files already in .cache/dac_t0 are reused. Requires curl and pdftotext.
Run from the repository root: python scripts/fetch_dac_t0_sources.py
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "dac_t0"
OUT = ROOT / "data" / "sources" / "dac_t0"
ACCESSED = "2026-10-28"
PDFS = {
    # ECDC, Threat Assessment Brief: Pneumonia cases possibly associated with a novel coronavirus in Wuhan,
    # China, 9 January 2020 (3 pp.). Publication page:
    # https://www.ecdc.europa.eu/en/publications-data/pneumonia-cases-possibly-associated-novel-coronavirus-wuhan-china
    "ecdc_2020-01-09_tab_ncov": ("https://www.ecdc.europa.eu/sites/default/files/documents/Threat-assessment-Pneumonia-cases-possibly-associated-to-a-novel-coronavirus-in-Wuhan-China.pdf",
                                 "2963d5b9f1b0527f6705099ce198d559f578664d11e7691c6d3c91ab50074623"),
    # ECDC, Rapid Risk Assessment: Monkeypox multi-country outbreak, 23 May 2022 (22 pp.). Publication page:
    # https://www.ecdc.europa.eu/en/publications-data/risk-assessment-monkeypox-multi-country-outbreak
    "ecdc_2022-05-23_rra_mpox": ("https://www.ecdc.europa.eu/sites/default/files/documents/Monkeypox-multi-country-outbreak.pdf",
                                 "13ab830a04aa5aa6640ab26eedafee40dfbcbacb5eec4a68fa9bdac95cf82ea0"),
}
CACHED = {"ecdc_2020-01-09_tab_ncov": "covid_tab.pdf", "ecdc_2022-05-23_rra_mpox": "mpox_rra.pdf"}


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (url, sha) in PDFS.items():
        p = CACHE / CACHED[name]
        if not p.exists():
            subprocess.run(["curl", "-sL", "--max-time", "60", "-o", str(p), url], check=True)
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if got != sha:
            raise SystemExit(f"{name}: sha256 {got} != {sha}")
        txt = subprocess.run(["pdftotext", "-layout", str(p), "-"], check=True, capture_output=True, text=True).stdout
        (OUT / f"{name}.txt").write_text(f"Source: {url}\nAccessed: {ACCESSED}\nsha256: {sha}\n\n{txt}", encoding="utf-8")
        print(f"{name}: sha256 ok")


if __name__ == "__main__":
    main()
