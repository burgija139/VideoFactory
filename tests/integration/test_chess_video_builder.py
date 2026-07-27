from unittest.mock import MagicMock, patch

from plugins.chess.video.chess_video_builder import ChessVideoBuilder
from plugins.chess.dto.puzzle_dto import PuzzleDTO
from plugins.chess.dto.video_plan import VideoPlan
from plugins.chess.dto.timeline_item import TimelineItem


def create_context():
    puzzle = PuzzleDTO(
        puzzle_id="builder-test",
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        moves="e2e4 e7e5",
        rating=1500,
        themes="opening"
    )

    plan = VideoPlan(
        speakers_count="1",
        timeline=[
            TimelineItem(
                time=0,
                text="Find the move",
                type="intro",
                character="naruto",
                emotion="natural"
            )
        ],
        intro_seconds=1,
        show_moves=False,
        timer_enabled=False
    )

    context = MagicMock()
    context.puzzle = puzzle
    context.video_plan = plan
    context.video_type = "opening_guess"

    return context


def test_video_builder_handles_static_puzzle():
    context = create_context()

    audio_item = MagicMock(
        start=0,
        end=1
    )

    with patch(
        "plugins.chess.video.chess_video_builder.subprocess.Popen"
    ) as popen, patch(
        "plugins.chess.video.chess_video_builder.subprocess.run"
    ) as run:

        process = MagicMock()
        process.stdin = MagicMock()

        popen.return_value = process

        builder = ChessVideoBuilder()

        builder.board_renderer.render = MagicMock(
            return_value=b"board"
        )

        builder.overlay_renderer.render = MagicMock(
            return_value=b"frame"
        )

        builder.move_audio_builder.build = MagicMock()

        builder.create(
            context,
            [audio_item],
            "integration.mp4"
        )

    builder.move_audio_builder.build.assert_called_once()

    assert process.stdin.write.called
    assert run.called