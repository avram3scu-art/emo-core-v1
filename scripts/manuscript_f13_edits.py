"""F13: insert the redrawn Figures 1 and 2 into "Decision or Supply?" as tracked changes (author "Claude").

Base: docs/sources/dac_paper/Decision_or_Supply_manuscript_F12_revised.docx with its F12 tracked changes accepted
(scripts/manuscript_f12_edits.accept_all), so the F13 changes are the only tracked changes.
Output: docs/sources/dac_paper/Decision_or_Supply_manuscript_F13_revised.docx
Changes: the "[Figure n about here]" placeholders are replaced by the PNGs from analysis/dac_ppe_figures.py;
the figure legends and the data availability statement are updated to match. Listed in docs/MANUSCRIPT_F13_CHANGES.md.
Usage: python scripts/manuscript_f13_edits.py <path to the docx skill's merge_runs.py>
"""

from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/sources/dac_paper/Decision_or_Supply_manuscript_F12_revised.docx"
OUT = ROOT / "docs/sources/dac_paper/Decision_or_Supply_manuscript_F13_revised.docx"
FIGS = {1: ROOT / "analysis/figures/dac_ppe_fig1.png", 2: ROOT / "analysis/figures/dac_ppe_fig2.png"}
MERGE = Path(sys.argv[1]) if len(sys.argv) > 1 else None


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


f9 = _load("f9", "scripts/manuscript_f9_edits.py")
f12 = _load("f12", "scripts/manuscript_f12_edits.py")
f9._id[0] = 9000
tracked, nid, AUTH = f9.tracked, f9.nid, f9.AUTH
WIDTH_EMU = 5486400  # 6 inches


def drawing(rid: str, n: int, png: Path) -> str:
    w, h = Image.open(png).size
    cx, cy = WIDTH_EMU, int(WIDTH_EMU * h / w)
    return (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:docPr id="{100 + n}" name="Figure {n}"/><wp:cNvGraphicFramePr>'
            '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
            '</wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{100 + n}" name="dac_ppe_fig{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            "</wp:inline></w:drawing></w:r>")


def place_figure(x: str, n: int, rid: str) -> str:
    """Replace the run '[Figure n about here]' by a tracked deletion plus a tracked insertion of the image."""
    old = f'<w:r><w:t xml:space="preserve">[Figure {n} about here]</w:t></w:r>'
    assert x.count(old) == 1, f"placeholder {n}"
    new = (f'<w:del w:id="{nid()}" {AUTH}><w:r><w:delText xml:space="preserve">[Figure {n} about here]</w:delText></w:r></w:del>'
           f'<w:ins w:id="{nid()}" {AUTH}>' + drawing(rid, n, FIGS[n]) + "</w:ins>")
    return x.replace(old, new)


def edits(x: str, rids: dict[int, str]) -> str:
    for n, rid in rids.items():
        x = place_figure(x, n, rid)
    x = tracked(x, "Squares mark orders and circles first deliveries; labels give the paired lag. The open square and dotted line show the first order under reading A of the contested testimony (31 January); the solid line on the same row shows reading B (4 March). The shaded band is the period over which China exported 3.86 billion masks; the dashed line marks China’s export controls.",
                "Squares mark orders and circles first deliveries; labels give the paired lag. Filled squares and solid lines "
                "show reading B of the contested first order (4 March); open squares and the dotted line show reading A "
                "(31 January) and the option reading (4 February). The shaded band is the period over which China exported "
                "3.86 billion masks; dashed lines mark China’s daily output of 116 million masks (29 February) and its export "
                "checks from 1 April.")
    x = tracked(x, "Filled symbols mark exact dates; bars with open ends mark windows; the open circle with an arrow marks a lower bound; the cross marks the EU’s first tender, which is not a firm order. The grey lines and diamond show the Belgian 3M order and its delivery on day 57 under reading B (solid, order day 34) and reading A (dotted, order day 1).",
                "Squares mark first firm orders, triangles first binding acts and circles first deliveries; filled symbols mark "
                "exact dates and bars mark windows; open symbols and thin bars mark alternative readings (Belgium: reading A and "
                "the option reading; France: the validation reading; Germany: the ministry reading). The cross marks the EU’s "
                "first tender, which is not a firm order. The grey line and diamond show the Belgian 3M order and its delivery "
                "on day 57 under reading B (solid, order day 34) and reading A (dotted, order day 1).")
    x = tracked(x, "Sections 4 and 5 are openly available in a public repository, to be archived with a persistent identifier; Figures 1 and 2 are to be redrawn from these files;",
                "Sections 4 and 5, and that draw Figures 1 and 2, are openly available in a public repository, to be archived "
                "with a persistent identifier;")
    return x


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        un = Path(tmp) / "un"
        subprocess.run(["unzip", "-q", str(SRC), "-d", str(un)], check=True)
        for p in un.rglob("*"):
            if p.is_symlink():
                p.unlink()
        doc = un / "word/document.xml"
        doc.write_text(f12.accept_all(doc.read_text(encoding="utf-8")), encoding="utf-8")
        if MERGE:
            subprocess.run([sys.executable, str(MERGE), str(un)], check=True, capture_output=True)
        rels = un / "word/_rels/document.xml.rels"
        r = rels.read_text(encoding="utf-8")
        nums = [int(n) for n in re.findall(r'Id="rId(\d+)"', r)]
        rids = {}
        (un / "word/media").mkdir(exist_ok=True)
        for k, n in enumerate((1, 2), start=1):
            rid = f"rId{max(nums) + k}"
            rids[n] = rid
            shutil.copy(FIGS[n], un / f"word/media/dac_ppe_fig{n}.png")
            r = r.replace("</Relationships>", f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                          f'officeDocument/2006/relationships/image" Target="media/dac_ppe_fig{n}.png"/></Relationships>')
        rels.write_text(r, encoding="utf-8")
        ct = un / "[Content_Types].xml"
        c = ct.read_text(encoding="utf-8")
        if 'Extension="png"' not in c:
            c = c.replace("<Default ", '<Default Extension="png" ContentType="image/png"/><Default ', 1)
            ct.write_text(c, encoding="utf-8")
        d = doc.read_text(encoding="utf-8")
        for ns, uri in (("wp", "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"),
                        ("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")):
            if f"xmlns:{ns}=" not in d[:3000]:
                d = d.replace("<w:document ", f'<w:document xmlns:{ns}="{uri}" ', 1)
        doc.write_text(edits(d, rids), encoding="utf-8")
        OUT.unlink(missing_ok=True)
        subprocess.run(["zip", "-Xqr", str(OUT), "."], cwd=un, check=True)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
