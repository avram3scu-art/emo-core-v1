"""Build the public EMO page (static HTML) from what is in the repository.

Reads the newest results/weekly/<date>/ folder, data/MANIFEST.json, the forecast ledger
and the analysis figures, and writes site/index.html plus the figures. Nothing is
computed here: every number on the page is copied from a file in the repository, and
each section links to that file, the script that made it, its input data and the
upstream source.

Run from the repository root:  python scripts/build_site.py [--out site]
"""
import argparse
import csv
import html
import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = os.environ.get("GITHUB_REPOSITORY", "avram3scu-art/emo-core-v1")
BRANCH = os.environ.get("GITHUB_REF_NAME", "emo-2026-10")
BLOB = f"https://github.com/{REPO}/blob/{BRANCH}/"
DOI = "10.5281/zenodo.23507467"

NHC_SOURCE = "https://www.nhc.noaa.gov/verification/pdfs/1970-present_OFCL_ATL_annual_trk_errors_noTDs.pdf"

NOT_MEASURED = [
    ("Continuous observation", "Only a weekly batch run exists (this page). No stream, no dashboard, no real-time ingestion."),
    ("Attention streams", "Wikipedia pageviews are fetched only for fixed article sets used in GWI tests; GDELT has never been ingested."),
    ("UIA (interface density)", "The a_UIA scalar is retired; UIA is redefined as the He profile and is not yet scored."),
    ("GWI levels", "GWI timing passed on hurricane landfalls, but its threshold failed cross-article calibration, so no GWI level is a measurement."),
    ("Long-range self-model fidelity", "Tested for significance (section 5): EIA energy forecasts beat 'no change' only at 3 months, "
                                       "EIA industrial-production forecasts at no horizon; the SPF beats it up to 2-4 quarters."),
    ("RDL remedies", "Not a validated recommender: v0.2 and v0.3 failed their held-out tests; v0.4 waits for data. "
                     "The ledger below records forecasts only; none has resolved."),
    ("DAC beyond two cases", "Ozone vs climate only on this page; DAC event dates are hand-coded by one coder and not refreshed automatically."),
    ("Prediction outside hurricanes", "τ_I is measured on one forecasting system (NHC Atlantic track errors), not on collective prediction in general."),
]


def esc(s):
    return html.escape(str(s))


def link(path, label=None):
    return f'<a href="{BLOB}{esc(path)}">{esc(label or path)}</a>'


def ext(url, label=None):
    return f'<a href="{esc(url)}">{esc(label or url)}</a>'


def latest_run():
    runs = sorted(p for p in (ROOT / "results/weekly").iterdir() if p.is_dir())
    for p in reversed(runs):
        if (p / "status.json").exists():
            return p
    raise SystemExit("no weekly run with status.json found")


def manifest_line(man, key):
    e = man.get(key)
    if not e:
        return ""
    return (f"{link(e['path'], 'data file')} (retrieved {esc(e['downloaded_at'][:10])}, "
            f"sha256 {esc(e['sha256'][:12])}…) · source {ext(e['source'], 'upstream')}")


def provenance(items):
    return '<ul class="prov">' + "".join(f"<li>{i}</li>" for i in items if i) + "</ul>"


