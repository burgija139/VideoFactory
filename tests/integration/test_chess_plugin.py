from unittest.mock import MagicMock, patch

from plugins.chess.chess_plugin import ChessPlugin
from plugins.chess.dto.puzzle_dto import PuzzleDTO
from plugins.chess.dto.timeline_item import TimelineItem
from plugins.chess.dto.video_plan import VideoPlan


def create_content():
    puzzle = PuzzleDTO(
        puzzle_id="integration-test",
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        moves="e2e4 e7e5",
        rating=1200,
        themes="opening"
    )

    plan = VideoPlan(
        speakers_count="1",
        timeline=[
            TimelineItem(
                time=0,
                text="Find the best move",
                type="intro",
                character="naruto",
                emotion="excited"
            )
        ]
    )

    content = MagicMock()
    content.puzzle = puzzle
    content.video_type = "opening_guess"
    content.video_plan = plan

    return content


def test_chess_plugin_generate_content():
    fake_tts = MagicMock()

    with patch(
        "plugins.chess.chess_plugin.ChessService"
    ) as service_class, patch(
        "plugins.chess.chess_plugin.ChessVideoBuilder"
    ), patch(
        "plugins.chess.chess_plugin.DialogueEngine"
    ):

        service = service_class.return_value

        content = create_content()

        service.get_content.return_value = content

        plugin = ChessPlugin(fake_tts)

        result = plugin.generate_content()

    assert result is content
    service.get_content.assert_called_once()


def test_chess_plugin_build_video_pipeline():
    fake_tts = MagicMock()

    content = create_content()

    audio_plan = [
        MagicMock(
            start=0,
            end=2
        )
    ]

    with patch(
        "plugins.chess.chess_plugin.ChessService"
    ), patch(
        "plugins.chess.chess_plugin.ChessVideoBuilder"
    ) as builder_class, patch(
        "plugins.chess.chess_plugin.DialogueEngine"
    ) as dialogue_class:

        dialogue = dialogue_class.return_value
        dialogue.build_dialogue.return_value = audio_plan

        plugin = ChessPlugin(fake_tts)

        plugin.build_video(content)

    dialogue.build_dialogue.assert_called_once_with(
        video_plan=content.video_plan,
        output_dir="temp_audio"
    )

    builder_class.return_value.create.assert_called_once_with(
        context=content,
        audio_plan=audio_plan,
        output_file="opening_guess_integration-test.mp4"
    )