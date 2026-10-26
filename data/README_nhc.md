# NHC Atlantic official track forecast errors, 1970–2025

File: `nhc_atlantic_official_track_errors_1970_2025.csv`
Columns: `year`, `lead_h` (forecast lead time, hours), `error_nmi` (annual mean track error, nautical miles), `n_forecasts`.

Source: National Hurricane Center, "Average NHC Atlantic Track Forecast Errors (n mi), Tropical Storms and Hurricanes",
https://www.nhc.noaa.gov/verification/pdfs/1970-present_OFCL_ATL_annual_trk_errors_noTDs.pdf
(verification based on the NHC best track database as of 5/12/26; homogeneous with best-track CLIPER5; includes subtropical storms).
Transcribed by machine from the PDF text layer (pdftotext -layout); row counts and spot values checked against the PDF.
Full check 2026-10-26: all 368 cells match the PDF text (one-off job `nhc-pdf`, run 40292776083; text and PDF SHA-256 in `results/nhc_check/`); `tests/test_nhc_transcription.py` keeps it checked.

Coverage notes from NHC: 36-h forecasts began in 1988; 96-h and 120-h forecasts began in 2001.
Public domain (US federal government work).

Note: `ecmwf_headline_scores.csv` in this folder has no documented source and should not be used as real data.
