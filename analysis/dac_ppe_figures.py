"""F13: Figures 1 and 2 of "Decision or Supply?", drawn from the six PPE event files only.

Inputs: data/dac_ppe/{BE,FR,DE,NL,SE,EU}.json (dates, readings, pairs), their profiles (first events per reading,
computed by emo/dac_standard.py) and data/dac_ppe/china_supply_events.json (dated supply events in China with their
sources). Days from t0 = 30 January 2020. Evidence class of the values shown: pre-registered on known history.
Writes analysis/figures/dac_ppe_fig1.{png,pdf} and dac_ppe_fig2.{png,pdf}. Run from the repository root.

Figure 1: the five Belgian federal mask orders from commercial suppliers, each joined to the first delivery of the
same order; the 3M order under its three readings (A 31 Jan, option 4 Feb, B 4 Mar).
Figure 2: per case, first firm order, first binding act and first delivery to a distribution level; windows as bars,
exact dates as filled markers; readings as separate marks; the EU tender (not a firm order) as a cross.
Colour is redundant with marker shape (square = order, triangle = binding act, circle = delivery), so the figures
read in greyscale. Palette: the dataviz skill's validated categorical slots 1-3 (light mode).
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from emo.dac_standard import compute_profile, load_event_file  # noqa: E402

D = ROOT / "data/dac_ppe"
OUT = ROOT / "analysis/figures"
T0 = dt.date(2020, 1, 30)
ORDER, ACT, DELIV = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#2b2b29", "#6b6a63", "#d9d8d2"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False})


def day(s: str) -> int:
    return (dt.date.fromisoformat(s) - T0).days


def events(case: str) -> list[dict]:
    return json.loads((D / f"{case}.json").read_text(encoding="utf-8"))["events"]


def china(ax, labels: bool) -> None:
    ev = json.loads((D / "china_supply_events.json").read_text(encoding="utf-8"))["events"]
    for e in ev:
        if e["kind"] == "band":
            ax.axvspan(e["day_start"], e["day_end"], color="#ecebe6", zorder=0, lw=0)
            if labels:
                ax.text((e["day_start"] + e["day_end"]) / 2, 1.0, e["label"], transform=ax.get_xaxis_transform(),
                        ha="center", va="bottom", fontsize=7, color=MUTED)
        else:
            ax.axvline(e["day"], color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
            if labels:  # above the plot, beside the line, so no data mark is covered
                left = e["day"] < 45
                ax.text(e["day"] + (-0.6 if left else 0.6), 1.07, e["label"], transform=ax.get_xaxis_transform(),
                        ha="right" if left else "left", va="bottom", fontsize=6.5, color=MUTED)


def fig1() -> None:
    ev = events("BE")
    orders = [e for e in ev if e["sublayer"] == "firm_order" and e.get("good") in ("FFP2 respirators", "surgical masks")]
    dels = {e["pairs_with"]: e for e in ev if e["sublayer"] == "delivery" and e.get("pairs_with") and e["date_status"] == "exact"}
    rows: list[tuple[str, list[dict], dict]] = []
    for oid in dict.fromkeys(o["event_id"] for o in orders):
        if oid not in dels:
            continue
        ro = [o for o in orders if o["event_id"] == oid]
        rows.append((oid, sorted(ro, key=lambda o: o["date_earliest"]), dels[oid]))
    rows.sort(key=lambda r: max(day(o["date_earliest"]) for o in r[1]))
    names = {"order_3M_ffp2": "3M, 500,000 FFP2", "order_life_surgical": "Life, 10,000,000 surgical",
             "order_ultrazonic_ffp2": "Ultrazonic, 1,000,000 FFP2", "order_life_ffp2": "Life, 3,000,000 FFP2",
             "order_xml_surgical": "XML, 2,200,000 surgical"}
    fig, ax = plt.subplots(figsize=(7.0, 3.6), dpi=200)
    china(ax, labels=True)
    for y, (_oid, ro, d) in enumerate(reversed(rows)):
        dd = day(d["date_earliest"])
        for o in ro:
            od = day(o["date_earliest"])
            main = o.get("reading") in (None, "C")
            ax.plot([od, dd], [y, y], color=INK if main else MUTED, lw=1.4 if main else 1.0,
                    ls="-" if main else (0, (2, 2)), zorder=2)
            ax.plot(od, y, marker="s", ms=6.5, mfc=ORDER if main else "white", mec=ORDER, mew=1.4, zorder=3)
            lab = {"A": "A", "B": "option", "C": "B"}.get(o.get("reading"), "")
            if lab:
                ax.text(od, y + 0.22, lab, ha="center", va="bottom", fontsize=6.5, color=MUTED)
        ax.plot(dd, y, marker="o", ms=6.5, mfc=DELIV, mec="white", mew=1.0, zorder=4)
        lags = [dd - day(o["date_earliest"]) for o in ro]
        txt = str(lags[-1]) + (" (A: " + str(lags[0]) + "; option: " + str(lags[1]) + ")" if len(lags) == 3 else "")
        ax.text(dd + 1.2, y, f"{txt} d", va="center", fontsize=7, color=INK)
    ax.set_yticks(range(len(rows)), [names.get(r[0], r[0]) for r in reversed(rows)])
    ax.set_xlim(-1, 95)
    ax.set_ylim(-0.6, len(rows) - 0.3)
    ax.set_xlabel("Days from 30 January 2020 (WHO emergency declaration)")
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker="s", ls="", mfc=ORDER, mec=ORDER, label="Order (reading B)"),
         Line2D([], [], marker="s", ls="", mfc="white", mec=ORDER, label="Order (reading A / option)"),
         Line2D([], [], marker="o", ls="", mfc=DELIV, mec="white", label="First delivery of that order")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=7, frameon=False)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"dac_ppe_fig1.{ext}")
    plt.close(fig)


def span(e: dict) -> tuple[int, int]:
    return day(e["date_earliest"]), day(e["date_latest"])


def fig2() -> None:
    cases = [("FR", "France"), ("BE", "Belgium"), ("DE", "Germany"), ("NL", "Netherlands"), ("SE", "Sweden"), ("EU", "EU level")]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=200)
    china(ax, labels=True)
    offs = {"firm_order": 0.22, "binding_act": 0.0, "delivery": -0.22}
    col = {"firm_order": ORDER, "binding_act": ACT, "delivery": DELIV}
    mk = {"firm_order": "s", "binding_act": "^", "delivery": "o"}
    for y, (case, _label) in enumerate(reversed(cases)):
        prof = compute_profile(load_event_file(D / f"{case}.json"))
        ev = {e["event_id"] + "|" + str(e.get("reading", "")): e for e in events(case)}
        drawn: set[str] = set()
        for p in prof["profiles"]:
            for sub in ("firm_order", "binding_act", "delivery"):
                s = p["sublayers"].get(sub)
                if not s:
                    continue
                for eid in s["first_event_ids"]:
                    rd = p["reading"].get(eid, "")
                    key = f"{eid}|{rd}"
                    if key in drawn or key not in ev:
                        continue
                    drawn.add(key)
                    a, b = span(ev[key])
                    main = rd == "" or (case == "BE" and rd == "C") or (case != "BE" and rd == "A")
                    yy = y + offs[sub] + (0.0 if main else 0.08)
                    if a != b:
                        ax.plot([a, b], [yy, yy], color=col[sub], lw=5 if main else 2.5, alpha=0.85 if main else 0.5,
                                solid_capstyle="butt", zorder=2)
                    else:
                        ax.plot(a, yy, marker=mk[sub], ms=6.5, mfc=col[sub] if main else "white", mec=col[sub],
                                mew=1.3, ls="", zorder=3)
        if case == "EU":
            t = next(e for e in events("EU") if e["event_id"] == "jpa_first_tender")
            a, b = span(t)
            ax.plot((a + b) / 2, y + offs["firm_order"], marker="x", ms=6, mew=1.4, color=ORDER, zorder=3)
        if case == "BE":
            o = {e["reading"]: day(e["date_earliest"]) for e in events("BE") if e["event_id"] == "order_3M_ffp2"}
            dd = day(next(e for e in events("BE") if e["event_id"] == "del_3M_ffp2")["date_earliest"])
            ax.plot([o["C"], dd], [y + 0.42] * 2, color=MUTED, lw=1.0, zorder=1)
            ax.plot([o["A"], o["C"]], [y + 0.42] * 2, color=MUTED, lw=1.0, ls=(0, (2, 2)), zorder=1)
            ax.plot(dd, y + 0.42, marker="D", ms=4.5, mfc=MUTED, mec="white", ls="", zorder=3)
    ax.set_yticks(range(len(cases)), [c[1] for c in reversed(cases)])
    ax.set_xlim(-1, 95)
    ax.set_ylim(-0.6, len(cases) - 0.35)
    ax.set_xlabel("Days from 30 January 2020 (WHO emergency declaration)")
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker="s", ls="", mfc=ORDER, mec=ORDER, label="First firm order"),
         Line2D([], [], marker="^", ls="", mfc=ACT, mec=ACT, label="First binding act"),
         Line2D([], [], marker="o", ls="", mfc=DELIV, mec=DELIV, label="First delivery"),
         Line2D([], [], marker="x", ls="", color=ORDER, label="EU tender (not a firm order)"),
         Line2D([], [], marker="D", ls="-", color=MUTED, ms=4, label="Belgian 3M order and its delivery")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=7, frameon=False)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"dac_ppe_fig2.{ext}")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig1()
    fig2()
    print("wrote analysis/figures/dac_ppe_fig1.{png,pdf}, dac_ppe_fig2.{png,pdf}")


if __name__ == "__main__":
    main()
