"""Single run of the RDL v0.3 held-out pair. Inputs: docs/RDL_BACKTEST_INPUTS.md section D."""
import itertools
from emo.remedy.backtest import StructureInputs, run_backtest_v03
from emo.remedy.bottlenecks import classify_bottlenecks
K = ("validation", "translation", "budget", "deployment", "persistence", "contradiction")
def prof(name, sc): return classify_bottlenecks(domain=name, jurisdiction="global", **{f"{k}_score": v for k, v in zip(K, sc)})
CLIMATE97 = 0.182
s = run_backtest_v03(prof("sulphur", (0.75, 0.5, 0.25, 0.75, 0.5, 0.75)), StructureInputs(10, 0.5, 0.10))
a = run_backtest_v03(prof("chrysotile", (1.0, 0.5, 0.25, 0.25, 0.5, 0.75)), StructureInputs(8, 0.5, 0.001))
for n, r in (("sulphur_1985", s), ("chrysotile_2004", a)):
    print(f"{n:16s} gap={r.remaining_gap} tractability={r.tractability} top3={r.top3}")
print(f"PRIMARY: sulphur > chrysotile: {s.tractability > a.tractability}; sulphur > climate_1997 ({CLIMATE97}): {s.tractability > CLIMATE97}")
print("\nSensitivity (pre-stated values):")
for sn, ssub, ssh, asub in itertools.product((10, 12), (0.5, 0.25), (0.10, 0.02), (0.5, 0.75)):
    ts = run_backtest_v03(prof("s", (0.75, 0.5, 0.25, 0.75, 0.5, 0.75)), StructureInputs(sn, ssub, ssh)).tractability
    ta = run_backtest_v03(prof("a", (1.0, 0.5, 0.25, 0.25, 0.5, 0.75)), StructureInputs(8, asub, 0.001)).tractability
    print(f"  sulphur n={sn} sub={ssub} share={ssh} -> {ts} | chrysotile sub={asub} -> {ta} | s>a {ts > ta} | s>clim97 {ts > CLIMATE97}")
