from fastapi import APIRouter

from infrastructure.job_queue.queue_client import QueueClient
from infrastructure.db.job_repository import JobRepository


router = APIRouter()

queue = QueueClient()
jobs = JobRepository()


@router.post("/videos")
def create_video(plugin_name: str):

    queue_message_id = queue.send({
        "plugin_name": plugin_name
    })

    job_id = jobs.create(
        queue_message_id=queue_message_id,
        plugin_name=plugin_name
    )

    return {
        "job_id": job_id,
        "queue_message_id": queue_message_id,
        "status": "queued"
    }


@router.get("/videos/{job_id}")
def get_video_status(job_id: str):

    row = jobs.get(job_id)

    if row is None:
        return {
            "error": "Video job not found"
        }

    return {
        "job_id": row[0],
        "plugin_name": row[1],
        "status": row[2],
        "output_url": row[3],
        "error_message": row[4],
        "created_at": row[5],
        "started_at": row[6],
        "completed_at": row[7]
    }