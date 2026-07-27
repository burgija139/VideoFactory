import pytest

from infrastructure.tts.voice_registry import VoiceRegistry


def test_registered_voice_exists():
    registry = VoiceRegistry()

    voice = registry.get_voice(
        "naruto",
        "excited"
    )

    assert "audio" in voice
    assert "text" in voice


@pytest.mark.parametrize(
    "character,emotion",
    [
        ("naruto", "natural"),
        ("naruto", "excited"),
        ("sasuke", "natural"),
        ("sasuke", "excited"),
    ]
)
def test_all_registered_voices(character, emotion):
    registry = VoiceRegistry()

    voice = registry.get_voice(
        character,
        emotion
    )

    assert voice["audio"].name.endswith(".wav")
    assert voice["text"].name.endswith(".txt")


def test_unknown_voice_raises_error():
    registry = VoiceRegistry()

    with pytest.raises(ValueError, match="Voice sample not found"):
        registry.get_voice(
            "unknown",
            "natural"
        )