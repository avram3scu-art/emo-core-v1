"""Secondary H3 counts by event set (exploratory, after the §18 run; no weight). Session 2.5."""
import csv
from pathlib import Path

from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / "data/loop_hurricanes/loop_events.csv").open()))


def both(r):
    return r["dc_Y_state_days"] not in ("", "nan") and r["dc_Y_fed_days"] not in ("", "nan")


print("Secondary H3 counts (exploratory, seen data, no weight; docs/LOOP_PROTOCOL.md §19)")
for label, sel in (("HU set (secondary, §10)", "1"), ("TS-only storms", "0")):
    s = [r for r in rows if r["ev_hu_set"] == sel]
    k = sum(both(r) for r in s)
    print(f"  {label}: both lags {k}/{len(s)}; exact one-sided binomial p = {binomtest(k, len(s), 0.5, 'greater').pvalue:.5f}")
kinds = [r for r in rows if r["at_target_kind"] != "storm"]
print(f"  list/season attention targets: {len(kinds)}, of which with both lags: {sum(both(r) for r in kinds)}")
