import wave
from unittest.mock import MagicMock, patch

from infrastructure.tts.tts_engine import TTSEngine


def create_wav(path):
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(8000)
        wav.writeframes(b"\x00\x00" * 8000)


def test_tts_engine_synthesizes_audio(tmp_path):
    generated = tmp_path / "generated.wav"
    output = tmp_path / "output.wav"

    create_wav(generated)

    with patch(
        "infrastructure.tts.tts_engine.VoiceRegistry"
    ) as registry_class, patch(
        "infrastructure.tts.tts_engine.UrlProvider"
    ) as provider_class, patch(
        "infrastructure.tts.tts_engine.Client"
    ) as client_class, patch(
        "infrastructure.tts.tts_engine.subprocess.run"
    ) as subprocess_run:

        registry = registry_class.return_value

        registry.get_voice.return_value = {
            "audio": tmp_path / "reference.wav",
            "text": tmp_path / "reference.txt"
        }

        (tmp_path / "reference.txt").write_text(
            "reference voice",
            encoding="utf-8"
        )

        provider_class.return_value.get_url.return_value = (
            "https://test.gradio.live"
        )

        client = client_class.return_value

        client.predict.return_value = str(generated)

        subprocess_run.return_value.returncode = 0

        # Pošto mockovani ffmpeg ne pravi fajl,
        # napravimo očekivani output ručno.
        create_wav(output)

        engine = TTSEngine()

        result = engine.synthesize(
            "naruto",
            "natural",
            "Hello chess fans",
            str(output)
        )

    assert result["path"] == str(output.resolve())
    assert result["duration"] > 0

    client.predict.assert_called_once()


def test_tts_engine_rejects_unknown_voice(tmp_path):
    with patch(
        "infrastructure.tts.tts_engine.VoiceRegistry"
    ) as registry_class, patch(
        "infrastructure.tts.tts_engine.UrlProvider"
    ) as provider_class, patch(
        "infrastructure.tts.tts_engine.Client"
    ):

        registry_class.return_value.get_voice.side_effect = (
            ValueError("Voice sample not found")
        )

        provider_class.return_value.get_url.return_value = (
            "https://test.gradio.live"
        )

        engine = TTSEngine()

        try:
            engine.synthesize(
                "unknown",
                "natural",
                "Test",
                str(tmp_path / "output.wav")
            )
            assert False
        except ValueError as error:
            assert "Voice sample not found" in str(error)