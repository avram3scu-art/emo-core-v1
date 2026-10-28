"""F9: cross-case statistics of the PPE case, recomputed from the six event files (docs/DAC_PPE_COMPARISON.md).

Evidence class: exploratory (descriptive statistics on known history; no pre-registered threshold).
Everything is in days from t0 = 30 January 2020 and is evaluated over all integer dates consistent with each
window, for every combination of readings (reading labels as in the event files).

Computes:
1. First order and first delivery (primary end point) per case and reading, from emo/dac_standard.py profiles.
2. Spread (max - min) of first-delivery days across the import-dependent cases with a dated delivery
   (BE, DE, NL; and with SE), as a range over all consistent dates.
3. Spread of first-order days across BE, DE, NL, per reading combination.
4. Unpaired first-order-to-first-delivery intervals per case and reading (from the profiles).
5. Spearman rank correlation between first-order and first-delivery days across cases (average ranks for
   ties), minimum and maximum over all consistent dates, for every reading combination; two case sets:
   BE, DE, NL, SE (import-dependent) and BE, FR, DE, NL, SE (all with an order and a delivery).
   Only relative positions matter, so each window is searched over its end points and the points just
   inside, at and just outside every other window's end points (exact over all orderings, ties included).
6. Belgian paired orders (manuscript Section 4.2): slope of delivery day on order day and the sums of squared
   errors of M1 and M2, per reading and with each order left out.
7. Counts for the manuscript's Table 2.
Writes analysis/dac_ppe_crosscase_output.txt. Run from the repository root.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from emo.dac_standard import compute_profile, load_event_file  # noqa: E402

CASES = ("BE", "FR", "DE", "NL", "SE", "EU")
OUT = ROOT / "analysis/dac_ppe_crosscase_output.txt"


def profiles(case):
    prof = compute_profile(load_event_file(ROOT / f"data/dac_ppe/{case}.json"))
    rows = []
    for p in prof["profiles"]:
        s = p["sublayers"]
        rows.append({
            "reading": ",".join(f"{k}={v}" for k, v in p["reading"].items()) or "-",
            "order": (s["firm_order"]["lag_from_t0"]["min_days"], s["firm_order"]["lag_from_t0"]["max_days"]) if "firm_order" in s else None,
            "delivery": (s["delivery"]["lag_from_t0"]["min_days"], s["delivery"]["lag_from_t0"]["max_days"]) if "delivery" in s else None,
            "unpaired": p.get("unpaired_first_order_to_first_delivery"),
        })
    return rows


def candidates(lo, hi, others):
    pts = {lo, hi}
    for b in others:
        for x in (b - 0.5, b, b + 0.5):
            if lo <= x <= hi:
                pts.add(x)
    return sorted(pts)


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    if sxx == 0 or syy == 0:
        return None
    return sxy / (sxx * syy) ** 0.5


def rank_patterns(windows):
    """Every rank vector (ties averaged) that some choice of dates within the windows produces."""
    b = [v for w in windows for v in w]
    cands = [candidates(lo, hi, b) for lo, hi in windows]
    return {tuple(ranks(list(x))) for x in itertools.product(*cands)}


def spearman_ranks(rx, ry):
    n = len(rx)
    mx, my = sum(rx) / n, sum(ry) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    return None if sxx == 0 or syy == 0 else sxy / (sxx * syy) ** 0.5


def range_over(windows_x, windows_y):
    # x and y windows are independent, so all (x pattern, y pattern) pairs are attainable.
    vals = [spearman_ranks(rx, ry) for rx in rank_patterns(windows_x) for ry in rank_patterns(windows_y)]
    vals = [v for v in vals if v is not None]
    return min(vals), max(vals)


def spread(windows):
    pts = [candidates(lo, hi, [v for w in windows for v in w]) for lo, hi in windows]
    s = [max(c) - min(c) for c in itertools.product(*pts)]
    return min(s), max(s)


def _fit(pts):
    """Least-squares slope of delivery day on order day, and SSE of M1 (one k) and M2 (one R)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else float("nan")
    k = sum(y - x for x, y in zip(xs, ys)) / n
    sse1 = sum((y - x - k) ** 2 for x, y in zip(xs, ys))
    sse2 = sum((y - my) ** 2 for y in ys)
    return f"orders {xs} deliveries {ys} slope {slope:.2f} SSE M1 {sse1:.1f} M2 {sse2:.1f}"


