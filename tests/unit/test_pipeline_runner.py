from unittest.mock import MagicMock, patch

from core.pipeline.pipeline_runner import PipelineRunner


def test_pipeline_runner_executes_plugin():
    tts = MagicMock()

    plugin = MagicMock()

    content = MagicMock()

    plugin.generate_content.return_value = content

    with patch(
        "core.pipeline.pipeline_runner.PluginLoader"
    ) as loader_class:

        loader = loader_class.return_value
        loader.load.return_value = plugin

        runner = PipelineRunner(tts)

        runner.run("chess")

    loader.load.assert_called_once_with(
        "chess",
        tts_engine=tts
    )

    plugin.generate_content.assert_called_once_with()
    plugin.build_video.assert_called_once_with(content)