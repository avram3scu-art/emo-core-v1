from __future__ import annotations

from emo.models.bottleneck_profile import BottleneckProfile
from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_portfolio import RemedyPortfolio
from emo.models.remedy_simulation import RemedySimulationResult

_PIPELINE = ("validation", "translation", "budget", "deployment", "persistence")


def dac_profile(profile: BottleneckProfile) -> dict:
    """
    The DAC profile as a profile: no aggregation, no weights.

    Each pipeline stage is reported with its own score and shortfall; contradiction is reported
    separately because it runs against the pipeline rather than along it. The weakest stage(s)
    are listed, not summed. This follows the DAC measurement rule that the profile "is not
    aggregated into a scalar: no weighting is justified a priori, and its components do not
    move together" (DAC manuscript, Section 2.8). Use this, not measured_gap, to describe a case.
    """
    stages = {k: round(float(getattr(profile, f"{k}_score")), 3) for k in _PIPELINE}
    low = min(stages.values())
    return {
        "stages": stages,
        "shortfalls": {k: round(1.0 - v, 3) for k, v in stages.items()},
        "weakest_stages": sorted(k for k, v in stages.items() if v == low),
        "contradiction": round(float(profile.contradiction_score), 3),
        "has_data": has_measured_data(profile),
    }


def measured_gap(profile: BottleneckProfile) -> float:
    """
    CONVENIENCE SCALAR, NOT A DAC MEASURE. Kept only because RDL v0.2/v0.3 (frozen, see
    docs/RDL_BACKTEST_PROTOCOL.md and RDL_V03_PROTOCOL.md) were defined and tested with it.
    It averages the stages with equal weights, which the DAC measurement rule does not justify;
    the v0.2/v0.3 backtests found it added little. Describe cases with dac_profile().

    How far the diagnosis-to-action pipeline is from working, in [0, 1].

    0 = every stage performs fully and there is no contradiction (nothing to repair);
    1 = every stage fails. Contradiction adds to the gap with half weight.
    """
    stages = [getattr(profile, f"{k}_score") for k in _PIPELINE]
    shortfall = sum(1.0 - s for s in stages) / len(stages)
    return round(min(1.0, shortfall + 0.5 * profile.contradiction_score * (1.0 - shortfall)), 3)


def has_measured_data(profile: BottleneckProfile) -> bool:
    """All-zero inputs mean 'no data' (missing scores are clamped to 0), not 'total failure'."""
    stages = [getattr(profile, f"{k}_score") for k in _PIPELINE]
    return any(s > 0 for s in stages) or profile.contradiction_score > 0


def simulate_remedy_pathways(
    portfolio: RemedyPortfolio,
    score: PortfolioScore,
    profile: BottleneckProfile | None = None,
) -> list[RemedySimulationResult]:
    """
    v0.2 gap-bounded simulation.

    v0.1 returned fixed numbers: 'do nothing' was always 0.05 and the portfolio's gain came
    only from labels on the interventions, so a system that already worked was still
    predicted to improve by ~0.6, and an all-zero (no data) input got a confident answer.

    v0.2 rules (still rule-based, not a causal model):
    - expected gain = measured gap x portfolio effectiveness (score.expected_dac_gain);
      a closed gap gives zero gain;
    - 'do nothing' = no change (0.0);
    - 'high friction' = gap x max(0, effectiveness - 0.25);
    - without a measured profile, or with all-zero inputs, the simulation refuses and says
      why, instead of returning numbers.
    Effectiveness values are still label-based assumptions, not evidence-based effect sizes.
    """
    if profile is None or not has_measured_data(profile):
        reason = ("No bottleneck profile was supplied." if profile is None
                  else "All bottleneck inputs are zero, which indicates missing data, not measured failure.")
        return [
            RemedySimulationResult(
                scenario="insufficient_data",
                expected_dac_improvement=0.0,
                persistence_outlook=0.0,
                contradiction_warning="Not assessed.",
                narrative=f"Simulation not run. {reason} Supply measured DAC sub-scores.",
                assumptions=["No estimate is produced without measured inputs."],
            )
        ]

    gap = measured_gap(profile)
    eff = max(0.0, min(1.0, score.expected_dac_gain))
    gain = round(gap * eff, 3)
    friction_gain = round(gap * max(0.0, eff - 0.25), 3)
    common = [
        f"Measured gap = {gap:.3f} (0 = nothing to repair).",
        "Portfolio effectiveness is a label-based assumption, not an evidence-based effect size.",
    ]

    do_nothing = RemedySimulationResult(
        scenario="do_nothing",
        expected_dac_improvement=0.0,
        persistence_outlook=round(profile.persistence_score, 3),
        contradiction_warning=(
            "High likelihood of unresolved bottlenecks." if gap >= 0.3 else "Little to repair."
        ),
        narrative="Without intervention, the measured gap is assumed to persist unchanged.",
        assumptions=common + ["No new remedy portfolio is activated."],
    )
    selected_portfolio = RemedySimulationResult(
        scenario="selected_portfolio",
        expected_dac_improvement=gain,
        persistence_outlook=round(score.persistence_likelihood, 3),
        contradiction_warning=(
            "Moderate contradiction risk remains."
            if score.contradiction_risk >= 0.5
            else "Contradiction risk appears manageable."
        ),
        narrative=(
            f"The selected portfolio ({', '.join(portfolio.sequence) or 'no sequence'}) "
            f"could close up to {gain:.3f} of a measured gap of {gap:.3f}."
        ),
        assumptions=common + ["The selected portfolio is implemented as designed."],
    )
    high_friction = RemedySimulationResult(
        scenario="high_friction",
        expected_dac_improvement=friction_gain,
        persistence_outlook=round(max(0.0, score.persistence_likelihood - 0.20), 3),
        contradiction_warning="High friction amplifies implementation and coordination risk.",
        narrative="Under high friction, effectiveness drops by 0.25 before scaling by the gap.",
        assumptions=common + ["Coordination burden rises above the current baseline."],
    )
    return [do_nothing, selected_portfolio, high_friction]
