"""Mechanics of the backtest engine on synthetic structures (no historical case is used)."""
from emo.remedy.backtest import StructureInputs, run_backtest
from emo.remedy.bottlenecks import classify_bottlenecks

PROFILE = dict(validation_score=0.8, translation_score=0.2, budget_score=0.4,
               deployment_score=0.3, persistence_score=0.4, contradiction_score=0.5)


def _p():
    return classify_bottlenecks(domain="synthetic", jurisdiction="global", **PROFILE)


def test_same_profile_without_structure_cannot_discriminate():
    a = run_backtest(_p(), None)
    b = run_backtest(_p(), None)
    assert a.predicted_gain == b.predicted_gain and a.top3 == b.top3


def test_easy_structure_beats_hard_structure():
    easy = StructureInputs(n_major_actors=5, substitutes=0.9, economic_share=0.005)
    hard = StructureInputs(n_major_actors=200, substitutes=0.1, economic_share=0.8)
    assert run_backtest(_p(), easy).predicted_gain > run_backtest(_p(), hard).predicted_gain


def test_binding_regulation_ranks_higher_when_structure_is_easy():
    easy = StructureInputs(n_major_actors=5, substitutes=0.9, economic_share=0.005)
    hard = StructureInputs(n_major_actors=200, substitutes=0.1, economic_share=0.8)
    rank = lambda r: [k for k, _ in r.top3]
    assert "binding_regulation" in rank(run_backtest(_p(), easy))
    assert "binding_regulation" not in rank(run_backtest(_p(), hard))


def test_no_data_is_refused():
    p = classify_bottlenecks(domain="synthetic", jurisdiction="global", validation_score=0,
                             translation_score=0, budget_score=0, deployment_score=0,
                             persistence_score=0, contradiction_score=0)
    assert run_backtest(p, None).refused
