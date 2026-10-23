"""Weekly EMO run: refresh open data, rerun analyses, check frozen records, run tests.

Writes results/weekly/<YYYY-MM-DD>/ with:
  SUMMARY.md       what changed this week, in plain words
  status.json      machine-readable result; "ok" is false if anything failed
  data_refresh.json
  <analysis>.txt   stdout of each measurement analysis (paths normalised)
  pytest.txt       test-suite output
  *.png            only for figures whose content changed this week

Frozen records are checked, never regenerated:
  - data/rdl_forecast_ledger.csv must still match data/rdl_forecast_ledger.sha256
    (the ledger is archived on Zenodo, DOI 10.5281/zenodo.23507467)
  - the RDL backtest scripts must reproduce their recorded outputs (see REPRO)

Run from the repository root: python scripts/weekly_run.py [--skip-refresh]
"""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_BASE = ROOT / "results" / "weekly"

# Measurement analyses: rerun every week; their output is expected to move with the data.
ANALYSES = {
    "dac_ozone": [],
    "dac_compare_ozone_climate": ["analysis/dac_ozone_vs_climate.png"],
    "organismality_plane": ["analysis/organismality_plane.png"],
    "information_time_nhc": [],  # NHC data is transcribed by hand; not refreshed
    "score_forecast_ledger": [],
}

# Frozen RDL runs: (script, recorded output, line filter). Output must match exactly.
# rdl_v03_development: the code now carries the logged effect-floor rule, so it
# reproduces development run 2, whose recorded file omits the "full ranking"
# lines. Development run 1 (rdl_v03_development_output.txt) predates that rule
# and is a historical record that the current code is not expected to reproduce.
REPRO = [
    ("rdl_backtest_run", "analysis/rdl_backtest_run_output.txt", None),
    ("rdl_backtest_heldout", "analysis/rdl_backtest_heldout_output.txt", None),
    ("rdl_v03_development", "analysis/rdl_v03_development_output_run2.txt", "full ranking="),
    ("rdl_v03_heldout", "analysis/rdl_v03_heldout_output.txt", None),
]
NOT_RUN = {
    "rdl_v04_test": "needs the Oslo-Seattle / IRD component file (requested 20 Oct 2026, not received)",
}


def run(cmd: list[str], timeout: int = 900) -> tuple[int, str]:
    env = dict(os.environ, PYTHONPATH=str(ROOT), MPLBACKEND="Agg")
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=timeout)
    out = (p.stdout + (("\n[stderr]\n" + p.stderr) if p.returncode and p.stderr else ""))
    return p.returncode, out.replace(str(ROOT) + "/", "").replace(str(ROOT), ".")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def previous_dir(today: str) -> Path | None:
    if not OUT_BASE.exists():
        return None
    dirs = sorted(d for d in OUT_BASE.iterdir() if d.is_dir() and d.name < today)
    return dirs[-1] if dirs else None


