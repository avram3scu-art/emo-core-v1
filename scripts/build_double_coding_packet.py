"""Build the second coder's packet for the mpox double coding (docs/DOUBLE_CODING.md §2).

Contains only the protocol, the empty coding sheet, the training answer and the
nine source texts; never Claude's event file, profiles or coding notes.
Deterministic: fixed file order and timestamps, so the zip's sha256 is stable.
"""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "double_coding" / "DAC_double_coding_packet_mpox.zip"
FILES = [
    ("README_protocol.md", ROOT / "docs" / "DOUBLE_CODING.md"),
    ("coding_sheet.csv", ROOT / "docs" / "double_coding" / "coding_sheet.csv"),
    ("training_answer.csv", ROOT / "docs" / "double_coding" / "training_answer.csv"),
] + [
    (f"sources/{p.name}", p)
    for p in sorted((ROOT / "data" / "sources" / "dac_mpox").glob("*.txt"))
]
FORBIDDEN = ("data/dac_mpox", "DAC_MPOX_CODING", "DAC_T0_EARLY_WARNING", "EU_profile")


def build() -> str:
    for _arc, src in FILES:
        if any(f in str(src) for f in FORBIDDEN):
            raise SystemExit(f"forbidden file in packet: {src}")
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, src in FILES:
            info = zipfile.ZipInfo(arc, date_time=(2026, 10, 29, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, src.read_bytes())
    return hashlib.sha256(OUT.read_bytes()).hexdigest()


if __name__ == "__main__":
    digest = build()
    print(f"{OUT.relative_to(ROOT)} files={len(FILES)} sha256={digest}")
    sys.exit(0)
