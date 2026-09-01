import time

from core.pipeline.pipeline_runner import PipelineRunner
from infrastructure.db.job_repository import JobRepository
from infrastructure.job_queue.queue_client import QueueClient
from infrastructure.tts.tts_engine import TTSEngine


def main():
    print("[Worker] Pokretanje...")

    queue = QueueClient()
    job_repository = JobRepository()

    print("[Worker] Inicijalizacija TTS modela...")
    tts_engine = TTSEngine()

    pipeline = PipelineRunner(tts_engine=tts_engine)

    print("[Worker] Čekam poslove...")

    while True:
        job = queue.receive(visibility_timeout=3600)

        if job is None:
            time.sleep(5)
            continue

        message_id = job["msg_id"]

        try:
            message = job["message"]
            plugin_name = message["plugin_name"]

            print(
                f"[Worker] Obrada posla "
                f"{message_id}: {plugin_name}"
            )

            job_repository.set_processing(message_id)

            pipeline.run(plugin_name)

            job_repository.set_completed(
                queue_message_id=message_id,
                output_url=None,
            )

            queue.delete(message_id)

            print(
                f"[Worker] Posao {message_id} uspešno završen."
            )

        except Exception as e:
            job_repository.set_failed(
                queue_message_id=message_id,
                error_message=str(e),
            )

            print(
                f"[Worker] Greška pri obradi posla "
                f"{message_id}: {e}"
            )


if __name__ == "__main__":
    main()