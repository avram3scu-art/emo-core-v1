"""Score the RDL forecast ledger (data/rdl_forecast_ledger.csv) against resolved outcomes.

Outcomes go in data/rdl_forecast_outcomes.csv (forecast_id,resolved_on,outcome[1/0],source) and are added only
after each resolve_by date. The ledger itself is never edited; corrections are new forecasts with new ids.
Score: Brier score of p_forecast vs a constant 0.5 baseline (lower is better)."""
import csv, os
L = {r["forecast_id"]: r for r in csv.DictReader(open("data/rdl_forecast_ledger.csv"))}
path = "data/rdl_forecast_outcomes.csv"
O = {r["forecast_id"]: r for r in csv.DictReader(open(path))} if os.path.exists(path) else {}
done = [(float(L[k]["p_forecast"]), int(O[k]["outcome"])) for k in O if k in L]
print(f"{len(L)} forecasts registered, {len(done)} resolved")
if done:
    b = sum((p - y) ** 2 for p, y in done) / len(done); b0 = sum((0.5 - y) ** 2 for _, y in done) / len(done)
    print(f"Brier RDL {b:.3f} vs baseline 0.5 {b0:.3f} -> {'RDL better' if b < b0 else 'RDL not better'}")
