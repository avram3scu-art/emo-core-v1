# EMO-Core — Emergent Mind Observatory

EMO is a research prototype for measuring how humanity responds to what it knows: how fast warnings turn into delivered action (DAC), how well collective prediction improves (τ_I and related metrics), and whether proposed remedies can be tested (RDL). It is **not** a running observatory. The only thing that runs on a schedule is a weekly GitHub Action (data refresh, analyses, tests, [public page](https://avram3scu-art.github.io/emo-core-v1/)); no dashboard or streaming pipeline has run.

Author: Adrian N. Avramescu (independent researcher, Antwerp). Plan of work: [`docs/PLAN.md`](docs/PLAN.md). Current state: [`docs/STATUS.md`](docs/STATUS.md).

## Status by pillar

| Pillar | Works on real data today | Not yet working | Evidence |
|---|---|---|---|
| DAC (warning to delivered response) | Ozone vs climate lags (OWID); five-country PPE profiles from parliamentary inquiries | Only one coder; only Belgium has orders paired with deliveries | JCCM manuscript under review; [`analysis/dac_ozone_vs_climate.png`](analysis/dac_ozone_vs_climate.png) |
| EMO metrics (τ_I, synergy, GWI, SMF; organismality plane) | Organismality plane 1989–2025; τ_I from NHC hurricane track errors (3–4% a year); GWI ignites on Atlantic hurricane landfalls in Wikipedia pageviews (pre-registered PASS); SMF detects forecast fidelity in EIA and SPF forecasts at 3–6 months, none for energy at 12 months (pre-registered); synergy passes synthetic controls only | GWI threshold failed cross-article calibration, so a GWI level is not a measurement; synergy found no structure beyond a surrogate null on three real climate streams (pre-registered FAIL); GDELT never ingested | [`docs/GWI_PROTOCOL.md`](docs/GWI_PROTOCOL.md), [`docs/GWI_CALIBRATION_PROTOCOL.md`](docs/GWI_CALIBRATION_PROTOCOL.md), [`docs/SMF_PROTOCOL.md`](docs/SMF_PROTOCOL.md), [`docs/SYNERGY_PROTOCOL.md`](docs/SYNERGY_PROTOCOL.md); [`analysis/`](analysis/) scripts; 57 passing tests (weekly run, 26 Oct 2026, after deleting unused code and its tests) |
| RDL (remedies) | Forecast ledger of 5 dated forecasts, public on Zenodo | v0.2 and v0.3 failed their held-out tests; v0.4 waits for Oslo–Seattle or IRD data | [`docs/RDL_*`](docs/); DOI [10.5281/zenodo.23507467](https://doi.org/10.5281/zenodo.23507467) |
| UIA (interface density) | 1 of the 6 a_UIA terms measurable (I, as τ_I) | a_UIA scalar retired (session 5); UIA redefined as the He profile (I, C, F, E, D), not yet scored; GWI may not score I (calibration failed) | [`docs/UIA_PROTOCOL.md`](docs/UIA_PROTOCOL.md) |
| Continuous running | Weekly GitHub Action since 23 Oct 2026 (started each Monday by an external scheduler calling GitHub's dispatch API; GitHub's own schedule is unreliable here): refresh, analyses, tests; commits only if tests pass; rebuilds the public page | No streaming or daily ingestion; the never-run Prefect/Airflow scaffolding was deleted on 26 Oct 2026 | [`.github/workflows/weekly_refresh.yml`](.github/workflows/weekly_refresh.yml) |

Note on tests: 102 pass in the weekly run of 23 Oct 2026 (`results/weekly/2026-10-23/pytest.txt`); the earlier figure of 57 was counted on 21 Oct 2026 before later tests were added.

DAC and UIA are reported as profiles of their components, never as a weighted score. RDL is **not** a validated recommender: its two tested versions failed.

The white papers in this repository (`WHITEPAPER_EMO_v1_*`) describe a live observatory with DestinE overlays and a dashboard. That does not exist: ECMWF declined data access, and the dashboard and pipelines have not run. The same applies to `deck/` (`LIVE_PIPELINES.md`, `DESTINE_INTEGRATION.md`, `ARCHITECTURE.md` and `README_DAC.md`, which described deleted code, were removed on 26 Oct 2026). These documents are scheduled for rewrite (plan, session 15).

## What is in the repository

- `emo/` — Python package: metric functions (synergy, GWI, SMF, τ_I), DAC lag, conversion and persistence code (`emo/metrics/dac`), and the RDL backtest (`emo/remedy`). Only code used by an analysis or the weekly run is kept; the retired a_UIA engine, the unused OI and reciprocity functions and other never-used modules were deleted on 26 Oct 2026 (git history).
- `analysis/` — scripts that produce the real-data results above, with their outputs.
- `docs/` — DAC, RDL, UIA, GWI and SMF protocols, the forecast ledger, the plan and the status.
- `tests/` — unit and integration tests.
- Deleted 26 Oct 2026 (never run, unused by any analysis; kept in git history): `api/`, `dashboard/`, `orchestration/`, `Dockerfile`, `emo/ingestion/`, `emo/twin_hooks/`, unused RDL remedy files. See `docs/AUDIT_2026-10-26.md`.

## Run it locally

Requires Python 3.11+.

```bash
git clone https://github.com/avram3scu-art/emo-core-v1.git
cd emo-core-v1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## AI disclosure

This repository was built with AI assistance. (1) All inputs were the author's own text, code and publicly available reference literature and data. (2) All AI-assisted outputs were verified by the author. (3) All scientific claims and interpretations are the author's own.

## Licence

AGPL-3.0 (see `LICENSE`); a commercial licence is described in `LICENSE-COMMERCIAL`.
