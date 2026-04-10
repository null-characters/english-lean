"""SM-2 scheduler unit tests."""

from __future__ import annotations

from datetime import datetime, timedelta

from english_lean.srs.sm2 import new_state, review_fail, review_success


def test_new_state_defaults() -> None:
    s = new_state()
    assert s.ease_factor == 2.5
    assert s.interval_days == 0
    assert s.repetitions == 0


def test_success_three_times_intervals() -> None:
    now = datetime(2026, 4, 10, 12, 0, 0)
    s = new_state()
    s, t1 = review_success(s, now)
    assert s.repetitions == 1 and s.interval_days == 1
    assert t1 == now + timedelta(days=1)

    s, t2 = review_success(s, now)
    assert s.repetitions == 2 and s.interval_days == 6
    assert t2 == now + timedelta(days=6)

    s, t3 = review_success(s, now)
    assert s.repetitions == 3
    assert s.interval_days == max(1, round(6 * 2.5))
    assert t3 == now + timedelta(days=s.interval_days)


def test_fail_resets_after_one_success() -> None:
    now = datetime(2026, 1, 1, 8, 0, 0)
    s, _ = review_success(new_state(), now)
    assert s.repetitions == 1
    s2, nxt = review_fail(s, now)
    assert s2.repetitions == 0
    assert s2.interval_days == 0
    assert s2.lapses == 1
    assert nxt == now


def test_ease_factor_floor() -> None:
    from dataclasses import replace

    from english_lean.srs import sm2

    low = replace(new_state(), ease_factor=1.0)
    s, _ = review_success(low, datetime(2026, 1, 1))
    assert s.ease_factor == sm2.EF_MIN
