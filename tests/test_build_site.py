"""The public page builds, has every required section, and every repository link points to a real file."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_site  # noqa: E402


def test_site_builds_with_sections_and_valid_links(tmp_path):
    html = build_site.build(tmp_path).read_text()
    for needle in ("What EMO does not yet measure", "Organismality plane", "NHC", "ozone vs climate",
                   "forecast ledger", "10.5281/zenodo.23507467", "Self-Model Fidelity"):
        assert needle in html, needle
    for fig in ("organismality_plane.png", "dac_ozone_vs_climate.png", "information_time_nhc.png"):
        assert (tmp_path / fig).exists()
    paths = set(re.findall(r'/blob/[^/"]+/([^"]+)"', html))
    assert paths
    missing = [p for p in paths if not (ROOT / p).exists()]
    assert not missing, missing


def test_results_json_matches_committed_files(tmp_path):
    import json

    build_site.build(tmp_path)
    data = json.loads((tmp_path / "results.json").read_text())
    assert len(data["preregistered_tests"]) == len(build_site.PREREGISTERED)
    for t in data["preregistered_tests"]:
        assert (ROOT / t["file"]).read_text().strip() == t["text"]
        assert (ROOT / t["protocol"]).exists()
    assert data["forecast_ledger"]["doi"] == "10.5281/zenodo.23507467"
