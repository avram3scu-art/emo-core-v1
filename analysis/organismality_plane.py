"""Humanity's path on the cooperation-conflict plane, 1989-2025.

x: international co-authorship share of articles (OpenAlex), excluding papers with Chinese or
   Indonesian authors (composition/coverage control) - cognitive cooperation
y: death rate in armed conflicts per 100,000 (UCDP via OWID), log scale, inverted
   so that up = less conflict. Upper right = more organismal (high cooperation,
   low conflict; cf. Queller & Strassmann 2009, citation unverified).
Run from the repository root: python analysis/organismality_plane.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[1]
g = lambda f: {int(x["key"]): x["count"] for x in json.load(open(root / f))["group_by"]}
# Excluding China and Indonesia: their 2020-25 single-country growth (and OpenAlex coverage
# changes for Indonesia) otherwise creates an artificial dip in the share. See data/README_cooperation.md.
m = g("data/sources/openalex_articles_multicountry_by_year_excl_CN_ID/openalex_articles_multicountry_by_year_excl_CN_ID.json")
a = g("data/sources/openalex_articles_anycountry_by_year_excl_CN_ID/openalex_articles_anycountry_by_year_excl_CN_ID.json")
d = pd.read_csv(root / "data/sources/owid_ucdp_death_rate_armed_conflicts/owid_ucdp_death_rate_armed_conflicts.csv")
conf = d[d.Entity == "World"].set_index("Year")[d.columns[3]]
years = list(range(1989, 2026))
x = np.array([100 * m[y] / a[y] for y in years])
y = np.array([conf[y] for y in years])

INK, MUTED, GRID, SURF = "#1f1f1d", "#6b6a66", "#e6e5e1", "#fcfcfb"
ramp = ["#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("blue", ramp)
norm = matplotlib.colors.Normalize(1989, 2025)

fig, ax = plt.subplots(figsize=(7.2, 7.6), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
for i in range(len(years) - 1):
    ax.plot(x[i:i + 2], y[i:i + 2], color=cmap(norm(years[i])), lw=2, solid_capstyle="round", zorder=2)
ax.scatter(x, y, c=[cmap(norm(t)) for t in years], s=34, edgecolors=SURF, linewidths=2, zorder=3)
ax.set_yscale("log"); ax.invert_yaxis()
labels = {1989: (6, -4), 1994: (8, 0), 2005: (8, 2), 2014: (-12, -16), 2019: (-34, 6), 2022: (8, -4), 2025: (8, -2)}
for t, (dx, dy) in labels.items():
    i = years.index(t)
    txt = {1994: "1994 (Rwanda)", 2022: "2022 (Ukraine, Ethiopia)"}.get(t, str(t))
    ax.annotate(txt, (x[i], y[i]), xytext=(dx, dy), textcoords="offset points", fontsize=9, color=INK)
ax.set_xlabel("Cooperation: share of articles co-authored across countries (%, excl. China & Indonesia)", color=INK, fontsize=9.5)
ax.set_ylabel("Conflict: deaths in armed conflicts per 100,000 people (log scale, fewer ↑)", color=INK, fontsize=9.5)
ax.set_yticks([0.3, 0.5, 1, 2, 5, 15]); ax.set_yticklabels(["0.3", "0.5", "1", "2", "5", "15"])
ax.grid(True, which="major", color=GRID, lw=0.8); ax.minorticks_off()
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
ax.text(0.98, 0.98, "more organismal ↗", transform=ax.transAxes, ha="right", va="top", fontsize=9, color=MUTED)
fig.suptitle("Humanity on the cooperation–conflict plane, 1989–2025", x=0.08, ha="left", fontsize=13, color=INK, y=0.985)
ax.set_title("Thinking together rose, then levelled off; violence fell, then returned. Each dot is a year.", loc="left", fontsize=9.5, color=MUTED, pad=10)
fig.text(0.08, 0.012, "Sources: OpenAlex (articles with known country; China & Indonesia excluded, see notes); UCDP via Our World in Data.",
         fontsize=7, color=MUTED, ha="left")
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cb = fig.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.035, pad=0.11, aspect=40)
cb.set_label("Year", color=MUTED, fontsize=8.5); cb.outline.set_visible(False); cb.ax.tick_params(colors=MUTED, labelsize=8, length=0)
fig.tight_layout(rect=(0, 0.02, 1, 0.985))
out = root / "analysis/organismality_plane.png"
fig.savefig(out, facecolor=SURF)
print("saved", out)
