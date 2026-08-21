# plugins/chess/chess_plugin.py

from core.plugin_system.base_plugin import BasePlugin
from infrastructure.storage.supabase_uploader import SupabaseUploader
from infrastructure.tts.dialogue_engine import DialogueEngine
from plugins.chess.service.chess_service import ChessService
from plugins.chess.video.chess_video_builder import ChessVideoBuilder


class ChessPlugin(BasePlugin):

    def __init__(self, tts_engine):
        # Pozivamo konstruktor apstraktne klase BasePlugin
        super().__init__(tts_engine)
        
        self.service = ChessService()
        self.video_builder = ChessVideoBuilder()
        
        self.uploader = SupabaseUploader()
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

        print(
            "[🎬 VideoFactory] Pokrećem renderovanje videa "
            "i miksovanje zvuka..."
        )

        return self.video_builder.create(
            context=content,
            audio_plan=audio_plan,
            output_file=output_file
        )
    
    def upload(self, file_path):
        remote_path = f"chess/{file_path.split('/')[-1]}"

        print(
            "[☁️ VideoFactory] Uploadujem video na Supabase..."
        )

        self.uploader.upload_video(
            local_file=file_path,
            remote_path=remote_path
        )

        print(
            f"☁️ Video uspešno uploadovan: "
            f"{file_path} -> {remote_path}"
        )