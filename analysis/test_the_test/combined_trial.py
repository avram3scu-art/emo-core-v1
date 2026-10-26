"""
THE SCIENCE OF TRUTH - combined departures and sample-size curve.

Three illustrative planning profiles combine several Section 9
departures at once. Teachers teach 2 classes (randomised and analysed
at teacher level) in the moderate and pessimistic profiles.
Differential attrition is reported separately as a bias check, since
more classrooms cannot cure bias.

All profile values are assumptions for planning, not estimates.
"""
import csv
import numpy as np
import sweep_trial as st

st.R = 1000
SEED = 20261027

PROFILES = {
    "optimistic": dict(icc=.10, rho=.60, rel=.80, fidelity=.90, contam=.10,
                       att_rate=.15, size_sd=4, k=1),
    "moderate": dict(icc=.15, rho=.50, rel=.70, fidelity=.80, contam=.20,
                     att_rate=.15, size_sd=4, k=2, teacher_var=.03,
                     teacher_level=True),
    "pessimistic": dict(icc=.20, rho=.40, rel=.60, fidelity=.70, contam=.30,
                        att_rate=.20, size_sd=6, k=2, teacher_var=.05,
                        teacher_level=True),
}
CLASSROOMS = (80, 120, 160, 240, 320)


def main():
    rng = np.random.default_rng(SEED)
    rows = []
    print(f"{'profile':12s} {'G':>4s} {'tau':>4s} {'ITT':>5s} {'prim':>6s} {'RI':>6s} {'bias':>7s} {'cover':>6s}")
    for name, kw in PROFILES.items():
        for G in CLASSROOMS:
            for tau in (0.0, 0.2):
                o = st.run_cell(rng, tau, G=G, **kw)
                rows.append(dict(profile=name, G=G, tau=tau, **o))
                print(f"{name:12s} {G:4d} {tau:4.2f} {o['target']:5.3f} "
                      f"{o['primary']:6.3f} {o['RI']:6.3f} {o['bias']:+7.3f} "
                      f"{o['coverage']:6.3f}", flush=True)
    print("\nBias check: moderate profile + 15% differential attrition")
    for G in (80, 320):
        kw = dict(PROFILES["moderate"], att_mech="differential")
        o = st.run_cell(rng, 0.0, G=G, **kw)
        rows.append(dict(profile="moderate+diff15", G=G, tau=0.0, **o))
        print(f"moderate+diff {G:4d} 0.00 FPR primary {o['primary']:.3f}  "
              f"bias {o['bias']:+.3f}  coverage {o['coverage']:.3f}", flush=True)
    with open("combined_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
