# Record of every test, simulation, probe, run and attempt

One row per item, added in the session it happens (CLAUDE.md, "Recording"). Failures stay.
Rows start at session 9 (26 Oct 2026). Sessions 1–8 are recorded in `docs/STATUS.md`, `docs/SESSION_LOG.md` and the protocol files (`docs/SMF_PROTOCOL.md`, `docs/SYNERGY_PROTOCOL.md`, `docs/RDL_*`); they have not yet been indexed here.

| Date | Session | Type | What | Protocol | Code | Data | Result | Commit / run |
|---|---|---|---|---|---|---|---|---|
| 2026-10-26 | 9 | check | Start step 3: latest weekly run | CLAUDE.md step 3 | `weekly_refresh.yml` | — | success, under 7 days old; not restarted | run 40330816177 |
| 2026-10-26 | 9 | attempt | Install pytest/ruff/mypy in Claude's workspace | — | pip | — | error: no package index reachable (pypi.org does not resolve; also failed through the proxy); all tests run in CI instead | — |
| 2026-10-26 | 9 | unit tests | DAC standard validator and profile, first push | `docs/DAC_STANDARD.md` | `emo/dac_standard.py`, `tests/dac_unit/test_dac_standard.py` | synthetic (`docs/dac_event_file_example.json`) | FAIL at mypy (pytest passed) | a89d48b / 40333436686 |
| 2026-10-26 | 9 | unit tests | mypy fix, guessed (log not readable) | same | same | same | FAIL at mypy | 5cb8932 / 40333679297 |
| 2026-10-26 | 9 | unit tests | mypy fix, second guess | same | same | same | FAIL at mypy | b2313e7 / 40333876702 |
| 2026-10-26 | 9 | CI change | mypy errors as annotations | — | `.github/workflows/ci.yml` | — | FAIL at mypy; error now visible (`dict.get` arg-type) | 5a5ca46 / 40333991062 |
| 2026-10-26 | 9 | unit tests | mypy arg-type fix | same | same | same | FAIL at ruff (not visible) | 9fcf1ef / 40334170890 |
| 2026-10-26 | 9 | CI change | ruff errors as annotations | — | `.github/workflows/ci.yml` | — | FAIL; visible: B905 `zip` without `strict` | 8bdde1a / 40334306373 |
| 2026-10-26 | 9 | unit tests | B905 fix | same | same | same | PASS (pytest incl. malformed-file and per-rule rejections, mypy, ruff); test count not readable | 3494540 / 40334445714 |
| 2026-10-26 | 9 | pre-registration | Ozone/climate conversion check | `docs/DAC_STANDARD.md` §5 | — | — | committed before conversion | a4de996 / 40334984122 |
| 2026-10-26 | 9 | reproduction check | Ozone and climate CSVs converted to the standard; lag ranges vs comparison-script lags | `docs/DAC_STANDARD.md` §5 | `scripts/convert_dac_csv.py` | `data/dac_{ozone,climate}_events.csv` → `.json` | PASS: 4,828 d ∈ [4,642; 5,006]; 6,712 d ∈ [6,555; 6,919] | c70276e / 40335072462 |
| 2026-10-26 | 9 | attempt | Locate the PPE event files (JCCM case) | — | `add_repo avram3scu-art/dac-eu-covid` | — | not found: files existed only in a past chat's workspace; not in any repo | — |
| 2026-10-26 | 9 | source | DAC manuscript supplied by Adrian (docx, anonymised; adds Belgian paired-order Table 3 and Figure 2; Table 4 = reporting standard, rows identical to the copied table) | — | pandoc | `docs/sources/DAC_JCCM_manuscript_anonymised.{docx,md}` | committed; latest version not confirmed by Adrian | this commit |
| 2026-10-26 | 9 | search | Public copy of the six PPE event files named in the manuscript's data statement | — | WebSearch: (1) Avramescu DAC event files PPE COVID-19 … zenodo; (2) github avram3scu-art dac | — | not found | — |
| 2026-10-26 | 9 | check | 15 attachments from Adrian checked by sha256 against the repo; PDFs identified from first pages | — | sha256sum, pdfinfo, pdftotext | `docs/sources/SOURCES_SUPPLIED.md` | 6 CSV/ledger files identical to repo copies; NHC PDF = session-8 checksum; 7 PDFs new (BE, FR, SE, DE ×2 sources for the PPE case; 2 Phil Trans B papers); no event files among them | this commit |
