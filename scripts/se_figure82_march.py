"""F8.5: read the March 2020 bar of Figure 8.2 of SOU 2021:89 (PDF p. 338) from the PDF's vector data.

The figure (deliveries of protective and testing equipment from Socialstyrelsen to regions and
municipalities per month) carries no numbers in its text. Bar segments are filled rectangles; each
segment's colour is matched to the legend and its height converted to items with the y-axis ticks.
Needs the cached PDF from scripts/fetch_dac_ppe_sources.py. Writes data/sources/dac_ppe/SE_fig8_2_march.csv.
Run from the repository root: python scripts/se_figure82_march.py
"""

import csv
from pathlib import Path

import pdfplumber

PDF = Path(".cache/dac_ppe/SE_sou_2021_89.pdf")
OUT = Path("data/sources/dac_ppe/SE_fig8_2_march.csv")


def colour(r):
    c = r["non_stroking_color"]
    return tuple(c) if isinstance(c, (list, tuple)) else c


def main() -> None:
    with pdfplumber.open(PDF) as pdf:
        p = pdf.pages[337]
        words = p.extract_words()
        ticks = sorted((int(t["text"]), (t["top"] + t["bottom"]) / 2) for t in words
                       if t["text"].isdigit() and t["x0"] < 130 and 370 < t["top"] < 490)
        (v0, y0), (v1, y1) = ticks[0], ticks[-1]
        per_pt = (v1 - v0) / (y0 - y1)
        legend = {}
        for r in p.rects:
            if r["top"] > 455 and r["height"] < 6 and r["width"] < 6:
                near = min((t for t in words if abs((t["top"] + t["bottom"]) / 2 - (r["top"] + r["bottom"]) / 2) < 4
                            and t["x0"] > r["x0"]), key=lambda t: t["x0"])
                line = sorted((t for t in words if abs(t["top"] - near["top"]) < 2 and near["x0"] <= t["x0"]), key=lambda t: t["x0"])
                label = []
                for t in line:  # label runs until the next legend square
                    if any(abs(q["x0"] - t["x0"] + 6) < 4 and abs(q["top"] - r["top"]) < 2 for q in p.rects if q is not r and q["width"] < 6):
                        break
                    label.append(t["text"])
                legend[colour(r)] = " ".join(label)
        march_x = min(round(r["x0"], 1) for r in p.rects if 8 < r["width"] < 10)
        rows = [(legend.get(colour(r), str(colour(r))), round(r["height"] * per_pt))
                for r in p.rects if abs(r["x0"] - march_x) < 1.5 and 8 < r["width"] < 10]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "items_march_2020_approx"])
        w.writerows(rows)
        w.writerow(["total", sum(n for _, n in rows)])
    for r in rows:
        print(*r, sep=": ")


if __name__ == "__main__":
    main()
