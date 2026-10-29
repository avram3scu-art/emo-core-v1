"""He direction test on the hurricane loop, 2015-2025 (docs/HE_CALIBRATION_PROTOCOL.md §10).

Pre-registered on known history. Run once; output analysis/he_loop_test_output.txt.
Also writes the UIA 2.0 profile table data/uia2_hurricanes_profile.csv (UIA_PROTOCOL §2.0).
"""
from pathlib import Path

import numpy as np

from emo.uia2 import LETTERS, profile_rows, write_profile

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data/loop_hurricanes/loop_events.csv"
PROFILE = ROOT / "data/uia2_hurricanes_profile.csv"
SEED = 2026102990
PERMS = 9999
ALPHA = 0.05


def tau_a(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    i, j = np.triu_indices(len(x), 1)
    return float((np.sign(x[i] - x[j]) * np.sign(y[i] - y[j])).sum() / len(i))


def td(he, L):
    return float(np.mean([tau_a(l, he) for l in L]))


def perm_p(rng, he, L, season, within):
    obs = td(he, L)
    count = 0
    for _ in range(PERMS):
        hp = he.copy()
        if within:
            for s in np.unique(season):
                idx = np.flatnonzero(season == s)
                hp[idx] = he[rng.permutation(idx)]
        else:
            hp = rng.permutation(he)
        count += td(hp, L) >= obs - 1e-12
    return obs, (1 + count) / (PERMS + 1)


def main():
    rows = profile_rows(EVENTS)
    assert all(2015 <= r["season"] <= 2025 for r in rows), "season outside 2015-2025"
    write_profile(rows, PROFILE)
    cases = [r for r in rows if r["He"] is not None and all(r[k] is not None for k in LETTERS)]
    cases.sort(key=lambda r: (r["season"], r["atcf"]))
    season = np.array([r["season"] for r in cases])
    he = np.array([r["He"] for r in cases])
    L = [np.array([r[k] for r in cases]) for k in LETTERS]
    sizes = {int(s): int((season == s).sum()) for s in np.unique(season)}

    print("He direction test, hurricane loop 2015-2025 (HE_CALIBRATION_PROTOCOL §10).")
    print("Evidence class: pre-registered on known history.")
    print(f"Profile rows written: {len(rows)} -> {PROFILE.relative_to(ROOT)}")
    print(f"Cases (He, F, A, W present): {len(cases)}; seasons {sizes}\n")

    rng = np.random.default_rng(SEED)
    t, p = perm_p(rng, he, L, season, within=True)
    print(f"PRIMARY  T-D = {t:+.4f}, within-season permutation p = {p:.4f} "
          f"({PERMS} perms, seed {SEED}); alpha {ALPHA}: {'PASS' if p < ALPHA else 'not significant'}")

    print("\nDescriptive, no weight:")
    for k, l in zip(LETTERS, L):
        print(f"  tau({k}, He) = {tau_a(l, he):+.3f}")
    years = season.astype(float)
    V = np.array([r["V_kt"] for r in cases])
    for k, l in zip(LETTERS, L):
        print(f"  shared trend: tau({k}, year) = {tau_a(l, years):+.3f}; severity: tau({k}, V) = {tau_a(l, V):+.3f}")
    print(f"  tau(He, year) = {tau_a(he, years):+.3f}; tau(He, V) = {tau_a(he, V):+.3f}")
    inter = [tau_a(L[a], L[b]) for a in range(3) for b in range(a + 1, 3)]
    print(f"  mean pairwise tau among letters = {np.mean(inter):+.3f} ({', '.join(f'{x:+.3f}' for x in inter)})")
    rng2 = np.random.default_rng(SEED + 1)
    _, p_all = perm_p(rng2, he, L, season, within=False)
    print(f"  across-all permutation p (the §3 null) = {p_all:.4f}")


if __name__ == "__main__":
    main()
