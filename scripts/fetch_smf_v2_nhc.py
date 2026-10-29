"""Fetch the 2026-season sources of the SMF v2 NHC test (docs/SMF_PROTOCOL.md §15).

Refuses before 2027-05-01 and when the NHC error file has no 2026 lines (it then prints the
count only, no values). Run from the repository root:

  python scripts/fetch_smf_v2_nhc.py HURDAT2_URL

HURDAT2_URL = the earliest HURDAT2 Atlantic file on https://www.nhc.noaa.gov/data/#hurdat that
covers 2026 (§15 rule 1); the script refuses a file without 2026 storms.
Writes data/smf_v2_nhc2026/sources/ and MANIFEST.json (URL, access time, SHA-256).
"""

from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "smf_v2_nhc2026"
SRC = OUT / "sources"
SEASON = 2026
NOT_BEFORE = dt.date(2027, 5, 1)
ERR_URL = "https://www.nhc.noaa.gov/verification/errors/1970-present_OFCL_v_BCD5_ind_ATL_TI_errors_noTDs.txt"
ADECK_URL = "https://ftp.nhc.noaa.gov/atcf/archive/{y}/aal{nn}{y}.dat.gz"
TAUS = ("24", "48", "72")


def get(url: str, tries: int = 4) -> bytes:
    r = None
    for k in range(tries):
        r = subprocess.run(["curl", "-sSfL", "-m", "300", url], capture_output=True)
        if r.returncode == 0:
            return r.stdout
        time.sleep(3 * (k + 1))
    raise RuntimeError(f"fetch failed: {url}: {r.stderr.decode()[:200] if r else ''}")


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def save(rel: str, data: bytes, manifest: dict, **kw: object) -> None:
    p = SRC / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    manifest[f"sources/{rel}"] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                                  "accessed": now(), **kw}


def main(argv: list[str]) -> int:
    if dt.date.today() < NOT_BEFORE:
        print(f"refused: the SMF v2 NHC sources may not be fetched before {NOT_BEFORE} (protocol §15)")
        return 2
    if len(argv) != 2:
        print(__doc__)
        return 2
    hurdat_url = argv[1]
    manifest: dict = {}

    err = get(ERR_URL)
    lines = err.decode("latin-1").splitlines()
    keep = [(i + 1, t) for i, t in enumerate(lines)
            if i < 11 or (len(t.split()) == 37 and t.split()[1].endswith(str(SEASON)))]
    n26 = len(keep) - min(11, len(lines))
    if n26 <= 0:
        print(f"refused: the error file has {n26} lines of {SEASON}; nothing written")
        return 3
    csv = "line,text\n" + "".join(f'{i},"{t}"\n' for i, t in keep)
    save("nhc_errors_2026.csv", csv.encode(), manifest, source=ERR_URL, full_file_lines=len(lines),
         full_file_sha256=hashlib.sha256(err).hexdigest(), note="header lines 1-11 and every 2026 line")

    hd = get(hurdat_url)
    htxt = hd.decode("latin-1").splitlines()
    start = [i for i, t in enumerate(htxt) if t[:2].isalpha() and t[4:8] == str(SEASON)]
    if not start:
        print(f"refused: {hurdat_url} has no {SEASON} storms; error file kept, nothing else written")
        return 4
    block = []
    i = start[0]
    while i < len(htxt):
        block.append(f'{i + 1},"{htxt[i]}"')
        i += 1
    save("hurdat2_2026.csv", ("line,text\n" + "\n".join(block) + "\n").encode(), manifest,
         source=hurdat_url, full_file_sha256=hashlib.sha256(hd).hexdigest(), note="every line from the 2026 season's earliest header on")

    stmids = sorted({t.split()[1] for _, t in keep[11:]})
    rows = ["stmid,line,text"]
    for s in stmids:
        url = ADECK_URL.format(y=SEASON, nn=s[2:4])
        raw = gzip.decompress(get(url)).decode("latin-1").splitlines()
        for j, t in enumerate(raw):
            p = [x.strip() for x in t.split(",")]
            if len(p) > 5 and p[4] == "OCD5" and p[5] in TAUS:
                rows.append(f'{s},{j + 1},"{t}"')
        manifest[f"adeck/{s}"] = {"source": url, "lines": len(raw), "accessed": now()}
    save("adeck_ocd5_2026.csv", ("\n".join(rows) + "\n").encode(), manifest,
         note="every OCD5 TAU 24/48/72 line of the 2026 storms' a-decks; line = line in the decompressed a-deck")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"written: {len(stmids)} storms; counts only, no values (protocol §15)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
