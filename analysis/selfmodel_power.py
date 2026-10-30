"""False-positive rate and power of the H8 test (docs/SELF_MODEL_PROTOCOL.md §7).

Synthetic only (infrastructure). Uses the registered code: emo.selfmodel.protocol
(fit_logistic, predict, base_rate, h8_score). Each forecast has a target (D 70 %, B 30 %),
a hazard, a stage (1 or 2 for D), days since reference (exponential, mean 2), and a true
probability logit = structure + u, where u (sd SIGMA_U, 30 % shared within a cluster) is
what hazard, stage and days do not explain. Clusters: 1 + Poisson(0.25) forecasts.
Baselines are fitted on TRAIN past forecasts of the same kind.

Scenarios for the AI forecast:
  null      AI = logistic fitted on an independent past sample (same expected Brier)
  struct    AI knows the true structure, none of u, noise sd 0.5 on the logit
  rho=0.5   AI knows the structure and half of u, noise sd 0.5
  rho=0.8   AI knows the structure and 0.8 of u, noise sd 0.3

  python analysis/selfmodel_power.py > analysis/selfmodel_power_output.txt
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emo.selfmodel.protocol as P  # noqa: E402

REPS, SEED, SIGMA_U, TRAIN = 600, 1, 1.0, 150   # n=120 is N_TARGET
HAZ_P = {"EQ": .25, "TS": .02, "TC": .2, "FL": .35, "VO": .05, "DR": .05, "WF": .08}
BETA_H = {"EQ": .3, "TS": 0., "TC": .4, "FL": .2, "VO": -.8, "DR": -.5, "WF": -1.}
ALPHA_T = {"D": -.6, "B": .6}
P.N_FLIPS = P.N_BOOT = 2000          # speed only; the registered scorer uses 10,000


def draw(rng, n):
    rows, cid = [], 0
    hz, hp = list(HAZ_P), np.array(list(HAZ_P.values()))
    while len(rows) < n:
        size = 1 + rng.poisson(0.25)
        zc = rng.normal()
        h = hz[rng.choice(len(hz), p=hp / hp.sum())]
        for _ in range(size):
            t = "D" if rng.random() < .7 else "B"
            stage = (1 if rng.random() < .6 else 2) if t == "D" else 3
            days = rng.exponential(2.0)
            struct = ALPHA_T[t] + BETA_H[h] + (.4 if stage == 2 else 0) - .3 * np.log1p(days)
            u = SIGMA_U * (np.sqrt(.3) * zc + np.sqrt(.7) * rng.normal())
            p = 1 / (1 + np.exp(-(struct + u)))
            rows.append({"target": t, "hazard": h, "stage": stage, "days": days,
                         "struct": struct, "u": u, "y": int(rng.random() < p), "cluster": cid})
        cid += 1
    return rows[:n]


def fit(rows):
    return {t: P.fit_logistic([r for r in rows if r["target"] == t]) for t in P.TARGETS}


def one(rng, n, scen):
    train, test = draw(rng, TRAIN), draw(rng, n)
    m = fit(train)
    br = {t: P.base_rate(r["y"] for r in train if r["target"] == t) for t in P.TARGETS}
    m2 = fit(draw(rng, TRAIN)) if scen == "null" else None
    out = []
    for r in test:
        if scen == "null":
            pa = P.predict(m2[r["target"]], r)
        else:
            rho, tau = {"struct": (0, .5), "rho=0.5": (.5, .5), "rho=0.8": (.8, .3)}[scen]
            z = r["struct"] + rho * r["u"] + tau * rng.normal()
            pa = float(1 / (1 + np.exp(-z)))
        out.append({"y": r["y"], "p_ai": pa, "p_base": br[r["target"]],
                    "p_logit": P.predict(m[r["target"]], r), "cluster": r["cluster"]})
    return P.h8_score(out, seed=int(rng.integers(1 << 31)))["verdict"]


def main():
    rng = np.random.default_rng(SEED)
    print(f"H8 power, {REPS} reps per cell; sigma_u={SIGMA_U}; train={TRAIN}; "
          f"alpha={P.ALPHA}, margin={P.MARGIN}, min n={P.MIN_N}, min clusters={P.MIN_CLUSTERS}")
    print("scenario  n    PASS   FAIL   not-shown  not-testable")
    for scen in ("null", "struct", "rho=0.5", "rho=0.8"):
        for n in (30, 45, 60, 90, 120):
            v = [one(rng, n, scen) for _ in range(REPS)]
            f = {k: v.count(k) / REPS for k in
                 ("PASS", "FAIL", "not shown at this size", "not testable at this size")}
            print(f"{scen:8s} {n:4d}  {f['PASS']:.3f}  {f['FAIL']:.3f}  "
                  f"{f['not shown at this size']:.3f}      {f['not testable at this size']:.3f}")


if __name__ == "__main__":
    main()
