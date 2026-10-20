"""RDL v0.3 development check (docs/RDL_V03_PROTOCOL.md). Inputs from docs/RDL_BACKTEST_INPUTS.md."""
from emo.remedy.backtest import GENERIC_LIBRARY, StructureInputs, run_backtest_v03, structure_multiplier, _CAPACITY, _DELIVERY
from emo.remedy.bottlenecks import classify_bottlenecks

CASES = {
    "ozone_1985":   ((0.5, 0.25, 0.25, 0.25, 0.5, 0.25), StructureInputs(12, 0.5, 0.005)),
    "climate_1997": ((0.75, 0.5, 0.5, 0.25, 0.5, 0.75), StructureInputs(20, 0.25, 0.10)),
    "climate_2015": ((1.0, 0.5, 0.5, 0.0, 0.5, 0.75), StructureInputs(19, 0.5, 0.10)),
    "leaded_2002":  ((1.0, 0.5, 0.25, 0.75, 0.5, 0.25), StructureInputs(117, 0.75, 0.001)),
}
KEYS = ("validation", "translation", "budget", "deployment", "persistence", "contradiction")
R = {}
for name, (sc, st) in CASES.items():
    p = classify_bottlenecks(domain=name, jurisdiction="global", **{f"{k}_score": v for k, v in zip(KEYS, sc)})
    R[name] = r = run_backtest_v03(p, st)
    full = sorted(((i.option_id, round(_CAPACITY[i.required_capacity]*structure_multiplier(i, st)[0]*_DELIVERY[i.delivery_effect]*structure_multiplier(i, st)[1], 3)) for i in GENERIC_LIBRARY), key=lambda t: -t[1])
    print(f"{name:13s} gap={r.remaining_gap} tractability={r.tractability} top3={r.top3}")
    print(f"{'':13s} full ranking={full}")

def top(n): return [k for k, _ in R[n].top3]
checks = {
    "ozone tractability > climate_1997": R["ozone_1985"].tractability > R["climate_1997"].tractability,
    "leaded tractability > climate_1997": R["leaded_2002"].tractability > R["climate_1997"].tractability,
    "no pledges in any top 3": all("voluntary_pledges" not in top(n) for n in R),
    "binding regulation in leaded top 3": "binding_regulation" in top("leaded_2002"),
}
for k, v in checks.items(): print(f"{'PASS' if v else 'FAIL'}  {k}")