def build(out: Path):
    run = latest_run()
    rel = run.relative_to(ROOT).as_posix()
    status = json.loads((run / "status.json").read_text())
    man = json.loads((ROOT / "data/MANIFEST.json").read_text())
    def read(name):
        return (run / f"{name}.txt").read_text().strip() if (run / f"{name}.txt").exists() else "(no output)"
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        sha = ""
    built = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    out.mkdir(parents=True, exist_ok=True)
    for fig in ("organismality_plane.png", "dac_ozone_vs_climate.png", "information_time_nhc.png"):
        shutil.copy(ROOT / "analysis" / fig, out / fig)

    def numbers(name):
        txt = "\n".join(ln for ln in read(name).splitlines() if not ln.startswith("saved "))
        return f'<a class="out" href="{BLOB}{rel}/{name}.txt" title="open the output file">{esc(txt)}</a>'

    def figure(fname, alt):
        return f'<a href="{BLOB}analysis/{fname}"><img src="{fname}" alt="{esc(alt)}"></a>'

    rows = list(csv.DictReader(open(ROOT / "data/rdl_forecast_ledger.csv")))
    ledger_hash = (ROOT / "data/rdl_forecast_ledger.sha256").read_text().split()[0]
    lrows = "".join(
        f"<tr><td>{esc(r['forecast_id'])}</td><td>{esc(r['case'])}</td><td>{esc(r['milestone'])}</td>"
        f"<td>{esc(r['registered'])}</td><td>{esc(r['resolve_by'])}</td><td>{esc(r['p_forecast'])}</td>"
        f"<td>{' '.join(ext(u.strip(), f'[{i+1}]') for i, u in enumerate(r['status_source'].split(';')) if u.strip())}</td></tr>"
        for r in rows)

    def smf_primary(path, title):
        f = ROOT / path
        if not f.exists():
            return ""
        keep, lines, take = [], f.read_text().splitlines(), 0
        for ln in lines:
            if ln.startswith(("===", "#####")) and "Profile" not in ln:
                keep.append(ln.strip())
            elif "[PRIMARY" in ln:
                keep.append(ln.strip())
                take = 3
            elif take:
                keep.append("  " + ln.strip())
                take -= 1
        txt = title + "\n" + "\n".join(keep)
        return f'<a class="out" href="{BLOB}{esc(path)}" title="open the output file">{esc(txt)}</a>'

    dm_path = ROOT / "results/smf_dm/result.txt"
    smf_dm = (f'<a class="out" href="{BLOB}results/smf_dm/result.txt" title="open the output file">'
              f'{esc(dm_path.read_text().strip())}</a>') if dm_path.exists() else ""
    smf_blocks = "".join(smf_primary(pth, t) for pth, t in (
        ("results/smf_steo_leads/result.txt", "EIA STEO, US energy CO2 (vs EIA Monthly Energy Review)"),
        ("results/smf_steo_elec/result.txt", "EIA STEO, US electricity retail sales"),
        ("results/smf_spf/result.txt", "Survey of Professional Forecasters, US unemployment rate (vs FRED UNRATE)"),
        ("results/smf_ip/result.txt", "Industrial production: EIA STEO and SPF (vs FRED INDPRO). Pre-registered reading 'forecaster effect' is not supported by later checks; see protocol section 12."),
    ))

    result = "all checks passed" if status.get("ok") else ("tests passed; some downloads failed" if status.get("commit_allowed") else "problems found")
    nm = "".join(f"<li><b>{esc(a)}.</b> {esc(b)}</li>" for a, b in NOT_MEASURED)

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EMO weekly page</title>
<style>
:root{{--bg:#fbfaf7;--ink:#1d1d1b;--muted:#5f5e5a;--line:#dcd9d0;--acc:#1f5f8b}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161615;--ink:#ecebe6;--muted:#a7a59d;--line:#3a3935;--acc:#7fb3d9}}}}
body{{background:var(--bg);color:var(--ink);font:16px/1.55 Georgia,serif;margin:0 auto;max-width:860px;padding:24px 16px 64px}}
h1{{font-size:1.7rem;margin:.2em 0}} h2{{font-size:1.25rem;margin-top:2.2em;border-top:1px solid var(--line);padding-top:1em}}
a{{color:var(--acc)}} .meta,.prov{{color:var(--muted);font-size:.9rem}} .prov{{padding-left:1.1em}}
img{{max-width:100%;height:auto;border:1px solid var(--line);background:#fff}}
a.out{{display:block;white-space:pre;overflow-x:auto;font:13px/1.4 ui-monospace,Menlo,monospace;color:var(--ink);
  border:1px solid var(--line);padding:10px;text-decoration:none}}
table{{border-collapse:collapse;font-size:.85rem;width:100%;display:block;overflow-x:auto}}
td,th{{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}}
.warn{{border-left:3px solid #b5651d;padding-left:12px}}
</style></head><body>
<h1>Emergent Mind Observatory — weekly page</h1>
<p>Adrian N. Avramescu, independent researcher, Antwerp.</p>
<p class="meta">Built {esc(built)} from commit {ext(f'https://github.com/{REPO}/commit/{sha}', sha)} ·
latest weekly run <b>{esc(status['date'])}</b>: {esc(result)} ({link(rel + '/SUMMARY.md', 'run summary')}) ·
this page is rebuilt by {link('.github/workflows/weekly_refresh.yml', 'the weekly Action')} after each successful run, by {link('scripts/build_site.py', 'this script')}.</p>
<p>EMO is a research prototype, not a running observatory. Every number below is copied from a file in the
{ext(f'https://github.com/{REPO}', 'repository')}; click a block of numbers or a figure to open its file.</p>

<h2>What EMO does not yet measure</h2>
<ul class="warn">{nm}</ul>
<p class="meta">Status by pillar: {link('README.md', 'README')} · current state: {link('docs/STATUS.md', 'STATUS')}.</p>

<h2>1. Organismality plane, 1989–2025</h2>
<p>x: share of articles with authors from more than one country (OpenAlex, excluding papers with Chinese or Indonesian authors);
y: death rate in armed conflicts per 100,000 (UCDP via OWID), inverted. A description of humanity's path, not a test.</p>
{figure('organismality_plane.png', 'Organismality plane')}
{provenance([
    'figure ' + link('analysis/organismality_plane.png') + ' · script ' + link('analysis/organismality_plane.py'),
    'co-authorship, multi-country: ' + manifest_line(man, 'openalex_articles_multicountry_by_year_excl_CN_ID.json'),
    'co-authorship, any country: ' + manifest_line(man, 'openalex_articles_anycountry_by_year_excl_CN_ID.json'),
    'conflict deaths: ' + manifest_line(man, 'owid_ucdp_death_rate_armed_conflicts.csv'),
    'notes: ' + link('data/README_cooperation.md') + ', ' + link('data/README_owid_conflict.md'),
])}

<h2>2. Information-time τ_I from NHC hurricane track errors</h2>
<p>How fast the error of official Atlantic track forecasts falls, by lead time, 1970–2025 (τ_I as % per year, 95% CI).
The control shuffles years and should find τ_I &gt; 0 only rarely.</p>
{figure('information_time_nhc.png', 'NHC track errors and tau_I by lead time')}
{numbers('information_time_nhc')}
{provenance([
    'figure ' + link('analysis/information_time_nhc.png') + ' · script ' + link('analysis/information_time_nhc.py') + ' · metric ' + link('emo/info_time.py' if (ROOT / 'emo/info_time.py').exists() else 'emo/info_time'),
    'data file ' + link('data/nhc_atlantic_official_track_errors_1970_2025.csv') + ' (transcribed from the NHC PDF; not refreshed automatically) · notes ' + link('data/README_nhc.md'),
    'source ' + ext(NHC_SOURCE, 'NHC verification, annual official track errors'),
])}

<h2>3. DAC: ozone vs climate</h2>
<p>Years from scientific warning to a binding treaty, and the level of the target quantity after it, relative to the baseline.
DAC is reported as this profile, never as a single weighted score.</p>
{figure('dac_ozone_vs_climate.png', 'DAC ozone vs climate')}
{numbers('dac_compare_ozone_climate')}
{provenance([
    'figure ' + link('analysis/dac_ozone_vs_climate.png') + ' · script ' + link('analysis/dac_compare_ozone_climate.py'),
    'ozone-depleting substances: ' + manifest_line(man, 'owid_ozone_depleting_substance_consumption.csv'),
    'CO₂ emissions: ' + manifest_line(man, 'owid_annual_co2_emissions.csv'),
    'event dates (hand-coded, each row cites its source): ' + link('data/dac_ozone_events.csv') + ', ' + link('data/dac_climate_events.csv'),
])}

<h2>4. RDL forecast ledger</h2>
<p>Dated forecasts registered before their outcomes are known. Deposited on Zenodo:
DOI {ext('https://doi.org/' + DOI, DOI)}. Ledger SHA-256 {esc(ledger_hash[:16])}… ({link('data/rdl_forecast_ledger.sha256', 'fingerprint')}),
checked unchanged in every weekly run. These are forecasts of a failed-and-untested hypothesis, not recommendations.</p>
<table><tr><th>id</th><th>case</th><th>milestone</th><th>registered</th><th>resolve by</th><th>p</th><th>sources</th></tr>{lrows}</table>
{numbers('score_forecast_ledger')}
{provenance([
    'ledger ' + link('data/rdl_forecast_ledger.csv') + ' · scoring ' + link('analysis/score_forecast_ledger.py') + ' · protocol ' + link('docs/RDL_FORECAST_LEDGER.md'),
])}

<h2>5. Self-Model Fidelity on real forecasts</h2>
<p>Does a published forecast track what then happens? Correlation of forecast and realised changes against a circular-shift null,
plus the forecast error against a "no change" forecast. Each test was pre-registered and run once; results are fixed and checked unchanged every week.
Primary samples exclude 2020-21 except where stated.</p>
<p><b>Deciding test (protocol section 13, 28 Oct 2026; pre-registered on known history).</b> Is the advantage over "no change" larger than chance?
Diebold-Mariano with Holm correction over 15 samples. Its verdict replaces the MSE point comparison in the older blocks below:
EIA energy significant at 3 months only (for CO2 the input fails a stationarity check, so its correlation p-value may be optimistic); SPF unemployment at 1, 2 and 4 quarters; industrial production only for the SPF at 1-2 quarters.</p>
{smf_dm}
<p>Older blocks (sections 8-12; their "verdict" lines used the MSE point comparison):</p>
{smf_blocks}
{provenance([
    'protocol and results ' + link('docs/SMF_PROTOCOL.md') + ' (sections 7-13) · metric ' + link('emo/smf.py'),
    'scripts ' + link('analysis/smf_steo_leads.py') + ', ' + link('analysis/smf_steo_elec.py') + ', ' + link('analysis/smf_spf.py') + ', ' + link('analysis/smf_ip.py') + ', ' + link('analysis/smf_dm.py'),
    'sources ' + ext('https://www.eia.gov/outlooks/steo/', 'EIA Short-Term Energy Outlook archives') + ', '
    + ext('https://www.eia.gov/totalenergy/data/monthly/', 'EIA Monthly Energy Review') + ', '
    + ext('https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters', 'Survey of Professional Forecasters') + ', '
    + ext('https://fred.stlouisfed.org/', 'FRED'),
])}

<h2>Data retrieved this week</h2>
<p class="meta">All series with retrieval date, change flag and hash: {link('data/MANIFEST.json')}. Tests in this run: {esc(read('pytest').splitlines()[-1] if read('pytest') else '')}
({link(rel + '/pytest.txt', 'log')}).</p>
<p class="meta">Machine-readable copy of this page: <a href="results.json">results.json</a> (same numbers and file links; rebuilt with the page).</p>
</body></html>
"""
    (out / "index.html").write_text(page)
    (out / ".nojekyll").write_text("")
    (out / "results.json").write_text(json.dumps(
        results_json(run, rel, status, man, sha, built, rows, ledger_hash, read), indent=1) + "\n")
    return out / "index.html"


# Pre-registered tests: (name, protocol, recorded result file). Recorded files are the
# frozen records; results.json copies their text, it computes nothing.
PREREGISTERED = [
    ("gwi_hurricanes", "docs/GWI_PROTOCOL.md", "analysis/gwi_hurricanes_output.txt"),
    ("gwi_calibration", "docs/GWI_CALIBRATION_PROTOCOL.md", "analysis/gwi_calibration_output.txt"),
    ("smf_eia_co2_lead12", "docs/SMF_PROTOCOL.md", "results/smf_steo/result.txt"),
    ("smf_eia_co2_leads", "docs/SMF_PROTOCOL.md", "results/smf_steo_leads/result.txt"),
    ("smf_eia_co2_lead18", "docs/SMF_PROTOCOL.md", "results/smf_steo_h18/result.txt"),
    ("smf_eia_electricity", "docs/SMF_PROTOCOL.md", "results/smf_steo_elec/result.txt"),
    ("smf_spf_unemployment", "docs/SMF_PROTOCOL.md", "results/smf_spf/result.txt"),
    ("smf_industrial_production", "docs/SMF_PROTOCOL.md", "results/smf_ip/result.txt"),
    ("smf_significance_dm", "docs/SMF_PROTOCOL.md", "results/smf_dm/result.txt"),
    ("synergy_climate", "docs/SYNERGY_PROTOCOL.md", "results/synergy_climate/result.txt"),
]


def results_json(run, rel, status, man, sha, built, rows, ledger_hash, read):
    """Machine-readable copy of the page: the same numbers, with the same file links."""
    analyses = [n for n in ("dac_ozone", "dac_compare_ozone_climate", "organismality_plane",
                            "information_time_nhc", "score_forecast_ledger") if (run / f"{n}.txt").exists()]
    return {
        "about": "EMO public results. Copied from committed files; nothing is computed here. "
                 "Each text links to its file in the repository.",
        "built": built, "commit": sha, "repository": BLOB.rstrip("/"),
        "weekly_run": {"folder": rel, "status": status},
        "measurements": {n: {"file": f"{rel}/{n}.txt", "text": read(n)} for n in analyses},
        "preregistered_tests": [
            {"name": n, "protocol": proto, "file": f, "text": (ROOT / f).read_text().strip()}
            for n, proto, f in PREREGISTERED if (ROOT / f).exists()
        ],
        "forecast_ledger": {"file": "data/rdl_forecast_ledger.csv", "sha256": ledger_hash,
                            "doi": "10.5281/zenodo.23507467", "rows": rows},
        "data_sources": man,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="site")
    print("wrote", build(ROOT / ap.parse_args().out))
