# EMO-Core — Emergent Mind Observatory

EMO is a research prototype for measuring how humanity responds to what it knows: how fast warnings turn into delivered action (DAC), how well collective prediction improves (τ_I and related metrics), and whether proposed remedies can be tested (RDL). It is **not** a running observatory. Nothing in this repository runs on a schedule yet, and no dashboard or pipeline has run.

Author: Adrian N. Avramescu (independent researcher, Antwerp). Plan of work: [`docs/PLAN.md`](docs/PLAN.md). Current state: [`docs/STATUS.md`](docs/STATUS.md).

## Status by pillar

| Pillar | Works on real data today | Not yet working | Evidence |
|---|---|---|---|
| DAC (warning to delivered response) | Ozone vs climate lags (OWID); five-country PPE profiles from parliamentary inquiries | Only one coder; only Belgium has orders paired with deliveries | JCCM manuscript under review; [`analysis/dac_ozone_vs_climate.png`](analysis/dac_ozone_vs_climate.png) |
| EMO metrics (OI, τ_I, synergy, GWI, SMF) | Organismality plane 1989–2025; τ_I from NHC hurricane track errors (3–4% a year); synergy, GWI and SMF pass noise controls | GDELT and Wikipedia attention streams never ingested; SMF and GWI not yet run on a real case | [`analysis/`](analysis/) scripts; 57 passing tests (recorded 21 Oct 2026; see note) |
| RDL (remedies) | Forecast ledger of 5 dated forecasts, public on Zenodo | v0.2 and v0.3 failed their held-out tests; v0.4 waits for Oslo–Seattle or IRD data | [`docs/RDL_*`](docs/); DOI [10.5281/zenodo.23507467](https://doi.org/10.5281/zenodo.23507467) |
| UIA (interface density) | Code exists (`emo/uia_engine`, about 450 lines) | All six weights set to 1.0; no term measured from real data; no test of what it predicts | [`emo/uia_engine/aggregate.py`](emo/uia_engine/aggregate.py) |
| Continuous running | Nothing | No scheduler deployed; Prefect and Airflow files exist but have never run | [`orchestration/`](orchestration/) |

Note on tests: `tests/` defines 82 test functions; 57 passing is the count recorded on 21 Oct 2026. The suite was not re-run in session 1 (packages could not be installed in that environment).

DAC and UIA are reported as profiles of their components, never as a weighted score. RDL is **not** a validated recommender: its two tested versions failed.

The white papers in this repository (`WHITEPAPER_EMO_v1_*`) describe a live observatory with DestinE overlays and a dashboard. That does not exist: ECMWF declined data access, and the dashboard and pipelines have not run. The same applies to `LIVE_PIPELINES.md`, `DESTINE_INTEGRATION.md` and `deck/`. These documents are scheduled for rewrite (plan, session 15).

## What is in the repository

- `emo/` — Python package: metric functions (OI, synergy, GWI, SMF, τ_I), a first-cut UIA engine (`emo/uia_engine`), DAC lag, conversion and persistence code, and RDL (`emo/remedy`).
- `api/` — FastAPI service exposing the metrics. Not deployed anywhere.
- `analysis/` — scripts that produce the real-data results above, with their outputs.
- `docs/` — DAC and RDL protocols, the forecast ledger, the plan and the status.
- `tests/` — unit and integration tests.
- `orchestration/`, `dashboard/`, `Dockerfile` — scaffolding that has never run in production.

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
