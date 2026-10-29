"""The second coder's packet holds only what docs/DOUBLE_CODING.md §2 allows, and is current."""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZIP = ROOT / "docs" / "double_coding" / "DAC_double_coding_packet_mpox.zip"


def _expected() -> dict[str, Path]:
    exp = {
        "README_protocol.md": ROOT / "docs" / "DOUBLE_CODING.md",
        "coding_sheet.csv": ROOT / "docs" / "double_coding" / "coding_sheet.csv",
        "training_answer.csv": ROOT / "docs" / "double_coding" / "training_answer.csv",
    }
    for p in (ROOT / "data" / "sources" / "dac_mpox").glob("*.txt"):
        exp[f"sources/{p.name}"] = p
    return exp


def test_packet_contents_exact_and_current() -> None:
    exp = _expected()
    with zipfile.ZipFile(ZIP) as z:
        assert sorted(z.namelist()) == sorted(exp)
        for name, src in exp.items():
            assert z.read(name) == src.read_bytes(), f"stale: {name}"


def test_packet_has_no_first_coding() -> None:
    with zipfile.ZipFile(ZIP) as z:
        blob = b"".join(z.read(n) for n in z.namelist())
    for marker in (b'"event_id": "hera_contract_1"', b"min_days", b"EU_profile.json\n"):
        assert marker not in blob
