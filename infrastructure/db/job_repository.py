from infrastructure.db.db_context import DBContext


class JobRepository:

    def __init__(self):
        self.db = DBContext()

    def create(self, queue_message_id, plugin_name):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO video_jobs (
                        queue_message_id,
                        plugin_name
                    )
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (queue_message_id, plugin_name),
                )

                return cursor.fetchone()[0]

    def set_processing(self, queue_message_id):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE video_jobs
                    SET
                        status = 'processing',
                        started_at = NOW()
                    WHERE queue_message_id = %s
                    """,
                    (queue_message_id,),
                )

    def set_completed(self, queue_message_id, output_url):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE video_jobs
                    SET
                        status = 'completed',
                        output_url = %s,
                        completed_at = NOW()
                    WHERE queue_message_id = %s
                    """,
                    (output_url, queue_message_id),
                )

    def set_failed(self, queue_message_id, error_message):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE video_jobs
                    SET
                        status = 'failed',
                        error_message = %s
                    WHERE queue_message_id = %s
                    """,
                    (error_message, queue_message_id),
                )

    def get(self, job_id):
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        plugin_name,
                        status,
                        output_url,
                        error_message,
                        created_at,
                        started_at,
                        completed_at
                    FROM video_jobs
                    WHERE id = %s
                    """,
                    (job_id,),
                )

                return cursor.fetchone()