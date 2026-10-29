"""Loop power, amendment 1 (docs/LOOP_PROTOCOL.md §12): stressed season clustering.

Synthetic only; reads no file. Functions imported unchanged from analysis/loop_power.py.
"""
import importlib.util
from pathlib import Path

import numpy as np

_spec = importlib.util.spec_from_file_location("loop_power", Path(__file__).with_name("loop_power.py"))
lp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lp)

SEED = 2026102924


def main():
    rng = np.random.default_rng(SEED)
    lp.KAPPA = 0.9
    print("Loop power amendment 1 (docs/LOOP_PROTOCOL.md §12). Synthetic only; no loop record read.")
    print(f"seed {SEED}, {lp.REPS} studies/cell, {lp.PERMS} permutations, KAPPA {lp.KAPPA}\n")
    for sig in (1.5, 2.5):
        lp.SIG_SEASON = sig
        for name, sizes in (("HU", lp.SIZES_HU), ("HU+TS", lp.SIZES_HUTS)):
            w, _, _ = lp.h4_cell(rng, sizes, 0.0)
            nv, _, _ = lp.h4_cell(rng, sizes, 0.0, naive=True)
            h5 = lp.h5_cell(rng, sizes, 0.0)
            print(f"SIG_SEASON {sig} {name:6s}: H4 within-season {w:.3f} | H4 naive {nv:.3f} | H5 {h5:.3f}",
                  flush=True)


if __name__ == "__main__":
    main()
