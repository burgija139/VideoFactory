from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from infrastructure.tts.url_provider import UrlProvider


def create_provider(tmp_path):
    with patch(
        "infrastructure.tts.url_provider.load_dotenv"
    ), patch.dict(
        "os.environ",
        {"MY_TTS_CHANNEL": "test-channel"}
    ):

        provider = UrlProvider()

    provider.cache_dir = tmp_path
    provider.cache_file = tmp_path / "tts_url_cache.txt"

    return provider


def test_url_provider_reads_cached_url(tmp_path):
    provider = create_provider(tmp_path)

    url = "https://example.gradio.live"

    provider.cache_file.write_text(
        url,
        encoding="utf-8"
    )

    provider.ntfy = MagicMock()

    assert provider.get_url() == url

    provider.ntfy.get_latest_message.assert_not_called()


def test_url_provider_refreshes_when_cache_missing(tmp_path):
    provider = create_provider(tmp_path)

    provider.ntfy.get_latest_message.return_value = (
        "https://example.gradio.live"
    )

    result = provider.get_url()

    assert result == "https://example.gradio.live"

    assert provider.cache_file.read_text(
        encoding="utf-8"
    ) == "https://example.gradio.live"


def test_url_provider_rejects_invalid_url(tmp_path):
    provider = create_provider(tmp_path)

    provider.ntfy.get_latest_message.return_value = (
        "https://google.com"
    )

    with pytest.raises(
        RuntimeError,
        match="nije validan"
    ):
        provider.refresh_url()


def test_url_provider_rejects_missing_message(tmp_path):
    provider = create_provider(tmp_path)

    provider.ntfy.get_latest_message.return_value = None

    with pytest.raises(
        RuntimeError,
        match="Nije pronađen URL"
    ):
        provider.refresh_url()