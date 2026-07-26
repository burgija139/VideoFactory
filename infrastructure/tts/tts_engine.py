import os
import shutil
import subprocess
import time
import wave
from pathlib import Path

from gradio_client import Client, handle_file

from infrastructure.tts.voice_registry import VoiceRegistry
from infrastructure.tts.url_provider import UrlProvider


class TTSEngine:

    def __init__(self):

        self.registry = VoiceRegistry()
        self.url_provider = UrlProvider()

        self.client = None
        self.server_url = None

        self._connect()

    def _connect(self, force_refresh: bool = False):

        if force_refresh:
            self.server_url = self.url_provider.refresh_url()
        else:
            self.server_url = self.url_provider.get_url()

        print(f"[🚀 TTS] Povezujem se na {self.server_url}")

        try:
            self.client = Client(self.server_url)

        except Exception as e:

            if force_refresh:
                raise e

            print("[⚠️ Cache URL nije validan. Tražim novi...")

            self.server_url = self.url_provider.refresh_url()

            self.client = Client(self.server_url)

    def _reconnect(self):

        print("[🔄 TTS] Ponovno povezivanje...")

        for attempt in range(5):

            try:

                self._connect(force_refresh=True)

                print("[✅ TTS] Ponovo povezan.")

                return

            except Exception as e:

                print(
                    f"[⚠️ Reconnect {attempt + 1}/5] {e}"
                )

                time.sleep(2)

        raise RuntimeError(
            "Ne mogu da uspostavim vezu sa F5-TTS serverom."
        )

    def synthesize(
        self,
        character: str,
        emotion: str,
        text: str,
        output_path: str,
    ):

        output_path = str(Path(output_path).resolve())

        voice = self.registry.get_voice(
            character,
            emotion
        )

        with open(
            voice["text"],
            "r",
            encoding="utf-8"
        ) as f:

            ref_text = f.read()

        print(
            f"[🛰️ Colab TTS] {character} ({emotion})"
        )

        result = None

        for attempt in range(2):

            try:

                result = self.client.predict(

                    ref_audio_input=handle_file(
                        str(voice["audio"])
                    ),

                    ref_text_input=ref_text,

                    gen_text_input=text,

                    remove_silence=True,

                    randomize_seed=True,

                    seed_input=0,

                    cross_fade_duration_slider=0.15,

                    nfe_slider=32,

                    speed_slider=1.0,

                    api_name="/basic_tts",
                )

                break

            except Exception as e:

                print(
                    f"[⚠️ Predict greška {attempt + 1}/2] {e}"
                )

                if attempt == 0:

                    self._reconnect()

                else:

                    raise

        if isinstance(result, (list, tuple)):
            generated_audio = result[0]
        else:
            generated_audio = result

        if isinstance(generated_audio, dict):
            generated_audio = generated_audio["path"]

        elif hasattr(generated_audio, "name"):
            generated_audio = generated_audio.name

        generated_audio = str(
            Path(generated_audio).resolve()
        )

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True,
        )

        ffmpeg = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                generated_audio,
                "-filter:a",
                "volume=0.70",
                output_path,
            ],
            capture_output=True,
            text=True,
        )

        if ffmpeg.returncode != 0:

            print(
                "[⚠️ FFmpeg nije uspeo. Kopiram original."
            )

            shutil.copy(
                generated_audio,
                output_path,
            )

        duration = self._get_duration(
            output_path
        )

        return {
            "path": output_path,
            "duration": duration,
        }

    def _get_duration(self, path):

        with wave.open(path, "rb") as wav:

            frames = wav.getnframes()
            rate = wav.getframerate()

        return frames / rate