def test_package_imports_and_exports() -> None:
    import emo
    import emo.metrics.dac.lag  # noqa: F401
    import emo.remedy.backtest  # noqa: F401

    for name in ["compute_gwi", "compute_smf", "compute_information_time", "compute_gaussian_synergy"]:
        assert callable(getattr(emo, name)), name
