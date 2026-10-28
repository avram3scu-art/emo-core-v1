"""F9: data-only revision of "Decision or Supply?" as tracked changes (author "Claude"), from the six PPE event files.

Input:  docs/sources/dac_paper/Decision_or_Supply_manuscript_anonymised.docx (unchanged original)
Output: docs/sources/dac_paper/Decision_or_Supply_manuscript_F9_revised.docx
Every value inserted here comes from data/dac_ppe/*_profile.json or analysis/dac_ppe_crosscase_output.txt;
docs/MANUSCRIPT_F9_CHANGES.md lists each change with its source. Requires the docx skill's merge_runs.py
(path in MERGE below) only to coalesce runs; no other dependency. Run from the repository root.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/sources/dac_paper/Decision_or_Supply_manuscript_anonymised.docx"
OUT = ROOT / "docs/sources/dac_paper/Decision_or_Supply_manuscript_F9_revised.docx"
MERGE = Path(sys.argv[1]) if len(sys.argv) > 1 else None
AUTH = 'w:author="Claude" w:date="2026-10-28T00:00:00Z"'
_id = [1000]


def nid() -> int:
    _id[0] += 1
    return _id[0]


def run(rpr: str, text: str, kind: str = "t") -> str:
    tag = "w:delText" if kind == "del" else "w:t"
    return f'<w:r>{rpr}<{tag} xml:space="preserve">{text}</{tag}></w:r>'


def tracked(x: str, old: str, new: str, start: int = 0) -> str:
    """Replace one occurrence (the only one at or after `start`) of `old` inside a single <w:t>."""
    o = escape(old)
    i = x.find(o, start)
    assert i >= 0, f"not found: {old[:70]}"
    assert x.find(o, i + 1) < 0 or start, f"not unique: {old[:70]}"
    rs = max(x.rfind("<w:r>", 0, i), x.rfind("<w:r ", 0, i))
    re_ = x.find("</w:r>", i) + len("</w:r>")
    r = x[rs:re_]
    m = re.match(r'<w:r(?: [^>]*)?>(<w:rPr>.*?</w:rPr>)?<w:t(?: [^>]*)?>(.*)</w:t></w:r>$', r, re.S)
    assert m, f"run not simple: {r[:200]}"
    rpr, text = m.group(1) or "", m.group(2)
    j = text.find(o)
    parts = []
    if text[:j]:
        parts.append(run(rpr, text[:j]))
    parts.append(f'<w:del w:id="{nid()}" {AUTH}>' + run(rpr, o, "del") + "</w:del>")
    if new:
        parts.append(f'<w:ins w:id="{nid()}" {AUTH}>' + run(rpr, escape(new)) + "</w:ins>")
    if text[j + len(o):]:
        parts.append(run(rpr, text[j + len(o):]))
    return x[:rs] + "".join(parts) + x[re_:]


def add_text(x: str, anchor: str, new: str) -> str:
    """Insert `new` after `anchor` as its own inserted run, without deleting the anchor."""
    o = escape(anchor)
    assert x.count(o) == 1, f"anchor not unique: {anchor[:60]}"
    i = x.find(o) + len(o)
    rs = max(x.rfind("<w:r>", 0, i), x.rfind("<w:r ", 0, i))
    re_ = x.find("</w:r>", i) + len("</w:r>")
    r = x[rs:re_]
    m = re.match(r'<w:r(?: [^>]*)?>(<w:rPr>.*?</w:rPr>)?<w:t(?: [^>]*)?>(.*)</w:t></w:r>$', r, re.S)
    rpr, text = m.group(1) or "", m.group(2)
    j = text.find(o) + len(o)
    parts = [run(rpr, text[:j]), f'<w:ins w:id="{nid()}" {AUTH}>' + run(rpr, escape(new)) + "</w:ins>"]
    if text[j:]:
        parts.append(run(rpr, text[j:]))
    return x[:rs] + "".join(parts) + x[re_:]


def new_paragraph_after(x: str, anchor: str, text: str) -> str:
    """Insert a tracked paragraph, styled like the anchor's paragraph, after the paragraph containing `anchor`."""
    o = escape(anchor)
    assert x.count(o) == 1, f"anchor not unique: {anchor[:60]}"
    i = x.find(o)
    ps = x.rfind("<w:p>", 0, i)
    pe = x.find("</w:p>", i) + len("</w:p>")
    ppr = re.sub(r"<w:rPr>.*?</w:rPr>", "", re.match(r"<w:p>(<w:pPr>.*?</w:pPr>)", x[ps:pe], re.S).group(1))
    ppr_ins = ppr.replace("</w:pPr>", f'<w:rPr><w:ins w:id="{nid()}" {AUTH}/></w:rPr></w:pPr>')
    para = f'<w:p>{ppr_ins}<w:ins w:id="{nid()}" {AUTH}>' + run("", escape(text)) + "</w:ins></w:p>"
    return x[:pe] + para + x[pe:]


