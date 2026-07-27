import pytest

from plugins.chess.service.puzzle_classifier import PuzzleClassifier


@pytest.mark.parametrize(
    "themes,expected",
    [
        ("matein2", "mate_in_2"),
        ("matein3", "mate_in_3"),
        ("opening", "opening_guess"),
        ("fork", "fork_tactic"),
        ("pin", "pin_tactic"),
        ("skewer", "skewer_tactic"),
        ("sacrifice", "sacrifice"),
        ("endgame", "endgame"),
        ("crushing", "crushing_attack"),
        ("defensive", "defensive_move"),
        ("hangingpiece", "tactic"),
        ("discoveredattack", "tactic"),
        ("doublecheck", "tactic"),
        ("something_unknown", "best_move"),
    ]
)
def test_puzzle_classifier(themes, expected):
    puzzle = type("Puzzle", (), {"themes": themes})()

    result = PuzzleClassifier().classify(puzzle)

    assert result == expected


def test_puzzle_classifier_is_case_insensitive():
    puzzle = type(
        "Puzzle",
        (),
        {"themes": "Fork"}
    )()

    assert PuzzleClassifier().classify(puzzle) == "fork_tactic"


def test_puzzle_classifier_handles_empty_themes():
    puzzle = type(
        "Puzzle",
        (),
        {"themes": None}
    )()

    assert PuzzleClassifier().classify(puzzle) == "best_move"