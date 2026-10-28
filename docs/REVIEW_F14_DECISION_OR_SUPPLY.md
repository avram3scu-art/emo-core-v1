# Final editor-style review: "Decision or Supply?" (F13 version), fix session F14, 28 Oct 2026

Reviewed: `docs/sources/dac_paper/Decision_or_Supply_manuscript_F13_revised.docx` (with the F9, F12 and F13 changes), as a submission to the *Journal of Contingencies and Crisis Management* (JCCM). This is a hostile pre-submission review (Adrian's standing protocol). It makes no decision on submission.

## Preconditions checked first

- **Adrian's check of the coded dates: not in the record.** No file, record row or commit documents it. The F14 prompt assumes it was done, but F13 closed at 16:51 and this session began at 16:52. Under CLAUDE.md the repository is the only memory, so for this review the check is **not done**. It must be recorded, for example as a dated list of the rows checked and any corrections, before the declaration can stand.
- **JCCM's own pages could not be opened.** wiley.com is not reachable from this session: WebFetch refused it, and headless Chromium failed twice. Opened instead:
  - [Wiley, hybrid open access](https://authors.wiley.com/author-resources/Journal-Authors/open-access/hybrid-open-access/index.html): "Most of our subscription-based journals offer a hybrid open access option"; open access requires an article publication charge that varies by journal. This implies, but does not state, a free subscription route.
  - [Wikipedia, JCCM](https://en.wikipedia.org/wiki/Journal_of_Contingencies_and_Crisis_Management): Wiley-Blackwell, quarterly, editor W. Timothy Coombs; nothing on fees.
  - Wiley's AI guidance as reproduced in F10: AI tools are not authors; their use must be described "transparently and in detail" in the Methods; "GenAI tools must not be used to create, alter, or manipulate original research data and results".
  - **Still to do by Adrian:** open the JCCM author guidelines and check (i) whether a non-open-access route without charge exists, (ii) the journal's own AI clause, (iii) whether coding public records with an AI model counts as creating research data under it.

## F10 points: fixed or open

| # | F10 point | Status | Evidence |
|---|---|---|---|
| 1 | AI-coded data not human-verified; Wiley AI rule | **Open (blocker)** | Adrian's check not recorded (above). §7 states the check is pending (F12). The declaration still says all outputs, "including every date", were verified by the author: false today. |
| 2 | Decisive test thin; M0 and EU rival at risk of straw men | **Partly fixed** | M0 is now a bound and the EU rival "not supported" (F12, after a search of the record found neither proposed). The FFP2 test still rests on three orders and stays undecided under reading B. No second paired case. |
| 3 | Cross-case headline fails under reading B | **Fixed** | Abstract, §1, §4.3, §5 and §8 now rest on what holds under every reading (days 41–61, inside the export surge; unpaired dates cannot test it). |
| 4 | Novelty without search | **Partly fixed** | Claim narrowed to the test; Auditor General of Canada (2021) added (F11, F12). Scopus, Web of Science and Google Scholar not searched (stated in §7). |
| 5 | Proposition 1 elementary | **Accepted as is** | Labelled a proposition; the paper says it is elementary. |
| 6 | Figures missing | **Fixed** | Redrawn from the event files (F13). |
| 7 | Known history | **Fixed** | Stated in §3.1 and §7. |
| 8 | Smaller points | **Partly fixed** | Option reading moved to notes (F12). Table 5's narrow columns still wrap. |

## Declarations against the record

| Declaration statement | Record | Holds? |
|---|---|---|
| AI language models "(OpenAI ChatGPT and Anthropic Claude)" were used to draft and edit text, locate sources, extract dated events and write scripts | All six event files, the scripts and the F9–F13 text changes were made by Claude (RECORD, F8–F13). No record of ChatGPT's role in the current version. | **Partly.** Claude's role is understated: it coded all the data, not just "extracted" events. Whether ChatGPT still contributes to this version is unknown to the record; Adrian should confirm or remove it. |
| "All inputs were the author's own manuscript text, publicly available reference literature and public legal and institutional records" | Inputs: Adrian's manuscript, public reports, acts, hearings, one Moniteur copy he supplied, web sources | **Holds** |
| "All AI-assisted outputs, including every date, figure and reference, were verified by the author" | No verification recorded | **Does not hold today** |
| "All scientific claims and interpretations are the author's own" | The argument changes of F12 were drafted by Claude at Adrian's instruction; he has not yet accepted them | **Holds only after Adrian reads and accepts the F9–F13 tracked changes** |
| Manuscript §7: "coded by an AI model (Claude) … the author's check … is pending, no human has recoded them" | Matches the record | **Holds** (and must be updated when the check is done) |
| Data availability: event files and scripts openly available, to be archived with a persistent identifier | Repository public (`gh api`, 28 Oct); no DOI issued | **Holds** as worded |

## Hostile assessment

- **Significance.** The question (was the delay set by the decision or by supply?) matters for preparedness and fits JCCM. But the empirical yield is now modest by the paper's own count. Of eleven explanations, one is bounded, two are not supported, two are consistent, five are unidentified and one is present. The central question is left open. An editor may read it as a careful method with a mostly negative result, and a reviewer will ask why the Canadian contract data, which could run the test, were not used.
- **Is it an article or a note?** The method (pairing orders with their deliveries, then testing slope against the spread of order dates) fits in a few pages. Its value lies in the coding protocol and the honest demonstration of what the record cannot decide. At about 7,600 words it is long for the evidence it carries.
- **Straw men.** Reduced since F12: M0 is a bound and the EU rival is not claimed as rejected.
- **Data and coding.** One coder, an AI model, with automated phrase checks but no human recoding and no intercoder agreement. The paper says so, but a reviewer will treat it as a weakness. Wiley's rule may treat it as a policy breach unless the author's verification is complete and described in the Methods.
- **Strengths.** Unusually transparent: every date sourced to a page, contested evidence carried as readings, public code and data, limits stated plainly.

## Verdict

**Not ready to submit.** Realistic chance at JCCM if submitted today: desk rejection likely, mainly on point 1 and on thin yield. If preconditions 1–3 below are met: a fair chance of being sent to review, and in my judgement roughly a one-in-five chance of eventual acceptance after revision. This is an estimate, not data.

## Recommendation (not a decision)

**Do not submit yet.** Before any submission decision:

1. **Adrian:** check the coded dates and record the check in the repository: the rows checked, by date, and any corrections. Then update §7 and the declaration to match, including what the AI model did (coded the data) and whether ChatGPT still has a role.
2. **Adrian:** read the tracked changes of F9, F12 and F13 and accept or reject each, so the claims are his.
3. **Adrian:** open the JCCM author guidelines and record the fee route and the AI clause. If the AI clause bars AI-coded data even after verification, choose another venue.
4. **Optional but strongest:** one session to check US federal contract records (FPDS) and the Spanish audit for a second paired case (F11, b). A second case would turn the paper from "one undecided test" into a comparison.
5. Then a new review session, on a different day from any submission decision.

**Free fallback:** a Zenodo preprint of the current version, labelled with its evidence class and the pending check. It costs nothing and keeps a journal route open if the journal allows preprints; that has not been verified for JCCM.
