# EMO 3.0 strategy: build the mirror, let it earn its claims

29 Oct 2026, session 3.0-design. **Proposed, awaiting Adrian's yes.** Basis: Adrian's six vision documents (`docs/sources/vision/`, plan 1 in `docs/sources/plan/`), his request of 29 Oct 18:17, and the repository as it stands (`docs/STATUS.md`, `docs/PLAN.md` 2.0, `docs/REVIEW_2_14_JOSS.md`). Rules proposed with it: `docs/CLAUDE_3_0_PROPOSED.md`.

## 1. Diagnosis

1. **Adrian is right that papers had become the goal.** Phase C of plan 2.0 is a white paper, a software paper, a report and briefs. Two sessions today produced reviews that said "not yet" (`docs/REVIEW_2_13_WHITEPAPER.md`, `docs/REVIEW_2_14_JOSS.md`). The reviews were correct; making papers the next step was the error.
2. **Waiting for the tests is not a strategy either.** At current sizes H4 cannot be decided in hurricanes before about 2036 and H5 not before about 2030 (`docs/PLAN.md` §4). A plan that only waits for seasons leaves the mirror unbuilt for a decade.
3. **What is missing is the instrument the vision describes.** Today EMO is a weekly batch over historical series. There is no per-event mirror, nothing that follows a hazard as it happens, no AI pillar, and no evidence on benefit. The vision documents describe exactly these.
4. **The bottleneck for every test is n.** Hurricanes give about 2 measured storms a season. A global, all-hazard stream (earthquakes, floods, storms, with public alert, attention and activation records) gives many events a month. That single choice decides whether the "mind" claim can be tested within years rather than decades.

## 2. Strategy in one sentence

Build the mirror as running code on a high-frequency global event stream, attach the AI pillar as humanity's tested self-model, and let papers, releases and partners follow from what runs, never the other way round.

## 3. The five pillars, each tied to something that can run and something that can fail

