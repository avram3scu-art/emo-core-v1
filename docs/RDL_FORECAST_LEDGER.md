# RDL forecast ledger (prospective test)

The only test of RDL whose outcomes nobody knows when the forecast is made.

- Ledger: data/rdl_forecast_ledger.csv. Append-only: entries are never edited; a revised forecast gets a new id and keeps the old one.
- Fingerprint: data/rdl_forecast_ledger.sha256 (SHA-256 of the ledger at registration), plus the git commit date. A public timestamp (e.g. a Zenodo deposit) would make registration verifiable by others.
- Score: T from the RDL v0.4 indicators (docs/RDL_V04_PROTOCOL.md), coded by the author from public sources; p_forecast = T. Brier score against a constant 0.5 baseline, using analysis/score_forecast_ledger.py.
- Limits stated now: five forecasts cannot validate anything; three of five have the same T (0.25), so the ledger barely discriminates; p = T is an uncalibrated mapping; the coding is the author's judgement, with notes. The ledger becomes informative only as it grows over years.
- First resolution: F001 (IMO), by 31 Dec 2026.
