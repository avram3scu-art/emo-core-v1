"""Hurricane loop test on 2015-2025 (docs/LOOP_PROTOCOL.md §5-§8, §14-§16, run plan §18).

Evidence class: pre-registered on known history. Run once in session 2.5.
"""
import csv
import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data/loop_hurricanes"
_spec = importlib.util.spec_from_file_location("loop_power", Path(__file__).with_name("loop_power.py"))
lp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lp)

SEED_H5 = 2026102930
PAIRS = [(x, y) for x in ("F", "W", "A") for y in ("Y_state", "Y_fed")]
COL = {"F": "pr_F", "W": "wn_W_hours", "A": "at_A", "Y_state": "dc_Y_state_days", "Y_fed": "dc_Y_fed_days",
       "V": "ev_V_kt", "R64": "ev_R64_nmi", "region": "dc_region", "EMpre": "dc_EMpre"}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def guard_n(counts):
    return sum(n - 1 for n in counts if n >= 1) - 5


def main():
    rows = list(csv.DictReader((D / "loop_events.csv").open()))
    excl = list(csv.DictReader((D / "exclusions.csv").open()))
    summ = json.loads((D / "summary.json").read_text())
    v = {k: np.array([num(r[c]) for r in rows]) for k, c in COL.items()}
    season = np.array([int(r["ev_season"]) for r in rows])
    print("Hurricane loop test 2015-2025 (docs/LOOP_PROTOCOL.md §18). Class: pre-registered on known history.")
    print(f"events {len(rows)} (HU {sum(r['ev_hu_set'] == '1' for r in rows)})")

    # H3 (§8.1)
    both = ~np.isnan(v["Y_state"]) & ~np.isnan(v["Y_fed"])
    k, n = int(both.sum()), len(rows)
    bt = binomtest(k, n, 0.5, alternative="greater")
    ys = v["Y_state"][~np.isnan(v["Y_state"])]
    q1, q3 = np.percentile(ys, [25, 75])
    h3 = bt.pvalue < 0.05 and q3 - q1 > 0
    print(f"\nH3: both lags measured {k}/{n} = {k / n:.3f}; exact one-sided binomial p = {bt.pvalue:.4f} "
          f"(PASS needs < 0.05); Y_state IQR {q3 - q1:.1f} d (Q1 {q1:.1f}, Q3 {q3:.1f}) -> {'PASS' if h3 else 'FAIL'}")
    yf = v["Y_fed"][~np.isnan(v["Y_fed"])]
    for name, a in (("Y_state", ys), ("Y_fed", yf)):
        print(f"  descriptive {name}: n {len(a)}, min {a.min():.0f}, median {np.median(a):.1f}, max {a.max():.0f} d")

    # H4 guard part 1 (§15, §18.1)
    print("\nH4 guard part 1 (counts from summary.json): n_within - 5 per pair (tested if >= 15)")
    cc = summ["complete_cases_by_season_per_pair"]
    testable = []
    for x, y in PAIRS:
        g = guard_n(cc[f"{x}~{y}"].values())
        testable.append(g >= 15)
        print(f"  {x}~{y}: {g} -> {'tested' if g >= 15 else 'cannot be tested at this size'}")
    # sensitivity without list/season targets (§18.5), counts only
    kind = np.array([r["at_target_kind"] for r in rows])
    keep = kind == "storm"
    print(f"Sensitivity A without list/season targets (no weight): {int((~keep).sum())} events dropped")
    for y in ("Y_state", "Y_fed"):
        m = keep & ~np.isnan(v["A"]) & ~np.isnan(v[y])
        g = guard_n(np.bincount(season[m] - 2015, minlength=11))
        print(f"  A~{y}: n {int(m.sum())}, n_within - 5 = {g} -> {'tested' if g >= 15 else 'cannot be tested at this size'}")
    if not any(testable):
        print("H4: no pair passes guard part 1 -> H4 not run; reads 'cannot be tested at this size'.")

    # H5 (§6, §18.4)
    print("\nH5 (season-mean trend of residual lags, C5, Holm over 2)")
    rng = np.random.default_rng(SEED_H5)
    ps = []
    for y in ("Y_state", "Y_fed"):
        m = ~np.isnan(v[y])
        for c in ("F", "V", "R64", "region", "EMpre"):
            m &= ~np.isnan(v[c])
        C = np.column_stack([np.ones(m.sum()), v["V"][m], v["R64"][m], (v["region"][m] == 4) * 1.0,
                             (v["region"][m] == 6) * 1.0, v["EMpre"][m], v["F"][m]])
        res = lp.resid(lp.u(v[y][m]), C)
        s = season[m]
        ks = np.unique(s)
        means = np.array([res[s == q].mean() for q in ks])
        S = -lp.kendall_rows(ks.astype(float), means[None, :])[0]
        perm = np.argsort(rng.random((999, len(means))), axis=1)
        null = -lp.kendall_rows(ks.astype(float), means[perm])
        p = (1 + (null >= S - 1e-12).sum()) / 1000
        ps.append(p)
        print(f"  {y}: n {int(m.sum())}, seasons {len(ks)} {ks.tolist()}, rank of C5 {np.linalg.matrix_rank(C)}/7, "
              f"S = -tau {S:+.3f}, one-sided p = {p:.3f}")
    adj = lp.holm(ps)
    print(f"  Holm-adjusted p: Y_state {adj[0]:.3f}, Y_fed {adj[1]:.3f} -> "
          f"{'PASS' if adj.min() < 0.05 else 'not significant'}")

    # Exclusions and descriptive lists (§8.2, §18.6)
    print(f"\nExclusions ({len(excl)} rows, exclusions.csv):")
    by = {}
    for e in excl:
        by.setdefault((e["link"], e["reason"]), []).append(e["atcf"])
    for (link, reason), ids in sorted(by.items()):
        print(f"  {link}:{reason} ({len(ids)}): {' '.join(ids)}")
    noc = {e["atcf"] for e in excl if e["reason"] == "no_candidate"}
    print(f"\nStorms with no qualifying FEMA candidate ({len(noc)}; descriptive, no rule change):")
    for r in rows:
        if r["ev_atcf"] in noc:
            print(f"  {r['ev_atcf']} {r['ev_name']:10s} {r['ev_state']} t0 {r['ev_t0_utc']} {r['ev_status_t0']} "
                  f"{r['ev_V_kt']} kt")


if __name__ == "__main__":
    main()