def cell(x: str, caption: str, row_key: str, col: int, new: str) -> str:
    """Tracked replacement of the whole text of one table cell (table after `caption`, row containing `row_key`)."""
    t = x.find(escape(caption))
    ts = x.find("<w:tbl>", t)
    te = x.find("</w:tbl>", ts)
    rows = [m.start() for m in re.finditer(r"<w:tr>", x[ts:te])]
    for rstart in rows:
        a = ts + rstart
        b = x.find("</w:tr>", a)
        cells = [m.start() + a for m in re.finditer(r"<w:tc>", x[a:b])]
        first = x[cells[0]:x.find("</w:tc>", cells[0])]
        if f">{escape(row_key)}<" in first:
            c0 = cells[col]
            c1 = x.find("</w:tc>", c0)
            texts = re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", x[c0:c1])
            assert len(texts) == 1, f"cell has {len(texts)} runs: {row_key}/{col}"
            return x[:c0] + tracked(x[c0:c1], _unescape(texts[0]), new) + x[c1:]
    raise AssertionError(f"row not found: {caption[:30]}/{row_key}")


def _unescape(s: str) -> str:
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def edits(x: str) -> str:
    # --- Abstract
    x = tracked(x, "Across countries, first deliveries fell within six days of one another although first orders were weeks apart.",
                "Across countries, first deliveries in Belgium, Germany and the Netherlands fell within 5–11 days of one another; "
                "their first orders were 2–16 days apart under the better-supported reading of the Belgian testimony and 31–49 days "
                "apart under the others.")
    # --- Section 1
    x = tracked(x, "Across the five member states and the EU level, first deliveries in the import-dependent countries fell within six days of one another although their first orders were weeks apart.",
                "Across the five member states and the EU level, first deliveries in Belgium, Germany and the Netherlands fell within "
                "5–11 days of one another, while their first orders were 2–16 days apart under the better-supported reading of the "
                "Belgian testimony and 31–49 days apart under the others.")
    # --- Section 3.1
    x = add_text(x, "together with the verbatim records of the hearings it cites (Chamber of Representatives, 2021b, 2021c)",
                 " and, for the first binding act, the Moniteur belge (Service public fédéral Economie, 2020)")
    x = tracked(x, "and for Sweden, the Corona Commission (SOU 2021:89).",
                "and for Sweden, the Corona Commission (SOU 2021:89), with its first interim report for the first deliveries (SOU 2020:80).")
    x = tracked(x, "the notification of the federal export ban (European Commission, 2020c) and one press report (Deutsches Ärzteblatt, 2020a).",
                "the notification of the federal export ban (European Commission, 2020c), the first procurement report of the Federal "
                "Ministry of Health (Bundesministerium für Gesundheit, 2020) and a report of the Federal Court of Audit to the "
                "Bundestag (Bundesrechnungshof, 2025); one press report (Deutsches Ärzteblatt, 2020a) is used for context only.")
    x = tracked(x, "Germany’s source dates the start of federal procurement (28 February) but no individual order, so its first order is a window closing at its first delivery; Sweden’s order is undated, so its window opens at t0.",
                "Germany’s sources date the start of federal procurement (28 February) and the start of the ministry’s own purchase "
                "contracts, which the Court of Audit places on 9 March (Bundesrechnungshof, 2025) and the ministry’s report in "
                "mid-March (Bundesministerium für Gesundheit, 2020); its first order is therefore a window under two readings. "
                "Sweden’s first order is dated only to February 2020, when the national health agency made minor purchases "
                "(SOU 2021:89). A date given as the beginning, middle or end of a month is coded as days 1–10, 11–20 or 21 to the end "
                "of the month.")
    x = tracked(x, "Binding acts are reported but not compared, because their content differs.",
                "Binding acts are reported but not compared, because their content differs. The event files were coded under rules "
                "fixed before coding, by one coder, an AI model (Claude), with every cited phrase checked automatically against its "
                "source page; the coder already knew the Belgian result and several first-order codings, so every "
                "coded date and lag is a test on known history, not a blind test; the cross-case statistics are exploratory.")
    # --- Section 3.2 and Table 2
    x = tracked(x, "A separate order file records the eight Belgian federal orders for which the chronology gives both an order date and a first-delivery date, all from the testimony and annexes of the head of the federal medical stock (Saniport).",
                "A separate order file records the eight Belgian federal orders for which the chronology gives both an order date and "
                "a first delivery, all from the testimony and annexes of the head of the federal medical stock (Saniport).")
    x = tracked(x, "and one was placed with a new domestic producer.",
                "and one was placed with a new domestic producer, whose first delivery, in early August, falls after the observation "
                "window (30 June 2020) and is coded as censored.")
    T2 = "Table 2. Event files and order file."
    rows = {"Belgium": ("Chamber special committee, Annex 5, hearings and Moniteur belge", "33", "33", "0", "4", "27"),
            "France": (None, "15", "15", "0", "1", "12"),
            "Germany": ("Bundestag papers, federal audit and ministry reports", "16", "15", "1", "2", "12"),
            "Netherlands": (None, "18", "18", "0", "4", "12"),
            "Sweden": ("Corona Commission, SOU 2021:89 and SOU 2020:80", "20", "20", "0", "2", "16"),
            "EU level": (None, "13", "13", "0", "3", "8")}
    for k, vals in rows.items():
        for col, v in enumerate(vals, start=1):
            if v is not None:
                x = cell(x, T2, k, col, v)
    x = _total_row(x, T2, ("115", "114", "1", "16", "87"))
    x = cell(x, T2, "Belgian orders", 2, "10 rows (8 orders)")
    x = cell(x, T2, "Belgian orders", 3, "10")
    x = cell(x, T2, "Belgian orders", 5, "2")
    x = cell(x, T2, "Belgian orders", 6, "6 paired orders with a dated delivery, 5 in the main series")
    x = tracked(x, "Substantive dated events exclude thresholds, events coded under a second role, the second bound of each window and, at EU level, four events concerning vaccines. The order file holds the contested first order under two readings, hence nine rows.",
                "Undated: coded missing or censored, including sublayers for which no event was found. Substantive dated events "
                "exclude the two WHO thresholds; each window counts once. The order file holds the contested first order under three "
                "readings (Section 4.1), hence ten rows.")
    # --- Section 4.1, Table 3
    x = tracked(x, "We take reading B (order on 4 March, day 34), stated directly by the official responsible for purchasing, as primary, and report reading A (31 January, day 1) alongside.",
                "We take reading B (order on 4 March, day 34), stated directly by the official responsible for purchasing, as primary, "
                "and report reading A (31 January, day 1) alongside. The 4 February entry, worded as an “option sur/commande” (an "
                "option on, or an order for, the masks), is kept in the event file as a third reading, the option reading (day 5); "
                "results under it are reported where they differ from those under reading A.")
    T3 = "Table 3. Belgian federal orders paired with their own first delivery (days from t0)."
    x = cell(x, T3, "1", 3, "34 (reading A: 1; option reading: 5)")
    x = cell(x, T3, "1", 5, "23 (reading A: 56; option reading: 52)")
    x = cell(x, T3, "6", 4, "after 152 (early August; censored)")
    x = cell(x, T3, "6", 5, "more than 102")
    x = tracked(x, "Delivery dates are as reported by the purchasing service.",
                "Delivery dates are as reported by the purchasing service. Order 6 was first delivered after the observation window "
                "(30 June 2020, day 152) and is coded as censored.")
    # --- Section 4.2 (new reading only)
    x = tracked(x, "Under reading A, the slope is 0.15 and the supply-limited model fits better with any one order left out.",
                "Under reading A, the slope is 0.15 and the supply-limited model fits better with any one order left out; under the "
                "option reading, the slope is 0.17, with the same result.")
    # --- Section 4.3, Table 5
    x = tracked(x, "Under reading B, the dated first orders of the import-dependent countries fall on or after day 29; Sweden’s cannot be dated; France ordered on day 8, from French manufacturers.",
                "Under reading B, the first orders of Belgium, Germany and the Netherlands fall on or after day 29; Sweden’s falls in "
                "February (days 2–30); France ordered on day 8 (day 20 if dated by the validation of its first purchase), from French "
                "manufacturers.")
    x = tracked(x, "First deliveries to a distribution level came on day 46 in Belgium, days 51–52 in Germany and day 51 in the Netherlands, within six days of one another, although their first orders were 2–17 days apart under reading B and 35–50 days apart under reading A.",
                "First deliveries to a distribution level came on day 46 in Belgium, days 41–50 in Germany and days 51–52 in the "
                "Netherlands, 5–11 days apart, while their first orders were 2–16 days apart under reading B and 35–49 days apart "
                "under reading A.")
    x = tracked(x, "France delivered first (days 39–45), most plausibly from its stock;",
                "France’s first delivery fell on days 39–52, most plausibly from its stock, a window that does not place it before "
                "Germany’s or Belgium’s;")
    T5 = "Table 5. First firm order, first binding act and first delivery (days from t0 = 30 January 2020)."
    t5 = {"France": {2: "8 (validation reading: 20; looser rule: 0)", 4: "39–52"},
          "Belgium": {2: "34 (A: 1; option: 5)", 3: "53†", 5: "12 (A: 45; option: 41)", 6: "23 (A: 56; option: 52); five orders 5–23"},
          "Germany": {2: "29–39 (ministry reading: 29–50)†", 4: "41–50†", 5: "2–21 (ministry reading: −9 to 21)"},
          "Netherlands": {4: "51–52", 5: "12–16"},
          "Sweden": {2: "2–30", 4: "47–61†", 5: "17–59"},
          "EU level": {2: "tender 28–29", 4: "86 (stockpile)"}}
    for k, cols in t5.items():
        for col, v in cols.items():
            x = cell(x, T5, k, col, v)
    x = tracked(x, "n.c.: not comparable, because the first French deliveries most plausibly came from the stock. —: not applicable or no paired record.",
                "n.c.: not comparable, because the first French deliveries most plausibly came from the stock. —: not applicable or "
                "no paired record. Option: the third reading of the Belgian first order (Section 4.1). Germany: first order under the "
                "Court of Audit’s date (9 March) and under the ministry’s (mid-March); a negative interval means the windows overlap. "
                "†: rests on the Moniteur belge, SOU 2020:80 or the German ministry and audit reports (Section 3.1). All values: test on known history.")
    x = tracked(x, "over all dates consistent with the windows, the Spearman rank correlation between order and delivery dates reaches +1.00 in every combination examined, and its lower end ranges from −0.80 to +0.60.",
                "over all dates consistent with the windows and every combination of readings, the Spearman rank correlation between "
                "order and delivery dates for Belgium, Germany, the Netherlands and Sweden runs from a lower end of −0.80 to −0.40 to "
                "an upper end of +0.80 to +1.00, and with France from −0.90 to −0.50 to +0.90 to +1.00 (exploratory).")
    # --- Section 5
    x = tracked(x, "The cross-case pattern, orders spread over weeks and deliveries within six days, is what a common supply constraint would produce.",
                "The cross-case pattern, first deliveries 5–11 days apart while first orders were 31–49 days apart under the earlier "
                "readings of the Belgian testimony, is what a common supply constraint would produce; under reading B, orders "
                "(2–16 days apart) were not more dispersed than deliveries.")
    x = tracked(x, "No dated import-dependent first delivery precedes day 46 (Sweden’s window opens on day 41), and all fall within the export surge from China.",
                "No import-dependent first delivery can fall before day 41, when Germany’s window opens, and all fall within the "
                "export surge from China (days 31–66).")
    x = tracked(x, "France, the only case with a national stock and domestic manufacturers in production, delivered first.",
                "France, the only case with a national stock and domestic manufacturers in production, delivered from day 39, although its "
                "window does not establish that it delivered first.")
    # --- Section 6.2
    x = tracked(x, "In 2020, the one case with a stock and domestic manufacturers in production delivered first,",
                "In 2020, the one case with a stock and domestic manufacturers in production delivered early,")
    # --- Section 7
    x = tracked(x, "All files were coded by one person, and the firm-order rule was fixed after a first round of coding.",
                "All files were coded by an AI model (Claude) under rules fixed before coding, with every cited phrase checked "
                "automatically against its source page; no human has yet recoded them, and the Belgian result and several "
                "first-order codings were known beforehand, so they are a test on known history, not a blind test.")
    # --- Section 8
    x = tracked(x, "Across five countries and the EU level, deliveries converged while orders diverged, as a supply constraint would predict, but unpaired dates cannot test it.",
                "Across five countries and the EU level, first deliveries in the import-dependent countries fell within days of one "
                "another, and orders were more dispersed only under some readings of the Belgian testimony; unpaired dates cannot "
                "test a supply constraint in any case.")
    # --- Data availability
    x = tracked(x, "The six event files, the Belgian order file and the scripts that compute every value in Tables 2–5 and Sections 4 and 5, and that draw Figures 1 and 2, are openly available in a public repository and archived with a persistent identifier;",
                "The six event files, the Belgian order file and the scripts that compute every value in Tables 2, 3 and 5 and "
                "Sections 4 and 5 are openly available in a public repository, to be archived with a persistent identifier; "
                "Figures 1 and 2 are to be redrawn from these files;")
    # --- References (four added)
    x = new_paragraph_after(x, "Box-Steffensmeier, J. M., & Jones, B. S. (2004).",
                            "Bundesministerium für Gesundheit. (2020, April 4). 1. Bericht über den Stand der Beschaffung von "
                            "Persönlicher Schutzausstattung (PSA) und intensivmedizinischer Ausstattung [Procurement task force, "
                            "first report]. https://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/C/Coronavirus/"
                            "Beschaffungsstab/1._Bericht_Beschaffungsstab_040420.pdf")
    x = new_paragraph_after(x, "Bundesministerium für Gesundheit. (2020, April 4).",
                            "Bundesrechnungshof. (2025, December 12). Bericht nach § 88 Absatz 2 BHO an die Enquete-Kommission des "
                            "Deutschen Bundestages: Beschaffung (medizinisches Material, Impfstoffe) und Versorgungssicherheit "
                            "[Report of the Federal Court of Audit to the Bundestag commission of inquiry]. "
                            "https://epflicht.ulb.uni-bonn.de/download/pdf/811470")
    x = new_paragraph_after(x, "Sénat. (2020).",
                            "Service public fédéral Economie. (2020). Arrêté ministériel du 23 mars 2020 portant des mesures "
                            "particulières dans le cadre la pandémie de SRAS-CoV-2 basées sur le livre XVIII du Code de droit "
                            "économique. Moniteur belge, 23 March 2020 (2nd ed.), 17611–17613.")
    x = _insert_before_para(x, "SOU 2021:89. (2021).",
                            "SOU 2020:80. (2020). Äldreomsorgen under pandemin [First interim report of the Corona Commission]. "
                            "Statens offentliga utredningar. https://regeringen.se/contentassets/a8e708fff5e84279bf11adbd0f78fcc1/"
                            "sou_2020_80_aldreomsorgen-under-pandemin.pdf")
    return x


