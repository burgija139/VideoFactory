import json

from infrastructure.db.db_context import DBContext


class QueueClient:

    def __init__(self, queue_name: str = "video_jobs"):
        self.queue_name = queue_name
        self.db = DBContext()

    def send(self, message: dict):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT pgmq.send(%s, %s::jsonb)",
                    (
                        self.queue_name,
                        json.dumps(message),
                    ),
                )

                return cursor.fetchone()[0]

    def receive(self, visibility_timeout: int = 30):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM pgmq.read(%s, %s, 1)",
                    (
                        self.queue_name,
                        visibility_timeout,
                    ),
                )

                row = cursor.fetchone()

        if row is None:
            return None

        return {
            "msg_id": row[0],
            "read_ct": row[1],
            "enqueued_at": row[2],
            "message": row[4],
        }

    def delete(self, message_id: int):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT pgmq.delete(%s, %s)",
                    (
                        self.queue_name,
                        message_id,
                    ),
                )

                return cursor.fetchone()[0]