def main() -> None:
    P = {c: profiles(c) for c in CASES}
    out = ["F9 cross-case statistics (exploratory). Days from t0 = 30 Jan 2020.", "",
           "1. First order, first delivery and unpaired interval per case and reading"]
    for c in CASES:
        for r in P[c]:
            u = r["unpaired"]
            out.append(f"  {c} [{r['reading']}]: order {r['order']}, delivery {r['delivery']}, "
                       f"unpaired {(u['min_days'], u['max_days']) if u else None}")
    out += ["", "2. Spread of first-delivery days (max - min over all consistent dates)"]
    d = {c: P[c][0]["delivery"] for c in ("BE", "DE", "NL", "SE")}
    out.append(f"  BE, DE, NL: {spread([d['BE'], d['DE'], d['NL']])}")
    out.append(f"  BE, DE, NL, SE: {spread([d['BE'], d['DE'], d['NL'], d['SE']])}")
    out += ["", "3. Spread of first-order days across BE, DE, NL, per reading combination"]
    for rb, rd in itertools.product(P["BE"], P["DE"]):
        out.append(f"  BE[{rb['reading']}] DE[{rd['reading']}]: {spread([rb['order'], rd['order'], P['NL'][0]['order']])}")
    out += ["", "5. Spearman (order day vs delivery day) across cases: (min, max) over consistent dates"]
    for label, cs in (("BE, DE, NL, SE", ("BE", "DE", "NL", "SE")), ("BE, FR, DE, NL, SE", ("BE", "FR", "DE", "NL", "SE"))):
        lows, highs = [], []
        for combo in itertools.product(*[P[c] for c in cs]):
            lo, hi = range_over([r["order"] for r in combo], [r["delivery"] for r in combo])
            lows.append(lo)
            highs.append(hi)
            out.append(f"  {label} | " + " ".join(f"{c}[{r['reading']}]" for c, r in zip(cs, combo)) + f": {lo:+.2f} to {hi:+.2f}")
        out.append(f"  {label}: lower end ranges {min(lows):+.2f} to {max(lows):+.2f}; upper end ranges {min(highs):+.2f} to {max(highs):+.2f}")
    out += ["", "6. Belgian paired orders (Section 4.2): slope of delivery on order day; SSE of M1 (D = O + k) and M2 (D = R)"]
    be = json.loads((ROOT / "data/dac_ppe/BE.json").read_text(encoding="utf-8"))["events"]
    dl = {e["pairs_with"]: e for e in be if e["sublayer"] == "delivery" and e.get("pairs_with") and e["date_status"] == "exact"}
    t0 = __import__("datetime").date(2020, 1, 30)

    def day(s):
        return (__import__("datetime").date.fromisoformat(s) - t0).days

    for reading in ("A", "B", "C"):
        for good in ("FFP2 respirators", "surgical masks"):
            pts = sorted((day(o["date_earliest"]), day(dl[o["event_id"]]["date_earliest"]), o["event_id"]) for o in be
                         if o["sublayer"] == "firm_order" and o.get("good") == good and o["event_id"] in dl
                         and o.get("reading") in (None, reading))
            if good == "surgical masks" and reading != "A":
                continue  # surgical orders do not depend on the 3M reading
            out.append(f"  reading {reading}, {good}: " + _fit(pts) + "".join(
                f"; without {p[2]}: " + _fit([q for q in pts if q is not p]) for p in pts if len(pts) > 2))
    out += ["", "7. Table 2 counts: entries, primary, secondary, undated (missing or censored), dated events excluding the two WHO thresholds"]
    for c in CASES:
        ev = json.loads((ROOT / f"data/dac_ppe/{c}.json").read_text(encoding="utf-8"))["events"]
        und = sum(e["date_status"] in ("missing", "censored") for e in ev)
        dated = sum(e["date_status"] not in ("missing", "censored") and e["event_id"] not in ("who_pheic", "who_pandemic") for e in ev)
        out.append(f"  {c}: {len(ev)}, {sum(e['source_type'] == 'primary' for e in ev)}, {sum(e['source_type'] == 'secondary' for e in ev)}, {und}, {dated}")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
