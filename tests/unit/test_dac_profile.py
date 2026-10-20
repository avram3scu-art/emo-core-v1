"""DAC profile is reported as a profile, never summed into one number."""
from emo.remedy.bottlenecks import classify_bottlenecks
from emo.remedy.simulation import dac_profile


def _p(**k):
    base = dict(validation_score=0.8, translation_score=0.2, budget_score=0.4,
                deployment_score=0.2, persistence_score=0.6, contradiction_score=0.7)
    base.update(k)
    return classify_bottlenecks(domain="synthetic", jurisdiction="global", **base)


def test_profile_has_no_scalar():
    d = dac_profile(_p())
    assert set(d) == {"stages", "shortfalls", "weakest_stages", "contradiction", "has_data"}
    assert all(not isinstance(v, float) for k, v in d.items() if k != "contradiction")


def test_contradiction_kept_separate_and_ties_listed():
    d = dac_profile(_p())
    assert "contradiction" not in d["stages"] and d["contradiction"] == 0.7
    assert d["weakest_stages"] == ["deployment", "translation"]


def test_profiles_with_equal_mean_stay_distinguishable():
    a = dac_profile(_p(validation_score=1.0, translation_score=0.0, budget_score=0.5,
                       deployment_score=0.5, persistence_score=0.5))
    b = dac_profile(_p(validation_score=0.5, translation_score=0.5, budget_score=0.5,
                       deployment_score=0.5, persistence_score=0.5))
    assert a["stages"] != b["stages"] and a["weakest_stages"] != b["weakest_stages"]
