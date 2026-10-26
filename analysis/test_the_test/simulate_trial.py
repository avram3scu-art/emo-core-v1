import numpy as np
from scipy.stats import t as student_t


def simulate_trial(tau, rng, n_classes=80, n_students=17, icc=0.10, rho=0.60):
    if n_classes % 2 != 0:
        raise ValueError("n_classes must be even.")
    if not 0 <= icc < 1:
        raise ValueError("icc must be in [0, 1).")
    if not 0 <= rho < 1:
        raise ValueError("rho must be in [0, 1).")

    treatment = np.repeat([0, 1], n_classes // 2)
    rng.shuffle(treatment)

    class_baseline = rng.normal(size=n_classes)
    individual_baseline = rng.normal(size=(n_classes, n_students))
    y0 = np.sqrt(icc) * class_baseline[:, None] + np.sqrt(1 - icc) * individual_baseline

    class_followup = rng.normal(size=n_classes)
    individual_followup = rng.normal(size=(n_classes, n_students))
    noise = np.sqrt(icc) * class_followup[:, None] + np.sqrt(1 - icc) * individual_followup

    y1 = rho * y0 + np.sqrt(1 - rho**2) * noise + tau * treatment[:, None]

    baseline_mean = y0.mean(axis=1)
    followup_mean = y1.mean(axis=1)

    X = np.column_stack([np.ones(n_classes), treatment, baseline_mean])
    beta = np.linalg.solve(X.T @ X, X.T @ followup_mean)
    residual = followup_mean - X @ beta
    df = n_classes - X.shape[1]
    variance = (residual @ residual) / df
    covariance = variance * np.linalg.inv(X.T @ X)
    se = np.sqrt(covariance[1, 1])
    statistic = beta[1] / se
    p_value = 2 * student_t.sf(abs(statistic), df)
    return beta[1], p_value


def run_simulation(repetitions=3000, effects=(0.00, 0.20, 0.30), seed=20261026):
    rng = np.random.default_rng(seed)
    print("THE SCIENCE OF TRUTH")
    print("INITIAL SIMULATION RESULTS")
    print("----------------------------------------")
    for tau in effects:
        results = [simulate_trial(tau, rng) for _ in range(repetitions)]
        estimates = np.array([r[0] for r in results])
        significant = np.array([r[1] < 0.05 for r in results])
        rejection_rate = significant.mean()
        monte_carlo_se = np.sqrt(rejection_rate * (1 - rejection_rate) / repetitions)
        print(
            f"True effect: {tau:.2f} SD | "
            f"Rejection rate: {rejection_rate:.4f} | "
            f"Monte Carlo SE: {monte_carlo_se:.4f} | "
            f"Mean estimate: {estimates.mean():.4f}"
        )


if __name__ == "__main__":
    run_simulation()