| Pillar (Adrian's document) | What it becomes in code | What can fail | Hypothesis |
|---|---|---|---|
| 1. Credibility (plan 1) | Every claim on the public page points to a file; release DOI; failure register | claims drift from code | rules, not a test |
| 2. Mirror (*Why Humanity Needs a Mirror*) | One public loop card per hazard event: warning, attention, decision, delivery, lag so far, and the knowing→doing stage | stages not measurable from records | H3 (extended) |
| 3. Continuous running (*Why EMO Must Run Continuously*) | Daily jobs append events and update cards; the page shows last successful run | jobs fail or need hands | rules: the word "continuous" is earned by unattended running (CLAUDE 3.0) |
| 4. Benefit (*Who may benefit*) | Registered test: do faster loops go with smaller losses, beyond severity? First user pilot | no association, or no loss data | **H9 (new)** |
| 5. AI (*What if humanity is already a mind*) | The **species self-model**: before each outcome, an AI writes (a) what humanity will do and (b) what a coherent whole that knows what humanity knows would do; (a) is scored, (b) is shown beside reality | (a) no better than a non-AI baseline | **H8 (new)** |

Adrian's mirror essay already maps onto the loop: latency = DAC lags; learning = H5; alignment (promise vs budget) = SMF; consistency (parts reinforcing or opposing) = counter-measures between levels in DAC. The six stages of *What if humanity is already a mind* (warning not recognised; recognised, not transmitted; reached decision-makers, no budget; funded, fragmented; coordinated, then collapsed; learned) become the stage field of each loop card.

## 4. Where Claude pushes back

1. **"AI as a substitute for humanity's mind."** Claude recommends against this wording. Adrian's own documents say EMO "is not a control system", "doesn't decide policy", is "non-oracular", and that "a mirror doesn't tell you what to do" (*Why Humanity Needs a Mirror*; *Why EMO Must Run Continuously* §8). A substitute mind would decide for people it has no mandate from, it would be one model's view (the "one mind" risk in `docs/PLAN.md` §13), and every DAC file is already coded by one AI with no human check. What the AI can honestly be is the **self-model humanity lacks**: a model of the whole that says what the whole knows, predicts what it will do, and shows what a coherent whole would do, tested in public and never in charge. That is pillar 5 at full strength without breaking pillar 2.
2. **"EMO cuts losses" (the simulation from last year).** That simulation is not in the repository, so no session can use it (CLAUDE.md, start rule 4). If Adrian supplies it, it is committed and labelled exploratory. EMO can measure; it can cut losses only when someone acts on what it shows. The claim is earned in two steps: H9 (association, registered) and one user pilot (Phase H).
3. **"Live cognitive layer for the planet."** Possible as a direction; claimed only when true. The proposed rule defines it: a component is called continuous or live only after it has run unattended daily for 14 days and the page shows its last run.
4. **"Everyone, all institutions."** Unchanged from plan 1: institutions are reached one at a time, through a host others trust.
5. **Blindness.** Once the mirror publishes a stream, its data count as opened. Every new test on that stream (H8, H9, and the extended H3) is registered before its cards go public or uses only events after its protocol commit. The registered flood and 2027 hurricane tests are already frozen and are unaffected.
6. **AI circularity.** The AI must never score itself: outcomes come from machine-readable records (activations, declarations), never from AI-coded files, and the AI must beat a simple statistical baseline, not only a naive one, before it counts as adding anything.
7. **Cost.** Forecasts written in sessions use Adrian's weekly allowance; forecasts written by a scheduled job need a paid API key. Which one is Adrian's decision (session 3.6).

## 5. Hypotheses added (H1–H7 unchanged)

| # | Hypothesis | Fails if | Status |
|---|---|---|---|
| H8 | Self-model: AI forecasts of response outcomes, committed before the outcome, beat both a naive base rate and a simple statistical model (Brier score) | not better than the statistical model after the pre-registered number of resolved events | not built; protocol and power in 3.5 |
| H9 | Benefit: events whose loop runs faster (shorter warning → decision lag) have smaller losses than severity explains | no association at adequate power, or no usable loss data (then "cannot be tested", not FAIL) | not built; feasibility in 3.7 |

## 6. Roadmap 3.0

No phase starts on the calendar; each starts when its gate is met. Dated sessions of plan 2.0 keep their dates.

| Phase | Sessions | Gate to the next |
|---|---|---|
| A, B (plan 2.0) | 2.1–2.12b | unchanged; dated sessions run on their dates |
| **C. The mirror runs** | 3.1–3.4 | daily jobs have run unattended for 14 days; cards public |
| **D. The self-model** | 3.5–3.6 | H8 protocol registered; ≥ 10 AI forecasts committed before outcomes |
| **E. Benefit and reach** | 3.7–3.8 | H9 verdict on feasibility; one country coherence profile feasibility note |
| **F. Credibility, as by-products** | 3.9 release, 2.16 report, 2.17 briefs, JOSS (≥ 19 Apr 2027), white paper share | release DOI resolves |
| **G. Partners and money** | 2.18–2.22 | a partner's written reply |
| **H. First user pilot** | 3.10 | one institution uses one card or profile, in writing |

| # | Session | Hypothesis | Done when |
|---|---|---|---|
| 3.1 | Global event stream: data check (documentation only: alerts, attention, activations, losses; licences, latency, coverage) | H3, H6, H8 | `docs/STREAM_DATA.md` with a verdict per source; no records opened |
| 3.2 | Daily ingestion: append-only event log from the chosen sources, daily Action, manifest with checksums | infrastructure | three consecutive daily runs commit without help |
| 3.3 | Loop card protocol: fields, the six knowing→doing stages defined from records, "not yet" vs "missing", synthetic checks; registered before any card is public | H3 | protocol and tests committed; no card published |
| 3.4 | Mirror page: one card per event, stage, lag so far, last run; rebuilt daily | infrastructure | page updates on its own for 14 days (checked in a later session) |
| 3.5 | Self-model protocol (pillar 5): the two outputs, ledger format, baselines (base rate, logistic), Brier scoring, contamination and circularity rules, power from synthetic data | H8 | protocol and power committed before any forecast |
| 3.6 | Self-model ledger: first AI forecasts committed with hashes before outcomes; Adrian decides in-session vs scheduled (API cost) | H8 | ≥ 10 forecasts committed; scoring script tested on synthetic outcomes |
| 3.7 | Benefit feasibility: loss data per event (documentation only); Adrian's earlier simulation committed as exploratory if supplied | H9 | protocol registered, or the reason it cannot be tested |
| 3.8 | Coherence profile pilot design (*Who may benefit*): one country, the four mirror dimensions as a profile from public records | H3, H6 | feasibility note and coding rules, or reason |
| 3.9 | Release 1.0 (was 2.15), now including the mirror | infrastructure | release DOI resolves |
| 3.10 | First user pilot: one crisis or early-warning body, one card or profile they use | H9 | a written reply |

Plan 2.0 sessions 2.13 (white paper, shared only after Adrian's verification), 2.14 (JOSS, resubmit check after 19 Apr 2027), 2.16, 2.17 and 2.18–2.22 stay, moved behind the mirror. The dated sessions 2.8 (2027 registry, before 1 June 2027), 2.10 (after 31 Dec 2026), 2.12 (15 Nov 2027) and 2.12b (about May 2028) keep priority on their dates.

## 7. What Adrian must decide

1. Adopt this strategy and CLAUDE.md 3.0 as proposed (Claude recommends **yes**: it builds all five pillars and keeps the rules that make them believable).
2. Pillar 5 wording: "the self-model humanity lacks, tested and never in charge" instead of "a substitute for humanity's mind" (Claude recommends **yes**, for the reasons in §4.1).
3. Supply last year's loss simulation, if he has it, for session 3.7 (Claude recommends **yes**; otherwise it cannot be used).

## Sources

Opened in this session: the six documents in `docs/sources/vision/` and `docs/sources/plan/` (attached by Adrian, 29 Oct 2026), and repository files named above. No external source was opened for this strategy; every data source in §6 is checked in session 3.1 before use.

## 8. Next session prompt (3.1, after Adrian's yes)

```text
EMO session 3.1: global event stream, data check. Repository: avram3scu-art/emo-core-v1 (branch emo-2026-10). Before anything else, read CLAUDE.md (3.0), docs/STATUS.md, docs/STRATEGY_3_0.md and the entry for session 3.1 in docs/PLAN.md, and follow them. One task only this session: the one below. Hypothesis moved: none directly (data check for H3, H6, H8). Stop when its "done when" is met, or tell me plainly why it cannot be met. Pre-register any test before opening its data. Cite only sources you opened. Keep replies short; I am on a limited weekly allowance.
Session 3.1 task: choose the high-frequency global hazard stream for the mirror and the self-model. From documentation only (no event records opened), check for each candidate link: warning or alert (e.g. USGS earthquake feeds and PAGER, GDACS alerts), attention (Wikipedia pageviews), decision (Copernicus EMS rapid mapping activations, IFRC GO emergency appeals and DREF), delivery or money (OCHA FTS, IFRC appeal funding), losses (EM-DAT or others): what it records, licence and terms, access (account, key, cost), update latency, coverage, and how events can be linked across sources. Every candidate named here is unverified until opened. Keep the registered flood test (docs/FLOOD_LOOP_PROTOCOL.md §3, §10, §11) and the 2027 hurricane registry unchanged; say whether any chosen source overlaps them.
Done when: docs/STREAM_DATA.md gives a verdict per source (use, use with conditions, reject), the expected number of linked events per month, and a recommended stream; no event record opened; record, STATUS and next prompt committed.
```
