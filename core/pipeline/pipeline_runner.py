# core/pipeline/pipeline_runner.py
from core.plugin_system.plugin_loader import PluginLoader

class PipelineRunner:

    def __init__(self, tts_engine):
        self.loader = PluginLoader()
        self.tts_engine = tts_engine # Čuvamo instancu

    def run(self, plugin_name):
        # Loaderu prosleđujemo tts_engine da bi mogao da ga ubaci u plugin
        plugin = self.loader.load(plugin_name, tts_engine=self.tts_engine)

        content = plugin.generate_content()

        plugin.build_video(content)