"""Registered 2027 forecasts for the hurricane loop (docs/LOOP_PROTOCOL.md §21).

Fits the §21 model on the 2015-2025 rows of data/loop_hurricanes/loop_events.csv, writes
data/loop_forecast_ledger.csv and its SHA-256, and prints the synthetic false-positive rate and
power of the §21 scoring test at the expected 2027 size (synthetic; counts and probabilities only).
"""
import csv
import hashlib
import itertools
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data/loop_hurricanes/loop_events.csv"
LEDGER = ROOT / "data/loop_forecast_ledger.csv"
REGISTERED = "2026-10-29"
RESOLVE = ("when the HURDAT2 file that first covers 2027 exists (OpenFEMA pulled the same day); "
           "void if none by 2028-10-01")
MAJOR_KT = 96
MIN_CLASS = 5
QUESTIONS = {  # id: (text, lag column, threshold)
    "Q2": ("Y_state <= 0 days (DR requested on or before the landfall date)", "dc_Y_state_days", 0),
    "Q3": ("Y_state <= 7 days", "dc_Y_state_days", 7),
    "Q4": ("Y_fed <= 1 day (DR declared within a day of the request)", "dc_Y_fed_days", 1),
    "Q5": ("Y_fed <= 7 days", "dc_Y_fed_days", 7),
}
SEED = 2027


def jeffreys(k, n):
    return (k + 0.5) / (n + 1)


def fit(rows):
    out = []
    # Q1: matched qualifying DR, by status at t0
    cls = {c: [r for r in rows if r["ev_status_t0"] == c] for c in ("HU", "TS")}
    k_all = sum(bool(r["dc_dr_number"]) for r in rows)
    base = jeffreys(k_all, len(rows))
    for c, rs in cls.items():
        k = sum(bool(r["dc_dr_number"]) for r in rs)
        out.append(("Q1", "matched to a qualifying FEMA DR (LOOP_PROTOCOL §3.1, amendment 5)",
                    f"status at t0 = {c}", k, len(rs), jeffreys(k, len(rs)), base))
    meas = [r for r in rows if r["dc_Y_state_days"] and r["dc_Y_fed_days"]]
    major = [r for r in meas if float(r["ev_V_kt"]) >= MAJOR_KT]
    minor = [r for r in meas if float(r["ev_V_kt"]) < MAJOR_KT]
    pooled = min(len(major), len(minor)) < MIN_CLASS
    for q, (text, col, thr) in QUESTIONS.items():
        k_all = sum(float(r[col]) <= thr for r in meas)
        base = jeffreys(k_all, len(meas))
        groups = [("all events with both lags (pooled: a class has < 5)", meas)] if pooled else [
            (f"V at t0 >= {MAJOR_KT} kt", major), (f"V at t0 < {MAJOR_KT} kt", minor)]
        for label, rs in groups:
            k = sum(float(r[col]) <= thr for r in rs)
            out.append((q, text + "; given a matched DR with both lags valid", label, k, len(rs),
                        jeffreys(k, len(rs)), base))
    return out, pooled, len(major), len(minor)


def sign_flip_p(d):
    d = np.asarray(d, float)
    n = len(d)
    if n == 0:
        return 1.0
    obs = d.sum()
    signs = np.array(list(itertools.product((1, -1), repeat=n)))
    return float(((signs * np.abs(d)).sum(1) >= obs - 1e-12).mean())


def simulate_season(rng, shares, f, truth):
    """One synthetic 2027 season; returns per-event summed Brier differences (baseline - forecast)."""
    n = rng.poisson(shares["events_per_season"])
    diffs = []
    for _ in range(n):
        c = "HU" if rng.random() < shares["hu"] else "TS"
        d = 0.0
        p1, b1 = f[("Q1", c)]
        y = rng.random() < truth[("Q1", c)]
        d += (b1 - y) ** 2 - (p1 - y) ** 2
        if y and rng.random() < shares["measured_given_dr"]:
            g = "major" if rng.random() < shares["major"] else "minor"
            for q in QUESTIONS:
                p, b = f[(q, g)]
                yq = rng.random() < truth[(q, g)]
                d += (b - yq) ** 2 - (p - yq) ** 2
        diffs.append(d)
    return diffs


