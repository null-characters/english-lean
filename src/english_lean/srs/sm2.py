"""Simplified SM-2 style scheduler (no DB, no wall clock reads)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

EF_MIN = 1.3


@dataclass(frozen=True)
class SrsState:
    ease_factor: float
    interval_days: int
    repetitions: int
    lapses: int = 0


def new_state() -> SrsState:
    return SrsState(ease_factor=2.5, interval_days=0, repetitions=0, lapses=0)


def _clamp_ef(ef: float) -> float:
    return max(EF_MIN, ef)


def review_success(state: SrsState, now: datetime) -> tuple[SrsState, datetime]:
    """
    Successful recall (e.g. spelling correct).
    Interval: first success 1d, second 6d, then round(prev_interval * ease_factor).
    Ease factor is unchanged in this MVP.
    """
    ef = _clamp_ef(state.ease_factor)
    if state.repetitions == 0:
        new_interval = 1
    elif state.repetitions == 1:
        new_interval = 6
    else:
        new_interval = max(1, round(state.interval_days * ef))

    new_state_ = SrsState(
        ease_factor=ef,
        interval_days=new_interval,
        repetitions=state.repetitions + 1,
        lapses=state.lapses,
    )
    next_at = now + timedelta(days=new_interval)
    return new_state_, next_at


def review_fail(state: SrsState, now: datetime) -> tuple[SrsState, datetime]:
    """
    Failed recall: reset repetition ladder; due immediately (same timestamp as ``now``).
    """
    new_state_ = SrsState(
        ease_factor=_clamp_ef(state.ease_factor),
        interval_days=0,
        repetitions=0,
        lapses=state.lapses + 1,
    )
    return new_state_, now
