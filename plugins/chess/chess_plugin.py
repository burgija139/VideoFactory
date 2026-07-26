# plugins/chess/chess_plugin.py
from core.plugin_system.base_plugin import BasePlugin
from plugins.chess.service.chess_service import ChessService
from plugins.chess.video.chess_video_builder import ChessVideoBuilder
from infrastructure.tts.dialogue_engine import DialogueEngine


class ChessPlugin(BasePlugin):

    def __init__(self, tts_engine):
        # Pozivamo konstruktor apstraktne klase BasePlugin
        super().__init__(tts_engine)
        
        self.service = ChessService()
        self.video_builder = ChessVideoBuilder()
        
        # Inicijalizujemo DialogueEngine koji je sada bezbedno u infrastrukturi
        self.dialogue_engine = DialogueEngine(tts_engine)

    def generate_content(self):
        return self.service.get_content()

    def build_video(self, content):
        puzzle = content.puzzle
        video_type = content.video_type
        video_plan = content.video_plan  # Sadrži generisani AI tajmlajn

        # 1. GENERIŠEMO TTS AUDIO PLAN PRE NEGO ŠTO KREIRAMO VIDEO
        print("[⚡ VideoFactory] Pokrećem generisanje TTS glasova...")
        audio_plan = self.dialogue_engine.build_dialogue(
            video_plan=video_plan,
            output_dir="temp_audio"
        )

        output_file = f"{video_type}_{puzzle.puzzle_id}.mp4"

        # 2. PROSLEĐUJEMO I CONTEXT I AUDIO_PLAN U BUILDER
        print("[🎬 VideoFactory] Pokrećem renderovanje videa i miksovanje zvuka...")
        self.video_builder.create(
            context=content,
            audio_plan=audio_plan,
            output_file=output_file
        )

        print(f"Generated video: {output_file}")