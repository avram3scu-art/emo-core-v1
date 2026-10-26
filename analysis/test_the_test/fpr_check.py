import numpy as np, sweep_trial as st
st.R = 2000; BATCH = 5   # 10,000 trials per cell
rng = np.random.default_rng(20261028)
base = dict(icc=.10, rho=.60, rel=.80, fidelity=.90, contam=.10, att_rate=.15, size_sd=4, k=1)
cells = {"optimistic (full)": base,
         "optimistic, equal sizes": dict(base, size_sd=0),
         "optimistic, no attrition": dict(base, att_rate=0),
         "optimistic, equal sizes + no attrition": dict(base, size_sd=0, att_rate=0)}
for G in (80, 160):
    for name, kw in cells.items():
        r = np.array([[st.run_cell(rng, 0.0, G=G, **kw)[m] for m in ("primary","RI","CR")] for _ in range(BATCH)]).mean(0)
        se = np.sqrt(.05*.95/(st.R*BATCH))
        print(f"G={G:3d} {name:40s} primary {r[0]:.4f}  RI {r[1]:.4f}  CR {r[2]:.4f}  (SE {se:.4f})", flush=True)
