import pytest

from core.plugin_system.base_plugin import BasePlugin


def test_base_plugin_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BasePlugin(tts_engine=None)


def test_concrete_plugin_receives_tts_engine():
    class TestPlugin(BasePlugin):

        def generate_content(self):
            return "content"

        def build_video(self, content):
            return content

    tts = object()
    plugin = TestPlugin(tts)

    assert plugin.tts_engine is tts
    assert plugin.generate_content() == "content"