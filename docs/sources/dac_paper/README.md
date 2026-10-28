# DAC paper: submissions and files (fix session F1)

Files supplied by Adrian, with origin and sha256. Session F1 (`docs/FIX_PLAN.md`).

| File | What | Origin | Supplied | sha256 |
|---|---|---|---|---|
| `FUTURES-D-26-00488.pdf` | Editorial Manager PDF (22 pages): submission sheet, cover letter, title page, manuscript "From Planetary Diagnostics to Collective Response: Diagnostic-to-Actuation Coupling as the Actuation Layer of the Emergent Mind Observatory", declarations | Adrian's Futures (Elsevier) account | 2026-10-28, attached in chat | 2527ecbdc6c726a55481830bb9fdfce33bf2a181d3a0265e6cc35907f0f24df2 |
| `Decision_or_Supply_manuscript_anonymised.docx` | Final DAC manuscript, "Decision or Supply? Testing Explanations of Delay Between a Pandemic Warning and the Delivery of Protective Equipment" (7,618 words) | Adrian's files (attached as `DAC_JCCM_manuscript_anonymised.docx`) | 2026-10-28 | d6cf44820ea22832cb7a78061cc897a5b0a4cd717e914c2a386cfd6f036ec8f1 |
| `Decision_or_Supply_supporting_information.docx` | Supporting Information, Table S1 (minimum reporting standard, with the "Identification" row) | Adrian's files | 2026-10-28 | cf21758dba1df14f3420f85a589d963239f3a968148eeb109649b40eafe69fad |
| (not copied again) | Earlier manuscript "From Warning to Delivery…", attached again; byte-identical to `docs/sources/DAC_JCCM_manuscript_anonymised.docx` | Adrian's files | 2026-10-28 | b665faab2be2aadc4057d604c16dc32e08f8c61b6f10eb5fbe0b999e3f0e5726 |
| `../other_papers/Avramescu_Diagnosticity_Condition_Manuscript.docx` | Not DAC: "The diagnosticity condition: a dilution theorem for persistence-based evidence" (separate project; attached in the same batch) | Adrian's files | 2026-10-28 | d10cd4b29b1090ef626f071a436478d70f9224bfda26d1c595acf8b5e46441fa |
| `revision_fragment_RQ_and_2.7_identification.txt` | Revision text: new research question (Section 1) and §2.7 "Identification" with Proposition 1 (M1 decision-limited vs M2 supply-limited) and proof; attached file. Section numbers (2.7, 2.8) differ from the final .docx (§2.2 Identification), so these are a later revision than `Decision_or_Supply_manuscript_anonymised.docx`; no full manuscript of that revision was supplied. | Adrian, from the drafting chat | 2026-10-28 | 351f4b84449c4e0b6f520aaa8e6557c5e8a43f5d9d8edbdfa17c9eccc7e3fef4 |
| `revision_fragment_2.8_existing_approaches.txt` | Revision text: §2.8 "Relation to existing approaches" with a new Table 1 (six approaches); pasted in chat. Section numbers (2.7, 2.8) differ from the final .docx (§2.2 Identification), so these are a later revision than `Decision_or_Supply_manuscript_anonymised.docx`; no full manuscript of that revision was supplied. | Adrian, from the drafting chat | 2026-10-28 | 00cb72c920cb6ad745f226968d17915c1a9585b1e68f0407b6f7ecbb2a0ef882 |

## Submission facts (as given by Adrian, 2026-10-28)

| Journal | Manuscript no. | Type | Submitted | Decision | Note |
|---|---|---|---|---|---|
| JCCM (Journal of Contingencies and Crisis Management) | — | — | **not submitted** (Adrian, 2026-10-28: "NO") | — | Any version. The README line "JCCM manuscript under review" is therefore false (audit 26b R2; fix in F2). |
| Futures (Elsevier) | FUTURES-D-26-00488 | Full Length Article | 2026-04-17 | 2026-04-18: desk reject ("not suitable for the journal") | Conceptual DAC paper; no case data. "Research data" link: `https://github.com/avradri/emo-core-v1` (the account the repo left on 21 Oct 2026). |

## Final DAC manuscript vs `docs/sources/DAC_JCCM_manuscript_anonymised.docx`

The attached "Decision or Supply?" is the later version (title in the file metadata; audit 26b R3). Compared by pandoc text diff, 2026-10-28 (about 1,400 changed lines; a rewrite, not an edit). Main changes: new title and abstract framed as a test of decision-limited vs supply-limited delay; new §2.2 "Identification" (separating the two needs at least two orders of the same good, each paired with its own delivery, on different dates); new Table 1 (the profile vs the closest existing approaches); Table 3 (five Belgian federal mask orders paired with deliveries); Table 4 (eleven candidate explanations tested); the five-country profiles move to Table 5; Supporting Information Table S1 adds the "Identification" row.

**Data statement (final version, §Data availability):** "The six event files, the Belgian order file and the scripts … are openly available in a public repository and archived with a persistent identifier". **Not true today:** none of these files is in this repository or any other known location. The paper was not submitted, so no letter to an editor is needed; the statement must be made true (F8 or recovered files) or changed before any submission.

## Futures paper vs the JCCM manuscripts

Different paper, not an earlier version. The Futures paper is conceptual: it defines DAC within EMO (six variables, five response modes) and proposes candidate domains, with no coded case. The JCCM manuscript is the empirical PPE case (five countries + EU). Checked by reading the PDF text (pdftotext), 2026-10-28.

Claims in it that the repository does not support today (audit 26b P1): "an operational EMO architecture" (abstract, cover letter); nothing in the repo is an operational architecture (README).

## Still missing (F1 closed with this list, 2026-10-28; Adrian: "I don't know where the files are")

- PPE event files: five countries (BE, FR, DE, NL, SE) + EU level.
- Belgian order file.
- Scripts that compute Tables 2–5 and draw Figures 1–2.
- Figures 1–2; title page of the final version; full manuscript of the later revision (only §1 RQ, §2.7 and §2.8 supplied).
- If these cannot be recovered: F8 (recode from primary sources).
