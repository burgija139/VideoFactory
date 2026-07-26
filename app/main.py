# main.py
from dotenv import load_dotenv
from core.pipeline.pipeline_runner import PipelineRunner

# Uvozimo samo TTSEngine, jer on sada samostalno sve radi u pozadini
from infrastructure.tts.tts_engine import TTSEngine

load_dotenv()

if __name__ == "__main__":
    print("[🚀 VideoFactory] Inicijalizacija TTS modela...")
    
    # Inicijalizacija bez ikakvih teških lokalnih modela ili argumenata.
    # __init__ u TTSEngine-u će sam povući HF_TOKEN iz .env fajla.
    tts_engine = TTSEngine()

    print("[⚙️ Pipeline] Pokretanje cevovoda...")
    # Prosleđujemo zajednički tts_engine u runner - ovo ostaje savršeno isto
    pipeline = PipelineRunner(tts_engine=tts_engine)
    pipeline.run("chess")