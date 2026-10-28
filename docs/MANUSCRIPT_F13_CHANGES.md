# Manuscript "Decision or Supply?": figures (fix session F13, 28 Oct 2026)

- **Base:** `docs/sources/dac_paper/Decision_or_Supply_manuscript_F12_revised.docx` with its F12 tracked changes accepted (in the XML).
- **Output, with F13 tracked changes only (author "Claude"):** `docs/sources/dac_paper/Decision_or_Supply_manuscript_F13_revised.docx`
- **Made by:** `scripts/manuscript_f13_edits.py`
- **Validated:** against the accepted base; schema checks pass and every edit is tracked. Rendered pages 9 and 13 checked.

**Figures:** `analysis/dac_ppe_figures.py` → `analysis/figures/dac_ppe_fig1.{png,pdf}`, `dac_ppe_fig2.{png,pdf}`.

- **Data:** the six event files and their profiles (emo/dac_standard.py) only.
- **China events:** `data/dac_ppe/china_supply_events.json`, each with a verbatim phrase from its source, checked by `tests/test_dac_ppe_figures.py` against `data/sources/lit/China_{nhc,yicai,mofcom}.txt`. Those texts come from the manuscript's cited URLs, opened 28 Oct 2026; MOFCOM was rendered with headless Chromium.
- **Palette:** the dataviz skill's validated categorical slots 1–3 (validator: all checks pass; aqua below 3:1 contrast, relieved by marker shape and the legend).
- **Greyscale:** shape carries identity (square = order, triangle = binding act, circle = delivery).

| # | Where | Before | After | Reason | Source |
|---|---|---|---|---|---|
| 1 | Figure 1 | "[Figure 1 about here]" (no figure existed) | the image | figures not recovered (F1); redrawn | `analysis/dac_ppe_figures.py`; BE.json |
| 2 | Figure 2 | "[Figure 2 about here]" | the image | as #1 | all six event files; china_supply_events.json |
| 3 | Figure 1 legend | readings A and B; "the dashed line marks China's export controls" | filled = reading B, open = reading A and the option reading; dashed lines = output of 116 million (29 Feb) and export checks from 1 April | matches the drawn figure (third reading; two dated China events) | BE.json; China sources |
| 4 | Figure 2 legend | "the open circle with an arrow marks a lower bound" | marker shapes; open symbols and thin bars = alternative readings (BE, FR, DE); no lower bound (none in the new files) | matches the drawn figure | profiles |
| 5 | Data availability | "Figures 1 and 2 are to be redrawn from these files" | the scripts "draw Figures 1 and 2" | now true (`analysis/dac_ppe_figures.py`) | — |
