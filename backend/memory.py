# backend/memory.py
import os
import asyncio
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

# 2. Setup custom knowledge base metadata table and Cascade rules
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS thread_metadata (
                        thread_id TEXT PRIMARY KEY,
                        title TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    -- Each thread belongs to the browser that created it
                    ALTER TABLE thread_metadata
                    ADD COLUMN IF NOT EXISTS owner_id TEXT;
                    """
                )

                # The owner column is added in the call above, so a failed FK
                # step here cannot roll it back or skip it
                cur.execute(
                    """
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


async def generate_title_from_llm(user_message: str) -> str:
    """Invokes LLM to generate a concise 1-4 word topic title for the chat."""
    try:
        from backend.core.config import llm
        from langchain_core.messages import SystemMessage, HumanMessage
        
        system_prompt = SystemMessage(
            content=(
                "You are a helpful assistant. Summarize the user's initial query into a concise, meaningful chat title.\n"
                "The title must be extremely brief (1 to 4 words, maximum 40 characters).\n"
                "Never use quotes, prefix, suffix, period, or formatting. Just output the raw summary text.\n"
                "Examples:\n"
                "Input: 'What is the project rule regarding npm vs yarn?' -> 'npm vs yarn Rule'\n"
                "Input: 'What was the fix for the Chiiro loader?' -> 'Chiiro Loader Fix'\n"
                "Input: 'How do I handle the MultiSelect scrolling bug?' -> 'MultiSelect Scroll Bug'"
            )
        )
        
        response = await llm.ainvoke([system_prompt, HumanMessage(content=user_message[:200])])
        title = response.content.strip()
        # Strip any "title:" prefix case-insensitively if generated
        if title.lower().startswith("title:"):
            title = title[6:].strip()
        title = title.replace('"', '').replace("'", "")
        if len(title) > 45:
            title = title[:42] + "..."
        return title or user_message[:40]
    except Exception as e:
        print(f"⚠️ [WARNING] Failed to generate title from LLM: {e}")
        return user_message[:40] + ("..." if len(user_message) > 40 else "")


async def register_thread(
    async_pool: AsyncConnectionPool, thread_id: str, user_message: str, owner_id: str
) -> tuple[bool, bool]:
    """Inserts the thread's metadata row with a fallback title, or checks its owner.

    Core: every checkpoint table has a foreign key to thread_metadata
    (setup_database_tables), so this row must exist before any checkpoint
    write. Makes no model call.

    Returns (owned, created). owned is True when the thread belongs to owner_id
    (newly created or already owned), False when another owner, or no owner,
    holds it. created is True only when this call inserted the row.
    """
    async with async_pool.connection() as conn:
        async with conn.cursor() as cur:
            # Write an optimistic title first to avoid blocking stream startup
            title = user_message[:40] + ("..." if len(user_message) > 40 else "")
            await cur.execute(
                """
                INSERT INTO thread_metadata (thread_id, title, owner_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (thread_id) DO NOTHING
                RETURNING thread_id
                """,
                (thread_id, title, owner_id),
            )
            if not await cur.fetchone():
                # The row already existed: re-read its owner instead of trusting the caller
                await cur.execute(
                    "SELECT owner_id FROM thread_metadata WHERE thread_id = %s", (thread_id,)
                )
                row = await cur.fetchone()
                return (row is not None and row[0] == owner_id), False
            return True, True


# The event loop keeps only a weak reference to a task, so a running title task
# is held here until it finishes
_title_tasks: set[asyncio.Task] = set()


def start_title_generation(async_pool: AsyncConnectionPool, thread_id: str, user_message: str) -> None:
    """Replaces the fallback title of a new thread with a model-made one, in the background.

    Optional: never raises, so a failure here cannot block or fail a chat turn.
    """
    coro = None
    try:
        # Kick off background LLM call to update it to a meaningful title
        async def update_title_bg():
            try:
                clean_title = await generate_title_from_llm(user_message)
                async with async_pool.connection() as conn_bg:
                    async with conn_bg.cursor() as cur_bg:
                        await cur_bg.execute(
                            "UPDATE thread_metadata SET title = %s WHERE thread_id = %s",
                            (clean_title, thread_id),
                        )
            except Exception as e:
                print(f"⚠️ [WARNING] Background title update failed: {e}")

        coro = update_title_bg()
        task = asyncio.create_task(coro)
        coro = None
        _title_tasks.add(task)
        task.add_done_callback(_title_tasks.discard)
    except Exception as e:
        # A coroutine that never became a task is closed, so it is not left unawaited
        if coro is not None:
            coro.close()
        print(f"⚠️ [WARNING] Background title update could not start: {e}")


async def get_thread_owner(async_pool: AsyncConnectionPool, thread_id: str) -> tuple[bool, str | None]:
    """Returns (exists, owner_id) for a thread's metadata row."""
    async with async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT owner_id FROM thread_metadata WHERE thread_id = %s", (thread_id,)
            )
            row = await cur.fetchone()
            return (row is not None, row[0] if row else None)


async def get_all_threads_history(async_pool: AsyncConnectionPool, owner_id: str, limit: int = 20, offset: int = 0):
    """Fetches a paginated list of the owner's thread IDs with their titles."""
    async with async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT m.thread_id, COALESCE(m.title, m.thread_id) as title
                FROM thread_metadata m
                WHERE m.owner_id = %s
                  AND EXISTS (SELECT 1 FROM checkpoints c WHERE c.thread_id = m.thread_id)
                ORDER BY m.created_at DESC NULLS LAST, m.thread_id DESC
                LIMIT %s OFFSET %s;
                """,
                (owner_id, limit, offset)
            )
            rows = await cur.fetchall()
            return [{"id": row[0], "title": row[1]} for row in rows]



async def delete_thread_from_db(async_pool: AsyncConnectionPool, thread_id: str, owner_id: str) -> bool:
    """Safely deletes thread metadata. PostgreSQL ON DELETE CASCADE handles LangGraph tables automatically.

    Deletes only a thread owned by owner_id; returns False when nothing matched.
    """
    async with async_pool.connection() as conn:
        async with conn.cursor() as cur:
            # We only need to delete the parent record now
            await cur.execute(
                "DELETE FROM thread_metadata WHERE thread_id = %s AND owner_id = %s;",
                (thread_id, owner_id),
            )
            return cur.rowcount > 0