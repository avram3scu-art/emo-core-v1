"""Run the pre-registered RDL backtest (docs/RDL_BACKTEST_PROTOCOL.md) on inputs in docs/RDL_BACKTEST_INPUTS.md."""
from emo.remedy.backtest import StructureInputs, run_backtest
from emo.remedy.bottlenecks import classify_bottlenecks

PROFILES = {
    "ozone_1985":   dict(validation_score=0.5,  translation_score=0.25, budget_score=0.25, deployment_score=0.25, persistence_score=0.5, contradiction_score=0.25),
    "climate_1997": dict(validation_score=0.75, translation_score=0.5,  budget_score=0.5,  deployment_score=0.25, persistence_score=0.5, contradiction_score=0.75),
    "climate_2015": dict(validation_score=1.0,  translation_score=0.5,  budget_score=0.5,  deployment_score=0.0,  persistence_score=0.5, contradiction_score=0.75),
}
STRUCTURE = {
    "ozone_1985":   StructureInputs(12, 0.5, 0.005),
    "climate_1997": StructureInputs(20, 0.25, 0.10),
    "climate_2015": StructureInputs(19, 0.5, 0.10),
}
BINDING_SET = {"binding_regulation", "finance_transfer", "trade_measures", "substitute_support"}

res = {}
for case, sc in PROFILES.items():
    p = classify_bottlenecks(domain=case, jurisdiction="global", **sc)
    for mode, s in (("no_structure", None), ("structure", STRUCTURE[case])):
        r = run_backtest(p, s); res[(case, mode)] = r
        print(f"{case:13s} {mode:13s} dominant={p.dominant_bottlenecks} gap={r.gap} gain={r.predicted_gain} top3={r.top3}")

def verdict(mode):
    oz, cl = res[("ozone_1985", mode)], res[("climate_1997", mode)]
    disc = oz.predicted_gain > cl.predicted_gain
    top_oz = [k for k, _ in oz.top3]
    resem = len(BINDING_SET.intersection(top_oz)) >= 2
    pledge_fail = [c for c in PROFILES if "voluntary_pledges" in [k for k, _ in res[(c, mode)].top3]]
    print(f"\n[{mode}] discrimination ozone>climate97: {disc} ({oz.predicted_gain} vs {cl.predicted_gain})")
    print(f"[{mode}] resemblance (>=2 of ozone top3 in binding set): {resem} {top_oz}")
    print(f"[{mode}] pledges in top3 for: {pledge_fail or 'none'}")
verdict("no_structure"); verdict("structure")
