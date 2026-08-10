import pytest
from pydantic import ValidationError

from plugins.chess.dto.timeline_item import TimelineItem
from plugins.chess.dto.video_plan import VideoPlan


def make_timeline():
    return [
        TimelineItem(
            time=0,
            text="Find the winning move",
            type="intro",
            character="naruto",
            emotion="excited"
        ),
        TimelineItem(
            time=5,
            text="Look at this position",
            type="moves",
            character="naruto",
            emotion="natural"
        ),
    ]


def test_video_plan_accepts_valid_data():
    plan = VideoPlan(
        speakers_count="1",
        timeline=make_timeline()
    )

    assert plan.title == "Chess Puzzle"
    assert plan.intro_seconds == 5
    assert plan.show_moves is True
    assert plan.timer_enabled is False
    assert len(plan.timeline) == 2


def test_video_plan_accepts_two_speakers():
    plan = VideoPlan(
        speakers_count="2",
        timeline=make_timeline()
    )

    assert plan.speakers_count == "2"


def test_video_plan_rejects_invalid_speaker_count():
    with pytest.raises(ValidationError):
        VideoPlan(
            speakers_count="3",
            timeline=make_timeline()
        )


def test_video_plan_rejects_invalid_pacing():
    with pytest.raises(ValidationError):
        VideoPlan(
            speakers_count="1",
            pacing="extreme",
            timeline=make_timeline()
        )


def test_video_plan_rejects_invalid_character():
    with pytest.raises(ValidationError):
        TimelineItem(
            time=0,
            text="Test",
            type="intro",
            character="goku",
            emotion="natural"
        )