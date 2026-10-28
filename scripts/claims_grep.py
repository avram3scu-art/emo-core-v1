"""F2: list every hit of claim words in the repository with its justification.

Words: live, real-time, realtime, deployed, operational, validated, ready, first.
Every hit gets one justification; a hit with none is printed as UNJUSTIFIED and the
script exits 1. Writes docs/F2_CLAIMS_GREP.md. Run from the repository root.
Excluded paths (data, results, supplied sources, recorded outputs) hold no claims by Claude.
"""

import re
import subprocess
import sys
from pathlib import Path

WORDS = r"\b(live|real-time|realtime|deployed|operational|validated|ready|first)\b"
EXCLUDE = [":!data", ":!results", ":!docs/sources", ":!analysis/*output*", ":!docs/F2_CLAIMS_GREP.md", ":!scripts/claims_grep.py"]

SUPERSEDED = ("WHITEPAPER_EMO_v1_", "deck/", "grants/", "README_EMO.md", "EMOStakeholderBenefits.md")
RECORDS = ("docs/STATUS.md", "docs/STATUS_ARCHIVE.md", "docs/RECORD.md", "docs/SESSION_LOG.md", "docs/SESSION_LOG_ARCHIVE.md", "docs/AUDIT_", "docs/FIX_PLAN.md",
           "docs/PLAN.md", "CLAUDE.md", "docs/archive/", "scripts/f3_backfill_record.py")
ORDINAL = re.compile(
    r"\bfirst[ _-]?(order|deliver|binding|signed|resolution|run|wave|week|meeting|mention|row|line|act|legally|budget|"
    r"date|event|recorded|declaration|alert|time|of |national|sample|two|three|half|step|reading|valid|fetch|amendment|"
    r"audit|readable|year|month|day|pass|attempt|value|column|element|key|edition|lead|appearance|case|occurrence|"
    r"forecast|test|non|t0|warning|purchase|firm|resulting|major|funding|physical|permanent|interim|round|report|procurement|French|Belgian|European|request|serves|sublayer|stage|landfall|error|task|simulation|full|such|collection|proposal|diagnos|treaty|"
    r"formal|ranked|synthetic|50|12|\(|\]|\)|=|\.|,|:|\"|$)", re.I)

