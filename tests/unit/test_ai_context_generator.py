from unittest.mock import MagicMock, patch

from plugins.chess.content_generation.ai_context_generator import AIContextGenerator
from plugins.chess.dto.puzzle_dto import PuzzleDTO


def create_context():
    puzzle = PuzzleDTO(
        puzzle_id="test123",
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        moves="e2e4 e7e5 g1f3",
        rating=1500,
        themes="fork"
    )

    return MagicMock(
        puzzle=puzzle,
        video_type="fork_tactic"
    )


def create_gemini_response():
    response = MagicMock()

    response.text = """
    {
        "title": "Amazing Chess Puzzle",
        "speakers_count": "1",
        "timeline": [
            {
                "time": 0,
                "text": "Can you find the winning move?",
                "type": "intro",
                "character": "naruto",
                "emotion": "excited"
            }
        ],
        "intro_seconds": 5,
        "show_moves": true,
        "timer_enabled": false,
        "timer_duration": 5,
        "pacing": "medium",
        "style": "viral"
    }
    """

    return response


def test_ai_context_generator_parses_gemini_response():
    with patch.dict(
        "os.environ",
        {"GEMINI_API_KEY": "fake-key"}
    ), patch(
        "plugins.chess.content_generation.ai_context_generator.genai.Client"
    ) as client_class:

        client = client_class.return_value

        client.models.generate_content.return_value = (
            create_gemini_response()
        )

        generator = AIContextGenerator()

        context = create_context()

        result = generator.generate(context)

    assert result.title == "Amazing Chess Puzzle"
    assert len(result.timeline) == 1
    assert result.timeline[0].character == "naruto"


def test_ai_context_generator_forces_static_puzzle_rules():
    with patch.dict(
        "os.environ",
        {"GEMINI_API_KEY": "fake-key"}
    ), patch(
        "plugins.chess.content_generation.ai_context_generator.random.random",
        return_value=0.99
    ), patch(
        "plugins.chess.content_generation.ai_context_generator.genai.Client"
    ) as client_class:

        response = create_gemini_response()

        client = client_class.return_value
        client.models.generate_content.return_value = response

        generator = AIContextGenerator()

        result = generator.generate(create_context())

    assert result.show_moves is False
    assert result.speakers_count == "1"
    assert result.timer_enabled is True
    assert result.timer_duration in [5, 7]