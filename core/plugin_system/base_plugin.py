# core/plugin_system/base_plugin.py
from abc import ABC, abstractmethod

class BasePlugin(ABC):

    def __init__(self, tts_engine):
        self.tts_engine = tts_engine

    @abstractmethod
    def generate_content(self):
        pass

    @abstractmethod
    def build_video(self, content):
        pass