"""SMF v2 on the 2026 NHC season (docs/SMF_PROTOCOL.md §15). Run once, on committed sources.

Refuses if data/smf_v2_nhc2026/sources/ is incomplete (sources are fetched by
scripts/fetch_smf_v2_nhc.py, not before 2027-05-01). Output: results/smf_v2_nhc2026/.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from emo.loop_hurricanes import parse_hurdat2  # noqa: E402
from emo.smf_nhc import ALPHA, DM_LAGS, MIN_STORMS, build_pairs, parse_adeck_base, parse_error_file, score  # noqa: E402

SRC = ROOT / "data" / "smf_v2_nhc2026" / "sources"
OUT = ROOT / "results" / "smf_v2_nhc2026"
FILES = ("nhc_errors_2026.csv", "hurdat2_2026.csv", "adeck_ocd5_2026.csv")


def rows(name: str) -> list[dict[str, str]]:
    with open(SRC / name, newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [f for f in FILES if not (SRC / f).exists()]
    if missing:
        print(f"refused: sources missing {missing}; fetch them with scripts/fetch_smf_v2_nhc.py (not before 2027-05-01)")
        return 2
    errs = parse_error_file((int(r["line"]), r["text"]) for r in rows(FILES[0]))
    storms = parse_hurdat2((int(r["line"]), r["text"]) for r in rows(FILES[1]))
    by: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for r in rows(FILES[2]):
        by[r["stmid"]].append((int(r["line"]), r["text"]))
    bases = {s: parse_adeck_base(v) for s, v in by.items()}
    pairs = build_pairs(errs, storms, bases, 2026)
    tests = score(pairs)

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pairs.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stmid", "t", "lead", "var", "ofcl", "ocd5", "err_line", "adeck_line"])
        for p in pairs:
            w.writerow([p.stmid, p.t.isoformat(), p.lead, p.var, f"{p.ofcl:.1f}", f"{p.base:.1f}", p.err_line, p.adeck_line])
    lines = [f"SMF v2, NHC 2026 season (docs/SMF_PROTOCOL.md §15): OFCL vs OCD5, storm means, DM-HLN lags {DM_LAGS}, "
             f"one-sided, Holm alpha {ALPHA}, min storms {MIN_STORMS}",
             f"{'test':14s} {'forecasts':>9s} {'storms':>6s} {'skill':>7s} {'mean_d':>8s} {'HLN':>7s} {'p':>8s} {'p_Holm':>8s}  verdict"]
    for t in tests:
        lines.append(f"{t.name:14s} {t.n:9d} {t.n_units:6d} {t.skill:7.3f} {t.mean_d:8.2f} {t.hln:7.2f} {t.p:8.4f} "
                     f"{t.p_holm:8.4f}  {t.verdict}")
    lines.append("Correlation extra: not computed (the error file holds errors, not forecasts; §15 rule 7).")
    (OUT / "result.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