def main():
    rows = list(csv.DictReader(open(TABLE)))
    rows = [r for r in rows if 2015 <= int(r["ev_season"]) <= 2025]
    fc, pooled, n_major, n_minor = fit(rows)
    fields = ["forecast_id", "registered", "domain", "question", "applies_to", "class", "k", "n",
              "p_forecast", "p_baseline", "resolve_when", "score", "protocol"]
    with open(LEDGER, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(fields)
        for i, (q, text, label, k, n, p, b) in enumerate(fc, 1):
            w.writerow([f"L2027-{i:02d}", REGISTERED, "hurricane loop (Atlantic, US landfall, HU+TS)",
                        f"{q}: {text}", "each 2027 event of the HU+TS set (LOOP_PROTOCOL §2, §16)", label,
                        k, n, f"{p:.4f}", f"{b:.4f}", RESOLVE,
                        "Brier; deciding baseline p_baseline (pooled classes); 0.5 reported, no weight; "
                        "one-sided sign-flip on per-event summed differences, p < 0.05",
                        "docs/LOOP_PROTOCOL.md §21"])
    digest = hashlib.sha256(LEDGER.read_bytes()).hexdigest()
    (ROOT / "data/loop_forecast_ledger.sha256").write_text(f"{digest}  data/loop_forecast_ledger.csv\n")
    print("2027 loop forecasts (docs/LOOP_PROTOCOL.md §21). Fit on 2015-2025 rows of loop_events.csv.")
    print(f"measured storms: V >= {MAJOR_KT} kt {n_major}, < {MAJOR_KT} kt {n_minor}; Q2-Q5 pooled: {pooled}")
    for i, (q, _, label, k, n, p, b) in enumerate(fc, 1):
        print(f"L2027-{i:02d} {q} [{label}] k/n {k}/{n} p {p:.3f} baseline {b:.3f}")
    print(f"ledger sha256 {digest}")

    # synthetic check of the scoring test (counts and the probabilities above only)
    f, truth_alt, truth_null = {}, {}, {}
    for q, _, label, _, _, p, b in fc:
        if q == "Q1":
            groups = [label.split("= ")[1]]
        elif pooled:
            groups = ["major", "minor"]
        else:
            groups = ["major" if ">=" in label else "minor"]
        for g in groups:
            f[(q, g)] = (p, b)
            truth_alt[(q, g)], truth_null[(q, g)] = p, b
    n_dr = sum(bool(r["dc_dr_number"]) for r in rows)
    meas = sum(bool(r["dc_Y_state_days"] and r["dc_Y_fed_days"]) for r in rows)
    shares = {"events_per_season": len(rows) / 11, "hu": sum(r["ev_status_t0"] == "HU" for r in rows) / len(rows),
              "measured_given_dr": meas / max(n_dr, 1), "major": n_major / max(n_major + n_minor, 1)}
    print("synthetic shares (counts): " + ", ".join(f"{k} {v:.3f}" for k, v in shares.items()))
    rng = np.random.default_rng(SEED)
    for name, truth in (("null (truth = pooled baseline)", truth_null), ("alternative (truth = forecasts)", truth_alt)):
        rej, nres = 0, []
        for _ in range(20000):
            d = simulate_season(rng, shares, f, truth)[:16]  # exact enumeration (2^n <= 65,536, §21 rule 5)
            rej += sign_flip_p(d) < 0.05
            nres.append(len(d))
        print(f"{name}, one season: rejection {rej / 20000:.3f} (events median {int(np.median(nres))})")


if __name__ == "__main__":
    main()
