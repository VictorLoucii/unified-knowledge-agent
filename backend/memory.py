# backend/memory.py
import os
import psycopg
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

# Get DB URI from environment
DB_URI = os.getenv("DATABASE_URL", "postgresql://localhost/postgres")


def setup_database_tables():
    """Synchronously sets up LangGraph tables and our custom metadata table."""
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            # 1. Setup LangGraph default tables (checkpoints, blobs, writes)
            setup_memory = PostgresSaver(conn)
            setup_memory.setup()

# 2. Setup custom Second Brain metadata table and Cascade rules
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS thread_metadata (
                        thread_id TEXT PRIMARY KEY,
                        title TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    -- Tie LangGraph's checkpoints to our metadata table
                    ALTER TABLE checkpoints 
                    DROP CONSTRAINT IF EXISTS fk_cascade_metadata_checkpoints;
                    ALTER TABLE checkpoints 
                    ADD CONSTRAINT fk_cascade_metadata_checkpoints 
                    FOREIGN KEY (thread_id) REFERENCES thread_metadata(thread_id) ON DELETE CASCADE;

                    -- Tie LangGraph's blobs to our metadata table
                    ALTER TABLE checkpoint_blobs 
                    DROP CONSTRAINT IF EXISTS fk_cascade_metadata_blobs;
                    ALTER TABLE checkpoint_blobs 
                    ADD CONSTRAINT fk_cascade_metadata_blobs 
                    FOREIGN KEY (thread_id) REFERENCES thread_metadata(thread_id) ON DELETE CASCADE;

                    -- Tie LangGraph's writes to our metadata table
                    ALTER TABLE checkpoint_writes 
                    DROP CONSTRAINT IF EXISTS fk_cascade_metadata_writes;
                    ALTER TABLE checkpoint_writes 
                    ADD CONSTRAINT fk_cascade_metadata_writes 
                    FOREIGN KEY (thread_id) REFERENCES thread_metadata(thread_id) ON DELETE CASCADE;
                    """
                )

                

        print("✅ PostgresSaver and Metadata tables verified/created.")
    except Exception as e:
        print(f"❌ Postgres Connection Error: {e}")
        print("👉 Ensure Postgres is running and DATABASE_URL in .env is correct.")


async def save_thread_title(
    async_pool: AsyncConnectionPool, thread_id: str, user_message: str
):
    """Generates and saves a title for a new thread if it doesn't exist."""
    async with async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT title FROM thread_metadata WHERE thread_id = %s", (thread_id,)
            )
            if not await cur.fetchone():
                # Simple logic: Take first 40 chars as the title
                title = user_message[:40] + ("..." if len(user_message) > 40 else "")
                await cur.execute(
                    "INSERT INTO thread_metadata (thread_id, title) VALUES (%s, %s)",
                    (thread_id, title),
                )


async def get_all_threads_history(async_pool: AsyncConnectionPool, limit: int = 20, offset: int = 0):
    """Fetches a paginated list of unique thread IDs joined with their titles."""
    async with async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT c.thread_id, COALESCE(m.title, c.thread_id) as title 
                FROM (SELECT DISTINCT thread_id FROM checkpoints) c
                LEFT JOIN thread_metadata m ON c.thread_id = m.thread_id
                ORDER BY m.created_at DESC NULLS LAST, c.thread_id DESC
                LIMIT %s OFFSET %s;
                """,
                (limit, offset)
            )
            rows = await cur.fetchall()
            return [{"id": row[0], "title": row[1]} for row in rows]



async def delete_thread_from_db(async_pool: AsyncConnectionPool, thread_id: str):
    """Safely deletes thread metadata. PostgreSQL ON DELETE CASCADE handles LangGraph tables automatically."""
    async with async_pool.connection() as conn:
        async with conn.cursor() as cur:
            # We only need to delete the parent record now
            await cur.execute(
                "DELETE FROM thread_metadata WHERE thread_id = %s;", (thread_id,)
            )