from unittest.mock import MagicMock

from infrastructure.tts.dialogue_engine import DialogueEngine
from plugins.chess.dto.timeline_item import TimelineItem
from plugins.chess.dto.video_plan import VideoPlan


def create_plan():
    return VideoPlan(
        speakers_count="1",
        timeline=[
            TimelineItem(
                time=0,
                text="Find the winning move",
                type="intro",
                character="naruto",
                emotion="excited"
            ),
            TimelineItem(
                time=5,
                text="This move is brilliant",
                type="moves",
                character="naruto",
                emotion="natural"
            ),
        ]
    )


def test_dialogue_engine_generates_audio_plan(tmp_path):
    tts = MagicMock()

    tts.synthesize.side_effect = [
        {
            "path": str(tmp_path / "line_0.wav"),
            "duration": 2.5
        },
        {
            "path": str(tmp_path / "line_1.wav"),
            "duration": 3.0
        },
    ]

    engine = DialogueEngine(tts)

    plan = create_plan()

    result = engine.build_dialogue(
        plan,
        str(tmp_path)
    )

    assert len(result) == 2

    assert result[0].start == 0
    assert result[0].end == 2.5

    assert result[1].start == 5
    assert result[1].end == 8

    assert tts.synthesize.call_count == 2


def test_dialogue_engine_propagates_tts_error(tmp_path):
    tts = MagicMock()

    tts.synthesize.side_effect = RuntimeError(
        "TTS unavailable"
    )

    engine = DialogueEngine(tts)

    try:
        engine.build_dialogue(
            create_plan(),
            str(tmp_path)
        )
        assert False, "Expected RuntimeError"
    except RuntimeError as error:
        assert "TTS unavailable" in str(error)