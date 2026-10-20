"""
RDL v0.4 test against independently coded regime data (docs/RDL_V04_PROTOCOL.md).

Usage: python3 analysis/rdl_v04_test.py components.csv
Category directions are in CODEBOOK below. They must be filled from the codebook and committed
BEFORE the data file is opened; until then they hold placeholders and the script refuses real data.
"""
from __future__ import annotations
import csv, random, sys
from statistics import mean

# ---- To be filled from the codebook, in its own commit, before opening the data ----
CODEBOOK = {
    "confirmed": False,                 # set True only in the codebook commit
    "malignancy_benign_sums": {1, 2},   # Var15 (+Var18+Var28 if Var15>=3) sums counted as benign
    "veto_codes_var40a": {1},           # Var40a codes meaning unanimity/consensus
    "var66_close_to_optimum": 1,        # which Var66 recode (1 or 2) means close to the optimum
}
DEVELOPMENT_REGIMES = ("ozone", "lrtap")   # matched case-insensitively in the 'regime' column


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def indicators(r: dict) -> dict:
    v = {k: _num(r.get(k)) for k in ("var15", "var18", "var28", "var40a", "var43", "var44", "var45", "var58")}
    out = {}
    if v["var15"] is not None:
        s = v["var15"]
        if s >= 3 and v["var18"] is not None and v["var28"] is not None:
            s += (0 if v["var18"] == 1 else 1) + (1 if v["var28"] in (3, 4) else 0)
        out["benign"] = 1 if int(s) in CODEBOOK["malignancy_benign_sums"] else 0
    if v["var40a"] is not None and v["var40a"] != 4:
        out["no_veto"] = 0 if int(v["var40a"]) in CODEBOOK["veto_codes_var40a"] else 1
    caps = [None if v[k] is None else int(hi) for k, hi in (
        ("var44", v["var44"] is not None and v["var44"] > 2),
        ("var45", v["var45"] is not None and v["var45"] != 1),
        ("var43", v["var43"] is not None and v["var43"] != 0))]
    caps = [c for c in caps if c is not None]
    if len(caps) >= 2:
        out["capacity"] = 1 if sum(caps) >= 2 else 0
    if v["var58"] is not None:
        out["low_uncertainty"] = 1 if v["var58"] <= 2 else 0
    return out


def tractability(r: dict):
    ind = indicators(r)
    return (mean(ind.values()) if len(ind) >= 3 else None), ind


def outcome(r: dict, which: str):
    x = _num(r.get(which))
    if x is None:
        return None
    if which == "var63":
        return 1 if x <= 2 else 2
    rec = 1 if x == 1 else 2
    return 2 if rec == CODEBOOK["var66_close_to_optimum"] else 1   # 2 = better


def _ranks(a):
    order = sorted(range(len(a)), key=lambda i: a[i]); r = [0.0] * len(a); i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[order[j + 1]] == a[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = _ranks(x), _ranks(y); mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def perm_p(x, y, stat, n=10000, seed=0):
    rng = random.Random(seed); obs = stat(x, y); y2 = list(y); hits = 0
    for _ in range(n):
        rng.shuffle(y2)
        hits += stat(x, y2) >= obs
    return obs, (hits + 1) / (n + 1)


def diff_means(g, y):  # mean outcome without veto minus with veto
    a = [b for f, b in zip(g, y) if f == 1]; c = [b for f, b in zip(g, y) if f == 0]
    return (mean(a) - mean(c)) if a and c else 0.0


def analyse(rows, label):
    print(f"\n== {label}: {len(rows)} components")
    for which, name in (("var63", "H1 behavioural change"), ("var66", "H2 problem-solving")):
        d = [(t, outcome(r, which)) for r in rows for t in [tractability(r)[0]] if t is not None and outcome(r, which) is not None]
        if len(d) < 8:
            print(f"{name}: too few usable components ({len(d)})"); continue
        rho, p = perm_p([a for a, _ in d], [b for _, b in d], spearman)
        print(f"{name}: n={len(d)} rho={rho:.3f} p={p:.4f} -> {'PASS' if p < 0.05 and rho > 0 else 'not shown'}")
    d = [(tractability(r), outcome(r, "var63")) for r in rows]
    d = [(t, i, y) for (t, i), y in d if t is not None and y is not None]
    if d and all("benign" in i for _, i, _ in d):
        rt = spearman([t for t, _, _ in d], [y for _, _, y in d]); rb = spearman([i["benign"] for _, i, _ in d], [y for _, _, y in d])
        print(f"H3 T vs benign alone: rho_T={rt:.3f} rho_benign={rb:.3f} -> {'T adds' if rt > rb else 'T adds nothing'}")
    v = [(i["no_veto"], y) for _, i, y in d if "no_veto" in i]
    if v:
        diff, p = perm_p([a for a, _ in v], [b for _, b in v], diff_means)
        print(f"H4 no-veto minus veto mean behavioural change: {diff:.3f} p={p:.4f}")


def main(path):
    if not CODEBOOK["confirmed"] and not path.startswith("synthetic"):
        sys.exit("Codebook directions not confirmed and committed. Refusing to open real data.")
    rows = list(csv.DictReader(open(path)))
    analyse(rows, "all components")
    dev = lambda r: any(k in r.get("regime", "").lower() for k in DEVELOPMENT_REGIMES)
    analyse([r for r in rows if not dev(r)], "without development regimes (VERDICT)")


if __name__ == "__main__":
    main(sys.argv[1])
