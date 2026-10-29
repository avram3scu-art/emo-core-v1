"""Loop power, amendment 2 (docs/LOOP_PROTOCOL.md §13): season clustering in the predicted direction.

Synthetic only; reads no file. Functions imported unchanged from analysis/loop_power.py.
"""
import importlib.util
from pathlib import Path

import numpy as np

_spec = importlib.util.spec_from_file_location("loop_power", Path(__file__).with_name("loop_power.py"))
lp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lp)

SEED = 2026102925


def main():
    rng = np.random.default_rng(SEED)
    lp._COEF.update({0.5: 1.885})   # §10 calibration (found with Y_SHOCK_SIGN = 1)
    lp.KAPPA, lp.Y_SHOCK_SIGN = 0.9, -1.0
    print("Loop power amendment 2 (docs/LOOP_PROTOCOL.md §13). Synthetic only; no loop record read.")
    print(f"seed {SEED}, {lp.REPS} studies/cell, {lp.PERMS} permutations, KAPPA {lp.KAPPA}, "
          f"Y_SHOCK_SIGN {lp.Y_SHOCK_SIGN}\n")
    for sig in (0.7, 1.5, 2.5):
        lp.SIG_SEASON = sig
        for name, sizes in (("HU", lp.SIZES_HU), ("HU+TS", lp.SIZES_HUTS)):
            w, _, _ = lp.h4_cell(rng, sizes, 0.0)
            nv, _, _ = lp.h4_cell(rng, sizes, 0.0, naive=True)
            _, pw, _ = lp.h4_cell(rng, sizes, 0.5)
            h5 = lp.h5_cell(rng, sizes, 0.0)
            print(f"SIG_SEASON {sig} {name:6s}: H4 FPR within {w:.3f} | naive {nv:.3f} | "
                  f"power r=0.5 within {pw:.3f} | H5 FPR {h5:.3f}", flush=True)


if __name__ == "__main__":
    main()
