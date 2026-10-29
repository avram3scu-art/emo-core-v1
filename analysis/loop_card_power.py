"""False-positive rate and power of the H3 stream test (docs/LOOP_CARD_PROTOCOL.md §9).

Synthetic only (infrastructure). Units arrive in clusters (same ISO3, hazard, month):
cluster sizes are 1 + Poisson(0.25); within a cluster the measurability probability is
drawn from a Beta with mean p and intra-cluster correlation 0.2. The number of units is
Poisson(lam). Uses emo.stream.cards.h3_score, the registered decision rule.

  python analysis/loop_card_power.py > analysis/loop_card_power_output.txt
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from emo.stream.cards import h3_score  # noqa: E402

REPS, ICC, SEED = 4000, 0.2, 0


def sample(rng, lam, p):
    n_target = rng.poisson(lam)
    units, cid = [], 0
    a = p * (1 - ICC) / ICC
    b = (1 - p) * (1 - ICC) / ICC
    while len(units) < n_target:
        size = 1 + rng.poisson(0.25)
        pc = rng.beta(a, b)
        for _ in range(size):
            units.append({"measurable": bool(rng.random() < pc), "cluster": (cid,)})
        cid += 1
    return units[:n_target]


def main():
    rng = np.random.default_rng(SEED)
    print(f"reps {REPS}, ICC {ICC}, seed {SEED}")
    print("lam  p     PASS   FAIL   undecided  not_testable")
    for lam in (30, 45, 60, 90):
        for p in (0.4, 0.5, 0.6, 0.7, 0.8):
            v = [h3_score(sample(rng, lam, p))["verdict"] for _ in range(REPS)]
            f = {k: v.count(k) / REPS for k in ("PASS", "FAIL", "not decided at this size",
                                                 "not testable at this size")}
            print(f"{lam:<4} {p:<5} {f['PASS']:.3f}  {f['FAIL']:.3f}  "
                  f"{f['not decided at this size']:.3f}      {f['not testable at this size']:.3f}")


if __name__ == "__main__":
    main()
