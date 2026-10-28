# EMO-Core — Emergent Mind Observatory

EMO is a research prototype for measuring how humanity responds to what it knows: how fast warnings turn into delivered action (DAC), how well collective prediction improves (τ_I and related metrics), and whether proposed remedies can be tested (RDL). It is **not** a running observatory. The only thing that runs on a schedule is a weekly GitHub Action (data refresh, analyses, tests, [public page](https://avram3scu-art.github.io/emo-core-v1/)); no dashboard or streaming pipeline has run.

Author: Adrian N. Avramescu (independent researcher, Antwerp). Plan of work: [`docs/PLAN.md`](docs/PLAN.md). Current state: [`docs/STATUS.md`](docs/STATUS.md).

## Status by pillar

Every result carries one evidence class: **[blind]** = pre-registered before its data were opened, outcome unknown; **[known history]** = pre-registered, but on cases whose outcome the author and Claude knew; **[exploratory]** = no pre-registration, descriptive. Synthetic checks of a method are not results on real data.

| Pillar | Results on real data today | Not yet working | Evidence |
|---|---|---|---|
| DAC (warning to delivered response) | Ozone vs climate: warning-to-binding-act lags of 4,642–5,006 and 6,555–6,919 days, n = 2, year-precise warning dates, secondary sources **[exploratory]** | The five-country PPE case (Belgium, France, Germany, the Netherlands, Sweden, EU) is **not in this repository**: its event files, order file and scripts were not recovered (28 Oct 2026) and must be recoded (plan F8). The DAC manuscript ("Decision or Supply?") has **not been submitted**. One coder only. | [`data/dac_ozone_events.json`](data/dac_ozone_events.json), [`data/dac_climate_events.json`](data/dac_climate_events.json), [`docs/DAC_STANDARD.md`](docs/DAC_STANDARD.md), [`analysis/dac_ozone_vs_climate.png`](analysis/dac_ozone_vs_climate.png) |
| EMO metrics (τ_I, synergy, GWI, SMF; organismality plane) | Organismality plane 1989–2025 **[exploratory]**; τ_I from NHC hurricane track errors, 3–4% a year, which restates NHC's known trend **[exploratory]**; GWI ignites on Atlantic hurricane landfalls in Wikipedia pageviews, PASS **[blind]**, decided by its significance condition only (p = 2.3e-13); its placebo condition used a non-significant result as evidence and is invalid, and its H ≥ 0.5 condition is a point threshold (`docs/GWI_PROTOCOL.md` §6 note); GWI cross-article calibration FAIL **[blind]**; SMF **[blind]**, with significance of the advantage over "no change" re-tested **[known history]** (Diebold–Mariano with Holm correction, `docs/SMF_PROTOCOL.md` §13): EIA forecasts of US energy CO2 and electricity beat "no change" significantly at 3 months (for CO2 the input fails a stationarity check, so its correlation p-value may be optimistic; §13); at 6 months they beat it in MSE, but not significantly; at 12 months they are worse. SPF unemployment forecasts beat "no change" at 1, 2 and 4 quarters (difference significant). For industrial production only the SPF at 1–2 quarters beats "no change" significantly; EIA at 3–6 months and the SPF at 4 quarters beat it in MSE, but not significantly; synergy on three climate streams FAIL **[blind]** | GWI threshold failed calibration, so a GWI level is not a measurement; synergy passes synthetic controls only; GDELT never ingested | [`docs/GWI_PROTOCOL.md`](docs/GWI_PROTOCOL.md), [`docs/GWI_CALIBRATION_PROTOCOL.md`](docs/GWI_CALIBRATION_PROTOCOL.md), [`docs/SMF_PROTOCOL.md`](docs/SMF_PROTOCOL.md) (§13: [`results/smf_dm/result.txt`](results/smf_dm/result.txt)), [`docs/SYNERGY_PROTOCOL.md`](docs/SYNERGY_PROTOCOL.md); [`analysis/`](analysis/) scripts |
| RDL (remedies) | v0.2 and v0.3 both FAIL on reserved historical cases **[known history]** (pre-registered, not blind); the forecast ledger of 5 dated forecasts, public on Zenodo, first resolution by 31 Dec 2026, is the only blind RDL test **[blind]**, not yet scored | No validated version; v0.4 waits for Oslo–Seattle or IRD data | [`docs/RDL_*`](docs/); DOI [10.5281/zenodo.23507467](https://doi.org/10.5281/zenodo.23507467) |
| UIA (interface density) | None scored. 1 of the 6 a_UIA terms measurable (I, as τ_I) | a_UIA scalar retired (session 5); UIA redefined as the He profile (I, C, F, E, D), not yet scored; He direction test needs 24 coded cases (2 exist) | [`docs/UIA_PROTOCOL.md`](docs/UIA_PROTOCOL.md), [`docs/HE_CALIBRATION_PROTOCOL.md`](docs/HE_CALIBRATION_PROTOCOL.md) |
| Continuous running | Weekly GitHub Action since 23 Oct 2026 (started each Monday by an external scheduler calling GitHub's dispatch API; GitHub's own schedule is unreliable here): refresh, analyses, tests; commits only if tests pass; rebuilds the public page | No streaming or daily ingestion; the never-run Prefect/Airflow scaffolding was deleted on 26 Oct 2026 | [`.github/workflows/weekly_refresh.yml`](.github/workflows/weekly_refresh.yml) |

Tests: 91 pass (CI run 40653907266, 28 Oct 2026, read from its annotation; CI and the weekly run report the count on every run).

DAC and UIA are reported as profiles of their components, never as a weighted score. RDL is **not** a validated recommender: its two tested versions failed on historical cases whose outcomes were known (not blind tests).

**Superseded documents.** The white papers (`WHITEPAPER_EMO_v1_*`), `deck/`, `grants/`, `README_EMO.md` and `EMOStakeholderBenefits.md` describe a live observatory, DestinE overlays, a dashboard and pipelines. None of that exists: ECMWF declined data access, and the dashboard and pipelines never ran. Each now carries a dated "superseded" banner; their "first" claims were never checked against the literature and are marked unverified. They are kept for the record and scheduled for rewrite (plan, session 15).

## What is in the repository

- `emo/` — Python package: metric functions (synergy, GWI, SMF, τ_I), the DAC event-file standard (`emo/dac_standard.py`, validator and profile), DAC lag, conversion and persistence code (`emo/metrics/dac`), and the RDL backtest (`emo/remedy`). Only code used by an analysis or the weekly run is kept; the retired a_UIA engine, the unused OI and reciprocity functions and other never-used modules were deleted on 26 Oct 2026 (git history).
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
