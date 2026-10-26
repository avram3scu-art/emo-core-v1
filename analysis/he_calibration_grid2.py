"""He calibration, amendment 1 (docs/HE_CALIBRATION_PROTOCOL.md section 7).

Uses the functions of analysis/he_calibration.py unchanged. Synthetic data only. Run once.
"""
import importlib.util
from itertools import product
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location("hc", Path(__file__).with_name("he_calibration.py"))
hc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hc)

SEED = 20261030
PARTS = {
    "A": ((22, 24, 26, 28), (0.0, 0.5)),
    "B": ((40, 60), (0.0, 0.3)),
}


def main():
    rng = np.random.default_rng(SEED)
    tests = ("T-A", "T-B", "T-C", "T-D")
    res = {}
    print("He calibration, amendment 1 (protocol section 7). Synthetic data only.")
    print(f"seed {SEED}, {hc.REPS} studies/cell, {hc.PERMS} permutations\n")
    print(f"{'part':>4} {'n':>3} {'m':>2} {'beta':>5} {'lam':>4} " + " ".join(f"{t:>6}" for t in tests))
    for part, (ns, betas) in PARTS.items():
        for n in ns:
            hc.CHUNK = 100 if n <= 30 else 20
            cdf = hc.mahonian_cdf(n)
            for m, beta, lam in product(hc.MS, betas, hc.LAMBDAS):
                r = hc.run_cell(rng, n, m, beta, lam, cdf)
                res[(n, m, beta, lam)] = r
                print(f"{part:>4} {n:3d} {m:2d} {beta:5.2f} {lam:4.1f} "
                      + " ".join(f"{r[t]:6.3f}" for t in tests), flush=True)

    print("\nPart A: T-D usable (FPR <= 0.060 at beta 0, power >= 0.80 at beta 0.5, both lambda)")
    for m in hc.MS:
        ok = [n for n in PARTS["A"][0]
              if all(res[(n, m, 0.0, lam)]["T-D"] <= 0.060 for lam in hc.LAMBDAS)
              and all(res[(n, m, 0.5, lam)]["T-D"] >= 0.80 for lam in hc.LAMBDAS)]
        print(f"m={m}: usable at n = {ok if ok else 'none of 22-28'}")
    print("\nPart B: T-D at beta 0.3 (power >= 0.80 and FPR <= 0.060, both lambda)")
    for m in hc.MS:
        for n in PARTS["B"][0]:
            fpr_ok = all(res[(n, m, 0.0, lam)]["T-D"] <= 0.060 for lam in hc.LAMBDAS)
            pw = [res[(n, m, 0.3, lam)]["T-D"] for lam in hc.LAMBDAS]
            print(f"m={m} n={n}: FPR ok = {fpr_ok}; power (lam 0, 0.5) = {pw[0]:.3f}, {pw[1]:.3f}; "
                  f"reaches 0.80 = {min(pw) >= 0.80}")


if __name__ == "__main__":
    main()
