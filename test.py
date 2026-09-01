from infrastructure.db.db_context import DBContext


sql = """
CREATE TABLE IF NOT EXISTS video_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    queue_message_id BIGINT UNIQUE NOT NULL,
    plugin_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    output_url TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,

    CONSTRAINT video_jobs_status_check
        CHECK (status IN (
            'queued',
            'processing',
            'completed',
            'failed'
        ))
);
"""

db = DBContext()

with db.connect() as conn:
    with conn.cursor() as cursor:
        cursor.execute(sql)

print("video_jobs tabela uspešno kreirana.")