"""F12: fetch the literature sources the manuscript cites from the F11 search, check sha256, write their text.

Auditor General of Canada (2021), Report 10: the publications.gc.ca link first serves an archive notice
page; a second request with the cookie it sets and wbdisable=true returns the PDF. Requires curl and pdftotext.
Run from the repository root: python scripts/fetch_lit_sources.py
"""

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "lit"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
SOURCES = {
    "OAG_Canada_2021_Report10.pdf": ("https://publications.gc.ca/collections/collection_2021/bvg-oag/FA1-27-2021-1-10-eng.pdf?wbdisable=true",
                                     "8720d449151899fdc40510663e8c3ef290536f77f0afe992178a8034fdf9e632"),
}


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    jar = CACHE / "cookies.txt"
    for name, (url, sha) in SOURCES.items():
        out = CACHE / name
        for _ in range(3):  # first request may return the archive notice and set a cookie
            if out.exists() and hashlib.sha256(out.read_bytes()).hexdigest() == sha:
                break
            subprocess.run(["curl", "-sSL", "-m", "120", "-A", UA, "-c", str(jar), "-b", str(jar), "-e", url.split("?")[0],
                            "-o", str(out), url], check=True)
        got = hashlib.sha256(out.read_bytes()).hexdigest()
        if got != sha:
            raise SystemExit(f"{name}: sha256 {got} != {sha}")
        txt = ROOT / "data/sources/lit" / name.replace(".pdf", ".txt")
        subprocess.run(["pdftotext", "-layout", str(out), str(txt)], check=True)
        print(f"{name}: sha256 ok; wrote {txt.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
