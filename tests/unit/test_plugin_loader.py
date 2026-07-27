from unittest.mock import MagicMock, patch

from core.plugin_system.plugin_loader import PluginLoader


def test_plugin_loader_loads_chess_plugin():
    loader = PluginLoader()
    fake_tts = MagicMock()

    fake_plugin_class = MagicMock()
    fake_plugin = MagicMock()
    fake_plugin_class.return_value = fake_plugin

    fake_module = MagicMock()
    fake_module.ChessPlugin = fake_plugin_class

    with patch(
        "importlib.import_module",
        return_value=fake_module
    ) as mock_import:

        result = loader.load("chess", fake_tts)

    mock_import.assert_called_once_with(
        "plugins.chess.chess_plugin"
    )

    fake_plugin_class.assert_called_once_with(
        tts_engine=fake_tts
    )

    assert result is fake_plugin