# core/plugin_system/plugin_loader.py
import importlib


class PluginLoader:

    def load(self, plugin_name, tts_engine):
        module_path = f"plugins.{plugin_name}.{plugin_name}_plugin"
        module = importlib.import_module(module_path)

        class_name = f"{plugin_name.capitalize()}Plugin"
        plugin_class = getattr(module, class_name)

        # Prosleđujemo tts_engine direktno u konstruktor učitanog plugina
        return plugin_class(tts_engine=tts_engine)