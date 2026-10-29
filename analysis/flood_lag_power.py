"""Flood lag description (H3 in floods): exact error rate and power of the measurability rule.

Session 2.11d-ext, 29 Oct 2026. Class: infrastructure (no data read). Committed before its run.
Protocol: docs/FLOOD_LOOP_PROTOCOL.md §11.

Rule (registered): K = activated episodes (§3, activation in [d0, d0 + 30]); M = those whose
lag is measurable (activationTime and eventTime present, eventTime date in [d0 - 3, d0 + 30]).
PASS iff K >= 5 and the exact one-sided 95% Clopper-Pearson lower bound of M/K > 0.5;
FAIL iff K >= 5 and the one-sided 95% upper bound < 0.5; otherwise "not shown at this size".
Model: K ~ Binomial(N, base), M | K ~ Binomial(K, q). Exact sums, no simulation.
"""

from scipy.stats import beta, binom


def lower(m, k):
    return 0.0 if m == 0 else beta.ppf(0.05, m, k - m + 1)


def upper(m, k):
    return 1.0 if m == k else beta.ppf(0.95, m + 1, k - m)


def probs(n, base, q):
    p_pass = p_fail = 0.0
    for k in range(5, n + 1):
        pk = binom.pmf(k, n, base)
        for m in range(k + 1):
            pm = pk * binom.pmf(m, k, q)
            if lower(m, k) > 0.5:
                p_pass += pm
            elif upper(m, k) < 0.5:
                p_fail += pm
    return p_pass, p_fail


def main():
    ns = [20, 30, 40, 45]
    for base in [0.3, 0.5]:
        print(f"activation share of episodes {base}")
        for q in [0.5, 0.7, 0.8, 0.9, 1.0]:
            row = "  ".join("N{} pass {:.3f} fail {:.3f}".format(n, *probs(n, base, q)) for n in ns)
            print(f"  q {q}: {row}")
        print("  q 0.3 (wrong-pass check): " + "  ".join(
            "N{} pass {:.3f} fail {:.3f}".format(n, *probs(n, base, 0.3)) for n in ns))


if __name__ == "__main__":
    main()
