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
        
        response = await llm.ainvoke([system_prompt, HumanMessage(content=user_message)])
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
                # Write an optimistic title first to avoid blocking stream startup
                title = user_message[:40] + ("..." if len(user_message) > 40 else "")
                await cur.execute(
                    "INSERT INTO thread_metadata (thread_id, title) VALUES (%s, %s)",
                    (thread_id, title),
                )
                
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

                asyncio.create_task(update_title_bg())


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