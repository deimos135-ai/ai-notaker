import aiosqlite
from datetime import datetime, timedelta

DB_PATH = "messages.db"

async def save_message(message):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                chat_id INTEGER,
                user TEXT,
                text TEXT,
                timestamp TEXT
            )
        """)
        await db.execute(
            "INSERT INTO messages (chat_id, user, text, timestamp) VALUES (?, ?, ?, ?)",
            (message.chat.id, message.from_user.full_name, message.text, datetime.utcnow().isoformat())
        )
        await db.commit()

async def get_messages_last_week():
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user, text FROM messages WHERE timestamp >= ?", (one_week_ago.isoformat(),)
        )
        rows = await cursor.fetchall()
        return [{"user": row[0], "text": row[1]} for row in rows]