# Remaining hits, judged one by one (file, word or phrase in the line) -> justification.
MANUAL = [
    ("README.md", "validated recommender", "negation: RDL is not a validated recommender"),
    ("README.md", "live observatory", "states that the superseded documents' live observatory does not exist"),
    ("README.md", "[blind]", "definition of the evidence class"),
    ("analysis/dac_ozone.py", "validated warnings", "DAC term: t0 is a validated warning (docs/DAC_STANDARD.md)"),
    ("docs/archive/DAC_METRICS.md", "validated diagnostics", "DAC term: t0 is a validated warning"),
    ("docs/DAC_STANDARD.md", "validates first", "describes the code: compute_profile calls the validator"),
    ("emo/info_time.py", "Validated gain", "defined in the same docstring as the lower 95% bound of the slope"),
    ("emo/remedy/intervention_library.py", "", "text of hypothetical remedy options (RDL library), not a claim about EMO"),
    ("emo/remedy/portfolio_builder.py", "first", "ordering of a rule (repair upstream first)"),
    ("emo/remedy/scoring.py", "first", "ordering of a rule"),
    ("emo/gwi.py", "first", "instruction: remove known common drivers first"),
    ("emo/dac_standard.py", "first", "variable name (first event)"),
    ("docs/RDL_V0_1.md", "first-class", "idiom for a built-in component; the status section is corrected (28 Oct)"),
    ("docs/RDL_V0_1.md", "not operational", "correction: RDL v0.1 is not operational"),
    ("docs/RDL_V03_PROTOCOL.md", "validated recommender", "negation: RDL is not a validated recommender"),
    ("docs/RDL_BACKTEST_INPUTS.md", "first", "ordering: rules first, then values"),
    ("docs/RDL_BACKTEST_PROTOCOL.md", "first ranked", "history: what the engine first did"),
    ("docs/UIA_PROTOCOL.md", "calibration first", "rule: calibration before scoring"),
    ("scripts/build_site.py", "real-time", "negation (no real-time ingestion) or a source's own name (Philadelphia Fed Real-Time Data Research)"),
    ("scripts/build_site.py", "validated recommender", "negation: not a validated recommender"),
    (".github/workflows/ci.yml", "first error line", "ordinal"),
    ("analysis/gwi_hurricanes.py", "first", "variable name / rule: first landfall per storm"),
    ("analysis/test_the_test/", "first", "ordinal in supplied text (first task, first simulation, first 12 hex digits)"),
    ("analysis/audit_2026-10-27/", "", "probe code: ordinal / variable names"),
    ("docs/dac_event_file_example.json", "", "synthetic example field values (first order, first delivery)"),
    ("scripts/convert_dac_csv.py", "", "coding rules: first treaty, first diagnostic event"),
    ("docs/RELATED_WORK.md", "first collection", "ordinal"),
    ("docs/SYNERGY_PROTOCOL.md", "first full year", "ordinal"),
    ("docs/HE_CALIBRATION_PROTOCOL.md", "first 50 lines", "ordinal"),
    ("docs/GWI_PROTOCOL.md", "first such record", "ordinal"),
    ("docs/RDL_V04_PROTOCOL.md", "two first", "ordinal"),
    ("docs/DAC_PPE_CODING.md", "validated", "means: passed by the validator emo/dac_standard.py"),
    ("scripts/dac_ppe_outputs.py", "validated", "means: passed by the validator emo/dac_standard.py"),
    ("scripts/weekly_run.py", "", "code comment or ordinal"),
    ("analysis/dac_ppe_figures.py", "validated", "means: passed the dataviz skill's palette validator"),
    ("scripts/manuscript_f13_edits.py", "first", "ordinal in quoted manuscript text (first tender, first order)"),
    ("docs/MANUSCRIPT_F13_CHANGES.md", "validated", "means: passed validate.py or the dataviz palette validator"),
    ("docs/MANUSCRIPT_F12_CHANGES.md", "validated", "means: passed the docx skill's validate.py (schema, every edit tracked)"),
    ("docs/REVIEW_F14_DECISION_OR_SUPPLY.md", "", "review of a manuscript: verdict 'not ready', quoted declarations, ordinals"),
    ("docs/REVIEW_F10_DECISION_OR_SUPPLY.md", "not ready", "negation: verdict that the manuscript is not ready"),
    ("docs/REVIEW_F10_DECISION_OR_SUPPLY.md", "first verified delivery", "DAC term for the delivery end point (manuscript §2.1)"),
]


def justify(path: str, line: str) -> str:
    if path.startswith(SUPERSEDED):
        return "superseded document: dated banner at top (28 Oct 2026); its 'first' claims marked [unverified]"
    if path.startswith(RECORDS):
        return "internal record or plan: quotes, negates, dates or plans; not a claim about the current system"
    words = {w.lower() for w in re.findall(WORDS, line, re.I)}
    if words == {"first"} and ORDINAL.search(line):
        return "ordinal 'first' (first event, order, run, ...), not a novelty claim"
    for f, needle, why in MANUAL:
        if path.startswith(f) and needle.lower() in line.lower():
            return why
    return "UNJUSTIFIED"


def main() -> int:
    out = subprocess.run(["git", "grep", "--untracked", "-I", "-i", "-n", "-E", WORDS, "--", ".", *EXCLUDE],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    rows, bad = [], 0
    for hit in out:
        path, num, line = hit.split(":", 2)
        why = justify(path, line)
        bad += why == "UNJUSTIFIED"
        text = line.strip()[:110].replace("|", "/")
        rows.append(f"| `{path}:{num}` | {text} | {why} |")
    md = ["# F2: claim-word grep (live / real-time / deployed / operational / validated / ready / first)", "",
          f"Generated by `scripts/claims_grep.py`. Hits: {len(rows)}. Unjustified: {bad}.", "",
          "| Where | Text (first 110 characters) | Justification |", "|---|---|---|", *rows, ""]
    Path("docs/F2_CLAIMS_GREP.md").write_text("\n".join(md))
    print(f"hits={len(rows)} unjustified={bad}")
    for r in rows:
        if r.endswith("| UNJUSTIFIED |"):
            print(r)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
