import os

from dotenv import load_dotenv
from supabase import Client, create_client


class SupabaseUploader:

    def __init__(self):
        load_dotenv()

        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        self.bucket = os.getenv("SUPABASE_BUCKET", "videos")

        if not supabase_url:
            raise ValueError("SUPABASE_URL nije podešen u .env")

        if not supabase_key:
            raise ValueError("SUPABASE_KEY nije podešen u .env")

        self.supabase: Client = create_client(
            supabase_url,
            supabase_key,
        )

    def upload_video(self, local_file: str, remote_path: str) -> str:
        if not os.path.isfile(local_file):
            raise FileNotFoundError(
                f"Video fajl ne postoji: {local_file}"
            )

        print(
            f"[SupabaseUploader] Uploading: "
            f"{local_file} -> {self.bucket}/{remote_path}"
        )

        with open(local_file, "rb") as file:
            self.supabase.storage.from_(self.bucket).upload(
                path=remote_path,
                file=file,
                file_options={
                    "content-type": "video/mp4",
                },
            )

        print(
            f"[SupabaseUploader] Upload uspešan: "
            f"{self.bucket}/{remote_path}"
        )

        return remote_path