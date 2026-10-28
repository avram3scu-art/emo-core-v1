# RDL forecast ledger (prospective test)

**Evidence class (added 28 Oct 2026, F6): pre-registered blind.** The outcomes were unknown when the forecasts were registered (2026-10-20) and deposited on Zenodo. This ledger is the only blind test of RDL; the backtest and v0.3 tests used historical cases with known outcomes.

The only test of RDL whose outcomes nobody knows when the forecast is made.

- Ledger: data/rdl_forecast_ledger.csv. Append-only: entries are never edited; a revised forecast gets a new id and keeps the old one.
- Fingerprint: data/rdl_forecast_ledger.sha256 (SHA-256 of the ledger at registration), plus the git commit date. A public timestamp (e.g. a Zenodo deposit) would make registration verifiable by others.
- Score: T from the RDL v0.4 indicators (docs/RDL_V04_PROTOCOL.md), coded by the author from public sources; p_forecast = T. Brier score against a constant 0.5 baseline, using analysis/score_forecast_ledger.py.
- Limits stated now: five forecasts cannot validate anything; three of five have the same T (0.25), so the ledger barely discriminates; p = T is an uncalibrated mapping; the coding is the author's judgement, with notes. The ledger becomes informative only as it grows over years.
- First resolution: F001 (IMO), by 31 Dec 2026.

## Public registration
Deposited on Zenodo on 2026-10-20: DOI 10.5281/zenodo.23507467 (version 1; ledger SHA-256 677eaf3428985802cc16b811e23584f3b73ff7a90b2474157cec39edbb803775). New forecasts and recorded outcomes are added as new versions of that record; the repository ledger and the deposit must have the same fingerprint for each version.
