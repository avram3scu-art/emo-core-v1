"""Loop power, amendment 3 (docs/LOOP_PROTOCOL.md §14): season fixed-effect statistic.

Synthetic only; reads no file. Functions from analysis/loop_power.py with STAT = "fe".
"""
import importlib.util
from pathlib import Path

import numpy as np

_spec = importlib.util.spec_from_file_location("loop_power", Path(__file__).with_name("loop_power.py"))
lp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lp)

SEED = 2026102926


def main():
    rng = np.random.default_rng(SEED)
    lp.STAT, lp.Y_SHOCK_SIGN = "fe", -1.0
    coefs = {r: lp.coupling_coef(r) for r in (0.3, 0.5)}
    print("Loop power amendment 3 (docs/LOOP_PROTOCOL.md §14). Synthetic only; no loop record read.")
    print(f"seed {SEED}, {lp.REPS} studies/cell, {lp.PERMS} permutations, STAT fe, Y_SHOCK_SIGN -1")
    print("coupling coefficient (fe statistic): " + ", ".join(f"r={r}: c={c:.3f}" for r, c in coefs.items()))
    print("\n(a) section 9 world (KAPPA 0.5, SIG_SEASON 0.7): any | true pair | 'no effect' on true pair")
    for name, sizes, p_drop in (("HU", lp.SIZES_HU, 0.0), ("HU 25% unmatched", lp.SIZES_HU, 0.25),
                                ("HU+TS", lp.SIZES_HUTS, 0.0)):
        for r in (0.0, 0.3, 0.5):
            a, t, e = lp.h4_cell(rng, sizes, r, p_drop)
            print(f"  {name:17s} r={r:.1f}: any {a:.3f} | true {t:.3f} | no-effect {e:.3f}", flush=True)
    for bs in ((4,), (6,), (4, 4, 4), (4, 4, 4, 4, 4)):
        for r in (0.0, 0.5):
            print(f"  blind sizes {str(bs):16s} r={r:.1f}: {lp.blind_cell(rng, bs, r):.3f}", flush=True)
    print("\n(b) stress (KAPPA 0.9): any rejection")
    lp.KAPPA = 0.9
    for sig in (1.5, 2.5):
        lp.SIG_SEASON = sig
        for name, sizes in (("HU", lp.SIZES_HU), ("HU+TS", lp.SIZES_HUTS)):
            for r in (0.0, 0.5):
                a, t, _ = lp.h4_cell(rng, sizes, r)
                print(f"  SIG_SEASON {sig} {name:6s} r={r:.1f}: any {a:.3f} | true {t:.3f}", flush=True)


if __name__ == "__main__":
    main()
