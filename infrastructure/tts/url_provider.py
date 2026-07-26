from pathlib import Path
import os

from dotenv import load_dotenv

from infrastructure.tts.ntfy_client import NtfyClient


class UrlProvider:

    def __init__(self):

        load_dotenv()

        self.channel = os.getenv("MY_TTS_CHANNEL")

        if not self.channel:
            raise ValueError("MY_TTS_CHANNEL nije definisan.")

        project_root = Path(__file__).resolve().parents[2]

        self.cache_dir = project_root / "infrastructure" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache_file = self.cache_dir / "tts_url_cache.txt"

        self.ntfy = NtfyClient(self.channel)

    def get_url(self) -> str:
        """
        Vraća URL iz cache-a.
        Ako cache ne postoji prvi put,
        automatski ide na ntfy.
        """

        cached = self._load_cache()

        if cached:

            print("[🌐 URL Provider] Koristim cache URL.")

            return cached

        print("[🌐 URL Provider] Cache ne postoji. Tražim URL sa ntfy...")

        return self.refresh_url()

    def refresh_url(self) -> str:
        """
        Uvek čita najnoviji URL sa ntfy
        i prepisuje cache.
        """

        message = self.ntfy.get_latest_message()

        if not message:
            raise RuntimeError(
                "Nije pronađen URL na ntfy kanalu."
            )

        url = message.strip()

        if "gradio.live" not in url:
            raise RuntimeError(
                "Dobijen URL nije validan."
            )

        self._save_cache(url)

        print(f"[✅ URL Provider] Novi URL: {url}")

        return url

    def _save_cache(self, url: str):

        with open(
            self.cache_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(url)

    def _load_cache(self):

        if not self.cache_file.exists():
            return None

        with open(
            self.cache_file,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read().strip()