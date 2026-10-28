"""F12: argument rewrite of "Decision or Supply?" as tracked changes (author "Claude") on top of the F9 revision.

Base: docs/sources/dac_paper/Decision_or_Supply_manuscript_F9_revised.docx with its F9 tracked changes accepted
(done here in the XML: deletions removed, insertions kept), so the F12 changes are the only tracked changes.
Output: docs/sources/dac_paper/Decision_or_Supply_manuscript_F12_revised.docx
Every change is listed in docs/MANUSCRIPT_F12_CHANGES.md. Values: days 41-61 and the case windows from
analysis/dac_ppe_crosscase_output.txt (section 1); Canadian figures from data/sources/lit/OAG_Canada_2021_Report10.txt
(Exhibit 10.7). Usage: python scripts/manuscript_f12_edits.py <path to the docx skill's merge_runs.py>
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/sources/dac_paper/Decision_or_Supply_manuscript_F9_revised.docx"
OUT = ROOT / "docs/sources/dac_paper/Decision_or_Supply_manuscript_F12_revised.docx"
MERGE = Path(sys.argv[1]) if len(sys.argv) > 1 else None

_spec = importlib.util.spec_from_file_location("f9", ROOT / "scripts/manuscript_f9_edits.py")
f9 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f9)
f9._id[0] = 5000
tracked, cell, add_text, new_paragraph_after, nid, AUTH, run = f9.tracked, f9.cell, f9.add_text, f9.new_paragraph_after, f9.nid, f9.AUTH, f9.run


def accept_all(x: str) -> str:
    """Accept the F9 tracked changes: drop deletions, unwrap insertions, drop inserted-paragraph marks."""
    x = re.sub(r"<w:del [^>]*>.*?</w:del>", "", x, flags=re.S)
    x = re.sub(r"<w:ins [^>]*/>", "", x)
    x = re.sub(r"<w:ins [^>]*>(.*?)</w:ins>", r"\1", x, flags=re.S)
    x = x.replace("<w:rPr></w:rPr>", "")
    return x


def new_row_after(x: str, caption: str, row_key: str, texts: list[str]) -> str:
    """Insert a tracked table row, modelled on the row containing `row_key`, after it."""
    t = x.find(escape(caption))
    ts = x.find("<w:tbl>", t)
    te = x.find("</w:tbl>", ts)
    i = x.find(escape(row_key), ts)
    assert ts < i < te, f"row not found: {row_key}"
    rs = x.rfind("<w:tr>", 0, i)
    re_ = x.find("</w:tr>", i) + len("</w:tr>")
    row = x[rs:re_]
    cells = re.findall(r"<w:tc>.*?</w:tc>", row, re.S)
    assert len(cells) == len(texts), (len(cells), len(texts))
    new_cells = []
    for c, txt in zip(cells, texts, strict=True):
        ppr = re.search(r"<w:pPr>.*?</w:pPr>", c, re.S).group(0)
        tcpr = re.search(r"<w:tcPr/>|<w:tcPr>.*?</w:tcPr>", c, re.S).group(0)
        new_cells.append(f"<w:tc>{tcpr}<w:p>{ppr}<w:ins w:id=\"{nid()}\" {AUTH}>" + run("", escape(txt)) + "</w:ins></w:p></w:tc>")
    new = f'<w:tr><w:trPr><w:ins w:id="{nid()}" {AUTH}/></w:trPr>' + "".join(new_cells) + "</w:tr>"
    return x[:re_] + new + x[re_:]


def edits(x: str) -> str:
    # (1) Novelty: Section 1, Section 2.3, Table 1, references
    x = add_text(x, "but its data do not link orders to their deliveries.",
                 " In Canada, the Auditor General linked 39 federal contracts to their own first deliveries: on average, "
                 "contract signature followed the request after 34 days for N95 respirators and 28 for gowns, and first "
                 "delivery followed signature after 71 and 57 days (Auditor General of Canada, 2021, Exhibit 10.7). Averages "
                 "of this kind show where the time was spent; they cannot show whether ordering earlier would have brought "
                 "delivery earlier.")
    x = tracked(x, "None is designed to link each order to the delivery of that same order from records, which Proposition 1 requires.",
                "Only an audit has linked contracts to their own deliveries, and it reports averages (Auditor General of "
                "Canada, 2021); none uses the spread of order dates across paired orders of one good, which Proposition 1 "
                "requires.")
    T1 = "Table 1. The profile and the closest existing approaches."
    x = new_row_after(x, T1, "Audits of procurement programmes",
                      ["Audit of contracts paired with their own first delivery (Auditor General of Canada, 2021)",
                       "Contract; days from request to contract and from contract to first delivery, averaged by good",
                       "Not as a test: averages assign the time to the agency or the supplier, not to a mechanism",
                       "The test from the spread of order dates across paired orders of one good"])
    x = new_paragraph_after(x, "Ansell, C., ",
                            "Auditor General of Canada. (2021). Report 10—Securing personal protective equipment and medical "
                            "devices. Reports of the Auditor General of Canada to the Parliament of Canada, Spring 2021. "
                            "https://publications.gc.ca/collections/collection_2021/bvg-oag/FA1-27-2021-1-10-eng.pdf")
    # (2) Cross-case: abstract, Section 1, Section 4.3, Section 5, Section 8
    x = tracked(x, "Across countries, first deliveries in Belgium, Germany and the Netherlands fell within 5–11 days of one another; their first orders were 2–16 days apart under the better-supported reading of the Belgian testimony and 31–49 days apart under the others.",
                "Across countries, every import-dependent first delivery fell between days 41 and 61 after the warning, "
                "inside the surge of Chinese exports; unpaired dates cannot show whether supply set that timing.")
    x = tracked(x, "Across the five member states and the EU level, first deliveries in Belgium, Germany and the Netherlands fell within 5–11 days of one another, while their first orders were 2–16 days apart under the better-supported reading of the Belgian testimony and 31–49 days apart under the others.",
                "Across the five member states and the EU level, every import-dependent first delivery fell between days 41 "
                "and 61, inside the surge of Chinese exports, but these dates are unpaired and cannot show whether supply set "
                "them.")
    x = tracked(x, "First deliveries to a distribution level came on day 46 in Belgium, days 41–50 in Germany and days 51–52 in the Netherlands, 5–11 days apart, while their first orders were 2–16 days apart under reading B and 35–49 days apart under reading A.",
                "First deliveries to a distribution level came on day 46 in Belgium, days 41–50 in Germany, days 51–52 in the "
                "Netherlands and days 47–61 in Sweden: every import-dependent first delivery fell between days 41 and 61, "
                "inside the export surge from China (days 31–66).")
    x = tracked(x, "France’s first delivery fell on days 39–52, most plausibly from its stock, a window that does not place it before Germany’s or Belgium’s;",
                "France’s first delivery fell on days 39–52, most plausibly from its stock;")
    x = tracked(x, "The cross-case pattern, first deliveries 5–11 days apart while first orders were 31–49 days apart under the earlier readings of the Belgian testimony, is what a common supply constraint would produce; under reading B, orders (2–16 days apart) were not more dispersed than deliveries. No import-dependent first delivery can fall before day 41, when Germany’s window opens, and all fall within the export surge from China (days 31–66).",
                "Across the import-dependent countries, every first delivery fell between days 41 and 61 (none can fall "
                "before day 41, when Germany’s window opens), inside the export surge from China (days 31–66).")
    x = tracked(x, "France, the only case with a national stock and domestic manufacturers in production, delivered from day 39, although its window does not establish that it delivered first.",
                "France, the only case with a national stock and domestic manufacturers in production, delivered from day 39.")
    x = tracked(x, "Across five countries and the EU level, first deliveries in the import-dependent countries fell within days of one another, and orders were more dispersed only under some readings of the Belgian testimony; unpaired dates cannot test a supply constraint in any case.",
                "Across five countries and the EU level, every import-dependent first delivery fell between days 41 and 61, "
                "inside the surge of Chinese exports, but unpaired dates cannot test a supply constraint.")
    # (3) Rivals: abstract, Section 1, Table 4 rows 1 and 9, Section 4.2 verdict summary, Section 5, Section 6.1, Section 8
    x = tracked(x, "The record rejects a delay common to the purchasing service and bounds any such delay at five days: surgical masks ordered on 15 March arrived in 5 days, respirators ordered on 16 March in 21. It also rejects waiting for European joint procurement.",
                "The record bounds any delay common to the purchasing service at five days: surgical masks ordered on 15 "
                "March arrived in 5 days, respirators ordered on 16 March in 21; and the first Belgian order preceded the end "
                "of the first European joint procurement call.")
    x = tracked(x, "The record rejects a delay common to the purchasing service: surgical masks ordered on 15 March 2020 were delivered in 5 days and FFP2 respirators ordered the next day in 21, so any delay common to the service’s orders was at most five days. It rejects waiting for European joint procurement.",
                "The record bounds any delay common to the purchasing service: surgical masks ordered on 15 March 2020 were "
                "delivered in 5 days and FFP2 respirators ordered the next day in 21, so such a delay was at most five days. "
                "The first Belgian order preceded the end of the first European joint procurement call, so it did not wait "
                "for that call.")
    T4 = "Table 4. Candidate explanations of the Belgian delay and what the paired record shows."
    x = cell(x, T4, "1. Delay common to the purchasing service (procedure, contracting, payment)", 3,
             "Bounded: any common component is at most 5 days")
    x = cell(x, T4, "9. Waiting for EU joint procurement", 3,
             "Not supported: the pattern is absent, and the explanation was not found proposed in the sources")
    x = tracked(x, "Verdicts use five terms:", "Verdicts use six terms: bounded (the record limits the size of a component),")
    x = tracked(x, "Of the eleven explanations, two are rejected, one is not supported, two are consistent with the record, five are unidentified and one is present. The paired record therefore does what an elapsed-time measure cannot: it excludes a delay common to everything the purchasing service bought and bounds any such delay at five days, and it excludes waiting for joint procurement.",
                "Of the eleven explanations, one is bounded, two are not supported, two are consistent with the record, five "
                "are unidentified and one is present. The paired record therefore does what an elapsed-time measure cannot: "
                "it bounds any delay common to everything the purchasing service bought at five days, and it shows that the "
                "first order did not wait for joint procurement.")
    x = tracked(x, "is rejected for Belgium and the Netherlands, which ordered before that outcome, and cannot be tested for Germany and Sweden.",
                "was not found proposed in the sources; its pattern is absent in Belgium, the Netherlands and Sweden, which "
                "ordered before that outcome, and cannot be checked for Germany.")
    x = tracked(x, "The delay was not a property of the purchasing service, which converted orders of surgical masks in five days, and it was not caused by waiting for the EU.",
                "Any delay that was a property of the purchasing service was at most five days, since it converted orders of "
                "surgical masks in five, and the first order did not wait for the EU’s joint call.")
    x = tracked(x, "the test rejects a delay common to the purchasing service, which delivered surgical masks five days after ordering them, and rejects waiting for European joint procurement.",
                "the test bounds any delay common to the purchasing service at five days, the time it took to deliver surgical "
                "masks, and shows that the first order did not wait for European joint procurement.")
    # (4) Limits
    x = tracked(x, "no human has yet recoded them,",
                "the author’s check of each coded date against its source is pending, no human has recoded them,")
    x = tracked(x, "The literature search covered the approaches in Table 1 and the official reports cited; a systematic search of recent studies of emergency procurement was not made.",
                "The literature search covered official audits and reports, reviews and open procurement data found by web "
                "search; Scopus, Web of Science and Google Scholar were not searched, so peer-reviewed studies of emergency "
                "procurement may be missed.")
    # (5) Option reading to notes (Tables 3 and 5)
    T3 = "Table 3. Belgian federal orders paired with their own first delivery (days from t0)."
    x = cell(x, T3, "1", 3, "34 (reading A: 1)")
    x = cell(x, T3, "1", 5, "23 (reading A: 56)")
    x = add_text(x, "(30 June 2020, day 152) and is coded as censored. ", "Under the option reading (Section 4.1), order 1 falls on day 5 and its paired lag is 52 days. ")
    T5 = "Table 5. First firm order, first binding act and first delivery (days from t0 = 30 January 2020)."
    x = cell(x, T5, "Belgium", 2, "34 (A: 1)")
    x = cell(x, T5, "Belgium", 5, "12 (A: 45)")
    x = cell(x, T5, "Belgium", 6, "23 (A: 56); five orders 5–23")
    x = tracked(x, "Option: the third reading of the Belgian first order (Section 4.1).",
                "Under the option reading of the Belgian first order (Section 4.1), the order falls on day 5, the unpaired "
                "interval is 41 days and the paired lag 52.")
    return x


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        un = Path(tmp) / "un"
        subprocess.run(["unzip", "-q", str(SRC), "-d", str(un)], check=True)
        for p in un.rglob("*"):
            if p.is_symlink():
                p.unlink()
        doc = un / "word/document.xml"
        doc.write_text(accept_all(doc.read_text(encoding="utf-8")), encoding="utf-8")
        if MERGE:
            subprocess.run([sys.executable, str(MERGE), str(un)], check=True, capture_output=True)
        doc.write_text(edits(doc.read_text(encoding="utf-8")), encoding="utf-8")
        OUT.unlink(missing_ok=True)
        subprocess.run(["zip", "-Xqr", str(OUT), "."], cwd=un, check=True)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