def main() -> int:
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    out = OUT_BASE / today
    out.mkdir(parents=True, exist_ok=True)
    prev = previous_dir(today)
    problems: list[str] = []
    md: list[str] = [f"# EMO weekly run, {today}", ""]

    # 1. Data refresh
    md += ["## Data refresh", ""]
    if "--skip-refresh" in sys.argv:
        refresh = {"skipped": True, "sources": []}
        md.append("Skipped (--skip-refresh).")
    else:
        code, txt = run([sys.executable, "scripts/refresh_open_data.py"])
        try:
            refresh = json.loads(txt.strip().splitlines()[-1])
        except (ValueError, IndexError):
            refresh = {"error": txt[-2000:], "sources": []}
            problems.append("data refresh script crashed")
        md += ["| file | status | changed | rows |", "|---|---|---|---|"]
        for s in refresh["sources"]:
            detail = (" - " + s["detail"][:140].replace("|", "/")) if s.get("detail") else ""
            md.append(f"| {s['file']} | {s['status']}{detail} "
                      f"| {'yes' if s.get('changed') else 'no'} | {s.get('rows', '')} |")
            if s["status"] != "ok":
                problems.append(f"refresh failed: {s['file']}")
        md += ["", "Not refreshed by design (manual or hand-coded): NHC track errors, DAC event dates, forecast ledger."]
    (out / "data_refresh.json").write_text(json.dumps(refresh, indent=2) + "\n")

    # 2. Frozen forecast ledger
    md += ["", "## Frozen records", ""]
    want = (ROOT / "data/rdl_forecast_ledger.sha256").read_text().split()[0]
    have = sha(ROOT / "data/rdl_forecast_ledger.csv")
    ledger_ok = want == have
    md.append(f"- Forecast ledger sha256 {'matches' if ledger_ok else 'DOES NOT MATCH'} the archived hash ({want[:12]}…).")
    if not ledger_ok:
        problems.append("forecast ledger changed")

    # 3. Reproducibility of frozen RDL runs
    repro = {}
    for script, recorded, drop in REPRO:
        code, txt = run([sys.executable, f"analysis/{script}.py"])
        lines = [ln for ln in txt.splitlines() if not (drop and drop in ln)]
        ref = (ROOT / recorded).read_text().splitlines()
        ok = code == 0 and [ln.rstrip() for ln in lines] == [ln.rstrip() for ln in ref]
        repro[script] = ok
        md.append(f"- `{script}` {'reproduces' if ok else 'DOES NOT reproduce'} `{recorded}`.")
        if not ok:
            problems.append(f"{script} no longer reproduces {recorded}")
            (out / f"REPRO_FAIL_{script}.txt").write_text(txt)
    for script, why in NOT_RUN.items():
        md.append(f"- `{script}` not run: {why}.")

    # 4. Measurement analyses
    md += ["", "## Analyses", ""]
    before = {f: sha(ROOT / f) for figs in ANALYSES.values() for f in figs}
    analyses = {}
    for name, figs in ANALYSES.items():
        code, txt = run([sys.executable, f"analysis/{name}.py"])
        (out / f"{name}.txt").write_text(txt)
        old = (prev / f"{name}.txt").read_text() if prev and (prev / f"{name}.txt").exists() else None
        if code != 0:
            status = "FAILED"
            problems.append(f"analysis {name} failed")
        elif old is None:
            status = "first recorded run"
        elif old == txt:
            status = f"unchanged since {prev.name}"
        else:
            status = f"changed since {prev.name}"
        analyses[name] = status
        md.append(f"- `{name}`: {status}")
        if old is not None and old != txt and code == 0:
            diff = difflib.unified_diff(old.splitlines(), txt.splitlines(), prev.name, today, lineterm="", n=0)
            md += ["", "```diff", *list(diff)[:40], "```", ""]
        for f in figs:
            if sha(ROOT / f) != before[f]:
                shutil.copy2(ROOT / f, out / Path(f).name)
                md.append(f"  - figure `{f}` changed; copy kept in this folder")
    md += ["", "Note: the subtitle of `dac_ozone_vs_climate.png` states fixed percentages "
           "(ozone -99 % in 20 years, CO₂ +48 %). If `dac_compare_ozone_climate` changed, check that text."]

    # 5. Tests
    md += ["", "## Tests", ""]
    code, txt = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], timeout=1800)
    (out / "pytest.txt").write_text(txt)
    tail = [ln for ln in txt.splitlines() if ln.strip()][-1:] or ["(no output)"]
    md.append(f"- pytest: {tail[0]}")
    tests_ok = code == 0
    if not tests_ok:
        problems.append("tests failed")

    ok = not problems
    # Gate for committing: unit tests pass, frozen records hold, every analysis ran.
    # A failed download is not a gate: its committed file is kept unchanged.
    gate = tests_ok and ledger_ok and all(repro.values()) and "FAILED" not in analyses.values()
    md = md[:2] + [f"**Result: {'all checks passed' if ok else 'PROBLEMS - ' + '; '.join(problems)}**", ""] + md[2:]
    (out / "SUMMARY.md").write_text("\n".join(md) + "\n")
    status = {"date": today, "ok": ok, "commit_allowed": gate, "problems": problems, "ledger_ok": ledger_ok,
              "reproducibility": repro, "analyses": analyses, "previous": prev.name if prev else None}
    (out / "status.json").write_text(json.dumps(status, indent=2) + "\n")
    print("\n".join(md))
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as fh:
            fh.write(f"commit_allowed={'true' if gate else 'false'}\nok={'true' if ok else 'false'}\nresult_dir={out.relative_to(ROOT)}\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
