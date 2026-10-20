"""
RDL controls: the simulation must respond to the measured situation.

- nothing to repair  -> predicted gain ~ 0
- no data            -> refusal, no numbers
- bigger gap         -> bigger predicted gain (same portfolio quality)
- unknown domain     -> clear error, not a silent empty portfolio
"""
import pytest

from emo.remedy.bottlenecks import classify_bottlenecks
from emo.remedy.intervention_library import get_intervention_options
from emo.remedy.portfolio_builder import build_remedy_portfolio
from emo.remedy.scoring import score_portfolio
from emo.remedy.simulation import simulate_remedy_pathways

DOMAIN = "climate_mitigation"


def _run(**scores):
    p = classify_bottlenecks(domain=DOMAIN, jurisdiction="global", **scores)
    port = build_remedy_portfolio(profile=p, options=get_intervention_options(DOMAIN, p.dominant_bottlenecks))
    sc = score_portfolio(port)
    return {r.scenario: r for r in simulate_remedy_pathways(port, sc, p)}


def test_nothing_to_repair_predicts_no_gain():
    r = _run(validation_score=1, translation_score=1, budget_score=1,
             deployment_score=1, persistence_score=1, contradiction_score=0)
    assert r["selected_portfolio"].expected_dac_improvement == 0.0
    assert r["do_nothing"].expected_dac_improvement == 0.0


def test_no_data_is_refused():
    r = _run(validation_score=0, translation_score=0, budget_score=0,
             deployment_score=0, persistence_score=0, contradiction_score=0)
    assert list(r) == ["insufficient_data"]


def test_missing_profile_is_refused():
    p = classify_bottlenecks(domain=DOMAIN, jurisdiction="global", validation_score=0.5,
                             translation_score=0.5, budget_score=0.5, deployment_score=0.5,
                             persistence_score=0.5, contradiction_score=0.5)
    port = build_remedy_portfolio(profile=p, options=get_intervention_options(DOMAIN, p.dominant_bottlenecks))
    out = simulate_remedy_pathways(port, score_portfolio(port))
    assert out[0].scenario == "insufficient_data"


def test_bigger_gap_gives_bigger_gain():
    small = _run(validation_score=0.9, translation_score=0.8, budget_score=0.7,
                 deployment_score=0.8, persistence_score=0.8, contradiction_score=0.1)
    large = _run(validation_score=0.9, translation_score=0.4, budget_score=0.2,
                 deployment_score=0.3, persistence_score=0.3, contradiction_score=0.8)
    assert large["selected_portfolio"].expected_dac_improvement > small["selected_portfolio"].expected_dac_improvement
    assert large["high_friction"].expected_dac_improvement <= large["selected_portfolio"].expected_dac_improvement


def test_unknown_domain_raises():
    with pytest.raises(ValueError):
        get_intervention_options("climate", ["budget"])
