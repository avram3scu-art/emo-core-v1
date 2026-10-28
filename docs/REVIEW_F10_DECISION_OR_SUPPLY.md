# Editor-style review: "Decision or Supply?" (revised F9 version), fix session F10, 28 Oct 2026

Reviewed: `docs/sources/dac_paper/Decision_or_Supply_manuscript_F9_revised.docx` (text copy `…_F9_revised.md`), as a submission to the *Journal of Contingencies and Crisis Management* (JCCM; the target named in the original file). This is a hostile pre-submission review (Adrian's standing protocol); it judges whether a skeptical editor would send the paper out, not whether it is correct.

## Verdict

**Not ready. Major revision before any submission.** A desk rejection at JCCM is likely if it went out as it stands. The reasons: an AI-coded dataset that no human has verified (a policy problem at Wiley, point 1), a cross-case section that no longer supports its own headline (point 3), and a thin empirical base for the one decisive test (point 2). If points 1–5 below are fixed, the paper is a credible JCCM submission. In my judgement it would then have a fair chance of review and a modest-to-fair chance of acceptance. These are estimates, not data.

## Points, most serious first

1. **Data integrity and the publisher's AI policy (blocker).** Wiley's guidance states that "GenAI tools must not be used to create, alter, or manipulate original research data and results", and that AI use must be described in detail ([Wiley AI Guidelines, as reproduced](https://the-hospitalist.org/wp-content/uploads/2025/04/Wiley-AI-Guidelines.pdf), opened 28 Oct 2026; JCCM's own author page could not be opened from here). All six event files were coded by an AI model (Claude). The safeguards so far are automatic checks that every cited phrase stands on its cited page; no human has recoded or verified them. The declaration says "All AI-assisted outputs, including every date … were verified by the author", which is not yet true. **Needed:** Adrian (or a second human coder) checks every coded date against its source, at minimum the Belgian order file and the first-order and first-delivery rows of each case (about 40 rows). The manuscript then states who coded and who verified. Until then the paper cannot be submitted honestly to a Wiley journal.
2. **The decisive test rests on three orders and does not decide.** The paper's central question (decision- or supply-limited FFP2 delay) is left open under the reading it calls better-supported. Its two firm results are narrow:
   - **M0 (a delay common to the purchasing service) is rejected by one contrast:** a surgical order of 15 March (5 days) against an FFP2 order of 16 March (21 days). Different goods from different suppliers, so a reviewer will say that M0 was never a serious rival: a straw-man risk. The paper should cite where M0 was actually proposed (inquiry testimony blaming procedure, for example), or present the result as a bound ("at most five days") rather than a rejection.
   - **"Waiting for EU joint procurement" is rejected:** the paper should show that this explanation was actually put forward in the Belgian or EU debate.
3. **The cross-case section no longer supports its headline (forced by the new files; see `docs/MANUSCRIPT_F9_CHANGES.md`).** Under reading B, first orders (2–16 days apart) are not more dispersed than first deliveries (5–11). France is not shown to have delivered first. The Spearman correlation no longer reaches +1.00. The abstract, §1, §5 and §8 still frame the cross-case result as convergence of deliveries. **Needed:** reframe it to what holds under every reading: all import-dependent first deliveries fall in days 41–61, inside China's export surge; first deliveries cannot be ordered by first orders; and the cross-case data cannot test a supply constraint (Proposition 1 iii). Or cut the cross-case section to Table 5 and two sentences. Either way the paper becomes a Belgian test with a descriptive comparison, which is what the evidence carries.
4. **Novelty and literature.** The paper claims that no existing approach links each order to the delivery of that same order (Table 1), but §7 admits that emergency procurement studies were not searched systematically. One search on 28 Oct found order-level public procurement records in other countries, for example [Canada's PSPC briefing on purchases and expected delivery](https://www.canada.ca/en/public-services-procurement/corporate/transparency/briefing-materials/standing-committee-government-operations-estimates/2020-06-09/overview-public-services-procurement-canada-purchases-expected-delivery-critical-items.html) and [documents produced to the House of Commons](https://ourcommons.azureedge.net/data/Motion2020-10-26/2021-02-05-SPDP-8550-432-1-03/HESA_PSPC-M-SPAC-M_0001875_E.pdf), plus press analyses of US federal order dates ([AP, via Daily Kos](https://www.dailykos.com/stories/2020/4/5/1934587/-AP-Trump-administrated-waited-until-mid-March-to-order-bulk-pandemic-supplies)). A reviewer may ask why Belgium's five orders and not those larger records. **Needed:** a systematic search before submission (operations-management studies of PPE lead times; public-procurement audits). Either name these records as the next test, or use one of them as a second paired case, which would also answer point 2.
5. **Proposition 1 is elementary,** and the paper says so. It is correctly labelled a proposition, not a theorem. Keep it short; reviewers will accept it as a framing device, not as the contribution.
6. **Figures 1–2 do not exist** in any recoverable form. They must be redrawn from the new files.
7. **Known history.** The coding was done with the Belgian result known. The revised §3.1 and §7 state this. Keep it; it is a strength to state, not a weakness to hide.
8. **Smaller points:**
   - Table 5's long cells wrap badly.
   - "Option reading" adds complexity. If point 3 shortens the cross-case section, the option reading can move to a note.
   - Name the end point "first verified delivery" consistently.

## Venue

- **JCCM: good topical fit.** Crisis management, the warning–response gap, the Boin and Rhinard line of work. Fees and the journal's own AI policy could not be opened from this session (wiley.com is not reachable here). **Adrian should check the author-guidelines page** for an article charge on the non-open-access route and for the AI disclosure rules before submitting. Futures is closed (desk-rejected, April 2026).
- **Alternatives**, only if JCCM declines (fees and policies not checked): *Risk, Hazards & Crisis in Public Policy*; *Policy Sciences*; *Journal of European Public Policy* (EU warning paradox).
- **Fallback:** Zenodo preprint (free), as with earlier papers.

## Recommended order of work

1. Done in F10: the false F9 sentence "coded by one person" is corrected to "an AI model (Claude) … no human has yet recoded them" (§3.1 and §7).
2. **Adrian verifies the key rows.** Claude prepares a checklist with every coded date, its quoted phrase and the page of the source PDF, so that checking takes about 1–2 hours of reading, not coding.
3. **Literature search session:** emergency procurement, PPE lead times, order-level public records.
4. **Rewrite session:** abstract, §1, §5 and §8 around what holds under every reading (point 3); M0 and EU framing (point 2).
5. **Figures**, then a final hostile review with a submit / don't-submit verdict. Never on the same day as the decision to submit.