def _total_row(x: str, caption: str, vals) -> str:
    """Table 2 total row: each cell holds one bold run."""
    for col, v in enumerate(vals, start=2):
        x = cell(x, caption, "Total", col, v)
    return x


def _insert_before_para(x: str, anchor: str, text: str) -> str:
    o = escape(anchor)
    i = x.find(o)
    assert i >= 0 and x.find(o, i + 1) < 0
    ps = x.rfind("<w:p>", 0, i)
    ppr = re.match(r"<w:p>(<w:pPr>.*?</w:pPr>)", x[ps:], re.S).group(1)
    ppr_ins = ppr.replace("</w:pPr>", f'<w:rPr><w:ins w:id="{nid()}" {AUTH}/></w:rPr></w:pPr>')
    para = f'<w:p>{ppr_ins}<w:ins w:id="{nid()}" {AUTH}>' + run("", escape(text)) + "</w:ins></w:p>"
    return x[:ps] + para + x[ps:]


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        un = Path(tmp) / "un"
        subprocess.run(["unzip", "-q", str(SRC), "-d", str(un)], check=True)
        for p in un.rglob("*"):
            if p.is_symlink():
                p.unlink()
        if MERGE:
            subprocess.run([sys.executable, str(MERGE), str(un)], check=True, capture_output=True)
        doc = un / "word/document.xml"
        doc.write_text(edits(doc.read_text(encoding="utf-8")), encoding="utf-8")
        OUT.unlink(missing_ok=True)
        subprocess.run(["zip", "-Xqr", str(OUT), "."], cwd=un, check=True)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
