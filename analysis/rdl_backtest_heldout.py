"""Single run of the held-out case (leaded petrol, 2002-09). Inputs: docs/RDL_BACKTEST_INPUTS.md section C."""
from emo.remedy.backtest import StructureInputs, run_backtest
from emo.remedy.bottlenecks import classify_bottlenecks

BIND = {"binding_regulation", "finance_transfer", "trade_measures", "substitute_support"}
def prof(dep, **k):
    base = dict(validation_score=1.0, translation_score=0.5, budget_score=0.25,
                deployment_score=dep, persistence_score=0.5, contradiction_score=0.25)
    return classify_bottlenecks(domain="leaded_petrol", jurisdiction="global", **base)
cl = classify_bottlenecks(domain="climate_1997", jurisdiction="global", validation_score=0.75, translation_score=0.5,
                          budget_score=0.5, deployment_score=0.25, persistence_score=0.5, contradiction_score=0.75)
c = run_backtest(cl, StructureInputs(20, 0.25, 0.10))
print(f"climate_1997 reference: gain={c.predicted_gain} quality={c.predicted_gain/c.gap:.3f}")
for label, n, dep in (("PRIMARY", 117, 0.75), ("sens n=30", 30, 0.75), ("sens dep=1.0", 117, 1.0), ("sens both", 30, 1.0)):
    p = prof(dep); r = run_backtest(p, StructureInputs(n, 0.75, 0.001)); top = [k for k, _ in r.top3]
    print(f"{label:13s} dominant={p.dominant_bottlenecks} gap={r.gap} gain={r.predicted_gain} quality={r.predicted_gain/r.gap:.3f} top3={r.top3}")
    print(f"{'':13s} discrimination={r.predicted_gain > c.predicted_gain} resemblance={len(BIND & set(top)) >= 2} pledges_in_top3={'voluntary_pledges' in top}")
