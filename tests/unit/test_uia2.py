from pathlib import Path

from emo.uia2 import he_value, profile_rows

ROOT = Path(__file__).resolve().parents[2]


def test_he_value_sign_and_missing():
    assert he_value(2.0, 3.0) == -5.0
    assert he_value(None, 3.0) is None


def test_profile_no_rows_after_2025_and_no_sum():
    rows = profile_rows(ROOT / "data/loop_hurricanes/loop_events.csv")
    assert len(rows) == 52
    assert all(r["season"] <= 2025 for r in rows)
    assert all(set(r) >= {"F", "A", "W", "He"} for r in rows)
    assert not any("score" in k or "uia" in k.lower() for k in rows[0])
