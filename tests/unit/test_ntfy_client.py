from unittest.mock import MagicMock, patch

from infrastructure.tts.ntfy_client import NtfyClient


def test_ntfy_returns_latest_message():
    response = MagicMock()

    response.text = (
        '{"event":"message","message":"old"}\n'
        '{"event":"message","message":"https://test.gradio.live"}\n'
    )

    response.raise_for_status.return_value = None

    with patch(
        "requests.get",
        return_value=response
    ) as mock_get:

        client = NtfyClient("video-factory")

        result = client.get_latest_message()

    assert result == "https://test.gradio.live"

    mock_get.assert_called_once()


def test_ntfy_ignores_invalid_json():
    response = MagicMock()

    response.text = (
        "not-json\n"
        '{"event":"message","message":"https://test.gradio.live"}\n'
    )

    response.raise_for_status.return_value = None

    with patch(
        "requests.get",
        return_value=response
    ):

        client = NtfyClient("test")

        assert (
            client.get_latest_message()
            == "https://test.gradio.live"
        )


def test_ntfy_returns_none_on_request_failure():
    with patch(
        "requests.get",
        side_effect=Exception("Network error")
    ):

        client = NtfyClient("test")

        assert client.get_latest_message() is None